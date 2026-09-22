<?php
/**
 * Plugin Name: Performance Diagnose Safe
 * Description: Read-only Frontend- und Serverdiagnose ohne MU-Plugin, Plugin-Deaktivierung oder Änderungen an der WordPress-Ladereihenfolge.
 * Version: 2.1.0
 * Requires at least: 5.8
 * Requires PHP: 7.4
 * Author: OpenAI
 * License: GPL-2.0-or-later
 */
if (!defined('ABSPATH')) { exit; }

const PADS_VERSION = '2.1.0';
const PADS_MAX_PAGEVIEWS = 200;
const PADS_TTL = 86400;
const PADS_MAX_QUERY_PATTERNS = 300;
const PADS_MAX_HTTP_ITEMS = 100;

$GLOBALS['pads_measure'] = false;
$GLOBALS['pads_request'] = null;
$GLOBALS['pads_query_patterns'] = array();
$GLOBALS['pads_query_patterns_dropped'] = 0;
$GLOBALS['pads_trace'] = array(
    'sanitize_key'=>array('fires'=>0,'sampled'=>0,'callsites'=>array()),
    'sanitize_text_field'=>array('fires'=>0,'sampled'=>0,'callsites'=>array()),
    'get_post_metadata'=>array('fires'=>0,'sampled'=>0,'callsites'=>array()),
    'get_term'=>array('fires'=>0,'sampled'=>0,'callsites'=>array()),
);
$GLOBALS['pads_menu_probe'] = array(
    'desktop_args'=>0,'mobile_args'=>0,
    'desktop_perf_filter_seen'=>0,'mobile_perf_filter_seen'=>0,
    'desktop_pre_calls'=>0,'mobile_pre_calls'=>0,
    'desktop_pre_nonnull'=>0,'mobile_pre_nonnull'=>0,
    'desktop_html'=>0,'mobile_html'=>0,
);
$GLOBALS['pads_current_menu_class'] = '';
$GLOBALS['pads_http_starts'] = array();
$GLOBALS['pads_http_done'] = array();

