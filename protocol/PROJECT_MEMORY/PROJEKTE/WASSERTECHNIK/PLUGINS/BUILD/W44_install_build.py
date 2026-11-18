#!/usr/bin/env python3
"""W44 single-plugin update after REAL 81/81 DataForSEO result.
Combines existing W43 plugin with the already-authorized existing W35 importer:
219 unchanged old/Pool owners + 81 independently market-proven product DRAFT pages
+ 90 article-category owners = 390 total. Never publishes a new page.
No second writer, no second SEO charge, no WordPress connection from CI.
"""
import json,re,hashlib,subprocess,sys,shutil,unicodedata,zipfile
from pathlib import Path

PROJECT=Path(__file__).resolve().parents[2]
SOURCE=PROJECT/"PLUGINS"/"BUILD"/"W43_install_build.py"
OLDZIP=PROJECT/"PRUEFUNG"/"_w43_release"/"WASSERTECHNIK_KATEGORIE_WORKFLOW_0.1.13_W43_GESAMTUPDATE_INSTALLIEREN.zip"
WORK=PROJECT/"PRUEFUNG"/"_w44_install_build"
OUT=WORK/"WASSERTECHNIK_KATEGORIE_WORKFLOW_0.1.14_W44_KOMPLETTUPDATE_INSTALLIEREN.zip"
FOLDER="wassertechnik-kategorie-workflow"
OLDPLAN=PROJECT/"PLUGINS"/"ASSETS"/"W35_wordpress_importplan_219.json"
W28=PROJECT/"PRUEFUNG"/"W28_SEO_EINMALHANDOFF_81_20261116.json"
W44=PROJECT/"PRUEFUNG"/"W44_DATAFORSEO_81_GESAMTAUSWERTUNG_20261118.json"
AREA={"TRINK":("wt_main_01","wasseraufbereitung"),"MESSEN":("wt_main_02","wasseranalyse"),
      "BRUNNEN":("wt_main_03","brunnen"),"REGEN":("wt_main_05","regenwasser"),
      "ABWASSER":("wt_main_08","abwassertechnik"),"POOL":("wt_main_pool_w27","pool-teichtechnik")}
def must(ok,explanation):
    if not ok: raise RuntimeError("W44 RELEASE GESPERRT: "+str(explanation))
def run(args,expected=None):
    r=subprocess.run(args,text=True,capture_output=True,timeout=240)
    must(r.returncode==0 and (expected is None or expected in r.stdout),
         "Test: "+" ".join(map(str,args))+"\n"+r.stderr[-3000:]+"\n"+r.stdout[-3000:])
    return r.stdout
def repl(source,a,b,label="Text"):
    must(source.count(a)==1,label+" nicht eindeutig: "+a[:70])
    return source.replace(a,b,1)
def slug(s):
    s=s.lower().replace("ä","ae").replace("ö","oe").replace("ü","ue").replace("ß","ss")
    s=unicodedata.normalize("NFKD",s).encode("ascii","ignore").decode("ascii")
    s=re.sub(r"[^a-z0-9]+","-",s).strip("-")
    must(bool(s),"leerer Slug");return s
