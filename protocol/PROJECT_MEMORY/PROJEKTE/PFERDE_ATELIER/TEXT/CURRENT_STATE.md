# TEXT – CURRENT STATE

STAND: 2026-09-09
STATUS: **AKTIV – M22 H8 PROVENANCE PRODUCT CANDIDATE UNDER TEST**

## AUTORITÄT

Diese Datei enthält ausschließlich den belastbaren aktuellen TEXT-Stand.
Historie → vollständiges Protokoll.
Aktuelle Arbeitsanweisung → `HOBBYRAUM.md`.
Fehlerdetails → autoritative TEXT-Fehlerquelle.

## CURRENT MAIN

`7531154a6218a06e49d35b78062933df3c886625`

PR #199 / M17 ist regulär über die Required Checks gemergt.
M17 `M17_HOST_FINALIZATION_NOT_FAIL_CLOSED` ist damit integriert behoben.

## DISPATCHER / SCHUTZ

Permanenter Dispatcher PR #107:
- offen, **nicht mergen**;
- Head exakt `7531154a6218a06e49d35b78062933df3c886625`.

GitHub Ruleset `Pferde Atelier Main Hardlock`:
- enforcement: active;
- bypass: **leer**;
- Required Checks: `hardlock`, `hardlock-base`.

## AKTUELLER INTEGRATIONSBLOCKER

`M22_INTERNAL_SIGNATURE_STILL_REQUIRED`

Fehler-ID:
`M22 – H8 Provenance / Integrität ohne interne Signatur`.

Root Cause:
- autoritative TECH-KEYFLOW-001/B15-Regel verlangt im internen 107007-/H8-Vorlauf nur Hash-/Batch-/Herkunftsbindung;
- kryptografische Signierung bleibt außerhalb dieses internen Worker-Korridors;
- current main enthält im H8-Korridor wieder die ältere `PFERDE_ATELIER_H8_BOOTSTRAP_SIGNED_BINDING_V1`-/Signer-Pflicht;
- bewiesener B15-Stand `7990029428399e8ba01d88a6543ce068812e9218` erfüllt den aktuellen Sollvertrag.

M23-Abgrenzung:
- externe Upload-/Release-Prüfung bleibt signiert;
- `validate_production_package()` mit ED25519 bleibt erhalten;
- nur der interne Preproduction-Pfad nutzt wieder `validate_production_package_integrity()`.

## AKTIVER M22-KANDIDAT

Branch:
`hobbyroom/m22-h8-provenance-no-internal-signature-20260909`

Head:
`0aebd56998c2cb4e102b0d3e19cb3ea29985a65c`

Scope exakt 6 vorhandene H8-Dateien:
- `control/single-door-boundary/H8_PREPRODUCTION_BOOTSTRAP_BOUNDARY.json`;
- `control/single-door-boundary/preproduction_provenance_guard.py`;
- `control/single-door-boundary/single_door_bootstrap.py`;
- `control/single-door-boundary/single_door_preproduction_handoff.py`;
- `control/single-door-boundary/project_single_door_entry_v2.py`;
- `control/single-door-boundary/test_h8_preproduction_bootstrap.py`.

Kein neuer Runner, Gate, Contract, Executor oder Parallelweg.

## PRÜFUNG – TATSÄCHLICH AUSGEFÜHRT

Source-level Positiv/Negativ:
- current main → FAIL `M22_INTERNAL_SIGNATURE_STILL_REQUIRED`;
- M22-Kandidat → PASS;
- interne Signer-/Trusted-Key-Abhängigkeit entfernt;
- Hash-/Provenienzbindung bleibt fail-closed;
- externe M23-Signaturprüfung bleibt erhalten;
- Codex-Capsule-Weg bleibt erhalten;
- H8-Test wieder zustandsunabhängig und enthält negative Hashprüfung.

Boundary:
- sämtliche 11 `file_bindings` gegen den Kandidaten geprüft;
- 11/11 Blob-SHAs stimmen exakt.

## NÄCHSTER BEKANNTER FEHLER DANACH

M35 bleibt unverändert der bekannte reale Liveblocker:
`PPM679_REAL_EXECUTION_FAILED:SOURCE_HASH_BINDING_MISMATCH`

Geparkter M35-Kandidat:
`ef2ecebeb2992013873ba72100d79ffd7c48393c`

M22 und M35 bleiben getrennte Reparaturen.

## LETZTER SICHERER POSITIVER REFERENZSTAND

- `d841ed7590436ac100b98f15194874573e09bc03`: 7/7 frisch produziert;
- `de21f6cd35c60849c551fd82f78e75ce57c99fab`: 7/7 + 107008 Review PASS.

`RECOVERY_BASE_SHA = de21f6cd35c60849c551fd82f78e75ce57c99fab`.

## OFFEN / NICHT BEHAUPTET

- serverseitige `hardlock`-/`hardlock-base`-Abnahme des M22-Kandidaten noch offen;
- kein neuer echter 7/7-Realtest nach M22;
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
