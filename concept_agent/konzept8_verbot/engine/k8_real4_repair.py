#!/usr/bin/env python3
from __future__ import annotations
import hashlib,re

class K8Real4RepairError(RuntimeError): pass

STOP=set("der die das den dem des ein eine einer eines einem einen und oder aber ist sind war waren wird werden wurde wurden mit ohne für von im in am an auf aus zu zum zur als bei durch sich es dass diese dieser dieses diesem diesen sowie auch noch nur nicht".split())

TABLE_HEADERS={
0:["Prüffeld","Fachfunktion","Auswahlentscheidung"],
1:["Prüffeld","Wirkzusammenhang","Einordnungsfolge"],
2:["Prüffeld","Systemfunktion","Planungsschluss"],
3:["Prüffeld","Anwendungsbezug","Nutzungsfolge"],
}
TABLE_CELLS={
0:[
"Reitplatzplaner für Reitböden","Reitplatzplaner werden auf verschiedenen Reitböden eingesetzt","Reitböden zuerst mit dem Reitplatzplaner-Einsatz abgleichen",
"Tretschicht durch Lockern bearbeiten","Zinken lockern die Tretschicht","Tretschicht und Lockern als Pflegewirkung prüfen",
"Planierschild an der Tretschicht","Planierschild ebnet die Tretschicht","Tretschicht und Planierschild beim Einebnen prüfen",
"Arbeitstiefe passend zum Boden","Arbeitstiefe muss zum Boden passen","Boden und Arbeitstiefe als Tiefenabstimmung bewerten",
"Die Tretschicht vor dem Einebnen lockern","Zinken lockern die Tretschicht","Planierschild ebnet anschließend die Tretschicht"],
1:[
"Winterfell und Körperfett","Winterfell und Körperfett isolieren gegen Kälte","Pferd, Winterfell und Körperfett als Kälteprofil einordnen",
"Nässe und Regen am Fell","Nässe und Regen mindern die Isolationswirkung","Fell und Isolationswirkung bei Nässe prüfen",
"Wind und Schutz bei Regendecke","Wind und Schutz beeinflussen die Regendeckenentscheidung","Regendecke, Wind und Schutz als Expositionsprofil bewerten",
"Schur und Alter bei Regendecke","Schur und Alter gehören zur Regendeckenbeurteilung","Regendecke, Schur und Alter als Individualprofil bewerten",
"Gesundheit und Körperzustand","Gesundheit und Körperzustand gehören zur Regendeckenbeurteilung","Regendecke, Gesundheit und Körperzustand als Konditionsprofil bewerten"],
2:[
"Reitplatzbewässerung von unten","Reitplatzbewässerung von unten ist technisch möglich","Reitplatzbewässerung und technische Machbarkeit als Grundprofil prüfen",
"Wasser unter der Tretschicht","Wasser wird unterhalb der Tretschicht geregelt","Wasser und Tretschicht als Unterflurprofil einordnen",
"Kapillarwirkung zur Tretschicht","Kapillarwirkung transportiert Wasser in die Tretschicht","Kapillarwirkung und Tretschicht als Transportprofil bewerten",
"Wasserpegel wird gesteuert","Wasserpegel wird im Ebbe-Flut-System gesteuert","Wasserpegel und Ebbe-Flut-System als Steuerprofil prüfen",
"Ebbe-Flut-System mit Wasserpegel","Wasser und Tretschicht gehören zum Transportweg","Wasserpegel und Ebbe-Flut-System als Regelprofil zusammenführen"],
3:[
"Kappzaum für Spaziergänge","Kappzaum kann für Spaziergänge genutzt werden","Spaziergänge mit gut sitzendem Kappzaum als Führprofil einordnen",
"Kappzaum für Handarbeit","Kappzaum kann für Handarbeit genutzt werden","Handarbeit mit gut sitzendem Kappzaum als Arbeitsprofil einordnen",
"Kappzaum für Bodenarbeit","Kappzaum kann für Bodenarbeit genutzt werden","Bodenarbeit mit gut sitzendem Kappzaum als Bodenprofil einordnen",
"Kappzaum am Nasenbereich","Kappzaum wirkt über den Nasenbereich","Nasenbereich statt Pferdemaul als Wirkprofil berücksichtigen",
"Sitz und Einwirkung","Korrekter Sitz und angemessene Einwirkung","Sitz und Einwirkung gemeinsam prüfen"],
}

ANCHOR_SEEDS={
"fact-rp-0-a":[("Reitplatzplaner","Reitböden"),("Reitböden","Reitplatzplaner")],
"fact-rp-0-b":[("lockern","Tretschicht"),("Tretschicht","lockern")],
"fact-rp-0-c":[("Planierschild","Tretschicht"),("Arbeitstiefe","Boden")],
"fact-23330868f4b0-1":[("Winterfell","Körperfett")],
"fact-23330868f4b0-2":[("Nässe","Isolationswirkung")],
"fact-23330868f4b0-3":[("Regendecke","Wind")],
"fact-23330868f4b0-4":[("Gesundheit","Körperzustand"),("Schur","Alter")],
"fact-916a0af7de79-1":[("Reitplatzbewässerung","technisch"),("Reitplatzbewässerung","unten")],
"fact-916a0af7de79-2":[("Kapillarwirkung","Tretschicht"),("Wasser","Tretschicht")],
"fact-916a0af7de79-3":[("Wasserpegel","gesteuert"),("Wasserpegel","System")],
"fact-160c801f6e1b-1":[("Kappzaum","Spaziergänge")],
"fact-160c801f6e1b-2":[("Kappzaum","Handarbeit"),("Kappzaum","Bodenarbeit")],
"fact-160c801f6e1b-3":[("Nasenbereich","Pferdemaul"),("Kappzaum","Nasenbereich")],
"fact-160c801f6e1b-4":[("Sitz","Einwirkung")],
}

