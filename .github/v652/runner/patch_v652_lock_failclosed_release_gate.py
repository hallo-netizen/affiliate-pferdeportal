from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
old="""[ \"$(git hash-object \"$WORK/.github/v652/patches/01_core_cron_selfpump_rootfix.patch\")\" = \"0e85087deca8875b244e466126e8fe5ffcf7ca49\" ] || block \"V6.52 production rootfix patch blob mismatch\"\n[ \"$(git hash-object \"$WORK/.github/v652/manifests/STEP1_SOURCE_SHA256.txt\")\" = \"476f1146ba563ce4b93429bdef90f69da12e5778\" ] || block \"V6.52 step1 manifest blob mismatch\"\n[ \"$(git hash-object \"$WORK/.github/v652/tests/test_background_selfpump_v652.php\")\" = \"28bf164355b678ce5920ffd7e7056904fba61030\" ] || block \"V6.52 background self-pump test blob mismatch\"\n(cd \"$SRC\" && patch -p1 --forward --batch < \"$WORK/.github/v652/patches/01_core_cron_selfpump_rootfix.patch\") > \"$E/12d_apply_v652_core_cron_selfpump.log\" 2>&1 || block \"V6.52 core-cron self-pump rootfix patch failed\"\n(cd \"$SRC\" && sha256sum -c \"$WORK/.github/v652/manifests/STEP1_SOURCE_SHA256.txt\") > \"$E/12e_v652_step1_source_manifest.log\" 2>&1 || block \"V6.52 step1 source manifest mismatch\"\n"""
new="""[ \"$(git hash-object \"$WORK/.github/v652/patches/01_core_cron_selfpump_rootfix.patch\")\" = \"0e85087deca8875b244e466126e8fe5ffcf7ca49\" ] || block \"V6.52 production rootfix patch blob mismatch\"\n[ \"$(git hash-object \"$WORK/.github/v652/patches/02_core_cron_lock_failclosed_rootfix.patch\")\" = \"ca0402ab565e98985c88a3a9ec1cd809fc280527\" ] || block \"V6.52 Cron-lock fail-closed rootfix patch blob mismatch\"\n[ \"$(git hash-object \"$WORK/.github/v652/manifests/STEP1_SOURCE_SHA256.txt\")\" = \"74d786b5fade9fb3ff454fd606b4ee6081d1d52f\" ] || block \"V6.52 step1 manifest blob mismatch\"\n[ \"$(git hash-object \"$WORK/.github/v652/tests/test_background_selfpump_v652.php\")\" = \"6b552feb1d38d80a5265bae6642fa073417a3bf6\" ] || block \"V6.52 background self-pump test blob mismatch\"\n(cd \"$SRC\" && patch -p1 --forward --batch < \"$WORK/.github/v652/patches/01_core_cron_selfpump_rootfix.patch\") > \"$E/12d_apply_v652_core_cron_selfpump.log\" 2>&1 || block \"V6.52 core-cron self-pump rootfix patch failed\"\n(cd \"$SRC\" && patch -p1 --forward --batch < \"$WORK/.github/v652/patches/02_core_cron_lock_failclosed_rootfix.patch\") > \"$E/12d2_apply_v652_cron_lock_failclosed.log\" 2>&1 || block \"V6.52 Cron-lock fail-closed rootfix patch failed\"\n(cd \"$SRC\" && sha256sum -c \"$WORK/.github/v652/manifests/STEP1_SOURCE_SHA256.txt\") > \"$E/12e_v652_step1_source_manifest.log\" 2>&1 || block \"V6.52 step1 source manifest mismatch\"\n"""
if s.count(old)!=1: raise SystemExit('BLOCKED: V6.52 production/materialization anchor mismatch')
s=s.replace(old,new,1)
s=s.replace("ASSERTIONS=16 FAIL=0", "ASSERTIONS=22 FAIL=0")
s=s.replace("ASSERTIONS=19 FAIL=0", "ASSERTIONS=25 FAIL=0")
old_setup='setup_wp(){ rm -rf "$WP"; mkdir -p "$WP"; wp core download --version=7.0.1 --path="$WP" --force --allow-root >/dev/null;'
new_setup='setup_wp(){ local core_version="${1:-7.0.1}"; rm -rf "$WP"; mkdir -p "$WP"; wp core download --version="$core_version" --path="$WP" --force --allow-root >/dev/null;'
if s.count(old_setup)!=1: raise SystemExit('BLOCKED: setup_wp anchor mismatch')
s=s.replace(old_setup,new_setup,1)
start=s.index('background_selfpump_gate(){')
end=s.index('\nreal_gate "$SRC" step1', start)
block=s[start:end]
old_head='background_selfpump_gate(){ local src="$1" p="$2" out="$E/$p/V652_BACKGROUND_SELFPUMP"; mkdir -p "$out"; setup_wp'
new_head='background_selfpump_gate(){ local src="$1" p="$2" core_version="${3:-7.0.1}" port="${4:-8099}" tag="${core_version//./_}" out="$E/$p/V652_BACKGROUND_SELFPUMP_$tag"; mkdir -p "$out"; setup_wp "$core_version"'
if block.count(old_head)!=1: raise SystemExit('BLOCKED: selfpump head anchor mismatch')
block=block.replace(old_head,new_head,1)
block=block.replace('http://127.0.0.1:8099', 'http://127.0.0.1:$port')
block=block.replace('php -S 127.0.0.1:8099', 'php -S "127.0.0.1:$port"')
block=block.replace("curl --fail --silent --show-error 'http://127.0.0.1:$port/?v652_selfpump_seed=1'", 'curl --fail --silent --show-error "http://127.0.0.1:$port/?v652_selfpump_seed=1"')
old_result="printf 'AUTONOMOUS_CORE_CRON_CHAIN=PASS\\nSEED_HTTP_REQUESTS=%s\\nPROBE_TICKS=3\\nHTTP_WP_CRON_REQUESTS=%s\\nNO_BROWSER_OR_APP_REQUEST_AFTER_SEED=PASS\\nSAFE_CHECKPOINT_PRESERVED=PASS\\n' \"$seed_hits\" \"$cron_hits\" > \"$out/RESULT.txt\""
new_result="printf 'AUTONOMOUS_CORE_CRON_CHAIN=PASS\\nWORDPRESS_VERSION=%s\\nSEED_HTTP_REQUESTS=%s\\nPROBE_TICKS=3\\nHTTP_WP_CRON_REQUESTS=%s\\nNO_BROWSER_OR_APP_REQUEST_AFTER_SEED=PASS\\nSAFE_CHECKPOINT_PRESERVED=PASS\\n' \"$core_version\" \"$seed_hits\" \"$cron_hits\" > \"$out/RESULT.txt\""
if block.count(old_result)!=1: raise SystemExit('BLOCKED: selfpump result anchor mismatch')
block=block.replace(old_result,new_result,1)
s=s[:start]+block+s[end:]
old_call=' background_selfpump_gate "$src" "$p" || return 1\n echo REAL_GATE=PASS > "$E/$p/RESULT.txt"'
new_call=' background_selfpump_gate "$src" "$p" 7.0.1 8099 || return 1\n background_selfpump_gate "$src" "$p" 6.8.3 8098 || return 1\n background_lock_failclosed_gate "$src" "$p" 7.0.1 8101 || return 1\n background_lock_failclosed_gate "$src" "$p" 6.8.3 8100 || return 1\n echo REAL_GATE=PASS > "$E/$p/RESULT.txt"'
if s.count(old_call)!=1: raise SystemExit('BLOCKED: real gate selfpump call anchor mismatch')
s=s.replace(old_call,new_call,1)
neg=r'''

background_lock_failclosed_gate(){ local src="$1" p="$2" core_version="${3:-7.0.1}" port="${4:-8101}" tag="${core_version//./_}" out="$E/$p/V652_CRON_LOCK_FAILCLOSED_$tag"; mkdir -p "$out"; setup_wp "$core_version"
 wp config set DISABLE_WP_CRON true --raw --path="$WP" --allow-root >/dev/null || return 1
 wp transient delete doing_cron --path="$WP" --allow-root >/dev/null 2>&1 || true
 rm -rf "$WP/wp-content/plugins/affiliate-portal-router"; cp -a "$src" "$WP/wp-content/plugins/affiliate-portal-router"; wp plugin activate affiliate-portal-router --path="$WP" --allow-root >/dev/null || return 1
 wp option update home "http://127.0.0.1:$port" --path="$WP" --allow-root >/dev/null || return 1
 wp option update siteurl "http://127.0.0.1:$port" --path="$WP" --allow-root >/dev/null || return 1
 mkdir -p "$WP/wp-content/mu-plugins"
 cat > "$WP/wp-content/mu-plugins/v652-lock-failclosed-probe.php" <<'PHPV652LOCK'
<?php
add_action('init', function(){
    if ((string)($_GET['v652_lock_seed'] ?? '') !== '1') { return; }
    if (!class_exists('Pferdeportal_Affiliate_Router')) { status_header(500); echo "router missing\n"; exit; }
    $p=Pferdeportal_Affiliate_Router::instance();
    wp_clear_scheduled_hook(Pferdeportal_Affiliate_Router::EBAY_WORKER_HOOK);
    $save=new ReflectionMethod($p,'ebay_public_checkpoint_save');$save->setAccessible(true);
    $cp=$save->invoke($p,array('checkpoint_id'=>'v652-lock-safe','created_at'=>time(),'business_campaign_ids'=>array(11),'private_listing_ids'=>array(22),'verification'=>array('probe'=>1)));
    if(!is_array($cp)){ status_header(500); echo "checkpoint failed\n"; exit; }
    update_option('v652_lock_checkpoint_before',serialize($cp),false);
    $run=array('schema'=>'1.0','build'=>Pferdeportal_Affiliate_Router::EBAY_RUNTIME_BUILD,'run_uuid'=>'v652-lock-probe','status'=>'running','phase'=>'transport_probe','started_at'=>time(),'updated_at'=>time(),'finished_at'=>0,'owner'=>'','lease_expires_at'=>0,'worker_transport'=>'wp_cron','resume_at'=>0,'checkpoint_base_id'=>$cp['checkpoint_id'],'checkpoint_candidate'=>array('business_campaign_ids'=>array(11),'private_listing_ids'=>array(22)),'phase_state'=>array(),'coverage'=>array(),'gapfill'=>array('attempts'=>0,'missing'=>array()),'errors'=>array());
    update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,$run,false);
    set_transient('doing_cron',sprintf('%.22F',microtime(true)),60);
    $m=new ReflectionMethod($p,'ebay_run_schedule_worker');$m->setAccessible(true);
    if(!$m->invoke($p,0)){ status_header(500); echo "schedule failed\n"; exit; }
    echo "V652_LOCK_SEEDED\n";
    exit;
}, PHP_INT_MAX);
PHPV652LOCK
 python3 - "$WP/wp-config.php" <<'PYV652LOCKCFG'
from pathlib import Path
import sys
p=Path(sys.argv[1]); lines=p.read_text().splitlines(); lines=[ln for ln in lines if 'DISABLE_WP_CRON' not in ln]; p.write_text('\n'.join(lines)+'\n')
PYV652LOCKCFG
 PHP_CLI_SERVER_WORKERS=4 php -S "127.0.0.1:$port" -t "$WP" > "$out/server.log" 2>&1 & local spid=$!; sleep 1
 set +e; curl --max-time 15 --fail --silent --show-error "http://127.0.0.1:$port/?v652_lock_seed=1" > "$out/seed.log" 2>&1; local seed_rc=$?; set -e
 if [ "$seed_rc" -ne 0 ]; then kill "$spid" 2>/dev/null || true; pkill -P "$spid" 2>/dev/null || true; wait "$spid" 2>/dev/null || true; return 1; fi
 grep -Fxq 'V652_LOCK_SEEDED' "$out/seed.log" || { kill "$spid" 2>/dev/null || true; pkill -P "$spid" 2>/dev/null || true; wait "$spid" 2>/dev/null || true; return 1; }
 local run_raw checkpoint_raw before_raw cron_raw
 run_raw=$(wp db query "SELECT option_value FROM wp_options WHERE option_name='ppar_ebay_run_state_v1' LIMIT 1;" --skip-column-names --path="$WP" --allow-root 2>/dev/null | tr -d '\r\n')
 checkpoint_raw=$(wp db query "SELECT option_value FROM wp_options WHERE option_name='ppar_ebay_public_checkpoint_v1' LIMIT 1;" --skip-column-names --path="$WP" --allow-root 2>/dev/null | tr -d '\r\n')
 before_raw=$(wp db query "SELECT option_value FROM wp_options WHERE option_name='v652_lock_checkpoint_before' LIMIT 1;" --skip-column-names --path="$WP" --allow-root 2>/dev/null | tr -d '\r\n')
 cron_raw=$(wp db query "SELECT option_value FROM wp_options WHERE option_name='cron' LIMIT 1;" --skip-column-names --path="$WP" --allow-root 2>/dev/null | tr -d '\r\n')
 printf '%s' "$run_raw" > "$out/run.serialized"; printf '%s' "$checkpoint_raw" > "$out/checkpoint.serialized"; printf '%s' "$before_raw" > "$out/checkpoint-before.serialized"
 kill "$spid" 2>/dev/null || true; pkill -P "$spid" 2>/dev/null || true; wait "$spid" 2>/dev/null || true
 [ "$checkpoint_raw" = "$before_raw" ] || return 1
 [[ "$cron_raw" != *"ppar_ebay_sync_worker"* ]] || return 1
 printf '%s' "$run_raw" | php -r '$r=unserialize(stream_get_contents(STDIN)); if(!is_array($r)||($r["run_uuid"]??"")!=="v652-lock-probe"||($r["status"]??"")!=="failed"||($r["phase"]??"")!=="failed"||($r["error_code"]??"")!=="background_transport_lock_timeout"||(int)($r["checkpoint_safe"]??0)!==1||($r["checkpoint_id"]??"")!=="v652-lock-safe"||(int)($r["restart_available"]??0)!==1||($r["owner"]??"")!==""||(int)($r["lease_expires_at"]??0)!==0){exit(1);} $e=$r["errors"]??array(); $last=end($e); if(!is_array($last)||($last["code"]??"")!=="background_transport_lock_timeout"){exit(1);}' || return 1
 local seed_hits; seed_hits=$(grep -c 'GET /?v652_lock_seed=1' "$out/server.log" || true); [ "$seed_hits" -eq 1 ] || return 1
 local cron_hits; cron_hits=$(grep -c 'POST /wp-cron.php' "$out/server.log" || true); [ "$cron_hits" -eq 0 ] || return 1
 local extra_hits; extra_hits=$(grep -E ' (GET|POST) /' "$out/server.log" | grep -v 'GET /?v652_lock_seed=1' | wc -l | tr -d ' ' || true); [ "$extra_hits" -eq 0 ] || return 1
 printf 'ORPHAN_CRON_LOCK_FAILCLOSED=PASS\nWORDPRESS_VERSION=%s\nRUN_TERMINAL_FAILED=PASS\nERROR_CODE=background_transport_lock_timeout\nRESTART_AVAILABLE=PASS\nSAFE_CHECKPOINT_BYTE_IDENTICAL=PASS\nSTALE_WORKER_EVENT_CLEARED=PASS\nNO_BROWSER_OR_APP_REQUEST_AFTER_SEED=PASS\n' "$core_version" > "$out/RESULT.txt"
}
'''
anchor='\nreal_gate "$SRC" step1 REAL_STEP1 6.50.1 || block "real WordPress/MariaDB workflow failed after V6.52 core-cron self-pump production step"'
if s.count(anchor)!=1: raise SystemExit('BLOCKED: real step1 invocation anchor mismatch')
s=s.replace(anchor,neg+anchor,1)
p.write_text(s)
