<?php
/** V84 fixture: actual new controller; WordPress functions and existing createOne worker mocked. */
declare(strict_types=1);
define('ABSPATH','/test/');
$opts=[];$posts=[];$terms=[];$postmeta=[];$termmeta=[];$writes=0;
function testcheck(bool $good,string $why):void {if(!$good)throw new RuntimeException('FAIL '.$why);echo "PASS ".$why."\n";}
function current_user_can($c):bool{return true;}
function add_action($hook,$fn,$priority=10):void{}
function get_option($name,$default=[]){global $opts;return $opts[$name]??$default;}
function update_option($name,$data,$autoload=false){global $opts;$opts[$name]=$data;return true;}
function add_option($name,$data,$deprecated='',$autoload='no'){global $opts;if(isset($opts[$name]))return false;$opts[$name]=$data;return true;}
function delete_option($name){global $opts;unset($opts[$name]);return true;}
function is_wp_error($x):bool {return false;}
function wp_json_encode($x,$opts=0){return json_encode($x,$opts);}
function get_posts($opts){global $posts;return array_values($posts);}
function get_terms($opts){global $terms;return array_values($terms);}
function get_post($id){global $posts;return $posts[(int)$id]??null;}
function get_term($id,$tax){global $terms;return $terms[(int)$id]??null;}
function get_post_meta($id,$key,$single=true){global $postmeta;return $postmeta[(int)$id][$key]??'';}
function get_term_meta($id,$key,$single=true){global $termmeta;return $termmeta[(int)$id][$key]??'';}
function update_post_meta($id,$key,$value):void{global $postmeta;$postmeta[(int)$id][$key]=$value;}
function update_term_meta($id,$key,$value):void{global $termmeta;$termmeta[(int)$id][$key]=$value;}
function sanitize_title($str):string {
    $s=iconv('UTF-8','ASCII//TRANSLIT//IGNORE',strtolower((string)$str));
    $s=strtolower((string)$s);
    $s=preg_replace('/[^a-z0-9]+/','-',$s);
    return trim($s,'-');
}
function wp_update_post($input,$return_error=false){
    global $posts;
    $id=(int)$input['ID'];
    if(!isset($posts[$id]))return 0;
    $posts[$id]->post_status=$input['post_status'];return $id;
}
class Robotik_V63_Delta {
    public static function prepare():array {
        global $posts,$terms;
        $pages=[];$cats=[];
        for($i=1;$i<=188;$i++)$pages['origin_page_'.str_pad((string)$i,3,'0',STR_PAD_LEFT)]=$i;
        for($i=1;$i<=296;$i++)$cats['origin_term_'.str_pad((string)$i,3,'0',STR_PAD_LEFT)]=1000+$i;
        // Marked existing parent IDs are created in this fixture explicitly.
        $pages['rbt_a7b82adfb00b8fd4']=1;
        $pages['rbt_4c3b60b5f506ff47']=2;
        $pages['rbt_c921e3a524a4ad2a']=3;
        $pages['rbt_e764c403a44632be']=4;
        $pages['rbt_ee14ec5df0d71085']=5;
        $pages['V52_HUB_Haushalt_Reinigung']=6;
        $pages['V52_HUB_Haushalt_Alltagshilfe']=7;
        $pages['rbt_2a9f15b10b6f0ff1']=8;
        // Return exactly 188 original sources with the actual parent names mapped to real mock IDs.
        $origin=[];
        for($i=1;$i<=188;$i++)$origin['origin_'.str_pad((string)$i,3,'0',STR_PAD_LEFT)]=$i;
        foreach(['rbt_a7b82adfb00b8fd4','rbt_4c3b60b5f506ff47','rbt_c921e3a524a4ad2a','rbt_e764c403a44632be','rbt_ee14ec5df0d71085','V52_HUB_Haushalt_Reinigung','V52_HUB_Haushalt_Alltagshilfe','rbt_2a9f15b10b6f0ff1'] as $i=>$key){unset($origin['origin_'.str_pad((string)($i+1),3,'0',STR_PAD_LEFT)]);$origin[$key]=$i+1;}
        return ['errors'=>[],'task_done'=>227,'task_remaining'=>0,'page_ids'=>$origin,'term_ids'=>$cats,
            'prior_wp_page_ids'=>range(1,188),'prior_wp_term_ids'=>range(1001,1296)];
    }
    public static function createOne(array $task,array &$pages,array &$terms):string {
        global $posts,$terms as $allterms,$writes;
        $source=$task['source_id'];
        if($task['kind']==='page'){
            if(isset($pages[$source]))return 'existing';
            $parent=(int)($pages[$task['parent_source_id']]??0);
            if(!$parent)throw new RuntimeException('Fixture: missing parent '.$source);
            $id=max(array_keys($posts))+1;
            $posts[$id]=(object)['ID'=>$id,'post_type'=>'page','post_parent'=>$parent,
                'post_name'=>$task['slug'],'post_title'=>$task['title'],'post_status'=>'draft'];
            update_post_meta($id,'_robotik_kategorie_node_id',$source);
            update_post_meta($id,'_robotik_page_role','product');
            $pages[$source]=$id;$writes++;return 'page';
        }
        if(isset($terms[$source]))return 'existing';
        $owner=(int)($pages[$task['parent_source_id']]??0);
        if(!$owner)throw new RuntimeException('Fixture: no category owner '.$source);
        $id=max(array_keys($allterms))+1;
        $allterms[$id]=(object)['term_id'=>$id,'parent'=>0,
            'name'=>$task['name'],'slug'=>$task['slug']];
        update_term_meta($id,'_robotik_kategorie_node_id',$source);
        update_term_meta($id,'_robotik_product_page_id',$owner);
        update_term_meta($id,'_robotik_short_label',$task['short_label']);
        $terms[$source]=$id;$writes++;return 'category';
    }
}
for($i=1;$i<=188;$i++)$posts[$i]=(object)['ID'=>$i,'post_type'=>'page','post_parent'=>0,
    'post_name'=>'baseline-'.$i,'post_title'=>'Baseline '.$i,'post_status'=>'publish'];
