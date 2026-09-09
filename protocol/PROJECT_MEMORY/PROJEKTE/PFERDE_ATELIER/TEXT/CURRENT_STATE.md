# TEXT – CURRENT STATE

STAND: 2026-09-09
STATUS: **BLOCKED – M17 FAIL-CLOSED REGRESSION BEFORE M35**

## AUTORITÄT

Diese Datei enthält ausschließlich den belastbaren aktuellen TEXT-Stand.
Historie → vollständiges Protokoll.
Aktuelle Arbeitsanweisung → `HOBBYRAUM.md`.
Fehlerdetails → autoritative TEXT-Fehlerquelle.

## CURRENT MAIN

`d6de9265cddc1b2a011d707ad615c144cdd9d4ab`

PR #196 ist als reine History Authority gemergt. Produktionscode blieb dabei unverändert.

## DISPATCHER / SCHUTZ

Permanenter Dispatcher PR #107:
- offen, **nicht mergen**;
- Head exakt `d6de9265cddc1b2a011d707ad615c144cdd9d4ab`.

GitHub Ruleset `Pferde Atelier Main Hardlock`:
- enforcement: active;
- bypass: **temporär Repository admin / For pull requests only aktiv**; vor Produktionsmerge zwingend wieder entfernen;
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

Aktive History Authority:
- Branch `hobbyroom/m16-m17-history-authority-20260909`;
- Head `5ea8d5da54ca946dd99b3d85a2f3fb8488b7a7b8`;
- ausschließlich bestehender M01–M35-Runner;
- M16-Orakel an aktuellen Signer-Vertrag angepasst;
- M17-Orakel auf echten Fail-closed-Vertrag gehärtet.

Geparkter M35-KISS-Kandidat:
- Branch `hobbyroom/m35-ppm-registry-hash-binding-20260909`;
- Head `ef2ecebeb2992013873ba72100d79ffd7c48393c`;
- unverändert, kein weiterer Fix.

## TESTS – TATSÄCHLICH AUSGEFÜHRT

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
