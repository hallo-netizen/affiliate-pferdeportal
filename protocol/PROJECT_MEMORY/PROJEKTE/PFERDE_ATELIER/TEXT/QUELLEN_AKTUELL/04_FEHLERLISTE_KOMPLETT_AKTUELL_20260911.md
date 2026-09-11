# STARTMASTER0107 – KOMPLETTE AKTUELLE FEHLERLISTE – 11.09.2026

STATUS: AUTORITATIVE AKTUELLE FEHLERQUELLE

VORGÄNGER NUR HISTORISCHER LANGBELEG:
`04_FEHLERLISTE_KOMPLETT_AKTUELL_20260905.md`

## AKTUELLE LIVE-WAHRHEIT – 11.09.2026

Current main:
`a2f2f1b4b7af1e905c6a0cb69c5389664b7c4ad6`

Letzter belastbarer Live-Baseline-/Recovery-Stand vor dem aktuellen Sichtbarkeitskandidaten:
`bb005a5324a0a6270aacb52b5927613bde1ab4bc`

M01–M36 sind die integrierte bekannte Regression.
Der danach ausgeführte frische Produktionslauf recherchierte und erzeugte den ersten Artikel und erreichte den echten PPM-6.7.9-/PSERC-Handoff. Dort endete der sichtbare äußere Befund mit:

`PPM679_REAL_EXECUTION_BLOCKED`

Der bereits zurückgegebene konkrete innere Bridge-Grund wurde vom äußeren Handoff nicht erhalten. Der ursprüngliche Codex-Task ist inzwischen nicht mehr verfügbar; deshalb bleibt der fachliche/technische innere Produktions-Rootcause ausdrücklich **UNKNOWN**, bis ein neuer echter erster Artikel denselben Handoff erreicht.

Aktive History-Regression: **M37**.
Aktuelle Arbeit ist ausschließlich zweiphasig nach vorhandenem Hobbyraum-Maschinenbeweis:
1. M37 in bestehender Matrix + bestehendem Runner als History-Autorität aufnehmen und auf unverändertem Main reproduzierbar FAIL beweisen.
2. Erst danach separater Produktfix: Handoff bleibt fail-closed, erhält aber den ersten bereits vorhandenen inneren PPM/PSERC-Grund sichtbar; anschließend kompletter M01–M37-PASS.

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
| M37 | `PPM679_REAL_EXECUTION_BLOCKED` – non-repairable PPM/PSERC inner reason visibility | **AKTIV / HISTORY-AUTORITÄT ZUERST** |

## M37 – EXAKTE GRENZE

Positiv:
- vorhandener verschachtelter nicht-reparierbarer `error_code` oder Reason-Code bleibt im äußeren BLOCKED sichtbar.

Negativ:
- ohne vorhandenen konkreteren Grund wird nichts erfunden; der Sammelcode bleibt `PPM679_REAL_EXECUTION_BLOCKED`.
- reparierbare `BLOCKED_CONTENT_*`, `BLOCKED_WAVE2_*`, `BLOCKED_CANONICAL_RUNTIME_LINK_*` bleiben unverändert `FACHWORKFLOW_REPAIR_REQUIRED`.

Produktions-Rootcause: **UNKNOWN BIS NEUER LIVE-LAUF**.
107008: nicht erreicht.
Publish: nicht ausgeführt / nicht erlaubt.
