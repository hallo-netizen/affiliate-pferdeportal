#!/usr/bin/env python3
from pathlib import Path
import sys

root=Path(sys.argv[1])

def rep(path, old, new, label):
    p=root/path
    s=p.read_text(encoding="utf-8")
    if old not in s:
        raise SystemExit(label+"_ANCHOR_MISSING")
    p.write_text(s.replace(old,new,1),encoding="utf-8")

rep(Path("includes/class-pste-research-driver.php"),
"""    private static function acquireLock(): string {$token=hash('sha256','driver|'.microtime(true).'|'.wp_generate_uuid4());$v=['token'=>$token,'expires_at'=>time()+self::LOCK_TTL];if(add_option(PSTE_OPTION_RESEARCH_DRIVER_LOCK,$v,'',false))return $token;$old=get_option(PSTE_OPTION_RESEARCH_DRIVER_LOCK,[]);if(is_array($old)&&(int)($old['expires_at']??0)<time()){if(get_option(PSTE_OPTION_RESEARCH_DRIVER_LOCK,[])===$old)delete_option(PSTE_OPTION_RESEARCH_DRIVER_LOCK);if(add_option(PSTE_OPTION_RESEARCH_DRIVER_LOCK,$v,'',false))return $token;}throw new RuntimeException('PSTE_RESEARCH_DRIVER_ALREADY_RUNNING');}
    private static function releaseLock(string $token): void {$v=get_option(PSTE_OPTION_RESEARCH_DRIVER_LOCK,[]);if(is_array($v)&&hash_equals($token,(string)($v['token']??'')))delete_option(PSTE_OPTION_RESEARCH_DRIVER_LOCK);}""",
"""    private static function acquireLock(): string {$token=hash('sha256','driver|'.microtime(true).'|'.wp_generate_uuid4());$v=['token'=>$token,'expires_at'=>time()+self::LOCK_TTL];if(add_option(PSTE_OPTION_RESEARCH_DRIVER_LOCK,$v,'',false))return $token;self::deleteExpiredLockAtomically(PSTE_OPTION_RESEARCH_DRIVER_LOCK);if(add_option(PSTE_OPTION_RESEARCH_DRIVER_LOCK,$v,'',false))return $token;throw new RuntimeException('PSTE_RESEARCH_DRIVER_ALREADY_RUNNING');}
    private static function releaseLock(string $token): void {self::deleteOwnedLockAtomically(PSTE_OPTION_RESEARCH_DRIVER_LOCK,$token);}
    private static function deleteExpiredLockAtomically(string $option): void {global $wpdb;$raw=$wpdb->get_var($wpdb->prepare("SELECT option_value FROM {$wpdb->options} WHERE option_name=%s",$option));if(!is_string($raw)||$raw==='')return;$v=maybe_unserialize($raw);if(!is_array($v)||(int)($v['expires_at']??0)>=time())return;PSTE_DB_Write_Guard::query($wpdb->prepare("DELETE FROM {$wpdb->options} WHERE option_name=%s AND option_value=%s",$option,$raw),'PSTE_LOCK_ATOMIC_EXPIRED_DELETE_FAILED');wp_cache_delete($option,'options');}
    private static function deleteOwnedLockAtomically(string $option,string $token): void {global $wpdb;$raw=$wpdb->get_var($wpdb->prepare("SELECT option_value FROM {$wpdb->options} WHERE option_name=%s",$option));if(!is_string($raw)||$raw==='')return;$v=maybe_unserialize($raw);if(!is_array($v)||!hash_equals($token,(string)($v['token']??'')))return;PSTE_DB_Write_Guard::query($wpdb->prepare("DELETE FROM {$wpdb->options} WHERE option_name=%s AND option_value=%s",$option,$raw),'PSTE_LOCK_ATOMIC_RELEASE_FAILED');wp_cache_delete($option,'options');}""","DRIVER")

