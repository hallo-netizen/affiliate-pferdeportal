#!/usr/bin/env python3
"""Rebuild HD-003 from the exact approved 1.50.794 ZIP, changing only footer links."""
import hashlib
import pathlib
import subprocess
import tempfile
import zipfile

BASE = pathlib.Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip")
DEST = pathlib.Path("dist/HOBBY_DEPOT_HD003_1.50.796_FOOTER_RECHTLICHES_SERVICE_FIX_VOLLPLUGIN.zip")
MAIN = "affiliate-portal-template-kit/pferde-template-kit.php"
PROFILE = "affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php"
EXPECTED_SHA = "52d7d67149ac09e22b7406ef59421ec7e4110c5d0efb11349e0f5357f8c4aa6f"

def replace_one(src, old, new, purpose):
    count = src.count(old)
    assert count == 1, f"{purpose} anchor expected once, found {count}"
    return src.replace(old, new, 1)

def change_profile(src):
    footer_fix = """
        // 1.50.796: AGB auch dann zeigen, wenn die WordPress-Seitenabfrage leer bleibt.
        // Der Pfad /agb/ ist aus dem vorhandenen Seitenexport bekannt.
        // Werbebedingungen gehoeren nur zu Service.
        $legal = array_values(array_filter($legal, static function($item) {
            $slug = sanitize_title((string)($item['label'] ?? ''));
            $path = parse_url((string)($item['url'] ?? ''), PHP_URL_PATH);
            $url_slug = sanitize_title((string)basename(trim((string)$path, '/')));
            return !in_array($slug, ['agb', 'werbebedingungen', 'werb-anzeigebedingungen'], true)
                && !in_array($url_slug, ['agb', 'werbebedingungen', 'werb-anzeigebedingungen'], true);
        }));
        $agb_url = self::page_link(['agb']);
        if ($agb_url === '') { $agb_url = home_url('/agb/'); }
        $agb_position = count($legal);
        foreach ($legal as $index => $item) {
            if (sanitize_title((string)($item['label'] ?? '')) === 'impressum') {
                $agb_position = $index + 1;
                break;
            }
        }
        array_splice($legal, $agb_position, 0, [['label' => 'AGB', 'url' => $agb_url]]);

"""
    legal_fallback = """        // Fail-safe nur fuer Rechtliches, falls der Import wirklich fehlt.
        if (!$legal) {
            foreach ([[['impressum'],'Impressum'],[['datenschutz'],'Datenschutz']] as $entry) {
                $url = self::page_link($entry[0]);
                if ($url !== '') { $legal[] = ['label'=>$entry[1], 'url'=>$url]; }
            }
        }
"""
    src = replace_one(src, legal_fallback, legal_fallback + footer_fix, "legal block")
    src = replace_one(src,
        "        $service = $compact([\n"
        "            $make_item('Werben im Hobby Depot', $ad_url),\n"
        "            $make_item('Preise', $prices_url),\n"
        "            $make_item('Kontakt', $contact_url),\n"
        "            $make_item('FAQ', $faq_url),\n"
        "        ]);",
        "        $terms_url = self::page_link(['werb-anzeigebedingungen', 'werbebedingungen']);\n"
        "        if ($terms_url === '') { $terms_url = home_url('/werb-anzeigebedingungen/'); }\n"
        "        $service = $compact([\n"
        "            $make_item('Werben im Hobby Depot', $ad_url),\n"
        "            $make_item('Werbebedingungen', $terms_url),\n"
        "            $make_item('Preise', $prices_url),\n"
        "            $make_item('Kontakt', $contact_url),\n"
        "            $make_item('FAQ', $faq_url),\n"
        "        ]);",
        "service fixed order")
    return src


