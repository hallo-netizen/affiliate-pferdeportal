<?php
// REAL-LIVE-ORACLE replay. Test-only. No production writes outside this disposable WP/MariaDB instance.
$GLOBALS['replay_fail']=array();
function rfatal($m){fwrite(STDERR,"FATAL ".$m."\n");exit(2);}
function rcheck($ok,$name,$detail=''){echo ($ok?'PASS ':'FAIL ').$name.($detail!==''?' :: '.$detail:'')."\n";if(!$ok)$GLOBALS['replay_fail'][]=$name;}

if(!class_exists('Pferdeportal_Affiliate_Router')) rfatal('plugin class missing');
if(Pferdeportal_Affiliate_Router::VERSION!=='6.72.185') rfatal('wrong version '.Pferdeportal_Affiliate_Router::VERSION);
$o=Pferdeportal_Affiliate_Router::instance();
$rm=function($name)use($o){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m;};
$rp=function($name)use($o){$p=new ReflectionProperty($o,$name);$p->setAccessible(true);return $p;};
$call=function($name,...$args)use($rm,$o){return $rm($name)->invokeArgs($o,$args);};
$rc=new ReflectionClass($o); $const=$rc->getConstants();

update_option('ppar_enabled','1',false);
update_option('ppar_assignments_v1',array(),false);
delete_option('ppar_debug');

$call('maybe_install_creative_library_schema');
$call('maybe_install_output_objects_schema');
if(method_exists($o,'maybe_install_control_contract_schema')) $call('maybe_install_control_contract_schema');

// Provider state: exact live networks/advertiser IDs, but no external provider calls.
$call('persist_network_settings','adcell',array(
  'enabled'=>1,'username'=>'live-replay-user','password'=>'live-replay-pass',
  'base_url'=>'https://www.adcell.de/api/v2/','test_path'=>'','csv_feed_url'=>''
));
$call('persist_network_settings','awin',array(
  'enabled'=>1,'publisher_id'=>'2990695','access_token'=>'live-replay-token','feed_api_key'=>''
));
$portalKey=sanitize_key((string)$call('output_local_portal_key'));
if($portalKey==='') rfatal('local portal key missing');
if(!empty($const['OPTION_NETWORK_AWIN_PROGRAMMES'])){
  update_option($const['OPTION_NETWORK_AWIN_PROGRAMMES'],array(
    array('id'=>118619,'name'=>'Cleos','relationship'=>'joined')
  ),false);
}
if(!empty($const['OPTION_AWIN_PROGRAMME_GATE'])){
  update_option($const['OPTION_AWIN_PROGRAMME_GATE'],array(
    '118619'=>array('status'=>'allow_local','portal_key'=>$portalKey,'programme_name'=>'Cleos','updated_at'=>time(),'updated_by'=>1)
  ),false);
}

// No tracking links are ever called. Destination health requests during planning are stubbed as already healthy.
// Frontend phase is counted separately and must perform zero HTTP.
$phase='planning'; $http=array('planning'=>0,'frontend'=>0);
add_filter('pre_http_request',function($pre,$args,$url)use(&$phase,&$http){
  if(!isset($http[$phase]))$http[$phase]=0; $http[$phase]++;
  return array('headers'=>array(),'body'=>'','response'=>array('code'=>200,'message'=>'OK'),'cookies'=>array(),'filename'=>null);
},PHP_INT_MAX,3);

