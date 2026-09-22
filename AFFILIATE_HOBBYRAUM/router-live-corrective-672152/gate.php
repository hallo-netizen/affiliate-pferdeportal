<?php
/*
 * Plugin Name: PPAR 6.72.152 Live-Pattern Gate
 */
if(!defined('ABSPATH')) exit;
final class PPAR152Gate{
  public $phase='old',$counts=['old'=>0,'new'=>0,'admin'=>0],$reg=0,$terms=0;
  private $defcache=[];
  public function __construct(){
    add_filter('sanitize_key',function($san,$raw){if(isset($this->counts[$this->phase]))$this->counts[$this->phase]++;return $san;},PHP_INT_MAX,2);
    add_filter('ppar_affiliate_provider_registry',function($r){$this->reg++;return $r;},10,1);
    add_filter('get_term',function($t){$this->terms++;return $t;},PHP_INT_MAX,1);
  }
  private function allowed(){return !is_admin() && !(defined('DOING_CRON')&&DOING_CRON) && !(defined('REST_REQUEST')&&REST_REQUEST) && !(defined('WP_CLI')&&WP_CLI) && !(function_exists('wp_doing_ajax')&&wp_doing_ajax());}
  private function old_rank($c,$ctx){
    $id=sanitize_key($c['id']);$net=sanitize_key($c['network']);$type=sanitize_key($c['creative_type']);
    $render=sanitize_key($c['render_mode']);$status=sanitize_key($c['programme_status']);$mode=sanitize_key($c['assignment_mode']);
    // repeated downstream single-field normalizations seen in 6.72.150
    $ok1=sanitize_key($c['creative_type'])==='banner';
    $ok2=sanitize_key($c['render_mode'])!=='html';
    $ok3=sanitize_key($c['network'])!=='';
    $ok4=sanitize_key($ctx['post_type'])==='page';
    $sl=array_map('sanitize_key',$ctx['slugs']);
    return [$id,$net,$type,$render,$status,$mode,$ok1,$ok2,$ok3,$ok4,$sl];
  }
  private function new_rank($c,$ctx){
    // same 6 per-candidate normalizations as 6.72.150; downstream reuses them
    $id=sanitize_key($c['id']);$net=sanitize_key($c['network']);$type=sanitize_key($c['creative_type']);
    $render=sanitize_key($c['render_mode']);$status=sanitize_key($c['programme_status']);$mode=sanitize_key($c['assignment_mode']);
    $post=sanitize_key($ctx['post_type']);$sl=array_map('sanitize_key',$ctx['slugs']);
    $ok1=$type==='banner';$ok2=$render!=='html';$ok3=$net!=='';$ok4=$post==='page';
    return [$id,$net,$type,$render,$status,$mode,$ok1,$ok2,$ok3,$ok4,$sl];
  }
  private function old_single($c){return sanitize_key($c['creative_type']);}
  private function new_single($c){return sanitize_key($c['creative_type']);}
  private function registry(){
    $raw=apply_filters('ppar_affiliate_provider_registry',['ebay'=>['capabilities'=>['creatives','outputs']], 'awin'=>['capabilities'=>['creatives','outputs']]]);
    $out=[];foreach($raw as $k=>$v){$k=sanitize_key($k);$out[$k]=['capabilities'=>array_map('sanitize_key',$v['capabilities'])];}
    return $out;
  }
  private function olddef($p){$p=sanitize_key($p);$r=$this->registry();return $r[$p]??null;}
  private function newdef($p){static $c=[];$raw=(string)$p;if($this->allowed()&&array_key_exists($raw,$c))return $c[$raw];$p=sanitize_key($raw);$r=$this->registry();$d=$r[$p]??null;if($this->allowed())$c[$raw]=$d;return $d;}
  private function oldterm(){return get_term_by('slug','private-anzeigen','hp_listing_category');}
  private function newterm(){static $done=false,$c=null;if($this->allowed()&&$done)return $c;$t=get_term_by('slug','private-anzeigen','hp_listing_category');if($this->allowed()){$c=is_object($t)?$t:null;$done=true;}return $t;}
  private function campaigns(){ $a=[]; for($i=0;$i<1200;$i++)$a[]=['id'=>'C '.$i,'network'=>$i%2?'ebay':'awin','creative_type'=>$i%3?'banner':'product','render_mode'=>$i%5?'image_link':'html','programme_status'=>'active','assignment_mode'=>'page_tree']; return $a; }
  public function publicGate(){
    $ctx=['post_type'=>'page','slugs'=>['Ausruestung','Pflege-Zubehoer']];
    $this->phase='old';$old=[];foreach($this->campaigns() as $c)$old[]=$this->old_rank($c,$ctx);$oldRank=$this->counts['old'];
    $before=$this->counts['old'];foreach($this->campaigns() as $c)$this->old_single($c);$oldSingle=$this->counts['old']-$before;
    for($i=0;$i<3000;$i++)$this->olddef($i%2?'ebay':'awin');for($i=0;$i<200;$i++)$this->oldterm();$oldTotal=$this->counts['old'];
    $this->phase='new';$new=[];foreach($this->campaigns() as $c)$new[]=$this->new_rank($c,$ctx);$newRank=$this->counts['new'];
    $before=$this->counts['new'];foreach($this->campaigns() as $c)$this->new_single($c);$newSingle=$this->counts['new']-$before;
    for($i=0;$i<3000;$i++)$this->newdef($i%2?'ebay':'awin');for($i=0;$i<200;$i++)$this->newterm();$newTotal=$this->counts['new'];
    return ['old_hash'=>hash('sha256',serialize($old)),'new_hash'=>hash('sha256',serialize($new)),'old_rank'=>$oldRank,'new_rank'=>$newRank,'old_single'=>$oldSingle,'new_single'=>$newSingle,'old_total'=>$oldTotal,'new_total'=>$newTotal];
  }
  public function adminGate(){ $this->phase='admin';for($i=0;$i<100;$i++){$this->newdef('ebay');$this->newterm();}return ['sanitize'=>$this->counts['admin'],'reg'=>$this->reg,'terms'=>$this->terms];}
}
$GLOBALS['g152']=new PPAR152Gate();
add_action('init',function(){if(!taxonomy_exists('hp_listing_category'))register_taxonomy('hp_listing_category','post',['public'=>false]);if(!term_exists('private-anzeigen','hp_listing_category'))wp_insert_term('Private Anzeigen','hp_listing_category',['slug'=>'private-anzeigen']);},1);
add_action('template_redirect',function(){if(!isset($_GET['g152']))return;header('Content-Type: application/json');echo wp_json_encode($GLOBALS['g152']->publicGate());exit;},-1000);
add_action('admin_post_nopriv_g152_admin',function(){header('Content-Type: application/json');echo wp_json_encode($GLOBALS['g152']->adminGate());exit;});
