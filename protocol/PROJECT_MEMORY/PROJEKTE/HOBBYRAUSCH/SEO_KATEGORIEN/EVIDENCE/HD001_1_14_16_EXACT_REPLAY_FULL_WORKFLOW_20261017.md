# HD-001 1.14.16 – EXACT REPLAY + FULL WORKFLOW EVIDENCE – 2026-10-17

## Grundlage

Realer Nutzerexport:
`hobby-depot-final-target-readback-20261017-113602-utc.json`

Realer 1.14.15-Stand:
- 3517 logisch;
- 3487 physisch;
- CREATE 1122;
- ADOPT 4;
- UPDATE 2359;
- ARCHIVE 1;
- BLOCKED;
- Fehler Hummelkästen + Lederprägen.

## Exakter Replay 1.14.15

Der reale Plan wurde mit dem unveränderten 1.14.15-Dry-Run-Code gegen eine aus dem Export und belegten Altobjekten rekonstruierte Live-Ausgangslage erneut erzeugt.

PASS:
- 3486/3486 Aktionen identisch;
- Reihenfolge identisch;
- object_id identisch;
- action identisch;
- mismatches identisch;
- summary identisch;
- errors identisch;
- action_exact=true;
- diffs=[].

## Korrektur

Tatsächliche alte Bindungen:
- Hummelkästen 902484 -> core:entity:b411cdf2ea6046005a4b;
- Lederprägen 902560 -> core:entity:ef539e4fcf98dc1c2437.

1.14.16 ergänzt nur diese Migrationsbindungen und optimiert bereits vor Release den nachfolgenden Syncpfad.

## 1.14.16 Positiv

Dry-Run:
- PASS;
- 3487 Ziele;
- CREATE 1122;
- ADOPT 4;
- UPDATE 2361;
- UNCHANGED 0;
- ARCHIVE 1;
- Errors 0.

Runner:
- COMPLETE;
- 3487/3487 Readback;
- 1122 created;
- 2361 updated;
- 4 adopted;
- 1 archived;
- error leer.

Frontend:
- 8 Welten;
- Header PASS;
- expected_count 112;
- 381/381 Hobbyseiten PASS;
- 0 unbound CORE pages.

Post-Sync:
- CREATE 0;
- ADOPT 0;
- UPDATE 0;
- UNCHANGED 3487;
- ARCHIVE 0;
- Errors 0.

## 1.14.16 Negativ

PASS:
- Hummel foreign -> BLOCKED;
- Hummel duplicate legacy -> BLOCKED;
- Leder foreign -> BLOCKED;
- Leder duplicate legacy -> BLOCKED;
- Live drift after saved Dry-Run -> real apply rejects;
- injected writer failure after 75 mutations -> ROLLBACK_PENDING -> ROLLED_BACK;
- post-rollback plan fingerprint/actions/summary/errors equal original plan;
- normal admin render -> no full scan;
- manual-only bootstrap -> 0 writes / 0 schedules / 0 network.

## Performance

- old sync depth sorting ~24.26 s local;
- cached depth sorting ~0.012 s;
- complete runner uses bounded batches;
- no single local sync tick approached timeout.

## Package

`HD001_V1.14.16_HOBBY_DEPOT_V7_1_EXACT_REPLAY_FULL_WORKFLOW_HARDPASS.zip`

ZIP SHA-256:
`bbee98fbf9bbfadf49f18bf64e9f64aba1a274b2266a1473ec89d87996654792`

Profile SHA-256:
`87275396fdd8e2e9d15b0a37a6d17a7a21889825d7cdb3f64f276005c73b99d0`

QA:
- PHP 33/33;
- ZIP 44/44;
- unzip PASS;
- roundtrip hashes 44/44 exact.

## Grenze

Noch kein Live-PASS für 1.14.16.
Der nächste reale Schritt ist ausschließlich der WordPress-Dry-Run. Kein Apply/Sync.
