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


## Reale Prinzipprüfung mit synthetischen Artikeln – 05.09.2026

Ziel dieser Prüfung war ausschließlich die technische Reihenfolge
`Fachworkflow-Ergebnisse -> echter PPM 6.7.9 -> FACHWORKFLOW_PASS -> ITEM_RECEIPT`.
Sie ist **kein Ersatz für den späteren realen 7/7-Produktionslauf**.

### Originalpakete

Für die Prüfung wurden die bereits archivierten Originalpakete bytegenau rekonstruiert und vor Ausführung geprüft:

- PPM 6.7.9:
  - Größe: 1.614.485 Byte
  - SHA-256: `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`
- PSERC-FIX:
  - Größe: 304.064 Byte
  - SHA-256: `77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314`

Keine Ersatzimplementierung und kein Fake-PPM wurden für die Positivläufe verwendet.

### Positive reale PPM-Läufe

Vier synthetische Artikel wurden an echte vorhandene PPM-Plan-Slots gebunden und jeweils vollständig durch den realen
`PSERC_PPM_Intake_Bridge::execute -> PPM679_Normal_Draft_Pipeline::execute_plan`
geführt.

1. FAQ
   - finaler Artikel-SHA: `075b125e243205581639b84b1b499f9509f6f91389407aedbbe6d1aa5e8ac995`
2. Beratung
   - finaler Artikel-SHA: `906345ed98a6a2547f45e3da6d1f8de87daa930c5ad207ce4d05d5cb25f02b87`
3. Vergleich
   - finaler Artikel-SHA: `240da0b1d3eb411b8ef6c2d3c0cd346277f7bdf4aadccfa355e09d4f9723b9b6`
4. Pflege
   - finaler Artikel-SHA: `e0ccf15f6b8c8731ae86d626735cd4b52614c765dda9639fbd96f396d05785c6`

Für alle vier:
- vor PPM kein `FACHWORKFLOW_PASS`,
- vor PPM kein finales `ITEM_RECEIPT`,
- echter PPM 6.7.9 ausgeführt,
- PPM-Status:
  `NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH`,
- `PPM content_hash == finaler Artikel-SHA`,
- erst danach `FACHWORKFLOW_PASS`,
- erst danach finales `ITEM_RECEIPT`,
- `publish_allowed=false`.

Ergebnis: **4/4 POSITIV PASS**.

### Negative reale Prüfungen

1. fehlender aktueller Fachworkflow-Kontext:
   - korrekt BLOCKED:
     `BOUND_FACHWORKFLOW_PRODUCTION_CONTEXT_MISSING`
2. falscher finaler Artikelhash:
   - korrekt BLOCKED:
     `PPM679_FINAL_ARTICLE_HASH_MISMATCH`
3. vorgefertigter PPM-Report:
   - korrekt BLOCKED:
     `PPM679_PREGENERATED_REPORT_FORBIDDEN`
4. nur behaupteter Fake-PPM-PASS ohne echte PPM-Bindung:
   - erster Test deckte auf, dass der Handoff diesen Fall zunächst materialisieren konnte,
     obwohl der nachgeschaltete Current-Action-Validator ihn später mit
     `PPM679_REAL_BINDING_MISSING` blockierte.
   - Das war für einen sicheren Fail-Closed-Übergang nicht ausreichend.

### Daraus entstandener enger KISS-Fix

In `fachworkflow_proof_handoff.py` wurde ausschließlich für `stage == "ppm"` hart gemacht:

- `ppm679_binding` muss vorhanden sein,
- andernfalls sofort:
  `PPM679_REAL_BINDING_MISSING`,
- der echte PPM-Pfad wird zwingend ausgeführt,
- erst danach darf der PPM-Proof PASS werden.

Commit:
`c8d471661fca98fd9e404c0f10b8a183f6764d6d`

Vorhandener Handoff-Test wurde entsprechend ergänzt:
`1724e264cdb446c719b6324256d73ab765e3d0af`

Danach komplette Prinzipserie erneut:
- **4/4 POSITIV PASS**
- **4/4 NEGATIV PASS**

Aktueller Handoff-SHA-256:
`e35cb7eb7ff9b2526b0b54f3ab402a8c5cb0a5dc9329206c5551e92a8889ec82`

107007- und Root-Hashbindung wurden anschließend erneut aktualisiert.

### Aussage dieses Beweises

Belegt ist jetzt:
**Der technische PPM-/PASS-Kreisschluss ist im Hobbyraum beseitigt und der Übergang arbeitet mit dem echten PPM 6.7.9 fail-closed.**

Noch nicht belegt:
**der vollständige reale 7/7-Produktionsworkflow auf diesem Hobbyraum-Stand.**
