> **KORREKTUR DER AUSWERTUNG (11.11.2026):** Die drei Einträge `DIRECT_SQL_WRITE / SQL_APPLIED`, `affected=1`, `write_code=PSTE_LOCK_ATOMIC_RELEASE_FAILED` zeigen laut Originalcode eine **erfolgreich angewendete SQL-Löschung**. Das Wort `FAILED` ist dort der nur im Fehlerfall geworfene Schutzcode, der auch bei erfolgreichem SQL zur Protokollkategorisierung übergeben wird. **Ein zweiter Fehler der Sperrenfreigabe ist nicht nachgewiesen und wird NICHT repariert.** Maßgeblich ist die [gemeinsame KISS-Abnahme .37](PSTE_05714437_KISS_GEMEINSAMER_FIX_ABNAHME_20261111.md).

# Pferdeatelier – tatsächlicher Flugschreiber .36: exakte Sperre und fehlender Wiederanlauf (11.11.2026)

**Echter Nachweis, kein Simulations-PASS und kein neues Plugin.** Quelle: unmittelbar vom Benutzer hochgeladene Datei `pste-workflow-flugschreiber-20261111-112222-utc.json`, SHA256 `0e3362023902579e89a35cddef54f6e733e2badc189032e9bc0405133fd6cbb3`; im lokalen Container als Original-JSON dekodiert. `contract=PSTE_FLIGHT_REPORT_V2`, `pste_version=0.57.144.36`, `generated_at_utc=2026-11-11T11:22:22+00:00`. 150 gespeicherte Batches, 1847 Einzelereignisse, `complete_historical_trace=false`; keine Behauptung über ältere, im gekürzten Flugschreiber nicht vorhandene Detailereignisse.

## Harter Befund aus echtem WordPress-Protokoll

- 3 wirkliche Ajax-Stopps mit genau gleichem Fehler `PSTE_EXISTING_ONLY_LOGIC_RECHECK_SOURCE_CHANGED_PROGRESS_PRESERVED` am 11.11.2026 **10:36:27, 11:15:18 und 11:22:18 UTC** (Deutschland +1 Stunde). HTTP 400 bei `pste_production_auto_step`.
- Neu durch .36 zuverlässig aufgezeichnetes **entscheidendes** Ereignis `EXISTING_ONLY_AUDIT / PROOF_MISMATCH_BLOCKED` am 11:22:18 UTC:
  - `proof_field=BASELINE_SHA256`.
  - `receipt_proof_sha256=41840fd1b35afee99cf7994e8b0f5ddb76532895fcdc9f99f4c90333503a8323`.
  - `checkpoint_proof_sha256=41840fd1b35afee99cf7994e8b0f5ddb76532895fcdc9f99f4c90333503a8323`. **Historischer Quittungs-/Checkpoint-Wert stimmt überein.**
  - `current_proof_sha256=ab1f9748848cb6d3f6cc83d1ba25c85772bffd6be75c03b051820e54e987c2b5`. **Aktueller Baseline-Wert unterscheidet sich tatsächlich.**
  - `previous_rows=5014`, `current_rows=5013`. Die Zählung erfasst gespeicherte automatische Bestandszeilen mit `manual_status=''` in `PSTE_Repository::retainedBacklogFingerprint()`; sie ist **nicht** die Gesamtzahl 5016. Der Rückgang um 1 beweist alleine weder eine Löschung noch welche Zeile verändert wurde (manuelle Markierung kann die Abfragezahl ebenso ändern).
  - `effect=NO_REENTRY_STARTED_PREVIOUS_PROGRESS_PRESERVED`, `provider_calls_by_diagnostic=0`.
