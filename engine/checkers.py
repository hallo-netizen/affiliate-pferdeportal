import hashlib, html as htmlmod, re
from collections import Counter
from html.parser import HTMLParser
from .core import load_values, stable
from .receipt import make_receipt

SPECIAL_HEADINGS={'fazit','weiterführende informationen','weiterfuehrende informationen'}
STOPWORDS={'der','die','das','den','dem','des','ein','eine','einer','eines','und','oder','mit','ohne','für','fuer','von','vor','nach','bei','im','in','am','an','auf','aus','zu','zum','zur','ist','sind','wird','werden','was','wie','wann','warum','welche','welcher','welches'}

class _BalanceParser(HTMLParser):
    VOID={'br','img','meta','link','hr','input','source','area','base','col','embed','param','track','wbr'}
    def __init__(self):
        super().__init__(); self.stack=[]; self.ok=True
    def handle_starttag(self,tag,attrs):
        if tag not in self.VOID: self.stack.append(tag)
    def handle_startendtag(self,tag,attrs):
        return
    def handle_endtag(self,tag):
        if tag in self.VOID: return
        if not self.stack or self.stack[-1]!=tag: self.ok=False; return
        self.stack.pop()

def article_hash(article):
    bound={k:article.get(k) for k in ('article_type','title','target_keyword','type_meta','research_claims','required_fact_ids','allowed_fact_ids','bound_links','link_registry','runtime_link_roles','wordpress_category','heading_intent_terms','comparison_source_bindings','table_decision','html')}
    return stable(bound)

def _plain(value):
    value=re.sub(r'(?is)<(script|style)\b[^>]*>.*?</\1>',' ',str(value or ''))
    value=re.sub(r'(?s)<[^>]+>',' ',value)
    return re.sub(r'\s+',' ',htmlmod.unescape(value)).strip()

def _norm(value):
    value=_plain(value).casefold().replace('ß','ss')
    value=re.sub(r'[^a-z0-9äöü]+',' ',value)
    return re.sub(r'\s+',' ',value).strip()

def _words(value):
    return re.findall(r'\b[\wÄÖÜäöüß-]+\b',_plain(value),re.UNICODE)

def _sig_tokens(value):
    return {x for x in _norm(value).split() if len(x)>=4 and x not in STOPWORDS}

def _sections(html):
    out=[]
    for m in re.finditer(r'(?is)<section\b([^>]*)>(.*?)</section>',str(html or '')):
        attrs=m.group(1); body=m.group(2)
        bm=re.search(r'data-block\s*=\s*["\']([^"\']+)["\']',attrs,re.I)
        block=bm.group(1) if bm else ''
        hm=re.search(r'(?is)<h2\b[^>]*>(.*?)</h2>',body)
        heading=_plain(hm.group(1)) if hm else ''
        content=body[hm.end():] if hm else body
        out.append({'block':block,'raw':m.group(0),'body':body,'heading':heading,'content':content,'text':_plain(content),'start':m.start(),'end':m.end()})
    return out

def _attrs(tag):
    return {k.lower():v for k,_,v in re.findall(r'([\w:-]+)\s*=\s*(["\'])(.*?)\2',tag,re.S)}

def _trace_tags(html,trace_class='ppm-source-trace'):
    out=[]
    for tag in re.findall(r'(?is)<span\b[^>]*>',str(html or '')):
        a=_attrs(tag); classes=set(a.get('class','').split())
        if trace_class in classes: out.append(a)
    return out

def _data_fact_ids(html):
    ids=[]
    for raw in re.findall(r'data-fact-ids\s*=\s*["\']([^"\']+)["\']',str(html or ''),re.I): ids.extend(raw.split())
    return ids

def _sentences(text):
    return [x.strip() for x in re.split(r'(?<=[.!?])\s+',_plain(text)) if x.strip()]

def _receipt(rule_id,owner,article,status,evidence=None):
    return make_receipt(rule_id,owner,'ARTICLE',article['article_id'],article_hash(article),status,evidence)

def _html_balanced(html):
    p=_BalanceParser()
    try: p.feed(str(html or '')); p.close()
    except Exception: return False
    return bool(p.ok and not p.stack)

def _links(html):
    sections=_sections(html); rows=[]
    for s in sections:
        for m in re.finditer(r'(?is)<a\b([^>]*)>(.*?)</a>',s['raw']):
            a=_attrs('<a '+m.group(1)+'>')
            rows.append({'block':s['block'],'role':a.get('data-link-role',''),'href':a.get('href',''),'anchor':_plain(m.group(2))})
    return rows

