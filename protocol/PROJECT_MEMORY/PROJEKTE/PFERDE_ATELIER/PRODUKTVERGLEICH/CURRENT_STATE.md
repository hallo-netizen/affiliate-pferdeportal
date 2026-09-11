# PRODUKTVERGLEICH – CURRENT STATE

STAND: 2026-09-11
STATUS: AKTIV / UPC 0.8.5 WORDPRESS-LIVE FAIL-CLOSED PASS / UPC 0.8.6 LOCAL HARD + FRESH-ZIP + READ-ONLY ARCHITEKTURAUDIT PASS, LIVE OFFEN / 175ER FACHDISPOSITION 150 V1-PRODUKTGRUPPEN + 25 V1-NOT-APPLICABLE + 0 UNGEKLÄRT / READINESS-PROFILPHASE AKTIV

## AUTORITÄT

Diese Datei ist die einzige aktuelle Büro-Standzusammenfassung.

- aktuelle Arbeit / NEXT ACTION: `HOBBYRAUM.md`
- einzige detaillierte Fehlerquelle: `FEHLERQUELLEN.md`
- Ziel: `ZIELVERTRAG_V2.md`
- Tagesprotokoll bis Akte 65: `PROTOKOLL_20260911.md`
- Nachhol-/Fortsetzungsprotokoll Akten 66–85: `PROTOKOLL_NACHHOLUNG_20260911.md`
- finale Paar-/Refresh-Autorität: `AKTENSCHRANK/31_ARCHITEKTURENTSCHEIDUNG_PLUGIN_FINAL_AUTHORITY_20260911.md`
- finale 175er V1-Disposition: `AKTENSCHRANK/60_FINAL_COVERAGE_DISPOSITION_175_V1_20260911.md`
- Readiness-Baseline: `AKTENSCHRANK/61_READINESS_BASELINE_V1_150_20260911.md`
- aktuelle source-bound Profilspecs: `AKTENSCHRANK/62_...` bis `85_...`
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

**Diese technischen PASS-Belege wurden in dieser Fortsetzung nicht neu ausgeführt.**
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

Seit der Readiness-Baseline wurden source-bound, aber **nicht materialisiert**, zusätzliche Profilspezifikationen für **71 Gruppen** erstellt.

Aktenübersicht:
- Akten 62–85 enthalten die source-bound Profil-/Faktenmatrizen;
- Akte 83: `schubkarren`, `mistcontainer`, `paddockzaeune`;
- Akte 84: `reitplatzboden`, `reitplatzumrandung`, `reitplatzbeleuchtung`;
- Akte 85: `reitplatzbewaesserung`, `reitplatzspiegel`, `reitplatzplaner`, `reitplatzschleppe`;
- keine source-bound Profilspec ändert den technischen 0.8.6-Profilbestand automatisch.

Wichtige Fail-closed-/Dedup-Regeln bleiben bindend, unter anderem:
- fehlende gleiche Nutzungsklasse/Subtyp-/Kompatibilitätsbindung -> kein Paar;
- `reitplatzbewaesserung` p163 = feste Anlage; mobile Systeme ausschließlich p170 `reitplatzbewaesserung-mobil`;
- `reitplatzplaner` != `reitplatzschleppe`; Marketingbezeichnungen entscheiden die Klasse nicht;
- `bahnplaner` p167 und `sandverteiler` p168 bleiben V1-NOT-APPLICABLE;
- `boxenmatten` gegen `liegeflaechen-im-offenstall` deduplizieren;
- `stallbesen` gegen `hofbesen` deduplizieren;
- keine 25er V1-NOT-APPLICABLE-Gruppe reaktivieren.

## AKTUELLER ARBEITSBLOCK

Die frühere Zuordnung `p163 hindernisstangen / p164 sprungstaender / p165 cavaletti` war falsch und ist als `PV-GOV-20260911-002` korrigiert. `hindernisstangen` liegt tatsächlich erst bei p331.

Autoritative Registry-Folge nach Akte 85:
- `p167 bahnplaner` -> V1-NOT-APPLICABLE, überspringen;
- `p168 sandverteiler` -> V1-NOT-APPLICABLE, überspringen;
- `p169 hufschlagraeumer`;
- `p170 reitplatzbewaesserung-mobil`;
- `p171 weidepflegegeraete`.

Nächster fachlich zulässiger Profilblock:
`hufschlagraeumer` -> `reitplatzbewaesserung-mobil` -> `weidepflegegeraete`.

Vor Pairing hart zu normalisieren:
- nur gleiche reale Produkt-/Nutzungsklasse und denselben mechanischen Subtyp paaren;
- p170 strikt von der festen p163-Beregnung trennen;
- `weidepflegegeraete` als Oberbegriff nur über einen klar definierten ersten Produkt-Subtyp öffnen;
- fehlende Herstellerfamilien-, OEM-, Anschluss-/Zugfahrzeug- oder Bauartgleichheit -> 0 Paar;
- kein finaler Produktpair manuell festschreiben; finale Paarentscheidung ausschließlich im Produktvergleichs-Plugin aus aktuellem Product Knowledge.

Arbeitsweise:
source-bound Faktenmatrix -> Nutzungsklasse/Pairing-Regeln -> Decision-Policy -> Produktgegenprüfung -> sinnvoll bündeln -> erst danach technische Materialisierung -> kompletter Positiv-/Negativ-/Mutation-/Fresh-ZIP-Test.

Kein SEO vor fachlich zulässigem Kandidatenuniversum.
Kein Writer/Draft/Publish aus diesem Büro.
Kein Codex.
Kein Merge.
Kein Publish.

NEXT ACTION ausschließlich `HOBBYRAUM.md`.
