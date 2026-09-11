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
STATUS: INFRASTRUKTUR CLOSED / 0.8.4 LOCAL HARD + WORDPRESS-LIVE PASS / FACHLICHE 175-GRUPPEN-RECHERCHE WEITER OFFEN

0.8.4 bindet 175/175 Portalgruppen, vollständige Paar-Coverage ohne Top-N und Research-Vollständigkeit fail-closed `UNPROVEN`.

## PV-FAMILY-085-001 – Readiness zählte Herstellerbezeichnungen statt Herstellerfamilien

STATUS: CLOSED IM 0.8.5-KANDIDAT / WORDPRESS-LIVE-VORCHECK OFFEN

### Befund

Im vorhandenen Schermaschinen-Recherchebestand stehen Herstellerbezeichnungen:
- `Aesculap/Kerbl`;
- `Kerbl`.

Der Paarplaner normalisierte beide bereits korrekt auf dieselbe Herstellerfamilie `kerbl-family` und erzeugte deshalb 0 echte Cross-Brand-Paare.

Die 0.8.4-Gruppenreadiness konnte rohe Herstellerstrings dagegen als zwei Hersteller zählen.
Damit wäre theoretisch ein falsches `PAIRING_READY` möglich gewesen.

### KISS-Fix 0.8.5

Eine Herstellerfamilien-Wahrheit für:
- Research-Kandidaten-Herstellerzahl;
- Inventar-Readiness;
- Cross-Brand-Paaruniversum;
- Paarplaner.

Die bestehende Planner-Normalisierung wird wiederverwendet, nicht dupliziert.

### Harter Beleg

- Aesculap/Kerbl + Kerbl => genau 1 Herstellerfamilie;
- Schermaschinen => 0 Cross-Family-Paare und `INSUFFICIENT_MANUFACTURERS`;
- synthetischer echter zweiter Hersteller `Lister` => 2 Familien und exakt 4 Cross-Family-Paare;
- drei unabhängige Rückfallmutationen korrekt ROT;
- komplette finale Fresh-ZIP-Regression 35/35 PASS;
- PHP-Lint 50/50;
- Source↔ZIP 71/71;
- Report-Hashes 70/70.

## PV-FACH-085-002 – vorhandene Mehrhersteller-Recherche war mangels Profil nicht nutzbar

STATUS: PARTIAL CLOSED IM 0.8.5 / LIVE-VORCHECK OFFEN / MARKT-RECHERCHEVOLLSTÄNDIGKEIT WEITER UNPROVEN

### Geschlossener Teil

Fachprofile/Decision-Policies gebunden für vorhandene echte Mehrhersteller-Gruppen:
- Winterdecken 20 Paare;
- Übergangsdecken 14;
- Stalldecken 28;
- Unterdecken 63;
- Steigbügel 5.

Insgesamt 130 zusätzliche echte Cross-Family-Paare.

### Weiter offen

Diese Aktivierung bedeutet **nicht**, dass der Markt vollständig recherchiert ist.
Fehlende Hersteller/Modelle werden weiter systematisch ergänzt.
Research-Vollständigkeit bleibt `UNPROVEN` bis gruppenspezifischer echter Beleg vorliegt.

## Aktueller erster offener Arbeitsblock

Kein 0.8.5-Reparaturfehler lokal belegt.
Nächster Schritt: WordPress-Live-Vorcheck 0.8.5, danach weitere Produktrecherche/Profilskalierung.

Keine künstlichen SEO-PASS-Werte.
Kein Writer/Draft/Publish.

## Regel

Neue Produktvergleichsfehler werden ausschließlich hier ergänzt.
Das zentrale Fehlerregister bleibt Wegweiser.
