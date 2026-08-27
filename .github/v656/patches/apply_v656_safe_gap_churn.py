#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys
if len(sys.argv)!=2:
    raise SystemExit('usage: apply_v656_safe_gap_churn.py <affiliate-portal-router-dir>')
root=Path(sys.argv[1])
run=root/'includes/trait-ppar-ebay-run.php'; ebay=root/'includes/trait-ppar-ebay.php'; main=root/'pferdeportal-affiliate-router.php'; readme=root/'readme.txt'
EXPECTED={
 'includes/trait-ppar-ebay-run.php':'c45a602ab60e13bf41f64347ea994fa2a6f5e20ebb1db1b74c51d15666b3d79e',
 'includes/trait-ppar-ebay.php':'02693cdae9cb8ed2e7c0601178b2d82c5fa8a11a9c41ea31d2a8ca29b50d7af5',
 'pferdeportal-affiliate-router.php':'90a8fe57b9feb646dc4512e27bd3c4b964b469f8bacd092f1e236586189243fd',
 'readme.txt':'18c5d948889cb377c0367d57df267f09fe76f272921b9d06d498abdd60679286',
}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
for rel,h in EXPECTED.items():
    p=root/rel
    if not p.is_file() or sha(p)!=h: raise SystemExit(f'BLOCKED baseline drift {rel} {sha(p) if p.exists() else "missing"}')

s=run.read_text()
anchor="""        return array('status'=>'pass','coverage'=>$coverage);\n    }\n\n    private function ebay_run_tick_coverage($run, $settings) {\n"""
helper="""        return array('status'=>'pass','coverage'=>$coverage);\n    }\n\n    /**\n     * V6.56 live-churn revalidation.\n     *\n     * A family that becomes newly missing while the already-running canonical\n     * gap-fill is being worked is normal marketplace churn, not proof that the\n     * existing safety contract may be skipped. Expand the durable proof scope\n     * monotonically, discover only the newly missing delta, then rerun the same\n     * canonical BUSINESS selector over the full accumulated proof scope. Public\n     * promotion remains blocked until the unchanged safe-gap contract passes.\n     */\n    private function ebay_run_schedule_new_business_gap_revalidation($run, $coverage, $origin_phase = '') {\n        $run=is_array($run)?$run:array();$coverage=is_array($coverage)?$coverage:array();\n        $missing=array_values(array_unique(array_filter(array_map('sanitize_key',(array)($coverage['missing']??array())))));\n        $targeted=array_values(array_unique(array_filter(array_map('sanitize_key',(array)($run['gapfill']['missing']??array())))));\n        sort($missing,SORT_STRING);sort($targeted,SORT_STRING);\n        if(!$missing || !$targeted || absint($run['gapfill']['attempts']??0)<1){return false;}\n        $target_map=array_fill_keys($targeted,true);$new=array();\n        foreach($missing as $id){if(!isset($target_map[$id])){$new[$id]=1;}}\n        $new=array_keys($new);sort($new,SORT_STRING);\n        if(!$new){return false;}\n\n        $required=array_values(array_unique(array_filter(array_map('sanitize_key',(array)$this->ebay_business_required_product_concept_ids()))));\n        sort($required,SORT_STRING);$required_map=array_fill_keys($required,true);\n        if(!$required){\n            $this->ebay_run_fail('business_coverage_state_inconsistent','BUSINESS-Versorgungsmanifest fehlt bei der dynamischen Lückenprüfung.',array('missing'=>$missing,'targeted'=>$targeted));\n            return true;\n        }\n        foreach($missing as $id){\n            if(!isset($required_map[$id])){\n                $this->ebay_run_fail('business_coverage_unknown_family','Unbekannte BUSINESS-Produktfamilie in der dynamischen Lückenprüfung.',array('family'=>$id));\n                return true;\n            }\n        }\n\n        // Monotonic proof scope: each physical family can enter this scope only\n        // once per run. Therefore marketplace churn cannot create an unbounded\n        // restart loop and no already-proven family is silently forgotten.\n        $expanded=$targeted;foreach($missing as $id){$expanded[]=$id;}\n        $expanded=array_values(array_unique($expanded));sort($expanded,SORT_STRING);\n        if(count($expanded)>count($required)){\n            $this->ebay_run_fail('business_coverage_state_inconsistent','BUSINESS-Lückenbeweis überschreitet das verbindliche Versorgungsmanifest.',array('targeted'=>$expanded));\n            return true;\n        }\n\n        $run['gapfill']['attempts']=max(1,absint($run['gapfill']['attempts']??0))+1;\n        $run['gapfill']['missing']=$expanded;\n        $run['gapfill']['discovery_missing']=$new;\n        $run['gapfill']['revalidation_count']=absint($run['gapfill']['revalidation_count']??0)+1;\n        $run['gapfill']['last_revalidation_at']=time();\n        $run['gapfill']['last_revalidation_from']=sanitize_key((string)$origin_phase);\n        if(!isset($run['phase_state'])||!is_array($run['phase_state'])){$run['phase_state']=array();}\n        $run['phase_state']['discovery']=array();\n        $run['phase_state']['selection']=array();\n        $run['coverage']=$coverage;\n        $run['phase']='gapfill_discovery';\n        $run['resume_reason']='business_safe_gap_dynamic_revalidation';\n        $run['no_progress_count']=0;\n        $run['progress_seq']=absint($run['progress_seq']??0)+1;\n        $run['last_progress_at']=time();\n        $this->ebay_run_save($run);\n        return true;\n    }\n\n    private function ebay_run_tick_coverage($run, $settings) {\n"""
if s.count(anchor)!=1: raise SystemExit('BLOCKED safe-gap helper anchor drift')
s=s.replace(anchor,helper,1)
old="""            $result=$this->ebay_run_business_safe_supply_gap_contract($run,$coverage);\n            if(($result['status']??'')!=='pass'){\n"""
new="""            if($this->ebay_run_schedule_new_business_gap_revalidation($run,$coverage,'coverage_verify')){return;}\n            $run=$this->ebay_run_load();\n            $result=$this->ebay_run_business_safe_supply_gap_contract($run,$coverage);\n            if(($result['status']??'')!=='pass'){\n"""
if s.count(old)!=1: raise SystemExit('BLOCKED coverage anchor drift')
s=s.replace(old,new,1)
old2="""            $current=$this->ebay_run_load();\n            $result=$this->ebay_run_business_safe_supply_gap_contract($current,$business);\n            if(($result['status']??'')!=='pass'){\n"""
new2="""            $current=$this->ebay_run_load();\n            if($this->ebay_run_schedule_new_business_gap_revalidation($current,$business,'public_verify')){return;}\n            $current=$this->ebay_run_load();\n            $result=$this->ebay_run_business_safe_supply_gap_contract($current,$business);\n            if(($result['status']??'')!=='pass'){\n"""
if s.count(old2)!=1: raise SystemExit('BLOCKED public verify anchor drift')
s=s.replace(old2,new2,1)
run.write_text(s)

