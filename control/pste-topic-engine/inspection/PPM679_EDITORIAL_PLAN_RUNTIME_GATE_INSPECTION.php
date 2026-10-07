<?php
require __DIR__.'/bootstrap-test.php';

PPM679_WP::reset_test_state();
$errors=PPM679_Editorial_Plan_Registry::validate();
ppm_test_assert($errors===array(),'editorial registry must validate');
$summary=PPM679_Editorial_Plan_Registry::summary();
ppm_test_assert($summary['portal_categories']===1124,'1124 portal categories');
ppm_test_assert($summary['journal_categories']===9,'9 journal categories');
ppm_test_assert($summary['total_slots']===5665,'5665 canonical plan slots');
ppm_test_assert($summary['publish_allowed']===false,'publish forbidden');
ppm_test_assert($summary['wissen_draft_allowed']===false,'Wissen draft blocked');

$journal=PPM679_Journal_Content_Block_Validator::read_only_live_snapshot();
ppm_test_assert($journal['ok']===true,'journal read-only snapshot pass');
ppm_test_assert(count($journal['snapshot']['terms'])===9,'journal snapshot contains nine terms');
ppm_test_assert($journal['snapshot']['hub']['ID']===9886,'journal hub id 9886');
ppm_test_assert($journal['snapshot']['hub']['post_type']==='page','journal hub is page');
ppm_test_assert($journal['snapshot']['wordpress_write_performed']===false,'journal snapshot performs no write');

$source=PPM679_Editorial_Plan_Registry::source();
ppm_test_assert(count($source['categories'])===1124,'full portal source categories');
$plan=PPM679_Editorial_Plan_Registry::plan();
$per=array();foreach($plan['slots'] as $slot){$per[$slot['stable_category_id']]=($per[$slot['stable_category_id']]??0)+1;}
ppm_test_assert(count($per)===1133,'1124 portal plus 9 journal category identities');
ppm_test_assert(count(array_filter($per,function($n){return $n!==5;}))===0,'every category has five slots');
ppm_test_assert(count(array_filter($plan['slots'],function($s){return strtolower($s['article_type'])==='journal';}))===45,'45 Journal plan slots');
ppm_test_assert(count(array_filter($plan['slots'],function($s){return strtolower($s['article_type'])==='journal'&&$s['draft_generation_allowed']!==true;}))===0,'Journal slots draft enabled only by signed release');

$legacy=array(
 array('plan_item_key'=>'faq-hufpflege-v4','title'=>'Wie oft sollten Pferdehufe kontrolliert und ausgekratzt werden?','topic'=>'Wie oft sollten Pferdehufe kontrolliert und ausgekratzt werden?','article_type'=>'FAQ','category_slug'=>''),
 array('plan_item_key'=>'beratung-putzbuersten-v4','title'=>'Welche Putzbürste passt für welchen Zweck?','topic'=>'Welche Putzbürste passt für welchen Zweck?','article_type'=>'Beratung','category_slug'=>''),
 array('plan_item_key'=>'vergleich-halfter-v4','title'=>'Lederhalfter oder Nylonhalfter – was passt besser?','topic'=>'Lederhalfter oder Nylonhalfter – was passt besser?','article_type'=>'Vergleich','category_slug'=>''),
 array('plan_item_key'=>'pflege-trense-v4','title'=>'Trensenzaum richtig reinigen und pflegen','topic'=>'Trensenzaum richtig reinigen und pflegen','article_type'=>'Pflege','category_slug'=>''),
);
$pre=PPM679_Editorial_Plan_Runtime_Gate::preflight($legacy,'test-v38','production');
ppm_test_assert($pre['ok']===true,'four-type first wave preflight pass');
ppm_test_assert(count($pre['bindings'])===4,'four bindings');

$five=$legacy;$five[]=$legacy[0];
$wave_errors=PPM679_Production_Wave_Governor::validate($five);
ppm_test_assert(count($wave_errors)>=2,'five item and duplicate type blocked');
$wissen_errors=PPM679_Journal_Content_Block_Validator::block_wissen_generation('Wissen');
ppm_test_assert(count($wissen_errors)===1&&$wissen_errors[0]['error_code']==='BLOCKED_WISSEN_ARTICLE_TYPE_NOT_RELEASED','Wissen hard blocked');

# Technical test artifacts do not count as production coverage and do not block regular production.
PPM679_WP::seed_test_post(array('ID'=>10205,'post_title'=>'[LT4-250-458A3B05] Was muss vor einer Fahrt mit Pferdeanhänger geprüft werden?','post_name'=>'test','post_status'=>'trash','post_type'=>'post','meta'=>array('_ppm679_test_marker'=>'LT4-250-458A3B05'),'category_ids'=>array()));
$technical_candidate=array(array('canonical_article_id'=>'canonical-faq-001','plan_item_key'=>'canonical-faq-001','title'=>'Was muss vor einer Fahrt mit Pferdeanhänger geprüft werden?','article_type'=>'FAQ','category_slug'=>'checklisten-fuer-pferdeanhaenger-faq'));
$tech_pre=PPM679_Editorial_Plan_Runtime_Gate::preflight($technical_candidate,'test-tech','technical_evidence');
ppm_test_assert($tech_pre['ok']===true,'failed/trash technical artifact does not block authorized evidence');

