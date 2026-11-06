#!/usr/bin/env python3
"""Build a *separate* Hab & Bewahr Affiliate candidate from all 26 neutral files.

NO write to the source neutral stem, Pferdeatelier, Hobbydepot, or WordPress.
All original functions remain present; only project bindings change.
"""
from __future__ import annotations
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile, ZIP_DEFLATED
import re, shutil, json, sys

HERE = Path(__file__).resolve().parent
OFFICE = HERE.parent
SOURCE = OFFICE / "NEUTRAL_STAMM" / "affiliate-portal-router"
BRIDGE = HERE / "includes" / "class-ppar-hab-bewahr-bridge.php"
WORK = HERE / "_build"
TARGET = WORK / "affiliate-portal-router"
OUT = HERE / "HAB_UND_BEWAHR_AFFILIATE_0.1.0_RC1.zip"

if not SOURCE.is_dir() or not BRIDGE.is_file():
    raise RuntimeError("Missing original neutral source / bridge")
if WORK.exists():
    shutil.rmtree(WORK)
TARGET.parent.mkdir(parents=True, exist_ok=True)
shutil.copytree(SOURCE,TARGET)
(TARGET/"includes"/BRIDGE.name).write_bytes(BRIDGE.read_bytes())

main_path = TARGET/"affiliate-portal-router.php"
original = (SOURCE/"affiliate-portal-router.php").read_text(encoding="utf-8")
body = original

def exactly(old,new):
    global body
    count = body.count(old)
    if count != 1:
        raise RuntimeError(f"Expected exactly one matching source string, got {count}: {old[:85]!r}")
    body = body.replace(old,new)

exactly("Plugin Name: Portalneutraler Affiliate-Stamm", "Plugin Name: Hab & Bewahr – Affiliate-Zentrale")
exactly("Description: Portalneutraler Affiliate-Stamm ohne gebundene Portal-Zielquelle. Entwicklungsbasis, nicht für Livebetrieb freigegeben.",
        "Description: Zentrale Affiliate-Verwaltung für Hab & Bewahr mit unabhängiger Zielquelle und bestehenden Provider-Funktionen.")
exactly("Version: 0.1.0-dev", "Version: 0.1.0-rc1")
exactly("Author: OpenAI", "Author: Hab & Bewahr")
exactly("Text Domain: affiliate-portal-router", "Text Domain: hab-bewahr-affiliate")
exactly("require_once __DIR__ . '/includes/class-ppar-portal-source.php';",
        "require_once __DIR__ . '/includes/class-ppar-portal-source.php';\n"
        "require_once __DIR__ . '/includes/class-ppar-hab-bewahr-bridge.php';")
# The old equestrian-design hooks serve a different theme. Keep their
# implementation methods byte-for-byte, but never register foreign hooks.
for hook in (
    "pftk_hub_grid_affiliate_data",
    "pftk_leaf_category_affiliate_slot_html",
    "pftk_leaf_page_affiliate_slot_html",
    "pftk_market_affiliate_slot_html",
):
    lines = body.splitlines(keepends=True)
    matched=[i for i,l in enumerate(lines) if "add_filter('"+hook+"'" in l]
    if len(matched)!=1: raise RuntimeError("Legacy theme hook changed: "+hook)
    lines[matched[0]] = "        // Hab & Bewahr uses its own hbdp_* design bridge; foreign theme hook disabled.\n"
    body="".join(lines)

exactly("    public function filter_the_content($content) {\n",
"""    public function filter_the_content($content) {
        // Hab & Bewahr's article template exclusively owns visible ad positions.
        // All article planning/rendering features remain active through the
        // hbdp_article_* adapters. Never insert the same HTML a second time.
        if (function_exists('hbdp_article_slot_html')
            && function_exists('is_singular') && is_singular('post')) {
            return $content;
        }
""")
exactly("    public function register_shortcodes() {\n",
"""    /** Safe public bridge to EXISTING article plans; never create fake offers. */
    public function hab_bw_article_slot($post_id, $kind) {
        $post_id=absint($post_id);
        if ($post_id < 1 || !$this->is_enabled() || !$this->article_hybrid_enabled()) { return ''; }
        if (get_post_type($post_id)!=='post' || get_post_status($post_id)!=='publish') { return ''; }
        $plan=$this->article_plan_get($post_id);
        if (!is_array($plan) || !$this->article_plan_is_current($post_id,$plan)) { return ''; }
        if ($kind==='products' && ($plan['products']['status'] ?? '')==='ready') {
            return $this->article_plan_render_products($post_id,(array)($plan['products']['campaign_post_ids'] ?? array()));
        }
        if ($kind==='banner' && in_array(($plan['banner']['status'] ?? ''),array('ready','pending_anchor'),true)) {
            return $this->article_plan_render_banner_campaign($post_id,absint($plan['banner']['campaign_post_id'] ?? 0));
        }
        return '';
    }

    /** Read existing campaign-selection engine, with real page context. */
    public function hab_bw_area_slot($page_id, $kind) {
        $page_id=absint($page_id);
        if ($page_id < 1 || !$this->is_enabled() || get_post_type($page_id)!=='page'
            || get_post_status($page_id)!=='publish') { return ''; }
        $context=$this->get_content_context($page_id);
        if ($kind==='banner') {
            return $this->render_affiliate_slot_for_context($page_id,$context,'product_after_category_tiles','portal_context','');
        }
        if ($kind==='products') {
            $html='';
            for ($i=1; $i<=3; $i++) {
                $part=$this->render_affiliate_slot_for_context($page_id,$context,'category_product_'.$i,'primary_product','');
                if (trim($part)!=='') { $html.=$part; }
            }
            return $html;
        }
        return '';
    }

    public function register_shortcodes() {
""")
# Use the project's actual glossary CPT if present, never a horse glossary.
body=body.replace("is_singular('uge_term')", "is_singular('hbdp_glossar_term')")
body=body.replace("get_post_type($post_id) !== 'uge_term'", "get_post_type($post_id) !== 'hbdp_glossar_term'")
exactly("Portal_Affiliate_Router::instance();", "PPAR_HB_Integration::bootstrap();\nPortal_Affiliate_Router::instance();")
assert body.count("Werbelink: Bei Kauf erhalten wir ggf. eine Provision.") == 3
body=body.replace("Werbelink: Bei Kauf erhalten wir ggf. eine Provision.", "Anzeige")

