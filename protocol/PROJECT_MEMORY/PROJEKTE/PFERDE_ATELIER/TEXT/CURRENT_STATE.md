# TEXT – CURRENT STATE

STAND: 2026-09-09
STATUS: **AKTIV – KISS HISTORY/GATE MAINTENANCE BEFORE M17 MERGE**

## AUTORITÄT

Diese Datei enthält ausschließlich den belastbaren aktuellen TEXT-Stand.
Historie → vollständiges Protokoll.
Aktuelle Arbeitsanweisung → `HOBBYRAUM.md`.
Fehlerdetails → autoritative TEXT-Fehlerquelle.

## CURRENT MAIN

`6e650edce60b24baf7d7feef66e60cca2817e59e`

PR #198 ist als reine M16/M17-History-Authority gemergt. Produktionscode blieb dabei unverändert.

## DISPATCHER / SCHUTZ

Permanenter Dispatcher PR #107:
- offen, **nicht mergen**;
- Head exakt `6e650edce60b24baf7d7feef66e60cca2817e59e`.

GitHub Ruleset `Pferde Atelier Main Hardlock`:
- enforcement: active;
- bypass: **leer**;
- Required Checks: `hardlock`, `hardlock-base`.

## AKTUELLER INTEGRATIONSBLOCKER

`M17_HOST_FINALIZATION_NOT_FAIL_CLOSED`

Befund:
- 107008 ruft `finalize_after_107008(...)` auf;
- `finalize_after_107008` kann `PSERC_FINAL_PACKAGE_BLOCKED` / `ok=false` zurückgeben;
- `runtime_entry_gate.py` prüft diesen Rückgabewert aktuell nicht, bevor `107008_FINAL_REVIEW_PASS_VISIBLE_RELEASE_REARMED` zurückgegeben wird;
- damit ist der historische M17-Vertrag „kein finaler PASS ohne erfolgreiche Host-Finalisierung“ aktuell verletzt.

M16:
- alter Runner-Marker war stale;
- aktueller Sollvertrag ist: keine Signer-Credentials/-Kommandos im 107007-/Runtime-Pfad; Signer erst in `finalize_after_107008`;
- dieser aktuelle M16-Vertrag ist auf main PASS.

M35:
- realer Liveblocker bleibt unverändert;
- Produktionskandidat `ef2ecebeb2992013873ba72100d79ffd7c48393c` bleibt unverändert geparkt, bis M17 wieder PASS ist.

## AKTUELLER REALBLOCKER

`PPM679_REAL_EXECUTION_FAILED:SOURCE_HASH_BINDING_MISMATCH`

Fehler-ID:
`M35 – Fact-Pack source-hash binding parity`.

Letzte erfolgreich erreichte Stelle im echten Realtest:
- frische `FACHWORKFLOW_HANDOFF_REQUEST.json` für Artikel 1 materialisiert;
- gebundener `fachworkflow_handoff.command` ausgeführt;
- echter PPM-6.7.9-Eingang erreicht;
- Stop erst bei Prüfung der Fact-Pack-Quellhashbindung.

Root Cause:
**belegt.** Der echte PPM-6.7.9-Vertrag speichert nach `canonical_fact_pack_import_v1` einen eigenen Registry-Hash. Der aktuelle Handoff liest diesen Hash bereits über `PPM679_Storage::fact_pack_hash(...)`, prüft ihn aber nur gegen `production_plan_item.source_hashes`, das noch den Forschungs-/Fact-Pack-Hash enthält. Dadurch werden zwei Hash-Namensräume verwechselt.

## REAL ÜBERWUNDEN AUF DEM AKTUELLEN WEG

- B02 / Fachworkflow-Worker-Kontext;
- B07/M32 / PPM-/PSERC-Runtime-Pfad;
- M28 / echter Request-first-Handoff;
- M34 / `CANONICAL_SLOT_MISSING` und zurückgerutschte Legacy-Handoff-Guards.

M34 wurde mit PR #190 als kompletter Handoff-Korridor auf den bewiesenen B01-Stand zurückgeführt.
Der nachfolgende Realtest kam real über Canonical/Slot hinaus.

## LETZTER SICHERER POSITIVER REFERENZSTAND

- `d841ed7590436ac100b98f15194874573e09bc03`: 7/7 frisch produziert;
- `de21f6cd35c60849c551fd82f78e75ce57c99fab`: 7/7 + 107008 Review PASS.

Diese Referenzen sind historische Vergleichsstände, **nicht** aktueller main.

## AKTIVER ARBEITSSTAND

M17-KISS-Kandidat #199:
- Branch `hobbyroom/m17-host-finalization-fail-closed-20260909`;
- Head `66e9f24a06a6ddb37fd5e8e50f4c158965263abd`;
- M17 selbst PASS;
- bestehende Runtime-Hashkette konsistent;
- serverseitiger Runner: current main reproduziert M17; Kandidat PASS M01–M21 und stoppt danach bei M22.

