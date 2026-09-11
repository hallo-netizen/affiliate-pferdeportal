# PRODUKTVERGLEICH – CURRENT STATE

STAND: 2026-09-11
STATUS: AKTIV / UPC 0.8.5 LIVE FAIL-CLOSED PASS / UPK 0.5.1 LIVE-BATCH ABGESCHLOSSEN / ERSTER 175ER RESEARCH-DURCHLAUF 97/78/0 / PLUGIN = FINALE PAARINSTANZ / TECHNISCHE GESAMTPRÜFUNG JETZT ZULÄSSIG

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

## INSTALLIERTER / GEPRÜFTER TECHNISCHER STAND

### Universal Product Comparison
`0.8.5-prototype`

SHA-256 der exakt lokal geprüften ZIP:
`0174051e6584902142f5be5787642426b30aab6c7ba15ef0b07ccbdb4a5844fd`

Belegt:
- 35/35 Regression PASS;
- PHP-Lint 50/50 PASS;
- Source↔ZIP 71/71 exakt;
- Report-Hashes 70/70 exakt;
- 175/175 Portalabdeckung;
- Herstellerfamilien-/Paar-/Dossier-/Kosten-Schutzregeln fail-closed;
- kein Writer-/Draft-/Publishweg.

WordPress-Live zeigte korrekt:
- Recherchekandidat ist nicht automatisch Product Knowledge;
- fehlendes Inventar bleibt `PRODUCT_INVENTORY_MISSING`;
- kein SEO-/Providerlauf wird erfunden;
- Kostenanzeige blieb $0.0000.

### Universal Product Knowledge
`0.5.1-prototype`

SHA-256 der exakt lokal geprüften ZIP:
`17ba686ebbfeac774de5224a042e8ea5fcc472b91774c47271e6b585d74960a1`

Lokal belegt:
- Positiv/Negativ PASS;
- Nonce/Capability PASS;
- sequenzielle Batchverarbeitung PASS;
- kanonischer `UPK_Research::run_product_group()`-Weg PASS;
- 4 Rückfallmutationen korrekt ROT;
- PHP-Lint 5/5;
- Source↔ZIP 8/8;
- Report-Hashes 7/7;
- UPC 0.8.5 gegen finale UPK-0.5.1-ZIP: 35/35 PASS.

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
Jede Registry-Identität wurde betrachtet und besitzt jetzt konkrete Research-Evidence oder einen sichtbaren source-bound Fach-/Produktklassen-/Artikeltyp-/Quellenblock.

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

Das PRODUKTVERGLEICH-System muss aus jeweils aktuellem Product Knowledge wiederholbar neu bewerten, insbesondere bei:
- neuen Modellen;
- Nachfolgern/Abkündigungen;
- geänderten Hersteller-/Familienzuordnungen;
- geänderten Herstellerfakten;
- neuen konkreten SEO-Vergleichsanfragen;
- geänderten Profilen/Decision-Policies.

Paare können dadurch neu entstehen, entfallen oder BLOCKED werden.

Dauerbeleg:
`AKTENSCHRANK/31_ARCHITEKTURENTSCHEIDUNG_PLUGIN_FINAL_AUTHORITY_20260911.md`.

## AKTUELLER ARBEITSBLOCK

Der erste breite Marktrecherche-Durchlauf ist abgeschlossen.

Jetzt **kein blindes Weiterrecherchieren**.

Erster zulässiger nächster Schritt:
Bestehende UPC-0.8.5-/UPK-0.5.1-Logik read-only hart gegen den nun vollständigen Fachstand prüfen:
1. Plugin ist tatsächlich letzte Paarinstanz;
2. Paaruniversum wird aus aktuellem gebundenem Product Knowledge berechnet;
3. neue/entfallene/ungültige Produkte führen bei Neubewertung korrekt zu neuen/entfallenen/BLOCKED Paaren;
4. bloße Research-Evidence kann kein Paar erzeugen;
5. Service/Knowledge/Checklisten-/nicht V1-fähige Registry-Gruppen bleiben fail-closed;
6. keine Top-N-/Pair-Cap;
7. SEO kann fachliche Paarfreigabe nicht überschreiben.

Nur eine konkret belegte technische Lücke darf anschließend einen KISS-Fix auslösen.

Parallel fachlich danach:
78 Partial-Gruppen nach Ursache klassifizieren und nur `MORE_MARKET_RESEARCH_REQUIRED`-Fälle erneut recherchieren.

Vor jeder zukünftigen Plugin-Übergabe zwingend:
**exakt auszugebende ZIP lokal positiv + negativ/Mutation + gegen den gesamten aktuellen Produktvergleichsworkflow prüfen.**

## NACHBARWEG

SEO/TEXT/ACM ist getrennt und wird hier nicht verändert.
Keine Produktvergleichs-Anbindung ohne separate Nachbarfreigabe.

Kein Merge.
Kein Publish.

NEXT ACTION ausschließlich `HOBBYRAUM.md`.
