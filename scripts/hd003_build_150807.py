#!/usr/bin/env python3
"""Build the full HD003 1.50.807 from the authentic 1.50.806 ZIP; preserve all non-target files."""
from pathlib import Path
from io import BytesIO
import hashlib, zipfile, re, json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT'
OLD = BASE / 'HOBBY_DEPOT_DESIGN_HD003_1.50.806.zip'
ART = BASE / 'ASSETS'
OUT = ROOT / 'dist/HOBBY_DEPOT_DESIGN_HD003_1.50.807_HOBBYFINDER.zip'
PROFILE = 'affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php'
ENTRY = 'affiliate-portal-template-kit/pferde-template-kit.php'
HERO = 'affiliate-portal-template-kit/assets/hobby-depot-v150617/hero-masters-v150807/hobbyfinder-lupe-approved.webp'
BANNER = 'affiliate-portal-template-kit/assets/hobby-depot-v150617/eigenwerbung-v150807/hobbyfinder-banner-flat.webp'
EXPECTED_ORIGINAL_SHA = '665a71d705ae80891ca43d56aca851c006608fcfcb61185381e3f96033635358'


def substitute_once(text, before, after, label):
    occurrences = text.count(before)
    assert occurrences == 1, f'{label}: original pattern occurrences={occurrences}'
    return text.replace(before, after, 1)


