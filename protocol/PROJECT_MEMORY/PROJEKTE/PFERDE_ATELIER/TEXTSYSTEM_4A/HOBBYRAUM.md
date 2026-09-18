# TEXTSYSTEM 4A – HOBBYRAUM

<!-- DERIVED_EXECUTION_SURFACE_V1 -->

> **NICHT CURRENT-AUTORITATIV.** Diese Datei ist nur die abgeleitete Ausführungsfläche für eine bereits von der zuständigen Current-Autorität freigegebene Arbeit.  
> Aktuellen Stand, Blocker und NEXT ACTION ausschließlich über `protocol/PROJECT_MEMORY/AUTORITAETSPLAN.json` aus der dort benannten Current-Autorität lesen.  
> Widerspruch oder stale Bindung = **BLOCKED**, niemals Hobbyraum gegen Current durchsetzen.


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

## FRISCHER SYSTEM-4-REALRUN

PR #238 / aktueller geprüfter Head:
`0b3d2acc17b2c32c6d12e677fe9026d3d8c7171a`

Erster echter 1-Artikel-Codex-Lauf:
- Artikel `Putzbox für Pferde richtig auswählen`;
- Ergebnis **BLOCKED BEFORE SYSTEM-4 INGRESS**;
- Root-`AGENTS.md` zog Codex vor der System-4-Tür in die alte/offizielle Runtime-Eintrittsstrecke;
- Blocker `CODEX_PRODUCTION_ENVIRONMENT_PROOF_MISSING`;
- keine fachliche Produktionsstufe gestartet;
- Zeit bis Block: **281 Sekunden / 4:41 Minuten**.

Bewertung:
- fail-closed von System 4 = positiv;
- für `eine Tür / ein Wächter / keine äußere Einflussnahme` = klarer Negativbeweis des aktuellen realen Einstiegs.

Zusätzlich bleibt die dokumentierte PASS-Herkunftslücke im worker-schreibbaren `state.json` relevant.

## ENTSCHEIDEND GEFUNDENE GRENZE

Ein im selben Codex-Task gestarteter 4A-Supervisor ist **kein unabhängiger Wächter**.

Verbindliche PASS-Kriterien:

`SUPERVISOR_OUTSIDE_WORKER_AUTHORITY`

und nach dem Realrun zusätzlich:

`SUPERVISOR_IS_THE_FIRST_AND_ONLY_WORKFLOW_ENTRY`

Der produktive Supervisor muss außerhalb der Codex-/Agent-Sandbox liegen und exklusiv State, Key, Phase, PASS, Route und Resume-Wahrheit besitzen. Repositoryweite/alte Produktionslogik darf den Worker nicht vor der 4A-Tür auf einen anderen Workflow ziehen.

## ABGELEITETE AUSFÜHRUNG DER IN CURRENT GEBUNDENEN NEXT ACTION

Nur diesen Punkt prüfen/bauen:
1. minimalen äußeren Supervisor-Betriebsweg definieren;
2. Supervisor ist die erste und einzige Produktions-Eingangstür;
3. keine neue Produktionsstufe und keine neue Fachregel;
4. ein persistenter Codex-/Agent-Arbeiter darf nur enge Arbeitsaufträge erhalten;
5. State/Key dürfen dem Agenten niemals als Datei/Eingabe zugänglich sein;
6. vorhandene System-4-Prüfer müssen in vertrauenswürdiger read-only Umgebung unverändert laufen;
7. FAIL hält denselben Artikel im Supervisor und öffnet nur `repair`;
8. Resume nur über authentifizierten Supervisor-Checkpoint;
9. finaler Ausgang bleibt vorhandener universeller WordPress-Handoff.

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
