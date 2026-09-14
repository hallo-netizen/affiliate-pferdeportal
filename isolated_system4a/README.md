# SYSTEM 4A — CURRENT STATE

STATUS: **TEST ONLY / BLOCKED BIS SYSTEM-4-BASISANGLEICHUNG + VOLLER RETEST / KEIN MERGE / KEIN PUBLISH**

Diese Datei ist die **eine aktuelle 4A-Statuswahrheit**.

## Aktueller Remote-Stand

PR #255, Branch `hobbyroom/system4a-capsule-v1-20260913`.

PR #255 basiert weiterhin auf System 4 Base `4368597a5d9dcce701f770584da3c87f66915beb`. Der aktuelle System-4-PR #238 steht inzwischen auf Head `28b1bd82af5ccbe5869bf83318ae73d2191bd132` und besitzt den neueren verbindlichen Zielvertrag `isolated_system4/ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_CODEX_WRITER_20260914.md`.

Damit ist 4A **nicht mehr gegen die aktuelle System-4-Basis abgenommen**. Die bisherigen 4A-Beweise bleiben gültige historische/gebundene Belege für exakt ihre damaligen Bytes, dürfen aber nicht als aktueller Produktions-PASS gegen den neueren System-4-Zielstand verwendet werden.

## Aktueller System-4-Zielstand

System 4 verfolgt aktuell verbindlich:

`gebundene Metadaten -> Maschine erzeugt Punkt-0 -> Maschine beschafft/verifiziert reale Quellen -> Root bindet Punkt-0 -> Supervisor besitzt den Lauf -> hashgebundener Worker-Dispatch -> fachliche Research-/Facts-/Context-Unterstützung -> Codex schreibt/repariert innerhalb des Maschinenvertrags -> echte LT/PPM-Prüfer -> Batch -> V2-Handoff -> bytegleiche Rekonstruktion`

Maschine besitzt Start, Bindungen, Route, Supervisor-State, Textmaschinen-/Qualitätsvertrag, Prüfer, PASS, Batch und Handoff. Codex besitzt weder Route noch Regeln noch PASS-Autorität.

Der aktuelle System-4-README-Stand meldet seinen lokal vollständig getesteten Punkt-0/Supervisor-Kandidaten weiterhin **BLOCKED FÜR PRODUKTION**, bis die getesteten Bytes vollständig und bytegleich remote gebunden und auf exakt diesem Remote-Code-Head vollständig positiv/negativ retestet wurden.

## Bisheriger 4A-No-Codex-Beweis — gebundener Altstand

Der bisherige 4A-Stand besitzt einen exakt reproduzierbaren No-Codex-Produktionsvertrag mit:

- `NO_CODEX_PRODUCTION_INPUT_V1.json`;
- `NO_CODEX_PRODUCTION_WORKER_V1.py`;
- `NO_CODEX_PRODUCTION_CONTRACT_V1.json`;
- `no_codex_production_contract.py`.

Für exakt diese gebundenen Bytes wurden zwei getrennte Null-bis-Ende-Läufe bytegleich bewiesen, inklusive echter LanguageTool-6.8- und PPM-6.7.9-Prüfung, Same-Article-Repair, Batch, V2-Handoff und Parent-Chat-Rekonstruktion.

Fehlerhistorie auf diesem gebundenen Altstand:
- bekannte Fehlertypen: **27**;
- real negativ ausgeführt: **27**;
- PASS: **27**;
- FAIL: **0**.

Vertrags-Negativsuite: **5/5 PASS**.

Diese Belege bleiben Belege ihres exakten damaligen Vertragsstands; sie sind **keine aktuelle Abnahme** für die inzwischen geänderte System-4-Basis.

## Neuer Abschlussbefund 2026-09-14

Frisch geprüft:
- PR #255: Draft, offen, unmerged;
- 4A-Head vor dieser Statuskorrektur: `266860eb33c990cd1fc0e38e128afc8483a905ab`;
- System-4-PR #238: Draft, offen, unmerged, Head `28b1bd82af5ccbe5869bf83318ae73d2191bd132`;
- offizieller Campus-/STARTMASTER0107-Stand bleibt separat in `control/startmaster0107/CURRENT_STATE.json` und dort BLOCKED auf 107007;
- kein Merge, kein Publish, kein neuer Codex-Lauf in dieser Abschlussprüfung.

Protokoll des Parallelstand-Befunds: PR-#255-Kommentar `5661452877`.

## NEXT ACTION

1. **Zuerst System 4 fertigstellen:** den bereits lokal getesteten Punkt-0/Supervisor-Code vollständig bytegleich auf PR #238 übertragen.
2. Auf exakt dem finalen Remote-Code-Head von System 4 die komplette Positiv-/Negativ-/Fehlerhistorien- und Null-bis-Ende-Strecke erneut ausführen; echter LT 6.8, echter PPM 6.7.9, Batch und Handoff eingeschlossen.
3. Immutable Base Hardlock muss auf genau diesem finalen System-4-Code-Head SUCCESS sein.
4. **Erst danach 4A** gegen genau diese aktuelle System-4-Basis abgleichen/rebasen.
5. Anschließend 4A vollständig von Rohinput bis bytegleicher Handoff-Datei positiv und negativ neu testen. Kein PASS aus alten 4A-Beweisen ableiten.
6. Kein Codex-Produktionslauf ohne neue ausdrückliche User-Freigabe.

Kein Merge. Kein Publish. `publish_allowed=false`.