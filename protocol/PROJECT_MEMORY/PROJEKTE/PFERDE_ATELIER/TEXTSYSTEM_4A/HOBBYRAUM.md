# TEXTSYSTEM 4A – HOBBYRAUM

STAND: 2026-09-13
STATUS: BLOCKED / ENTSCHEIDUNGSBEWEIS EXTERNE WÄCHTERGRENZE

## AKTUELLE ARBEITSBINDUNG

THEMA: `4A_EXTERNAL_SUPERVISOR_AUTHORITY`
STATUS: `BLOCKED`
BLOCKER: `EXTERNAL_SUPERVISOR_AUTHORITY_BOUNDARY_NOT_YET_PROVEN`

## BEREITS BEWIESEN

4A V3 Kapselkern lokal positiv/negativ: **16/16 PASS**.

Bewiesen:
- Supervisor besitzt im Kapselkern Route/Phase;
- Worker liefert ausschließlich Arbeitsinhalt;
- State-/Publish-Injektion BLOCK;
- Same-Article-Repair;
- HMAC-Checkpoint + Tamper-BLOCK;
- Resume am gebundenen Schritt;
- 1.000 isolierte Kapseln;
- Batch nur aus ARTICLE_PASS.

Vorhandene System-4-Prüfer werden über einen dünnen Read-only-Adapter direkt aufgerufen; keine neue Fach-/Text-/Design-/Qualitätsregel wurde gebaut.

## FRISCHER SYSTEM-4-VERGLEICH

PR #238 / Head bei diesem Stand:
`8da5a3f45ff42d3fae652d0a64071a9ea10770a4`

System 4 ist inzwischen universell für 1..N und gebundene Beitragsarten ausgelegt. Diese Punkte und der WordPress-Handoff sind kein 4A-Vorteil.

Der relevante Unterschied bleibt: System 4 lässt Codex weiterhin die persistierten Artikel-`state.json`-Workspaces im eigenen Task führen und die Controller-Schritte selbst aufrufen.

## ENTSCHEIDEND GEFUNDENE GRENZE

Ein im selben Codex-Task gestarteter 4A-Supervisor ist **kein unabhängiger Wächter**.

Wenn Codex den Supervisor starten/ersetzen oder den Authority-Key wählen/lesen kann, besitzt Codex wieder die Workflow-Autorität. Dann ist 4A nur zusätzliche Verpackung und wird verworfen.

Verbindliches PASS-Kriterium:

`SUPERVISOR_OUTSIDE_WORKER_AUTHORITY`

Der produktive Supervisor muss außerhalb der Codex-/Agent-Sandbox liegen und exklusiv State, Key, Phase, PASS, Route und Resume-Wahrheit besitzen.

## JETZT VERBINDLICHE NEXT ACTION

Nur diesen Punkt prüfen/bauen:

1. minimalen äußeren Supervisor-Betriebsweg definieren;
2. keine neue Produktionsstufe und keine neue Fachregel;
3. ein persistenter Codex-/Agent-Arbeiter darf nur enge Arbeitsaufträge erhalten;
4. State/Key dürfen dem Agenten niemals als Datei/Eingabe zugänglich sein;
5. vorhandene System-4-Prüfer müssen in vertrauenswürdiger read-only Umgebung unverändert laufen;
6. FAIL muss denselben Artikel im Supervisor halten und nur `repair` öffnen;
7. Resume darf nur über authentifizierten Supervisor-Checkpoint erfolgen;
8. finaler Ausgang bleibt der vorhandene universelle WordPress-Handoff.

Erst wenn diese äußere Grenze praktisch ohne neue Kaskade beweisbar ist, weiter zu realem LT/PPM-E2E.

## STOPPREGELN

- Keine neue Textmaschine.
- Keine neue Fach-/Text-/Design-/Qualitätsregel.
- Kein Ersatzprüfer.
- Keine neue WordPress-Schnittstelle.
- Kein weiterer Signer/Receipt-/Room-/Package-Weg.
- Keine Agent-zu-Agent-Freitextübergaben als Workflowsteuerung.
- Kein Merge/Publish.
- Wenn echte äußere Wächtertrennung wieder eine Sicherheitskaskade erzeugt: **4A STOPPEN und Härtung in System 4 übernehmen.**