function pads_recording_key($uid){ return 'pads_recording_' . (int)$uid; }
function pads_report_key($uid){ return 'pads_report_' . (int)$uid; }
function pads_is_frontend(){ return !is_admin() && !wp_doing_ajax() && !(defined('REST_REQUEST') && REST_REQUEST) && !wp_doing_cron(); }
function pads_is_recording($uid){
    static $cache=array();
    $uid=(int)$uid;
    if(!$uid) return false;
    if(array_key_exists($uid,$cache)) return $cache[$uid];
    $s=get_transient(pads_recording_key($uid));
    return $cache[$uid]=(is_array($s) && !empty($s['active']));
}
function pads_report($uid){ $r=get_user_meta((int)$uid,pads_report_key($uid),true); return is_array($r)?$r:array(); }
function pads_save_report($uid,$r){ update_user_meta((int)$uid,pads_report_key($uid),$r); }
function pads_env(){
    global $wp_version,$wpdb;
    $db='';
    if(isset($wpdb) && is_object($wpdb) && method_exists($wpdb,'db_version')) { try{$db=$wpdb->db_version();}catch(Throwable $e){} }
    return array(
        'wordpress_version'=>(string)$wp_version,
        'php_version'=>PHP_VERSION,
        'db_version'=>$db,
        'php_sapi'=>PHP_SAPI,
        'memory_limit'=>(string)ini_get('memory_limit'),
        'max_execution_time'=>(string)ini_get('max_execution_time'),
        'savequeries'=>(defined('SAVEQUERIES') && SAVEQUERIES),
        'object_cache'=>function_exists('wp_using_ext_object_cache') ? wp_using_ext_object_cache() : null,
        'active_plugins'=>array_values((array)get_option('active_plugins',array())),
    );
}
function pads_new_report($session){
    return array(
        'tool'=>'Performance Diagnose Safe','version'=>PADS_VERSION,
        'session_id'=>$session['session_id'],'started_at_utc'=>$session['started_at_utc'],'stopped_at_utc'=>null,
        'site'=>home_url('/'),'environment'=>pads_env(),'pageviews'=>array(),
        'notes'=>array(
            'Read-only Diagnose: keine MU-Datei, keine Plugin-Deaktivierung, keine active_plugins-Filterung, keine Änderung an wp-config.php.',
            'Server-Gesamtzeit und Query-Anzahl gelten für den gesamten Request. Query-Muster werden aus Sicherheitsgründen erst nach WordPress init mitgeschnitten.',
            'Exakte SQL-Zeiten stehen nur zur Verfügung, wenn SAVEQUERIES außerhalb dieses Plugins bereits aktiv ist.',
            'Browserwerte eines eingeloggten Administrators können Admin-Bar-Assets enthalten.',
            'V2.1 verwendet keinen globalen all-Hook mehr. Nur vier gezielte Hot-Hooks werden gezählt; Callstacks werden stark gesampelt, damit die Messung selbst die PHP-Zeit deutlich weniger verfälscht.',
            'Der Menü-Probe weist separat nach, ob der Affiliate-Design-Performance-Shortcut im Desktop/Mobile-Menüpfad tatsächlich aktiv war.'
        )
    );
}
function pads_owner_from_text($text){
    $text=wp_normalize_path((string)$text);
    if(preg_match('#/wp-content/plugins/([^/]+)/#i',$text,$m)) return $m[1];
    if(preg_match('#/wp-content/mu-plugins/([^/]+)/#i',$text,$m)) return 'mu:'.$m[1];
    if(preg_match('#/wp-content/themes/([^/]+)/#i',$text,$m)) return 'theme:'.$m[1];
    return 'core/theme/unknown';
}
function pads_backtrace_owner(){
    $self=wp_normalize_path(__DIR__).'/';
    foreach(debug_backtrace(DEBUG_BACKTRACE_IGNORE_ARGS,30) as $f){
        if(empty($f['file'])) continue;
        $x=wp_normalize_path($f['file']);
        if(strpos($x,$self)===0) continue;
        $o=pads_owner_from_text($x);
        if($o!=='core/theme/unknown') return $o;
    }
    return 'core/theme/unknown';
}
function pads_query_signature($sql){
    $x=(string)$sql;
    $x=preg_replace("/'(?:''|[^'])*'/",'?',$x);
    $x=preg_replace('/\\b\\d+(?:\\.\\d+)?\\b/','?',$x);
    $x=preg_replace('/\\s+/',' ',trim($x));
    return substr($x,0,900);
}
function pads_safe_url($url){
    $p=wp_parse_url((string)$url);
    if(!is_array($p)) return (string)$url;
    $scheme=isset($p['scheme'])?$p['scheme'].'://':'';
    $host=$p['host']??'';
    $port=isset($p['port'])?':'.$p['port']:'';
    $path=$p['path']??'';
    $keys=array();
    if(!empty($p['query'])){ parse_str($p['query'],$q); $keys=array_keys((array)$q); }
    return $scheme.$host.$port.$path.($keys?'?'.implode('&',array_map(function($k){return rawurlencode((string)$k).'=[redacted]';},$keys)):'');
}

/* Measurement is armed only on init, after authentication is available. Low-level hooks NEVER call get_transient/current_user_can. */
add_action('init',function(){
    if(!pads_is_frontend()) return;
    $uid=get_current_user_id();
    if(!$uid || !current_user_can('manage_options')) return;
    if(!pads_is_recording($uid)) return;
    $GLOBALS['pads_measure']=true;
    $GLOBALS['pads_request']=array(
        'id'=>wp_generate_uuid4(),'uid'=>$uid,
        'start'=>isset($_SERVER['REQUEST_TIME_FLOAT'])?(float)$_SERVER['REQUEST_TIME_FLOAT']:microtime(true),
        'url'=>home_url(wp_unslash($_SERVER['REQUEST_URI']??'/')),
        'query_count_at_init'=>isset($GLOBALS['wpdb']->num_queries)?(int)$GLOBALS['wpdb']->num_queries:0
    );
},PHP_INT_MAX);

add_filter('query',function($sql){
    if(empty($GLOBALS['pads_measure'])) return $sql;
    $owner=pads_backtrace_owner();
    $sig=pads_query_signature($sql);
    $key=md5($owner.'|'.$sig);
    if(!isset($GLOBALS['pads_query_patterns'][$key])){
        if(count($GLOBALS['pads_query_patterns'])>=PADS_MAX_QUERY_PATTERNS){ $GLOBALS['pads_query_patterns_dropped']++; return $sql; }
        $GLOBALS['pads_query_patterns'][$key]=array('owner'=>$owner,'signature'=>$sig,'count'=>0);
    }
    $GLOBALS['pads_query_patterns'][$key]['count']++;
    return $sql;
},PHP_INT_MAX,1);