def _paragraphs(section):
    return [_plain(x) for x in re.findall(r'(?is)<p\b[^>]*>(.*?)</p>',section.get('body','')) if _plain(x)]

def _duplicate_ratio(text):
    ss=[_norm(s) for s in _sentences(text) if len(_words(s))>=5]
    if not ss: return 0.0
    c=Counter(ss); duplicate_excess=sum(max(0,n-1) for n in c.values())
    return duplicate_excess/len(ss)

def _max_pair_similarity(texts):
    sets=[_sig_tokens(x) for x in texts if _sig_tokens(x)]
    best=0.0
    for i in range(len(sets)):
        for j in range(i+1,len(sets)):
            u=sets[i]|sets[j]
            if u: best=max(best,len(sets[i]&sets[j])/len(u))
    return best

def structural_receipts(article):
    v=load_values(); legacy=v['ppm_parity']; cfg=v['types'].get(article.get('article_type')) or {}
    html=article['html']; title=str(article.get('title') or ''); kw=str(article.get('target_keyword') or '')
    sections=_sections(html); blocks=[x['block'] for x in sections if x['block']]
    block_map={s['block']:s for s in sections if s['block']}
    lists=set(re.findall(r'data-list\s*=\s*["\']([^"\']+)["\']',html,re.I))
    links=_links(html)
    required_blocks=list(cfg.get('required_blocks') or [])
    required_lists=set(cfg.get('required_lists') or [])
    meta=article.get('type_meta') or {}; schema=cfg.get('type_meta_schema') or {}; meta_ok=True; meta_find=[]
    for name in schema.get('required') or []:
        if name not in meta: meta_ok=False; meta_find.append('missing:'+name)
    for name,spec in (schema.get('fields') or {}).items():
        if name not in meta: continue
        val=meta[name]; typ=spec.get('type')
        if typ=='string':
            if not isinstance(val,str) or len(val.strip())<int(spec.get('min_length',0)): meta_ok=False; meta_find.append('invalid:'+name)
        elif typ=='list':
            if not isinstance(val,list) or len(val)<int(spec.get('min_items',0)): meta_ok=False; meta_find.append('invalid:'+name)
            elif spec.get('unique_items') and len({str(x) for x in val})!=len(val): meta_ok=False; meta_find.append('duplicate:'+name)
    qm=(cfg.get('question_mark')!='REQUIRED' or title.rstrip().endswith('?'))
    title_norm=_norm(title); body_norm=_norm(html)
    h1_count=len(re.findall(r'(?is)<h1\b',html))
    visible_marker=bool(re.search(legacy['visible_test_marker_regex'],_plain(html),re.I))
    machine_words=[w for w in legacy.get('forbidden_machine_status_words',[]) if w.casefold() in _plain(html).casefold()]
    p_count=len(re.findall(r'(?is)<p\b',html)); h2_count=len(re.findall(r'(?is)<h2\b',html))
    nonempty_missing=[b for b in required_blocks if b not in block_map or not _plain(block_map[b]['body'])]
    expected=[b for b in required_blocks if b!='table' or 'table' in block_map]
    order_ok=[b for b in blocks if b in expected]==expected
    h2_bad=[]; p_bad=[]
    for b in expected:
        s=block_map.get(b)
        if not s: continue
        if b!='intro':
            hc=len(re.findall(r'(?is)<h2\b[^>]*>.*?</h2>',s['body']))
            if hc!=1: h2_bad.append((b,hc))
        if b not in ('checklist',):
            pc=len(re.findall(r'(?is)<p\b[^>]*>.*?</p>',s['body']))
            if pc<1: p_bad.append(b)
    max_list=max([len(re.findall(r'(?is)<li\b[^>]*>.*?</li>',x)) for x in re.findall(r'(?is)<(?:ul|ol)\b[^>]*>.*?</(?:ul|ol)>',html)] or [0])
    intro=block_map.get('intro'); intro_pars=_paragraphs(intro) if intro else []
    intro_words=sum(len(_words(x)) for x in intro_pars)
    intro_ok=bool(sections and sections[0]['block']=='intro' and intro and len(re.findall(r'(?is)<h[1-6]\b',intro['body']))==0 and intro_pars and legacy['intro']['minimum_words']<=intro_words<=legacy['intro']['maximum_words'])
    adjacent_bad=bool(re.search(r'(?is)</h[2-6]>\s*<h[2-6]\b',html))
    between_bad=[]
    min_between=int(legacy['headings']['minimum_words_between_headings'])
    for s in sections:
        if s['heading'] and s['block'] not in ('conclusion','further_information') and len(_words(s['content']))<min_between:
            between_bad.append(s['block'])
    faq_ok=True; faq_evidence={}
    if article.get('article_type')=='FAQ':
        ans=block_map.get('answer'); pars=_paragraphs(ans) if ans else []
        first=pars[0] if pars else ''
        faq_ok=bool(first and len(_words(first))>=int(legacy['faq']['direct_answer_minimum_words']))
        nf=_norm(first)
        bad_open=[x for x in legacy['faq']['forbidden_meta_openings'] if nf.startswith(_norm(x))]
        faq_ok=faq_ok and not bad_open; faq_evidence={'words':len(_words(first)),'forbidden_openings':bad_open}
    category=article.get('wordpress_category') or {}; forbidden_slugs=set(legacy['wordpress_binding']['forbidden_category_slugs'])
    category_ok=(int(category.get('id') or 0)>=int(legacy['wordpress_binding']['category_id_minimum']) and str(category.get('slug') or '').casefold() not in forbidden_slugs)
    actual_pairs={(x['role'],x['href'],x['anchor']) for x in links}
    bound=article.get('bound_links') or []
    expected_pairs={(str(x.get('role') or ''),str(x.get('href') or ''),str(x.get('anchor') or '')) for x in bound}
    bound_ok=(actual_pairs==expected_pairs) if bound else False
    registry={str(x.get('href') or ''):x for x in article.get('link_registry') or []}
    registry_ok=bool(links) and all(x['href'] in registry and registry[x['href']].get('active',True) for x in links)
    placement_ok=bool(bound) and all(any(y['role']==x.get('role') and y['href']==x.get('href') and y['block']==x.get('block') for y in links) for x in bound)
    relative_ok=all(x['href'].startswith('/') and not x['href'].startswith('//') and '://' not in x['href'] for x in links)
    further_ok=sum(1 for x in links if x['role']=='further_information' and x['block']=='further_information')==1
    distributed_ok=(len(links)==len({x['block'] for x in links})) if links else False
    runtime_roles=set(article.get('runtime_link_roles') or [])
    runtime_ok=runtime_roles==set(v['global']['required_link_roles'])
    clustered_ok=not (links and all(x['block']=='further_information' for x in links)) and all(x['block']!='further_information' for x in links if x['role']!='further_information')
    rows=[
      ('title.keyword_required',bool(kw and kw.casefold() in title.casefold()),{'title':title,'keyword':kw}),
      ('title.colon_forbidden',':' not in title,{}),
      ('structure.duplicate_block_names_forbidden',len(blocks)==len(set(blocks)),{'blocks':blocks}),
      ('structure.required_blocks',set(required_blocks).issubset(set(blocks)),{'missing':sorted(set(required_blocks)-set(blocks))}),
      ('structure.required_lists',required_lists.issubset(lists),{'missing':sorted(required_lists-lists)}),
      ('links.visible_exact',len(links)==int(v['global']['visible_links_exact']),{'actual':len(links)}),
      ('links.required_roles',{x['role'] for x in links}==set(v['global']['required_link_roles']),{'actual':sorted({x['role'] for x in links})}),
      ('type.question_mark_policy',qm,{}),('type.metadata_schema',meta_ok,{'findings':meta_find}),
      ('structure.body_h1_forbidden',h1_count==0,{'actual':h1_count}),
      ('structure.title_not_repeated_in_body',not bool(title_norm and title_norm in body_norm),{}),
      ('structure.visible_test_marker_forbidden',not visible_marker,{}),
      ('structure.machine_status_word_forbidden',not machine_words,{'hits':machine_words}),
      ('structure.paragraph_floor',p_count>=int(legacy['content']['minimum_paragraphs']),{'actual':p_count}),
      ('structure.h2_floor',h2_count>=int(legacy['content']['minimum_h2']),{'actual':h2_count}),
      ('structure.required_blocks_nonempty',not nonempty_missing,{'missing':nonempty_missing}),
      ('structure.section_ids_unique',len(blocks)==len(set(blocks)),{'blocks':blocks}),
      ('structure.section_order',order_ok,{'actual':blocks,'expected':expected}),
      ('structure.section_h2_exact_one',not h2_bad,{'bad':h2_bad}),
      ('structure.section_paragraph_required',not p_bad,{'bad':p_bad}),
      ('structure.list_minimum_items',max_list>=int(legacy['lists']['minimum_items_in_one_list']),{'max_items':max_list}),
      ('structure.intro_first',bool(sections and sections[0]['block']=='intro'),{}),
      ('structure.intro_structure',intro_ok,{'words':intro_words}),
      ('structure.adjacent_headings_forbidden',not adjacent_bad,{}),
      ('structure.faq_direct_answer',faq_ok,faq_evidence),
      ('structure.text_between_headings_minimum',not between_bad,{'bad':between_bad}),
      ('structure.html_balanced',_html_balanced(html),{}),
      ('links.bound_pairs_exact',bound_ok,{'actual':sorted(actual_pairs),'expected':sorted(expected_pairs)}),
      ('links.registry_active',registry_ok,{}),('links.section_placement',placement_ok,{}),
      ('links.relative_internal_only',relative_ok,{}),('links.further_information_position',further_ok,{}),
      ('links.distributed_across_blocks',distributed_ok,{}),('links.runtime_roles_bound',runtime_ok,{}),
      ('links.not_clustered_at_end',clustered_ok,{}),('wordpress.semantic_category_binding',category_ok,category),
    ]
    return [_receipt(rid,'structural_checker',article,'PASS' if ok else 'FAIL',ev) for rid,ok,ev in rows]

