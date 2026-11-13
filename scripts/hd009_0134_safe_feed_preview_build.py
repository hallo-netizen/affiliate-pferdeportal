#!/usr/bin/env python3
"""HD009 0.1.34 – safe read-only preview of alternative idealo feed 2901.
Patch exact existing 0.1.33, retain whole plugin, no edit to production settings.
"""
from pathlib import Path
from zipfile import ZipFile
import hashlib,io,sys

root=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE")
original=root/"CURRENT.zip"
out=Path(sys.argv[1] if len(sys.argv)>1 else "/tmp/HD009_0.1.34_SAFE_FEED_PREVIEW.zip")
expected="b6482b5d880e941c97ac726dffa85fbc46ba8514587e23700951d176ebcb63db"
def sha(s):return hashlib.sha256(s).hexdigest()
assert sha(original.read_bytes())==expected, "Abort: HD009 0.1.33 source changed"
trait_name="affiliate-portal-router/includes/trait-ppar-idealo.php"
main_name="affiliate-portal-router/hobby-depot-affiliate-router.php"
with ZipFile(original) as z:
    assert len(z.namelist())==41 and z.testzip() is None
    infos=z.infolist()
    files={f.filename:z.read(f.filename) for f in infos}
    trait=files[trait_name].decode("utf8")
    main=files[main_name].decode("utf8")

def only(s, old, new, label):
    num=s.count(old)
    assert num==1,f"{label}: expected 1 anchor, found {num}"
    return s.replace(old,new,1)

newconst="""    const HD_IDEALO_PREVIEW_OPTION = 'ppar_hd009_feed_preview_v1';
    const HD_IDEALO_PREVIEW_TOKEN = 'ppar_hd009_feed_preview_token_v1';
    const HD_IDEALO_PREVIEW_LOCK = 'ppar_hd009_feed_preview_lock_v1';

"""
trait=only(trait,
"    public function idealo_register_hooks() {",
newconst+"    public function idealo_register_hooks() {",
"constants")
trait=only(trait,
"        if (!$is_ajax_request) { add_action('admin_post_ppar_idealo_import_file', array($this, 'handle_idealo_import_file')); }",
"""        if (!$is_ajax_request) { add_action('admin_post_ppar_idealo_import_file', array($this, 'handle_idealo_import_file')); }
        if (!$is_ajax_request) {
            add_action('admin_post_ppar_hd009_preview_standard', array($this, 'hd_idealo_start_standard_preview'));
            add_action('admin_post_ppar_hd009_preview_worker', array($this, 'hd_idealo_process_standard_preview'));
            add_action('admin_post_nopriv_ppar_hd009_preview_worker', array($this, 'hd_idealo_process_standard_preview'));
        }""",
"admin-only handlers")

