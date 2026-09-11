# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-11
STATUS: AKTIV / 0.8.4 FINAL-FRESH-ZIP LOCAL PASS / WORDPRESS-LIVE-RETEST OFFEN

## AKTUELLER KANDIDAT

`universal-product-comparison-0.8.4-prototype.zip`

SHA-256:
`00035ec0e166d9830f97140b6fc0f4f7666504d548bac507b1b206a2173ce856`

Ausgangsbasis:
exakt geprüfte 0.8.3-ZIP.

## WAS 0.8.4 NEU BELEGT

- autoritative 175/175 Vergleichsgruppen-Registry;
- alle Gruppen sichtbar auswählbar;
- Readiness je Gruppe sichtbar statt stiller Auslassung;
- `PAIRING_READY`, `PROFILE_MISSING`, `POLICY_MISSING`, `PRODUCT_INVENTORY_MISSING`, `INSUFFICIENT_MANUFACTURERS`, `GROUP_KEY_COLLISION` fail-closed;
- vollständiges Cross-Brand-Paaruniversum ohne Top-N-Limit;
- fachlich unpassende Paare sichtbar BLOCKED vor SEO-/Providerkosten;
- Research-Kandidaten und Research-Vollständigkeit strikt getrennt;
- vorhandene Recherche aus Product Knowledge bleibt sichtbar;
- keine falsche Behauptung „Markt vollständig recherchiert“.

## HARTER LOKAL-PASS

Finale Fresh-ZIP:
- 32/32 Tests PASS;
- 48/48 PHP-Lint PASS;
- Source↔ZIP 67/67;
- Report-Hashes 66/66;
- 175/175 Portalparität;
- 50-Produkte-Test: 1000/1000 Cross-Brand-Paare erhalten;
- davon 500 sinnvoll COMPARABLE / 500 Nutzungsklasse BLOCKED;
- fünf 0.8.4-Mutationen korrekt ROT;
- bestehende 0.8–0.8.3 Regression weiter PASS;
- kein Auto-Publish.

## NEXT ACTION WORDPRESS

1. ausschließlich 0.8.4 installieren/ersetzen;
2. WordPress neu laden;
3. `Produktvergleich` öffnen;
4. **noch keinen Workflow starten**;
5. zuerst prüfen:
   - Version 0.8.4-prototype;
   - Produktgruppen-Dropdown zeigt deutlich mehr als Regendecken / 175er Portalabdeckung;
   - Regendecken bleibt vorhandener Proofstand;
   - alte SEO-Endstände bleiben erhalten;
   - für unveränderten Regendecken-Bestand weiterhin $0.0000 neue Providerkosten;
   - nicht vorbereitete Gruppen zeigen sichtbar PROFILE/POLICY/INVENTORY-Lücken und starten keinen Providerlauf;
6. Screenshot an Arbeitschat zurückgeben;
7. erst danach genau einen Regendecken-Regressionslauf;
8. nichts veröffentlichen.

## DANACH

Nach LIVE-PASS 0.8.4 beginnt hier **nicht** eine Plugin-Fixschleife, sondern der fachliche Skalierungsblock:
- bestehende 14 recherchierten Vergleichsgruppen zuerst vollständig auswerten;
- fehlende Hersteller/Produkte sichtbar nachrecherchieren;
- Profile/Decision-Policies nur fachlich gebunden ergänzen;
- danach weitere der 175 Gruppen;
- pro Gruppe alle sinnvollen A-vs-B-Paare, keine willkürliche Obergrenze.

## BLOCK-GRENZE

BLOCK bei:
- falscher Version/SHA;
- weniger/mehr als 175 autoritative Vergleichsgruppen ohne Quelländerung;
- still fehlender Gruppe;
- stillem Merge der `weidezaungeraete`-Kollision;
- Top-N-/Pair-Cap;
- falscher Research-Vollständigkeitsbehauptung;
- unerwarteten Providerkosten für bestehenden Regendecken-Stand;
- unerwartetem Writer-/Draft-/Publishweg.

Kein SEO/TEXT-/ACM-Umbau.
Kein Publish.
