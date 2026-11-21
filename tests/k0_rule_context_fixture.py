import hashlib

def rule_context(identity):
    typ=identity['article_type']
    if typ=='Beratung':
        type_meta={'decision_goal':'Eine passende Entscheidung anhand der Kriterien treffen.','decision_criteria':['Kriterium A','Kriterium B']}
        blocks=('criteria','decision','further_information')
        list_name='criteria'
    elif typ=='FAQ':
        type_meta={'primary_question':identity['title']}
        blocks=('answer','details','further_information')
        list_name='key_answers'
    elif typ=='Pflege':
        type_meta={'procedure_goal':'Den Ablauf sicher und nachvollziehbar durchführen.','procedure_steps':['Schritt A','Schritt B'],'risk_controls':['Risiko A']}
        blocks=('steps','risks','further_information')
        list_name='steps'
    elif typ=='Vergleich':
        type_meta={'comparison_targets':['Option A','Option B'],'comparison_criteria':['Kriterium A','Kriterium B']}
        blocks=('options','comparison','further_information')
        list_name='advantages'
    else:
        type_meta={}
        blocks=('intro','comparison','further_information')
        list_name='criteria'
    claims={}
    for n in range(1,4):
        fid=f'F{n}'
        claims[fid]={
          'source_title':f'Quelle {n}',
          'source_url':f'https://example.test/{n}',
          'evidence_text_sha256':hashlib.sha256(f'Quelle {n}: neutraler Originaltext zur Versuchsaussage {n}.'.encode('utf-8')).hexdigest(),
          'statement':f'Belastbare Aussage {n}',
          'evidence_text':f'Quelle {n}: neutraler Originaltext zur Versuchsaussage {n}.',
          'claim_status':'FULLY_SUPPORTED',
          'article_types':[typ],
        }
    links=[
      {'role':'parent_category','href':'/parent/','anchor':'Parent','block':blocks[0]},
      {'role':'semantic_related','href':'/related/','anchor':'Related','block':blocks[1]},
      {'role':'further_information','href':'/further/','anchor':'Further','block':blocks[2]},
    ]
    return {
      'contract':'K0_AUTHORING_RULE_CONTEXT_V1',
      'type_meta':type_meta,
      'research_claims':claims,
      'required_fact_ids':['F1','F2','F3'],
      'allowed_fact_ids':['F1','F2','F3'],
      'bound_links':links,
      'link_registry':[{'href':x['href'],'active':True} for x in links],
      'runtime_link_roles':['parent_category','semantic_related','further_information'],
      'wordpress_category':{'id':0,'slug':identity['category'],'taxonomy':'category','id_source':'WORDPRESS_REST_RESOLVE_AT_RUNTIME'},
      'heading_intent_terms':[identity['target_keyword'],'Kriterium','Praxis'],
      'comparison_source_bindings':[],
      'table_decision':{
        'k0_policy':'K0_TABLE_MEANINGFUL_ONLY_V1',
        'decision':'INCLUDE_ADDED_VALUE','exception_code':None,
        'rationale':'Die Tabelle schafft einen eigenständigen Vergleichswert.',
        'reader_question':identity['target_keyword'],
        'reader_benefit':'Leser können die einzelnen Eigenschaften nach ihrem Nutzen direkt vergleichen.',
        'why_not_prose':'Im Fließtext wäre das Gegenüberstellen mehrerer eigenständiger Kriterien umständlicher.',
        'comparison_axes':['Eigenschaft des Themas','Nutzen für die Entscheidung'],
        'source_fact_ids':['F1','F2'],
      },
      'semantic_rule_results':{'table.value_required_if_present':'PASS'},
      'table_multiword_exceptions':[],
      'expected_list_name':list_name,
    }

def adapt_historical_table_context_for_current_k0(ctx):
    """QA-only table policy adaptation; source claims and identity unchanged."""
    import copy
    ctx=copy.deepcopy(ctx)
    identity=ctx['identity']
    decision=ctx['rule_context']['table_decision']
    if decision.get('k0_policy')=='K0_TABLE_MEANINGFUL_ONLY_V1':
        return ctx
    decision['k0_policy']='K0_TABLE_MEANINGFUL_ONLY_V1'
    if decision.get('decision')=='INCLUDE_ADDED_VALUE':
        decision['reader_question']=identity['target_keyword']
        decision['reader_benefit']=decision.get('rationale') or 'Leser vergleichen unabhängige Eigenschaften für ihre konkrete Frage.'
        if len(decision['reader_benefit'])<30:
            decision['reader_benefit']='Leser vergleichen unabhängige Eigenschaften für ihre konkrete Frage.'
        decision['why_not_prose']='Mehrere eigenständige Kriterien lassen sich direkt vergleichen und sind im Fließtext schwerer zu überblicken.'
        decision['comparison_axes']=['Eigenschaften und Einordnung','Unterschiedliche Nutzungssituationen']
        decision['source_fact_ids']=ctx['rule_context']['allowed_fact_ids'][:2]
    return ctx
