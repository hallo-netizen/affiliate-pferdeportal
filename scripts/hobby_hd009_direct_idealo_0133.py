#!/usr/bin/env python3
"""HD009 0.1.33 – smallest source-proof direct iPN export fix.
Original 0.1.32 remains untouched; this builds a complete installable WordPress ZIP
from exact checked CURRENT.zip. No manual CSV, no frontend database/HTTP, no schema changes.
"""
import hashlib
import sys
import zipfile
from io import BytesIO
from pathlib import Path

BASE = Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE")
INPUT = BASE / "CURRENT.zip"
TARGET = Path(sys.argv[1] if len(sys.argv)>1 else "/tmp/HOBBY_DEPOT_AFFILIATE_HD009_0.1.33_DIRECT_IDEALO.zip")
EXPECTED_SHA256 = "d433db74b493407a4c26faef591574e644201846078b7aa7aa3541126f9359b8"
SHA = lambda v: hashlib.sha256(v).hexdigest()
original = INPUT.read_bytes()
assert SHA(original) == EXPECTED_SHA256, "HD009 0.1.32 source changed: refuse patch!"
trait = "affiliate-portal-router/includes/trait-ppar-idealo.php"
main  = "affiliate-portal-router/hobby-depot-affiliate-router.php"

def exact(s, old, new, label):
    hits = s.count(old)
    assert hits == 1, f"{label}: expected exactly one source anchor, found {hits}"
    return s.replace(old, new, 1)

