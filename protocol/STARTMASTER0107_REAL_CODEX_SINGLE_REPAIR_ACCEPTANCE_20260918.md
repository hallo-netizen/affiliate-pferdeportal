# STARTMASTER0107 — Freigabe: genau ein realer Codex-Repair-Beweis

Stand: 18.09.2026

## Status

Die Test-/Proof-Lücke ist geschlossen.

- PR #331: gemergt auf `1431bf52ea73932c809d242a429cdd62e7b93a0b`.
- System-4A Real Acceptance Run `35389785292`: PASS.
- Hardlock Run `35389831741`: PASS.
- Hardlock-Base Run `35389831731`: PASS.
- PPM 6.7.9, LanguageTool 6.8, Qualitätsgrenzen, Textregeln, Design und Produktionsarchitektur unverändert.

## Textqualität und Struktur bleiben getrennt

Der vom Nutzer gelieferte Codex-Artikel zu Putzplatzmatten ist als hashgebundener positiver `CONTENT_ONLY`-Qualitätsanker gespeichert. Er beweist ausdrücklich keine Strukturkonformität und keinen Fullcheck-/Produktions-PASS. Er darf nicht als vorbereitete Reparaturdatei oder PASS-Fixture verwendet werden.

## Nutzerfreigabe Codex

Der Nutzer hat am 18.09.2026 Codex ausdrücklich bis zum Morgen des 19.09.2026 bzw. bis zum Erreichen des Codex-Nutzungslimits freigegeben.

## Genau erlaubter Realtest

Genau ein frischer realer Codex-Artikel-0-Repair-Acceptance-Lauf.

- Kein Artikel 1.
- Kein Batch-Advance.
- Kein 7er-Lauf.
- Kein Publish.
- Keine WordPress-Schreibaktion.
- Keine Code-/Regel-/Architekturänderung während des Realtests.

Wenn der erste echte Fullcheck `REPAIR_REQUIRED` liefert, müssen vor jeder Reparatur dauerhaft erfasst werden:

- exakte Artikelbytes vor Repair;
- SHA-256 des Artikels;
- kompletter Findings-Payload;
- SHA-256 des Findings-Payloads;
- Workspace-State und Revision.

Danach darf nur Codex denselben Artikel reparieren. Anschließend läuft wieder der echte Fullcheck. Bei weiterem `REPAIR_REQUIRED` bleibt derselbe Artikel gebunden.

Bei finalem PASS müssen dauerhaft erfasst werden:

- exakte finale Artikelbytes;
- finaler SHA-256;
- finale Revision;
- LanguageTool PASS;
- PPM PASS;
- PPM `CONTENT_QUALITY_CHECK_OK`.

Die dauerhafte Evidence wird im PR-107-Terminalkommentar mit SHA-256 und Base64 für Vorher-Artikel, Findings je Repair-Zyklus und finalen Artikel ausgegeben. Damit bleibt sie auch bei Workspace-Verlust rekonstruierbar.

Ein Mock, deterministischer Testworker oder eine vorbereitete `final`-Fixture kann niemals `REAL_CODEX_REPAIR_PROVEN` erzeugen.

Wenn der Artikel ohne Repair direkt PASS erreicht, lautet das Ergebnis `REAL_CODEX_REPAIR_NOT_EXERCISED`; Artikel 1 bleibt trotzdem verboten.
