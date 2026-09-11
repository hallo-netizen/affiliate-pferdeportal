# PRODUKTVERGLEICH – CURRENT STATE

STAND: 2026-09-11
STATUS: AKTIV / UPC 0.8.5 LIVE FAIL-CLOSED PASS / UPK 0.5.1 LIVE-BATCH 17/17 ABGESCHLOSSEN / MARKTRECHERCHE A–J GESICHERT / 175-GRUPPEN-COVERAGE KONSOLIDIERT / NÄCHSTER GAP DECKENGURTE

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
- aktuelle Marktrecherchebelege: `AKTENSCHRANK/13_MARKTRECHERCHE_BATCH_A_20260911.md` bis `22_MARKTRECHERCHE_BATCH_J_20260911.md`
- konsolidierte 175er Coverage-/Gap-Map: `AKTENSCHRANK/25_MARKTRECHERCHE_COVERAGE_175_A_J_20260911.md`

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
- Herstellerfamilien-/Paar-/Dossier-/Kosten-Schutzregeln weiter fail-closed;
- kein Writer-/Draft-/Publishweg.

WordPress-Live zeigte zusätzlich korrekt:
- Recherchekandidat ist nicht automatisch Product Knowledge;
- fehlendes Inventar bleibt `PRODUCT_INVENTORY_MISSING`;
- kein SEO-/Providerlauf wird dadurch erfunden;
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
- UPC 0.8.5 gegen exakt finale UPK-0.5.1-ZIP: 35/35 PASS.

## WORDPRESS-LIVE-BATCH 0.5.1

Der reale Batch über die alte freigegebene Recherchebasis ist abgeschlossen:
- 17/17 Recherchegruppen verarbeitet;
- PASS 6;
- TEIL-PASS 8;
- BLOCKED 3;
- `pairing-ready 9` laut Product-Knowledge-Batchsummary.

Wichtig:
Diese 17 Gruppen stammen aus einer kleinen Alt-Recherchebasis von nur 102 Produktkandidaten. Der Batch war eine Quellenprüfung/Materialisierung dieser vorhandenen Basis und **keine Markt-Recherche über alle 175 Vergleichsgruppen**.

Daher gilt weiterhin:
`Research-Vollständigkeit = UNPROVEN`.

Aus dem Batch darf ohne anschließende Produktvergleichs-Vorschau keine neue globale Live-Paarzahl behauptet werden.

## MARKTRECHERCHE A–J / 175ER COVERAGE

Die zehn Research-Evidence-Akten A–J sind gegen die autoritative Portal-Registry mit exakt 175 eindeutigen `product_slug`-Identitäten konsolidiert.

Der source-bound Coverage-Checkpoint ergibt:
- `EVIDENCE_PRESENT`: 70;
- `PARTIAL_AMBIGUOUS`: 57;
- `NO_GROUP_EVIDENCE`: 48;
- Summe: 175/175.

Diese Statuswerte bedeuten **nicht** Markt-Vollständigkeit und **nicht** Pairing-Ready. Hersteller-/Modellkandidaten und offene Fakten-/Nutzungsklassenfragen bleiben in ihren jeweiligen Research-Akten gebunden.

Der frühere Chat-Zwischenwert `129 / 52 / 77 / 46` ist verworfen; autoritativ für diesen Checkpoint ist ausschließlich `AKTENSCHRANK/25_MARKTRECHERCHE_COVERAGE_175_A_J_20260911.md`.

Wichtiger Fail-closed-Befund:
Die sichtbare Bezeichnung `Weidezaungeräte` existiert mit zwei verschiedenen Registry-Identitäten (`weidezaungeraete` und `weide-zauntechnik-weidezaungeraete`). Keine stille Zusammenführung.

## AKTUELLES GESAMTZIEL

Für alle 175 autoritativen Vergleichsgruppen:
`Marktrecherche -> echte Herstellerfamilien -> aktuelle konkrete Modelle -> Herstellerquellen -> gruppenspezifische Faktenmatrix -> Sinn-/Nutzungsebenenprüfung -> alle fachlich zulässigen A-vs-B-Paare -> erst danach SEO`.

Keine Top-N-/Pair-Cap.
Keine automatische Übernahme bloßer Research-Funde.
Keine Markt-Vollständigkeitsbehauptung ohne gruppenspezifischen Beleg.

## AKTUELLER ARBEITSBLOCK

Keine weitere Pluginentwicklung.

Der A–J-vs-175-Abgleich ist abgeschlossen. Der erste echte `NO_GROUP_EVIDENCE`-Gap in Registry-Reihenfolge ist:
`pferdedecken-deckengurte`.

Jetzt ausschließlich dort mit aktueller Hersteller-/Modellrecherche fortsetzen. Danach den nächsten echten Gap aus der Coverage-Map nehmen.

Erst nach einem großen belastbaren Forschungsblock wird das bestehende Product Knowledge einmal gebündelt aktualisiert.

Vor jeder zukünftigen Plugin-Übergabe zwingend:
**exakt auszugebende ZIP lokal positiv + negativ/Mutation + gegen den gesamten aktuellen Produktvergleichsworkflow prüfen.**

## NACHBARWEG

SEO/TEXT/ACM ist getrennt und wird hier nicht verändert.
Aktueller frisch geprüfter ACM-Head aus der letzten Abschlussprüfung:
`ba511c2caec5e970948cf8e5c0139bcfea017ce2`

Dort erster echter Realtest-Blocker:
`CODEX_PRODUCTION_ENVIRONMENT_PROOF_MISSING`.

Keine Produktvergleichs-Anbindung, solange der Nachbarweg nicht separat freigegeben ist.

Kein Merge.
Kein Publish.

NEXT ACTION ausschließlich `HOBBYRAUM.md`.
