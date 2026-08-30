# STARTMASTER0107 – Runtime-Lifecycle-Finalfix

Stand: 2026-08-30

## Scope

Ausschließlich die zwei im vollständigen 21-Punkte-Gesamtworkflow-Test gefundenen Lifecycle-Lücken:

1. fehlender wiederverwendbarer Binder für neue Runtime-Batches,
2. fehlendes Leeren/Re-Arm des permanenten 107007-Slots nach 107008.

Keine Fach-, Inhalts-, Qualitäts-, SEO-, Design-, PPM-, PSTE-, PSERC-, LanguageTool- oder Publish-Regel wurde geändert. Kein neuer Artikel wurde erzeugt oder veröffentlicht.

## Implementierung

- `runtime_batch_slot_lifecycle.py` bindet einen aktuellen READY-Snapshot fail-closed als neue Generation.
- Produktionspaket kann direkt gemeinsam oder nachgelagert gebunden werden.
- Snapshot, Batch und Produktionspaket werden durch den bestehenden Runtime-Guard vollständig validiert.
- Nach finalem Review löscht `clear-after-review` ausschließlich die aktuelle Runtime-Generation und setzt den Slot auf `NO_ACTIVE_BATCH` zurück.
- Der Entrance Gate Controller darf nur beim explizit gebundenen finalen `final_rearm` und nur nach erfüllter JSON-Precondition auf den im State hashgebundenen 107007-Rearm-Target zurückkehren.
- Ohne vorheriges Leeren des Runtime-Slots ist der Re-Arm fail-closed blockiert.

## Lokale Positivtests

Bestehender `cloud_repo_ci_test.py`: PASS.

Lifecycle positiv/negativ: PASS.

Historischer echte 6er-Fixture-Durchlauf:

- Batch SHA-256: `3669e186f2464d081cf0dd3188203f9fdbe20a23b5e30ae4a0ea3c2d24ea7b8f`
- Package ID: `1bffe5aced0751f4155a395ad3cdbb5debd100f8e651b8a53d7972809024ad94`
- Binder → `RUNTIME_BATCH_EXECUTION_READY`: PASS
- Runtime Guard → `RUNTIME_INPUTS_BOUND`: PASS
- 107007 Entrance → PASS
- 107007 PASS → ausschließlich 107008: PASS
- `clear-after-review` → `RUNTIME_SLOT_CLEARED_AND_IDLE`: PASS
- 107008 PASS → `FINAL_STEP_PASS_REARMED`: PASS
- erneuter Entrance → 107007: PASS
- Runtime Guard danach → `READY_IDLE`: PASS

## Negativtest

107008-PASS ohne vorheriges Leeren des Runtime-Slots:

`FINAL_REARM_PRECONDITION_MISMATCH:0:status`

Ergebnis: PASS – Re-Arm wird korrekt blockiert.

## Relevante SHA-256

- `runtime_batch_slot_lifecycle.py`: `3ba63de1dd28182bff1a3472db5519b7c5a1c8aaa62c7c0885cae4ebf17fe837`
- `RUNTIME_BATCH_SLOT_CONTRACT_V1.json`: `e3e2e40b022f3976289b4ccd9fbe1b447c6e8ce39e6cbf151a6ccaeb40a9696a`
- `STEP_107008...json`: `cf14a65af9057da6439799aa2666a8ae9e472919711396b56a5f4710324bd68e`
- `STEP_107007...json`: `ff4fc9387023277bb41e42fb57c08a3f2d222b74299df252d40faa243e02f2e8`
- `CURRENT_STATE.json`: `27aae78f328b5f1378da76e50c8f00ab4c2a49c1b481985d5420d35e639f8004`
- `PFERDE_ATELIER_START_HERE.json`: `86ce3bd476dc83fe1da3e17590341eb13e9dc30720684c7d65a5fd025440ecf4`
- lokaler neuer `cloud_entry.py`: `49fcaaacf40c29a616232a421fc2254e4cecefd8d0030f2b54a789dba376ab85`

## Erwarteter Endzustand

Nach jedem erfolgreich reviewten Batch:

`107008 PASS → Runtime NO_ACTIVE_BATCH → 107007 ARMED/IDLE`

Der nächste Produktionslauf benötigt keine dauerhafte Artikelbindung und keinen neuen Workflow-Step.
