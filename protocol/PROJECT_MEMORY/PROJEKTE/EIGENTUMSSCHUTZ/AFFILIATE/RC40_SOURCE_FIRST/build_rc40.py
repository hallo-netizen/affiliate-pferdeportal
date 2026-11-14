#!/usr/bin/env python3
"""One source-reading owner at beginning of EACH path: import or legacy rebind.
Then one EXISTING Hab target/format decision, then stored frontend only.
Build the complete RC39 release unmodified first; alter exactly 4 files.
"""
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from hashlib import sha256
R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
raw=P.read_bytes()
assert sha256(raw).hexdigest()=="135c97298a20da952d2ec0c1a127123cde54cc903ffbdc06f5f2e2761aa9bcfa","Exact RC39 archive required"
B="affiliate-portal-router/"
CRE=B+"includes/trait-ppar-creative-library.php"
OUT=B+"includes/trait-ppar-output-objects.php"
MAIN=B+"affiliate-portal-router.php"
README=B+"readme.txt"
def one(s,old,new):
    assert s.count(old)==1,("Unverified original source: stop",s.count(old),old[:160])
    return s.replace(old,new,1)
with ZipFile(BytesIO(raw)) as source:
    assert source.testzip() is None and len(source.namelist())==36
    data={z.filename:source.read(z.filename) for z in source.infolist()}
    c=data[CRE].decode()
    # The ONE source-content reader is portal neutral. It never chooses a
    # target, fetches banner images, reads the frontend or creates tables.
    # Every credible content field comes directly from the original record.
    reader=r'''
    /** ONE read of original banner content BEFORE any automatic allocation.
     * Idempotent for a previously read original. Used both by initial import
     * and the EXISTING legacy 60-item WordPress reconcile. No new worker.
     */
    private function creative_library_read_original_banner_once($row) {
        if(!is_array($row) || sanitize_key((string)($row['creative_type']??''))!=='banner') return $row;
        $payload=json_decode((string)($row['payload']??''),true);
        $payload=is_array($payload)?$payload:array();
        if((int)($payload['_source_read_version']??0)===1
           && is_array($payload['_source_evidence']??null)) return $row;
        $html=(string)($payload['html']??'');
        $img_title=$html!==''?$this->creative_library_html_attr($html,'img','title'):'';
        $img_alt=$html!==''?$this->creative_library_html_attr($html,'img','alt'):'';
        $anchor_title=$html!==''?$this->creative_library_html_attr($html,'a','title'):'';
        // HTML-only text: remove images and script text, never interpret
        // untrusted HTML as an instruction or an authenticated destination.
        $visible='';
        if($html!=='') {
            $text=preg_replace('~<script\b[^>]*>.*?</script>~is',' ',$html);
            $text=preg_replace('~<img\b[^>]*>~is',' ',$text);
            $visible=sanitize_text_field(wp_strip_all_tags((string)$text));
        }
        $partner=sanitize_text_field((string)($row['partner_name']??''));
        $original_title=sanitize_text_field((string)($payload['creative_title']??''));
        if($original_title===''){
            $candidate=sanitize_text_field((string)($row['title']??''));
            if($candidate!=='' && strtolower($candidate)!==strtolower(trim($partner.' Banner'))
               && !in_array(sanitize_key((string)($payload['title_source']??'')),
                    array('manual_missing','provider_missing'),true)){
                $original_title=$candidate;
            }
        }
        if($original_title==='' && $img_title!=='')$original_title=$img_title;
        $payload['title_source']=$original_title===''?'manual_missing':
            (sanitize_key((string)($payload['title_source']??''))?:'provider_original');

        $tracking=esc_url_raw((string)($row['tracking_url']??''));
        $destination=esc_url_raw((string)($row['destination_url']??''));
        $source=sanitize_key((string)($payload['_destination_source']??''));
        $destination_evidence='';
        // A genuine decoded/explicit/resolved landing page gives its PATH
        // and query's declared product, never a guessed affiliate ad_id.
        if(in_array($source,array('provider_explicit','decoded_tracking','resolved_redirect'),true)
           && $destination!=='' && ($destination!==$tracking || $source==='provider_explicit')){
            $p=wp_parse_url($destination);
            $p=is_array($p)?$p:array();
            $destination_evidence=trim(rawurldecode((string)($p['path']??'')), "/ \t\n\r");
            $q=array();parse_str((string)($p['query']??''),$q);
            foreach(array('deep','product','insurance','category','tariff') as $name) {
                if(is_scalar($q[$name]??null)){
                    $v=trim((string)$q[$name]);if($v!=='' && strlen($v)<=160) $destination_evidence.=' '.$v;
                }
            }
        }
        // Some genuine Tarifcheck partner links declare the product in deep=
        // directly within the HTML anchor URL, before an HTTP redirect.
        $p=$tracking!==''?wp_parse_url($tracking):array();
        $p=is_array($p)?$p:array();
        $host=strtolower((string)($p['host']??''));
        $host=preg_replace('/^www\./','',$host);
        $first_party=$host==='tarifcheck.de' || substr($host,-14)==='.tarifcheck.de';
        $known_click=$host==='a.partner-versicherung.de'||$host==='partner-versicherung.de';
        if($known_click||$first_party){
            $q=array();parse_str((string)($p['query']??''),$q);
            if(is_scalar($q['deep']??null)){
                $deep=trim((string)$q['deep']);
                if($deep!==''&&strlen($deep)<=160) $destination_evidence.=' '.$deep;
            }
            if($first_party) {
                $path=trim(rawurldecode((string)($p['path']??'')), "/ \t\n\r");
                if($path!=='' && !preg_match('~^(?:click|redirect|go|out)(?:[/._-]|$)~i',$path)){
                    $destination_evidence.=' '.$path;
                }
            }
        }

        $provider=implode(' ',array_filter(array(
            (string)($payload['provider_topic_name']??''),
            (string)($payload['promotion_category_name']??''),
            (string)($payload['provider_category_name']??''),
        ),'strlen'));
        $text=implode(' ',array_filter(array(
            $original_title,$img_title,$img_alt,$anchor_title,
            (string)($payload['alt_text']??''),
            (string)($row['description']??''),
            (string)($row['tags']??''),
            (string)($payload['information']??''),
            (string)($payload['banner_name']??''),
            $visible,
        ),'strlen'));
        // Original image filename is a weaker hint, ONLY if it includes an
        // explicit insurance product, not generic ad, size or hash.
        $image_path=(string)wp_parse_url((string)($row['image_url']??''),PHP_URL_PATH);
        $filename=(string)pathinfo($image_path,PATHINFO_FILENAME);
        $image_hint=preg_match('/(?:hausrat|haftpflicht|rechtsschutz|kfz|motorrad|pflegeversicherung|krankenversicherung|wohngeba|berufsunfa|reiseversicherung)/i',$filename)
            ? str_replace(array('-','_'), ' ', $filename) : '';
        $payload['_source_evidence']=array(
            'destination'=>sanitize_text_field(trim($destination_evidence)),
            'provider'=>sanitize_text_field($provider),
            'text'=>sanitize_text_field($text),
            'image_hint'=>sanitize_text_field($image_hint),
        );
        $payload['_source_read_version']=1;
        $row['payload']=wp_json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
        return $row;
    }

'''
    c=one(c,
        "    private function creative_library_normalize_row($row, $mapping, $context) {",
        reader+"    private function creative_library_normalize_row($row, $mapping, $context) {")
    # The parser's original title source is never masked by a fabricated
    # provider-name placeholder. This occurs BEFORE image/target classification.
    c=one(c,
        """        $title = sanitize_text_field($this->creative_library_mapped_value($row, $mapping, 'title'));
        $description = sanitize_textarea_field($this->creative_library_mapped_value($row, $mapping, 'description'));""",
        """        $title = sanitize_text_field($this->creative_library_mapped_value($row, $mapping, 'title'));
        $source_title=$title;
        $description = sanitize_textarea_field($this->creative_library_mapped_value($row, $mapping, 'description'));""")
    c=one(c,
        """            '_destination_source'=>$destination_source,
            '_preverify_topic_status'=>'portal_pending',""",
        """            '_destination_source'=>$destination_source,
            'title_source'=>($source_title!=='' || $alt!=='')?'provider_original':'manual_missing',
            '_preverify_topic_status'=>'portal_pending',""")
    # The full raw fields are now available, but the only source extraction
    # occurs BEFORE any possible assignment / output processing.
    c=one(c,
        """        // Source freshness must include provider payload fields as well.""",
        """        if($type==='banner') {
            // First and only source-read. Future allocation uses this saved
            // immutable evidence, not a second parse of HTML.
            $normalized=$this->creative_library_read_original_banner_once($normalized);
        }
        // Source freshness must include provider payload fields as well.""")
    data[CRE]=c.encode()

    o=data[OUT].decode()
    # Legacy data are read with the very SAME method immediately before the
    # existing owner's assignment. The result is saved into existing payload.
    o=one(o,
        """        $destination=esc_url_raw((string)($row['destination_url']??''));
        $comparison_partner=$this->output_comparison_banner_partner($row);""",
        """        // REQUIRED FIRST STEP: read every original field exactly once,
        // including previously stored banners (no reimport).
        if(method_exists($this,'creative_library_read_original_banner_once')){
            $row=$this->creative_library_read_original_banner_once($row);
            $payload=json_decode((string)($row['payload']??''),true);
            $payload=is_array($payload)?$payload:array();
        }
        $destination=esc_url_raw((string)($row['destination_url']??''));
        $comparison_partner=$this->output_comparison_banner_partner($row);""")
    # Consolidate the legacy redirect write into the ONE existing final update.
    o=one(o,
        """                    $wpdb->update($this->creative_library_table(),array(
                        'destination_url'=>$resolved_url,
                        'payload'=>$row['payload'],
                    ),array('id'=>$row_id));
                    $source=$resolved_source;""",
        """                    // Destination/evidence are saved in the existing
                    // SINGLE update below, not a separate intermediate write.
                    $source=$resolved_source;""")
    o=one(o,
        """        $wpdb->update($this->creative_library_table(),array(
            'payload'=>wp_json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),
            'topic_status'=>$mapped>0?'auto_verified':'no_match',""",
        """        $wpdb->update($this->creative_library_table(),array(
            'destination_url'=>$destination,
            'payload'=>wp_json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),
            'topic_status'=>$mapped>0?'auto_verified':'no_match',""")
    # The existing Hab classifier consumes ONLY evidence read at step 1.
    # Legacy direct-unit calls without saved evidence keep old behavior.
    o=one(o,
        """        $family=$this->output_tarifcheck_banner_family($row);
        if ($family==='kosten') return null; // finance path unchanged; never insurance
        if (!class_exists('PPAR_HB_Integration') || empty($portal['local'])) {""",
        """        $pre_payload=json_decode((string)($row['payload']??''),true);
        $pre_payload=is_array($pre_payload)?$pre_payload:array();
        $source_evidence=$pre_payload['_source_evidence']??null;
        if(is_array($source_evidence) && (int)($pre_payload['_source_read_version']??0)===1){
            // No second banner parsing or second target choice.
            $source_words=$this->output_text(implode(' ',array_values($source_evidence)));
            if(preg_match('/\\b(kredit|kreditvergleich|girokonto|baufinanzierung|stromtarif|gastarif|dsl)\\b/u',$source_words)){
                return null;
            }
            $family=preg_match('/\\b(versicherung|versicherungen|versicherungsvergleich|haftpflicht)\\b/u',$source_words)
                ?'versicherung':'blocked';
        }else{
            // Historical direct plugin calls outside the banner import retain
            // their original contract; imported originals always use step 1.
            $family=$this->output_tarifcheck_banner_family($row);
        }
        if ($family==='kosten') return null; // finance path unchanged
        if (!class_exists('PPAR_HB_Integration') || empty($portal['local'])) {""")
    o=one(o,
        """        // Three pre-existing evidence tiers, stronger first.
        $tiers=array(
            $this->output_destination_semantic_text($row),
            trim((string)($payload['provider_topic_name']??'').' '.(string)($payload['promotion_category_name']??'')),
            trim($real_title.' '.(string)($row['description']??'').' '.(string)($row['tags']??'')
              .' '.(string)($payload['banner_name']??'').' '.$original_anchor_text),
        );""",
        """        // The original content was read ONCE at the workflow entrance.
        // Do not re-examine target link / HTML here.
        $tiers=is_array($source_evidence)
            ? array((string)($source_evidence['destination']??''),
                    (string)($source_evidence['provider']??''),
                    trim((string)($source_evidence['text']??'').' '.(string)($source_evidence['image_hint']??'')))
            : array(
                $this->output_destination_semantic_text($row),
                trim((string)($payload['provider_topic_name']??'').' '.(string)($payload['promotion_category_name']??'')),
                trim($real_title.' '.(string)($row['description']??'').' '.(string)($row['tags']??'')
                    .' '.(string)($payload['banner_name']??'').' '.$original_anchor_text),
            );""")
    # Do not perform the legacy general comparison-family classification in
    # advance of Hab's sole owner; for unrelated providers retain old behavior.
    o=one(o,
        """        $comparison_partner=$this->output_comparison_banner_partner($row);
        $tarifcheck_family=$this->output_tarifcheck_banner_family($row);
        $portals=$this->output_portal_registry();""",
        """        $comparison_partner=$this->output_comparison_banner_partner($row);
        // This is reserved for NON-HAB paths; Hab's owner makes one decision.
        $tarifcheck_family='';
        $portals=$this->output_portal_registry();""")
    o=one(o,
        """            // Die zwei vereinbarten Vergleichsfamilien bleiben die einzigen
            // Mehrziel-Faelle: Kredit -> alle Kosten-Blaetter, Versicherung -> alle""",
        """            // Non-HAB legacy branches remain unchanged.
            if($tarifcheck_family===''){
                $tarifcheck_family=$this->output_tarifcheck_banner_family($row);
            }
            // Die zwei vereinbarten Vergleichsfamilien bleiben die einzigen
            // Mehrziel-Faelle: Kredit -> alle Kosten-Blaetter, Versicherung -> alle""")
    o=one(o,"$option='ppar_hab_rc39_tarifcheck_reconcile_v1';","$option='ppar_hab_rc40_tarifcheck_reconcile_v1';")
    data[OUT]=o.encode()
    m=data[MAIN].decode()
    m=one(m,"Version: 0.1.36-rc39","Version: 0.1.37-rc40")
    data[MAIN]=m.encode()
    rd=data[README].decode()
    rd=one(rd,"Stable tag: 0.1.36-rc39","Stable tag: 0.1.37-rc40")
    data[README]=rd.encode()
    changed={CRE,OUT,MAIN,README}
    assert all(data[n]==source.read(n) for n in source.namelist() if n not in changed)
    out=BytesIO()
    with ZipFile(out,"w") as z:
        for info in source.infolist():z.writestr(info,data[info.filename])
    new=out.getvalue()
with ZipFile(BytesIO(new)) as check:
    assert check.testzip() is None and len(check.namelist())==36
    assert b"_source_read_version" in check.read(CRE)
    assert b"ppar_hab_rc40_tarifcheck_reconcile_v1" in check.read(OUT)
P.write_bytes(new)
print("RC40_ONE_READ_BEFORE_SINGLE_DECISION_AND_SAVE_BUILD_PASS",len(new),sha256(new).hexdigest())
