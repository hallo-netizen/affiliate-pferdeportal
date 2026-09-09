# SEO/TEXT-BÜRO – ALTERNATIVROUTE ZENTRALMASCHINE

Status: AKTIV – ausschließlich Konzept-/Hobbyraumroute
Branch: `alternative/seo-text-central-machine-20260908`
Ausgangsbasis: `914638e67a265cf2e8951b1177a7d80fdf904e98`
Datum: 2026-09-08

## Harte Trennung

Diese Route ist absichtlich vom laufenden STARTMASTER-/Reparaturweg getrennt.

VERBOTEN auf dieser Route:
- kein Schreiben auf `main`
- kein Merge nach `main` ohne ausdrückliche spätere Freigabe
- keine Änderung an Textmaschine, PPM, PSERC, PSTE oder LanguageTool
- keine Änderung an bestehenden Fach-, Inhalts-, SEO-, Qualitäts-, Design-, Tabellen-, Link-, Dubletten-/Kannibalisierungs- oder Publish-Regeln
- keine Änderung an CURRENT_STATE oder aktiven STARTMASTER-Step-Bundles
- keine WordPress-Schreibaktion
- kein Auto-Publish
- keine Nutzung dieser Route als Ersatzroute für einen BLOCKED-Zustand im laufenden Produktionsworkflow

## Unverhandelbare Zielregeln

1. Chat/KI hat 0,0 Workflow-Entscheidungsfreiheit.
2. Jeder Worker darf nur genau seinen gebundenen Mikroschritt ausführen.
3. Kein Worker darf Reihenfolge, Folgeschritt, Regeln oder Reparaturweg wählen.
4. Keine Worker-zu-Worker-Kommunikation.
5. Ein technischer, nicht-intelligenter Steuerkern besitzt allein Reihenfolge und Zustand.
6. Prüfer dürfen nur mechanisch nach festem Vertrag PASS oder BLOCKED liefern.
7. Bestehende Textmaschine bleibt unangetastet und autoritativ.
8. Das Konzept muss themenunabhängig, automatisierbar, nachhaltig und erweiterbar sein.
9. Nach Dateiausgabe muss eine manipulationssichere Übergabe bis WordPress vorgesehen werden; externe Signierung bleibt grundsätzlich erhalten.
10. Interne Signierung wird nicht als Voraussetzung wieder eingeführt.
11. Jede Konzeptänderung wird lokal positiv und negativ getestet, bevor sie als Kandidat gilt.

## CHAT-START-ZWANGSGATE – GILT AUCH IN JEDEM NEUEN CHAT

Bevor in irgendeinem Chat technische ACM-Arbeit begonnen, fortgesetzt, geplant oder ein Kandidat erzeugt wird, müssen zwingend frisch gelesen werden:

1. `control/seo-text-buero/alternative-central-machine/00_ROUTE_BOUNDARY.md`
2. `control/seo-text-buero/alternative-central-machine/AKTENSCHRANK/58_ACM_ROUTE_STATUS_20260909.md`
3. die dort ausdrücklich benannten autoritativen Fehler-/Übergabequellen, wenn sie für den nächsten Schritt relevant sind.

Ohne diesen frischen Read:
`ACM_CHAT_START_BLOCKED`

Verboten ist:
- aus Erinnerung weiterarbeiten;
- aus einem alten Chatstatus weiterarbeiten;
- eine ältere P0–P59-Akte als CURRENT verwenden;
- einen früheren PASS ungeprüft auf den aktuellen Schritt übertragen.

### Übernahme alter Bausteine – harte Trennung

Altbestand darf nur in zwei Klassen behandelt werden:

**A. Fach-/Sicherheitsbaustein**
Beispiele:
- Textmaschine
- PPM
- PSERC
- PSTE
- LanguageTool-Regeln
- vorhandene Validatoren
- externe Signatur
- WordPress Draft-/Readback-/DOM-Prüfer

Diese dürfen nur unverändert als bestehende Autorität benutzt werden.

**B. Workflow-/Übergabe-/Orchestrierungsbaustein**
Beispiele:
- Current Action / 107007-Orchestrierung
- Handoff-Vertrag
- Stage-Proof-Semantik
- Reihenfolge-/State-/Worker-Bindung
- Runner/Controller/Executor

