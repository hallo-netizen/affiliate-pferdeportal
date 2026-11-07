<?php
declare(strict_types=1);
define('ABSPATH','/qa/');
$GLOBALS['options']=[];
function maybe_serialize($v):string{return serialize($v);}
function get_option(string $name,$default=null){return $GLOBALS['options'][$name]??$default;}
function wp_cache_delete(string $key,string $group):bool{return true;}
function good(bool $ok,string $name):void{if(!$ok)throw new RuntimeException('FAILED '.$name);echo "PASS $name\n";}
final class ExistingWordpressOptionsMock {
    public string $options='wp_options';
    public string $last_error='';
    public array $pending=[];
    public int $calls=0;
    public function prepare(string $sql,...$args):string {
        good(str_contains($sql,"BINARY option_value=BINARY %s"),'same existing option compared byte-for-byte');
        $this->pending=$args;
        return 'ATOMIC_COMPARE_AND_STORE';
    }
    public function query(string $sql):int {
        good($sql==='ATOMIC_COMPARE_AND_STORE','single SQL update, no extra lock or table');
        [$replacement,$key,$expected]=$this->pending;
        $this->calls++;
        if(!isset($GLOBALS['options'][$key])||serialize($GLOBALS['options'][$key])!==$expected)return 0;
        $GLOBALS['options'][$key]=unserialize($replacement,['allowed_classes'=>false]);
        return 1;
    }
}
$wpdb=new ExistingWordpressOptionsMock();
require_once $argv[1] ?? throw new RuntimeException('patched MINI code missing');
$original=['completed'=>[
    'topic-a'=>['raw_query'=>'horseware regendecken','decision'=>'JA','titles'=>[['intent'=>'brand','title'=>'Horseware Regendecken im Vergleich']]],
    'topic-b'=>['raw_query'=>'regenmantel pferd','decision'=>'JA','titles'=>[['intent'=>'rains','title'=>'Regenmäntel fürs Pferd richtig auswählen']]]
    ],'active'=>null,'last_report'=>[],'seo_decisions'=>[]];
$GLOBALS['options']['pste_mini_keyword_roundtrip_v1']=$original;
$sha=hash('sha256','unchanged-existing-WP-PSTE-PSERC-plan');
$snapshot=['complete'=>true,'sha256'=>$sha];
$document=function(string $key,string $raw,string $title)use($sha):array{
    return ['contract'=>'PSTE_MINI_SEO_DECISIONS_V1','owner'=>'EXTERNAL_SINGLE_SEO_EDITOR',
        'snapshot_sha256'=>$sha,'items'=>[[
        'pool_key'=>$key,'raw_query'=>$raw,
        'source_sha256'=>hash('sha256',$key.'|'.$raw),'box'=>'FREI',
        'intent_summary'=>'independent buyer intent',
        'intent_slot'=>str_repeat('a',64),'approved_title'=>$title]]];
};
$alpha=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($original,
    $document('topic-a','horseware regendecken','Horseware Regendecken im Vergleich'),$snapshot);
$beta=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($original,
    $document('topic-b','regenmantel pferd','Regenmäntel fürs Pferd richtig auswählen'),$snapshot);
$save=(new ReflectionClass(PSTE_Mini_Workflow::class))->getMethod('storeSeoDecisionsIfUnchanged');
$save->invoke(null,$original,$alpha);
good(($GLOBALS['options']['pste_mini_keyword_roundtrip_v1']['seo_decisions']['topic-a']['box']??'')==='FREI',
    'first approved slot stored in existing WP option');
try{$save->invoke(null,$original,$beta);throw new RuntimeException('CAS conflict was silently ignored');}
catch(ReflectionException $e){throw $e;}
catch(RuntimeException $e){
    good($e->getMessage()==='PSTE_MINI_ATOMIC_OPTION_CONFLICT_RELOAD_AND_RETRY',
        'concurrent old-state import rejected atomically');
}
$current=get_option('pste_mini_keyword_roundtrip_v1');
$betaRetried=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($current,
    $document('topic-b','regenmantel pferd','Regenmäntel fürs Pferd richtig auswählen'),$snapshot);
good(($betaRetried['seo_decisions']['topic-b']['box']??'')==='KLAERUNG',
    'same slot denied on safe retry WITHOUT second SEO judgement');
$save->invoke(null,$current,$betaRetried);
good(($GLOBALS['options']['pste_mini_keyword_roundtrip_v1']['seo_decisions']['topic-a']['box']??'')==='FREI',
    'first slot preserved after second importer was refused');
good($wpdb->calls===3,'three single-row atomic writes, not three semantic checks');
echo "ATOMIC_EXISTING_OPTION_QA_PASS\n";
