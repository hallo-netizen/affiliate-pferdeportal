#!/usr/bin/env python3
"""Archive exact QA-verified HD003 1.50.814, preserving 1.50.813."""
from pathlib import Path
import hashlib,shutil
root=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH')
office=root/'PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT'
src=Path('/tmp/HOBBY_DEPOT_DESIGN_HD003_1.50.814_OHNE_LEERKARTEN.zip')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original='5fb7053f31d705b9c2001fbcdfecf518c05d8c1fe52283f058943ca48f6eba73'
new='263284e057b9c2a3cc57cc4807301ab2e74c1daeae8dfeb0a16191c49a9dc18f'
assert sha(office/'CURRENT.zip')==original,'Unexpected old CURRENT, refuse'
assert sha(office/'HOBBY_DEPOT_DESIGN_HD003_1.50.813.zip')==original,'Backup missing, refuse'
assert sha(src)==new,'QA SHA changed, refuse'
for dest in [office/'CURRENT.zip',office/'HOBBY_DEPOT_DESIGN_HD003_1.50.814.zip']:
    shutil.copy2(src,dest)
    assert sha(dest)==new
report=root/'DESIGN/HD003_FEHLERPROTOKOLL_LEERE_PRODUKTKARTEN_20261113.md'
log=report.read_text()
log+='''

## Stand 04 – vollständiges Plugin nach harten Tests im Büro archiviert
- Datei \`HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip\` und versionsfeste Datei \`HOBBY_DEPOT_DESIGN_HD003_1.50.814.zip\` sind vollständig, byte-identisch und auf SHA256 \`'''+new+'''\` verifiziert.
- Vorversion \`HOBBY_DEPOT_DESIGN_HD003_1.50.813.zip\` ist unverändert vorhanden.
- Keine WordPress-Liveinstallation durch das Büro; keine echte Airbrush-Produktversorgung nachgewiesen.
- Download nach Freigabe: https://github.com/hallo-netizen/affiliate-pferdeportal/releases/download/hobby-hd003-1.50.814-no-empty-product-cards-20261113/HOBBY_DEPOT_DESIGN_HD003_1.50.814_OHNE_LEERKARTEN.zip
'''
report.write_text(log)
for doc in [
    office/'MANIFEST.md',
    root/'PLUGINS/PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md'
]:
    old=doc.read_text()
    doc.write_text(
        '# HD003 CURRENT 1.50.814 – keine leeren Affiliate-Produktkarten\n\n'
        'Fehlerwurzel: eingeloggte Produktplatzhalter wurden als Empfehlungen-Karten ausgegeben. '
        '3 Quellzeilen korrigiert, 36 originale PHP-Lauftests und 1.291 ZIP-CRC bestanden. '
        'Vollversion sha256 \`'+new+'\`. Vorversion 1.50.813 sicher gespeichert. '
        'Lücken bei echter Produktversorgung bestehen weiter. '
        'Führendes Fehlerregister: \`DESIGN/HD003_FEHLERPROTOKOLL_LEERE_PRODUKTKARTEN_20261113.md\`.\n\n'
        'GitHub Actions: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43411117782\n\n'
        '---\n\n'+old
    )
print('CURRENT_VERIFIED',src.stat().st_size,sha(office/'CURRENT.zip'))
print('BACKUP_150813_VERIFIED',sha(office/'HOBBY_DEPOT_DESIGN_HD003_1.50.813.zip'))
