#!/usr/bin/env bash
set -euo pipefail
ARTIFACT_ID=9479335485
ROOT=/tmp/v652-cron-lock-diagnostic
WP=$ROOT/wp
ART=$ROOT/artifact
rm -rf "$ROOT"; mkdir -p "$ART"
gh api "repos/${GITHUB_REPOSITORY}/actions/artifacts/${ARTIFACT_ID}/zip" > "$ROOT/artifact.zip"
unzip -q "$ROOT/artifact.zip" -d "$ART"
SRC=$(find "$ART" -type d -path '*/BLOCKED_DIAGNOSTIC_V12/affiliate-portal-router' -print -quit)
[ -n "$SRC" ] || { echo 'BLOCKED: source missing from blocked artifact'; exit 1; }
setup_wp(){
  rm -rf "$WP"; mkdir -p "$WP"
  wp core download --version=7.0.1 --path="$WP" --force --allow-root >/dev/null
  wp config create --path="$WP" --dbname=v651gate --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --skip-check --allow-root >/dev/null
  wp db reset --yes --path="$WP" --allow-root >/dev/null
  wp core install --path="$WP" --url=http://v652.test --title='V652 Lock Diagnostic' --admin_user=gateadmin --admin_password='GateOnly-20260822!' --admin_email=gate@example.invalid --skip-email --allow-root >/dev/null
  rm -rf "$WP/wp-content/plugins/affiliate-portal-router"; cp -a "$SRC" "$WP/wp-content/plugins/affiliate-portal-router"
  wp plugin activate affiliate-portal-router --path="$WP" --allow-root >/dev/null
  wp option update home http://127.0.0.1:8101 --path="$WP" --allow-root >/dev/null
  wp option update siteurl http://127.0.0.1:8101 --path="$WP" --allow-root >/dev/null
  mkdir -p "$WP/wp-content/mu-plugins"
  cat > "$WP/wp-content/mu-plugins/v652-lock-probe.php" <<'PHP'
<?php
add_action('plugins_loaded', function(){
    if (!class_exists('Pferdeportal_Affiliate_Router')) { return; }
    $p=Pferdeportal_Affiliate_Router::instance();
    remove_action(Pferdeportal_Affiliate_Router::EBAY_WORKER_HOOK, array($p,'run_ebay_canonical_worker'));
    add_action(Pferdeportal_Affiliate_Router::EBAY_WORKER_HOOK, function() use ($p){
        $n=absint(get_option('v652_lock_probe_count',0))+1;
        update_option('v652_lock_probe_count',$n,false);
        if($n>=3){
            $r=get_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,array());
            $r['status']='completed';$r['phase']='complete';$r['finished_at']=time();$r['owner']='';$r['lease_expires_at']=0;
            update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,$r,false); return;
        }
        $m=new ReflectionMethod($p,'ebay_run_schedule_worker');$m->setAccessible(true);$m->invoke($p,0);
    },-100);
},1000);
add_action('init', function(){
    if ((string)($_GET['v652_lock_seed'] ?? '') !== '1') { return; }
    $p=Pferdeportal_Affiliate_Router::instance();
    wp_clear_scheduled_hook(Pferdeportal_Affiliate_Router::EBAY_WORKER_HOOK);
    update_option('v652_lock_probe_count',0,false);
    $run=array('schema'=>'1.0','build'=>Pferdeportal_Affiliate_Router::EBAY_RUNTIME_BUILD,'run_uuid'=>'v652-lock-probe','status'=>'running','phase'=>'transport_probe','started_at'=>time(),'updated_at'=>time(),'finished_at'=>0,'owner'=>'','lease_expires_at'=>0,'worker_transport'=>'wp_cron','resume_at'=>0,'checkpoint_candidate'=>array('business_campaign_ids'=>array(),'private_listing_ids'=>array()),'phase_state'=>array(),'coverage'=>array(),'gapfill'=>array('attempts'=>0,'missing'=>array()),'errors'=>array());
    update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,$run,false);
    $pre=(string)get_transient('doing_cron'); update_option('v652_lock_pre',$pre,false);
    $m=new ReflectionMethod($p,'ebay_run_schedule_worker');$m->setAccessible(true);
    $ok=$m->invoke($p,0);
    add_action('shutdown', function(){
        $next=wp_next_scheduled(Pferdeportal_Affiliate_Router::EBAY_WORKER_HOOK);
        $lock=(string)get_transient('doing_cron');
        file_put_contents('/tmp/v652-lock-shutdown.log',json_encode(array('next'=>$next,'lock'=>$lock,'count'=>get_option('v652_lock_probe_count',0)))."\n",FILE_APPEND);
    },PHP_INT_MAX);
    echo $ok ? "SEEDED\n" : "SCHEDULE_FAIL\n"; exit;
},PHP_INT_MAX);
PHP
}
run_scenario(){ local name="$1" lockmode="$2"; local out="$ROOT/$name"; mkdir -p "$out"; rm -f /tmp/v652-lock-shutdown.log
  if [ "$lockmode" = clean ]; then wp transient delete doing_cron --path="$WP" --allow-root >/dev/null 2>&1 || true; else wp eval 'set_transient("doing_cron",sprintf("%.22F",microtime(true)),60);' --path="$WP" --allow-root >/dev/null; fi
  wp transient get doing_cron --path="$WP" --allow-root > "$out/lock_before.txt" 2>&1 || true
  php -S 127.0.0.1:8101 -t "$WP" > "$out/server.log" 2>&1 & local spid=$!; sleep 1
  curl --fail --silent --show-error 'http://127.0.0.1:8101/?v652_lock_seed=1' > "$out/seed.txt"
  local count=0; for i in $(seq 1 40); do count=$(wp db query "SELECT option_value FROM wp_options WHERE option_name='v652_lock_probe_count' LIMIT 1;" --skip-column-names --path="$WP" --allow-root 2>/dev/null | tr -d '\r\n ' || true); [ "$count" = 3 ] && break; sleep 0.25; done
  echo "$count" > "$out/final_count.txt"; cp /tmp/v652-lock-shutdown.log "$out/shutdown.log" 2>/dev/null || true
  wp option get v652_lock_pre --path="$WP" --allow-root > "$out/pre_seen.txt" 2>&1 || true
  wp transient get doing_cron --path="$WP" --allow-root > "$out/lock_after.txt" 2>&1 || true
  kill "$spid" 2>/dev/null || true; wait "$spid" 2>/dev/null || true
}
setup_wp; run_scenario clean clean
setup_wp; run_scenario active_lock active
printf '%s\n' '=== CLEAN ==='; cat "$ROOT/clean/final_count.txt" "$ROOT/clean/pre_seen.txt" "$ROOT/clean/shutdown.log" "$ROOT/clean/server.log"
printf '%s\n' '=== ACTIVE LOCK ==='; cat "$ROOT/active_lock/final_count.txt" "$ROOT/active_lock/pre_seen.txt" "$ROOT/active_lock/shutdown.log" "$ROOT/active_lock/server.log"
[ "$(cat "$ROOT/clean/final_count.txt")" = 3 ] || { echo 'DIAG_FAIL: clean dispatch did not self-pump'; exit 1; }
[ "$(cat "$ROOT/active_lock/final_count.txt")" = 0 ] || { echo 'DIAG_FAIL: expected active-lock reproduction did not stay blocked'; exit 1; }
grep -q '"next":[1-9]' "$ROOT/active_lock/shutdown.log" || { echo 'DIAG_FAIL: active-lock event was not left scheduled'; exit 1; }
echo 'ROOTCAUSE_REPRODUCED=ACTIVE_DOING_CRON_LOCK_CAUSES_FALSE_SUCCESS_AND_STRANDED_DUE_EVENT'