function pads_trace_should_sample($hook,$count){
    if($count<=32) return true;
    $step=2048;
    if($hook==='get_post_metadata' || $hook==='get_term') $step=512;
    elseif($hook==='sanitize_text_field') $step=1024;
    return ($count % $step)===0;
}
function pads_trace_callsite($hook){
    $self=wp_normalize_path(__DIR__).'/';
    $site='core/theme/unknown|unknown';
    foreach(debug_backtrace(DEBUG_BACKTRACE_IGNORE_ARGS,30) as $f){
        if(empty($f['file'])) continue;
        $file=wp_normalize_path((string)$f['file']);
        if(strpos($file,$self)===0) continue;
        if(strpos($file,'/wp-includes/')!==false || strpos($file,'/wp-admin/')!==false) continue;
        $owner=pads_owner_from_text($file);
        $line=isset($f['line'])?(int)$f['line']:0;
        $func='';
        if(!empty($f['class'])) $func.=(string)$f['class'].(string)($f['type']??'::');
        if(!empty($f['function'])) $func.=(string)$f['function'];
        $site=$owner.'|'.basename($file).':'.$line.($func!==''?'|'.$func:'');
        break;
    }
    if(!isset($GLOBALS['pads_trace'][$hook]['callsites'][$site])) $GLOBALS['pads_trace'][$hook]['callsites'][$site]=0;
    $GLOBALS['pads_trace'][$hook]['callsites'][$site]++;
    $GLOBALS['pads_trace'][$hook]['sampled']++;
}
function pads_trace_hit($hook){
    if(empty($GLOBALS['pads_measure']) || !isset($GLOBALS['pads_trace'][$hook])) return;
    $count=++$GLOBALS['pads_trace'][$hook]['fires'];
    if(pads_trace_should_sample($hook,$count)) pads_trace_callsite($hook);
}
add_filter('sanitize_key',function($sanitized,$raw){ pads_trace_hit('sanitize_key'); return $sanitized; },PHP_INT_MAX,2);
add_filter('sanitize_text_field',function($filtered,$raw){ pads_trace_hit('sanitize_text_field'); return $filtered; },PHP_INT_MAX,2);
add_filter('get_post_metadata',function($check,$object_id,$meta_key,$single,$meta_type){ pads_trace_hit('get_post_metadata'); return $check; },PHP_INT_MAX,5);
add_filter('get_term',function($term,$taxonomy){ pads_trace_hit('get_term'); return $term; },PHP_INT_MAX,2);

/* Exact live probe for the standalone Affiliate Design Performance menu shortcut. */
add_filter('wp_nav_menu_args',function($args){
    if(empty($GLOBALS['pads_measure']) || !is_array($args)) return $args;
    $class=(string)($args['menu_class']??'');
    if($class!=='pftk-brand-menu-v15065' && $class!=='pftk-mobile-menu-v15074') return $args;
    $GLOBALS['pads_current_menu_class']=$class;
    $kind=$class==='pftk-brand-menu-v15065'?'desktop':'mobile';
    $GLOBALS['pads_menu_probe'][$kind.'_args']++;
    if(class_exists('PA_Affiliate_Design_Performance')){
        $seen=has_filter('pre_wp_setup_nav_menu_item',array('PA_Affiliate_Design_Performance','pre_setup'));
        if($seen!==false) $GLOBALS['pads_menu_probe'][$kind.'_perf_filter_seen']++;
    }
    return $args;
},PHP_INT_MAX,1);
add_filter('pre_wp_setup_nav_menu_item',function($pre,$menu_item){
    if(empty($GLOBALS['pads_measure'])) return $pre;
    $class=(string)($GLOBALS['pads_current_menu_class']??'');
    if($class==='pftk-brand-menu-v15065'){
        $GLOBALS['pads_menu_probe']['desktop_pre_calls']++;
        if($pre!==null) $GLOBALS['pads_menu_probe']['desktop_pre_nonnull']++;
    } elseif($class==='pftk-mobile-menu-v15074'){
        $GLOBALS['pads_menu_probe']['mobile_pre_calls']++;
        if($pre!==null) $GLOBALS['pads_menu_probe']['mobile_pre_nonnull']++;
    }
    return $pre;
},PHP_INT_MAX,2);
add_filter('wp_nav_menu',function($html,$args){
    if(empty($GLOBALS['pads_measure']) || !is_object($args)) return $html;
    $class=(string)($args->menu_class??'');
    if($class==='pftk-brand-menu-v15065') $GLOBALS['pads_menu_probe']['desktop_html']++;
    elseif($class==='pftk-mobile-menu-v15074') $GLOBALS['pads_menu_probe']['mobile_html']++;
    if($class==='pftk-brand-menu-v15065' || $class==='pftk-mobile-menu-v15074') $GLOBALS['pads_current_menu_class']='';
    return $html;
},999998,2);