# One successful technical evidence blocks another technical evidence run.
PPM679_WP::seed_test_post(array('ID'=>10362,'post_title'=>'Was muss vor einer Fahrt mit Pferdeanhänger geprüft werden?','post_name'=>'control','post_status'=>'draft','post_type'=>'post','meta'=>array('_ppm679_test_marker'=>'LT2','_ppm679_canonical_article_id'=>'canonical-faq-001'),'category_ids'=>array(1048)));
$tech_again=PPM679_Editorial_Plan_Runtime_Gate::preflight($technical_candidate,'test-tech-again','technical_evidence');
ppm_test_assert($tech_again['ok']===false&&$tech_again['status']==='BLOCKED_DUPLICATE_TECHNICAL_EVIDENCE_ALREADY_EXISTS','second successful technical evidence blocked');

# Published content blocks silent recreation.
PPM679_WP::reset_test_state();
$slot=PPM679_Editorial_Plan_Registry::find_slot(array('plan_item_key'=>'faq-hufpflege-v4'));
ppm_test_assert(is_array($slot),'legacy slot resolved');
PPM679_WP::seed_test_post(array('ID'=>20001,'post_title'=>$slot['working_title'],'post_name'=>'existing','post_status'=>'publish','post_type'=>'post','meta'=>array('_ppm679_canonical_article_id'=>$slot['canonical_article_id']),'category_ids'=>array()));
$duplicate=PPM679_Editorial_Plan_Runtime_Gate::preflight(array(array('canonical_article_id'=>$slot['canonical_article_id'],'title'=>$slot['working_title'],'article_type'=>$slot['article_type'],'category_slug'=>$slot['category_slug'])),'test-duplicate','production');
ppm_test_assert($duplicate['ok']===false&&$duplicate['status']==='BLOCKED_SYSTEMWIDE_CONTENT_DUPLICATE','published duplicate blocked');

# Reimport is versioned and fail closed.
$old=array(array('stable_category_id'=>'journal:a','name'=>'A','slug'=>'a','content_block'=>'journal','allowed_article_types'=>array('wissen'),'active'=>true));
$add=$old;$add[]=array('stable_category_id'=>'journal:b','name'=>'B','slug'=>'b','content_block'=>'journal','allowed_article_types'=>array('wissen'),'active'=>true);
$r=PPM679_Category_Reimport_Validator::compare($old,$add);
ppm_test_assert($r['ok']===true&&$r['changes'][0]['change_type']==='ADD','additive category import proposed');
$ren=array(array('stable_category_id'=>'journal:a','name'=>'A neu','slug'=>'a-neu','content_block'=>'journal','allowed_article_types'=>array('wissen'),'active'=>true));
$r=PPM679_Category_Reimport_Validator::compare($old,$ren);
ppm_test_assert($r['ok']===true&&$r['changes'][0]['status']==='BLOCKED_PENDING_EXPLICIT_APPROVAL','rename never silently applied');
$collision=$add;$collision[1]['slug']='a';
$r=PPM679_Category_Reimport_Validator::compare($old,$collision);
ppm_test_assert($r['ok']===false&&$r['status']==='BLOCKED_CATEGORY_REIMPORT_SLUG_COLLISION','slug collision blocked');

# Runtime plan state is separate from the master and updated only after draft readback.
PPM679_WP::reset_test_state();
$state=PPM679_Editorial_Plan_Runtime_Gate::record_readback(array(array('canonical_article_id'=>$slot['canonical_article_id'],'plan_slot_sha256'=>'abc','inventory_snapshot_sha256'=>'def')),array(array('post_id'=>30001,'post_status'=>'draft','canonical_article_id'=>$slot['canonical_article_id'],'content_hash'=>'123')));
ppm_test_assert($state['ok']===true,'runtime state write through protected adapter');
$stored=PPM679_WP::get_option('ppm679_editorial_plan_runtime_state_v1',array());
ppm_test_assert(isset($stored['items'][$slot['canonical_article_id']]),'runtime state persisted separately');
ppm_test_assert($stored['items'][$slot['canonical_article_id']]['publish_allowed']===false,'runtime state no publish');

$out=array(
 'status'=>'PASS_V38_EDITORIAL_PLAN_JOURNAL_SYSTEMWIDE_DEDUP',
 'portal_categories'=>1124,'journal_categories'=>9,'canonical_plan_slots'=>5665,
 'inventory_baseline_counts'=>array('publish'=>12,'draft'=>3,'trash'=>24),
 'wissen_planning'=>true,'wissen_draft_generation'=>false,
 'initial_wave_max_drafts'=>4,'automatic_publish_allowed'=>false,
 'journal_read_only_snapshot'=>true,'category_reimport_fail_closed'=>true,
 'masterfile_is_runtime_database'=>false
);
echo json_encode($out,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_PRETTY_PRINT)."\n";