# broad replacements for identical one-line lock patterns
for rel in ["includes/class-pste-research-job.php","includes/class-pste-breadth-research-queue.php"]:
    p=root/rel
    s=p.read_text(encoding="utf-8")
    if "private static function deleteOwnedOptionLockAtomically" not in s:
        anchor="    private static function errorCode" if "research-job" in rel else "    private static function isTransientCoordinationCode"
        helper="""    private static function deleteExpiredOptionLockAtomically(string $option): void {global $wpdb;$raw=$wpdb->get_var($wpdb->prepare("SELECT option_value FROM {$wpdb->options} WHERE option_name=%s",$option));if(!is_string($raw)||$raw==='')return;$v=maybe_unserialize($raw);if(!is_array($v)||(int)($v['expires_at']??0)>=time())return;PSTE_DB_Write_Guard::query($wpdb->prepare("DELETE FROM {$wpdb->options} WHERE option_name=%s AND option_value=%s",$option,$raw),'PSTE_LOCK_ATOMIC_EXPIRED_DELETE_FAILED');wp_cache_delete($option,'options');}
    private static function deleteOwnedOptionLockAtomically(string $option,string $token): void {global $wpdb;$raw=$wpdb->get_var($wpdb->prepare("SELECT option_value FROM {$wpdb->options} WHERE option_name=%s",$option));if(!is_string($raw)||$raw==='')return;$v=maybe_unserialize($raw);if(!is_array($v)||!hash_equals($token,(string)($v['token']??'')))return;PSTE_DB_Write_Guard::query($wpdb->prepare("DELETE FROM {$wpdb->options} WHERE option_name=%s AND option_value=%s",$option,$raw),'PSTE_LOCK_ATOMIC_RELEASE_FAILED');wp_cache_delete($option,'options');}
"""
        if anchor not in s: raise SystemExit(rel+"_HELPER_ANCHOR_MISSING")
        s=s.replace(anchor,helper+anchor,1)
    s=s.replace("if(get_option(PSTE_OPTION_RESEARCH_CONTROL_LOCK,[])===$existing)delete_option(PSTE_OPTION_RESEARCH_CONTROL_LOCK);","self::deleteExpiredOptionLockAtomically(PSTE_OPTION_RESEARCH_CONTROL_LOCK);")
    s=s.replace("if(get_option(PSTE_OPTION_BREADTH_RESEARCH_LOCK,[])===$existing)delete_option(PSTE_OPTION_BREADTH_RESEARCH_LOCK);","self::deleteExpiredOptionLockAtomically(PSTE_OPTION_BREADTH_RESEARCH_LOCK);")
    s=s.replace("if(get_option(PSTE_OPTION_RESEARCH_STEP_LOCK,[])===$existing)delete_option(PSTE_OPTION_RESEARCH_STEP_LOCK);","self::deleteExpiredOptionLockAtomically(PSTE_OPTION_RESEARCH_STEP_LOCK);")
    s=s.replace("private static function releaseLaunchLock(string $token): void {$existing=get_option(PSTE_OPTION_RESEARCH_CONTROL_LOCK,[]);if(is_array($existing)&&hash_equals($token,(string)($existing['token']??'')))delete_option(PSTE_OPTION_RESEARCH_CONTROL_LOCK);}","private static function releaseLaunchLock(string $token): void {self::deleteOwnedOptionLockAtomically(PSTE_OPTION_RESEARCH_CONTROL_LOCK,$token);}")
    s=s.replace("private static function releaseQueueLock(string $token): void {$existing=get_option(PSTE_OPTION_BREADTH_RESEARCH_LOCK,[]);if(is_array($existing)&&hash_equals($token,(string)($existing['token']??'')))delete_option(PSTE_OPTION_BREADTH_RESEARCH_LOCK);}","private static function releaseQueueLock(string $token): void {self::deleteOwnedOptionLockAtomically(PSTE_OPTION_BREADTH_RESEARCH_LOCK,$token);}")
    s=s.replace("private static function releaseStepLock(string $token): void {$existing=get_option(PSTE_OPTION_RESEARCH_STEP_LOCK,[]);if(is_array($existing)&&hash_equals($token,(string)($existing['token']??'')))delete_option(PSTE_OPTION_RESEARCH_STEP_LOCK);}","private static function releaseStepLock(string $token): void {self::deleteOwnedOptionLockAtomically(PSTE_OPTION_RESEARCH_STEP_LOCK,$token);}")
    p.write_text(s,encoding="utf-8")

# budget release
p=root/"includes/class-pste-budget-reservations.php"
s=p.read_text(encoding="utf-8")
old="private static function releaseLock(string $token): void {$existing=get_option(PSTE_OPTION_BUDGET_LOCK,[]);if(is_array($existing)&&hash_equals($token,(string)($existing['token']??'')))delete_option(PSTE_OPTION_BUDGET_LOCK);}"
new="private static function releaseLock(string $token): void {global $wpdb;$raw=$wpdb->get_var($wpdb->prepare(\"SELECT option_value FROM {$wpdb->options} WHERE option_name=%s\",PSTE_OPTION_BUDGET_LOCK));if(!is_string($raw)||$raw==='')return;$existing=maybe_unserialize($raw);if(!is_array($existing)||!hash_equals($token,(string)($existing['token']??'')))return;PSTE_DB_Write_Guard::query($wpdb->prepare(\"DELETE FROM {$wpdb->options} WHERE option_name=%s AND option_value=%s\",PSTE_OPTION_BUDGET_LOCK,$raw),'PSTE_BUDGET_LOCK_ATOMIC_RELEASE_FAILED');wp_cache_delete(PSTE_OPTION_BUDGET_LOCK,'options');}"
if old not in s: raise SystemExit("BUDGET_RELEASE_ANCHOR_MISSING")
p.write_text(s.replace(old,new,1),encoding="utf-8")

