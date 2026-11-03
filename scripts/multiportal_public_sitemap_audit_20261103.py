#!/usr/bin/env python3
"""Read-only public SEO inventory: WordPress sitemap sets vs real navigable HTML on 3 sites."""
import concurrent.futures
import collections
import html.parser
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

SITES = {
 "HOBBY DEPOT": "https://www.hobby-depot.de",
 "HAB & BEWAHR": "https://hab-und-bewahr.de",
 "PFERDEATELIER": "https://pferde-atelier.de",
}
BLOCKED = ("/wp-admin", "/wp-login", "/wp-json", "/wp-content", "/wp-includes", "/xmlrpc", "/feed", "/author/", "/account/", "/my-account", "/kasse", "/warenkorb", "/cart", "/checkout")
EXCLUDED_SUFFIX = (".jpg", ".jpeg", ".png", ".webp", ".svg", ".gif", ".avif", ".css", ".js", ".ico", ".pdf", ".mp4", ".woff", ".txt", ".zip", ".xml")
if os.environ.get("AUDIT_SITE"):
    SITES = {os.environ["AUDIT_SITE"]: SITES[os.environ["AUDIT_SITE"]]}
MAX_LINK_PAGES = int(os.environ.get("AUDIT_NAV","110"))
MAX_SEED_PAGES = int(os.environ.get("AUDIT_SEED","140"))
MAX_VALIDATE = int(os.environ.get("AUDIT_VERIFY","400"))
MAX_HTML_BYTES = 1100000
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; SitemapEvidenceAudit/1.0; +https://www.hobby-depot.de)", "Accept": "text/html,application/xml,text/xml;q=0.9,*/*;q=0.8"}