// Exact LIVE page IDs, titles, slugs and parents captured read-only from pferde-atelier.de.
$pages=array(
  95=>array('Ausrüstung','ausruestung',0),
  103=>array('Decken','ausruestung-decken',95),
  104=>array('Halfter & Stricke','ausruestung-halfter-stricke',95),
  105=>array('Pflege','ausruestung-pflege',95),
  106=>array('Reiterbedarf','ausruestung-reiterbedarf',95),
  107=>array('Stall & Weide','ausruestung-stall-weide',95),
  108=>array('Sattel & Zubehör','ausruestung-sattel',95),
  109=>array('Trensen & Gebisse','ausruestung-trensen-gebisse',95),
  162=>array('Pferdedecken','pferdedecken',103),
  163=>array('Regendecken','regendecken',103),
  164=>array('Winterdecken','winterdecken',103),
  165=>array('Fliegendecken','fliegendecken',103),
  166=>array('Abschwitzdecken','abschwitzdecken',103),
  167=>array('Ekzemerdecken','ekzemerdecken',103),
  168=>array('Ausreitdecken','ausreitdecken',103),
  169=>array('Halfter','halfter',104),
  170=>array('Fohlenhalfter','fohlenhalfter',104),
  171=>array('Lederhalfter','lederhalfter',104),
  172=>array('Knotenhalfter','knotenhalfter',104),
  173=>array('Führstricke','fuehrstricke',104),
  174=>array('Anbindestricke','anbindestricke',104),
  175=>array('Bodenarbeitsseile','bodenarbeitsseile',104),
  176=>array('Putzzeug','putzzeug',105),
  177=>array('Putzboxen','putzboxen',105),
  178=>array('Putzkisten','putzkisten',105),
  179=>array('Putzschränke','putzschraenke',105),
  180=>array('Striegel','striegel',105),
  181=>array('Kardätschen','kardaetschen',105),
  182=>array('Hufpflege','hufpflege',105),
  183=>array('Reithosen','reithosen',106),
  184=>array('Reitstiefel','reitstiefel',106),
  185=>array('Reithandschuhe','reithandschuhe',106),
  186=>array('Reithelme','reithelme',106),
  187=>array('Sicherheitswesten','sicherheitswesten',106),
  188=>array('Reitjacken','reitjacken',106),
  189=>array('Turnierbekleidung','turnierbekleidung',106),
  190=>array('Futtertröge','futtertroege',107),
  191=>array('Heuraufen','heuraufen',107),
  192=>array('Satteldecken','satteldecken',108),
  193=>array('Schabracken','schabracken',108),
  194=>array('Sattelgurte','sattelgurte',108),
  195=>array('Steigbügel','steigbuegel',108),
  196=>array('Sattelschränke','sattelschraenke',108),
  197=>array('Satteltransport','satteltransport',108),
  972134=>array('Pferdesättel','pferdesaettel',108),
  198=>array('Englische Trensen','englische-trensen',109),
  199=>array('Gebisse','gebisse',109),
  200=>array('Gebisslose Zäumungen','gebisslose-zaeumungen',109),
  201=>array('Zügel','zuegel',109),
  202=>array('Sperrriemen','sperrriemen',109),
  203=>array('Reithalfter','reithalfter',109),
  972141=>array('Trensen','trensen',109)
);
foreach($pages as $id=>$p){
  if(get_post($id)){wp_delete_post($id,true);}
  $made=wp_insert_post(array(
    'import_id'=>$id,'post_type'=>'page','post_status'=>'publish','post_title'=>$p[0],
    'post_name'=>$p[1],'post_parent'=>$p[2],'post_content'=>''
  ),true);
  if(is_wp_error($made)||absint($made)!==absint($id)) rfatal('page exact-id create failed '.$id.' got '.(is_wp_error($made)?$made->get_error_message():$made));
}
clean_post_cache(95);

// Exact live oracle captured read-only: visible creative per real page.
$live=array(
  103=>'607373',104=>'391771',105=>'607373',106=>'452177',107=>'391771',108=>'607373',109=>'452177',
  162=>'374472',163=>'393901',164=>'467974',165=>'452177',166=>'607373',167=>'375241',168=>'awin4654108',
  169=>'322270',170=>'393901',171=>'467974',172=>'452177',173=>'607373',174=>'375241',175=>'awin4654108',
  176=>'322270',177=>'391771',178=>'467974',179=>'452177',180=>'607373',181=>'375241',182=>'awin4654108',
  183=>'322270',184=>'391771',185=>'467974',186=>'452177',187=>'607373',188=>'375241',189=>'awin4654108',
  190=>'322270',191=>'391771',
  192=>'391771',193=>'467974',194=>'452177',195=>'607373',196=>'375241',197=>'awin4654108',972134=>'322674',
  198=>'322270',199=>'374472',200=>'393901',201=>'467974',202=>'452177',203=>'607373',972141=>'awin4654108'
);

