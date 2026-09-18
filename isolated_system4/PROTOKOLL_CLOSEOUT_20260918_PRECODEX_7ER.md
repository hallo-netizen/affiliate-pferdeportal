# PROTOKOLL — SYSTEM 4 PRE-CODEX 7ER CLOSEOUT — 2026-09-18

Status: historischer WAS/WARUM-/Testnachweis. Keine CURRENT-Autorität. Operative Wahrheit ausschließlich `control/startmaster0107/CURRENT_STATE.json`.

## Tatsächlich erledigt

- Aktueller kanonischer Main frisch geprüft: `508f9dbb3650c99e5d41dbab83086af46945e225`.
- START_HERE routet auf `control/startmaster0107/CURRENT_STATE.json`.
- Verbindlicher Zielvertrag frisch geprüft: `isolated_system4/ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_CODEX_WRITER_20260914.md`; Ziel unverändert.
- Vollständige vorhandene System-4-Simulationsstrecke auf exakt diesem Main ausgeführt: GitHub Actions Run `35352311907` = SUCCESS.
- Darin vollständig PASS:
  - 1 Artikel bis V2-Enddatei;
  - 3 Artikel bis V2-Enddatei;
  - positive und negative Point-0-/Root-/Research-/Facts-/Context-/Draft-/LT-/PPM-/Repair-/Batch-/Handoff-Prüfungen;
  - absichtlich reparierbarer Fehler im Mehrartikel-Lauf wurde erkannt, zum richtigen Owner zurückgegeben, repariert und erneut erfolgreich geprüft;
  - historische Exact-/Visible-Body-Wiederverwendung blockiert;
  - Codex im Test ausdrücklich nicht verwendet.
- Frische-/NEW-Schutz auf aktuellem Main vorhanden und im Run `35352311907` grün.
- Alte Recovery-Artikel desselben 7er-Batches wurden vor Codex identifiziert und ausdrücklich als Produktionsquelle ausgeschlossen.
- Bestehender dauerhafter Endstempel-Release für denselben Batch wurde vor Codex identifiziert:
  - Batch: `7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a`
  - Release-Tag: `endstempel-7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a`
  - Asset: `GEN1_7_ARTIKEL_PSERC_APPROVED_PRODUCTION_PACKAGE_107008_FINAL.json`.
- Die vorhandenen Release-Gates blockieren byteverschiedene Wiederverwendung desselben Zielpfads bzw. Release-Replay ausdrücklich.
- Kein neuer realer Codex-Lauf wurde nach diesem Preflight gestartet.

## Warum der Codex-Start gestoppt blieb

Der aktuelle 7er-Batch besitzt bereits dieselbe historische Batch-/Release-Identität. Ein neuer NEW-Lauf mit neuen Textbytes würde deshalb später in die vorhandenen Kollisions-/Replay-Sperren laufen.

Zusätzlich gilt unverändert die harte Abschlussbedingung: Der Lauf ist erst vollständig abgeschlossen, wenn die finale signierte und WordPress-formatgeprüfte Importdatei dauerhaft abrufbar ist und als identische Datei im Parent-Chat ausgegeben werden kann. Ein `/tmp`-, Codex-Sandbox-, Log-, Proof- oder bloßer Artifact-Verweis genügt nicht.

## Zielvertrag

Unverändert. Keine Text-, SEO-, Design-, PPM-, PSERC-, WordPress- oder Publish-Regel wurde geändert oder gelockert.

## Current-/Eine-Wahrheit-Korrektur

`control/startmaster0107/CURRENT_STATE.json` wurde auf den tatsächlichen neuen Blocker nachgezogen.

`isolated_system4/README.md` wurde ausdrücklich als reine Architekturübersicht gekennzeichnet und verweist für operativen Status/NEXT ACTION auf die eine Current-Autorität. Damit ist die frühere mögliche zweite Statuswahrheit entfernt.

`control/startmaster0107/PFERDE_ATELIER_START_HERE.json` wurde nur auf den neuen SHA der Current-Autorität rebunden; die Bürotür bleibt Navigation.

## Aktueller erster Blocker

`CURRENT_7ER_BATCH_ALREADY_HAS_DURABLE_RELEASE_IDENTITY_COLLISION`

## Genau eine NEXT ACTION

Vor irgendeinem Codex-Start muss im bestehenden System-4-/STARTMASTER0107-Weg der frische 7er-Lauf eine nicht kollidierende Run-/Output-Identität erhalten, ohne die sieben gebundenen Themen aufzuteilen, ohne Artikelmetadaten/Slots/Regeln zu ändern und ohne alte Recovery-Texte als Produktionsquelle zu verwenden. Danach müssen Point-0/Head/Hashes sowie die dauerhafte finale Chat-Datei-Ausgabe positiv und negativ belegt sein. Erst dann darf der echte 7er-Batch mit Codex starten.

## Nicht anfassen

- keine Herauslösung eines einzelnen echten Artikels als eigener Produktionsbatch;
- keine alte Recovery-Datei als Schreibquelle;
- keine manuelle Batch-Hash-Manipulation;
- keine neue Parallelroute/Architektur;
- keine Regeländerung an Textmaschine, Design, LT, PPM, PSERC oder WordPress;
- kein Auto-Publish.