add_filter('http_request_args',function($args,$url){
    if(empty($GLOBALS['pads_measure'])) return $args;
    $key=wp_generate_uuid4();
    $GLOBALS['pads_http_starts'][$key]=array('url'=>(string)$url,'t'=>microtime(true),'owner'=>pads_backtrace_owner());
    $args['_pads_key']=$key;
    return $args;
},PHP_INT_MAX,2);
add_action('http_api_debug',function($response,$context,$class,$args,$url){
    if(empty($GLOBALS['pads_measure'])) return;
    $key=$args['_pads_key']??'';
    if(!$key || empty($GLOBALS['pads_http_starts'][$key])) return;
    $s=$GLOBALS['pads_http_starts'][$key]; unset($GLOBALS['pads_http_starts'][$key]);
    if(count($GLOBALS['pads_http_done'])>=PADS_MAX_HTTP_ITEMS) return;
    $GLOBALS['pads_http_done'][]=array(
        'url'=>pads_safe_url($url),'host'=>(string)wp_parse_url($url,PHP_URL_HOST),
        'seconds'=>round(max(0,microtime(true)-$s['t']),6),'owner'=>$s['owner'],
        'error'=>is_wp_error($response)?$response->get_error_message():'',
        'response_code'=>is_wp_error($response)?0:(int)wp_remote_retrieve_response_code($response)
    );
},PHP_INT_MAX,5);