# sandbox
p=root/"includes/class-pste-semantic-review-sandbox.php"
s=p.read_text(encoding="utf-8")
old="private static function releaseLock(string $token): void {if($token==='PSTE_BATCH_CONTEXT_LOCK')return;$old=get_option(PSTE_OPTION_SEMANTIC_SANDBOX_LOCK,[]);if(is_array($old)&&hash_equals($token,(string)($old['token']??'')))delete_option(PSTE_OPTION_SEMANTIC_SANDBOX_LOCK);}"
new="private static function releaseLock(string $token): void {if($token==='PSTE_BATCH_CONTEXT_LOCK')return;global $wpdb;$raw=$wpdb->get_var($wpdb->prepare(\"SELECT option_value FROM {$wpdb->options} WHERE option_name=%s\",PSTE_OPTION_SEMANTIC_SANDBOX_LOCK));if(!is_string($raw)||$raw==='')return;$old=maybe_unserialize($raw);if(!is_array($old)||!hash_equals($token,(string)($old['token']??'')))return;PSTE_DB_Write_Guard::query($wpdb->prepare(\"DELETE FROM {$wpdb->options} WHERE option_name=%s AND option_value=%s\",PSTE_OPTION_SEMANTIC_SANDBOX_LOCK,$raw),'PSTE_SANDBOX_LOCK_ATOMIC_RELEASE_FAILED');wp_cache_delete(PSTE_OPTION_SEMANTIC_SANDBOX_LOCK,'options');}"
if old not in s: raise SystemExit("SANDBOX_RELEASE_ANCHOR_MISSING")
p.write_text(s.replace(old,new,1),encoding="utf-8")

# safe migration release
p=root/"includes/class-pste-safe-migration-job.php"
s=p.read_text(encoding="utf-8")
old="private static function releaseStepLock(string $token): void {try{$old=get_option(PSTE_OPTION_SAFE_MIGRATION_STEP_LOCK,[]);if(is_array($old)&&hash_equals($token,(string)($old['token']??'')))delete_option(PSTE_OPTION_SAFE_MIGRATION_STEP_LOCK);}catch(Throwable $e){}}"
new="private static function releaseStepLock(string $token): void {try{global $wpdb;$raw=$wpdb->get_var($wpdb->prepare(\"SELECT option_value FROM {$wpdb->options} WHERE option_name=%s\",PSTE_OPTION_SAFE_MIGRATION_STEP_LOCK));if(!is_string($raw)||$raw==='')return;$old=maybe_unserialize($raw);if(!is_array($old)||!hash_equals($token,(string)($old['token']??'')))return;PSTE_DB_Write_Guard::query($wpdb->prepare(\"DELETE FROM {$wpdb->options} WHERE option_name=%s AND option_value=%s\",PSTE_OPTION_SAFE_MIGRATION_STEP_LOCK,$raw),'PSTE_SAFE_MIGRATION_LOCK_ATOMIC_RELEASE_FAILED');wp_cache_delete(PSTE_OPTION_SAFE_MIGRATION_STEP_LOCK,'options');}catch(Throwable $e){}}"
if old not in s: raise SystemExit("SAFE_RELEASE_ANCHOR_MISSING")
p.write_text(s.replace(old,new,1),encoding="utf-8")


# Hard postconditions: no silent partial application.
checks = {
    "includes/class-pste-research-driver.php": [
        "deleteOwnedLockAtomically(PSTE_OPTION_RESEARCH_DRIVER_LOCK,$token)",
        "deleteExpiredLockAtomically(PSTE_OPTION_RESEARCH_DRIVER_LOCK)",
    ],
    "includes/class-pste-research-job.php": [
        "deleteOwnedOptionLockAtomically(PSTE_OPTION_RESEARCH_STEP_LOCK,$token)",
        "deleteExpiredOptionLockAtomically(PSTE_OPTION_RESEARCH_STEP_LOCK)",
    ],
    "includes/class-pste-breadth-research-queue.php": [
        "deleteOwnedOptionLockAtomically(PSTE_OPTION_BREADTH_RESEARCH_LOCK,$token)",
        "deleteExpiredOptionLockAtomically(PSTE_OPTION_BREADTH_RESEARCH_LOCK)",
    ],
}
for rel, needles in checks.items():
    text=(root/rel).read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            raise SystemExit(rel+"_ATOMIC_LOCK_POSTCONDITION_MISSING_"+needle)
unsafe = {
    "includes/class-pste-research-driver.php": ["delete_option(PSTE_OPTION_RESEARCH_DRIVER_LOCK)"],
    "includes/class-pste-research-job.php": ["delete_option(PSTE_OPTION_RESEARCH_STEP_LOCK)"],
    "includes/class-pste-breadth-research-queue.php": ["delete_option(PSTE_OPTION_BREADTH_RESEARCH_LOCK)"],
}
for rel, needles in unsafe.items():
    text=(root/rel).read_text(encoding="utf-8")
    for needle in needles:
        if needle in text:
            raise SystemExit(rel+"_UNSAFE_LOCK_DELETE_REMAINS_"+needle)

print("PASS ATOMIC_LOCK_ROOTFIX_INJECTED_AND_VERIFIED")
