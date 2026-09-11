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
STATUS: INFRASTRUKTUR CLOSED / ERSTER 175ER RESEARCH-DURCHLAUF 97/78/0 / FACHLICHE VOLLSTÄNDIGKEIT WEITER OFFEN

Geschlossen:
- 175/175 Portalgruppen in Registry;
- jede Gruppe sichtbar;
- keine stille Top-N-/Pair-Cap;
- Research-Vollständigkeit fail-closed `UNPROVEN`;
- erster Research-Durchlauf: 97 `EVIDENCE_PRESENT`, 78 `PARTIAL_AMBIGUOUS`, 0 `NO_GROUP_EVIDENCE`.

Weiter offen:
- 78 Partial-Gruppen nach Ursache klassifizieren;
- Markt-/Produktrecherche dort fortsetzen, wo wirklich `MORE_MARKET_RESEARCH_REQUIRED` gilt;
- gruppenspezifische Profile/Policies/Product Knowledge vervollständigen;
- alle daraus entstehenden fachlich zulässigen Paare.

## PV-FAMILY-085-001 – Readiness zählte Herstellerbezeichnungen statt Herstellerfamilien
STATUS: CLOSED IM 0.8.5 / LOKAL HART PASS

KISS-Fix:
Eine Herstellerfamilien-Wahrheit für Research-Zählung, Inventar-Readiness, Paaruniversum und Planner.

Harter Beleg:
- Aesculap/Kerbl + Kerbl => 1 Familie;
- synthetischer echter zweiter Hersteller => erwartete Cross-Family-Paare;
- drei Mutationen korrekt ROT;
- finale 0.8.5-Regression 35/35 PASS.

## PV-FACH-085-002 – Fachprofile für vorhandene Mehrhersteller-Recherche
STATUS: PROFILE/POLICY LOCAL PASS / ALT-BASIS LIVE MATERIALISIERT / REALE POST-BATCH-PAARZAHL NOCH NICHT SEPARAT ABGELESEN / MARKTVOLLSTÄNDIGKEIT UNPROVEN

Fachprofile/Policies sind lokal gegen freigegebene Recherchekandidaten geprüft für:
- Winterdecken;
- Übergangsdecken;
- Stalldecken;
- Unterdecken;
- Steigbügel.

Die lokal berechneten 130 Cross-Family-Paare waren **Katalogpotential nach erfolgreicher Materialisierung**, nicht vorab bewiesene Live-Paarzahlen.

Der 0.5.1-Live-Batch hat die alte Recherchebasis real geprüft/materialisiert. Eine globale tatsächliche Live-Paarzahl nach diesem Batch wurde im Produktvergleich nicht separat abgelesen und wird daher nicht behauptet.

## PV-TEST-085-003 – Recherchekandidaten im Lokaltest als materialisiertes Inventar behandelt
STATUS: CLOSED / TESTGRENZE KORRIGIERT / UPK 0.5.1 LOCAL HARD + WORDPRESS-LIVE-BATCH ABGESCHLOSSEN

Der 0.8.5-Live-Gegenbeleg zeigte korrekt:
- Research-Kandidaten werden nicht automatisch Product Knowledge;
- fehlendes Inventar bleibt `PRODUCT_INVENTORY_MISSING`;
- kein Paar/SEO-/Providerlauf wird erfunden;
- Kosten bleiben $0.0000.

UPK 0.5.1 schloss ausschließlich die echte Materialisierungslücke über den vorhandenen kanonischen `UPK_Research::run_product_group()`-Weg.

## PV-LIFECYCLE-086-001 – abgekündigte/unklare Produkte blieben im aktuellen Paaruniversum
STATUS: CLOSED IM 0.8.6 LOCAL HARD + FRESH-ZIP / WORDPRESS-LIVE OFFEN

### Realer Befund

Autoritative Ausgangsbasis war die exakt hashgebundene UPC-0.8.5-ZIP.

0.8.5 las `list_products_by_group()` bei jeder Planung neu, filterte aber den von UPK gelieferten `lifecycle_status` weder vor Pairing noch vor Readiness-Zählung.

Harter Solltest gegen unveränderte 0.8.5:
- zwei `ACTIVE`-Produkte;
- ein ansonsten vergleichbares `DISCONTINUED`-Produkt.

Ergebnis ROT:
- `candidate_count = 3` statt 1;
- `manufacturer_count = 3` statt 2;
- das abgekündigte Produkt blieb in zwei Paaren.

### KISS-Fix 0.8.6

Paarbar:
- `ACTIVE`;
- `TEMPORARILY_UNAVAILABLE`.

Fail-closed ausgeschlossen:
- `DISCONTINUED`;
- `UNKNOWN`;
- fehlender Lifecycle.

Deduplizierung erfolgt vor Lifecycle-Prüfung, damit eine ältere ACTIVE-Zeile nicht wieder auflebt, wenn der neueste kanonische Stand bereits abgekündigt ist.

`TEMPORARILY_UNAVAILABLE` bleibt bewusst paarbar: temporäre Angebotssituation ist Commerce/AFFILIATE und darf nicht allein die fachliche Modellgültigkeit entfernen.

### Harter Beleg

Exakt geprüfte Fresh-ZIP:
`universal-product-comparison-0.8.6-prototype.zip`

SHA-256:
`6ad160d18fb0973463c214de4356447923cbb728e222725e5407868e580c24f6`

- Working Tree 38/38 Regression PASS;
- zwei Lifecycle-Mutationen korrekt ROT;
- PHP-Lint 51/51 PASS;
- Source↔Fresh-ZIP 74/74 exakt;
- Report-Hashes 73/73 exakt;
- Fresh-ZIP Regression 38/38 PASS;
- Fresh-ZIP PHP-Lint 51/51 PASS.

Dauerbeleg:
`AKTENSCHRANK/39_V086_LIFECYCLE_REEVALUATION_HARD_LOCAL_RECEIPT.md`.

## AKTUELLER ERSTER OFFENER ARBEITSBLOCK

Kein zweiter Pluginfehler wird vermutet oder vorweggenommen.

Aktive Arbeit:
**Gesamtaudit im exakt geprüften 0.8.6-Stand am nächsten ungeklärten Punkt fortsetzen: zuerst beweisen, dass Research-Evidence ohne materialisiertes Product Knowledge kein Paar erzeugen kann.**

Danach nur bei PASS:
Nicht-V1-Gruppen fail-closed, SEO ohne Fach-Override und bestehender Dossier-Neuaudit.

Keine künstlichen SEO-PASS-Werte.
Kein Writer/Draft/Publish.
Kein Merge.
Kein Publish.

## Regel

Neue Produktvergleichsfehler werden ausschließlich hier ergänzt.
Das zentrale Fehlerregister bleibt Wegweiser.
