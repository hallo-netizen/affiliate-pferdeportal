# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-11
STATUS: AKTIV / 0.8.5 FINAL-FRESH-ZIP LOCAL PASS / WORDPRESS-LIVE-VORCHECK OFFEN

## AKTUELLER KANDIDAT

`universal-product-comparison-0.8.5-prototype.zip`

SHA-256:
`0174051e6584902142f5be5787642426b30aab6c7ba15ef0b07ccbdb4a5844fd`

Ausgangsbasis:
exakt geprüfte 0.8.4-ZIP.

## WAS 0.8.5 NEU ÖFFNET

Zusätzliche fachlich gebundene vorhandene Gruppen:
- Winterdecken: 20 Cross-Family-Paare;
- Übergangsdecken: 14;
- Stalldecken: 28;
- Unterdecken: 63;
- Steigbügel: 5.

Summe: **130 zusätzliche sinnvolle Paar-Kandidaten** aus bereits vorhandener Product-Knowledge-Recherche.

Schermaschinen besitzt zwar ein Fachprofil, bleibt aber `INSUFFICIENT_MANUFACTURERS`, weil `Aesculap/Kerbl` und `Kerbl` dieselbe Herstellerfamilie sind.

## HARTER LOKAL-PASS

- 35/35 Regression PASS;
- 50/50 PHP-Lint PASS;
- Source↔ZIP 71/71;
- Report-Hashes 70/70;
- 175/175 Portalabdeckung weiter PASS;
- 130/130 echte Cross-Family-Paare erhalten;
- Herstellerfamilienregel für Readiness und Planner identisch;
- drei neue Mutationen korrekt ROT;
- bestehende Regressionen/Mutation Guards weiter PASS;
- kein Auto-Publish.

## NEXT ACTION WORDPRESS

1. ausschließlich 0.8.5 installieren/ersetzen;
2. `Produktvergleich` öffnen;
3. **keinen Gesamtworkflow starten**;
4. Screenshot des oberen Coverage-Bereichs;
5. erwartet:
   - Version `0.8.5-prototype`;
   - 175/175 Gruppen;
   - `PAIRING_READY: 6`;
   - `PROFILE_MISSING: 166`;
   - `INSUFFICIENT_MANUFACTURERS: 1`;
   - `GROUP_KEY_COLLISION: 2`;
   - Research-Kandidaten: mehrere echte Herstellerfamilien in 6 Gruppen, nur eine Herstellerfamilie in 8 Gruppen;
6. danach Winterdecken auswählen und nur `Vorschau aktualisieren` / read-only prüfen;
7. erwartet Winterdecken:
   - `PAIRING_READY`;
   - 8 vorhandene Produkte;
   - 3 Herstellerfamilien;
   - vollständiges Cross-Family-Paaruniversum 20;
   - Research-Vollständigkeit weiterhin `UNPROVEN`;
8. vor jedem möglichen Providerlauf zuerst Kostenanzeige prüfen;
9. nichts veröffentlichen.

## DANACH

Keine weitere Plugin-Fixschleife, wenn Live-Vorcheck passt.
Dann fachlich weiter:
- Ein-Hersteller-Gruppen mit echten Konkurrenzherstellern vervollständigen;
- fehlende Faktenmatrix je Modell hart belegen;
- erst dann Product Knowledge erweitern;
- danach weitere Profile;
- pro Gruppe alle sinnvollen Paare, keine künstliche Obergrenze.

## BLOCK-GRENZE

BLOCK bei:
- falscher Version/SHA;
- Verlust der 175er Registry;
- weniger als die erwarteten 130 neuen echten Cross-Family-Paare;
- Schermaschinen fälschlich `PAIRING_READY` ohne echten zweiten Hersteller;
- roher Herstellername statt Herstellerfamilie als Readiness-Wahrheit;
- Research-Vollständigkeit fälschlich COMPLETE;
- Top-N-/Pair-Cap;
- Providerlauf ohne vorherige Kostenanzeige;
- Writer-/Draft-/Publish-Aktivierung.

Kein SEO/TEXT-/ACM-Umbau.
Kein Publish.
