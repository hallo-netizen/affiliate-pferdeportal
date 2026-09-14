# SYSTEM 4A — AUTHORITY BOUNDARY

## Verbindliches Ziel

System 4A existiert nur, wenn ein einziger produktiver Supervisor technisch außerhalb der Verfügungsgewalt des Workers liegt.

PASS-Kriterium:

`SUPERVISOR_OUTSIDE_WORKER_AUTHORITY`

Der Supervisor besitzt exklusiv:
- Workflow-State;
- Phase/Route;
- Authority-Key;
- Resume-Wahrheit;
- PASS-Verwendung;
- finalen Ausgang.

Der Worker darf nur den jeweils erlaubten Fachauftrag sehen und ausschließlich Arbeitsinhalt zurückgeben.

## Unzulässig

- Supervisor im selben Workerraum als normaler Kindprozess;
- produktiver In-Process-Worker-Callable;
- Authority-Key im Worker-Workspace;
- worker-schreibbare Phase/PASS/Publish-Felder;
- freie Seiteneinstiege in Einzelphasen;
- Worker-Auswahl des nächsten Schritts;
- synthetische Prüfer-PASS-Daten als produktiver Ersatz;
- neue Signer-/Token-/Room-/Receipt-/Package-Kaskaden.

Der direkte `FullChainSupervisor.run_full(..., worker_callable, ...)`-Weg ist deshalb im Produktionsmodus technisch blockiert:

`PRODUCTION_REQUIRES_EXTERNAL_SUPERVISOR_HOST`

## Autoritätsbeweis

Die technische Grenze ist positiv und negativ nachgewiesen:

- Worker läuft als getrennte Cross-UID-Ausführung;
- Supervisor-State und Authority-Key sind für den Worker nicht schreibbar;
- Phase/PASS-/Publish-Injektion über Workerantwort wird blockiert;
- direkte State-Manipulation wird blockiert;
- HMAC-State bleibt nach Negativangriffen gültig.

## Vollständiger Produktionsbeweis — NO CODEX

Der aktuelle No-Codex-Produktionsvertrag beweist die vollständige Kette:

`gebundener Rohinput -> Root Entry -> External Supervisor -> Cross-UID Worker -> Research -> Facts / Fact-Pack -> Context -> Supervisor-Authoring-Bindung -> Draft -> echte LanguageTool-6.8-Prüfung -> Same-Article-Repair -> echte PPM-6.7.9-Prüfung -> weiterer Same-Article-Repair -> erneute echte Prüfung -> Batch Gate -> V2-Handoff -> Inline-Transport -> Parent-Chat-Entpackung -> finale Datei`

Der Beweis verwendet:

- keine Mocks;
- keine vorbereitete `quality_binding`;
- keine vorgegebenen Runtime-Links;
- keine synthetischen LT-/PPM-PASS-Daten;
- keinen Codex.

Zwei getrennte Null-bis-Ende-Läufe erzeugen dieselbe Enddatei bytegleich und feldgleich. Parent-Chat-Rekonstruktion ist jeweils bytegleich zur Enddatei.

Zusätzlich werden die bekannten Fehlerklassen negativ getestet; eine Mutation an Input, Worker, Produktionsquelle, Output oder Parent-Handoff macht die Abnahme ungültig.

## Produktions-E2E

Produktions-E2E muss die real gebundenen System-4-Prüfer ausführen. Insbesondere dürfen `production_checks.run_all`, LanguageTool 6.8 und PPM 6.7.9 nicht gemockt oder durch synthetische PASS-Evidence ersetzt werden.

Fehlende oder abweichende reale Abhängigkeit = BLOCKED.

Der aktuell bewiesene Einstieg ist ausschließlich der gebundene No-Codex-Vertrag über `realcase_production_entry.py` und `ExternalSupervisorHost(mode='production')`.

## Gültigkeitsgrenze

Die Abnahme gilt nur für exakt gebundene Vertragsbytes und Produktionsquellcode-Fingerprints. Jede Änderung an einem gebundenen Produktionsbyte oder Pflichtfeld entwertet den PASS und erzwingt erneut:

1. vollständigen Fehlerhistorien-Regressionslauf;
2. Null-bis-Ende positiv;
3. Null-bis-Ende negativ;
4. zwei getrennte Reproduktionsläufe;
5. Byte-/Feldgleichheitsbeweis bis zur finalen Datei.

Kein Merge. Kein Publish. Kein Codex-Lauf ohne ausdrückliche User-Freigabe mit den Worten `Starte Codex`.
