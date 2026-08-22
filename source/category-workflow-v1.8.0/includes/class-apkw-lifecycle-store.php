<?php
if (!defined('ABSPATH')) { exit; }

/** Persistent project memory for baselines, deltas and research candidates. */
final class APKW_LifecycleStore {
    public const CONTRACT='MASTER016_R9_PERSISTENT_LEARNING_MEMORY_V1';

    public static function load(string $project_id):array{
        $key=self::key($project_id);$state=get_option($key,[]);if(!is_array($state))$state=[];
        return $state+['contract'=>self::CONTRACT,'project_id'=>$project_id,'baseline'=>null,'history'=>[],'research_candidates'=>[]];
    }
    public static function save(string $project_id,array $state):void{update_option(self::key($project_id),$state,false);}
    public static function baseline(string $project_id):?array{$s=self::load($project_id);return is_array($s['baseline']??null)?$s['baseline']:null;}
    public static function record_baseline(array $package,array $mapping,array $readback,string $run_id,array $meta=[]):array{
        $project_id=(string)($package['project']['project_id']??'');if($project_id==='')throw new RuntimeException('Baseline ohne project_id ist unzulässig.');
        $state=self::load($project_id);$previous=$state['baseline']??null;$version=(int)($previous['baseline_version']??0)+1;
        $baseline=['baseline_version'=>$version,'recorded_at_utc'=>gmdate('c'),'run_id'=>$run_id,'review_scope_sha256'=>APKW_Validator::review_scope_hash($package),'technical_scope_sha256'=>APKW_Validator::technical_structure_scope_hash($package),'package'=>$package,'concept_object_map'=>$mapping,'readback'=>$readback,'meta'=>$meta];
        $state['baseline']=$baseline;$state['history'][]=['type'=>$previous===null?'INITIAL_BASELINE':'DELTA_BASELINE','baseline_version'=>$version,'run_id'=>$run_id,'review_scope_sha256'=>$baseline['review_scope_sha256'],'technical_scope_sha256'=>$baseline['technical_scope_sha256'],'recorded_at_utc'=>$baseline['recorded_at_utc']];self::save($project_id,$state);return $baseline;
    }
    public static function restore_baseline(string $project_id,$baseline):void{$state=self::load($project_id);$state['baseline']=is_array($baseline)?$baseline:null;$state['history'][]=['type'=>'ROLLBACK_BASELINE','recorded_at_utc'=>gmdate('c'),'restored_version'=>is_array($baseline)?(int)($baseline['baseline_version']??0):0];self::save($project_id,$state);}
    public static function add_research_candidate(string $project_id,array $candidate):array{
        $idea=trim((string)($candidate['idea']??$candidate['keyword']??''));if($idea==='')throw new RuntimeException('Research-Kandidat benötigt eine Idee oder ein Keyword.');
        $state=self::load($project_id);$id='rc-'.substr(hash('sha256',$project_id.'|'.$idea.'|'.wp_json_encode($candidate,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)),0,24);
        foreach($state['research_candidates'] as $existing)if(($existing['candidate_id']??'')===$id)return $existing;
        $row=['candidate_id'=>$id,'status'=>'RESEARCH_CANDIDATE','idea'=>$idea,'source'=>(string)($candidate['source']??'manual_or_downstream'),'created_at_utc'=>gmdate('c'),'payload'=>$candidate,'direct_publish_allowed'=>false];
        $state['research_candidates'][]=$row;$state['history'][]=['type'=>'RESEARCH_CANDIDATE_ADDED','candidate_id'=>$id,'recorded_at_utc'=>$row['created_at_utc']];self::save($project_id,$state);return $row;
    }
    private static function key(string $project_id):string{return 'apkw_lifecycle_'.substr(hash('sha256',APKW_MASTER_CONTRACT_ID.'|'.trim($project_id)),0,40);}
}
