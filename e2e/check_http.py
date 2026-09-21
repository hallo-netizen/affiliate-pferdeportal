#!/usr/bin/env python3
import hashlib, html, json, re, sys, urllib.request
scenario=sys.argv[1]
if scenario!='healthy':
    try:
        marker=open('/tmp/aff-history-stop','r',encoding='utf-8').read().strip()
    except FileNotFoundError:
        marker=''
    if marker:
        print(f'SCENARIO_SKIPPED_AFTER_FIRST_HISTORY_BREAK={scenario}:{marker}')
        raise SystemExit(0)
targets={
  'reithelme':186,'reithandschuhe':187,'reitstiefel':188,'sicherheitswesten':189,
  'gerten':190,'sporen':191,'halfter-und-stricke-stallhalfter':174,
}
results={}
for slug,pid in targets.items():
    url=f'http://127.0.0.1:8080/?page_id={pid}&e2e={scenario}-{pid}'
    req=urllib.request.Request(url,headers={'Cache-Control':'no-store','User-Agent':'affiliate-e2e'})
    body=urllib.request.urlopen(req,timeout=30).read().decode('utf-8','replace')
    slots=[]
    for i in (1,2,3):
        m=re.search(fr'<!--E2E_SLOT_{i}_START-->(.*?)<!--E2E_SLOT_{i}_END-->',body,re.S)
        segment=m.group(1) if m else ''
        provider='none'
        low=segment.lower()
        if 'ebay.de' in low or 'rover.ebay' in low: provider='ebay'
        elif 'idealo.de' in low or 'ipn.idealo' in low: provider='idealo'
        tm=re.search(r'<strong class="ppar-banner-title">([^<]+)</strong>',segment,re.S)
        title=html.unescape(tm.group(1).strip()) if tm else ''
        slots.append({
            'slot':i,
            'real':'data-ppar-category-product-card="1"' in segment,
            'provider':provider,
            'title':title,
            'html_sha256':hashlib.sha256(segment.encode()).hexdigest(),
        })
    results[slug]=slots
print('SCENARIO='+scenario)
for slug,slots in results.items():
    print(slug+'='+json.dumps(slots,ensure_ascii=False,separators=(',',':')))
fail=[]
if scenario=='healthy':
    for slug,slots in results.items():
        if sum(x['real'] for x in slots)!=3: fail.append(f'HEALTHY_CARD_COUNT:{slug}')
    p={x['provider'] for x in results['reithelme']}
    if not {'ebay','idealo'} <= p: fail.append('HEALTHY_REITHELME_PROVIDER_MIX')
elif scenario=='ebay_control_open':
    for slug,slots in results.items():
        if sum(x['real'] for x in slots)!=3: fail.append(f'CONTROL_OPEN_CARD_COUNT:{slug}')
    p={x['provider'] for x in results['reithelme']}
    if 'ebay' not in p: fail.append('CONTROL_OPEN_EBAY_STILL_ABSENT')
elif scenario=='idealo_only':
    for slug,slots in results.items():
        if any(x['provider']=='ebay' for x in slots): fail.append(f'IDEALO_ONLY_EBAY_VISIBLE:{slug}')
elif scenario=='one_exact_stallhalfter':
    if sum(x['real'] for x in results['halfter-und-stricke-stallhalfter'])!=1: fail.append('STALLHALFTER_NOT_EXACTLY_ONE')
elif scenario=='live_damage':
    if any(x['provider']=='ebay' for x in results['reithelme']): fail.append('LIVE_DAMAGE_EBAY_VISIBLE')
    if sum(x['real'] for x in results['halfter-und-stricke-stallhalfter'])!=1: fail.append('LIVE_DAMAGE_STALLHALFTER_NOT_ONE')
if fail:
    for x in fail: print('FAIL_'+x,file=sys.stderr)
    raise SystemExit(1)