// Exact real banners observed live, plus exact no-follow destination redirects and advertiser IDs.
$banners=array(
  array('adcell','12248','Lax Tierfutter','374472','https://t.adcell.com/p/image?promoId=374472&slotId=98720','https://t.adcell.com/p/click?promoId=374472&slotId=98720','https://www.lax-tierfutter.de/?bid=374472-98720-'),
  array('adcell','13043','Procavallo','393901','https://t.adcell.com/p/image?promoId=393901&slotId=98720','https://t.adcell.com/p/click?promoId=393901&slotId=98720','https://www.procavallo.de/online-designer?bid=393901-98720-'),
  array('adcell','14256','SanoVet','467974','https://t.adcell.com/p/image?promoId=467974&slotId=98720','https://t.adcell.com/p/click?promoId=467974&slotId=98720','https://www.sanovet.com/Anwendungsgebiete/?bid=467974-98720-'),
  array('adcell','14332','VetriGold','452177','https://t.adcell.com/p/image?promoId=452177&slotId=98720','https://t.adcell.com/p/click?promoId=452177&slotId=98720','https://www.vetrigold.de/?touchpoint=452177-98720&pubid=248502&atxs=acg&bid=452177-98720-'),
  array('adcell','17148','Hotti24','607373','https://t.adcell.com/p/image?promoId=607373&slotId=98720','https://t.adcell.com/p/click?promoId=607373&slotId=98720','https://www.hotti24.de/?utm_source=adcell&utm_medium=affiliate&utm_campaign=banner&bid=607373-98720-'),
  array('adcell','7276','Vetevo','375241','https://t.adcell.com/p/image?promoId=375241&slotId=98720','https://t.adcell.com/p/click?promoId=375241&slotId=98720','https://vetevo.de/collections/alle-produkte?f_tierart=F_Hund&utm_source=adcell&utm_medium=affiliate&utm_campaign=hund&utm_content=728x90&klar_source=adcell&bid=375241-98720-'),
  array('adcell','10787','HKM','322270','https://t.adcell.com/p/image?promoId=322270&slotId=98720','https://t.adcell.com/p/click?promoId=322270&slotId=98720','https://www.hkm-sports.com/de/kollektionen/lyon.html?bid=322270-98720-'),
  array('adcell','13043','Procavallo','391771','https://t.adcell.com/p/image?promoId=391771&slotId=98720','https://t.adcell.com/p/click?promoId=391771&slotId=98720','https://www.procavallo.de/online-designer?bid=391771-98720-'),
  array('adcell','10787','HKM','322674','https://t.adcell.com/p/image?promoId=322674&slotId=98720','https://t.adcell.com/p/click?promoId=322674&slotId=98720','https://www.hkm-sports.com/de/reiter/reithelme-sicherheitswesten/reithelme.html?utm_source=affiliate&utm_medium=banner&utm_campaign=Reithelme&bid=322674-98720-'),
  array('adcell','10787','HKM','321102','https://t.adcell.com/p/image?promoId=321102&slotId=98720','https://t.adcell.com/p/click?promoId=321102&slotId=98720','https://www.hkm-sports.com/de/sale.html?utm_source=affiliate&utm_medium=banner&utm_campaign=sale&bid=321102-98720-'),
  array('awin','118619','Cleos','4654108','https://www.awin1.com/cshow.php?s=4654108&v=118619&q=593761&r=2990695','https://www.awin1.com/cread.php?s=4654108&v=118619&q=593761&r=2990695','https://www.cleos.de/produkt/kleintierversicherung?utm_source=awin&utm_content=4654108&utm_medium=2990695')
);

