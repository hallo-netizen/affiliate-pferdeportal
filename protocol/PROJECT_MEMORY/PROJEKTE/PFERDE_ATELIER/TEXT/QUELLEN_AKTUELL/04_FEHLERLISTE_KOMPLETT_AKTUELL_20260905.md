# STARTMASTER0107 – KOMPLETTE AKTUELLE FEHLERLISTE – 05.09.2026

## A. M01–M33 – bestehende historische Regressionen

| ID | Fehlerklasse | Teststatus | Live-Status / Bemerkung |
|---|---|---|---|
| M01 | State-/Bundle-Hash chain | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M02 | Unique article files / keine ARTICLE.md-Kollision | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M03 | PREPARED Persist/Restore | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M04 | Finalize CLI real aufrufbar | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M05 | Durable Release/Receipt | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M06 | No fake production contract | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M07 | Recovery not automatically final | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M08 | PPM 6.7.9 Original-ZIP vorhanden | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M09 | PSERC-FIX Original-ZIP vorhanden | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M10 | Preflight fail-closed | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M11 | Real PPM call | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M12 | Fake PPM blocked | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M13 | PPM content_hash == final article SHA | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M14 | Current Action Handoff | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M15 | 107007 Handoff instruction konsistent | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M16 | Signer boundary außerhalb Codex | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M17 | 107008 fail-closed | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M18 | ENDSTEMPEL constants | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M19 | Merge trigger | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M20 | Delivery 7 Artikel + Envelope + Manifest | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M21 | No auto-publish | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M22 | Signed production package / H8 | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M23 | Preproduction/Runtime Guards | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M24 | No H8 rollback | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M25 | Article prompt / Fachworkflow boundary | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M26 | Bound Fachworkflow production context | im bestehenden Runner enthalten | früher mehrfach LIVE BLOCKED; auf aktuellem main im letzten Lauf überwunden |
| M27 | Current-main / production environment identity | im bestehenden Runner enthalten | Preflight/HEAD im letzten Lauf PASS |
| M28 | Fachworkflow-Handoff request executable | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M29 | Release metadata current-batch identity | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M30 | Final context batch identity | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M31 | Codex-native bound action / kein separater Executor | im bestehenden Runner enthalten | durch PR #136 explizit gebunden; letzter Lauf kam darüber hinaus |
| M32 | PPM runtime package path ohne Env-Abhängigkeit | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M33 | GitHub ENDSTEMPEL ohne Codex git auth | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |

## B. Reale Blocker / Wiederholungsfehler außerhalb bzw. quer zur Matrix

### B01 – WordPress-Kategorie-Identität
- Bereits am 28.08. als Wiederholungsfehler dokumentiert.
- Historisch: Name/Slug/Taxonomy müssen korrekt zur gebundenen Kategorie passen.
- Aktuell erster Live-Blocker: `BOUND_WORDPRESS_CATEGORY_ID_MISSING_FOR_REAL_PPM679_EXECUTION`.
- **Harte Nutzerregel:** Nicht durch Erweiterung des SEO-5-Felder-Handoffs lösen.

### B02 – `BOUND_CURRENT_FACHWORKFLOW_EXECUTION_CONTEXT_MISSING`
- 04./05.09 mehrfach erster realer Blocker vor Artikel 1.
- Ursache im aktuellen Vertrag: Codex-Worker-Rolle nicht hart genug als Fachworkflow-Ausführung gebunden.
- PR #136 bindet Current Codex als Fachworkflow-Worker.
- Letzter Live-Lauf auf `c8a96e7…` kam über diesen Blocker hinaus → derzeit **live überwunden**.

### B03 – PPM-/PASS-Reihenfolge / Kreisschluss
- Nach Einführung echten PPM 6.7.9 wurde zeitweise ein bereits vollständiger Fachworkflow-PASS/Receipt vor dem realen PPM faktisch vorausgesetzt.
- PR #135 ordnet vorhandenen Handoff neu: realer Fachoutput → echter PPM → erst danach finaler PASS/Receipt.
- 4 positive + 4 negative Prinziptests PASS; vollständiger Livebeweis noch ausstehend, weil Live vorher am Kategoriepunkt stoppt.