def fact_receipts(article):
    v=load_values(); legacy=v['ppm_parity']; html=article['html']; typ=article['article_type']; cfg=v['types'][typ]
    trace_cfg=v['global']['source_trace']; traces=_trace_tags(html,trace_cfg['class']); claims=article.get('research_claims') or {}
    attrs_ok=True; binding_find=[]; real_ok=True; real_find=[]
    for t in traces:
        for attr in trace_cfg['required_attributes']:
            if not t.get(attr): attrs_ok=False; binding_find.append('missing:'+attr)
        fid=t.get('data-fact-id',''); claim=claims.get(fid)
        if not claim: attrs_ok=False; binding_find.append('unknown:'+fid); continue
        if t.get('data-source-title')!=str(claim.get('source_title') or ''): attrs_ok=False; binding_find.append('title:'+fid)
        if t.get('data-source-hash')!=str(claim.get('evidence_text_sha256') or ''): attrs_ok=False; binding_find.append('hash:'+fid)
        title=str(t.get('data-source-title') or ''); h=str(t.get('data-source-hash') or '')
        placeholder=bool(re.fullmatch(r'(?i)\s*(?:test|dummy|example|beispiel|placeholder)(?:\s+(?:quelle|source|f?\d+))*\s*',title))
        if placeholder: real_ok=False; real_find.append('title:'+fid)
        if not re.fullmatch(r'[0-9a-fA-F]{64}',h) or len(set(h.casefold()))<4: real_ok=False; real_find.append('hash:'+fid)
    used_ids=set(_data_fact_ids(html)); known_ids=set(claims); unknown=sorted(used_ids-known_ids)
    trace_required=(len(traces)>=int(trace_cfg['minimum_count']) and not unknown)
    sections={s['block']:s for s in _sections(html) if s['block']}; block_find=[]
    for block in cfg.get('fact_trace_required_blocks') or []:
        sec=sections.get(block)
        if sec is not None and not _trace_tags(sec['raw'],trace_cfg['class']): block_find.append(block)
    required_blocks_ok=not block_find
    factual_units=[]
    for s in _sections(html):
        if s['block']=='further_information': continue
        for tag,inner in re.findall(r'(?is)<(p|li|td)\b[^>]*>(.*?)</\1>',s['raw']):
            raw_match=None
            # locate a matching full tag for data-fact-ids; simplified by searching inner text in section tags
            candidates=re.findall(r'(?is)<'+tag+r'\b[^>]*>.*?</'+tag+r'>',s['raw'])
            for cand in candidates:
                if inner in cand: raw_match=cand; break
            if _plain(inner): factual_units.append((s['block'],raw_match or inner,_plain(inner)))
    unbound=[]
    lexical_total=0; lexical_supported=0; numeric_bad=[]
    for block,raw,text in factual_units:
        ids=set(_data_fact_ids(raw))
        if not ids: unbound.append(block); continue
        ref_claims=[claims.get(fid) for fid in ids if claims.get(fid)]
        if ref_claims:
            lexical_total+=1
            visible=_sig_tokens(text)
            fact_tokens=set()
            for cl in ref_claims:
                fact_tokens|=_sig_tokens(str(cl.get('statement') or '')+' '+str(cl.get('evidence_text') or ''))
            if visible & fact_tokens: lexical_supported+=1
        for num in re.findall(r'(?<![A-Za-zÄÖÜäöüß])\d+(?:[.,]\d+)?(?![A-Za-zÄÖÜäöüß])',text):
            support=' '.join(str((cl or {}).get('statement') or '')+' '+str((cl or {}).get('evidence_text') or '') for cl in ref_claims)
            if num not in support: numeric_bad.append((block,num))
    visible_refs_ok=not unbound
    exists_ok=not unknown
    verified_bad=[fid for fid in used_ids if fid in claims and str(claims[fid].get('claim_status') or '')!='FULLY_SUPPORTED']
    type_bad=[fid for fid in used_ids if fid in claims and typ not in (claims[fid].get('article_types') or [])]
    required_ids=set(article.get('required_fact_ids') or known_ids)
    coverage=(len(used_ids & required_ids)/len(required_ids) if required_ids else 1.0)
    coverage_ok=coverage>=float(legacy['facts']['required_selected_fact_coverage_ratio'])
    lex_ratio=(lexical_supported/lexical_total if lexical_total else 1.0)
    lexical_ok=lex_ratio>=float(legacy['facts']['minimum_trace_lexical_support_ratio'])
    allow=set(article.get('allowed_fact_ids') or [])
    allow_ok=bool(allow) and used_ids.issubset(allow)
    comparison_ok=True; comparison_find=[]
    if typ=='Vergleich':
        bindings=article.get('comparison_source_bindings') or []
        comparison_ok=bool(bindings) and all(str(x.get('source_label') or '')==str(x.get('nearest_option_heading') or '') for x in bindings)
        comparison_find=[x for x in bindings if str(x.get('source_label') or '')!=str(x.get('nearest_option_heading') or '')]
    conclusion=sections.get('conclusion'); conclusion_ok=True; conclusion_find=[]
    if conclusion:
        cids=set(_data_fact_ids(conclusion['raw'])); tids={x.get('data-fact-id') for x in _trace_tags(conclusion['raw'],trace_cfg['class'])}
        if not cids.issubset(tids): conclusion_ok=False; conclusion_find=sorted(cids-tids)
    rows=[
      ('facts.trace_required',trace_required,{'trace_count':len(traces),'unknown_fact_ids':unknown}),
      ('facts.trace_binding',attrs_ok,{'findings':binding_find}),('facts.trace_required_blocks',required_blocks_ok,{'missing_trace_blocks':block_find}),
      ('facts.conclusion_no_new_untraced_facts',conclusion_ok,{'untraced':conclusion_find}),
      ('facts.real_source_trace',real_ok,{'findings':real_find}),('facts.source_label_option_match',comparison_ok,{'findings':comparison_find}),
      ('facts.visible_unit_fact_refs',visible_refs_ok,{'unbound':unbound}),('facts.referenced_fact_exists',exists_ok,{'unknown':unknown}),
      ('facts.referenced_fact_verified',not verified_bad,{'bad':verified_bad}),('facts.referenced_fact_type_allowed',not type_bad,{'bad':type_bad}),
      ('facts.numeric_claim_supported',not numeric_bad,{'bad':numeric_bad}),('facts.fact_pack_coverage',coverage_ok,{'actual':coverage}),
      ('facts.trace_lexical_support',lexical_ok,{'actual':lex_ratio,'supported':lexical_supported,'total':lexical_total}),
      ('facts.runtime_fact_allowlist',allow_ok,{'allowed':sorted(allow),'used':sorted(used_ids)}),
    ]
    return [_receipt(rid,'fact_trace_checker',article,'PASS' if ok else 'FAIL',ev) for rid,ok,ev in rows]

