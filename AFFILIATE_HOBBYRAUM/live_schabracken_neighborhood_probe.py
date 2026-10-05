import json,re,urllib.request,time,html

UA={'User-Agent':'PferdeAtelier-Readonly-Neighborhood/1.0'}
def get_json(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=30) as r:
        return json.load(r)
def get_html(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=30) as r:
        return r.read().decode('utf-8','replace')

def banner(raw):
    pats=[
      r'<a[^>]+class=["\\\'][^"\\\']*ppar-overview-wide-banner-link[^"\\\']*["\\\'][^>]*>.*?</a>',
      r'<a[^>]+class=["\\\'][^"\\\']*ppar-category-large-banner-link[^"\\\']*["\\\'][^>]*>.*?</a>'
    ]
    for p in pats:
        m=re.search(p,raw,re.I|re.S)
        if not m: continue
        h=re.sub(r'\\s+',' ',html.unescape(m.group(0)))
        href=re.search(r'href=["\\\']([^"\\\']+)',h,re.I)
        src=re.search(r'<img[^>]+src=["\\\']([^"\\\']+)',h,re.I)
        return {'href':href.group(1) if href else '', 'src':src.group(1) if src else '', 'html':h[:1200]}
    return {'href':'','src':'','html':''}

parents=[95,108]
rows=[]
seen=set()
for parent in parents:
    pages=get_json(f'https://pferde-atelier.de/wp-json/wp/v2/pages?parent={parent}&per_page=100&_fields=id,parent,slug,link,status,title')
    for p in pages:
        if p['id'] in seen: continue
        seen.add(p['id']); rows.append(p)
# include children of every discovered page, bounded
for p in list(rows):
    children=get_json(f'https://pferde-atelier.de/wp-json/wp/v2/pages?parent={p["id"]}&per_page=100&_fields=id,parent,slug,link,status,title')
    for q in children:
        if q['id'] not in seen:
            seen.add(q['id']); rows.append(q)

print('PAGE_COUNT',len(rows))
for p in sorted(rows,key=lambda x:(x['parent'],x['id'])):
    raw=get_html(p['link']+'?ppar_neighborhood_probe=1')
    b=banner(raw)
    print(json.dumps({
      'id':p['id'],'parent':p['parent'],'slug':p['slug'],'title':p['title'].get('rendered',''),
      'link':p['link'],'banner_href':b['href'],'banner_src':b['src']
    },ensure_ascii=False))
    time.sleep(0.2)
