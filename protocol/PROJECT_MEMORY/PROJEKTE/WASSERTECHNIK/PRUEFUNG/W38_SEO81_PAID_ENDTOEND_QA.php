<?php
declare(strict_types=1);
/**
 * W38 provider mock: runs the REAL original WT001 PaidResearch class with
 * the 81 keyword trait. Simulates 3 provider endpoints, never contacts API or WP.
 * Invoke each scenario separately so exit() in the WP handler is genuinely tested.
 */
$root=$argv[1]??'';$case=$argv[2]??'success';
if(!is_file($root.'/wassertechnik-kategorie-workflow.php'))exit(2);
define('ABSPATH','/');define('WASSERTECHNIK_DFS_LOGIN','mock-user');
define('WASSERTECHNIK_DFS_PASSWORD','mock-not-a-real-secret');
$GLOBALS['site']='wasser.oliver-beil.de';$GLOBALS['admin']=true;
$GLOBALS['options']=[];$GLOBALS['calls']=[];$GLOBALS['redirect']='';
$GLOBALS['case']=$case;$GLOBALS['old_option_name']='';
function add_action(...$a){} function add_shortcode(...$a){} function add_menu_page(...$a){}
function add_submenu_page(...$a){} function plugin_dir_path($p){return dirname($p).'/';}
function home_url($suffix='/'){return 'https://'.$GLOBALS['site'].$suffix;}
function wp_parse_url($url,$part){return parse_url($url,$part);}
function current_user_can($cap){return $GLOBALS['admin'];}
function wp_json_encode($v,$opt=0){return json_encode($v,$opt);}
function wp_unslash($s){return $s;} function wp_nonce_field(...$a){} function submit_button(...$a){} function esc_html($s){return htmlspecialchars((string)$s,ENT_QUOTES,'UTF-8');} function esc_url($s){return esc_html($s);} function esc_attr($s){return esc_html($s);}
function check_admin_referer($nonce){return true;} // handler still checks explicit consent and plan hash
function wp_die($s){throw new RuntimeException('WP_BLOCK '.$s);}
function is_wp_error($v){return $v instanceof WP_Error;}
class WP_Error {}
function get_option($key,$default=false){return $GLOBALS['options'][$key]??$default;}
function update_option($key,$v,$autoload=false){$GLOBALS['options'][$key]=$v;return true;}
function add_option($key,$v,$deprecated='',$autoload=false){
    if(array_key_exists($key,$GLOBALS['options']))return false;
    $GLOBALS['options'][$key]=$v;return true;
}
function admin_url($path=''){return 'https://wasser.oliver-beil.de/wp-admin/'.$path;}
function wp_safe_redirect($url,$code=302){$GLOBALS['redirect']=$url;return true;}
function wp_remote_retrieve_response_code($r){return $r['status'];}
function wp_remote_retrieve_body($r){return $r['body'];}
function wp_remote_post($url,$args) {
    $task=json_decode($args['body'],true,512,JSON_THROW_ON_ERROR)[0];
    $keys=$task['keywords']??[];
    if(count($keys)!==81 || count(array_unique($keys))!==81)
        throw new RuntimeException('wrong provider payload 81 terms');
    $GLOBALS['calls'][]=['url'=>$url,'keywords'=>$keys];
    $step=count($GLOBALS['calls']);
    if($GLOBALS['case']==='network' && $step===1)return new WP_Error();
    if($GLOBALS['case']==='provider' && $step===2) {
        $payload=['status_code'=>50000,'status_message'=>'Mock failed provider step',
            'cost'=>0,'tasks'=>[['id'=>'provider-failure','status_code'=>50000,
                                'status_message'=>'Mock failure','cost'=>0,'result'=>[]]]];
        return ['status'=>500,'body'=>json_encode($payload)];
    }
    $items=[];
    foreach($keys as $keyword){
        if($step===1)$items[]=['keyword'=>$keyword,'search_volume'=>22,'competition'=>'LOW','cpc'=>0.1];
        elseif($step===2)$items[]=['keyword'=>$keyword,'keyword_difficulty'=>41];
        else $items[]=['keyword'=>$keyword,'keyword_intent'=>['label'=>'commercial','probability'=>0.7]];
    }
    if($step===2 && $GLOBALS['case']==='partial')$items=array_slice($items,0,40);
    if($step===2 && $GLOBALS['case']==='duplicate')$items=array_fill(0,81,$items[0]);
    if($step===2 && $GLOBALS['case']==='empty')$items=[];
    $cost=($GLOBALS['case']==='budget' && $step===1)?0.3:0.02;
    $payload=['status_code'=>20000,'status_message'=>'Ok.','cost'=>$cost,
        'tasks'=>[['id'=>'mock-step-'.$step,'status_code'=>20000,
                   'status_message'=>'Ok.','cost'=>$cost,
                   'result'=>[['items'=>$items]]]]];
    return ['status'=>200,'body'=>json_encode($payload)];
}
require $root.'/wassertechnik-kategorie-workflow.php';
$ref=new ReflectionClass(Wassertechnik_PaidResearch::class);
$oldReportName=$ref->getReflectionConstant('REPORT')->getValue();
$GLOBALS['old_option_name']=$oldReportName;
[$legacy,$oldTerms]=Wassertechnik_PaidResearch::planned();
[$plan,$newTerms,$newOwners]=Wassertechnik_PaidResearch::planned81();
if(count($oldTerms)!==218 || count($newTerms)!==81 ||
   count(array_intersect($oldTerms,$newTerms))!==0)throw new RuntimeException('Incorrect planning');
