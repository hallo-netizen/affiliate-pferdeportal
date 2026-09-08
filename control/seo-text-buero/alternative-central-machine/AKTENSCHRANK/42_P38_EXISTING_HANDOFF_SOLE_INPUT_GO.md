# P38 – BESTEHENDE HANDOFF-DATEI IST DIE EINZIGE PRODUKTIONS-EINGANGSWAHRHEIT

Datum: 2026-09-08
Status: GO

## Ergebnis

Der aktuelle reale Workflow besitzt bereits exakt eine geeignete Übergabedatei:

`FACHWORKFLOW_HANDOFF_REQUEST.json`

Vertrag:
`PFERDE_ATELIER_FACHWORKFLOW_HANDOFF_REQUEST_V1`

Exakt 16 Pflichtfelder.

Die realen Identitäten sind bereits enthalten:
- batch_sha256
- canonical_article_id
- plan_slot

Der komplette Produktionskontext ist bereits enthalten:
- fact_pack
- production_plan_item
- production_plan_header
- workflow_release_item
- workflow_release_metadata

Zusätzlich:
- Stage-Proofs
- Contract-Binding + Hash
- gebundene Output-Pfade
- Receipt-/PASS-Refs

## Harter Befund

- new_handoff_file_required = false
- new_handoff_format_required = false
- new_job_manifest_required_for_target_architecture = false
- prototype_signed_job_manifest_role = LAB_TEST_ONLY
- publish_allowed = false

Damit entfällt im Zielbetrieb das zusätzliche signierte Jobmanifest aus P10/P34/P36.

Es war ausschließlich Laborwerkzeug zum Beweis von Reihenfolge, Skalierung und Manipulationsschutz.

## KISS-Zielbild wird kleiner

Nicht:

Chat -> neues Jobmanifest -> neue Übergabe -> Controller -> Handoff

Sondern:

`bestehender Chat/Codex -> bestehende FACHWORKFLOW_HANDOFF_REQUEST.json -> dünne Zentralsteuerung`

Genau eine Übergabewahrheit.

## Noch zwingend zu prüfen

Der heutige vorhandene `fachworkflow_proof_handoff.py materialize` ruft den realen PPM-Pfad auf.

Da der bestehende PPM-Normal-Draft-Gesamtpfad Drafts erzeugen kann, muss vor Übernahme in die Zielarchitektur geprüft werden:

Kann die Zentralmaschine aus der bestehenden Handoff-Datei zuerst den schreibfreien PPM-`prepare()`-Stand erzeugen, dann extern signieren, und ERST DANACH den Draft schreiben?

Wenn der heutige materialize-Befehl vor der externen Signatur bereits schreibt:
nicht einfach übernehmen.

Keine neue Handoff-Datei bauen.
Nur den Verarbeitungspunkt hinter derselben bestehenden Datei korrigieren/abbinden.
