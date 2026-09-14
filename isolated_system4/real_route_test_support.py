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
        'intro':'Einleitung',
        'criteria':'Auswahlkriterien',
        'decision':'Entscheidung',
        'table':'Vergleich',
        'conclusion':'Fazit',
        'further_information':'weitere Informationen',
    }
    roles=(
        'Ausgangspunkt der Auswahl','Prüfmaßstab für die Nutzung','Bezugspunkt für den Vergleich',
        'Kontrollpunkt für die Entscheidung','Orientierung für die praktische Einordnung',
        'Grenze für die abschließende Bewertung','Grundlage für die sachliche Abwägung',
        'Leitlinie für die konkrete Prüfung','Bezugsgröße für die Planung',
        'Kriterium für die nachvollziehbare Auswahl','Prüfpunkt für die Alltagstauglichkeit',
        'Maßstab für die abschließende Kontrolle',
    )
    perspectives=(
        'ohne die Quellenaussage zu erweitern','mit direktem Bezug auf den gesicherten Quellenstand',
        'ausschließlich innerhalb des belegten Aussageumfangs','als klar abgegrenzter Teil der Auswahlprüfung',
        'für eine nachvollziehbare und an die Quelle gebundene Entscheidung',
        'mit Trennung zwischen belegter Aussage und bloßer Vermutung','als fester Bezug für die weitere Einordnung',
        'mit Konzentration auf den tatsächlich belegten Punkt','als überprüfbare Grundlage der Entscheidung',
        'ohne zusätzliche fachliche Behauptung','mit eindeutiger Bindung an den realen Quellenstand',
        'als dokumentierter Prüfpunkt im Artikel',
    )
    transitions=(
        'Damit bleibt für diesen Abschnitt eindeutig, welcher Quellenpunkt die Bewertung trägt',
        'So lässt sich die Entscheidung an einer nachprüfbaren Aussage ausrichten',
        'Auf diese Weise bleibt die Einordnung eng am belegten Inhalt',
        'Dadurch wird der Prüfschritt nicht durch unbelegte Zusatzannahmen erweitert',
        'So bleibt die fachliche Grenze der belegten Aussage sichtbar',
        'Damit ist die Grundlage der Auswahl für den Leser nachvollziehbar',
        'Dadurch bleibt die Aussage auch bei der praktischen Einordnung überprüfbar',
        'So wird der reale Quellenpunkt konsequent von allgemeinen Annahmen getrennt',
        'Damit bleibt die Argumentation innerhalb des gebundenen Faktenrahmens',
        'So kann der Abschnitt auf einem klar benannten Quellenpunkt aufbauen',
        'Dadurch wird der belegte Inhalt nicht durch neue Tatsachen ersetzt',
        'Damit bleibt die belegte Aussage in ihrer ursprünglichen Bedeutung erhalten',
    )

    def display_section(section:str)->str:
        return section_labels.get(section,'Sachprüfung')

    def sentence(fact_id:str,seed:int,section:str)->str:
        fact=claim_map[fact_id]
        role=roles[(seed+index*3)%len(roles)]
        perspective=perspectives[(seed*2+index)%len(perspectives)]
        transition=transitions[(seed*5+index)%len(transitions)]
        return f'Bei „{display_section(section)}“ dient folgende belegte Aussage als {role}: {fact}; sie wird {perspective} verwendet. {transition}.'

    fid=allowed[0]
    intro_text=sentence(fid,1,'intro')
    if len(intro_text.split())<ilo:
        intro_text+=' Der Einstieg benennt damit nur den belegten Ausgangspunkt und lässt weitergehende Annahmen bewusst außen vor.'
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
    expected_link_blocks=[str(row.get('section_id') or '') for row in link_rows]
    missing_link_blocks=[name for name in expected_link_blocks if name not in other]
    if missing_link_blocks:
        raise AssertionError('REAL_BOUND_LINK_SECTION_MISSING:'+','.join(missing_link_blocks))

    heading_suffixes=(
        'sachlich einordnen','gezielt prüfen','für die Auswahl bewerten','im Vergleich betrachten',
        'für die Praxis abwägen','als Entscheidungspunkt nutzen','an der Quelle prüfen','nachvollziehbar zusammenführen',
    )
    target_paras=max(min_paragraphs-1,len(other)*2,4)
    paras_per=max(2,(target_paras+len(other)-1)//len(other))
    target_words=max(min_words-len(intro_text.split()),500)
    words_per=max(48,(target_words+len(other)*paras_per-1)//(len(other)*paras_per))

    seed=10
    for bi,name in enumerate(other):
        intent=intent_terms[(bi+index)%len(intent_terms)]
        heading=f'{intent} {heading_suffixes[(bi+index)%len(heading_suffixes)]}'
        parts=[f'<h2>{heading}</h2>']
        section_links=[row for row in link_rows if str(row.get('section_id') or '')==name]
        for pi in range(paras_per):
            fact_id=allowed[(bi+pi)%len(allowed)]
            text=sentence(fact_id,seed,name)
            addon=0
            while len(text.split())<words_per:
                addon+=1
                extra_seed=seed+addon*7
                extra_role=roles[extra_seed%len(roles)]
                extra_perspective=perspectives[(extra_seed+3)%len(perspectives)]
                starters=('Zusätzlich','Ergänzend','Daneben','Für die Auswahl','Bei der Prüfung','Im nächsten Schritt')
                starter=starters[(extra_seed+index)%len(starters)]
                text+=f' {starter} wird dieser Quellenpunkt bei {identity["target_keyword"]} als {extra_role} betrachtet, {extra_perspective}; maßgeblich bleibt dabei nur die bereits belegte Aussage.'
            if pi==0:
                for row in section_links:
                    text+=f' <a href="{row["href"]}">{row["anchor"]}</a>'
            parts.append(f'<p data-fact-ids="{fact_id}">{text}</p>')
            seed+=1
        blocks.append(f'<section data-block="{name}">'+''.join(parts)+'</section>')

    if len(blocks)>1:
        list_starts=(
            'Die Grundprüfung hält fest:',
            'Bei der Nutzungsprüfung gilt:',
            'Im Vergleich wird beachtet:',
            'Zum Abschluss wird geprüft:',
        )
        list_rows=[]
        for n in range(4):
            fact_id=allowed[n%len(allowed)]
            fact=claim_map[fact_id]
            list_rows.append(f'<li data-fact-ids="{fact_id}">{list_starts[n]} „{fact}“ bleibt als eigener belegter Prüfpunkt erhalten.</li>')
        blocks[1]=blocks[1].replace('</section>','<ul>'+''.join(list_rows)+'</ul></section>',1)

    table_count=int(t.get('table_count_exact') or 0)
    if table_count:
        if table_count!=1:
            raise AssertionError('REAL_TABLE_COUNT_NOT_SUPPORTED')
        table_positions=[i for i,name in enumerate(other,start=1) if name=='table']
        if len(table_positions)!=1:
            raise AssertionError('REAL_BOUND_TABLE_BLOCK_MISSING_OR_DUPLICATE')
        rows=max(int(g.get('min_table_body_rows') or 1),4)
        table_labels=(
            ('Quellenpunkt','Bedeutung für die Auswahl','Prüfschritt'),
            ('Belegter Maßstab','Praktische Einordnung','Entscheidungsbezug'),
            ('Gebundene Aussage','Kontrollperspektive','Abschlussprüfung'),
            ('Faktenbasis','Vergleichsaspekt','Dokumentierter Bezug'),
        )
        cell_frames=(
            'Als Quellenkern bleibt festgehalten: {fact}.',
            'Für die sachliche Einordnung wird ausschließlich dieser belegte Punkt genutzt: {fact}.',
            'Die Auswahlprüfung erhält damit einen klaren Bezug: {fact}.',
            'Im Vergleich wird die folgende Aussage als abgegrenzter Maßstab geführt: {fact}.',
            'Für die praktische Bewertung ist dieser Quellenpunkt dokumentiert: {fact}.',
            'Die Entscheidung wird an dieser gebundenen Aussage gespiegelt: {fact}.',
            'Als Kontrollgrundlage dient die belegte Aussage: {fact}.',
            'Für die abschließende Prüfung bleibt dieser Beleg maßgeblich: {fact}.',
            'Der Quellenstand liefert für diesen Tabellenpunkt folgende Aussage: {fact}.',
            'Zur nachvollziehbaren Abwägung wird diese Quellenaussage getrennt ausgewiesen: {fact}.',
            'Der Vergleich stützt sich an dieser Stelle auf den gebundenen Inhalt: {fact}.',
            'Als dokumentierte Entscheidungsbasis gilt hier der Quellenpunkt: {fact}.',
        )
        body=[]
        for r in range(rows):
            cells=[]
            for col in range(3):
                fact_id=allowed[(r+col)%len(allowed)]
                fact=claim_map[fact_id]
                frame=cell_frames[(r*3+col)%len(cell_frames)]
                cells.append(f'<td data-fact-ids="{fact_id}">{frame.format(fact=fact)}</td>')
            body.append('<tr>'+''.join(cells)+'</tr>')
        labels=table_labels[index%len(table_labels)]
        table=(f'<table class="system-129-table comparison-table"><thead><tr>'
               f'<th data-fact-ids="{allowed[0]}">{identity["target_keyword"]}: {labels[0]}</th>'
               f'<th data-fact-ids="{allowed[1%len(allowed)]}">{identity["target_keyword"]}: {labels[1]}</th>'
               f'<th data-fact-ids="{allowed[2%len(allowed)]}">{identity["target_keyword"]}: {labels[2]}</th>'
               f'</tr></thead><tbody>'+''.join(body)+'</tbody></table>')
        pos=table_positions[0]
        blocks[pos]=blocks[pos].replace('</section>',table+'</section>',1)

    if sum(1 for name in other for row in link_rows if str(row.get('section_id') or '')==name)!=len(link_rows):
        raise AssertionError('REAL_BOUND_LINK_NOT_PLACED_EXACTLY_ONCE')
    classes=' '.join(c['system4_guards']['design']['required_root_classes'])
    article=f'<article class="{classes}" data-article-type="{identity["article_type"]}">'+''.join(blocks)+'</article>'
    authoring_contract.validate_candidate(article,c)
    return article
