# Pferdeatelier – ECHTE Gesamtdiagnose des fehlgeschlagenen WP-Tests ausgewertet (11.11.2026)

**Quelle:** Nutzerdatei `pste-gesamtdiagnose-2026-11-11.json` (284-KB-Originaldatei). Als Original-JSON gelesen. `contract=PSTE_STORED_DECISION_EVIDENCE_V3`, `pste_version=0.57.144.35`. Dieser Befund ersetzt Vermutungen und bloße Offline-PASS-Zahlen. **Kein Plugin freigegeben, kein WordPress-/K0-Schreibzugriff.**

## Harte tatsächliche Feststellungen
1. **Download hat funktioniert:** Der vollständige Report enthält `evidence_scan_complete=true`, `topics=5016`, `expected_total=5016`, `workflow_status`, `automatic_protocol`, `workflow_trace`, `workflow_history`. Der bisherige Download liest unnötig den gesamten Bestand (separater UI-KISS-BLOCKER), aber die Datei ist vollständig und lesbar.
2. **Genau bestätigter Stopp am 11.11.2026 10:36:27 UTC** (11:36:27 Uhr Deutschland): `WORKFLOW_ERROR / AJAX_BLOCKED` mit `action=pste_production_auto_step`, HTTP 400, `PSTE_EXISTING_ONLY_LOGIC_RECHECK_SOURCE_CHANGED_PROGRESS_PRESERVED`. Die vollständige gespeicherte Historie enthält **zwei** Vorkommen desselben Fehlers; das aktuell abgeschnittene Flugschreiberfenster enthält eines.
3. **Aktueller Produktionsstand:** `portal_baseline.status=CURRENT`, `portal_context.status=COMPLETE` 4488/4488, `existing_audit.status=COMPLETE` 5014/5014, `pserc_job.status=COMPLETE` mit 8 Kandidaten und 3 READY. Der sichtbare Fehler ist also **kein neuer DataForSEO-Providerfehler** (`no_provider_calls=true`) und kein K0-Schreibfehler.
4. **Historische Drift-Indizien:** Die Bestandprüfung zeigt `updated_at_utc=2026-11-03T17:41:54Z`, die gespeicherte WordPress-Baseline wurde am **09.11.2026** erfasst und der Redaktionsplan am **10.11.2026** kompiliert. Dies belegt verschiedene Altersstände der Prüf-/Planartefakte, **nicht** welches Hashfeld falsch ist.
5. **Historie ist umfangreich, aber nicht komplett auf der Einzelereignisebene:** 3182 erfasste Flugschreiber-Batches, 67942 Ereignisse, 0 ungültige Batches, 4 Fehlerarten; `workflow_trace.complete_historical_trace=false` (nur 35 letzte Batches/187 Einzelereignisse), `workflow_history.complete=true` für die aggregierten Zählungen. Die genaue vergleichende Audit-Hash-Tupel-Aufzeichnung wurde in .35 am STOP **nicht** mitgegeben.
6. `topics=5016` und `existing_audit.local_backlog_total=5014` bezeichnen **unterschiedliche Zählmengen**, keine aus dieser Differenz alleine ableitbare Datenbeschädigung.
7. Der **alte PSERC-Snapshot bleibt 3 READY** und ist kein Nachweis des neuen `BOUND_TYPE`-K0-Herkunftsbelegs. Keine neue Recherche nötig.

## Codefundstelle: exakt warum der bisherige Fehlercode unzureichend ist
In tatsächlich ausgelieferter PSTE .35:
`includes/class-pste-breadth-research-queue.php` → `beginLogicChangedLocalRevalidation` (um die Zeilen 779–825):
- Dieselbe Sammel-Exception `PSTE_EXISTING_ONLY_LOGIC_RECHECK_SOURCE_CHANGED_PROGRESS_PRESERVED` wird für **mehrere** Abweichungen verwendet: frühere Quittung vs. altes gespeichertes Checkpoint vs. aktuelle Baseline / Inventar / Struktur (Zeilen 791–794), **ODER** alter Backlog-Fingerprint vs. aktueller bei gleicher Zeilenzahl (Zeilen 815–817).
- Ohne drei echte Vergleichstupel aus der Datenbank ist **NICHT belegt**, welche dieser Alternativen zutrifft. Der Report enthält nur den Fehlercode und Schrittzahlen, keine genannten drei Tupel. Bitte nicht wieder ein einzelnes Feld behaupten.
- Der Eintrittspfad in `PSTE_Breadth_Research_Queue::start()` besitzt bereits einen separaten Recoveryweg `beginEvidenceRevalidation`, der Bestandsänderungen schützen soll. Ob er hier wegen veralteter Quittung/Checkpoint-Kombination nicht erreicht wird, muss an den Original-Belegen geprüft werden. **Nicht einfach Vergleichsschutz abschalten.**
- Eine spätere .36 QA-Protokollfassung fügt genau dieses Feldprotokoll hinzu, ist aber **NICHT** Quelle dieses .35-Exports; die historische Feldabweichung ist in der Datei nicht rückwirkend vorhanden.

## Konsequenz / harte Folgeabnahme
1. **Kein erneuter blind gestarteter 5014er Audit**, keine weiteren kleinen Plugin-Releases, kein K0-Eingriff, keine neue DataForSEO-Recherche.
2. Alte Quittung + altes Checkpoint + aktuelle Binding-/Backlog-Fingerprints im **isolierten QA** gegeneinander lesen (read-only), zeigen welches Feld tatsächlich abweicht; danach ein einziges sauberes Recoverykonzept im vorhandenen Workflow. Bestandsprüfung darf keine fremde Quelle als gültig fälschen. Keine unnötigen Wiederholungen.
3. Diagnose-Download zukünftig **sofort aus dem gespeicherten kompakten Fehler- und Flugschreiberstand**, detailreicher 5016er Scan nur freiwillig.
4. Gemeinsame KISS-Abnahme: realer Fehlernachweis, kein stilles Neusignieren, direkter Fehlerdownload ohne 126+ Datenbankseiten, kein Provider-Call, vollständig frischer 3-READY-PSERC-Nachweis und unveränderte K0-Ausgabe. Realer WordPress-Test bis dahin offen.

**Status:** `REAL_WP_FAIL_CONFIRMED`; `ERROR_HISTOGRAM_CONFIRMED`; `FIELD_COMPARISON_NOT_IN_V35_EXPORT`; `NO_RELEASE`; `K0_UNCHANGED`.
