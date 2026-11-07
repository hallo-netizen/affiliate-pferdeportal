#!/usr/bin/env python3
"""The existing WP planning owner CONSUMES the sole source-bound external decision.
No new gate/worker. Legacy paths retain their existing behavior.
Input: ZIP built from the original v22 by apply_existing_mini_kisten_import.py.
"""
from zipfile import ZipFile
from pathlib import Path
import sys, difflib
source=Path(sys.argv[1])
target=Path(sys.argv[2])
target.parent.mkdir(parents=True, exist_ok=True)
PLAN="Portal SEO Topic Engine/includes/class-pste-planning-readiness-gate.php"
REPO="Portal SEO Topic Engine/includes/class-pste-repository.php"
CONTEXT="Portal SEO Topic Engine/includes/class-pste-context-evaluator.php"
with ZipFile(source) as inp:
    files=[(info,inp.read(info.filename)) for info in inp.infolist()]
data={info.filename:b for info,b in files}
plan=data[PLAN].decode("utf-8")
repository=data[REPO].decode("utf-8")
context=data[CONTEXT].decode("utf-8")
needle="""    public static function apply(array $candidate,array $inventoryItems,array $categoryItems): array {
        $before=self::bindingSnapshot($candidate);"""
replacement="""    public static function apply(array $candidate,array $inventoryItems,array $categoryItems): array {
        // Existing planning gate CONSUMES the earlier external result instead
        // of running preTitleDuplicate and PSTE_Cannibalization again.
        $poolKey=(string)($candidate['pool_key']??'');
        $raw=PSTE_Editorializer::sourceQuery($candidate);
        $receipt=($poolKey!==''&&class_exists('PSTE_Mini_Workflow'))
            ?PSTE_Mini_Workflow::singleOwnerSeoFor($poolKey,$raw):[];
        $miniAwaiting=$poolKey!==''&&class_exists('PSTE_Mini_Workflow')
            &&PSTE_Mini_Workflow::isMiniTopicAwaitingSeo($poolKey);
        if($receipt||$miniAwaiting){
            $box=(string)($receipt['box']??'KLAERUNG');
            $sourceTitle=(string)($receipt['approved_title']??'');
            $candidateTitle=(string)($candidate['production_title']??'');
            if($box==='FREI'&&($sourceTitle===''||!hash_equals($sourceTitle,$candidateTitle)))
                $box='KLAERUNG';
            $ok=$box==='FREI';
            $status=$ok?'PASS':($box==='BELEGT'?'BLOCKED':'REVIEW_REQUIRED');
            $match=$box==='BELEGT'?[
                ['source'=>'EXTERNAL_SINGLE_SEO_OWNER','matched_ref'=>(string)($receipt['matched_ref']??'')]]:[];
            $gate=['contract'=>self::CONTRACT,'status'=>$status,'ok'=>$ok,
                'decision'=>$status,'reason_codes'=>['PSTE_SINGLE_EXTERNAL_SEO_DECISION'],
                'matches'=>$match,'semantic_identity_source'=>'EXTERNAL_SOURCE_BOUND_INTENT',
                'external_editorial_receipt'=>$receipt,
                'external_seo_owner_verdict'=>$box,
                'pre_title_duplicate_gate'=>['contract'=>self::PRE_TITLE_CONTRACT,
                    'ok'=>$ok,'reason_codes'=>['SKIPPED_ALREADY_DECIDED_EXTERNALLY'],
                    'matches'=>$match],
                'cannibalization'=>['decision'=>'NOT_RUN_ALREADY_DECIDED_EXTERNALLY',
                    'reason_codes'=>[],'matches'=>[]],
                'provider_calls'=>0,'write_attempted'=>false,'content_or_design_touched'=>false];
            $candidate['pre_title_duplicate_gate']=(array)$gate['pre_title_duplicate_gate'];
            $candidate['planning_readiness_gate']=$gate;
            $candidate['closest_existing_matches']=$match;
            if(!$ok){$candidate['decision']='BLOCKED';$candidate['human_review_required']=true;
                $candidate['discovery_only']=true;$candidate['candidate_role']='DISCOVERY_PROBE';}
            return $candidate;
        }
        // Legacy topics not reviewed externally: do NOT silently remove their protection.
        $before=self::bindingSnapshot($candidate);"""
