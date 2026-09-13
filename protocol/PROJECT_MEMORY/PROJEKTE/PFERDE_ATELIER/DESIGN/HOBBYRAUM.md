# DESIGN – HOBBYRAUM

STAND: 2026-09-13
STATUS: AKTIV / JOURNAL V1.50.477 TECHNISCHER KANDIDAT PASS / LIVE-READBACK OFFEN

## AKTUELLER AUFTRAG

Die Journal-Startseite wird nach dem vom Nutzer freigegebenen Entwurf neu gegliedert:

1. normale redaktionelle Journal-Themen oben;
2. eigener Abschnitt `Wissen & Nachschlagen`;
3. dort zwei breite Einstiege `Glossar` und `Pferderassen`;
4. danach `Neu im Journal`;
5. Glossar- und Pferderassen-Beiträge dürfen in `Neu im Journal` und `Besonders lesenswert` nicht erscheinen.

## EXAKTE ARBEITSBASIS

Nicht `main` und nicht ein älterer Versionszweig.

Exakte aktuelle LIVE-Basis aus dem gebundenen Design-Hobbyraum-Artefakt:
`DESIGN_HOBBYRAUM_CANDIDATE.zip`

SHA-256:
`11b664a10d4ef0ec82f0011436eb92715d9efd14474893fecddcb64e91e6fe0b`

Diese Bytes entsprechen dem im `CURRENT_STATE.md` dokumentierten LIVE-Stand `1.50.472 / Contract V104 + DESIGN-ORDER-SWAP-002`.

## WARUM DER MINI-PATCH-RUNNER HIER NICHT GILT

Der bestehende `MINIMAL_PATCH_RUNNER.py` darf ausschließlich zwei direkt aufeinanderfolgende Codebereiche vertauschen. Der aktuelle Auftrag ist ausdrücklich kein Elementtausch, sondern eine neue Journal-Struktur mit zusätzlicher Kategorieauflösung, eigenem Wissensbereich, responsiver Darstellung und Query-Ausschlussregeln. Der Mini-Patch-Runner bleibt für künftige echte Miniänderungen unverändert verbindlich, ist für diesen Auftrag aber fachlich nicht anwendbar.

## TECHNISCHER KANDIDAT

Version:
`1.50.477`

Plugin-Identität bleibt unverändert:
`affiliate-portal-template-kit/pferde-template-kit.php`

Geändert wurde ausschließlich diese eine Plugin-Datei. Die übrigen 497 Paketdateien sind gegenüber der exakten LIVE-Basis unverändert.

Umsetzung:
- Pferderassen-Kategorie `1482` wird aus dem normalen Themenraster in `Wissen & Nachschlagen` verschoben;
- neue WordPress-Kategorie `Glossar` wird fail-closed exakt über Slug `glossar`, ersatzweise exakten Namen `Glossar`, aufgelöst;
- oberes Themenraster enthält acht redaktionelle Bereiche;
- Wissensbereich enthält genau `Glossar` und `Pferderassen`;
- Reihenfolge: `Themen im Pferde Journal → Wissen & Nachschlagen → Neu im Journal`;
- vorhandene Kategorie-Thumbnails werden nur als kleine `medium_large`-Lazy-Images genutzt; fehlt ein Bild, bleibt die bisherige Icon-Karte erhalten;
- Glossar erhält A–Z-/Lexikon-Visual;
- Pferderassen erhält Rassen-Visual bzw. vorhandenes Kategorienbild;
- Desktop: zwei breite Wissenskarten nebeneinander; Tablet/Mobil responsiv untereinander;
- `category__not_in` schließt Glossar und Pferderassen hart aus `Neu im Journal` und `Besonders lesenswert` aus, auch bei Mehrfachkategorisierung.

## TECHNISCHE PRÜFUNGEN

Lokaler/exakter Paket-Gate auf den gebundenen Bytes:
- PHP-Lint aller 4 PHP-Dateien: PASS;
- Konfigurationsvertrag: 10 Kategorien = 8 redaktionell + 2 Wissen/Nachschlagen: PASS;
- Glossar + Pferderassen Rollenbindung: PASS;
- Abschnittsreihenfolge: PASS;
- harte Query-Ausschlüsse in beiden Beitragsabfragen: PASS;
- exakte Glossar-Auflösung positiv: PASS;
- fehlendes Glossar erzeugt keine erfundene Ersatzkategorie: FAIL-CLOSED / PASS;
- gegenüber LIVE-Basis genau 1 Paketdatei verändert: PASS;
- Paketstruktur 498/498 identisch: PASS;
- Source ↔ entpacktes Übergabepaket: byte-identisch PASS;
- ZIP-Integrität und PHP-Lint nach Entpacken: PASS.

Wichtig: Das ist ein technischer Kandidaten-PASS, kein Pferde-LIVE-PASS.

## EXAKTES ÜBERGABEPAKET

`PFERDE_ATELIER_DESIGN_V1.50.477_CONTRACT_V104_JOURNAL_WISSEN_NACHSCHLAGEN_INSTALLIEREN.zip`

SHA-256:
`5fe869e076bf3c30f34889cd6a887c23eb46a81b5502f49a859abffb380db458`

## NEXT ACTION

1. exakt dieses Paket in WordPress über das vorhandene Designplugin installieren/ersetzen;
2. reale Journal-Startseite prüfen;
3. prüfen: acht normale Themen oben;
4. prüfen: `Glossar` und `Pferderassen` gemeinsam im eigenen Wissensbereich;
5. prüfen: `Neu im Journal` enthält keine Glossar-/Rassenbeiträge;
6. Desktop + Mobil real ansehen;
7. erst nach Nutzer-Readback LIVE-Status ändern.

## NICHT ANFASSEN

- `main`;
- Glossar-Plugin;
- Textmaschine;
- Affiliate-Zentrale;
- Kategorieinhalte selbst;
- bestehende DESIGN-LIVE-Wahrheit vor Nutzer-Readback.
