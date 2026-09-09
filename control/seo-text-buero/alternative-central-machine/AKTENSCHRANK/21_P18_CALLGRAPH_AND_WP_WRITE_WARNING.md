# P18 – INTERNE NORMAL-DRAFT-DELEGATION

Datum: 2026-09-08
Status: TEIL-GO MIT ARCHITEKTUR-WARNUNG

## Callgraph ab execute_plan

Erreichbare interne Methoden:
- execute_plan
- bootstrap
- generate_all
- check_all
- create_drafts
- readback
- abort_run
- block_run
- result
- id_value

Wichtige feste Delegationen:

### generate_all
ruft:
`PPM679_Content_Generator::generate`

### check_all
ruft:
`PPM679_Content_Validator::check`
und
`PPM679_Fail_Closed_Aggregator::aggregate_item_results`

### create_drafts
ruft:
`PPM679_Normal_Draft_Adapter::prepare`
und
`PPM679_Normal_Draft_Adapter::create_draft`

### readback
ruft:
`PPM679_Normal_Draft_Readback_Validator::validate_batch`

### execute_plan selbst
bindet u.a.:
- Editorial Plan Runtime Gate
- Live State Gate
- Plan Validator
- No-Publish-Endstatus

## KISS-Befund zu Fachprüfungen

P17s fehlende direkte Link-/Language-/SEO-/Design-Namen in execute_plan bedeuten nicht automatisch, dass diese Prüfungen außen gebaut werden müssen.

`check_all` besitzt bereits genau einen zentralen Fachprüf-Einstieg:
`PPM679_Content_Validator::check`
mit anschließendem Fail-Closed-Aggregator.

Diesen bestehenden Validatorpfad zuerst weiterverfolgen.
Keine externen Doppel-Gates bauen.

## WICHTIGE ARCHITEKTUR-WARNUNG

Der reale Normal-Draft-Pfad enthält:
`PPM679_Normal_Draft_Adapter::create_draft`

Damit liegt die WordPress-Draft-Erzeugung im heutigen Normal-Draft-Pfad innerhalb der Pipeline.

Das kann mit dem Ziel der Alternativarchitektur kollidieren:

gewünschtes Ziel:
fertiger geprüfter Dateioutput
-> externe Signatur
-> WordPress-Eingangsprüfung
-> erst dann WordPress-Write

Wenn der einzige reale PPM-Pfad zwingend bereits vorher WordPress schreibt, darf er NICHT einfach 1:1 als Produktionsbaustein übernommen werden.

## Konsequenz

Vor weiterer Fachgate-Detailanalyse wird zuerst geprüft:

Gibt es im unveränderten PPM bereits einen echten
CHECK_ONLY / NO_WRITE
Weg, der denselben fachlichen Prüfpfad ausführt, ohne WordPress-Draft zu erzeugen?

Wenn JA:
diesen vorhandenen Weg verwenden; keine PPM-Änderung.

Wenn NEIN:
STOP und Architekturentscheidung erforderlich.
Nicht PPM verändern.
Nicht neue Umgehungslogik bauen.

## P19

Read-only Prüfung des unveränderten PPM:
- check_only
- draft_allowed
- create_drafts-Bedingung
- Normal_Draft_Adapter
- vorhandene No-Write-/Check-only-Tests

Keine Änderung an PPM/Textmaschine.
