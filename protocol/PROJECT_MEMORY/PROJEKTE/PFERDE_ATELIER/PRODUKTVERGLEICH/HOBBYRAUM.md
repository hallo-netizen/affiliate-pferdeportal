# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-11
STATUS: AKTIV

## AKTUELL

175/175 fachlich disponiert:
- 150 V1-fähige Produkt-Evidence-Gruppen;
- 25 `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`;
- 0 ungeklärte Coverage-Gruppen.

UPC 0.8.6 besitzt technisch weiterhin nur 7 maschinenfeste Vergleichsprofile/Decision-Policies; 143/150 sind technisch noch offen.

Seit der Readiness-Baseline sind source-bound, aber **nicht materialisiert**, weitere Profilspecs für **30 Gruppen** erstellt.

Belege:
`AKTENSCHRANK/60_FINAL_COVERAGE_DISPOSITION_175_V1_20260911.md`
`AKTENSCHRANK/61_READINESS_BASELINE_V1_150_20260911.md`
`AKTENSCHRANK/62_...` bis `AKTENSCHRANK/72_...`.

Neu gebunden:
- Akte 70: Liegeflächen / Offenstall-Bodenbefestigung / Fressständer;
- Akte 71: Trennwände / Stalldokumente / Futtertafeln;
- Akte 72: Werkzeughalter / Namensschilder / Stalltafeln.

Technischer 0.8.6-Stand bleibt unverändert lokal hart grün. WordPress-Live für 0.8.6 ist offen.

## BRANCH

`hobbyroom/productvergleich-workflow-v070-20260908`

## NEXT ACTION

Registry nach `stalltafeln` frisch direkt aus der Portalstruktur gelesen.

Nächster fachlich zulässiger Profilblock:
1. `whiteboards-fuer-stallplanung`
2. `hoftraktoren`
3. `hoflader-zubehoer`

Danach:
`hofbesen`.

Für den Dreierblock source-bound binden:
- konkrete Produkt-/Konstruktionsklasse je Registry-Key;
- gemeinsame Faktenmatrix;
- Nutzungsklasse/Pairing-Regeln;
- Decision-Policy je Fact-Key;
- aktuelle Herstellerprodukte dagegen prüfen.

Vor Paaruniversum hart prüfen:
- Whiteboards: zentrale Stallplanung/Organisation, keine Einzelbox-Stalltafel oder Futterplantafel;
- Hoftraktoren: gleiche Fahrzeug-/Leistungs-/Antriebsklasse und Hofnutzung; keine Hoflader/UTV/Kommunalgeräte vermischen;
- Hoflader-Zubehör: Pflicht-Subtyp nach Anbaugerät; Schaufel, Greifschaufel, Palettengabel, Ballenspieß, Kehrmaschine etc. getrennt halten.

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