$GLOBALS['options'][$oldReportName]=['request_id'=>'old218-existing','source_fingerprint'=>$legacy['fingerprint'],'sentinel'=>'PRESERVE_218_RESULTS'];
$_POST=['explicit_paid_approval'=>'1','plan_fingerprint'=>$plan['fingerprint']];
if($case==='stale')$_POST['plan_fingerprint']='wrong-fingerprint';
if($case==='locked')$GLOBALS['options']['wassertechnik_dfs_w38_81_paid_lock']=['request_id'=>'already-run'];
if($case==='nonadmin')$GLOBALS['admin']=false;
if($case==='wrongsite')$GLOBALS['site']='other.example';
if($case==='noapproval')$_POST['explicit_paid_approval']='0';
if($case==='reportonly')$GLOBALS['options']['wassertechnik_dfs_w38_81_paid_report']=[
    'request_id'=>'past-81-paid','keywords_requested'=>81,
    'source_fingerprint'=>$plan['fingerprint'],'legacy_fingerprint'=>$plan['legacy_fingerprint']
];

if(in_array($case,['ui','ui-stale'],true)){
    $rows=[];
    foreach($newTerms as $idx=>$term)$rows[]=[
        'keyword'=>$term,'owner'=>$newOwners[$term],
        'search_volume'=>$idx===0?0:($idx===1?120:null),
        'search_intent'=>$idx===1?'commercial':null,
        'organic_keyword_difficulty'=>$idx===1?42:null
    ];
    $GLOBALS['options']['wassertechnik_dfs_w38_81_paid_report']=[
        'schema'=>'wassertechnik-dfs-w38-81-research-v1',
        'request_id'=>'verified-81-ui','keywords_requested'=>81,
        'source_fingerprint'=>$case==='ui-stale'?'wrong':$plan['fingerprint'],
        'legacy_fingerprint'=>$plan['legacy_fingerprint'],
        'state'=>'COMPLETE_WITH_GAPS','cost_usd'=>0.08,
        'rows'=>$rows,'skipped_steps'=>[['kind'=>'difficulty','status'=>'NICHT_GEPRUEFT']]
    ];
    $before=serialize($GLOBALS['options']);
    ob_start();
    Wassertechnik_Seo81_Preview::screen();
    $html=ob_get_clean();
    if($before!==serialize($GLOBALS['options']))throw new RuntimeException('UI modified WP data');
    if($case==='ui'){
        if(substr_count($html,'<tr>')!==82
            || !str_contains($html,'COMPLETE_WITH_GAPS')
            || !str_contains($html,'nicht gemessen')
            || !str_contains($html,'>0</td>')
            || !str_contains($html,'kommer') && !str_contains($html,'commercial')
            || !str_contains($html,'nicht freigegeben'))
            throw new RuntimeException('UI output / zero vs null / status incorrect');
    } else {
        if(!str_contains($html,'GESPERRT')||str_contains($html,'>120</td>'))
            throw new RuntimeException('UI leaked data from stale W28 report');
    }
    echo 'PASS W38 '.$case.' read-only results show status, gaps and no false approval'.PHP_EOL;
    exit(0);
}
if(in_array($case,['stale','locked','reportonly','nonadmin','wrongsite','noapproval'],true)){
    // Shutdown assertions are registered BEFORE the WP handler, which calls exit().
    register_shutdown_function(function()use($case,$oldReportName){
        if($GLOBALS['calls']!==[]) {fwrite(STDERR,'FAIL '.$case.' paid unexpectedly'.PHP_EOL);exit(5);}
        if($GLOBALS['options'][$oldReportName]['sentinel']!=='PRESERVE_218_RESULTS')
            {fwrite(STDERR,'FAIL old218 mutated'.PHP_EOL);exit(6);}
        echo 'PASS W38 negative '.$case.' provider_calls=0 old218=preserved'.PHP_EOL;
    });
    try{Wassertechnik_PaidResearch::paid81();}
    catch(Throwable $e){exit(0);}
} else {
    register_shutdown_function(function()use($case,$oldReportName){
        $report=$GLOBALS['options']['wassertechnik_dfs_w38_81_paid_report']??[];
        $lock=$GLOBALS['options']['wassertechnik_dfs_w38_81_paid_lock']??null;
        $expectedCalls=$case==='network'?1:($case==='budget'?1:3);
        if(count($GLOBALS['calls'])!==$expectedCalls){fwrite(STDERR,'FAIL HTTP request count '.count($GLOBALS['calls']).' vs '.$expectedCalls.PHP_EOL);exit(7);}
        if(($GLOBALS['options'][$oldReportName]['sentinel']??'')!=='PRESERVE_218_RESULTS')
            {fwrite(STDERR,'FAIL old 218 report changed'.PHP_EOL);exit(8);}
        if(!$lock || ($report['keywords_requested']??0)!==81 || count($report['rows']??[])!==81)
            {fwrite(STDERR,'FAIL missing durable 81-only lock or report'.PHP_EOL);exit(9);}
        if($case==='success' && ($report['state']??'')!=='COMPLETED')
            {fwrite(STDERR,'FAIL success status: '.($report['state']??'none').PHP_EOL);exit(10);}
        if(in_array($case,['provider','partial','duplicate','empty'],true) && (($report['state']??'')!=='COMPLETE_WITH_GAPS'||count($report['skipped_steps']??[])!==1))
            {fwrite(STDERR,'FAIL provider gap state'.PHP_EOL);exit(11);}
        if(in_array($case,['budget','network'],true) && ($report['state']??'')!=='PARTIAL_STOPPED_NO_AUTO_RETRY')
            {fwrite(STDERR,'FAIL stop without retry'.PHP_EOL);exit(12);}
        if(in_array($case,['success','partial','duplicate','empty'],true) && count($report['completed']??[])!==3)
            {fwrite(STDERR,'FAIL missing three provider responses'.PHP_EOL);exit(13);}
        if($case==='success' && ($report['rows'][0]['search_volume']??null)!==22)
            {fwrite(STDERR,'FAIL volume mapping'.PHP_EOL);exit(14);}
        if($case==='success' && ($report['rows'][0]['organic_keyword_difficulty']??null)!==41)
            {fwrite(STDERR,'FAIL difficulty mapping'.PHP_EOL);exit(15);}
        if($case==='success' && ($report['rows'][0]['search_intent']??null)!=='commercial')
            {fwrite(STDERR,'FAIL intent mapping'.PHP_EOL);exit(16);}
        if(!str_contains($GLOBALS['redirect'],'wassertechnik-seo81-preview'))
            {fwrite(STDERR,'FAIL WP admin redirect'.PHP_EOL);exit(17);}
        echo 'PASS W38 '.$case.' calls='.count($GLOBALS['calls']).' state='.$report['state'].' old218=preserved'.PHP_EOL;
    });
}
Wassertechnik_PaidResearch::paid81();
