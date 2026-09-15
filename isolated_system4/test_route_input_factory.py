from __future__ import annotations
import copy, hashlib, json, threading, zipfile
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import sys

import chat_start_gate, production_checks, source_acquisition

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
PPM=REPO/production_checks.PPM_PACKAGE_REL
G9_MEMBER='portal-production-machine/contracts/g9-single-faq-approved-candidate-v1.json'

SCENARIOS=[
 {
  'title':'Warum sollte der Reifendruck am Pferdeanhänger vor der Fahrt geprüft werden?',
  'keyword':'Reifendruck am Pferdeanhänger',
  'slug':'reifendruck-pferdeanhaenger',
  'intent_terms':['Reifendruck','Reifen','Pferdeanhänger','Fahrt','Kontrolle'],
  'direct_answer':'Der Reifendruck am Pferdeanhänger sollte vor der Fahrt kontrolliert werden, weil nur passend befüllte und unbeschädigte Reifen ihre Aufgabe zuverlässig erfüllen. Maßgeblich sind die Vorgaben für Reifen und Anhänger; zusätzlich gehört eine Sichtkontrolle der Reifen und Ventile vor dem Losfahren dazu.',
  'table_value':'Die Tabelle ordnet die einzelnen Reifenkontrollen nach Prüfpunkt, erkennbarem Zustand und sinnvoller Handlung vor der Fahrt.',
  'sources':[
   ('Reifendruck und Belastung','Der vorgeschriebene Reifendruck bestimmt, wie sich die Aufstandsfläche eines Anhängerreifens unter Last verhält und wie gleichmäßig die Karkasse arbeitet. Ein deutlich zu niedriger Druck vergrößert die Verformung des Reifens, erhöht seine Erwärmung und verändert das Fahrverhalten. Für die Kontrolle zählt deshalb der zum montierten Reifen und Anhänger passende Sollwert des Herstellers, nicht ein pauschaler Wert aus Erinnerung. Gemessen wird möglichst am kalten Reifen, damit Erwärmung während der Fahrt das Ergebnis nicht verfälscht und beide Seiten unter vergleichbaren Bedingungen beurteilt werden können.'),
   ('Sichtkontrolle der Anhängerreifen','Eine Reifenprüfung am Pferdeanhänger umfasst mehr als das Ablesen eines Druckmessers, weil sichtbare Schäden unabhängig vom Luftdruck auftreten können. An Lauffläche und Seitenwand werden Schnitte, Beulen, Fremdkörper und auffällige Risse gesucht, während zugleich Profil und gleichmäßiger Abrieb betrachtet werden. Ventile und Ventilkappen werden auf festen Sitz und erkennbare Beschädigungen geprüft, damit ein schleichender Druckverlust nicht unbemerkt bleibt. Zeigt ein Reifen eine ungewöhnliche Form oder einen klaren Schaden, wird die Ursache vor der Abfahrt geklärt und der betroffene Reifen nicht einfach durch Nachfüllen als unauffällig bewertet.')
  ]
 },
 {
  'title':'Warum muss die Beleuchtung am Pferdeanhänger vor der Fahrt kontrolliert werden?',
  'keyword':'Beleuchtung am Pferdeanhänger',
  'slug':'beleuchtung-pferdeanhaenger',
  'intent_terms':['Beleuchtung','Pferdeanhänger','Rücklicht','Blinker','Kontrolle'],
  'direct_answer':'Die Beleuchtung am Pferdeanhänger sollte vor jeder Fahrt geprüft werden, damit Bremslicht, Rücklicht, Blinker und Kennzeichenbeleuchtung zuverlässig funktionieren. Die Kontrolle zeigt außerdem früh, ob Stecker, Kabel oder Leuchten auffällig sind und vor dem Losfahren überprüft werden müssen.',
  'table_value':'Die Tabelle verbindet jede wichtige Leuchtenfunktion mit einer einfachen Sichtprüfung und der passenden Reaktion bei einer festgestellten Auffälligkeit.',
  'sources':[
   ('Funktionen der Anhängerbeleuchtung','Bremsleuchten machen eine Verzögerung des Zugfahrzeugs für nachfolgenden Verkehr sichtbar und müssen deshalb beim Betätigen der Bremse eindeutig aufleuchten. Fahrtrichtungsanzeiger zeigen den geplanten Richtungswechsel rechts oder links an und werden getrennt geprüft, damit ein einseitiger Ausfall erkannt wird. Rückleuchten kennzeichnen den Anhänger bei Dunkelheit dauerhaft nach hinten, während die Kennzeichenbeleuchtung das amtliche Kennzeichen erkennbar hält. Eine gemeinsame Funktionskontrolle umfasst daher verschiedene Schaltzustände und nicht nur den kurzen Blick auf eine einzelne Lampe.'),
   ('Stecker Kabel und Leuchten prüfen','Die elektrische Verbindung zwischen Zugfahrzeug und Pferdeanhänger beginnt am korrekt eingesetzten Stecker, dessen fester Sitz vor der Abfahrt kontrolliert wird. Anschließend werden sichtbare Kabelabschnitte auf Quetschungen, Scheuerstellen oder lose Führung betrachtet, bevor die einzelnen Leuchten gemeinsam mit einer zweiten Person oder durch einen geeigneten Kontrollablauf geprüft werden. Feuchtigkeit im Leuchtengehäuse, flackerndes Licht oder eine vollständig dunkle Funktion sind konkrete Auffälligkeiten und verlangen eine Ursachenklärung. Erst wenn Rücklicht, Bremslicht, Blinker und Kennzeichenbeleuchtung nachvollziehbar funktionieren, ist dieser elektrische Kontrollabschnitt abgeschlossen.')
  ]
 },
 {
  'title':'Warum sollte die Anhängerkupplung vor dem Losfahren geprüft werden?',
  'keyword':'Anhängerkupplung',
  'slug':'anhaengerkupplung-pferdeanhaenger',
  'intent_terms':['Anhängerkupplung','Kupplung','Pferdeanhänger','Sicherung','Kontrolle'],
  'direct_answer':'Die Anhängerkupplung sollte vor dem Losfahren kontrolliert werden, damit der Pferdeanhänger korrekt verbunden und die vorgesehene Sicherung vollständig hergestellt ist. Zur Prüfung gehören der erkennbare Kupplungszustand, die Sicherungseinrichtungen und ein kurzer Kontrollgang vor der Abfahrt.',
  'table_value':'Die Tabelle fasst Kupplung, Sicherung und Kontrollgang so zusammen, dass jeder Prüfpunkt vor der Abfahrt eindeutig abgearbeitet werden kann.',
  'sources':[
   ('Kupplung vor der Abfahrt','Beim Ankuppeln muss die Kupplung des Pferdeanhängers vollständig auf dem Kugelkopf sitzen und nach dem vorgesehenen Mechanismus verriegelt sein. Eine vorhandene Sicherheits- oder Verschleißanzeige wird direkt am Kupplungskopf abgelesen, weil eine nur scheinbar geschlossene Verbindung nicht als ausreichende Kontrolle gilt. Das Abreißseil oder die für das jeweilige System vorgesehene Sicherung wird an der dafür bestimmten Stelle befestigt und darf nicht lose über ungeeignete Bauteile gelegt werden. Das Stützrad wird nach dem Anheben vollständig in Fahrstellung gebracht und so gesichert, dass es sich während der Fahrt nicht absenken kann.'),
   ('Kontrollgang nach dem Ankuppeln','Ein abschließender Rundgang nach dem Ankuppeln verbindet mehrere zuvor getrennte Handgriffe zu einer letzten Plausibilitätskontrolle am stehenden Gespann. Dabei werden Verriegelung der Kupplung, Lage der Sicherung, elektrische Steckverbindung und die hochgestellte Position des Stützrads nacheinander betrachtet, ohne einen Punkt aus Gewohnheit zu überspringen. Auffälliges Spiel, eine unklare Anzeige oder eine nicht eindeutig befestigte Sicherung führen zurück zum jeweiligen Bauteil und werden vor dem Start geklärt. Erst der erneut bestätigte Zustand beendet den Kupplungsabschnitt und erlaubt den Übergang zur nächsten Vorbereitung des Gespanns.')
  ]
 },
]

