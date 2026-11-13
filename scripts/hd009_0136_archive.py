#!/usr/bin/env python3
from pathlib import Path
import hashlib,shutil
root=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH')
office=root/'PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE'
source=Path('/tmp/HOBBY_DEPOT_HD009_0.1.36_PRODUCT_RELEVANCE_AND_BUTTONS.zip')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(office/'CURRENT.zip')=='c30b3381928454671a8784f99c6bd59aaec79c800b9d38925462fc9dd29fe246'
assert sha(source)=='c5207290e535aaad03f26713d4e39b59836475e63cfeff9d57dc04a53944ca68'
assert (office/'HOBBY_DEPOT_AFFILIATE_HD009_0.1.35.zip').exists()
for dest in [office/'CURRENT.zip',office/'HOBBY_DEPOT_AFFILIATE_HD009_0.1.36.zip']:
    shutil.copy2(source,dest);assert sha(dest)==sha(source)
report=(
'# HD009 0.1.36 – Belegte Produktrelevanz, echte Kurzmerkmale und Mehranbieter-Karten\n\n'
'Datum 13.11.2026. Vollversion, aus exakt CURRENT 0.1.35 aufgebaut, '
'darunter enthält die Basis auch 0.1.34 sicheren Feedvergleich. '
'Nur eine bestehende PHP-Hauptdatei geändert; kein neuer Import, keine DB-Tabelle, '
'keine Frontend-API, kein WordPress-Core, keine fremden Portale.\n\n'
'Belegter Livefehler: Auf Hobby Depot /gestalten/malen-zeichnen/airbrush/ '
'standen zwei Damenbekleidungsprodukte mit Modellname Malene und Cotton Batik. '
'Der 0.1.35 Zielpfad war allein nicht ausreichend; die neuen Regeln verlangen '
'nun zusätzlich **direkte Hobbybegriffe im tatsächlichen konkreten Produkttitel** '
'(nur Idealo auf WordPress-Hobbyseiten). Malene ist nicht Malen, '
'Gründl Cotton Batik nicht Airbrush. Andere Provider werden nicht verändert; '
'Artikel, Banner, GTIN und iPN-API bleiben bestehen. '
'Wenn kein sicher passendes Produkt existiert, darf der Slot leer bleiben.\n\n'
'Produktkarte: Der vorhandene Kategorie-Produkt-HTML-Aufbau hat nun '
'Bild über Titel/Text statt nebeneinander: inline grid columns exakt eine '
'Spalte. Die Karte kann bereits vorhandene Mehrfachanbieter-Buttons von '
'multiprovider_matching_offers_for_banner weiter ausgeben. '
'Wenn der Produktname wörtlich eine Maßangabe, Farbe, Material, '
'Set oder konkreten Typ enthält, gibt es 1-3 kurze Fakten unter '
'"Auf einen Blick". Keine erfundenen Spezifikationen.\n\n'
'Beweis QA: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43404268478\n'
'13 echte PHP-Lauftests (3 falsche und 1 passende Airbrush-Kampagne, '
'Artikel-/Amazon-/eBay-Unverändertheit, Teleskop-Plural, Wortstamm, '
'reale Maße/Farben/Set und kein erfundener Fakt); alle 24 PHP-Lints, '
'41 CRC, sämtliche 40 anderen Plugin-Dateien unverändert. '
'Multiprovider-Rendering, Feedimport, API und Vergleichsmethoden unverändert.\n\n'
'Die tatsächliche Liveinstallation und echte Amazon-Produktüberschneidungen '
'sind nicht nachgewiesen. Das Standardfeed 2901 wurde mit echten Daten '
'noch nicht gegen 2747 geprüft. Keine Behauptung einer höheren Abdeckung.\n\n'
'Release: https://github.com/hallo-netizen/affiliate-pferdeportal/releases/tag/'
'hobby-hd009-0.1.36-proven-hobby-cards-20261113\n'
)
(root/'AFFILIATE/HD009_0.1.36_PRODUCTS_FACTS_BUTTONS_20261113.md').write_text(report+'\nSHA256: '+sha(source)+'\n')
for p in [office/'MANIFEST.md',root/'PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/CURRENT.md']:
    t=p.read_text()
    p.write_text('# HD009 CURRENT 0.1.36 – Produktrelevanz und Fakten\n\n'
                 'Full plugin '+sha(source)+'. Alte 0.1.35- und 0.1.34-Stände erhalten. '
                 'Beweis: AFFILIATE/HD009_0.1.36_PRODUCTS_FACTS_BUTTONS_20261113.md\n\n---\n'+t)
print('HD009_0136_ARCHIVED',source.stat().st_size,sha(source))
