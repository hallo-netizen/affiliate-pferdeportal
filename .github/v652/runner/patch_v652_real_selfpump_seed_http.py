from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text()
anchor="},1000);\nPHPV652MU"
insert=r'''},1000);
add_action('init', function(){
    if ((string)($_GET['v652_selfpump_seed'] ?? '') !== '1') { return; }
    if (!class_exists('Pferdeportal_Affiliate_Router')) { status_header(500); echo "router missing\n"; exit; }
    $p=Pferdeportal_Affiliate_Router::instance();
    wp_clear_scheduled_hook(Pferdeportal_Affiliate_Router::EBAY_WORKER_HOOK);
    $cp=array('checkpoint_id'=>'v652-selfpump-safe','created_at'=>time(),'business_campaign_ids'=>array(11),'private_listing_ids'=>array(22),'verification'=>array('probe'=>1));
    update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_PUBLIC_CHECKPOINT,$cp,false);
    $run=array('schema'=>'1.0','build'=>Pferdeportal_Affiliate_Router::EBAY_RUNTIME_BUILD,'run_uuid'=>'v652-selfpump-probe','status'=>'running','phase'=>'transport_probe','started_at'=>time(),'updated_at'=>time(),'finished_at'=>0,'owner'=>'','lease_expires_at'=>0,'worker_transport'=>'wp_cron','resume_at'=>0,'checkpoint_candidate'=>array('business_campaign_ids'=>array(11),'private_listing_ids'=>array(22)),'phase_state'=>array(),'coverage'=>array(),'gapfill'=>array('attempts'=>0,'missing'=>array()),'errors'=>array());
    update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,$run,false);
    update_option('v652_selfpump_probe_count',0,false);
    $m=new ReflectionMethod($p,'ebay_run_schedule_worker');$m->setAccessible(true);
    if(!$m->invoke($p,0)){ status_header(500); echo "schedule failed\n"; exit; }
    echo "V652_SELF_PUMP_SEEDED\n";
    exit;
}, PHP_INT_MAX);
PHPV652MU'''
if s.count(anchor) != 1:
    raise SystemExit('BLOCKED: selfpump MU insertion anchor not found exactly once')
s=s.replace(anchor,insert,1)
start=" cat > /tmp/v652-selfpump-seed.php <<'PHPV652SEED'\n"
end=" grep -Fxq 'V652_SELF_PUMP_SEEDED' \"$out/seed.log\" || { kill \"$spid\" 2>/dev/null || true; wait \"$spid\" 2>/dev/null || true; return 1; }\n"
i=s.find(start); j=s.find(end,i)
if i < 0 or j < 0:
    raise SystemExit('BLOCKED: old CLI selfpump seed block not found')
j += len(end)
new=r''' php -S 127.0.0.1:8099 -t "$WP" > "$out/server.log" 2>&1 & local spid=$!; sleep 1
 set +e; curl --fail --silent --show-error 'http://127.0.0.1:8099/?v652_selfpump_seed=1' > "$out/seed.log" 2>&1; local seed_rc=$?; set -e
 if [ "$seed_rc" -ne 0 ]; then kill "$spid" 2>/dev/null || true; wait "$spid" 2>/dev/null || true; return 1; fi
 grep -Fxq 'V652_SELF_PUMP_SEEDED' "$out/seed.log" || { kill "$spid" 2>/dev/null || true; wait "$spid" 2>/dev/null || true; return 1; }
'''
s=s[:i]+new+s[j:]
old=" local cron_hits; cron_hits=$(grep -c 'POST /wp-cron.php' \"$out/server.log\" || true); [ \"$cron_hits\" -ge 3 ] || return 1\n printf 'AUTONOMOUS_CORE_CRON_CHAIN=PASS\\nPROBE_TICKS=3\\nHTTP_WP_CRON_REQUESTS=%s\\nNO_BROWSER_REQUEST_AFTER_SEED=PASS\\nSAFE_CHECKPOINT_PRESERVED=PASS\\n' \"$cron_hits\" > \"$out/RESULT.txt\"\n"
new2=" local seed_hits; seed_hits=$(grep -c 'GET /?v652_selfpump_seed=1' \"$out/server.log\" || true); [ \"$seed_hits\" -eq 1 ] || return 1\n local cron_hits; cron_hits=$(grep -c 'POST /wp-cron.php' \"$out/server.log\" || true); [ \"$cron_hits\" -ge 3 ] || return 1\n local non_chain_hits; non_chain_hits=$(grep -E ' (GET|POST) /' \"$out/server.log\" | grep -v 'GET /?v652_selfpump_seed=1' | grep -v 'POST /wp-cron.php' | wc -l | tr -d ' ' || true); [ \"$non_chain_hits\" -eq 0 ] || return 1\n printf 'AUTONOMOUS_CORE_CRON_CHAIN=PASS\\nSEED_HTTP_REQUESTS=%s\\nPROBE_TICKS=3\\nHTTP_WP_CRON_REQUESTS=%s\\nNO_BROWSER_OR_APP_REQUEST_AFTER_SEED=PASS\\nSAFE_CHECKPOINT_PRESERVED=PASS\\n' \"$seed_hits\" \"$cron_hits\" > \"$out/RESULT.txt\"\n"
if s.count(old) != 1:
    raise SystemExit('BLOCKED: selfpump result proof block not found exactly once')
s=s.replace(old,new2,1)
p.write_text(s)
