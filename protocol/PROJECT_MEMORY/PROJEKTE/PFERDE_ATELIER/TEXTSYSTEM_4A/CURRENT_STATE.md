# TEXTSYSTEM 4A – CURRENT STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

> **Einzige aktuelle Zustandsautorität dieses Scopes.** Status, erster offener Blocker und NEXT ACTION werden nur hier gepflegt.  
> `HOBBYRAUM.md` ist lediglich abgeleitete Ausführungsfläche.


STAND: 2026-09-13
STATUS: BLOCKED / EXTERNE WÄCHTERGRENZE NOCH NICHT BEWIESEN

## Vergleichsbasis

### System 4
- PR #238
- Branch `hobbyroom/system4-true-single-room-v1`
- aktueller geprüfter Head nach erstem Realrun: `0b3d2acc17b2c32c6d12e677fe9026d3d8c7171a`
- 1..N, freie gebundene Beitragsart und universeller WordPress-Handoff sind System-4-Bestand und kein 4A-Vorteil.

### System 4A
- PR #255
- Branch `hobbyroom/system4a-capsule-v1-20260913`
- direkt auf System 4 aufgesetzt; kein Merge/Publish.

## Einziger legitimer Unterschied 4A

4A bleibt ausschließlich wegen dieser Frage offen:

> **Kann der Workflow-State und die einzige technische Eingangstür außerhalb der Verfügungsgewalt des Codex-/Workers liegen?**

System 4 lässt Codex weiterhin im selben Task die `state.json`-Workspaces führen und die einzelnen Controller-Schritte aufrufen. 4A versucht dagegen genau eine äußere Autorität: Supervisor besitzt State/Phase/Route/PASS; Codex erhält nur den gerade erlaubten Fachauftrag.

## Erster echter System-4-Lauf — realer neuer Befund

Der erste echte 1-Artikel-Codex-Lauf von System 4 wurde am 2026-09-13 ausgeführt.

Gebundener Artikel:
- `Beratung`;
- `Putzbox für Pferde richtig auswählen`;
- Keyword `Putzbox für Pferde`;
- 1 Item;
- `publish_allowed=false`.

Ergebnis:
- **BLOCKED BEFORE SYSTEM-4 INGRESS**;
- repositoryweite Root-`AGENTS.md` griff vor der System-4-Anweisung;
- Codex wurde in die bestehende offizielle Runtime-Eintrittsstrecke gezogen;
- Blocker `CODEX_PRODUCTION_ENVIRONMENT_PROOF_MISSING`;
- keine Recherche, Fakten, Fact-Pack, Draft, LT, PPM, Batch oder WordPress-Datei erzeugt;
- Zeit bis zum Block: **281 Sekunden / 4:41 Minuten**.

Bewertung:
- System 4 verhielt sich korrekt fail-closed; kein Bypass, kein falsches PASS.
- Gleichzeitig ist real bewiesen, dass eine äußere repositoryweite Steuerung den Worker **vor der System-4-Tür** umlenken kann.
- Damit ist die Anforderung `keine Einflussmöglichkeit von außen / eine Tür – ein Wächter` in System 4 aktuell noch nicht erfüllt.

## V3-Kapselkern – realer lokaler Test

Erster V3-Lauf: **15/16 PASS**; reiner Testfixture-Fehler gefunden, Controller unverändert.
Nach ausschließlicher Korrektur des Tests: **16/16 PASS**.

Bewiesen im V3-Kern:
- Statuskopie verändert echten State nicht;
- keine externe Publish-Eingabefläche;
- keine Phasensprünge;
- falscher Prüfer-Hash öffnet kein Gate;
- manipulierter Checkpoint BLOCK;
- Resume exakt am gebundenen Schritt;
- Same-Article-Repair;
- Worker-Injektion von `phase`/`publish_allowed` BLOCK;
- Supervisor führt Route automatisch;
- Batch nur aus ARTICLE_PASS;
- 1.000 unabhängige Kapseln ohne Zustandsvermischung.

**4A V3 KAPSELKERN: PASS 16/16.**

Kein Produktions-PASS daraus ableiten.

## Konkreter System-4-PASS-Herkunftsbefund

Die State-Frage ist zusätzlich nicht nur theoretisch.