methods=r'''
    /**
     * Read-only preview of standard feed 2901. Nothing here edits the live
     * idealo settings, staged feed rows, materialized campaigns, output mode,
     * Amazon/DataForSEO, eBay, or the hobby category registry.
     *
     * The alternative feed is verified for this SAME adspace via findFeeds
     * before its CSV.GZ is fetched. Read-only report stored in one WP option.
     */
    private function hd_idealo_preview_save($data) {
        $safe = is_array($data) ? $data : array();
        $safe['updated_at'] = time();
        update_option(self::HD_IDEALO_PREVIEW_OPTION, $safe, false);
    }

    private function hd_idealo_preview_current() {
        $state = get_option(self::HD_IDEALO_PREVIEW_OPTION, array());
        return is_array($state) ? $state : array();
    }

    private function hd_idealo_preview_allowed($settings) {
        if (!$this->hd_idealo_feed_source_ready($settings)) { return false; }
        // Only compare against the validated, successful 2747 baseline.
        if ((string)($settings['feed_id']??'') !== '2747'
            || (string)($settings['last_import_feed_id']??'') !== '2747'
            || (string)($settings['last_import_adspace_id']??'') !== '568912'
            || absint($settings['last_import_at']??0) <= 0) { return false; }
        $refresh = sanitize_key((string)($settings['refresh_state']??''));
        if (in_array($refresh,array('running','queued'),true)
            || get_transient(self::IDEALO_REFRESH_LOCK)) { return false; }
        return true;
    }

    /** Reuse the *exact* HD009 matcher without writing a single feed row. */
    private function hd_idealo_preview_csv($path) {
        if (!is_file($path)) { return new WP_Error('hd009_preview_no_file','Vergleichsfeed nicht verfügbar.'); }
        $fh = $this->idealo_open_feed_stream($path);
        if (is_wp_error($fh)) { return $fh; }
        $header = fgetcsv($fh,0,',','"','\\');
        if (!is_array($header)) { $this->idealo_stream_close($fh); return new WP_Error('hd009_preview_headers','Feed-Kopfzeile fehlt.'); }
        if (isset($header[0])) { $header[0] = preg_replace('/^\xEF\xBB\xBF/','',(string)$header[0]); }
        $header = array_map('trim',$header);
        $required = array('id','product_title','product_deeplink','ean','gtins_product','asins_product','main_category','sub_category','brand_name');
        $missing = array_diff($required,$header);
        $image_field = in_array('image_url',$header,true) ? 'image_url' : (in_array('image_url_1',$header,true) ? 'image_url_1' : '');
        if ($image_field==='') { $missing[]='image_url|image_url_1'; }
        if ($missing) { $this->idealo_stream_close($fh); return new WP_Error('hd009_preview_columns','Der Vergleichsfeed hat andere Pflichtspalten: '.implode(', ',$missing)); }
        $mi = $this->idealo_match_index();
        if (is_wp_error($mi)) { $this->idealo_stream_close($fh); return $mi; }
        $stats=array('seen'=>0,'matching_rows'=>0,'bad_rows'=>0,'missing_identity'=>0,
            'no_image'=>0,'no_match'=>0,'ambiguous'=>0,'context_rejected'=>0,
            'concept_ids'=>array(),'hobby_families'=>array());
        while (($values=fgetcsv($fh,0,',','"','\\'))!==false) {
            $stats['seen']++;
            if (count($values)!==count($header)) { $stats['bad_rows']++; continue; }
            $row=array_combine($header,$values);
            if (!is_array($row) || trim((string)($row['product_title']??''))===''
                || trim((string)($row['product_deeplink']??''))===''
                || trim((string)($row[$image_field]??''))==='') { $stats['missing_identity']++; continue; }
            if (!$this->idealo_normalize_gtins_from_values(array($row['ean']??'',$row['gtins_product']??''))) {
                $stats['missing_identity']++; continue;
            }
            $match=$this->idealo_match_feed_row_to_concept($row);
            if (is_wp_error($match)) { $this->idealo_stream_close($fh); return $match; }
            $status=(string)($match['status']??'none');
            if ($status==='ambiguous') { $stats['ambiguous']++; continue; }
            if ($status==='context_rejected') { $stats['context_rejected']++; continue; }
            if ($status!=='matched' || !is_array($match['concept']??null)) { $stats['no_match']++; continue; }
            if ($this->idealo_direct_image_url((string)$row[$image_field])==='') {
                $stats['no_image']++; continue;
            }
            $concept=$match['concept'];
            $id=sanitize_key((string)($concept['id']??''));
            if ($id==='') { $stats['no_match']++; continue; }
            $stats['matching_rows']++;
            $stats['concept_ids'][$id]=true;
            $family=(string)($concept['main_hub']??'').'|'.(string)($concept['hub']??'');
            if (trim($family,'|')!=='') { $stats['hobby_families'][$family]=true; }
        }
        $this->idealo_stream_close($fh);
        if (!$stats['seen']) { return new WP_Error('hd009_preview_empty','Der Vergleichsfeed enthält keine Produkte.'); }
        $stats['matched_concepts']=count($stats['concept_ids']);
        $stats['matched_families']=count($stats['hobby_families']);
        unset($stats['hobby_families']);
        return $stats;
    }

    /** Baseline is read with SELECT only; no staged/product writes. */
    private function hd_idealo_preview_existing_concepts($settings) {
        global $wpdb;
        $table=$this->network_sync_table('products');
        $started=absint($settings['last_import_started_at']??0);
        if ($started<=0) { return new WP_Error('hd009_preview_no_baseline','Kein vollständiger 2747-Import bekannt.'); }
        $sql=$wpdb->prepare("SELECT DISTINCT category FROM {$table} WHERE network=%s AND quality_status=%s AND last_seen >= %d",
            'idealo','pass',$started);
        $ids=(array)$wpdb->get_col($sql);
        $map=$this->idealo_match_index();
        if (is_wp_error($map)) { return $map; }
        $out=array();
        foreach ($ids as $id) {
            $id=sanitize_key((string)$id);
            if ($id!=='' && isset($map['concepts'][$id])) { $out[$id]=true; }
        }
        return $out;
    }

    /** Heavy work exclusively on private, independently dispatched admin worker. */
    private function hd_idealo_standard_feed_compare_work() {
        $before=$this->idealo_settings();
        if (!$this->hd_idealo_preview_allowed($before)) {
            return new WP_Error('hd009_preview_baseline_changed','2747-Import ist nicht stabil oder seine Freigabe fehlt.');
        }
        $baseline=$this->hd_idealo_preview_existing_concepts($before);
        if (is_wp_error($baseline)) { return $baseline; }
        $other=$before;
        $other['feed_id']='2901';
        $other['feed_url']='';  // NEVER reuse 2747 download URL.
        $other['feed_etag']=''; $other['feed_last_modified']='';  // NEVER share feed's 304 cache.
        $metadata=$this->idealo_find_feed_metadata($other);
        if (is_wp_error($metadata)) { return $metadata; } // Must be authorized for same 568912.
        if ((string)($metadata['feed_id']??'')!=='2901') {
            return new WP_Error('hd009_preview_wrong_feed','Antwort gehört nicht zu Standardfeed 2901.');
        }
        $download=$this->idealo_download_feed_to_temp($other);
        if (is_wp_error($download)) { return $download; }
        if (($download['status']??'')!=='downloaded' || empty($download['path'])) {
            return new WP_Error('hd009_preview_not_downloaded','Standardfeed konnte nicht erneut abgerufen werden.');
        }
        $path=(string)$download['path'];
        try { $preview=$this->hd_idealo_preview_csv($path); }
        finally { @unlink($path); }
        if (is_wp_error($preview)) { return $preview; }
        $after=$this->idealo_settings();
        if ((string)($after['feed_id']??'')!=='2747' ||
            absint($after['last_import_at']??0)!==absint($before['last_import_at']??0)) {
            return new WP_Error('hd009_preview_baseline_changed','2747-Bestand wurde während der Prüfung verändert; bitte Ergebnis nicht verwenden.');
        }
        $concepts=$preview['concept_ids'];
        $new=array_diff_key($concepts,$baseline);
        $lost=array_diff_key($baseline,$concepts);
        $catalog=$this->idealo_match_index();
        if (is_wp_error($catalog)) { return $catalog; }
        $label=function($ids) use ($catalog) {
            $out=array();
            foreach (array_keys($ids) as $id) {
                $out[]=sanitize_text_field((string)($catalog['concepts'][$id]['title']??$id));
            }
            sort($out,SORT_NATURAL|SORT_FLAG_CASE);
            return $out;
        };
        return array(
            'status'=>'success','current_feed'=>'2747','compared_feed'=>'2901',
            'baseline_at'=>absint($before['last_import_at']??0),
            'baseline_matched'=>count($baseline),
            'standard_2901_matched'=>$preview['matched_concepts'],
            'standard_2901_rows'=>$preview['matching_rows'],
            'standard_2901_feed_rows'=>$preview['seen'],
            'standard_2901_api_products'=>absint($metadata['number_of_products']??0),
            'standard_2901_hobby_families'=>$preview['matched_families'],
            'both_covered'=>count(array_intersect_key($baseline,$concepts)),
            'only_2747'=>count($lost),'only_2901'=>count($new),
            'total_union'=>count($baseline)+count($new),
            'new_hobbies'=>$label($new),
            'lost_hobbies'=>$label($lost),
            'parser'=>array(
                'malformed'=>$preview['bad_rows'],'no_identity'=>$preview['missing_identity'],
                'no_image'=>$preview['no_image'],'not_matched'=>$preview['no_match'],
                'ambiguous'=>$preview['ambiguous'],'context_rejected'=>$preview['context_rejected']),
            'message'=>'Lesender Vergleich abgeschlossen; bestehender Produktbestand, Feed-ID und Anzeigen wurden nicht geändert.',
        );
    }

    public function hd_idealo_start_standard_preview() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_hd009_preview_standard','hd009_preview_nonce');
        $s=$this->idealo_settings();
        if (!$this->hd_idealo_preview_allowed($s)) {
            $this->hd_idealo_preview_save(array('status'=>'blocked','message'=>'Erst muss der bisherige Feed 2747 vollständig importiert sein und darf nicht gerade aktualisiert werden.'));
        } elseif (get_transient(self::HD_IDEALO_PREVIEW_LOCK)) {
            $this->hd_idealo_preview_save(array('status'=>'running','message'=>'Ein Feedvergleich läuft bereits.'));
        } else {
            $token=wp_generate_password(48,false,false);
            set_transient(self::HD_IDEALO_PREVIEW_TOKEN,hash('sha256',$token),20*MINUTE_IN_SECONDS);
            set_transient(self::HD_IDEALO_PREVIEW_LOCK,'queued',60*MINUTE_IN_SECONDS);
            $this->hd_idealo_preview_save(array('status'=>'running','started_at'=>time(),'message'=>'Standardfeed 2901 wird ohne Datenbankimport geprüft.'));
            $response=wp_remote_post(admin_url('admin-post.php'),array(
                'timeout'=>1,'blocking'=>false,'redirection'=>0,
                'sslverify'=>apply_filters('https_local_ssl_verify',false),
                'headers'=>array('Cache-Control'=>'no-cache'),
                'body'=>array('action'=>'ppar_hd009_preview_worker','token'=>$token),
                'user-agent'=>'Affiliate-Zentrale/'.self::VERSION.'; '.home_url('/'),
            ));
            if (is_wp_error($response)) {
                delete_transient(self::HD_IDEALO_PREVIEW_LOCK);
                delete_transient(self::HD_IDEALO_PREVIEW_TOKEN);
                $this->hd_idealo_preview_save(array('status'=>'failed','message'=>'Hintergrundstart nicht erreichbar: '.$response->get_error_message()));
            }
        }
        wp_safe_redirect(admin_url('admin.php?page=affiliate-portal-provider-idealo'));
        exit;
    }

    public function hd_idealo_process_standard_preview() {
        $token=isset($_POST['token'])?(string)wp_unslash($_POST['token']):'';
        $hash=get_transient(self::HD_IDEALO_PREVIEW_TOKEN);
        if (!is_string($hash) || $hash==='' || $token==='' || !hash_equals($hash,hash('sha256',$token))) {
            if (function_exists('status_header')) { status_header(403); }
            exit;
        }
        delete_transient(self::HD_IDEALO_PREVIEW_TOKEN);
        if (!get_transient(self::HD_IDEALO_PREVIEW_LOCK)) {
            if (function_exists('status_header')) { status_header(409); }
            exit;
        }
        @set_time_limit(0);
        if (function_exists('ignore_user_abort')) { @ignore_user_abort(true); }
        $completed=false;
        register_shutdown_function(function() use (&$completed) {
            if ($completed) { return; }
            $last=error_get_last();
            if (!is_array($last) || !in_array((int)($last['type']??0),array(E_ERROR,E_PARSE,E_CORE_ERROR,E_COMPILE_ERROR,E_USER_ERROR),true)) { return; }
            delete_transient(self::HD_IDEALO_PREVIEW_LOCK);
            $this->hd_idealo_preview_save(array('status'=>'failed','message'=>'Feedvergleich durch einen PHP-Fehler abgebrochen. Der bestehende Produktbestand bleibt unverändert.'));
        });
        try {
            $r=$this->hd_idealo_standard_feed_compare_work();
            if (is_wp_error($r)) { $r=array('status'=>'failed','message'=>$r->get_error_message()); }
            $this->hd_idealo_preview_save($r);
        } catch (Throwable $e) {
            $this->hd_idealo_preview_save(array('status'=>'failed','message'=>'Feedvergleich abgebrochen: '.sanitize_text_field($e->getMessage())));
        } finally {
            $completed=true;
            delete_transient(self::HD_IDEALO_PREVIEW_LOCK);
        }
        if (function_exists('status_header')) { status_header(204); }
        exit;
    }

    public function hd_idealo_render_feed_preview() {
        $s=$this->idealo_settings();
        $state=$this->hd_idealo_preview_current();
        $status=sanitize_key((string)($state['status']??'not_started'));
        ?>
        <section class="postbox" style="padding:18px;margin-top:18px;max-width:900px">
          <h2>Idealo-Feeds vergleichen – ohne Import</h2>
          <p>Vorhandener Feed 2747 bleibt aktiv. Standardfeed 2901 wird mit derselben Hobby-Zuordnung nur geprüft: keine neuen Produktkarten, kein Wechsel der Feed-ID, keine Veränderung an eBay oder Amazon.</p>
          <p><strong>Vergleich:</strong> <?php echo esc_html($status); ?>
          <?php if (!empty($state['updated_at'])) { echo ' · '.esc_html(wp_date('d.m.Y H:i',(int)$state['updated_at'])); } ?>
          <?php if (!empty($state['message'])) { echo '<br>'.esc_html((string)$state['message']); } ?></p>
          <?php if ($status==='running' && !empty($state['started_at']) && (time()-absint($state['started_at']))>3600): ?>
            <p><strong>Hinweis:</strong> Der Hintergrundvergleich antwortet seit über 60 Minuten nicht. Der Produktbestand wurde nicht geändert.</p>
          <?php endif; ?>
          <?php if ($status==='success'): ?>
            <p><strong>2747 – bisher versorgte Hobbys:</strong> <?php echo absint($state['baseline_matched']??0); ?><br>
            <strong>2901 – nach denselben Regeln passende Hobbys:</strong> <?php echo absint($state['standard_2901_matched']??0); ?><br>
            <strong>Nur durch 2901 zusätzlich:</strong> <?php echo absint($state['only_2901']??0); ?><br>
            <strong>Nur durch 2747:</strong> <?php echo absint($state['only_2747']??0); ?><br>
            <strong>Gemeinsam versorgt:</strong> <?php echo absint($state['both_covered']??0); ?><br>
            <strong>Zusammen insgesamt:</strong> <?php echo absint($state['total_union']??0); ?><br>
            <strong>Passende Standardfeed-Produktzeilen:</strong> <?php echo absint($state['standard_2901_rows']??0); ?></p>
            <?php if (!empty($state['new_hobbies'])): ?>
              <details><summary>Zusätzlich passende Hobbys aus 2901</summary><p><?php echo esc_html(implode(' · ',array_slice((array)$state['new_hobbies'],0,120))); ?></p></details>
            <?php endif; ?>
            <?php if (!empty($state['lost_hobbies'])): ?>
              <details><summary>Hobbys, die beim reinen Wechsel verloren gingen</summary><p><?php echo esc_html(implode(' · ',array_slice((array)$state['lost_hobbies'],0,120))); ?></p></details>
            <?php endif; ?>
          <?php endif; ?>
          <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
            <input type="hidden" name="action" value="ppar_hd009_preview_standard">
            <?php wp_nonce_field('ppar_hd009_preview_standard','hd009_preview_nonce'); ?>
            <button class="button button-secondary" <?php disabled($status==='running' && !empty($state['started_at']) && (time()-absint($state['started_at']))<3600); ?>>Standardfeed 2901 gefahrlos vergleichen</button>
          </form>
        </section><?php
    }

'''
trait=only(trait,
"    public function idealo_render_sync_card($provider,$definition,$contract_version) {",
methods+"    public function idealo_render_sync_card($provider,$definition,$contract_version) {",
"add isolated read-only comparison methods")
trait=only(trait,
'        </div>\n        <section class="postbox" style="padding:18px;margin-top:18px;max-width:900px"><h2>Feed-Test / Fallback</h2>',
'        </div>\n        <?php $this->hd_idealo_render_feed_preview(); ?>\n        <section class="postbox" style="padding:18px;margin-top:18px;max-width:900px"><h2>Feed-Test / Fallback</h2>',
"render comparison within existing provider specialist")
assert "private function idealo_import_feed_file" in trait and "private function idealo_materialize_campaigns" in trait
# Strong static isolation: preview code may read remote CSV & SELECT only; never publish.
fragment=trait[trait.index("    private function hd_idealo_preview_save"):trait.index("    public function idealo_render_sync_card(")]
for forbidden in ["network_sync_upsert_products(","save_campaign_record(","idealo_materialize_campaigns(","delete_posts(","wp_insert_post(","update_post_meta(","self::OPTION_NETWORK_IDEALO,"]:
    assert forbidden not in fragment, f"Illegal write in preview: {forbidden}"
