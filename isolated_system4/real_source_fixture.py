from __future__ import annotations
import hashlib


def h(text:str)->str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def source_and_claims(index:int,target_keyword:str):
    rows={
        0:{
            'source_id':'real-fei-jumping-rules',
            'source_title':'FEI Jumping Rules – Schooling Areas and Practice Obstacles',
            'source_url':'https://inside.fei.org/sites/default/files/Jumping_Rules_2020_clean.pdf',
            'retrieved_at':'2026-09-14T15:00:00+02:00',
            'evidence':'The OC must provide at least one schooling area sufficiently large for optimal training conditions. There must be a minimum of one vertical and one spread obstacle.',
            'source_kind':'PARENT_CHAT_REAL_WEB_SNAPSHOT',
            'claims':[
                'Für das Training soll eine ausreichend große Arbeitsfläche zur Verfügung stehen.',
                'Im Trainingsbereich soll mindestens ein Steilsprung vorhanden sein.',
                'Im Trainingsbereich soll mindestens ein breites Hindernis vorhanden sein.',
            ],
        },
        1:{
            'source_id':'real-ifce-lighting-working-areas',
            'source_title':'IFCE Equipedia – Lighting working areas',
            'source_url':'https://equipedia.ifce.fr/en/equipedia-the-universe-of-the-horse-ifce/infrastructure-and-equipment/establishments-and-environment/exercising-areas/lighting-working-areas',
            'retrieved_at':'2026-09-14T15:00:00+02:00',
            'evidence':'Outdoor arena: 200 lux. 100–150 lux are acceptable for tests. For competitions an average illumination of 500 lux is recommended.',
            'source_kind':'PARENT_CHAT_REAL_WEB_SNAPSHOT',
            'claims':[
                'Für einen Außenreitplatz werden im Mittel 200 Lux empfohlen.',
                'Für Prüfungen können 100 bis 150 Lux ausreichend sein.',
                'Für Wettbewerbe werden im Mittel 500 Lux empfohlen.',
            ],
        },
        2:{
            'source_id':'real-lwk-niedersachsen-manure-storage',
            'source_title':'Landwirtschaftskammer Niedersachsen – Dünge-Verordnung und Pferdemistlagerung',
            'source_url':'https://www.lwk-niedersachsen.de/lwk/news/35505_Duenge-Verordnung_-_Worauf_muss_sich_der_Pferdehalter_einstellen',
            'retrieved_at':'2026-09-14T15:00:00+02:00',
            'evidence':'Es darf kein Sickersaft auslaufen. Die Mindestlagerkapazität beträgt zwei Monate. Der Container muss entweder abgedeckt werden oder unter Dach stehen.',
            'source_kind':'PARENT_CHAT_REAL_WEB_SNAPSHOT',
            'claims':[
                'Bei der Mistlagerung darf kein Sickersaft auslaufen.',
                'Für Pferdemist ist eine Mindestlagerkapazität von zwei Monaten vorzuhalten.',
                'Ein verwendeter Container muss abgedeckt sein oder unter einem Dach stehen.',
            ],
        },
    }
    if index not in rows:
        raise ValueError('REAL_SOURCE_INDEX_UNSUPPORTED')
    cfg=rows[index]
    evidence=cfg['evidence']
    src={
        'source_id':cfg['source_id'],
        'source_title':cfg['source_title'],
        'source_url':cfg['source_url'],
        'retrieved_at':cfg['retrieved_at'],
        'evidence':evidence,
        'snapshot_sha256':h(evidence),
        'http_status':200,
        'source_kind':cfg['source_kind'],
    }
    claims=[]
    for n,statement in enumerate(cfg['claims']):
        claims.append({
            'fact_id':f'real-fact-{index}-{n}',
            'source_id':cfg['source_id'],
            'statement':statement,
            'evidence_text':evidence,
            'evidence_text_sha256':h(evidence),
        })
    return src,claims
