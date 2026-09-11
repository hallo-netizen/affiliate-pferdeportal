# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-11
STATUS: AKTIV

## AKTUELL

175/175 fachlich disponiert:
- 150 V1-fähige Produkt-Evidence-Gruppen;
- 25 `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`;
- 0 ungeklärte Coverage-Gruppen.

UPC 0.8.6 besitzt technisch weiterhin nur 7 maschinenfeste Vergleichsprofile/Decision-Policies; 143/150 sind technisch noch offen.

Seit der Readiness-Baseline sind source-bound, aber **nicht materialisiert**, weitere Profilspecs für 7 Gruppen erstellt:
- High-Neck-Decken;
- Deckengurte;
- Deckentaschen/Aufbewahrung;
- Stall-, Knoten-, Sicherheits- und Fohlenhalfter.

Belege:
`AKTENSCHRANK/60_FINAL_COVERAGE_DISPOSITION_175_V1_20260911.md`
`AKTENSCHRANK/61_READINESS_BASELINE_V1_150_20260911.md`
`AKTENSCHRANK/62_PROFILE_FACT_MATRIX_HIGH_NECK_DECKEN_V1_20260911.md`
`AKTENSCHRANK/63_PROFILE_FACT_MATRIX_DECKENZUBEHOER_V1_20260911.md`
`AKTENSCHRANK/64_PROFILE_FACT_MATRIX_HALFTER_V1_20260911.md`

Technischer 0.8.6-Stand bleibt lokal hart grün. WordPress-Live für 0.8.6 ist offen.

## BRANCH

`hobbyroom/productvergleich-workflow-v070-20260908`

## NEXT ACTION

Nächster fachlich zusammenhängender Profilblock in Registry-Reihenfolge:
1. `pferdebuersten`
2. `striegel`
3. `kardaetschen`

Für diese drei source-bound binden:
- konkrete Produktklasse je Registry-Key;
- gemeinsame Faktenmatrix;
- Nutzungsklasse/Pairing-Regeln;
- Decision-Policy je Fact-Key;
- aktuelle Herstellerprodukte dagegen prüfen.

Danach `schermaschinen` überspringen, weil bereits maschinenfest in UPC 0.8.6 vorhanden, und mit der nächsten V1-Gruppe ohne Profil fortfahren.

Keine finalen Produktpärchen manuell festlegen.
Kein Pluginrelease pro Gruppe.
Erst sinnvoll gebündelte Profilspecs -> technische Materialisierung -> kompletter Positiv-/Negativ-/Mutation-/Fresh-ZIP-Test.

## BLOCK-GRENZE

Kein Research-Fund automatisch als Product Knowledge.
Kein SEO vor fachlich zulässigem Kandidatenuniversum.
Keine freie Decision-Policy ohne Fakten-/Quellenbindung.
Finale Paarentscheidung ausschließlich im Plugin aus aktuellem Product Knowledge; regelmäßige Neubewertung bleibt Pflicht.
Kein Merge.
Kein Publish.
