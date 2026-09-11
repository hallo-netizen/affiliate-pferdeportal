# PFERDE ATELIER – TEXT – CURRENT STATE

STAND: 2026-09-11
STATUS: BLOCKED / M37 PRODUCT_FIX ACTIVE

## EINE AKTUELLE WAHRHEIT

Current technical main:
`f791dcc6c926f9c136faed29957e64786ffca08e`

Letzter belastbarer Live-/Recovery-Baseline-Stand:
`bb005a5324a0a6270aacb52b5927613bde1ab4bc`

Aktuelle autoritative Fehlerquelle:
`QUELLEN_AKTUELL/04_FEHLERLISTE_KOMPLETT_AKTUELL_20260911.md`

Vorgänger `QUELLEN_AKTUELL/04_FEHLERLISTE_KOMPLETT_AKTUELL_20260905.md` ist nur historische Langfassung und keine CURRENT-Wahrheit mehr.

## AKTUELLER REALBLOCKER

Der letzte frische Lauf recherchierte und erzeugte den ersten Artikel und erreichte den echten PPM-6.7.9-/PSERC-Handoff.
Sichtbarer äußerer Stop:

`PPM679_REAL_EXECUTION_BLOCKED`

Der konkrete bereits vorhandene innere Bridge-Grund wurde vom äußeren Handoff nicht sichtbar erhalten. Der ursprüngliche Codex-Task ist nicht mehr verfügbar.

**Produktions-Rootcause bleibt UNKNOWN.**
Nicht raten und keinen PPM-/PSERC-Fehler erfinden.

## REGRESSION

M01–M37 sind jetzt die verbindliche bekannte Regression.

History-Phase M37: **PASS / integriert**.
- PR248
- History-Head `245b596f9d6dd67c759527a0f211dbe957f4e34f`
- Merge/Main `f791dcc6c926f9c136faed29957e64786ffca08e`
- `HOBBYROOM_HISTORY_REPRODUCTION_PASS:M37`
- `HOBBYROOM_HISTORY_MACHINE_PROOF_PASS:M37`
- hardlock PASS
- hardlock-base PASS

## AKTIVER PRODUKTFIX

PR247 / Branch:
`hobbyroom/ppm-inner-reason-visibility-20260911`

Head:
`59ad44da3d89769c05f0725f9929135b0262f4dd`

Diff exakt vier Dateien:
- `control/startmaster0107/fachworkflow_proof_handoff.py`
- `control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json`
- `control/startmaster0107/CURRENT_STATE.json`
- `control/startmaster0107/PFERDE_ATELIER_START_HERE.json`

Matrix und Runner kommen unverändert aus Main.

Fix-Grenze:
- nur Observability;
- Handoff bleibt BLOCKED;
- vorhandenen ersten inneren nicht-reparierbaren PPM/PSERC-Grund erhalten;
- nichts erfinden;
- reparierbare Content-Codes bleiben RepairRequired;
- Hashkette nachziehen.

## PASS-GRENZE PRODUKTFIX

Der vorhandene hardlock-base muss auf PR247 beweisen:
1. current main reproduziert M37 als ersten FAIL;
2. Kandidat läuft mit demselben bestehenden M01–M37-Runner vollständig `GESAMT PASS`;
3. `HOBBYROOM_HISTORY_MACHINE_PROOF_PASS:M37`;
4. hardlock + hardlock-base PASS auf demselben Head.

Erst danach Integration.

## DANACH

Genau einen frischen ersten Artikel über den gebundenen 107007-Weg bis zum echten PPM/PSERC-Handoff laufen lassen.
Dann nur den ersten konkret sichtbar gewordenen inneren Grund bearbeiten.
Kein neuer 7/7-Lauf vor dem Ein-Artikel-Beweis.

## HARTE GRENZEN

- kein neuer Runner/Gate/Controller/Sidecar;
- keine PPM-/PSERC-/PSTE-/Textmaschinen-/Recherche-/SEO-/Link-/Tabellen-/Designregel ändern;
- kein Fake-Rootcause;
- keine Reparatur während des Produktionslaufs;
- kein WordPress-Write;
- Kein Publish.
