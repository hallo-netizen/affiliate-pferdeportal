# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-09
STATUS: AKTIV / PV-LIVE-002+003 / 0.8.0 GESAMTWORKFLOW-KORREKTUR

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

0.8.0 ausschließlich intern im Hobbyraum fertigstellen.

Pflicht vor irgendeiner neuen ZIP:
1. echte Produktnachfrage A + B ohne direkte Paaranfrage => Vergleich kann PASS werden;
2. direkte A-gegen-B-Nachfrage => PASS;
3. nur A oder nur B Nachfrage => BLOCKED;
4. keine Nachfrage => NO_ELIGIBLE;
5. generische Gruppenanfrage => kein konkretes Produkt-/Paar-Signal;
6. alte 0.7.x-Signale => stale/research again;
7. abgelaufene Signale => stale;
8. frische positive Signale gegen aktuellen Inventory-/Structure-/Cannibalization-Stand revalidieren;
9. kompletter Workflow bis Dossier in einem Test;
10. Provider-Teilfail, Same-Brand, falsche Produktklasse, Drift und Dubletten negativ;
11. echte PSTE-0.56.25-Kostenobergrenze;
12. komplette bestehende Regression;
13. Mutationstests müssen beweisen, dass die neuen Tests alte fehlerhafte Logik wirklich abfangen;
14. Fresh-ZIP erneut komplett testen und bytegleich zum geprüften Source-Stand.

Kein Writer, kein Draft, kein Publish. Keine Zwischen-ZIP.
