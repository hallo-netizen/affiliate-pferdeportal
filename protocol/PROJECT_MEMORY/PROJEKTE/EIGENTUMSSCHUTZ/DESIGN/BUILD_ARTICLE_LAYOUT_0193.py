"""Build only from the user's installed original HAB-001 0.1.192. Never overwrite CURRENT."""
import hashlib,io,json,re,subprocess,tempfile
from pathlib import Path
from zipfile import ZipFile
ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
source=ROOT/"PLUGINS/ISOLIERTE_PLUGINS/HAB-001-DESIGN/CURRENT.zip"
sha=lambda b:hashlib.sha256(b).hexdigest()
raw=source.read_bytes()
assert sha(raw)=="d8f08ca73da4c56be61d55fdde02dac5ed5a1ecadcbc986221e2c93357ec8302","Unexpected source version; refuse build"
prefix="hab-bewahr-design-vorschau/"
main=prefix+"hab-bewahr-design-vorschau.php"
css=prefix+"assets/article-design.css"
article=prefix+"includes/article-page.php"
with ZipFile(io.BytesIO(raw)) as z:
    assert len(z.infolist())==432 and z.testzip() is None
    infos=z.infolist()
    before={i.filename:z.read(i.filename) for i in infos}
after=dict(before)
old=before[css].decode()
assert "display:block;overflow-x:auto" in old and ".hb-article-reading table" in old
# Preserve the old rules for desktop and all other page types. The table now uses
# its native grid; scroll the outer wrapper, never the table itself.
patch=r"""
/* 0.1.193 – Single articles only: responsive tables and editorial Merksatz. */
.hbdp-body .hb-article-reading .hb-article-table-scroll{
 display:block;box-sizing:border-box;max-width:100%;width:100%;overflow-x:auto;
 -webkit-overflow-scrolling:touch;margin:24px 0 26px
}
.hbdp-body .hb-article-reading .hb-article-table-scroll table,
.hbdp-body .hb-article-reading table.hb-fachtabelle,
.hbdp-body .hb-article-reading table{
 display:table!important;width:100%!important;min-width:100%;max-width:none!important;
 table-layout:auto;overflow:visible;box-sizing:border-box
}
.hbdp-body .hb-article-reading .hb-article-table-scroll table{margin:0}
.hbdp-body .hb-article-reading th,.hbdp-body .hb-article-reading td{
 min-width:0;white-space:normal;overflow-wrap:anywhere
}
.hbdp-body .hb-article-reading .hb-article-table-scroll th,
.hbdp-body .hb-article-reading .hb-article-table-scroll td{min-width:3.5rem}
.hbdp-body .hb-article-reading .hb-merksatz{
 position:relative;box-sizing:border-box;max-width:100%;padding:17px 19px 17px 45px;
 background:#f7ece6;border:1px solid #e9cfc2;border-left:4px solid var(--hbdp-terracotta,#a45d42);
 border-radius:5px;color:#41352f;margin:27px 0 31px;line-height:1.65
}
.hbdp-body .hb-article-reading .hb-merksatz::before{
 content:"";position:absolute;top:19px;left:15px;width:19px;height:19px;
 background:center/contain no-repeat url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' fill='none' stroke='%23a45d42' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M9 18h6M10 22h4M9 15c0-2-4-3-4-7a7 7 0 0 1 14 0c0 4-4 5-4 7'/%3E%3C/svg%3E")
}
.hbdp-body .hb-article-reading .hb-merksatz p{margin:0 0 8px}
.hbdp-body .hb-article-reading .hb-merksatz p:last-child{margin:0}
.hbdp-body .hb-article-reading .hb-merksatz > p:first-child > strong,
.hbdp-body .hb-article-reading .hb-merksatz > strong{color:#a45d42}
"""
after[css]=(old+"\n"+patch).encode()
# Rendering-only normalization. Existing marked blocks remain unchanged. All
# original article HTML is preserved inside wrappers; no stored post changes.
php=r"""
/** HAB-001 0.1.193: presentation only, called on the existing article reading HTML. */
function hbdp_article_layout_0193($html) {
    if (!is_string($html) || $html==='') return $html;
    $html=preg_replace_callback('~<table\b[^>]*>.*?</table\s*>~is',static function($m){
        return '<div class="hb-article-table-scroll">'.$m[0].'</div>';
    },$html);
    if (preg_match('~class\s*=\s*["\x27][^"\x27]*\bhb-merksatz\b~i',$html)) return $html;
    // Exact editorial heading only; never highlight arbitrary bold paragraphs.
    $html=preg_replace_callback('~<p\b[^>]*>\s*<(strong|b)\b[^>]*>\s*Merksatz\s*:?\s*</\1>\s*</p>\s*<p\b[^>]*>.*?</p>~isu',static function($m){
        return '<div class="hb-merksatz">'.$m[0].'</div>';
    },$html);
    if (!preg_match('~class\s*=\s*["\x27][^"\x27]*\bhb-merksatz\b~i',$html)) {
        $html=preg_replace_callback('~<p\b[^>]*>\s*<(strong|b)\b[^>]*>\s*Merksatz\s*:\s*</\1>[^<].*?</p>~isu',static function($m){
            return '<div class="hb-merksatz">'.$m[0].'</div>';
        },$html);
    }
    return $html;
}
"""
# The original renderer must explicitly apply the existing content filter.
# Scope to its actual call, not another new global WordPress filter.
ap=before[article].decode()
matches=list(re.finditer(r"apply_filters\s*\(\s*(['\"])the_content\1\s*,\s*(?:\$[A-Za-z_]\w*(?:->\w+)?|get_the_content\(\))\s*\)",ap))
assert len(matches)==1,("Expected one original article content call",len(matches))
m=matches[0]
ap=ap[:m.start()]+"hbdp_article_layout_0193("+m.group(0)+")"+ap[m.end():]
assert not ap.rstrip().endswith("?>"),"Review source placement"
after[article]=(ap+"\n"+php).encode()
s=before[main].decode()
assert s.count("Version: 0.1.192")==1
s=s.replace("Version: 0.1.192","Version: 0.1.193",1)
s,n=re.subn(r"(wp_enqueue_style\(\s*'hbdp-article-design'[^;\n]*,\s*)'[^']+'\s*\)",r"\g<1>'0.1.193')",s)
assert n==1,"No exact article stylesheet enqueue found"
after[main]=s.encode()
assert set(before)==set(after)
assert {k for k in before if before[k]!=after[k]}=={main,css,article}
out=Path("hab-design-article-candidate");out.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory() as d:
    p=Path(d)
    for name,data in after.items():
        if name.endswith(".php"):
            f=p/Path(name).name;f.write_bytes(data)
            subprocess.run(["php","-l",str(f)],check=True,capture_output=True)
    h=p/"layout.php"
    h.write_text("<?php\n"+php+"\n"+r"""
$cases=[
'<p><strong>Merksatz</strong></p><p>Originaltext &amp; mehr.</p>',
'<p><strong>Merksatz:</strong> Originaltext.</p>',
'<blockquote class="hb-merksatz"><p>Originaltext.</p></blockquote>',
'<p><strong>Unveränderte Überschrift</strong></p><p>Originaltext.</p>',
'<figure class="wp-block-table"><table><tbody><tr><td>Original</td></tr></tbody></table></figure>'
];
foreach($cases as $i=>$c){
  $r=hbdp_article_layout_0193($c);
  if ($i<3 && substr_count($r,'class="hb-merksatz"')!==1) exit(21);
  if ($i===3 && $r!==$c) exit(22);
  if ($i===4 && strpos($r,'class="hb-article-table-scroll"')===false) exit(23);
  if (str_replace(['<div class="hb-merksatz">','<div class="hb-article-table-scroll">','</div>'],'',$r)!==$c) exit(24);
}
echo "PHP presentation tests PASS\n";
""")
    subprocess.run(["php",str(h)],check=True)
target=out/"Hab-und-Bewahr-Design-0.1.193-TESTKANDIDAT.zip"
with ZipFile(target,"w") as z:
    for i in infos:z.writestr(i,after[i.filename])
with ZipFile(target) as z:
    assert z.testzip() is None and len(z.infolist())==432
    assert all(z.read(k)==v for k,v in after.items())
(out/"article-design.css").write_bytes(after[css])
(out/"evidence.json").write_text(json.dumps({"source_sha256":sha(raw),"candidate_sha256":sha(target.read_bytes()),"entries":432,"changed_files":sorted([main,css,article]),"php_lint_count":sum(x.endswith(".php") for x in after),"php_render_cases":5,"live_pass":False},indent=2))
print("Candidate built; never promoted to CURRENT.")
