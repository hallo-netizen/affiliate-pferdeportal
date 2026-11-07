<?php
declare(strict_types=1);
define('ABSPATH','/qa/');
define('ARRAY_A','ARRAY_A');
require_once $argv[1] ?? throw new RuntimeException('MINI source required');
function check(bool $ok,string $label):void{if(!$ok)throw new RuntimeException('FAILED '.$label);echo "PASS $label\n";}
function get_post_types(array $args,string $format='names'): array {
    return ($args['public']??false)?['post','page','pferderasse']:['page','pferderasse'];
}
function wp_strip_all_tags(string $s):string{return strip_tags($s);}
function wp_json_encode($x,int $options=0){return json_encode($x,$options);}
final class PSTE_Editorializer {public static function sourceQuery(array $x):string{return (string)($x['raw_query']??'');}}
final class PSTE_Repository {public static function table(string $x):string{return 'wp_pste_topic_pool';}}
final class PSTE_Snapshot {public static function editorialPlan():array{return ['status'=>'NOT_AVAILABLE','sha256'=>'NOT_AVAILABLE','items'=>[]];}}
final class FakeDb {
    public string $posts='wp_posts';
    public string $postmeta='wp_postmeta';
    public string $term_relationships='wp_term_relationships';
    public string $term_taxonomy='wp_term_taxonomy';
    public string $terms='wp_terms';
    public string $last_error='';
    public bool $failCount=false;
    private int $wpCountCalls=0;
    public function prepare(string $sql,...$args):string {
        $n=0;
        return preg_replace_callback('/%[sd]/',static function(array $m) use (&$n,$args):string {
            $v=$args[$n++];
            return $m[0]==='%d'?(string)(int)$v:"'".str_replace("'","''",(string)$v)."'";
        },$sql);
    }
    public function get_var(string $sql) {
        if(str_contains($sql,'FROM wp_posts')){
            $this->wpCountCalls++;
            return ($this->failCount && $this->wpCountCalls>1)?3:2;
        }
        if(str_contains($sql,'FROM wp_pste_topic_pool'))return 1;
        throw new RuntimeException('Unexpected COUNT query:'.$sql);
    }
    public function get_results(string $sql,string $format):array {
        if(str_contains($sql,'FROM wp_posts')){
            preg_match('/ID>(\d+)/',$sql,$m);
            if((int)($m[1]??0)>0)return [];
            return [
                ['ID'=>7,'post_title'=>'Pferdeanhänger für zwei Pferde',
                    'post_type'=>'post','post_status'=>'publish','post_name'=>'pferdeanhaenger',
                    'post_content'=>'<h2>Passende Anhänger auswählen</h2>Long article content','post_modified_gmt'=>'2026-11-07 12:00:00'],
                ['ID'=>9,'post_title'=>'Pferde-Glossar: Regendecke',
                    'post_type'=>'pferderasse','post_status'=>'private','post_name'=>'decke',
                    'post_content'=>'<h3>Was ist eine ungefütterte Decke?</h3>Glossar','post_modified_gmt'=>'2026-11-07 12:10:00'],
            ];
        }
        if(str_contains($sql,'FROM wp_postmeta'))return [
            ['post_id'=>7,'meta_value'=>'2er pferdeanhänger'],['post_id'=>9,'meta_value'=>'ungefüttert']
        ];
        if(str_contains($sql,'FROM wp_term_relationships'))return [
            ['post_id'=>7,'category_id'=>234,'category_name'=>'Pferdeanhänger']
        ];
        if(str_contains($sql,'FROM wp_pste_topic_pool')){
            preg_match('/id>(\d+)/',$sql,$m);
            if((int)($m[1]??0)>0)return [];
            return [['id'=>101,'pool_key'=>'pste-planned-101',
                'payload_json'=>json_encode(['raw_query'=>'horseware regendecken',
                    'production_title'=>'Regendecken von Horseware','target_keyword'=>'horseware regendecken',
                    'target_category_name'=>'Regendecken','proposed_article_type'=>'Beratung',
                    'intent_profile'=>['search_intent'=>'Marke']]),
                'planning_suitability'=>'YES','automatic_pool_status'=>'PASS']];
        }
        throw new RuntimeException('Unexpected SQL:'.$sql);
    }
}
final class PSERC_Plan_Snapshot_Store {
    public static bool $missing=false;
    public static function getActive():array {return ['contract'=>'PSERC_PLAN_SNAPSHOT_V1',
        'generation'=>str_repeat('a',20),'snapshot_sha256'=>str_repeat('1',64),
        'dependency'=>[],'counts'=>['compiled_items'=>1]];}
    public static function verifyHeader(array $header):bool{return ($header['contract']??'')==='PSERC_PLAN_SNAPSHOT_V1';}
    public static function getRecord(string $g,string $k,int $i):?array {
        return self::$missing?null:['status'=>'REVIEW_REQUIRED_SEMANTIC_OVERLAP',
            'seo_topic_id'=>'pserc-final-1','title'=>['production_title'=>'Günstige Pferdedecken'],
            'target_keyword'=>['value'=>'guenstige pferdedecken'],'article_type'=>'Beratung',
            'category'=>['slug'=>'regendecken'],'canonical_slot'=>null,'intent_profile'=>[]];
    }
}
final class PSERC_Plan_Dependency_Fingerprint {public static bool $current=true;public static function isCurrent(array $x):bool{return self::$current;}}
$wpdb=new FakeDb();
$out=PSTE_Mini_Workflow::readParkhausForMini();
check($out['complete']===true,'all three existing sources complete');
check(count($out['items'])===4,'two WP, one PSTE and one PSERC row retained');
check(count(array_filter($out['items'],static fn($x)=>($x['source']??'')==='WORDPRESS'))===2,'all relevant WP post types included');
check($out['items'][1]['status']==='private','private SEO page included');
check(in_array('Was ist eine ungefütterte Decke?',$out['items'][1]['headings'],true),'heading from full article retained');
check(!array_key_exists('post_content',$out['items'][0]),'article body not duplicated into export');
check($out['items'][0]['target_keyword']==='2er pferdeanhänger','real SEO target metadata retained');
check($out['items'][2]['source']==='PSTE_PLAN'&&$out['items'][3]['source']==='PSERC_ACTIVE_PLAN','both planning sources included');
check($out['items'][3]['status']==='REVIEW_REQUIRED_SEMANTIC_OVERLAP','held PSERC plan retained');
check(preg_match('/^[a-f0-9]{64}$/D',$out['sha256'])===1,'single snapshot version fingerprint');
PSERC_Plan_Dependency_Fingerprint::$current=false;
$out=PSTE_Mini_Workflow::readParkhausForMini();
check($out['complete']===false,'stale PSERC source never produces complete parkhouse');
PSERC_Plan_Dependency_Fingerprint::$current=true;
$wpdb=new FakeDb();$wpdb->failCount=true;
$out=PSTE_Mini_Workflow::readParkhausForMini();
check($out['complete']===false&&$out['reason']==='WP_INVENTORY_CHANGED_DURING_SCAN','changed WordPress during export blocks completeness');
echo "QA ONLY: coverage based on test DB, not verified real WP or external semantic worker\n";
