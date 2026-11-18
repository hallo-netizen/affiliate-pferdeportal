#!/usr/bin/env python3
"""W43: build ONE installable WT001 upgrade using the pre-tested W42 combined build.
No WordPress access, DataForSEO charges or WP content writes. All QA locally within Actions.
The earlier 0.1.7 original bytes were not retained; this is FUNCTIONAL W11 parity, not byte parity.
"""
from __future__ import annotations
from pathlib import Path
import hashlib, json, subprocess, sys, tempfile, zipfile, shutil

PROJ=Path(__file__).resolve().parents[2]
BUILD=PROJ/"PLUGINS"/"BUILD"/"W33_build.py"
STAGE=PROJ/"PRUEFUNG"/"_w43_release"
ORIGINAL=PROJ/"PRUEFUNG"/"_w33_offline_build"/"WASSERTECHNIK_WT001_0.1.12_W41_GESAMTPRUEFUNG_NICHT_INSTALLIEREN.zip"
OUT=STAGE/"WASSERTECHNIK_KATEGORIE_WORKFLOW_0.1.13_W43_GESAMTUPDATE_INSTALLIEREN.zip"
ROOT="wassertechnik-kategorie-workflow"
VERSION="0.1.13"
def ensure(condition,why):
    if not condition: raise RuntimeError("W43 ABNAHME FEHLER: "+why)
def run(args, expected=None, timeout=120):
    r=subprocess.run(args,capture_output=True,text=True,timeout=timeout)
    if r.returncode or (expected is not None and expected not in r.stdout):
        raise RuntimeError("W43 Gesamtprüfung fehlerhaft: "+" ".join(map(str,args))+"\n"+r.stderr[-3500:]+"\n"+r.stdout[-3500:])
    print("PASS",args[-1] if len(args)>1 else args[0])
    return r.stdout
def update_once(path,before,after):
    src=path.read_text(encoding="utf-8")
    ensure(src.count(before)==1,"Textänderung nicht eindeutig: "+path.name+" :: "+before[:70])
    path.write_text(src.replace(before,after,1),encoding="utf-8")
