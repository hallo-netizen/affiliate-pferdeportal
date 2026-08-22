#!/usr/bin/env bash
set -euo pipefail
ARTIFACT_ID=9479335485
ROOT=/tmp/v652-multiworker-selfpump; WP=$ROOT/wp; ART=$ROOT/artifact
rm -rf "$ROOT"; mkdir -p "$ART"
gh api "repos/${GITHUB_REPOSITORY}/actions/artifacts/${ARTIFACT_ID}/zip" > "$ROOT/artifact.zip"
unzip -q "$ROOT/artifact.zip" -d "$ART"
SRC=$(find "$ART" -type d -path '*/BLOCKED_DIAGNOSTIC_V12/affiliate-portal-router' -print -quit)
[ -n "$SRC" ] || { echo 'BLOCKED: source missing'; exit 1; }
mkdir -p "$WP"
wp core download --version=7.0.1 --path="$WP" --force --allow-root >/dev/null
wp config create --path="$WP" --dbname=v651gate --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --skip-check --allow-root >/dev/null
wp db reset --yes --path="$WP" --allow-root >/dev/null
wp core install --path="$WP" --url=http://127.0.0.1:8121 --title='V652 Multiworker' --admin_user=a --admin_password='GateOnly-20260822!' --admin_email=a@example.invalid --skip-email --allow-root >/dev/null
rm -rf "$WP/wp-content/plugins/affiliate-portal-router"; cp -a "$SRC" "$WP/wp-content/plugins/affiliate-portal-router"
wp plugin activate affiliate-portal-router --path="$WP" --allow-root >/dev/null
wp option update home http://127.0.0.1:8121 --path="$WP" --allow-root >/dev/null
wp option update siteurl http://127.0.0.1:8121 --path="$WP" --allow-root >/dev/null
wp transient delete doing_cron --path="$WP" --allow-root >/dev/null 2>&1 || true
mkdir -p "$WP/wp-content/mu-plugins"
cat > "$WP/wp-content/mu-plugins/v652-multi-probe.php" <<'PHP'
<?php
add_action('plugins_loaded',function(){
 if(!class_exists('Pferdeportal_Affiliate_Router'))return; $p=Pferdeportal_Affiliate_Router::instance();
 remove_action(Pferdeportal_Affiliate_Router::EBAY_WORKER_HOOK,array($p,'run_ebay_canonical_worker'));
 add_action(Pferdeportal_Affiliate_Router::EBAY_WORKER_HOOK,function()use($p){
  $n=absint(get_option('v652_multi_count',0))+1; update_option('v652_multi_count',$n,false);
  file_put_contents('/tmp/v652-multi-ticks.log',json_encode(['n'=>$n,'pid'=>getmypid(),'lock'=>(string)get_transient('doing_cron'),'at'=>microtime(true)])."\n",FILE_APPEND);
  if($n>=3){$r=get_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,[]);$r['status']='completed';$r['phase']='complete';$r['finished_at']=time();$r['owner']='';$r['lease_expires_at']=0;update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,$r,false);return;}
  $m=new ReflectionMethod($p,'ebay_run_schedule_worker');$m->setAccessible(true);$m->invoke($p,0);
 },-100);
},1000);
add_action('init',function(){
 if(($_GET['v652_multi_seed']??'')!=='1')return; $p=Pferdeportal_Affiliate_Router::instance();
 wp_clear_scheduled_hook(Pferdeportal_Affiliate_Router::EBAY_WORKER_HOOK); update_option('v652_multi_count',0,false);
 $run=['schema'=>'1.0','build'=>Pferdeportal_Affiliate_Router::EBAY_RUNTIME_BUILD,'run_uuid'=>'v652-multi-probe','status'=>'running','phase'=>'transport_probe','started_at'=>time(),'updated_at'=>time(),'finished_at'=>0,'owner'=>'','lease_expires_at'=>0,'worker_transport'=>'wp_cron','resume_at'=>0,'checkpoint_candidate'=>['business_campaign_ids'=>[],'private_listing_ids'=>[]],'phase_state'=>[],'coverage'=>[],'gapfill'=>['attempts'=>0,'missing'=>[]],'errors'=>[]];
 update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,$run,false); update_option('v652_multi_pre_lock',(string)get_transient('doing_cron'),false);
 $m=new ReflectionMethod($p,'ebay_run_schedule_worker');$m->setAccessible(true); $ok=$m->invoke($p,0); echo $ok?"MULTI_SEEDED\n":"SCHEDULE_FAIL\n"; exit;
},PHP_INT_MAX);
PHP
rm -f /tmp/v652-multi-ticks.log
PHP_CLI_SERVER_WORKERS=4 php -S 127.0.0.1:8121 -t "$WP" > "$ROOT/server.log" 2>&1 & SP=$!
trap 'kill "$SP" 2>/dev/null || true; pkill -P "$SP" 2>/dev/null || true' EXIT
sleep 1
curl --fail --silent --show-error 'http://127.0.0.1:8121/?v652_multi_seed=1' > "$ROOT/seed.txt"
grep -Fxq MULTI_SEEDED "$ROOT/seed.txt"
count=0
for i in $(seq 1 100); do count=$(wp db query "SELECT option_value FROM wp_options WHERE option_name='v652_multi_count' LIMIT 1;" --skip-column-names --path="$WP" --allow-root 2>/dev/null|tr -d '\r\n '||true); [ "$count" = 3 ]&&break; sleep .25; done
pre=$(wp option get v652_multi_pre_lock --path="$WP" --allow-root 2>/dev/null||true)
echo "COUNT=$count PRE_LOCK=$pre"
echo '=== TICKS ==='; cat /tmp/v652-multi-ticks.log 2>/dev/null||true
echo '=== SERVER ==='; cat "$ROOT/server.log"
[ "$count" = 3 ] || { echo 'MULTIWORKER_CORE_CRON_SELFPUMP=FAIL'; exit 1; }
cron_hits=$(grep -c 'POST /wp-cron.php' "$ROOT/server.log"||true); [ "$cron_hits" -ge 3 ] || { echo "CRON_HITS=$cron_hits"; exit 1; }
seed_hits=$(grep -c 'GET /?v652_multi_seed=1' "$ROOT/server.log"||true); [ "$seed_hits" -eq 1 ] || exit 1
extra=$(grep -E ' (GET|POST) /' "$ROOT/server.log"|grep -v 'GET /?v652_multi_seed=1'|grep -v 'POST /wp-cron.php'|wc -l|tr -d ' '||true); [ "$extra" -eq 0 ]||{ echo "EXTRA=$extra";exit 1; }
echo "MULTIWORKER_CORE_CRON_SELFPUMP=PASS CRON_HITS=$cron_hits"
