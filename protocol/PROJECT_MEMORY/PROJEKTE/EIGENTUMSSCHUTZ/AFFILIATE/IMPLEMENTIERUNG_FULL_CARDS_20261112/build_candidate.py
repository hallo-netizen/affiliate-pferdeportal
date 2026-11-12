#!/usr/bin/env python3
"""Hab-only, no shared source copying: connect existing iPN API settings to
the existing image/product feed importer and category selection.
Not a release until real feed-backed category output is demonstrated.
"""
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
import hashlib
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
p=root/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
old=p.read_bytes()
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(old)=="c9d501396d5500e699eb6dd8d867318c41e8ea8efc43c8fe00ad9ee4ab4e32d1",("Unapproved HAB base",sha(old))
base="affiliate-portal-router/"
trait=base+"includes/trait-ppar-idealo.php"
main=base+"affiliate-portal-router.php"
ebay=base+"includes/trait-ppar-ebay.php"
readme=base+"readme.txt"
def replace_one(s,a,b):
 count=s.count(a)
 assert count==1, ("Unexpected anchor count",count,a[:180])
 return s.replace(a,b,1)
with ZipFile(BytesIO(old)) as z:
 assert z.testzip() is None and len(z.namelist())==36
 names=z.namelist()
 files={i.filename:z.read(i.filename) for i in z.infolist()}
 t=files[trait].decode()
 anchor="    private function idealo_download_feed_to_temp($settings) {"
 insertion=r'''    /**
     * Connect the already approved iPN Partner API to its documented CSV export.
     * No second credential, no new API, no public browser request, no URL storage.
     * All sensitive parameters are used server-side for the background import.
     * @see Ingenious Partner Marketing 2022 productdata/export migration notes.
     */
    private function hb_idealo_feed_source_ready($settings = null) {
        $settings = is_array($settings) ? $settings : $this->idealo_settings();
        return !empty($settings['enabled'])
            && (string)($settings['adspace_id'] ?? '') === '568944'
            && $this->idealo_credentials_present($settings)
            && (
                trim((string)($settings['feed_url'] ?? '')) !== ''
                || absint($settings['api_last_checked_at'] ?? 0) > 0
            );
    }

    private function hb_idealo_feed_download_url($settings) {
        if (!$this->hb_idealo_feed_source_ready($settings)) {
            return new WP_Error('hb_idealo_feed_not_verified',
                'Idealo für Hab & Bewahr: erst eigene Werbefläche 568944, Feed-ID und API-Verbindung prüfen.');
        }
        $manual=trim((string)($settings['feed_url'] ?? ''));
        if ($manual!=='') { return $this->idealo_validate_feed_url($manual); }
        // Official documented export path; iPN-API-Key remains in memory, and
        // the user never has to copy/paste a private export link into WordPress.
        $url=add_query_arg(array(
            'apiKey'=>(string)$settings['api_key'],
            'feedId'=>(string)$settings['feed_id'],
            'adspaceId'=>'568944',
            'format'=>'CSV',
            'csvSeparator'=>'COMMA',
            'compression'=>'GZIP',
        ),$this->idealo_partner_api_base().'/creatives/productdata/export');
        return $this->idealo_validate_feed_url($url);
    }

'''
 t=replace_one(t,anchor,insertion+anchor)
 t=replace_one(t,
    "$url = $this->idealo_validate_feed_url((string)($settings['feed_url'] ?? ''));",
    "$url = $this->hb_idealo_feed_download_url($settings);")
 t=replace_one(t,
    "if (trim((string)($s['feed_url']??''))==='') { return new WP_Error('idealo_feed_url_missing','Es ist noch keine vom iPN erzeugte Feed-URL gespeichert.'); }",
    "if (!$this->hb_idealo_feed_source_ready($s)) { return new WP_Error('idealo_feed_not_ready','Idealo-Produktfeed: eigene Hab-&-Bewahr-Verbindung zunächst prüfen.'); }")
 t=replace_one(t,
    "$s=$this->idealo_settings(); $wanted=!empty($s['enabled'])&&!empty($s['auto_refresh'])&&trim((string)$s['feed_url'])!==''&&$this->idealo_credentials_present($s);",
    "$s=$this->idealo_settings(); $wanted=!empty($s['auto_refresh'])&&$this->hb_idealo_feed_source_ready($s);")
 # Provider card already exists and owns the upload/trigger. No UI duplication.
 t=replace_one(t,
    "<?php if (trim((string)$s['feed_url'])!==''): ?> <form method=\"post\"",
    "<?php if ($this->hb_idealo_feed_source_ready($s)): ?> <form method=\"post\"")
 t=replace_one(t,
    "trim((string)$s['feed_url'])!==''?'automatisierbar':'Download-URL noch offen'",
    "$this->hb_idealo_feed_source_ready($s)?'über iPN-Partner-API bereit':'API-Verbindung noch nicht geprüft'")
 t=replace_one(t,
    "(!empty($s['auto_refresh'])&&trim((string)$s['feed_url'])!=='')?'bereit':'wartet auf Feed-URL'",
    "(!empty($s['auto_refresh'])&&$this->hb_idealo_feed_source_ready($s))?'bereit':'wartet auf API-Freigabe'")
 t=replace_one(t,
    "Feed automatisch alle zwölf Stunden auf Änderungen prüfen (nur bei gespeicherter Download-URL)",
    "Feed automatisch alle zwölf Stunden über die bestätigte iPN-Verbindung aktualisieren")
 t=replace_one(t,
    "Offizielle iPN-Download-URL für den eigenen Feed <span",
    "Optionale abweichende iPN-Download-URL (automatischer Export über bestätigten API-Zugang möglich) <span")
 # Fix selection: in existing 'hybrid' mode category cards must use image-backed
 # real product identity instead of a generic family comparison. Scope fixed 3 slots.
 t=replace_one(t,
    """        // Hybrid: idealo is a family/category comparison when it stands alone.
        // Exact concrete idealo offers remain available only as an additional
        // button on an already selected concrete product via exact GTIN.
        return $kind === 'comparison';""",
    """        // Hab category recommendations need real image-backed GTIN products.
        // Hybrid still means category comparison on every unrelated slot.
        if (preg_match('/^category_product_[123]$/D', sanitize_key((string)$slot_type))) {
            return $kind === 'product';
        }
        return $kind === 'comparison';""")
 # Successful real import unblocks two temporary pre-import gates, without
 # publishing zero or unmaterialized feeds and without resetting manual choices.
 needle="""        if (!is_wp_error($materialized)) { $settings['last_materialized_at']=time(); $settings['last_materialized_count']=absint($materialized['campaigns']??0); $settings['last_materialized_targets']=absint($materialized['targets']??0); update_option(self::OPTION_NETWORK_IDEALO,$settings,false); }"""
 new="""        if (!is_wp_error($materialized)) {
            $settings['last_materialized_at']=time();
            $settings['last_materialized_count']=absint($materialized['campaigns']??0);
            $settings['last_materialized_targets']=absint($materialized['targets']??0);
            if ($settings['last_materialized_count'] > 0 && $settings['last_materialized_targets'] > 0) {
                // Existing product cards are already live-authorized by the user;
                // only flip the temporary "existing eBay only" setup default
                // once actual image+GTIN campaigns have been saved.
                if (sanitize_key((string)($settings['output_mode']??'')) === 'ebay_only') {
                    $settings['output_mode']='automatic';
                }
                // For category slots, the existing Hybrid mode now delivers
                // concrete image-backed products; preserve other slot behavior.
            }
            update_option(self::OPTION_NETWORK_IDEALO,$settings,false);
            $this->idealo_sync_campaign_activation();
        }"""
 t=replace_one(t,needle,new)
 # Make sure real imported campaign at materialization was set inactive by ebay_only,
 # and the post-import sync reactivates it once quality and target gates pass.
 t=replace_one(t,
    "if (is_wp_error($response)) { @unlink($tmp); return $response; }",
    "if (is_wp_error($response)) { @unlink($tmp); return new WP_Error('hab_idealo_export_transport_failed','Der offizielle iPN-Produktdatenexport konnte nicht abgerufen werden.'); }")
 # The old exact-GTIN combination lost the OWN base provider whenever a
 # second merchant was found. Preserve idealo as a real CTA beside matching eBay
 # and verified Amazon; do not invent any provider URL or change identity gates.
 t=replace_one(t,
    "if (!$offers && $current_url!=='') { $offers[$base['network']]=$base; }",
    "if ($current_url!=='' && !isset($offers[$base['network']])) { $offers[$base['network']]=$base; }")
 # Every provider filter must preserve the actual category slot when
 # deciding whether image-backed idealo products are acceptable.
 t=replace_one(t,
    "public function multiprovider_filter_candidates_by_strategy($candidates) {",
    "public function multiprovider_filter_candidates_by_strategy($candidates, $slot_type='') {")
 t=replace_one(t,
    "array_values((array)$candidates),function($candidate){",
    "array_values((array)$candidates),function($candidate)use($slot_type){")
 t=replace_one(t,
    "$this->idealo_standalone_campaign_allowed($campaign);",
    "$this->idealo_standalone_campaign_allowed($campaign,$slot_type);")
 t=replace_one(t,
    "public function multiprovider_reorder_candidates($candidates,$mode='separate') {",
    "public function multiprovider_reorder_candidates($candidates,$mode='separate',$slot_type='') {")
 t=replace_one(t,
    "$candidates=$this->multiprovider_filter_candidates_by_strategy($candidates);",
    "$candidates=$this->multiprovider_filter_candidates_by_strategy($candidates,$slot_type);")
 files[trait]=t.encode()
 e=files[ebay].decode()
 e=replace_one(e,
    "private function ebay_filter_ranked_product_candidates_provider_cohort($candidates) {",
    "private function ebay_filter_ranked_product_candidates_provider_cohort($candidates, $slot_type='') {")
 # One request-local cache entry per slot because hybrid strategy differs on
 # category products versus all other placements.
 e=replace_one(e,
    "$cohort_cache_key = hash('sha256', serialize($fingerprint));",
    "$cohort_cache_key = hash('sha256', sanitize_key((string)$slot_type).'|'.serialize($fingerprint));")
 e=replace_one(e,
    "$out = $this->multiprovider_reorder_candidates($out, $mode);",
    "$out = $this->multiprovider_reorder_candidates($out, $mode, $slot_type);")
 files[ebay]=e.encode()
 m=files[main].decode()
 # Propagate the real slot through all three central selection paths, not just
 # through the final renderer after candidates have been removed.
 assert m.count("ebay_filter_ranked_product_candidates_provider_cohort($candidates);")==3
 m=m.replace("ebay_filter_ranked_product_candidates_provider_cohort($candidates);",
             "ebay_filter_ranked_product_candidates_provider_cohort($candidates,$slot_type);")
 assert m.count("multiprovider_filter_candidates_by_strategy($candidates);")==3
 m=m.replace("multiprovider_filter_candidates_by_strategy($candidates);",
             "multiprovider_filter_candidates_by_strategy($candidates,$slot_type);")
 m=replace_one(m,"Version: 0.1.19-rc22","Version: 0.1.20-rc23")
 files[main]=m.encode()
 d=files[readme].decode()
 d=replace_one(d,"Stable tag: 0.1.19-rc22","Stable tag: 0.1.20-rc23")
 files[readme]=d.encode()
 assert "hb_insurance_scope" in m
 assert "hb_amazon_category_search_fallback" in m
 assert "multiprovider_matching_offers_for_banner" in m
 for key in names:
    if key not in (trait,main,ebay,readme):assert files[key]==z.read(key),key
 buf=BytesIO()
 with ZipFile(buf,'w') as out:
    for member in z.infolist():out.writestr(member,files[member.filename])
 payload=buf.getvalue()
with ZipFile(BytesIO(payload)) as z:
 assert z.testzip() is None and len(z.namelist())==36
 assert b'0.1.20-rc23' in z.read(main)
 assert b'creatives/productdata/export' in z.read(trait)
 assert b'ppar-hb-category-products-grid' in z.read(base+"assets/frontend.css")
p.write_bytes(payload)
print('HAB_RC23_CANDIDATE',len(payload),sha(payload),'36 ZIP CRC PASS, 4 files changed, user-facing release withheld until real data end-to-end proof')