function pads_assets(){
    $out=array();
    foreach(array('wp_scripts'=>'js','wp_styles'=>'css') as $g=>$type){
        if(empty($GLOBALS[$g])||!is_object($GLOBALS[$g])) continue;
        $d=$GLOBALS[$g]; $handles=array_unique(array_merge((array)$d->queue,(array)$d->done));
        foreach($handles as $h){
            if(empty($d->registered[$h])) continue;
            $src=(string)$d->registered[$h]->src; if(!$src) continue;
            $path=wp_parse_url($src,PHP_URL_PATH); $owner='core/theme/external';
            if($path && preg_match('#/wp-content/plugins/([^/]+)/#',$path,$m))$owner=$m[1];
            elseif($path && preg_match('#/wp-content/themes/([^/]+)/#',$path,$m))$owner='theme:'.$m[1];
            $bytes=0;
            if($path && defined('WP_CONTENT_DIR')){
                $pos=strpos($path,'/wp-content/');
                if($pos!==false){$local=wp_normalize_path(WP_CONTENT_DIR.'/'.ltrim(substr($path,$pos+12),'/')); if(is_file($local)){$z=@filesize($local);if($z!==false)$bytes=(int)$z;}}
            }
            if(!isset($out[$owner]))$out[$owner]=array('count'=>0,'bytes'=>0,'items'=>array());
            $out[$owner]['count']++; $out[$owner]['bytes']+=$bytes;
            if(count($out[$owner]['items'])<50)$out[$owner]['items'][]=array('handle'=>$h,'type'=>$type,'src'=>pads_safe_url($src),'bytes'=>$bytes);
        }
    }
    return $out;
}
function pads_included_files_by_owner(){
    $out=array();$seen=0;
    foreach(get_included_files() as $f){
        if(++$seen>5000) break;
        $owner=pads_owner_from_text($f);
        if(!isset($out[$owner]))$out[$owner]=array('count'=>0,'sample'=>array());
        $out[$owner]['count']++;
        if(count($out[$owner]['sample'])<10)$out[$owner]['sample'][]=wp_normalize_path($f);
    }
    return $out;
}
function pads_targeted_trace(){
    $out=array();
    foreach((array)$GLOBALS['pads_trace'] as $hook=>$row){
        $sites=(array)($row['callsites']??array()); arsort($sites);
        $top=array(); foreach(array_slice($sites,0,40,true) as $site=>$samples){ $top[]=array('callsite'=>$site,'samples'=>(int)$samples); }
        $out[$hook]=array('fires'=>(int)($row['fires']??0),'sampled'=>(int)($row['sampled']??0),'top_callsites'=>$top);
    }
    return $out;
}
function pads_query_details(){
    $out=array('available'=>false,'time_s'=>null,'captured'=>0,'by_owner'=>array(),'slow'=>array(),'groups'=>array());
    if(!(defined('SAVEQUERIES')&&SAVEQUERIES) || empty($GLOBALS['wpdb']->queries) || !is_array($GLOBALS['wpdb']->queries)) return $out;
    $out['available']=true;$out['time_s']=0.0;$groups=array();
    foreach($GLOBALS['wpdb']->queries as $q){
        $sql=(string)($q[0]??'');$sec=(float)($q[1]??0);$caller=(string)($q[2]??'');$owner=pads_owner_from_text($caller);$sig=pads_query_signature($sql);
        $out['captured']++;$out['time_s']+=$sec;
        if(!isset($out['by_owner'][$owner]))$out['by_owner'][$owner]=array('seconds'=>0.0,'queries'=>0);
        $out['by_owner'][$owner]['seconds']+=$sec;$out['by_owner'][$owner]['queries']++;
        $k=md5($owner.'|'.$sig);if(!isset($groups[$k]))$groups[$k]=array('owner'=>$owner,'signature'=>$sig,'count'=>0,'seconds'=>0.0,'max_seconds'=>0.0);
        $groups[$k]['count']++;$groups[$k]['seconds']+=$sec;$groups[$k]['max_seconds']=max($groups[$k]['max_seconds'],$sec);
        if($sec>=0.02 && count($out['slow'])<100)$out['slow'][]=array('seconds'=>$sec,'owner'=>$owner,'sql_signature'=>$sig);
    }
    uasort($groups,function($a,$b){return $b['seconds']<=>$a['seconds'];});$out['groups']=array_slice(array_values($groups),0,100);
    usort($out['slow'],function($a,$b){return $b['seconds']<=>$a['seconds'];});$out['slow']=array_slice($out['slow'],0,50);
    return $out;
}
function pads_merge($uid,$id,$part,$data){
    $r=pads_report($uid);if(!$r)return;
    if(!isset($r['pageviews'][$id]))$r['pageviews'][$id]=array('request_id'=>$id);
    if($part==='browser' && isset($r['pageviews'][$id]['browser'])){
        $old=(array)$r['pageviews'][$id]['browser'];
        foreach(array('lcp_ms','cls','inp_ms','long_task_ms') as $k) if(isset($old[$k])&&(!isset($data[$k])||$old[$k]>$data[$k]))$data[$k]=$old[$k];
    }
    $r['pageviews'][$id][$part]=$data;
    if(count($r['pageviews'])>PADS_MAX_PAGEVIEWS)$r['pageviews']=array_slice($r['pageviews'],-PADS_MAX_PAGEVIEWS,null,true);
    pads_save_report($uid,$r);
}

