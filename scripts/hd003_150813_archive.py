#!/usr/bin/env python3
from pathlib import Path
import hashlib,shutil
root=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH')
office=root/'PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT'
source=Path('/tmp/HOBBY_DEPOT_DESIGN_HD003_1.50.813_SICHTBARE_FARBEN.zip')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(office/'CURRENT.zip')=='1a5cad59bf033780abcc08f3ae70f7e7fbaf6a8c209d4cd97371e5828287dafc', 'Prior current differs; refuse replacement'
assert sha(source)=='5fb7053f31d705b9c2001fbcdfecf518c05d8c1fe52283f058943ca48f6eba73', 'Built plugin differs from QA result'
for p in [office/'CURRENT.zip',office/'HOBBY_DEPOT_DESIGN_HD003_1.50.813.zip']:
    shutil.copy2(source,p)
    assert sha(p)==sha(source)
report="""# HD003 CURRENT 1.50.813 – sichtbares Beige und Türkis

Datum: 13.11.2026.

Nur drei Farbangaben der Kategorie-Empfehlungsbuttons korrigiert: Hintergrund #EFDECA (sichtbares Beige statt #FAF8F4), Text #00777D (kräftiges Türkis) und Rahmen #81AAA8. Anordnung der Bilder, Mehrfachanbieter-Buttons, 1px-Ecken, Mobilansicht, Hero und Footer unverändert. Vier Browsergrößen auf Farben/Stichpunkte geprüft, 1291 ZIP-Dateien und 13 PHP-Dateien bestanden. Noch nicht live installiert.

Original SHA256: 1a5cad59bf033780abcc08f3ae70f7e7fbaf6a8c209d4cd97371e5828287dafc
Vollständiges neues ZIP SHA256: 5fb7053f31d705b9c2001fbcdfecf518c05d8c1fe52283f058943ca48f6eba73
GitHub Actions: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43408810672
Release: https://github.com/hallo-netizen/affiliate-pferdeportal/releases/tag/hobby-hd003-1.50.813-visible-teal-beige-20261113

Keine Liveinstallation in WordPress aus dem Repo behauptet.
"""
(root/'DESIGN/HD003_SICHTBARE_PRODUKTBUTTONS_1.50.813_20261113.md').write_text(report)
for p in [office/'MANIFEST.md',root/'PLUGINS/PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md']:
    old=p.read_text()
    p.write_text('# HD003 CURRENT 1.50.813 – sichtbares Beige und Türkis\n\nVollständiges CURRENT.zip SHA256: 5fb7053f31d705b9c2001fbcdfecf518c05d8c1fe52283f058943ca48f6eba73. Vorversion als versioniertes ZIP archiviert. Details: DESIGN/HD003_SICHTBARE_PRODUKTBUTTONS_1.50.813_20261113.md.\n\n---\n\n'+old)
print('ARCHIVED',source.stat().st_size,sha(source))
