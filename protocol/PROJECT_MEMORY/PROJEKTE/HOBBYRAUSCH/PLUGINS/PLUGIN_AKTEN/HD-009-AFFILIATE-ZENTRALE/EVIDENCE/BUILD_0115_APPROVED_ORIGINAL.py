#!/usr/bin/env python3
"""Reproducible minimal HD009 update: import EXACT existing approved HD003 banner; no new architecture."""
import hashlib
import pathlib
import shutil
import subprocess
import tempfile
import zipfile

ROOT=pathlib.Path(__file__).resolve().parents[5]
ROOT=pathlib.Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH")
HD009=ROOT/"PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip"
HD003=ROOT/"PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip"
APPROVED_PATH="affiliate-portal-template-kit/assets/hobby-depot-v150617/eigenwerbung-v150791/banner-freigabe-originalbild-2170x725.png"
APPROVED_SHA="3cc834d9f67305ce752574b794d834b4b20304ada93eb1518bbae6fd2eb8e579"
BANNER_PATH="affiliate-portal-router/assets/hdar-approved-own-ad-original-2170x725.png"
MAIN="affiliate-portal-router/hobby-depot-affiliate-router.php"
README="affiliate-portal-router/readme.txt"
FALLBACK=r'''    /**
     * Only on otherwise empty wide slots, after the existing creative selection.
     * Uses the exact original HD003 artwork incl. the original logo and buttons.
     * No table, provider, booking, or separate banner system.
     */
    private function hdar_approved_rental_banner_fallback($slot_type) {
        if (!HDAR_Amazon_Start::launch_active() || !$this->overview_wide_banner_slot($slot_type)) { return ''; }
        static $shown = false;
        if ($shown) { return ''; }
        $filename = 'hdar-approved-own-ad-original-2170x725.png';
        $file = plugin_dir_path(__FILE__) . 'assets/' . $filename;
        $original_hash = '3cc834d9f67305ce752574b794d834b4b20304ada93eb1518bbae6fd2eb8e579';
        if (!is_file($file) || hash_file('sha256', $file) !== $original_hash) { return ''; }
        $resolve = static function($paths) {
            if (!function_exists('get_page_by_path') || !function_exists('get_permalink')) { return ''; }
            foreach ((array) $paths as $slug) {
                $page = get_page_by_path($slug, OBJECT, 'page');
                if (is_object($page) && (string) ($page->post_status ?? '') === 'publish') {
                    $url = get_permalink($page);
                    if (is_string($url) && $url !== '') { return $url; }
                }
            }
            return '';
        };
        $conditions = $resolve(array('werbebedingungen','werb-anzeigebedingungen'));
        $prices = $resolve(array('preise'));
        $image_url = plugins_url('assets/' . $filename, __FILE__);
        $html = '<div class="ppar-affiliate-slot ppar-hdar-approved-own-ad" data-ppar-slot="' . esc_attr($slot_type) . '" data-hdar-own-ad="approved-hd003" style="position:relative;width:100%;max-width:100%;margin:0 auto;line-height:0">'
            . '<img src="' . esc_url($image_url) . '" width="2170" height="725" loading="lazy" decoding="async" alt="Hobby Depot – Hier könnte Ihre Werbung stehen" style="display:block;width:100%;height:auto;object-fit:contain;border:0">';
        if ($conditions !== '') {
            $html .= '<a href="' . esc_url($conditions) . '" aria-label="Werbebedingungen" style="position:absolute;left:4.25%;top:69.5%;width:22.65%;height:15%;display:block;z-index:1"></a>';
        }
        if ($prices !== '') {
            $html .= '<a href="' . esc_url($prices) . '" aria-label="Preise" style="position:absolute;left:28.85%;top:69.5%;width:13.2%;height:15%;display:block;z-index:1"></a>';
        }
        $shown = true;
        return $html . '</div>';
    }

'''
with zipfile.ZipFile(HD009) as z:
    entries={i.filename:z.read(i.filename) for i in z.infolist() if not i.is_dir()}
