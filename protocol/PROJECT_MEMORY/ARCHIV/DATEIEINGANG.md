# ARCHIV – DATEIEINGANG

STAND: 2026-09-05

## Wer sortiert?

Die Zuordnung übernimmt der bearbeitende Chat nach der Masterdateien-Regel.

Der Nutzer muss NICHT selbst entscheiden, in welchen Archivbereich eine Datei gehört.

## Wann muss der Nutzer hochladen?

### Kein Upload nötig
Wenn die Datei bereits:
- im zugänglichen GitHub-Repository liegt oder
- in ChatGPT Library/Chat bereits vorhanden und lesbar ist.

### Einmaliger Upload nötig
Wenn die Datei ausschließlich lokal liegt.

Dann einmal bereitstellen.

## Ablauf

1. Original identifizieren.
2. Hash bilden.
3. vollständig inventarisieren.
4. aktuelle Wahrheit vs. Historie trennen.
5. Büro/Modul/Zielvertrag/Fehlerbeleg zuordnen.
6. persistente Archivkopie anlegen.
7. Archiv-Ampel setzen.
8. Hauptquelle/Referenz festhalten.

## Archiv-Ampel für lokale Löschung

### ROT
Nicht vollständig archiviert.
Lokale Datei behalten.

### GELB
Hash + Archivkopie vorhanden, aber nur ein unabhängiges Speichersystem.
Lokale Datei weiter behalten.

### GRÜN
Hash + mindestens zwei unabhängige verifizierte Speicherorte.
Dann darf im Archivregister stehen:
`LOKALE_KOPIE_ENTBEHRLICH: JA`

Der Nutzer muss das nicht selbst beurteilen.

## Rohdateien / Secrets

Secrets niemals in ein öffentliches Repository kopieren.

Existenz, Funktion, Hash und sichere Zuordnung bleiben trotzdem dokumentiert.

## Harte Regel

**Ich sage erst dann ausdrücklich, dass eine lokale Kopie entbehrlich ist, wenn der Archiv-Eintrag GRÜN ist.**