def patch_profile(data):
    s = data.decode('utf-8')
    # Change only the dedicated hobbyfinder magazine page. Other magazine pages retain their existing text/photos.
    s = substitute_once(s, "'asset' => 'hero-masters-v150684/suchen-finden.webp',", "'asset' => 'hero-masters-v150807/hobbyfinder-lupe-approved.webp',", 'hobbyfinder-only asset')
    s = substitute_once(s, "'claim' => 'Finde, was wirklich zu dir passt.',", "'claim' => 'Finde, was zu dir passt.',", 'claim')
    s = substitute_once(s, "'hero' => 'Acht kurze Fragen bringen dich von deinen Wünschen zu einer überschaubaren Auswahl.',", "'hero' => 'Das passende Hobby für dich.',", 'short subtitle')

    # Add a compact approved self-ad for hobbyfinder only; actual partner creative always wins.
    new_helper = '''    /** 1.50.807: Hobbyfinder-only compact, approved own-ad motif. No change to paid partner ads. */
    private static function hobbyfinder_flat_own_ad_v150807() {
        $terms = self::rental_terms_url_v150790();
        $prices = self::rental_prices_url_v150790();
        $action = static function($label, $url, $name) {
            $class = 'hd-hf-ad-action-v150807 ' . $name;
            if ($url !== '') {
                return '<a class="' . esc_attr($class) . '" href="' . esc_url($url) . '" aria-label="' . esc_attr($label) . '"><span>' . esc_html($label) . '</span></a>';
            }
            return '<span class="' . esc_attr($class . ' is-unavailable') . '" aria-label="' . esc_attr($label) . ': nicht verfügbar"><span>' . esc_html($label) . '</span></span>';
        };
        return '<div class="hd-hf-own-ad-v150807" aria-label="Freie Werbefläche Hobbyfinder">'
             . '<img src="' . esc_url(self::asset_url('eigenwerbung-v150807/hobbyfinder-banner-flat.webp')) . '" alt="Hobby Depot – Hier könnte Ihre Werbung stehen" width="1250" height="90" loading="lazy">'
             . '<strong class="hd-hf-ad-mobile-title-v150807">Hier könnte Ihre Werbung stehen</strong>'
             . $action('Werbebedingungen', $terms, 'is-terms')
             . $action('Preise', $prices, 'is-prices')
             . '</div>';
    }

'''
    s = substitute_once(s, '    private static function render_magazine_target_by_slug_v150722($slug, $page = null) {', new_helper + '    private static function render_magazine_target_by_slug_v150722($slug, $page = null) {', 'helper insertion')
    # Replace the one rental in magazine-target function, not any other site rental placement.
    before = "        $html .= self::render_rental_for('journal');\n        return $html . self::magazine_styles_v150719() . '</div>';"
    after = '''        $rental = self::render_rental_for('journal');
        // Only the unpaid, existing house banner on Hobbyfinder gets the compact design.
        // Booked / third-party ads and all other pages are returned byte-for-byte unchanged.
        if ($slug === 'hobbyfinder' && strpos($rental, 'hd-own-ad-v150791') !== false) {
            $rental = '<section class="hd-rental hd-hf-rental-v150807" aria-label="Werbeplatz">' . self::hobbyfinder_flat_own_ad_v150807() . '</section>';
        }
        $html .= $rental;
        return $html . self::magazine_styles_v150719() . '</div>';'''
    s = substitute_once(s, before, after, 'magazine target rental')

    # Keep CSS scoped inside existing magazine stylesheet. On small screens the ad becomes
    # native accessible text links instead of shrinking the baked-on labels to unreadable size.
    css = r'''
        /* HD003 1.50.807: ONLY /magazin/hobbyfinder/ (no site-wide advertising change). */
        .hd-mag-target-v150719[data-hd-magazine-target="hobbyfinder"] .hd-mag-hero-v150719 .hd-bp-hero-media img{object-position:63% center!important}
        .hd-mag-target-v150719[data-hd-magazine-target="hobbyfinder"] .hd-hf-rental-v150807{margin:20px 0 8px!important;padding:0!important;width:100%;max-width:100%}
        .hd-mag-target-v150719[data-hd-magazine-target="hobbyfinder"] .hd-hf-own-ad-v150807{position:relative;isolation:isolate;display:block;width:100%;height:auto;line-height:0;overflow:hidden;border-radius:9px;background:#f8f0e8;box-shadow:none}
        .hd-mag-target-v150719[data-hd-magazine-target="hobbyfinder"] .hd-hf-own-ad-v150807>img{width:100%!important;height:auto!important;display:block!important;aspect-ratio:1250/90!important;object-fit:contain!important;border:0!important;margin:0!important;padding:0!important}
        .hd-mag-target-v150719[data-hd-magazine-target="hobbyfinder"] .hd-hf-ad-mobile-title-v150807{display:none}
        .hd-mag-target-v150719[data-hd-magazine-target="hobbyfinder"] .hd-hf-ad-action-v150807{display:block;position:absolute;top:12%;height:77%;z-index:2;box-sizing:border-box;border:0!important;background:transparent!important;border-radius:6px;cursor:pointer;outline-offset:2px;text-decoration:none!important}
        .hd-mag-target-v150719[data-hd-magazine-target="hobbyfinder"] .hd-hf-ad-action-v150807.is-terms{left:76.0%;width:13.9%}
        .hd-mag-target-v150719[data-hd-magazine-target="hobbyfinder"] .hd-hf-ad-action-v150807.is-prices{left:90.9%;width:8.8%}
        .hd-mag-target-v150719[data-hd-magazine-target="hobbyfinder"] .hd-hf-ad-action-v150807 span{position:absolute;clip-path:inset(50%);width:1px;height:1px;overflow:hidden;white-space:nowrap}
        .hd-mag-target-v150719[data-hd-magazine-target="hobbyfinder"] .hd-hf-ad-action-v150807:focus-visible{outline:3px solid #199da0!important}
        .hd-mag-target-v150719[data-hd-magazine-target="hobbyfinder"] .hd-hf-ad-action-v150807.is-unavailable{cursor:not-allowed}
        @media(max-width:640px){
          .hd-mag-target-v150719[data-hd-magazine-target="hobbyfinder"] .hd-hf-own-ad-v150807{min-height:0;display:flex;align-items:center;justify-content:flex-start;gap:8px;flex-wrap:wrap;padding:12px!important;box-sizing:border-box;line-height:1.3}
          .hd-mag-target-v150719[data-hd-magazine-target="hobbyfinder"] .hd-hf-own-ad-v150807>img{display:none!important}
          .hd-mag-target-v150719[data-hd-magazine-target="hobbyfinder"] .hd-hf-ad-mobile-title-v150807{display:block;flex:1 0 100%;font-size:16px;line-height:1.2;color:#102f39;font-weight:750}
          .hd-mag-target-v150719[data-hd-magazine-target="hobbyfinder"] .hd-hf-ad-action-v150807{display:inline-flex;position:static;width:auto!important;left:auto!important;top:auto!important;max-width:100%;height:auto;min-height:39px;padding:9px 12px;align-items:center;justify-content:center;border-radius:6px;line-height:1.1}
          .hd-mag-target-v150719[data-hd-magazine-target="hobbyfinder"] .hd-hf-ad-action-v150807 span{position:static;clip-path:none;display:inline;color:inherit;width:auto;height:auto;white-space:normal;font-size:12px;font-weight:700}
          .hd-mag-target-v150719[data-hd-magazine-target="hobbyfinder"] .hd-hf-ad-action-v150807.is-terms{background:#279ca1!important;color:#fff!important}
          .hd-mag-target-v150719[data-hd-magazine-target="hobbyfinder"] .hd-hf-ad-action-v150807.is-prices{background:#fff!important;color:#102f39!important;border:1px solid #d3dce0!important}
        }
'''
    css = css.replace(r'\"', '"')
    s = substitute_once(s, "        return '<style id=\"hd-mag-style-v150722\">\n", "        return '<style id=\"hd-mag-style-v150722\">\n" + css, 'scoped style insertion')
    assert '2.8.14' not in s
    return s.encode('utf8')


