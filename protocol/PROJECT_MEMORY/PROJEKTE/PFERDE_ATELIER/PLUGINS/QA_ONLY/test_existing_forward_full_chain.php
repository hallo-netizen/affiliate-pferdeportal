<?php
declare(strict_types=1);
/**
 * Existing PSTE_Mini_Workflow::forwardToPlan() integration mock. No production WP writes.
 * Run as subprocess: php test_existing_forward_full_chain.php /path/to/patched.php [good|stale|onebad]
 * The real method exits after WP redirection; shutdown observes exact resulting state.
 */
define('ABSPATH','/qa/');
define('ARRAY_A','ARRAY_A');
define('PSTE_VERSION','0.57.144.22-QA');
$GLOBALS['opts']=['ppm679_editorial_plan_runtime_state_v1'=>['items'=>[
    'existing-qa-plan'=>['canonical_article_id'=>'existing-qa-plan',
        'plan_slot_sha256'=>hash('sha256','original-existing-qa-plan'),
        'title'=>'Already planned independent topic','status'=>'PLANNED']
]]];
function get_option(string $name,$default=[]){return $GLOBALS['opts'][$name]??$default;}
function update_option(string $name,$value,$autoload=false):bool{$GLOBALS['opts'][$name]=$value;return true;}
function wp_json_encode($value,int $flags=0):string{return json_encode($value,$flags|JSON_UNESCAPED_UNICODE);}
function get_post_types(array $filter,string $return='names'):array{return ['post','page'];}
function wp_strip_all_tags(string $html):string{return strip_tags($html);}
function get_current_user_id():int{return 1;}
function admin_url(string $path):string{return 'https://example.test/wp-admin/'.$path;}
function wp_safe_redirect(string $url):void{$GLOBALS['redirect']=$url;}
function set_transient(string $name,$data,int $ttl=0):bool{return true;}
function get_transient(string $name){return false;}
function wp_die($message):void{throw new RuntimeException('UNEXPECTED_WP_DIE: '.$message);}
final class PSTE_Auth {public static function assertAdmin(string $action,string $nonce):void{
    if($action!=='pste_mini_forward_to_plan')throw new RuntimeException('WRONG_AUTH_ACTION');
}}
final class PSTE_Editorializer {public static function sourceQuery(array $p):string{return (string)($p['raw_query']??'');}}
final class PSERC_Plan_Dependency_Fingerprint {
    public static bool $current=true;
    public static function isCurrent(array $x):bool{return self::$current;}
}
final class PSERC_Plan_Snapshot_Store {
    public static function getActive():array{return ['contract'=>'PSERC_PLAN_SNAPSHOT_V1',
        'generation'=>str_repeat('a',20),'snapshot_sha256'=>str_repeat('1',64),
        'dependency'=>[],'counts'=>['compiled_items'=>0]];}
    public static function verifyHeader(array $x):bool{return ($x['contract']??'')==='PSERC_PLAN_SNAPSHOT_V1';}
    public static function getRecord(string $gen,string $kind,int $n):?array{return null;}
}
final class PSTE_Snapshot {public static function editorialPlan():array{return ['status'=>'NOT_AVAILABLE','sha256'=>'NOT_AVAILABLE','items'=>[]];}}
final class PSTE_Repository {
    public static array $saved=[];
    public static function table(string $name):string{return 'wp_pste_topic_pool';}
    public static function saveManualTitleOverride(string $key,string $title,int $uid):array{
        self::$saved[]=$key;
        return ['contract'=>'PSTE_MANUAL_TITLE_OVERRIDE_RESULT_V1','status'=>'PASS'];
    }
}
final class PSTE_Admin {
    public static array $queued=[];
    public static function scheduleTitleDeskReentry(array $keys,bool $replay=false):int{self::$queued=$keys;return count($keys);}
    public static function processTitleDeskReentry():void{}
}
final class FakeDb {
    public string $posts='wp_posts',$postmeta='wp_postmeta',
        $term_relationships='wp_term_relationships',$term_taxonomy='wp_term_taxonomy',
        $terms='wp_terms',$last_error='';
    public function prepare(string $sql,...$values):string{
        foreach($values as $v){$x=strpos($sql,'%s');$fmt='%s';
            if($x===false){$x=strpos($sql,'%d');$fmt='%d';}
            if($x===false)break;
            $sql=substr_replace($sql,$fmt==='%d'?(string)(int)$v:"'".str_replace("'","''",(string)$v)."'", $x,2);
        }
        return $sql;
    }
    public function get_var(string $sql):int{return 0;}
    public function get_results(string $sql,string $format='ARRAY_A'):array{
        if(str_contains($sql,'FROM wp_pste_topic_pool WHERE pool_key IN')){
            $rows=[];
            foreach((array)$GLOBALS['qa_input_rows'] as $key=>$raw){
                if(($GLOBALS['qa_one_bad']??false)&&$key==='topic-bad')continue;
                $rows[]=['pool_key'=>$key,'payload_json'=>json_encode(['raw_query'=>$raw])];
            }
            return $rows;
        }
        return [];
    }
}
$wpdb=new FakeDb();
require_once $argv[1] ?? throw new RuntimeException('Missing patched MINI file');
$mode=$argv[2]??'good';
$queries=['topic-good'=>'horseware regendecken','topic-belegt'=>'pferdeanhänger 2 pferde',
    'topic-klaerung'=>'pferd decken'];
