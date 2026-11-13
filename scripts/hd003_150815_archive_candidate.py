#!/usr/bin/env python3
"""Archive exact QA-passed editor note HD003 1.50.815 as candidate; never touch CURRENT."""
from pathlib import Path
from zipfile import ZipFile
import hashlib,shutil
root=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH')
office=root/'PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT'
source=Path('/tmp/HOBBY_DEPOT_DESIGN_HD003_1.50.815_EDITOR_PLATZVORSCHAU.zip')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(office/'CURRENT.zip')=='263284e057b9c2a3cc57cc4807301ab2e74c1daeae8dfeb0a16191c49a9dc18f'
assert sha(source)=='191349ae0f41d6f4d38587d180a12e98b95bff32fb96f132867d4ad7d0b74b1d'
with ZipFile(source) as z:
    assert z.testzip() is None and len(z.namelist())==1291
target=office/'CANDIDATES/HOBBY_DEPOT_DESIGN_HD003_1.50.815_ADMIN_VORSCHAU_NUR_TEST.zip'
target.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(source,target)
assert sha(target)==sha(source)
text='''# HD003 1.50.815 – Admin-Vorschau (isolierter Kandidat)

Status: geprüft, aber **noch nicht auf Hobby Depot installiert**. CURRENT 1.50.814 bleibt unverändert.

- Admin sieht bei 0 echten Produktkarten eine einzige kompakte Erklärung der drei freien Produktplätze.
- Ausgeloggte Besucher sehen keine leere Empfehlungssektion.
- 1 bzw. 3 echte Produktkarten bleiben vollständig sichtbar; keine Produktdaten/Provider geändert.
- Keine großen falschen Produkt-Platzhalter; andere Vorschautypen, Farben, Layout, Hero, Footer unverändert.
- 38 echte PHP-Methoden-Funktionstests, vollständige 1291 ZIP-Dateien CRC sowie alle PHP-Dateien Syntax bestanden.
- Vollständiges Kandidaten-ZIP SHA256 191349ae0f41d6f4d38587d180a12e98b95bff32fb96f132867d4ad7d0b74b1d
- QA: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43442464715
- Ausstehend: echte Liveabnahme und Prüfung passender Idealo-Produkte.
'''
(target.parent/'CANDIDATE_1.50.815_STATUS.md').write_text(text)
report=root/'DESIGN/HD003_FEHLERPROTOKOLL_LEERE_PRODUKTKARTEN_20261113.md'
old=report.read_text()
report.write_text(old+'''

## Stand 06 – eingeloggte Vorschau gesondert korrigiert
- Eigenen Fehler in 1.50.814 bestätigt: Die vorherigen drei falschen Admin-Produktkacheln wurden entfernt, aber **auch jede Orientierung**, wo Produktwerbung sitzt.
- In 1.50.815 erscheint bei eingeloggtem Anwender stattdessen ein **schmaler, klar gekennzeichneter Hinweis**, nicht drei große Scheinprodukte. Öffentlicher Besucher ohne Produkte sieht überhaupt keinen Empfehlungsblock.
- 38 echte Original-PHP-Methodentests: Null/Eins/Drei Produkte, angemeldet/abgemeldet, Kategorien/Homepage, echte Karten 1:1 beibehalten, alle bestanden; volles 1291-Dateien-ZIP CRC und sämtliche PHP-Lints erfolgreich.
- QA: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43442464715
- **Als Testkandidat archiviert**, nicht als Live-Erfolg oder abgeschlossenes Idealo-Problem deklariert. Bisherige CURRENT 1.50.814 unverändert.
''')
print('HD003_815_CANDIDATE_ONLY',target.stat().st_size,sha(target),'CURRENT_PRESERVED',sha(office/'CURRENT.zip'))