def test_rendered_footer(real_profile, includes_agb):
    """Execute the actual plugin render_footer method with a fake WP menu."""
    import re
    marker = '    public static function render_footer() {'
    assert real_profile.count(marker) == 1
    start = real_profile.index(marker)
    end = real_profile.index('    public static function affiliate_page_type(', start)
    method = real_profile[start:end].strip()
    assert method.endswith('}')
    case = '1' if includes_agb else '0'
    harness = """<?php
error_reporting(E_ALL);
class FooterTest {
    public static $footer_rendered = false;
    private static function page_link($paths) {
      // Simulate failing AGB get_page_by_path: this was the original bug.
      $map = ['werbung'=>'/werbung/','preise'=>'/preise/','kontakt'=>'/kontakt/',
        'faq'=>'/faq/','journal'=>'/journal/','magazin'=>'/magazin/',
        'werb-anzeigebedingungen'=>'/werb-anzeigebedingungen/'];
      foreach ($paths as $key) if (isset($map[$key])) return $map[$key];
      return '';
    }
    private static function asset_url($name) { return '/assets/'.$name; }
    private static function footer_market_links_v150742() {
      return [['label'=>'Alle Anzeigen','url'=>'/anzeigenmarkt/']];
    }
""" + method + """
}
function is_admin(){return false;}
function home_url($v='/'){return 'https://www.hobby-depot.de'.$v;}
function wp_date($v){return '2026';}
function esc_attr($v){return htmlspecialchars($v,ENT_QUOTES);}
function esc_html($v){return htmlspecialchars($v,ENT_QUOTES);}
function esc_url($v){return htmlspecialchars($v,ENT_QUOTES);}
function sanitize_title($v){return strtolower(trim(preg_replace('/[^a-z0-9-]+/i','-',(string)$v),'-'));}
function wp_get_nav_menu_object($v){return (object)['term_id'=>($v==='rechtliches'||$v==='Rechtliches')?1421:1135];}
function wp_get_nav_menu_items($id) {
    if ($id==1135) $entries=[['Werben im Hobby Depot','/werbung/'],['Preise','/preise/'],
        ['Kontakt','/kontakt/'],['FAQ','/faq/']];
    else {
        $entries=[['Impressum','/impressum/'],['Datenschutz','/datenschutz/'],
            ['Werbebedingungen','/werb-anzeigebedingungen/']];
        if (__CASE__) array_splice($entries, 1, 0, [['AGB','/agb/']]);
    }
    return array_map(fn($e)=>(object)['title'=>$e[0], 'url'=>$e[1], 'menu_item_parent'=>0], $entries);
}
FooterTest::render_footer();
""".replace('__CASE__', case)
    with tempfile.TemporaryDirectory() as tmp:
        file = pathlib.Path(tmp) / "footer-test.php"
        file.write_text(harness, encoding="utf-8")
        test = subprocess.run(["php", str(file)], capture_output=True, text=True)
    assert test.returncode == 0, test.stderr
    html = test.stdout
    legal = re.search(r'<nav[^>]+aria-label="Rechtliches"[^>]*>(.*?)</nav>', html, re.S)
    service = re.search(r'<nav[^>]+aria-label="Service"[^>]*>(.*?)</nav>', html, re.S)
    assert legal and service, "Footer columns missing"
    assert html.count('>AGB</a>') == 1, "AGB missing or duplicate"
    assert 'href="https://www.hobby-depot.de/agb/">AGB</a>' in legal.group(1)
    assert html.count('>Werbebedingungen</a>') == 1, "Terms missing or duplicate"
    assert 'Werbebedingungen' not in legal.group(1), "Terms still in Rechtliches"
    assert 'AGB' not in service.group(1), "AGB wrongly in Service"
    labels = re.findall(r'<li><a [^>]+>([^<]+)</a></li>', service.group(1))
    assert labels == ['Werben im Hobby Depot','Werbebedingungen','Preise','Kontakt','FAQ'], labels
    assert html.count('<nav ') == 4, "Footer columns changed"
    print("PASS real render_footer: AGB menu entry present?", includes_agb, "service order", labels)

def main():
    source_sha = hashlib.sha256(BASE.read_bytes()).hexdigest()
    assert source_sha == EXPECTED_SHA, f"Unexpected source version: {source_sha}"
    with zipfile.ZipFile(BASE) as source:
        assert source.testzip() is None
        infos = source.infolist()
        assert len(infos) == 1290, len(infos)
        contents = {i.filename: source.read(i.filename) for i in infos}
    assert len(contents) == len(infos), "Duplicate archive paths"
    assert MAIN in contents and PROFILE in contents
    altered = contents.copy()
    for name in (MAIN, PROFILE):
        src = altered[name].decode("utf-8")
        if name == PROFILE:
            src = change_profile(src)
        assert "1.50.794" in src, f"Missing source version in {name}"
        altered[name] = src.replace("1.50.794", "1.50.796").encode("utf-8")
    changed = [name for name in contents if contents[name] != altered[name]]
    assert set(changed) == {MAIN, PROFILE}, changed
    DEST.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DEST, "w") as destination:
        for info in infos:
            destination.writestr(info, altered[info.filename])
    with zipfile.ZipFile(DEST) as check:
        assert check.testzip() is None
        assert check.namelist() == [i.filename for i in infos]
        assert all(check.read(k) == contents[k] for k in contents if k not in (MAIN, PROFILE))
        with tempfile.TemporaryDirectory() as tmp:
            for name in (MAIN, PROFILE):
                path = pathlib.Path(tmp) / pathlib.Path(name).name
                path.write_bytes(check.read(name))
                result = subprocess.run(["php", "-l", str(path)], capture_output=True, text=True)
                assert result.returncode == 0, result.stdout + result.stderr
    profile = altered[PROFILE].decode("utf-8")
    test_rendered_footer(profile, False)
    test_rendered_footer(profile, True)
    result_sha = hashlib.sha256(DEST.read_bytes()).hexdigest()
    print("PASS: input SHA+CRC / 1290 files / only two edited PHP files / PHP syntax / no changed other files")
    print("RELEASE_SHA256=", result_sha)
    print("RELEASE_SIZE=", DEST.stat().st_size)

if __name__ == "__main__":
    main()
