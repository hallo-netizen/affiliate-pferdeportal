from __future__ import annotations
import copy,json
from pathlib import Path

import authoring_contract,controller,point0_snapshot,root_entry,supervisor
from live_route_test_support import head,production_snapshot_bytes,write_json
from real_source_fixture import source_and_claims


def start_to_context_real(base:Path,index:int):
    raw=production_snapshot_bytes(3)
    snapshot=base/'production-snapshot.json'
    snapshot.write_bytes(raw)
    metadata=json.loads(raw.decode('utf-8'))['next_textmachine_metadata_batch']['items'][index]
    src,claims=source_and_claims(index,metadata['target_keyword'])
    prepared=point0_snapshot.prepare(
        production_snapshot_bytes=raw,
        root_manifest_sha256=root_entry._critical_manifest_sha256(),
        head_sha=head(),
    )
    p0=point0_snapshot.finalize(
        prepared,
        research_provider='PARENT_CHAT_REAL_WEB_SNAPSHOT',
        sources=[src],
    )
    p0p=base/f'point0-real-{index}.json'
    p0p.write_bytes(point0_snapshot.canon(p0))
    workspace=base/f'real-item-{index}'
    rc=root_entry.main(['root_entry.py','start-point0',str(p0p),str(workspace),str(index)])
    if rc!=0:
        raise AssertionError('ROOT_POINT0_REAL_SOURCE_FAILED:'+str(index))
    research=supervisor.expected_research_document(workspace)
    rp=write_json(base/f'research-real-{index}.json',research)
    if controller.main(['controller.py','research',str(workspace),str(rp)])!=0:
        raise AssertionError('REAL_RESEARCH_FAILED:'+str(index))
    facts_doc={'contract':'SYSTEM4_FACTS_EVIDENCE_V1','claims':copy.deepcopy(claims)}
    fp=write_json(base/f'facts-real-{index}.json',facts_doc)
    if controller.main(['controller.py','facts',str(workspace),str(fp)])!=0:
        raise AssertionError('REAL_FACTS_FAILED:'+str(index))
    state=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
    source_sha=state['source_snapshot_sha256']
    pack_claims=[]
    for row in claims:
        enriched=copy.deepcopy(row)
        enriched['claim_status']='FULLY_SUPPORTED'
        enriched['article_types']=[state['article']['article_type']]
        pack_claims.append(enriched)
    pack={
        'contract':'canonical_fact_pack_v1',
        'status':'SOURCE_VERIFIED_PRODUCTION_READY',
        'source_snapshot_id':source_sha,
        'fact_pack_id':source_sha,
        'sources':copy.deepcopy(research['sources']),
        'claims':pack_claims,
    }
    ids=[row['fact_id'] for row in claims]
    a=state['article']
    plan={
        'article_type':a['article_type'],
        'target_keyword':a['target_keyword'],
        'topic':a['title'],
        'source_snapshot_id':source_sha,
        'runtime_order':{
            'order_id':f'real-route-{index}',
            'article_type':a['article_type'],
            'title':a['title'],
            'slug':f'real-route-{index}',
            'subject_scope':'real_source_corridor',
            'subject_label':a['target_keyword'],
            'lead':'Gebundener Einstieg ausschließlich aus dem realen Quellenstand.',
            'conclusion':'Gebundener Abschluss ausschließlich aus dem realen Quellenstand.',
            'allowed_fact_ids':ids,
        },
    }
    pp=write_json(base/f'pack-real-{index}.json',pack)
    pl=write_json(base/f'plan-real-{index}.json',plan)
    if controller.main(['controller.py','context',str(workspace),str(pp),str(pl)])!=0:
        raise AssertionError('REAL_CONTEXT_FAILED:'+str(index))
    state=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
    if state['phase']!='DRAFT_REQUIRED':
        raise AssertionError('REAL_DRAFT_REQUIRED_NOT_REACHED')
    return workspace,snapshot,state


