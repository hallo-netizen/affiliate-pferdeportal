#!/usr/bin/env python3
"""Read-only acceptance ledger from real eBay run exports and the full QA 6.72.346 ZIP.
No WordPress mutation, no API calls, no simulated positive business results.
"""
import csv, json, pathlib, hashlib, zipfile, collections, datetime
D=pathlib.Path('/mnt/data'); O=D/'ebay_gesamtvertrag'; O.mkdir(exist_ok=True)
runfile=D/'pferdeatelier-ebay-lauf-574cb003b132.csv'
gapfile=D/'Pferdeatelier_eBay_fehlende_Produktfamilien_97507628-4f4.csv'
zipfile_path=D/'Affiliate_6.72.346_EBAY_GESAMTWORKFLOW_TEST.zip'
with runfile.open(encoding='utf-8-sig', newline='') as f: run=list(csv.DictReader(f,delimiter=';'))
with gapfile.open(encoding='utf-8-sig', newline='') as f: gaps=list(csv.DictReader(f,delimiter=';'))
assert run and gaps
last=run[-1]; uuids=set(r['run_uuid'] for r in run)
assert len(uuids)==1, 'Run export must not combine different runs'
assert all(x['run_uuid']==last['run_uuid'] for x in gaps), 'Gap export must be same run'
assert int(last['covered'])+len(gaps)==int(last['required']), 'Missing-family accounting conflict'
assert len(set(x['familien_id'] for x in gaps))==len(gaps), 'duplicate missing families'
assess=collections.Counter(x['bewertung'] for x in gaps)
accepted=[x for x in gaps if int(x['davon_angenommen'] or 0)>0]
not_searched=[x for x in gaps if int(x['anfragen'] or 0)==0]
no_accepted=[x for x in gaps if int(x['anfragen'] or 0)>0 and int(x['davon_angenommen'] or 0)==0]
assert len(gaps)==len(accepted)+len(not_searched)+len(no_accepted)
with zipfile.ZipFile(zipfile_path) as z:
    crc=z.testzip();names=z.namelist();run_trait=z.read('affiliate-portal-router/includes/trait-ppar-ebay-run.php').decode();ebay_trait=z.read('affiliate-portal-router/includes/trait-ppar-ebay.php').decode()
    catalog=json.loads(z.read('affiliate-portal-router/assets/ebay-portal-catalog-v2.json'))
    plugin=z.read('affiliate-portal-router/pferdeportal-affiliate-router.php').decode()
assert crc is None and len(names)==66
required=catalog['business_supply_contract']['required_count']-len(catalog['ebay_non_goods_concept_ids'])
assert required==int(last['required'])
assert all(x['familien_id'] in set(catalog['business_supply_contract']['required_product_concept_ids']) for x in gaps)
assert 'ebay_business_recheck_selected_stale_source' in ebay_trait
assert 'ebay_public_checkpoint_save' in run_trait and 'ebay_run_commit_public_checkpoint' in run_trait
assert 'ebay_run_finish_requested_stop' in run_trait and 'ebay_run_resume_operator_stop' in run_trait
assert 'ebay_run_tick_gapfill' in run_trait and 'ebay_run_tick_gapfill_select' in run_trait
assert 'ebay_external_tick_due_operation' in run_trait and 'run_ebay_canonical_worker' in run_trait
assert '6.72.346' in plugin

