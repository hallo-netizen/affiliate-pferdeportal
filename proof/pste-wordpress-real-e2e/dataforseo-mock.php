<?php
add_filter('query', static function($sql){
    if (stripos((string)$sql, 'pste_research_driver_lock_v1') === false) return $sql;
    $bt = debug_backtrace(DEBUG_BACKTRACE_IGNORE_ARGS, 12);
    $frames = [];
    foreach ($bt as $f) {
        $fn = (isset($f['class']) ? $f['class'].'::' : '').($f['function'] ?? '');
        $file = isset($f['file']) ? basename((string)$f['file']) : '';
        $line = (int)($f['line'] ?? 0);
        $frames[] = $fn.'@'.$file.':'.$line;
    }
    error_log('PSTE_LOCKSQL t='.sprintf('%.6f',microtime(true)).' pid='.getmypid().' uri='.(string)($_SERVER['REQUEST_URI']??'CLI').' sql_b64='.base64_encode((string)$sql).' bt_b64='.base64_encode(implode('>', $frames)));
    return $sql;
});

/**
 * External-provider-only deterministic mock.
 * NEVER intercept localhost / WordPress loopback. Internal PSTE runs unmodified.
 */
add_filter('pre_http_request', function($pre,$args,$url){
    $host=(string)parse_url($url,PHP_URL_HOST);
    if(!in_array($host,['sandbox.dataforseo.com','api.dataforseo.com'],true)) return $pre;
    $path=(string)parse_url($url,PHP_URL_PATH);
    $mode=(string)get_option('pste_e2e_provider_mode','normal');
    $counts=get_option('pste_e2e_provider_counts',[]);
    if(!is_array($counts))$counts=[];
    $counts[$path]=(int)($counts[$path]??0)+1;
    update_option('pste_e2e_provider_counts',$counts,false);

    if($mode==='transport_unknown_once' && str_contains($path,'keyword_suggestions') && (int)$counts[$path]===1){
        return new WP_Error('pste_e2e_transport_unknown','forced unknown provider outcome');
    }
    if($mode==='safe_503_once' && str_contains($path,'keyword_suggestions') && (int)$counts[$path]===1){
        return ['headers'=>[],'body'=>wp_json_encode(['status_code'=>50300,'status_message'=>'forced 503','cost'=>0.003]),'response'=>['code'=>503,'message'=>'Service Unavailable'],'cookies'=>[],'filename'=>null];
    }
    if($mode==='sleep_once' && str_contains($path,'keyword_suggestions') && (int)$counts[$path]===1){
        sleep(30);
    }

    $bodyRaw=(string)($args['body']??'');
    $req=json_decode($bodyRaw,true);
    $seed='';
    if(is_array($req)&&isset($req[0])&&is_array($req[0])){
        $seed=trim((string)($req[0]['keyword']??''));
        if($seed===''&&!empty($req[0]['keywords'][0]))$seed=trim((string)$req[0]['keywords'][0]);
    }
    if($seed==='')$seed='Heutaschen';
    $family=preg_replace('/\s+/u',' ',trim($seed));

    $ok=function(array $body){
        return ['headers'=>[],'body'=>wp_json_encode($body,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),'response'=>['code'=>200,'message'=>'OK'],'cookies'=>[],'filename'=>null];
    };
    $kw=function(string $q,int $vol){
        return ['keyword_data'=>['keyword'=>$q,'keyword_info'=>['search_volume'=>$vol,'monthly_searches'=>[],'competition'=>0.2,'cpc'=>0.15]]];
    };
    $base=['status_code'=>20000,'status_message'=>'Ok.','cost'=>0.001,'tasks_count'=>1,'tasks_error'=>0];

    if(str_ends_with($path,'/keyword_suggestions/live')){
        $body=$base;$body['tasks']=[['status_code'=>20000,'status_message'=>'Ok.','cost'=>0.001,'result'=>[['items'=>[
            $kw($family.' richtig auswählen',90),
            $kw($family.' sicher verwenden',70),
            $kw($family.' Größen vergleichen',60),
            $kw('Welche '.$family.' sind für Pferde geeignet?',50)
        ]]]]];
        return $ok($body);
    }
    if(str_ends_with($path,'/related_keywords/live')){
        $body=$base;$body['tasks']=[['status_code'=>20000,'status_message'=>'Ok.','cost'=>0.001,'result'=>[['items'=>[
            $kw($family.' kaufen worauf achten',80),
            $kw($family.' Vorteile Nachteile',65),
            $kw($family.' Pflege und Reinigung',55),
            $kw('Wie verwendet man '.$family.' richtig?',45)
        ]]]]];
        return $ok($body);
    }
    if(str_ends_with($path,'/keyword_ideas/live')){
        $body=$base;$body['tasks']=[['status_code'=>20000,'status_message'=>'Ok.','cost'=>0.001,'result'=>[['items'=>[
            $kw($family.' Test und Vergleich',75),
            $kw($family.' Kosten',58),
            $kw($family.' Sicherheit',52),
            $kw('Was muss man bei '.$family.' beachten?',48)
        ]]]]];
        return $ok($body);
    }
    if(str_ends_with($path,'/task_post')){
        $body=$base;$body['tasks']=[['id'=>'12345678-1234-1234-1234-123456789012','status_code'=>20000,'status_message'=>'Ok.','cost'=>0.001,'result'=>[]]];
        return $ok($body);
    }
    if(str_ends_with($path,'/tasks_ready')){
        $body=$base;
        $ready=true;
        if($mode==='paa_pending_once'){
            $n=(int)get_option('pste_e2e_paa_ready_count',0)+1;update_option('pste_e2e_paa_ready_count',$n,false);
            if($n===1)$ready=false;
        }
        $body['tasks']=[['status_code'=>20000,'status_message'=>'Ok.','cost'=>0.0,'result'=>[$ready?['id'=>'12345678-1234-1234-1234-123456789012']:[]]]];
        return $ok($body);
    }
    if(str_contains($path,'/task_get/advanced/')){
        $body=$base;$body['tasks']=[['status_code'=>20000,'status_message'=>'Ok.','cost'=>0.001,'result'=>[[
            'items'=>[
                ['type'=>'people_also_ask_element','title'=>'Welche '.$family.' sind für Pferde geeignet?'],
                ['type'=>'people_also_ask_element','title'=>'Wie befestigt man '.$family.' sicher?'],
                ['type'=>'people_also_ask_element','title'=>'Was kosten gute '.$family.'?']
            ]
        ]]]];
        return $ok($body);
    }
    return new WP_Error('pste_e2e_unhandled_provider_path',$path);
},10,3);
