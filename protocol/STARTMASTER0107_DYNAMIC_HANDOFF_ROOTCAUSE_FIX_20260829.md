# STARTMASTER0107 – Dynamic-Handoff-Ursachenfix – 29.08.2026

## Nachgewiesene Ursache
Die vorgebundene 107001→107008-Kette war als statische Capsule-Kette gebaut. 107002–107008 benötigten jedoch dynamische, aus dem jeweils vorherigen Schritt entstehende Ergebnisse. `authorized_inputs` ist absichtlich SHA-statisch. Deshalb konnte der nächste Schritt seinen Vorgängeroutput nicht gleichzeitig dynamisch und hashgebunden erhalten. Das ist die Ursache der leeren/unausführbaren Folge-Capsules; kein Fachworkflowfehler.

## Ursachenfix
- unveränderte geschützte `cloud-entry-gate`-Schicht bleibt Pflicht und unverändert;
- zusätzlicher hashgebundener Entrance-Controller unter `control/startmaster0107/runtime-gate-v3/`;
- jeder Schritt bleibt exakt vorgebunden und monoton 107001→107008;
- Vorgängeroutput wird als `NEXT_INPUT` mit eigenem Manifest und SHA jeder Nutzdatei gebunden;
- der Worker erhält keine Navigations-, State-Write- oder Workflow-Change-Autorität;
- State-Fortschreibung erfolgt nur nach PASS-Receipt + passendem Result-Manifest + exakter `next_binding`;
- jeder Schritt verlangt getrennte POSITIVE-, NEGATIVE- und FULL_WORKFLOW_REGRESSION-Evidenz;
- jede Testevidenz muss an den unveränderten Regression-Baseline-SHA `2c216a6f4491aa2a5e8165d6fafc86faa9fa4696c08f7981f627d4aab5cf71cd` gebunden sein;
- kein Auto-Publish.

## 107001
Die sechs bereits vorgesehenen Rootfix-Beweis-/Workflowartefakte sind byte-identisch gebunden. Die beiden binären Installer bleiben über ihre exakten SHA-256 und Source-Tree-Hashes im unveränderten Regression-Baseline gebunden; in der CAPSULE_ONLY-Ausführung werden ausschließlich die bereits aus dem gebundenen PSTE-0.56.25-Stand erzeugten hashgebundenen Rootfix-Kontexte transportiert, darunter die exakten Queue-Extension-Methoden. Der Auftrag fordert konkreten Rootfix statt abstraktem Vorschlag sowie Positiv-/Negativ-/Gesamtworkflow-Test.

## Lokale harte Prüfung
- Runtime-Gate-/Kettenprüfung: 238/238 PASS.
- zusätzlicher Release-/Gesamtworkflow-Audit: 70/70 PASS.
- beide aktuellen Installer: SHA exakt, ZIP-Integrität PASS, vollständiger PHP-Lint PASS.
- Legacy `cloud-entry-gate`: Positiv PASS; Bundle-Tamper und Sidejump negativ blockiert.
- Continuity-Positiv/Negativtest: PASS.
- geschützte Legacy-Eingangstür byte-identisch.

## Freigaberegel
Noch keine Freigabe vor GitHub-PR mit beiden Pflichtchecks `hardlock` und `hardlock-base` PASS. Danach Merge und Post-Merge-Verifikation. Der 40/40-Fachrootfix selbst bleibt bis zur Codex-Ausführung `LIVE_FAIL_NOT_FIXED`.