add_action('wp_footer',function(){
    if(empty($GLOBALS['pads_measure'])||empty($GLOBALS['pads_request'])) return;
    $id=$GLOBALS['pads_request']['id'];$nonce=wp_create_nonce('pads_frontend');$ajax=admin_url('admin-ajax.php');
?>
<script id="pads-recorder">
(function(){
const requestId=<?php echo wp_json_encode($id); ?>,endpoint=<?php echo wp_json_encode($ajax); ?>,nonce=<?php echo wp_json_encode($nonce); ?>;
let lcp=0,lcpEl=null,cls=0,inp=0,longTasks=0,longTaskMs=0,errors=[],sentLate=false;
function elInfo(el){if(!el)return null;try{return{tag:el.tagName||'',id:el.id||'',class:(typeof el.className==='string'?el.className:'').slice(0,180),src:(el.currentSrc||el.src||'').slice(0,500)}}catch(e){return null}}
try{new PerformanceObserver(l=>{for(const e of l.getEntries()){if(e.startTime>=lcp){lcp=e.startTime;lcpEl=elInfo(e.element)}}}).observe({type:'largest-contentful-paint',buffered:true})}catch(e){}
try{new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)cls+=e.value}).observe({type:'layout-shift',buffered:true})}catch(e){}
try{new PerformanceObserver(l=>{for(const e of l.getEntries()){if(e.interactionId&&e.duration>inp)inp=e.duration}}).observe({type:'event',durationThreshold:40,buffered:true})}catch(e){}
try{new PerformanceObserver(l=>{for(const e of l.getEntries()){longTasks++;longTaskMs+=e.duration}}).observe({type:'longtask',buffered:true})}catch(e){}
addEventListener('error',e=>{if(errors.length<20)errors.push({message:String(e.message||''),source:String(e.filename||''),line:e.lineno||0})});
function owner(u){try{const x=new URL(u,location.href);let m=x.pathname.match(/\/wp-content\/plugins\/([^/]+)\//);if(m)return m[1];m=x.pathname.match(/\/wp-content\/themes\/([^/]+)\//);if(m)return'theme:'+m[1];return x.origin===location.origin?'core/theme/unknown':'external:'+x.hostname}catch(e){return'unknown'}}
function payload(){const n=performance.getEntriesByType('navigation')[0]||{},res=performance.getEntriesByType('resource')||[],by={},slow=[];let transfer=0,decoded=0;for(const r of res){const o=owner(r.name);if(!by[o])by[o]={count:0,duration_ms:0,transfer_bytes:0,decoded_bytes:0};by[o].count++;by[o].duration_ms+=Math.max(0,r.duration||0);by[o].transfer_bytes+=r.transferSize||0;by[o].decoded_bytes+=r.decodedBodySize||0;transfer+=r.transferSize||0;decoded+=r.decodedBodySize||0;slow.push({url:r.name.split('?')[0],owner:o,duration_ms:Math.max(0,r.duration||0),transfer_bytes:r.transferSize||0,decoded_bytes:r.decodedBodySize||0,initiator:r.initiatorType||'',protocol:r.nextHopProtocol||''})}slow.sort((a,b)=>b.duration_ms-a.duration_ms);slow.length=Math.min(60,slow.length);const paints={};for(const p of performance.getEntriesByType('paint')||[])paints[p.name]=p.startTime;return{request_id:requestId,url:location.href.split('#')[0],title:document.title,recorded_at_utc:new Date().toISOString(),logged_in:document.body&&document.body.classList.contains('logged-in'),admin_bar:document.body&&document.body.classList.contains('admin-bar'),dom_elements:document.getElementsByTagName('*').length,lcp_ms:lcp,lcp_element:lcpEl,cls:cls,inp_ms:inp,long_tasks:longTasks,long_task_ms:longTaskMs,errors:errors,paints:paints,navigation:{ttfb_ms:n.responseStart||0,response_ms:(n.responseEnd||0)-(n.responseStart||0),dom_interactive_ms:n.domInteractive||0,dom_content_loaded_ms:n.domContentLoadedEventEnd||0,load_ms:n.loadEventEnd||performance.now(),transfer_bytes:n.transferSize||0,decoded_bytes:n.decodedBodySize||0},resources_by_owner:by,resource_count:res.length,total_resource_transfer_bytes:transfer,total_resource_decoded_bytes:decoded,slow_resources:slow}}
function send(kind){const fd=new FormData();fd.append('action','pads_frontend_metrics');fd.append('nonce',nonce);fd.append('kind',kind);fd.append('payload',JSON.stringify(payload()));if(kind==='final'&&navigator.sendBeacon){navigator.sendBeacon(endpoint,fd)}else{fetch(endpoint,{method:'POST',body:fd,credentials:'same-origin',keepalive:true}).catch(()=>{})}}
addEventListener('load',()=>setTimeout(()=>{send('after-load');sentLate=true},4000),{once:true});
addEventListener('pagehide',()=>send('final'),{once:true});
})();
</script>
<?php
},PHP_INT_MAX);

add_action('wp_ajax_pads_frontend_metrics',function(){
    check_ajax_referer('pads_frontend','nonce');
    if(!current_user_can('manage_options'))wp_send_json_error(array('message'=>'Keine Berechtigung.'),403);
    $p=json_decode(wp_unslash($_POST['payload']??''),true);if(!is_array($p)||empty($p['request_id']))wp_send_json_error(array('message'=>'Ungültige Messdaten.'),400);
    $id=preg_replace('/[^a-zA-Z0-9-]/','',(string)$p['request_id']);pads_merge(get_current_user_id(),$id,'browser',$p);wp_send_json_success();
});

