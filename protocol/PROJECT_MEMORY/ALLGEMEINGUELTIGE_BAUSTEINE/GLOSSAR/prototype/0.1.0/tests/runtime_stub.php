<?php
// Minimal WordPress stubs for contract tests. No real WordPress behaviour is claimed.
define('ABSPATH','/tmp/');
$GLOBALS['actions']=[];$GLOBALS['filters']=[];$GLOBALS['options']=[];$GLOBALS['registered_post_types']=[];$GLOBALS['registered_taxonomies']=[];
function plugin_dir_path($f){return dirname($f).'/';}
function register_activation_hook($f,$c){} function register_deactivation_hook($f,$c){}
function add_action($h,$c,$p=10,$a=1){$GLOBALS['actions'][$h][]=$c;} function add_filter($h,$c,$p=10,$a=1){$GLOBALS['filters'][$h][]=$c;}
function apply_filters($h,$v,...$args){ foreach($GLOBALS['filters'][$h]??[] as $c){$v=$c($v,...$args);} return $v; }
function get_option($k,$d=[]){return $GLOBALS['options'][$k]??$d;} function update_option($k,$v){$GLOBALS['options'][$k]=$v;}
function sanitize_text_field($s){return trim(strip_tags((string)$s));} function sanitize_textarea_field($s){return trim(strip_tags((string)$s));}
function sanitize_title($s){$s=strtolower(trim((string)$s));$s=preg_replace('/[^a-z0-9]+/','-',$s);return trim($s,'-');}
function sanitize_key($s){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$s));} function absint($v){return abs((int)$v);}
function esc_url_raw($s){return filter_var($s,FILTER_SANITIZE_URL);} function flush_rewrite_rules($hard=true){}
function register_post_type($n,$a){$GLOBALS['registered_post_types'][$n]=$a;} function register_taxonomy($n,$o,$a){$GLOBALS['registered_taxonomies'][$n]=$a;}
function get_post_meta($id,$k,$single=true){return $GLOBALS['meta'][$id][$k]??'';} function update_post_meta($id,$k,$v){$GLOBALS['meta'][$id][$k]=$v;}
function get_the_title($id=0){return $GLOBALS['titles'][$id]??'Testbegriff';} function get_bloginfo($k){return 'Testportal';} function get_permalink($id){return 'https://example.test/glossar/testbegriff/';}
function is_singular($t=null){return true;} function get_queried_object_id(){return 7;} function esc_attr($s){return htmlspecialchars((string)$s,ENT_QUOTES);} function esc_url($s){return $s;}
function add_shortcode($a,$b){} function is_page($id){return false;} function wp_register_style(...$a){} function wp_enqueue_style(...$a){} function wp_add_inline_style(...$a){}
require dirname(__DIR__).'/universal-glossary-engine/universal-glossary-engine.php';
UGE_Core::register_content();
$fail=[];
$pt=$GLOBALS['registered_post_types']['uge_term']??null;
$tx=$GLOBALS['registered_taxonomies']['uge_group']??null;
if(!$pt || !$pt['public'] || $pt['show_in_menu']!=='uge-glossary') $fail[]='CPT contract';
if(in_array('thumbnail',$pt['supports'],true)) $fail[]='image requirement';
if(!$tx || !$tx['hierarchical'] || $tx['public']!==false) $fail[]='group contract';
$GLOBALS['titles'][7]='Beispiel';
$title=UGE_SEO::title(7); $desc=UGE_SEO::description(7);
if($title!=='Beispiel – Bedeutung & Erklärung | Testportal') $fail[]='SEO title pattern';
if(strpos($desc,'Beispiel')===false) $fail[]='SEO desc pattern';
$san=UGE_Config::sanitize(['rewrite_base'=>' !!! ','accordion_excerpt_words'=>999,'index_mode'=>'evil']);
if($san['rewrite_base']!=='glossar') $fail[]='empty slug fallback';
if($san['accordion_excerpt_words']!==120) $fail[]='word clamp';
if($san['index_mode']!=='index') $fail[]='index allowlist';
$GLOBALS['options'][UGE_Config::OPTION]=['design_profile'=>'pferde_atelier'];
$tokens=UGE_Config::design_tokens();
if($tokens['accent']!=='#27a653' || $tokens['radius']!=='22px') $fail[]='pferde profile';
$GLOBALS['options'][UGE_Config::OPTION]=['design_profile'=>'neutral'];
$neutral=UGE_Config::design_tokens();
if($neutral['accent']==='#27a653') $fail[]='profile isolation';
add_filter('uge_config', function($c){$c['label']='Lexikon';$c['term_label']='Eintrag';$c['group_label']='Themen';$c['rewrite_base']='wissen';$c['seo_title_pattern']='{term} | {site} Lexikon';return $c;});
add_filter('uge_field_schema', function($s){$s['source_note']=['label'=>'Quellenhinweis','type'=>'text','required'=>false];return $s;});
add_filter('uge_design_tokens', function($t,$profile){if($profile==='neutral'){$t['accent']='#123456';$t['radius']='4px';}return $t;},10,2);
UGE_Core::register_content();
$pt2=$GLOBALS['registered_post_types']['uge_term'];
if($pt2['labels']['singular_name']!=='Eintrag' || $pt2['rewrite']['slug']!=='wissen') $fail[]='second portal config';
if(!isset(UGE_Config::field_schema()['source_note'])) $fail[]='field extension';
if(UGE_Config::design_tokens()['accent']!=='#123456') $fail[]='second portal design';
if(UGE_SEO::title(7)!=='Beispiel | Testportal Lexikon') $fail[]='second portal SEO';
if($fail){foreach($fail as $f) echo "FAIL: $f\n";exit(1);} echo "RUNTIME_STUB_TOTAL_PASS\n";
