# Pferde Atelier – ein gemeinsamer KISS-Fix für bestätigte WordPress-Fehler (11.11.2026)

**Status:** `LOCAL_QA_PASS` für **PSTE 0.57.144.37**, exakt ein koordiniertes Test-Plugin als Ersatz von PSTE .36 auf der **getrennten WordPress-Testseite**. **KEIN LIVE-GO, echter WordPress/MySQL-Test bleibt offen.** PSERC .65 und K0 werden **nicht** geändert.

## Echte Ursachen, nicht erfunden
Die tatsächlich vom Betreiber hochgeladene Datei `pste-workflow-flugschreiber-20261111-112222-utc.json` (PSTE .36, 1847 Ereignisse im letzten 150-Batches-Fenster) zeigt:
- 11.11.2026 11:22:18 UTC: `EXISTING_ONLY_AUDIT / PROOF_MISMATCH_BLOCKED`, `proof_field=BASELINE_SHA256`, historische Quittung und Checkpoint **übereinstimmend**, aktuelle Baseline **abweichend**; alter lokaler Pool 5014, aktueller 5013. Der Bericht beweist **nicht**, warum eine Zeile aus `manual_status=''` fiel – keine behauptete Löschung.
- Fehlercode `PSTE_EXISTING_ONLY_LOGIC_RECHECK_SOURCE_CHANGED_PROGRESS_PRESERVED`; ursprünglicher `startQueue` konnte nur unveränderten/gewachsenen Bestand in den sicheren Bestandsrecheck übergeben; die Verringerung blieb im Logic-Only-Fehlerpfad hängen.
- **WICHTIGE KORREKTUR DER VORHERIGEN ANALYSE:** Die dreimalige Meldung `DIRECT_SQL_WRITE / SQL_APPLIED`, `write_code=PSTE_LOCK_ATOMIC_RELEASE_FAILED`, `affected=1` bedeutet nach tatsächlicher `PSTE_DB_Write_Guard::query`-Codeprüfung **erfolgreichen DELETE** mit Fehlercode-Bezeichner als Sicherheitskennzeichen; dies ist **kein zweiter Laufzeitfehler**. Die zuvor behauptete defekte Sperrenfreigabe ist nicht belegt. **Sperren-Code unverändert lassen.**

Weiterer nachgewiesener UX-Fehler in PSTE .36: Die Schaltfläche „Gesamtdiagnose herunterladen“ startet das JavaScript `scanTopics()` mit etwa 126 Einzelbatch-AJAX-Abfragen über 5016 Themen, obwohl bereits `PSTE_Flight_Recorder::report(150)` und ein geschützter `admin-post`-Download existieren.

## Genau 3 veränderte Dateien (aus gesamtem 121-Dateien-Paket)
1. **Wiederanlauf:** `includes/class-pste-breadth-research-queue.php` erkennt **verkleinerten aktuellen Bestand** nach Prüfung des signierten historischen QUEUE/RECEIPT-Paares. Startet ausdrücklich eine **neue lokale, bereits vorhandene 40-Zeilen-Prüfung ab Cursor 0**, ohne neuen Anbieteraufruf. Alter abgeschlossener Queue- und Auditnachweis bleiben im Vorgängerzustand und alten Receipt erhalten, bis der neue Audit wirklich vollständig abgeschlossen wurde. Kein stiller Wertetransfer vom alten 5014-Checkpoint.
2. **Fortsetzen nach Pause und Abbruch:** Dieselbe Datei unterscheidet den **beabsichtigten** Nullanfang des verkleinerten Bestands von einer irrtümlichen alten Null-Duplikat-Queue; inmitten des neuen Laufs geht der echte neue Cursor nicht verloren. Zweiter Start während RUNNING BLOCKED; wiederholter Start nach COMPLETE löst **0 neue Themenbatches** aus.
3. **Sichere Freigabe:** Vor dem neuen vollständigen Nachweis müssen gelesene Zahl mit zu Beginn festgehaltener Gesamtzahl und aktuell gespeicherter Zahl übereinstimmen; Kontextfelder `baseline/inventory/structure/editorial_plan` dürfen während des Laufs nicht abdriften. Sonst PAUSED_ERROR, **alte Quittung erhalten**. Laufende 40-Zeilen-Logik, Fach-/Entscheidungslogik und Signierung unverändert.
4. **Fehlerprotokoll:** Der existierende Flugschreiber meldet den gezielten neuen Start einmalig mit alten/neuen Zählern und Kennzeichen `OLD_SIGNED_PREDECESSOR=PRESERVED` (kein zweiter Logger, keine neue Tabelle).
5. **Download:** `includes/class-pste-admin.php`: der Standardknopf lädt **den bereits vorhandenen gespeicherten Flugschreiber direkt über `pste_export_flight_protocol`**. Keine `pste_evidence_read_batch`-Anforderung über diesen Knopf; der alte große Themen-Vollbericht bleibt **nur freiwillig in einem zugeklappten Bereich mit deutlicher Warnung**.
6. **Versionsdatei:** `portal-seo-topic-engine.php` nur 0.57.144.36 → 0.57.144.37. **14 von 14 fachlichen SEO-Regeldateien byteidentisch** mit .36, deshalb selbst kein neuer Regel-Hash-/SEO-Neuaudit allein durch das Update.

