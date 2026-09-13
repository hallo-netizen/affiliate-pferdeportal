# TEXTSYSTEM 4A – CURRENT STATE

STAND: 2026-09-13
STATUS: BLOCKED / EXTERNE WÄCHTERGRENZE NOCH NICHT BEWIESEN

## Vergleichsbasis

### System 4
- PR #238
- Branch `hobbyroom/system4-true-single-room-v1`
- frisch geprüfter Head: `8da5a3f45ff42d3fae652d0a64071a9ea10770a4`
- 1..N, freie gebundene Beitragsart und universeller WordPress-Handoff sind inzwischen System-4-Bestand und kein 4A-Vorteil.

### System 4A
- PR #255
- Branch `hobbyroom/system4a-capsule-v1-20260913`
- direkt auf System 4 aufgesetzt; kein Merge/Publish.

## Einziger legitimer Unterschied 4A

4A bleibt ausschließlich wegen dieser Frage offen:

> **Kann der Workflow-State technisch außerhalb der Verfügungsgewalt des Codex-/Workers liegen?**

System 4 lässt Codex weiterhin im selben Task die `state.json`-Workspaces führen und die einzelnen Controller-Schritte aufrufen. Damit besitzt Codex die persistierten Workflow-State-Dateien mit.

4A versucht dagegen:
- Supervisor besitzt State/Phase/Route/PASS allein;
- Codex erhält nur den gerade erlaubten Fachauftrag;
- Worker-Rückgabe erlaubt nur Arbeitsinhalt;
- Prüfer entscheiden nur PASS/FAIL/Findings;
- FAIL bleibt derselbe Artikel und öffnet ausschließlich Repair;
- Checkpoint ist HMAC-authentifiziert.

## V3-Kapselkern – realer lokaler Test

Erster V3-Lauf: **15/16 PASS**. Dabei wurde ein reiner Testfixture-Fehler gefunden; der Controller wurde nicht geändert.

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

Die State-Frage ist nicht mehr nur theoretisch.

Im aktuellen `batch_gate.py` werden gespeicherte FULL-/LT-/PPM-Evidence-Felder auf erwartete Werte und Hashbezüge geprüft; LT und PPM werden dort nicht erneut ausgeführt und es gibt keine ausschließlich vom echten Prüfer erzeugte Attestation.

Der vorhandene System-4-Test `test_batch_gate.py` belegt diese Eigenschaft selbst:
- `production_evidence(draft)` erzeugt LT-/PPM-PASS-Evidence synthetisch im Testcode;
- `make_fixture()` schreibt diese Werte direkt in `state['checks']['production_evidence']`;
- der positive Test erwartet danach von `batch_gate.collect_batch(...)` `SYSTEM4_BATCH_FULL_PASS_COLLECTED`.

Der finale `handoff_transport.py` prüft Fact-Trace, Design und Batchregeln erneut real, übernimmt LT-/PPM-PASS aber ebenfalls als strukturierte Evidence ohne erneute LT-/PPM-Ausführung.

Damit kann die aktuelle Grenze die **Herkunft** eines formal passenden LT-/PPM-PASS nicht allein aus dem vom Worker schreibbaren State beweisen.

Das beweist keinen praktischen externen Angriff. Es beweist aber exakt die für die Projektanforderung relevante Herkunftslücke: Worker-State und Prüfer-PASS sind noch nicht technisch vollständig voneinander getrennt.

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

Wenn Codex den produktiven Supervisor selbst starten, dessen Authority-Key wählen/lesen oder einen Ersatzcontroller starten kann, besitzt Codex faktisch wieder die Workflow-Autorität. Dann hat 4A keinen ausreichenden strukturellen Vorteil gegenüber System 4.

Darum ist für 4A verbindlich:

`SUPERVISOR_OUTSIDE_WORKER_AUTHORITY`

Der produktive Supervisor muss außerhalb der Codex-/Agent-Sandbox laufen und exklusiv State, Key, Phase, PASS, Route und Resume-Wahrheit halten. Codex darf ausschließlich enge Fachaufträge erhalten und Arbeitsinhalt zurückgeben.

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