Diese dürfen **nicht automatisch** übernommen werden, nur weil sie bereits existieren.

Vor jeder solchen Übernahme muss separat bewiesen werden:
1. keine bekannte Fehlerklasse wird mit übernommen;
2. keine neue oder alte Worker-/Chat-Freiheit bleibt bestehen;
3. keine doppelte Wahrheit entsteht;
4. keine Lifecycle-/Reihenfolgekollision entsteht;
5. Gesamtsystemwirkung ist positiv/negativ geprüft.

Fehlt einer dieser Beweise:
`OLD_WORKFLOW_COMPONENT_ADOPTION_BLOCKED`

### Bekannter Fehlgriff dieser Route

Die Entscheidung P27/P38, `FACHWORKFLOW_HANDOFF_REQUEST.json` als komplette einzige Produktions-Eingangswahrheit zu übernehmen, war zu breit.

Zulässige Motivation war:
- vorhandenen Chat/Codex-Start wiederverwenden;
- keine neue Dateiübergabe erfinden;
- Identitäten/Hashes nicht neu erfinden.

Nicht ausreichend getrennt wurde:
- **Transport-/Identitätsvertrag** der Datei
gegen
- **alte 12-Stage-Orchestrierungs-/Proof-Semantik**.

Dadurch wurde eine bekannte Altlast erneut in den Realintegrationstest hineingetragen.

Diese Übernahme gilt deshalb nicht mehr als pauschal freigegeben.
Transport/Identität und Workflow-/Stage-Semantik müssen getrennt bewertet werden.

## PRE-CHANGE-ZWANGSGATE – FAIL CLOSED

Vor **jeder** technischen Änderung, jedem Fix, jedem neuen Testkandidaten und jedem Schreibzugriff muss diese Prüfung vollständig beantwortet werden.

Alle Antworten müssen eindeutig `NEIN` sein.  
`JA`, `UNKLAR`, `NICHT BELEGT` oder fehlende Evidenz => **STOP / KEINE ÄNDERUNG**.

1. Entsteht ein neuer Baustein, eine neue Schicht, ein neuer Runner, Controller, Handoff, Executor, Validator oder Ersatzweg?
2. Entsteht irgendwo neue Chat-/Worker-/KI-Entscheidungsfreiheit oder kann eine bestehende feste Autorität umgangen, gewählt oder neu interpretiert werden?
3. Wird eine alte Schnittstelle oder Altlogik übernommen, die bekannte Fehler-/Freiheitsklassen in ACM hineintragen kann?
4. Kann die Änderung irgendeinen anderen Teil des Gesamtworkflows beeinflussen – direkt oder indirekt – ohne dass diese Wirkung vollständig bestimmt und geprüft ist?

Zusätzlich zwingend vor GO:
- aktuelle ACM-Standwahrheit lesen;
- relevante autoritative Campus-/TEXT-Fehler- und Übergabequellen lesen;
- unmittelbare Vorstufe + Änderung + unmittelbare Nachstufe gegen den gesamten Zielworkflow prüfen;
- Systemwirkung auf Textmaschine, PPM, PSERC, PSTE, LanguageTool, Links, Tabellen, SEO, Design/DOM, Signatur, WordPress, Publish-Safety und Batch/State bestimmen;
- keine historische PASS-Aussage als Ersatz für aktuellen Beweis verwenden.

Nur bei `4x NEIN + SYSTEMWIRKUNG BELEGT` darf genau **eine kleinste Änderung** als Kandidat entstehen.

Nach jeder zulässigen Änderung zwingend:
1. Positivtest;
2. Negativtest;
3. kompletter Workflow-Gegencheck;
4. Gesamtsystem-Auswirkungsprüfung;
5. erst danach nächster Schritt.

Kein PASS in einem Einzeltest darf einen Gesamtworkflow-PASS ersetzen.

## Zweck

Nicht den bestehenden Produktionsweg reparieren.

Hier wird ausschließlich geprüft, ob eine alternative Architektur dieselben oder stärkere Sicherheitsgarantien mit weniger fehleranfälliger Übergabelogik erreichen kann.

Alle Ergebnisse dieses Chats werden ausschließlich in diesem Ordner/Branch dokumentiert.
