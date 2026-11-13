#!/usr/bin/env python3
from pathlib import Path
import hashlib,shutil
root=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH')
office=root/'PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE'
source=Path('/tmp/HOBBY_DEPOT_HD009_0.1.37_RELEVANT_FACTS.zip')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(office/'CURRENT.zip')=='c5207290e535aaad03f26713d4e39b59836475e63cfeff9d57dc04a53944ca68', 'Prior current differs; refuse replacement'
assert sha(source)=='34b870ad459e9b075a5c8c0aedc335939a72f6689d03216bcfd4134798c73503', 'Built plugin differs from QA result'
for p in [office/'CURRENT.zip',office/'HOBBY_DEPOT_AFFILIATE_HD009_0.1.37.zip']:
    shutil.copy2(source,p)
    assert sha(p)==sha(source)
report="""# HD009 CURRENT 0.1.37 – sichere Airbrush-Ausgabe und Stichpunkte

Datum: 13.11.2026.

Auf Hobbyseiten werden konkrete Idealo-Produkte unmittelbar vor der HTML-Ausgabe nach tatsächlichem Hobbybegriff im Produkttitel geprüft. Die bestehende Zielzuordnung gilt jetzt für alle Idealo-Quellen statt nur für ein Quellenkürzel. Die drei falschen Airbrush-Produkte wurden in der originalen render_banner-Funktion abgewiesen; echte Airbrushpistolen oder Set-Produkte bestanden den Test. Keine Kamera-Platzhalter ohne Produktbild. Belegbare kurze Stichpunkte aus Produktname, Preis und Anbieter, keine erfundenen Eigenschaften. 19 PHP-Funktionstests, 41 ZIP-Dateien, 24 PHP-Dateien, übrige 40 Plugin-Dateien unverändert. Amazon/eBay/Mehrfachanbieter/Feed-Vergleich unverändert. Noch nicht live installiert.

Original SHA256: c5207290e535aaad03f26713d4e39b59836475e63cfeff9d57dc04a53944ca68
Vollständiges neues ZIP SHA256: 34b870ad459e9b075a5c8c0aedc335939a72f6689d03216bcfd4134798c73503
GitHub Actions: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43408681944
Release: https://github.com/hallo-netizen/affiliate-pferdeportal/releases/tag/hobby-hd009-0.1.37-last-render-facts-20261113

Keine Liveinstallation in WordPress aus dem Repo behauptet.
"""
(root/'AFFILIATE/HD009_AIRBRUSH_FAKTEN_AUSGABE_0.1.37_20261113.md').write_text(report)
for p in [office/'MANIFEST.md',root/'PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/CURRENT.md']:
    old=p.read_text()
    p.write_text('# HD009 CURRENT 0.1.37 – sichere Airbrush-Ausgabe und Stichpunkte\n\nVollständiges CURRENT.zip SHA256: 34b870ad459e9b075a5c8c0aedc335939a72f6689d03216bcfd4134798c73503. Vorversion als versioniertes ZIP archiviert. Details: AFFILIATE/HD009_AIRBRUSH_FAKTEN_AUSGABE_0.1.37_20261113.md.\n\n---\n\n'+old)
print('ARCHIVED',source.stat().st_size,sha(source))
