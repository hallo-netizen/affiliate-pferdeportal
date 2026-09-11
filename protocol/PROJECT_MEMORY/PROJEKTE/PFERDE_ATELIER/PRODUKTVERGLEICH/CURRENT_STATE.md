# PRODUKTVERGLEICH – CURRENT STATE

STAND: 2026-09-11
STATUS: AKTIV / UPC 0.8.5 LIVE FAIL-CLOSED PASS / UPC 0.8.6 LOCAL HARD + FRESH-ZIP PASS, LIVE OFFEN / UPK 0.5.1 LIVE-BATCH ABGESCHLOSSEN / ERSTER 175ER RESEARCH-DURCHLAUF 97/78/0 / PLUGIN = FINALE PAARINSTANZ / TECHNISCHER GESAMTAUDIT LÄUFT

## AUTORITÄT

Diese Datei ist die einzige aktuelle Büro-Standzusammenfassung.

- aktuelle Arbeit: `HOBBYRAUM.md`
- Fehlerdetails: `FEHLERQUELLEN.md`
- Ziel: `ZIELVERTRAG_V2.md`
- Fachvertrag: `AKTENSCHRANK/05_FACH_DOSSIER_ARTIKELTYP_VERTRAG_V1.md`
- 0.8.4 Live-Beleg: `AKTENSCHRANK/10_V084_WORDPRESS_LIVE_RECEIPT.md`
- 0.8.5 lokaler Prüfbeleg: `AKTENSCHRANK/11_V085_HARD_LOCAL_RELEASE_RECEIPT.md`
- Testgrenzen-/UPK-0.5.1-Beleg: `AKTENSCHRANK/12_V085_LIVE_INVENTORY_GAP_UPK051_HARD_LOCAL_RECEIPT.md`
- 0.5.1 WordPress-Live-Batch: `AKTENSCHRANK/23_UPK051_WORDPRESS_LIVE_BATCH_RECEIPT_20260911.md`
- A–J-Checkpoint: `AKTENSCHRANK/25_MARKTRECHERCHE_COVERAGE_175_A_J_20260911.md`
- Research K–T: `AKTENSCHRANK/26_...` bis `37_...` mit Architekturbeleg `31_...`
- finale Plugin-Autorität/Refresh-Regel: `AKTENSCHRANK/31_ARCHITEKTURENTSCHEIDUNG_PLUGIN_FINAL_AUTHORITY_20260911.md`
- aktueller 175er Research-Coverage-Beleg: `AKTENSCHRANK/38_MARKTRECHERCHE_COVERAGE_DELTA_K_T_20260911.md`
- 0.8.6 Lifecycle-Fix-Hardbeleg: `AKTENSCHRANK/39_V086_LIFECYCLE_REEVALUATION_HARD_LOCAL_RECEIPT.md`

## INSTALLIERTER / GEPRÜFTER TECHNISCHER STAND

### Universal Product Comparison – letzter WordPress-Live-Stand
`0.8.5-prototype`

SHA-256:
`0174051e6584902142f5be5787642426b30aab6c7ba15ef0b07ccbdb4a5844fd`

WordPress-Live zeigte korrekt fail-closed:
- Recherchekandidat ist nicht automatisch Product Knowledge;
- fehlendes Inventar bleibt `PRODUCT_INVENTORY_MISSING`;
- kein SEO-/Providerlauf wird erfunden;
- Kostenanzeige blieb $0.0000.

### Universal Product Comparison – aktueller lokal hart geprüfter Kandidat
`0.8.6-prototype`

Exakt geprüfte Fresh-ZIP:
`universal-product-comparison-0.8.6-prototype.zip`

SHA-256:
`6ad160d18fb0973463c214de4356447923cbb728e222725e5407868e580c24f6`

Geschlossener erster Auditfehler:
`PV-LIFECYCLE-086-001`.

Root Cause:
0.8.5 las aktuelles Product Knowledge neu, ließ aber `DISCONTINUED`/`UNKNOWN`/fehlenden Lifecycle in Paaruniversum und Readiness einfließen.

0.8.6 KISS-Regel:
- `ACTIVE`: paarbar;
- `TEMPORARILY_UNAVAILABLE`: paarbar;
- `DISCONTINUED`: fail-closed ausgeschlossen;
- `UNKNOWN`/fehlend: fail-closed ausgeschlossen;
- kanonische Deduplizierung erfolgt vor Lifecycle-Prüfung, damit kein alter `ACTIVE`-Datensatz wieder auflebt.

Harter Beleg:
- unveränderte exakte 0.8.5 gegen Sollregression: ROT, 3 statt 1 Paar;
- Working Tree Regression **38/38 PASS**;
- zwei neue Lifecycle-Mutationen korrekt ROT;
- PHP-Lint **51/51 PASS**;
- Fresh-ZIP Source↔ZIP **74/74 exakt**;
- Report-Hashes **73/73 exakt**;
- Fresh-ZIP Regression **38/38 PASS**;
- Fresh-ZIP PHP-Lint **51/51 PASS**;
- 175/175 Portalparität PASS;
- 1000-Pair-No-Cap-Regel PASS;
- SEO/Product-Knowledge/Dossier-Gesamtkorridor PASS.