def fetch(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as response:
            return {"code": response.status, "url": response.url, "headers": dict(response.headers), "data": response.read(MAX_HTML_BYTES)}
    except urllib.error.HTTPError as e:
        return {"code": e.code, "url": url, "headers": dict(e.headers), "data": e.read(1000)}
    except Exception as e:
        return {"code": 0, "url": url, "headers": {}, "data": (type(e).__name__ + ": " + str(e)).encode()}

def loc(url, base):
    try:
        p = urllib.parse.urlsplit(urllib.parse.urljoin(base, url))
        b = urllib.parse.urlsplit(base)
        if p.scheme not in ("http", "https"): return None
        if p.netloc.lower().removeprefix("www.") != b.netloc.lower().removeprefix("www."): return None
        path = p.path or "/"
        if any(path.lower().startswith(x) for x in BLOCKED): return None
        if any(path.lower().endswith(x) for x in EXCLUDED_SUFFIX): return None
        if re.search(r"/page/[0-9]+/?$", path): return None
        if path != "/" and not path.endswith("/"): path += "/"
        return path
    except (ValueError, TypeError): return None

class Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hrefs = set()
        self.robots = []
        self.canonical = []
        self.title = ""
        self.in_title = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and attrs.get("href"): self.hrefs.add(attrs["href"])
        if tag == "meta" and attrs.get("name","").lower() in ("robots","googlebot"):
            self.robots.append(attrs.get("content", ""))
        if tag == "link" and "canonical" in attrs.get("rel", "").lower():
            self.canonical.append(attrs.get("href",""))
        if tag == "title": self.in_title = True
    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
    def handle_data(self, data):
        if self.in_title: self.title += data

def page_fetch(path, root):
    res = fetch(root + path)
    html = None
    if res["code"] == 200 and ("html" in res["headers"].get("Content-Type","").lower() or res["data"][:50].lower().find(b"<html") >= 0):
        html = Page()
        try: html.feed(res["data"].decode("utf-8", "replace"))
        except Exception: pass
    x = {k:v for k,v in res.items() if k != "data"}
    x["robots"] = [] if html is None else html.robots
    x["canonicals"] = [] if html is None else html.canonical
    x["title"] = "" if html is None else html.title.strip()[:95]
    x["links"] = [] if html is None else sorted({p for link in html.hrefs if (p := loc(link,root))})
    return path, x

def robots_disallow(res):
    return [l.strip() for l in res["data"].decode("utf-8","replace").splitlines() if re.match(r"^(User-agent|Disallow|Sitemap):", l, re.I)][:40]

def tag_text(tag): return tag.rsplit("}",1)[-1]

def gather_sitemap(root):
    top = root + "/sitemap_index.xml"
    todo = collections.deque([top])
    checked = set()
    smap = collections.defaultdict(set)
    failures = []
    urls = set()
    while todo and len(checked) < 50:
        u = todo.popleft()
        if u in checked: continue
        checked.add(u)
        r = fetch(u)
        if r["code"] != 200:
            failures.append((u,r["code"],r["data"][:80].decode("utf8","replace")))
            continue
        try: tree = ET.fromstring(r["data"])
        except Exception as e:
            failures.append((u,"INVALID_XML",str(e)))
            continue
        tags = [e.text.strip() for e in tree.iter() if tag_text(e.tag) == "loc" and e.text]
        if tag_text(tree.tag) == "sitemapindex":
            for v in tags: todo.append(v)
        elif tag_text(tree.tag) == "urlset":
            for v in tags:
                p=loc(v,root)
                if p:
                    urls.add(p)
                    smap[urllib.parse.urlsplit(u).path].add(p)
    return urls,smap,failures,sorted(checked)

def good_candidate(p,x,root):
    if x["code"] != 200: return False,"HTTP_"+str(x["code"])
    if not x["links"] and not x["robots"] and not x["canonicals"]: return False,"NON_HTML"
    if "noindex" in " ".join(x["robots"]).lower(): return False,"NOINDEX_META"
    hdr = " ".join(v for k,v in x["headers"].items() if k.lower()=="x-robots-tag").lower()
    if "noindex" in hdr: return False,"NOINDEX_HEADER"
    if x["canonicals"]:
        cp = loc(x["canonicals"][0],root)
        if cp != p: return False,"CANONICAL_OTHER:" + str(cp)
    return True,"INDEXABLE"

def kind(p):
    if p.startswith("/hobbyregister/"): return "hobbyregister"
    if p.startswith("/glossar/"): return "glossar"
    if p.startswith("/pferderassen/"): return "pferderassen"
    if p.startswith("/anzeigenmarkt/") or p.startswith("/listing/"): return "anzeigenmarkt"
    if p.startswith("/journal/"): return "journal"
    if p.startswith("/category/"): return "category"
    if p == "/": return "homepage"
    return "path-depth-"+str(len([x for x in p.split("/") if x]))

def audit(name,root):
    print("\n===== START",name,root,"=====", flush=True)
    start=time.monotonic()
    robots=fetch(root+"/robots.txt")
    all_urls, maps, failures, xmlfiles=gather_sitemap(root)
    print("SITEMAP_TOTAL_URLS",len(all_urls),"SITEMAP_FILES",len(maps),"XML_ATTEMPTS",len(xmlfiles),"FAILS",failures,flush=True)
    for source, urls in sorted(maps.items()):
        print("SITEMAP_FILE",source,"COUNT",len(urls),flush=True)
    print("ROBOTS_TXT_HTTP",robots["code"],"RULES",robots_disallow(robots),flush=True)
    # First crawl linked navigation, BFS across page levels.
    fetched = {}
    links = collections.defaultdict(set)
    frontier=collections.deque(["/"])
    to_process={"/"}
    visited=set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        while frontier and len(visited)<MAX_LINK_PAGES:
            batch=[]
            while frontier and len(batch)<12 and len(visited)+len(batch)<MAX_LINK_PAGES:
                u=frontier.popleft()
                if u not in visited:
                    batch.append(u);visited.add(u)
            if not batch: continue
            for p,x in pool.map(lambda p:page_fetch(p,root),batch):
                fetched[p]=x
                for linked in x["links"]:
                    links[linked].add(p)
                    if linked not in to_process and len(to_process)<MAX_LINK_PAGES*8:
                        frontier.append(linked);to_process.add(linked)
        print("NAV_HTML_CHECKED",len(visited),"NAV_LINK_URLS",len(links),flush=True)
        # Then sample sitemap-driven pages deliberately by group, especially deeper category levels.
        rest = list(all_urls-set(fetched))
        rest.sort(key=lambda p:(0 if kind(p) != "hobbyregister" else 1, len(p.split("/")),p))
        # Spread across site by category/depth using a deterministic stride.
        seed=rest[:MAX_SEED_PAGES]
        for i in range(0,len(seed),20):
            for p,x in pool.map(lambda p:page_fetch(p,root),seed[i:i+20]):
                fetched[p]=x
                for linked in x["links"]: links[linked].add(p)
        print("SITEMAP_SEED_CHECKED",len(seed),"DISCOVERED_LINK_URLS",len(links),flush=True)
        # Check any discovered linked pages missing from all sitemaps.
        missing_paths=sorted((set(links)|{"/"})-all_urls)
        missing_paths=[p for p in missing_paths if p not in ("/wp-sitemap/", "/sitemap_index/")]
        if len(missing_paths)>MAX_VALIDATE: print("NOTE:MISSING_CANDIDATES_TRUNCATED",len(missing_paths),MAX_VALIDATE)
        missing_paths=missing_paths[:MAX_VALIDATE]
        for i in range(0,len(missing_paths),20):
            candidates = [p for p in missing_paths[i:i+20] if p not in fetched]
            for p,x in pool.map(lambda p:page_fetch(p,root),candidates):
                fetched[p]=x
        present=[]
        excluded=collections.defaultdict(list)
        for p in missing_paths:
            if p not in fetched: continue
            ok,reason=good_candidate(p,fetched[p],root)
            if ok: present.append(p)
            else: excluded[reason].append(p)
        print("INDEXABLE_MISSING_FROM_SITEMAP",len(present),flush=True)
        for p in sorted(present,key=lambda p:(kind(p),p))[:85]:
            print("MISSING_INDEXABLE",kind(p),p,"TITLE",fetched[p]["title"],"LINKED_FROM",sorted(links.get(p,[]))[:2],flush=True)
        for reason, pages in sorted(excluded.items(),key=lambda q:-len(q[1])):
            print("MISSING_BUT_EXCLUDED",reason,"COUNT",len(pages),"EXAMPLES",pages[:8],flush=True)
        sitemap_health=collections.defaultdict(list)
        for p in sorted(all_urls & set(fetched)):
            ok,reason=good_candidate(p,fetched[p],root)
            if not ok: sitemap_health[reason].append(p)
        for reason,pages in sorted(sitemap_health.items(),key=lambda q:-len(q[1])):
            print("IN_SITEMAP_BUT_ISSUE",reason,"COUNT_IN_SAMPLED",len(pages),"EXAMPLES",pages[:12],flush=True)
        print("LIVE_EXPECTED_NO_INDEX_TEST",[(p,[(k,fetched[p].get(k)) for k in ("code","robots","canonicals")] if p in fetched else "not sampled") for p in ["/hobbyregister/alabasterschnitzen/","/hobbyregister/3d-druck/"] if name=="HOBBY DEPOT"],flush=True)
    result={
        "site":name,"root":root, "sitemap_total":len(all_urls),
        "sitemap_file_counts":{k:len(v) for k,v in maps.items()},
        "sitemap_failures":failures,
        "sitemap_urls":sorted(all_urls),
        "robots_rules":robots_disallow(robots),
        "nav_pages_checked":len(visited),
        "sitemap_pages_sampled":len(seed),
        "linked_pages_discovered":len(links),
        "missing_candidates_tested":len(missing_paths),
        "indexable_missing": [{"path":p,"category":kind(p),"title":fetched[p]["title"],"linked_from":sorted(links.get(p,[]))[:3]} for p in present],
        "missing_excluded":{k:v for k,v in excluded.items()},
        "sitemap_sample_issues":{k:v for k,v in sitemap_health.items()},
        "duration_s":int(time.monotonic()-start)
    }
    print("AUDIT_FINISHED",name,"DURATION",result["duration_s"],"sec",flush=True)
    return result

if __name__ == "__main__":
    results=[]
    for name,root in SITES.items():
        try: results.append(audit(name,root))
        except Exception as e:
            import traceback
            print("AUDIT_ERROR",name,traceback.format_exc(),flush=True)
            results.append({"site":name,"error":str(e)})
    Path("multiportal-seo-audit-20261103.json").write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding="utf8")
    print("\nFINAL_SUMMARY",[(x.get("site"),x.get("sitemap_total"),len(x.get("indexable_missing",[])),x.get("error","")) for x in results],flush=True)
