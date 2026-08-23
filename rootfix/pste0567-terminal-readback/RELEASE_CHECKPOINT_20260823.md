# PSTE 0.56.7 – Terminal Readback Rootfix – Release Checkpoint

## Scope
Ausschließlich der nach 0.56.6 verbliebene Terminal-Readback-Fehler nach abgeschlossenem request-bounded Research-FINALIZE. Keine neue Recherche, keine Änderung an DataForSEO-Queries, Familien-/Kategoriezuordnung, Artikeltypen, Titeln, SEO, fachlichen Sandbox-Entscheidungen, Textmaschine, PSERC, PPM, Design, WordPress-Inhalten oder Publish.

## Live-Ausgangslage
- URL/Browserfluss meldete `research_complete=1`.
- Aktiver Einzellauf war verschwunden.
- Persistenter Readback zeigte dennoch `Letzter abgeschlossener Lauf: RUNNING`.
- Vorher: Provider 3/3 abgeschlossen, Kosten 0.048000 USD; request-bounded SANDBOX/CONTEXT-FINALIZE lief durch.

## Root Cause
`PSTE_Repository::saveRun()` ersetzt die komplette Run-Zeile. Während FINALIZE schrieb `PSTE_Research_Job::saveProgressRun()` wiederholt `status=RUNNING` mit progress-only Payload und verdrängte damit den in PREPARE gespeicherten aggregierten Terminalstatus/Diagnostik. `completeResearchFinalizeJob()` setzte anschließend zwar `research_finalize_state=COMPLETE`, stellte den terminalen Run-Status aber nicht wieder her. Ergebnis: COMPLETE-Fluss ohne aktiven Job, persistenter Status trotzdem RUNNING.

## Fix 0.56.7
- FINALIZE-Progress bewahrt den PREPARED/COMPLETE-Aggregatpayload.
- PREPARE bindet den vorgesehenen Terminalstatus explizit.
- COMPLETE berechnet den Terminalstatus nochmals aus den persistierten Kandidatenentscheidungen, prüft Count/Status, schreibt terminal und liest hart zurück.
- Eng begrenzte Recovery für exakt den 0.56.6-Orphan-Fall: latest run = RUNNING + Workflow LONGTAIL_RESEARCH_TO_METADATA_V2 + provider_steps_completed=3 + research_finalize_state=COMPLETE. Recovery berechnet nur aus bereits persistierten Kandidaten; 0 Providercalls, 0 Kandidatenwrites, 0 Artikel-/Taxonomiewrites; aktiver Job wird nicht neu erzeugt.

## Delta 0.56.6 → 0.56.7
Geändert:
- `portal-seo-topic-engine.php`
- `includes/class-pste-repository.php`
- `includes/class-pste-research-job.php`
- `includes/class-pste-runner.php`

Neu:
- `CHANGELOG_0.56.7.md`

202 weitere Plugin-Dateien byteidentisch. Geschützte Provider-/Query-/Family-/Title-/Metadata-/Article-Type-/Sandbox-/Context-/Admin-Dateien explizit byteidentisch.

## Harte Tests
- PHP-Lint Source/Fresh: 72/72 PASS.
- JSON Source/Fresh: 52/52 PASS.
- Source↔Fresh: 207/207 byteidentisch.
- 0.56.6 Reproduktion: Progress verdrängt PREPARE; nach COMPLETE bleibt Status RUNNING – reproduziert.
- 0.56.7: Progress erhält PREPARE/Diagnostik; COMPLETE → terminal ANALYZED; Readback-Marker PASS.
- Legacy 0.56.6 Orphan: RUNNING/COMPLETE → ANALYZED_NO_ELIGIBLE_CANDIDATE; Marker REPAIRED_0_56_6; 0 Providercalls; 0 Kandidatenwrites; kein neuer aktiver Job.
- Negativ: deklarierter Terminalstatus-Mismatch → BLOCKED ohne Writes.
- Negativ: Kandidatenzahl-Mismatch → BLOCKED ohne Writes.
- Research-FINALIZE State Machine Source/Fresh PASS; alter 2.1.0 Resume → COMPLETE, 0 Providercalls; Stall → PAUSED_ERROR/PSTE_RESEARCH_FINALIZE_STALLED.
- Record-Store Runtime Overlay Source/Fresh PASS.
- Browser-Finalize-Progress Source/Fresh PASS.
- Aktuelle 619-Themen-Projektion 0.56.6/0.56.7/Fresh identisch: SHA `b1950e47c0200830cb71394370bf63f2b22f9f18a1ba5e2bec1f7fd5f170933f`.
- PSERC Capability 0.56.6/0.56.7 identisch: `9d2636ecda87e2d93106deaff4f1358e4fa9cf906c1d55177e3119d94df65d8f`.
- PPM 6.7.9: 137/137 erneut PASS; Ergebnis byteidentisch zum STARTMASTER0065-Beleg.
- Link Policy 1.0.1: 19/19 erneut PASS; Ergebnis byteidentisch zum STARTMASTER0065-Beleg.
- PSERC 0.28.3 unverändert; Fresh PHP-Lint 40/40 PASS; Package Integrity PASS. Die hashgebundenen 0065-Gesamtbelege (41/41 Normal, 58/58 Terminal, 9/9 Package, One-Click, negative Drift-Gates) bleiben wegen byteidentischer PSERC-Quelle unverändert wiederverwendbar.

## Installer
`portal-seo-topic-engine_0.56.7_TERMINAL_READBACK_ROOTFIX.zip`
SHA-256: `f1e80717cb398573b5f6d229f75655689eb368e5dce2215d6c8432e746c27cb8`

## Sicherheitsgrenze
Kein Publish. Keine neue Recherche zur Reparatur nötig. Der bestehende 0.56.6-Orphan soll nach Installation von 0.56.7 beim Readback ausschließlich lokal terminalisiert werden.

`main` wird nicht verändert. Kein Merge.