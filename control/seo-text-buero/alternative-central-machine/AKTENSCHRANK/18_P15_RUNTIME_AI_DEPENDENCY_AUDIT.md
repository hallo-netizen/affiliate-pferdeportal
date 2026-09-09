# P15 – RUNTIME-AI-/EXTERNABHÄNGIGKEITS-AUDIT

Datum: 2026-09-08
Status: TEIL-PASS / P16 ZWINGEND

## Harte Ergebnisse

Ausführbare PPM-/PSERC-/PSTE-Dateien wurden auf:
- Claude
- Anthropic
- OpenAI
- ChatGPT/GPT/LLM
- API-/Netzwerkaufrufe

geprüft.

Ergebnis:
- runtime_network_hit_count = 0
- kein api.anthropic
- kein api.openai
- kein wp_remote_post/get zu AI
- kein curl/API-Aufruf zu externem AI-Reviewer

Damit existiert im geprüften Code KEIN automatischer Live-Aufruf zu Claude/OpenAI.

## Aber: Reviewer-Status ist in ausführbarem PPM-Code vorhanden

Mehrere Dateien enthalten ausdrücklich:
- PENDING_CLAUDE_REVIEW
- independent Claude review
- external_claude_review_required=true
- PASS_LOCAL_STRUCTURAL_PENDING_CLAUDE
- BASELINE_PLUS_HASHED_DELTA_REQUIRES_EXTERNAL_CLAUDE

Besonders:
- includes/three-type-bundled-local-preflight.php
- includes/three-type-bundled-release-validator.php
- includes/three-type-local-content-validator.php
- includes/content-structure-language-gate.php

## Bestehende Tests

Ohne externe AI-/Netzwerkverbindung erfolgreich:

- test-mainblock1-link-targets.php -> PASS
- test-mainblock1-g9-corrected-candidate.php -> PASS, aber ausdrücklich:
  external_claude_review_required=true
  external_pass_claimed=false
- test-wave2-content-mutations.php -> PASS; Manipulationen fail-closed
- test-v38-editorial-plan-journal-dedup.php -> PASS
- test-v31-status-wording-governance.php -> PASS

## Bewertung

### Kein heimlicher Live-AI-Aufruf
PASS.

### 0,0 freie Reviewautorität im gesamten PPM-Paket
NICHT BEWIESEN.

Das Paket enthält Modi, die einen externen unabhängigen Claude-Review als noch offene Qualitätsstufe modellieren.

Wenn dieser Review im aktuell verwendeten Normal-Draft-Produktionspfad zwingend wäre, kollidiert das mit der Zielanforderung:
kein frei entscheidender externer Reviewer.

Wenn diese Claude-Pfade dagegen nur andere/ältere Produktionsmodi betreffen und der aktuelle gebundene Normal-Draft-Pfad seine Fachregeln vollständig deterministisch bzw. durch bereits gebundene Evidence prüft, ist der aktuelle Zielweg nicht betroffen.

## P16 – zwingende Pfadprüfung

Nur den aktuell relevanten realen Pfad untersuchen:

`PSERC_PPM_Intake_Bridge::execute -> PPM679_Normal_Draft_Pipeline::execute_plan`

Prüfen:
1. Verwendet genau dieser Pfad Claude-/External-Review-Status?
2. Enthält dessen Normal-Draft-Fixture Claude-Evidence?
3. Kann Normal-Draft ohne Claude-Vermerk vollständig CONTENT_QUALITY_CHECK_OK erreichen?
4. Welche LanguageTool-/Link-/Table-Evidence verlangt exakt dieser Pfad?

Kein Umbau.
Keine Regeländerung.
Keine Ersatzprüfung.

Bis P16:
P15 = TEIL-PASS.