### B04 – Fake-PPM-PASS im Handoff
- Prinziptest fand, dass ein behaupteter PPM-PASS zunächst bis zum nachgelagerten Validator gelangen konnte.
- Fail-closed im Handoff geschlossen: PPM-Stufe verlangt echte `ppm679_binding` und realen PPM-Pfad.

### B05 – `CODEX_CHECKOUT_NOT_CURRENT_MAIN` / stale Environment
- Historisch wiederholt.
- Aktueller Preflight verlangt/prüft main-Identität; letzter Live-Lauf HEAD exakt `c8a96e7…` PASS.

### B06 – `CODEX_PRODUCTION_ENVIRONMENT_PROOF_MISSING`
- Hobbyraum kann absichtlich keinen Produktionsproof liefern, weil Preflight current main verlangt.
- Kein Produktionsfehler auf aktuellem main; wichtig für Testmethodik.

### B07 – Runtime-Pakete PPM/PSERC nicht gebunden / Env-Variablen fehlen
- Historisch: `PPM679_PACKAGE_ZIP` / `PSERC_FIX_ZIP` fehlten.
- Repo-gebundene Pakete später ergänzt; Original-SHAs dokumentiert.

### B08 – `BOUND_RUNTIME_PRODUCTION_CONTEXT_MISSING`
- Historischer realer Blocker nach PPM-Härtung.
- Später präzisiert: Bootstrap-Paket ist nicht Fachworkflow-Kontext.

### B09 – `ITEM_RECEIPT_FIELDS_OR_CONTRACT_INVALID` / Pass-Ref-Mismatch
- Historische Übergabe-/Receipt-Probleme während Handoff-Umstellungen.

### B10 – `RELEASE_METADATA_INVALID`
- Historischer Blocker: Release-Metadaten nicht exakt an Batch/Count gebunden.

### B11 – `FINAL_CONTEXT_BATCH_MISMATCH`
- Historischer Blocker zwischen 107007/107008/Host-Finalisierung.

### B12 – `STAGING_DESTINATION_COLLISION:ARTICLE.md`
- Reale 7/7-Produktion auf `d841ed…` erzeugte 7 Artikel und alle 12 Stages, kollidierte danach wegen gemeinsamem `ARTICLE.md`.
- Später mit artikel-/plan-slot-eindeutigen Dateinamen adressiert.

### B13 – GitHub Endstempel / fehlendes remote/auth
- Reale `de21…`-Strecke erreichte 107008 PASS; danach Endstempel/Auth-Persistenzproblem.
- Hostseitiger Signer/Endstempelweg später gehärtet.

### B14 – Test-Live-Paritätslücke
- Systemischer Fehler: Regressionstests können PASS melden, obwohl die reale Verkettung nicht bewiesen ist.
- Besonders kritisch: der sogenannte „last real regression re-check“ im Runner ist kein echter Replay des letzten 7/7-Laufs.
- Dieser Punkt erklärt die wiederkehrende Erfahrung „Tests grün, Live wieder alter Fehler“.

## C. Letzte real bewiesene positive Referenzen

- `d841ed7590436ac100b98f15194874573e09bc03`: 7/7 frisch produziert; alle zwölf Stages; späterer Lauf erreichte 107008.
- `de21f6cd35c60849c551fd82f78e75ce57c99fab`: 7/7 + 107008 Review PASS; späterer Fehler erst im GitHub-Endstempel/Auth-Bereich.

## D. Aktuell offen

**Nur ein aktueller erster Live-Blocker ist belegt:** `BOUND_WORDPRESS_CATEGORY_ID_MISSING_FOR_REAL_PPM679_EXECUTION` beim ersten Artikel auf main `c8a96e7…`.

Keine Aussage, dass dies der letzte Fehler der Kette ist; der Lauf wurde korrekt am ersten Blocker beendet.