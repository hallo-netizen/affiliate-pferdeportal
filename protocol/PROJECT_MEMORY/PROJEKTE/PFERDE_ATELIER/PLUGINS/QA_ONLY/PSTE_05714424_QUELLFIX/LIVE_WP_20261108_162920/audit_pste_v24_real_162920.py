from __future__ import annotations
import json, hashlib, collections, pathlib
P=pathlib.Path('/mnt/data/pferdeatelier-mini-ergebnisse-20261108-162920.json')
d=json.loads(P.read_bytes())
s=d['parkhaus_snapshot']; rows=s['items']; by={k:[x for x in rows if x.get('source')==k] for k in ['WORDPRESS','PSTE_PLAN','EDITORIAL_PLAN','PSERC_ACTIVE_PLAN','PPM679_EXISTING_EDITORIAL_RUNTIME','MINI_RESERVED']}
source_expected={'WORDPRESS':1024,'PSTE_PLAN':1,'EDITORIAL_PLAN':9,'PSERC_ACTIVE_PLAN':1,'PPM679_EXISTING_EDITORIAL_RUNTIME':144,'MINI_RESERVED':0}
assert len(rows)==1179 and {k:len(v) for k,v in by.items()}==source_expected
assert d['parkhaus_complete'] is False and s['complete'] is False and s['sha256']==''
assert s['reason']=='EDITORIAL_PLAN_UNRESOLVED:9;PPM679_RUNTIME_TITLE_UNRESOLVED:3'
assert len(d['seo_subjects'])==87 and collections.Counter(x['decision'] for x in d['items'])=={'JA':87,'VIELLEICHT':9,'NEIN':4}
ghost={'title':'Array','primary_longtail_query':'Array','category_name':'','intent_cluster_id':'','headings':[],'source_reference':''}
ghost_hash=hashlib.sha256(json.dumps(ghost,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
assert len(by['EDITORIAL_PLAN'])==9 and all(x['raw_record_sha256']==ghost_hash for x in by['EDITORIAL_PLAN'])
wpids={x['id'] for x in by['WORDPRESS']}; ppm=by['PPM679_EXISTING_EDITORIAL_RUNTIME']; orphan=[x for x in ppm if x['post_id'] not in wpids]
assert len(orphan)==3 and [x['post_id'] for x in orphan]==[972356,972414,972560]
assert sum(x['title_status']=='RESOLVED' for x in ppm)==141
assert all(x['title']=='' and x['title_status']=='UNRESOLVED_SOURCE_TITLE' for x in orphan)
assert len({x['canonical_article_id'] for x in ppm})==144
assert len({x['plan_slot'] for x in ppm})==144
report={
 'scope':'READ_ONLY_FORENSIC_AUDIT_FROM_ACTUAL_WORDPRESS_V24_EXPORT',
 'input_file':P.name,
 'input_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),
 'size_bytes':P.stat().st_size,
 'generated_from':d['created_utc'],
 'contract':d['contract'],
 'keywords':dict(collections.Counter(x['decision'] for x in d['items'])),
 'seo_subjects':len(d['seo_subjects']),
 'parkhaus_items':len(rows),
 'sources_item_count':source_expected,
 'parkhaus_complete':s['complete'],
 'approval_sha256':s['sha256'],
 'diagnostic_sha256':s['diagnostic_sha256'],
 'reason':s['reason'],
 'source_editorial_legacy_ghosts':{'count':9,'all_identical':True,'reconstructed_exact_source_row':ghost,'reconstructed_source_sha256':ghost_hash,'has_real_article_title':False,'has_article_id':False,'has_plan_slot':False,'has_source_reference':False},
 'source_ppm679':{'count':144,'resolved_article_titles':141,'unresolved_references':[{k:r.get(k) for k in ['canonical_article_id','plan_slot','post_id','status','post_status','title_status']} for r in orphan],'canonical_ids_unique':True,'slots_unique':True},
 'safety':{'eligible_for_external_free_approval':False,'current_snapshot_reference_is_diagnostic_only':True,'do_not_use_diagnostic_hash_for_import':True,'do_not_delete_orphan_slot_reservations':True,'no_live_database_access_in_this_audit':True},
 'provenance_limit':'The exported editorial rows do not identify whether they came from the stored PSTE option or a third-party WordPress filter. No original title data can be reconstructed from nine literally identical rows. PPM679 unresolved posts were not returned by the live v24 reader; no proof of past deletion beyond absent current lookup.',
}
out=pathlib.Path('/mnt/data/PSTE_V24_ECHTEXPORT_162920_AUDIT.json');out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');
print(out)
print(json.dumps({k:report[k] for k in ['input_sha256','parkhaus_items','parkhaus_complete','reason','source_editorial_legacy_ghosts','source_ppm679']},ensure_ascii=False,indent=2))