# Do not transplant old equestrian examples as product business policies.
for old,new in (
  ("Reithandschuhe Damen Leder","Fenstersicherung aus Metall"),
  ("Reithose, Reitjacke, Reitschuh, Reitweste","Fensterschloss, Fenstergriff, Türschloss, Riegel"),
  ("Reitstiefel","Türschloss"),
  ("Heunetze fuer\n", "Kameras fuer\n"),
):
    body=body.replace(old,new)

main_path.write_text(body,encoding="utf-8")
readme=TARGET/"readme.txt"
readme.write_text("""=== Hab & Bewahr – Affiliate-Zentrale ===
Requires at least: 6.0
Requires PHP: 7.4
Stable tag: 0.1.0-rc1

Complete independent installable candidate built from the 26-file neutral
affiliate source, preserving every existing source function. Adds local
WordPress category + Hab & Bewahr design adapters; does not copy data,
tokens, images, schedules or settings from other installations.

Activation: OFF by default. The product catalog requires a current
revision-bound category-workflow snapshot and at least three published
specific product pages. No fallback to the bundled historical category
tree. Provider connections must be configured again on the Hab & Bewahr
WordPress site. No live integration or 6.72.306 parity claim.
""",encoding="utf-8")

old_paths=sorted(p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob("*") if p.is_file())
new_paths=sorted(p.relative_to(TARGET).as_posix() for p in TARGET.rglob("*") if p.is_file())
assert len(old_paths)==26, (len(old_paths),old_paths)
assert len(new_paths)==27, len(new_paths)
assert set(old_paths).issubset(new_paths)

# Strong functional no-regression check: all original function method names
# remain defined, including unused legacy methods.
rx=re.compile(r"\b(?:public|private|protected)?\s*(?:static\s+)?function\s+([a-zA-Z_]\w*)\s*\(")
lost=[]
counts={}
for rel in old_paths:
    a=(SOURCE/rel).read_text(encoding="utf-8",errors="replace")
    z=(TARGET/rel).read_text(encoding="utf-8",errors="replace")
    fa=set(rx.findall(a))
    fz=set(rx.findall(z))
    lost += [(rel,f) for f in sorted(fa-fz)]
    counts[rel]={"source_functions":len(fa),"output_functions":len(fz),"byte_identical":a==z}
assert not lost, ("Functions removed",lost)

# The code must not reference or ship project-farm URLs, third-party portal
# sources, or foreign stored product data.
for p in TARGET.rglob("*"):
    if not p.is_file(): continue
    t=p.read_text(encoding="utf-8",errors="replace").lower()
    assert not re.search(r"pferde.?atelier|pferde-atelier\.de|hobby.?depot|hobbyrausch|hd-004|pftk_",t),p
    assert not re.search(r"api[_-]?key\s*=\s*['\"][^'\"]{20,}",t),p

with ZipFile(OUT,"w",ZIP_DEFLATED,compresslevel=9) as z:
    for path in sorted(p for p in TARGET.rglob("*") if p.is_file()):
        z.write(path,Path("affiliate-portal-router")/path.relative_to(TARGET))
with ZipFile(OUT) as z:
    assert len(z.infolist())==27 and z.testzip() is None
    assert b"Plugin Name: Hab & Bewahr" in z.read("affiliate-portal-router/affiliate-portal-router.php")
manifest={
  "version":"0.1.0-rc1",
  "source":"26 neutral original files from EIGENTUMSSCHUTZ/AFFILIATE/NEUTRAL_STAMM",
  "source_files":len(old_paths),"output_files":len(new_paths),
  "functions_removed":lost,
  "file_checks":counts,
  "sha256":sha256(OUT.read_bytes()).hexdigest(),
  "size_bytes":OUT.stat().st_size,
  "release_status":"INSTALLABLE_CANDIDATE__WP_LIVE_NOT_TESTED__NO_6_72_306_PARITY_CLAIM"
}
(HERE/"build_report.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding="utf-8")
print("AFFILIATE_HB_BUILD_PASS files=27 existing_functions_preserved sha256="+manifest["sha256"]+" bytes="+str(manifest["size_bytes"]))
