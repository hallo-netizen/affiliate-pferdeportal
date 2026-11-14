#!/usr/bin/env python3
"""HAB RC42: ONLY ONE ADMIN-ONLY read-only export inside existing HAB-004.
Build on exact QA-passed RC41. No import, target or frontend modifications.
"""
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from hashlib import sha256
R=Path('protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ')
P=R/'PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip'
raw=P.read_bytes()
assert sha256(raw).hexdigest()=='28a0921047aff8c03b18bb214d38efc94a154bfe9cc413f9aca437c3789ec222','Exact RC41 required'
B='affiliate-portal-router/'
CRE=B+'includes/trait-ppar-creative-library.php'
MAIN=B+'affiliate-portal-router.php'
README=B+'readme.txt'
def once(s,a,b):
    assert s.count(a)==1,('Original source changed',s.count(a),a[:160])
    return s.replace(a,b,1)
with ZipFile(BytesIO(raw)) as z:
    assert z.testzip() is None and len(z.namelist())==36
    files={info.filename:z.read(info.filename) for info in z.infolist()}
    m=files[MAIN].decode()
    m=once(m,
        "            add_action('admin_post_ppar_creative_library_import', array($this, 'handle_creative_library_import'));",
        """            add_action('admin_post_ppar_creative_library_import', array($this, 'handle_creative_library_import'));
            // Hab RC42: one private read-only source export; no new worker.
            add_action('admin_post_ppar_hab_tarifcheck_source_export', array($this, 'hb_tarifcheck_source_export'));""")
    m=once(m,"Version: 0.1.38-rc41","Version: 0.1.39-rc42")
    files[MAIN]=m.encode()
    c=files[CRE].decode()
    method=r'''
    /**
     * Hab RC42: one private read-only evidence export of the EXISTING
     * Tarifcheck banner records, current verified WP tree and output objects.
     * No classification, no reimport, no database writes, no new tables,
     * no frontend hook and no changes to any other portals.
     */
    public function hb_tarifcheck_source_export() {
        if(!current_user_can('manage_options')){
            wp_die('Keine Berechtigung für den Tarifcheck-Bestandsbericht.');
        }
        check_admin_referer('ppar_hab_tarifcheck_source_export');
        $host=strtolower((string)wp_parse_url(home_url('/'),PHP_URL_HOST));
        if(!preg_match('/(^|\.)hab-und-bewahr\.de$/',$host)){
            wp_die('Dieser Diagnoseexport ist nur im Hab-&-Bewahr-Portal verfügbar.');
        }
        global $wpdb;
        $table=$this->creative_library_table();
        // Exactly the existing library's Tarifcheck filter; NO mutation.
        $sql=$wpdb->prepare(
            "SELECT * FROM {$table} WHERE creative_type='banner'".
            " AND (partner_external_id=%s OR LOWER(partner_name)=%s)".
            " ORDER BY id ASC",
            'tarifcheck','tarifcheck'
        );
        $rows=(array)$wpdb->get_results($sql,ARRAY_A);
        $items=array();
        $hashes=array();
        foreach($rows as $row){
            if(!is_array($row))continue;
            $payload=json_decode((string)($row['payload']??''),true);
            $payload=is_array($payload)?$payload:array();
            // The payload whitelist includes all source-related evidence
            // but excludes any provider raw secrets or unrelated credentials.
            $fields=array(
                '_destination_source','_source_read_version','_source_evidence',
                '_original_html_attributes_available',
                'title_source','creative_title','alt_text','html',
                'provider_topic_name','provider_topic_id','provider_topic_source',
                'promotion_category_name','provider_category_name',
                'banner_name','name','information','anchor_text',
                'description','tags','creative_description','creative_tag',
                '_dimension_state','_dimension_error','_declared_width','_declared_height',
                '_preverify_topic_status','_preverify_topic_targets',
                '_hb_insurance_plan_reason','_hb_insurance_original_reason',
            );
            $evidence=array();
            foreach($fields as $field){
                if(array_key_exists($field,$payload)){
                    $evidence[$field]=$payload[$field];
                }
            }
            $stored_targets=json_decode((string)($row['topic_targets']??'[]'),true);
            $stored_targets=is_array($stored_targets)?$stored_targets:array();
            $items[]=array(
                'id'=>absint($row['id']??0),
                'identity_hash'=>(string)($row['identity_hash']??''),
                'provider'=>(string)($row['provider']??''),
                'partner_name'=>(string)($row['partner_name']??''),
                'partner_external_id'=>(string)($row['partner_external_id']??''),
                'external_id'=>(string)($row['external_id']??''),
                'source_hash'=>(string)($row['source_hash']??''),
                'original_or_placeholder_title'=>(string)($row['title']??''),
                'description'=>(string)($row['description']??''),
                'tags'=>(string)($row['tags']??''),
                'tracking_url'=>(string)($row['tracking_url']??''),
                'destination_url'=>(string)($row['destination_url']??''),
                'image_url'=>(string)($row['image_url']??''),
                'dimensions'=>array(absint($row['width']??0),absint($row['height']??0)),
                'source_status'=>(string)($row['source_status']??''),
                'availability_state'=>(string)($row['availability_state']??''),
                'review_status'=>(string)($row['review_status']??''),
                'selected'=>absint($row['selected']??0),
                'content_scope'=>(string)($row['content_scope']??''),
                'topic_status'=>(string)($row['topic_status']??''),
                'topic_score'=>absint($row['topic_score']??0),
                'topic_targets'=>$stored_targets,
                'topic_targets_raw'=>(string)($row['topic_targets']??''),
                'source_evidence_saved'=>$evidence,
            );
            $hash=strtolower((string)($row['identity_hash']??''));
            if(preg_match('/^[a-f0-9]{64}$/',$hash))$hashes[$hash]=$hash;
        }
        $actual_nodes=array();
        $tree_state='not_available';
        if(class_exists('PPAR_HB_Integration') && method_exists('PPAR_HB_Integration','verified_nodes')){
            $nodes=PPAR_HB_Integration::verified_nodes();
            if(is_array($nodes)){
                $tree_state='verified_nodes_read';
                foreach($nodes as $key=>$n){
                    if(!is_array($n))continue;
                    $actual_nodes[]=array(
                        'key'=>(string)$key,
                        'parent'=>(string)($n['parent']??''),
                        'type'=>(string)($n['type']??''),
                        'name'=>(string)($n['name']??''),
                        'slug'=>(string)($n['slug']??''),
                        'wp_id'=>absint($n['wp_id']??0),
                    );
                }
            }
        }
        // Saved output-object records are not evidence of frontend visibility;
        // include them so the actual publish state and chosen pages can be audited.
        $outputs=array();
        if($hashes && method_exists($this,'output_objects_table')){
            $output_table=$this->output_objects_table();
            $marks=implode(',',array_fill(0,count($hashes),'%s'));
            $out_sql=$wpdb->prepare(
                "SELECT id,creative_identity_hash,portal_key,target_key,slot_id,".
                "status,campaign_post_id FROM {$output_table}".
                " WHERE output_type='portal_banner' AND creative_identity_hash IN ({$marks})".
                " ORDER BY id ASC LIMIT 20000",
                ...array_values($hashes)
            );
            $found=(array)$wpdb->get_results($out_sql,ARRAY_A);
            foreach($found as $out){
                if(!is_array($out))continue;
                $outputs[]=array(
                    'id'=>absint($out['id']??0),
                    'creative_identity_hash'=>(string)($out['creative_identity_hash']??''),
                    'portal_key'=>(string)($out['portal_key']??''),
                    'target_key'=>(string)($out['target_key']??''),
                    'slot_id'=>(string)($out['slot_id']??''),
                    'status'=>(string)($out['status']??''),
                    'campaign_post_id'=>absint($out['campaign_post_id']??0),
                );
            }
        }
        $result=array(
            'report'=>'HAB_TARIFCHECK_STORED_SOURCE_READ_ONLY',
            'created_at_utc'=>gmdate('c'),
            'status'=>'actual_wordpress_stored_rows_not_original_partner_html',
            'read_only'=>true,
            'count'=>count($items),
            'category_tree_status'=>$tree_state,
            'category_tree'=>$actual_nodes,
            'banner_items'=>$items,
            'stored_output_objects'=>$outputs,
            'limitations'=>array(
                'Old source HTML attributes erased during earlier imports cannot be rebuilt from storage.',
                'An active stored object alone does not prove frontend display.',
                'All URLs and affiliate IDs are private: do not post this file on public GitHub.',
            ),
        );
        $body=wp_json_encode($result,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_PRETTY_PRINT);
        if(!is_string($body) || $body==='')wp_die('Bestandsbericht konnte nicht erstellt werden.');
        if(headers_sent())wp_die('Download konnte nicht gestartet werden.');
        nocache_headers();
        header('Content-Type: application/json; charset=utf-8');
        header('Content-Disposition: attachment; filename="hab-tarifcheck-bestandspruefung-'.gmdate('Ymd-His').'.json"');
        header('X-Content-Type-Options: nosniff');
        echo $body;
        exit;
    }

'''
    c=once(c,
        "    public function render_creative_library_page() {",
        method+"    public function render_creative_library_page() {")
    # Only a back-office button on the actual Hab & Bewahr installation.
    c=once(c,
        """            <h1>Werbemittel &amp; Ausspielung</h1>""",
        """            <h1>Werbemittel &amp; Ausspielung</h1>
            <?php
              $ppar_hb_export_host=strtolower((string)wp_parse_url(home_url('/'),PHP_URL_HOST));
              if(current_user_can('manage_options') && preg_match('/(^|\\.)hab-und-bewahr\\.de$/',$ppar_hb_export_host)):
                $ppar_hb_export_url=wp_nonce_url(
                    admin_url('admin-post.php?action=ppar_hab_tarifcheck_source_export'),
                    'ppar_hab_tarifcheck_source_export');
            ?>
              <p><a class="button button-secondary" href="<?php echo esc_url($ppar_hb_export_url); ?>">Tarifcheck-Bestand einmalig als JSON exportieren</a>
              <span class="description">Nur lesen: vorhandene Banner, gespeicherte Hinweise, Ziele und Kategorien. Keine Änderungen.</span></p>
            <?php endif; ?>""")
    files[CRE]=c.encode()
    rd=files[README].decode()
    rd=once(rd,"Stable tag: 0.1.38-rc41","Stable tag: 0.1.39-rc42")
    files[README]=rd.encode()
    allowed={MAIN,CRE,README}
    assert all(files[name]==z.read(name) for name in z.namelist() if name not in allowed)
    b=BytesIO()
    with ZipFile(b,'w') as dst:
        for info in z.infolist():dst.writestr(info,files[info.filename])
    data=b.getvalue()
with ZipFile(BytesIO(data)) as z:
    assert len(z.namelist())==36 and z.testzip() is None
    assert b"admin_post_ppar_hab_tarifcheck_source_export" in z.read(MAIN)
    assert b"function hb_tarifcheck_source_export()" in z.read(CRE)
P.write_bytes(data)
print("RC42_READONLY_SINGLE_EXPORT_BUILD_PASS",len(data),sha256(data).hexdigest())
