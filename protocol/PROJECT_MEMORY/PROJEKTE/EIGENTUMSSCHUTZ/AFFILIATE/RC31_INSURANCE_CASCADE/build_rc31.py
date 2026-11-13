#!/usr/bin/env python3
"""HAB-004 RC31: user Zielvertrag: each REAL Tarifcheck insurance banner only
inside the verified insurance world, cascaded down its SAME insurance branch.
Never re-import/delete originals. Existing Idealo/feed and physical product
mapping untouched; clarify Idealo-only coverage report. KISS: one existing
mapping function, stored target keys, one admin-incremental migration.
"""
from pathlib import Path
from zipfile import ZipFile
from hashlib import sha256
from io import BytesIO
R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
raw=P.read_bytes()
assert sha256(raw).hexdigest()=="baa8e87cbab1f1bbbbce4f482bd73a706985f583c847f543eb93fbf7c644f34f","Unexpected RC30 base; stop"
BASE="affiliate-portal-router/"
output=BASE+"includes/trait-ppar-output-objects.php"
main=BASE+"affiliate-portal-router.php"
readme=BASE+"readme.txt"
idealo=BASE+"includes/trait-ppar-idealo.php"
def once(s,a,b):
    assert s.count(a)==1,("RC30 anchor mismatch",s.count(a),a[:150])
    return s.replace(a,b,1)

