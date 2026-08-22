#!/usr/bin/env bash
set -euo pipefail
# Immutable counterproof against the pre-fix V6.52 patch01 artifact.
ARTIFACT_ID=9480472444
ROOT=/tmp/v652-orphan-lock-liveness
ART=$ROOT/artifact
rm -rf "$ROOT"; mkdir -p "$ART"
gh api "repos/${GITHUB_REPOSITORY}/actions/artifacts/${ARTIFACT_ID}/zip" > "$ROOT/artifact.zip"
unzip -q "$ROOT/artifact.zip" -d "$ART"
SRC=$(find "$ART" -type d -path '*/BLOCKED_DIAGNOSTIC_V12/affiliate-portal-router' -print -quit)
[ -n "$SRC" ] || { echo 'BLOCKED: source missing'; exit 1; }

run_case(){
  local ver="$1"
  local port="$2"
  local tag="${ver//./_}"
  local WP="$ROOT/wp-$tag"
  local OUT="$ROOT/out-$tag"
  rm -rf "$WP" "$OUT"; mkdir -p "$WP" "$OUT"
  wp core download --version="$ver" --path="$WP" --force --allow-root >/dev/null
  wp config create --path="$WP" --dbname=v651gate --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --skip-check --allow-root >/dev/null
  wp db reset --yes --path="$WP" --allow-root >/dev/null
  wp core install --path="$WP" --url="http://127.0.0.1:$port" --title='V652 Orphan Lock' --admin_user=a --admin_password='GateOnly-20260822!' --admin_email=a@example.invalid --skip-email --allow-root >/dev/null
  wp config set DISABLE_WP_CRON true --raw --path="$WP" --allow-root >/dev/null
  wp transient delete doing_cron --path="$WP" --allow-root >/dev/null 2>&1 || true
  rm -rf "$WP/wp-content/plugins/affiliate-portal-router"; cp -a "$SRC" "$WP/wp-content/plugins/affiliate-portal-router"
  wp plugin activate affiliate-portal-router --path="$WP" --allow-root >/dev/null
  wp option update home "http://127.0.0.1:$port" --path="$WP" --allow-root >/dev/null
  wp option update siteurl "http://127.0.0.1:$port" --path="$WP" --allow-root >/dev/null
  mkdir -p "$WP/wp-content/mu-plugins"
  cat > "$WP/wp-content/mu-plugins/v652-orphan-probe.php" <<'PHP'
<?php
add_action('plugins_loaded',function(){
 if(!class_exists('Pferdeportal_Affiliate_Router'))return; $p=Pferdeportal_Affiliate_Router::instance();
 remove_action(Pferdeportal_Affiliate_Router::EBAY_WORKER_HOOK,array($p,'run_ebay_canonical_worker'));
 add_action(Pferdeportal_Affiliate_Router::EBAY_WORKER_HOOK,function()use($p){
  $n=absint(get_option('v652_orphan_count',0))+1; update_option('v652_orphan_count',$n,false);
  $r=get_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,[]);$r['status']='completed';$r['phase']='complete';$r['finished_at']=time();$r['owner']='';$r['lease_expires_at']=0;update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,$r,false);
 },-100);
},1000);
add_action('init',function(){
 if(($_GET['v652_orphan_seed']??'')!=='1')return; $p=Pferdeportal_Affiliate_Router::instance();
 wp_clear_scheduled_hook(Pferdeportal_Affiliate_Router::EBAY_WORKER_HOOK); update_option('v652_orphan_count',0,false);
 $run=['schema'=>'1.0','build'=>Pferdeportal_Affiliate_Router::EBAY_RUNTIME_BUILD,'run_uuid'=>'v652-orphan-probe','status'=>'running','phase'=>'transport_probe','started_at'=>time(),'updated_at'=>time(),'finished_at'=>0,'owner'=>'','lease_expires_at'=>0,'worker_transport'=>'wp_cron','resume_at'=>0,'checkpoint_candidate'=>['business_campaign_ids'=>[],'private_listing_ids'=>[]],'phase_state'=>[],'coverage'=>[],'gapfill'=>['attempts'=>0,'missing'=>[]],'errors'=>[]];
 update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,$run,false);
 set_transient('doing_cron',sprintf('%.22F',microtime(true)),60);
 $m=new ReflectionMethod($p,'ebay_run_schedule_worker');$m->setAccessible(true);$ok=$m->invoke($p,0);
 echo $ok?"ORPHAN_SEEDED\n":"SCHEDULE_FAIL\n"; exit;
},PHP_INT_MAX);
PHP
  python3 - "$WP/wp-config.php" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); lines=p.read_text().splitlines(); lines=[x for x in lines if 'DISABLE_WP_CRON' not in x]; p.write_text('\n'.join(lines)+'\n')
PY
  PHP_CLI_SERVER_WORKERS=4 php -S "127.0.0.1:$port" -t "$WP" > "$OUT/server.log" 2>&1 & local SP=$!
  sleep 1
  curl --fail --silent --show-error "http://127.0.0.1:$port/?v652_orphan_seed=1" > "$OUT/seed.txt"
  grep -Fxq ORPHAN_SEEDED "$OUT/seed.txt"
  sleep 4
  local count; count=$(wp db query "SELECT option_value FROM wp_options WHERE option_name='v652_orphan_count' LIMIT 1;" --skip-column-names --path="$WP" --allow-root 2>/dev/null|tr -d '\r\n '||true)
  local status; status=$(wp db query "SELECT option_value FROM wp_options WHERE option_name='ppar_ebay_run_state_v1' LIMIT 1;" --skip-column-names --path="$WP" --allow-root 2>/dev/null||true)
  local cron_hits; cron_hits=$(grep -c 'POST /wp-cron.php' "$OUT/server.log"||true)
  echo "WP=$ver COUNT=$count CRON_HITS=$cron_hits"
  echo "$status" > "$OUT/run-serialized.txt"
  kill "$SP" 2>/dev/null || true; pkill -P "$SP" 2>/dev/null || true; wait "$SP" 2>/dev/null || true
  [ "$count" = 0 ] || { echo "COUNTERPROOF_UNEXPECTED_TICK_WP_${tag}"; return 1; }
  [ "$cron_hits" = 0 ] || { echo "COUNTERPROOF_UNEXPECTED_CRON_WP_${tag}"; return 1; }
  echo "PRE_FIX_ORPHAN_LOCK_STALL_WP_${tag}=EXPECTED_RED_CONFIRMED"
}

run_case 6.8.3 8141
run_case 7.0.1 8142
echo 'PRE_FIX_ORPHAN_LOCK_COUNTERPROOF=PASS'
