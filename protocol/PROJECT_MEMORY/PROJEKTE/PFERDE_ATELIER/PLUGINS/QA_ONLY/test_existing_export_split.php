<?php
declare(strict_types=1);
define('ABSPATH','/qa/');
require_once $argv[1] ?? throw new RuntimeException('patched plugin source argument required');
function get_option(string $name,$default=[]):array {
    if($name==='pste_mini_keyword_roundtrip_v1')return [
        'completed'=>['p1'=>['raw_query'=>'pferdedecken 0g',
            'decision'=>'JA','titles'=>[['intent'=>'Regendecken','title'=>'Regendecken ohne Füllung']]]],
        'active'=>null,'last_report'=>[]];
    return is_array($default)?$default:[];
}
function wp_json_encode($data,int $flags=0):string {return json_encode($data,$flags);}
function nocache_headers():void {}
final class PSTE_Auth {public static function assertAdmin(string $action,string $nonce):void{}}
$_POST['_wpnonce']='test';
if(($argv[2]??'')==='seo')$_POST['include_parkhaus']='1';
PSTE_Mini_Workflow::exportResults();
