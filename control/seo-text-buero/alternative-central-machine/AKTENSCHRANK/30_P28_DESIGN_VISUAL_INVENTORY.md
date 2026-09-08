# P28 – DESIGN/VISUAL-AUTORITÄT INVENTUR

Datum: 2026-09-08
Status: GO ZU P29, NOCH KEIN AUSFÜHRUNGS-PASS

## Wichtiger Befund

Der bestehende Content-Structure-Language-Gate sagt ausdrücklich:

`no final editorial or visual PASS`

Das ist korrekt:
Der Text-/Content-Validator darf sich keinen finalen Visual-PASS selbst geben.

## Bestehende separate Visual-/Design-Autorität in PPM

Hard-Rule-Register enthält u.a.:

### HR-DOM-001
- Desktop/mobile real DOM pair and matching structure
- Validator: `Rendered DOM validator`
- Evidence: raw DOM pair
- Positivtest:
  `tests/qf03-wordpress-draft-readback-dom/test-qf03-rendered-dom-positive.php`
- Negativtest:
  `tests/qf03-wordpress-draft-readback-dom/test-qf03-rendered-dom-mutations.php`

### HR-DOM-002
- Rendered table computed styles match hard table rules
- Validator: `Table hard-rule validator`
- Evidence: computed style evidence
- vorhandener Positiv-/Negativtest

### HR-CONT-001
- Content validator + rendered DOM validator
- Evidence: source/readback/DOM

### HR-WP-001
- Draft only and exact post/readback hash
- Draft adapter + readback validator
- server readback

Weitere Wave4-Regeln binden explizit:
- wp-draft-adapter
- wp-readback-validator
- rendered-dom-validator

## PSERC/PSTE

PSERC untersagt eigene Content-/Format-/Design-Autorität:
- `text_machine_is_only_content_and_format_authority=true`
- `content_or_design_authority=false`
- `design_or_quality_payload_allowed=false`

PSTE:
- design_modified=false
- content_or_design_touched=false

Damit sind PSERC/PSTE keine freien Designworker.

## Architekturfolgerung

Design/Visual soll NICHT als neuer Worker vor dem Write gebaut werden.

Bestehender sinnvoller Pfad:

1. Fach-/Content-Prüfung
2. prepare()
3. externe Signatur
4. verifizierter Draft-Write
5. exakter Readback
6. vorhandener Rendered-DOM-/Computed-Style-Validator
7. design_format PASS oder BLOCKED
8. weiterhin kein Publish

Damit prüft das System das reale WordPress-Ergebnis statt eine KI visuell urteilen zu lassen.

## P29

Harter Test:
- Rendered DOM positiver Originaltest
- Rendered DOM Mutationen negativer Originaltest
- Rendered Table DOM Evidence Test
- Validatorcode auf Claude/GPT/LLM/human/manual/network prüfen

Wenn externe freie Reviewer-Autorität nötig:
STOP.

Wenn alles deterministisch/fail-closed:
design_format GO.

Keine Designregel ändern.