## Testergebnis – TATSÄCHLICH ausgeführt auf exakt wieder entpackter finaler ZIP
- **Original-PHP-Klasse** `PSTE_Breadth_Research_Queue` mit realen originalsignierten PRE_TYPE-Profilen der drei alten WordPress-Artikel, sonst **simuliertem WP-Optionsspeicher und simulierten Themenzeilen**:
  - 5014 → **5013**, exakt 126 Batches zu 40, COMPLETE, neuer gültiger Nachweis, alte signierte Queue preserved, 0 Anbieteraufrufe.
  - 5014 → 5014 bei Kontextdrift, 126 lokale Batches, COMPLETE.
  - 5014 → 4014, 101 Batches, COMPLETE.
  - Zwischenstopp bei 40/5013, sichere Wiederaufnahme und absichtlicher Abbruch/Fortsetzung **ohne Cursor-Rücksprung**.
  - Zweiter Klick nach COMPLETE: **0 zusätzliche Themenbatches**; doppelter Start während RUNNING blockiert.
  - Schadhafter alter Checkpoint blockiert vor Änderung; beschädigte alte Receipt wird **nicht als gültig wiederverwendet**, sondern nur nach erneutem lokalem Durchlauf ersetzt.
  - Zwischenzeitlich sinkende Zeilenzahl oder driftender Baseline-Wert beim Prüfen: **kein neuer Receipt**, sicherer Stopp.
  - Nach ersten 40/5013: kein vorzeitig freigegebener neuer Nachweis.
- Direkter echter `PSTE_Admin::renderEvidenceAuditControl()`-PHP-Aufruf in WP-Attrappe: **10 UI-Prüfungen PASS**, Nonce + Admin-POST + fast form, große Diagnose nur nach explizitem Klick. Kein neuer AJAX-Leseweg für den primären Knopf.
- Finale ZIP **selbst neu entpackt**, 121/121 Archivdateien CRC/Inhalts-Hash PASS; **83/83 PHP-Syntax PASS**, exakt **3 geänderte Dateien**, 118 unverändert, WordPress-Pluginordner unverändert. **ZIP SHA256: `0a29c46837a1879b9a66bf26ae48f8fd8d0a86ed8be22c7d2919a38a49d5e881`**; 651602 Bytes.

## Wichtige Grenze – weder verharmlosen noch blinden Restart
**Vorherige synthetische PASS-Zahlen sind kein Ersatz für den realen WordPress-Test.** Die 5013-Zeilen-WP/MySQL-Datenbank wurde nicht hier ausgeführt. Der aktuelle WordPress-Inhalt kann nach einer echten Quellenänderung **einmal den vollen lokalen Bestandsdurchlauf von 5013 Datensätzen verlangen**; das ist für einen neuen vollständigen Prüfbeleg nötig, keine neue kostenpflichtige Recherche. Er wird in 40er-Schritten mit sicheren Zwischenständen fortgesetzt, nicht bei jedem Download oder erneuten Klick von vorne gestartet. K0 bleibt inaktiv; vorhandenes PSERC .65 bleibt unverändert.

**Permanente Library `/pferdeatelier/PLUGINS/QA/`:**
- `PSTE-0.57.144.37-KISS-GESAMTKORREKTUR-NUR-WORDPRESS-TEST.zip`
- `PSTE-0.57.144.37-KISS-GESAMTKORREKTUR-QUELLPATCH.patch`
- `PSTE-0.57.144.37-KISS-GESAMTKORREKTUR-PAKETPRUEFUNG.json`
- `PSTE-0.57.144.37-KISS-GESAMTKORREKTUR-REPLAY.json`

**Status:** `COMBINED_ROOT_FIX_OFFLINE_PASS`, `WP_TEST_REMAINS_OPEN`, `NO_LIVE_RELEASE`, `NO_NEW_DFSEO`, `NO_K0_MODIFICATION`. Keine weiteren Mini-Releases.