assert "SELECT DISTINCT category" in fragment
assert "idealo_find_feed_metadata($other)" in fragment
assert "idealo_download_feed_to_temp($other)" in fragment
assert "$other['feed_id']='2901'" in fragment
assert "$other['feed_etag']=''" in fragment
assert "$other['feed_url']=''" in fragment
assert "hd_idealo_preview_csv($path)" in fragment
assert "idealo_match_feed_row_to_concept($row)" in fragment

assert main.count("0.1.33") >= 1
main=main.replace("0.1.33","0.1.34")
files[trait_name]=trait.encode('utf8')
files[main_name]=main.encode('utf8')
with ZipFile(original) as z:
    diff=[n for n in files if files[n]!=z.read(n)]
    assert set(diff)=={trait_name,main_name},diff
result=io.BytesIO()
with ZipFile(result,"w") as w:
    for info in infos: w.writestr(info,files[info.filename])
blob=result.getvalue()
with ZipFile(io.BytesIO(blob)) as z:
    assert z.testzip() is None and len(z.namelist())==41
    assert b"Version: 0.1.34" in z.read(main_name)
out.parent.mkdir(parents=True,exist_ok=True)
out.write_bytes(blob)
print("BUILD_SHA",sha(blob),"BYTES",len(blob),"ORIGINAL_SHA",expected)
print("DIFF_ONLY",diff)
print("FULL_PLUGIN_FILES",len(infos),"PREVIEW_READ_ONLY_GUARDS_PASS")