with zipfile.ZipFile(BytesIO(original)) as z:
    assert z.testzip() is None and len(z.namelist()) == 41, "Damaged or unexpected original"
    infos = z.infolist()
    src = {i.filename: z.read(i.filename) for i in infos}
    code = src[trait].decode("utf-8")
    before = code

    # The exact source of the current problem: import, 12h refresh and button
    # currently require a manually saved Feed URL although findFeeds is PASS.
    # The already-present download/CSV/GZIP pipeline remains unchanged.
    methods = r'''    /**
     * Only the already enabled and verified Hobby Depot iPN account may import.
     * The last real findFeeds check must have passed for this site's own
     * adspace/feed pair. Never reuse other portals' saved source URLs.
     */
    private function hd_idealo_feed_source_ready($settings = null) {
        $s = is_array($settings) ? $settings : $this->idealo_settings();
        return !empty($s['enabled'])
            && (string)($s['adspace_id'] ?? '') === '568912'
            && !empty($s['hobby_feed_verified'])
            && ctype_digit((string)($s['feed_id'] ?? ''))
            && absint($s['feed_id'] ?? 0) > 0
            && $this->idealo_credentials_present($s)
            && absint($s['api_last_checked_at'] ?? 0) > 0;
    }

    /**
     * Existing private iPN API credentials, already checked via findFeeds,
     * are sufficient for the official CSV.GZ export. Only on the server.
     * A previously saved official URL still works as before.
     * @see https://ingenioustechnologies.atlassian.net/wiki/spaces/KB/pages/3310846106/
     */
    private function hd_idealo_feed_download_url($settings) {
        if (!$this->hd_idealo_feed_source_ready($settings)) {
            return new WP_Error('idealo_feed_not_verified',
                'Zuerst die Hobby-Depot-Werbefläche und den Feed über die Partner-API prüfen.');
        }
        $manual = trim((string)($settings['feed_url'] ?? ''));
        if ($manual !== '') { return $this->idealo_validate_feed_url($manual); }
        $url = add_query_arg(array(
            'apiKey'       => (string)$settings['api_key'],
            'feedId'       => (string)$settings['feed_id'],
            'adspaceId'    => '568912',
            'format'       => 'CSV',
            'csvSeparator' => 'COMMA',
            'compression'  => 'GZIP',
        ), $this->idealo_partner_api_base().'/creatives/productdata/export');
        return $this->idealo_validate_feed_url($url);
    }

'''
    code=exact(code,
        "    private function idealo_download_feed_to_temp($settings) {",
        methods+"    private function idealo_download_feed_to_temp($settings) {",
        "insert existing-plugin source selector")
    code=exact(code,
        "$url = $this->idealo_validate_feed_url((string)($settings['feed_url'] ?? ''));",
        "$url = $this->hd_idealo_feed_download_url($settings);",
        "use API export in existing download")
    code=exact(code,
        "if (trim((string)($s['feed_url']??''))==='') { return new WP_Error('idealo_feed_url_missing','Es ist noch keine vom iPN erzeugte Feed-URL gespeichert.'); }",
        "if (!$this->hd_idealo_feed_source_ready($s)) { return new WP_Error('idealo_feed_not_verified','Zuerst die freigegebene Hobby-Depot-API-Verbindung prüfen.'); }",
        "keep existing manual worker, remove the redundant URL-only barrier")
    code=exact(code,
        "$s=$this->idealo_settings(); $wanted=!empty($s['enabled'])&&!empty($s['auto_refresh'])&&trim((string)$s['feed_url'])!==''&&$this->idealo_credentials_present($s);",
        "$s=$this->idealo_settings(); $wanted=!empty($s['auto_refresh'])&&$this->hd_idealo_feed_source_ready($s);",
        "allow existing 12-hour schedule with verified API")
    code=exact(code,
        "<?php if (trim((string)$s['feed_url'])!==''): ?> <form method=\"post\"",
        "<?php if ($this->hd_idealo_feed_source_ready($s)): ?> <form method=\"post\"",
        "show existing Feed jetzt aktualisieren button for verified API")
    code=exact(code,
        "trim((string)$s['feed_url'])!==''?'automatisierbar':'Download-URL noch offen'",
        "$this->hd_idealo_feed_source_ready($s)?'über die Partner-API bereit':'API-Freigabe noch nicht bestätigt'",
        "show correct remote feed status")
    code=exact(code,
        "(!empty($s['auto_refresh'])&&trim((string)$s['feed_url'])!=='')?'bereit':'wartet auf Feed-URL'",
        "(!empty($s['auto_refresh'])&&$this->hd_idealo_feed_source_ready($s))?'bereit':'wartet auf API-Freigabe'",
        "show correct auto-refresh readiness")
    code=exact(code,
        "Feed automatisch alle zwölf Stunden auf Änderungen prüfen (nur bei gespeicherter Download-URL)",
        "Feed automatisch alle zwölf Stunden über die bestätigte idealo-Partner-API aktualisieren",
        "explain unchanged 12-hour refresher")
    code=exact(code,
        "Offizielle iPN-Download-URL für den Hobby-Depot-Feed <span",
        "Optionale iPN-Download-URL (der direkte API-Export funktioniert ohne Eingabe) <span",
        "mark manual URL as optional")

    # Guardrails: no automatic publication, no new network or schema.
    assert "private function idealo_import_feed_file(" in code
    assert "private function idealo_materialize_campaigns(" in code
    assert "private function idealo_refresh_remote_feed(" in code
    assert "private function idealo_dispatch_manual_worker(" in code
    assert "private function idealo_queue_manual_refresh(" in code
    assert "private function idealo_campaigns_should_be_active(" in code
    assert "if ($source==='idealo_product_feed_v1')" in code
    assert code.count("creatives/productdata/export") == 1
    assert "568944" not in methods and "568313" not in methods, "Cross-portal identifiers in source"
    assert "'output_mode' => 'ebay_only'" in code, "Do not change public provider mode behind user's back"
    src[trait] = code.encode("utf-8")

    header = src[main].decode("utf-8")
    assert header.count("0.1.32") > 0, "Version baseline is not 0.1.32"
    assert header.count("0.1.32") < 10, "Unexpected version markers"
    header = header.replace("0.1.32", "0.1.33")
    src[main] = header.encode("utf-8")

    changed = {name for name in src if src[name] != z.read(name)}
    assert changed == {trait,main}, f"Unexpected changes to unrelated files: {changed}"
    output = BytesIO()
    with zipfile.ZipFile(output,"w") as dst:
        for info in infos:
            dst.writestr(info,src[info.filename])
    payload = output.getvalue()

with zipfile.ZipFile(BytesIO(payload)) as z:
    assert len(z.namelist()) == 41 and z.testzip() is None
    assert b"Version: 0.1.33" in z.read(main)
    assert b"private function hd_idealo_feed_source_ready" in z.read(trait)
    assert b"private function hd_idealo_feed_download_url" in z.read(trait)

TARGET.parent.mkdir(parents=True,exist_ok=True)
TARGET.write_bytes(payload)
print("SOURCE_SHA256", SHA(original))
print("NEW_SHA256",SHA(payload))
print("SOURCE_ENTRIES",41,"TARGET_ENTRIES",41)
print("CHANGED_FILES",sorted(changed))
print("BYTES",len(payload))
print("BUILD_OUTPUT",str(TARGET))
