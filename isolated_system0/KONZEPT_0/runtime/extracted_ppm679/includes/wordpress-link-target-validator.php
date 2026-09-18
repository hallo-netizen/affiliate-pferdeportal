<?php
if (!defined('ABSPATH')) { return; }
final class PPM679_WordPress_Link_Target_Validator {
 const CONTRACT_FILE='contracts/wordpress-link-target-snapshot-v1.json';
 private static function load(){ $p=PPM679_PLUGIN_DIR.self::CONTRACT_FILE; $d=is_file($p)?json_decode((string)file_get_contents($p),true):null; return is_array($d)?$d:null; }
 private static function err($code,$rule,$path,$expected,$actual,$reason,$context){return PPM679_Diagnostic::error($code,$rule,$path,$expected,$actual,$reason,$context,'',__CLASS__,null,array(self::CONTRACT_FILE));}
 public static function validate_bound_article($html,$binding,$context='link_target_source'){
  $c=self::load();$errors=array(); if(!is_array($c)){return array(self::err('BLOCKED_LINK_TARGET_SNAPSHOT_MISSING','LINK_TARGET_SNAPSHOT_MUST_EXIST','contract',self::CONTRACT_FILE,null,'Der reale Zielobjekt-Schnappschuss fehlt.',$context));}
  $self=(string)($c['contract_self_sha256']??'');$copy=$c;unset($copy['contract_self_sha256']);if($self===''||!hash_equals($self,PPM679_Diagnostic::stable_hash($copy))){$errors[]=self::err('BLOCKED_LINK_TARGET_SNAPSHOT_HASH','LINK_TARGET_SNAPSHOT_SELF_HASH_MUST_MATCH','contract.contract_self_sha256',PPM679_Diagnostic::stable_hash($copy),$self,'Der Zielobjekt-Schnappschuss wurde verändert.',$context);}
  $targets=array();foreach((array)($c['targets']??array()) as $t){$targets[(string)($t['role']??'')]=$t;}
  $bound=array();foreach((array)($binding['link_bindings']??array()) as $b){$bound[(string)($b['role']??'')]=$b;}
  foreach((array)($c['required_roles']??array()) as $role){$t=$targets[$role]??null;$b=$bound[$role]??null;if(!is_array($t)||!is_array($b)){$errors[]=self::err('BLOCKED_LINK_ROLE_TARGET_MISSING','EVERY_REQUIRED_LINK_ROLE_REQUIRES_REAL_TARGET','links.'.$role,'target and binding',array($t,$b),'Eine Linkrolle ist nicht an ein reales Ziel gebunden.',$context);continue;}
   foreach(array('relative_url'=>'href','declared_object_type'=>'target_type','status'=>'target_status') as $tf=>$bf){if((string)($t[$tf]??'')!==(string)($b[$bf]??'')){$errors[]=self::err('BLOCKED_LINK_TARGET_BINDING','LINK_BINDING_MUST_MATCH_READ_ONLY_STRUCTURE_SNAPSHOT','links.'.$role.'.'.$bf,$t[$tf]??null,$b[$bf]??null,'Das Linkziel weicht vom Struktur-Schnappschuss ab.',$context);}}
   if(!in_array((string)($t['declared_object_type']??''),array('page','category'),true)||($t['status']??'')!=='publish'){$errors[]=self::err('BLOCKED_LINK_TARGET_TYPE_STATUS','LINK_TARGET_MUST_BE_PUBLISHED_PAGE_OR_CATEGORY','links.'.$role,array('page|category','publish'),array($t['declared_object_type']??null,$t['status']??null),'Beiträge, Entwürfe und unbekannte Ziele sind verboten.',$context);}
   $href=(string)($b['href']??'');$anchor=(string)($b['anchor']??'');if($href===''||strpos((string)$html,'href="'.$href.'"')===false||$anchor===''||strpos((string)$html,'>'.$anchor.'</a>')===false){$errors[]=self::err('BLOCKED_LINK_VISIBLE_PAIR','EXACT_REAL_LINK_PAIR_MUST_BE_VISIBLE','links.'.$role,array($href,$anchor),'missing','Das gebundene reale Linkpaar fehlt im Artikel.',$context);}
  }
  foreach(array('führt eine Ebene höher','zulässige Kategorie','im Beitrag','angeblich','Beitrag <a') as $bad){if(stripos(strip_tags((string)$html),$bad)!==false){$errors[]=self::err('BLOCKED_LINK_UNNATURAL_META_SENTENCE','LINK_SENTENCE_MUST_BE_NATURAL_READER_TEXT','content.links.language','no technical meta sentence',$bad,'Technische Linkregel-Sprache darf nicht im Lesertext erscheinen.',$context);}}
  return $errors;
 }
 public static function revalidate_live_before_write($binding,$context='link_target_live_read_only',$override=null){
  $c=self::load();$errors=array();$resolved=array(); if(!is_array($c)){return array('ok'=>false,'report'=>PPM679_Diagnostic::blocked('BLOCKED_LINK_TARGET_SNAPSHOT_MISSING',array(),$context));}
  $map=is_array($override)?$override:null;
  foreach((array)($c['targets']??array()) as $t){$url=(string)($t['canonical_url']??'');$role=(string)($t['role']??'');
   if($map!==null){$r=$map[$role]??array();$id=(int)($r['id']??0);$type=(string)($r['type']??'');$status=(string)($r['status']??'');$parent_url=(string)($r['parent_url']??'');}
   else { $id=function_exists('url_to_postid')?(int)url_to_postid($url):0; $type=$id>0&&function_exists('get_post_type')?(string)get_post_type($id):''; $status=$id>0&&function_exists('get_post_status')?(string)get_post_status($id):''; $parent_url=''; if($id>0&&function_exists('get_post_field')&&function_exists('get_permalink')){$pid=(int)get_post_field('post_parent',$id);$parent_url=$pid>0?(string)get_permalink($pid):'';} }
   if($id<=0||$type!=='page'||$status!=='publish'){$errors[]=self::err('BLOCKED_LINK_LIVE_RESOLUTION','LIVE_READ_ONLY_TARGET_MUST_RESOLVE_TO_PUBLISHED_PAGE','live_links.'.$role,array('id>0','page','publish'),array('id'=>$id,'type'=>$type,'status'=>$status),'Das reale Linkziel konnte vor dem Schreiben nicht sicher bestätigt werden.',$context);}
   $expected_parent=(string)($t['parent_relative_url']??''); if($expected_parent!==''&&$parent_url!==''&&rtrim(parse_url($parent_url,PHP_URL_PATH)??'','/').'/'!==rtrim($expected_parent,'/').'/'){$errors[]=self::err('BLOCKED_LINK_LIVE_PARENT','LIVE_TARGET_PARENT_MUST_MATCH_BOUND_HIERARCHY','live_links.'.$role.'.parent',$expected_parent,$parent_url,'Die reale Hierarchie des Linkziels hat sich geändert.',$context);}
   $resolved[$role]=array('id'=>$id,'type'=>$type,'status'=>$status,'canonical_url'=>$url,'parent_url'=>$parent_url);
  }
  if($errors){return array('ok'=>false,'write_attempted'=>false,'report'=>PPM679_Diagnostic::blocked($errors[0]['error_code'],$errors,$context,'',array('resolved'=>$resolved,'read_only'=>true,'publish_allowed'=>false)));}
  return array('ok'=>true,'status'=>'PASS_LINK_TARGETS_READ_ONLY_REVALIDATED','resolved'=>$resolved,'write_attempted'=>false,'publish_allowed'=>false);
 }
}