def editorial_receipts(article):
    v=load_values(); cfg=v['heading']; legacy=v['ppm_parity']; html=article['html']; sections=_sections(html)
    headings=[s['heading'] for s in sections if s['heading']]; norm=[_norm(x) for x in headings]
    title=_norm(article.get('title')); target=_norm(article.get('target_keyword')); collision=bool(target and title==target)
    exact=sum(1 for h in norm if target and target in h)
    lo=int(cfg['exact_target_phrase_occurrences_when_title_equals_target']) if collision else int(cfg['exact_target_phrase_occurrences_min_when_no_title_collision'])
    hi=int(cfg['exact_target_phrase_occurrences_when_title_equals_target']) if collision else int(cfg['exact_target_phrase_occurrences_max'])
    target_ok=lo<=exact<=hi
    stop=set(cfg['significant_keyword_stop_tokens']); sig=[x for x in target.split() if len(x)>=4 and x not in stop]
    token_counts={tok:sum(tok in h.split() for h in norm) for tok in set(sig)}
    staccato_ok=all(n<=int(cfg['significant_target_keyword_token_h2_occurrences_max']) for n in token_counts.values())
    leads=[h.split()[0] for h in norm if h and h not in SPECIAL_HEADINGS]; lead_counts=Counter(leads)
    phrase_ok=all(n<=int(cfg['repeated_heading_lead_word_max']) for n in lead_counts.values())
    duplicate_ok=len(norm)==len(set(norm))
    hard_ok=all(len(_words(h))<=int(cfg['hard_h2_words_max']) and len(h)<=int(cfg['hard_h2_chars_max']) for h in headings)
    endings=[h.split()[-1] for h in norm if h and h not in SPECIAL_HEADINGS]; end_counts=Counter(endings)
    grammar_ok=all(n<=int(cfg['repeated_heading_end_word_max']) for n in end_counts.values())
    natural_find=[]; meta_tokens=set()
    for p in cfg['abstract_meta_patterns']: meta_tokens.update(_norm(p).split())
    generic={_norm(x) for x in legacy['headings']['generic_or_technical_headings']}|{_norm(x) for x in legacy['known_bad_headings']}
    fragments=[_norm(x) for x in legacy['headings']['forbidden_fragments']]
    for s in sections:
        hn=_norm(s['heading'])
        if not hn or hn in SPECIAL_HEADINGS: continue
        if hn in generic or any(f and f in hn for f in fragments): natural_find.append('generic:'+s['heading']); continue
        if any(_norm(p) in hn for p in cfg['abstract_meta_patterns']): natural_find.append('abstract:'+s['heading']); continue
        ht={x for x in hn.split() if len(x)>=4 and x not in stop and x not in meta_tokens}; ct=set(_norm(s['text']).split())
        if ht and len(ht & ct)<int(cfg['content_overlap_min_significant_tokens']): natural_find.append('content:'+s['heading'])
    natural_ok=not natural_find
    intent_terms={_norm(x) for x in article.get('heading_intent_terms') or [] if _norm(x)}
    intent_bad=[]
    for s in sections:
        hn=_norm(s['heading'])
        if not hn or hn in SPECIAL_HEADINGS: continue
        if intent_terms and not (_sig_tokens(hn)&set().union(*[_sig_tokens(x) for x in intent_terms])): intent_bad.append(s['heading'])
    intent_ok=bool(intent_terms) and not intent_bad
    sem_bad=[]; threshold=float(legacy['headings']['near_duplicate_token_similarity'])
    hrows=[(s['heading'],_sig_tokens(s['heading'])) for s in sections if _norm(s['heading']) not in SPECIAL_HEADINGS and _sig_tokens(s['heading'])]
    for i in range(len(hrows)):
        for j in range(i+1,len(hrows)):
            a,b=hrows[i][1],hrows[j][1]; sim=len(a&b)/len(a|b) if a|b else 0
            if sim>=threshold: sem_bad.append((hrows[i][0],hrows[j][0],sim))
    forbidden=[x.casefold() for x in v['surface']['forbidden_generator_phrases']]
    non_template_ok=not any(p in _plain(html).casefold() for p in forbidden)
    sentences=[_norm(x) for x in _sentences(html) if len(_words(x))>=5]; repeats=Counter(sentences)
    repetition_ok=all(n==1 for n in repeats.values())
    plain_cf=_plain(html).casefold(); reg_hits=[x for x in legacy['known_error_regression_patterns'] if x.casefold() in plain_cf]
    unnatural_hits=[x for x in legacy['known_language_regression_phrases'] if x.casefold() in plain_cf]
    dup_ratio=_duplicate_ratio(html); intro=next((s for s in sections if s['block']=='intro'),None); intro_sim=_max_pair_similarity(_paragraphs(intro) if intro else [])
    intro_cfg=v['intro_orientation']; intro_pars=_paragraphs(intro) if intro else []
    first_sentence=''
    if intro_pars:
        ss=_sentences(intro_pars[0]); first_sentence=ss[0] if ss else intro_pars[0]
    first_words=len(_words(first_sentence))
    topic_tokens=_sig_tokens(article.get('target_keyword') or article.get('title') or '')
    first_tokens=_sig_tokens(first_sentence)
    overlap=len(topic_tokens & first_tokens)
    intro_orientation_ok=bool(
        first_sentence
        and int(intro_cfg['first_sentence_minimum_words'])<=first_words<=int(intro_cfg['first_sentence_maximum_words'])
        and overlap>=int(intro_cfg['subject_overlap_minimum_significant_tokens'])
    )
    rows=[
      ('heading.target_phrase_control',target_ok,{'actual':exact,'min':lo,'max':hi}),('heading.keyword_staccato_forbidden',staccato_ok,{'counts':token_counts}),
      ('heading.phrase_family_repetition_forbidden',phrase_ok,{'counts':dict(lead_counts)}),('heading.duplicate_normalized_forbidden',duplicate_ok,{}),
      ('heading.hard_length',hard_ok,{}),('heading.natural_concrete_section_language',natural_ok,{'findings':natural_find}),
      ('heading.grammatical_variety',grammar_ok,{'endings':dict(end_counts)}),('surface.non_template_language',non_template_ok,{}),
      ('surface.repetition_forbidden',repetition_ok,{'duplicates':{k:v for k,v in repeats.items() if v>1}}),
      ('heading.intent_binding',intent_ok,{'bad':intent_bad,'terms':sorted(intent_terms)}),('heading.semantic_duplicate_forbidden',not sem_bad,{'bad':sem_bad}),
      ('surface.known_regression_patterns_forbidden',not reg_hits,{'hits':reg_hits}),('surface.known_unnatural_language_forbidden',not unnatural_hits,{'hits':unnatural_hits}),
      ('surface.duplicate_sentence_ratio',dup_ratio<=float(legacy['content']['maximum_duplicate_sentence_ratio']),{'actual':dup_ratio}),
      ('surface.intro_similarity',intro_sim<=float(legacy['content']['maximum_intro_pair_similarity']),{'actual':intro_sim}),
      ('intro.orientation_sentence',intro_orientation_ok,{'first_sentence':first_sentence,'words':first_words,'subject_overlap':overlap,'topic_tokens':sorted(topic_tokens)}),
    ]
    return [_receipt(rid,'editorial_checker',article,'PASS' if ok else 'FAIL',ev) for rid,ok,ev in rows]