**WordPress-Live für 0.8.6 wurde noch nicht ausgeführt.**

### Universal Product Knowledge
`0.5.1-prototype`

SHA-256:
`17ba686ebbfeac774de5224a042e8ea5fcc472b91774c47271e6b585d74960a1`

Lokal belegt:
- Positiv/Negativ PASS;
- Nonce/Capability PASS;
- sequenzielle Batchverarbeitung PASS;
- kanonischer `UPK_Research::run_product_group()`-Weg PASS;
- 4 Rückfallmutationen korrekt ROT;
- PHP-Lint 5/5;
- Source↔ZIP 8/8;
- Report-Hashes 7/7.

## WORDPRESS-LIVE-BATCH 0.5.1

Realer Batch über alte freigegebene Recherchebasis:
- 17/17 Gruppen verarbeitet;
- PASS 6;
- TEIL-PASS 8;
- BLOCKED 3;
- `pairing-ready 9` laut Batchsummary.

Grenze:
Die Altbasis umfasste nur 17 Gruppen / 102 Kandidaten. Sie ist keine 175-Gruppen-Marktrecherche und kein Markt-Vollständigkeitsbeleg.

## ERSTER RESEARCH-DURCHLAUF 175/175

Autoritativer aktueller Beleg:
`AKTENSCHRANK/38_MARKTRECHERCHE_COVERAGE_DELTA_K_T_20260911.md`

Aktuell:
- `EVIDENCE_PRESENT`: **97**;
- `PARTIAL_AMBIGUOUS`: **78**;
- `NO_GROUP_EVIDENCE`: **0**;
- Summe: **175/175**.

`0 NO_GROUP_EVIDENCE` bedeutet nur:
Jede Registry-Identität wurde betrachtet und besitzt konkrete Research-Evidence oder einen sichtbaren source-bound Fach-/Produktklassen-/Artikeltyp-/Quellenblock.

Es bedeutet ausdrücklich nicht:
- Markt-Vollständigkeit;
- Product Knowledge vollständig;
- 175 READY/Pairing-Ready;
- 175 PRODUCT_COMPARISON-V1-fähige Gruppen;
- SEO-PASS;
- fertige Dossiers.

Die 78 `PARTIAL_AMBIGUOUS` enthalten unterschiedliche Ursachen und müssen künftig in echte Ursachenklassen zerlegt werden, statt pauschal erneut recherchiert zu werden.

## FINALE PAAR-/AKTUALISIERUNGSAUTORITÄT

Verbindlich:
Die letzte Entscheidung, welche konkreten Produkte als A-vs-B-Vergleich zulässig sind und ein Dossier erhalten dürfen, liegt beim PRODUKTVERGLEICH-System/Plugin.

Research/Product Knowledge liefert Produktbestand/Fakten.
SEO liefert Nachfrage-/A-vs-B-/Keyword-/Kannibalisierungssignale.
SEO darf keine fachlich unzulässige Paarung erzwingen.

Das PRODUKTVERGLEICH-System muss aus jeweils aktuellem Product Knowledge wiederholbar neu bewerten. `PV-LIFECYCLE-086-001` ist für Abkündigung/unklaren Lifecycle im lokalen Kandidaten geschlossen; die übrigen Auditregeln werden weiter einzeln hart geprüft.

Dauerbeleg:
`AKTENSCHRANK/31_ARCHITEKTURENTSCHEIDUNG_PLUGIN_FINAL_AUTHORITY_20260911.md`.

## AKTUELLER ARBEITSBLOCK

Der erste breite Marktrecherche-Durchlauf ist abgeschlossen.
Der erste technische Auditfehler ist belegt und als 0.8.6 lokal hart geschlossen.

Jetzt **keinen zweiten spekulativen Fix**.

Der bestehende Gesamtaudit wird ab dem nächsten noch nicht hart belegten Punkt fortgesetzt:
1. bloße Research-Evidence kann kein Paar erzeugen;
2. Service/Knowledge/Checklisten-/nicht V1-fähige Registry-Gruppen bleiben fail-closed;
3. SEO kann fachliche Paarfreigabe nicht überschreiben;
4. keine Top-N-/Pair-Cap – bestehender 1000-Pair-Test bleibt Regression;
5. bestehende Dossiers werden bei aktuellem Inventar-/Profil-/Policy-Drift tatsächlich fail-closed neu auditiert.

Nur eine konkret belegte nächste technische Lücke darf einen weiteren KISS-Fix auslösen.

Parallel fachlich danach:
78 Partial-Gruppen nach Ursache klassifizieren und nur `MORE_MARKET_RESEARCH_REQUIRED`-Fälle erneut recherchieren.

Vor jeder Plugin-Übergabe zwingend:
**exakt auszugebende ZIP lokal positiv + negativ/Mutation + gegen den gesamten aktuellen Produktvergleichsworkflow + Fresh-ZIP prüfen.**

## NACHBARWEG

SEO/TEXT/ACM ist getrennt und wird hier nicht verändert.
Keine Produktvergleichs-Anbindung ohne separate Nachbarfreigabe.

Kein Merge.
Kein Publish.

NEXT ACTION ausschließlich `HOBBYRAUM.md`.
