# STARTMASTER0107 – KOMPLETTE AKTUELLE FEHLERLISTE – 18.09.2026

STATUS: AUTORITATIVE AKTUELLE FEHLERQUELLE

VORGÄNGER NUR HISTORISCHER LANGBELEG:
`04_FEHLERLISTE_KOMPLETT_AKTUELL_20260905.md`

## AKTUELLE LIVE-WAHRHEIT – 18.09.2026

Current main / technischer M39-Baseline-Stand:
`f9bc719efd0924a18ee876ee8581a566afa7ecda`

Letzter belastbarer Live-Baseline-/Recovery-Stand vor M37:
`bb005a5324a0a6270aacb52b5927613bde1ab4bc`

M01–M38 sind verbindliche bekannte Regression und integriert.
M39 ist der aktuell offene History-Fall und noch **nicht** als Produktfix freigegeben.

M37 History-Autorität:
- PR248;
- `HOBBYROOM_HISTORY_REPRODUCTION_PASS:M37`;
- `HOBBYROOM_HISTORY_MACHINE_PROOF_PASS:M37`;
- hardlock PASS;
- hardlock-base PASS;
- Merge/Main `f791dcc6c926f9c136faed29957e64786ffca08e`.

M37 Produktfix:
- PR247;
- Kandidat `59ad44da3d89769c05f0725f9929135b0262f4dd`;
- hardlock PASS;
- hardlock-base PASS;
- `HOBBYROOM_HISTORY_REPRODUCTION_PASS:M37`;
- `HOBBYROOM_HISTORY_MACHINE_PROOF_PASS:M37`;
- Merge/Main `f1d1605f18bd23d9189f89ad173598958718d08a`.

Der M37-Fix ändert ausschließlich Observability.

## AKTUELLER PRODUKTIONSSTATUS / M39

Der erste frische Artikel erreichte nach realer LanguageTool-Reparatur den echten PPM-6.7.9-/PSERC-Handoff. Er stoppte mit dem belegten ersten technischen Blocker:

`PPM679_REAL_EXECUTION_BLOCKED:PSERC_BRIDGE_PPM_PLAN_VERSION_MISMATCH`

Zweiter Artikel wurde nicht gestartet. 107008 wurde nicht erreicht. Kein WordPress-Write, kein Publish.

Die bestehende autorisierte Abschlusslogik enthält für den akzeptierten `production_plan_v4`-Header bereits die Versionsbindungen:
- `plan_contract_version == "4.0.0"`
- `required_plugin_version == "6.7.9"`

M38 prüft, ob der current Fachworkflow diese beiden gebundenen Versionsfelder im real erzeugten `production_plan_header` erhält und der Handoff sie fail-closed vor dem realen PPM/PSERC-Aufruf prüft.

Der aktuelle Pre-Codex-Gesamttest hat einen neuen technischen Abschlussfehler offengelegt:

`CURRENT_7ER_BATCH_ALREADY_HAS_DURABLE_RELEASE_IDENTITY_COLLISION`

Der gebundene 7er-Batch besitzt bereits eine ältere dauerhafte Endstempel-Ausgabe unter derselben Batch-ID. Ein neuer NEW-Lauf mit neuen Artikelbytes darf diese alte Ausgabe weder überschreiben noch dieselbe Release-ID wiederverwenden. Die fachliche Batch-ID muss unverändert bleiben; benötigt wird ausschließlich eine getrennte technische Release-ID pro Ausgabelauf.

Der vollständige System-4-Simulationslauf auf Kandidat `0a2a41db0b6798b865ef0e75f1d3425bb079ed2d` hat die vorgesehene Produktlösung bereits funktional mit 40/40 PASS bewiesen. Vor Integration wird M39 jetzt getrennt als History-Fall gebunden.

## VERBINDLICHE HISTORISCHE REGRESSION M01–M39

