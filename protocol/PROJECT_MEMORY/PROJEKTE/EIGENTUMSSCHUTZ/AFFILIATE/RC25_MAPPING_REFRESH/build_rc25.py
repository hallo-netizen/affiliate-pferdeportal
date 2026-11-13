#!/usr/bin/env python3
"""HAB-only RC25: existing Idealo import checks BOTH feed and product mapping.
No new worker, table, matcher or source; rebuild from verified RC24 only.
"""
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
from hashlib import sha256

root = Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
plugin = root / "PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
old = plugin.read_bytes()
assert sha256(old).hexdigest() == "888f6325cc011c3a380d2aae03054b8870db088c11ae6057e2fc1e4ce422f6a2", "RC25 MUST start from exact verified RC24"

base="affiliate-portal-router/"
idealo=base+"includes/trait-ppar-idealo.php"
main=base+"affiliate-portal-router.php"
readme=base+"readme.txt"
def once(s,a,b):
    n=s.count(a)
    assert n==1, ("Expected EXACTLY one known original anchor",n,a[:160])
    return s.replace(a,b,1)

with ZipFile(BytesIO(old)) as z:
    assert z.testzip() is None and len(z.namelist())==36
    files={i.filename:z.read(i.filename) for i in z.infolist()}
    t=files[idealo].decode("utf8")
    # Source-reproducible root cause: unchanged remote hash returns before the
    # feed can be re-matched against the NEW RC24 product concept catalog.
    t=once(t,
"""    private function idealo_refresh_remote_feed($metadata_first=true) {
        $s=$this->idealo_settings();
        if ($metadata_first) {""",
"""    private function idealo_refresh_remote_feed($metadata_first=true) {
        $s=$this->idealo_settings();
        // Re-process the same partner feed when the actual product-to-target
        // mapping changes. The signature stays in the EXISTING provider option.
        $mi=$this->idealo_match_index();
        if (is_wp_error($mi)) { return $mi; }
        $signature_concepts=(array)($mi['concepts']??array());
        ksort($signature_concepts,SORT_STRING);
        $catalog_signature=hash('sha256',wp_json_encode($signature_concepts));
        $catalog_changed=!hash_equals((string)($s['last_catalog_signature']??''),$catalog_signature);
        if ($metadata_first) {""")
    t=once(t,
"""&& absint($s['last_import_at']??0)>0) { return array('status'=>'unchanged','message'=>'Feed-Hash unverändert; kein Download.'); }""",
"""&& absint($s['last_import_at']??0)>0 && !$catalog_changed) { return array('status'=>'unchanged','message'=>'Feed und Produktzuordnung unverändert; kein Download.'); }""")
    t=once(t,
"""        $download=$this->idealo_download_feed_to_temp($s); if (is_wp_error($download)) { return $download; }""",
"""        // A changed mapping requires the bytes even when an ETag/304 would
        // otherwise skip the same remote feed. Never bypass normal cache
        // checks when the mapping and partner feed are both unchanged.
        $download_settings=$s;
        if ($catalog_changed) {
            $download_settings['feed_etag']='';
            $download_settings['feed_last_modified']='';
        }
        $download=$this->idealo_download_feed_to_temp($download_settings); if (is_wp_error($download)) { return $download; }""")
    t=once(t,
"""$s['last_download_at']=time(); $s['last_remote_file_hash']=(string)($s['api_last_feed_hash']??''); update_option(self::OPTION_NETWORK_IDEALO,$s,false);""",
"""$s['last_download_at']=time(); $s['last_remote_file_hash']=(string)($s['api_last_feed_hash']??''); $s['last_catalog_signature']=$catalog_signature; update_option(self::OPTION_NETWORK_IDEALO,$s,false);""")
    files[idealo]=t.encode("utf8")
    m=files[main].decode("utf8")
    m=once(m,"Version: 0.1.21-rc24","Version: 0.1.22-rc25")
    files[main]=m.encode("utf8")
    rd=files[readme].decode("utf8")
    rd=once(rd,"Stable tag: 0.1.21-rc24","Stable tag: 0.1.22-rc25")
    files[readme]=rd.encode("utf8")

    touched={idealo,main,readme}
    assert all(files[x]==z.read(x) for x in z.namelist() if x not in touched)
    out=BytesIO()
    with ZipFile(out,"w") as fresh:
        for item in z.infolist():
            fresh.writestr(item,files[item.filename])
    blob=out.getvalue()
with ZipFile(BytesIO(blob)) as check:
    assert len(check.namelist())==36 and check.testzip() is None
    assert b"Version: 0.1.22-rc25" in check.read(main)
    assert b"last_catalog_signature" in check.read(idealo)
plugin.write_bytes(blob)
print("HAB_RC25_MINIMAL_BUILD_PASS",len(blob),sha256(blob).hexdigest(), "3 existing files changed; 33 identical")