def n(key):return int(last[key] or 0)
# One result per end-to-end gate. UNKNOWN never means PASS.
gates=[
 {'gate':'Katalog/Sollfamilien','state':'PASS','evidence':f'Katalog {required}; echter Lauf {n("required")} Pflichtfamilien; {len(gaps)} fehlend'},
 {'gate':'Ein einziger verlässlich ankommender GitHub-Arbeitsaufruf','state':'NICHT NACHGEWIESEN','evidence':'Main-Workflow */15 + Selbstverkettung; beobachtete ausgefallene geplante Starts nach 10:25; PR 759 blockiert'},
 {'gate':'Lauf und Cursor ohne Nullsetzung weiterbearbeitet','state':'NICHT ABGENOMMEN','evidence':f'Original CSV: {last["status"]}/{last["phase"]} Fortschritt {n("progress_seq")}; letzter Nutzerstand Schritt 475, später PAUSIERT'},
 {'gate':'Individuell passende Quellen recherchiert','state':'OFFEN','evidence':f'{len(not_searched)} fehlende Familien ohne zugeordneten Einzelabruf IM AKTUELLEN SUCHTEIL; {len(no_accepted)} abgefragt ohne angenommenes Angebot'},
 {'gate':'Nur einmalige Produkt-/Familienentscheidung','state':'NUR LOKAL GEPRUEFT','evidence':'QA54: eine Planner-Entscheidung je Produkt/Portal/Durchgang; reale WordPress-Daten nicht gegengeprüft'},
 {'gate':'Ausgewählte Produkte aktuell und veröffentlicht','state':'NICHT BESTANDEN IM REALEN EXPORT','evidence':f'{n("selection_scanned")} geprüft, {n("selection_materialized")} materialisiert, {n("skipped_item_errors_count")} übersprungen; QA58-Mockfix noch nicht im echten Lauf nachgewiesen'},
 {'gate':'Angenommene Angebote erklären die Abdeckung','state':'NICHT BESTANDEN IM REALEN EXPORT','evidence':f'{len(accepted)} fehlende Familien hatten angenommene Angebote im Suchteil; dennoch keine Abdeckung'},
 {'gate':'Alte nachweislich gültige Produkte bleiben erhalten','state':'NICHT LIVE VERIFIZIERT','evidence':'578 gespeicherte Freigaben in WordPress-Oberfläche; kein vollständiger echter Source/Creative/Frontend-Abgleich'},
 {'gate':'Öffentliche Abdeckung und HivePress-Ausgabe','state':'NICHT BESTANDEN IM REALEN EXPORT','evidence':f'{n("covered")}/{required} Familien im gespeicherten geprüften Kandidatenstand; öffentliche Seiten nicht endabgenommen'},
 {'gate':'Protokolle dauerhaft gespeichert','state':'FEHLER IM LIVE-SCREENSHOT','evidence':'WordPress meldet fehlgeschlagenen Protokoll-Speichervorgang; Export kann historische Einträge enthalten, aber nicht vollständig'},
 {'gate':'Vollständiger Abschluss und sicherer Folgestart','state':'NICHT ABGENOMMEN','evidence':f'Der echte Export endet {last["status"]}/{last["phase"]}, nicht completed; QA63 Abschlussfrist nur lokal getestet'},
 {'gate':'Keine schädliche PRIVATE-/Fremdanbieter-Veröffentlichung','state':'NICHT LIVE ABGENOMMEN','evidence':'QA29 PRIVATE-Altlasten-Livebereinigung gescheitert; spätere lokale KISS-Prüfungen ersetzen keine öffentliche Kontrolle'},
]
report={
 'title':'Ebay Gesamtabnahme nach historischen Fehlern QA27–QA65',
 'run_uuid':last['run_uuid'],
 'original_csv':runfile.name,'original_events':len(run),
 'original_last':{k:last[k] for k in ['status','phase','progress_seq','transport_ticks','selection_scanned','selection_materialized','skipped_item_errors_count','covered','required','search_found','search_accepted']},
 'real_missing_csv':gapfile.name,'missing_count':len(gaps),
 'missing_breakdown':{'no_related_individual_query_in_current_partial_section':len(not_searched),'accepted_but_still_uncovered':len(accepted),'queries_but_no_accepted_offer':len(no_accepted)},
 'historical_issues':[
 {'qa':'27–31,39–43,55,59–65','issue':'GitHub-Wecksignal, REST-Status, Stopp/Fortsetzen, scheinbar aktiver Lauf','result':'Einmalige Tick-Verarbeitung lokal geprüft; regelmäßige reale Zustellung NICHT abgenommen; Main unverändert, PR #759 geschützt'},
 {'qa':'36–41','issue':'Familienkapazität stoppt kompletten Lauf; alte Fehlerläufe nicht wieder aufgenommen','result':'Lokal korrigiert; aktuelle sichere Produktabdeckung nicht bewiesen'},
 {'qa':'48–50','issue':'Gapfill entfernt vorherige Kandidaten, Abschluss/Cleanup konnte 482 von 578 SAFE-IDs verlieren','result':'Lokal korrigiert, QA50 Mock 578→580; echter öffentlicher Bestand nicht gemessen'},
 {'qa':'51–54','issue':'Doppelte Partner-/Portalentscheidungen, unterschiedliche Produktbestandslisten, Verfügbarkeitsworker trifft Fachentscheidung','result':'Lokal vereinheitlicht, Safe-Checkpoint-CAS; realer Gesamtbestand nicht abgenommen'},
 {'qa':'56–58','issue':'Nur 5/283 nach vielen Ticks, 153 abgelaufene ausgewählte Produkte','result':'Lokale gezielte getItem-Neubestätigung; echter Export weiterhin 153 skips'},
 {'qa':'63','issue':'Teilrecherche-Ende fälschlich statt Gesamtabschluss als Startuhr','result':'Lokal korrigiert, kein abgeschlossener Live-Gesamtlauf'},
 {'qa':'29','issue':'PRIVATE-Altanzeigen-Livebereinigung gescheitert','result':'Keine bestätigte Live-Endabnahme'},
 {'qa':'laufender Screenshot','issue':'Audit-Speichervorgang fehlgeschlagen','result':'Weiterhin im WordPress-Screenshot gemeldet'},
 ],
 'code':{'package':zipfile_path.name,'sha256':hashlib.sha256(zipfile_path.read_bytes()).hexdigest(),'crc':'PASS','php_files':sum(x.endswith('.php') for x in names),'zip_files':len(names)},
 'gates':gates,
 'full_contract_accepted':all(g['state']=='PASS' for g in gates),
 'important':'QA63 130/130 testet simulierte WP-/eBay-Antworten. Dieser Report ist ein echter Evidenzabgleich und KEIN neuer erfolgreicher Live-Lauf.',
}
(O/'EBAY_GESAMTABNAHME_ERGEBNIS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['# eBay: ein Gesamtabnahmevertrag gegen alle dokumentierten Fehler (QA27–QA65)','',
'**Gesamturteil: NICHT BESTANDEN.** Keine weitere Testzählung wird als Live-Lösung bezeichnet.','',
'## Echte Daten',f'- Ein Run {last["run_uuid"]}: {len(run)} Originalereignisse, zuletzt {last["status"]}/{last["phase"]}, {n("covered")}/{required} Familien.',
 f'- Auswahl: {n("selection_scanned")} geprüft, {n("selection_materialized")} materialisiert, {n("skipped_item_errors_count")} übersprungen.',
 f'- Fehlende {len(gaps)} Familien: {len(not_searched)} im aktuellen Suchteil ohne Einzelabruf, {len(accepted)} mit angenommenen Angeboten aber ohne Abdeckung, {len(no_accepted)} mit Abrufen ohne Annahme.',
 '- 578 bisherige Freigaben sind nach dem WordPress-Screenshot gespeichert, aber NICHT mit aktuell gültigen sichtbaren Angeboten gleichzusetzen.',
 '', '## Abgleich gegen die historische Fehlerliste']
