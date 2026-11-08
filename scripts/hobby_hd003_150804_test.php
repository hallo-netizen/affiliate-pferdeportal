<?php
/** Positive and negative runtime checks against actual HD003 1.50.804 class, no WP installation. */
define('ABSPATH','/tmp/');
class WP_Term {
  public $term_id,$name,$slug,$taxonomy,$description='';
  function __construct($id,$name,$slug,$taxonomy='category'){$this->term_id=$id;$this->name=$name;$this->slug=$slug;$this->taxonomy=$taxonomy;}
}
class WP_Post { public $ID=0; }
$GLOBALS['term_meta']=[5311=>801,5312=>0,5313=>802,5314=>803,5315=>804];
$GLOBALS['image_state']=[
 801=>['https://example.invalid/wp-content/uploads/drachen-leinen.webp',1500,1000],
 803=>['https://example.invalid/wp-content/uploads/broken.webp',0,0],
 804=>['https://example.invalid/wp-content/uploads/another.webp',1600,1067]
];
function get_term_meta($id,$key,$single){return $key==='thumbnail_id'?($GLOBALS['term_meta'][$id]??0):0;}
function wp_attachment_is_image($id){return isset($GLOBALS['image_state'][$id]);}
function wp_get_attachment_image_src($id,$size){return $GLOBALS['image_state'][$id]??false;}
function wp_get_attachment_image($id,$size,$icon=false,$args=[]){return isset($GLOBALS['image_state'][$id]) ? '<img data-wp-master-id="'.$id.'" src="'.esc_attr($GLOBALS['image_state'][$id][0]).'" alt="'.esc_attr((string)($args['alt']??'')).'">' : '';}
function get_term_link($term){return '/category/'.esc_attr($term->slug).'/';}
function is_wp_error($v){return false;}
function esc_url($v){return htmlspecialchars((string)$v,ENT_QUOTES,'UTF-8');}
function esc_attr($v){return htmlspecialchars((string)$v,ENT_QUOTES,'UTF-8');}
function esc_html($v){return htmlspecialchars((string)$v,ENT_QUOTES,'UTF-8');}
function sanitize_title($v){return strtolower(str_replace([' ','&'],['-',''],trim((string)$v)));}
function sanitize_key($v){return preg_replace('/[^a-z0-9_\\-]/','',strtolower((string)$v));}
function get_option($k,$d=[]){return $d;}
function wp_strip_all_tags($v){return strip_tags((string)$v);}
function wp_trim_words($v,$n=10,$more='…'){return implode(' ',array_slice(explode(' ',(string)$v),0,$n));}
function get_the_title($p){return $p instanceof WP_Term ? $p->name : '';}
function get_permalink($p){return '/test/';}
function get_post_meta($id,$key,$single){return '';}
function get_the_ID(){return 0;}
require_once $argv[1];
$rc=new ReflectionClass('Hobby_Depot_Profile_V150709');
function invoke($method,...$args){global $rc;$m=$rc->getMethod($method);$m->setAccessible(true);return $m->invoke(null,...$args);}
$n=0;
function check($b,$name){global $n; $n++;if(!$b){fwrite(STDERR,"FAIL [$n]: $name\n");exit(2);}echo "PASS [$n]: $name\n";}

$good=new WP_Term(5311,'Drachen & Leinen','sportdrachen-drachen-leinen');
$none=new WP_Term(5312,'Keine Bilddatei','kein-bild');
$wrongid=new WP_Term(5313,'Unbekannte Bildnummer','falsche-id');
$badsize=new WP_Term(5314,'Ungültige Bildmaße','defektes-bild');
$other=new WP_Term(5311,'Post Tag','post-tag','post_tag');
check(invoke('term_master_data_v150804',$good)['id']===801,'Reads exact existing thumbnail_id');
$hero=invoke('term_master_hero_v150804',$good);
$tile=invoke('term_master_tile_v150804',$good);
check(str_contains($hero,'drachen-leinen.webp'),'Hero uses exact URL of uploaded native image');
check(str_contains($tile,'drachen-leinen.webp'),'Tile uses exact URL of uploaded native image');
check(str_contains($hero,'data-hd-term-master="801"'),'Hero identifies the correct native attachment');
check(str_contains($tile,'data-hd-term-master="801"'),'Tile identifies SAME native attachment');
check(str_contains($hero,'Drachen &amp; Leinen'),'Hero's term name is HTML-escaped');
check(str_contains($tile,'hd-next-icon'),'Tile keeps the existing icon container layout');
foreach([$none,$wrongid,$badsize,$other] as $term) {
  check(invoke('term_master_data_v150804',$term)===[],'Invalid/wrong-taxonomy data rejected '.$term->slug);
  check(invoke('term_master_tile_v150804',$term)==='','Invalid/wrong-taxonomy tile falls back '.$term->slug);
  check(invoke('term_master_hero_v150804',$term)==='','Invalid/wrong-taxonomy hero falls back '.$term->slug);
}
$source=file_get_contents($argv[1]);
check(substr_count($source,"self::term_master_tile_v150804(")===3,'All THREE real category tile routes call the new helper');
check(substr_count($source,"self::term_master_hero_v150804(")===3,'All THREE real owned-category routes call the new helper');
check(str_contains($source,'render_category_level_term_cards_v150687'),'Original category-level rendering method preserved');
check(str_contains($source,'category_hero_image_v150757'),'Original WordPress page hero source preserved');
check(str_contains($source,'category_image_v150774'),'Existing approved fallback images preserved');
check(str_contains($source,'render_leaf_category_body_v150750'),'Old leaf category body and affiliate sections preserved');
echo "ALL $n PHP POSITIVE AND NEGATIVE TESTS PASSED\n";
