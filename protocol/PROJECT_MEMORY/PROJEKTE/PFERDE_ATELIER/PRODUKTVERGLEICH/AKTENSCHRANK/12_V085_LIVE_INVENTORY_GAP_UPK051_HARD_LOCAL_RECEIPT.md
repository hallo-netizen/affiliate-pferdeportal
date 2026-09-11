# PRODUKTVERGLEICH – 0.8.5 LIVE INVENTORY GAP / UPK 0.5.1 HARD LOCAL RECEIPT

Stand: 2026-09-11
Status: ROOT CAUSE BELEGT / UPK 0.5.1 LOCAL HARD PASS / WORDPRESS-LIVE OFFEN

## Live-Auslöser

Nach Installation von UPC 0.8.5 zeigte WordPress:
- `PAIRING_READY: 1`;
- `PROFILE_MISSING: 166`;
- `PRODUCT_INVENTORY_MISSING: 6`;
- 2 Key-Kollisionen;
- Winterdecken Research 8 Kandidaten / 3 Hersteller / `UNPROVEN`;
- Winterdecken Product-Knowledge-Inventar 0 Produkte / 0 Hersteller;
- 0 Cross-Family-Paare;
- $0.0000 Providerkosten.

Das Live-System blockierte korrekt und erfand keine Produkte/Paarungen.

## Root Cause

Der lokale UPC-0.8.5-Test erzeugte aus den vorhandenen freigegebenen Recherchekandidaten synthetische Laufzeitprodukte, um Profile, Policies, Herstellerfamilien und Paarlogik zu testen.

Dieser Test belegte nicht die bereits erfolgte Persistierung derselben Kandidaten im echten WordPress-Product-Knowledge-Inventar.

Die erwartete Live-Aussage `PAIRING_READY: 6` war deshalb unzulässig.

## Vorhandener kanonischer Product-Knowledge-Weg

UPK 0.5.0 besaß bereits:
`UPK_Research::run_product_group($group)`

Dieser Weg:
1. liest freigegebene Recherchekandidaten;
2. prüft Herstellerquellen live;
3. übernimmt nur PASS-Produkte/Fakten;
4. verwendet den vorhandenen Importweg in Product Knowledge.

Kein neuer Importer erforderlich.

## KISS-Fix UPK 0.5.1

Artefakt:
`universal-product-knowledge-0.5.1-prototype.zip`

SHA-256:
`17ba686ebbfeac774de5224a042e8ea5fcc472b91774c47271e6b585d74960a1`

Änderung ausschließlich Admin-Orchestrierung:
- Batchbutton für alle bereits freigegebenen Recherchegruppen;
- eine Gruppe pro AJAX-Request;
- sequenziell;
- jeder Schritt ruft unverändert `UPK_Research::run_product_group()`;
- Einzelgruppenweg bleibt erhalten;
- fachlich BLOCKED bleibt sichtbar;
- Transport/Security-Fehler stoppt;
- keine Markt-Vollständigkeitsbehauptung.

Unverändert aus 0.5.0:
- Research-/Livecheck-Logik;
- Repository-/Persistenzlogik;
- freigegebener Recherchekatalog.

## Harter lokaler Beleg

UPK 0.5.1 finale Fresh-ZIP:
- Positiv-/Negativtest PASS;
- Nonce/Capability PASS;
- Sequenz PASS;
- kanonischer Gruppenlauf PASS;
- 4 Mutation Guards korrekt ROT;
- PHP-Lint 5/5 PASS;
- Source↔ZIP 8/8 exakt;
- Report-Hashbindung 7/7 exakt;
- keine SEO-/UPC-/Writer-/Publish-Autorität.

Gesamtworkflow:
- UPC 0.8.5 komplette Regression gegen exakt finale UPK-0.5.1-ZIP: **35/35 PASS**.

## Live-Grenze

Noch nicht bewiesen:
- welche Research-Kandidaten heute ihre Herstellerquellenprüfung bestehen;
- wie viele Produkte tatsächlich importiert werden;
- welche Gruppen danach mindestens zwei echte Herstellerfamilien besitzen;
- reale daraus entstehende Paarzahlen.

Daher keine festen Live-Paarzahlen vor Batchende behaupten.
Research-Vollständigkeit bleibt `UNPROVEN`.

## Next Action

UPK 0.5.1 installieren -> Produktwissen öffnen -> Oberfläche/Version/Button read-only bestätigen -> erst danach genau einen sequenziellen Batchlauf.

UPC 0.8.5 bleibt installiert und unverändert.
Kein Produktvergleich-Gesamtworkflow vorher.
Kein Publish.