for g in report['historical_issues']:
 lines.append(f'- **QA {g["qa"]}:** {g["issue"]}. **Stand:** {g["result"]}.')
lines+=['','## EIN verbindlicher Gesamtabnahmetest (keine unabhängigen Erfolgsbehauptungen)','', '| Teil des Gesamtworkflows | Stand | Beweis |','|---|---|---|']
for g in gates:lines.append(f'| {g["gate"]} | **{g["state"]}** | {g["evidence"]} |')
lines+=['','## Konsequenz','- Ein vorhandener GitHub-Aufruf muss einen gespeicherten kanonischen Lauf nachweislich voranbringen (oder korrekt pausieren), ohne neue Suche/Cursor-Reset.',
'- eBay-Suche, Produktwahl, aktuelle Angebotsprüfung, einheitliche SAFE-Freigabe, veröffentlichte HivePress-Ausgabe und Bereinigung müssen mit denselben echten WordPress-Produkten bis zum terminalen Ende geprüft werden.',
'- Für fehlende Familien muss die ECHTE Quelle einer von drei Befunden zugeordnet sein: kein zugeordneter Suchlauf, Suche ohne brauchbaren Treffer, Treffer ohne Publikationsnachweis. Kein unbelegter „Markt leer“-Abschluss.',
'- Jede einzelne fachliche Prüfung hat genau einen Besitzer; GitHub weckt nur, der kanonische WordPress-Lauf steuert, die öffentliche Freigabe wird einmal festgelegt, die Aktualitätsarbeit ändert keine Kategorie/Produktfamilie.',
'- Weder ältere SAFE-Kampagnen noch die Lauf-ID oder Cursor dürfen bei fehlerhaften Teilantworten gelöscht werden. Kein neuer Pluginstand auf Grundlage nur synthetischer 130/130-Ticks.',
'', '## Quellen und Nachweisgrenze', f'- `{runfile.name}` (Originalexport), `{gapfile.name}` (Originalfehlfamilien), `{zipfile_path.name}` (gepackter Originalcode; SHA256 `{report["code"]["sha256"]}`).',
'- GitHub Änderungsregister QA27–QA65 und echte Heartbeat-Jobs (u.a. Run 43580485610, 43568795402).',
'- Die WordPress-Datenbank, eBay-API und öffentlichen Produktseiten wurden durch diese Prüfung NICHT verändert oder live neu abgenommen.',
'']
(O/'EBAY_GESAMTABNAHME_FEHLERABGLEICH.md').write_text('\n'.join(lines),encoding='utf-8')
print('LIVE_GESAMTVERTRAG_PASS',report['full_contract_accepted']);print('EVIDENZ',len(run),'events',n('covered'),'/',required,'covered',len(gaps),'missing');print('LUECKEN',report['missing_breakdown']);print('GESAMTABNAHME_GATE_STATES',collections.Counter(g['state'] for g in gates));print('REPORTS',O)