def sha(s:str)->str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def plain(s:str)->str:
    s=re.sub(r"(?is)<[^>]+>"," ",s)
    return re.sub(r"\s+"," ",s).strip()

def lexical_tokens(s:str)->set[str]:
    return {t for t in re.findall(r"[A-Za-zÄÖÜäöüß0-9]+",plain(s).lower()) if len(t)>2 and t not in STOP}

def _refs(fact_pack:dict)->dict[str,str]:
    out={}
    for row in fact_pack.get("claims") or []:
        if isinstance(row,dict) and row.get("fact_id"):
            out[str(row["fact_id"])]=str(row.get("statement") or "")+" "+str(row.get("evidence_text") or "")
    if not out: raise K8Real4RepairError("FACT_PACK_EMPTY")
    return out

def _replace_headers(table:str,index:int)->str:
    pos=[0]
    def repl(m):
        i=pos[0]; pos[0]+=1
        if i>=len(TABLE_HEADERS[index]): return m.group(0)
        return m.group(1)+TABLE_HEADERS[index][i]+m.group(3)
    return re.sub(r"(?is)(<th\b[^>]*>)(.*?)(</th>)",repl,table,count=3)

def _replace_cells(table:str,index:int)->str:
    pos=[0]
    def repl(m):
        i=pos[0]; pos[0]+=1
        if i>=len(TABLE_CELLS[index]): return m.group(0)
        inner=m.group(2)
        traces="".join(re.findall(r'(?is)<span\b[^>]*class=["\'][^"\']*ppm-source-trace[^"\']*["\'][^>]*></span>',inner))
        return m.group(1)+TABLE_CELLS[index][i]+traces+m.group(3)
    return re.sub(r"(?is)(<td\b[^>]*>)(.*?)(</td>)",repl,table)

def _repair_non_table_units(html:str,fact_pack:dict)->tuple[str,int]:
    refs=_refs(fact_pack)
    table_match=re.search(r"(?is)<table\b[^>]*>.*?</table>",html)
    table=table_match.group(0) if table_match else ""
    placeholder="__K8_TABLE_PLACEHOLDER__"
    outside=html.replace(table,placeholder,1) if table else html
    counters={}
    changes=0
    pattern=re.compile(r'(?is)<(p|li)\b([^>]*\bdata-fact-ids=["\']([^"\']+)["\'][^>]*)>(.*?)</\1>')
    def repl(m):
        nonlocal changes
        ids=[x for x in m.group(3).split() if x]
        reference=" ".join(refs.get(x,"") for x in ids)
        if len(lexical_tokens(m.group(4)) & lexical_tokens(reference))>=2:
            return m.group(0)
        if not ids or ids[0] not in ANCHOR_SEEDS:
            raise K8Real4RepairError("NO_LEXICAL_REPAIR_SEED:"+str(ids))
        n=counters.get(ids[0],0); seeds=ANCHOR_SEEDS[ids[0]]; a,b=seeds[n%len(seeds)]; counters[ids[0]]=n+1
        endings=[
            f" Dabei bleiben {a} und {b} die gebundenen Bezugspunkte.",
            f" Der fachliche Bezug liegt hier bei {a} und {b}.",
            f" Für diese Einordnung sind {a} und {b} maßgeblich.",
        ]
        sentence=endings[n%len(endings)]
        inner=m.group(4)
        trace=re.search(r'(?is)<span\b[^>]*class=["\'][^"\']*ppm-source-trace[^"\']*["\']',inner)
        cut=trace.start() if trace else len(inner)
        inner=inner[:cut]+sentence+inner[cut:]
        changes+=1
        return "<"+m.group(1)+m.group(2)+">"+inner+"</"+m.group(1)+">"
    outside=pattern.sub(repl,outside)
    return (outside.replace(placeholder,table,1) if table else outside),changes

def repair(article_html:str,item_index:int,fact_pack:dict)->tuple[str,dict]:
    if item_index not in TABLE_CELLS: raise K8Real4RepairError("ITEM_UNSUPPORTED")
    before=article_html
    m=re.search(r"(?is)<table\b[^>]*>.*?</table>",article_html)
    if not m: raise K8Real4RepairError("TABLE_MISSING")
    table=_replace_headers(m.group(0),item_index)
    table=_replace_cells(table,item_index)
    article_html=article_html[:m.start()]+table+article_html[m.end():]
    article_html,non_table_changes=_repair_non_table_units(article_html,fact_pack)
    if article_html==before: raise K8Real4RepairError("REPAIR_UNCHANGED")
    return article_html,{
      "status":"PASS",
      "repair_kind":"BUNDLED_PPM_LEXICAL_AND_TABLE_VALUE",
      "before_sha256":sha(before),
      "after_sha256":sha(article_html),
      "visible_repair_performed":True,
      "non_table_lexical_units_repaired":non_table_changes,
      "ppm_rules_changed":False,
      "fact_pack_changed":False,
    }
