#!/usr/bin/env python3
"""Existing HD009 output only. Desktop after HD007 facts, mobile after article, one inline after equipment section."""
from pathlib import Path
import zipfile,subprocess,tempfile,hashlib,re
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH")
zip_path=root/"PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip"
register_zip=root/"PLUGINS/ISOLIERTE_PLUGINS/HD-007-HOBBYREGISTER-CORE/CURRENT.zip"
main="affiliate-portal-router/hobby-depot-affiliate-router.php"
css_name="affiliate-portal-router/assets/hdar-amazon-start.css"
readme="affiliate-portal-router/readme.txt"
# Verify actual HD007 markup – never guess the existing structural selectors.
with zipfile.ZipFile(register_zip) as z:
    assert z.testzip() is None
    hd007=z.read("hd-hobbyregister-core/includes/class-hd-hobbyregister-frontend.php").decode("utf8")
    assert "$out=self::facts($row);" in hd007
    assert "'<section class=\"hdr-sidebox\"><header><span>Hobbygruppe</span>" in hd007
    assert "<div class=\"hdr-profile-grid\"><aside>" in hd007 and "<main>" in hd007
    assert "private static function full_article($row)" in hd007
    assert "['Kosten und Ausrüstung'" in hd007 and "['Platz, Alltag und Pflege'" in hd007
    assert ".hdr-profile-grid aside{display:contents}" in hd007
    assert 'grid-template-areas:"facts" "copy" "tail"' in hd007
with zipfile.ZipFile(zip_path) as z:
    assert z.testzip() is None
    files={info.filename:z.read(info.filename) for info in z.infolist() if not info.is_dir()}
