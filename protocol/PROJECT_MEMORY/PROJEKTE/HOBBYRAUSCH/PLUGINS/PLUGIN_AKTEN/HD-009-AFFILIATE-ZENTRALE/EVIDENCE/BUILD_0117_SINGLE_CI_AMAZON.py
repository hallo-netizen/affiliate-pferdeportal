#!/usr/bin/env python3
"""Single tested, additive HD009 release. Native rankings are retained; only missing Amazon-house creative and HD007 profile mount."""
from pathlib import Path
import hashlib, re, tempfile, subprocess, zipfile
ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH")
HOBBY=ROOT/"PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip"
DESIGN=ROOT/"PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip"
MAIN="affiliate-portal-router/hobby-depot-affiliate-router.php"
README="affiliate-portal-router/readme.txt"
CSS="affiliate-portal-router/assets/hdar-amazon-start.css"
assets={
"affiliate-portal-router/assets/hdar-ci-logo-original.png":"affiliate-portal-template-kit/assets/hobby-depot-v150617/eigenwerbung-v150790/logo-original-ohne-unterzeile.png",
"affiliate-portal-router/assets/hdar-ci-malen-zeichnen.webp":"affiliate-portal-template-kit/assets/hobby-depot-v150617/hero-masters-v150684/malen-zeichnen.webp",
"affiliate-portal-router/assets/hdar-ci-modellbau.webp":"affiliate-portal-template-kit/assets/hobby-depot-v150617/hero-masters-v150684/modellbau.webp",
}
PHP=r"""
    /**
     * Hobby Depot CI banner: uses existing affiliate slot and native ranking first.
     * Only one matching Amazon search creative on an otherwise genuinely empty slot.
     * No additional campaign table, remote request or separate ranking mechanism.
     */
    private function hdar_ci_amazon_banner($context, $slot_type, $content_id, $register_row = null) {
        if (!HDAR_Amazon_Start::launch_active() || !$this->is_enabled()) { return ''; }
        $slot = sanitize_key((string)$slot_type);
        $square = in_array($slot, array('glossary_single_banner','glossary_single_desktop_banner'), true);
        $wide = $this->overview_wide_banner_slot($slot) ||
            in_array($slot, array('glossary_single_mobile_banner','post_inline_banner','hub_mid_banner','template_mid_banner'), true);
        if (!$square && !$wide) { return ''; }
        if (!is_array($context)) { return ''; }
        $topic = trim(sanitize_text_field((string)($context['primary_name'] ?? '')));
        if (is_array($register_row)) { $topic = trim(sanitize_text_field((string)($register_row['name'] ?? ''))); }
        if ($topic === '' || in_array(mb_strtolower($topic), array('hobbyregister','glossar','hobby depot','hobbys'), true)) { return ''; }
        $amazon = $this->amazon_settings();
        $tag = trim((string)($amazon['tracking_id'] ?? ''));
        if (empty($amazon['enabled']) || !preg_match('/^[A-Za-z0-9-]+-21$/D',$tag)) { return ''; }
        $slug = sanitize_title($topic);
        $post_id = absint($context['post_id'] ?? 0);
        $photo = '';
        if (is_array($register_row) && class_exists('HD_Hobbyregister_Core_Stable127') &&
            method_exists('HD_Hobbyregister_Core_Stable127','image_entry')) {
            $entry = HD_Hobbyregister_Core_Stable127::image_entry((string)($register_row['registry_id'] ?? ''));
            if (is_array($entry)) {
                foreach (array('url','image_url','src') as $key) {
                    if (!empty($entry[$key]) && is_string($entry[$key])) { $photo=esc_url_raw($entry[$key]); break; }
                }
            }
        }
        if ($photo === '' && $post_id > 0 && function_exists('get_the_post_thumbnail_url')) {
            $photo = (string)get_the_post_thumbnail_url($post_id,'large');
        }
        if ($photo === '') {
            $known = array(
                'malen-zeichnen'=>'hdar-ci-malen-zeichnen.webp',
                'modellbau'=>'hdar-ci-modellbau.webp',
            );
            $filename = $known[$slug] ?? '';
            if ($filename !== '' && is_file(plugin_dir_path(__FILE__).'assets/'.$filename)) {
                $photo = plugins_url('assets/'.$filename,__FILE__);
            }
        }
        if ($photo === '') { return ''; } // No matching photograph = no invented banner.
        $scheme = strtolower((string)wp_parse_url($photo,PHP_URL_SCHEME));
        if (!in_array($scheme,array('http','https'),true)) { return ''; }
        $logo_file = plugin_dir_path(__FILE__).'assets/hdar-ci-logo-original.png';
        if (!is_file($logo_file)) { return ''; }
        static $shown = array();
        $key = $square ? 'square' : 'wide';
        if (!empty($shown[$key])) { return ''; }
        $url = 'https://www.amazon.de/s?k='.rawurlencode($topic.' Hobby Zubehör').'&tag='.rawurlencode($tag);
        $size = $square ? 'square' : 'wide';
        $html='<div class="ppar-affiliate-slot hdar-ci-amazon-slot hdar-ci-amazon-slot-'.$size.'" data-ppar-slot="'.esc_attr($slot).'">'
            .'<span class="hdar-ci-label">Anzeige</span>'
            .'<a class="hdar-ci-amazon-banner hdar-ci-amazon-banner-'.$size.'" href="'.esc_url($url).'" rel="sponsored nofollow noopener noreferrer" target="_blank" aria-label="'.esc_attr('Ausrüstung für '.$topic.' bei Amazon entdecken').'">'
            .'<span class="hdar-ci-content">'
            .'<img class="hdar-ci-logo" src="'.esc_url(plugins_url('assets/hdar-ci-logo-original.png',__FILE__)).'" alt="Hobby Depot" loading="lazy">'
            .'<span class="hdar-ci-subline">Entdecke deine Ausrüstung</span>'
            .'<strong class="hdar-ci-title">'.esc_html($topic).'</strong>'
            .'<span class="hdar-ci-button">Bei Amazon entdecken</span>'
            .'</span><span class="hdar-ci-photo"><img src="'.esc_url($photo).'" alt="'.esc_attr($topic).'" loading="lazy" decoding="async"></span>'
            .'</a></div>';
        $shown[$key] = true;
        return $html;
    }

    /** HD007 owns the register markup directly, not WordPress the_content.
     * This is the missing mount only, reusing render_affiliate_slot_for_context. */
    public function hdar_ci_register_footer() {
        if (!HDAR_Amazon_Start::launch_active() || is_admin() ||
            !function_exists('hd_hobbyregister_ready') || !hd_hobbyregister_ready() ||
            !function_exists('hd_hobbyregister_records')) { return; }
        $path=(string)wp_parse_url((string)($_SERVER['REQUEST_URI'] ?? ''),PHP_URL_PATH);
        if (!preg_match('~^/hobbyregister/([a-z0-9-]+)/?$~i',$path,$found)) { return; }
        $slug=sanitize_key($found[1]); $row=null;
        foreach ((array)hd_hobbyregister_records() as $item) {
            if (!is_array($item)) { continue; }
            if (sanitize_title((string)($item['name'] ?? '')) === $slug) { $row=$item; break; }
        }
        if (!$row) { return; }
        $name=(string)$row['name'];
        $context=array(
            'post_id'=>0,'post_type'=>'hobbyregister_profile',
            'primary_slug'=>$slug,'primary_name'=>$name,
            'slugs'=>array($slug),'names'=>array($name),
            'haystack'=>strtolower($name.' '.$slug),
        );
        // Existing engine renders a relevant authorised provider creative first.
        $html=$this->render_affiliate_slot_for_context('hobbyregister_'.$slug,$context,'glossary_single_desktop_banner','portal_context','');
        if (trim($html)==='') { $html=$this->hdar_ci_amazon_banner($context,'glossary_single_desktop_banner','hobbyregister_'.$slug,$row); }
        if (trim($html)==='') { return; }
        $id='hdar-ci-register-'.$slug;
        echo '<div id="'.esc_attr($id).'" hidden>'. $html .'</div>';
        echo '<script>(function(){function f(){var b=document.getElementById('.wp_json_encode($id).'),t=document.querySelector("[data-hd-register-profile] .hdr-profile-grid aside");if(!b||!t)return; b.hidden=false; t.appendChild(b);}if(document.readyState==="loading"){document.addEventListener("DOMContentLoaded",f,{once:true});}else{f();}})();</script>';
    }

"""
STYLE=r"""
/* Hobby Depot: existing house CI, native content picture and exact logo.
   CSS presentation only; no duplicate banner selection or product feed. */
.hdar-ci-amazon-slot{display:block!important;box-sizing:border-box!important;width:100%!important;max-width:none!important;height:auto!important;min-height:0!important;overflow:visible!important;padding:0!important;margin:10px 0 18px!important;background:transparent!important;border:0!important;box-shadow:none!important}
.hdar-ci-label{display:block;font-size:10px;line-height:1.35;letter-spacing:.05em;color:#6d777a;margin:0 0 5px}
.hdar-ci-amazon-banner{display:flex!important;position:relative;box-sizing:border-box!important;overflow:hidden!important;background:#f6f1e9!important;color:#20343b!important;text-decoration:none!important;width:100%!important;border:1px solid #e4dcd0!important;border-radius:9px!important;box-shadow:none!important}
.hdar-ci-content{box-sizing:border-box;display:flex;flex-direction:column;align-items:flex-start;justify-content:center;gap:6px;min-width:0;width:61%;padding:14px 20px 14px 22px}
.hdar-ci-logo{display:block;object-fit:contain;object-position:left center;max-width:160px!important;width:42%!important;height:auto!important;max-height:68px!important;flex:0 0 auto}
.hdar-ci-subline{font-family:Montserrat,Arial,sans-serif;font-size:11px;line-height:1.25;letter-spacing:.045em;opacity:.8}
.hdar-ci-title{display:block;font-family:Montserrat,Arial,sans-serif;color:#18313a;font-size:clamp(17px,2.2vw,27px);line-height:1.15;overflow-wrap:anywhere}
.hdar-ci-button{display:inline-flex;align-items:center;justify-content:center;max-width:100%;min-height:34px;padding:7px 13px;border-radius:5px;background:#258f95;color:white!important;font-family:Montserrat,Arial,sans-serif;font-weight:700;font-size:12px;line-height:1.1;text-align:center}
.hdar-ci-amazon-banner:hover .hdar-ci-button,.hdar-ci-amazon-banner:focus-visible .hdar-ci-button{background:#b77f1a}
.hdar-ci-photo{display:block;width:39%;min-width:0;overflow:hidden;position:relative}
.hdar-ci-photo>img{display:block!important;position:absolute;inset:0;object-fit:cover!important;object-position:center!important;width:100%!important;height:100%!important;max-width:none!important;border:0!important}
.hdar-ci-amazon-banner-wide{aspect-ratio:6 / 1;min-height:138px}
.hdar-ci-amazon-banner-square{aspect-ratio:1 / 1;flex-direction:column!important;max-width:700px}
.hdar-ci-amazon-banner-square .hdar-ci-content{width:100%;min-height:48%;padding:15px 18px;gap:5px}
.hdar-ci-amazon-banner-square .hdar-ci-photo{width:100%;flex:1 1 50%;min-height:45%}
.hdar-ci-amazon-banner-square .hdar-ci-title{font-size:clamp(19px,2.6vw,25px)}
.hdar-ci-amazon-banner-square .hdar-ci-logo{width:40%!important;max-width:150px!important}
.hdar-ci-amazon-slot .ppar-affiliate-label,.hdar-ci-amazon-slot .ppar-affiliate-disclosure{display:none!important}
.pa356-partner:has(.hdar-ci-amazon-slot),.pa255-network:has(.hdar-ci-amazon-slot),.pa266-network:has(.hdar-ci-amazon-slot),.ppar-overview-banner-v67266:has(.hdar-ci-amazon-slot){height:auto!important;max-height:none!important;overflow:visible!important;min-height:0!important}
body .ppar-affiliate-slot.hdar-ci-amazon-slot img.hdar-ci-logo{width:auto!important;max-width:150px!important;height:auto!important;object-fit:contain!important}
@media(max-width:640px){.hdar-ci-amazon-banner-wide{aspect-ratio:auto;min-height:180px}.hdar-ci-amazon-banner-wide .hdar-ci-content{width:67%;padding:12px;gap:4px}.hdar-ci-amazon-banner-wide .hdar-ci-photo{width:33%}.hdar-ci-amazon-banner-wide .hdar-ci-title{font-size:clamp(15px,4.3vw,21px)}.hdar-ci-button{font-size:10px;padding:7px}.hdar-ci-logo{max-width:105px!important}.hdar-ci-amazon-banner-square{aspect-ratio:1 / 1}.hdar-ci-amazon-banner-square .hdar-ci-content{min-height:53%;padding:11px}}
"""
with zipfile.ZipFile(HOBBY) as z:
    assert z.testzip() is None
    entries={i.filename:z.read(i.filename) for i in z.infolist() if not i.is_dir()}