def main():
    # Complete earlier tests first: original 0.1.4, 218 SEO owners, DataForSEO 81,
    # W35 219 import / 17 redirects, W42 79 navigation owners, rollback and safeguards.
    run([sys.executable,str(BUILD)],expected='"full_mock": "PASS"',timeout=220)
    ensure(ORIGINAL.is_file(),"geprüfter W42 Gesamtbau fehlt")
    STAGE.mkdir(parents=True,exist_ok=True)
    tmp=STAGE/"source"
    if tmp.exists(): shutil.rmtree(tmp)
    tmp.mkdir()
    with zipfile.ZipFile(ORIGINAL) as z:
        ensure(z.testzip() is None,"Basis ZIP CRC")
        ensure(all(n.startswith(ROOT+"/") and ".." not in Path(n).parts for n in z.namelist()),"Basis Plugin-Pfade")
        z.extractall(tmp)
    package=tmp/ROOT
    main_php=package/"wassertechnik-kategorie-workflow.php"
    trait=package/"includes"/"class-wassertechnik-seo81-paid-trait.php"
    readme=package/"README.txt"
    update_once(main_php,"Version: 0.1.12","Version: "+VERSION)
    update_once(main_php,"public const VERSION = '0.1.12';","public const VERSION = '"+VERSION+"';")
    update_once(trait,"'plugin_version'=>'0.1.10'","'plugin_version'=>Wassertechnik_Kategorie_Workflow::VERSION")
    update_once(main_php,'Die Keywordliste findest du unter „Wassertechnik Kategorie → DataForSEO“.',
        '<strong>Nächster Schritt:</strong> Unter „81 neue SEO-Kandidaten“ den einmaligen DataForSEO-Auftrag nach Kostenfreigabe starten. Die bisherigen 218 Begriffe nicht wiederholen. Erst danach über die neuen Produkte entscheiden. Die 219 bisherigen WordPress-Ziele bleiben separat geschützt.')
    readme.write_text(
        "Wassertechnik Kategorie-Workflow WT001 "+VERSION+" – ein einziges Installationsupdate\n"
        "Pluginverzeichnis: wassertechnik-kategorie-workflow; selbe WordPress-Pluginidentität wie 0.1.7.\n"
        "Fachmaster W27: sieben kaufnahe Hauptbereiche plus getrennter Fachtechnik-Zugang.\n"
        "218 bestehende W4/W5 SEO-Owner und gespeicherte Ergebnisse bleiben unverändert.\n"
        "81 neue W28-Kaufkandidaten im vorhandenen DataForSEO-SEO-Motor; ein gesonderter\n"
        "nur nach ausdrücklicher Kostenfreigabe ausgelöster Sammelauftrag (maximal 0,25 USD).\n"
        "Das Plugin führt beim Installieren KEINE kostenpflichtige Abfrage durch.\n"
        "W35 ist der EINZIGE aktive WordPress-Schreiber; 219 historische Ziele (114 Seiten\n"
        "einschließlich Pool-Entwurf + 105 Kategorien), 17 Besitzer-geprüfte 301-Weiterleitungen.\n"
        "Import ausschließlich nach einmaliger ausdrücklicher Admin-Freigabe mit Readback/Rollback.\n"
        "Die 81 neuen Produkte sind ausdrücklich NICHT zum WP-Seitenimport freigegeben.\n"
        "W42 Menü: eine WordPress-Seitenlesung, 79 bestehende Produktowner, keine Dubletten.\n"
        "Offline-Kompatibilität anhand W11-Dokumentation und vollständiger QA bestätigt.\n"
        "Die ursprünglichen vollständigen Quellbytes von 0.1.7 waren im Archiv nicht vorhanden;\n"
        "keine Behauptung eines bytegleichen Vergleichs oder eines WordPress-Live-Tests.\n"
        "Vor WordPress-Update ein aktuelles reguläres Site-Backup sicherstellen.\n",
        encoding="utf-8")
    # Full original QA reproduced against the *final version*. The test's
    # version/README assertions are adapted only for release labelling.
    qa=PROJ/"PRUEFUNG"/"W33_FULL_PLUGIN_MOCK_QA.php"
    source=qa.read_text(encoding="utf-8")
    old="str_contains($readme,'NICHT INSTALLIEREN') && str_contains($readme,'0.1.12')"
    ensure(source.count(old)==1,"Original-README-Test unerwartet")
    source=source.replace(old,"!str_contains($readme,'NICHT INSTALLIEREN') && str_contains($readme,'0.1.13')")
    old="Wassertechnik_Kategorie_Workflow::VERSION==='0.1.12'"
    ensure(source.count(old)==1,"Originalversions-Test unerwartet")
    source=source.replace(old,"Wassertechnik_Kategorie_Workflow::VERSION==='0.1.13'")
    test=PROJ/"PRUEFUNG"/"W43_RELEASE_MOCK_TEMP.php"
    try:
        test.write_text(source,encoding="utf-8")
        for php in package.rglob("*.php"):
            run(["php","-l",str(php)],expected="No syntax errors")
        run(["php",str(test),str(package)],expected="PASS W33 FULL OFFLINE REGRESSION")
        run(["php",str(PROJ/"PRUEFUNG"/"W41_NAVIGATION_HISTORIE_GESAMT_QA.php"),str(package)],
            expected="PASS W41 NAVIGATION: 10/10")
        w35=PROJ/"PRUEFUNG"/"W35_WP_IMPORT_ENDTOEND_QA.php"
        for case in ("blank","old9","idempotent","collision","rollback",
                     "update-rollback","stale","wrongsite","nonadmin","redirect"):
            run(["php",str(w35),str(package),case],expected="PASS ",timeout=30)
        paidqa=PROJ/"PRUEFUNG"/"W38_SEO81_PAID_ENDTOEND_QA.php"
        for case in ("success","provider","partial","duplicate","empty","network",
                     "budget","stale","locked","reportonly","nonadmin","wrongsite",
                     "noapproval","ui","ui-stale"):
            run(["php",str(paidqa),str(package),case],expected="PASS W38",timeout=30)
    finally:
        test.unlink(missing_ok=True)
    # Scope: no programmatic deletion of old WP data, credentials, plugin options
    # and no automatic paid API action. Only one active WordPress writer is W35.
    content=main_php.read_text(encoding="utf-8")
    ensure(content.count("Wassertechnik_Kategorie_Importer::boot();")==1,"Doppel-Importer")
    ensure("Wassertechnik_W34_Inventory_Readback::boot();" not in content,"Alte zweite Inventur aktiv")
    ensure(content.count("Wassertechnik_PaidResearch::boot();")==1,"Doppel-SEO-Motor")
    ensure("Version: "+VERSION in content and "VERSION = '"+VERSION+"'" in content,"Version inkonsistent")
    ensure("paid81" in (package/"includes"/"class-wassertechnik-seo81-paid-trait.php").read_text(),"81 SEO fehlt")
    ensure("Wassertechnik_W32_Navigation::boot();" in content,"Navigation nicht aktiviert")
    ensure(not any("NICHT INSTALLIEREN" in f.read_text(encoding="utf-8")
                   for f in [main_php,readme]),"Sperrtext in Installationspaket")
    ensure((package/"ASSETS"/"W35_wordpress_importplan_219.json").is_file(),"Importplan fehlt")
    ensure((package/"assets"/"wassertechnik-w28-seo-handoff.json").is_file(),"81er Handoff fehlt")
    members=sorted(p for p in package.rglob("*") if p.is_file())
    with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in members: z.write(p,p.relative_to(tmp))
    with zipfile.ZipFile(OUT) as z:
        ensure(z.testzip() is None,"Ausgabe ZIP CRC")
        ensure(len(z.namelist())==len(members),"ZIP-Dateien fehlen")
        ensure(all(n.startswith(ROOT+"/") for n in z.namelist()),"ZIP-Pluginordner falsch")
    digest=hashlib.sha256(OUT.read_bytes()).hexdigest()
    report={"status":"INSTALLATIONS_ZIP_OFFLINE_GESAMT_QA_PASS",
      "name":OUT.name,"sha256":digest,"size_bytes":OUT.stat().st_size,
      "member_count":len(members),"plugin_version":VERSION,"installable_plugin_folder":ROOT,
      "old_218_seo_preserved":True,"new_81_dataforseo_ready_needs_explicit_approval":True,
      "old_0_1_7_source_bytes_available":False,"documented_w11_functional_compatibility":True,
      "wp_live_install_executed":False,"dataforseo_live_paid_executed":False,
      "wp_import_executed":False,"old_wp_reports_not_deleted":True,
      "tests":["W33 original overall regression","W41/W42 menu and owner checks",
               "W35 10 scenarios","W38/W39 15 API/SEO scenarios","PHP lint","ZIP CRC"]}
    (STAGE/"W43_RELEASE_ABNAHME.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("W43 RELEASE PASS "+json.dumps(report,ensure_ascii=False))
if __name__=="__main__": main()
