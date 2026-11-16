<?php
declare(strict_types=1);
require dirname(__DIR__) . '/PLUGINS/QUELLCODE/W30_seo_handoff_readonly.php';
$base = [
  'version' => 'W28_2026-11-16',
  'einzige_masterquelle' => 'protocol/PROJECT_MEMORY/PROJEKTE/WASSERTECHNIK/REGISTER_GLOSSAR/W27_ZENTRALES_FACHREGISTER_20261116.json',
  'status' => 'ABGELEITETER_EINMAL_HANDOFF_NICHT_AKTIVER_MASTER_KEINE_SEO_WP_FREIGABE',
  'anzahl' => 81,
  'produkte' => []
];
for ($i=1;$i<=81;$i++) {
 $id='W14-'.str_pad((string)$i,3,'0',STR_PAD_LEFT);
 $base['produkte'][]=['register_id'=>$id,'kanonisch_id'=>$id,'produktname'=>'Testprodukt '.$i,'geplanter_hauptbereich'=>'TRINK',
 'keyword_vorschlag_ungeprueft'=>'testprodukt '.$i,'seo_status'=>'ungeprueft','w5_suchvolumen'=>'nicht_gemessen',
 'fachstatus'=>'marktprodukt','seo_owner_freigabe'=>false,'wp_seitenfreigabe'=>false,'referenzierte_funktionsvergleiche'=>[],
 'quellen'=>[['url'=>'https://example.org/'. $i]],
 'artikelkategorien'=>[['name'=>'Auswahl','article_ideas'=>['Einbau '.$i,'Betrieb '.$i,'Auswahl '.$i]]]];
}
for($i=0;$i<9;$i++)$base['produkte'][$i]['artikelkategorien'][]=['name'=>'Montage','article_ideas'=>['Schutz '.$i,'Pflege '.$i,'Kosten '.$i]];
$path=tempnam(sys_get_temp_dir(),'wt30_');
$assert=function($label,$doc,$ok)use($path){file_put_contents($path,json_encode($doc,JSON_UNESCAPED_UNICODE));$failed=false;try{$v=Wassertechnik_W30_Seo_Handoff::read($path);if(!$ok){$failed=true;}elseif($v['anzahl']!==81||$v['rubriken']!==90){$failed=true;}}catch(Throwable $e){if($ok){echo 'ERROR '.$label.': '.$e->getMessage().PHP_EOL;$failed=true;}}echo ($failed?'FAIL':'PASS').' '.$label.PHP_EOL;if($failed)exit(1);};
$assert('original 81, 90 rubriken',$base,true);
$a=$base;$a['produkte'][3]['kanonisch_id']='W14-002';$assert('alias/inconsistent canonical blocked',$a,false);
$a=$base;$a['produkte'][5]['register_id']=$a['produkte'][4]['register_id'];$assert('duplicate ID blocked',$a,false);
$a=$base;$a['produkte'][5]['keyword_vorschlag_ungeprueft']=$a['produkte'][4]['keyword_vorschlag_ungeprueft'];$assert('duplicate keyword blocked',$a,false);
$a=$base;unset($a['produkte'][3]);$assert('missing product blocked',$a,false);
$a=$base;$a['produkte'][3]['seo_owner_freigabe']=true;$assert('unapproved owner not silently approved',$a,false);
$a=$base;$a['produkte'][3]['wp_seitenfreigabe']=true;$assert('WP write not allowed',$a,false);
$a=$base;$a['produkte'][3]['seo_status']='complete';$assert('new unsupported SEO result blocked',$a,false);
$a=$base;$a['produkte'][3]['w5_suchvolumen']=0;$assert('missing volume not zero',$a,false);
$a=$base;$a['produkte'][3]['artikelkategorien'][0]['article_ideas']=['A','A','B'];$assert('duplicate article directions blocked',$a,false);
$a=$base;unset($a['produkte'][3]['quellen']);$assert('missing manufacturer sources blocked',$a,false);
$a=$base;$a['einzige_masterquelle']='fake W27';$assert('wrong master blocked',$a,false);
$a=$base;$a['produkte'][3]['geplanter_hauptbereich']='INDUSTRIE';$assert('unallowed main menu group blocked',$a,false);
unlink($path);
$actual=__DIR__.'/W28_SEO_EINMALHANDOFF_81_20261116.json';
if(is_file($actual)){$got=Wassertechnik_W30_Seo_Handoff::read($actual);echo 'PASS actual W28 file: '.$got['anzahl'].' candidates and '.$got['rubriken'].' rubric drafts'.PHP_EOL;}
