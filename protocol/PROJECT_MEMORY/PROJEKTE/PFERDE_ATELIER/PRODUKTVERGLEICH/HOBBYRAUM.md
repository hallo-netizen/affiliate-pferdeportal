# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-11
STATUS: AKTIV

## AKTUELL

175/175 fachlich disponiert:
- 150 V1-fähige Produkt-Evidence-Gruppen;
- 25 `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`;
- 0 ungeklärte Coverage-Gruppen.

UPC 0.8.6 besitzt technisch weiterhin nur 7 maschinenfeste Vergleichsprofile/Decision-Policies; **143/150 sind technisch noch offen**.

Seit der Readiness-Baseline sind source-bound, aber **nicht materialisiert**, weitere Profilspecs für **49 Gruppen** erstellt.

Belege:
`AKTENSCHRANK/60_FINAL_COVERAGE_DISPOSITION_175_V1_20260911.md`
`AKTENSCHRANK/61_READINESS_BASELINE_V1_150_20260911.md`
`AKTENSCHRANK/62_...` bis `AKTENSCHRANK/78_...`.

Jüngste Blöcke:
- 76: Lüfter / Zeitschaltuhren / Kameras;
- 77: Mobile Unterstände / Windschutz / Dachrinnen;
- 78: Unterstand-Beleuchtung / Boxentüren / Boxenriegel / Boxengitter.

Technischer 0.8.6-Stand bleibt unverändert lokal hart grün. WordPress-Live für 0.8.6 ist offen.

## BRANCH

`hobbyroom/productvergleich-workflow-v070-20260908`

## NEXT ACTION

Registry nach `boxengitter` frisch direkt aus der Portalstruktur gelesen.

Nächster fachlich zulässiger Profilblock:
1. `boxenmatten`
2. `krippen-fuer-pferdeboxen`
3. `lecksteinhalter-fuer-boxen`

Für diesen Block source-bound binden:
- konkrete Produkt-/Konstruktionsklasse;
- Faktenmatrix;
- Nutzungsklasse/Pairing-Regeln;
- Decision-Policy je Fact-Key;
- aktuelle Herstellerprodukte dagegen prüfen.

Vor Paaruniversum hart prüfen:
- Boxenmatten: gleiche Stall-/Boxenmattenklasse nach Material, Stärke und Verlegung; keine Bodenraster oder abweichende Matratzensysteme blind kreuzen;
- Krippen: gleiche Futterkrippen-/Trogklasse, Material, Volumen und Montageart; keine Raufe/Tränke;
- Lecksteinhalter: gleiche Bau-/Montageklasse und passende Lecksteinform/-größe; keine Leckschale bzw. Leckstein selbst.

Akte 78 bleibt fail-closed, wo Herstellerbreite fehlt:
- `boxenriegel`: aktuell 0 Cross-Brand-Paare;
- `boxengitter`: 0 Paar zwischen 500x500-Gittereinsatz und großem Aufsatzgitter.

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