def stable(v)->str:
    return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def writej(path:Path,v)->None:
    path.write_text(json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, format, *args): pass

def _template_item()->dict:
    with zipfile.ZipFile(PPM) as z:
        g9=json.loads(z.read(G9_MEMBER).decode('utf-8'))
    return copy.deepcopy(g9['item'])

def _dynamic_scenario(index:int)->dict:
    n=index+1
    phrase=f'Kontrollpunkt {n} am Pferdeanhänger'
    return {
      'title':f'Warum sollte {phrase} vor der Fahrt geprüft werden?',
      'keyword':phrase,
      'slug':f'kontrollpunkt-{n}-pferdeanhaenger',
      'intent_terms':['Kontrollpunkt','Pferdeanhänger','Fahrt','Prüfung',f'Kontrollpunkt {n}'],
      'direct_answer':f'{phrase} wird in diesem deterministischen Skalierungstest vor der Fahrt geprüft, damit der gebundene Ablauf für einen zusätzlichen Artikel denselben technischen Weg durchläuft. Der Testinhalt stammt vollständig aus den hierfür bereitgestellten Quellen und erzeugt keinen vorgefertigten Artikeltext.',
      'table_value':f'Die Tabelle ordnet die gebundenen Aussagen zu Kontrollpunkt {n} nach Ausgangslage, Beobachtung und eindeutiger Handlung vor der Fahrt.',
      'sources':[
        (f'Quelle A zu Kontrollpunkt {n}',f'Kontrollpunkt {n} ist ein eigenständiger Prüfschritt dieses deterministischen Skalierungstests und besitzt eine nur für diesen Artikel gebundene Quellenbasis. Die Prüfung wird vor der Fahrt durchgeführt und das Ergebnis für den aktuellen Durchlauf neu festgestellt, statt einen früheren Zustand zu übernehmen. Eine erkennbare Abweichung führt zurück zu genau diesem Kontrollpunkt und wird vor dem nächsten Schritt geklärt. Dadurch bleibt der zusätzliche Artikel auch bei großen Batches fachlich und technisch von den benachbarten Testartikeln unterscheidbar.'),
        (f'Quelle B zu Kontrollpunkt {n}',f'Für Kontrollpunkt {n} gilt im Test eine feste Reihenfolge aus Beobachtung, Bewertung und erneuter Kontrolle nach einer Korrektur, wobei jede Stufe aus der eigenen gebundenen Quelle hervorgeht. Ein früheres Ergebnis ersetzt die aktuelle Prüfung nicht und eine unklare Beobachtung beendet den Abschnitt ausdrücklich nicht. Erst ein eindeutiger Zustand schließt diesen Testschritt ab und erlaubt den Übergang zum nachfolgenden Artikelprozess. Die Formulierung bleibt dabei an den individuellen Sachverhalt von Kontrollpunkt {n} gekoppelt und darf nicht als allgemeine Vorlage für andere Batchpositionen dienen.')
      ]
    }

