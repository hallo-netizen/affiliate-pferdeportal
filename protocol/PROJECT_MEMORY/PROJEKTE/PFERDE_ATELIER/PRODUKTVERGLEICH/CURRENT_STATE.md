# PRODUKTVERGLEICH – CURRENT STATE

STAND: 2026-09-11
STATUS: AKTIV / UPC 0.8.5 LIVE FAIL-CLOSED PASS / UPK 0.5.1 LIVE-BATCH 17/17 ABGESCHLOSSEN / 175-GRUPPEN-COVERAGE SOURCE-BOUND 78/60/37 / PLUGIN = FINALE PAARINSTANZ / NÄCHSTER GAP MISTLAGERUNG

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
- Research K–O: `AKTENSCHRANK/26_...` bis `30_...`
- finale Plugin-Autorität/Refresh-Regel: `AKTENSCHRANK/31_ARCHITEKTURENTSCHEIDUNG_PLUGIN_FINAL_AUTHORITY_20260911.md`
- Research Batch P: `AKTENSCHRANK/32_MARKTRECHERCHE_BATCH_P_20260911.md`
- aktuelle Coverage-Fortschreibung: `AKTENSCHRANK/33_MARKTRECHERCHE_COVERAGE_DELTA_K_P_20260911.md`

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

Realer Batch über die alte freigegebene Recherchebasis:
- 17/17 Gruppen verarbeitet;
- PASS 6;
- TEIL-PASS 8;
- BLOCKED 3;
- `pairing-ready 9` laut Product-Knowledge-Batchsummary.

Grenze:
Die Altbasis umfasste nur 17 Gruppen / 102 Kandidaten. Sie ist keine 175-Gruppen-Marktrecherche und kein Markt-Vollständigkeitsbeleg.

`Research-Vollständigkeit = UNPROVEN`.

## RESEARCH-COVERAGE 175

Autoritativer A–J-Checkpoint:
- `EVIDENCE_PRESENT`: 70;
- `PARTIAL_AMBIGUOUS`: 57;
- `NO_GROUP_EVIDENCE`: 48;
- Summe 175/175.

Danach source-bound Research K–P:
- K Deckengurte -> Evidence;
- L Deckentaschen/Aufbewahrung -> Evidence;
- M Sicherheitshalfter -> Evidence;
- N Satteltransport -> Evidence;
- O Sperrriemen -> Evidence;
- P Frostwächter -> Partial;
- P Lüfter im Stall -> Partial;
- P Wasserleitungen im Stall -> Partial;
- P Mistboy -> Evidence;
- P Schubkarren -> Evidence;
- P Mistcontainer -> Evidence.

Aktueller Research-Coverage-Stand gemäß Akte 33:
- `EVIDENCE_PRESENT`: **78**;
- `PARTIAL_AMBIGUOUS`: **60**;
- `NO_GROUP_EVIDENCE`: **37**;
- Summe: **175/175**.

Diese Werte bedeuten **nicht** Markt-Vollständigkeit, Pairing-Ready, Product Knowledge oder SEO-PASS.

Die sichtbare Bezeichnung `Weidezaungeräte` existiert weiterhin mit zwei getrennten Registry-Identitäten:
- `weidezaungeraete`;
- `weide-zauntechnik-weidezaungeraete`.

Keine stille Zusammenführung.

## FINALE PAAR-/AKTUALISIERUNGSAUTORITÄT

Verbindlich:
Die letzte Entscheidung, welche konkreten Produkte tatsächlich als A-vs-B-Vergleich zulässig sind und ein Dossier erhalten dürfen, liegt beim PRODUKTVERGLEICH-System/Plugin.

Research/Product Knowledge liefert aktuellen Produktbestand und Fakten.
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

## AKTUELLES GESAMTZIEL

Für alle 175 autoritativen Vergleichsgruppen:
`Marktrecherche -> echte Herstellerfamilien -> aktuelle konkrete Modelle -> Herstellerquellen -> gruppenspezifische Faktenmatrix -> Sinn-/Nutzungsebenenprüfung -> Plugin bestimmt fachlich zulässige A-vs-B-Kandidaten -> SEO-Evidenz -> Plugin trifft finale Paar-/Dossierentscheidung -> später Textproduktion`.

Keine Top-N-/Pair-Cap.
Keine automatische Übernahme bloßer Research-Funde.
Keine Markt-Vollständigkeitsbehauptung ohne gruppenspezifischen Beleg.

## AKTUELLER ARBEITSBLOCK

Keine weitere Pluginentwicklung.

Die laufende Arbeit ist reine Markt-/Produktrecherche der verbleibenden `NO_GROUP_EVIDENCE`-Keys.

Erster verbleibender echter Gap in Registry-Reihenfolge:
`mistlagerung`.

Danach nur den jeweils nächsten echten Gap aus der source-bound Coverage-Fortschreibung nehmen.

Erst nach einem großen belastbaren Forschungsblock wird das bestehende Product Knowledge gebündelt aktualisiert und anschließend geprüft, ob die bestehende Pluginlogik die finale Paarentscheidung + regelmäßige Neubewertung bereits vollständig erfüllt oder ein KISS-Fix erforderlich ist.

Vor jeder zukünftigen Plugin-Übergabe zwingend:
**exakt auszugebende ZIP lokal positiv + negativ/Mutation + gegen den gesamten aktuellen Produktvergleichsworkflow prüfen.**

## NACHBARWEG

SEO/TEXT/ACM ist getrennt und wird hier nicht verändert.
Letzter separat geprüfter ACM-Head aus der Abschlussprüfung:
`ba511c2caec5e970948cf8e5c0139bcfea017ce2`

Dort erster echter Realtest-Blocker:
`CODEX_PRODUCTION_ENVIRONMENT_PROOF_MISSING`.

Keine Produktvergleichs-Anbindung, solange der Nachbarweg nicht separat freigegeben ist.

Kein Merge.
Kein Publish.

NEXT ACTION ausschließlich `HOBBYRAUM.md`.
