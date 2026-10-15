# HOBBYRAUSCH – IMAGE-ONLY SIMULATION 7 – LOCAL PASS

STAND: 2026-10-15
BASIS: `AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_HOBBY_DEPOT_HUB2_IMAGE_CURATED_WIDER_CLEARER_NOFRAME_LOCALPASS.zip`
ROLLE: rein lokale technische Simulation. KEIN Release. KEIN Installationspaket.

## Zweck
Beweisen, dass die neuen Bilddateien später ohne Architektur-, Mapping- oder Codeänderung in die eingefrorene 1.50.650-Basis eingesetzt werden können.

## Eingesetzte WIP-Einzelquellen
- Astronomie
- Papierkunst
- Textilgestaltung
- Malen & Zeichnen
- Schrift & Lettering
- Guss & Formen
- Miniaturen & Szenen – WIP-Auswahl Kandidat B

## Technische Ableitung
Pro Kategorie:
- Hero: exakt **600×220**, WEBP
- Preview: exakt **200×107**, WEBP
- gleicher bestehender 1.50.650-Zielpfad
- keine Hochskalierung der Quelle

## Positivtest
PASS:
- exakt **14** bestehende Bilddateien geändert;
- **0** Dateien hinzugefügt;
- **0** Dateien entfernt;
- **0** Nicht-Bilddateien verändert;
- **0** PHP-Dateien verändert;
- **0** CSS-/JS-Dateien verändert;
- **0** JSON-/TXT-Dateien verändert;
- `assets/hobby-depot-v150650/hub2-image-map.json` byte-identisch.

Mapping SHA-256 vor/nach:
`0f669f05a232512ad4d4fd386300115f29832c3b249dcb568e7abf957d120a66`

## Zieldatei-Prüfung
PASS:
- 7/7 Hero-Dateien: 600×220 WEBP
- 7/7 Preview-Dateien: 200×107 WEBP
- 14/14 Ausgabedateien eindeutig
- keine zusätzlichen Zielpfade
- keine Datei außerhalb der 14 erwarteten Bildpfade geändert

## Roundtrip
Die lokale WIP-Struktur wurde gezippt und erneut entpackt.

PASS:
- **981/981 Dateien** nach ZIP-Roundtrip byte-identisch zum simulierten WIP-Verzeichnis.

## Ergebnis
Der KISS-Pfad ist technisch bestätigt:

**1.50.650 unverändert lassen → nur bestehende Hero-/Preview-Bilddateien am bestehenden Pfad ersetzen.**

Es ist kein Helper-Plugin, kein neues Mapping, kein Hook und kein Architekturumbau erforderlich.

Der vollständige Kandidat darf trotzdem erst nach kompletter 30/30-Motivfreigabe gebaut werden.
