# HOBBYRAUM – SYSTEM 4 Produktionsabschluss

Status: **BLOCKED – globale FEHLER→WERKSTATT-Invariante teilweise implementiert, aber noch nicht vollständig durch den Gesamtworkflow geführt und auf dem aktuellen Runtime-Head abgenommen.**

## Verbindlicher Einstieg

`control/startmaster0107/PFERDE_ATELIER_START_HERE.json` → `control/startmaster0107/CURRENT_STATE.json` → FRISCHECHECK → dortige NEXT ACTION.

Diese Datei ist **keine zweite CURRENT_STATE**. Dynamischer Stand steht ausschließlich in `CURRENT_STATE.json`.

## Erledigt

- [x] 1. Offizieller CURRENT_STATE und START_HERE wurden auf die aktuelle Arbeit nachgezogen.
- [x] 2. Produktionsweg 107007 bleibt System4-only; kein Legacy-/Fachworkflow-Fallback.
- [x] 3. Reale 7er-Produktion wurde tatsächlich ausgeführt. Der jüngste frische Lauf erreichte mit allen 7 Artikeln den Batch-Eingang und stoppte dort korrekt bei `BATCH_REPEATED_SENTENCE_TEMPLATE_BLOCKED:21>6`; kein WordPress-Handoff und kein Publish.
- [x] 4. Ursache des unnötigen terminalen Abbruchs identifiziert: der Batchfehler war reparierbar, aber es fehlte die globale Rückgabe in eine Werkstatt.
- [x] 5. Globale Regel dauerhaft festgelegt: `isolated_system4/GLOBAL_WORKSHOP_RULE_20260917.md` – **FEHLER → WERKSTATT**, unabhängig von Prüfer, Stufe und Finding-Anzahl.
- [x] 6. Teilimplementierung vorhanden: strukturierte Batch-Repetition-Findings, `global_workshop.py`, Batch-/Controller-/Parent-Workshop-Capture, All-Findings-Continuation im Repair-Router, Writer-Anweisung ohne `findings[0]`-Reduktion.
- [x] 7. Isolierte positive/negative Werkstatt-Unit-Prüfung: 3/3 PASS; zusätzlicher lokaler 21-Satz-Fall erzeugt 21 strukturierte Findings und repairable Workshop-Route; Hash-/Integritätsfall bleibt non-repairable.
- [x] 8. Codex-Nutzungsregel bestätigt: Codex ausschließlich für echte gebundene Artikelproduktion nach ausdrücklicher Nutzerfreigabe; nicht für Implementierung, Tests, Diagnose oder Architektur.

## Offen / erster Blocker

- [ ] 9. `isolated_system4/full_route_start.py` muss die globale Werkstatt-Continuation selbst weiterführen. Aktuell kann ein `BatchGateWorkshop` im vollständigen Route-Runner noch als terminaler `SYSTEM4_FULL_ROUTE_FAIL` enden.
- [ ] 10. `isolated_system4/repair_router.py` muss gemischte Findings nach `(Owner, Target)` getrennt routen. Aktuell werden zwar alle Findings erhalten, aber der primäre Owner/Target wird noch aus dem ersten Finding gewählt.
- [ ] 11. Handoff-/Top-Level-Fehler müssen nachweislich unter dieselbe globale FEHLER→WERKSTATT-Regel fallen; keine lokale Sonderroute.
- [ ] 12. Positiv-/Negativregression ergänzen, die mindestens 4 Artikel mit realistischem Wiederholungsbefund durch Werkstatt → Reparatur → kompletten Recheck → erneuten Batch führt.
- [ ] 13. Danach vollständigen System4 Positiv-/Negativ-Schutzring und realen LT6.8/PPM6.7.9-Korridor auf exakt dem resultierenden Runtime-Head ausführen. Aktuell existiert für Runtime-Head `5391f6915ad5674264304cb7e33774bd9e338b2c` noch **kein** vollständiger Acceptance-Run.
- [ ] 14. Erst nach grünem Acceptance-Head die 107007-Bindung reparieren: tatsächlicher Launch-SHA256 `bf629ea68555f3a14166f1b10eb9ae5910a2e9ae06881aac48f9aa6a9f4f423e`, STEP_107007 deklariert noch `1bfefd0370251ca45ba5868e80a244182da76a865f7713e0b3bde6d5ff492d59`. Anschließend komplette Hash-/Vorgängerbindung frisch prüfen.
- [ ] 15. Erst danach – und nur nach ausdrücklicher Nutzerfreigabe – einen neuen realen Artikelproduktionslauf starten und bis zur tatsächlichen `SYSTEM4_WORDPRESS_HANDOFF_V1.json` nachweisen.

## NEXT ACTION

**OHNE CODEX:** zuerst `full_route_start.py` an die globale Werkstatt-Continuation anbinden und gemischte Owner/Target-Findings im `repair_router.py` sauber gruppieren. Danach gezielte positive/negative Tests einschließlich ≥4-Artikel-Batch-Repetition und anschließend der vollständige Acceptance-Korridor auf exakt demselben Runtime-Head.

## Nicht anfassen

- Textmaschine / Inhaltsregeln
- PPM 6.7.9
- LanguageTool 6.8
- Design / Theme / WordPress-Plugin
- gebundene Fachmetadaten ohne autoritativen Owner
- Legacy-/Fachworkflow-Ersatzwege
- Auto-Publish (`publish_allowed=false`)

## Harte Abschlussregel

Ein Punkt wird nur auf [x] gesetzt, wenn Datei-/Commit-/Run-Beweis vorliegt. Kein PASS aus Erinnerung oder Code-Lesen.
