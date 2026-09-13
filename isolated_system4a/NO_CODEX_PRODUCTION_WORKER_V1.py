import json,sys,hashlib,re
RESEARCH={'contract': 'SYSTEM4_RESEARCH_EVIDENCE_V1', 'sources': [{'source_id': 'src-adac-towing-2026', 'source_title': 'ADAC – Autos für Pferdeanhänger', 'source_url': 'https://www.adac.de/rund-ums-fahrzeug/auto-kaufen-verkaufen/kauftipps/autos-fuer-pferdeanhaenger/', 'retrieved_at': '2026-09-13T18:00:00+02:00', 'evidence': 'Für Pferdeanhänger muss die zulässige Anhängelast des konkreten Zugfahrzeugs zum tatsächlichen Anhängergewicht passen. Pferdeanhänger können beladen schwer sein, und Ausrüstung benötigt zusätzlichen sicheren Stauraum.', 'snapshot_sha256': '1c6408791666046476a2f9bd087f84e9fe058e2b2f67da1ad55d643c55c41c04'}, {'source_id': 'src-adac-stuetzlast-2026', 'source_title': 'ADAC – Stützlast bei Anhängern', 'source_url': 'https://www.adac.de/rund-ums-fahrzeug/auto-kaufen-verkaufen/kauftipps/stuetzlast/', 'retrieved_at': '2026-09-13T18:00:00+02:00', 'evidence': 'Bei einem Anhänger sind die zulässigen Stützlastwerte von Zugfahrzeug, Kupplung und Anhänger zu beachten. Wenn die Werte voneinander abweichen, ist der kleinere zulässige Wert maßgeblich.', 'snapshot_sha256': 'bc1f47e63c3410c55d8b2d1a7cf942fc2ac92117a36f1ab93f17fa1b1adfe72c'}, {'source_id': 'src-adac-loading-2026', 'source_title': 'ADAC – Tipps zum Fahren mit Anhänger', 'source_url': 'https://www.adac.de/rund-ums-fahrzeug/ausstattung-technik-zubehoer/ladungssicherung/fahren-mit-anhaenger/', 'retrieved_at': '2026-09-13T18:00:00+02:00', 'evidence': 'Schwere Lasten sollten beim Anhänger möglichst über der Achse liegen. Die Ladung muss so gesichert sein, dass sie auch bei starken Brems- oder Ausweichbewegungen nicht verrutscht oder umfällt.', 'snapshot_sha256': '2a1e351164f6146d34cd84087c18485b921a8c1c04c94bce91622165b64fc2e0'}, {'source_id': 'src-bmel-transport-2026', 'source_title': 'BMLEH – Schutz von Tieren beim Transport', 'source_url': 'https://www.bmel.de/DE/themen/tiere/tierschutz/eu-tierschutztransport-vo.html', 'retrieved_at': '2026-09-13T18:00:00+02:00', 'evidence': 'Beim Tiertransport tragen die beteiligten Personen Verantwortung für das Wohlergehen der Tiere, einschließlich der Vorgänge beim Be- und Entladen. Geeignete Ausrüstung und Verfahren gehören zu den Anforderungen an sichere Transporte.', 'snapshot_sha256': '332952972fef076381d814619cad483613ba041fe56666e584c79df8715ccaa4'}, {'source_id': 'src-adac-coupling-2026', 'source_title': 'ADAC – Anhänger richtig ankuppeln und sichern', 'source_url': 'https://www.adac.de/rund-ums-fahrzeug/ausstattung-technik-zubehoer/ladungssicherung/fahren-mit-anhaenger-techniktipps/', 'retrieved_at': '2026-09-13T18:00:00+02:00', 'evidence': 'Beim Ankuppeln eines Anhängers sollte die Verbindung zum Zugfahrzeug in einer festen Reihenfolge hergestellt und abschließend kontrolliert werden. Je nach Anhänger gehört auch eine zusätzliche Sicherungsverbindung dazu.', 'snapshot_sha256': '67ab79a796175293ffc829152c03ca188ec2a6aa5c5a064d2c97a77e2bc5fe46'}]}
FACTS={'contract': 'SYSTEM4_FACTS_EVIDENCE_V1', 'claims': [{'fact_id': 'F1', 'source_id': 'src-adac-towing-2026', 'statement': 'Die Checkliste muss Anhängelast und tatsächliches Anhängergewicht als zusammengehörige Prüfpunkte behandeln.', 'evidence_text': 'Für Pferdeanhänger muss die zulässige Anhängelast des konkreten Zugfahrzeugs zum tatsächlichen Anhängergewicht passen.', 'evidence_text_sha256': '8a7e627c646a806900c204121e728d8dbd2f3f7bfd6e8fbe7e10117213fb1c4f'}, {'fact_id': 'F2', 'source_id': 'src-adac-towing-2026', 'statement': 'Zusätzliche Ausrüstung benötigt einen sicheren Platz und gehört deshalb in die praktische Transportvorbereitung.', 'evidence_text': 'Pferdeanhänger können beladen schwer sein, und Ausrüstung benötigt zusätzlichen sicheren Stauraum.', 'evidence_text_sha256': 'de603a9b1de4347ca4373015a982b068bbc676aa096bf5369992ca4a683c472e'}, {'fact_id': 'F3', 'source_id': 'src-adac-stuetzlast-2026', 'statement': 'Eine belastbare Checkliste vergleicht die Stützlastgrenzen von Fahrzeug, Kupplung und Anhänger und richtet sich nach dem kleineren zulässigen Wert.', 'evidence_text': 'Wenn die Werte voneinander abweichen, ist der kleinere zulässige Wert maßgeblich.', 'evidence_text_sha256': '9a29afec5db654b7cd60750aec12f3933f616f10d49ae89934a51f6b1e928be9'}, {'fact_id': 'F4', 'source_id': 'src-adac-loading-2026', 'statement': 'Die Beladungsprüfung muss Lastverteilung und Sicherung berücksichtigen, damit die Ladung bei Brems- oder Ausweichbewegungen nicht verrutscht.', 'evidence_text': 'Die Ladung muss so gesichert sein, dass sie auch bei starken Brems- oder Ausweichbewegungen nicht verrutscht oder umfällt.', 'evidence_text_sha256': 'ad12ee1c297e1fa88797f7958be8f954c6383219c1c0f76066d5a9b9a27c32ff'}, {'fact_id': 'F5', 'source_id': 'src-bmel-transport-2026', 'statement': 'Eine Transportcheckliste muss das Wohlergehen des Pferdes sowie das sichere Be- und Entladen als eigene Prüffelder enthalten.', 'evidence_text': 'Beim Tiertransport tragen die beteiligten Personen Verantwortung für das Wohlergehen der Tiere, einschließlich der Vorgänge beim Be- und Entladen.', 'evidence_text_sha256': 'a76765e6b9065b165dd34a2cd73e2bd6d9bd00858139cf891f5e92ee4164381c'}, {'fact_id': 'F6', 'source_id': 'src-adac-coupling-2026', 'statement': 'Vor der Abfahrt sollte die Kupplungsverbindung nach einer festen Reihenfolge hergestellt und abschließend kontrolliert werden.', 'evidence_text': 'Beim Ankuppeln eines Anhängers sollte die Verbindung zum Zugfahrzeug in einer festen Reihenfolge hergestellt und abschließend kontrolliert werden.', 'evidence_text_sha256': '3c97792022e652f62e94ae1aca13e0487a6b28ab94f6c0fa13aaf4c291e05d84'}]}