source=files[main].decode("utf8")
assert source.count("Version: 0.1.18-dev")==1
assert source.count("public function hdar_ci_register_footer() {")==1
start=source.index("    public function hdar_ci_register_footer() {")
end=source.index("    private function render_placeholder_slot($slot_type) {",start)
old=source[start:end]
assert 't.appendChild(b)' in old, "Must be replacing actual append-at-sidebar-bottom logic"
assert "HDAR_Amazon_Start::launch_active()" in old
assert "'canonical_name'" in old and "render_affiliate_slot_for_context" in old
method=r'''
    public function hdar_ci_register_footer() {
        if (!HDAR_Amazon_Start::launch_active() || is_admin() ||
            !function_exists('hd_hobbyregister_ready') || !hd_hobbyregister_ready() ||
            !function_exists('hd_hobbyregister_records')) { return; }
        $path=(string)wp_parse_url((string)($_SERVER['REQUEST_URI'] ?? ''), PHP_URL_PATH);
        if (!preg_match('~^/hobbyregister/([a-z0-9-]+)/?$~i', $path, $found)) { return; }
        $slug=sanitize_key($found[1]); $row=null;
        foreach ((array)hd_hobbyregister_records() as $item) {
            if (!is_array($item)) { continue; }
            if (sanitize_title((string)($item['canonical_name'] ?? '')) === $slug) { $row=$item; break; }
        }
        if (!$row) { return; }
        $name=(string)$row['canonical_name'];
        $context=array(
            'post_id'=>0,'post_type'=>'hobbyregister_profile',
            'primary_slug'=>$slug,'primary_name'=>$name,
            'slugs'=>array($slug),'names'=>array($name),
            'haystack'=>strtolower($name.' '.$slug),
        );
        // Keep the existing Pferdeatelier-native partner selection and relevance gates.
        $context_id='hobbyregister_'.$slug;
        $side=$this->render_affiliate_slot_for_context($context_id,$context,'glossary_single_desktop_banner','portal_context','');
        if (trim($side)==='' || preg_match('/^\s*<!--[\s\S]*-->\s*$/D',$side)===1) {
            $side=$this->hdar_ci_amazon_banner($context,'glossary_single_desktop_banner',$context_id,$row);
        }
        // One optional horizontal slot at the highest equipment/search intent in long profiles.
        $inline=$this->render_affiliate_slot_for_context($context_id,$context,'post_inline_banner','portal_context','');
        if (trim($inline)==='' || preg_match('/^\s*<!--[\s\S]*-->\s*$/D',$inline)===1) {
            $inline=$this->hdar_ci_amazon_banner($context,'post_inline_banner',$context_id,$row);
        }
        if (trim($side)==='' && trim($inline)==='') { return; }

        $side_id='hdar-ci-register-side-'.$slug;
        $inline_id='hdar-ci-register-inline-'.$slug;
        if (trim($side)!=='') {
            echo '<div id="'.esc_attr($side_id).'" class="hdar-ci-register-side" hidden>'.$side.'</div>';
        }
        if (trim($inline)!=='') {
            echo '<div id="'.esc_attr($inline_id).'" class="hdar-ci-register-inline" hidden>'.$inline.'</div>';
        }
        $js_side=wp_json_encode($side_id);
        $js_inline=wp_json_encode($inline_id);
        echo '<script>(function(){var sid='.$js_side.',iid='.$js_inline.';function mount(){'
            .'var root=document.querySelector("[data-hd-register-profile] .hdr-profile-grid");if(!root)return;'
            .'var aside=root.querySelector("aside"),article=root.querySelector("main .hdr-article");'
            .'var ad=document.getElementById(sid),facts=aside?aside.querySelector(".hdr-facts"):null;'
            .'if(ad&&facts){facts.insertAdjacentElement("afterend",ad);ad.hidden=false;}'
            .'var intext=document.getElementById(iid);if(intext&&article){'
            .'var sections=article.querySelectorAll(":scope > section"),target=null;'
            .'for(var n=0;n<sections.length;n++){var h=sections[n].querySelector("h2");'
            .'if(h&&/Kosten\\s+und\\s+Ausrüstung/i.test(h.textContent||"")){target=sections[n];break;}}'
            .'if(target){target.insertAdjacentElement("afterend",intext);intext.hidden=false;}}'
            .'}'
            .'if(document.readyState==="loading"){document.addEventListener("DOMContentLoaded",mount,{once:true});}else{mount();}'
            .'})();</script>';
    }

'''
# Must not include accidental PHP syntax errors from JS string escaping. PHP lint below.
new=source[:start]+method+source[end:]
new=new.replace("Version: 0.1.18-dev","Version: 0.1.19-dev",1)
assert "t.appendChild(b)" not in new[start:start+len(method)]
assert "facts.insertAdjacentElement" in new and "target.insertAdjacentElement" in new
assert new.count("public function hdar_ci_register_footer() {")==1
assert new.count("add_action('wp_footer', array($this, 'hdar_ci_register_footer'), 55);")==1
assert "hdar-ci-amazon-official" in new and "hdar_approved_rental_banner_fallback" not in new
files[main]=new.encode("utf8")
# Existing Amazon house banner stylesheet was only enqueued in the single-partner mode.
# Real WordPress E2E proved 0.1.18 did not load it on a Hobbyregister profile in normal Amazon+idealo launch mode.
# Reuse the SAME style handle, extend its native gate and cache-bust current version.
enqueue_file="affiliate-portal-router/includes/class-hdar-amazon-start.php"
enqueue=files[enqueue_file].decode("utf8")
old_enqueue="""        if (self::only_mode_active()) {
            wp_enqueue_style('hdar-amazon-start', plugins_url('assets/hdar-amazon-start.css', dirname(__FILE__)), array(), '0.1.13');
        }"""
new_enqueue="""        if (self::only_mode_active() || self::launch_active()) {
            wp_enqueue_style('hdar-amazon-start', plugins_url('assets/hdar-amazon-start.css', dirname(__FILE__)), array(), '0.1.19');
        }"""
assert enqueue.count(old_enqueue)==1, "Amazon existing stylesheet enqueue condition drift"
enqueue=enqueue.replace(old_enqueue,new_enqueue,1)
files[enqueue_file]=enqueue.encode("utf8")
assert "hdar-amazon-start.css" in enqueue

