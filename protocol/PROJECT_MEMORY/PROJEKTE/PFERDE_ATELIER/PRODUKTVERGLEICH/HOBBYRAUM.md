# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-11
STATUS: AKTIV

## AKTUELL

175/175 fachlich disponiert:
- 150 V1-fähige Produkt-Evidence-Gruppen;
- 25 `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`;
- 0 ungeklärte Coverage-Gruppen.

UPC 0.8.6 besitzt technisch weiterhin nur 7 maschinenfeste Vergleichsprofile/Decision-Policies; **143/150 sind technisch noch offen**.

Seit der Readiness-Baseline sind source-bound, aber **nicht materialisiert**, weitere Profilspecs für **45 Gruppen** erstellt.

Belege:
`AKTENSCHRANK/60_FINAL_COVERAGE_DISPOSITION_175_V1_20260911.md`
`AKTENSCHRANK/61_READINESS_BASELINE_V1_150_20260911.md`
`AKTENSCHRANK/62_...` bis `AKTENSCHRANK/77_...`.

Jüngste Blöcke:
- 75: Hofbeleuchtung / Stallbeleuchtung / Frostwächter;
- 76: Lüfter / Zeitschaltuhren / Kameras;
- 77: Mobile Unterstände / Windschutz / Dachrinnen.

Technischer 0.8.6-Stand bleibt unverändert lokal hart grün. WordPress-Live für 0.8.6 ist offen.

## BRANCH

`hobbyroom/productvergleich-workflow-v070-20260908`

## NEXT ACTION

Registry nach `dachrinnen-am-unterstand` frisch direkt aus der Portalstruktur gelesen.

Nächster fachlich zulässiger Profilblock:
1. `unterstand-beleuchtung`
2. `boxentueren`
3. `boxenriegel`
4. `boxengitter`

Für diesen Block source-bound binden:
- konkrete Produkt-/Konstruktionsklasse;
- Faktenmatrix;
- Nutzungsklasse/Pairing-Regeln;
- Decision-Policy je Fact-Key;
- aktuelle Herstellerprodukte dagegen prüfen.

Vor Paaruniversum hart prüfen:
- Unterstand-Beleuchtung: gleiche technische Leuchtenklasse; nicht bloß Hof- oder Stallbeleuchtung über einen anderen Standort-Key duplizieren;
- Boxentüren: gleiche Türbauart, Öffnungsmechanik, Material-/Füllungsklasse und Größenklasse;
- Boxenriegel: gleiche Verriegelungsmechanik und Montageklasse; Türbeschlag nicht mit allgemeinem Stallriegel mischen;
- Boxengitter: gleiche Gitter-/Front-/Montageklasse; keine komplette Boxenfront, Trennwand oder Fenstervergitterung blind kreuzen.

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
