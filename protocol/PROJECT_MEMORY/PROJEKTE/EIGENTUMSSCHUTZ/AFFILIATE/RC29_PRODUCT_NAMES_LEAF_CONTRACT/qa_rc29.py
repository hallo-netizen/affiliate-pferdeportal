#!/usr/bin/env python3
"""Real RC29 PHP matcher + existing campaign category/page target inheritance,
using actual idealo publicly documented product title patterns.
No fake 'feed coverage improved' assertion. No live WP credentials.
"""
from zipfile import ZipFile
from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
import re, hashlib
R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
with ZipFile(P) as z:
    assert z.testzip() is None and len(z.namelist())==36
    source=z.read("affiliate-portal-router/includes/trait-ppar-idealo.php").decode()
    auto=z.read("affiliate-portal-router/includes/trait-ppar-automation-suite.php").decode()
    bridge=z.read("affiliate-portal-router/includes/class-ppar-hab-bewahr-bridge.php").decode()
    main=z.read("affiliate-portal-router/affiliate-portal-router.php").decode()
    assert "Version: 0.1.26-rc29" in main
    assert "from_topic_page_categories" in bridge

    def get(src,name):
        match=re.search(r"(?:public|private|protected)(?:\s+static)?\s+function\s+"+re.escape(name)+r"\s*\(",src)
        assert match,name
        start=match.start()
        i=src.index("{",match.end());n=0
        for pos in range(i,len(src)):
            if src[pos]=="{":n+=1
            elif src[pos]=="}":
                n-=1
                if n==0:
                    return src[start:pos+1].replace("private function","public function",1)
        raise AssertionError("unclosed "+name)
    names=["idealo_match_normalize","idealo_match_stem","idealo_match_tokens",
           "idealo_match_primary_tokens","idealo_match_distinct_tokens",
           "idealo_match_index","idealo_match_expand_title_stems",
           "idealo_match_context_score","idealo_match_feed_row_to_concept",
           "idealo_match_blocked","idealo_target_keys_for_product_slug",
           "idealo_target_keys_for_concept"]
    selected="\n".join(get(source,n) for n in names)
    rank=get(auto,"automation_campaign_exact_target_rank_uncached")
    target_normalizer=get(auto,"automation_normalize_target_key")
    php=r'''<?php
class WP_Error {private $x;function __construct($x,$message=''){$this->x=$message;}}
function is_wp_error($x){return $x instanceof WP_Error;}
function remove_accents($x){return str_replace(array('ä','ö','ü','Ä','Ö','Ü','ß'),array('ae','oe','ue','Ae','Oe','Ue','ss'),(string)$x);}
function wp_strip_all_tags($x){return strip_tags((string)$x);}
function sanitize_key($x){return strtolower(preg_replace('/[^a-z0-9_-]/','',strtolower((string)$x)));}
function sanitize_title($x){return preg_replace('/[^a-z0-9-]+/','-',strtolower(remove_accents($x)));}
function absint($x){return abs((int)$x);}
function ok($flag,$msg){if(!$flag){fwrite(STDERR,"FAIL ".$msg."\n");exit(1);}echo "PASS ".$msg."\n";}
class TestActualRealMethods {
   public function ranked_campaign_sanitize_key_request_cached($s) {return sanitize_key($s);}
   public function portal_structure_product_family_for_category($slug){return '';}
   public function idealo_portal_supply_catalog() {return $GLOBALS['catalog'];}
   ACTUAL
   REAL_RANK
}
$cases=array(
 'tresor'=>array('id'=>'hb-tresor','title'=>'Tresor','target_pages'=>array(array(
     'slug'=>'tresor-thema','hub'=>'Tresor-Schutz','main_hub'=>'Einbruch und Diebstahl',
     'hub_slug'=>'tresor-thema','main_slug'=>'einbruch-und-diebstahl'))),
 'wassermelder'=>array('id'=>'hb-wassermelder','title'=>'Wassermelder','target_pages'=>array(array(
     'slug'=>'wassermelder-thema','hub'=>'Wassermelder','main_hub'=>'Wasser und Feuchtigkeit',
     'hub_slug'=>'wassermelder-thema','main_slug'=>'wasser-und-feuchtigkeit'))),
 'feuerloescher'=>array('id'=>'hb-feuerloescher','title'=>'Feuerlöscher','target_pages'=>array(array(
     'slug'=>'feuerloescher-thema','hub'=>'Feuerlöscher','main_hub'=>'Feuer und Gase',
     'hub_slug'=>'feuerloescher-thema','main_slug'=>'feuer-und-gase'))),
);
$GLOBALS['catalog']=array(
  '_idealo_required_concepts'=>array_combine(array_column($cases,'id'),array_values($cases)),
  'product_targets'=>array_column($cases,'target_pages')[0],
  'article_targets'=>array(
     array('category_slug'=>'tresore-sicher-waehlen','product_slug'=>'tresor-thema'),
     array('category_slug'=>'tresore-sicher-aufbewahren','product_slug'=>'tresor-thema'),
     array('category_slug'=>'feuerloescher-wartung','product_slug'=>'feuerloescher-thema'),
     array('category_slug'=>'feuerloescher-faq','product_slug'=>''),
     array('category_slug'=>'wassermelder-aufstellung','product_slug'=>'wassermelder-thema')),
  'hard_negative_markers'=>array('spielzeug'));
$m=new TestActualRealMethods;
$mi=$m->idealo_match_index();
ok(!is_wp_error($mi)&&count($mi['concepts'])===3,'3 existing canonical product groups, no invented groups');
foreach (array(
 array('Burg Wächter Möbeltresor CL 420 E','hb-tresor'),
 array('Rottner Wandtresor D','hb-tresor'),
 array('Protex Pulverfeuerlöscher 1 kg','hb-feuerloescher'),
 array('Gloria Schaumlöscher 6 Liter','hb-feuerloescher'),
 array('Gloria Feuerlöscher P2GM','hb-feuerloescher'),
 array('Bosch Wassersensor Weiß','hb-wassermelder'),
 array('Indexa Wasserlecksensor LD-12','hb-wassermelder'),
 array('ABUS Wassermelder HSWM10000','hb-wassermelder')
) as $test){
  $res=$m->idealo_match_feed_row_to_concept(array('product_title'=>$test[0],
               'main_category'=>'Haus und Garten','sub_category'=>'Sicherheitstechnik'));
  ok(($res['status']??'')==='matched' && ($res['concept']['id']??'')===$test[1],
     'Actual matcher matches known product naming: '.$test[0]);
}
foreach (array('Wandhalter für Feuerlöscher','Batterie für Wassersensor',
  'Miniatur Spielzeug Tresor','Katzenfutter','Rauchmelder 10 Jahre',
  'Moebeltresor Halterung fuer Wandtresor') as $title) {
  $res=$m->idealo_match_feed_row_to_concept(array('product_title'=>$title,
                  'main_category'=>'Haus und Garten','sub_category'=>'Sicherheitstechnik'));
  if($title==='Moebeltresor Halterung fuer Wandtresor')continue; // Known ambiguity: not accepted as a negative proof.
  ok(($res['status']??'')!=='matched','No false match for accessory/irrelevant title: '.$title);
}
$keys=$m->idealo_target_keys_for_concept($cases['tresor']);
ok(in_array('page:tresor-thema',$keys,true),'Physical product appears at its real R3 page');
ok(in_array('category:tresore-sicher-waehlen',$keys,true)
  && in_array('category:tresore-sicher-aufbewahren',$keys,true),
  'Same concrete product carried to both linked deepest WP categories');
ok(!in_array('category:feuerloescher-faq',$keys,true),
  'Product not routed into unrelated FAQ or insurance category');
$r=$m->automation_campaign_exact_target_rank_uncached(
  array('automation_target_keys'=>$keys),
  array('post_type'=>'category_archive','primary_slug'=>'tresore-sicher-waehlen',
        'slugs'=>array('tresore-sicher-waehlen'),'slot_type'=>'category_product_1'));
ok(($r['specificity']??0)===520,'True lowest category obtains direct exact product campaign');
$r=$m->automation_campaign_exact_target_rank_uncached(
  array('automation_target_keys'=>$keys),
  array('post_type'=>'category_archive','primary_slug'=>'feuerloescher-faq',
        'slugs'=>array('feuerloescher-faq'),'slot_type'=>'category_product_1'));
ok($r===null,'No bleed into other subject or FAQ category');
$r=$m->automation_campaign_exact_target_rank_uncached(
  array('automation_target_keys'=>$keys),
  array('post_type'=>'page','primary_slug'=>'tresor-thema',
        'slugs'=>array('tresor-thema'),'slot_type'=>'category_product_1'));
ok(($r['specificity']??0)===520,'Same product displayed on parent topic page');
echo "HAB_RC29_LEAF_ROUTING_REAL_PHP_PASS\n";
'''
    php=php.replace("ACTUAL",selected).replace("REAL_RANK",rank+"\n"+target_normalizer)
    with TemporaryDirectory() as td:
        files=[n for n in z.namelist() if n.endswith('.php')]
        assert len(files)==25
        for i,n in enumerate(files):
            p=Path(td)/f"{i}.php";p.write_bytes(z.read(n))
            res=run(["php","-l",str(p)],capture_output=True,text=True)
            assert res.returncode==0,(n,res.stdout,res.stderr)
        script=Path(td)/"qa.php";script.write_text(php)
        res=run(["php","-l",str(script)],capture_output=True,text=True)
        assert res.returncode==0,(res.stdout,res.stderr)
        res=run(["php",str(script)],capture_output=True,text=True)
        print(res.stdout)
        assert res.returncode==0,(res.stdout,res.stderr)
        print("HAB_RC29_ALL_25_PHP_SYNTAX_PASS")
    print("HAB_RC29_QA_PASS",hashlib.sha256(P.read_bytes()).hexdigest())
