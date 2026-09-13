# SYSTEM 4A — TESTNACHWEIS 2026-09-13

Belegdatei, keine zweite CURRENT_STATE. **Aktueller Status steht ausschließlich in `README.md`.**

## Aktueller No-Codex-Produktionsvertrag

Der aktuelle 4A-Stand besitzt einen exakt reproduzierbaren, Codex-freien Produktionsvertrag:

- `NO_CODEX_PRODUCTION_INPUT_V1.json`
- `NO_CODEX_PRODUCTION_WORKER_V1.py`
- `NO_CODEX_PRODUCTION_CONTRACT_V1.json`
- `no_codex_production_contract.py`

Der Vertrag bindet:

- Rohinput bytegenau;
- Worker bytegenau;
- produktionsrelevante Quellcode-Dateien über SHA256;
- LanguageTool 6.8;
- PPM 6.7.9;
- PPM Editorial Plan;
- PPM Kategoriequelle;
- PPM Artikeltyp-Templates;
- gepinnten WordPress-Snapshot;
- erwartete Artikelidentität, Plan-/Quality-Binding-Fingerprints und Handoff-Enddatei.

`codex_allowed=false`.

## Fehlerhistorie / Regression

Die Fehlerhistorie wurde vor der Abnahme vollständig geprüft und als ausführbarer Katalog erneut negativ ausgeführt.

- bekannte Fehlertypen: **27**;
- negativ ausgeführt: **27**;
- PASS: **27**;
- FAIL: **0**.

Die geprüften Klassen umfassen u. a. Fact-ID-/Fact-Pack-Abweichungen, Plan-Slot-Fehler, Context-/Runtime-Mismatch, Hash-/Manifest-Mismatch, Kategorie-/Linkbindung, Pflichtfeld-/Artikelidentitätsfehler, Batch-Kontext-Mismatch, Worker-/PASS-Autoritätsverletzungen, private Worker-Runtime und Handoff-/Inline-Manipulationen.

## Null-bis-Ende-Lauf

Der vollständige Produktionsweg wurde mit echten Prüfern ausgeführt:

`Schritt 0 / gebundener Input -> Root Entry -> Research -> Facts / Fact-Pack -> Context -> Authoring-Bindung -> Draft -> LanguageTool 6.8 -> Same-Article-Repair -> erneute Prüfung -> PPM 6.7.9 -> Same-Article-Repair -> erneute Prüfung -> Batch Gate -> Handoff-Erstellung -> Inline-Transport -> Parent-Chat-Entpackung -> finale Datei`

Ergebnis Lauf A:

- Root / Ingress: PASS
- Research: PASS
- Facts / Fact-Pack: PASS
- Context: PASS
- Supervisor-Authoring-Bindung: PASS
- Draft: PASS
- LanguageTool 6.8 echt: PASS nach Repair
- PPM 6.7.9 echt: PASS nach weiterem Same-Article-Repair
- Batch: PASS
- Handoff: PASS
- Parent-Chat-Integrität: PASS
- Revision: 3

Ergebnis Lauf B aus einem zweiten leeren Laufverzeichnis: identisch PASS.

## Reproduzierbarkeit

Die beiden vollständigen Läufe wurden aus getrennten leeren Laufverzeichnissen mit denselben Vertragsbytes erzeugt.

Bewiesen:

- Enddatei A = Enddatei B bytegleich;
- vollständige JSON-Felder A = B feldgleich;
- Parent-Chat A = Enddatei A bytegleich;
- Parent-Chat B = Enddatei B bytegleich;
- Enddateigröße jeweils **29.391 Byte**;
- Enddatei SHA256 jeweils `8a3fab64fb1e654257f12bb8c9ead716abbf3cf7f207d50c6b1c69d386ca1cc4`;
- `publish_allowed=false`.

## Vertrags-Negativsuite

Zusätzlich wurde der gebundene Produktionsvertrag gezielt manipuliert:

1. falscher Plan-Slot -> korrekt BLOCK;
2. falsche Kategorie -> korrekt BLOCK;
3. Worker-Byteänderung -> korrekt BLOCK;
4. Enddatei-Manipulation -> korrekt BLOCK;
5. Parent-Handoff-Manipulation -> korrekt BLOCK.

**5/5 PASS.**

## Abnahmegrenze

Dieser Nachweis gilt nur für exakt die gebundenen Vertrags- und Produktionsbytes.

Jede Änderung entwertet den PASS und verlangt erneut:

- 27/27 Fehlerhistorien-Negativtests;
- Null-bis-Ende A;
- Null-bis-Ende B;
- Byte-/Feldvergleich;
- Parent-Handoff-Integritätsvergleich;
- 5/5 Vertrags-Negativsuite.

Kein Teiltest, Fixture, Codeblick oder äquivalenter Ersatzweg darf als Produktionsabnahme gelten.

## Historische Befunde

Frühere grüne Fixture-/Goldplan-Läufe bleiben historische Architektur-/Diagnosebelege und sind keine aktuelle Produktionsabnahme.

Frühere reale Blocker — private Worker-Python-Runtime, freier Factory-Aufruf, nichtkanonische Kategorie, ungebundener Plan-Slot und `PPM679_QUALITY_BINDING_MISSING` — bleiben als Regressionen erhalten.

## Aktueller Nachweisstatus

**NO-CODEX-PRODUKTIONSVERTRAG: PASS.**

PR #255 bleibt **Draft / unmerged / unpublished**. Kein Codex ohne ausdrückliche User-Freigabe **„Starte Codex“**.
