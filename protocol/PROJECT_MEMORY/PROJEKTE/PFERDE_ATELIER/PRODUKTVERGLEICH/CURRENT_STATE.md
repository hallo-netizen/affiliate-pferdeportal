# PRODUKTVERGLEICH – CURRENT STATE

STAND: 2026-09-11
STATUS: AKTIV / 0.8.4 FINAL-FRESH-ZIP LOCAL HARD PASS / WORDPRESS-LIVE-RETEST OFFEN / 175-GRUPPEN-RECHERCHE WEITER OFFEN

## AUTORITÄT

Diese Datei ist die einzige aktuelle Büro-Standzusammenfassung.

- aktuelle Arbeit: `HOBBYRAUM.md`
- Fehlerdetails: `FEHLERQUELLEN.md`
- Ziel: `ZIELVERTRAG_V2.md`
- Fachvertrag: `AKTENSCHRANK/05_FACH_DOSSIER_ARTIKELTYP_VERTRAG_V1.md`
- 0.8.3 Proof-Belege: `AKTENSCHRANK/06_V083_HARD_LOCAL_RELEASE_RECEIPT.md` und `07_V083_WORDPRESS_LIVE_REPEAT_RECEIPT.md`
- 0.8.4 Prüfbeleg: `AKTENSCHRANK/09_V084_HARD_LOCAL_RELEASE_RECEIPT.md`

## 0.8.4 KANDIDAT

`universal-product-comparison-0.8.4-prototype.zip`

SHA-256:
`00035ec0e166d9830f97140b6fc0f4f7666504d548bac507b1b206a2173ce856`

## AUTORITATIVE PORTALABDECKUNG

Portalquelle:
`affiliate-portal-router/assets/portal-structure-v279.json`

SHA-256:
`b86a160e6b8cf720077830422ca6b574203ce171fdc65d357fe9c6bed039c2e0`

Gebunden:
- 329 Produktseiten;
- 1124 Themenkategorien;
- **175/175 Vergleichs-Produktgruppen**;
- Regendecken = Proofgruppe 1/175.

0.8.4 zeigt alle 175 Gruppen in der Produktvergleichsoberfläche. Keine Gruppe darf still verschwinden.

## SINNHAFTIGKEIT / PAARABDECKUNG

Verbindlicher Weg:
`alle Produkte der Gruppe -> gesamtes A-vs-B-Paaruniversum -> Same Brand / fachlich unpassende Nutzung BLOCK -> nur sinnvolle Paare -> SEO`.

Keine Top-N-/Pair-Cap.

Harter Großtest:
- 50 Produkte;
- 5 Hersteller;
- 1000 Cross-Brand-Paare vollständig erzeugt;
- 500 fachlich vergleichbar;
- 500 falsche Nutzungsklasse sichtbar BLOCKED;
- 0 verlorene Paare;
- Reihenfolge/alte Dubletten ändern Coverage nicht.

## RECHERCHEWAHRHEIT

Wichtig getrennt:
- `PAIRING_READY` = vorhandene Fakten/Profil/Policy reichen zur Paarprüfung;
- `research_completeness_status = UNPROVEN` = Markt-/Produktrecherche ist **nicht** als vollständig bewiesen.

Der aktuelle Product-Knowledge-Recherchekatalog enthält 17 Gruppen mit Produktkandidaten. Davon gehören 14 zum autoritativen 175er Vergleichsscope; 3 liegen außerhalb dieses Vergleichsscopes.

Vorhandene Kandidaten dürfen sinnvoll geprüft werden, während fehlende Produkte/Hersteller weiterhin sichtbar Recherchearbeit bleiben.

Keine Gruppe wird allein wegen vorhandener Kandidaten als vollständig recherchiert bezeichnet.

## ZWEI PORTAL-KEY-KOLLISIONEN

Die Portalquelle enthält zweimal den kurzen Produktgruppen-Key `weidezaungeraete` unter zwei verschiedenen Portal-Slugs.

0.8.4 verschmilzt diese nicht still.
Status: `GROUP_KEY_COLLISION` bis die autoritative Identität geklärt ist.

## HARTER LOKALBELEG 0.8.4

Finale Fresh-ZIP:
- 32/32 ausführbare Positiv-/Negativ-/Regressionstests PASS;
- PHP-Lint 48/48 PASS;
- Source↔finale ZIP 67/67 exakt;
- Report-Hashbindung 66/66 exakt;
- 175/175 Portalparität PASS;
- Product Knowledge 0.5.0 SHA exakt;
- PSTE 0.56.25 SHA exakt;
- 0.8.3 Dossier-/Policy-/Kosten-/Auditregeln unverändert PASS;
- Research-Vollständigkeits-Falschbehauptung wird von Mutationstest ROT;
- Drop einer Portalgruppe / Manipulation einer mittleren Gruppe / Top-N-Paarcap / ignorierte Key-Kollision werden ROT;
- kein Writer-/Draft-/Publishweg;
- kein Auto-Publish.

## OFFENES GESAMTZIEL

0.8.4 schließt die generische Registry-/Coverage-Infrastruktur, **nicht** die reale Produktrecherche aller 175 Gruppen.

Weiter offen:
1. WordPress-Live-Retest 0.8.4;
2. Produktrecherche je Vergleichsgruppe möglichst vollständig ausbauen;
3. gruppenspezifische Profile/Decision-Policies fachlich binden;
4. alle dadurch sinnvollen A-vs-B-Paare vollständig prüfen;
5. Coverage/Recherche-Vollständigkeit erst bei echtem Beleg auf vollständig setzen;
6. erster echter positiver Dossier-V2-Livefall;
7. danach erst spätere SEO/TEXT-/ACM-Anbindung.

Kein Publish.

NEXT ACTION ausschließlich `HOBBYRAUM.md`.
