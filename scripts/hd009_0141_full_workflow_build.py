#!/usr/bin/env python3
"""One consolidated HD009 release candidate: refresh the ONE matching decision.

Keep original full ZIP, original import/materializer and provider order. Make the
existing worker automatically recompute data after a rule change, including when
the upstream idealo file did not change. Preserve last-good with a single
existing activation gate until the recomputation actually succeeds.
"""
from pathlib import Path
from zipfile import ZipFile
import hashlib,io,sys

src=Path(sys.argv[1]);dest=Path(sys.argv[2])
sha=lambda x:hashlib.sha256(x).hexdigest()
assert sha(src.read_bytes())=="6ac221827ebd74e19a209198b5a04129527ca442a5f47871041754a85f1549c9", "Wrong complete 0.1.40 base"
trait="affiliate-portal-router/includes/trait-ppar-idealo.php"
main="affiliate-portal-router/hobby-depot-affiliate-router.php"
with ZipFile(src) as z:
    assert z.testzip() is None and len(z.namelist())==41
    entries=z.infolist()
    files={item.filename:z.read(item.filename) for item in entries}
s=files[trait].decode("utf-8")
def only(old,new,label):
    global s
    assert s.count(old)==1, f"{label}: expected 1, found {s.count(old)}"
    s=s.replace(old,new,1)
def edit_method(start_name,next_name,change):
    global s
    beg=s.index(start_name);end=s.index(next_name,beg+len(start_name))
    old=s[beg:end]
    new=change(old)
    assert new!=old,(start_name,"No modification")
    s=s[:beg]+new+s[end:]
def inside_once(old,new,label):
    assert old.count(label)==0 if False else True
    assert old.count(old)==0 if False else True
    return new

# One central rule revision identifier for both initial validity and updates.
only("    private function idealo_match_index() {",
     """    /** Existing Idealo matcher is the ONLY semantic eligibility authority. */
    private function idealo_match_contract_revision() {
        return 'hd009-match-0.1.41';
    }

    private function idealo_match_index() {""",
     "single matching revision")

# Contextual 'related' goods MUST share the same original negative-marker rule,
# instead of skipping it on the positive category+equipment path.
def edit_context(block):
    marker="""        if ($this->idealo_match_blocked($full, $catalog)) { return 0; }
"""
    assert block.count(marker)==1, "Original context negative marker not found"
    return block.replace(marker,"",1)
edit_method("    private function idealo_match_context_score(",
            "    /** Conservative one-row matcher:",edit_context)
def edit_match(block):
    old="""        $category_stems=array(); foreach ($this->idealo_match_tokens($main_n.' '.$sub_n) as $token) { $category_stems[]=$this->idealo_match_stem($token); }"""
    assert block.count(old)==1
    new="""        // A single negative decision happens here for ALL eligible routes.
        // No separate later judgement at output or in comparison workers.
        if ($this->idealo_match_blocked($title_n.' '.$main_n.' '.$sub_n,$mi['catalog'])) {
            return array('status'=>'context_rejected');
        }
"""+old
    return block.replace(old,new,1)
edit_method("    private function idealo_match_feed_row_to_concept(",
            "    public function idealo_provider_access_snapshot(",edit_match)

# Existing activation gate only admits products after the upgraded once-only
# matching rule has been run on real feed rows; no topical decision here.
def edit_activation(block):
    old="""        return !empty($s['enabled']) && $this->idealo_credentials_present($s)
"""
    new="""        return !empty($s['enabled']) && $this->idealo_credentials_present($s)
            && (string)($s['last_match_revision']??'')===$this->idealo_match_contract_revision()
"""
    assert block.count(old)==1
    return block.replace(old,new,1)
edit_method("    private function idealo_campaigns_should_be_active(",
            "    public function idealo_campaign_publicly_allowed(",edit_activation)

# The existing real import first makes the ONE decision and stages it, then
# publishes materialized records. Marker is switched before materializer so
# the existing active calculation remains true; rollback on failure.
def edit_import(block):
    old="""        $settings['last_message']=sprintf("""
    new="""        $old_match_revision=(string)($settings['last_match_revision']??'');
        $settings['last_match_revision']=$this->idealo_match_contract_revision();
        $settings['last_message']=sprintf("""
    assert block.count(old)==1
    block=block.replace(old,new,1)
    old="""        $materialized=$this->idealo_materialize_campaigns(); $settings=$this->idealo_settings();
"""
    new="""        $materialized=$this->idealo_materialize_campaigns(); $settings=$this->idealo_settings();
        if (is_wp_error($materialized)) {
            $settings['last_match_revision']=$old_match_revision;
            update_option(self::OPTION_NETWORK_IDEALO,$settings,false);
            $this->idealo_sync_campaign_activation();
            return $materialized;
        }
"""
    assert block.count(old)==1
    return block.replace(old,new,1)