s=ebay.read_text()
old="""                $exact = is_array($run['gapfill']['missing'] ?? null) ? $run['gapfill']['missing'] : array();\n                $out = array();\n"""
new="""                // During a V6.56 churn revalidation, discovery touches only\n                // families that became newly missing. Selection still owns the\n                // complete monotonic gapfill.missing proof scope.\n                $exact = is_array($run['gapfill']['discovery_missing'] ?? null) && $run['gapfill']['discovery_missing']\n                    ? $run['gapfill']['discovery_missing']\n                    : (is_array($run['gapfill']['missing'] ?? null) ? $run['gapfill']['missing'] : array());\n                $out = array();\n"""
if s.count(old)!=1: raise SystemExit('BLOCKED recovery discovery anchor drift')
s=s.replace(old,new,1)
s=s.replace('V6.17: exact BUSINESS product coverage comes first','V6.17/V6.56: exact BUSINESS product coverage comes first',1)
ebay.write_text(s)

s=main.read_text()
for old,new in [
(" * Version: 6.55.0"," * Version: 6.56.0"),
("const VERSION = '6.55.0';","const VERSION = '6.56.0';"),
("const EBAY_RUNTIME_BUILD = '6.55.0-kiss-public-heartbeat-github-scheduler-20260823';","const EBAY_RUNTIME_BUILD = '6.56.0-safe-gap-churn-revalidation-rootfix-20260827';")]:
    if s.count(old)!=1: raise SystemExit('BLOCKED main metadata anchor drift '+old)
    s=s.replace(old,new,1)
main.write_text(s)

s=readme.read_text()
old='Affiliate-Zentrale 6.55.0 – KISS PUBLIC HEARTBEAT + GITHUB SCHEDULER'
if s.count(old)!=1 or s.count('Stable tag: 6.55.0')!=1: raise SystemExit('BLOCKED readme metadata baseline drift')
s=s.replace(old,'Affiliate-Zentrale 6.56.0 – SAFE-GAP CHURN REVALIDATION ROOTFIX',1)
s=s.replace('Stable tag: 6.55.0','Stable tag: 6.56.0',1)
needle='V6.55.0 benötigt keinen zusätzlichen Cron-Anbieter'
insert="""V6.56.0 – SAFE-GAP CHURN REVALIDATION ROOTFIX\nEin während eines laufenden kanonischen BUSINESS-Gap-Fills neu fehlendes Produktkonzept beendet den Gesamtlauf nicht mehr allein aufgrund des alten Einmal-Snapshots. Der Beweisumfang wird monoton erweitert, nur neu fehlende Familien werden erneut per eBay-Discovery geprüft und anschließend läuft die unveränderte kanonische BUSINESS-Auswahl über den vollständigen Beweisumfang. Öffentliche Promotion bleibt bis zum unveränderten Safe-Gap-/Public-Gate gesperrt; echte Materialisierungs-, Speicher-, Checkpoint-, Runtime- und Invariantenfehler bleiben fail-closed.\n\n"""
if s.count(needle)!=1: raise SystemExit('BLOCKED readme body anchor drift')
s=s.replace(needle,insert+needle,1)
readme.write_text(s)
print('V656_SAFE_GAP_CHURN_PATCH=PASS')
for rel in EXPECTED: print(rel+'='+sha(root/rel))