def _scenarios(count:int)->list[dict]:
    if count<1: raise RuntimeError('TEST_ROUTE_COUNT_MUST_BE_POSITIVE')
    rows=[copy.deepcopy(v) for v in SCENARIOS[:min(count,len(SCENARIOS))]]
    for index in range(len(rows),count): rows.append(_dynamic_scenario(index))
    return rows

def _serve_sources(root:Path, scenarios:list[dict]):
    requests={}
    for i,sc in enumerate(scenarios):
        rows=[]
        for j,(title,evidence) in enumerate(sc['sources']):
            name=f'item-{i}-source-{j}.html'
            (root/name).write_text(f'<!doctype html><html><head><title>{title}</title></head><body><article><h1>{title}</h1><p>{evidence}</p></article></body></html>',encoding='utf-8')
            source_id='src-'+hashlib.sha256((title+'\n'+evidence).encode('utf-8')).hexdigest()[:32]
            rows.append({'source_id':source_id,'source_title':title,'path':name})
        requests[i]=rows
    handler=lambda *a,**kw: Quiet(*a,directory=str(root),**kw)
    server=ThreadingHTTPServer(('127.0.0.1',0),handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    return server,requests

def create(out:Path,count:int)->dict:
    scenarios=_scenarios(count)
    if out.exists() and any(out.iterdir()): raise RuntimeError('TEST_FIXTURE_DIR_NOT_EMPTY')
    out.mkdir(parents=True,exist_ok=True)
    template=_template_item()
    quality0=copy.deepcopy(template['quality_binding'])
    category=(template.get('category_binding') or {}).get('slug') or (quality0.get('wordpress_category') or {}).get('slug')
    if not category: raise RuntimeError('TEMPLATE_CATEGORY_MISSING')
    items=[]; plan_rows=[]
    for i,sc in enumerate(scenarios):
        slot=hashlib.sha256(f'system4a-live-parity-fresh-{count}-{i}-{sc["title"]}'.encode()).hexdigest()
        items.append({'title':sc['title'],'target_keyword':sc['keyword'],'category':category,'article_type':'FAQ','plan_slot':slot})
        plan=copy.deepcopy(template)
        plan['article_type']='FAQ'; plan['target_keyword']=sc['keyword']; plan['topic']=sc['title']
        q=copy.deepcopy(quality0)
        q['intent_terms']=list(sc['intent_terms']); q['faq_direct_answer']=sc['direct_answer']; q['table_value_statement']=sc['table_value']
        plan['quality_binding']=q; plan['quality_binding_hash']=stable(q)
        cb=plan.get('category_binding')
        if isinstance(cb,dict): cb['slug']=category
        plan['canonical_article']={'title':sc['title'],'article_type':'FAQ'}
        for k in ('validation_contract_version','section_requirements','section_requirements_hash'): plan.pop(k,None)
        plan_rows.append({'item_index':i,'plan_slot':slot,'production_plan_item':plan})
    batch_sha=stable({'count':count,'items':items})
    snapshot={'contract':'SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1','next_textmachine_metadata_batch':{'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2','status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE','batch_sha256':batch_sha,'item_count':count,'items':items,'publish_allowed':False}}
    event={'contract':chat_start_gate.START_EVENT_CONTRACT,'button_id':chat_start_gate.START_BUTTON_ID,'action':chat_start_gate.START_ACTION,'route':chat_start_gate.START_ROUTE,'article_count':count,'batch_sha256':batch_sha,'publish_allowed':False}
    writej(out/'snapshot.template.json',snapshot); writej(out/'start_button.json',event)
    writej(out/'plans.json',{'contract':'SYSTEM4_MACHINE_PREWRITE_PLAN_BATCH_V1','item_count':count,'items':plan_rows})
    source_root=out/'source-pages'; source_root.mkdir()
    server,request_rows=_serve_sources(source_root,scenarios)
    try:
        _,port=server.server_address
        source_items=[]
        for i,item in enumerate(items):
            rows=[]
            for row in request_rows[i]:
                rows.append({'source_id':row['source_id'],'source_title':row['source_title'],'source_url':f'http://127.0.0.1:{port}/{row["path"]}','source_kind':'TEST_HTTP_SOURCE'})
            source_items.append({'item_index':i,'plan_slot':item['plan_slot'],'sources':rows})
        request_batch={'contract':source_acquisition.CONTRACT,'item_count':count,'items':source_items}
        acquired=source_acquisition.acquire_batch(request_batch,retrieved_at='2026-09-15T08:30:00+00:00')
    finally:
        server.shutdown(); server.server_close()
    writej(out/'acquired.json',acquired); writej(out/'source_requests.json',request_batch)
    proof={'contract':'SYSTEM4_TEST_ROUTE_INPUT_FACTORY_V2','article_count':count,'batch_sha256':batch_sha,'pre_point0_article_body_count':0,'source_acquisition_contract':acquired['contract'],'source_count':sum(len(x['sources']) for x in acquired['items']),'count_domain':'1..N'}
    writej(out/'input_factory_proof.json',proof)
    return proof

def main(argv:list[str])->int:
    if len(argv)!=3: raise SystemExit('usage: test_route_input_factory.py <out-dir> <positive-count>')
    print(json.dumps(create(Path(argv[1]),int(argv[2])),ensure_ascii=False,sort_keys=True)); return 0

if __name__=='__main__': raise SystemExit(main(sys.argv))
