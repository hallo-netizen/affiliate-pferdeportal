# STARTMASTER0107 – Closeout / Nachholprüfung 2026-09-11 (M37 + erster Liveartikel)

Status: **BLOCKED / USER PAUSE ACTIVE**  
Publish: **verboten**  
107008: **nicht erreicht**

## Autoritativer Endstand

- Technischer/Livetest-Baseline-Commit vor der reinen Closeout-Dokumentationsintegration: `f1d1605f18bd23d9189f89ad173598958718d08a`. Den jeweils aktuellen Repository-`main` nicht aus diesem Chronologieprotokoll ableiten, sondern frisch aus dem Branch lesen.
- `CURRENT_STARTMASTER` bleibt `STARTMASTER0107`.
- PR107 bleibt permanenter, ungemergter Dispatcher; sein Head entsprach beim letzten Produktionsstart exakt dem damaligen technischen Main-Commit. Vor jedem künftigen Start muss er gemäß seinem Vertrag erneut auf den dann aktuellen `main` synchronisiert werden.
- M37 History-Autorität wurde über PR248 integriert.
- M37 Produkt-/Observability-Fix wurde über PR247 integriert.
- Der bestehende Maschinenbeweis M01–M37 sowie `hardlock`/`hardlock-base` wurde vor Integration erbracht.
- M37 ändert keine PPM-/PSERC-/PSTE-/Text-/SEO-/Link-/Design-/Publishregel. Es erhält bei einem weiterhin fail-closed BLOCKED den bereits vorhandenen ersten inneren PPM/PSERC-Grund.

## Tatsächlich ausgeführter Livebefund nach M37

Erster und einziger gestarteter frischer Artikel:
`Das Wichtigste über Hindernisstangen für Pferde`.

1. Reales LanguageTool lieferte `FACHWORKFLOW_REPAIR_REQUIRED / GERMAN_SPELLER_RULE`.
2. Die vollständige Finding zeigte eindeutig den Tippfehler `Stangenarbiet`.
3. Ausschließlich dieser belegte Tippfehler wurde im selben ersten Artikel zu `Stangenarbeit` korrigiert.
4. Derselbe Artikel erreichte danach den realen PPM-6.7.9-/PSERC-Handoff.
5. Aktueller erster echter technischer Blocker:
   `PPM679_REAL_EXECUTION_BLOCKED:PSERC_BRIDGE_PPM_PLAN_VERSION_MISMATCH`.
6. Zweiter Artikel: **nicht gestartet**.
7. Repository-tracked Änderungen durch den Live-Lauf: **keine**.
8. 107008: **nicht erreicht**.
9. Publish / WordPress write: **nicht ausgeführt**.

Live-Evidenz: PR107 issuecomment-5638153888.

## Letzte Read-only Diagnose

PR107 issuecomment-5638208428 konnte `expected`/`actual` der Planversion **nicht** auslesen, weil die Capsule ausschließlich den gebundenen Produktionsschritt 107007 autorisierte.

Daher gilt:
- exakter innerer Fehlercode ist **bewiesen**;
- konkrete `expected`-/`actual`-Versionsfelder und minimale Fixstelle sind **noch nicht bewiesen**;
- keine Detailursache raten.

## Parallelweg PR249

PR249 `Hobbyraum history: register M38 plan-version regression` ist:
- Draft,
- unmerged,
- Branch `hobbyroom/m38-plan-version-history-20260911`,
- Head `0d23e592a91a448fcc07fb5bd0a54b59985ef70c`.

Zum Closeout-Zeitpunkt enthält sein Diff nur `.tmp_m38_history_anchor`.
Die angekündigten M38-Änderungen an bestehender Matrix/Runner sind damit **noch nicht materialisiert oder maschinell bewiesen**.

Die im PR-Text vorgeschlagenen Werte `plan_contract_version == "4.0.0"` und
`required_plugin_version == "6.7.9"` werden bis zur unabhängigen Beweisführung
**nicht als aktuelle Root-Cause-Wahrheit übernommen**.

PR249 nicht überschreiben, nicht mergen und nicht als PASS behandeln.

## NEXT ACTION nach explizitem Resume

1. Main und PR249 frisch erneut lesen.
2. Falls PR249 weiterhin der gebundene M38-History-Weg ist: nur bestehende Fehlermatrix + bestehenden Regressionrunner ergänzen; temporären Anchor entfernen.
3. Beweisen: Main M01–M37 PASS, M38 erster neuer FAIL; History-Kandidat mit bestehendem History-Maschinenbeweis/hardlocks.
4. Erst danach separater kleinstmöglicher Produktfix gegen die **bewiesene** Versionsabweichung.
5. Danach genau einen frischen ersten Artikel erneut vollständig durch reales LanguageTool + reales PPM/PSERC.
6. Erst nach Einartikel-PASS restlichen Batch bis 107008; vor Publish stoppen.

## WAS / WARUM

- M37 wurde gebaut, weil der äußere Handoff einen real vorhandenen inneren PPM/PSERC-Blockgrund auf den Sammelcode reduzierte.
- Die Änderung ist reine Observability bei unverändertem Fail-Closed-Verhalten.
- Die LanguageTool-Reparatur war keine Regeländerung, sondern eine einmalige, durch vollständige reale Finding belegte Textkorrektur.
- Nach Wiederauftreten von `PSERC_BRIDGE_PPM_PLAN_VERSION_MISMATCH` wird die frühere Einstufung `RESOLVED_BY_PR237` nur noch als historischer Vorgängerbefund behandelt, nicht als aktuelle Wahrheit.
- Keine allgemeine Campus-Architektur, kein Zielvertrag, keine Fachregel und kein Publishweg wurden geändert.

## NICHT ANFASSEN während Pause

- keine Produktion / kein zweiter Artikel;
- kein Merge von PR249;
- kein Produktfix;
- keine PPM-/PSERC-/PSTE-/Textmaschinen-/Fach-/SEO-/Link-/Tabellen-/Designregel;
- kein neuer Runner, Gate, Controller oder Sidecar;
- kein Publish / kein WordPress write;
- System-3-Parallelwege nicht mit STARTMASTER0107 vermischen.

## Closeout-Klassifikation

- Aktueller Projektstatus: `BLOCKED`.
- Grund: realer `PSERC_BRIDGE_PPM_PLAN_VERSION_MISMATCH` plus expliziter User-Pause.
- Zielvertrag: unverändert.
- Archiv: nicht betroffen; ältere Livebefunde bleiben Historie und dürfen CURRENT nicht überschreiben.
- Campus-/Architekturfolge: keine allgemeingültige Architekturänderung; M37 ist eine lokale STARTMASTER0107-Observability-Reparatur.
