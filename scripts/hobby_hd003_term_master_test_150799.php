<?php
/** Executes ACTUAL design methods against a simulated WP category (positive/negative). */
define('ABSPATH','/tmp/');
class WP_Term {
    public $term_id,$name,$slug,$taxonomy='category';
    function __construct($id,$name,$slug){$this->term_id=$id;$this->name=$name;$this->slug=$slug;}
}
class WP_Post {}
$GLOBALS['term_meta']=[5311=>801,5312=>0,5313=>802,5314=>803];
$GLOBALS['image_state']=[
 801=>['https://test.invalid/wp-content/uploads/drachen-leinen.webp',1200,400],
 803=>['https://test.invalid/wp-content/uploads/broken.webp',0,0]
];
function get_term_meta($id,$key,$single){return $key==='thumbnail_id'?($GLOBALS['term_meta'][$id]??0):0;}
function wp_attachment_is_image($id){return isset($GLOBALS['image_state'][$id]);}
function wp_get_attachment_image_src($id,$size){return $GLOBALS['image_state'][$id]??false;}
function wp_get_attachment_image($id,$size,$icon=false,$args=[]){return isset($GLOBALS['image_state'][$id])?'<img src="'.esc_attr($GLOBALS['image_state'][$id][0]).'" data-wp-id="'.$id.'">':'';}
function get_term_link($term){return '/category/'.$term->slug.'/';}
function is_wp_error($v){return false;}
function esc_url($v){return htmlspecialchars($v,ENT_QUOTES);}
function esc_attr($v){return htmlspecialchars($v,ENT_QUOTES);}
function esc_html($v){return htmlspecialchars($v,ENT_QUOTES);}
function sanitize_title($v){return strtolower(str_replace([' ','&'],['-',''],trim($v)));}
function get_option($k,$d=[]){return $d;}
require_once $argv[1];
$rc=new ReflectionClass('Hobby_Depot_Profile_V150709');
function invoke($method,...$args){global $rc;$m=$rc->getMethod($method);$m->setAccessible(true);return $m->invoke(null,...$args);}
function check($b,$name){if(!$b){fwrite(STDERR,"FAIL: $name\n");exit(2);}echo "PASS: $name\n";}
$good=new WP_Term(5311,'Drachen & Leinen','sportdrachen-drachen-leinen');
$none=new WP_Term(5312,'Ohne Bild','ohne-bild');
$invalid=new WP_Term(5313,'Ungültige Mediennummer','ungueltig');
$broken=new WP_Term(5314,'Defekte Bildmaße','defekt');
$foreign=new WP_Term(5311,'Anderes','anderes');$foreign->taxonomy='post_tag';
$hero=invoke('term_master_hero_v150799',$good);
$tile=invoke('term_master_tile_v150799',$good);
check(str_contains($hero,'drachen-leinen.webp'),'Hero uses exact existing photo');
check(str_contains($hero,'data-hd-term-master="801"'),'Hero declares saved attachment ID');
check(str_contains($tile,'data-hd-term-master="801"'),'Tile uses SAME saved attachment ID');
check(str_contains($hero,'Drachen &amp; Leinen'),'Title correctly escaped');
foreach ([$none,$invalid,$broken,$foreign] as $term) {
 check(invoke('term_master_hero_v150799',$term)==='','Invalid or missing hero safely excluded: '.$term->slug);
 check(invoke('term_master_tile_v150799',$term)==='','Invalid or missing tile safely excluded: '.$term->slug);
}
$cards=invoke('render_category_level_term_cards_v150687',[$good],null,'bewegen','');
check(str_contains($cards,'data-hd-term-master="801"'),'ACTUAL design card renderer uses master image');
check(str_contains($cards,'has-photo'),'ACTUAL card labels image card');
$cards=invoke('render_category_level_term_cards_v150687',[$none],null,'bewegen','');
check(!str_contains($cards,'has-photo'),'ACTUAL card without photo keeps original symbol');
$code=file_get_contents($argv[1]);
check(str_contains($code,"$"."out.=self::term_master_hero_v150799("."$"."term)"),'ACTUAL owned-category template invokes master hero');
echo "ALL 16 POSITIVE AND NEGATIVE ASSERTIONS PASS\n";
