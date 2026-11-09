#!/usr/bin/env python3
"""Read-only public WordPress/Yoast SEO audit for Hobby Depot, 2026-11-09."""
import re, json, zipfile, collections, pathlib, concurrent.futures, xml.etree.ElementTree as ET, time
from urllib.parse import urljoin,urlparse,parse_qs
import requests
from bs4 import BeautifulSoup

OUT=pathlib.Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/SEO/EVIDENCE')
OUT.mkdir(parents=True, exist_ok=True)
ROOT='https://www.hobby-depot.de'
S=requests.Session()
S.headers.update({'User-Agent':'Mozilla/5.0 (compatible; HobbyDepotSEO-Audit/1.0; public read-only)'})
def get(url,timeout=18):
    try:
        r=S.get(url,timeout=timeout,allow_redirects=True)
        return {'status':r.status_code,'final':r.url,'body':r.text,'ctype':r.headers.get('content-type','')}
    except Exception as e:
        return {'status':None,'final':url,'error':f'{type(e).__name__}: {e}','body':'','ctype':''}

def meta(html):
    soup=BeautifulSoup(html[:2000000],'html.parser')
    title=soup.title.get_text(' ',strip=True) if soup.title else ''
    def sel(k,v):
        tag=soup.find('meta',attrs={k:v})
        return tag.get('content','') if tag else ''
    links=soup.find_all('link',rel=True)
    canonical=next((t.get('href','') for t in links if 'canonical' in t.get('rel',[])),'')
    body=soup.body
    return {
        'title':title,'description':sel('name','description'),'robots':sel('name','robots'),
        'canonical':canonical,'og_title':sel('property','og:title'),
        'og_description':sel('property','og:description'),
        'has_yoast':('Yoast SEO' in html or 'yoast-seo' in html.lower()),
        'body_class':body.get('class',[]) if body else [],'h1':next((x.get_text(' ',strip=True)[:200] for x in soup.find_all('h1')), ''),
        'internal_links':sorted(set(urljoin(ROOT,a.get('href')) for a in soup.find_all('a',href=True)
            if urlparse(urljoin(ROOT,a.get('href'))).netloc in ('hobby-depot.de','www.hobby-depot.de')))[:500]
    }

result={'run_date':'2026-11-09','root':ROOT,'public_only':True,
        'home':{},'sitemaps':{},'rest':{},'source':{},'sampled_pages':{},
        'findings':{},'errors':[]}
for host in ['https://hobby-depot.de/','https://www.hobby-depot.de/']:
    r=get(host)
    v={'status':r['status'],'final':r['final'],'error':r.get('error','')}
    if r['status']==200:
        v.update(meta(r['body']))
        if r['final'].startswith('https://'):ROOT=urljoin(r['final'],'/')
    result['home'][host]=v
    print('HOME',host,v['status'],v['final'],'title',v.get('title'),'description',v.get('description'),'canonical',v.get('canonical'), 'robots',v.get('robots'))

zp=pathlib.Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip')
with zipfile.ZipFile(zp) as z:
    for fname in z.namelist():
        if not fname.endswith('.php') or z.getinfo(fname).file_size>4000000:continue
        txt=z.read(fname).decode('utf-8','replace')
        if 'hobbyfinder' not in txt.lower() and 'yoast' not in txt.lower() and 'seo' not in txt.lower():continue
        lines=txt.splitlines()
        matches=[{'line':i+1,'text':line[:600]} for i,line in enumerate(lines)
                 if re.search(r'hobbyfinder|wpseo_|yoast|pre_get_document_title|is_front_page|is_home\(|add_rewrite_rule|add_shortcode|template_redirect|wp_head|register_post_type|register_taxonomy',line,re.I)]
        result['source'][fname]={'matches':matches[:120],'total_matches':len(matches)}
        print('PLUGIN_FILE',fname,'hobbyfinder_or_seo_matches',len(matches))
        for item in matches[:25]:print('PLUGIN_LINE',item['line'],item['text'][:300])
# sitemap top
candidates=[ROOT+'sitemap_index.xml',ROOT+'wp-sitemap.xml']
allmap={}
for url in candidates:
    r=get(url)
    d={'status':r['status'],'final':r['final'],'error':r.get('error',''),'raw_excerpt':r['body'][:1000]}
    if r['status']==200 and 'xml' in r['body'][:2000].lower():
        try:
            e=ET.fromstring(r['body'])
            locs=[n.text for n in e.iter() if n.tag.endswith('}loc') or n.tag=='loc']
            d['entry_count']=len(locs);d['entries']=locs[:500]
            if 'sitemapindex' in e.tag.lower():allmap.update({x:[] for x in locs if x and 'hobby-depot.de' in x})
            else:d['urls']=locs[:5000]
        except Exception as ex:d['parse_error']=str(ex)
    result['sitemaps'][url]=d
    print('SITEMAP_INDEX',url,r['status'],'entries',d.get('entry_count'),'error',d.get('error'))
for url in list(allmap)[:120]:
    r=get(url)
    d={'status':r['status'],'error':r.get('error',''),'url_count':0,'urls':[]}
    if r['status']==200:
        try:
            e=ET.fromstring(r['body'])
            links=[n.text for n in e.iter() if n.tag.endswith('}loc') or n.tag=='loc']
            d['url_count']=len(links);d['urls']=links
        except Exception as ex:d['error']=str(ex)
    allmap[url]=d
    print('SUBSITEMAP',url,r['status'],'urls',d['url_count'],'error',d['error'][:150])
