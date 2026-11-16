#!/usr/bin/env python3
"""W33 reproducible offline build from the original retained WT001 0.1.4.
No live WordPress, no paid research, no WordPress importer activation.
NEVER install this artifact until existing 0.1.7 runtime parity is established.
"""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
PLUGINS = PROJECT / "PLUGINS"
SOURCE = PLUGINS / "WASSERTECHNIK_KATEGORIE_WORKFLOW_0.1.4_FORTSETZUNG_OHNE_NEUSTART_NUR_TEST.zip"
ORIGINAL_SHA = "73b50022aecde2e3d7fd805acfeb94c7c588489abe85383da0905a5fd5736fd4"
W6 = PROJECT / "KATEGORIEKONZEPT" / "W6_WORDPRESS_IMPORTVORSCHAU_218_20261114.json"
W28 = PROJECT / "PRUEFUNG" / "W28_SEO_EINMALHANDOFF_81_20261116.json"
W32 = PLUGINS / "ASSETS" / "W32_wassertechnik-navigation.json"
BUILD_DIR = Path(os.environ.get("W33_BUILD_DIR", str(PROJECT / "PRUEFUNG" / "_w33_offline_build")))
OUT = BUILD_DIR / "WASSERTECHNIK_WT001_0.1.8_W33_GESAMTPRUEFUNG_NICHT_INSTALLIEREN.zip"
ROOT = "wassertechnik-kategorie-workflow"

