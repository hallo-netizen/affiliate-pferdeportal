# P27 – BESTEHENDER CODEX-START + BESTEHENDE FACT-PACK-/DATEIÜBERGABE

Datum: 2026-09-08
Status: GO

## Wichtige Nutzer-Vorgaben

Bereits vorhandene Infrastruktur muss wiederverwendet werden:

1. Codex ist bereits aus jedem Chat startbar, auch aus der Artikelerstellung.
2. Die korrekte Dateiübergabe ist bereits im Workflow implementiert.

Keine neue Entry-/Runner-/Handoff-Architektur bauen.

## Harte Prüfung gegen aktuellen autoritativen main-Stand

Getesteter main-Commit:
`78bb2576214a8c0a82d201ed35530ad9ac885481`

Der Alternativbranch blieb dabei unverändert.
Der aktuelle main-Stand wurde nur in einem temporären read-only Git-Worktree geprüft.

## Ergebnis

PASS.

### Fact-Pack-Produzent
Im aktuellen 107007 ist ausdrücklich gebunden:

`CURRENT_BOUND_CODEX_FACHWORKFLOW_WORKER`

Dieser Worker erzeugt die realen aktuellen Fachworkflow-Ausgaben selbst:
- Recherche / fact_pack
- finaler Artikel
- production_plan-Kontext
- workflow_release-Kontext
- reale Stage-Artefakte/Proofs

Damit:
KEIN neuer Fact-Pack-Produzent nötig.

### Codex-Start
Bestehender Current-Action-Weg wird wiederverwendet.

Selftest:
`CODEX_CURRENT_ACTION_KISS_SELFTEST_PASS`

Belegt u.a.:
- current Codex ist gebundener Fachworkflow-Worker
- kein separater Fachworkflow-Executor
- keine separate Capability
- echte Outputs müssen erzeugt werden
- Worker darf PASS nicht selbst attestieren
- content_or_quality_authority = NONE
- publish_allowed = false

### Dateiübergabe
Bestehender:
`FACHWORKFLOW_HANDOFF_REQUEST.json`

wird wiederverwendet.

Feldliste exakt und nicht zur Laufzeit wählbar:
16 feste Felder:
- contract
- room_token
- batch_sha256
- canonical_article_id
- plan_slot
- allowed_output_root
- item_receipt_ref
- fachworkflow_pass_ref
- contract_binding_ref
- contract_binding_sha256
- stage_proofs
- fact_pack
- production_plan_item
- production_plan_header
- workflow_release_item
- workflow_release_metadata

Kein zusätzliches Feld, kein fehlendes Feld.

Bestehende Handoff-Unittests:
2/2 PASS.

## Architekturfolge

Die Zentralmaschinen-Alternative erfindet NICHT:
- Codex-Start
- Worker-Entry
- Fact-Pack-Handoff
- Dateiübergabeformat
- zweiten Executor

Sie verwendet diese vorhandenen technischen Infrastrukturpunkte nur als fest gebundene Ein-/Ausgangsgrenze.

## Isolation

Der Test hat main read-only geprüft.
Der Alternativbranch wurde nicht mit main gemergt.
Keine produktive Datei wurde verändert.

## GO/STOP

GO.

Nächster Schritt P28:
finales Design/Visual-Gate im bestehenden unveränderten Fachworkflow identifizieren und prüfen, ob es deterministisch/fail-closed ohne freie AI-/Chatentscheidung umgesetzt ist.

Keine neue Designlogik bauen.