assert MAIN in entries and README in entries
p=entries[MAIN].decode("utf-8")
assert "Version: 0.1.14-dev" in p
p=p.replace("Version: 0.1.14-dev","Version: 0.1.15-dev",1)
old="""            if ($launch && $selection && !$this->hdar_launch_public_campaign_allowed($selection['campaign'] ?? null)) {
                return ''; // Never reveal unrelated providers even via fixed overrides.
            }"""
new="""            if ($launch && $selection && !$this->hdar_launch_public_campaign_allowed($selection['campaign'] ?? null)) {
                // Selected campaign belongs to an inactive partner; NEVER display it.
                return $this->hdar_approved_rental_banner_fallback($slot_type);
            }"""
assert p.count(old)==1
p=p.replace(old,new,1)
old="""        if ($this->overview_wide_banner_slot($slot_type) || preg_match('/^category_product_[123]$/', sanitize_key((string)$slot_type))) {
            return $this->debug_comment('affiliate_no_real_creative', $content_id, $slot_type, '', '');
        }"""
new="""        if ($this->overview_wide_banner_slot($slot_type)) {
            // Existing real-banner selection already ran; fill only an empty wide spot.
            $approved_own_ad = $this->hdar_approved_rental_banner_fallback($slot_type);
            if ($approved_own_ad !== '') { return $approved_own_ad; }
        }
        if ($this->overview_wide_banner_slot($slot_type) || preg_match('/^category_product_[123]$/', sanitize_key((string)$slot_type))) {
            return $this->debug_comment('affiliate_no_real_creative', $content_id, $slot_type, '', '');
        }"""
assert p.count(old)==1
p=p.replace(old,new,1)
marker="    private function render_placeholder_slot($slot_type) {"
assert p.count(marker)==1
p=p.replace(marker,FALLBACK+marker,1)
entries[MAIN]=p.encode("utf-8")
readme=entries[README].decode("utf-8")
assert "Stable tag: 0.1.14-dev" in readme
readme=readme.replace("Stable tag: 0.1.14-dev","Stable tag: 0.1.15-dev",1)
readme+="\n== 0.1.15-dev ==\nPixelidentische freigegebene HD003-Eigenwerbegrafik als einmaliger Fallback auf leerer Querbannerflaeche. Original-Logo und beide Button-Hotspots erhalten. Keine eigene Datenhaltung, kein manueller Import, kein Ersatz fuer zahlende Anzeigen oder existierende automatische Kampagnen. Das nicht abgenommene Quadratmotiv wird nicht ersatzweise erzeugt.\n"
entries[README]=readme.encode("utf-8")
with zipfile.ZipFile(HD003) as z:
    exact=[x for x in z.namelist() if x.endswith("eigenwerbung-v150791/banner-freigabe-originalbild-2170x725.png")]
    assert len(exact)==1
    orig=z.read(exact[0])
assert hashlib.sha256(orig).hexdigest()==APPROVED_SHA
entries[BANNER_PATH]=orig
with tempfile.TemporaryDirectory() as tmp:
    d=pathlib.Path(tmp)
    count=0
    for path,b in entries.items():
        if path.endswith(".php"):
            fn=d/path
            fn.parent.mkdir(parents=True,exist_ok=True)
            fn.write_bytes(b)
            check=subprocess.run(["php","-l",str(fn)],capture_output=True,text=True)
            assert check.returncode==0, check.stdout+check.stderr
            count+=1
    assert count==24
    o=d/"CURRENT.zip"
    with zipfile.ZipFile(o,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
        for name in sorted(entries):
            z.writestr(name,entries[name])
    with zipfile.ZipFile(o) as z:
        assert z.testzip() is None
        assert len([x for x in z.namelist() if x.endswith(".png") and "approved-own-ad" in x])==1
        assert z.read(BANNER_PATH)==orig
        assert len(z.namelist())==31
    shutil.copy2(o,HD009)
print("HD009 0.1.15-dev:",HD009.stat().st_size,"bytes SHA256",hashlib.sha256(HD009.read_bytes()).hexdigest(),"PHP 24 PASS; ZIP 31 entries PASS; original logo banner pixel-identical PASS")
