#!/usr/bin/env python3
from pathlib import Path
import hashlib,shutil
root=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH')
office=root/'PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT'
source=Path('/tmp/HOBBY_DEPOT_DESIGN_HD003_1.50.811_PRODUKTKARTEN.zip')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(office/'CURRENT.zip')=='d63c2c7413f1f3d8ac635abffd3ec7ea69ea0fddff5b4fc6dd4e676ac9c7b1c6'
assert sha(source)=='3cc8118ed5d9d22acadfd2e9aa9184068f71cbe9ccb2574bcffacdd16d8ac6df'
assert (office/'HOBBY_DEPOT_DESIGN_HD003_1.50.810.zip').exists()
for p in [office/'CURRENT.zip',office/'HOBBY_DEPOT_DESIGN_HD003_1.50.811.zip']:
    shutil.copy2(source,p)
    assert sha(p)==sha(source)
report="""
# Hobby Depot HD003 1.50.811 – Kategorie-Empfehlungen

Datum: 13.11.2026. Nur Design HD003; 1.50.810 bleibt unverändert archiviert.

Echter Problembeleg: Auf der Airbrush-Kategorieseite wurden drei
kürzende 84px-Anzeigenkacheln gezeigt; vollständiger Affiliate-Produktplatz
unter der Kachel hatte bereits 416px Höhe, war aber abgeschnitten.
Zusätzlich doppelte Angabe Anzeige Partner über dem Gitter und auf jeder Karte.
Beweis https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43399151033

KISS-Lösung: Eine einzige sichtbare und zugängliche Kennzeichnung
Anzeige vor dem Block Empfehlungen. Die Gruppenkarten geben kein
eigenes Anzeige Partner mehr aus; außerhalb dieses Blocks bleiben alle
anderen Werbekennzeichnungen unverändert. Die vorhandenen echten
Produktkacheln in einem 3/2/1-Raster erhalten ihre vollständige
Originalhöhe, echte Bilder mit 150px, lesbare 14px Produkttitel.
Kein neues Affiliate- oder Bilder-System und keine Änderung an Hero,
Footer, Kategorien, Banner, Mobil-Hobbyfinder, Register oder Partnerdaten.

Harte Tests: 1291/1291 ZIP-CRC, 13/13 PHP-Lint, ausschließlich zwei
bestehende Plugin-Dateien geändert (Version und Kategorieprofil),
echter Headless-Chrome-Test auf unveränderter öffentlicher Airbrush-Seite
bei 1440px (3 Spalten), 850px (2), 390px (1).
Kartenhöhe exakt 418px, nicht abgeschnitten, Bilder 150px, Titel 14px,
ein sichtbares Anzeige und keine Kartenlabel-Duplikate.
https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43401407288

Die Änderung wurde im Browser mit testweise eingefügtem CSS nachgewiesen,
noch nicht in echtes WordPress installiert. Die thematische Produktwahl
gehört getrennt zu HD009 0.1.35.
"""
(root/'DESIGN/HD003_PRODUKTKARTEN_ANZEIGE_EINMAL_1.50.811_20261113.md').write_text(report+"\nSHA256: "+sha(source)+"\n")
for path in [office/'MANIFEST.md',root/'PLUGINS/PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md']:
    old=path.read_text()
    path.write_text('# HD003 CURRENT 1.50.811 – ein Anzeige-Hinweis / Produktkarten 3-2-1\n\n'
      'Vollständiges ZIP SHA256: '+sha(source)+'. Sicherung 1.50.810 erhalten. '
      'Beweis: DESIGN/HD003_PRODUKTKARTEN_ANZEIGE_EINMAL_1.50.811_20261113.md.\n\n---\n\n'+old)
print('ARCHIVED_HD003_CURRENT_811',source.stat().st_size,sha(source))