def prepare_targets(legacy,seo,products):
    old=legacy["wp_targets"]
    result=json.loads(json.dumps(legacy,ensure_ascii=False))
    ids={r["owner_id"] for r in old}
    paths={r["path"] for r in old if r["kind"]=="page"}
    slugs={r["slug"] for r in old if r["kind"]=="category"}
    entries={e["owner_id"]:e for e in seo["entries"]}
    must(len(entries)==81 and len(products)==81,"81 Fach-/SEO-Owner erwartet")
    must(len(old)==219 and len([r for r in old if r["kind"]=="page"])==114,"alte W35-Festbasis")
    newpages=[];newcats=[];published=[];owners=[]
    for p in products:
        id=p["kanonisch_id"];s=entries.get(id)
        must(s and s["label"]==p["produktname"] and s["keyword"]==p["keyword_vorschlag_ungeprueft"],
             "Master/W44 mismatch: "+id)
        must(s["owner_approval_on_wordpress"] is False and p["seo_owner_freigabe"] is False
             and p["wp_seitenfreigabe"] is False,"keine vorzeitige SEO/WordPress-Freigabe")
        must(p["fachstatus"]=="marktprodukt" and len(p["quellen"])>0,
             "Marktbeleg fehlt: "+id)
        area=p["geplanter_hauptbereich"];must(area in AREA,"unbekannter W27-Hauptbereich")
        parent,root=AREA[area]
        oid="wt_w44_prod_"+id
        path=root+"/"+slug(p["produktname"])
        must(path not in paths and oid not in ids,"WP-Doppel-Owner/-Pfad "+path)
        ids.add(oid);paths.add(path);owners.append(oid)
        newpages.append({"kind":"page","owner_id":oid,"title":p["produktname"],
           "legacy_title":None,"path":path,"legacy_path":None,
           "parent_owner_id":parent,"prior_parent_owner_id":None,
           "w6_original":False,"w44_new_draft":True,"seo_published":False,
           "draft_on_new":True,"source_product_id":id,
           "source_keyword":p["keyword_vorschlag_ungeprueft"],"source_seo_phase":"COMPLETED"})
        for j,cat in enumerate(p["artikelkategorien"],1):
            catid="wt_w44_cat_"+id+"_"+str(j)
            termslug="wt-w44-"+slug(id)+"-"+slug(cat["name"])
            must(catid not in ids and termslug not in slugs,
                 "Doppelte Kategorie "+catid+"/"+termslug)
            ids.add(catid);slugs.add(termslug)
            must(len(cat["article_ideas"])>=3,"zu wenig Artikelrichtungen "+catid)
            newcats.append({"kind":"category","owner_id":catid,
               "title":cat["name"],"slug":termslug,
               "legacy_slug":None,"product_owner_id":oid,
               "product_path":path,"legacy_product_path":None,
               "w6_original":False,"w44_new_draft":True,"source_product_id":id,
               "article_ideas":cat["article_ideas"]})
    must(len(newpages)==81 and len(newcats)==90,"81 neue Entwurfsseiten/90 Rubriken")
    result["wp_targets"].extend(newpages)
    result["wp_targets"].extend(newcats)
    result["source_candidates"]="PRUEFUNG/W44_DATAFORSEO_81_GESAMTAUSWERTUNG_20261118.json"
    result["source_paid_request_id"]=seo["source_request_id"]
    result["source_paid_state"]=seo["result_state"]
    result["source_paid_cost_usd"]=seo["spent_usd"]
    result["schema"]="wassertechnik-w35-one-time-wp-import-v1"
    result["counts"].update(total=390,pages=195,categories=195,new_hub_only=1,
                            products_new_draft_planned=81,
                            article_categories_new_draft_planned=90,
                            products_new_approved=0,
                            keyword_values_preserved=218,old_owner_count=218)
    result["policy"]+=" W44 adds only 81 W27 manufacturer-proven product drafts plus 90 attached article rubrics after the original single W35 admin approval. No SEO-owner permission or public publication follows merely from the paid API result."
    return result,owners
