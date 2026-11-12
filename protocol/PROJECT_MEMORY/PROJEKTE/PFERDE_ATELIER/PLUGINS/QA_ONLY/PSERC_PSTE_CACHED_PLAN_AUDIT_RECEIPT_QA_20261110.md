> **NEUERER QA-STAND (10.11.2026):** Diese frühe Prüfung ist überholt: A/B lieferte generische Artikeltyp-Absicht statt ursprünglicher SEO-Suchabsicht; die ursprüngliche Audit-Reparatur validierte nur das Nachweisformat. Der korrigierte, dreifach wiederholte Gesamttest (**5.562/5.562 PASS**) samt hartem QA-Quellpatch liegt in [PSTE_PSERC_GESAMTQA_ECHTQUELLEN_INTENT_WIEDERANLAUF_20261110.md](PSTE_PSERC_GESAMTQA_ECHTQUELLEN_INTENT_WIEDERANLAUF_20261110.md). **Keine Plugin-Installation oder Livefreigabe aus diesem historischen Protokoll ableiten.**

# PSERC/PSTE – echter alter Redaktionsplan wird trotz neuem PSTE-Urteil wiederverwendet (QA 10.11.2026)

**Status: QA-Quellfix und lokale Wiederholungstests. NICHT installierbar, keine WordPress- oder K0-Liveänderungen. Kein neuer Plugin-Release.**

## 1. Exakte Quellen
- Echt heruntergeladener neuester Nutzerexport `seo-redaktionsplan-ohne-suchintent-nachweis-... (2).json` 90.640 Bytes, Datei-SHA256 `29638fef9606925b5b6f322fcde695581999ec0c41bd111bca0bcb655fbf1220`, identisch mit (1). Gespeichert vom alten `compiler_version=0.28.61` am `2026-11-10T15:47:48+00:00`, damalige PSTE-Quellversion `0.57.144.32`.
- Drei reale READY-Artikel, alle drei mit `intent_profile.phase=PRE_TYPE` ohne finales `search_intent`. **Keine reale K0-Quellenfreigabe.**
- Original PSERC `0.28.63` und PSTE `0.57.144.33`/QA `0.57.144.34` aus den physisch gelesenen Plugin-ZIPs. GitHub K0 QA-Quellenbindungsprüfung nur lokal nachgestellt.

## 2. Warum die alten 963 Tests nicht genügt haben
Die bisherige PSTE-Quellcodekorrektur erzeugt lokal bei allen drei Themen `BOUND_TYPE`. Ihr Wiederholungs-/Negativtest prüfte **nicht** die gespeicherte WordPress-/PSERC-Plan-Wiederverwendung. Das reale WordPress-Dateiergebnis ist daher weiterhin derselbe alte Plan.

Wichtige Präzisierung zum bisherigen Verdacht: Der `PSTE_Breadth_Research_Queue::backlogAuditLogicHash` ist zwischen `PSTE .33` und `.34` unterschiedlich (Original-Funktionsaufruf, kein geratenes Versionsfeld):
- .33: `3223323e4c7d85f8b1cfb99fd8937db5df5867e9f3069c5dd474d5ea26a82d57`
- .34: `7ded9639ab7ff765318969d5d939db53697fec3c6e1454e236399038e43f45c7`
Deshalb ist **nicht bewiesen**, dass die PSTE-Bestandsprüfung selbst das lokale Neuberechnen überspringen MUSS. Eine korrekte alte Audit-Quittung müsste bei geänderter Normalweglogik veralten. Der tatsächliche Stand dieses WordPress-Audits ist ohne privaten Datenbank-Readback unbekannt.

**Separater, hart nachgestellter PSERC-Fehler:** `PSERC_Plan_Dependency_Fingerprint::current()` stützte die gespeicherten Themen-Daten ausschließlich auf `MAX(id)` der PSTE-Tabellen + Kontext/Capabilities. Änderungen **bereits bestehender** `payload_json`-Zeilen verändern `MAX(id)` nicht. Auch nach lokal erfolgreicher Neubewertung kann `PSERC_Plan_Compile_Job::start()` deswegen denselben alten 3-READY-Snapshot als `COMPLETE` wiederverwenden.

