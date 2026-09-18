<?php
if (!defined('ABSPATH')) { return; }

final class PPM679_Systemwide_Duplicate_Guard {
    public static function preflight($candidates,$inventory,$mode='production'){
        $errors=array();$bindings=array();$batch_titles=array();$batch_ownership=array();
        $items=(array)($inventory['runtime_snapshot']['items']??$inventory['items']??array());
        foreach((array)$candidates as $i=>$candidate){
            $slot=PPM679_Editorial_Plan_Registry::find_slot($candidate);
            if(!is_array($slot)){$errors[]=self::err('BLOCKED_EDITORIAL_PLAN_SLOT_UNRESOLVED','EVERY_CANDIDATE_MUST_RESOLVE_TO_EXACT_CANONICAL_PLAN_SLOT','candidates['.$i.']','one canonical plan slot',$candidate,'Der Beitrag ist nicht eindeutig im vollständigen Redaktionsplan gebunden.',$i);continue;}
            $wissen=PPM679_Journal_Content_Block_Validator::block_wissen_generation($slot['article_type']??'');if($wissen){$errors=array_merge($errors,$wissen);continue;}
            if(($slot['draft_generation_allowed']??false)!==true){$errors[]=self::err('BLOCKED_EDITORIAL_PLAN_SLOT_NOT_PRODUCTION_ENABLED','PLAN_SLOT_MUST_BE_EXPLICITLY_DRAFT_ENABLED','plan.'.$slot['canonical_article_id'].'.draft_generation_allowed',true,$slot['draft_generation_allowed']??null,'Diese Planposition ist noch nicht für die Entwurfserzeugung freigegeben.',$i);continue;}
            $title=PPM679_Editorial_Plan_Registry::normalize_title((string)($candidate['title']??$candidate['topic']??$slot['working_title']??''));$cid=(string)$slot['canonical_article_id'];$ownership=(string)$slot['keyword_ownership_key'];
            if(isset($batch_titles[$title])||isset($batch_ownership[$ownership])){$errors[]=self::err('BLOCKED_BATCH_DUPLICATE_INTENT','ONE_BATCH_MUST_NOT_CONTAIN_DUPLICATE_TITLE_OR_KEYWORD_OWNERSHIP','candidates['.$i.']',array('unique title','unique ownership'),array('title'=>$title,'ownership'=>$ownership),'Der Produktionslauf enthält intern eine Dublette.',$i);continue;}
            $batch_titles[$title]=true;$batch_ownership[$ownership]=true;
            foreach($items as $existing){$ex=PPM679_Content_Inventory_Reconciler::classify($existing);$same_cid=$ex['canonical_article_id']!==''&&$ex['canonical_article_id']===$cid;$same_title=$ex['normalized_title']!==''&&$ex['normalized_title']===$title;if(!$same_cid&&!$same_title){continue;}
                $role=(string)$ex['inventory_role'];
                if(in_array($role,array('TECHNICAL_EVIDENCE_FAILED','TECHNICAL_TEST_ARTIFACT'),true)){continue;}
                if($mode==='technical_evidence'&&$role==='TECHNICAL_EVIDENCE_SUCCESS'){$errors[]=self::err('BLOCKED_DUPLICATE_TECHNICAL_EVIDENCE_ALREADY_EXISTS','ONLY_ONE_SUCCESSFUL_TECHNICAL_EVIDENCE_DRAFT_PER_CANONICAL_ARTICLE','inventory.posts.'.$ex['post_id'],'no prior successful evidence',$ex,'Für diese kanonische Artikelidentität existiert bereits ein erfolgreicher Kontrollentwurf.',$i);continue 2;}
                if($mode==='technical_evidence'&&$role==='REGULAR_DRAFT_REVIEW_REQUIRED'){continue;}
                $errors[]=self::err('BLOCKED_SYSTEMWIDE_CONTENT_DUPLICATE','PUBLISHED_DRAFT_OR_NONTECHNICAL_TRASH_CONTENT_MUST_BLOCK_SILENT_RECREATION','inventory.posts.'.$ex['post_id'],'no blocking canonical duplicate',$ex,'Das Thema existiert bereits veröffentlicht, als regulärer Entwurf oder als nicht geklärter Papierkorbbeitrag.',$i);continue 2;
            }
            $bindings[]=array('candidate_index'=>$i,'canonical_article_id'=>$cid,'stable_category_id'=>$slot['stable_category_id'],'category_slug'=>$slot['category_slug'],'article_type'=>$slot['article_type'],'keyword_ownership_key'=>$ownership,'plan_slot_sha256'=>PPM679_Diagnostic::stable_hash($slot),'inventory_snapshot_sha256'=>(string)($inventory['runtime_snapshot']['snapshot_sha256']??$inventory['snapshot_sha256']??''));
        }
        if($errors){return array('ok'=>false,'status'=>(string)$errors[0]['error_code'],'errors'=>$errors,'bindings'=>$bindings,'publish_allowed'=>false);}
        return array('ok'=>true,'status'=>'SYSTEMWIDE_DUPLICATE_AND_OWNERSHIP_GATE_PASS','errors'=>array(),'bindings'=>$bindings,'publish_allowed'=>false);
    }
    private static function err($code,$rule,$path,$expected,$actual,$reason,$index=null){return PPM679_Diagnostic::error($code,$rule,$path,$expected,$actual,$reason,'systemwide_duplicate_guard','',__CLASS__,$index,array(PPM679_Editorial_Plan_Registry::PLAN,PPM679_Editorial_Plan_Registry::INVENTORY));}
}