def sh(s): return hashlib.sha256(s.encode()).hexdigest()
def fact_pack(source_sha):
    src={s['source_id']:s for s in RESEARCH['sources']}
    cs=[]
    for c in FACTS['claims']:
        x=dict(c); x['source_url']=src[c['source_id']]['source_url']; x['claim_status']='FULLY_SUPPORTED'; x['article_types']=['Beratung']; x['display_label']=c['statement']; x['locator']=c['evidence_text']; cs.append(x)
    return {'contract':'canonical_fact_pack_v1','status':'SOURCE_VERIFIED_PRODUCTION_READY','source_snapshot_id':source_sha,'fact_pack_id':source_sha,'sources':RESEARCH['sources'],'claims':cs}

def plan(article,pack):
    ids=[c['fact_id'] for c in pack['claims']]
    order_id='beratung-checklisten-realcase-001'
    slug='welche-variante-von-checklisten-fuer-pferdeanhaenger-passt-zu-welchem-bedarf'
    lead='Eine gute Checkliste für den Pferdeanhänger passt zum tatsächlichen Einsatz und trennt technische, organisatorische und tierbezogene Kontrollen. Sie hilft nur dann, wenn sie die entscheidenden Punkte vor der Abfahrt in einer sinnvollen Reihenfolge abfragt und keine Grenze durch einen anderen Vorteil ersetzt.'
    conclusion='Die passende Checkliste ist kein möglichst langer Zettel, sondern eine klare Entscheidungshilfe. Sie verbindet Fahrzeug und Anhänger, Kupplung und Stützlast, Beladung und Sicherung sowie das Wohlergehen des Pferdes. Je nach Fahrt kann der Schwerpunkt wechseln, die grundlegenden Kontrollfelder bleiben jedoch erhalten.'
    ro={'order_id':order_id,'article_type':'Beratung','title':article['title'],'slug':slug,'subject_scope':'horse_trailer_checklist_selection','subject_label':'die Auswahl einer geeigneten Checkliste für Pferdeanhänger','lead':lead,'conclusion':conclusion,'links':[],'allowed_fact_ids':ids,'required_sections':['Fazit','Weiterführende Informationen'],'section_fact_ids':ids,'table_focus':ids[:4]}
    ca={'order_id':order_id,'article_type':'Beratung','title':article['title'],'slug':slug,'body_html':'PENDING_RUNTIME_DRAFT','body_text':'PENDING_RUNTIME_DRAFT','body_html_sha256':sh('PENDING_RUNTIME_DRAFT'),'content_plan_hash':hashlib.sha256(json.dumps(ro,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'type_meta':{'decision_goal':'Eine passende Transportcheckliste anhand des konkreten Einsatzes auswählen','decision_criteria':['Fahrzeug und Anhänger','Beladung und Sicherung','Pferdewohl und Ablauf']}}
    return {'article_type':'Beratung','target_keyword':article['target_keyword'],'topic':article['title'],'source_snapshot_id':pack['fact_pack_id'],'runtime_order':ro,'canonical_article':ca,'source_hashes':[]}

def trace(fid, pack):
    c=next(x for x in pack['claims'] if x['fact_id']==fid)
    return '<span class="ppm-source-trace" data-fact-id="%s" data-source-hash="%s" data-source-title="%s"></span>'%(fid,c['evidence_text_sha256'],c['source_id'])

def body(req):
    a=req['article']; ctx=req['production_context']; pack=ctx['fact_pack']; q=ctx['production_plan_item']['quality_binding']; links={x['role']:x for x in q['link_bindings']}
    def link(role):
        x=links[role]; return '<a data-link-role="%s" href="%s">%s</a>'%(role,x['href'],x['anchor'])
    T=lambda ids: ' data-fact-ids="'+' '.join(ids)+'"'
    parts=[]
    parts.append('<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung" data-order-id="beratung-checklisten-realcase-001">')
    parts.append('<section data-block="intro">')
    parts.append('<p'+T(['F1','F3','F5'])+'>Wer eine Checkliste für den Pferdeanhänger auswählt, sollte nicht nach möglichst vielen Punkten suchen. Entscheidend ist, ob die Liste zum eigenen Gespann und zum geplanten Transport passt. Technische Grenzen, die sichere Verbindung von Fahrzeug und Anhänger, die Beladung sowie das Wohlergehen des Pferdes gehören deshalb in getrennte Kontrollfelder.</p>')
    parts.append('<p'+T(['F4','F6'])+'>Eine brauchbare Liste führt außerdem in einer sinnvollen Reihenfolge durch die Vorbereitung. Sie beginnt bei den unveränderlichen Voraussetzungen, geht anschließend zur Kupplung und Beladung über und endet mit einer letzten Kontrolle unmittelbar vor der Abfahrt. So werden wichtige Punkte nicht durch Routine oder Zeitdruck verdrängt.</p></section>')
    parts.append('<section data-block="criteria"><h2>Welche Checkliste zum eigenen Gespann passt</h2>')
    parts.append('<p'+T(['F1'])+'>Die erste Auswahlfrage betrifft Fahrzeug und Anhänger. Eine Checkliste sollte die zulässige Anhängelast des konkreten Zugfahrzeugs mit dem tatsächlichen Bedarf des Pferdeanhängers zusammenbringen. Ein allgemeiner Fahrzeugname reicht dafür nicht; die später genutzte Kombination muss anhand ihrer eigenen Unterlagen geprüft werden.'+trace('F1',pack)+'</p>')
    parts.append('<p'+T(['F3'])+'>Ebenso braucht die Liste ein eigenes Feld für die Stützlast. Treffen unterschiedliche Grenzwerte von Fahrzeug, Kupplung und Anhänger zusammen, darf die Kontrolle nicht nur einen davon nennen. Die Entscheidung muss sich am kleineren zulässigen Wert orientieren und diesen als verbindliche Grenze behandeln.'+trace('F3',pack)+'</p>')
    parts.append('<p'+T(['F6'])+'>Für die mechanische Verbindung ist eine feste Reihenfolge hilfreich: ankuppeln, Verbindung kontrollieren und die vorgesehene zusätzliche Sicherung berücksichtigen. Eine Liste, die diesen Ablauf nur mit einem pauschalen Haken abbildet, ist für die Abfahrtskontrolle weniger geeignet als eine klar gegliederte Variante.'+trace('F6',pack)+'</p>')
    parts.append('<p>Zur Einordnung des Themas führt die '+link('parent_category')+'. Dort lässt sich prüfen, ob die gewählte Liste wirklich zum betreffenden Anhängerbereich gehört und ob für den eigenen Einsatz weitere Unterpunkte sinnvoll sind.</p>')
    parts.append('<ul data-list="criteria">')
    parts.append('<li'+T(['F1'])+'>Die Kombination aus Zugfahrzeug und Anhänger muss als eigener Prüfbereich erscheinen und darf nicht nur allgemein als Fahrzeugkontrolle bezeichnet sein.</li>')
    parts.append('<li'+T(['F3'])+'>Stützlastgrenzen sollten getrennt von anderen Gewichten abgefragt werden, damit der maßgebliche kleinere Wert nicht übersehen wird.</li>')
    parts.append('<li'+T(['F6'])+'>Kupplung und Sicherungsverbindung brauchen eine konkrete Abschlusskontrolle statt eines unspezifischen Sammelpunkts.</li>')
    parts.append('<li'+T(['F4'])+'>Beladung und Ladungssicherung sollten gemeinsam geprüft werden, weil Gewichtsverteilung und Verrutschen unterschiedliche Risiken betreffen.</li>')
    parts.append('<li'+T(['F5'])+'>Das Pferd selbst und der Ablauf beim Be- und Entladen gehören als eigener Abschnitt in die Transportvorbereitung.</li>')
    parts.append('</ul></section>')
    parts.append('<section data-block="decision"><h2>Kontrolltiefe nach Fahrt und Nutzung wählen</h2>')
    parts.append('<p'+T(['F4'])+'>Für kurze Routinefahrten kann eine kompakte Liste genügen, wenn die unveränderlichen Voraussetzungen bereits sauber dokumentiert sind. Vor jeder Fahrt bleiben jedoch Beladung und Sicherung relevant. Schwere Ausrüstung sollte so angeordnet werden, dass die Fahrstabilität nicht unnötig verschlechtert wird, und bewegliche Gegenstände müssen zuverlässig gesichert sein.'+trace('F4',pack)+'</p>')
    parts.append('<p'+T(['F2'])+'>Eine längere oder ausrüstungsintensive Fahrt benötigt mehr Platz in der Checkliste. Sattel, Decken, Futter oder weiteres Zubehör dürfen nicht einfach nachträglich irgendwo verstaut werden. Die Liste sollte deshalb einen eigenen Punkt für sicheren Stauraum enthalten und ihn vor der Abfahrt tatsächlich abhaken lassen.</p>')
    parts.append('<p'+T(['F5'])+'>Sobald ein Pferd transportiert wird, darf die Vorbereitung nicht bei Technik enden. Eine geeignete Liste betrachtet auch das Wohlergehen des Tieres und die Abläufe beim Ein- und Ausladen. Diese Punkte gehören nicht in einen allgemeinen Erinnerungsblock, sondern in einen klaren Abschnitt mit eindeutiger Zuständigkeit.'+trace('F5',pack)+'</p>')
    parts.append('<p>Für rechtliche und organisatorische Hintergründe kann zusätzlich '+link('semantic_related')+' genutzt werden. Dieser Verweis ergänzt die Checkliste, ersetzt aber nicht die konkrete Kontrolle der eigenen Kombination und des geplanten Transports.</p>')
    parts.append('<p'+T(['F1','F3'])+'>Bei der Auswahl sollte jede Muss-Bedingung für sich bestehen. Eine passende Anhängelast gleicht keine ungeklärte Stützlast aus, und eine gute Ladungssicherung macht eine ungeeignete Fahrzeug-Anhänger-Kombination nicht zulässig. Eine Checkliste ist deshalb dann gut, wenn sie solche Grenzen sichtbar trennt und nicht zu einem einzigen Gesamthaken zusammenfasst.</p>')
    parts.append('</section>')
    parts.append('<section data-block="table"><h2>Auswahlkriterien in einer Tabelle prüfen</h2>')
    parts.append('<p'+T(['F1','F3','F4'])+'>Die Tabelle hilft dabei, verschiedene Checklisten vor der Nutzung nach denselben Kriterien zu beurteilen. Wichtig ist nicht die Zahl der Punkte, sondern ob die entscheidenden Kontrollbereiche klar beschrieben, voneinander getrennt und praktisch abhakbar sind.</p>')
    parts.append('<table class="system-129-table comparison-table"><thead><tr><th>Kriterium</th><th>Woran eine geeignete Liste erkennbar ist</th><th>Warum das für die Auswahl wichtig ist</th></tr></thead><tbody>')
    rows=[
      ('F1','Fahrzeug und Anhänger','Die konkrete Kombination wird ausdrücklich geprüft','Technische Grenzen bleiben der Ausgangspunkt'),
      ('F3','Stützlast','Mehrere mögliche Grenzwerte werden getrennt erfasst','Der kleinere zulässige Wert kann klar berücksichtigt werden'),
      ('F4','Beladung und Sicherung','Lastverteilung und feste Sicherung stehen als eigene Punkte bereit','Vorbereitung und Fahrstabilität werden nicht vermischt'),
      ('F5','Pferdewohl und Ablauf','Be- und Entladen sowie Tierwohl sind sichtbar eingebunden','Die Checkliste endet nicht bei der Fahrzeugtechnik'),
    ]
    for fid,a1,a2,a3 in rows:
      parts.append('<tr><td'+T([fid])+'>'+a1+'</td><td'+T([fid])+'>'+a2+'</td><td'+T([fid])+'>'+a3+'</td></tr>')
    parts.append('</tbody></table>')
    parts.append('<p'+T(['F2','F6'])+'>Ergänzend sollte die gewählte Liste Raum für fahrtspezifische Punkte lassen. Dazu können zusätzlicher Stauraum, besondere Ausrüstung oder ein abweichender Ablauf gehören. Solche Ergänzungen sind sinnvoll, solange sie die grundlegenden Prüfblöcke nicht verdrängen und die Abschlusskontrolle der Verbindung erhalten bleibt.</p></section>')
    parts.append('<section data-block="conclusion"><h2>Fazit</h2>')
    parts.append('<p'+T(['F1','F3','F4'])+'>Die passende Checkliste für den Pferdeanhänger ist diejenige, die die eigene Kombination eindeutig abbildet. Sie trennt Anhängelast, Stützlast, Kupplung, Beladung und Sicherung in nachvollziehbare Schritte. Dadurch wird sichtbar, an welcher Stelle eine Voraussetzung geklärt ist und wo vor der Fahrt noch eine konkrete Angabe oder Kontrolle fehlt.</p>')
    parts.append('<p'+T(['F5','F6'])+'>Gleichzeitig muss die Liste über die reine Technik hinausgehen. Das sichere Be- und Entladen und das Wohlergehen des Pferdes gehören ebenso hinein wie eine abschließende Kontrolle der Verbindung zum Zugfahrzeug. Wer die Kontrolltiefe an Fahrt und Nutzung anpasst, erhält eine praktische Liste, ohne die unverzichtbaren Grundprüfungen jedes Mal neu erfinden zu müssen.</p>')
    parts.append('<p'+T(['F2','F4'])+'>Eine gute Auswahlentscheidung erkennt man deshalb weniger an der Länge der Checkliste als an ihrer Struktur. Sie führt zuerst durch die Grenzen des Gespanns, dann durch Verbindung und Beladung und schließlich durch die tierbezogenen und organisatorischen Punkte. Offene Fragen bleiben sichtbar, statt durch bereits erledigte Punkte verdeckt zu werden.</p></section>')
    parts.append('<section data-block="further_information"><h2>Weiterführende Informationen</h2>')
    parts.append('<p>Weitere Grundlagen zum Themenbereich stehen unter '+link('further_information')+'. Für die konkrete Fahrt bleibt entscheidend, die eigene Fahrzeug-Anhänger-Kombination, die aktuelle Beladung und den Zustand des Pferdes unmittelbar vor der Abfahrt zu prüfen.</p>')
    parts.append('<p class="ppm-ai-disclosure">Dieser Beitrag wurde mithilfe von KI vorformuliert und anschließend redaktionell geprüft und überarbeitet.</p></section></article>')
    return '\n'.join(parts)

def handle(req):
    task=req['task']
    if task=='research': return json.dumps(RESEARCH,ensure_ascii=False,sort_keys=True)
    if task=='facts': return json.dumps(FACTS,ensure_ascii=False,sort_keys=True)
    if task=='context':
        pack=fact_pack(req['source_snapshot_sha256']); return json.dumps({'fact_pack':pack,'production_plan_item':plan(req['article'],pack)},ensure_ascii=False,sort_keys=True)
    if task=='draft': return body(req)
    if task=='repair':
        repaired=req['draft']
        codes={f.get('error_code') for f in req.get('findings',[])}
        if 'LANGUAGETOOL_FINDING' in codes:
            repaired=repaired.replace('ausrüstungsintensive Fahrt','Fahrt mit umfangreicher Ausrüstung')
            repaired=repaired.replace('praktisch abhakbar sind','praktisch prüfbar sind')
            repaired=repaired.replace('fahrtspezifische Punkte','auf die jeweilige Fahrt bezogene Punkte')
        if 'BLOCKED_WAVE2_HEADING_INTENT_MISMATCH' in codes:
            repaired=repaired.replace('Kontrolltiefe nach Fahrt und Nutzung wählen','Checklisten für Pferdeanhänger nach Fahrt und Nutzung auswählen')
            repaired=repaired.replace('Auswahlkriterien in einer Tabelle prüfen','Checklisten für Pferdeanhänger anhand von Kriterien vergleichen')
        return repaired
    raise RuntimeError('UNKNOWN_TASK:'+str(task))
for line in sys.stdin:
    env=json.loads(line); content=handle(env['request']); print(json.dumps({'contract':env['contract'],'session_id':env['session_id'],'result':{'content':content}},ensure_ascii=False),flush=True)
