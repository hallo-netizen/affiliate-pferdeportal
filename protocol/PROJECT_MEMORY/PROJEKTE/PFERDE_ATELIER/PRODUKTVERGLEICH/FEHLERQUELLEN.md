# PRODUKTVERGLEICH – AUTORITATIVE FEHLERQUELLE

STAND: 2026-09-11
ROLLE: einzige detaillierte Fehlerquelle für den aktuellen PRODUKTVERGLEICH-Arbeitsweg.

## PV-ERR-001 – falsche WordPress-Kategoriehierarchie
STATUS: CLOSED

## PV-ERR-002 – historischer eigener Draftweg
STATUS: CLOSED / NICHT MEHR ZIELARCHITEKTUR

## PV-ERR-003 – falscher Hauptmenü-Positivtest
STATUS: CLOSED / ECHTER WP-LIFECYCLE ALS PFLICHT ERHALTEN

## PV-LIVE-001 – falsches PASS bei null geeigneten Vergleichen
STATUS: CLOSED / LIVE 0.8.1–0.8.4 BESTÄTIGT / REGRESSION AKTIV

## PV-ERR-004 – PASS ohne realen Dossier-Receipt
STATUS: CLOSED IM 0.8.1+ / REGRESSION AKTIV

## PV-COST-082-001 – bezahlte Produkt-/Paar-Zwischenergebnisse nicht dauerhaft genug gebunden
STATUS: CLOSED / LOKAL + WORDPRESS-LIVE 0.8.2–0.8.4 PASS

## PV-FACH-083-001 – Fachinterpretation nicht vollständig im Dossier gebunden
STATUS: CLOSED / 0.8.3 LOCAL HARD + WORDPRESS-LIVE-REGRESSION PASS

## PV-SCALE-084-001 – Proofgruppe statt vollständiger Vergleichsgruppen-Abdeckung

STATUS: INFRASTRUKTUR CLOSED / 0.8.4 LOCAL HARD + WORDPRESS-LIVE PASS / FACHLICHE 175-GRUPPEN-RECHERCHE+PROFILE WEITER OFFEN

### Ursprungsbefund

0.8.3 kannte nur die Proofgruppe Regendecken.
Die autoritative Portalstruktur enthält 175 Vergleichs-Produktgruppen.

### KISS-Fix 0.8.4

- 175/175 Gruppen portalgebunden;
- jede Gruppe live sichtbar/selectable;
- Readiness sichtbar;
- keine stille Auslassung;
- keine Top-N-/Pair-Cap;
- vollständiges Cross-Brand-Paaruniversum;
- fachlich unpassende Paare vor SEO/Providerkosten BLOCK;
- Coverage-Receipt;
- Research-Kandidaten und Markt-Recherchevollständigkeit strikt getrennt;
- Key-Kollisionen fail-closed statt stiller Verschmelzung.

### Harter lokaler Beleg

- finale Fresh-ZIP 32/32 Tests PASS;
- PHP-Lint 48/48;
- Source↔ZIP 67/67;
- Report-Hashes 66/66;
- 175/175 Portalparität;
- 50 Produkte / 5 Hersteller -> 1000 Cross-Brand-Paare vollständig;
- 500 fachlich sinnvoll, 500 falsche Nutzungsklasse BLOCKED;
- fünf 0.8.4-Mutationen korrekt ROT.

### WordPress-Live-Beleg 0.8.4

Vor Lauf:
- Version 0.8.4;
- 175/175 Gruppen sichtbar;
- Regendecken PAIRING_READY;
- Research UNPROVEN;
- 172 PROFILE_MISSING;
- 2 Key-Kollisionen;
- PSTE PASS/READY;
- $0.0000 maximale neue Providerkosten.

Nach genau einem Regendecken-Gesamtworkflow:
- `NO_ELIGIBLE_COMPARISONS`;
- Provider-Aufrufe 0;
- Kosten $0.0000;
- SEO-PASS 0;
- blockiert 8;
- Dossiers 0.

Damit ist die **Registry-/Coverage-Infrastruktur 0.8.4 geschlossen**.

### Weiter offener fachlicher Skalierungsauftrag

Kein Infrastrukturfehler, sondern noch nicht abgeschlossene Facharbeit:
- Produktrecherche möglichst vollständig für alle 175 Vergleichsgruppen;
- gruppenspezifische Vergleichsprofile/Decision-Policies;
- alle daraus sinnvollen A-vs-B-Paare;
- Research-Vollständigkeit nur bei echtem Beleg;
- positiver Dossier-V2-Livefall bei erstem realen SEO-PASS.

Keine künstlichen SEO-PASS-Werte.
Kein Writer/Draft/Publish.

## Regel

Neue Produktvergleichsfehler werden ausschließlich hier ergänzt.
Das zentrale Fehlerregister bleibt Wegweiser.
