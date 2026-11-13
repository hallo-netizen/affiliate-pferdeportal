#!/usr/bin/env python3
"""Archive only the hard-tested 0.1.34 candidate. Never replace CURRENT 0.1.33."""
from pathlib import Path
import hashlib,shutil,os
root=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH')
office=root/'PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE'
source=Path('/tmp/HOBBY_DEPOT_HD009_0.1.34_FEEDVERGLEICH.zip')
original=office/'CURRENT.zip'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(original)=='b6482b5d880e941c97ac726dffa85fbc46ba8514587e23700951d176ebcb63db'
folder=office/'CANDIDATES'
folder.mkdir(exist_ok=True)
target=folder/source.name
shutil.copy2(source,target)
assert sha(target)==sha(source)
assert sha(original)=='b6482b5d880e941c97ac726dffa85fbc46ba8514587e23700951d176ebcb63db'
text=(
"# HD009 0.1.34 – geprüfter, lesender Idealo-Feedvergleich\n\n"
"**Status:** Installierbarer Vergleichskandidat; CURRENT 0.1.33 unverändert.\n\n"
"**Fakten:** Hobby Depot PID 568912, zwei freigeschaltete Feeds: 2747 Fashion/Sport/Outdoor "
"und 2901 Standard. Aus Feed 2747 wurden zuletzt 2.530 Produkte auf 52 Hobbyziele "
"mit 429 Produktkarten zugeordnet. Die wirkliche 2901-Abdeckung war bisher **nicht getestet**.\n\n"
"**Umsetzung:** Ein neuer Vergleichsknopf auf der vorhandenen idealo-Fachseite von HD009. "
"Er nutzt den vorhandenen API-Key nur auf dem Server, bestätigt Feed 2901 für PID 568912 "
"erneut über die offizielle iPN-findFeeds-API und liest den 2901-CSV.GZ-Feed einmalig "
"im Hintergrund ohne Produktimport. Die passenden Produktzeilen werden mit dem *unveränderten* "
"Originalmatcher und denselben Bild- und GTIN-Regeln geprüft. Die 2747-Versorgung wird "
"nur per SELECT aus bestehenden Produkteinträgen gelesen. Ausgabe: Überlappung, zusätzliche "
"2901-Hobbys, bei Wechsel verlorene 2747-Hobbys, Gesamtsumme und Hobbytitel.\n\n"
"**Datenschutz und Schutz:** Kein geänderter Idealo-Feed, keine geänderten Anzeigen, "
"keine neuen Kampagnen, kein veröffentlichter Produktwechsel, keine Änderung an "
"Amazon/DataForSEO, eBay, Design oder WordPress-Kern. Nur ein Vergleichsbericht in einer "
"isolierten WordPress-Option. Button benötigt Administratorrecht und Nonce, Hintergrundarbeiter "
"hat ein einmaliges Zeit-Token. Keine automatischen oder wiederholten Feedvergleiche.\n\n"
"**Hard-QA:** Unveränderte 41 Original-ZIP-Dateieinträge, Syntax aller 24 PHP-Dateien, "
"13 vorhandene Originalmethoden exakt unverändert, verbotene Schreibzugriffe im Vergleich "
"statisch ausgeschlossen, 25 echte PHP-Funktionstests mit synthetischen CSV.GZ-Feeds "
"(Zuordnung, falsche Treffer, EAN/GTIN, Bilder, Feedverfügbarkeit, fremde Werbefläche, "
"Doppelstart und Abgleich 2901 gegen vorhandene 2747-Konzeptliste). "
"Keine Behauptung über noch nicht gelesene echte 2901-Daten.\n\n"
"**Live-Abnahme:** Nach bewusster Installation auf Hobby Depot den Vergleichsknopf "
"einmal betätigen. Nach Abschluss echte Zahlen für beide Feeds vergleichen. "
"Vorher **keine Änderung der Feed-ID und keine Umstellung des Imports**.\n\n"
"Belege: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/"
+os.environ['GITHUB_RUN_ID']+"\n"
"Release: https://github.com/hallo-netizen/affiliate-pferdeportal/releases/tag/"
"hobby-hd009-0.1.34-safe-feedcompare-20261113\n"
"SHA256: "+sha(source)+"\n"
)
(root/'AFFILIATE/HD009_FEEDVERGLEICH_2747_2901_0.1.34_20261113.md').write_text(text)
(folder/'README_0.1.34.md').write_text("Geprüfter Kandidat HD009 0.1.34, CURRENT bleibt 0.1.33.\nSHA256: "+sha(source)+"\n")
print('CANDIDATE_ONLY',target.name,source.stat().st_size,sha(source))
print('CURRENT_UNCHANGED_0133',sha(original))
