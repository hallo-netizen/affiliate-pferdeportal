import hashlib, html, json, re, time, urllib.request

base='https://pferde-atelier.de/ausruestung/ausruestung-sattel/schabracken/'
modes=[
    ('normal',base,{}),
    ('repeat',base,{}),
    ('cachebuster',base+'?ppar_probe_20261005=1',{}),
    ('nocache',base+'?ppar_probe_20261005=2',{'Cache-Control':'no-cache','Pragma':'no-cache'}),
]
for name,url,headers in modes:
    req=urllib.request.Request(url,headers={'User-Agent':'PferdeAtelier-Readonly-Probe/1.0',**headers})
    with urllib.request.urlopen(req,timeout=30) as r:
        raw=r.read().decode('utf-8','replace')
        hs=dict(r.headers.items())
        print('===== MODE',name,'STATUS',r.status,'BYTES',len(raw),'SHA',hashlib.sha256(raw.encode()).hexdigest(),'=====')
        for k,v in hs.items():
            if k.lower() in {'date','age','cache-control','x-cache','x-litespeed-cache','x-litespeed-tag','server','vary','cf-cache-status','etag','last-modified'}:
                print('HEADER',k,':',v)
        versions=sorted(set(re.findall(r'affiliate-portal-router/[^"\\\' >]+[?&]ver=([0-9.]+)',raw,re.I)))
        print('PLUGIN_ASSET_VERSIONS',versions)
        body=re.search(r'<body[^>]+class=["\\\']([^"\\\']+)["\\\']',raw,re.I)
        print('BODY_CLASS',body.group(1) if body else '')
        pats=[
            r'<a[^>]+class=["\\\'][^"\\\']*ppar-overview-wide-banner-link[^"\\\']*["\\\'][^>]*>.*?</a>',
            r'<a[^>]+class=["\\\'][^"\\\']*ppar-category-large-banner-link[^"\\\']*["\\\'][^>]*>.*?</a>',
        ]
        hits=[]
        for p in pats:
            hits.extend(re.findall(p,raw,re.I|re.S))
        print('BANNER_HIT_COUNT',len(hits))
        for i,h in enumerate(hits,1):
            h=re.sub(r'\\s+',' ',html.unescape(h))
            href=re.search(r'href=["\\\']([^"\\\']+)',h,re.I)
            src=re.search(r'<img[^>]+src=["\\\']([^"\\\']+)',h,re.I)
            alt=re.search(r'<img[^>]+alt=["\\\']([^"\\\']*)',h,re.I)
            print('BANNER',i,'HREF',href.group(1) if href else '','SRC',src.group(1) if src else '','ALT',alt.group(1) if alt else '')
            print('BANNER_HTML',h[:5000])
        for marker in ['SanoVet','sanovet','Gesunde Pferde','Schabracken Designer','ppar-overview-wide-banner-link','product_after_category_tiles']:
            print('MARKER',marker,raw.lower().find(marker.lower()))
    time.sleep(1)

api='https://pferde-atelier.de/wp-json/wp/v2/pages?slug=schabracken&_fields=id,parent,slug,link,status,title'
with urllib.request.urlopen(api,timeout=30) as r:
    rows=json.load(r)
print('REST_SCHABRACKEN',json.dumps(rows,ensure_ascii=False))
if rows:
    parent=int(rows[0].get('parent') or 0)
    depth=0
    while parent and depth<10:
        with urllib.request.urlopen(f'https://pferde-atelier.de/wp-json/wp/v2/pages/{parent}?_fields=id,parent,slug,link,status,title',timeout=30) as r:
            p=json.load(r)
        print('REST_PARENT',json.dumps(p,ensure_ascii=False))
        parent=int(p.get('parent') or 0)
        depth+=1
