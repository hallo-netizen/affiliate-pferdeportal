# PRODUKTVERGLEICH – CURRENT STATE

STAND: 2026-09-11
STATUS: AKTIV / UPC 0.8.5 WORDPRESS-LIVE FAIL-CLOSED PASS / UPC 0.8.6 LOCAL HARD + FRESH-ZIP + READ-ONLY ARCHITEKTURAUDIT PASS, LIVE OFFEN / 175ER FACHDISPOSITION 150 V1-PRODUKTGRUPPEN + 25 V1-NOT-APPLICABLE + 0 UNGEKLÄRT / READINESS-PROFILPHASE AKTIV

## AUTORITÄT

Diese Datei ist die einzige aktuelle Büro-Standzusammenfassung.

- aktuelle Arbeit / NEXT ACTION: `HOBBYRAUM.md`
- einzige detaillierte Fehlerquelle: `FEHLERQUELLEN.md`
- Ziel: `ZIELVERTRAG_V2.md`
- Tagesprotokoll bis Akte 65: `PROTOKOLL_20260911.md`
- Nachhol-/Fortsetzungsprotokoll: `PROTOKOLL_NACHHOLUNG_20260911.md`
- finale Paar-/Refresh-Autorität: `AKTENSCHRANK/31_ARCHITEKTURENTSCHEIDUNG_PLUGIN_FINAL_AUTHORITY_20260911.md`
- finale 175er V1-Disposition: `AKTENSCHRANK/60_FINAL_COVERAGE_DISPOSITION_175_V1_20260911.md`
- Readiness-Baseline: `AKTENSCHRANK/61_READINESS_BASELINE_V1_150_20260911.md`
- aktuelle source-bound Profilspecs: `AKTENSCHRANK/62_...` bis `86_...`
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

Seit der Readiness-Baseline wurden source-bound, aber **nicht materialisiert**, zusätzliche Profilspezifikationen für **74 Gruppen** erstellt.

Aktenübersicht:
- Akten 62–86 enthalten die source-bound Profil-/Faktenmatrizen;
- Akte 84: `reitplatzboden`, `reitplatzumrandung`, `reitplatzbeleuchtung`;
- Akte 85: `reitplatzbewaesserung`, `reitplatzspiegel`, `reitplatzplaner`, `reitplatzschleppe`;
- Akte 86: `hufschlagraeumer`, `reitplatzbewaesserung-mobil`, `weidepflegegeraete`;
- keine source-bound Profilspec ändert den technischen 0.8.6-Profilbestand automatisch.

Wichtige Fail-closed-/Dedup-Regeln bleiben bindend, unter anderem:
- fehlende gleiche Nutzungsklasse/Subtyp-/Kompatibilitätsbindung -> kein Paar;
- `reitplatzbewaesserung` p163 = feste Anlage; mobile Systeme ausschließlich p170 `reitplatzbewaesserung-mobil`;
- `hufschlagraeumer`: Handgerät != Batterie-Standalone != Planer-Anbaugerät;
- p170 Cross-Family-Pairing nur bei belastbarer Hersteller-/OEM-Identität;
- `weidepflegegeraete` p171 erste Klasse = reiner 3-m-Grünlandstriegel ohne montiertes Sägerät; Nachsaat p172 und Weideschleppen p173 separat;
- `bahnplaner` p167 und `sandverteiler` p168 bleiben V1-NOT-APPLICABLE;
- keine 25er V1-NOT-APPLICABLE-Gruppe reaktivieren.

## AKTUELLER ARBEITSBLOCK

Die frühere Zuordnung `p163 hindernisstangen / p164 sprungstaender / p165 cavaletti` war falsch und ist als `PV-GOV-20260911-002` korrigiert. `hindernisstangen` liegt tatsächlich erst bei p331.

Autoritative Registry-Folge nach Akte 86:
- `p172 nachsaat-fuer-pferdeweiden`;
- `p173 weideschleppen`;
- `p174 unkrautstecher`.

Nächster fachlich zulässiger Profilblock:
`nachsaat-fuer-pferdeweiden` -> `weideschleppen` -> `unkrautstecher`.

Vor Pairing hart zu normalisieren:
- Nachsaat-Mischung/Saatgutprodukt von Nachsaatmaschine strikt trennen und Registry-Intent source-bound festlegen;
- p173 passive Weideschleppe nicht mit p171 Federzinken-Grünlandstriegel duplizieren;
- Unkrautstecher nur innerhalb identischer Hand-/Hebel-/Standmechanik paaren;
- fehlende Herstellerfamilien-, Bauart-, Saatgut-/Einsatz- oder Anschlussgleichheit -> 0 Paar;
- kein finaler Produktpair manuell festschreiben; finale Paarentscheidung ausschließlich im Produktvergleichs-Plugin aus aktuellem Product Knowledge.

Arbeitsweise:
source-bound Faktenmatrix -> Nutzungsklasse/Pairing-Regeln -> Decision-Policy -> Produktgegenprüfung -> sinnvoll bündeln -> erst danach technische Materialisierung -> kompletter Positiv-/Negativ-/Mutation-/Fresh-ZIP-Test.

Kein SEO vor fachlich zulässigem Kandidatenuniversum.
Kein Writer/Draft/Publish aus diesem Büro.
Kein Codex.
Kein Merge.
Kein Publish.

NEXT ACTION ausschließlich `HOBBYRAUM.md`.
