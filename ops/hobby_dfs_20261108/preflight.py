#!/usr/bin/env python3
"""Read-only comparison of current structured hobby input with the existing product slots."""
from pathlib import Path
from zipfile import ZipFile
from collections import Counter,defaultdict
import json,unicodedata,re
ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS")
with ZipFile(ROOT/"HD-007-HOBBYREGISTER-CORE/CURRENT.zip") as z:
    recs=json.loads(z.read("hd-hobbyregister-core/data/hobby-register.json"))["records"]
with ZipFile(ROOT/"HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip") as z:
    leaf=json.loads(z.read("affiliate-portal-template-kit/assets/hobby-depot-v150750/leaf-category-map-v150750.json"))
hobbies=set(x["parent_slug"] for x in leaf.values())
world_by_hobby={x["parent_slug"]:(x["chain"][0]["path"].split("/")[0]) for x in leaf.values()}
def slug(text, umlaut_mode="short"):
    text=str(text).lower()
    if umlaut_mode=="german":
        text=text.replace("ä","ae").replace("ö","oe").replace("ü","ue")
    else:
        text=text.replace("ä","a").replace("ö","o").replace("ü","u")
    text=text.replace("ß","ss")
    text=unicodedata.normalize("NFKD",text)
    return re.sub("-+","-",re.sub("[^a-z0-9]+","-",text)).strip("-")
by_slug=defaultdict(list)
for x in recs:
    ids=[slug(x["canonical_name"]),slug(x["canonical_name"],"german"),slug(x["registry_id"].removeprefix("hobby:")),slug(x["registry_id"].removeprefix("hobby:"),"german")]
    for alias in x.get("aliases") or []:
        if isinstance(alias,str):ids.extend([slug(alias),slug(alias,"german")])
    for key in set(ids):by_slug[key].append(x)
missing=sorted(hobbies-set(by_slug))
ambiguous=[x for x in hobbies if len({r["registry_id"] for r in by_slug.get(x,[])})>1]
skipwords=["zeit","platz","freude","geduld","interesse","kenntnisse","genehmigung","erfahrung","lust","übung","wind","wetter","ruhen","ausdauer","natur","raum","arbeitsfläche","geeigneten","freie","freier","freien"]
skip=re.compile(r"\b(?:"+"|".join(skipwords)+r")\b",re.I)
rows=[]
for s in sorted(hobbies):
    if s not in by_slug:continue
    x=next((r for r in by_slug[s] if slug(r["canonical_name"])==s),by_slug[s][0])
    need=x["result_profile"]["what_do_you_need"].strip()
    first=need.rstrip(".").split(",",1)[0].strip()
    potential=bool(first and len(first)<55 and len(first.split())<=6 and not skip.search(first) and " oder " not in first.lower() and " und " not in first.lower())
    world=world_by_hobby.get(s) or "unbekannt"
    rows.append((world,s,x["canonical_name"],first,potential,need))
counts=Counter("Prüfwort" if x[4] else "Unklar" for x in rows)
worlds=Counter(x[0] for x in rows)
print("CATEGORY_COVERAGE",len(hobbies),"REGISTER_MATCHED",len(rows),"MISSING",len(missing),"AMBIGUOUS",len(ambiguous))
print("SEARCH_TERM_PREFLIGHT",dict(counts))
print("WORLD_COVERAGE",dict(worlds))
print("MISSING_SAMPLE",missing[:50])
for s in ["sportdrachen","3d-druck","architekturmodellbau","munzen","airbrush-modellbau","alabasterschnitzen"]:
    for row in rows:
        if row[1]==s:print("EXAMPLE",row)
selected=[]
for world in sorted(worlds):
    pool=[x for x in rows if x[0]==world]
    selected.extend(pool[:3])
    selected.extend([x for x in pool if not x[4]][:2])
