# P31 – USER-VISUAL-AUTORITÄTSGRENZE

Datum: 2026-09-08
Status: GO FÜR AUTOMATISCHEN PRODUKTIONSKERN

## Harte Ergebnisse

Exakter Normal-Draft-Pfad:
- Pipeline: kein User-Visual-Bezug
- Content Validator: kein User-Visual-Bezug
- Normal-Draft Adapter / prepare/create_draft: kein User-Visual-Bezug
- Readback: kein User-Visual-Bezug

Echter 1–4-Draft-Lauf:
4/4 erreichen
`NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH`

ohne User-Visual-PASS.

## Ergebnis

User Visual blockiert NICHT:
- CONTENT_QUALITY_CHECK_OK
- prepare()
- create_draft()
- Normal-Draft-Endstatus

User Visual ist separat NACH dem maschinellen Rendered-DOM-PASS.

Ein technischer FAIL kann durch User Visual nicht zu PASS gemacht werden.

## Bedeutung für 0,0 Freiheit

GO.

Die automatische Produktionsmaschine kann vollständig bis zum geprüften, signierten, geschriebenen und maschinell DOM-validierten Draft laufen, ohne menschliche/KI-Entscheidung.

Die separate User-Visual-/Content-Abnahme:
- liegt außerhalb der technischen Produktionsautorität
- verändert keinen technischen PASS
- kann keinen FAIL überstimmen
- bleibt mit `publish_allowed=false` verbunden

Damit beeinflusst sie nicht die erzeugte Textqualität oder den Produktionsweg.

## Capture

Der bestehende PPM kann deterministisch Capture-Aufträge vorbereiten:
- Desktop 1440x1200
- Mobile 390x844
- Post-ID + Readback-Hash gebunden
- HTTP_RESPONSE_AFTER_WORDPRESS_RENDER

Der lokale Test behauptet korrekterweise keine echte Server-Capture, wenn sie nicht ausgeführt wurde.

## KISS

Keine neue visuelle KI.
Kein menschlicher Reviewer im Produktionspfad.
Vorhandene DOM-/Style-Validatoren bleiben maßgeblich.

## P32

Letzte Rollenklärung:
- PSTE
- PSERC
- aktueller gebundener Codex-Fachworker
- PPM

Ziel:
jede Komponente genau eine klar abgegrenzte Verantwortung; keine doppelte Workflowautorität.