def write_final_tests(package):
    # Keep old W43 tests untouched; verify FINAL W44 plugin on adapted W35 WP fixture.
    oldtest=(PROJECT/"PRUEFUNG"/"W35_WP_IMPORT_ENDTOEND_QA.php").read_text()
    test=oldtest
    mapping={
      "count($plan['wp_targets'])===219":"count($plan['wp_targets'])===390",
      "verifyTarget($plan,114,0)":"verifyTarget($plan,195,0)",
      "verifyTarget($plan,1,23)":"verifyTarget($plan,82,23)",
      "verifyTarget($plan,0,0)":"verifyTarget($plan,0,0)",
      "$scenario==='blank'?114:1":"$scenario==='blank'?195:82",
      "count($GLOBALS['pages'])===116":"count($GLOBALS['pages'])===197",
      "count($GLOBALS['terms'])===106":"count($GLOBALS['terms'])===196",
      "count(array_filter($GLOBALS['pages'],fn($x)=>$x->post_status==='draft'))===2":
       "count(array_filter($GLOBALS['pages'],fn($x)=>$x->post_status==='draft'))===83",
      "'219 current W27 targets":" '390 current W27/W44 targets",
      "'114 W27 pages plus":" '195 W27/W44 pages plus",
      "'105 W27 category owners":" '195 W27/W44 category owners",
      "'complete 219-owner WP readback":" 'complete 390-owner WP readback",
      "'entire 114 page insert rolled back'":"'entire 195 page insert rolled back'",
      "'existing 105 category owners unchanged":"'existing 105 old category owners unchanged'",
    }
    for a,b in mapping.items():
        must(a in test,"W35-Regressionstoken fehlt "+a)
        test=test.replace(a,b)
    # Original old9 fixture MUST NOT precreate 90 new categories.
    test=repl(test,"foreach($plan['wp_targets'] as $r) if($r['kind']==='category'){",
              "foreach($plan['wp_targets'] as $r) if($r['kind']==='category' && $r['w6_original']){")
    # No delayed stage: simulate a fully imported 390-owner system in one idempotence test.
    snippet="""    $pool=$GLOBALS['posts_next']++;
    $GLOBALS['pages'][$pool]=(object)['ID'=>$pool,'post_name'=>'pool-teichtechnik','post_parent'=>0,
        'post_title'=>'Pool & Teichtechnik','post_status'=>'draft'];
    $GLOBALS['meta_p'][$pool]['_wt_owner_id']='wt_main_pool_w27';
"""
    replacement=snippet+"""    $ids['wt_main_pool_w27']=$pool;
    foreach($plan['wp_targets'] as $r)if($r['kind']==='page'&&($r['w44_new_draft']??false)){
        $newid=$GLOBALS['posts_next']++; $ids[$r['owner_id']]=$newid;
        $GLOBALS['pages'][$newid]=(object)['ID'=>$newid,'post_name'=>basename($r['path']),
            'post_parent'=>$ids[$r['parent_owner_id']], 'post_title'=>$r['title'],'post_status'=>'draft'];
        $GLOBALS['meta_p'][$newid]['_wt_owner_id']=$r['owner_id'];
    }
    foreach($plan['wp_targets'] as $r)if($r['kind']==='category'&&($r['w44_new_draft']??false)){
        $term=$GLOBALS['cats_next']++;
        $GLOBALS['terms'][$term]=(object)['term_id'=>$term,'slug'=>$r['slug'],'name'=>$r['title']];
        $GLOBALS['meta_c'][$term]['_wt_owner_id']=$r['owner_id'];
    }
"""
    test=repl(test,snippet,replacement,"W35 idempotent fixture")
    temp=PROJECT/"PRUEFUNG"/"W44_FULL_IMPORT_TEMP.php"
    try:
        temp.write_text(test)
        for scenario in ["blank","old9","idempotent","collision","rollback","update-rollback",
                         "stale","wrongsite","nonadmin","redirect"]:
            run(["php",str(temp),str(package),scenario],expected="PASS ")
            print("PASS W44 WP "+scenario)
    finally:temp.unlink(missing_ok=True)
    # Final original standalone SEO 81/218 / navigation mock stays intact.
    old=(PROJECT/"PRUEFUNG"/"W33_FULL_PLUGIN_MOCK_QA.php").read_text()
    old=old.replace("VERSION==='0.1.12'","VERSION==='0.1.14'")
    old=old.replace("str_contains($readme,'NICHT INSTALLIEREN') && str_contains($readme,'0.1.12')",
                    "!str_contains($readme,'NICHT INSTALLIEREN') && str_contains($readme,'0.1.14')")
    temp=PROJECT/"PRUEFUNG"/"W44_FULL_LEGACY_TEMP.php"
    try:
        temp.write_text(old)
        run(["php",str(temp),str(package)],expected="PASS W33 FULL OFFLINE REGRESSION")
    finally:temp.unlink(missing_ok=True)
    run(["php",str(PROJECT/"PRUEFUNG"/"W41_NAVIGATION_HISTORIE_GESAMT_QA.php"),str(package)],
         expected="PASS W41 NAVIGATION: 10/10")
    qa=PROJECT/"PRUEFUNG"/"W38_SEO81_PAID_ENDTOEND_QA.php"
    for case in ("success","provider","partial","duplicate","empty","network","budget","stale",
                 "locked","reportonly","nonadmin","wrongsite","noapproval","ui","ui-stale"):
        run(["php",str(qa),str(package),case],expected="PASS ")
    print("PASS W44 old 218 SEO + 15/15 DataForSEO provider cases + 10/10 import cases")