register_shutdown_function(function(){
    if(empty($GLOBALS['pads_measure'])||empty($GLOBALS['pads_request'])) return;
    $r=$GLOBALS['pads_request'];$uid=(int)$r['uid'];if(!$uid)return;
    $db=pads_query_details();$httpBy=array();$httpTime=0.0;
    foreach((array)$GLOBALS['pads_http_done'] as $h){$httpTime+=(float)$h['seconds'];$o=$h['owner'];if(!isset($httpBy[$o]))$httpBy[$o]=array('seconds'=>0.0,'calls'=>0,'items'=>array());$httpBy[$o]['seconds']+=(float)$h['seconds'];$httpBy[$o]['calls']++;if(count($httpBy[$o]['items'])<30)$httpBy[$o]['items'][]=$h;}
    $patterns=array_values((array)$GLOBALS['pads_query_patterns']);usort($patterns,function($a,$b){return $b['count']<=>$a['count'];});$patterns=array_slice($patterns,0,100);
    $data=array(
        'url'=>$r['url'],'captured_at_utc'=>gmdate('c'),'server_time_s'=>round(max(0,microtime(true)-$r['start']),6),
        'db_queries_total'=>isset($GLOBALS['wpdb']->num_queries)?(int)$GLOBALS['wpdb']->num_queries:0,
        'db_queries_before_init'=>(int)$r['query_count_at_init'],'db_query_timing'=>$db,
        'query_patterns_after_init'=>$patterns,'query_patterns_dropped'=>(int)$GLOBALS['pads_query_patterns_dropped'],
        'targeted_trace'=>pads_targeted_trace(),'design_performance_probe'=>(array)$GLOBALS['pads_menu_probe'],
        'hot_hooks'=>array(),'hook_tags_dropped'=>0,
        'http_time_s'=>round($httpTime,6),'http_calls'=>count((array)$GLOBALS['pads_http_done']),'http_by_owner'=>$httpBy,
        'assets'=>pads_assets(),'included_files_by_owner'=>pads_included_files_by_owner(),
        'peak_memory_bytes'=>memory_get_peak_usage(true),'memory_bytes'=>memory_get_usage(true),
        'response_code'=>function_exists('http_response_code')?http_response_code():null,
        'queried_post_type'=>function_exists('get_post_type')?get_post_type():null,
        'is_singular'=>function_exists('is_singular')?is_singular():null,'is_archive'=>function_exists('is_archive')?is_archive():null,
        'template'=>isset($GLOBALS['template'])?wp_normalize_path((string)$GLOBALS['template']):'',
        'last_php_error'=>error_get_last()
    );
    pads_merge($uid,$r['id'],'server',$data);
});

