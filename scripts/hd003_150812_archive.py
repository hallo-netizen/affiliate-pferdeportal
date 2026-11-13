#!/usr/bin/env python3
from pathlib import Path
import hashlib,shutil
root=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH')
office=root/'PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT'
source=Path('/tmp/HOBBY_DEPOT_DESIGN_HD003_1.50.812_PRODUCT_KARTEN_VOLL.zip')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(office/'CURRENT.zip')=='3cc8118ed5d9d22acadfd2e9aa9184068f71cbe9ccb2574bcffacdd16d8ac6df'
assert sha(source)=='1a5cad59bf033780abcc08f3ae70f7e7fbaf6a8c209d4cd97371e5828287dafc'
assert (office/'HOBBY_DEPOT_DESIGN_HD003_1.50.811.zip').exists()
for dest in [office/'CURRENT.zip',office/'HOBBY_DEPOT_DESIGN_HD003_1.50.812.zip']:
    shutil.copy2(source,dest);assert sha(dest)==sha(source)
report=(
'# HD003 Design 1.50.812 – Bild, Fakten und Anbieterbuttons korrekt\n\n'
'Datum 13.11.2026. Nur bestehende Kategoriekarten im Designplugin. '
'Keine Änderung am Hero, mobilen Hobbyfinder, anderen Anzeigen, '
'Werbeplätzen oder anderen Portalen.\n\n'
'Verbindlicher Look: Produktbild 150 × 150 px zentriert oben; '
'darunter Produkttitel 14 px, maximal drei wörtlich belegte Produktmerkmale '
'aus HD009, optional Preis. Ein oder mehrere Anbieter-Buttons am unteren Kartenende, '
'beige #FAF8F4, türkis #0F8F95, Radius 1 px, '
'Hover ausschließlich Farbwechsel. '
'Feste gleichmäßige Kartenhöhe, 3/2/1 responsives Raster. '
'Eine Kennzeichnung "Anzeige" über dem kompletten Block, '
'keine doppelten Partner-Tags pro Produktkarte.\n\n'
'Bewiesene QA: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43404530781. '
'Browser (echte öffentliche Airbrush-HTML-Grundlage mit isolierter CSS-/HTML-Probe): '
'1440/850/390/360 px 3/2/1/1 Spalten, Bilder 150px über dem Titel, '
'CTA 17px vor Kartenunterkante, beige/Türkis, 1px Radius, '
'gleich hohe 440px Karten. '
'1291 ZIP-CRC PASS, 13 PHP-Dateien Syntax PASS, zwei Dateien geändert '
'(Version und existierendes Designprofil); CSS ausschließlich im '
'bisherigen Kategorie-Empfehlungs-Abschnitt.\n\n'
'Prüfe die installierte echte Hobbyseite erneut nach Update. '
'Nicht mit bereits installierter Version oder Liveabnahme verwechseln.\n\n'
'Release: https://github.com/hallo-netizen/affiliate-pferdeportal/releases/tag/'
'hobby-hd003-1.50.812-final-product-cards-20261113\n'
)
(root/'DESIGN/HD003_1.50.812_PRODUKTKARTEN_20261113.md').write_text(report+'\nSHA256: '+sha(source)+'\n')
for p in [office/'MANIFEST.md',root/'PLUGINS/PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md']:
    t=p.read_text()
    p.write_text('# HD003 CURRENT 1.50.812 – richtige Produktkarten\n\n'
                 'Full plugin '+sha(source)+'. 1.50.811 unverändert archiviert. '
                 'Beleg: DESIGN/HD003_1.50.812_PRODUKTKARTEN_20261113.md\n\n---\n'+t)
print('HD003_150812_ARCHIVED',source.stat().st_size,sha(source))
