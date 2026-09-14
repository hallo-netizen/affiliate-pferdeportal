from __future__ import annotations
import hashlib


def h(text:str)->str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def source_and_claims(index:int,target_keyword:str):
    rows={
        0:{
            'source_id':'new-topic-verbraucherzentrale-pferdehaftpflicht',
            'source_title':'Verbraucherzentrale – Haftpflichtversicherung für Haustiere',
            'source_url':'https://www.verbraucherzentrale.de/wissen/geld-versicherungen/weitere-versicherungen/haftpflichtversicherung-fuer-haustiere-33442',
            'retrieved_at':'2026-09-14T16:30:00+02:00',
            'evidence':'Wichtige Punkte bei der Pferdehalterhaftpflicht sind der Verstoß von Halterpflichten, der Schutz für Pferdehüter, Flurschäden sowie Deckschäden. Pferdebesitzer sollten zudem auf die Mitversicherung bei Reitbeteiligung achten. Umfang und Preis variieren von Versicherer zu Versicherer. Gleiches gilt für die Ausschlüsse. Wichtig ist daher immer ein genauer Blick in den konkreten Vertrag und die darin enthaltenen Versicherungsbedingungen.',
            'claims':[
                'Bei einer Pferdehaftpflicht sollte die Mitversicherung einer Reitbeteiligung geprüft werden.',
                'Auch der Schutz für Pferdehüter ist ein wichtiger Punkt der Haftpflichtversicherung für Pferde.',
                'Der konkrete Versicherungsumfang und mögliche Ausschlüsse sollten vor Vertragsabschluss geprüft werden.',
            ],
        },
        1:{
            'source_id':'new-topic-aaep-uv-mask',
            'source_title':'AAEP Proceedings – UV protection with masks after eyelid SCC treatment',
            'source_url':'https://aaep.org/wp-content/uploads/2024/02/Proceedings-64th-Annual-Convention-2018.pdf',
            'retrieved_at':'2026-09-14T16:30:00+02:00',
            'evidence':'Recurrence was reduced when horses wore a mask with greater than 90% UV light protection postoperatively. The discussion states that squamous cell carcinoma is a UV light-induced neoplasia and that protecting the horse from additional UV light exposure is an important part of preventing recurrence.',
            'claims':[
                'UV-Licht kann bei bestimmten Erkrankungen am Pferdeauge eine wichtige Rolle spielen.',
                'Eine Maske mit ausgeprägtem UV-Schutz kann nach einer Behandlung am Augenlid zusätzlichen Schutz vor UV-Licht bieten.',
                'Beim Schutz empfindlicher Augen kann die Verringerung zusätzlicher UV-Lichtexposition ein relevantes Auswahlkriterium sein.',
            ],
        },
        2:{
            'source_id':'new-topic-umn-alfalfa-pellets',
            'source_title':'University of Minnesota Extension – Alternative feedstuffs for horses',
            'source_url':'https://extension.umn.edu/agriculture/animals-and-livestock/horse/alternative-feedstuffs-for-horses',
            'retrieved_at':'2026-09-14T16:30:00+02:00',
            'evidence':'Alfalfa pellets: Nutritional content is similar to hay. High in fiber. May have less dust and waste than hay. You can use it as a total replacement. Horses spend less time eating. Horses may overeat.',
            'claims':[
                'Alfalfa-Pellets liefern eine faserreiche Futterquelle mit einem Nährstoffprofil, das Heu ähneln kann.',
                'Alfalfa-Pellets können weniger Staub und Futterverluste verursachen als Heu.',
                'Pferde können Pellets schneller aufnehmen und dadurch eher zum Überfressen neigen.',
            ],
        },
    }
    if index not in rows:
        raise ValueError('NEW_TOPIC_REAL_SOURCE_INDEX_UNSUPPORTED')
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
        'source_kind':'PARENT_CHAT_REAL_WEB_SNAPSHOT',
    }
    claims=[]
    for n,statement in enumerate(cfg['claims']):
        claims.append({
            'fact_id':f'new-topic-real-fact-{index}-{n}',
            'source_id':cfg['source_id'],
            'statement':statement,
            'evidence_text':evidence,
            'evidence_text_sha256':h(evidence),
        })
    return src,claims