def _strip_blocks(html,blocks):
    out=str(html or '')
    for block in blocks: out=re.sub(r'(?is)<section\b[^>]*data-block\s*=\s*(["\'])'+re.escape(block)+r'\1[^>]*>.*?</section>',' ',out)
    return out

def balance_receipts(article):
    v=load_values(); cfg=v['balance']; typ=v['types'][article['article_type']]; html=article['html']; sections=_sections(html); total=len(_words(html))
    normal=[s for s in sections if s['block'] not in set(cfg['exempt_blocks']) and s['heading']]; counts=[len(_words(s['content'])) for s in normal]
    section_ok=all(int(cfg['normal_h2_section_min_words'])<=n<=int(cfg['normal_h2_section_max_words']) for n in counts)
    ratio_ok=(not counts or min(counts)>0 and max(counts)/min(counts)<=float(cfg['normal_h2_longest_to_shortest_max_ratio']))
    main_ratio=(sum(counts)/total if total else 0.0); main_ok=main_ratio>=float(cfg['normal_h2_combined_minimum_ratio'])
    further=next((s for s in sections if s['block']=='further_information'),None); further_words=len(_words(further['content'])) if further else 0
    further_ok=further_words<=int(cfg['further_information_maximum_words'])
    conclusion=next((s for s in sections if s['block']=='conclusion'),None); cwords=len(_words(conclusion['content'])) if conclusion else 0
    cratio=(cwords/total if total else 0.0); cparas=len(re.findall(r'(?is)<p\b[^>]*>',conclusion['content'])) if conclusion else 0
    hard_limits=bool(conclusion and cratio<=float(cfg['conclusion_maximum_ratio']) and cparas<=int(cfg['conclusion_maximum_paragraphs']))
    cmin=bool(conclusion and cratio>=float(typ['conclusion_min_ratio']))
    rows=[('words.hard_total_range',int(cfg['hard_total_words_min'])<=total<=int(cfg['hard_total_words_max']),{'actual':total}),('words.section_range',section_ok,{'counts':counts}),
      ('words.section_balance_ratio',ratio_ok,{'counts':counts}),('words.main_text_minimum_ratio',main_ok,{'actual':main_ratio}),('words.further_information_maximum',further_ok,{'actual':further_words}),
      ('conclusion.hard_limits',hard_limits,{'ratio':cratio,'paragraphs':cparas}),
      ('conclusion.type_minimum_ratio',cmin,{'actual':cratio,'minimum':typ['conclusion_min_ratio']}),('conclusion.minimum_paragraphs',cparas>=2,{'actual':cparas,'minimum':2})]
    return [_receipt(rid,'balance_checker',article,'PASS' if ok else 'FAIL',ev) for rid,ok,ev in rows]

