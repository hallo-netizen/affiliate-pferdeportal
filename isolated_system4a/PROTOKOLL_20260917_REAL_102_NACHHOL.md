# PROTOKOLL — SYSTEM 4A REAL 102 REPAIR NACHHOLPRÜFUNG — 17.09.2026

Dieses Dokument ist **Historie/Protokoll**, keine CURRENT_STATE und kein Einstiegspunkt.

## Anlass

Die frühere Punkt-5-Aussage `102/102 Repair PASS` wurde gegen den tatsächlich ausgeführten Testcode geprüft. Ergebnis: der alte Test bewies Owner-Routing und gemeinsame Rückwege, aber nicht 102 reale Einzelreparaturen. Punkt 5 wurde deshalb unter dem neuen HARD RULE wieder geöffnet.

## Ausgeführte Arbeit

- Neuer mockfreier Real-102-Harness auf Branch `hobbyroom/system4a-real-102-repair-matrix-clean-20260917` gebaut.
- 102er-Verteilung hart gebunden: 96 DRAFT_WORKER / 3 PARENT_TITLE_MACHINE / 2 PORTAL_LINK_MACHINE / 1 PARENT_CATEGORY_MACHINE.
- Drei W4-Heading-Regeln als falsch geroutet entdeckt: reparierbar, aber zuvor HARD_BLOCK. Testweg auf DRAFT_WORKER korrigiert und Regression gebunden.
- Veraltete PPM-Canonical-Fixture durch Mutationen auf aktueller grüner System-4A-Basis ersetzt.
- 15 aktuelle Canonical-PPM-Mutationen erreichen im letzten echten Lauf jeweils ihren exakten Fehlercode.
- `tests/test-historical-regressions.php` aus dem gebundenen PPM-Paket vollständig inspiziert.
- Festgestellt: Datei enthält 16 alte Infrastruktur-Incidents, nicht die 22 Content-Regeln, die ihr die Registry als `negative_test` zuordnet.
- Run `35214897183`, Head `2eba56cda276c67721577f0104ad89b65a2af890`, endet deshalb korrekt FAIL; kein 102/102-PASS erzeugt.
- Im selben Run für alle 22 Codes im PHP-Testbestand gesucht: nur `BLOCKED_CONTENT_REQUIRED_BLOCK_MISSING` besitzt direkte Treffer in `three-type-bundled-local/*-negative.php`; die übrigen 21 nicht.

## Entscheidung / WARUM

Die historische Testdatei darf nicht durch bloßes Ausgeben erwarteter Fehlercodes künstlich grün gemacht werden. Für die 22 Regeln müssen echte aktuelle Mutationen oder echte vorhandene Tests gebunden werden. Erst danach ist ein 102/102-PASS zulässig.

## Nicht verändert

- Produktions-`control/startmaster0107/CURRENT_STATE.json` nicht manuell verändert; Autorität bleibt `ENTRANCE_GATE_ONLY`.
- Keine 107008-Aktivierung.
- Kein ENDSTEMPEL-/Publish-Bypass.
- Zielvertrag unverändert.
- Plugins: NICHT BETROFFEN.

## Offener erster Fehler / NEXT ACTION

22 veraltete/falsche `negative_test`-Bindungen auf `tests/test-historical-regressions.php` mit echten aktuellen Einzelmutationen schließen; dann `System 4A Real 102 Repair Matrix` wiederholen, bis `TEXTMASCHINE_REAL_REPAIR_FULL_PASS:102/102` real PASS ist.

Danach erst: globaler PASS-Audit `Was behauptet jeder PASS – und was testet der Code wirklich?`.
