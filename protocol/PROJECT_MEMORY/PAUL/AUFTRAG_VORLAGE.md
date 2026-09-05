# PAUL – ZUWEISUNGSSCHEMA

STATUS: NUR SCHEMA / KEINE AKTUELLE AUFTRAGSWAHRHEIT

## Zweck

Diese Datei ist **keine Paul-Auftragsakte** und wird niemals als aktueller Auftrag fortgeschrieben.

Die einzige aktuelle Paul-Zuweisung liegt – nur solange Paul wirklich arbeitet – direkt im zuständigen Büro-`HOBBYRAUM.md`.

Damit braucht der Nutzer keinen Übergabeprompt zu erzeugen.

## Verbindlicher Block im zuständigen HOBBYRAUM

```
<!-- PAUL_ASSIGNMENT_V1
STATUS: ACTIVE
WORKER: PAUL
ASSIGNMENT_ID: <eindeutige ID>
PAUL_BRANCH: paul/<auftrag>
TECHNICAL_BASE_SHA: <exakter 40-stelliger Ausgangscommit>
WRITE_SCOPE: <datei;verzeichnis/> oder READ_ONLY
TASK_SOURCE: <autoritative Problem-/Auftragsquelle>
TARGET_SOURCE: <autoritative Zielquelle>
RULES_SOURCE: <autoritative Hard-Rules-Quelle>
-->
```

## Bedeutung

- `ASSIGNMENT_ID`: Identität genau dieses Paul-Auftrags.
- `PAUL_BRANCH`: exklusiver Paul-Arbeitsbranch.
- `TECHNICAL_BASE_SHA`: Ausgangscommit, von dem der Paul-Branch abstammt.
- `WRITE_SCOPE`: einzige technischen Dateien/Verzeichnisse, die Paul verändern darf; `READ_ONLY` erlaubt keine Writes.
- `TASK_SOURCE`: Verweis auf die autoritative Problem-/Auftragsquelle.
- `TARGET_SOURCE`: Verweis auf den autoritativen Zielvertrag/die Zielquelle.
- `RULES_SOURCE`: Verweis auf die bindende Hard-Rules-Quelle.

Problem-/Fehlertext, Zielinhalt und Regeln werden hier **nicht dupliziert**.

## Automatik

Der trusted Paul-Scope-Gate liest den offiziellen Campus selbst.

Er verlangt:
- genau einen aktiven Paul-Auftrag campusweit;
- Branch = `PAUL_BRANCH`;
- technischer Ausgangscommit = Vorfahr des Paul-Heads;
- alle Writes innerhalb `WRITE_SCOPE`;
- niemals Write unter `protocol/PROJECT_MEMORY/**`;
- relevante Quellen vor Start und vor Rückgabe unverändert bzw. frisch geprüft.

Fehlt die Bindung:
`PAUL_NOT_ASSIGNED`.

Mehrere Bindungen:
`PAUL_MULTIPLE_ASSIGNMENTS_BLOCKED`.

Relevante Drift:
`STALE_ASSIGNMENT_BLOCKED`.

## Rückgabe

Paul liefert Befund, Ursache, KISS-Lösung, Positiv-/Negativtests, Commit(s), offene Risiken.

Der zuständige Arbeitschat entscheidet über Übernahme/Anpassung/Verwerfen und aktualisiert danach allein die offizielle Campuswahrheit.
