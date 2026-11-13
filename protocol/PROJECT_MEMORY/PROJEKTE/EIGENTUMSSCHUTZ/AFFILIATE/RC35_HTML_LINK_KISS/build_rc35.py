#!/usr/bin/env python3
"""RC35: one import-time decision reads real original HTML link evidence.
No second decision and no new worker. Build only from exact RC34 original.
"""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from hashlib import sha256
R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
raw=P.read_bytes()
assert sha256(raw).hexdigest()=="bdd7ba78da62995768ee3c476f60fa7c18352161c7d6f9b5bade35978853cb62","Require exact RC34"
base="affiliate-portal-router/"
out=base+"includes/trait-ppar-output-objects.php"
creative=base+"includes/trait-ppar-creative-library.php"
main=base+"affiliate-portal-router.php"
readme=base+"readme.txt"
def one(s,a,b):
    assert s.count(a)==1,("unexpected source",s.count(a),a[:170])
    return s.replace(a,b,1)
with ZipFile(BytesIO(raw)) as original:
    assert original.testzip() is None and len(original.namelist())==36
    data={z.filename:original.read(z.filename) for z in original.infolist()}
    o=data[out].decode()
    # This is the existing single evidence reader, NOT another classifier.
    o=one(o,
        "        if (in_array($destination_source, array('tracking_fallback','tracking_checked'), true)) { return ''; }",
        r"""        if (in_array($destination_source, array('tracking_fallback','tracking_checked'), true)) {
            // The HTML's anchor href is already stored as tracking_url.
            // A real Tarifcheck deep=insurance-type is direct source evidence,
            // even when HTTP redirects did not produce a separate destination.
            // Do NOT reinterpret anonymous third-party tracking hostnames.
            if ($this->output_comparison_banner_partner($row)==='tarifcheck') {
                $tracked=esc_url_raw((string)($row['tracking_url']??''));
                $parts=wp_parse_url($tracked);
                $parts=is_array($parts)?$parts:array();
                $host=strtolower((string)($parts['host']??''));
                $host=preg_replace('/^www\./','',$host);
                if ($host==='a.partner-versicherung.de' || $host==='partner-versicherung.de') {
                    $params=array();
                    parse_str((string)($parts['query']??''),$params);
                    $deep=is_scalar($params['deep']??null)?trim((string)$params['deep']):'';
                    if ($deep!=='' && strlen($deep)<=160) {
                        return $this->output_text($deep);
                    }
                }
                // A first-party landing-page path in the original href is
                // already a genuine destination: no extra HTTP or inference.
                if ($host==='tarifcheck.de' || substr($host,-14)==='.tarifcheck.de') {
                    $path=(string)($parts['path']??'');
                    if ($path!=='' && $path!=='/'
                        && !preg_match('~/(?:click|redirect|go|out)(?:[./]|$)~i',$path)) {
                        return $this->output_text($path);
                    }
                }
            }
            return '';
        }""")
    # Original anchor text is saved in payload.html by the existing importer.
    # Recover it IN the same existing import decision for old originals.
    o=one(o,
        """        $real_title=in_array($title_source,array('provider_missing','manual_missing'),true)
            ? '' : (string)($row['title']??'');
        // Three pre-existing evidence tiers, stronger first.""",
        """        $real_title=in_array($title_source,array('provider_missing','manual_missing'),true)
            ? '' : (string)($row['title']??'');
        $original_anchor_text=wp_strip_all_tags((string)($payload['html']??''));
        // Three pre-existing evidence tiers, stronger first.""")
    o=one(o,
        """              .' '.(string)($payload['banner_name']??'')),""",
        """              .' '.(string)($payload['banner_name']??'').' '.$original_anchor_text),""")
    # German singular/plural normalization within the ONE verified WP tree
    # match. A deep=kfz-versicherung must match a real Kfz-Versicherungen node.
    o=one(o,
        "        $all=implode(' ', $evidence);",
        """        $all=preg_replace('/versicherungen\\b/u','versicherung',implode(' ', $evidence));""")
    o=one(o,
        "            foreach ($phrases as $phrase) {",
        """            foreach ($phrases as $phrase) {
                $phrase=preg_replace('/versicherungen\\b/u','versicherung',$phrase);""")
    # The general family evaluator uses the SAME recovered original anchor text.
    o=one(o,
        """                (string)($payload['name'] ?? ''),
            ))),""",
        """                (string)($payload['name'] ?? ''),
                wp_strip_all_tags((string)($payload['html']??'')),
            ))),""")
    # Revisit old verified originals ONCE with this fixed import evidence.
    # RC34 has already marked its old pass complete; do not reuse that option.
    o=one(o,
        "$option='ppar_hab_rc34_tarifcheck_reconcile_v1';",
        "$option='ppar_hab_rc35_tarifcheck_reconcile_v1';")
    # When real original deep/path evidence exists, do not fetch the same
    # tracking URL again just to repeat a decision already available locally.
    o=one(o,
        """if(in_array($source,array('tracking_checked','tracking_fallback'),true)
            && method_exists($this,'creative_library_resolve_tracking_destination_import')){""",
        """if(in_array($source,array('tracking_checked','tracking_fallback'),true)
            && $this->output_destination_semantic_text($row)===''
            && method_exists($this,'creative_library_resolve_tracking_destination_import')){""")

    data[out]=o.encode()
    c=data[creative].decode()
    # A completed safe 3xx redirect on SAME domain is still a real redirect.
    # Old code threw the real landing URL away for same-host destinations.
    c=one(c,
        """if ($current !== $tracking_url && $final_host !== '' && $initial_host !== '' && $final_host !== $initial_host) {""",
        """if ($current !== $tracking_url && $final_host !== '' && $initial_host !== '') {""")
    data[creative]=c.encode()
    m=data[main].decode()
    m=one(m,"Version: 0.1.31-rc34","Version: 0.1.32-rc35")
    data[main]=m.encode()
    rd=data[readme].decode()
    rd=one(rd,"Stable tag: 0.1.31-rc34","Stable tag: 0.1.32-rc35")
    data[readme]=rd.encode()
    touched={out,creative,main,readme}
    assert all(data[n]==original.read(n) for n in original.namelist() if n not in touched)
    buf=BytesIO()
    with ZipFile(buf,"w") as new:
        for item in original.infolist():new.writestr(item,data[item.filename])
    final=buf.getvalue()
with ZipFile(BytesIO(final)) as verify:
    assert verify.testzip() is None and len(verify.namelist())==36
    assert b"0.1.32-rc35" in verify.read(main)
    assert b"original_anchor_text" in verify.read(out)
    assert b"partner-versicherung.de" in verify.read(out)
P.write_bytes(final)
print("RC35_HTML_LINK_SAME_OWNER_BUILD_PASS",len(final),sha256(final).hexdigest())
