#!/usr/bin/env python3
import urllib.request,re,html
from html.parser import HTMLParser
u="https://hobby-depot.de/gestalten/malen-zeichnen/"
print("URL",u)
try:
    req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0 (compatible; HD009-Banner-QA/1.0)"})
    with urllib.request.urlopen(req,timeout=25) as r:
        content=r.read().decode("utf-8","replace")
        print("HTTP",r.status,"SIZE",len(content))
    for term in ["hdar-ci-amazon-slot","hdar-ci-amazon-banner","hdar-ci-label","ANZEIGE","ppar-overview-banner","banner-slot"]:
        matches=list(re.finditer(re.escape(term),content,re.IGNORECASE))
        print("TERM",term,"COUNT",len(matches))
        for m in matches[:2]:
            print("NEIGHBOR",content[max(0,m.start()-1000):m.end()+900].replace("\n"," ")[:2100])
except Exception as e:
    print("PUBLIC_HTTP_ERROR",type(e).__name__,str(e))

for rule in ["hd-next-partner-banner{","hd-next-partner-banner>div{","hd-next-partner-banner > div{","hd-next-partner-banner .ppar-affiliate-slot","hd-banner-span-3{"]:
    for m in list(re.finditer(re.escape(rule),content,re.IGNORECASE))[:4]:
        print("CSS_RULE",rule,content[max(0,m.start()-80):m.start()+720].replace("\n"," ")[:800])