def main():
    run([sys.executable,str(SOURCE)],expected="W43 RELEASE PASS")
    must(OLDZIP.exists(),"W43 verified final ZIP missing")
    must(not WORK.exists(),"prevent stale W44 output")
    WORK.mkdir(parents=True)
    with zipfile.ZipFile(OLDZIP) as z:
        must(z.testzip() is None,"W43 ZIP CRC")
        z.extractall(WORK)
    pkg=WORK/FOLDER
    seo=json.loads(W44.read_text(encoding="utf8"))
    products=json.loads(W28.read_text(encoding="utf8"))["produkte"]
    old=json.loads(OLDPLAN.read_text(encoding="utf8"))
    must(seo["result_state"]=="COMPLETED" and seo["researched"]["keywords"]==81
         and seo["spent_usd"]<=0.25,"W44 verified paid research incomplete/over budget")
    plan,newids=prepare_targets(old,seo,products)
    newpath=pkg/"ASSETS"/"W44_wordpress_importplan_390.json"
    newpath.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    (pkg/"ASSETS"/"W44_SEO81_RECHERCHE_BEWERTUNG.json").write_text(
       json.dumps(seo,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    mainphp=pkg/"wassertechnik-kategorie-workflow.php"
    code=mainphp.read_text(encoding="utf8")
    code=repl(code,"Version: 0.1.13","Version: 0.1.14")
    code=repl(code,"public const VERSION = '0.1.13';","public const VERSION = '0.1.14';")
    mainphp.write_text(code,encoding="utf8")
    importer=pkg/"includes"/"class-wassertechnik-import.php"
    src=importer.read_text(encoding="utf8")
    for a,b in [
      ("ASSETS/W35_wordpress_importplan_219.json","ASSETS/W44_wordpress_importplan_390.json"),
      ("count($j['wp_targets'])!==219","count($j['wp_targets'])!==390"),
      ("count($pages)!==114||count($cats)!==105","count($pages)!==195||count($cats)!==195"),
      ("W35-Anzahl falsch: 114 Seiten, 105 Kategorien","W44-Anzahl falsch: 195 Seiten, 195 Kategorien"),
      ("Eine Gesamtentscheidung: 114 Seiten (davon eine leere Pool-Hub-Seite als Entwurf), 105 Beitragskategorien. Alle 218 bestehenden W6-Owner werden beibehalten. 81 neue Produkte werden NICHT angelegt.",
       "Eine Gesamtentscheidung: 195 Seiten (113 alte Seiten + 1 Pool-Einstieg + 81 NEUE PRODUKT-ENTWURFSEITEN), 195 Beitragskategorien (105 alte + 90 neue). Alle 218 ursprünglichen W6-Owner bleiben erhalten. Keine der 81 neuen Seiten wird automatisch veröffentlicht."),
      ("(219-count($state['missing_pages'])","(390-count($state['missing_pages'])"),
      ("'total'=>219","'total'=>390")]:
        src=repl(src,a,b,"W35 eine Importerquelle")
    importer.write_text(src,encoding="utf8")
    nav=pkg/"includes"/"class-wassertechnik-navigation.php"
    n=nav.read_text(encoding="utf8")
    for a,b in [
      ("ASSETS/W35_wordpress_importplan_219.json","ASSETS/W44_wordpress_importplan_390.json"),
      ("count($j['wp_targets'] ?? []) !== 219","count($j['wp_targets'] ?? []) !== 390"),
      ("return count($paths)===114?$paths:[];","return count($paths)===195?$paths:[];")]:
        n=repl(n,a,b,"Navigation weiterverwenden")
    marker="        $available=self::published_owner_links($plan,$paths);"
    dynamic="""        // W44: existing 79 links remain; 81 future draft pages join menu only AFTER an
        // administrator publishes a product. One WordPress owner list read, no extra writer.
        $wf=dirname(__DIR__).'/ASSETS/W44_wordpress_importplan_390.json';
        $w=is_readable($wf)?json_decode((string)file_get_contents($wf),true):[];
        if(is_array($w))foreach(($w['wp_targets']??[]) as $p){
            if(($p['kind']??'')!=='page'||!($p['w44_new_draft']??false))continue;
            $plan['existing_w4_pages'][]=[
                'owner_id'=>$p['owner_id'],'product_name'=>$p['title'],
                'wordpress_path'=>$p['path'],
                'bereich'=>(string)($p['w44_area']??''),'menu'=>true];
        }
"""
    n=repl(n,marker,dynamic+marker,"W44 dynamic draft-only menu")
    nav.write_text(n,encoding="utf8")
    # area is retained in each WordPress product plan, never chosen again in frontend
    for row in plan["wp_targets"]:
        if row.get("w44_new_draft") and row["kind"]=="page":
            must(row["source_product_id"] in {x["kanonisch_id"] for x in products},"area owner missing")
    for row in plan["wp_targets"]:
        if row.get("w44_new_draft") and row["kind"]=="page":
            row["w44_area"]=next(x["geplanter_hauptbereich"] for x in products
                                if x["kanonisch_id"]==row["source_product_id"])
    newpath.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    readme=pkg/"README.txt"
    readme.write_text(
        "WT001 0.1.14 – W44 gesamter Wassertechnik-Workflow – WORDPRESS-UPDATE\n"
        "Gleiche bestehende Pluginidentität und Dateien, kein Zusatzplugin.\n"
        "81/81 DataForSEO-Ergebnisse aus dem echten abgeschlossenen Kostenauftrag ausgewertet;\n"
        "Kosten 0,13344 USD, keine Wiederholung. 218 alte Keywords/SEO-Optionen bleiben intakt.\n"
        "W35 ist der EINZIGE Importer; er hat jetzt einen EINZIGEN, ownergesicherten 390er-Plan\n"
        "mit 219 unveränderten alten/Pool-Ownern plus 81 neuen PRODUKT-ENTWURFSEITEN\n"
        "und 90 neuen Produkt-Rubriken. Neue Seiten werden IMMER als ENTWURF erstellt,\n"
        "nicht automatisch veröffentlicht, und es entsteht keinerlei Blog-/Artikelinhalt.\n"
        "Nur nach Admin-Bestätigung des konkreten Gesamtbestandes wird importiert.\n"
        "17 bisherige Redirects werden nach Vorhandensein veröffentlichter Ziele erhalten.\n"
        "Zwei fachlich verschiedene Unterarten Systemtrenner/12-V-Wohnmobilpumpe bleiben\n"
        "mit eigenem langen Produktnamen unterscheidbar. Alte 218 Owner unberührt.\n"
        "Nach WordPress-Installation: Wassertechnik Kategorie -> W35 – Zielstruktur ->\n"
        "Vorschau auf 390 Ziele lesen, EINMAL Häkchen/Freigabe ausführen.\n"
        "Kein WP-/DataForSEO-Livezugriff durch Chat/GitHub. Vorher Backup erstellen.\n",
        encoding="utf8")
    # Not accidentally writing any previously approved 81 public URLs.
    must(len([p for p in plan["wp_targets"] if p.get("w44_new_draft") and p["kind"]=="page"])==81,
         "81 new pages missing")
    must(all(x["draft_on_new"] for x in plan["wp_targets"] if x.get("w44_new_draft") and x["kind"]=="page"),
         "new published page present")
    for p in pkg.rglob("*.php"):
        run(["php","-l",str(p)],expected="No syntax errors")
    write_final_tests(pkg)
    members=sorted(x for x in pkg.rglob("*") if x.is_file())
    with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for file in members:z.write(file,file.relative_to(WORK))
    with zipfile.ZipFile(OUT) as z:
        must(z.testzip() is None and len(z.namelist())==len(members),"ZIP invalid")
    digest=hashlib.sha256(OUT.read_bytes()).hexdigest()
    info={"status":"OFFLINE_BUILD_AND_FULL_QA_PASS","version":"0.1.14",
          "plugin_zip":OUT.name,"sha256":digest,"zip_files":len(members),
          "bytes":OUT.stat().st_size,"old_wp_targets":219,"new_product_drafts":81,
          "new_content_categories":90,"wp_targets_total":390,"redistribution_redirects":17,
          "old_keywords_preserved":218,"paid_keywords_new_completed":81,"paid_cost_usd":0.13344,
          "wp_live_writes":0,"dataforseo_live_calls_during_build":0}
    (WORK/"W44_ABNAHME_ZUSAMMENFASSUNG.json").write_text(
        json.dumps(info,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("W44 RELEASE PASS "+json.dumps(info,ensure_ascii=False))
if __name__=="__main__":main()