add_action('admin_menu',function(){add_management_page('Performance Diagnose Safe','Performance Diagnose Safe','manage_options','performance-diagnose-safe','pads_admin');});
add_action('wp_ajax_pads_start',function(){
    check_ajax_referer('pads_admin','nonce');if(!current_user_can('manage_options'))wp_send_json_error(array('message'=>'Keine Berechtigung.'),403);
    $uid=get_current_user_id();$s=array('active'=>true,'session_id'=>wp_generate_uuid4(),'started_at_utc'=>gmdate('c'));
    set_transient(pads_recording_key($uid),$s,PADS_TTL);pads_save_report($uid,pads_new_report($s));wp_send_json_success(array('session'=>$s));
});
add_action('wp_ajax_pads_stop',function(){
    check_ajax_referer('pads_admin','nonce');if(!current_user_can('manage_options'))wp_send_json_error(array('message'=>'Keine Berechtigung.'),403);
    $uid=get_current_user_id();$r=pads_report($uid);if($r){$r['stopped_at_utc']=gmdate('c');pads_save_report($uid,$r);}delete_transient(pads_recording_key($uid));wp_send_json_success(array('pageviews'=>count($r['pageviews']??array())));
});
add_action('wp_ajax_pads_clear',function(){check_ajax_referer('pads_admin','nonce');if(!current_user_can('manage_options'))wp_send_json_error(null,403);delete_user_meta(get_current_user_id(),pads_report_key(get_current_user_id()));wp_send_json_success();});
add_action('admin_post_pads_export',function(){
    if(!current_user_can('manage_options'))wp_die('Keine Berechtigung.');check_admin_referer('pads_export');$r=pads_report(get_current_user_id());if(!$r)wp_die('Kein Bericht vorhanden.');
    nocache_headers();header('Content-Type: application/json; charset=utf-8');header('Content-Disposition: attachment; filename="performance-diagnose-safe-'.gmdate('Ymd-His').'.json"');echo wp_json_encode($r,JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE);exit;
});
function pads_admin(){
    if(!current_user_can('manage_options'))return;$uid=get_current_user_id();$r=pads_report($uid);$s=get_transient(pads_recording_key($uid));$active=is_array($s)&&!empty($s['active']);$count=count($r['pageviews']??array());$nonce=wp_create_nonce('pads_admin');$export=wp_nonce_url(admin_url('admin-post.php?action=pads_export'),'pads_export');
?>
<div class="wrap"><h1>Performance Diagnose Safe</h1>
<p><strong>Aufzeichnung:</strong> <?php echo $active?'LÄUFT':'GESTOPPT'; ?> · Seitenaufrufe: <strong><?php echo (int)$count; ?></strong></p>
<p><button class="button button-primary" id="pads-start" <?php disabled($active); ?>>Aufzeichnung starten</button> <button class="button" id="pads-stop" <?php disabled(!$active); ?>>Aufzeichnung stoppen</button> <?php if($r): ?><a class="button" href="<?php echo esc_url($export); ?>">JSON-Bericht herunterladen</a><?php endif; ?> <button class="button" id="pads-clear">Bericht löschen</button></p>
<div class="notice notice-info inline"><p><strong>Sicherheitsregel:</strong> Dieses Plugin erstellt keine MU-Datei, deaktiviert keine Plugins und verändert weder <code>active_plugins</code> noch <code>wp-config.php</code>.</p></div>
<h2>Erfasste Seiten</h2><table class="widefat striped"><thead><tr><th>URL</th><th>Server</th><th>Queries</th><th>HTTP</th><th>TTFB</th><th>LCP</th><th>DOM</th><th>Requests</th></tr></thead><tbody>
<?php if($r && !empty($r['pageviews'])):foreach(array_reverse($r['pageviews']) as $pv):$sv=$pv['server']??array();$b=$pv['browser']??array();?><tr><td><?php echo esc_html($b['url']??$sv['url']??''); ?></td><td><?php echo isset($sv['server_time_s'])?esc_html(number_format_i18n($sv['server_time_s'],3)).' s':'—'; ?></td><td><?php echo isset($sv['db_queries_total'])?(int)$sv['db_queries_total']:'—'; ?></td><td><?php echo isset($sv['http_time_s'])?esc_html(number_format_i18n($sv['http_time_s'],3)).' s':'—'; ?></td><td><?php echo isset($b['navigation']['ttfb_ms'])?esc_html(number_format_i18n($b['navigation']['ttfb_ms'],0)).' ms':'—'; ?></td><td><?php echo isset($b['lcp_ms'])?esc_html(number_format_i18n($b['lcp_ms'],0)).' ms':'—'; ?></td><td><?php echo isset($b['dom_elements'])?(int)$b['dom_elements']:'—'; ?></td><td><?php echo isset($b['resource_count'])?(int)$b['resource_count']:'—'; ?></td></tr><?php endforeach;else:?><tr><td colspan="8">Noch keine Messdaten.</td></tr><?php endif;?></tbody></table><p id="pads-msg"></p></div>
<script>(function(){const ajax=<?php echo wp_json_encode(admin_url('admin-ajax.php')); ?>,nonce=<?php echo wp_json_encode($nonce); ?>;async function call(a){const f=new FormData();f.append('action',a);f.append('nonce',nonce);const x=await fetch(ajax,{method:'POST',credentials:'same-origin',body:f});const j=await x.json();if(!j.success)throw new Error((j.data&&j.data.message)||'Fehler');return j.data}const m=document.getElementById('pads-msg');document.getElementById('pads-start').onclick=async()=>{try{await call('pads_start');location.reload()}catch(e){m.textContent=e.message}};document.getElementById('pads-stop').onclick=async()=>{try{await call('pads_stop');location.reload()}catch(e){m.textContent=e.message}};document.getElementById('pads-clear').onclick=async()=>{if(!confirm('Bericht wirklich löschen?'))return;try{await call('pads_clear');location.reload()}catch(e){m.textContent=e.message}}})();</script>
<?php }