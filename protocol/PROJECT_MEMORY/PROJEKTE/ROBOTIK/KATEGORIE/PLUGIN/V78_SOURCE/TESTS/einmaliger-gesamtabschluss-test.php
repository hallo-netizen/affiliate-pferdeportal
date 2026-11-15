<?php
/** V78 fixture: one approval, preexisting index 16, automatic 227 -> 68 -> 64. */
declare(strict_types=1);
define('ABSPATH','/test/');
$options=[];$changes=[];
function current_user_can($cap):bool{return true;}
function get_option($key,$fallback=[]){global $options;return $options[$key]??$fallback;}
function update_option($key,$value,$autoload=false){global $options,$changes;$options[$key]=$value;$changes[$key]=($changes[$key]??0)+1;return true;}
function add_option($key,$value,$deprecated='',$autoload='no'){global $options;if(isset($options[$key]))return false;$options[$key]=$value;return true;}
function delete_option($key){global $options;unset($options[$key]);return true;}
function add_action($action,$handler,$priority=10){return true;}
function check(bool $ok,string $what):void{if(!$ok)throw new RuntimeException('FAIL '.$what);echo "PASS $what\n";}
class Robotik_V63_Delta {
    public static int $write=0;
    public static function prepare():array{return ['errors'=>[],'task_count'=>227,'task_done'=>0,'task_remaining'=>227,'prior_wp_page_ids'=>[],'prior_wp_term_ids'=>[]];}
    public static function resumeSaved():void {global $options;$s=$options['robotik_v63_delta_state'];if($s['status']!=='BLOCKED')throw new Exception('resume only blocked');$s['status']='WRITING';$options['robotik_v63_delta_state']=$s;}
    public static function advance():array {global $options;$s=$options['robotik_v63_delta_state'];if($s['status']!=='WRITING')throw new Exception('wrong import state');$s['index']=min(227,$s['index']+32);self::$write++;if($s['index']===227){$s['status']='COMPLETE_SAFE_DELTA_WITH_16_HOLDS';$s['verified']=227;} $options['robotik_v63_delta_state']=$s;return $s;}
}
class Robotik_V65_Publication {
    public static int $write=0;
    public static function preview():array{return ['ready'=>true,'items'=>array_fill(0,68,['id'=>1]),'drafts'=>68,'published'=>0];}
    public static function resumeSaved():void {global $options;$s=$options['robotik_v65_publication_state'];if($s['status']!=='BLOCKED')throw new Exception('resume only blocked');$s['status']='WRITING';$options['robotik_v65_publication_state']=$s;}
    public static function advance():array {global $options;$s=$options['robotik_v65_publication_state'];if($s['status']!=='WRITING')throw new Exception('wrong publish state');$s['index']=min(68,$s['index']+22);self::$write++;if($s['index']===68){$s['status']='COMPLETE';$s['verified']=68;} $options['robotik_v65_publication_state']=$s;return $s;}
}
class Robotik_V77_Fachnachtrag {
    public static int $write=0;
    public static function plan():array{return ['errors'=>[],'tasks'=>array_fill(0,64,['kind'=>'page']),'done'=>0,'remaining'=>64,'prior_pages'=>[],'prior_terms'=>[]];}
    public static function resumeSaved():void {global $options;$s=$options['robotik_v77_fachnachtrag_state'];if($s['status']!=='BLOCKED')throw new Exception('resume only blocked');$s['status']='WRITING';$options['robotik_v77_fachnachtrag_state']=$s;}
    public static function advance():array {global $options;$s=$options['robotik_v77_fachnachtrag_state'];if($s['status']!=='WRITING')throw new Exception('wrong followup state');$s['index']=min(64,$s['index']+16);self::$write++;if($s['index']===64){$s['status']='COMPLETE';$s['verified']=64;} $options['robotik_v77_fachnachtrag_state']=$s;return $s;}
}
$sourceFile=$argv[1]??dirname(__DIR__).'/includes/class-robotik-v78-gesamtabschluss.php';
require $sourceFile;
$manifest=hash_file('sha256',dirname($sourceFile).'/../assets/robotik-v62-sollvorschau.json');
check(strlen($manifest)===64,'real manifest present');
check((Robotik_V78_Gesamtabschluss::advance()['status']??'')!=='COMPLETE','no unattended start');
$options['robotik_v78_gesamtabschluss_state']=['status'=>'RUNNING','phase'=>'uebernehmen','authorized_once'=>true,'manifest'=>$manifest,'error'=>''];
$options['robotik_v63_delta_state']=['status'=>'WRITING','index'=>16,'total'=>227];
$loops=0;
while(($options['robotik_v78_gesamtabschluss_state']['status']??'')==='RUNNING'&&$loops++<32){
    Robotik_V78_Gesamtabschluss::advance();
}
check($loops<32,'single workflow terminates');
check($options['robotik_v78_gesamtabschluss_state']['status']==='COMPLETE','global final status complete');
check($options['robotik_v63_delta_state']['index']===227,'original resumed from 16 of 227');
check($options['robotik_v65_publication_state']['index']===68,'68 published in same flow');
check($options['robotik_v77_fachnachtrag_state']['index']===64,'64 followup actions in same flow');
check(Robotik_V63_Delta::$write===7 && Robotik_V65_Publication::$write===4 && Robotik_V77_Fachnachtrag::$write===4,'single phase order without restart');
check($options['robotik_v78_gesamtabschluss_state']['authorized_once']===true,'one approval persisted');
$previous=Robotik_V63_Delta::$write;Robotik_V78_Gesamtabschluss::advance();
check(Robotik_V63_Delta::$write===$previous,'completed flow cannot run twice');
// A real failure remains blocked, never jumps ahead.
$options['robotik_v78_gesamtabschluss_state']=['status'=>'RUNNING','phase'=>'uebernehmen','authorized_once'=>true,'manifest'=>'NOT_THE_MANIFEST','error'=>''];
Robotik_V78_Gesamtabschluss::advance();
check($options['robotik_v78_gesamtabschluss_state']['status']==='BLOCKED','manifest change blocks instead of writing');
// A paused V63 import continues from the saved index with the same consent.
$options['robotik_v78_gesamtabschluss_state']=['status'=>'RUNNING','phase'=>'uebernehmen','authorized_once'=>true,'manifest'=>$manifest,'error'=>''];
$options['robotik_v63_delta_state']=['status'=>'BLOCKED','index'=>16,'total'=>227];
unset($options['robotik_v65_publication_state'],$options['robotik_v77_fachnachtrag_state']);
Robotik_V78_Gesamtabschluss::advance();
check($options['robotik_v78_gesamtabschluss_state']['status']==='RUNNING','blocked original resumed without renewed approval');
check($options['robotik_v63_delta_state']['index']===48,'blocked original preserves 16 completed steps');
echo "V78 ONE_APPROVAL FULL_FLOW MOCK PASS\n";
