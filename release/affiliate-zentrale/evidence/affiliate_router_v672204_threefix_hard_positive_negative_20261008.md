# Affiliate Zentrale 6.72.204 – fokussierter Dreifach-Härtetest

Datum: 2026-10-08

## Exakter Scope
Ausschließlich:
1. Glossar-Einzelbeiträge: Banner wieder sichtbar; bestehender Desktop-/Mobil-Formatvertrag bleibt.
2. Pferderassen-Einzelbeiträge: Banner wieder sichtbar; bestehender Desktop-/Mobil-Formatvertrag bleibt.
3. Beiträge mit `[affiliate_rechner]`: kein automatischer Inline-/Mid-Banner im Text; unterer Banner bleibt; Produktboxen bleiben.

Keine sonstige Affiliate-Fachlogik wurde für diesen Fix geändert.

## Lokale harte Simulation
- PASS: 43
- FAIL: 0
- Positiv/Negativ: aktuelle und alte Designversionsklassen, fehlende Marker/Anker, Duplicate-Guard, Desktop-only/Mobile-only, exakte Formatgrenzen inkl. max. 10 % Upscale, falsche Ratio, Rechner-Shortcode vs. Klartext, Inline aus / Bottom an / Produkte unverändert.

## Frisches WordPress + MariaDB
- Workflow Run: 37762816137
- Ergebnis: SUCCESS
- Plugin aktiv: 6.72.204
- Manifest: 28 Dateien
- Source-Manifest SHA256: 7e9b510c6021cd44ccbd0630d712a48a5a2997f968382494b2912bf21b34a660
- PHP-Syntax: PASS
- Fokussierter Positiv-/Negativtest: 52 PASS / 0 FAIL
- Format-Matcher: reale `output_row_matches_slot_rule()`-Regel geprüft
- Performance/DB-Scope: keine neue Frontend-DB-Abfrage, kein Frontend-HTTP, keine neue Tabelle
- Final ZIP Byteidentität: 28/28 PASS

## Exakter getesteter Installer
- Datei: AFFILIATE_ZENTRALE_6.72.204.zip
- SHA256: aea45135ced0606c3aa63aa2b2489213d1a2b4b2b5c03cfdb494e3c163d6de92
- Bytes: 820403
- Workflow Artifact ID: 11542523698

Ergebnis: **THREE_FOCUSED_6_72_204_GATES_PASS**
