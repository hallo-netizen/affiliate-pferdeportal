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
STATUS: CLOSED / LIVE 0.8.1–0.8.3 BESTÄTIGT / REGRESSION AKTIV

## PV-ERR-004 – PASS ohne realen Dossier-Receipt
STATUS: CLOSED IM 0.8.1+ / REGRESSION AKTIV

## PV-COST-082-001 – bezahlte Produkt-/Paar-Zwischenergebnisse nicht dauerhaft genug gebunden
STATUS: CLOSED / LOKAL + WORDPRESS-LIVE 0.8.2/0.8.3 PASS

## PV-FACH-083-001 – Fachinterpretation nicht vollständig im Dossier gebunden
STATUS: CLOSED / 0.8.3 LOCAL HARD + WORDPRESS-LIVE-REGRESSION PASS

0.8.3 belegt für Regendecken:
- Dossier V2;
- Decision-Policy;
- Kostenwiederverwendung;
- fail-closed bei Null-Eignung;
- kein Auto-Publish.

## PV-SCALE-084-001 – Produktvergleich deckt nur Proofgruppe Regendecken statt aller Vergleichs-Produktgruppen ab

STATUS: OPEN / AKTUELLER ERSTER OFFENER PUNKT

### Befund

Die autoritative Portalstruktur enthält:
- 329 Produktseiten;
- 1124 Artikelkategorien;
- **175 eindeutige Produktgruppen mit eigener Themenkategorie `Vergleich`**.

0.8.3 bietet in `comparison-profiles.json` nur `regendecken` an.

Damit ist der Mechanismus bewiesen, die fachliche Portalabdeckung aber nicht vollständig.

### Ziel

Für jede der 175 Vergleichsgruppen:
- möglichst vollständiger realer Produktbestand;
- alle fachlich zulässigen A-vs-B-Paare;
- vollständige terminale SEO-Prüfung oder explizit offener Status;
- Dossier V2 für reale SEO-PASS-Paare;
- vollständiger Coverage-Nachweis.

### Hard Rules

- keine stille Auslassung von Gruppen;
- keine willkürliche Gruppen-/Paarobergrenze;
- fehlendes Profil/Policy/Inventar sichtbar BLOCK/OPEN;
- inkompatible Produkte vor Providerkosten aussortieren;
- Wiederaufnahme ohne doppelte Providerkosten;
- keine künstlichen SEO-PASS-Werte;
- PRODUCT_COMPARISON bleibt exakt A vs B;
- kein Writer/Draft/Publish.

### KISS-Fixrichtung

Generische, portalgebundene Registry + Coverage-Status.
Nicht 175 Gruppen im PHP-Code hartcodieren.
Gruppenspezifische Fachprofile bleiben Daten/Verträge und müssen vor READY vollständig gebunden sein.

## Regel

Neue Produktvergleichsfehler werden ausschließlich hier ergänzt.
Das zentrale Fehlerregister bleibt Wegweiser.
