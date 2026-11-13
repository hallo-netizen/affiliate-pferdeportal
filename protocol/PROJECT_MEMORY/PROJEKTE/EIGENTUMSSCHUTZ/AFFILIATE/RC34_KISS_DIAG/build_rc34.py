#!/usr/bin/env python3
"""RC34: genuine KISS root fix, not another insurance policy.
One existing partner identity method; no second banner target writer;
same reconciling admin worker (max 60) sees all actual Tarifcheck originals;
live per-original published/error report on EXISTING Creative Library page.
Zero new table, worker, schedule, app, design, source feed, new routing concept.
"""
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from hashlib import sha256
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
zip_path=root/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
raw=zip_path.read_bytes()
assert sha256(raw).hexdigest()=="b07f9dbde9267bbfa9764e36ed92787d52c96881e306e0409784e5a1ca83f51a","Require exact green RC33 baseline"
B="affiliate-portal-router/"
output=B+"includes/trait-ppar-output-objects.php"
creative=B+"includes/trait-ppar-creative-library.php"
main=B+"affiliate-portal-router.php"
readme=B+"readme.txt"
def one(src, old, new):
    n=src.count(old)
    assert n==1,("unexpected source, patch MUST not guess",n,old[:180])
    return src.replace(old,new,1)
with ZipFile(BytesIO(raw)) as original:
    assert original.testzip() is None and len(original.namelist())==36
    files={inf.filename:original.read(inf.filename) for inf in original.infolist()}
    o=files[output].decode()
    # One existing source of truth for identifying Tarifcheck/CHECK24.
    # Historic direct partner IDs are strong explicit evidence; human labels
    # and real offer destinations remain supported. Do NOT trust tracking hosts.
    o=one(o,
      """        $partner = $this->output_text((string)($row['partner_name'] ?? ''));
        $destination = esc_url_raw((string)($row['destination_url'] ?? ''));""",
      """        $partner = $this->output_text((string)($row['partner_name'] ?? ''));
        $verified_partner_id=sanitize_key((string)($row['partner_external_id']??''));
        $provider=sanitize_key((string)($row['provider']??''));
        // A registered direct-provider ID is stronger than free-form display
        // labels (some old records are named "Tarifcheck DE" or "TC").
        if(in_array($provider,array('direct','manual'),true)) {
            if($verified_partner_id==='tarifcheck')return 'tarifcheck';
            if($verified_partner_id==='check24')return 'check24';
        }
        $destination = esc_url_raw((string)($row['destination_url'] ?? ''));""")
    # Remove all duplicate writers for an ALREADY STORED canonical banner
    # mapping; only the importer owns its topic_targets. Leave non-stored
    # first-time fallback behavior as the user already had it.
    o=one(o,
        """        if(in_array($source,array('hab_insurance_specific_verified',
                                  'hab_insurance_general_verified'),true)) return;""",
        """        if(in_array($source,array(
            'hab_insurance_specific_verified','hab_insurance_general_verified',
            'creative_library_destination_map','creative_library_general_fallback',
            'tarifcheck_insurance_all_insurance_categories',
            'check24_insurance_all_insurance_categories',
            'tarifcheck_credit_all_cost_categories',
            'check24_credit_all_cost_categories',
        ),true)) return;""")
    # Fix the *existing*, same owner migration. No second job. The old exact
    # partner-name SQL skipped genuine originals labelled "Tarifcheck DE";
    # and after marking complete it would NEVER revisit them.
    o=one(o,
       """        $option='ppar_hab_rc33_tarifcheck_reconcile_v1';""",
       """        $option='ppar_hab_rc34_tarifcheck_reconcile_v1';""")
    o=one(o,
       """"AND (partner_external_id=%s OR LOWER(partner_name)=%s) ".
            "ORDER BY id ASC LIMIT 60", $cursor,'tarifcheck','tarifcheck');""",
       """"AND (partner_external_id=%s OR LOWER(partner_name) LIKE %s ".
            "OR LOWER(destination_url) LIKE %s) ".
            "ORDER BY id ASC LIMIT 60", $cursor,'tarifcheck','%tarifcheck%','%tarifcheck.de%');""")
    o=one(o,
       """            $cursor=max($cursor,absint($row['id']??0));
            $payload=json_decode((string)($row['payload']??''),true);""",
       """            $cursor=max($cursor,absint($row['id']??0));
            // Use THE SAME owner identity as normal import and front-end;
            // the broad SQL shortlist alone is never a partner decision.
            if($this->output_comparison_banner_partner($row)!=='tarifcheck')continue;
            $payload=json_decode((string)($row['payload']??''),true);""")
    files[output]=o.encode()

    # Read-only explanation of where actual saved banner work was rejected,
    # inside the current Creative Library backend, not another tool/site.
    # One summary query, one output-object query; no external URL accesses.
    c=files[creative].decode()
    report=r'''
    /**
     * HAB RC34 KISS: real stored-Tarifcheck error protocol, read-only.
     * Does not assign, select, veto, verify images, or invoke any worker.
     * Uses SAME source partner detector and persisted source/output decisions.
     * Keeps personal affiliate tracking URLs entirely out of the report.
     */
    private function hab_rc34_tarifcheck_report() {
        if(!current_user_can('manage_options') || !class_exists('PPAR_HB_Integration'))return;
        global $wpdb;
        $table=$this->creative_library_table();
        $sql=$wpdb->prepare("SELECT id,provider,partner_name,partner_external_id,identity_hash,
          title,source_status,availability_state,review_status,topic_status,topic_targets,
          width,height,payload,destination_url
          FROM {$table} WHERE creative_type='banner' AND
          (partner_external_id=%s OR LOWER(partner_name) LIKE %s
           OR LOWER(destination_url) LIKE %s)
          ORDER BY id ASC LIMIT 251",
          'tarifcheck','%tarifcheck%','%tarifcheck.de%');
        $all=(array)$wpdb->get_results($sql,ARRAY_A);
        $rows=array();
        foreach($all as $row){
            if(!is_array($row) || $this->output_comparison_banner_partner($row)!=='tarifcheck')continue;
            $rows[]=$row;
        }
        $truncated=count($rows)>250;
        $rows=array_slice($rows,0,250);
        $local_key=$this->output_local_portal_key();
        $objects_by_hash=array();
        if($rows && method_exists($this,'output_objects_table')){
            $hashes=array_values(array_unique(array_filter(array_map(static function($row){
                $hash=strtolower((string)($row['identity_hash']??''));
                return preg_match('/^[a-f0-9]{64}$/',$hash)?$hash:'';
            },$rows))));
            if($hashes){
                $in=implode(',',array_fill(0,count($hashes),'%s'));
                $params=array_merge(array($local_key),$hashes);
                $objects=(array)$wpdb->get_results($wpdb->prepare(
                    "SELECT creative_identity_hash,status,decision_reason,slot_id,campaign_post_id
                     FROM {$this->output_objects_table()}
                     WHERE portal_key=%s AND output_type='portal_banner'
                     AND creative_identity_hash IN ({$in}) ORDER BY id DESC",
                     ...$params),ARRAY_A);
                foreach($objects as $obj){
                    if(!is_array($obj))continue;
                    $hash=strtolower((string)($obj['creative_identity_hash']??''));
                    if(!isset($objects_by_hash[$hash]))$objects_by_hash[$hash]=array();
                    $objects_by_hash[$hash][]=$obj;
                }
            }
        }
        $counts=array('erfasst'=>0,'bild_offen'=>0,'bild_fehler'=>0,'ziel_fehlt'=>0,
                      'ausgabe_fehlt'=>0,'ausgabe_gesperrt'=>0,
                      'ausgabe_entwurf'=>0,'ausgabe_aktiv'=>0,'veto'=>0);
        $problems=array();
        foreach($rows as $row){
            $counts['erfasst']++;
            $p=json_decode((string)($row['payload']??''),true);
            $p=is_array($p)?$p:array();
            $dimension=sanitize_key((string)($p['_dimension_state']??'pending'));
            $maps=json_decode((string)($row['topic_targets']??'[]'),true);
            $maps=is_array($maps)?$maps:array();
            $ours=array_values(array_filter($maps,static function($m)use($local_key){
                return is_array($m) && sanitize_key((string)($m['portal_key']??''))===$local_key
                    && sanitize_key((string)($m['state']??''))==='mapped';
            }));
            $obj=(array)($objects_by_hash[strtolower((string)($row['identity_hash']??''))]??array());
            $type='';
            $reason='';
            if(sanitize_key((string)($row['review_status']??''))==='rejected'
                || sanitize_key((string)($row['source_status']??''))!=='active'
                || sanitize_key((string)($row['availability_state']??''))!=='active'){
                $type='veto';$reason='Original ist gesperrt oder nicht aktiv';
            }elseif($dimension==='failed'){
                $type='bild_fehler';$reason='Bildprüfung fehlgeschlagen';
                $error=sanitize_text_field((string)($p['_dimension_error']??''));
                if($error!=='')$reason.=': '.substr($error,0,130);
            }elseif(!in_array($dimension,array('verified','mismatch'),true)
                || empty($p['_image_sha256'])
                || absint($row['width']??0)<=0 || absint($row['height']??0)<=0){
                $type='bild_offen';$reason='Bildprüfung nicht abgeschlossen';
            }elseif(!$ours){
                $type='ziel_fehlt';$reason='Kein fachlich freigegebener Versicherungszweig gespeichert';
            }elseif(!$obj){
                $type='ausgabe_fehlt';$reason='Zuordnung vorhanden, aber keine Ausgabe erzeugt';
            }else{
                $active=false;$draft=false;$blocked_reason='';
                foreach($obj as $item){
                    $status=sanitize_key((string)($item['status']??''));
                    if($status==='published'
                        && absint($item['campaign_post_id']??0)>0
                        && get_post_status(absint($item['campaign_post_id']))==='publish'){
                        $active=true;break;
                    }
                    if(in_array($status,array('draft','review','ready'),true))$draft=true;
                    if($blocked_reason==='' && strpos($status,'block')===0){
                        $blocked_reason=sanitize_text_field((string)($item['decision_reason']??''));
                    }
                }
                if($active){$type='ausgabe_aktiv';$reason='Ausgabe veröffentlicht; Frontend separat kontrollieren';}
                elseif($blocked_reason!==''){
                    $type='ausgabe_gesperrt';$reason='Ausgabe gesperrt: '.substr($blocked_reason,0,140);
                }elseif($draft){$type='ausgabe_entwurf';$reason='Ausgabe nur Entwurf oder in Prüfung';}
                else{$type='ausgabe_gesperrt';$reason='Kein veröffentlichter Banner aus vorhandener Zuordnung';}
            }
            $counts[$type]++;
            if($type!=='ausgabe_aktiv' && count($problems)<15){
                $name=sanitize_text_field((string)($row['title']??''));
                if($name==='')$name='Banner #'.absint($row['id']??0);
                $problems[]=array('name'=>substr($name,0,100),'reason'=>$reason);
            }
        }
        // Tiny aggregate checkpoint in existing WP options. No original
        // tracking URL, image link, private partner code or new DB table.
        update_option('ppar_hab_rc34_tarifcheck_last_check',
            array('checked_at'=>time(),'counts'=>$counts,'sample_limit'=>250),false);
        echo '<div class="ppar-library-panel" style="margin:12px 0">';
        echo '<h2>Tarifcheck: Warum wird kein Banner angezeigt?</h2>';
        echo '<p><strong>'.esc_html((string)$counts['erfasst']).' Banner gefunden</strong>';
        if($truncated)echo ' (erste 250 ausgewertet)';
        echo ' · Bild offen: '.absint($counts['bild_offen'])
            .' · Bildfehler: '.absint($counts['bild_fehler'])
            .' · Ziel fehlt: '.absint($counts['ziel_fehlt'])
            .' · Ausgabe fehlt: '.absint($counts['ausgabe_fehlt'])
            .' · Ausgabe gesperrt: '.absint($counts['ausgabe_gesperrt'])
            .' · nur Entwurf: '.absint($counts['ausgabe_entwurf'])
            .' · aktiv: '.absint($counts['ausgabe_aktiv'])
            .' · gesperrtes Original: '.absint($counts['veto']).'</p>';
        if(!$rows){
            echo '<p><strong>Keine Tarifcheck-Originale in dieser Werbemittelablage gefunden.</strong> Eingebundene Codes müssen hier als echte Bildbanner gespeichert sein.</p>';
        }elseif($problems){
            echo '<p><strong>Erste konkreten Ursachen aus den echten gespeicherten Bannern:</strong></p><ul style="list-style:disc;margin-left:22px">';
            foreach($problems as $entry){
                echo '<li>'.esc_html($entry['name']).': '.esc_html($entry['reason']).'</li>';
            }
            echo '</ul>';
        }else echo '<p>Alle gefundenen Banner sind gespeichert und veröffentlicht. Falls sie nicht sichtbar sind, muss der Seitenplatz geprüft werden.</p>';
        echo '<p><small>Nur Lesediagnose aus gespeicherten Daten. Kein Import, keine Änderung an Banner, Link oder Themenzuordnung. Stand: '.esc_html(wp_date('d.m.Y H:i')).'</small></p>';
        echo '</div>';
    }

'''
    c=one(c,"    public function render_creative_library_page() {",report+"    public function render_creative_library_page() {")
    c=one(c,
         """            <h1>Werbemittel &amp; Ausspielung</h1>
            <p>Zentrale für Import""",
         """            <h1>Werbemittel &amp; Ausspielung</h1>
            <?php $this->hab_rc34_tarifcheck_report(); ?>
            <p>Zentrale für Import""")
    files[creative]=c.encode()
    m=files[main].decode()
    m=one(m,"Version: 0.1.30-rc33","Version: 0.1.31-rc34")
    files[main]=m.encode()
    read=files[readme].decode()
    read=one(read,"Stable tag: 0.1.30-rc33","Stable tag: 0.1.31-rc34")
    files[readme]=read.encode()
    touched={output,creative,main,readme}
    assert all(files[name]==original.read(name) for name in original.namelist() if name not in touched)
    buf=BytesIO()
    with ZipFile(buf,"w") as new:
        for item in original.infolist():new.writestr(item,files[item.filename])
    updated=buf.getvalue()
with ZipFile(BytesIO(updated)) as test:
    assert test.testzip() is None and len(test.namelist())==36
    assert b"0.1.31-rc34" in test.read(main)
    assert b"hab_rc34_tarifcheck_report()" in test.read(creative)
    assert b"ppar_hab_rc34_tarifcheck_reconcile_v1" in test.read(output)
zip_path.write_bytes(updated)
print("HAB_RC34_KISS_BUILD_PASS",len(updated),sha256(updated).hexdigest())