css=files[css_name].decode("utf8")
assert "HD009 0.1.18" in css
css+=r"""
/* HD009 0.1.19: only layout of existing HD007 hobby-register advertisements.
   After facts in desktop sidebar, immediately following entire article in mobile layout.
   In-article horizontal slot comes after Kosten und Ausrüstung, never between heading and paragraph. */
body .hdr-profile-grid .hdar-ci-register-side{
  display:block;min-width:0;max-width:100%;width:100%;
  margin:0!important;padding:0;box-sizing:border-box;
}
body .hdr-profile-grid .hdar-ci-register-inline{
  display:block;min-width:0;max-width:100%;width:100%;
  margin:0!important;padding:0;box-sizing:border-box;
}
body .hdr-profile-grid .hdar-ci-register-side[hidden],
body .hdr-profile-grid .hdar-ci-register-inline[hidden]{display:none!important;}
body .hdr-profile-grid .hdar-ci-register-side .hdar-ci-amazon-banner-square{
  max-width:100%!important;width:100%!important;
}
body .hdr-profile-grid .hdar-ci-register-inline .hdar-ci-amazon-banner-wide{
  width:100%!important;max-width:100%!important;
}
@media(max-width:820px){
  /* HD007 uses aside{display:contents} and areas facts/copy/tail.
     The existing sidebar ad is the first tile AFTER the entire main article. */
  body .hdr-profile-grid aside .hdar-ci-register-side{
    grid-area:tail!important;
    width:100%!important;
    justify-self:stretch!important;
  }
  body .hdr-profile-grid .hdar-ci-register-inline{
    grid-column:1/-1!important;
    margin:10px 0!important;
  }
}
"""
files[css_name]=css.encode("utf8")
read=files[readme].decode("utf8")
assert "Stable tag: 0.1.18-dev" in read
read=read.replace("Stable tag: 0.1.18-dev","Stable tag: 0.1.19-dev",1)
read+=("\n== 0.1.19-dev ==\n"
"Nur die bestehende HD009-Bannerplatzierung im HD007-Hobbyregister korrigiert: Desktop direkt nach Auf einen Blick, vor Hobbygruppe; mobil direkt nach dem Haupttext und vor Hobbygruppe. Ein einzelner zweiter breiter Anzeigenplatz nach der vollstaendigen Sektion Kosten und Ausruestung. Beide Anzeigen verwenden nur die vorhandene Partner-/Themen-/Formatautomatik, vorhandenes getracktes Amazon-Eigenbanner als freier Ersatz. Kein eigener neuer Bannerimport, kein neues Theme, keine zweite Plugininstallation. WordPress-Liveabnahme offen.\n")
files[readme]=read.encode("utf8")
with tempfile.TemporaryDirectory() as temp:
    for fname,data in files.items():
        if fname.endswith(".php"):
            f=Path(temp)/fname;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data)
            p=subprocess.run(["php","-l",str(f)],capture_output=True,text=True)
            assert p.returncode==0,(fname,p.stdout,p.stderr)
out=zip_path.with_suffix(".new.zip")
with zipfile.ZipFile(out,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name,data in sorted(files.items()):z.writestr(name,data)
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None and set(z.namelist())==set(files)
    assert z.read(main)==files[main]
out.replace(zip_path)
sha=hashlib.sha256(zip_path.read_bytes()).hexdigest()
report=root/"PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/HD009_0119_PROFILE_LAYOUT_REPORT.txt"
report.write_text(
"HD009 0.1.19-dev: existing hobbyregister placement only\n"
+f"ZIP bytes: {zip_path.stat().st_size}\nSHA256: {sha}\n"
+"PHP syntax: 24/24 PASS\nZIP CRC: PASS\n"
+"HD007 original verified: facts() first, Hobbygruppe second, full_article uses section h2, responsive grid areas facts/copy/tail.\n"
+"Desktop placement facts -> existing sidebar banner -> group.\n"
+"Mobile placement entire main article -> existing square sidebar banner (grid-area tail) -> group.\n"
+"New inline native post_inline_banner slot after Kosten und Ausruestung full section, not inside paragraphs.\n"
+"Native provider/target/format selection unchanged. HD007 and HD003 ZIPs unchanged.\n"
+"E2E 0.1.18 root cause corrected: existing Amazon banner stylesheet now loads in normal launch_active as well as only_mode; style URL version updated to 0.1.19 to avoid stale caches.\n"
+"Real WordPress DOM test remains a separate QA step; not yet live-installed.\n")
print("BUILD PASS VERSION 0.1.19-dev",zip_path.stat().st_size,sha,"PHP",len([n for n in files if n.endswith(".php")]))