def valid_real_article(state:dict,index:int)->str:
    c=state['authoring_contract']
    identity=c['article_identity']
    g=c['global_requirements']
    s=c['structure_requirements']
    t=c['type_requirements']
    b=c['bound_requirements']
    allowed=list(b['allowed_fact_ids'])
    claims=state.get('production_context',{}).get('fact_pack',{}).get('claims',[])
    claim_map={str(row.get('fact_id') or ''):str(row.get('statement') or '').strip().rstrip(' .!?') for row in claims if isinstance(row,dict)}
    if any(not claim_map.get(fact_id) for fact_id in allowed):
        raise AssertionError('REAL_BOUND_FACT_STATEMENT_MISSING')

    min_words=int(g.get('min_words') or 0)
    min_paragraphs=int(g.get('min_paragraphs') or 0)
    min_h2=int(g.get('min_h2') or 0)
    intro=s.get('intro') if isinstance(s.get('intro'),dict) else {}
    intro_name=str(intro.get('required_block') or 'intro')
    ilo=max(int(intro.get('minimum_words') or 1),20)
    ihi=int(intro.get('maximum_words') or max(ilo,200))
    intent_terms=[str(x).strip() for x in b.get('intent_terms',[]) if str(x).strip()]
    if not intent_terms:
        raise AssertionError('REAL_BOUND_INTENT_TERMS_MISSING')
    required=list(t.get('required_blocks') or [])
    other=[x for x in required if x!=intro_name]
    while len(other)<max(min_h2,2):
        other.append(f'content_{len(other)+1}')

    section_labels={
        'intro':'Einleitung','criteria':'Auswahlkriterien','decision':'Entscheidung',
        'table':'Vergleich','conclusion':'Fazit','further_information':'weitere Informationen',
    }
    aspects=(
        'Auswahl','Material','Nutzung','Sicherheit','Pflege','Eignung','Praxis','Vergleich',
        'Planung','Kontrolle','Entscheidung','Anwendung','Untergrund','Ausstattung','Haltung','Training',
        'Stall','Weide','Reitplatz','Dokumentation','Einordnung','Prüfung','Abwägung','Orientierung',
    )
    openers=(
        'Im Abschnitt „{section}“ ist belegt:',
        'Beim Abschnitt „{section}“ gilt als Beleg:',
        'Aus dem Quellenstand für „{section}“ folgt:',
        'Für „{section}“ ist dokumentiert:',
        'Innerhalb von „{section}“ bleibt festgehalten:',
        'Zur Prüfung in „{section}“ ist gebunden:',
        'Als Grundlage für „{section}“ dient:',
        'Unter „{section}“ wird als Quellenpunkt geführt:',
    )

    def label(section:str)->str:
        return section_labels.get(section,'Sachprüfung')

    def paragraph(fact_id:str,seed:int,section:str)->str:
        fact=claim_map[fact_id]
        a=aspects[(seed+index*3)%len(aspects)]
        d=aspects[(seed*2+5+index)%len(aspects)]
        e=aspects[(seed*3+9+index)%len(aspects)]
        opener=openers[(seed+index)%len(openers)].format(section=label(section))
        return (
            f'{opener} {fact}; bei {identity["target_keyword"]} wird diese Aussage im Zusammenhang mit {a}, {d} und {e} '
            f'eingeordnet, wobei ausschließlich der dokumentierte Quelleninhalt maßgeblich bleibt und unbelegte Ergänzungen '
            f'ausdrücklich außerhalb der Bewertung bleiben.'
        )

    fid=allowed[0]
    intro_text=paragraph(fid,1,'intro')
    if len(intro_text.split())<ilo:
        intro_text+=' Der Einstieg benennt damit nur den belegten Ausgangspunkt für die weitere sachliche Prüfung.'
    if len(intro_text.split())>ihi:
        intro_text=' '.join(intro_text.split()[:ihi]).rstrip(' ,;:')+'.'

    traces=''
    if t.get('fact_trace_required') is True:
        need=max(int(b.get('source_trace_minimum') or 0),1)
        for fact_id in allowed[:need]:
            meta=b['fact_authority'][fact_id]
            traces+=f'<span class="ppm-source-trace" data-fact-id="{fact_id}" data-source-title="{meta["source_id"]}" data-source-hash="{meta["evidence_text_sha256"]}"></span>'
    blocks=[f'<section data-block="{intro_name}"><p data-fact-ids="{fid}">{intro_text}{traces}</p></section>']

    link_rows=[row for row in b.get('link_bindings',[]) if isinstance(row,dict) and row.get('active') is not False]
    missing=[str(row.get('section_id') or '') for row in link_rows if str(row.get('section_id') or '') not in other]
    if missing:
        raise AssertionError('REAL_BOUND_LINK_SECTION_MISSING:'+','.join(missing))

    target_paras=max(min_paragraphs-1,len(other)*2,4)
    paras_per=max(2,(target_paras+len(other)-1)//len(other))
    target_words=max(min_words-len(intro_text.split()),500)
    words_per=max(48,(target_words+len(other)*paras_per-1)//(len(other)*paras_per))
    heading_suffixes=(
        'sachlich einordnen','gezielt prüfen','für die Auswahl bewerten','im Vergleich betrachten',
        'für die Praxis abwägen','als Entscheidungspunkt nutzen','an der Quelle prüfen','nachvollziehbar zusammenführen',
    )

    seed=10
    for bi,name in enumerate(other):
        intent=intent_terms[(bi+index)%len(intent_terms)]
        heading=f'{intent} {heading_suffixes[(bi+index)%len(heading_suffixes)]}'
        parts=[f'<h2>{heading}</h2>']
        section_links=[row for row in link_rows if str(row.get('section_id') or '')==name]
        for pi in range(paras_per):
            fact_id=allowed[(bi+pi)%len(allowed)]
            text=paragraph(fact_id,seed,name)
            addon=0
            while len(text.split())<words_per:
                addon+=1
                a=aspects[(seed+addon*4+index)%len(aspects)]
                d=aspects[(seed+addon*7+11+index)%len(aspects)]
                text=text.rstrip('.')+f'; im Bezug auf {a} und {d} dient derselbe Beleg lediglich als nachvollziehbarer Prüfrahmen ohne neue Tatsachen.'
            if pi==0:
                for row in section_links:
                    text+=f' <a href="{row["href"]}">{row["anchor"]}</a>'
            parts.append(f'<p data-fact-ids="{fact_id}">{text}</p>')
            seed+=1
        blocks.append(f'<section data-block="{name}">'+''.join(parts)+'</section>')

    if len(blocks)>1:
        list_openers=('Festgehalten bleibt','Dokumentiert ist','Als Prüfpunkt gilt','Gebunden bleibt')
        list_rows=[]
        for n in range(4):
            fact_id=allowed[n%len(allowed)]
            fact=claim_map[fact_id]
            a=aspects[(40+n*3+index)%len(aspects)]
            list_rows.append(
                f'<li data-fact-ids="{fact_id}">{list_openers[n]} für {a}: {fact}; '
                f'die Liste übernimmt damit nur den belegten Inhalt für die weitere Auswahl.</li>'
            )
        blocks[1]=blocks[1].replace('</section>','<ul>'+''.join(list_rows)+'</ul></section>',1)

    table_count=int(t.get('table_count_exact') or 0)
    if table_count:
        if table_count!=1:
            raise AssertionError('REAL_TABLE_COUNT_NOT_SUPPORTED')
        table_positions=[i for i,name in enumerate(other,start=1) if name=='table']
        if len(table_positions)!=1:
            raise AssertionError('REAL_BOUND_TABLE_BLOCK_MISSING_OR_DUPLICATE')
        rows=max(int(g.get('min_table_body_rows') or 1),4)
        cell_openers=(
            'Belegt für {a} ist:', 'Dokumentiert zu {a} bleibt:', 'Als Quellenpunkt für {a} gilt:',
            'Im Bereich {a} ist festgehalten:', 'Zur Einordnung von {a} dient:', 'Unter {a} bleibt gebunden:',
        )
        body=[]
        for r in range(rows):
            cells=[]
            for col in range(3):
                fact_id=allowed[(r+col)%len(allowed)]
                fact=claim_map[fact_id]
                a=aspects[(60+r*5+col*2+index)%len(aspects)]
                d=aspects[(67+r*7+col*3+index)%len(aspects)]
                opener=cell_openers[(r*3+col+index)%len(cell_openers)].format(a=a)
                cells.append(
                    f'<td data-fact-ids="{fact_id}">{opener} {fact}; '
                    f'{d} bezeichnet hier nur die sachliche Einordnung dieses Quellenpunkts.</td>'
                )
            body.append('<tr>'+''.join(cells)+'</tr>')
        table=(f'<table class="system-129-table comparison-table"><thead><tr>'
               f'<th data-fact-ids="{allowed[0]}">{identity["target_keyword"]}: Quellenpunkt</th>'
               f'<th data-fact-ids="{allowed[1%len(allowed)]}">{identity["target_keyword"]}: Einordnung</th>'
               f'<th data-fact-ids="{allowed[2%len(allowed)]}">{identity["target_keyword"]}: Prüfung</th>'
               f'</tr></thead><tbody>'+''.join(body)+'</tbody></table>')
        pos=table_positions[0]
        blocks[pos]=blocks[pos].replace('</section>',table+'</section>',1)

    if sum(1 for name in other for row in link_rows if str(row.get('section_id') or '')==name)!=len(link_rows):
        raise AssertionError('REAL_BOUND_LINK_NOT_PLACED_EXACTLY_ONCE')
    classes=' '.join(c['system4_guards']['design']['required_root_classes'])
    article=f'<article class="{classes}" data-article-type="{identity["article_type"]}">'+''.join(blocks)+'</article>'
    authoring_contract.validate_candidate(article,c)
    return article
