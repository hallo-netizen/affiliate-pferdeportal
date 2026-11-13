#!/usr/bin/env python3
"""RC33: one authoritative insurance banner topic decision, written at import.
Later stages READ it, never replace it or try to infer topic again.
Safety (images, tracking URLs, manual veto, real slot) stays intact.
No other portal source files changed.
"""
from zipfile import ZipFile
from io import BytesIO
from pathlib import Path
from hashlib import sha256
R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
raw=P.read_bytes()
assert sha256(raw).hexdigest()=="fa72cf9519ccaf92c672581eff35a8e4908a3f15511a1ef5f272448a36c99d56","RC31 base must be exact"
B="affiliate-portal-router/"
main=B+"affiliate-portal-router.php"
routing=B+"includes/trait-ppar-output-objects.php"
readme=B+"readme.txt"
def once(s,a,b):
    assert s.count(a)==1,("Anchor unexpected",s.count(a),a[:220])
    return s.replace(a,b,1)
def replace_method(s,signature,new):
    start=s.index("    private function "+signature+"(")
    end=s.index("\n    }\n",start)+7
    assert s[start:end].count("    private function ")==1
    return s[:start]+new+s[end:]

with ZipFile(BytesIO(raw)) as z:
    assert z.testzip() is None and len(z.namelist())==36
    data={i.filename:z.read(i.filename) for i in z.infolist()}
    o=data[routing].decode()
    # SOURCE OF TRUTH: only once on import in the existing
    # output_assign_banner_targets_from_destination_once() method.
    # Subsequent planning must never overwrite the original topic_targets.
    o=once(o,
        """        $target=is_array($classification['target']??null)?$classification['target']:array();
        $target_key=sanitize_text_field((string)($target['key']??''));""",
        """        // RC33: insurance banner topic_targets are owned ONLY by the
        // source-URL-based classifier. The old library planner must not write
        // a second, incomplete mapping over its verified subtree.
        $source=sanitize_key((string)($classification['source']??''));
        if(in_array($source,array('hab_insurance_specific_verified',
                                  'hab_insurance_general_verified'),true)) return;
        $target=is_array($classification['target']??null)?$classification['target']:array();
        $target_key=sanitize_text_field((string)($target['key']??''));""")
    # The original RECORD PROVENANCE must survive the read, not be replaced with
    # the generic "creative_library_destination_map" identity.
    # A stable proof label rides in a pre-existing campaign field; NO new DB field.
    o=once(o,
        """            'reason'=>$record_source==='tarifcheck_credit_all_cost_categories'
                ? 'Gespeicherte Tarifcheck-Kredit-Zielkarte für alle Kosten-Kategorien.'""",
        """            'reason'=>in_array($record_source,array('hab_insurance_specific_verified',
                                        'hab_insurance_general_verified'),true)
                ? ('HB_INSURANCE_CANONICAL:'.$record_source)
                : ($record_source==='tarifcheck_credit_all_cost_categories'
                ? 'Gespeicherte Tarifcheck-Kredit-Zielkarte für alle Kosten-Kategorien.'""")
    o=once(o,
        """                            : ($state==='general'?'Gespeicherter allgemeiner Banner-Fallback aus der Creative-Library.':'Gespeicherte Ziel-URL-Zuordnung aus der Creative-Library.')))),""",
        """                            : ($state==='general'?'Gespeicherter allgemeiner Banner-Fallback aus der Creative-Library.':'Gespeicherte Ziel-URL-Zuordnung aus der Creative-Library.'))))),""")
    o=once(o,
        """            'source'=>$multi_source?$record_source:($state==='general'?'creative_library_general_fallback':'creative_library_destination_map'),""",
        """            'source'=>in_array($record_source,array('hab_insurance_specific_verified',
                                                 'hab_insurance_general_verified'),true)
                ? $record_source
                : ($multi_source?$record_source:($state==='general'?'creative_library_general_fallback':'creative_library_destination_map')),""")
    # Previously recorded blanket insurance labels remain in Review until the
    # one-time migration recalculates the single trusted subtree; no old leaks.
    o=once(o,
        """        $record_source=sanitize_key((string)($record['source']??''));
        $multi_source=in_array($record_source,array(""",
        """        $record_source=sanitize_key((string)($record['source']??''));
        if (class_exists('PPAR_HB_Integration')
            && !empty($portal['local'])
            && in_array($record_source,array(
                'tarifcheck_insurance_all_insurance_categories',
                'check24_insurance_all_insurance_categories'),true)) {
            return array('status'=>'review','confidence'=>0,
                'reason'=>'Überholte Mehrfachzuordnung; neue Versicherungs-Zielkarte wird zentral erstellt.',
                'target'=>null,'alternatives'=>array(),
                'source'=>'hab_insurance_superseded_mapping');
        }
        $multi_source=in_array($record_source,array(""")
    o=once(o,
        "$option='ppar_hab_rc31_tarifcheck_reconcile_v1';",
        "$option='ppar_hab_rc33_tarifcheck_reconcile_v1';")
    data[routing]=o.encode()

    m=data[main].decode()
    m=once(m,"Version: 0.1.28-rc31","Version: 0.1.30-rc33")
    # Full replacement of legacy SECOND content classifier (regex on labels,
    # network list, random special/general), not another new condition.
    # Only read the existing exact classification and checked target keys.
    authority=r'''    /**
     * The one existing import-time decision is authoritative for insurance.
     * Runtime neither reads banner titles for meaning nor selects a new topic.
     * Actual location + canonical stored target keys decide delivery.
     * Security of link/image, consent, manual veto and slot is separate.
     */
    private function hb_insurance_banner_rank($campaign,$context,$slot_type='') {
        if (!is_array($campaign)
            || sanitize_key((string)($campaign['creative_type']??''))!=='banner'
            || sanitize_key((string)($campaign['source']??''))!=='output_object_v4'
            || sanitize_key((string)($campaign['assignment_mode']??''))!=='page_tree'
            || strpos((string)($campaign['auto_topic_reason']??''),
                      'HB_INSURANCE_CANONICAL:hab_insurance_')!==0
            || empty($campaign['automation_target_keys'])
            || !method_exists($this,'automation_campaign_exact_target_rank')) return null;
        $ctx=$context;
        $ctx['slot_type']=$slot_type!=='' ? sanitize_key((string)$slot_type)
                                         : sanitize_key((string)($context['slot_type']??''));
        $rank=$this->automation_campaign_exact_target_rank($campaign,$ctx);
        return is_array($rank) ? $rank : null;
    }

    /** Thin compatibility gate; same ONE authoritative decision as ranking.
     * No separate title, vendor or family classifier remains in output.
     */
    private function hb_insurance_campaign_allowed($campaign, $context, $slot_type) {
        $scope=$this->hb_insurance_scope($context);
        if($scope==='other')return true;
        if($scope!=='insurance')return false;
        return is_array($this->hb_insurance_banner_rank($campaign,$context,$slot_type));
    }
'''
    m=replace_method(m,"hb_insurance_campaign_allowed",authority)
    # One real stored mapping, no second per-page title/topic selection.
    # Some historical upgrade steps rewrote the initial legacy guard, so
    # accept only the two EXACT known source forms; never guess an anchor.
    before_guard="""    private function campaign_match_rank($campaign, $context) {
        if (!$this->hb_insurance_campaign_allowed($campaign,$context,(string)($context['slot_type'] ?? ''))) { return null; }
        $mode ="""
    without_guard="""    private function campaign_match_rank($campaign, $context) {
        $mode ="""
    new_rank_head="""    private function campaign_match_rank($campaign, $context) {
        $hb_scope=$this->hb_insurance_scope($context);
        if($hb_scope==='mixed')return null;
        if($hb_scope==='insurance')return $this->hb_insurance_banner_rank($campaign,$context,(string)($context['slot_type']??''));
        $mode ="""
    if m.count(before_guard)==1:
        m=once(m,before_guard,new_rank_head)
    else:
        m=once(m,without_guard,new_rank_head)
    # Remove a historical exception that allowed banners outside the
    # one central Creative Library. Some later source versions already
    # carry the correct strict rule.
    old_exception="""            if ($required_type === 'banner' && $forced_campaign_id_norm === ''
                && (string)($runtime_campaign['source'] ?? '') !== 'output_object_v4'
                && !($this->hb_insurance_scope($rank_context)==='insurance'
                     && $this->hb_insurance_campaign_allowed($runtime_campaign,$rank_context,$slot_type))) { continue; }"""
    strict_central="""            if ($required_type === 'banner' && $forced_campaign_id_norm === ''
                && (string)($runtime_campaign['source'] ?? '') !== 'output_object_v4') { continue; }"""
    if m.count(old_exception)==1:
        m=once(m,old_exception,strict_central)
    else:
        assert m.count(strict_central)==1,"Central-source rule unexpectedly changed"
    # Remove remaining RC19 duplicate semantic selection that tried to prioritize
    # "all insurance" by reading title, on top of the canonical plan, if any.
    # Search & characterize in QA; no ungrounded regex deletions.
    data[main]=m.encode()

    rd=data[readme].decode()
    rd=once(rd,"Stable tag: 0.1.28-rc31","Stable tag: 0.1.30-rc33")
    data[readme]=rd.encode()
    changed={routing,main,readme}
    assert all(data[n]==z.read(n) for n in z.namelist() if n not in changed)
    out=BytesIO()
    with ZipFile(out,"w") as zz:
        for i in z.infolist():zz.writestr(i,data[i.filename])
    final=out.getvalue()
with ZipFile(BytesIO(final)) as verify:
    assert verify.testzip() is None and len(verify.namelist())==36
    assert b"HB_INSURANCE_CANONICAL:" in verify.read(main)
    assert b"HB_INSURANCE_CANONICAL:" in verify.read(routing)
    assert b"Version: 0.1.30-rc33" in verify.read(main)
P.write_bytes(final)
print("RC33_SINGLE_AUTHORITY_BUILD_PASS",len(final),sha256(final).hexdigest())
