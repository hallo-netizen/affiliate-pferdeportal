# PSTE 0.56.8 – Candidate-Persistence / Research-Recovery – Release-Checkpoint

## Scope
Ausschließlich die technische Persistenzkonsistenz des vorhandenen Recherchepfads und der lokale Recoverypfad für `PSTE_RESEARCH_FINALIZE_PREPARE_COUNT_MISMATCH`.

Keine Änderung an DataForSEO-Abfragen, Providerreihenfolge, Kostenlogik, Auswahl offener Familien, Familien-/Kategorie-/Artikeltyp-/Titel-/SEO-Entscheidungen, Sandbox-Reviewentscheidungen, Textmaschine, PSERC, PPM, Design, WordPress-Inhalten oder Publish.

## Root Cause
Distinkte Discovery-Gruppen können auf dieselbe technische `candidate_id` konvergieren. Die Kandidatentabelle erzwingt historisch `UNIQUE(run_uuid,candidate_id)` und `saveCandidate()` nutzt `REPLACE`, sodass last-write-wins gilt. 0.56.6 verglich vor FINALIZE die unverdichtete In-Memory-Anzahl mit der tatsächlich speicherbaren Kandidatenmenge und erzeugte dadurch `PSTE_RESEARCH_FINALIZE_PREPARE_COUNT_MISMATCH`.

0.56.8 bildet vor `candidate_count`/Queue/Persistenz exakt dieselbe last-write-wins-Persistenzmenge ab und erlaubt einen bereits bezahlten 3/3-Lauf mit genau diesem Fehler lokal replay-safe fortzusetzen. Der Breitenlauf nutzt denselben Kindlauf-Recoverypfad.

## Delta 0.56.7 → 0.56.8
Geändert:
- `portal-seo-topic-engine.php`: `55d0ba3af27a63ccc0c15db224896366468a35c4a89160929a78f482b9c6ae44` → `28955c10ed3418a0399837906a5c38e0bf42a6834ad7ddfe2754d649073aef20`
- `includes/class-pste-runner.php`: `5c61aff4219b4d62b82804bb4cf4ee3c5c0bfdf086cbf3fcc9eb36764143aae0` → `8756857bc32c7505d16945d95c7cbfba4a5857513c6b6635dd154e1345e894a2`
- `includes/class-pste-research-job.php`: `d9d734125e8ef112ec95ed81a229d5532e90b8ed4bc36dbb2a52489ac1ec9a41` → `cd464f84141e14cac481e7ef4e7b4aae86d27c22bda78a2a4cab167888832d97`
- `includes/class-pste-breadth-research-queue.php`: `2578f27bb1c590bc3fef7c6298983bfbc1e7e92b02188788083e622a455cbe2f` → `32d68e70f2cc8658db08295c83e4d71b1c6d5b2c9364b5fd116903d0b4ef4b7b`
- `CHANGELOG_0.56.8.md`: neu

203 bestehende Dateien sind byteidentisch. 0 entfernt.

## Harte Tests
- Candidate-ID-Kollisions-/Persistenztest Source + Fresh: PASS; historischer last-write-wins-Gewinner unverändert.
- FINALIZE State Machine Source + Fresh: PASS; alter 2.1.0-Job → 2.2.0 → COMPLETE; 0 Providercalls; Count-Mismatch-Replay → COMPLETE; Stall weiterhin fail-closed `PAUSED_ERROR/PSTE_RESEARCH_FINALIZE_STALLED`.
- Breitenlauf Restart nach `CANCELLED`: COMPLETE; 2 Familien vollständig.
- Breitenlauf Count-Mismatch-Recovery: COMPLETE.
- Source↔Fresh: 208/208 byteidentisch.
- PHP: 72/72 Source + 72/72 Fresh PASS.
- JSON: 52/52 Source + 52/52 Fresh PASS.
- Aktuelle Projektion: 619/619 unverändert, SHA-256 `b1950e47c0200830cb71394370bf63f2b22f9f18a1ba5e2bec1f7fd5f170933f`.
- PSERC Capability unverändert: `9d2636ecda87e2d93106deaff4f1358e4fa9cf906c1d55177e3119d94df65d8f`.
- PPM 6.7.9: offizieller 137er Satz Source + Fresh frisch erneut ausgeführt, 137/137 PASS, Source/Fresh-Ausgabe byteidentisch.
- Link Policy 1.0.1: offizieller 19er Satz Source + Fresh frisch erneut ausgeführt, 19/19 PASS, Source/Fresh-Ausgabe byteidentisch.
- PSERC 0.28.3 frisch erneut: 41/41 Normal PASS; 58/58 Terminal PASS; 9/9 Package PASS; One-Click PASS; Snapshot- und Batch-Drift BLOCKED; publish false; Source + Fresh.

## Installer
`portal-seo-topic-engine_0.56.8_CANDIDATE_PERSISTENCE_ROOTFIX.zip`
SHA-256: `de4901395360506a0c33dd2c705dcc533effee124c2c0cd47475df2ae6e91221`

Status: Code und systemweite Regression PASS. Finale STARTMASTER0067-Verpackung/Fresh-Unpack folgt separat. `main` bleibt unverändert; kein Merge.
