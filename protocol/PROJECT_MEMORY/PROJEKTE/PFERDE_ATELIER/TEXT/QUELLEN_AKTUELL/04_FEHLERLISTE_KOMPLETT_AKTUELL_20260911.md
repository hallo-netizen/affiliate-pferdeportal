# STARTMASTER0107 – KOMPLETTE AKTUELLE FEHLERLISTE – 17.09.2026

STATUS: AUTORITATIVE AKTUELLE FEHLERQUELLE

VORGÄNGER NUR HISTORISCHER LANGBELEG:
`04_FEHLERLISTE_KOMPLETT_AKTUELL_20260905.md`

## AKTUELLE LIVE-WAHRHEIT – 17.09.2026

Current main / technischer M38-Baseline-Stand:
`f1d1605f18bd23d9189f89ad173598958718d08a`

Letzter belastbarer Live-Baseline-/Recovery-Stand vor M37:
`bb005a5324a0a6270aacb52b5927613bde1ab4bc`

M01–M37 sind verbindliche bekannte Regression und integriert.
M38 ist der aktuell offene History-Fall und noch **nicht** als Produktfix freigegeben.

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

## AKTUELLER PRODUKTIONSSTATUS / M38

Der erste frische Artikel erreichte nach realer LanguageTool-Reparatur den echten PPM-6.7.9-/PSERC-Handoff. Er stoppte mit dem belegten ersten technischen Blocker:

`PPM679_REAL_EXECUTION_BLOCKED:PSERC_BRIDGE_PPM_PLAN_VERSION_MISMATCH`

Zweiter Artikel wurde nicht gestartet. 107008 wurde nicht erreicht. Kein WordPress-Write, kein Publish.

Die bestehende autorisierte Abschlusslogik enthält für den akzeptierten `production_plan_v4`-Header bereits die Versionsbindungen:
- `plan_contract_version == "4.0.0"`
- `required_plugin_version == "6.7.9"`

M38 prüft, ob der current Fachworkflow diese beiden gebundenen Versionsfelder im real erzeugten `production_plan_header` erhält und der Handoff sie fail-closed vor dem realen PPM/PSERC-Aufruf prüft.

## VERBINDLICHE REGRESSION M01–M38

M01–M37: historisch / Regression / integriert.
M38: current Fachworkflow production-plan version binding / **HISTORY_AUTHORITY_MAINTENANCE OFFEN**.

History-Kandidat:
- PR249;
- Branch `hobbyroom/m38-plan-version-history-20260911`;
- ausschließlich bestehende Fehlermatrix + bestehender Regressionrunner;
- erwarteter Maschinenbeweis: Main M01–M37 PASS, M38 erster neuer FAIL;
- kein Produktfix in dieser Phase.

Erst nach maschinellem M38-History-Beweis darf ein separater kleinstmöglicher Produktfix erfolgen. Danach genau ein frischer erster Artikel durch reales LanguageTool + reales PPM/PSERC; erst nach Einartikel-PASS Restbatch bis 107008; vor Publish stoppen.
