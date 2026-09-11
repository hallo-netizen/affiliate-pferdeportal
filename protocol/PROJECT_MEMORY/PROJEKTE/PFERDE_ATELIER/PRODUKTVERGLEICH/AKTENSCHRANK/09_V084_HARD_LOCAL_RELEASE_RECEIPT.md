# PRODUKTVERGLEICH 0.8.4 – HARD LOCAL RELEASE RECEIPT

Stand: 2026-09-11
Status: LOCAL + FINAL-FRESH-ZIP HARD PASS / WORDPRESS-LIVE-RETEST OFFEN

Artefakt:
`universal-product-comparison-0.8.4-prototype.zip`

SHA-256:
`00035ec0e166d9830f97140b6fc0f4f7666504d548bac507b1b206a2173ce856`

## Anlass

PV-SCALE-084-001:
0.8.3 bewies den kompletten Produktvergleichsmechanismus nur für die Proofgruppe Regendecken.
Die autoritative Portalstruktur enthält 175 Vergleichs-Produktgruppen.

## KISS-Änderung 0.8.4

Kein 175-faches PHP-Hardcoding.
Kein neuer Writer.
Kein neuer SEO-Providerweg.
Kein neues Handoff.

Nur:
- portalgebundene `group-registry.json`;
- read-only `UPC_Group_Registry`;
- 175er Readiness-/Coverage-Anzeige;
- vollständige Cross-Brand-Paarabdeckung ohne Top-N-Cap;
- sichtbare Coverage-/Research-Lücken;
- bestehender Workflow bleibt für unvorbereitete Gruppen fail-closed.

## Autoritative Portalbindung

Quelle:
`affiliate-portal-router/assets/portal-structure-v279.json`

SHA-256:
`b86a160e6b8cf720077830422ca6b574203ce171fdc65d357fe9c6bed039c2e0`

Auswertung:
- 329 Produktseiten;
- 1124 Themenkategorien;
- 175/175 Vergleichsgruppen.

Abgeleiteter autoritativer Katalog SHA-256:
`4eecef55a3033a4691f8a832eba5fb1657cdb15826ee47d366dccbaabfbb1fa2`

Registry-Parität 175/175 PASS.

## Sinnhaftigkeit / vollständige Paarabdeckung

Regel:
`gesamtes Paaruniversum -> Same Brand / fachlich falsche Nutzung BLOCK -> nur sinnvolle Paare -> SEO`.

Keine willkürliche Pair-/Top-N-Grenze.

Großtest:
- 50 Produkte;
- 5 Hersteller;
- 1000 Cross-Brand-Paare vollständig;
- 500 COMPARABLE;
- 500 falsche Nutzungsklasse BLOCKED;
- Inputreihenfolge unverändert;
- alte Dubletten erhöhen Paaruniversum nicht.

## Research-Wahrheit

Der vorhandene Product-Knowledge-Recherchekatalog enthält 17 Gruppen mit Kandidaten.
14 davon gehören zum 175er Vergleichsscope.

Hard Rule:
`Kandidaten vorhanden != Markt vollständig recherchiert`.

Da der aktuelle UPK-Katalog keinen Vollständigkeitsvertrag besitzt, bleibt:
`research_completeness_status = UNPROVEN` für 175/175.

Vorhandene sinnvolle Paare dürfen schon geprüft werden; fehlende Hersteller/Produkte bleiben sichtbar Recherchearbeit.

## Key-Kollision

Die Portalquelle enthält zwei verschiedene Portal-Slugs mit demselben kurzen Key `weidezaungeraete`.
0.8.4 verschmilzt sie nicht still.
Beide bleiben `GROUP_KEY_COLLISION`, bis die autoritative Identität geklärt ist.

## Harte lokale Prüfung

Arbeitsbaum:
- 32/32 ausführbare Tests PASS;
- PHP-Lint 48/48 PASS.

Prefinal Fresh-ZIP:
- Source↔ZIP 67/67 PASS;
- 32/32 Tests PASS;
- PHP-Lint 48/48 PASS.

Finale Fresh-ZIP:
- Source↔ZIP 67/67 PASS;
- Report-Hashbindung 66/66 PASS;
- 32/32 Tests PASS;
- PHP-Lint 48/48 PASS.

Exakte Abhängigkeiten:
- UPK 0.5.0 SHA `80218ec721631353d62a7e3058e76d9c4a4829802c4d5c6bd6f1f2014b6879e3`;
- PSTE 0.56.25 SHA `8122e3fa2273fe4d8e53476f557ed0ddd99a197e8b1c40302f35db245ebb0f95`.

Real-PSTE-False-Pair-Beleg wurde nicht künstlich ersetzt. Er wird nur weitergeführt, weil die zuständige `class-upc-seo-discovery.php` byte-identisch zur real getesteten 0.8.2-Quelle bleibt.

## 0.8.4 Mutation Guards

Alle korrekt ROT:
- autoritative Gruppe entfernen;
- mittlere Portalgruppe manipulieren;
- Paaruniversum künstlich auf Top-N begrenzen;
- Key-Kollision ignorieren;
- Research-Vollständigkeit ohne Beleg auf COMPLETE setzen.

Bestehende 0.8/0.8.3 Mutation Guards bleiben PASS.

## Gesamtworkflow-Grenzen

Weiter unverändert:
`Portalgruppe -> Produktwissen -> Sinnprüfung/Vergleichbarkeit -> SEO -> Dossier V2 -> unabhängiger Audit`.

Unvorbereitete Gruppen starten keinen Providerlauf.
Persistente SEO-Evidenz bleibt wiederverwendet.
Writer/Draft/Publish dormant.
Kein Auto-Publish.

## Noch offen

0.8.4 löst die Registry-/Coverage-Infrastruktur, **nicht** die reale Produktrecherche aller 175 Gruppen.

Nach WordPress-Live-PASS:
- Produktinventare je Gruppe möglichst vollständig erweitern;
- Profile/Decision-Policies fachlich binden;
- alle sinnvollen A-vs-B-Paare vollständig prüfen;
- erst bei echtem Beleg Research-Vollständigkeit schließen.

Noch kein WordPress-LIVE-PASS für 0.8.4.
