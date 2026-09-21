#!/usr/bin/env python3
from pathlib import Path
import sys

repo = Path(sys.argv[1])
job = Path(sys.argv[2])

s = repo.read_text(encoding="utf-8")
old = """    public static function recordCostOnce(string $runUuid,string $endpoint,float $estimated,float $actual): bool {
        global $wpdb;
        $table=self::table('cost_ledger');
        $rows=$wpdb->get_results($wpdb->prepare("SELECT estimated_cost,actual_cost FROM $table WHERE run_uuid=%s AND endpoint_key=%s ORDER BY id ASC",$runUuid,$endpoint),ARRAY_A)?:[];"""
new = """    public static function recordCostOnce(string $runUuid,string $endpoint,float $estimated,float $actual): bool {
        global $wpdb;
        $table=self::table('cost_ledger');
        $rows=$wpdb->get_results($wpdb->prepare("SELECT estimated_cost,actual_cost FROM $table WHERE run_uuid=%s AND endpoint_key=%s ORDER BY id ASC",$runUuid,$endpoint),ARRAY_A)?:[];
        error_log('PSTE_STATETRACE COST_ENTER t='.sprintf('%.6f',microtime(true)).' pid='.getmypid().' run='.$runUuid.' endpoint='.$endpoint.' estimated='.sprintf('%.6f',$estimated).' actual='.sprintf('%.6f',$actual).' rows_b64='.base64_encode(wp_json_encode($rows,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)));"""
if old not in s:
    raise SystemExit("COST_ENTER_ANCHOR_MISSING")
s=s.replace(old,new,1)

old = """            if(abs($storedEstimated-$estimated)>0.0000005||abs($storedActual-$actual)>0.0000005)throw new RuntimeException('PSTE_COST_LEDGER_ATTEMPT_MISMATCH');"""
new = """            if(abs($storedEstimated-$estimated)>0.0000005||abs($storedActual-$actual)>0.0000005){error_log('PSTE_STATETRACE COST_MISMATCH t='.sprintf('%.6f',microtime(true)).' pid='.getmypid().' run='.$runUuid.' endpoint='.$endpoint.' stored_estimated='.sprintf('%.6f',$storedEstimated).' new_estimated='.sprintf('%.6f',$estimated).' stored_actual='.sprintf('%.6f',$storedActual).' new_actual='.sprintf('%.6f',$actual));throw new RuntimeException('PSTE_COST_LEDGER_ATTEMPT_MISMATCH');}"""
if old not in s:
    raise SystemExit("COST_MISMATCH_ANCHOR_MISSING")
s=s.replace(old,new,1)
repo.write_text(s,encoding="utf-8")

s = job.read_text(encoding="utf-8")
old = """    private static function save(array $job): void {$job=self::withHash($job);update_option(PSTE_OPTION_ACTIVE_RESEARCH_JOB,$job,false);$stored=get_option(PSTE_OPTION_ACTIVE_RESEARCH_JOB,null);if(!is_array($stored)||!hash_equals((string)$job['sha256'],(string)($stored['sha256']??'')))throw new RuntimeException('PSTE_RESEARCH_JOB_READBACK_MISMATCH');self::assertJob($stored);}"""
new = """    private static function save(array $job): void {$expectedSha=(string)($job['sha256']??'');$job=self::withHash($job);error_log('PSTE_STATETRACE JOB_SAVE_ENTER t='.sprintf('%.6f',microtime(true)).' pid='.getmypid().' uuid='.(string)($job['job_uuid']??'').' phase='.(string)($job['phase']??'').' phase_state='.(string)($job['phase_state']??'').' status='.(string)($job['status']??'').' expected='.$expectedSha.' sha='.(string)($job['sha256']??''));global $wpdb;$option=PSTE_OPTION_ACTIVE_RESEARCH_JOB;$raw=$wpdb->get_var($wpdb->prepare("SELECT option_value FROM {$wpdb->options} WHERE option_name=%s",$option));if($raw===null){if(!add_option($option,$job,'',false))throw new RuntimeException('PSTE_RESEARCH_JOB_STALE_SNAPSHOT');}else{$current=maybe_unserialize($raw);$currentSha=is_array($current)?(string)($current['sha256']??''):'';if($expectedSha===''||$currentSha===''||!hash_equals($expectedSha,$currentSha))throw new RuntimeException('PSTE_RESEARCH_JOB_STALE_SNAPSHOT');$newRaw=maybe_serialize($job);$changed=PSTE_DB_Write_Guard::query($wpdb->prepare("UPDATE {$wpdb->options} SET option_value=%s WHERE option_name=%s AND option_value=%s",$newRaw,$option,$raw),'PSTE_RESEARCH_JOB_CAS_WRITE_FAILED');if((int)$changed!==1)throw new RuntimeException('PSTE_RESEARCH_JOB_STALE_SNAPSHOT');wp_cache_delete($option,'options');}$stored=get_option($option,null);$storedSha=is_array($stored)?(string)($stored['sha256']??''):'NON_ARRAY';error_log('PSTE_STATETRACE JOB_SAVE_READBACK t='.sprintf('%.6f',microtime(true)).' pid='.getmypid().' uuid='.(string)($job['job_uuid']??'').' wanted='.(string)($job['sha256']??'').' got='.$storedSha.' stored_phase='.(is_array($stored)?(string)($stored['phase']??''):'').' stored_phase_state='.(is_array($stored)?(string)($stored['phase_state']??''):'').' stored_status='.(is_array($stored)?(string)($stored['status']??''):'') );if(!is_array($stored)||!hash_equals((string)$job['sha256'],$storedSha)){error_log('PSTE_STATETRACE JOB_READBACK_MISMATCH t='.sprintf('%.6f',microtime(true)).' pid='.getmypid().' uuid='.(string)($job['job_uuid']??'').' wanted='.(string)($job['sha256']??'').' got='.$storedSha);throw new RuntimeException('PSTE_RESEARCH_JOB_READBACK_MISMATCH');}self::assertJob($stored);}"""
if old not in s:
    raise SystemExit("JOB_SAVE_ANCHOR_MISSING")
s=s.replace(old,new,1)
job.write_text(s,encoding="utf-8")

print("PASS STATE_TRACE_INJECTED")
