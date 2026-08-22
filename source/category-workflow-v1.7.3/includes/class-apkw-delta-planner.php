<?php
if (!defined('ABSPATH')) { exit; }

/** Read-only post-FINAL baseline/delta planner. No WordPress writes. */
final class APKW_DeltaPlanner {
    public const CONTRACT='MASTER016_R8_DYNAMIC_BASELINE_DELTA_V1';

    public static function plan(array $baseline,array $candidate):array{
        $base=self::index($baseline);$next=self::index($candidate);$changes=[];$research_required=[];
        foreach($next as $id=>$node){
            if(!isset($base[$id])){
                $changes[]=['concept_id'=>$id,'change'=>'ADDED','research_required'=>true,'reason'=>'NEW_CONCEPT_ID'];$research_required[]=$id;continue;
            }
            $old=$base[$id];$fields=[];
            foreach(['name','slug','parent_concept_id','level','primary_keyword','research_cluster_id','search_intent','status'] as $f){if(self::norm($old[$f]??null)!==self::norm($node[$f]??null))$fields[]=$f;}
            if(!$fields){$changes[]=['concept_id'=>$id,'change'=>'UNCHANGED','research_required'=>false,'changed_fields'=>[]];continue;}
            $identity_changed=in_array('research_cluster_id',$fields,true);
            $changes[]=['concept_id'=>$id,'change'=>'UPDATED','research_required'=>$identity_changed,'changed_fields'=>$fields,'reason'=>$identity_changed?'RESEARCH_IDENTITY_CHANGED':'SAME_RESEARCH_IDENTITY_DELTA_REUSES_BOUND_EVIDENCE'];
            if($identity_changed)$research_required[]=$id;
        }
        foreach($base as $id=>$node)if(!isset($next[$id]))$changes[]=['concept_id'=>$id,'change'=>'RETIRED_REVIEW_REQUIRED','research_required'=>false,'automatic_delete'=>false,'reason'=>'MISSING_FROM_NEW_CONCEPT_VERSION_NEVER_AUTO_DELETE'];
        usort($changes,static fn($a,$b)=>strcmp((string)$a['concept_id'],(string)$b['concept_id']));
        return [
            'contract'=>self::CONTRACT,
            'baseline_review_scope_sha256'=>APKW_Validator::review_scope_hash($baseline),
            'candidate_review_scope_sha256'=>APKW_Validator::review_scope_hash($candidate),
            'change_count'=>count(array_filter($changes,static fn($r)=>($r['change']??'')!=='UNCHANGED')),
            'research_required_concept_ids'=>array_values(array_unique($research_required)),
            'full_workflow_regression_required'=>true,
            'automatic_delete'=>false,
            'stable_identity'=>'concept_id',
            'changes'=>$changes,
        ];
    }
    private static function index(array $package):array{$out=[];foreach(is_array($package['nodes']??null)?$package['nodes']:[] as $n){if(!is_array($n))continue;$id=trim((string)($n['concept_id']??''));if($id!=='')$out[$id]=$n;}return $out;}
    private static function norm($v):string{if($v===null)return '';if(is_bool($v))return $v?'1':'0';return trim((string)$v);}
}
