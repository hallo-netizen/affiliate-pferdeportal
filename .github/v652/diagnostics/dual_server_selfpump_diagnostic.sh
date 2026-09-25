#!/usr/bin/env bash
set -euo pipefail
ARTIFACT_ID=9479335485
ROOT=/tmp/v652-dual-selfpump
WP=$ROOT/wp
ART=$ROOT/artifact
rm -rf "$ROOT"; mkdir -p "$ART"
gh api "repos/${GITHUB_REPOSITORY}/actions/artifacts/${ARTIFACT_ID}/zip" > "$ROOT/artifact.zip"
unzip -q "$ROOT/artifact.zip" -d "$ART"
SRC=$(find "$ART" -type d -path '*/BLOCKED_DIAGNOSTIC_V12/affiliate-portal-router' -print -quit)
[ -n "$SRC" ] || { echo 'BLOCKED: source missing from blocked artifact'; exit 1; }
rm -rf "$WP"; mkdir -p "$WP"
wp core download --version=7.0.1 --path="$WP" --force --allow-root >/dev/null
wp config create --path="$WP" --dbname=v651gate --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --skip-check --allow-root >/dev/null
wp db reset --yes --path="$WP" --allow-root >/dev/null
wp core install --path="$WP" --url=http://127.0.0.1:8101 --title='V652 Dual Server Diagnostic' --admin_user=gateadmin --admin_password='GateOnly-20260822!' --admin_email=gate@example.invalid --skip-email --allow-root >/dev/null
rm -rf "$WP/wp-content/plugins/affiliate-portal-router"; cp -a "$SRC" "$WP/wp-content/plugins/affiliate-portal-router"
wp plugin activate affiliate-portal-router --path="$WP" --allow-root >/dev/null
# Browser/start traffic lands on 8101; all WordPress-generated loopbacks go to an independent PHP worker on 8102.
wp option update home http://127.0.0.1:8101 --path="$WP" --allow-root >/dev/null
wp option update siteurl http://127.0.0.1:8102 --path="$WP" --allow-root >/dev/null
wp transient delete doing_cron --path="$WP" --allow-root >/dev/null 2>&1 || true
mkdir -p "$WP/wp-content/mu-plugins"
cat > "$WP/wp-content/mu-plugins/v652-dual-probe.php" <<'PHP'
<?php
add_action('plugins_loaded', function(){
    if (!class_exists('Pferdeportal_Affiliate_Router')) { return; }
    $p=Pferdeportal_Affiliate_Router::instance();
    remove_action(Pferdeportal_Affiliate_Router::EBAY_WORKER_HOOK, array($p,'run_ebay_canonical_worker'));
    add_action(Pferdeportal_Affiliate_Router::EBAY_WORKER_HOOK, function() use ($p){
        $n=absint(get_option('v652_dual_probe_count',0))+1;
        update_option('v652_dual_probe_count',$n,false);
        file_put_contents('/tmp/v652-dual-ticks.log',json_encode(array('n'=>$n,'at'=>microtime(true),'lock'=>(string)get_transient('doing_cron')))."\n",FILE_APPEND);
        if($n>=3){
            $r=get_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,array());
            $r['status']='completed';$r['phase']='complete';$r['finished_at']=time();$r['owner']='';$r['lease_expires_at']=0;
            update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,$r,false); return;
        }
        $m=new ReflectionMethod($p,'ebay_run_schedule_worker');$m->setAccessible(true);$m->invoke($p,0);
    },-100);
},1000);
add_action('init', function(){
    if ((string)($_GET['v652_dual_seed'] ?? '') !== '1') { return; }
    $p=Pferdeportal_Affiliate_Router::instance();
    wp_clear_scheduled_hook(Pferdeportal_Affiliate_Router::EBAY_WORKER_HOOK);
    update_option('v652_dual_probe_count',0,false);
    $run=array('schema'=>'1.0','build'=>Pferdeportal_Affiliate_Router::EBAY_RUNTIME_BUILD,'run_uuid'=>'v652-dual-probe','status'=>'running','phase'=>'transport_probe','started_at'=>time(),'updated_at'=>time(),'finished_at'=>0,'owner'=>'','lease_expires_at'=>0,'worker_transport'=>'wp_cron','resume_at'=>0,'checkpoint_candidate'=>array('business_campaign_ids'=>array(),'private_listing_ids'=>array()),'phase_state'=>array(),'coverage'=>array(),'gapfill'=>array('attempts'=>0,'missing'=>array()),'errors'=>array());
    update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,$run,false);
    update_option('v652_dual_pre_lock',(string)get_transient('doing_cron'),false);
    $m=new ReflectionMethod($p,'ebay_run_schedule_worker');$m->setAccessible(true);
    $ok=$m->invoke($p,0);
    echo $ok ? "DUAL_SEEDED\n" : "SCHEDULE_FAIL\n"; exit;
},PHP_INT_MAX);
PHP
rm -f /tmp/v652-dual-ticks.log
php -S 127.0.0.1:8102 -t "$WP" > "$ROOT/loopback.log" 2>&1 & P2=$!
php -S 127.0.0.1:8101 -t "$WP" > "$ROOT/browser.log" 2>&1 & P1=$!
trap 'kill "$P1" "$P2" 2>/dev/null || true' EXIT
sleep 1
curl --fail --silent --show-error 'http://127.0.0.1:8101/?v652_dual_seed=1' > "$ROOT/seed.txt"
grep -Fxq DUAL_SEEDED "$ROOT/seed.txt"
count=0
for i in $(seq 1 80); do
  count=$(wp db query "SELECT option_value FROM wp_options WHERE option_name='v652_dual_probe_count' LIMIT 1;" --skip-column-names --path="$WP" --allow-root 2>/dev/null | tr -d '\r\n ' || true)
  [ "$count" = 3 ] && break
  sleep 0.25
done
wp option get v652_dual_pre_lock --path="$WP" --allow-root > "$ROOT/pre_lock.txt" 2>&1 || true
printf 'COUNT=%s\n' "$count"
printf '%s\n' '=== PRE LOCK ==='; cat "$ROOT/pre_lock.txt"
printf '%s\n' '=== TICKS ==='; cat /tmp/v652-dual-ticks.log 2>/dev/null || true
printf '%s\n' '=== BROWSER SERVER ==='; cat "$ROOT/browser.log"
printf '%s\n' '=== LOOPBACK SERVER ==='; cat "$ROOT/loopback.log"
[ "$count" = 3 ] || { echo 'DUAL_SERVER_SELFPUMP=FAIL'; exit 1; }
cron_hits=$(grep -c 'POST /wp-cron.php' "$ROOT/loopback.log" || true)
[ "$cron_hits" -ge 3 ] || { echo "DUAL_SERVER_CRON_HITS=$cron_hits"; exit 1; }
extra_browser=$(grep -E ' (GET|POST) /' "$ROOT/browser.log" | grep -v 'GET /?v652_dual_seed=1' | wc -l | tr -d ' ' || true)
[ "$extra_browser" -eq 0 ] || { echo "UNEXPECTED_BROWSER_HITS=$extra_browser"; exit 1; }
echo "DUAL_SERVER_SELFPUMP=PASS CRON_HITS=$cron_hits"