def require(test: bool, msg: str) -> None:
    if not test:
        raise RuntimeError(msg)

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    require(SOURCE.is_file(), "Original WT001 0.1.4 archiv fehlt")
    original = SOURCE.read_bytes()
    require(sha(original) == ORIGINAL_SHA, "ORIGINAL SHA MISMATCH - not the preserved 0.1.4")
    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    BUILD_DIR.mkdir(parents=True)
    with zipfile.ZipFile(SOURCE) as zipped:
        require(len(zipped.namelist()) == 6, "Original membership count changed")
        require(zipped.testzip() is None, "Original ZIP CRC failed")
        require(all(name.startswith(ROOT+"/") and ".." not in Path(name).parts for name in zipped.namelist()),
                "Unsafe ZIP original paths")
        zipped.extractall(BUILD_DIR)
    pkg = BUILD_DIR / ROOT
    (pkg/"includes").mkdir(exist_ok=True)
    (pkg/"assets").mkdir(exist_ok=True)
    (pkg/"ASSETS").mkdir(exist_ok=True)
    original_classes = sorted((pkg/"includes").glob("*.php"))
    original_checksums = {x.name: sha(x.read_bytes()) for x in original_classes}
    require(len(original_classes) == 3, "Original 0.1.4 has unexpected number of PHP classes")

    additions = {
        "class-wassertechnik-import.php": "W9_class-wassertechnik-import.php",
        "class-wassertechnik-seo-handoff.php": "W30_seo_handoff_readonly.php",
        "class-wassertechnik-seo81-preview.php": "W31_class-wassertechnik-seo81-preview.php",
        "class-wassertechnik-navigation.php": "W32_class-wassertechnik-navigation.php",
    }
    for dest, src in additions.items():
        file = PLUGINS/"QUELLCODE"/src
        require(file.is_file(), "Missing vetted module "+str(file))
        shutil.copyfile(file, pkg/"includes"/dest)
    shutil.copyfile(W28, pkg/"assets"/"wassertechnik-w28-seo-handoff.json")
    shutil.copyfile(W32, pkg/"ASSETS"/"W32_wassertechnik-navigation.json")

    w6=json.loads(W6.read_text(encoding="utf-8"))
    rows=w6["proposed_owner_targets"]
    require(len(rows)==218, "W6 not 218")
    require(len({p["owner_id"] for p in rows})==218, "W6 duplicate owner")
    oldpages={p["proposed_page_path"] for p in rows if p["wp_object"]=="page"}
    manifest=[]
    for p in rows:
        ispage=p["wp_object"]=="page"
        if ispage:
            manifest.append({
                "kind":"page","owner_id":p["owner_id"],
                "title":p["title"],"path":p["proposed_page_path"],
                "parent_path":p["parent_page_path"] or ""
            })
        else:
            product_path=p["parent_page_path"]
            require(product_path in oldpages, "W6 category without actual product path "+p["owner_id"])
            manifest.append({
                "kind":"category","owner_id":p["owner_id"],"title":p["title"],
                "slug":p["proposed_category_slug"],"product_path":product_path
            })
    require(sum(1 for x in manifest if x["kind"]=="page")==113, "W6 pages")
    require(sum(1 for x in manifest if x["kind"]=="category")==105, "W6 categories")
    (pkg/"assets"/"wassertechnik-wp-import-plan.json").write_text(
        json.dumps({"schema":"wassertechnik-w6-import-v1","entries":manifest},
                   ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")

    main_php = pkg/"wassertechnik-kategorie-workflow.php"
    content = main_php.read_text(encoding="utf-8")
    expected="require_once __DIR__ . '/includes/class-wassertechnik-paid-research.php';"
    require(content.count(expected)==1, "WP bootstrap version not original")
    content = content.replace(expected, expected+"\n"+
        "require_once __DIR__ . '/includes/class-wassertechnik-import.php';\n"+
        "require_once __DIR__ . '/includes/class-wassertechnik-seo-handoff.php';\n"+
        "require_once __DIR__ . '/includes/class-wassertechnik-seo81-preview.php';\n"+
        "require_once __DIR__ . '/includes/class-wassertechnik-navigation.php';")
    original_boot="        Wassertechnik_PaidResearch::boot();"
    require(content.count(original_boot)==1, "Original boot changed")
    content=content.replace(original_boot, original_boot+"\n"+
        "        Wassertechnik_Seo81_Preview::boot();\n"+
        "        Wassertechnik_W32_Navigation::boot();\n"+
        "        // Import remains NOT booted: W6 has 9 old roots, W27 mandates a different 7-group target.\n"+
        "        // Do not activate W9 before a separately approved new 7-root manifest and WP readback.")
    require(content.count("Version: 0.1.4")==1 and content.count("VERSION = '0.1.4'")==1,
            "Original version expected")
    content=content.replace("Aktueller Fachplan W4:</strong> 8 Hauptbereiche, 19 Zwischenbereiche, 1 Industrieeinstieg, 6 Industrie-Landingvorschlaege, 79 Produktseiten, 105 Inhaltskategorien und 356 grobe Artikelideen. Kostenloser SEO-Pruefplan: 218 Begriffe.", "Fachplan W27:</strong> sieben kaufnahe Hauptbereiche (einschliesslich Pool und Teich), 71 vorhandene Kauf-Produktseiten, acht Industrie-Produktseiten und 81 neue noch SEO-ungepruefte Produkttypen. Der bisherige W4-SEO-Plan mit 218 Begriffen bleibt erhalten.")
    require("Aktueller Fachplan W4:" not in content, "Old contradictory eight-item homepage retained")
    (pkg/"README.txt").write_text("WT001 0.1.8 - W33 REKONSTRUKTION / NICHT INSTALLIEREN\n"
        "Zusammengefuehrter schreibfreier Probeaufbau. 218 alte SEO Owner unveraendert, "
        "81 weitere SEO Kandidaten nur Vorschau, W27 Navigation sieben Hauptbereiche.\n"
        "W6 Altimporter mit 9 alten WordPress Hauptseiten bleibt bewusst NICHT aktiv. "
        "Keine neue SEO-/WordPress-Freigabe, keine kostenpflichtigen Abfragen.\n"
        "Original 0.1.7 fehlt; keine Live- oder verlustfreie Updateabnahme vorhanden.\n", encoding="utf-8")
    content=content.replace("Version: 0.1.4", "Version: 0.1.8")
    content=content.replace("VERSION = '0.1.4'", "VERSION = '0.1.8'")
    content=content.replace("Kein Import oder Veroeffentlichen.", "Nur Vorschau, Import und Veroeffentlichung gesperrt.")
    # Keep original SEO logic literally unmodified, including 218 owner lock, budget and persisted report keys.
    main_php.write_text(content,encoding="utf-8")
    for file in original_classes:
        require(sha(file.read_bytes())==original_checksums[file.name], "Original class changed "+file.name)

    # Ensure candidate preview and final navigation have no forbidden WordPress mutators.
    for name in ("class-wassertechnik-seo-handoff.php","class-wassertechnik-seo81-preview.php","class-wassertechnik-navigation.php"):
        src=(pkg/"includes"/name).read_text(encoding="utf-8")
        require(not any(x in src for x in ("wp_insert_post","wp_insert_term","wp_update_post","wp_update_term","wp_remote_post","update_option(")),
                "Unexpected writer in read-only module "+name)
    # The old W9 importer source exists inside the ZIP but is intentionally never hooked.
    require("Wassertechnik_Kategorie_Importer::boot();" not in content,
            "Old 9-root importer must never be activated")

    h=json.loads(W28.read_text(encoding="utf-8"))
    require(len(h["produkte"])==81 and h["anzahl"]==81
            and all(p["seo_owner_freigabe"] is False and p["wp_seitenfreigabe"] is False for p in h["produkte"]),
            "Unsafe W28 SEO approvals")
    n=json.loads(W32.read_text(encoding="utf-8"))
    require(len(n["existing_w4_pages"])==79 and len(n["hauptbereiche"])==7
            and n["wp_buy_menu_count"]==71 and n["wp_industry_count"]==8
            and sum(g["new_not_approved"] for g in n["hauptbereiche"])==81,
            "W32 7 groups / 79 owners mismatch")

    for php in sorted(pkg.rglob("*.php")):
        res=subprocess.run(["php","-l",str(php)],capture_output=True,text=True)
        require(res.returncode==0,"PHP lint failure: "+str(php)+": "+res.stdout+res.stderr)
    test=PROJECT/"PRUEFUNG"/"W33_FULL_PLUGIN_MOCK_QA.php"
    require(test.is_file(),"Missing full regression test")
    res=subprocess.run(["php",str(test),str(pkg)],capture_output=True,text=True)
    print(res.stdout, end="")
    require(res.returncode==0,"QA FAILURE: "+res.stderr+" "+res.stdout)
    members=sorted(p for p in pkg.rglob("*") if p.is_file())
    with zipfile.ZipFile(OUT,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zipped:
        for f in members:
            zipped.write(f, f.relative_to(BUILD_DIR))
    with zipfile.ZipFile(OUT) as zipped:
        require(zipped.testzip() is None and len(zipped.namelist())==len(members),"Built ZIP CRC or file count fail")
    print(json.dumps({"status":"OFFLINE_QA_PASS_NOT_INSTALLABLE","zip":str(OUT),
                      "sha256":sha(OUT.read_bytes()),"zip_files":len(members),
                      "old_w4_seo_owners":218,"old_w4_products":79,"new_seo_pending":81,
                      "seven_menu_areas":7,"legacy_w6_importer_exposed":False,
                      "wordpress_live_test":False,"php_lint":"PASS","full_mock":"PASS"},
                     ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
