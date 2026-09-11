# PRODUKTVERGLEICH – CURRENT STATE

STAND: 2026-09-11
STATUS: AKTIV / UPC 0.8.5 LIVE FAIL-CLOSED PASS / RECHERCHEKANDIDATEN NOCH NICHT MATERIALISIERT / UPK 0.5.1 LOCAL HARD PASS / LIVE-MATERIALISIERUNG OFFEN

## AUTORITÄT

Diese Datei ist die einzige aktuelle Büro-Standzusammenfassung.

- aktuelle Arbeit: `HOBBYRAUM.md`
- Fehlerdetails: `FEHLERQUELLEN.md`
- Ziel: `ZIELVERTRAG_V2.md`
- Fachvertrag: `AKTENSCHRANK/05_FACH_DOSSIER_ARTIKELTYP_VERTRAG_V1.md`
- 0.8.4 Live-Beleg: `AKTENSCHRANK/10_V084_WORDPRESS_LIVE_RECEIPT.md`
- 0.8.5 lokaler Prüfbeleg: `AKTENSCHRANK/11_V085_HARD_LOCAL_RELEASE_RECEIPT.md`
- Korrektur-/UPK-0.5.1-Beleg: `AKTENSCHRANK/12_V085_LIVE_INVENTORY_GAP_UPK051_HARD_LOCAL_RECEIPT.md`

## UPC 0.8.5

Kandidat:
`universal-product-comparison-0.8.5-prototype.zip`

SHA-256:
`0174051e6584902142f5be5787642426b30aab6c7ba15ef0b07ccbdb4a5844fd`

0.8.5 bleibt als Vergleichs-/Policy-/Herstellerfamilien-Kandidat lokal hart grün:
- 35/35 Regression PASS;
- PHP-Lint 50/50;
- Source↔ZIP 71/71;
- Report-Hashes 70/70;
- 175/175 Portalabdeckung;
- kein Auto-Publish.

## WORDPRESS-LIVE-BEFUND 0.8.5 – KORREKTUR

Der Live-Vorcheck widerlegte eine lokale Testannahme, nicht den Fail-closed-Schutz.

Live sichtbar:
- Version `0.8.5-prototype`;
- `PAIRING_READY: 1`;
- `PROFILE_MISSING: 166`;
- `POLICY_MISSING: 0`;
- `PRODUCT_INVENTORY_MISSING: 6`;
- `GROUP_KEY_COLLISION: 2`;
- maximale neue Providerkosten `$0.0000`.

Winterdecken:
- Recherchekatalog: 8 Kandidaten / 3 Hersteller / `UNPROVEN`;
- echtes Product-Knowledge-Inventar: 0 Produkte / 0 Hersteller;
- Cross-Family-Paaruniversum: 0;
- Status korrekt `PRODUCT_INVENTORY_MISSING`;
- kein SEO-/Providerlauf.

Damit beweist 0.8.5 live korrekt:
**Recherchekandidaten werden nicht als Produktwissen ausgegeben. Ohne materialisiertes Product-Knowledge-Inventar bleibt die Gruppe fail-closed.**

## KORRIGIERTE BEDEUTUNG DER 130 PAARE

Die lokal belegten 130 Paare sind **potentielle Cross-Family-Paare des freigegebenen Recherchekatalogs nach erfolgreicher Quellenprüfung und Materialisierung**.

Sie sind noch keine 130 live vorhandenen Produktwissen-Paare.

Betroffene katalogseitige Potentiale:
- Winterdecken 20;
- Übergangsdecken 14;
- Stalldecken 28;
- Unterdecken 63;
- Steigbügel 5.

Die tatsächliche Live-Zahl darf erst nach echter Herstellerquellenprüfung und Import aus den real PASSenden Produkten abgeleitet werden.

## ROOT CAUSE PV-TEST-085-003

Der lokale 0.8.5-Fachtest baute freigegebene Recherchekandidaten für seine Policy-/Paarprüfung synthetisch als Laufzeitprodukte auf.

Dadurch bewies er korrekt:
- Profile/Policies können die Kandidaten fachlich verarbeiten;
- Herstellerfamilien-/Paarlogik ist korrekt.

Er bewies aber **nicht**, dass diese Kandidaten bereits in der echten WordPress-Product-Knowledge-Datenbank materialisiert waren.

Diese Grenze war im Release-Status zu optimistisch formuliert.

## KISS-FIX: UNIVERSAL PRODUCT KNOWLEDGE 0.5.1

Finaler Kandidat:
`universal-product-knowledge-0.5.1-prototype.zip`

SHA-256:
`17ba686ebbfeac774de5224a042e8ea5fcc472b91774c47271e6b585d74960a1`

0.5.1 baut **keinen neuen Recherche-/Importweg**.

Es automatisiert nur den bereits vorhandenen kanonischen Weg:
`approved research group -> UPK_Research::run_product_group() -> Live-Herstellerprüfung -> nur PASS-Produkte/Fakten -> vorhandener import_package() -> Product Knowledge`.

Neu ist ausschließlich:
- ein Batch-Button für alle bereits freigegebenen Recherchegruppen;
- sequenziell genau eine Gruppe pro AJAX-Request;
- bestehender Einzelgruppenweg bleibt erhalten;
- fachlich BLOCKED bleibt sichtbar;
- Transport/Security-Fehler stoppt fail-closed;
- keine Behauptung Markt vollständig recherchiert.

Unverändert byte-identisch aus 0.5.0:
- `class-upk-research.php`;
- `class-upk-repository.php`;
- `approved-product-research-seeds.json`.

## HARTER LOKALBELEG UPK 0.5.1

Finale Fresh-ZIP:
- Batch Positiv/Negativ PASS;
- Security/Nonce/Capability PASS;
- sequenzielle Verarbeitung PASS;
- kanonischer `run_product_group()`-Pfad PASS;
- 4 Rückfallmutationen korrekt ROT;
- PHP-Lint 5/5 PASS;
- Source↔ZIP 8/8 exakt;
- Report-Hashes 7/7 exakt;
- kein UPC/PSTE/SEO/Writer/Publish-Eigentum.

Gesamtgegenprüfung:
**UPC 0.8.5 gegen exakt die finale UPK-0.5.1-ZIP: 35/35 PASS.**

## OFFENES GESAMTZIEL

Weiter offen:
1. UPK 0.5.1 auf WordPress installieren und nur Oberfläche/Version prüfen;
2. vorhandene 17 freigegebene Recherchegruppen über den bestehenden kanonischen Weg sequenziell live prüfen/materialisieren;
3. pro Gruppe nur tatsächlich PASSende Produkte/Fakten übernehmen;
4. danach UPC-Vorschau neu lesen und reale Inventar-/Paarzahlen bestimmen;
5. fehlende Hersteller/Modelle weiter systematisch recherchieren;
6. Research-Vollständigkeit bleibt `UNPROVEN`, bis echter gruppenspezifischer Vollständigkeitsbeleg existiert;
7. erst danach SEO-Kostenstufen für neue reale Paare.

Kein Publish.
Kein Produktvergleich-Gesamtworkflow vor erfolgreicher Materialisierung.

NEXT ACTION ausschließlich `HOBBYRAUM.md`.
