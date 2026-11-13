#!/usr/bin/env python3
"""Read exact RC36; record one existing import decision's blocking reason.
The RC34 admin screen only READS stored facts. Zero new logic/worker/slots.
"""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from hashlib import sha256
R=Path('protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ')
P=R/'PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip'
raw=P.read_bytes()
assert sha256(raw).hexdigest()=='c209d2ab37b889bd901e4aa665dde6ecce94e43f3541a2458f39e7e525a42dc4','Exact RC36 prerequisite'
B='affiliate-portal-router/'
OUT=B+'includes/trait-ppar-output-objects.php'
CRE=B+'includes/trait-ppar-creative-library.php'
MAIN=B+'affiliate-portal-router.php'
README=B+'readme.txt'
def one(s,a,b):
    assert s.count(a)==1,(s.count(a),a[:190])
    return s.replace(a,b,1)
with ZipFile(BytesIO(raw)) as source:
    assert source.testzip() is None and len(source.namelist())==36
    files={i.filename:source.read(i.filename) for i in source.infolist()}
    o=files[OUT].decode()
    o=one(o,
        '            $hb_plan=$this->hb_rc31_insurance_banner_plan($row,$portal,$targets,$wanted);',
        '''            $hb_plan=$this->hb_rc31_insurance_banner_plan($row,$portal,$targets,$wanted);
            // A SINGLE import decision already knows its exact blocker.
            // Store only that reason (no private URL, HTML, IDs) for the
            // existing admin report. Never classify again in the report.
            if($comparison_partner==='tarifcheck'
                && !empty($portal['local']) && class_exists('PPAR_HB_Integration')){
                $hb_reason=is_array($hb_plan)
                    ? (string)($hb_plan['reason']??'Keine Begründung zurückgegeben')
                    : 'Nicht als Versicherungszweig eingestuft';
                $payload['_hb_insurance_reason']=sanitize_text_field($hb_reason);
                $payload['_hb_insurance_result']=is_array($hb_plan)
                    ? sanitize_key((string)($hb_plan['status']??'unknown'))
                    : 'not_insurance';
            }''')
    o=one(o,
        '''        global $wpdb;
        // No source asset or manually approved banner is deleted. Unverifiable
        // targets are removed from *automatic placements* only (fail closed).
        $wpdb->update($this->creative_library_table(),array(
            'topic_status'=>$mapped>0?'auto_verified':'no_match',''',
        '''        global $wpdb;
        // One existing library update also saves the reason from the SAME
        // import decision. Source banner code and its URLs are not changed.
        if(isset($payload['_hb_insurance_result'])
           && $mapped===0 && $payload['_hb_insurance_result']==='ready'){
            $payload['_hb_insurance_reason']='Fachliches Ziel erkannt, aber keine Zuordnung gespeichert';
        }
        // No source asset or manually approved banner is deleted. Unverifiable
        // targets are removed from *automatic placements* only (fail closed).
        $wpdb->update($this->creative_library_table(),array(
            'payload'=>wp_json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),
            'topic_status'=>$mapped>0?'auto_verified':'no_match',''')
    o=one(o,"$option='ppar_hab_rc36_tarifcheck_reconcile_v1';","$option='ppar_hab_rc37_tarifcheck_reconcile_v1';")
    files[OUT]=o.encode()
    c=files[CRE].decode()
    c=one(c,
        '''        $problems=array();
        foreach($rows as $row){''',
        '''        $problems=array();
        $hb_missing_reasons=array();
        $hb_missing_source_types=array();
        $hb_blocked_formats=array();
        foreach($rows as $row){''')
    c=one(c,
        '''            $counts[$type]++;
            if($type!=='ausgabe_aktiv' && count($problems)<15){''',
        '''            $counts[$type]++;
            // Read ONLY saved original/decision facts. No new topic/slot
            // classifier and no tracking-link or image fetch on this page.
            if($type==='ziel_fehlt'){
                $r=sanitize_text_field((string)($p['_hb_insurance_reason']??'Keine Entscheidung im alten Datensatz protokolliert'));
                if($r==='')$r='Keine Entscheidung im alten Datensatz protokolliert';
                $hb_missing_reasons[$r]=($hb_missing_reasons[$r]??0)+1;
                $origin=sanitize_key((string)($p['_destination_source']??'unbekannt'));
                if($origin==='')$origin='unbekannt';
                $hb_missing_source_types[$origin]=($hb_missing_source_types[$origin]??0)+1;
            }
            if($type==='ausgabe_gesperrt'){
                $format=absint($row['width']??0).' x '.absint($row['height']??0);
                $hb_blocked_formats[$format]=($hb_blocked_formats[$format]??0)+1;
            }
            if($type!=='ausgabe_aktiv' && count($problems)<15){''')
    c=one(c,
        '''        if(!$rows){
            echo '<p><strong>Keine Tarifcheck-Originale in dieser Werbemittelablage gefunden.</strong> Eingebundene Codes müssen hier als echte Bildbanner gespeichert sein.</p>';''',
        '''        if($rows){
            arsort($hb_missing_reasons);arsort($hb_missing_source_types);arsort($hb_blocked_formats);
            echo '<details open><summary><strong>Ursachen aus allen gespeicherten Tarifcheck-Bannern</strong></summary>';
            echo '<p><strong>Warum Ziel fehlt (bereits bei der einzigen Einleseentscheidung festgestellt):</strong></p><ul>';
            foreach($hb_missing_reasons as $reason=>$number){
                echo '<li>'.absint($number).' × '.esc_html($reason).'</li>';
            }
            echo '</ul><p><strong>Art des gespeicherten Ziellinks bei fehlender Zuordnung:</strong></p><ul>';
            foreach($hb_missing_source_types as $origin=>$number){
                echo '<li>'.absint($number).' × '.esc_html($origin).'</li>';
            }
            echo '</ul><p><strong>Bildmaße gesperrter Ausgaben (keine neuen Anzeigenplätze erfunden):</strong></p><ul>';
            foreach($hb_blocked_formats as $format=>$number){
                echo '<li>'.absint($number).' × '.esc_html($format).' Pixel</li>';
            }
            echo '</ul><p><small>Nur vorhandene Originalmaße und gespeicherte Entscheidungen. Keine Partner-IDs, Trackinglinks oder HTML-Codes ausgegeben.</small></p></details>';
        }
        if(!$rows){
            echo '<p><strong>Keine Tarifcheck-Originale in dieser Werbemittelablage gefunden.</strong> Eingebundene Codes müssen hier als echte Bildbanner gespeichert sein.</p>';''')
    files[CRE]=c.encode()
    m=files[MAIN].decode()
    m=one(m,'Version: 0.1.33-rc36','Version: 0.1.34-rc37')
    files[MAIN]=m.encode()
    rd=files[README].decode()
    rd=one(rd,'Stable tag: 0.1.33-rc36','Stable tag: 0.1.34-rc37')
    files[README]=rd.encode()
    expect={OUT,CRE,MAIN,README}
    assert all(files[name]==source.read(name) for name in source.namelist() if name not in expect)
    out=BytesIO()
    with ZipFile(out,'w') as dst:
        for i in source.infolist():dst.writestr(i,files[i.filename])
    result=out.getvalue()
with ZipFile(BytesIO(result)) as v:
    assert v.testzip() is None and len(v.namelist())==36
    assert b'ppar_hab_rc37_tarifcheck_reconcile_v1' in v.read(OUT)
    assert b'$hb_missing_reasons' in v.read(CRE)
P.write_bytes(result)
print('RC37_ONLY_SAVED_IMPORT_REASON_AND_EXISTING_READONLY_REPORT',len(result),sha256(result).hexdigest())
