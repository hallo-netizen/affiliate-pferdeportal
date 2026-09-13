# SYSTEM 4A — AUTHORITY BOUNDARY

## Verbindliches Ziel

System 4A existiert nur, wenn ein einziger produktiver Supervisor technisch außerhalb der Verfügungsgewalt des Codex-/Workers liegt.

PASS-Kriterium:

`SUPERVISOR_OUTSIDE_WORKER_AUTHORITY`

Der Supervisor besitzt exklusiv:
- Workflow-State;
- Phase/Route;
- Authority-Key;
- Resume-Wahrheit;
- PASS-Verwendung;
- finalen Ausgang.

Codex/Worker darf nur den jeweils erlaubten Fachauftrag sehen und ausschließlich Arbeitsinhalt zurückgeben.

## Unzulässig

- Supervisor im selben Codex-Task als normaler Kindprozess;
- produktiver In-Process-Worker-Callable;
- Authority-Key im Worker-Workspace;
- worker-schreibbare Phase/PASS/Publish-Felder;
- freie Seiteneinstiege in Einzelphasen;
- Worker-Auswahl des nächsten Schritts;
- synthetische Prüfer-PASS-Daten als produktiver Ersatz;
- neue Signer-/Token-/Room-/Receipt-/Package-Kaskaden.

Der direkte `FullChainSupervisor.run_full(..., worker_callable, ...)`-Weg ist deshalb im Produktionsmodus technisch blockiert:

`PRODUCTION_REQUIRES_EXTERNAL_SUPERVISOR_HOST`

## Lokaler Autoritätsbeweis 2026-09-13

`os_boundary_acceptance.py` wurde lokal unter getrennter OS-Benutzerkennung für Supervisor und Worker positiv/negativ ausgeführt.

Ergebnis:

`SYSTEM4A_EXTERNAL_SUPERVISOR_OS_BOUNDARY_PASS: POSITIVE_ROUTE + 10_NEGATIVE_AUTHORITY_CHECKS`

Dabei nachgewiesen:
- erlaubte Kommunikation ausschließlich über die enge Supervisor-Schnittstelle;
- Worker kann Supervisor-State nicht lesen;
- Worker kann Supervisor-State nicht schreiben;
- Worker kann Authority-Key nicht lesen;
- Worker kann Authority-Key nicht schreiben;
- Worker kann Supervisorprozess nicht beenden;
- Worker kann Supervisor-Environment nicht lesen;
- Worker kann Supervisor-Socket nicht ersetzen;
- Worker kann im privaten Supervisorbereich keinen Fake-State erzeugen;
- Phase/PASS-Injektion über Workerantwort wird blockiert;
- direkte `set_state`-Operation wird blockiert;
- HMAC-State bleibt nach den Angriffen gültig.

Dieser Beweis zeigt: **eine echte technische Autoritätsgrenze ist lokal möglich.** Er ist noch kein vollständiger Produktions-E2E mit realem Codex, LT und PPM.

## Vollketten-Beweis

Die Autoritätsgrenze gilt produktiv erst als vollständig bewiesen, wenn lokal positiv und negativ die komplette Kette geprüft ist:

`FIRST ENTRY -> EXTERNAL SUPERVISOR -> ISOLATED WORKER -> RESEARCH -> FACTS -> CONTEXT -> DRAFT -> REAL FULLCHECK -> REPAIR -> BATCH -> EXACT HANDOFF -> PARENT CHAT -> READBACK`

Ein Test, der direkt innerhalb der Kette startet, echte Prüfer mockt oder nur Teilkomponenten prüft, ist kein Produktions-Vollkettenbeweis.

## Produktions-E2E

Produktions-E2E muss die real gebundenen System-4-Prüfer ausführen. Insbesondere dürfen `production_checks.run_all`, LanguageTool 6.8 und PPM 6.7.9 nicht gemockt oder durch synthetische PASS-Evidence ersetzt werden.

Fehlende reale Abhängigkeit = BLOCKED.

## Abbruch

Wenn diese Grenze nicht mit genau einem äußeren Supervisor realisierbar ist, 4A stoppen und nur die nachgewiesenen Härtungen in System 4 übernehmen.
