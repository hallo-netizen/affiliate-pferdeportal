# P16 – EXAKTER NORMAL-DRAFT-PFAD / CLAUDE-FREIHEIT

Datum: 2026-09-08
Status: GO FÜR DEN AKTUELL GEPRÜFTEN NORMAL-DRAFT-PFAD

## Geprüfter Pfad

`PSERC_PPM_Intake_Bridge::execute -> PPM679_Normal_Draft_Pipeline::execute_plan`

Nicht das gesamte historische PPM-Paket als abstrakte Einheit.

## Harte Ergebnisse

### Normal-Draft-Testdateien
Claude/Anthropic/OpenAI/GPT/LLM-Treffer:
0

### PPM679_Normal_Draft_Pipeline
Claude/Anthropic/OpenAI/GPT/LLM-Treffer:
0

### nd_language_evidence
AI-/Claude-Treffer:
0

### nd_quality_binding
AI-/Claude-Treffer:
0

### Echter Originaltest
`tests/normal-draft-production/test-01-positive-1-to-4.php`

PASS:
- 1 Draft
- 2 Drafts
- 3 Drafts
- 4 Drafts

Status jeweils:
`NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH`

publish_allowed=false

## Schlussfolgerung zu P14/P15

Das PPM-Paket enthält andere Modi mit:
- PENDING_CLAUDE_REVIEW
- independent Claude review
- external Claude evidence

Diese Modi dürfen NICHT ungeprüft in die Alternativarchitektur übernommen werden.

Der aktuell geprüfte Normal-Draft-Produktionspfad zeigt diese Abhängigkeit dagegen nicht.

Daher:
- kein externer Claude-Worker im aktuellen Normal-Draft-Pfad erforderlich
- kein Live-AI-Review als Runtime-Voraussetzung gefunden
- P14-Freiheitsalarm ist für andere PPM-Modi real, aber nicht für den hier geprüften Zielpfad

## Harte Architekturregel daraus

Die Zentralmaschine darf nicht „PPM allgemein“ frei aufrufen.

Sie darf ausschließlich den exakt gebundenen, hashgeprüften Normal-Draft-Einstieg verwenden.

Andere PPM-Modi:
DENY, solange sie nicht separat gegen 0,0 Freiheit geprüft wurden.

Damit entsteht keine Moduswahl für Chat/Worker.

## KISS

PASS.

Keine Änderung an PPM.
Keine Entfernung von Claude-Regeln aus anderen Modi.
Keine neue Ersatzprüfung.

Nur der bereits funktionierende, freiheitsärmere Zielpfad wird als zulässige Schnittstelle gebunden.

## Nächster Schritt P17

Nur prüfen:
Welche der bestehenden Fachregeln erzwingt exakt dieser Normal-Draft-Pfad selbst?

Ziel:
- vorhandene interne Prüfungen wiederverwenden
- keine Doppel-Gates bauen
- fehlende externe Pflichtkomponenten sauber identifizieren

Keine Integration und keine Regeländerung.
