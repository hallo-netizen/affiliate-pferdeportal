#!/usr/bin/env python3
"""HAB only RC24: remove 50-concept bottleneck, honest coverage accounting,
German card text, genuine source-backed properties, bottom-aligned CTAs.
Build from exactly verified and user-installed HAB RC23; no Pferde Atelier files.
"""
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
import hashlib
ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=ROOT/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
OLD=P.read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
assert sha(OLD)=="c51f6517637a1db5fc4bf7e96613a697e79f8d70031ac48228d47659e86351f4",("Unexpected Hab RC23 source",sha(OLD))
prefix="affiliate-portal-router/"
bridge=prefix+"includes/class-ppar-hab-bewahr-bridge.php"
idealo=prefix+"includes/trait-ppar-idealo.php"
main=prefix+"affiliate-portal-router.php"
css=prefix+"assets/frontend.css"
readme=prefix+"readme.txt"
def once(s,old,new):
  n=s.count(old)
  assert n==1,("Expected exactly one source anchor",n,old[:160])
  return s.replace(old,new,1)
with ZipFile(BytesIO(OLD)) as z:
 assert z.testzip() is None and len(z.namelist())==36
 files={i.filename:z.read(i.filename) for i in z.infolist()}
 b=files[bridge].decode("utf8")
 # Distinguish insurance, clear information, unclassified topics, product targets
 # using the actual active WP tree rather than hardcoded 311 & 59.
 b=once(b,
 "        $seen_concepts = array();\n        foreach ($nodes as $n) {",
 """        $seen_concepts = array();
        $coverage_audit=array('all_core_categories'=>0,'insurance_excluded'=>0,
            'information_excluded'=>0,'unclassified_review'=>0,'unpublished_review'=>0,
            'recognized_product_categories'=>0,'unclassified_examples'=>array(),
            'information_examples'=>array(),'insurance_examples'=>array());
        foreach ($nodes as $n) {""")
 b=once(b,
 """            if (!$parent || !$world) { continue; }
            $category_label = (string)$n['name'];
            $family = self::product_family($category_label);
            $target_slug = '';""",
 """            if (!$parent || !$world) { continue; }
            $category_label = (string)$n['name'];
            $coverage_audit['all_core_categories']++;
            $world_name=mb_strtolower((string)($world['name']??''));
            $world_slug=sanitize_title((string)($world['slug']??''));
            $is_insurance=(strpos($world_slug,'versicher')!==false
                || strpos($world_name,'versicher')!==false);
            $is_information=(bool)preg_match('/(?:häufige fragen|haeufige fragen|kosten\\s*&\\s*aufwand|beratung|schadenmeldung|was tun|faq)/iu',$category_label);
            $family = self::product_family($category_label);
            if ($is_insurance) {
                $coverage_audit['insurance_excluded']++;
                if(count($coverage_audit['insurance_examples'])<12)$coverage_audit['insurance_examples'][]=$category_label;
                $family='';
            } elseif ($is_information) {
                $coverage_audit['information_excluded']++;
                if(count($coverage_audit['information_examples'])<12)$coverage_audit['information_examples'][]=$category_label;
                $family='';
            } elseif ($family==='') {
                // Unknown is NOT declared unavailable: product group may be missing in
                // the vocabulary; show it for a focused audit, not as a false gap.
                $coverage_audit['unclassified_review']++;
                if(count($coverage_audit['unclassified_examples'])<35)$coverage_audit['unclassified_examples'][]=$category_label;
            } else {
                $coverage_audit['recognized_product_categories']++;
            }
            $target_slug = '';""")
 b=once(b,
 """                if (!isset($seen_concepts[$unique]) && count($rules) < 50) {""",
 """                if (!isset($seen_concepts[$unique])) {""")
 b=once(b,
 """            // ALL existing article categories remain reachable, whether or""",
 """            if ($family!=='' && $target_slug==='') { $coverage_audit['unpublished_review']++; }
            // ALL existing article categories remain reachable, whether or""")
 b=once(b,
 """        $profiles=array();
        foreach ($worlds as $entry) {""",
 """        $coverage_audit['eligible_product_concepts']=count($concepts);
        $coverage_audit['unclassified_review_note']='Nicht erkannte Kategorien sind zur Prüfung vorgemerkt; nicht automatisch von Produktempfehlungen ausgeschlossen.';
        $profiles=array();
        foreach ($worlds as $entry) {""")
 b=once(b,
 """            'search_rules'=>$rules,'business_concepts'=>$concepts,""",
 """            'search_rules'=>$rules,'business_concepts'=>$concepts,
            'hab_product_coverage_audit'=>$coverage_audit,""")
 # Add product noun classes occurring on current public Hab WP categories, without
 # treating services, insurance tariffs or information pages as merchandise.
 b=once(b,
 """            'notstrom'=>'Notstromgerät','luftentfeuchter'=>'Luftentfeuchter',""",
 """            'notstrom'=>'Notstromgerät','luftentfeuchter'=>'Luftentfeuchter',
            'bilgenpumpe'=>'Bilgenpumpe','balkonkraftwerk'=>'Balkonkraftwerk',
            'ueberspannungsableiter'=>'Überspannungsableiter',
            'akkuladegeraet'=>'Akkuladegerät',
            'bewasserungssystem'=>'Bewässerungssystem',
            'abdichtungsmaterial'=>'Abdichtungsmaterial',
            'abholbox'=>'Abholbox','blitzschutz'=>'Blitzschutz',
            'gaswarneinrichtung'=>'Gaswarneinrichtung',
            'aussenrollladen'=>'Außenrollladen','sicherheitsfolie'=>'Sicherheitsfolie',
            'vorhangeschloss'=>'Vorhängeschloss',
            'dachbox'=>'Dachbox','absperrhahn'=>'Absperrhahn',
            'schliesssystem'=>'Schließsystem',""")
 files[bridge]=b.encode("utf8")
 t=files[idealo].decode("utf8")
 # A compact, sourced set of high-signal product properties; no invented unit,
 # synthetic price or product attribute. All values originate in the feed/title.
 product_features=r'''    private function idealo_hab_card_properties($payload, $title) {
        $payload=is_array($payload)?$payload:array();
        $parts=array();
        $brand=trim(sanitize_text_field((string)($payload['brand_name']??'')));
        if($brand!=='') $parts[]='Marke: '.mb_substr($brand,0,48);
        $dimension=trim(sanitize_text_field((string)($payload['size']??$payload['product_size']??'')));
        if($dimension==='' && preg_match('/(?<![0-9])([0-9]{2,3}\s*\/\s*[0-9]{2,3})(?![0-9])/u',(string)$title,$m)) {
            $dimension=preg_replace('/\s+/','',$m[1]);
        }
        if($dimension!=='')$parts[]='Maße: '.mb_substr($dimension,0,36);
        $model=trim(sanitize_text_field((string)($payload['model_number']??$payload['manufacturer_part_number']??'')));
        if($model==='' && preg_match('/\(([A-Za-z0-9-]{3,24})\)\s*$/u',(string)$title,$m))$model=$m[1];
        if($model!=='')$parts[]='Art.-Nr.: '.mb_substr($model,0,35);
        if(count($parts)<2) {
            $category=trim(sanitize_text_field((string)($payload['sub_category']??'')));
            if($category!=='' && mb_strtolower($category)!==mb_strtolower($brand))
                $parts[]='Produktart: '.mb_substr($category,0,55);
        }
        return implode(' · ',array_slice($parts,0,3));
    }

    /** Coverage audit lives in the EXISTING idealo setting option; no new table. */
    private function idealo_hab_coverage_report() {
        $mi=$this->idealo_match_index();
        if (is_wp_error($mi)) return array('error'=>$mi->get_error_message());
        $s=$this->idealo_settings();
        $concepts=(array)($mi['concepts']??array());
        $matched=(array)($s['last_matched_concept_ids']??array());
        // Also reflects the existing staged set immediately after an upgrade,
        // before another huge feed download is needed.
        if (!$matched && isset($GLOBALS['wpdb'])) {
            global $wpdb;
            $table=$this->network_sync_table('products');
            $ids=(array)$wpdb->get_col("SELECT DISTINCT category FROM {$table} WHERE network='idealo' AND quality_status='pass'");
            $matched=array_values(array_filter(array_map('sanitize_key',$ids)));
        }
        $have=array_fill_keys($matched,true);$missing=array();
        foreach($concepts as $id=>$concept) {
            if (isset($have[$id]))continue;
            $missing[]=array('id'=>$id,'produktgruppe'=>(string)($concept['title']??''),
                'themenbereich'=>(string)($concept['main_hub']??''),
                'grund'=>'Kein sicherer passender Feedartikel nachgewiesen');
        }
        return array('concept_count'=>count($concepts),
            'matched_count'=>max(0,count($concepts)-count($missing)),
            'missing_count'=>count($missing),
            'not_matched'=>array_slice($missing,0,80),
            'tree'=>(array)($mi['catalog']['hab_product_coverage_audit']??array()),
            'feed_rows_seen'=>absint($s['last_feed_rows_seen']??0),
            'feed_accepted'=>absint($s['last_import_count']??0),
            'reasons'=>(array)($s['last_feed_reject_stats']??array()),
            'last_run'=>absint($s['last_import_at']??0));
    }

'''
 t=once(t,"    private function idealo_import_feed_file($path, $source_label = 'Eigener Hab & Bewahr iPN Datafeed') {",product_features+"    private function idealo_import_feed_file($path, $source_label = 'Eigener Hab & Bewahr iPN Datafeed') {")
 # Preserve real reason statistics on full streaming CSV importer. Each processed
 # feed row goes in precisely one outcome bucket; no per-row transient storage.
 t=once(t,
 """        $rows=array(); $seen=0; $malformed=0; $ambiguous=0; $context_rejected=0; $matched_concepts=array(); $matched_hubs=array();""",
 """        $rows=array(); $seen=0; $malformed=0; $ambiguous=0; $context_rejected=0; $matched_concepts=array(); $matched_hubs=array();
        $reject=array('malformed'=>0,'missing_title_link_image'=>0,'missing_gtin'=>0,
            'no_product_concept_match'=>0,'ambiguous_match'=>0,'context_rejected'=>0,
            'image_not_approved'=>0,'accepted'=>0);""")
 t=once(t,
 """            $seen++; if (count($values)!==count($headers)) { $malformed++; continue; }
            $row=array_combine($headers,$values); if (!$row) { $malformed++; continue; }""",
 """            $seen++; if (count($values)!==count($headers)) { $malformed++; $reject['malformed']++; continue; }
            $row=array_combine($headers,$values); if (!$row) { $malformed++; $reject['malformed']++; continue; }""")
 t=once(t,
 """            if (trim((string)($row['product_title']??''))==='' || trim((string)($row['product_deeplink']??''))==='' || trim((string)($row[$image_field]??''))==='') { continue; }
            $gtins=$this->idealo_normalize_gtins_from_values(array($row['ean']??'',$row['gtins_product']??'')); if (!$gtins) { continue; }""",
 """            if (trim((string)($row['product_title']??''))==='' || trim((string)($row['product_deeplink']??''))==='' || trim((string)($row[$image_field]??''))==='') { $reject['missing_title_link_image']++; continue; }
            $gtins=$this->idealo_normalize_gtins_from_values(array($row['ean']??'',$row['gtins_product']??'')); if (!$gtins) { $reject['missing_gtin']++; continue; }""")
 t=once(t,
 """            $status=(string)($match['status']??'none'); if ($status==='ambiguous') { $ambiguous++; continue; } if ($status==='context_rejected') { $context_rejected++; continue; } if ($status!=='matched' || !is_array($match['concept']??null)) { continue; }""",
 """            $status=(string)($match['status']??'none'); if ($status==='ambiguous') { $ambiguous++; $reject['ambiguous_match']++; continue; } if ($status==='context_rejected') { $context_rejected++; $reject['context_rejected']++; continue; } if ($status!=='matched' || !is_array($match['concept']??null)) { $reject['no_product_concept_match']++; continue; }""")
 t=once(t,
 """            $row['__idealo_concept_id']=$concept_id; $row['__idealo_match_score']=(string)absint($match['score']??0); $row['__idealo_context_score']=(string)absint($match['context']??0); $row['__currency_eur']='EUR'; $row['__programme_external_id']='84749'; $row['__programme_name']='idealo DE'; $row['__price']=isset($row['price'])?(string)$row['price']:''; $row['__image_url']=$this->idealo_direct_image_url((string)$row[$image_field]); if ($row['__image_url']==='') { continue; }
            $rows[]=$row; $matched_concepts[$concept_id]=true; $matched_hubs[(string)($concept['main_hub']??'').'|'.(string)($concept['hub']??'')]=true;""",
 """            $row['__idealo_concept_id']=$concept_id; $row['__idealo_match_score']=(string)absint($match['score']??0); $row['__idealo_context_score']=(string)absint($match['context']??0); $row['__currency_eur']='EUR'; $row['__programme_external_id']='84749'; $row['__programme_name']='idealo DE'; $row['__price']=isset($row['price'])?(string)$row['price']:''; $row['__image_url']=$this->idealo_direct_image_url((string)$row[$image_field]); if ($row['__image_url']==='') { $reject['image_not_approved']++; continue; }
            $reject['accepted']++;
            $rows[]=$row; $matched_concepts[$concept_id]=true; $matched_hubs[(string)($concept['main_hub']??'').'|'.(string)($concept['hub']??'')]=true;""")
 t=once(t,
 """        $settings['last_feed_hash']=$hash?:''; $settings['last_import_started_at']=$import_started_at; $settings['last_import_at']=time(); $settings['last_import_count']=count($rows); $settings['last_matched_concepts']=count($matched_concepts); $settings['last_matched_hubs']=count(array_filter(array_keys($matched_hubs),static function($v){return trim((string)$v,'|')!=='';})); $settings['last_ambiguous_count']=$ambiguous; $settings['last_context_rejected_count']=$context_rejected;""",
 """        $settings['last_feed_hash']=$hash?:''; $settings['last_import_started_at']=$import_started_at; $settings['last_import_at']=time(); $settings['last_import_count']=count($rows); $settings['last_matched_concepts']=count($matched_concepts); $settings['last_matched_hubs']=count(array_filter(array_keys($matched_hubs),static function($v){return trim((string)$v,'|')!=='';})); $settings['last_ambiguous_count']=$ambiguous; $settings['last_context_rejected_count']=$context_rejected;
        $settings['last_feed_rows_seen']=$seen;
        $settings['last_feed_reject_stats']=$reject;
        $settings['last_matched_concept_ids']=array_keys($matched_concepts);
        $settings['last_eligible_concepts']=count((array)($mi['concepts']??array()));""")
 t=once(t,
 """        $settings['last_message']=sprintf('%s: %d sichere Produkte, %d/311 Produktkonzepte und %d/59 Hub-Familien; %d Feedzeilen geprüft; %d fehlerhaft; %d mehrdeutig verworfen.',$source_label,count($rows),count($matched_concepts),absint($settings['last_matched_hubs']),$seen,$malformed,$ambiguous);""",
 """        $settings['last_message']=sprintf('%s: %d sichere Produkte, %d/%d tatsächlich produktfähige Konzepte und %d Hub-Familien; %d Feedzeilen geprüft; %d fehlerhaft; %d mehrdeutig verworfen.',
            $source_label,count($rows),count($matched_concepts),count((array)$mi['concepts']),
            absint($settings['last_matched_hubs']),$seen,$malformed,$ambiguous);""")
 t=once(t,
 """        return array('campaigns'=>$saved_count,'targets'=>$targets,'retired'=>$retired,'contract_concepts'=>311,'strategy'=>$this->idealo_link_strategy());""",
 """        return array('campaigns'=>$saved_count,'targets'=>$targets,'retired'=>$retired,'contract_concepts'=>count($concept_map),'strategy'=>$this->idealo_link_strategy());""")
 # Reuse original import data. Campaigns get visible true properties without
 # inventing features; existing staged materialization is refreshed on upgrade.
 t=once(t,
 """$campaign['title']=$title; $campaign['description']=''; $campaign['button_text']='Bei idealo vergleichen';""",
 """$campaign['title']=$title; $campaign['description']=$this->idealo_hab_card_properties($payload,$title); $campaign['button_text']='Bei idealo vergleichen';""")
 t=once(t,
 """        if ((string)get_option(self::IDEALO_SCHEMA_OPTION,'0')==='5') { return; }""",
 """        if ((string)get_option(self::IDEALO_SCHEMA_OPTION,'0')==='6') { return; }""")
 t=once(t,
 """        update_option(self::IDEALO_SCHEMA_OPTION,'5',false); $this->idealo_sync_campaign_activation();""",
 """        update_option(self::IDEALO_SCHEMA_OPTION,'6',false); $this->idealo_sync_campaign_activation();""")
 # One admin overview audit on existing idealo specialist page only.
 t=once(t,
 """            <section class="postbox" style="padding:18px"><h2>Providerbestand</h2>""",
 """            <?php $hb_audit=$this->idealo_hab_coverage_report(); $hb_tree=(array)($hb_audit['tree']??array()); $hb_why=(array)($hb_audit['reasons']??array()); ?>
            <section class="postbox" style="padding:18px">
                <h2>Produktabdeckung – prüfbarer Bericht</h2>
                <?php if (!empty($hb_audit['error'])): ?>
                  <p><?php echo esc_html((string)$hb_audit['error']); ?></p>
                <?php else: ?>
                  <p><strong>Für Produktangebote erkannt:</strong> <?php echo absint($hb_audit['concept_count']??0); ?> Produktgruppen ·
                     <strong>Mit Treffern:</strong> <?php echo absint($hb_audit['matched_count']??0); ?> ·
                     <strong>Ohne Treffer:</strong> <?php echo absint($hb_audit['missing_count']??0); ?></p>
                  <p><strong>Aus der Produktwerbung ausgeschlossen:</strong> <?php echo absint($hb_tree['insurance_excluded']??0); ?> Versicherungs-Kategorien,
                     <?php echo absint($hb_tree['information_excluded']??0); ?> reine Info-/FAQ-Kategorien.
                     <strong>Zu prüfen:</strong> <?php echo absint($hb_tree['unclassified_review']??0); ?> weitere Kategorien, deren Produktart bislang nicht eindeutig erkannt wurde.</p>
                  <p><strong>Letzter Feed:</strong> <?php echo absint($hb_audit['feed_rows_seen']??0); ?> Zeilen untersucht,
                     <?php echo absint($hb_audit['feed_accepted']??0); ?> Produkte aufgenommen.</p>
                  <?php if ($hb_why): ?>
                    <details><summary>Warum Feedzeilen nicht übernommen wurden</summary><ul>
                      <?php foreach($hb_why as $key=>$value): ?><li><?php echo esc_html(str_replace('_',' ',(string)$key)); ?>: <?php echo absint($value); ?></li><?php endforeach; ?>
                    </ul></details>
                  <?php endif; ?>
                  <details><summary>Produktgruppen ohne Feedtreffer (erste 80)</summary>
                    <table class="widefat striped"><thead><tr><th>Produktgruppe</th><th>Bereich</th><th>Grund</th></tr></thead><tbody>
                    <?php foreach ((array)($hb_audit['not_matched']??array()) as $miss): ?><tr><td><?php echo esc_html((string)($miss['produktgruppe']??'')); ?></td>
                    <td><?php echo esc_html((string)($miss['themenbereich']??'')); ?></td><td><?php echo esc_html((string)($miss['grund']??'')); ?></td></tr><?php endforeach; ?></tbody></table>
                  </details>
                  <details><summary>Weitere Themen zur Produkt-Eignungsprüfung (erste 35)</summary><ul>
                  <?php foreach ((array)($hb_tree['unclassified_examples']??array()) as $un): ?><li><?php echo esc_html((string)$un); ?></li><?php endforeach; ?>
                  </ul></details>
                  <p><small>Die frühere Anzeige 11/311 war kein belastbarer Abdeckungswert. Versicherungen bleiben separat. Fehlende GTINs, Bilder und eindeutige Zuordnungen werden nicht geschätzt.</small></p>
                <?php endif; ?>
            </section>
            <section class="postbox" style="padding:18px"><h2>Providerbestand</h2>""")
 t=once(t,
 """<strong>Portalabdeckung:</strong> <?php echo absint($s['last_matched_concepts']??0); ?>/311 Konzepte · <?php echo absint($s['last_matched_hubs']??0); ?>/59 Hub-Familien""",
 """<strong>Produktabdeckung:</strong> <?php echo absint($s['last_matched_concepts']??0); ?>/<?php echo absint($hb_audit['concept_count']??0); ?> erkannte kaufbare Produktgruppen · <?php echo absint($s['last_matched_hubs']??0); ?> Hub-Familien""")
 files[idealo]=t.encode("utf8")
 m=files[main].decode("utf8")
 m=once(m,"Version: 0.1.20-rc23","Version: 0.1.21-rc24")
 m=once(m,
 """        $availability = isset($banner['availability']) ? trim(strtr((string)$banner['availability'], $replacements)) : '';""",
 """        $availability = isset($banner['availability']) ? trim(strtr((string)$banner['availability'], $replacements)) : '';
        if (preg_match('/^category_product_[123]$/D', sanitize_key((string)$slot_type))) {
            $avail_key=strtolower($availability);
            if ($avail_key==='available'||$avail_key==='in_stock') $availability='Verfügbar';
            elseif ($avail_key==='out_of_stock'||$avail_key==='unavailable') $availability='Derzeit nicht verfügbar';
        }""")
 files[main]=m.encode("utf8")
 styles=files[css].decode("utf8")
 assert "/* HAB RC24" not in styles
 styles+=r'''

/* HAB RC24 – only category product cards, zero additional frames. */
.ppar-hb-category-products-grid > .ppar-affiliate-slot {
  border:1px solid #d2dbd5!important;
  box-shadow:none!important;
}
.ppar-hb-category-products-grid .ppar-affiliate-content,
.ppar-hb-category-products-grid .ppar-banner-link[data-ppar-category-product-card="1"] {
  border:0!important; outline:0!important; box-shadow:none!important;
}
.ppar-hb-category-products-grid .ppar-banner-text[data-ppar-category-product-text="1"]{
  display:flex!important; flex-direction:column!important; flex:1 1 auto!important;
  min-height:0!important; align-items:stretch!important;
}
.ppar-hb-category-products-grid .ppar-banner-description{
  display:block!important;
  color:#495d51!important; font-size:11.5px!important; line-height:1.5!important;
  font-weight:400!important; overflow-wrap:anywhere!important;
  margin:0!important; padding:0!important;
}
.ppar-hb-category-products-grid .ppar-banner-availability{
  font-size:11px!important; color:#526b5d!important;
}
.ppar-hb-category-products-grid .ppar-banner-text > .ppar-banner-button{
  margin-top:auto!important; flex-shrink:0!important;
}
.ppar-hb-category-products-grid .ppar-banner-text > .ppar-banner-actions{
  margin-top:auto!important; flex-shrink:0!important;
  width:100%!important;
}
.ppar-hb-category-products-grid .ppar-banner-button,
.ppar-hb-category-products-grid .ppar-banner-offer-button{
  border-width:1px!important; box-shadow:none!important;
}
'''
 files[css]=styles.encode("utf8")
 rd=files[readme].decode("utf8")
 rd=once(rd,"Stable tag: 0.1.20-rc23","Stable tag: 0.1.21-rc24")
 files[readme]=rd.encode("utf8")
 touched={bridge,idealo,main,css,readme}
 for name in z.namelist():
   if name not in touched:assert files[name]==z.read(name),name
 out=BytesIO()
 with ZipFile(out,"w") as fresh:
   for item in z.infolist():fresh.writestr(item,files[item.filename])
 blob=out.getvalue()
with ZipFile(BytesIO(blob)) as check:
 assert len(check.namelist())==36 and check.testzip() is None
 assert b"count($rules) < 50" not in check.read(bridge)
 assert b"Version: 0.1.21-rc24" in check.read(main)
 assert b"'last_feed_reject_stats'" in check.read(idealo)
P.write_bytes(blob)
print("HAB_RC24_BUILD_PASS",len(blob),sha(blob),"modified",len(touched),"files; original all other files retained")