$table=$call('creative_library_table');
$created=array();
foreach($banners as $b){
  list($provider,$partnerId,$partnerName,$external,$image,$tracking,$destination)=$b;
  $raw=array(
    'creative_id'=>$external,'creative_type'=>'banner','creative_title'=>$partnerName.' '.$external,
    'creative_description'=>'','creative_tag'=>'','image_source'=>$image,
    'destination_url'=>$destination,'tracking_url'=>$tracking,'width'=>'728','height'=>'90','status'=>'active'
  );
  $mapping=$call('creative_library_detect_mapping',array_keys($raw));
  $norm=$call('creative_library_normalize_row',$raw,$mapping,array(
    'provider'=>$provider,'partner_external_id'=>$partnerId,'partner_name'=>$partnerName,
    'source_kind'=>'banner','run_uuid'=>'live51-replay'
  ));
  if(is_wp_error($norm))rfatal('normalize '.$external.' '.$norm->get_error_message());
  $norm['width']=728;$norm['height']=90;$norm['topic_status']='auto_verified';
  $payload=json_decode((string)$norm['payload'],true);$payload=is_array($payload)?$payload:array();
  $payload['_dimension_state']='verified';$payload['_dimension_error']='';
  $payload['_image_sha256']=hash('sha256','live-image-'.$external);
  $payload['_image_mime']='image/jpeg';$payload['_image_bytes']=65536;$payload['_measured_at']=time();
  $norm['payload']=wp_json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
  $up=$call('creative_library_upsert',$norm);
  if(!in_array($up,array('imported','updated','unchanged'),true))rfatal('upsert '.$external.' '.print_r($up,true));
  $row=$GLOBALS['wpdb']->get_row($GLOBALS['wpdb']->prepare("SELECT * FROM {$table} WHERE identity_hash=%s",$norm['identity_hash']),ARRAY_A);
  if(!is_array($row))rfatal('creative row missing '.$external);
  $planned=$call('output_plan_creative',$row,true,$portalKey);
  if(!is_array($planned))rfatal('planner result missing '.$external);
  $row=$GLOBALS['wpdb']->get_row($GLOBALS['wpdb']->prepare("SELECT * FROM {$table} WHERE identity_hash=%s",$norm['identity_hash']),ARRAY_A);
  $records=json_decode((string)($row['topic_targets']??''),true);$records=is_array($records)?$records:array();
  echo 'CLASSIFY '.wp_json_encode(array(
    'creative'=>$external,'provider'=>$provider,'partner_id'=>$partnerId,'destination'=>$destination,
    'planner'=>$planned,'topic_targets'=>$records
  ),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
  $created[$external]=array('identity'=>$norm['identity_hash'],'records'=>$records,'planned'=>$planned);
}

// Force all request-local campaign/rank caches to refill from the materialized state.
try{$rp('campaigns_request_cache')->setValue($o,null);}catch(Throwable $e){}
foreach(array('ranked_campaigns_request_cache','ranked_campaign_candidate_index_request_cache','ranked_campaign_raw_records_request_cache','ranked_campaign_from_post_request_cache') as $prop){
  try{$rp($prop)->setValue($o,array());}catch(Throwable $e){}
}

// 1:1 context contract checks from live hierarchy.
$getctx=function($id)use($call){return $call('get_content_context',$id);};
$ctx193=$getctx(193); $ctx186=$getctx(186);
echo 'CONTEXT193 '.wp_json_encode($ctx193,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
echo 'CONTEXT186 '.wp_json_encode($ctx186,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
rcheck(absint(get_post(193)->post_parent)===108,'real_schabracken_parent_108');
rcheck(sanitize_key((string)Pferde_Template_Kit::affiliate_page_type(193))==='category','real_schabracken_design_type_category');
rcheck(sanitize_key((string)Pferde_Template_Kit::affiliate_page_type(186))==='category','real_reithelme_design_type_category');

// Classification sanity: current source must derive the obvious Reithelme edge itself.
// No expected target was inserted into the creative input.
$helmetRecords=$created['322674']['records']??array();
$helmetJson=wp_json_encode($helmetRecords,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
rcheck(strpos($helmetJson,'page:186')!==false,'raw_destination_derives_real_reithelme_page_186',$helmetJson);

// Render phase: zero outbound HTTP, real post IDs and real slot by real design context.
$phase='frontend'; $http['frontend']=0;
$render=function($id)use($call){
  $type=sanitize_key((string)Pferde_Template_Kit::affiliate_page_type($id));
  $slot=in_array($type,array('hub1','hub2'),true)?'hub_after_cards':'product_after_category_tiles';
  $html=(string)$call('render_affiliate_slot',$id,$slot,'portal_context','');
  $href='';
  if(preg_match('/href="([^"]+)"/i',$html,$m))$href=html_entity_decode($m[1],ENT_QUOTES,'UTF-8');
  $key='';
  if(strpos($href,'t.adcell.com/')!==false){
    parse_str((string)wp_parse_url($href,PHP_URL_QUERY),$q);$key=(string)($q['promoId']??'');
  }elseif(strpos($href,'awin1.com/')!==false){
    parse_str((string)wp_parse_url($href,PHP_URL_QUERY),$q);$key='awin'.(string)($q['s']??'');
  }
  return array('type'=>$type,'slot'=>$slot,'href'=>$href,'key'=>$key,'html'=>$html);
};

$match=0;$mismatch=0;$oracleRows=array();
$q0=(int)$GLOBALS['wpdb']->num_queries;
foreach($live as $id=>$expected){
  $r=$render($id);
  $ok=$r['key']===$expected;
  if($ok)$match++;else$mismatch++;
  $oracleRows[]=array('id'=>$id,'title'=>get_the_title($id),'type'=>$r['type'],'slot'=>$r['slot'],'live'=>$expected,'local'=>$r['key'],'same'=>$ok,'href'=>$r['href']);
  echo 'REPLAY '.wp_json_encode(end($oracleRows),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
}
$q1=(int)$GLOBALS['wpdb']->num_queries;
echo 'REPLAY_SUMMARY '.wp_json_encode(array(
  'pages'=>count($live),'match'=>$match,'mismatch'=>$mismatch,
  'frontend_http_calls'=>$http['frontend'],'frontend_db_queries_total'=>$q1-$q0,
  'planning_http_calls_stubbed'=>$http['planning']
),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";

rcheck(count($live)===51,'live_oracle_has_51_pages');
rcheck($http['frontend']===0,'frontend_zero_http_calls','calls='.$http['frontend']);

// Critical live divergences / matches are printed explicitly. Do not force the fixture to fit the oracle.
$byId=array();foreach($oracleRows as $x)$byId[$x['id']]=$x;
echo 'CRITICAL_REITHELME '.wp_json_encode($byId[186]??array(),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
echo 'CRITICAL_SCHABRACKEN '.wp_json_encode($byId[193]??array(),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
echo 'CRITICAL_PFERDESAETTEL '.wp_json_encode($byId[972134]??array(),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";

if($mismatch>0){
  echo "REAL51_REPLAY_DIVERGENCE_PROVEN mismatches=$mismatch matches=$match\n";
  echo "INTERPRETATION current 6.72.185 plus real raw pages/banners does not recreate live persisted output state; persistent live state is therefore materially different and must not be guessed.\n";
}else{
  echo "REAL51_REPLAY_EXACT_MATCH_51_OF_51\n";
}
if($GLOBALS['replay_fail']){echo 'HARD_FAILURES '.wp_json_encode($GLOBALS['replay_fail'])."\n";exit(1);}
echo "REAL51_REPLAY_GATE_COMPLETE\n";
