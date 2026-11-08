#!/usr/bin/env python3
"""Offline product-result relevance contract for a future HD009 DataForSEO worker.
No network, prices, images or WP updates.
"""
import re,unicodedata,urllib.parse
def norm(s):
    s=unicodedata.normalize("NFKD",str(s).lower())
    return re.sub(r"\s+"," ",re.sub(r"[^a-z0-9]+"," ",''.join(x for x in s if not unicodedata.combining(x)))).strip()
def concrete_term(phrase):
    t=norm(phrase)
    # Free-text equipment phrases are not automatically trusted as products.
    reject={"karton","holz","papier","material","werkzeug","computer","wasser",
            "schere","farbe","zeit","geduld","platz","modell","schrauben","leitung",
            "leinen","lupe","kleber","ausrüstung","zubehör","ideen","buch"}
    return t if t and t not in reject and len(t)>=8 and len(t.split())<=5 else ""
def products(answer,term,limit=3):
    if not concrete_term(term):return []
    if not isinstance(answer,dict) or answer.get("status_code")!=20000:return []
    task=(answer.get("tasks") or [{}])[0]
    if task.get("status_code")!=20000:return []
    out={}
    for result in task.get("result") or []:
        for item in result.get("items") or []:
            if not isinstance(item,dict) or item.get("type")!="amazon_serp":continue
            title=str(item.get("title") or "").strip()
            url=str(item.get("url") or "")
            host=(urllib.parse.urlparse(url).hostname or "").lower()
            if host not in ("amazon.de","www.amazon.de"):continue
            code=str(item.get("data_asin") or "").upper().strip()
            if not re.fullmatch("[A-Z0-9]{10}",code):continue
            words=set(norm(title).split())
            if not all(x in words for x in norm(term).split()):continue
            if code not in out:out[code]={"asin":code,"title":title[:160]}
            if len(out)==limit:break
        if len(out)==limit:break
    return list(out.values())
def response(*rows):
    return {"status_code":20000,"tasks":[{"status_code":20000,
       "result":[{"items":list(rows)}]}]}
def item(title,code="B012345678",url="https://www.amazon.de/dp/B012345678",kind="amazon_serp"):
    return {"type":kind,"data_asin":code,"title":title,"url":url,
            "image_url":"https://example.com/unauthorised-image.jpg","price_from":29.5,
            "availability":"in_stock"}
def test():
    cases=0
    def expect(testcase,yes,quantity):
        nonlocal cases
        got=products(*testcase)
        assert len(got)==quantity,(got,quantity)
        # Explicitly never capture unchecked Amazon image, price, availability.
        for p in got:assert set(p)=={"asin","title"},p
        cases+=1
    good=response(item("HQ Symphony Lenkdrachen für Einsteiger"),
                  item("Lenkdrachen für Kinder",code="B012345679"),
                  item("Drachen Luftballon",code="B012345680"))
    expect((good,"Lenkdrachen"),True,2)
    expect((good,"Karton"),False,0)
    expect((response(item("Lenkdrachen",url="https://www.ebay.de/itm/123")),"Lenkdrachen"),False,0)
    expect((response(item("Lenkdrachen",code="BAD")),"Lenkdrachen"),False,0)
    expect((response(item("Drachen-Maske Karneval")),"Lenkdrachen"),False,0)
    expect((response(item("Lenkdrachen",kind="amazon_paid")),"Lenkdrachen"),False,0)
    expect((response(item("Lenkdrachen"),item("Lenkdrachen")),"Lenkdrachen"),True,1)
    expect((response(item("3D Drucker für Filament")),"3D-Drucker"),True,1)
    expect(({"status_code":20000,"tasks":[{"status_code":40000,"result":[]}]},"Lenkdrachen"),False,0)
    expect(({"status_code":40300,"tasks":[{"status_code":20000,"result":[]}]},"Lenkdrachen"),False,0)
    assert concrete_term("Karton")=="" and concrete_term("freie Fläche")!=""
    print("PRODUCT_RELEVANCE_GUARDS_PASS",cases,"test cases")
    print("NO_UNLICENSED_IMAGES_OR_PRICES_PERSISTED_PASS")
if __name__=="__main__":test()