edit_method("    private function idealo_import_feed_file(",
            "    private function idealo_target_keys_for_product_slug(",edit_import)

# An unchanged file is NOT proof that a new matcher has run. Bypass the remote
# hash and HTTP etag exactly once when the rule revision changes; after a
# successful re-import the revision is recorded by the original importer.
def edit_refresh(block):
    old="""        $s=$this->idealo_settings();
        if ($metadata_first) {"""
    new="""        $s=$this->idealo_settings();
        $rematch_required=(string)($s['last_match_revision']??'')!==$this->idealo_match_contract_revision()
            || (string)($s['last_import_feed_id']??'')!==(string)($s['feed_id']??'')
            || (string)($s['last_import_adspace_id']??'')!==(string)($s['adspace_id']??'');
        if ($metadata_first) {"""
    assert block.count(old)==1
    block=block.replace(old,new,1)
    old="""if (!empty($s['last_remote_file_hash']) && $s['last_remote_file_hash']===(string)($metadata['last_file_hash']??'') && absint($s['last_import_at']??0)>0) { return array('status'=>'unchanged','message'=>'Feed-Hash unverändert; kein Download.'); }"""
    new="""if (!$rematch_required && !empty($s['last_remote_file_hash']) && $s['last_remote_file_hash']===(string)($metadata['last_file_hash']??'') && absint($s['last_import_at']??0)>0) {
                $s['last_import_at']=time(); // unchanged feed was confirmed fresh, not missing
                update_option(self::OPTION_NETWORK_IDEALO,$s,false);
                return array('status'=>'unchanged','message'=>'Feed unverändert und aktuell bestätigt.');
            }"""
    assert block.count(old)==1
    block=block.replace(old,new,1)
    old="""        $download=$this->idealo_download_feed_to_temp($s); if (is_wp_error($download)) { return $download; }"""
    new="""        $download_settings=$s;
        if ($rematch_required) {
            // Never get HTTP 304 when a new rule needs EVERY original feed row.
            $download_settings['feed_etag']='';
            $download_settings['feed_last_modified']='';
        }
        $download=$this->idealo_download_feed_to_temp($download_settings); if (is_wp_error($download)) { return $download; }"""
    assert block.count(old)==1
    block=block.replace(old,new,1)
    old="""        if (($download['status']??'')==='not_modified') { $s['feed_etag']=(string)($download['etag']??$s['feed_etag']); $s['feed_last_modified']=(string)($download['last_modified']??$s['feed_last_modified']); update_option(self::OPTION_NETWORK_IDEALO,$s,false); return array('status'=>'unchanged','message'=>'HTTP 304: Feed unverändert.'); }"""
    new="""        if (($download['status']??'')==='not_modified') {
            if ($rematch_required) { return new WP_Error('idealo_rematch_requires_feed','Produktregeln geändert: kompletter Feed erforderlich, 304 reicht nicht.'); }
            $s['feed_etag']=(string)($download['etag']??$s['feed_etag']);
            $s['feed_last_modified']=(string)($download['last_modified']??$s['feed_last_modified']);
            $s['last_import_at']=time();
            update_option(self::OPTION_NETWORK_IDEALO,$s,false);
            return array('status'=>'unchanged','message'=>'Feed unverändert und aktuell bestätigt.');
        }"""
    assert block.count(old)==1
    return block.replace(old,new,1)
edit_method("    private function idealo_refresh_remote_feed(",
            "    public function idealo_sync_dispatch(",edit_refresh)

# Reuse the one existing background worker when the active installation has
# earlier-matched rows. One attempt per 12h on failure, no repeated fetches.
def edit_schedule(block):
    old="""        $s=$this->idealo_settings(); $wanted=!empty($s['auto_refresh'])&&$this->hd_idealo_feed_source_ready($s);
        $next=wp_next_scheduled(self::IDEALO_REFRESH_HOOK);"""
    new="""        $s=$this->idealo_settings(); $source_ready=$this->hd_idealo_feed_source_ready($s);
        $wanted=!empty($s['auto_refresh'])&&$source_ready;
        $needs_rule_refresh=!empty($s['enabled']) && $source_ready && absint($s['last_import_at']??0)>0
            && ((string)($s['last_match_revision']??'')!==$this->idealo_match_contract_revision()
                || (string)($s['last_import_feed_id']??'')!==(string)($s['feed_id']??'')
                || (string)($s['last_import_adspace_id']??'')!==(string)($s['adspace_id']??''));
        if ($needs_rule_refresh && function_exists('wp_schedule_single_event')
            && !wp_next_scheduled(self::IDEALO_MANUAL_REFRESH_HOOK)
            && (time()-absint($s['match_rebuild_requested_at']??0))>=12*HOUR_IN_SECONDS) {
            wp_schedule_single_event(time()+60,self::IDEALO_MANUAL_REFRESH_HOOK);
            $s['match_rebuild_requested_at']=time();
            update_option(self::OPTION_NETWORK_IDEALO,$s,false);
        }
        $next=wp_next_scheduled(self::IDEALO_REFRESH_HOOK);"""
    assert block.count(old)==1
    return block.replace(old,new,1)
