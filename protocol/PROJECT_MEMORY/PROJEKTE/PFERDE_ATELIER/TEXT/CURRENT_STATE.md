# TEXT – CURRENT STATE

STAND: 2026-09-09
STATUS: **AKTIV – M36 HISTORY AUTHORITY / REALTEST BLOCKED**

## AUTORITÄT

Diese Datei enthält ausschließlich den belastbaren aktuellen TEXT-Stand.
Historie → vollständiges Protokoll.
Aktuelle Arbeitsanweisung → `HOBBYRAUM.md`.
Fehlerdetails → autoritative TEXT-Fehlerquelle.

## CURRENT MAIN

`05f5d00ec924e108d6700f39d22d9ec1d47318a6`

M01–M35 sind maschinell Gesamt-PASS und regulär integriert.
Der danach ausgeführte echte 7/7-Realtest hat einen neuen ersten technischen Blocker aufgedeckt.

## REALTEST 09.09.2026

HEAD:
`05f5d00ec924e108d6700f39d22d9ec1d47318a6`

PASS:
- Cloud Entry;
- Production Preflight;
- Runtime Entry `OFFICIAL_RUNTIME_ENTRY_PASS`.

Erster echter Blocker:
`H8_BOOTSTRAP_PROVENANCE_BINDING_NOT_CURRENT`

Stop:
- vor `CURRENT_BOUND_ACTION_READY`;
- `STEP_TERMINAL_NONPASS`;
- state_advanced=false;
- keine Reparatur im Realtest;
- kein Publish / kein WordPress-Write.

## ROOT CAUSE M36

Aktueller Runtime-State ist konsistent:
- status `EXECUTION_READY`;
- generation 1;
- Batch-/Snapshot-/Manifest-Hashes stimmen.

Persistiertes Paket:
`control/startmaster0107/runtime_inbox/generations/000001/PRODUCTION_PACKAGE.json`

trägt noch:
`PFERDE_ATELIER_H8_BOOTSTRAP_SIGNED_BINDING_V1`

Aktueller Guard erwartet:
`PFERDE_ATELIER_H8_BOOTSTRAP_PROVENANCE_BINDING_V1`

Alle Provenienzfelder außer Vertragsname/Binding-Hash stimmen exakt.
Das persistierte H8- und Production-Paket sind identisch alt.
Die incoming-Quelle besitzt keine H8-Bindung.

Der vorhandene Bootstrap besitzt im Repo keinen produktiven Producer; ein Reset/Reattach löst das Problem daher nicht ohne neue externe Erzeugung.

## AKTUELLER ARBEITSWEG

Neuer Fehler:
`M36 – Persisted H8 legacy-binding compatibility after provenance migration`

Zuerst History Authority:
- Matrix/Runner um M36 erweitern;
- current main muss M01–M35 PASS und exakt M36 FAIL reproduzieren;
- kein Produktcode in diesem Schritt.

History-Kandidat:
- Branch `hobbyroom/m36-history-authority-20260909`;
- Head `2465052149974f52cfb84797cf369cea430c23cc`;
- exakt Matrix + bestehender Runner.

Danach erst Produktfix:
- eng begrenzter Legacy-Alias nur für `PFERDE_ATELIER_H8_BOOTSTRAP_SIGNED_BINDING_V1`;
- alle Provenienzidentitäten müssen aktuell sein;
- unbekannter Vertrag BLOCK;
- falsche Generation/Batch/Snapshot/Manifest/Origin BLOCK;
- keine interne Signaturpflicht zurück;
- keine Paketmutation/Neusignierung.

## ZIEL

Unverändert:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`.

Kein Auto-Publish.