result['sitemaps']['submaps']=allmap
indexed=set(url.rstrip('/')+'/' for sm in allmap.values() for url in sm['urls'] if url)
def rjson(url):
    r=get(url)
    try:j=json.loads(r['body']) if r['status']==200 else None
    except Exception:j=None
    return (r['status'],j,r.get('error',''),r['body'][:300] if not j else '')
# WordPress REST
status,wp,error,raw=rjson(ROOT+'wp-json/')
result['rest']['root']={'status':status,'error':error,'name':wp.get('name') if isinstance(wp,dict) else None,
                       'namespaces':wp.get('namespaces',[]) if isinstance(wp,dict) else [],
                       'raw':raw}
print('WP_REST_ROOT',status,result['rest']['root'].get('name'),'namespace',len(result['rest']['root'].get('namespaces',[])))
endpoints={'pages':'pages','posts':'posts','categories':'categories'}
for name,endpoint in endpoints.items():
    entries=[];seen=set();messages=[]
    for page in range(1,151):
        url=ROOT+f'wp-json/wp/v2/{endpoint}?per_page=100&page={page}&_fields=id,link,status,slug,type,parent,yoast_head_json'
        status,j,err,raw=rjson(url)
        if status!=200 or not isinstance(j,list):
            messages.append({'page':page,'http':status,'error':err,'response':raw[:200]})
            break
        if not j:break
        for it in j:
            link=it.get('link','')
            if link in seen:continue
            seen.add(link)
            seo=it.get('yoast_head_json') or {}
            entries.append({'id':it.get('id'),'link':link,'status':it.get('status'),
                'type':it.get('type'),'slug':it.get('slug'),'parent':it.get('parent'),
                'robots':seo.get('robots',''),'canonical':seo.get('canonical',''),
                'title':seo.get('title',''),'description':seo.get('description',''),
                'in_xml':link.rstrip('/')+'/' in indexed})
        if len(j)<100:break
    result['rest'][name]={'count':len(entries),'error':messages,'entries':entries}
    missing=[e for e in entries if not e['in_xml']]
    print('WP_REST',name,'count',len(entries),'missing_from_Yoast_sitemap',len(missing),
          'status_error',messages[:1],'sample',[(x['id'],x['link'],x['robots']) for x in missing[:12]])

# Check representative public dynamic routes, especially the Hobbyfinder.
interesting=[
 '/', '/hobbyfinder/','/magazin/hobbyfinder/','/hobby-register/','/hobbyregister/',
 '/magazin/','/glossar/','/hobbys/','/kontakt/','/anzeigen/','/hobbyfinder',
 '/magazin/hobby-finder/','/hobby-finder/','/magazin/hobbyregister/',
]
for entry in result['rest'].get('pages',{}).get('entries',[]):
    if any(x in (entry.get('slug') or '') for x in ['hobby','magazin','glossar','kontakt','startseite','finder','register','anzeigen']):
        interesting.append(entry['link'])
for x in result['home'].values():
    for link in x.get('internal_links',[]):
        if any(word in link.lower() for word in ['hobbyfinder','hobby-register','hobbyregister','magazin','glossar','kontakt','anzeigen']):
            interesting.append(link)
for name,entry in list(allmap.items())[:12]:
    interesting+=entry['urls'][:3]
unique=list(dict.fromkeys(urljoin(ROOT,x) if x.startswith('/') else x for x in interesting))
for url in unique[:95]:
    r=get(url)
    summary={'status':r['status'],'final':r['final'],'error':r.get('error','')}
    if r['status']==200:
        summary.update({k:v for k,v in meta(r['body']).items() if k!='internal_links'})
    result['sampled_pages'][url]=summary
    print('SAMPLED',url,r['status'],r['final'],'title',summary.get('title'),'desc',str(summary.get('description',''))[:120], 'robots',summary.get('robots'),'canonical',summary.get('canonical'))
# sample public REST pages that Yoast omitted
for group in ['pages','posts','categories']:
    missing=[x for x in result['rest'].get(group,{}).get('entries',[]) if not x['in_xml']]
    for p in missing[:min(25,len(missing))]:
        url=p['link']
        if url in result['sampled_pages']:continue
        r=get(url)
        sm={'status':r['status'],'final':r['final'],'error':r.get('error','')}
        if r['status']==200:sm.update({k:v for k,v in meta(r['body']).items() if k!='internal_links'})
        result['sampled_pages'][url]=sm
        print('MISSING_SAMPLE',group,url,'status',r['status'],'title',sm.get('title'),'robots',sm.get('robots'),'canonical',sm.get('canonical'))
# Summarise
result['findings']={'total_yoast_urls':len(indexed),
     'sitemap_types':{k:v['url_count'] for k,v in allmap.items()},
     'rest_missing_count':{k:sum(not e['in_xml'] for e in v.get('entries',[]))
                    for k,v in result['rest'].items() if isinstance(v,dict) and 'entries' in v},
     'rest_total_count':{k:v.get('count',0) for k,v in result['rest'].items() if isinstance(v,dict) and 'entries' in v},
     'sampled_total':len(result['sampled_pages']),
     'sampled_404':[u for u,x in result['sampled_pages'].items() if x['status']==404],
     'sampled_no_description':[u for u,x in result['sampled_pages'].items() if x['status']==200 and not x.get('description')],
     'sampled_no_canonical':[u for u,x in result['sampled_pages'].items() if x['status']==200 and not x.get('canonical')],
     'sampled_noindex':[u for u,x in result['sampled_pages'].items() if 'noindex' in str(x.get('robots',''))],
}
report=OUT/'HOBBYDEPOT_YOAST_LIVE_AUDIT_20261109.json'
report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('REPORT',report,'BYTES',report.stat().st_size)
print('SUMMARY',json.dumps(result['findings'],ensure_ascii=False)[:10000])