- Der Flugschreiber enthält außerdem **dreimal** `DIRECT_SQL_WRITE / SQL_APPLIED`, `write_code=PSTE_LOCK_ATOMIC_RELEASE_FAILED`, `affected=1`, `transaction_commit_not_verified=true` – **separates Problem** der internen Start-Lock-Freigabe; nicht mit der primären Baseline-Sperre gleichsetzen.
- `stored_current_state.last_automatic_block` bestätigt: Bestandsprüfung alt `COMPLETE 5014/5014`, Kontext `COMPLETE`, Compiler `COMPLETE`; aktueller Start geblockt, keine Bestands-Queue-Mutation. `topic_total=5016` ist eine **andere Gesamtzählmenge**.
- Der Original-Flugschreiber .36 **hat den genauen Fehler endlich gespeichert**. Ältere .35-Gesamtdiagnose konnte ihn nicht liefern; diese .36-Datei ist verbindlicher neuer Sachstand.

## Aus ausgelieferter Quellfunktion nachgewiesener Wiederanlauf-Bug

Original `includes/class-pste-breadth-research-queue.php` (aus `PSTE .36`):
1. In `start()` wird der alternative sichere Bestands-Recheck bei geändertem Quellnachweis nur für `$newRowCount >= $oldRowCount` betreten; hier **5013 < 5014**, also nicht.
2. Daraufhin wird `beginLogicChangedLocalRevalidation()` versucht. Diese Route verlangt identische Baseline und wirft für den nun nachgewiesenen abweichenden Wert die beobachtete `PSTE_EXISTING_ONLY_LOGIC_RECHECK_SOURCE_CHANGED_PROGRESS_PRESERVED`-Exception.
3. Der bisherige `beginEvidenceRevalidation()`-Fallback würde hier ebenfalls wegen `$total<$oldProcessed` abbrechen. Die Software hat also **keinen abgesicherten Wiederanlauf für einen kleiner gewordenen automatischen Bestandsbereich**.
4. Es wäre gefährlich, die Hashsperre oder den Zählervergleich einfach auszuschalten oder den alten Stand still als gültig neu zu signieren. Der exakte geänderte Artikel bzw. Grund des Baseline-Wechsels ist mit diesem kompakten Export **noch nicht identifiziert**.

## Verbindlicher gemeinsamer Folgefix (NICHT als neues Mini-Plugin)

- Bestehenden geprüften Vorgängerstatus/alte Quittung unverändert erhalten. Gegen die aktuelle WordPress-TEST-Datenbank **nur lesend** feststellen, warum der automatische Bereich um 1 kleiner wurde und wodurch sich die Baseline geändert hat; Vergleich darf **ohne** gewaltsame Wiederherstellung/Neu-Signatur erfolgen.
- Den **bestehenden** lokalen Audit-/Recheck-Worker so erweitern, dass eine **nachgewiesen** erlaubte verringerte Themenmenge kontrolliert behandelt werden kann, mit gegen aktuelle Themen neu geprüfter kompletter Belegkette und erst danach neuem PSERC-Manifest; ein verschwundener oder manuell übernommener Themenstand darf nicht einfach übernommen werden.
- Start-Lock-Freigabe `PSTE_LOCK_ATOMIC_RELEASE_FAILED` als **separaten** Fehler in derselben Abnahme untersuchen, nicht übergehen.
- **Direkter 1-Klick-Stoppbericht** aus bereits gespeicherten Daten, ohne die 5016 Themen in 126+ Ajax-Batches abzuscannen. Detailvollscan nur optional, nie als Pflicht.
- **Echte Positiv- UND Negativtests** speziell 5014→5013, unveränderte 5014, wachsende Menge, veränderte Baseline, veränderte einzelne alte Themen, defekte Signatur, manuelle Markierung, doppelte Klicks/Lock-Fehler/Reload; **kein DataForSEO, kein K0-Umbau, keine Live-Installation und keine Plugin-Freigabe vor dieser gemeinsamen Abnahme**.

**Stand: `REAL_BASELINE_PROOF_MISMATCH_CONFIRMED`, `MISSING_DECREASED_BACKLOG_RECOVERY_CONFIRMED_IN_SOURCE`, `SECONDARY_LOCK_RELEASE_ANOMALY`, `NO_RELEASE`, `K0_UNTOUCHED`.**
