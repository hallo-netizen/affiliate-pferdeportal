<?php
declare(strict_types=1);
/**
 * W31 regression: run twice, once with untouched WT001 0.1.4 and once with the
 * staged additive source patch. Only mock functions. Never live WordPress.
 * Usage: php W31_WT001_014_GESAMT_REGRESSION.php /path/to/plugin-root
 */
$base=$argv[1]??'';
if(!$base)exit(2);
define('ABSPATH','/');
$GLOBALS['hooks']=[];$GLOBALS['updates']=0;$GLOBALS['posts']=0;$GLOBALS['term_writes']=0;$GLOBALS['http']=0;$GLOBALS['host']='wasser.oliver-beil.de';$GLOBALS['isadmin']=true;
function add_action($name,$call,$priority=10){$GLOBALS['hooks'][]=$name;}
function add_menu_page(...$args){return true;}
function add_submenu_page(...$args){return true;}
function wp_parse_url($url,$component){return parse_url($url,$component);}
function home_url($path='/'){return 'https://'.$GLOBALS['host'].$path;}
function current_user_can($right){return $GLOBALS['isadmin'];}
function wp_die($s){throw new RuntimeException('WP_DIE: '.$s);}
function wp_json_encode($value,$flags=0){return json_encode($value,$flags);}
function esc_html($s){return htmlspecialchars($s,ENT_QUOTES,'UTF-8');}
function update_option(...$a){$GLOBALS['updates']++;throw new RuntimeException('Unexpected WP WRITE');}
function wp_insert_post(...$a){$GLOBALS['posts']++;throw new RuntimeException('Unexpected WP PAGE WRITE');}
function wp_insert_term(...$a){$GLOBALS['term_writes']++;throw new RuntimeException('Unexpected WP TERM WRITE');}
function wp_remote_post(...$a){$GLOBALS['http']++;throw new RuntimeException('Unexpected PAID API');}
require $base.'/wassertechnik-kategorie-workflow.php';
$pre=Wassertechnik_DataForSEO::build_preflight();
[$origin,$terms,$owners]=Wassertechnik_PaidResearch::planned();
assert(count($terms)===218);
$counts=['preflight'=>$pre['unique_keywords'],'planned'=>count($terms),'fingerprint'=>$pre['fingerprint'],'counts'=>$pre['count'],'write_calls'=>$GLOBALS['updates']+$GLOBALS['posts']+$GLOBALS['term_writes'],'paid_calls'=>$GLOBALS['http']];
if(class_exists('Wassertechnik_Seo81_Preview')){
 $asset=$base.'/assets/wassertechnik-w28-seo-handoff.json';
 if(file_exists($asset))exit(3);
 ob_start();Wassertechnik_Seo81_Preview::screen();$s=ob_get_clean();
 if(!str_contains($s,'GESPERRT:'))throw new RuntimeException('Missing input must fail closed');
 $data=['version'=>'W28_2026-11-16','einzige_masterquelle'=>'protocol/PROJECT_MEMORY/PROJEKTE/WASSERTECHNIK/REGISTER_GLOSSAR/W27_ZENTRALES_FACHREGISTER_20261116.json','status'=>'ABGELEITETER_EINMAL_HANDOFF_NICHT_AKTIVER_MASTER_KEINE_SEO_WP_FREIGABE','anzahl'=>81,'produkte'=>[]];
 for($i=1;$i<=81;$i++){$id='W14-'.str_pad((string)$i,3,'0',STR_PAD_LEFT);$data['produkte'][]=['register_id'=>$id,'kanonisch_id'=>$id,'produktname'=>'Testprodukt '.$i,'geplanter_hauptbereich'=>'TRINK','keyword_vorschlag_ungeprueft'=>'testprodukt '.$i,'seo_status'=>'ungeprueft','w5_suchvolumen'=>'nicht_gemessen','fachstatus'=>'marktprodukt','seo_owner_freigabe'=>false,'wp_seitenfreigabe'=>false,'referenzierte_funktionsvergleiche'=>[],'quellen'=>[['url'=>'https://example.org/'.$i]],'artikelkategorien'=>[['name'=>'Einsatz','article_ideas'=>['Auswahl '.$i,'Betrieb '.$i,'Einbau '.$i]]]];}
 for($i=0;$i<9;$i++)$data['produkte'][$i]['artikelkategorien'][]=['name'=>'Pflege','article_ideas'=>['Wartung '.$i,'Reinigung '.$i,'Kosten '.$i]];
 file_put_contents($asset,json_encode($data,JSON_UNESCAPED_UNICODE));
 try{
  $p=Wassertechnik_Seo81_Preview::payload();if($p['anzahl']!==81||$p['rubriken']!==90)throw new RuntimeException('Wrong new input');
  ob_start();Wassertechnik_Seo81_Preview::screen();$html=ob_get_clean();
  if(substr_count($html,'<tr>')!==82||!str_contains($html,'NICHT GEMESSEN'))throw new RuntimeException('81 rows preview failed');
  $GLOBALS['host']='evil.example.com';try{Wassertechnik_Seo81_Preview::payload();throw new RuntimeException('Host guard FAIL');}catch(RuntimeException $e){if($e->getMessage()==='Host guard FAIL')throw $e;}
  $GLOBALS['host']='wasser.oliver-beil.de';$GLOBALS['isadmin']=false;try{Wassertechnik_Seo81_Preview::screen();throw new RuntimeException('Admin guard FAIL');}catch(RuntimeException $e){if($e->getMessage()==='Admin guard FAIL')throw $e;}
 }finally{unlink($asset);$GLOBALS['isadmin']=true;}
 $counts['new81_read']='PASS';$counts['new81_html_rows']=81;$counts['missing_file_fail_closed']=true;$counts['wrong_host_blocked']=true;$counts['not_admin_blocked']=true;$counts['hooks']=count($GLOBALS['hooks']);
}
$counts['write_calls']=$GLOBALS['updates']+$GLOBALS['posts']+$GLOBALS['term_writes'];$counts['paid_calls']=$GLOBALS['http'];
if($counts['write_calls']>0||$counts['paid_calls']>0)throw new RuntimeException('Unexpected site write or paid call');
echo json_encode($counts,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES).PHP_EOL;