## 3. Kleiner isolierter Quellfix – kein neuer Prüf-/Workerweg
Im vorhandenen `PSERC_Plan_Dependency_Fingerprint::current()` zusätzlich **eine** bestehende Option lesen: die von PSTE gespeicherte `PSTE_RETAINED_BACKLOG_AUDIT_RECEIPT_V1`-Quittung. Nur deren bereits berechnete signierte SHA256 als zusätzliche Eigenschaft des vorhandenen Topic-Fingerprints führen. Bei absichtlich nicht vorhandenem Audit den Sentinel `NOT_AVAILABLE`; defekte Form/Hashfeld => sicherer Stopp. Keine erneute SEO-Entscheidung, keine neue DB-Tabelle, keine zusätzliche Frontend-DB-Abfrage, kein weiterer Worker und kein DataForSEO-Call. **Die gültige Auditevidenz entscheidet weiterhin ausschließlich `PSTE_Breadth_Research_Queue::existingOnlyAuditCurrent()`; PSERC liest nur ihre Identität.**

Lokale Quellkopie: `/mnt/data/psqa/cache_replay_qa/class-pserc-plan-dependency-fingerprint.php`; Diff: `audit_receipt_binding.patch` (SHA256 `49f0a26d143ef9827a30e8e106f667ad4216152a4b161fb856573dcdea63fdc2`).

## 4. Tatsächlich durchgelaufene Regression
- **Originaler, unveränderter PSERC-Compiler + unverändertes Original-Fingerprint:** 16/16 erwartete lokale Prüfungen PASS. In der Nachstellung gleiche Topic-Tabellen-IDs, geänderte fertiggestellte PSTE-Audit-Quittung: Alter Snapshot wird **fälschlich** wiederverwendet; 0 neue Compilerjobs.
- **Original PSERC-Compiler + isoliert korrigierter Fingerprint:** **526/526 lokale Positiv-/Negativprüfungen PASS**. Bei neuer gültiger PSTE-Auditquittung und unveränderten `MAX(id)` erkennt er den alten Plan als veraltet und legt korrekt einen neuen Compilerjob an. 250 wiederholte alte/neue Quittungen, 250 Determinismusproben, 5 ungültige Auditoptionen BLOCK, fehlende Quittung markiert, identischer Stand bleibt idempotent. PHP-Syntax PASS.
- Vorhandene 3-Artikel-Kette erneut ausgeführt: **60/60 direkte PSTE-Intent-/PSERC-Manifestschecks**, **330/330 PSTE-Normalweg-/Negativtests**, **573/573 K0-Quellbindungs-/Manipulationsprüfungen** PASS. Insgesamt 963+526 zusätzliche zielgerichtete Checks, **0 Fehler**. Der Originalfehler ist ausdrücklich im Test als erwartetes Fehlverhalten dargestellt, nicht als erfolgreich behobene Livefunktion.
- Der 3er-Original-Batch und alle 3 gespeicherten Titel/Keywords/Kategorien/Planplätze bleiben unverändert. Ursprüngliche unbewiesene `PRE_TYPE`-Profile sind weiter **nicht freigegeben**.

## 5. Freigabegrenze
- Der Test nutzt echten Benutzerexport und Original-PHP, **aber synthetische WordPress-Optionen/Datenbank-Watermarks, teilweise synthetische Kategorie-/SEO-Freigaben**. Hier ist kein WordPress/MySQL-Server verfügbar. **Keine echte WordPress-Installation/DB-Lesung und kein frisch geschriebener K0-Artikel.**
- Keine neue ZIP/versionierte Installation aus diesen Tests erzeugt. Alte K0-Autor-Kontexte mit widersprechender Suchintention bleiben absichtlich BLOCKED, nicht still überschrieben.
- Der lokale Fix behebt die nachgestellte **PSERC-Cache-Invaliderungslücke**; die reale PSTE-Ausführung und korrekte Speicherung der `BOUND_TYPE`-Profile auf WordPress ist **noch unbewiesen**.
- Vor irgendeiner neuen Installation: gesamtes Paket mit bestehenden Release-Hashes neu versiegeln, echte WP-TEST-Bestandsverarbeitung/Quittung/PSERC-Neulauf und Ausgabe `mit-suchintent-nachweis` nachweisen. Keine erneute kostenpflichtige Keyword-Recherche, keine manuellen K0-Entscheidungen.

**Aktueller Zustand: `LOCAL_CACHED_PLAN_ROOTFIX_PASS`, `FULL_LOCAL_TESTS_PASS_FOR_TESTED_SURFACES`, `REAL_WP_EXPORT_STILL_OLD`, `NO_RELEASE`.**