| ID | Fehlerklasse | Aktueller Status |
|---|---|---|
| M01 | State-/Bundle-Hash chain | historisch / Regression |
| M02 | Unique article files | historisch / Regression |
| M03 | PREPARED Persist/Restore | historisch / Regression |
| M04 | Finalize CLI | historisch / Regression |
| M05 | Durable Release/Receipt | historisch / Regression |
| M06 | No fake production contract | historisch / Regression |
| M07 | Recovery not automatically final | historisch / Regression |
| M08 | PPM ZIP available | historisch / Regression |
| M09 | PSERC ZIP available | historisch / Regression |
| M10 | Runtime toolbox / Preflight fail-closed | historisch / Regression |
| M11 | Real PPM call | historisch / Regression |
| M12 | Fake PPM blocked | historisch / Regression |
| M13 | PPM content_hash parity | historisch / Regression |
| M14 | Current Action Handoff | historisch / Regression |
| M15 | 107007 Handoff instruction | historisch / Regression |
| M16 | Signer boundary | historisch / Regression |
| M17 | 107008 fail-closed | historisch / Regression |
| M18 | ENDSTEMPEL constants | historisch / Regression |
| M19 | Merge trigger | historisch / Regression |
| M20 | Delivery | historisch / Regression |
| M21 | No auto-publish | historisch / Regression |
| M22 | H8 Provenance / Integrität | historisch / Regression |
| M23 | Preproduction/Runtime Guards | historisch / Regression |
| M24 | No H8 rollback | historisch / Regression |
| M25 | Article prompt / Fachworkflow boundary | historisch / Regression |
| M26 | Bound Fachworkflow production context | historisch / Regression |
| M27 | Current-main / production environment identity | historisch / Regression |
| M28 | Fachworkflow-Handoff request executable | historisch / Regression |
| M29 | Release metadata current-batch identity | historisch / Regression |
| M30 | Final context batch identity | historisch / Regression |
| M31 | Codex-native bound action | historisch / Regression |
| M32 | PPM package path binding | historisch / Regression |
| M33 | GitHub ENDSTEMPEL ohne Codex git auth | historisch / Regression |
| M34 | Legacy PPM handoff guards / canonical slot parity | historisch / Regression |
| M35 | PPM Fact-Pack source-hash binding parity | historisch / Regression |
| M36 | Persisted H8 legacy-binding compatibility | historisch / Regression |
| M37 | `PPM679_REAL_EXECUTION_BLOCKED` – non-repairable PPM/PSERC inner reason visibility | **AKTIV / HISTORY-AUTORITÄT ZUERST** |
| M38 | `PPM679_REAL_EXECUTION_BLOCKED:PSERC_BRIDGE_PPM_PLAN_VERSION_MISMATCH` – current Fachworkflow production-plan version binding | integriert / Regression |
| M39 | `CURRENT_7ER_BATCH_ALREADY_HAS_DURABLE_RELEASE_IDENTITY_COLLISION` – frische technische Release-ID getrennt von logischer Batch-ID | **HISTORY_AUTHORITY_MAINTENANCE OFFEN** |

History-Kandidat:
- PR249;
- Branch `hobbyroom/m38-plan-version-history-20260911`;
- ausschließlich bestehende Fehlermatrix + bestehender Regressionrunner;
- erwarteter Maschinenbeweis: Main M01–M37 PASS, M38 erster neuer FAIL;
- kein Produktfix in dieser Phase.

Erst nach maschinellem M38-History-Beweis darf ein separater kleinstmöglicher Produktfix erfolgen. Danach genau ein frischer erster Artikel durch reales LanguageTool + reales PPM/PSERC; erst nach Einartikel-PASS Restbatch bis 107008; vor Publish stoppen.


## M39 HISTORY-KANDIDAT

- Branch `hobbyroom/m39-release-identity-history-20260918`
- Head `5546adc61404437ac9de7ff35bba2d982b9d6266`
- nur Fehlermatrix + bestehender Regressionrunner
- erwartet: M01–M38 PASS, M39 erster neuer FAIL
- kein Produktfix in dieser Phase