for($i=1001;$i<=1296;$i++)$terms[$i]=(object)['term_id'=>$i,'parent'=>0,'name'=>'Baseline '.($i-1000),'slug'=>'baseline-'.($i-1000)];
$options=['status'=>'COMPLETE'];
$opts['robotik_v78_gesamtabschluss_state']=$options;
$opts['robotik_v77_fachnachtrag_state']=['status'=>'COMPLETE','verified'=>64];
$source=$argv[1]??dirname(__DIR__).'/includes/class-robotik-v84-kategorien-nachtrag.php';
require $source;
$start=Robotik_V84_Kategorien_Nachtrag::plan();
testcheck($start['errors']===[] && $start['remaining']===48,'48 unique tasks, 188+296 preserved');
$manifest=hash_file('sha256',dirname($source).'/../assets/robotik-v84-delta.json');
$opts['robotik_v84_kategorien_nachtrag_state']=['status'=>'WRITING','index'=>0,'total'=>48,
    'authorized_once'=>true,'manifest'=>$manifest,'error'=>'','prior_pages'=>range(1,188),
    'prior_terms'=>range(1001,1296),'created_pages'=>0,'created_categories'=>0];
$loops=0;
while(($opts['robotik_v84_kategorien_nachtrag_state']['status']??'')==='WRITING'&&$loops++<12)
    Robotik_V84_Kategorien_Nachtrag::advance();
$s=$opts['robotik_v84_kategorien_nachtrag_state'];
testcheck($loops===6 && $s['status']==='COMPLETE','one approved task runs 6 batches');
testcheck($s['index']===48 && $s['verified']===48 &&
          $s['created_pages']===16 && $s['created_categories']===32,
          '16 pages published and 32 own flat categories');
testcheck($writes===48 && count($posts)===204 && count($terms)===328,'exactly 48 new objects, original sizes untouched');
$p=Robotik_V84_Kategorien_Nachtrag::plan();
testcheck($p['done']===48 && $p['errors']===[],'48 true WordPress meta/slug/owner readbacks');
Robotik_V84_Kategorien_Nachtrag::advance();
testcheck($writes===48,'second run does not duplicate items');
testcheck($posts[1]->post_name==='baseline-1' && $terms[1001]->slug==='baseline-1','old WordPress identities preserved');
$opts['robotik_v84_kategorien_nachtrag_state']=['status'=>'WRITING','index'=>0,'total'=>48,
    'authorized_once'=>true,'manifest'=>'CHANGED','error'=>'','prior_pages'=>range(1,188),
    'prior_terms'=>range(1001,1296)];
Robotik_V84_Kategorien_Nachtrag::advance();
testcheck($opts['robotik_v84_kategorien_nachtrag_state']['status']==='BLOCKED' && $writes===48,
          'changed manifest cannot publish');
echo "V84 16/32 ONE APPROVAL MOCK PASS\n";
