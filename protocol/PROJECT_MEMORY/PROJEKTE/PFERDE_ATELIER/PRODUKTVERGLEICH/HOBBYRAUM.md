# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-11
STATUS: AKTIV

## AKTUELL

175/175 fachlich disponiert:
- 150 V1-fähige Produkt-Evidence-Gruppen;
- 25 `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`;
- 0 ungeklärte Coverage-Gruppen.

UPC 0.8.6 besitzt technisch weiterhin nur 7 maschinenfeste Vergleichsprofile/Decision-Policies; 143/150 sind technisch noch offen.

Seit der Readiness-Baseline sind source-bound, aber **nicht materialisiert**, weitere Profilspecs für 21 Gruppen erstellt:
- High-Neck-Decken;
- Deckengurte;
- Deckentaschen/Aufbewahrung;
- Stall-, Knoten-, Sicherheits- und Fohlenhalfter;
- Pferdebürsten;
- Striegel;
- Kardätschen;
- Satteldecken;
- Schabracken;
- Sattelgurte;
- Sattelschränke;
- Satteltransport;
- Englische Trensen;
- Gebisse;
- gebisslose Zäumungen;
- Zügel;
- Sperrriemen;
- Reithalfter.

Belege:
`AKTENSCHRANK/60_FINAL_COVERAGE_DISPOSITION_175_V1_20260911.md`
`AKTENSCHRANK/61_READINESS_BASELINE_V1_150_20260911.md`
`AKTENSCHRANK/62_...` bis `AKTENSCHRANK/69_...`.

Technischer 0.8.6-Stand bleibt unverändert lokal hart grün. WordPress-Live für 0.8.6 ist offen.

## BRANCH

`hobbyroom/productvergleich-workflow-v070-20260908`

## NEXT ACTION

Registry nach `reithalfter` frisch gegen Portalstruktur + finale V1-Disposition geprüft.

Explizit überspringen:
- `offenstallraufen` -> `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`;
- `offenstalltore` -> `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`.

Nächster fachlich zulässiger Profilblock in Registry-Reihenfolge:
1. `liegeflaechen-im-offenstall`
2. `offenstall-bodenbefestigung`
3. `fressstaender-im-offenstall`

Danach:
`trennwaende-im-offenstall`.

Für den Dreierblock source-bound binden:
- konkrete Produkt-/Konstruktionsklasse je Registry-Key;
- gemeinsame Faktenmatrix;
- Nutzungsklasse/Pairing-Regeln;
- Decision-Policy je Fact-Key;
- aktuelle Herstellerprodukte dagegen prüfen.

Vor Paaruniversum hart prüfen:
- Liegefläche: Gummi-/Matten-/Belagsklasse und Einsatzart nicht mit kompletter Bodenbefestigung vermischen;
- Offenstall-Bodenbefestigung: Paddock-/Flächenbefestigungssysteme nach Bau-/Mechanikklasse normalisieren; keine reine Liege-/Boxenmatte einschleusen;
- Fressständer: echter räumlich abgegrenzter Individual-Fressstand, nicht bloß Fressgitter/Fresszaun/Raufe.

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