assert MAIN in entries and README in entries and CSS in entries
s=entries[MAIN].decode("utf-8")
assert s.count("Version: 0.1.16-dev")==1
assert "hdar_approved_rental_banner_fallback" not in s
assert "overview_wide_banner_campaign_eligible" in s and "'ratio_min'=>5.00,'ratio_max'=>12.00" in s
assert "glossary_single_desktop_banner" in s and "glossary_single_mobile_banner" in s
assert "HDAR_Amazon_Start::render_slot" in s
assert s.count("    private function render_placeholder_slot($slot_type) {")==1
s=s.replace("Version: 0.1.16-dev","Version: 0.1.17-dev",1)
s=s.replace("    private function render_placeholder_slot($slot_type) {",PHP+"    private function render_placeholder_slot($slot_type) {",1)
old="""        // V2.4.0: Die fest definierten Banner-/Produktplätze der Produkt- und
"""
assert old in s
s=s.replace(old, """        // KISS: EXISTING provider/creative ranking ran above. Add only one
        // themed Amazon house-creative on a truly unoccupied native banner slot.
        if ($launch) {
            $house = $this->hdar_ci_amazon_banner($context, $slot_type, $content_id);
            if ($house !== '') { return $house; }
        }
""" + old,1)
hook="        add_filter('the_content', array($this, 'inject_glossary_single_banner'), 40);"
assert s.count(hook)==1
s=s.replace(hook,hook+"\n        add_action('wp_footer', array($this, 'hdar_ci_register_footer'), 55);",1)
entries[MAIN]=s.encode("utf-8")
readme=entries[README].decode("utf-8")
assert readme.count("Stable tag: 0.1.16-dev")==1
entries[README]=(readme.replace("Stable tag: 0.1.16-dev","Stable tag: 0.1.17-dev",1)+
  "\n== 0.1.17-dev ==\nEine korrigierte, bestehende Affiliate-Ausgabe: Eigene Amazon-Suchbanner mit Hobby-Depot-Original-Logo und passendem Hobbyfoto auf wirklich freien Quer-, Glossar- und Artikelplaetzen. Hobbyregister-Einzelprofil erhaelt den bisher fehlenden Integrationspunkt; vorgegebene HD007-Seitenstruktur unveraendert. Vorhandene Partner-/Kategorierangfolge bleibt vorrangig, nichts ueberschrieben. Keine DataForSEO-Abfrage, keine neue DB/Tabelle, kein Extra-Plugin. Fehlendes passendes Bild bedeutet kein Banner. Eigene Mietwerbung bleibt getrennt.\n").encode("utf-8")
