<?php
if (!defined('ABSPATH')) { return; }

final class PPM679_Editorial_Plan_Runtime_Gate {
    public static function preflight($candidates,$context='production',$mode='production',$test_inventory=null,$skip_live_journal=false){
        $errors=PPM679_Editorial_Plan_Registry::validate();if($mode==='production'){$errors=array_merge($errors,PPM679_Production_Wave_Governor::validate($candidates));}
        if($errors){return self::blocked($errors,$context);}
        $journal_required=self::requires_live_journal($candidates);$journal=null;if(!$skip_live_journal&&$journal_required){$journal=PPM679_Journal_Content_Block_Validator::read_only_live_snapshot();if(empty($journal['ok'])){return $journal;}}
        $runtime=is_array($test_inventory)?$test_inventory:PPM679_Content_Inventory_Reconciler::runtime_inventory();$reconciled=PPM679_Content_Inventory_Reconciler::reconcile($runtime);
        $dup=PPM679_Systemwide_Duplicate_Guard::preflight($candidates,$reconciled,$mode);if(empty($dup['ok'])){return self::blocked((array)$dup['errors'],$context,array('journal_snapshot'=>$journal['snapshot']??null,'inventory'=>$reconciled,'bindings'=>$dup['bindings']??array()));}
        $report=PPM679_Diagnostic::ok('EDITORIAL_PLAN_INVENTORY_JOURNAL_AND_SYSTEMWIDE_DUPLICATE_PREFLIGHT_PASS',$context,'',array('bindings'=>$dup['bindings'],'journal_live_verification_required'=>$journal_required,'journal_snapshot'=>$journal['snapshot']??null,'inventory_snapshot'=>$reconciled['runtime_snapshot'],'canonical_group_count'=>$reconciled['canonical_group_count'],'draft_allowed'=>true,'publish_allowed'=>false,'write_attempted'=>false));
        return array('ok'=>true,'status'=>$report['status'],'report'=>$report,'bindings'=>$dup['bindings'],'inventory'=>$reconciled,'journal'=>$journal,'publish_allowed'=>false,'write_attempted'=>false);
    }
    public static function record_readback($bindings,$readback_items,$context='draft_readback'){
        $state=(array)PPM679_WP::get_option('ppm679_editorial_plan_runtime_state_v1',array('contract'=>'PPM679_EDITORIAL_PLAN_RUNTIME_STATE_V1','items'=>array(),'updated_at'=>null));
        foreach((array)$bindings as $binding){$cid=(string)($binding['canonical_article_id']??'');if($cid===''){continue;}$match=null;foreach((array)$readback_items as $item){if((string)($item['canonical_article_id']??'')===$cid||count($readback_items)===1){$match=$item;break;}}$state['items'][$cid]=array('canonical_article_id'=>$cid,'status'=>'DRAFT_CREATED_READBACK_PASS','post_id'=>(int)($match['post_id']??0),'post_status'=>(string)($match['post_status']??'draft'),'content_hash'=>(string)($match['content_hash']??''),'plan_slot_sha256'=>(string)($binding['plan_slot_sha256']??''),'inventory_snapshot_sha256'=>(string)($binding['inventory_snapshot_sha256']??''),'updated_at'=>gmdate('c'),'publish_allowed'=>false);}
        $state['updated_at']=gmdate('c');$state['state_sha256']=PPM679_Diagnostic::stable_hash($state);$ok=PPM679_WP::update_option('ppm679_editorial_plan_runtime_state_v1',$state);return array('ok'=>$ok,'status'=>$ok?'EDITORIAL_RUNTIME_STATE_UPDATED':'BLOCKED_EDITORIAL_RUNTIME_STATE_WRITE','state'=>$state,'publish_allowed'=>false);
    }
    private static function requires_live_journal($candidates){
        $journal=PPM679_Editorial_Plan_Registry::journal();$journal_slugs=array();
        foreach((array)($journal['categories']??array()) as $category){$slug=trim((string)($category['slug']??''));if($slug!==''){$journal_slugs[$slug]=true;}}
        foreach((array)$candidates as $candidate){
            $candidate=is_array($candidate)?$candidate:array();
            $type=strtolower(trim((string)($candidate['article_type']??'')));
            $canonical_id=trim((string)($candidate['canonical_article_id']??''));
            $category_slug=trim((string)($candidate['category_slug']??''));
            if($type==='wissen'||$type==='journal'||strpos($canonical_id,'journal:')===0||isset($journal_slugs[$category_slug])){return true;}
            $slot=PPM679_Editorial_Plan_Registry::find_slot($candidate);
            if(is_array($slot)){
                $content_block=strtolower(trim((string)($slot['content_block']??'')));
                $stable_category_id=(string)($slot['stable_category_id']??'');
                if($content_block==='journal'||strpos($stable_category_id,'journal:')===0||in_array(strtolower((string)($slot['article_type']??'')),array('wissen','journal'),true)){return true;}
            }
        }
        return false;
    }
    private static function blocked($errors,$context,$extra=array()){return array('ok'=>false,'status'=>(string)($errors[0]['error_code']??'BLOCKED_EDITORIAL_PREFLIGHT'),'report'=>PPM679_Diagnostic::blocked((string)($errors[0]['error_code']??'BLOCKED_EDITORIAL_PREFLIGHT'),$errors,$context,'',array_merge(array('write_attempted'=>false),$extra)),'publish_allowed'=>false,'write_attempted'=>false);}
}
