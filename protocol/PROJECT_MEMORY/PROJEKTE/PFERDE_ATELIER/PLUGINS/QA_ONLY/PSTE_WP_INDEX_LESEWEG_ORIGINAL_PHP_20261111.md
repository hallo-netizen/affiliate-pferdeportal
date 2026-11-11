# Pferdeatelier – WordPress-Kontext-Leseweg gegen echten PSTE-Quellcode geprüft (11.11.2026)

**Prüfurteil:** `LOCAL_INDEX_READ_ONLY_PASS`, 381/381 gezielte PHP-Prüfungen bestanden; **NICHT** `REAL_WP_MYSQL_E2E_PASS`. Kein neues Plugin, kein DataForSEO-Aufruf, kein K0-Eingriff.

## Quellen und genaues Datum

Die echte archivierte WordPress-Projektdatei `pste-plan-kategorien-pruefstand-2026-11-09.json` ist **vorhanden und per Files lesbar** (11.925.212 Bytes, generiert 2026-11-09 12:22:45 UTC von PSTE 0.57.144.27). Sie enthält u. a. die echte Baseline `PSTE_SITE_BASELINE_V1` mit 1.176 Kategorien, einen abgeschlossenen `PSTE_CONTEXT_REFRESH_JOB_V9_EQUIVALENT_STRUCTURE_RESUME` für 4.488 Einheiten und das historische Index-/Planmanifest. Diese Datei ist nicht der aktuelle MySQL-Pool vom 11.11.2026.

Der reale spätere PSERC-Dreierexport vom 10.11.2026 ist ebenfalls vorhanden, Original-90.640 Bytes, enthält 3 x `PRE_TYPE`. Der bisher gemeldete erneute Export identisch zum Vor-Export ist ein echter negativer Abnahmebeleg.

## Was diesmal ECHT getestet wurde

Aus dem tatsächlichen lokal entpackten PSTE-0.57.144.35-QA-Paket wird die **ungeänderte Originalklasse `PSTE_Context_Index_Store::runtimeBinding`** direkt über PHP aufgerufen. Die 11.9-MB-Bestandsdatei konnte nicht als Originalbyte-Datei in die Ausführungsumgebung übernommen werden; die WP-Optionen und das Manifest sind deshalb **ausdrücklich lokal simuliert** (mit Original-Hashwerten aus dem datierten WP-Kontextexport). Es wird kein Live-WP-Kontakt vorgetäuscht.

- **120-mal** Original-Lesemethode bei gültig signiertem Testmanifest aufgerufen: kontraktgenau, identischer Fingerabdruck, **0 Schreibzugriffe**.
- **10 negative Fälle**: fehlendes, hashmanipuliertes, widersprechendes oder inkonsistentes Manifest, divergierender Plan-, Inventar-, Kontext- oder Strukturbezug, falscher Vertrag. Alle korrekt **BLOCKED**, **0 Schreibzugriffe**.
- Gesamtsumme **381/381 Checks PASS**, 0 Aufrufe der WP-Schreibfunktionen im Test.
- Die vorhandenen vollständigen QA-Archive PSTE .35 (121 Dateien) und PSERC .65 (63 Dateien) wurden erneut auf ZIP-CRC geprüft, beide PASS; Versions-/Datei-SHA von GitHub-Vorprotokollen unverändert.
- Test verwendet realen Quellcode, aber **simulierte Optionen**, nicht die echte WP-Datenbank.

## Warum diese Prüfung sinnvoll war

Eine frühere Analyse vom 09.11. hatte darauf hingewiesen, dass der technische Kontextleser bei fehlendem Index ungefragt WordPress-Optionsdaten neu aufbauen kann. Im **jetzigen PSTE .35 Quellcode** ist `runtimeBinding()` ausdrücklich nur noch ein Leser: Er ruft `loadManifest()`, **nicht** den mutierenden `rehydrateCompletedRuntimeIndex()` auf. Der separate Wiederaufbau `rebuildCompletedRuntimeIndexForExplicitOwner()` ist nur für den freigegebenen zuständigen Bearbeitungsweg vorgesehen.

Der neue reale PHP-Test bestätigt diese Trennung für die 120+10 getesteten Zustände. Eine pauschale Aussage „WordPress wurde vollständig durchgetestet“ wäre weiterhin falsch.

## Dokumentierte Original-Testbelege

- [Wiederholbarer PHP-Test](PSTE_KONTEXT_LESEWEG_ORIGINAL_PHP_QA_20261111.php), SHA256 `d344fbc5eb5191721f82c648219ecbe6d41750a0e3d822b4717d65e236fcbc91`.
- [Ergebnis-JSON](PSTE_KONTEXT_LESEWEG_ORIGINAL_PHP_QA_ERGEBNIS_20261111.json), SHA256 `3619d24dc837abff7536cdbf2505b5b67a9325b09d5b2033c159639527c021f5`.

## Noch offene letzte echte Abnahme

Nur ein WordPress-/MySQL-TEST mit der aktuellen Datenbank kann nachweisen, dass die gespeicherten PSTE-`topic_pool`-Zeilen die Original-SEO-Profile dauerhaft enthalten, die vorhandene Bestandsprüfung nach einer Regeländerung wirklich ausgeführt wurde, die neue signierte Auditquittung akzeptiert wird und PSERC anschließend ein **neues** Manifest mit `BOUND_TYPE` statt unverändertem altem `PRE_TYPE` exportiert.

**Keine Live-Freigabe, kein automatischer K0-Lauf, kein weiteres Blind-Plugin und keine neue DataForSEO-Recherche.** Das verifizierte Archiv aus Nov9 und das spätere 3er-Manifest reichen für einen Offline-Quell-/Kontexttest, sind aber kein aktueller Live-DB-Nachweis.
