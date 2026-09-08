# P11 – UNVERÄNDERLICHER 12-GATE-VERTRAG

Datum: 2026-09-08
Status: GO

## Ziel

Alle aktuell autoritativ geforderten Fach-/Qualitätsgates müssen exakt erhalten bleiben.
Kein Gate darf:
- fehlen
- doppelt vorkommen
- umsortiert werden
- optional werden
- zur Laufzeit deaktiviert werden
- durch ein fremdes Gate ersetzt werden
- Regeln ändern
- Publish erlauben

## Autoritative Quelle

Aktueller Fachworkflow:
`control/startmaster0107/fachworkflow_proof_handoff.py`

Dort aktuell exakt 12 Pflichtstufen:

1. research_fact_pack
2. textmachine_article_type_structure
3. table_contract
4. internal_links
5. languagetool
6. ppm
7. pserc
8. pste
9. duplicate_cannibalization
10. seo
11. design_format
12. publish_safety

P11 kopiert keine Fachregeln.
Es friert nur diese vorhandene Pflichtliste als technischen Vertrag ein.

## Laborlauf

12/12 PASS.

Positiv:
- autoritative Quelle entspricht exakt dem eingefrorenen 12er-Vertrag
- alle 12 Gates exakt einmal -> PASS

Negativ:
- Gate fehlt -> BLOCKED
- Gate ersetzt/dupliziert -> BLOCKED
- Reihenfolge geändert -> BLOCKED
- unbekanntes neues Gate eingeschleust -> BLOCKED
- Gate meldet FAIL -> BLOCKED
- Gate wurde nicht real ausgeführt -> BLOCKED
- content_or_quality_rules_changed=true -> BLOCKED
- publish_allowed=true -> BLOCKED
- enabled=false als Laufzeitschalter -> BLOCKED
- optional=true als Laufzeitschalter -> BLOCKED

## Wichtiger Architekturpunkt

P11 legt NICHT fest, dass jedes Gate einen eigenen technischen Prozess oder Worker braucht.

Wenn mehrere bestehende Gates bereits innerhalb derselben unveränderten Fachkomponente atomar erzwungen werden, dürfen sie dort bleiben.

KISS:
Keine künstliche Aufspaltung nur um „mehr Räume“ zu erzeugen.

Unverhandelbar bleibt:
Jedes der 12 Gates muss separat nachweisbar erfüllt sein.

## 0,0 Freiheit

PASS.

Der Chat/Worker kann:
- kein Gate wählen
- kein Gate deaktivieren
- kein Gate hinzufügen
- kein Gate überspringen
- kein Gate als optional markieren
- die 12er-Liste nicht zur Laufzeit verändern

## Textmaschine / Fachregeln

Unverändert.
P11 enthält keine inhaltliche Regel und interpretiert keine Fachanforderung neu.

## GO/STOP

GO.

Nächster Schritt P12:
Nur Komponenten-Inventur.

Für jedes Gate wird ermittelt:
- welche bestehende unveränderte Komponente heute tatsächlich dafür zuständig ist
- ob mehrere Gates bereits sicher in derselben Komponente liegen
- ob eine eindeutige autoritative Quelle existiert

Keine neue Komponente bauen.
Keine fehlende Implementierung erfinden.
Unklare Zuständigkeit = offen/STOP für genau dieses Gate.