if($mode==='onebad')$queries['topic-bad']='fleece regendecke';
$GLOBALS['qa_input_rows']=$queries;
$GLOBALS['qa_one_bad']=$mode==='onebad';
$completed=[];foreach($queries as $key=>$raw){
    $title='Ratgeber für '.$raw;
    $completed[$key]=['decision'=>'JA','raw_query'=>$raw,'batch_id'=>'qa-batch',
        'titles'=>[['intent'=>'Ratgeber','title'=>$title]]];
}
$state=['completed'=>$completed,'active'=>null,'last_report'=>[],'seo_decisions'=>[]];
$GLOBALS['opts']['pste_mini_keyword_roundtrip_v1']=$state;
$snapshot=PSTE_Mini_Workflow::readParkhausForMini();
if(!$snapshot['complete'])throw new RuntimeException('TEST_SOURCE_INCOMPLETE '.json_encode($snapshot));
foreach($queries as $key=>$raw){
    $box=($key==='topic-good'||$key==='topic-bad')?'FREI':($key==='topic-belegt'?'BELEGT':'KLAERUNG');
    $state['seo_decisions'][$key]=[
        'contract'=>'PSTE_MINI_SEO_DECISIONS_V1','box'=>$box,'raw_query'=>$raw,
        'source_sha256'=>hash('sha256',$key.'|'.$raw),
        'snapshot_sha256'=>$snapshot['sha256'],
        'approved_title'=>'Ratgeber für '.$raw,
        'intent_slot'=>hash('sha256','slot|'.$raw)];
}
$GLOBALS['opts']['pste_mini_keyword_roundtrip_v1']=$state;
if($mode==='stale')PSERC_Plan_Dependency_Fingerprint::$current=false;
$_POST['_wpnonce']='qa';
register_shutdown_function(static function()use($mode){
    $s=(array)get_option('pste_mini_keyword_roundtrip_v1',[]);
    $r=(array)($s['last_plan_report']??[]);
    $out=['mode'=>$mode,'forwarded'=>(int)($r['forwarded']??-1),
        'scheduled'=>(int)($r['scheduled']??-1),'held_count'=>(int)($r['blocked']??-1),
        'save_keys'=>PSTE_Repository::$saved,'queue_keys'=>PSTE_Admin::$queued,
        'clarification'=>array_keys((array)($s['clarification']??[])),
        'redirect'=>(string)($GLOBALS['redirect']??'')];
    echo "FORWARD_QA_RESULT ".json_encode($out,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
});
PSTE_Mini_Workflow::forwardToPlan();
