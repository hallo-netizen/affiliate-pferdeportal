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
- aktuelle source-bound Profilspecs: `AKTENSCHRANK/62_...` bis `82_...`
- UPC-0.8.6 Lifecycle-Hardbeleg: `AKTENSCHRANK/39_V086_LIFECYCLE_REEVALUATION_HARD_LOCAL_RECEIPT.md`
- UPC-0.8.6 Read-only Architektur-Audit: `AKTENSCHRANK/41_V086_READ_ONLY_ARCHITECTURE_AUDIT_RECEIPT.md`

## TECHNISCHER STAND

Letzter WordPress-Live-Stand:
`UPC 0.8.5-prototype`
SHA-256 `0174051e6584902142f5be5787642426b30aab6c7ba15ef0b07ccbdb4a5844fd`

Aktueller lokal hart geprüfter Kandidat:
`UPC 0.8.6-prototype`
SHA-256 `6ad160d18fb0973463c214de4356447923cbb728e222725e5407868e580c24f6`

0.8.6 belegt unverändert:
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

Die 25 V1-NOT-APPLICABLE-Keys bleiben fail-closed und erzeugen kein Produktpaar.

## READINESS-GAP

Exakter technischer UPC-0.8.6-Stand:
- 175 Registry-Gruppen;
- **7 maschinenfeste** Vergleichsprofile/Decision-Policies;
- **143/150 V1-fähige Gruppen technisch noch offen**.

Seit der Readiness-Baseline wurden source-bound, aber **nicht materialisiert**, zusätzliche Profilspezifikationen für **61 Gruppen** erstellt.

Aktenübersicht:
- 62–78: bisherige source-bound Profilblöcke bis Unterstand-Beleuchtung / Boxentüren / Boxenriegel / Boxengitter;
- 79: Boxenmatten / Krippen / Lecksteinhalter;
- 80: Putzplatzmatten / Anbindebalken / Anbinderinge;
- 81: Putzboxhalter / Schlauchhalter / Waschplatz;
- 82: Mistboy / Bollengabeln / Stallbesen.

Wichtige aktuelle Fail-closed-/Dedup-Bindungen:
- `boxenriegel`: nur eine sauber separate Einzelproduktfamilie -> 0 Cross-Brand-Paare;
- `boxengitter`: unterschiedliche Unterklassen -> 0 Paar bis zweite Herstellerfamilie je Subtyp;
- `boxenmatten`: Cross-Group-Dedup gegen `liegeflaechen-im-offenstall`;
- `putzboxhalter`: nur eine eigenständige Boxkantenhalter-Familie -> 0 Cross-Brand-Paare;
- `stallbesen`: Cross-Group-Dedup gegen `hofbesen`, da aktuelle Produkte selbst als Stall- und Hofbesen geführt werden;
- keine source-bound Profilspec ändert den technischen 0.8.6-Profilbestand.

## AKTUELLER ARBEITSBLOCK

Autoritative Portalstruktur frisch weitergelesen:
- `p155 schubkarren`;
- `p156 mistcontainer`;
- `p157 mistlagerung` -> `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`, überspringen;
- `p158 paddockzaeune`;
- `p159 reitplatzboden`;
- `p160 reitplatzdrainage` -> `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`, überspringen.

Nächster Profilblock:
`paddockzaeune` -> `reitplatzboden`, danach nächsten zulässigen Registry-Key hinter `reitplatzdrainage` direkt aus der autoritativen Portalstruktur lesen.

Vor Pairing hart zu normalisieren:
- Paddockzäune: konkrete Zaun-/Panel-/Material-/Elektrifizierungs-Unterklasse; keine Obergruppe blind gegen Holz-, Kunststoff-, Elektro- oder mobile Panels mischen;
- Reitplatzboden: konkrete serien-/systemgebundene Boden-/Tretschichtklasse; keine Bauleistung, Drainage oder unterschiedliche Schichtsysteme blind paaren;
- `reitplatzdrainage` bleibt V1 fail-closed NOT_APPLICABLE.

Arbeitsweise:
source-bound Faktenmatrix -> Nutzungsklasse/Pairing-Regeln -> Decision-Policy -> Produktgegenprüfung -> sinnvoll bündeln -> erst danach technische Materialisierung -> kompletter Positiv-/Negativ-/Mutation-/Fresh-ZIP-Test.

Finale konkrete Paarentscheidung ausschließlich im Produktvergleichs-Plugin aus aktuellem Product Knowledge; regelmäßige Neubewertung bleibt Pflicht.

Kein SEO vor fachlich zulässigem Kandidatenuniversum.
Kein Merge.
Kein Publish.

NEXT ACTION ausschließlich `HOBBYRAUM.md`.
