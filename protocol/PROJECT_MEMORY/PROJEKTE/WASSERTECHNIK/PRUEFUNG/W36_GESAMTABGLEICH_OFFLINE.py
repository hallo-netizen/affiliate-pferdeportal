#!/usr/bin/env python3
"""W36: one offline read-only audit of binding target, WP owners, SEO source, candidate handoff.
No network requests, no WP writes, no chargeable API. Does not create an installable plugin.
"""
from __future__ import annotations
import hashlib
import json
import re
import zipfile
from pathlib import Path

P = Path(__file__).resolve().parents[1]
R = P / "PRUEFUNG"
K = P / "KATEGORIEKONZEPT"
L = P / "PLUGINS"
def req(ok: bool, explanation: str):
    if not ok:
        raise AssertionError(explanation)
    print("PASS", explanation)

def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))

def audit():
    contract = (P / "ZIELVERTRAG.md").read_text(encoding="utf-8")
    for phrase in ("Die letzte *Seitenebene* ist produktbezogen", "3–5", "WordPress-Core unverändert",
                   "SEO findet erst im WordPress-Kategorie-Plugin statt", "einmalige ADD-only-Änderung"):
        req(phrase in contract, "Zielvertrag: " + phrase)
    w6 = load(K / "W6_WORDPRESS_IMPORTVORSCHAU_218_20261114.json")
    w28 = load(R / "W28_SEO_EINMALHANDOFF_81_20261116.json")
    w35 = load(L / "ASSETS" / "W35_wordpress_importplan_219.json")
    w32 = load(L / "ASSETS" / "W32_wassertechnik-navigation.json")
    seo = load(R / "ORIGINAL_DATAFORSEO_218_20261114.json")
    old = w6["proposed_owner_targets"]
    targets = w35["wp_targets"]
    products = w28["produkte"]
    old_ids = {x["owner_id"] for x in old}
    new_ids = {x["owner_id"] for x in targets}
    req(len(old) == len(old_ids) == 218, "exactly 218 original distinct WP/SEO owner targets")
    req(len(targets) == len(new_ids) == 219 and old_ids.issubset(new_ids), "219 WP targets preserving all 218 originals")
    req(len(new_ids-old_ids) == 1 and next(iter(new_ids-old_ids)) == "wt_main_pool_w27",
        "the only new WP owner is the Pool/Teich hub, not a product")
    pages = [x for x in targets if x["kind"] == "page"]
    categories = [x for x in targets if x["kind"] == "category"]
    req(len(pages) == 114 and len(categories) == 105, "114 pages/105 category targets")
    paths = {p["owner_id"]: p["path"] for p in pages}
    req(len(set(paths.values())) == 114, "unique WP page paths")
    req(all(p["parent_owner_id"] is None or p["parent_owner_id"] in paths for p in pages),
        "all pages have a real parent owner, no menu-only fake WP pages")
    req(all(c["product_owner_id"] in paths for c in categories), "all category targets belong to an existing product page")
    roots = {x["path"] for x in pages if x["parent_owner_id"] is None}
    req(roots == set(w35["consumer_roots"] + w35["info_roots"]) and len(w35["consumer_roots"]) == 7,
        "exactly 7 consumer roots + 1 industry information entry")
    req(len(w35["redirects"]) == 17 and len({x["from"] for x in w35["redirects"]}) == 17,
        "exactly 17 distinct legacy URL moves")
    req(len(w32["existing_w4_pages"]) == 79 and w32["wp_buy_menu_count"] == 71 and w32["wp_industry_count"] == 8,
        "W27 navigation 79 old product owners = 71 consumer + 8 industry")
    req(w32["wp_owner_count"] == 79 and len(w32["hauptbereiche"]) == 7,
        "navigation uses 7 approved existing WP product groups")
    req(len(products) == w28["anzahl"] == 81 and len({x["register_id"] for x in products}) == 81,
        "81 independent new canonical candidates")
    req(sum(len(p["artikelkategorien"]) for p in products) == 90
        and all(len(c["article_ideas"]) >= 3 and len(set(c["article_ideas"])) == len(c["article_ideas"]) for p in products for c in p["artikelkategorien"]),
        "90 real product-specific category ideas, min. 3 distinct article angles")
    req(all(p["seo_status"] == "ungeprueft" and p["seo_owner_freigabe"] is False
                and p["wp_seitenfreigabe"] is False and p["quellen"] for p in products),
        "81 source-backed products remain unapproved for SEO and WP import")
    req(seo["source_fingerprint"] == "9570a11250f6d3684f52af69239a9af2090a292ba1646dafde76380c471b3462"
        and seo["keywords_requested"] == 218, "original 218-SEO plan/fingerprint unchanged")
    req(seo["state"] == "COMPLETE_WITH_GAPS", "old SEO provider report has explicit missing data")
    source = L / "WASSERTECHNIK_KATEGORIE_WORKFLOW_0.1.4_FORTSETZUNG_OHNE_NEUSTART_NUR_TEST.zip"
    req(hashlib.sha256(source.read_bytes()).hexdigest()
        == "73b50022aecde2e3d7fd805acfeb94c7c588489abe85383da0905a5fd5736fd4",
        "original WP/DataForSEO plugin 0.1.4 byte-exact")
    discovered = {}
    with zipfile.ZipFile(source) as z:
        req(z.testzip() is None and len(z.namelist()) == 6, "original WordPress plugin ZIP intact")
        for name in z.namelist():
            if not name.endswith(".php"):
                continue
            src = z.read(name).decode("utf-8")
            funcs = re.findall(r"\bfunction\s+([A-Za-z0-9_]+)\s*\(", src)
            classes = re.findall(r"\bclass\s+([A-Za-z0-9_]+)", src)
            discovered[name.rsplit("/",1)[-1]] = {"classes": classes, "methods": funcs}
    req(any("Wassertechnik_PaidResearch" in v["classes"] for v in discovered.values()),
        "real paid SEO provider class exists in original plugin")
    req(any("Wassertechnik_DataForSEO" in v["classes"] for v in discovered.values()),
        "real DataForSEO preflight class exists in original plugin")
    preview = (L/"QUELLCODE"/"W39_class-wassertechnik-seo81-preview.php").read_text(encoding="utf-8")
    shared_paid = (L/"QUELLCODE"/"W39_seo81_paid_trait.php").read_text(encoding="utf-8")
    req("Wassertechnik_W30_Seo_Handoff::read" in preview
        and "Wassertechnik_PaidResearch::panel81()" in preview and "Wassertechnik_PaidResearch::read81()" in preview
        and "admin_post_wassertechnik_dfs_w38_81_paid" in preview,
        "81 original W28 candidates have one explicit WT001 paid-action intake")
    req("self::planned()" in shared_paid and "self::fetch(" in shared_paid
        and "self::apply(" in shared_paid and "self::W38_LOCK" in shared_paid
        and "self::W38_REPORT" in shared_paid and "unique_matched_rows" in shared_paid,
        "new 81 paid job reuses original 218 engine; separate locks and results")
    # Never call a paid endpoint or write to WordPress during this audit.
    report = {"status":"PASS_W39_81_SEO_DATA_INTEGRITY_OFFLINE_LIVE_WP_UNKNOWN",
        "legacy_wp_owners":218,"wp_targets":219,"wp_pages":114,"wp_categories":105,
        "consumer_roots":7,"industry_information_roots":1,"legacy_redirects":17,
        "existing_product_owners":79,"existing_buy_links":71,"existing_industry_owners":8,
        "new_products_unapproved":81,"candidate_content_categories":90,
        "seo_provider_original_version":"0.1.4","seo_old_keywords":218,
        "live_wp_admin_parity":"NICHT_GEPRUEFT","plugin_0_1_7_parity":"NICHT_GEPRUEFT",
        "provider_intake_for_81":"W39_KORREKTE_MESSERGEBNISSE_OHNE_SEITENFREIGABE",
        "original_plugin_functions":discovered,
        "wordpress_writes":0,"paid_api_requests":0,"installation_release":False}
    out = R / "_w36_gesamtpruefung_offline.json"
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("W36 ORIGINAL PHP FUNCTIONS",json.dumps(discovered,ensure_ascii=False))
    print("W36 RESULT",json.dumps({k:v for k,v in report.items() if k!="original_plugin_functions"},ensure_ascii=False))

if __name__=="__main__":
    audit()
