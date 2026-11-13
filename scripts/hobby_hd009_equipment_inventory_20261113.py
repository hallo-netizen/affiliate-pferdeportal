#!/usr/bin/env python3
"""Read-only, literal equipment inventory across the source Hobby Depot registry.

No guessed purchaseability, no assumed per-hobby coverage (iPN WordPress data
is private). No plugin changes. No generic keyword as proof of product suitability.
"""
import csv
import collections
import hashlib
import json
import re
import zipfile
from pathlib import Path

root=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH')
base=root/'PLUGINS/ISOLIERTE_PLUGINS'
hd007=base/'HD-007-HOBBYREGISTER-CORE/CURRENT.zip'
hd009=base/'HD-009-AFFILIATE-ZENTRALE/CURRENT.zip'
assert hashlib.sha256(hd007.read_bytes()).hexdigest()=='ba838946d5b04a5f31f92bc993aba69a924250cbd78bd6beb6a52ed32144ec4f'
assert hashlib.sha256(hd009.read_bytes()).hexdigest()=='b6482b5d880e941c97ac726dffa85fbc46ba8514587e23700951d176ebcb63db'
with zipfile.ZipFile(hd007) as z:
    reg=json.loads(z.read('hd-hobbyregister-core/data/hobby-register.json'))
records=reg['records']
assert len(records)==862
terminal=[r for r in records if r.get('source_identity',{}).get('current_terminal_hobby_page') is True]
assert len(terminal)==381,('Terminal source count differs',len(terminal))

# These labels describe the quality of the FIRST literal noun phrase only.
# Generic does NOT mean an ineligible hobby or no buyable products.
generic={
'platz','sichere aufbewahrung','regalplatz','aufbewahrung','arbeitsfläche','werkstatt',
'geduld','zeit','zugang','wasser','holz','papier','karton','werkzeug','werkzeuge',
'kleber','farbe','farben','schere','scheren','messer','lupe','computer','kamera',
'stoffe','stoff','erde','licht','luft','material','metallringe','bogen',
'substrat','geeignetes substrat','pflanzen','pflanze','kleine pflanzen','rohmaterial',
'grundmaterial','filament','saatgut','tisch','regal','handwerkzeug',
'pflege','futter','spiegel','hilfsmittel','zubehör',
}
negexpr=re.compile(r'\b(?:geduld|zeit|platz|arbeitsfläche|arbeitsplatz|kenntnisse|erfahrung|zugang|wetter|erlaubnis|erlaubten|geeignet|sicher|freie|kosten|je nach|optional|ausreichend)\b',re.I)
rows=[];quality=collections.Counter();worlds=collections.Counter();primitives=collections.Counter();candidate_terms=collections.Counter()
for r in terminal:
    name=r['canonical_name']
    nid=r['registry_id']
    sid=r.get('source_identity') or {}
    need=str((r.get('result_profile') or {}).get('what_do_you_need') or '')
    assert need.strip(),('Missing equipment field',name)
    # Never use free-form second/third equipment automatically.
    first=re.split(r'[,;]',need,1)[0].strip().strip('.')
    first_l=first.lower()
    parts=re.split(r',|;|\bund\b|\boder\b',need)
    parts=[x.strip().strip('.') for x in parts if x.strip().strip('.')]
    # Informational assessment only; not an active keyword decision.
    if not first or first_l in generic or negexpr.search(first):
        label='Erste Angabe allgemein – Ausrüstung gesondert prüfen'
        quality['first_generic']=quality['first_generic']+1
    else:
        label='Erste Angabe konkret – Produktprüfung nötig'
        quality['first_concrete']=quality['first_concrete']+1
    quality['has_need']+=1
    world=sid.get('natural_world') or 'ohne Weltangabe'
    worlds[world]+=1
    primitives[first_l]+=1
    if label.startswith('Erste Angabe konkret'):
        candidate_terms[first_l]+=1
    rows.append({
        'Hobby':name,'Registry ID':nid,'Welt':world,
        'Erste Ausrüstungsangabe':first,'Weitere Ausrüstungsangaben':' | '.join(parts[1:]),
        'Originalwortlaut Bedarf':need,'Vorprüfung':label,
        'Status Idealo 2747 am Hobbyziel':'nicht einzeln prüfbar – keine private Feed-/WordPress-Zielliste',
        'Nächster Prüfpunkt':'Mit echten Idealo-Produktdaten und eindeutigem Ziel vergleichen'
    })
out=root/'AFFILIATE/EVIDENCE'
out.mkdir(parents=True,exist_ok=True)
csvpath=out/'HD009_HOBBYREGISTER_AUSRUESTUNGSINVENTUR_381_20261113.csv'
with csvpath.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]))
    w.writeheader();w.writerows(rows)
summary={
'run_date':'2026-11-13',
'exact_plugin_source_sha256':{
  'HD007':hashlib.sha256(hd007.read_bytes()).hexdigest(),
  'HD009':hashlib.sha256(hd009.read_bytes()).hexdigest()},
'registry_all_entries':len(records),'terminal_hobby_entries':len(terminal),
'terminal_with_equipment':quality['has_need'],
'first_equipment_descriptive_precheck':{
  'concrete_needs_product_review':quality['first_concrete'],
  'generic_needs_product_review':quality['first_generic'],
  'note':'These are only literal wording observations, NOT a purchaseability/exclusion decision'},
'by_natural_world':dict(sorted(worlds.items())),
'most_common_first_terms':primitives.most_common(25),
'concrete_first_ambiguous_frequency':[(k,v) for k,v in candidate_terms.most_common(30) if v>1],
'live_wp_evidence_20261112':{
  'idealo_feed':2747,
  'feed_description':'Fashion, Sport, Outdoor, shown in publisher iPN portal',
  'api_feed_products_at_last_check':543676,
  'staged_products':2530,'pass_products':2530,'warn':0,
  'materialized_cards':429,'mapped_targets':52,
  'total_terminal_hobbies':381,
  'interpretation':'Neither per-hobby matched list nor broad feed 2901 is available to this offline code audit; do not infer which of the 329 remaining hobbies are unsuitable vs absent from 2747 vs unmatched by keywords'},
'prohibited_inference':'No per-hobby coverage computed from the 52 aggregate. No universal product suitability claim. No automatic choice of generic later gear.',
'next_evidence':'Compare existing provider feed 2747 and a permitted standard feed 2901 using the same existing import checks and same HD009 matcher before raising keyword matching breadth; protect feed/adspace provenance.'
}
jsonpath=out/'HD009_HOBBYREGISTER_AUSRUESTUNGSINVENTUR_SUMMARY_20261113.json'
jsonpath.write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print('VERIFIED_COUNTS',json.dumps({k:v for k,v in summary.items() if k in ['registry_all_entries','terminal_hobby_entries','terminal_with_equipment','first_equipment_descriptive_precheck','by_natural_world']},ensure_ascii=False))
print('COMMON_FIRST',summary['most_common_first_terms'])
print('CSV',csvpath,'ROWS',len(rows))
print('JSON',jsonpath)
for name in ['Kettenhemdflechten','Münzen','Buchbinden','3D-Druck','Airbrush']:
    for r in rows:
        if r['Hobby']==name: print('EXAMPLE',json.dumps(r,ensure_ascii=False)[:1400]);break
