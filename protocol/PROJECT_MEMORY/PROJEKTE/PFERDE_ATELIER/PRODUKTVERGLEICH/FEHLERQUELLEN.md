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

## PV-SCALE-084-001 – Proofgruppe statt vollständiger Vergleichsgruppen-Abdeckung

STATUS: PARTIAL CLOSED / 0.8.4 REGISTRY+COVERAGE LOCAL HARD PASS / WORDPRESS-LIVE-RETEST OFFEN / PRODUKTRECHERCHE+PROFILE 175-GRUPPEN-GESAMTZIEL WEITER OFFEN

### Ursprungsbefund

0.8.3 kannte in der auswählbaren Profilkonfiguration nur Regendecken.
Die autoritative Portalstruktur enthält jedoch:
- 329 Produktseiten;
- 1124 Themenkategorien;
- **175 eindeutige Produktgruppen mit eigener `Vergleich`-Kategorie**.

Regendecken ist 1/175.

### KISS-Fix 0.8.4 – lokal belegt

0.8.4 ergänzt keine 175 PHP-Hardcodes, sondern eine portalgebundene Datenregistry + Coverage:
- 175/175 Gruppen exakt aus Portalquelle gebunden;
- jede Gruppe sichtbar;
- fehlendes Profil/Policy/Inventar bleibt sichtbar OPEN/BLOCKED;
- keine stille Auslassung;
- keine willkürliche Gruppen-/Paarobergrenze;
- Same Brand und fachlich unpassende Nutzung vor Providerkosten ausgesondert;
- vollständiges Cross-Brand-Paaruniversum je vorbereiteter Gruppe;
- Coverage-Receipt;
- Research-Kandidaten und Markt-Recherchevollständigkeit getrennt.

### Harter Beleg 0.8.4

Finale Fresh-ZIP:
- 32/32 ausführbare Tests PASS;
- PHP-Lint 48/48 PASS;
- Source↔ZIP 67/67;
- Report-Hashes 66/66;
- 175/175 Portalparität PASS;
- Großtest 50 Produkte / 5 Hersteller -> 1000 Cross-Brand-Paare vollständig;
- davon 500 fachlich vergleichbar, 500 falsche Nutzungsklasse sichtbar BLOCKED;
- Reihenfolge/Dubletten verändern Coverage nicht;
- fünf 0.8.4-Mutationen korrekt ROT.

### Research-Hard-Rule

Der aktuelle Product-Knowledge-Recherchekatalog enthält Produktkandidaten, aber **keinen Markt-Vollständigkeitsbeleg**.

Daher 0.8.4:
`research_completeness_status = UNPROVEN` für 175/175, bis echte gruppenspezifische Vollständigkeit bewiesen ist.

Vorhandene sinnvolle Paare dürfen bereits geprüft werden; fehlende Produkte/Hersteller bleiben als Recherchearbeit offen.

### Portal-Key-Kollision

Zwei autoritative Portal-Slugs besitzen denselben kurzen Key `weidezaungeraete`.
0.8.4 verschmilzt sie nicht still, sondern zeigt `GROUP_KEY_COLLISION`.

### Weiter offener Teil desselben Skalierungsziels

Nach 0.8.4-LIVE-PASS:
- Produktrecherche möglichst vollständig für alle 175 Vergleichsgruppen;
- gruppenspezifische fachliche Profile/Decision-Policies;
- alle daraus sinnvollen A-vs-B-Paare;
- globale Coverage ohne stille Lücke;
- positiver Dossier-V2-Livefall.

Keine künstlichen SEO-PASS-Werte.
Kein Writer/Draft/Publish.

## Regel

Neue Produktvergleichsfehler werden ausschließlich hier ergänzt.
Das zentrale Fehlerregister bleibt Wegweiser.
