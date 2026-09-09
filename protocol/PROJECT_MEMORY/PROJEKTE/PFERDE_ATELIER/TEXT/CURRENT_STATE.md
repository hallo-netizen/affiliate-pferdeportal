# TEXT – CURRENT STATE

STAND: 2026-09-09
STATUS: **AKTIV – M35 PRODUCT CANDIDATE FINAL HISTORY TEST**

## AUTORITÄT

Diese Datei enthält ausschließlich den belastbaren aktuellen TEXT-Stand.
Historie → vollständiges Protokoll.
Aktuelle Arbeitsanweisung → `HOBBYRAUM.md`.
Fehlerdetails → autoritative TEXT-Fehlerquelle.

## CURRENT MAIN

`d32e16cdf6b45ffa282e42fa78e07da84863e362`

M17, M22 und M26 sind regulär integriert behoben.
Letzter Merge: PR #202 / M26.

## DISPATCHER / SCHUTZ

Permanenter Dispatcher PR #107:
- offen, **nicht mergen**;
- Head exakt `d32e16cdf6b45ffa282e42fa78e07da84863e362`.

GitHub Ruleset `Pferde Atelier Main Hardlock`:
- enforcement: active;
- Required Checks: `hardlock`, `hardlock-base`;
- Produktionsmerge nur bei leerem Bypass.

## AKTUELLER INTEGRATIONS- UND REALBLOCKER

`PPM679_REAL_EXECUTION_FAILED:SOURCE_HASH_BINDING_MISMATCH`

Fehler-ID:
`M35 – Fact-Pack source-hash binding parity`.

Letzte real erreichte Stelle:
- frische `FACHWORKFLOW_HANDOFF_REQUEST.json`;
- gebundener Fachworkflow-Handoff;
- echter PPM-6.7.9-Eingang;
- Stop bei PPM-Registry-Quellhashbindung.

Root Cause:
- Research-/Content-Fact-Pack-Hash und interner PPM-Registry-Hash sind zwei unterschiedliche Hash-Namensräume;
- PPM speichert nach `canonical_fact_pack_import_v1` einen eigenen Registry-Hash;
- der Handoff liest diesen Hash bereits über `PPM679_Storage::fact_pack_hash(...)`;
- der alte Code vergleicht ihn fälschlich mit den Research-Hashes in `production_plan_item.source_hashes`.

## AKTIVER M35-KANDIDAT

PR #197:
`M35: bind internal PPM plan to registry fact-pack hash`

Branch:
`hobbyroom/m35-ppm-registry-hash-binding-20260909`

Fresh Head:
`a611a5c150cc3d8f182ca9c1855339fb98fea0c2`

Base:
`d32e16cdf6b45ffa282e42fa78e07da84863e362`

Scope:
- exakt eine Produktionsdatei:
  `control/startmaster0107/fachworkflow_proof_handoff.py`.

KISS-Fix:
- leerer PPM-Registry-Hash bleibt BLOCK;
- sonst ausschließlich in der internen PPM-Plan-Kopie:
  `$item['source_hashes']=[$expectedSource];`
- erst danach Planaufbau.

Nicht geändert:
- Research-/Content-Evidence-Hash;
- SEO 5-Felder;
- Textmaschine;
- Fachregeln;
- PPM-/PSERC-/PSTE-Regeln;
- LanguageTool;
- Design;
- Publish.

## BEREITS GEPRÜFT

- M34 PASS;
- M35 positiv PASS;
- fehlende Registry-Bindung BLOCK;
- Registry-Bindung erst nach Planaufbau BLOCK;
- fresh main enthält den Fehler weiterhin;
- rebased M35-Kandidat enthält exakt den bewiesenen Fix.

## LETZTER SICHERER POSITIVER REFERENZSTAND

- `d841ed7590436ac100b98f15194874573e09bc03`: 7/7 frisch produziert;
- `de21f6cd35c60849c551fd82f78e75ce57c99fab`: 7/7 + 107008 Review PASS.

`RECOVERY_BASE_SHA = de21f6cd35c60849c551fd82f78e75ce57c99fab`.

## OFFEN / NICHT BEHAUPTET

- serverseitiger vollständiger M01–M35-PASS des fresh M35-Kandidaten noch offen;
- M35 noch nicht gemergt;
- kein neuer 7/7-Realtest;
- kein Publish;
- keine WordPress-Schreibaktion.

## ZIEL

Unverändert:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`.

Kein Auto-Publish.