def build():
    assert OLD.exists(), f'Base ZIP missing: {OLD}'
    assert hashlib.sha256(OLD.read_bytes()).hexdigest() == EXPECTED_ORIGINAL_SHA, 'wrong 1.50.806 base!'
    assert (ART / 'hobbyfinder-lupe-approved-v150807.webp').exists(), 'approved hero asset not committed'
    assert (ART / 'hobbyfinder-banner-flat-approved-v150807.webp').exists(), 'approved banner asset not committed'
    OUT.parent.mkdir(parents=True, exist_ok=True)
    changed, names = set(), set()
    with zipfile.ZipFile(OLD) as source, zipfile.ZipFile(OUT, 'w') as target:
        assert source.testzip() is None, 'base ZIP integrity fail'
        for member in source.infolist():
            assert member.filename not in names, f'duplicate {member.filename}'
            names.add(member.filename)
            data = source.read(member)
            if member.filename == PROFILE:
                data = patch_profile(data)
                changed.add(member.filename)
            elif member.filename == ENTRY:
                raw = data.decode('utf8')
                assert re.search(r'Version:\s*1\.50\.806\b', raw), 'plugin version header missing'
                data = re.sub(r'(Version:\s*)1\.50\.806\b', r'\g<1>1.50.807', raw).replace('1.50.806', '1.50.807').encode('utf8')
                changed.add(member.filename)
            target.writestr(member, data)
        for name,path in ((HERO, ART / 'hobbyfinder-lupe-approved-v150807.webp'), (BANNER, ART / 'hobbyfinder-banner-flat-approved-v150807.webp')):
            assert name not in names, 'approved asset path already occupied!'
            target.writestr(name, path.read_bytes(), compress_type=zipfile.ZIP_STORED)
    assert changed == {PROFILE,ENTRY}, changed
    with zipfile.ZipFile(OLD) as original, zipfile.ZipFile(OUT) as updated:
        assert updated.testzip() is None
        assert len(updated.namelist()) == len(original.namelist()) + 2
        assert set(updated.namelist()) - set(original.namelist()) == {HERO,BANNER}
        for name in original.namelist():
            if name not in changed:
                assert original.read(name) == updated.read(name), f'unintended original changed: {name}'
        assert updated.read(HERO) == (ART / 'hobbyfinder-lupe-approved-v150807.webp').read_bytes()
        assert updated.read(BANNER) == (ART / 'hobbyfinder-banner-flat-approved-v150807.webp').read_bytes()
        from PIL import Image
        for name in (HERO,BANNER):
            with Image.open(BytesIO(updated.read(name))) as image:
                image.verify()
        s=updated.read(PROFILE).decode('utf8')
        assert "'hero' => 'Das passende Hobby für dich.'" in s
        assert "'claim' => 'Finde, was zu dir passt.'" in s
        assert s.count('private static function hobbyfinder_flat_own_ad_v150807()') == 1
        assert "if ($slug === 'hobbyfinder' && strpos($rental, 'hd-own-ad-v150791') !== false)" in s
        assert 'max-width:640px' in s
        assert '<span>' in s and 'Werbebedingungen' in s and 'Preise' in s
        assert "'asset' => 'hero-masters-v150684/suchen-finden.webp'" not in s
    meta={'version':'1.50.807','base_sha256':EXPECTED_ORIGINAL_SHA,'zip_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'zip_size':OUT.stat().st_size,'zip_entries':len(updated.namelist()),'changed_files':sorted(changed),'added_assets':[HERO,BANNER]}
    (OUT.parent / 'HD003_150807_BUILD_REPORT.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(meta,indent=2,ensure_ascii=False))
    return OUT

if __name__=='__main__': build()