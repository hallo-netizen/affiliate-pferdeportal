# SYSTEM 4A — CURRENT STATE

STATUS: **TEST ONLY / NO-CODEX-PRODUKTIONSVERTRAG PASS / KEIN MERGE / KEIN PUBLISH**

Diese Datei ist die eine aktuelle 4A-Statuswahrheit.

## Aktueller Remote-Stand

PR #255, Branch `hobbyroom/system4a-capsule-v1-20260913`.

Der aktuelle 4A-Stand besitzt einen **exakt reproduzierbaren No-Codex-Produktionsvertrag**. Codex ist für diesen Vertrag ausdrücklich ausgeschlossen (`codex_allowed=false`).

Der Vertrag besteht aus:

- `NO_CODEX_PRODUCTION_INPUT_V1.json` — exakt gebundene Rohinput-Bytes;
- `NO_CODEX_PRODUCTION_WORKER_V1.py` — exakt gebundene Worker-Bytes;
- `NO_CODEX_PRODUCTION_CONTRACT_V1.json` — Abhängigkeiten, Produktionsquellcode-Fingerprints und erwartete Endzustände;
- `no_codex_production_contract.py` — ausführbarer Positiv-/Negativ- und Reproduzierbarkeitsbeweis.

## Bewiesener Produktionsweg

Der vollständige Null-bis-Ende-Weg lautet:

`gebundener Rohinput -> Root Entry -> Production Ingress -> Cross-UID Worker -> Research -> Facts / Fact-Pack -> Context -> Supervisor-Authoring-Bindung -> Draft -> echte LanguageTool-6.8-Prüfung -> Same-Article-Repair -> erneute echte Prüfung -> echte PPM-6.7.9-Prüfung -> zweiter Same-Article-Repair -> erneute echte Prüfung -> Batch Gate -> V2-Handoff -> Inline-Transport -> Parent-Chat-Entpackung -> finale Datei`

Es wurde **kein Codex** verwendet.

## Reproduzierbarkeitsbeweis

Zwei vollständige Produktionsläufe wurden aus zwei voneinander getrennten, leeren Laufverzeichnissen mit exakt denselben Vertragsbytes ausgeführt.

Ergebnis:

- Lauf A: **PASS**;
- Lauf B: **PASS**;
- Enddatei A = Enddatei B: **bytegleich**;
- vollständige JSON-Struktur A = B: **feldgleich**;
- Parent-Chat-Datei A = Enddatei A: **bytegleich**;
- Parent-Chat-Datei B = Enddatei B: **bytegleich**;
- echte LanguageTool 6.8: **PASS**;
- echte PPM 6.7.9: **PASS**;
- Revision: **3**;
- zwei echte Same-Article-Repairs;
- Enddatei: **29.391 Byte**;
- Enddatei SHA256: `8a3fab64fb1e654257f12bb8c9ead716abbf3cf7f207d50c6b1c69d386ca1cc4`.

Zusätzlich sind die produktionsrelevanten Quellcode-Dateien sowie LT-/PPM-/PPM-Vertragsquellen im Produktionsvertrag bytegenau über SHA256 gebunden. Eine Abweichung macht den Vertrag ungültig.

## Fehlerhistorie / Regression

Die aktuelle Fehlerhistorie wurde vollständig in einen ausführbaren Regressionstest-Katalog überführt.

- bekannte Fehlertypen: **27**;
- real negativ ausgeführt: **27**;
- PASS: **27**;
- FAIL: **0**.

Darin enthalten sind insbesondere:

- falsche/unbekannte Fact-IDs;
- Fact-ID nicht im kanonischen Fact-Pack;
- falscher/fehlender PPM-Plan-Slot;
- Context-/Runtime-Mismatch;
- Manifest-/Hash-Mismatch;
- falsche Kategorie;
- falsche Linkbindung;
- fehlende Pflichtfelder;
- falsche Artikelidentität;
- Batch-/Artikel-Kontext-Mismatch;
- Worker-/PASS-Autoritätsverletzung;
- Handoff-/Inline-Manipulation;
- private/nicht zugängliche Worker-Runtime;
- bereits dokumentierte analoge Fehlerklassen.

## Vertrags-Negativsuite

Zusätzlich zum 27er-Fehlerkatalog wurden Vertragsmanipulationen fail-closed geprüft:

- falscher Plan-Slot -> BLOCK;
- falsche Kategorie -> BLOCK;
- Worker-Byteänderung -> BLOCK;
- Enddatei-Manipulation -> BLOCK;
- Parent-Handoff-Manipulation -> BLOCK.

Ergebnis: **5/5 PASS**.

## Harte Abnahmegrenze

Für diesen No-Codex-Produktionsvertrag gilt PASS nur solange **alle gebundenen Bytes unverändert** bleiben.

Eine Änderung an Input, Worker, Produktionscode, gebundener Abhängigkeit, Vertrag oder relevanter Ausgabe entwertet die Abnahme. Danach müssen erneut ausgeführt werden:

1. vollständige Fehlerhistorie / 27 Negativtests;
2. vollständiger Null-bis-Ende-Lauf A;
3. vollständiger Null-bis-Ende-Lauf B;
4. Byte- und Feldvergleich A/B;
5. Parent-Handoff-Integritätsvergleich;
6. Vertrags-Negativsuite.

Kein PASS aus Teiltests, Codeansicht, Erinnerung oder äquivalenten Fixtures.

## Frühere reale Blocker

Frühere Codex-/Realweg-Blocker wie private Worker-Python-Runtime, freier Factory-Aufruf, nichtkanonische Kategorie, ungebundener Plan-Slot und `PPM679_QUALITY_BINDING_MISSING` bleiben Teil der Regression und dürfen nicht aus der Fehlerhistorie entfernt werden.

Historische Fixture-/Goldplan-PASS gelten nicht als aktuelle Produktionsabnahme.

## NEXT ACTION

Der **No-Codex-Produktionsvertrag selbst ist nach dem aktuell bewiesenen Stand PASS**.

PR #255 bleibt trotzdem **Draft / unmerged / unpublished**. Es erfolgt kein Merge oder Publish ohne ausdrückliche User-Freigabe.

Ein Codex-Lauf ist nicht Bestandteil dieses Vertrages und bleibt verboten, solange der User nicht ausdrücklich mit den Worten **„Starte Codex“** freigibt.
