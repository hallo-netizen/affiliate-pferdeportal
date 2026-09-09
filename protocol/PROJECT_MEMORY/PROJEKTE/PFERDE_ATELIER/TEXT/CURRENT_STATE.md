# TEXT – CURRENT STATE

STAND: 2026-09-09
STATUS: **AKTIV – M36 PRODUCT FIX UNDER TEST**

## CURRENT MAIN

`239a64261c1fbaf467d0adbd5a2bb1ad2139eca4`

PR #203 / M36 History Authority ist regulär integriert.
M01–M35 bleiben historisch PASS; M36 reproduziert jetzt den echten Realblocker.

## AKTUELLER REALBLOCKER

`H8_BOOTSTRAP_PROVENANCE_BINDING_NOT_CURRENT`

Der echte 7/7-Realtest auf dem vorherigen main stoppte nach:
- Cloud Entry PASS;
- Production Preflight PASS;
- Runtime Entry PASS;

und vor `CURRENT_BOUND_ACTION_READY`.

## ROOT CAUSE

Runtime-/Batch-/Snapshot-/Manifest-Identität ist aktuell.

Persistiertes Paket:
`control/startmaster0107/runtime_inbox/generations/000001/PRODUCTION_PACKAGE.json`

trägt noch:
`PFERDE_ATELIER_H8_BOOTSTRAP_SIGNED_BINDING_V1`

Aktueller Sollvertrag:
`PFERDE_ATELIER_H8_BOOTSTRAP_PROVENANCE_BINDING_V1`

Alle übrigen Provenienzfelder stimmen exakt.
Ein einfacher Reset/Reattach ist keine KISS-Lösung, weil im Repo kein produktiver Bootstrap-Producer für den Neuaufbau existiert.

## AKTIVER M36-KANDIDAT

Branch:
`hobbyroom/m36-h8-legacy-provenance-alias-20260909`

Head:
`fceee7f1959ed2597489a86161b92a024d5a30fc`

Scope:
- 1 Logikdatei:
  `control/single-door-boundary/preproduction_provenance_guard.py`
- 5 ausschließlich bestehende Hash-/Pointer-Bindungen:
  - `control/single-door-boundary/H8_PREPRODUCTION_BOOTSTRAP_BOUNDARY.json`
  - `control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json`
  - `control/startmaster0107/CURRENT_STATE.json`
  - `control/startmaster0107/PFERDE_ATELIER_START_HERE.json`
  - `control/CURRENT_STARTMASTER.json`

KISS-Fix:
- aktueller Provenance-Vertrag bleibt unverändert;
- ausschließlich alter Vertrag `PFERDE_ATELIER_H8_BOOTSTRAP_SIGNED_BINDING_V1` wird als read-only Legacy-Alias zugelassen;
- der alte Binding-Hash muss gültig sein;
- room/receipt/generation/batch/snapshot/manifest/origin müssen exakt dem aktuellen Binding entsprechen;
- unbekannter H8-Vertrag BLOCK;
- keine interne ED25519-/Signer-Pflicht;
- keine Paketmutation / keine Neusignierung.

## VORPRÜFUNG

- main: Legacy-Alias fehlt → erwarteter M36 FAIL;
- Kandidat: aktuelles persistiertes Legacy-Paket identitätsgleich → PASS-fähig;
- falsche Generation → BLOCK;
- unbekannter Vertrag → BLOCK;
- Signer-Tokens im Provenance-Guard: keine;
- Boundary file_bindings: 11/11 PASS;
- bestehende H8 → STEP107007 → CURRENT_STATE → START_HERE / Pointer-Hashkette nachgezogen.

## OFFEN

- serverseitiger M01–M36-Gesamttest des Produktkandidaten;
- kein neuer Realtest vor Produktmerge;
- kein Publish / kein WordPress-Write.

## LETZTER SICHERER POSITIVER REFERENZSTAND

- `d841ed7590436ac100b98f15194874573e09bc03`: 7/7 frisch produziert;
- `de21f6cd35c60849c551fd82f78e75ce57c99fab`: 7/7 + 107008 Review PASS.

`RECOVERY_BASE_SHA = de21f6cd35c60849c551fd82f78e75ce57c99fab`.

## ZIEL

Unverändert:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`.

Kein Auto-Publish.
