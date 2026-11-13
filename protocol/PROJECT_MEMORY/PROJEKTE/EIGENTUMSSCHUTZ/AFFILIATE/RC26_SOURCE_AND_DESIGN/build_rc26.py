#!/usr/bin/env python3
"""HAB RC26: resolve existing two-feed selection from the REAL provider feed list;
suppress test/mock sources; preserve RC25 import; apply requested HAB-only styles.
No new database, plugin, worker, provider or front-end network calls.
"""
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from hashlib import sha256
ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=ROOT/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
old=P.read_bytes()
assert sha256(old).hexdigest()=="ee333cd180d266e468919fdc37c57ca4d96a2d9cf353d797ca2e7c31040d3793","Not verified RC25"
base="affiliate-portal-router/"
trait=base+"includes/trait-ppar-idealo.php"
main=base+"affiliate-portal-router.php"
css=base+"assets/frontend.css"
readme=base+"readme.txt"
def once(s,a,b):
    assert s.count(a)==1,("expected one anchor",s.count(a),a[:150])
    return s.replace(a,b,1)
def replace_method(s,start,after,new):
    a=s.index(start)
    b=s.index(after,a)
    return s[:a]+new+s[b:]
with ZipFile(BytesIO(old)) as z:
    assert z.testzip() is None and len(z.namelist())==36
    f={i.filename:z.read(i.filename) for i in z.infolist()}
    t=f[trait].decode("utf-8")
    feed_methods=r'''    /** Use the already existing iPN findFeeds endpoint to inspect ALL authorized
     *  feeds of exactly the saved Hab & Bewahr adspace. No key or URL is logged. */
    private function idealo_hab_available_feeds($settings) {
        if (!$this->idealo_credentials_present($settings)
            || (string)($settings['adspace_id']??'')!=='568944') {
            return new WP_Error('hb_feed_account_invalid','Hab & Bewahr: Adspace 568944 und iPN-Zugang müssen stimmen.');
        }
        $result=array();
        for ($page=0;$page<20;$page++) {
            $url=add_query_arg(array('adspaceId'=>'568944','page'=>$page,'rowsPerPage'=>100),
                $this->idealo_partner_api_base().'/creatives/productdata/findFeeds');
            $response=$this->idealo_partner_api_post($url,(string)$settings['api_key']);
            if (is_wp_error($response)) {return $response;}
            if ((int)wp_remote_retrieve_response_code($response)!==200) {
                return new WP_Error('hb_feed_list_http','iPN-Feedliste konnte nicht geladen werden.');
            }
            $data=json_decode((string)wp_remote_retrieve_body($response),true);
            if (!is_array($data) || !is_array($data['entries']??null)) {
                return new WP_Error('hb_feed_list_invalid','iPN-Feedliste hat kein gültiges Format.');
            }
            foreach ($data['entries'] as $entry) {
                if (!is_array($entry)) continue;
                $id=preg_replace('/\D+/', '',(string)($entry['feedId']??''));
                if ($id==='') continue;
                $result[$id]=array(
                    'feed_id'=>$id,
                    'name'=>sanitize_text_field((string)($entry['name']??'')),
                    'advertiser_id'=>sanitize_text_field((string)($entry['advertiserId']??'')),
                    'advertiser_name'=>sanitize_text_field((string)($entry['advertiserName']??'')),
                    'last_updated_at'=>sanitize_text_field((string)($entry['lastUpdatedAt']??'')),
                    'last_modified_at'=>sanitize_text_field((string)($entry['lastModifiedAt']??'')),
                    'number_of_products'=>absint($entry['numberOfProducts']??0),
                    'last_file_hash'=>sanitize_text_field((string)($entry['lastFileHash']??'')),
                    'update_interval'=>sanitize_text_field((string)($entry['updateInterval']??'')),
                );
            }
            if ($page+1>=max(1,absint($data['totalPages']??1))) break;
        }
        return array_values($result);
    }

    private function idealo_hab_feed_is_mock($feed) {
        return (bool)preg_match('/\b(mock|demo|test|sample|beispiel)\b/iu',(string)($feed['name']??''));
    }

    private function idealo_hab_feed_is_standard($feed) {
        return !$this->idealo_hab_feed_is_mock($feed)
            && (bool)preg_match('/\bstandard[\s_-]*(daten|data)?feed\b/iu',(string)($feed['name']??''));
    }

    /** Reset only the EXISTING provider option when switching the production source.
     *  The old staged rows stay audit-ready, but become publicly ineligible until
     *  the NEW feed is successfully imported. Do not overwrite old API credentials. */
    private function idealo_hab_clear_feed_results($settings) {
        foreach (array('feed_etag','feed_last_modified','last_remote_file_hash',
            'last_feed_hash','last_catalog_signature','last_message') as $key) $settings[$key]='';
        foreach (array('last_import_at','last_import_started_at','last_import_count',
            'last_materialized_at','last_materialized_count','last_materialized_targets',
            'last_matched_concepts','last_matched_hubs','last_feed_rows_seen') as $key) $settings[$key]=0;
        $settings['last_matched_concept_ids']=array();
        $settings['last_feed_reject_stats']=array();
        $settings['refresh_state']='idle';
        $settings['refresh_last_message']='Andere Feedquelle gewählt: erst den echten Standarddatenfeed importieren.';
        return $settings;
    }

    private function idealo_find_feed_metadata($settings = null) {
        $settings=is_array($settings)?$settings:$this->idealo_settings();
        $feeds=$this->idealo_hab_available_feeds($settings);
        if (is_wp_error($feeds)) return $feeds;
        foreach ($feeds as $feed) {
            if ((string)$feed['feed_id']!==(string)($settings['feed_id']??'')) continue;
            if ($this->idealo_hab_feed_is_mock($feed)) {
                return new WP_Error('hb_mock_feed_forbidden','Der ausgewählte iPN-Mock-/Testfeed darf nicht öffentlich importiert werden.');
            }
            return $feed;
        }
        return new WP_Error('hb_feed_not_found','Die eingestellte Feed-ID ist für Hab & Bewahr nicht freigegeben.');
    }
'''
    t=replace_method(t,"    private function idealo_find_feed_metadata($settings = null) {",
                     "    /**\n     * Canonical portal product supply contract.",feed_methods)
    test_method=r'''    public function idealo_provider_access_test($handled,$provider,$contract_version) {
        if ($provider!=='idealo') return $handled;
        $settings=$this->idealo_settings();
        $feeds=$this->idealo_hab_available_feeds($settings);
        if (is_wp_error($feeds)) {
            $this->provider_set_access_state('idealo','failed',$feeds->get_error_message());
            return $feeds;
        }
        $safe=array(); $standards=array(); $selected=null;
        foreach ($feeds as $entry) {
            $mock=$this->idealo_hab_feed_is_mock($entry);
            $id=(string)$entry['feed_id'];
            $safe[]=array('feed_id'=>$id,'name'=>(string)$entry['name'],
                'number_of_products'=>absint($entry['number_of_products']),
                'mock'=>$mock);
            if ($this->idealo_hab_feed_is_standard($entry)) $standards[]=$entry;
            if ($id===(string)($settings['feed_id']??'') && !$mock) $selected=$entry;
        }
        // A unique explicitly named production Standard feed wins over old
        // hardcoded 2901. No guesses when two production feeds are ambiguous.
        if (count($standards)===1) $selected=$standards[0];
        $settings['api_feed_inventory']=$safe; // existing WordPress option
        if (!$selected) {
            update_option(self::OPTION_NETWORK_IDEALO,$settings,false);
            $error=new WP_Error('hb_no_production_feed',
                'Kein eindeutig freigegebener Standarddatenfeed gewählt. Verfügbare Feeds prüfen; Mock/Test ausgeschlossen.');
            $this->provider_set_access_state('idealo','failed',$error->get_error_message());
            return $error;
        }
        if ((string)($settings['feed_id']??'')!==(string)$selected['feed_id']) {
            $settings=$this->idealo_hab_clear_feed_results($settings);
            $settings['feed_id']=(string)$selected['feed_id'];
            $settings['feed_url']=''; // the existing direct iPN export uses exact feedId
        }
        $settings['api_last_checked_at']=time();
        $settings['api_last_feed_hash']=(string)$selected['last_file_hash'];
        $settings['api_last_updated_at']=(string)$selected['last_updated_at'];
        $settings['api_last_product_count']=absint($selected['number_of_products']);
        $settings['api_last_advertiser_name']=(string)$selected['advertiser_name'];
        $settings['api_last_feed_name']=(string)$selected['name'];
        $settings['api_last_message']='Partner-API PASS: Standardfeed '.(string)$selected['feed_id'].' geprüft.';
        update_option(self::OPTION_NETWORK_IDEALO,$settings,false);
        $message='iPN: '.(string)$selected['name'].' – Feed '.(string)$selected['feed_id'].
            ', '.absint($selected['number_of_products']).' Produkte (Adspace 568944). Mock/Test nicht importiert.';
        $this->provider_set_access_state('idealo','connected',$message);
        return array('status'=>'connected','message'=>$message,'metadata'=>$selected);
    }
'''
    t=replace_method(t,"    public function idealo_provider_access_test($handled, $provider, $contract_version) {",
                      "    private function idealo_validate_feed_url($url) {",test_method)
    a_save=t.index("    public function idealo_provider_access_save(")
    a_id=t.index("        $settings['feed_id']",a_save)
    b_id=t.index("\n",a_id)
    print('HAB_RC25_ORIGINAL_FEED_SAVE',t[a_id:b_id].strip())
    t=t[:a_id]+r'''        // Only a previously verified NON-mock production feed can be selected.
        $requested=preg_replace('/\D+/', '',(string)($raw['feed_id']??''));
        $verified=array();
        foreach ((array)($old['api_feed_inventory']??array()) as $entry) {
            if (!is_array($entry)||!empty($entry['mock'])) continue;
            $verified[(string)($entry['feed_id']??'')]=true;
        }
        if ($requested!=='' && isset($verified[$requested]) && $requested!==(string)($old['feed_id']??'')) {
            $settings=$this->idealo_hab_clear_feed_results($settings);
            $settings['feed_id']=$requested;
            $settings['feed_url']='';
            $settings['api_last_checked_at']=0;
        }'''+t[b_id:]
    field_anchor='<p><strong>Feed-ID:</strong> <code>2901</code><input type="hidden" name="ppar_provider[idealo][feed_id]" value="2901"> <span class="description">Gebundener Standardfeed; portalweiter Superset-Feed.</span></p>'
    i_field=t.find('name="ppar_provider[idealo][feed_id]"')
    print('HAB_RC25_ACTUAL_FEED_FIELD',t[max(0,i_field-260):i_field+310] if i_field>=0 else 'not in plugin')
    if field_anchor in t:
        t=once(t,field_anchor,
        r'''<p><label>Produktfeed aus geprüftem iPN-Konto<br><select name="ppar_provider[idealo][feed_id]">
            <?php $has_feed=false; foreach ((array)($s['api_feed_inventory']??array()) as $entry): if (!is_array($entry)||!empty($entry['mock'])) continue; $has_feed=true; ?>
            <option value="<?php echo esc_attr((string)$entry['feed_id']); ?>" <?php selected((string)$s['feed_id'],(string)$entry['feed_id']); ?>><?php echo esc_html((string)$entry['name'].' · Feed '.(string)$entry['feed_id'].' · '.absint($entry['number_of_products']).' Produkte'); ?></option>
            <?php endforeach; if (!$has_feed): ?><option value="<?php echo esc_attr((string)$s['feed_id']); ?>">Vorhandener Feed <?php echo esc_html((string)$s['feed_id']); ?> – API-Prüfung ausführen</option><?php endif; ?>
            </select></label><span class="description">Mock-/Testfeeds werden niemals für die öffentliche Produktwerbung angeboten. Bei einem eindeutig benannten Standardfeed erfolgt die Auswahl automatisch nach API-Prüfung.</span></p>''')
    # The confirmed official direct API export (already used successfully by RC23)
    # wins over any old manually stored download URL. This prevents importing
    # the OTHER feed after a source switch.
    t=once(t,
        "        $manual=trim((string)($settings['feed_url'] ?? ''));\n        if ($manual!=='') { return $this->idealo_validate_feed_url($manual); }",
        "        // Hab always downloads the exact approved feedId through the existing iPN export.\n        // An older manually saved URL must not silently import a different feed.")
    if 'Offizielle iPN-Download-URL für Feed 2901 <span' in t:
        t=once(t,
        'Offizielle iPN-Download-URL für Feed 2901 <span',
        'Optionale frühere Download-URL (wird nicht mehr zum Import verwendet) <span')
    t=once(t,
        '<section class="postbox" style="padding:18px"><h2>Partner-API</h2><p>',
        '<section class="postbox" style="padding:18px"><h2>Partner-API</h2><p><strong>Produktquelle:</strong> <?php echo esc_html((string)($s[\'api_last_feed_name\']??\'noch nicht geprüft\')); ?> · Feed <?php echo esc_html((string)($s[\'feed_id\']??\'\')); ?><br>')
    t=once(t,
        '<section class="postbox" style="padding:18px;margin-top:18px;max-width:900px"><h2>Feed-Test / Fallback</h2>',
        r'''<section class="postbox" style="padding:18px;margin-top:18px;max-width:900px">
          <h2>iPN-Feedvergleich – überprüfte Quellen</h2>
          <p>Nur Feeds, die die Partner-API für die Hab-&-Bewahr-Werbefläche gemeldet hat. Keine Schätzungen aus dem Idealo-Gesamtsortiment.</p>
          <?php foreach ((array)($s['api_feed_inventory']??array()) as $entry): if (!is_array($entry)) continue; ?>
          <p><strong><?php echo esc_html((string)$entry['name']); ?></strong> · Feed <?php echo esc_html((string)$entry['feed_id']); ?>
          · <?php echo absint($entry['number_of_products']); ?> Produkte
          · <?php echo !empty($entry['mock'])?'TEST – ausgeschlossen':((string)$entry['feed_id']===(string)$s['feed_id']?'PRODUKTIV GEWÄHLT':'nicht gewählt'); ?></p>
          <?php endforeach; ?>
          <?php if (empty($s['api_feed_inventory'])): ?><p>Noch keine vollständige Feedliste geprüft. Unter Anbieter & APIs einmal „Speichern & API prüfen“ ausführen.</p><?php endif; ?>
        </section>
        <section class="postbox" style="padding:18px;margin-top:18px;max-width:900px"><h2>Feed-Test / Fallback</h2>''')
    if 'Produktiv ist Feed 2901 für den serverseitigen Stream-Abruf vorgesehen.' in t:
        t=once(t,'Produktiv ist Feed 2901 für den serverseitigen Stream-Abruf vorgesehen.',
                 'Produktiv wird ausschließlich der in der Partner-API verifizierte Standardfeed für den serverseitigen Stream-Abruf verwendet.')
    f[trait]=t.encode("utf8")
    m=f[main].decode("utf8")
    m=once(m,"Version: 0.1.22-rc25","Version: 0.1.23-rc26")
    m=once(m,"border:1px solid #d2dbd5!important;overflow:hidden!important",
           "border:0!important;overflow:visible!important")
    f[main]=m.encode("utf8")
    st=f[css].decode("utf8")
    st=once(st,
        ".ppar-hb-category-products-grid > .ppar-affiliate-slot {\n  border:1px solid #d2dbd5!important;",
        ".ppar-hb-category-products-grid > .ppar-affiliate-slot {\n  border:0!important;")
    st+=r'''

/* HAB RC26 only: user-approved frameless product cards and branded buttons.
   Verified portal palette: terracotta #B35C40, ivory/beige #FAF8F4.
   No rules for other portals or insurance banners. */
.ppar-hb-category-products-grid > .ppar-affiliate-slot {
  border:0!important;
  outline:0!important;
  box-shadow:none!important;
}
.ppar-hb-category-products-grid .ppar-banner-button,
.ppar-hb-category-products-grid .ppar-banner-offer-button {
  border:1px solid #B35C40!important;
  border-radius:1px!important;
  background:#FAF8F4!important;
  color:#B35C40!important;
  box-shadow:none!important;
}
.ppar-hb-category-products-grid .ppar-banner-button:hover,
.ppar-hb-category-products-grid .ppar-banner-offer-button:hover,
.ppar-hb-category-products-grid .ppar-banner-button:focus-visible,
.ppar-hb-category-products-grid .ppar-banner-offer-button:focus-visible {
  background:#EFE5DA!important;
  color:#B35C40!important;
  border-color:#B35C40!important;
}
@media(max-width:640px) {
  .ppar-hb-category-products-grid {
    margin-bottom:32px!important;
  }
}
'''
    f[css]=st.encode("utf8")
    rd=f[readme].decode("utf8")
    rd=once(rd,"Stable tag: 0.1.22-rc25","Stable tag: 0.1.23-rc26")
    f[readme]=rd.encode("utf8")
    touched={trait,main,css,readme}
    assert all(f[name]==z.read(name) for name in z.namelist() if name not in touched)
    dest=BytesIO()
    with ZipFile(dest,"w") as out:
        for item in z.infolist():
            out.writestr(item,f[item.filename])
    blob=dest.getvalue()
with ZipFile(BytesIO(blob)) as check:
    assert check.testzip() is None and len(check.namelist())==36
    a=check.read(trait)
    assert b"idealo_hab_available_feeds" in a and b"hb_mock_feed_forbidden" in a
    assert b"last_catalog_signature" in a and b"Version: 0.1.23-rc26" in check.read(main)
P.write_bytes(blob)
print("HAB_RC26_BUILD_PASS",len(blob),sha256(blob).hexdigest(),"changed",sorted(touched))