M22-Gegenprüfung:
- autoritative B15/TECH-KEYFLOW-001-Regel: interner 107007-/H8-Vorlauf hash-/batch-/herkunftsgebunden, keine interne ED25519-/Signer-Pflicht;
- bewiesener Stand `7990029428399e8ba01d88a6543ce068812e9218`: korrigiertes M22-Orakel PASS;
- current main: korrigiertes M22-Orakel FAIL `M22_INTERNAL_SIGNATURE_STILL_REQUIRED`;
- M22 ist damit ein realer späterer bekannter Regressionstreffer, nicht Grund M17 und M22 in einen Sammelfix zu mischen.

Aktive KISS-Wartung:
- Branch `hobbyroom/m22-sequential-history-gate-20260909`;
- Head `90eb7e897897636d51bc13e8ad590fe5d953b0c3`;
- exakt 3 Dateien: bestehender Regression-Runner, bestehende Matrix, bestehendes `paul_scope_gate.py`;
- kein neuer Runner/Gate/Contract;
- vorhandenes Feld `HISTORY_EXPECTED_FAIL` wird bei PRODUCT_FIX als optionaler exakt gebundener nächster späterer bekannter FAIL verwendet.
- PR #200 offen;
- normaler `hardlock`: PASS;
- `hardlock-base`: ausschließlich `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`, weil `control/paul-scope-gate/paul_scope_gate.py` sich selbst als immutable schützt;
- kein weiterer technischer FAIL vor diesem Selbstschutz erreicht.

Geparkter M35-Kandidat:
- `ef2ecebeb2992013873ba72100d79ffd7c48393c`;
- unverändert.

## TESTS – TATSÄCHLICH AUSGEFÜHRT

Sequenz-/M22-Prüfung:
- PRODUCT_FIX M17 → M22: PASS;
- M17 → M35: PASS;
- M17 → M17 oder rückwärts: BLOCK;
- ohne `HISTORY_EXPECTED_FAIL`: Gesamt-PASS bleibt Pflicht;
- korrigiertes M22-Orakel: current main FAIL `M22_INTERNAL_SIGNATURE_STILL_REQUIRED`;
- dasselbe Orakel auf bewiesenem B15-Stand `799002…`: PASS.

M17-Kandidat `66e9f24…` lokal/source-level:
- M16 PASS;
- M17 positiv PASS;
- fehlender Finalization-Guard BLOCK;
- Guard in falscher Reihenfolge BLOCK;
- vollständige Hash-Kette Runtime → 107008 → 107007 → CURRENT_STATE → START_HERE → Pointer rechnerisch konsistent.

History Authority #196:
- M15 aktueller Request-first-Vertrag positiv PASS;
- alte Direct-Submit-/No-Handoff-Semantik negativ BLOCK;
- M35-Modell positiv PASS;
- fehlende Registry-Bindung negativ BLOCK;
- zu späte Bindung nach Planaufbau negativ BLOCK;
- current main reproduziert unter der neuen History-Regel exakt `M35_PPM_REGISTRY_HASH_NOT_MATERIALIZED`.

M35-Kandidat `ef2eceb…` lokal/source-level:
- M34 PASS;
- M35 positiv PASS;
- fehlende Registry-Bindung BLOCK;
- Bindung nach Planaufbau BLOCK.

Auf PR #190:
- `hardlock`: PASS;
- `hardlock-base`: PASS;
- Scope: exakt 1 Datei;
- statischer Korridorcheck Request → PPM → PASS/Receipt → Submission → 107008: PASS.

Auf main `2325f6e1…`:
- echter STARTMASTER0107-Realtest gestartet;
- M28 real passiert;
- M34 / Canonical real passiert;
- erster Stop: M35 `SOURCE_HASH_BINDING_MISMATCH`.

## TESTS – OFFEN / NICHT BEHAUPTET

- M17-Produktionfix noch nicht gebaut oder integriert;
- M35-Kandidat bis M17-PASS pausiert;
- serverseitige `hardlock`-/`hardlock-base`-Abnahme des M35-Kandidaten nicht maßgeblich, solange M17 offen ist;
- kein 7/7-PASS auf aktuellem main;
- 107008 auf aktuellem main nicht erreicht;
- kein Live-PASS des M35-Fixes;
- kein Publish;
- keine WordPress-Schreibaktion.

## ZIEL

Unverändert:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`.

Kein Auto-Publish.
Veröffentlichung nur nach ausdrücklicher Nutzerfreigabe.

## NEXT ACTION

Nicht hier dupliziert.
Ausschließlich `HOBBYRAUM.md` enthält die aktuelle NEXT ACTION.