Im aktuellen `batch_gate.py` werden gespeicherte FULL-/LT-/PPM-Evidence-Felder auf erwartete Werte und Hashbezüge geprüft; LT und PPM werden dort nicht erneut ausgeführt und es gibt keine ausschließlich vom echten Prüfer erzeugte Attestation.

Der vorhandene System-4-Test `test_batch_gate.py` belegt diese Eigenschaft selbst: `production_evidence(draft)` erzeugt LT-/PPM-PASS-Evidence synthetisch im Testcode und der positive Test erwartet anschließend `SYSTEM4_BATCH_FULL_PASS_COLLECTED`.

Der finale `handoff_transport.py` prüft Fact-Trace, Design und Batchregeln erneut real, übernimmt LT-/PPM-PASS aber ebenfalls als strukturierte Evidence ohne erneute LT-/PPM-Ausführung.

Das beweist keinen praktischen externen Angriff. Es beweist aber die Herkunftslücke: Worker-State und Prüfer-PASS sind technisch noch nicht vollständig getrennt.

4A-Beleg im PR:
`isolated_system4a/SYSTEM4_STATE_AUTHORITY_GAP.md`.

## Vorhandene Prüfer

4A besitzt einen dünnen Read-only-Adapter, der keine eigene Fach-/Design-/Qualitätsregel enthält und direkt die vorhandenen System-4-Module aufruft:
- Research/Facts/Fact-Pack/Article/Repair/Batch aus `content_guard`;
- Design aus `design_guard`;
- Context/FULL aus `production_checks`;
- Wiederholungsprüfung aus `batch_repetition_guard`.

Der komplette reale LT/PPM-E2E über diesen Adapter ist noch nicht bewiesen.

## Entscheidend gefundene Grenze

Ein HMAC im selben Codex-Arbeitsbereich ist **kein unabhängiger Wächter**.

Verbindliches 4A-Kriterium:

`SUPERVISOR_OUTSIDE_WORKER_AUTHORITY`

Der produktive Supervisor muss außerhalb der Codex-/Agent-Sandbox laufen und exklusiv State, Key, Phase, PASS, Route und Resume-Wahrheit halten. Zusätzlich muss bewiesen werden, dass repositoryweite/alte Eintrittslogik den Worker nicht vor dieser 4A-Tür auf einen anderen Weg zwingen kann.

Die harte Definition liegt in:
`isolated_system4a/AUTHORITY_BOUNDARY.md` auf PR #255.

## Aktueller Blocker

`EXTERNAL_SUPERVISOR_AUTHORITY_BOUNDARY_NOT_YET_PROVEN`

Bis dieser Punkt real bewiesen ist:
- keine weitere Text-/Design-/Prüflogik bauen;
- keinen neuen Handoff/Signer/Receipt/Room/Package-Weg bauen;
- keinen WordPress-Umbau bauen;
- keine Produktionsfreigabe.

## Kritischer Preis von echtem 4A

Echte Trennung benötigt einen äußeren Laufzeitbaustein, der Codex/Agent aufruft und State/Key selbst hält. Das erhöht Betriebs- und Wartungskomplexität gegenüber System 4.

Der Vorteil wäre echte Workflow-Autorität außerhalb von Codex; der Nachteil ist dieser zusätzliche externe Runtime-Baustein.

## Abbruchschwelle

Wenn die äußere Supervisor-Grenze nur durch neue Signer-, Token-, Room-, Receipt- oder Package-Kaskaden erreichbar ist: **4A sofort stoppen.**

Dann werden die brauchbaren Härtungsideen in System 4 übernommen statt ein fünftes System zu bauen.

## NEXT ACTION

Ausschließlich die äußere Supervisor-Grenze beweisen:
1. minimalen äußeren Supervisor-Betriebsweg definieren;
2. Supervisor als erste und einzige Produktions-Eingangstür beweisen;
3. State/Key/Phase/PASS/Route/Resume außerhalb der Worker-Autorität halten;
4. vorhandene System-4-Prüfer unverändert in vertrauenswürdiger Read-only-Umgebung ausführen;
5. keine neue Fach-/Text-/Design-/Qualitätsregel und keine neue Signer-/Receipt-/Room-/Package-Kaskade bauen.

Erst bei realem PASS dieser Grenze darf der reale LT/PPM-E2E folgen. Bei erneuter Sicherheitskaskade: 4A stoppen und die brauchbare Härtung in System 4 übernehmen.