entries[CSS]=entries[CSS]+b"\n"+STYLE.encode("utf-8")
with zipfile.ZipFile(DESIGN) as z:
    for target,source in assets.items():
        assert source in z.namelist(),source
        entries[target]=z.read(source)
assert len(entries)==len(set(entries))
assert b"HDAR_Amazon_Start::render_slot" in entries[MAIN]
assert b"hdar_ci_register_footer" in entries[MAIN]
assert b"object-fit:cover" in entries[CSS]
assert b"image_entry" in entries[MAIN]
with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)
    php_files=sorted(n for n in entries if n.endswith(".php"))
    for n in php_files:
        f=root/n;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(entries[n])
        p=subprocess.run(["php","-l",str(f)],capture_output=True,text=True)
        assert p.returncode==0,(n,p.stdout,p.stderr)
tmpfile=HOBBY.with_suffix(".next.zip")
with zipfile.ZipFile(tmpfile,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for n,b in sorted(entries.items()):z.writestr(n,b)
with zipfile.ZipFile(tmpfile) as z:
    assert z.testzip() is None
    assert set(z.namelist())==set(entries)
    assert z.read(MAIN)==entries[MAIN]
    assert z.read("affiliate-portal-router/assets/hdar-ci-logo-original.png")==entries["affiliate-portal-router/assets/hdar-ci-logo-original.png"]
tmpfile.replace(HOBBY)
sha=hashlib.sha256(HOBBY.read_bytes()).hexdigest()
report=ROOT/"PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/HD009_0117_CI_SINGLE_RELEASE_REPORT.txt"
report.write_text(f"Version: 0.1.17-dev\nBytes: {HOBBY.stat().st_size}\nSHA-256: {sha}\nFiles: {len(entries)}\nPHP: {len(php_files)}/{len(php_files)} PASS\nZIP CRC: PASS\nThree existing HD003 approved original files copied unchanged: logo, Malen hero, Modellbau hero.\nNo rental ad fallback.\nExisting partner campaign picker, category/parent-path, slot format, products, glossary and fees stay unchanged.\nNew: thematic Amazon discovery banner only on empty native slots, no price/product claims; missing image fails closed.\nNew: HD007 register route uses current HD009 renderer as integration point; no extra plugin.\nActual WP front-end and true Amazon referral clicks NOT tested in this build.\n",encoding="utf8")
print("HD009 0.1.17 prepared",HOBBY.stat().st_size,sha,len(php_files),"PHP PASS")
