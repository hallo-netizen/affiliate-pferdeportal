# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-30
STATUS: BUCHBINDEN RESEARCH COMPLETE / 2× LIVE READBACK FAIL MIT 7 CREATE / V1.9.3 DIAGNOSE POS+NEG HARD PASS / DIAGNOSE-LIVERUN NÄCHSTES

## Harte Abnahmeregel

**Keine Datei, kein Pluginstand und kein Produktionsschritt gilt als abnahmefähig ohne dokumentierte lokale Positiv- UND Negativsimulation.**

## Live-Protokoll – jetzt bewiesen

Die beiden echten Buchbinden-Dry-Runs waren identisch:
- CREATE 7;
- ADOPT_EXISTING 0;
- UPDATE 0;
- UNCHANGED 0.

Beide Apply-Versuche:
`DEPLOY_READBACK_MISMATCH | Automatischer Rollback: PASS`

Damit ist der Fehler eindeutig im CREATE→Readback-Pfad eingegrenzt.

## Lokale Reproduktion

Exakter echter Buchbinden-Kandidat:
- Preflight 7 CREATE;
- lokaler Deploy+Readback PASS.

Daraus folgt:
Der lokale Mock bildet mindestens eine Live-WordPress-Abweichung noch nicht ab.

## Diagnostischer V1.9.3-Stand

Installer SHA:
`6bd488625e545a1921d88423c1658792d8747aa81b035140c93bcc1174a4fda3`

Kein Produktionsfix.

Erfasst beim Readback je Knoten:
- name;
- slug;
- parent;
- concept_meta;
- logical_parent_meta;
- jeweils expected und actual.

Positiv-/Negativsimulation:
- exakter 7-CREATE-Pfad PASS;
- absichtlich falscher slug erkannt;
- falscher name erkannt;
- falscher parent erkannt;
- falsches concept_meta erkannt;
- falsches logical_parent_meta erkannt;
- jeweiliger Rollback PASS.

Regression:
251/251 PASS.
Fresh-Unpack PHP PASS.
Runtime-Parität 22/22.

## NEXT ACTION

V1.9.3 installieren und den **bereits vorhandenen** Dry-Run genau einmal über
`Geprüften Plan anwenden`
ausführen.

Kein neuer Research-Lauf.
Keine neue Datei.
Kein neuer Dry-Run nötig.

Wenn Live erneut abweicht:
Die Fehlermeldung vollständig hier einfügen.
Sie enthält jetzt den exakten Knoten und Soll/Ist-Feldwert; danach wird erst der reale Ursachenfix gebaut.