out=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/AFFILIATE/DATAFORSEO_KOSTENFREIE_VORPRUEFUNG_20261108.md")
lines=[
"# Hobbydepot: DataForSEO-Produktbefüllung – Quellenprüfung vom 08.11.2026",
"",
"Status: ausschließlich Datenprüfung. Keine kostenpflichtige DataForSEO-Abfrage, kein Produkt veröffentlicht, keine neue Plugin-Version.",
"",
"## Echte Quellen",
"- HD009 0.1.28: DataForSEO-Recherche derzeit nur nach Klick im Backend. Einzelne ASINs benötigen manuelle Freigabe in der vorhandenen WordPress-Option hdar_amazon_approved_v1. Ohne Freigabe bleibt eine Produktbox leer.",
"- Hab & Bewahr HAB-004: eigener geprüfter DataForSEO-Automatiklauf mit Tageslimit, Auftragsabfrage und eindeutigen Fehlerhinweisen. Der vollständige Produktkartenbetrieb ist aber noch nicht abgenommen; echte Amazon-Produktbilder fehlen.",
"- HD007: 862 von 862 Hobbydatensätzen haben einen geprüften Text zum benötigten Material oder zur Ausrüstung.",
"- HD003: der aktuelle Kategoriestamm liefert die fachliche Zielzuordnung für sämtliche Kategorieseiten.",
"",
"## Abgleich Register zu bestehenden Hobbyzielen",
f"- Distinkte Hobby-Slugs der aktuellen HD003-Kategoriemappe: {len(hobbies)}",
f"- Eindeutiger Namensabgleich mit Hobbyregister: {len(rows)}",
f"- Ohne automatischen Namensabgleich: {len(missing)}",
f"- Mehrdeutige Mehrfachkandidaten: {len(ambiguous)}",
f"- Erste kompakte Ausrüstungsphrasen als mögliche Recherchewörter: {counts['Prüfwort']}",
f"- Erster Ausrüstungsbegriff für direkte Recherche zu ungenau: {counts['Unklar']}",
"",
"Diese Begriffe sind keine fertig geprüften Produktempfehlungen. Keine automatische Übernahme fachlich ungeeigneter Artikel.",
"",
"## Beispielhafte Eingaben zur Prüfung",
"| Welt | Hobby | Ausrüstungsphrase | Einschätzung |",
"|---|---|---|---|"
]
def clean(v):return str(v).replace("|","/").replace("\n"," ").strip()
for world,s,name,first,potential,need in selected:
    lines.append(f"| {clean(world)} | {clean(name)} | {clean(first)} | {'Suchwort-Kandidat' if potential else 'Noch prüfen'} |")
lines += [
"",
"## Fehlende Zuordnungen",
", ".join(missing[:75]) if missing else "Keine.",
"",
"## Bewährte und offene Schritte",
"1. Bereits vorhandene DataForSEO-Verbindung und Produktplatzierung in HD009 behalten; keinen zweiten Workflow, keine neue Produktdatenbank und keine weitere Portalverknüpfung.",
"2. Hab-Worker nur mit seinem mehrfach getesteten Status-/Tageskostenlimit und kostenfreiem Task-GET als Muster benutzen, nicht das fremde Kategorie-/Tracking-Setup übernehmen.",
"3. Recherchebegriff aus dem geprüften Materialbedarf ableiten; zunächst sichere Beispiele wie Sportdrachen: Lenkdrachen und 3D-Druck: 3D-Drucker. Die unklaren Fälle bleiben gesperrt.",
"4. Nach dem Abruf exakte Amazon.de-Ziel-URL, Produkt-ASIN, Produkttitel und fachliche Eignung gegenprüfen. Keine Preise, Bestände oder Bilder aus DataForSEO ungeprüft übernehmen.",
"5. Amazon-Bilder für einzelne Produktkarten nur über eine vertraglich freigegebene Amazon-Inhaltsquelle wie Creators API oder PA API. Erst danach gelten bebilderte Produktboxen als fertig.",
"",
"Dieses Protokoll ist ein Prüfstand, kein Live-Nachweis und kein freigegebenes Installations-Plugin."
]
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text("\n".join(lines)+"\n")
print("AUDIT_REPORT_CREATED",out,"lines",len(lines))
