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
class_anchor = "final class PSTE_Research_Job {"
if class_anchor not in s:
    raise SystemExit("JOB_CLASS_ANCHOR_MISSING")
s=s.replace(class_anchor,class_anchor+"\n    private static string $activeStepFenceToken='';",1)
advance_anchor = "$token=self::acquireStepLock();"
if advance_anchor not in s:
    raise SystemExit("JOB_ADVANCE_LOCK_ANCHOR_MISSING")
s=s.replace(advance_anchor,advance_anchor+"self::$activeStepFenceToken=$token;",1)
old = """    private static function save(array $job): void {$job=self::withHash($job);update_option(PSTE_OPTION_ACTIVE_RESEARCH_JOB,$job,false);$stored=get_option(PSTE_OPTION_ACTIVE_RESEARCH_JOB,null);if(!is_array($stored)||!hash_equals((string)$job['sha256'],(string)($stored['sha256']??'')))throw new RuntimeException('PSTE_RESEARCH_JOB_READBACK_MISMATCH');self::assertJob($stored);}"""
new = """    private static function save(array $job): void {if(self::$activeStepFenceToken!==''){$lock=get_option(PSTE_OPTION_RESEARCH_STEP_LOCK,[]);if(!is_array($lock)||!hash_equals(self::$activeStepFenceToken,(string)($lock['token']??'')))throw new RuntimeException('PSTE_RESEARCH_STEP_FENCE_LOST');}$job=self::withHash($job);error_log('PSTE_STATETRACE JOB_SAVE_ENTER t='.sprintf('%.6f',microtime(true)).' pid='.getmypid().' uuid='.(string)($job['job_uuid']??'').' phase='.(string)($job['phase']??'').' phase_state='.(string)($job['phase_state']??'').' status='.(string)($job['status']??'').' sha='.(string)($job['sha256']??''));$updateResult=update_option(PSTE_OPTION_ACTIVE_RESEARCH_JOB,$job,false);global $wpdb;$directRaw=$wpdb->get_var($wpdb->prepare("SELECT option_value FROM {$wpdb->options} WHERE option_name=%s",PSTE_OPTION_ACTIVE_RESEARCH_JOB));$direct=is_string($directRaw)?maybe_unserialize($directRaw):null;error_log('PSTE_STATETRACE JOB_WRITE_RESULT t='.sprintf('%.6f',microtime(true)).' pid='.getmypid().' update_result='.($updateResult?'1':'0').' db_error='.base64_encode((string)$wpdb->last_error).' direct_sha='.(is_array($direct)?(string)($direct['sha256']??''):'NON_ARRAY'));$stored=get_option(PSTE_OPTION_ACTIVE_RESEARCH_JOB,null);$storedSha=is_array($stored)?(string)($stored['sha256']??''):'NON_ARRAY';error_log('PSTE_STATETRACE JOB_SAVE_READBACK t='.sprintf('%.6f',microtime(true)).' pid='.getmypid().' uuid='.(string)($job['job_uuid']??'').' wanted='.(string)($job['sha256']??'').' got='.$storedSha.' stored_phase='.(is_array($stored)?(string)($stored['phase']??''):'').' stored_phase_state='.(is_array($stored)?(string)($stored['phase_state']??''):'').' stored_status='.(is_array($stored)?(string)($stored['status']??''):'') );if(!is_array($stored)||!hash_equals((string)$job['sha256'],$storedSha)){error_log('PSTE_STATETRACE JOB_READBACK_MISMATCH t='.sprintf('%.6f',microtime(true)).' pid='.getmypid().' uuid='.(string)($job['job_uuid']??'').' wanted='.(string)($job['sha256']??'').' got='.$storedSha);throw new RuntimeException('PSTE_RESEARCH_JOB_READBACK_MISMATCH');}self::assertJob($stored);}"""
if old not in s:
    raise SystemExit("JOB_SAVE_ANCHOR_MISSING")
s=s.replace(old,new,1)
delete_old = """    private static function deleteIfSame(array $job): void {$stored=self::rawJob();if($stored!==null&&hash_equals((string)$job['job_uuid'],(string)($stored['job_uuid']??'')))delete_option(PSTE_OPTION_ACTIVE_RESEARCH_JOB);}"""
delete_new = """    private static function deleteIfSame(array $job): void {$stored=self::rawJob();$lock=get_option(PSTE_OPTION_RESEARCH_STEP_LOCK,[]);error_log('PSTE_STATETRACE JOB_DELETE_CHECK t='.sprintf('%.6f',microtime(true)).' pid='.getmypid().' uuid='.(string)($job['job_uuid']??'').' phase='.(string)($job['phase']??'').' status='.(string)($job['status']??'').' phase_state='.(string)($job['phase_state']??'').' stored_uuid='.(is_array($stored)?(string)($stored['job_uuid']??''):'NONE').' step_lock='.(is_array($lock)?(string)($lock['token']??''):'NONE'));if($stored!==null&&hash_equals((string)$job['job_uuid'],(string)($stored['job_uuid']??''))){$ok=delete_option(PSTE_OPTION_ACTIVE_RESEARCH_JOB);error_log('PSTE_STATETRACE JOB_DELETE_DONE t='.sprintf('%.6f',microtime(true)).' pid='.getmypid().' uuid='.(string)($job['job_uuid']??'').' phase='.(string)($job['phase']??'').' status='.(string)($job['status']??'').' ok='.($ok?'1':'0'));}}"""
if delete_old not in s:
    raise SystemExit("JOB_DELETE_ANCHOR_MISSING")
s=s.replace(delete_old,delete_new,1)

job.write_text(s,encoding="utf-8")

print("PASS STATE_TRACE_INJECTED")
