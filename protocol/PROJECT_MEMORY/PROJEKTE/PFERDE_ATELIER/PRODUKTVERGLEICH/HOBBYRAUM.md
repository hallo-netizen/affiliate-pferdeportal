# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-09
STATUS: AKTIV / PV-LIVE-001 / 0.7.1 WORDPRESS-RETEST

## AKTUELLER AUFTRAG

Den realen 0.7.0-WordPress-Fehler `PV-LIVE-001` im bestehenden Gesamtworkflow reparieren.

## AUSGANGSPUNKT

Realer Livebefund:
- 8 Regendecken-Kandidaten;
- 16 Provider-Aufrufe / $0.1920;
- danach 0 SEO-PASS, 8 blockiert, 0 Dossiers;
- trotzdem grünes `PASS`;
- post-run Kostenfeld zeigte $0.0000 mit irreführender Beschriftung `dieses Laufs`.

Autoritative Fehlerquelle:
`FEHLERQUELLEN.md`.

Technischer Hobbyraum:
`hobbyroom/productvergleich-workflow-v070-20260908`

## KISS-KORREKTUR

Nur:
1. finaler Workflowstatus kennt `NO_ELIGIBLE_COMPARISONS`;
2. dieser Status wird nie als Success-Notice gerendert;
3. Run-Notice zeigt finalen SEO-PASS-/Blockiert-Stand;
4. Kostenfeld wird als Schätzung für einen **jetzt neu gestarteten** Lauf beschriftet;
5. exakter 8→16→8 BLOCKED→0-Dossier-Livefall wird Regressionstest.

Keine neue Architektur. Kein Writer. Kein Draft. Kein Publish.

## PFLICHTPRÜFUNG VOR NÄCHSTER ZIP

- bestehende 0.6/0.7 Regressionen;
- exakter PV-LIVE-001-Negativfall;
- echter A-gegen-B-SEO-Positivfall;
- generische Anfrage negativ;
- Same-Brand negativ;
- Vergleichbarkeit negativ;
- Provider PARTIAL negativ;
- Dossier-/Profil-Drift negativ;
- autoritative PSTE-0.56.25-Kostenrate;
- Admin-Notice Positiv/Negativ;
- PHP-Lint;
- statische Write-/Publish-Grenzen;
- komplette Suite aus frisch gepackter ZIP in leerem Verzeichnis.

## NEXT ACTION

**Einziger nächster Schritt: realer WordPress-Retest mit genau 0.7.1.**

1. vorhandenes Universal Product Comparison durch 0.7.1 ersetzen;
2. Produktvergleich → Vergleichsplanung → Regendecken;
3. Gesamtworkflow starten;
4. Screenshot zurückgeben.

Erwartung für denselben Nachfragemangel:
- **kein grünes PASS**;
- Status `NO_ELIGIBLE_COMPARISONS`;
- 0 SEO-PASS / 8 blockiert / 0 Dossiers;
- tatsächliche Providerkosten bleiben im Run-Notice sichtbar;
- Kostenfeld darunter bezeichnet eindeutig nur einen **neuen** Lauf.

Kein weiterer Pluginstand vor diesem Retest.