assert plan.count(needle)==1
plan=plan.replace(needle,replacement)
# Original topic key is already a persistent row field, not a new database
# column. Carry its identity to the same planning gate; no new query/review.
needle="            $working=$payload;"
replacement="""            $working=$payload;
            $working['pool_key']=(string)($row['pool_key']??'');"""
assert repository.count(needle)==1
repository=repository.replace(needle,replacement)
# Existing CONTEXT worker records version/provenance only for externally
# owned MINI topics. It must NOT run a second text/heading similarity loop.
signature="    public static function evaluate(array $payload, array $inventory, array $plan, array $index): array {"
assert context.count(signature)==1
context=context.replace(signature,"    public static function evaluate(array $payload, array $inventory, array $plan, array $index, string $poolKey=''): array {")
anchor="""        // Missing family means this family-scoped comparison has no matches."""
contextFast="""        // Once a MINI topic belongs to the single external SEO owner,
        // this context reader ONLY stamps the existing source versions.
        // No PSTE_Normalizer::similarity, title comparison or editorial veto.
        if($poolKey!==''&&class_exists('PSTE_Mini_Workflow')
            &&PSTE_Mini_Workflow::isMiniTopicAwaitingSeo($poolKey)){
            $payload['reason_codes']=array_values(array_diff(
                (array)($payload['reason_codes']??[]),[
                'ANSWER_EQUIVALENT_EXISTING','ANSWER_EQUIVALENT_PLANNED',
                'CONTEXT_REFRESH_FAILED','CONTEXT_REFRESH_STALE',
                'CONTEXT_FAMILY_MISSING','PSTE_CONTEXT_QUERY_MISSING']));
            $payload['portal_context']=[
                'inventory_snapshot_sha256'=>(string)($inventory['sha256']??''),
                'editorial_plan_snapshot_sha256'=>(string)($plan['sha256']??'NOT_AVAILABLE'),
                'editorial_plan_status'=>(string)($plan['status']??'AVAILABLE'),
                'matches'=>[], 'synced_at_utc'=>gmdate('c'),
                'semantic_comparison'=>'NOT_RUN_SINGLE_EXTERNAL_SEO_OWNER'];
            $payload['context_state']='CURRENT';
            return ['state'=>'CURRENT','reason_code'=>null,'matches'=>[],'payload'=>$payload];
        }
"""
assert context.count(anchor)==1
context=context.replace(anchor,contextFast+"\n"+anchor)
call="        $evaluation=PSTE_Context_Evaluator::evaluate($payload,$inventory,$plan,$rowIndex);"
assert repository.count(call)==1
repository=repository.replace(call,"        $evaluation=PSTE_Context_Evaluator::evaluate($payload,$inventory,$plan,$rowIndex,$topicKey);")
changes={PLAN:plan.encode("utf-8"),REPO:repository.encode("utf-8"),CONTEXT:context.encode("utf-8")}
with ZipFile(target,"w") as out:
    for info,b in files:
        out.writestr(info,changes.get(info.filename,b))
for k,new in [(PLAN,plan),(REPO,repository),(CONTEXT,context)]:
    old=data[k].decode("utf-8")
    print("PATCHED",k,"old",len(old),"new",len(new))
    print("DIFF_LINES",len(list(difflib.unified_diff(old.splitlines(),new.splitlines()))))
print("LEGACY_FALLBACK_PRESERVED; K0_AND_PSERC_UNCHANGED; NO_PRODUCTION_RELEASE")
