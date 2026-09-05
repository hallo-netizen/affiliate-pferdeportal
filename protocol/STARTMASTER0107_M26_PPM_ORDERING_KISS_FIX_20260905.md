# STARTMASTER0107 – M26 / PPM-Reihenfolge KISS-Fix – 05.09.2026

## Scope

Nur Hobbyraum-Branch `hobbyroom/m01-m33-executable-regression-suite`.
`main` unverändert.

Keine Änderung an:
- Textmaschine / verbindlichem Texterstellungsprompt
- Beitragsarten-/Regelpaket
- PPM 6.7.9 selbst
- PSERC / PSTE
- Link-/Tabellen-/SEO-/Designregeln
- Signer-Grenze
- 107008
- WordPress / Publish
- Cloud Entry / immutable Gates

## Chronologisch belegter Root Cause

1. `d841ed7590436ac100b98f15194874573e09bc03`
   - realer 7/7-Lauf erzeugte alle sieben Artikel und zwölf Stage-Ergebnisse je Artikel;
   - spätere Wiederholung erreichte 107008.
   - PR #107 Laufbelege: Kommentare 5533993233 / 5534778649.

2. `de21f6cd35c60849c551fd82f78e75ce57c99fab`
   - realer 7/7-Lauf + 107008 PASS;
   - späterer Blocker erst GitHub-Endstempel/Auth.
   - PR #107 Kommentar 5536771612.

3. `6818cc89a8806d9059467a341b3fc31d22b6c3ea`
   - echter PPM-6.7.9-Nachweis wurde zwingend;
   - Validator verlangte bereits finalen PPM-Report/content_hash.

4. `9d7fe0a43a022f873a10da290b94cb2fd8ebcda2`
   - realer PPM-Aufruf wurde in den bestehenden `fachworkflow_proof_handoff.py` eingebaut.

5. `9aabd213ade9c9b4f4f0a611f7115a2897af7b66`
   - bestehender Handoff wurde in Current Action sichtbar.

6. Danach:
   - PPM-Paketpfad wurde gebunden;
   - reale Läufe kamen bis `BOUND_RUNTIME_PRODUCTION_CONTEXT_MISSING`;
   - später bis `BOUND_CURRENT_FACHWORKFLOW_EXECUTION_CONTEXT_MISSING`.

## Exakter Kreisschluss vor diesem Fix

Der Hobbyraum-Stand vor dem Fix verlangte vor `submission_command` bereits ein Vorab-`ITEM_RECEIPT` mit `pre_submit_context`.
Damit hing der echte PPM indirekt an einer bereits materialisierten Vorstufe, während `FACHWORKFLOW_PASS`/finales Receipt semantisch erst NACH echtem PPM gültig sein dürfen.

Zusätzlich beschrieb `ppm679_requirement` vor PPM bereits Felder des noch nicht existierenden PPM-Reports.

## KISS-Lösung

Keine neue Architektur und kein neuer Contract.

Verwendet wird ausschließlich der bereits vorhandene:
`PFERDE_ATELIER_FACHWORKFLOW_HANDOFF_REQUEST_V1`.

Neue Reihenfolge:

```
bestehender Fachworkflow / Textmaschine unverändert
→ realer aktueller fact_pack + production_plan/workflow_release-Kontext
→ finaler Artikel + reale Nicht-PPM-Stages
→ PPM-Stage nur als noch NICHT bestandener Eingang:
   final_article_ref + final_article_sha256
→ bestehender FACHWORKFLOW_HANDOFF_REQUEST_V1
→ genau eine submission_command
→ bestehender fachworkflow_proof_handoff intern
→ echter PPM 6.7.9
→ PPM content_hash == finaler Artikel-SHA
→ finaler PPM-Proof
→ erst jetzt FACHWORKFLOW_PASS
→ erst jetzt finales ITEM_RECEIPT
→ bestehende Room-Bridge
```

Der Worker führt keinen separaten Handoff-Befehl und keinen `submit-request` aus.

## Geänderte Produktionsdateien

1. `control/single-door-boundary/codex_current_action.py`
   - Vorab-Receipt/`pre_submit_context` entfernt.
   - vorhandenen Handoff-Request als Datenübergabe gebunden.
   - `submission_command` bindet exakt diesen Request.
   - Current Action validiert Request gegen aktuellen Artikel/Slot/Batch/Root/Contract.
   - bestehender Handoff wird intern ausgeführt.
   - PPM-Anforderung getrennt in:
     - pre-PPM: `final_article_ref`, `final_article_sha256`
     - final: vollständige PPM-6.7.9-Bindung inkl. Report-Hash.

2. `control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json`
   - nur Ausführungsreihenfolge präzisiert.
   - kein Vorab-`FACHWORKFLOW_PASS`, kein Vorab-`ITEM_RECEIPT`.
   - kein separater Handoff-Befehl, kein zweiter Executor, keine Capability-Suche.

3. Hash-Nachziehung:
   - `CURRENT_STATE.json`
   - `PFERDE_ATELIER_START_HERE.json`

## Geänderte Tests / Matrix

- `HOBBYRAUM_M01_M33_REGRESSION.py`
- `HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md`
- `test_ppm679_current_action_binding.py`

Keine neue Matrix, kein neuer Runner.

## Unveränderte Kernbeweise

- Texterstellungsprompt Git-Blob:
  `9238db0cfb94d9b354ca60bc3b745861daa51fd7`
- Article-Type-Templates SHA-256:
  `dc79a6d7d30fba2f7f13c80d35bf4d137669f2b3469d7bc28a5d0873858f192f`
- PPM 6.7.9 Package SHA-256:
  `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`
- `fachworkflow_proof_handoff.py` wurde durch diesen Fix nicht verändert.

## Prüfstatus

Implementierungs-Head vor diesem Protokoll:
`648d5ff11a94abbf33aac961063a7d08b0912699`

GitHub Actions auf diesem Head:
- `hardlock`: PASS
- `hardlock-base`: FAIL

Der `hardlock-base`-FAIL ist kein neuer Fixfehler:
- gleicher FAIL bereits auf vorherigem Hobbyraum-Head
  `65d5b50273a588895af289dda075b6820e0c48e8`;
- Ursache laut GitHub-Log: bereits vorhandene Änderung an geschütztem `AGENTS.md` gegenüber main.

Wichtig:
Der komplette M01–M33-Runner wurde in dieser Sitzung noch NICHT real auf dem finalen Head ausgeführt, weil:
- kein bestehender GitHub-Workflow diesen Runner ausführt;
- es wurde bewusst kein neuer Workflow gebaut;
- lokaler Container konnte GitHub nicht per DNS erreichen.

Daher kein falsches `GESAMT PASS`.

## Noch notwendiger Realbeweis

Vor Merge weiterhin:
1. M01–M33 auf exakt finalem Hobbyraum-Head real ausführen.
2. Danach echter frischer 7/7-E2E.
3. Erst bei 7/7 + 107008 PASS Merge-Kandidat.
4. Kein Auto-Publish.
