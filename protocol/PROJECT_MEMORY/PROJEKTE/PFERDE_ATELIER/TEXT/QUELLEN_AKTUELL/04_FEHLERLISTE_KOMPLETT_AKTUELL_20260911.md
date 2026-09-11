# STARTMASTER0107 – KOMPLETTE AKTUELLE FEHLERLISTE – 11.09.2026

STATUS: AUTORITATIVE AKTUELLE FEHLERQUELLE

VORGÄNGER NUR HISTORISCHER LANGBELEG:
`04_FEHLERLISTE_KOMPLETT_AKTUELL_20260905.md`

## AKTUELLE LIVE-WAHRHEIT – 11.09.2026

Current main:
`f791dcc6c926f9c136faed29957e64786ffca08e`

Letzter belastbarer Live-Baseline-/Recovery-Stand vor dem aktuellen Sichtbarkeitskandidaten:
`bb005a5324a0a6270aacb52b5927613bde1ab4bc`

M01–M37 sind jetzt die verbindliche bekannte Regression. M37 wurde in PR248 ausschließlich als History-Autorität integriert; der bestehende Maschinenbeweis lieferte `HOBBYROOM_HISTORY_REPRODUCTION_PASS:M37` und `HOBBYROOM_HISTORY_MACHINE_PROOF_PASS:M37`, hardlock und hardlock-base PASS.

Der letzte frische Produktionslauf recherchierte und erzeugte den ersten Artikel und erreichte den echten PPM-6.7.9-/PSERC-Handoff. Dort endete der sichtbare äußere Befund mit:

`PPM679_REAL_EXECUTION_BLOCKED`

Der bereits zurückgegebene konkrete innere Bridge-Grund wurde vom äußeren Handoff nicht erhalten. Der ursprüngliche Codex-Task ist inzwischen nicht mehr verfügbar; deshalb bleibt der eigentliche Produktions-Rootcause ausdrücklich **UNKNOWN**, bis nach abgeschlossenem M37-Produktfix genau ein neuer echter erster Artikel denselben Handoff erreicht.

Aktive Arbeit: **M37 PRODUCT_FIX**.
Produktkandidat: PR247 / `hobbyroom/ppm-inner-reason-visibility-20260911` / Head `59ad44da3d89769c05f0725f9929135b0262f4dd`.

Zulässiger Fix ausschließlich:
- Handoff bleibt fail-closed BLOCKED;
- der erste bereits vorhandene konkrete nicht-reparierbare PPM/PSERC-Grund wird sichtbar erhalten;
- ohne konkreteren Grund wird nichts erfunden;
- reparierbare `BLOCKED_CONTENT_*`, `BLOCKED_WAVE2_*`, `BLOCKED_CANONICAL_RUNTIME_LINK_*` bleiben `FACHWORKFLOW_REPAIR_REQUIRED`;
- bestehende Hashkette wird nachgezogen.

Kein neuer Runner, kein neuer Gate, kein neuer Controller, keine PPM-/PSERC-/PSTE-/Textmaschinen-/SEO-/Link-/Tabellen-/Design-/Publish-Regeländerung.
Kein Publish.

## VERBINDLICHE HISTORISCHE REGRESSION M01–M37

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
| M37 | `PPM679_REAL_EXECUTION_BLOCKED` – non-repairable PPM/PSERC inner reason visibility | **AKTIV / PRODUCT_FIX** |

## M37 – PASS-GRENZE

BEFORE auf aktuellem Main:
- bestehender M01–M37-Runner muss exakt M37 als ersten FAIL reproduzieren.

AFTER auf Produktkandidat:
- kompletter bestehender M01–M37-Runner = `GESAMT PASS`;
- hardlock = PASS;
- hardlock-base = PASS;
- `HOBBYROOM_HISTORY_MACHINE_PROOF_PASS:M37`.

Produktions-Rootcause: **UNKNOWN BIS NEUER LIVE-LAUF**.
107008: nicht erreicht.
Publish: nicht ausgeführt / nicht erlaubt.
