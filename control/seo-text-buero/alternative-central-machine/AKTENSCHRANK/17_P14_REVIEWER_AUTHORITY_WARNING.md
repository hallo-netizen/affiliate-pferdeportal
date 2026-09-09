# P14 – FREIHEITS-AUDIT DER BESTEHENDEN RULE-OWNER

Datum: 2026-09-08
Status: WARNUNG / P15 ERFORDERLICH

## Ergebnis

Im unveränderten PPM-Hard-Rule-Register:
- 52 unterschiedliche validator_or_reviewer-Angaben
- 20 Regeln mit verdächtigem AI-/Reviewer-Bezug

Besonders relevant:

### HR-LINK-002
- Regel: One hierarchy-up target and complementary targets
- validator_or_reviewer:
  `PPM679_WordPress_Link_Target_Validator + Claude`
- required_evidence:
  `snapshot + editorial review`

### HR-LINK-003
- Regel: Natural link sentences without rule meta-language
- validator_or_reviewer:
  `Forbidden phrase scan + Claude`
- required_evidence:
  `text + Claude verdict`

### HR-LANG-001
- Regel: Natural German and no known regression phrases
- validator_or_reviewer:
  `Language evidence + Claude`
- required_evidence:
  `hashed delta + Claude verdict`

Weitere System-/Planungsregeln nennen u.a.
`independent reviewer` bzw. `independent Claude review`.

## Bewertung gegen 0,0 Freiheit

Noch NICHT akzeptabel als ungeprüfter Befund.

Wenn ein externer Claude/LLM während jedes Produktionslaufs frei PASS/FAIL entscheiden könnte:
STOP für die Zielarchitektur.

Wenn „Claude review“ dagegen ausschließlich historisches, bereits eingefrorenes Build-/Zertifizierungsevidence ist und der reale Lauf nur deterministische, fest versionierte Validatoren ausführt:
keine Runtime-Freiheit.

Diese Unterscheidung ist noch zu beweisen.

## P15

Zwingend prüfen:

1. Gibt es in ausführbarem PPM-/PSERC-/PSTE-Code einen Live-Aufruf zu Claude/Anthropic/OpenAI/LLM?
2. Gibt es API-/Netzwerkabhängigkeit für diese Reviewer-Regeln?
3. Laufen die zugehörigen vorhandenen Positiv-/Negativtests ohne externe KI?
4. Ist „Claude verdict“ lediglich eingefrorene Build-/Review-Metadokumentation oder echte Runtime-Autorität?

Bis P15:
kein Full-GO für diese Rule-Owner.
Keine Regel ändern.
Keine Textmaschine ändern.
