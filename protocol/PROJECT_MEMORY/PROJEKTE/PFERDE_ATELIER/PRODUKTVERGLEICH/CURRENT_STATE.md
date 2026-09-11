# PRODUKTVERGLEICH – CURRENT STATE

STAND: 2026-09-11
STATUS: AKTIV / UPC 0.8.5 WORDPRESS-LIVE FAIL-CLOSED PASS / UPC 0.8.6 LOCAL HARD + FRESH-ZIP + READ-ONLY ARCHITEKTURAUDIT PASS, LIVE OFFEN / 175ER FACHDISPOSITION 150 V1-PRODUKTGRUPPEN + 25 V1-NOT-APPLICABLE + 0 UNGEKLÄRT / READINESS-PROFILPHASE AKTIV

## AUTORITÄT

Diese Datei ist die einzige aktuelle Büro-Standzusammenfassung.

- aktuelle Arbeit: `HOBBYRAUM.md`
- Fehlerdetails: `FEHLERQUELLEN.md`
- Ziel: `ZIELVERTRAG_V2.md`
- finale Paar-/Refresh-Autorität: `AKTENSCHRANK/31_ARCHITEKTURENTSCHEIDUNG_PLUGIN_FINAL_AUTHORITY_20260911.md`
- finale 175er V1-Disposition: `AKTENSCHRANK/60_FINAL_COVERAGE_DISPOSITION_175_V1_20260911.md`
- Readiness-Baseline: `AKTENSCHRANK/61_READINESS_BASELINE_V1_150_20260911.md`
- aktuelle source-bound Profilspecs: `AKTENSCHRANK/62_...` bis `69_...`
- UPC-0.8.6 Lifecycle-Hardbeleg: `AKTENSCHRANK/39_V086_LIFECYCLE_REEVALUATION_HARD_LOCAL_RECEIPT.md`
- UPC-0.8.6 Read-only Architektur-Audit: `AKTENSCHRANK/41_V086_READ_ONLY_ARCHITECTURE_AUDIT_RECEIPT.md`

## TECHNISCHER STAND

Letzter WordPress-Live-Stand:
`UPC 0.8.5-prototype`
SHA-256 `0174051e6584902142f5be5787642426b30aab6c7ba15ef0b07ccbdb4a5844fd`

Aktueller lokal hart geprüfter Kandidat:
`UPC 0.8.6-prototype`
SHA-256 `6ad160d18fb0973463c214de4356447923cbb728e222725e5407868e580c24f6`

0.8.6 belegt:
- Lifecycle-Gap geschlossen;
- 38/38 Regression PASS;
- 51/51 PHP-Lint PASS;
- Source↔Fresh-ZIP 74/74 exakt;
- Report-Hashes 73/73 exakt;
- 175/175 Portalparität PASS;
- 1000-Pair-No-Cap PASS;
- Research ohne Product Knowledge -> 0 Paare;
- Nicht-V1-Gruppen fail-closed;
- SEO kann fachliches BLOCKED nicht überschreiben;
- Dossier-Neuaudit bei Produktentfall fail-closed.

**WordPress-Live für 0.8.6 wurde noch nicht ausgeführt.**

UPK 0.5.1 bleibt gebunden:
SHA-256 `17ba686ebbfeac774de5224a042e8ea5fcc472b91774c47271e6b585d74960a1`

## 175ER FACHDISPOSITION

- `PRODUCT_EVIDENCE_PRESENT`: **150**
- `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`: **25**
- `UNRESOLVED_COVERAGE`: **0**
- Summe: 175/175.

Die 25 V1-NOT-APPLICABLE-Keys sind bewusst fail-closed und erzeugen kein Produktpaar.

## READINESS-GAP

Exakter UPC-0.8.6-Gegencheck:
- 175 Registry-Gruppen;
- **7 maschinenfeste** Vergleichsprofile/Decision-Policies;
- damit **143/150 V1-fähige Gruppen maschinenfest noch offen**.

Seit dieser Baseline wurden source-bound, aber noch **nicht materialisiert**, zusätzliche Profilspezifikationen für **21 Gruppen** erstellt:
- `high-neck-decken`;
- `deckengurte`;
- `deckentaschen-und-aufbewahrung`;
- `stallhalfter`;
- `knotenhalfter`;
- `sicherheitshalfter`;
- `fohlenhalfter`;
- `pferdebuersten`;
- `striegel`;
- `kardaetschen`;
- `satteldecken`;
- `schabracken`;
- `sattelgurte`;
- `sattelschraenke`;
- `satteltransport`;
- `englische-trensen`;
- `gebisse`;
- `gebisslose-zaeumungen`;
- `zuegel`;
- `sperrriemen`;
- `reithalfter`.

Akte 67 bindet Sattelschränke/Satteltransport/englische Trensen.
Akte 68 bindet Gebisse/gebisslose Zäumungen/Zügel mit harten Wirk-/Konstruktionsklassen.
Akte 69 bindet Sperrriemen/Reithalfter mit hartem Cross-Brand-Kompatibilitätsgate; fehlende belegte Kompatibilitätsüberschneidung muss korrekt bei 0 Paaren bleiben.

Diese 21 Specs ändern den technischen 0.8.6-Profilbestand noch nicht. Sie sind Vorarbeit für einen später gebündelten Daten-/Release-Schritt.

## AKTUELLER ARBEITSBLOCK

Registry nach `reithalfter` frisch geprüft:
- `offenstallraufen` = `PRODUCT_COMPARISON_V1_NOT_APPLICABLE` -> überspringen;
- nächster V1-fähiger Key `liegeflaechen-im-offenstall`;
- `offenstalltore` = `PRODUCT_COMPARISON_V1_NOT_APPLICABLE` -> überspringen;
- danach `offenstall-bodenbefestigung`;
- danach `fressstaender-im-offenstall`;
- anschließend `trennwaende-im-offenstall`.

Nächster Profilblock:
`liegeflaechen-im-offenstall` -> `offenstall-bodenbefestigung` -> `fressstaender-im-offenstall`.

Arbeitsweise:
source-bound Faktenmatrix -> Nutzungsklasse/Pairing-Regeln -> Decision-Policy -> Produktgegenprüfung -> in sinnvollen Blöcken sammeln -> erst dann technische Materialisierung -> kompletter Positiv-/Negativ-/Mutation-/Fresh-ZIP-Test.

Finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin und muss aus aktuellem Product Knowledge regelmäßig neu bewertet werden.

Kein SEO vor fachlich zulässigem Kandidatenuniversum.
Kein Merge.
Kein Publish.

NEXT ACTION ausschließlich `HOBBYRAUM.md`.