# This logic uses the exact existing verified category tree, not words like
# "Wissen > Versicherungen & Recht" or a guessed topic-to-category mapping.
helper=r'''
    /**
     * Verified Hab-only insurance routing. Only the current WP ancestry is
     * authoritative. A specific genuine insurance banner goes to one R2/R3
     * page and its actual descendants; a documented *general* insurance
     * comparison may go to the insurance root and descendants.
     * Does not change original partner data or the visual slots.
     *
     * Return null for non-insurance creatives; otherwise ready/blocked.
     */
    private function hb_rc31_insurance_banner_plan($row,$portal,$targets,$wanted) {
        $partner=$this->output_comparison_banner_partner($row);
        if (!in_array($partner,array('tarifcheck','check24'),true)) return null;
        $family=$this->output_tarifcheck_banner_family($row);
        if ($family==='kosten') return null; // finance path unchanged; never insurance
        if (!class_exists('PPAR_HB_Integration') || empty($portal['local'])) {
            return array('status'=>'blocked','reason'=>'No verified local Hab insurance tree');
        }
        $nodes=PPAR_HB_Integration::verified_nodes();
        $root='core:world:insurance';
        if (!is_array($nodes) || empty($nodes[$root]['wp_id'])) {
            return array('status'=>'blocked','reason'=>'Missing verified insurance root');
        }
        $payload=json_decode((string)($row['payload']??''),true);
        $payload=is_array($payload)?$payload:array();
        $title_source=sanitize_key((string)($payload['title_source']??''));
        $real_title=in_array($title_source,array('provider_missing','manual_missing'),true)
            ? '' : (string)($row['title']??'');
        // Three pre-existing evidence tiers, stronger first.
        $tiers=array(
            $this->output_destination_semantic_text($row),
            trim((string)($payload['provider_topic_name']??'').' '.(string)($payload['promotion_category_name']??'')),
            trim($real_title.' '.(string)($row['description']??'').' '.(string)($row['tags']??'')
              .' '.(string)($payload['banner_name']??'')),
        );
        $evidence=array();
        foreach($tiers as $text) {
            $normal=$this->output_text((string)$text);
            if ($normal!=='') $evidence[]=$normal;
        }
        if (!$evidence) return array('status'=>'blocked','reason'=>'No verified insurance creative evidence');
        $all=implode(' ', $evidence);
        // Never allow credit, shopping, energy, or financing masquerading as insurance.
        if (preg_match('/\b(kredit|kreditvergleich|girokonto|baufinanzierung|stromtarif|gastarif|dsl)\b/u',$all)) {
            return array('status'=>'blocked','reason'=>'Financial or non-insurance content');
        }
        $eligible=array();
        foreach ($nodes as $key=>$node) {
            if (!is_array($node) || empty($node['wp_id'])) continue;
            $cursor=$key;$seen=array();$depth=0;$under=false;
            while(isset($nodes[$cursor]) && !isset($seen[$cursor]) && $depth<25) {
                $seen[$cursor]=true;
                if($cursor===$root){$under=true;break;}
                $cursor=(string)($nodes[$cursor]['parent']??'');
                $depth++;
            }
            if($under) $eligible[$key]=array('node'=>$node,'depth'=>$depth);
        }
        $candidate_matches=array();
        foreach ($eligible as $key=>$item) {
            $node=$item['node'];
            if ($key===$root || ($node['type']??'')!=='page') continue;
            // R2/R3 pages only; editorial end categories do not choose banners.
            $name=$this->output_text((string)($node['name']??''));
            $slug=$this->output_text(str_replace(array('-','_'),' ',(string)($node['slug']??'')));
            $phrases=array_values(array_unique(array_filter(array($name,$slug))));
            foreach ($phrases as $phrase) {
                if(strlen($phrase)<5 || in_array($phrase,array('versicherungen','versicherung','vorsorge','krankenschutz'),true)) continue;
                $rx='/(?<![a-z0-9])'.preg_quote($phrase,'/').'(?![a-z0-9])/u';
                if(preg_match($rx,$all)) {
                    $candidate_matches[$key]=array('depth'=>$item['depth'],'length'=>strlen($phrase));
                    break;
                }
            }
        }
        $anchor='';
        if($candidate_matches) {
            // Prefer a more specific real R3 to its own R2 ancestor only.
            uasort($candidate_matches,static function($a,$b) {
                return $b['depth']<=>$a['depth'] ?: $b['length']<=>$a['length'];
            });
            $keys=array_keys($candidate_matches);
            $anchor=(string)$keys[0];
            foreach(array_slice($keys,1) as $other) {
                $cursor=$anchor;$same_branch=false;$seen=array();
                while(isset($nodes[$cursor]) && !isset($seen[$cursor])) {
                    $seen[$cursor]=true;
                    if($cursor===$other){$same_branch=true;break;}
                    $cursor=(string)($nodes[$cursor]['parent']??'');
                }
                if(!$same_branch) {
                    return array('status'=>'blocked','reason'=>'Conflicting specific insurance names');
                }
            }
        } else {
            $generic=(bool)preg_match(
                '/(?:versicherungsvergleich|alle versicherungen|versicherungen vergleichen|versicherungsschutz vergleichen|versicherungen im vergleich)/u',$all);
            if(!$generic || $family==='blocked' && !preg_match('/versicherungsvergleich/u',$all)) {
                return array('status'=>'blocked','reason'=>'No verified specific/general insurance');
            }
            $anchor=$root;
        }

        // Exact WP IDs and ancestry from the verified HB tree, not name matching
        // after the initial unique banner type is selected.
        $allowed=array();
        foreach($eligible as $key=>$item) {
            $cursor=$key;$seen=array();$is_descendant=false;
            while(isset($nodes[$cursor]) && !isset($seen[$cursor])) {
                $seen[$cursor]=true;
                if($cursor===$anchor){$is_descendant=true;break;}
                $cursor=(string)($nodes[$cursor]['parent']??'');
            }
            if(!$is_descendant) continue;
            $node=$item['node'];
            $type=sanitize_key((string)($node['type']??''));
            if(!in_array($type,array('page','category'),true)) continue;
            $allowed[$type.':'.absint($node['wp_id'])]=true;
        }
        $source_target=null;$keys=array();
        foreach((array)$targets as $target) {
            if(!is_array($target))continue;
            $type=sanitize_key((string)($target['type']??''));
            if(!in_array($type,(array)$wanted,true) ||
                empty($allowed[$type.':'.absint($target['id']??0)])) continue;
            $canonical=$this->output_campaign_target_key($target);
            if($canonical==='') continue;
            $keys[$canonical]=$canonical;
            if($type===($nodes[$anchor]['type']??'') &&
                absint($target['id']??0)===absint($nodes[$anchor]['wp_id']??0)) {
                $source_target=$target;
            }
        }
        if(!$source_target || !$keys) {
            return array('status'=>'blocked','reason'=>'No verified WP target for insurance product');
        }
        // Always one stored record; its exact canonical path keys include ONLY
        // descendants of the chosen insurance page (no unrelated R2/R3).
        return array(
            'status'=>'ready','target'=>$source_target,
            'path_target_keys'=>array_values($keys),
            'source'=>$anchor===$root?'hab_insurance_general_verified':'hab_insurance_specific_verified',
            'reason'=>'Verified genuine '.($anchor===$root?'general insurance':'specific insurance').' branch',
            'confidence'=>100
        );
    }

'''
with ZipFile(BytesIO(raw)) as z:
    assert z.testzip() is None and len(z.namelist())==36
    files={i.filename:z.read(i.filename) for i in z.infolist()}
    o=files[output].decode()
    o=once(o,"    private function output_tarifcheck_target_allowed($target, $family) {",helper+"    private function output_tarifcheck_target_allowed($target, $family) {")
    # Take the *specific* HB contract before the outdated broad all-insurance branch.
    o=once(o,
        """            $wanted=array_values(array_filter(array_map('sanitize_key',(array)($portal['banner_target_types']??array('page','category')))));

            // Die zwei vereinbarten Vergleichsfamilien""",
        """            $wanted=array_values(array_filter(array_map('sanitize_key',(array)($portal['banner_target_types']??array('page','category')))));
            $hb_plan=$this->hb_rc31_insurance_banner_plan($row,$portal,$targets,$wanted);
            if (is_array($hb_plan)) {
                if(($hb_plan['status']??'')==='ready' && !empty($hb_plan['target'])) {
                    $verified_target=$hb_plan['target'];
                    $new_records[]=array(
                        'portal_key'=>$portal_key,
                        'state'=>'mapped',
                        'level'=>'verified_branch',
                        'target_key'=>sanitize_text_field((string)$verified_target['key']),
                        'target_label'=>sanitize_text_field((string)($verified_target['label']??'')),
                        'path_target_keys'=>(array)($hb_plan['path_target_keys']??array()),
                        'confidence'=>100,
                        'source'=>sanitize_key((string)($hb_plan['source']??'hab_insurance_verified')),
                        'destination_source'=>$source,
                        'destination_url'=>$destination,
                        'updated_at'=>time(),
                    );
                    $mapped++;
                }
                // Unknown/specific ambiguous Banner: NEVER send it to all
                // insurance categories. Keep its stored asset for review.
                continue;
            }

            // Die zwei vereinbarten Vergleichsfamilien""")
    # Existing family logic continues to allow finance only; forbid the obsolete
    # blanket insurance branch in any unverified HB page.
    o=once(o,
       "            if(in_array($tarifcheck_family,array('kosten','versicherung'),true)){",
       "            if($tarifcheck_family==='kosten'){")
    o=once(o,
        """        global $wpdb;
        $wpdb->update($this->creative_library_table(),array(
            'topic_status'=>$mapped>0?'auto_verified':'no_match',""",
        """        global $wpdb;
        // No source asset or manually approved banner is deleted. Unverifiable
        // targets are removed from *automatic placements* only (fail closed).
        $wpdb->update($this->creative_library_table(),array(
            'topic_status'=>$mapped>0?'auto_verified':'no_match',""")
    # Add one admin-only incremental pass over already imported Tarifcheck
    # creatives. Never reupload, redownload or re-key their partner image.
    migrate=r'''
    /** Rebind existing VERIFIED originals in safe 60-row WP-admin batches.
     * One update option, no new WP table, worker, cron, or user clicks.
     * Each admin request advances; when done the gate is a cheap get_option.
     */
    public function hb_rc31_reconcile_stored_tarifcheck_once() {
        if(!is_admin() || !current_user_can('manage_options')
           || !class_exists('PPAR_HB_Integration')
           || !method_exists($this,'creative_library_table')) return;
        $page=sanitize_key((string)($_GET['page']??''));
        if(strpos($page,'affiliate-portal')!==0) return;
        $option='ppar_hab_rc31_tarifcheck_reconcile_v1';
        $state=get_option($option,array());
        if(!is_array($state))$state=array();
        if(!empty($state['complete']))return;
        $cursor=absint($state['cursor']??0);
        global $wpdb;
        $table=$this->creative_library_table();
        $sql=$wpdb->prepare(
            "SELECT * FROM {$table} WHERE id>%d AND creative_type='banner' ".
            "AND (partner_external_id=%s OR LOWER(partner_name)=%s) ".
            "ORDER BY id ASC LIMIT 60", $cursor,'tarifcheck','tarifcheck');
        $rows=(array)$wpdb->get_results($sql,ARRAY_A);
        foreach($rows as $row) {
            if(!is_array($row))continue;
            $cursor=max($cursor,absint($row['id']??0));
            $payload=json_decode((string)($row['payload']??''),true);
            $payload=is_array($payload)?$payload:array();
            if(!in_array(sanitize_key((string)($payload['_dimension_state']??'')),
                          array('verified','mismatch'),true))continue;
            $result=$this->output_assign_banner_targets_from_destination_once($row);
            if(!is_array($result) || empty($result['updated']))continue;
            // Existing campaign-materialization path, now with the new actual
            // branch keys. One qualified asset is handled at a time.
            if(method_exists($this,'output_plan_creative')) {
                $row['topic_targets']=wp_json_encode((array)($result['targets']??array()),
                       JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
                $row['topic_status']=empty($result['mapped'])?'no_match':'auto_verified';
                $row['topic_score']=empty($result['mapped'])?0:100;
                $this->output_plan_creative($row,true);
            }
        }
        update_option($option,array(
            'cursor'=>$cursor,
            'complete'=>count($rows)<60?1:0,
            'updated_at'=>time(),
        ),false);
    }

'''
    o=once(o,"    private function output_banner_compatible_slots($row,$portal) {",migrate+"    private function output_banner_compatible_slots($row,$portal) {")
    files[output]=o.encode()

    m=files[main].decode()
    m=once(m,"Version: 0.1.27-rc30","Version: 0.1.28-rc31")
    m=once(m,
        "        $this->tariff_tools_register_hooks();",
        """        $this->tariff_tools_register_hooks();
        // RC31: existing verified Tarifcheck originals are automatically
        // reclassified after update, no reimport and no new WP interface.
        if (!$is_ajax_request) {
            add_action('admin_init',array($this,'hb_rc31_reconcile_stored_tarifcheck_once'),55);
        }""")
    files[main]=m.encode()
    rd=files[readme].decode()
    rd=once(rd,"Stable tag: 0.1.27-rc30","Stable tag: 0.1.28-rc31")
    files[readme]=rd.encode()
    t=files[idealo].decode()
    t=once(t,"<h2>Produktabdeckung – prüfbarer Bericht</h2>",
        "<h2>Idealo-Feedabdeckung – prüfbarer Bericht</h2>")
    t=once(t,">Produktgruppen ohne Feedtreffer (erste 80)</summary>",
        ">Nur bei Idealo ohne nachgewiesenen Feedtreffer (erste 80; andere Händler können passende Karten liefern)</summary>")
    files[idealo]=t.encode()
    changed={output,main,readme,idealo}
    assert all(files[name]==z.read(name) for name in z.namelist() if name not in changed)
    dst=BytesIO()
    with ZipFile(dst,"w") as w:
        for item in z.infolist():w.writestr(item,files[item.filename])
    data=dst.getvalue()
with ZipFile(BytesIO(data)) as check:
    assert check.testzip() is None and len(check.namelist())==36
    assert b"0.1.28-rc31" in check.read(main)
    assert b"hb_rc31_insurance_banner_plan" in check.read(output)
P.write_bytes(data)
print("HAB_RC31_BUILD_PASS",len(data),sha256(data).hexdigest())
