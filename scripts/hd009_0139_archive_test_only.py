#!/usr/bin/env python3
"""Archive only exact QA-passed HD009 0.1.39 – do NOT overwrite CURRENT or release."""
from pathlib import Path
import hashlib,shutil
from zipfile import ZipFile
root=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH')
office=root/'PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE'
candidate=Path('/tmp/HOBBY_DEPOT_HD009_0.1.39_VALIDATED_EQUIPMENT_CANDIDATE.zip')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(office/'CURRENT.zip')=='34b870ad459e9b075a5c8c0aedc335939a72f6689d03216bcfd4134798c73503'
assert sha(candidate)=='94528a6c572c77891c1b5faa8824018d5fd389a731b029607dbad2cc4dc45c7c'
with ZipFile(candidate) as z:
    assert z.testzip() is None and len(z.namelist())==41
dest=office/'CANDIDATES/HOBBY_DEPOT_HD009_0.1.39_VERIFIZIERTE_AUSRUESTUNG_NUR_TEST.zip'
dest.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(candidate,dest)
assert sha(dest)==sha(candidate) and sha(office/'CURRENT.zip')=='34b870ad459e9b075a5c8c0aedc335939a72f6689d03216bcfd4134798c73503'
p=dest.parent/'CANDIDATE_0.1.39_STATUS.md'
p.write_text('''# HD009 0.1.39 – nur geprüfte Zwischenfassung

**Nicht auf WordPress installieren**, bevor ein echter Feedimport die Produktversorgung überprüfbar bestätigt.
Original HD009 CURRENT 0.1.37 bleibt unverändert.

- 34 Original-PHP-Funktionstests mit echtem Hobbyregister bestanden.
- Ganzes Plugin 41/41 CRC, alle PHP-Dateien auf Syntax geprüft.
- Deckt 20 zusätzliche eindeutige Ausrüstungs-Aliasse von 381 aktiven Hobbykonzepten ab; vorhandene direkt passende Produkte bleiben möglich.
- Mehrdeutige und allgemeine Begriffe weiterhin ausgenommen; CB/RC/3D müssen im wirklichen Produkttitel vollständig vorkommen.
- Die drei konkret vorgeführten falschen Airbrush-Produkte werden weiterhin verworfen.
- **Kein Nachweis**, dass Feed 2747 oder 2901 tatsächlich Airbrushpistolen enthält.
- Nicht am eigentlichen GitHub-CURRENT und nicht an Live-WordPress geändert.
- Vollversion SHA256: 94528a6c572c77891c1b5faa8824018d5fd389a731b029607dbad2cc4dc45c7c
- Beleg: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43443268758
- Coverage: AFFILIATE/HD009_0139_REAL_381_COVERAGE_20261113.md
''')
print('ARCHIVED_TEST_CANDIDATE_ONLY',dest.stat().st_size,sha(dest))
print('UNCHANGED_CURRENT',sha(office/'CURRENT.zip'))
