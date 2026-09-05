# BAUCONTAINER – NEUES PROJEKTGEBÄUDE

Zweck: Minimaler Ablauf für ein eigenständiges neues Projekt.

## Vor dem Bau

1. Hauptpförtner lesen.
2. Projektziel/Anforderungen bestimmen.
3. Modulregister prüfen.
4. nur passende allgemeingültige Module auswählen.
5. nur wirklich fehlende Funktionen neu vorsehen.

## Minimaler Aufbau

```
protocol/PROJECT_MEMORY/PROJEKTE/<PROJEKT>/
├── START_HERE.md
└── <ERSTES_BÜRO>/
    ├── START_HERE.md
    ├── CURRENT_STATE.md
    └── HOBBYRAUM.md
```

## Pflicht für jeden neuen Eingang

Jedes neue Gebäude und jedes neue Büro MUSS den Standard erfüllen:

`BAUCONTAINER/EINGANGSSTANDARD.md`

Also oben sofort:
- WAS IST DAS?
- HIER BIST DU RICHTIG, WENN …
- DU DARFST …
- DU DARFST NICHT …
- ALS NÄCHSTES …

**Ein Klick = alles klar.**

## Nutzung allgemeiner Module

Allgemeiner Kern bleibt an seinem Hauptort.

Projekt dokumentiert nur:
- MOD-ID
- Hauptort
- verwendeten Stand
- projektspezifische Konfiguration
- Projektdaten/-historie

## Weitere Regeln

- weitere Büros erst bei echtem Bedarf;
- keine bestehende Projektarchitektur blind kopieren;
- Fehler nur als Verweis registrieren;
- wichtige Änderungen mit WARUM dokumentieren.

Projektgebäude kann technisch im selben oder eigenen Repository liegen.


## Neue Bauvorschriften – verpflichtend

### Flur-/Adressregel
- jedes neue Verzeichnis unter PROJECT_MEMORY erhält sofort `START_HERE.md`;
- neues Projekt zusätzlich in `PROJEKTE/START_HERE.md` eintragen;
- bestehende/verteilte Adressen nicht still umbenennen; bei Umbau Weiterweiser erhalten.

### Büro-Leitungen
Jedes neue Projektbüro führt vor echter Arbeit sichtbar über:
1. `CURRENT_STATE.md`;
2. `HOBBYRAUM.md`;
3. Handlungsverzeichnis;
4. Fehlerregister;
5. Änderungsregister;
6. Zielvertragsregister;
7. gebundenen Arbeitsweg.

### Hobbyraum
Pflicht:
`BAUCONTAINER/HOBBYRAUM_STANDARD.md`

Genau ein Hobbyraum pro Büro.
Zustände nur:
FREI / AKTIV / BLOCKED.

Direktlink in HOBBYRAUM muss selbst 1-Klick-konform sein.

### Abnahme
Vor Freigabe eines neuen Gebäudes:
positive und negative Architekturprüfung gegen
`BAUCONTAINER/EINGANGSSTANDARD.md`
und
`BAUCONTAINER/HOBBYRAUM_STANDARD.md`.


## Informationsrollen für neue Büros

Neue Büros werden nur mit dieser Trennung freigegeben:
- START_HERE = Wegweiser
- CURRENT_STATE = aktuelle Büro-Zusammenfassung
- HOBBYRAUM = aktuelle Arbeitsbindung / NEXT ACTION
- FEHLERREGISTER = Index zur Fehlerquelle
- ZIELVERTRAEGE/REGISTER = Index zur Zielquelle
- ARCHIV = Historie

Vor Freigabe negativ prüfen:
- keine dynamischen Versionsangaben in START_HERE als zweite Wahrheit;
- keine Fehlerhistorie in HOBBYRAUM;
- keine ausführliche Fehlerkopie im zentralen Fehlerregister.