edit_method("    public function idealo_ensure_refresh_schedule(",
            "    private function idealo_refresh_lock_acquire(",edit_schedule)

files[trait]=s.encode("utf-8")
m=files[main].decode("utf-8")
# Both placement and thematic acceptance have exactly one authority:
# feed matcher for product identity; standard campaign_match_rank for placement.
# Remove a second late Idealo-specific page gate from the cached render path.
old_late="""            if (!$this->hd_idealo_product_targets_exact_hobby_page($campaign, $rank_context, $slot_type)) {
                continue;
            }
"""
marker="if (!$this->hd_idealo_product_targets_exact_hobby_page("
assert m.count(marker)==1,"Expected exactly one duplicate target check"
pos=m.index(marker)
line_start=m.rfind("\n",0,pos)+1
continue_pos=m.index("continue;",pos)
closing_line_end=m.index("\n",m.index("\n",continue_pos)+1)+1
removed_block=m[line_start:closing_line_end]
assert removed_block.count("continue;")==1 and "}" in removed_block,removed_block
m=m[:line_start]+m[closing_line_end:]
begin=m.index("    private function hd_idealo_product_targets_exact_hobby_page(")
end=m.index("    private function category_product_shared_rank_base(",begin)
assert "private function hd_idealo_product_targets_exact_hobby_page(" in m[begin:end]
m=m[:begin]+m[end:]
if "hd_idealo_product_targets_exact_hobby_page" in m:
    for i,line in enumerate(m.splitlines()):
        if "hd_idealo_product_targets_exact_hobby_page" in line:
            print("REMAINING_LATE_CALL",i,repr("\\n".join(m.splitlines()[max(0,i-3):i+5])))
    raise AssertionError("Old late target method still referenced")

# The original single campaign placement resolver is now the only exact
# Idealo page-slot decision, using the already stored target keys.
first=m.index("    private function campaign_match_rank(")
last=m.index("    private function get_content_context(",first)
rank=m[first:last]
spot="        $glossary_single_banner = $required_creative_type === 'banner'"
assert rank.count(spot)==1
early=r"""        // Idealo feed products are bound ONCE to targets at import.
        // On a hobby page, only its exact stored page key may fill product
        // slots. Other networks keep their original rank rules untouched.
        if ($required_creative_type==='product'
            && preg_match('/^category_product_[123]$/',$slot_type)
            && $context_post_type==='page'
            && sanitize_key((string)($campaign['network']??''))==='idealo'
            && sanitize_key((string)($campaign['source']??''))==='idealo_product_feed_v1') {
            $slug=sanitize_title((string)($context['primary_slug']??''));
            return $slug!=='' && in_array('page:'.$slug,(array)($campaign['automation_target_keys']??array()),true)
                ? array('specificity'=>500,'matches'=>1,'reason'=>'Gespeichertes genaues Idealo-Hobbyziel.')
                : null;
        }

"""
rank=rank.replace(spot,early+spot,1)
# Prevent the global ANY-article Idealo fallback from bypassing the
# single imported topic decision. eBay's longstanding fallback is unchanged.
old_fallback=r"""            $verified_idealo = $provider === 'idealo'
                && $source === 'idealo_product_feed_v1'
                && sanitize_key((string)($campaign['product_identity_source'] ?? '')) === 'gtin'
                && !empty($campaign['product_gtins']);
            if ($verified_ebay || $verified_idealo) {"""
new_fallback="""            if ($verified_ebay) {"""
assert rank.count(old_fallback)==1,"Generic article fallback changed"
rank=rank.replace(old_fallback,new_fallback,1)
m=m[:first]+rank+m[last:]
assert m.count("Version: 0.1.40")==1
m=m.replace("Version: 0.1.40","Version: 0.1.41",1)
files[main]=m.encode("utf-8")
with ZipFile(src) as z:
    modified=[n for n in files if files[n]!=z.read(n)]
    assert set(modified)=={trait,main}, modified
stream=io.BytesIO()
with ZipFile(stream,"w") as z:
    for item in entries: z.writestr(item,files[item.filename])
dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_bytes(stream.getvalue())
with ZipFile(dest) as z:
    assert z.testzip() is None
    assert len(z.namelist())==41
    assert b"Version: 0.1.41" in z.read(main)
    assert b"hd009-match-0.1.41" in z.read(trait)
    assert b"hd_idealo_category_title_relevant" not in z.read(main)
print("HD009_0141_FULL_SHA256",sha(dest.read_bytes()),"BYTES",dest.stat().st_size,"CHANGED",modified)