def _table_parts(table):
    headers=[_plain(x) for x in re.findall(r'(?is)<th\b[^>]*>(.*?)</th>',table)]; rows=[]
    for tr in re.findall(r'(?is)<tr\b[^>]*>(.*?)</tr>',table):
        cells=[_plain(x) for x in re.findall(r'(?is)<td\b[^>]*>(.*?)</td>',tr)]
        if cells: rows.append(cells)
    return headers,rows

def table_receipts(article):
    v=load_values(); cfg=v['table']; legacy=v['ppm_parity']['table']; html=article['html']; typ=article['article_type']; tables=re.findall(r'(?is)<table\b[^>]*>.*?</table>',html)
    count=len(tables); policy=cfg['presence_policy'][typ]; presence_ok=(count==1 if policy=='REQUIRED' else count<=1)
    canonical_ok=True; labels_ok=True; cells_ok=True; summary_ok=True; value_ok=True; min_rows_ok=True; structure_ok=True; evidence={}
    exceptions=set(article.get('table_multiword_exceptions') or [])
    if count==1:
        table=tables[0]; om=re.search(r'(?is)<table\b([^>]*)>',table); attrs=_attrs('<table '+(om.group(1) if om else '')+'>'); classes=set(attrs.get('class','').split())
        canonical_ok=set(v['global']['canonical_table_classes']).issubset(classes); headers,rows=_table_parts(table)
        min_rows_ok=len(rows)>=int(legacy['minimum_body_rows']); columns=max([len(r) for r in rows] or [0]); structure_ok=bool(re.search(r'(?is)<thead\b',table) and re.search(r'(?is)<tbody\b',table) and columns>=int(legacy['minimum_columns']))
        for x in headers:
            if len(_words(x))>int(cfg['header_maximum_words']) and x not in exceptions: labels_ok=False
            if re.search(r'[.!?;:]\s*$',x): labels_ok=False
        for row in rows:
            for i,x in enumerate(row):
                limit=int(cfg['first_column_maximum_words'] if i==0 else cfg['other_cells_hard_maximum_words'])
                if len(_words(x))>limit and x not in exceptions:
                    if i==0: labels_ok=False
                    else: cells_ok=False
                if re.search(r'[.!?;:]\s*$',x): cells_ok=False
        table_sec=next((s for s in _sections(html) if s['block']=='table'),None)
        if not table_sec: summary_ok=False
        else:
            tm=re.search(r'(?is)<table\b[^>]*>.*?</table>',table_sec['body']); after=table_sec['body'][tm.end():] if tm else ''
            pars=re.findall(r'(?is)<p\b[^>]*>(.*?)</p>',after); sc=v['global']['post_table_summary']; summary_ok=len(pars)==int(sc['paragraphs_exact'])
            if pars:
                wc=len(_words(pars[0])); ss=len(_sentences(pars[0])); summary_ok=summary_ok and int(sc['words_min'])<=wc<=int(sc['words_max']) and int(sc['sentences_min'])<=ss<=int(sc['sentences_max'])
        semantic=article.get('semantic_rule_results') or {}; value_ok=(semantic.get('table.value_required_if_present')=='PASS'); evidence['table_value_semantic_result']=semantic.get('table.value_required_if_present')
    decision_cfg=cfg['optional_decision']; decision=article.get('table_decision') or {}
    optional_decision_ok=True; decision_evidence={'policy':policy,'count':count,'decision':decision}
    if policy=='OPTIONAL':
        expected_decision=decision_cfg['include_value'] if count==1 else decision_cfg['omit_value']
        optional_decision_ok=(
            decision.get('decision')==expected_decision
            and len(str(decision.get('rationale') or '').strip())>=int(decision_cfg['rationale_minimum_chars'])
        )
        decision_evidence['expected_decision']=expected_decision
    rows_out=[('table.required_for_comparison',presence_ok,{'count':count,'policy':policy}),('table.presence_policy',presence_ok,{'count':count,'policy':policy}),('table.minimum_rows',min_rows_ok,{}),('table.structure',structure_ok,{}),
      ('table.canonical_classes',canonical_ok,{}),('table.compact_labels',labels_ok,{}),('table.compact_cells',cells_ok,{}),('table.post_summary_policy',summary_ok,{}),('table.value_required_if_present',value_ok,evidence),('table.optional_decision_documented',optional_decision_ok,decision_evidence)]
    return [_receipt(rid,'table_checker',article,'PASS' if ok else 'FAIL',ev) for rid,ok,ev in rows_out]

def adapter_receipts(article):
    ok=(article.get('external_results') or {}).get('LanguageTool 6.8')=='PASS'
    return [_receipt('lt68.language_zero_unresolved','lt68_adapter',article,'PASS' if ok else 'FAIL',{'external_result':(article.get('external_results') or {}).get('LanguageTool 6.8')})]

def run_article_checks(article):
    return structural_receipts(article)+fact_receipts(article)+editorial_receipts(article)+balance_receipts(article)+table_receipts(article)+adapter_receipts(article)

run_once=run_article_checks
