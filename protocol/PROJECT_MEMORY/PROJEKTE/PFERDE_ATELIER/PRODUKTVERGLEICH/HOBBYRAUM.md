# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-11
STATUS: AKTIV

## AKTUELL

175/175 fachlich disponiert:
- 150 V1-fähige Produkt-Evidence-Gruppen;
- 25 `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`;
- 0 ungeklärte Coverage-Gruppen.

UPC 0.8.6 besitzt technisch weiterhin nur 7 maschinenfeste Vergleichsprofile/Decision-Policies; **143/150 sind technisch noch offen**.

Seit der Readiness-Baseline sind source-bound, aber **nicht materialisiert**, weitere Profilspecs für **61 Gruppen** erstellt.

Belege:
`AKTENSCHRANK/60_FINAL_COVERAGE_DISPOSITION_175_V1_20260911.md`
`AKTENSCHRANK/61_READINESS_BASELINE_V1_150_20260911.md`
`AKTENSCHRANK/62_...` bis `AKTENSCHRANK/82_...`.

Jüngste Blöcke:
- 79: Boxenmatten / Krippen / Lecksteinhalter;
- 80: Putzplatzmatten / Anbindebalken / Anbinderinge;
- 81: Putzboxhalter / Schlauchhalter / Waschplatz;
- 82: Mistboy / Bollengabeln / Stallbesen.

Technischer 0.8.6-Stand bleibt unverändert lokal hart grün. WordPress-Live für 0.8.6 ist offen.

## BRANCH

`hobbyroom/productvergleich-workflow-v070-20260908`

## NEXT ACTION

Autoritative Portalstruktur in exakter Registry-Reihenfolge:
1. `p155 schubkarren`
2. `p156 mistcontainer`
3. `p157 mistlagerung` -> `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`, **überspringen**
4. `p158 paddockzaeune`
5. danach `p159 reitplatzboden`
6. `p160 reitplatzdrainage` -> `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`, **überspringen**

Nächster fachlich zulässiger Profilblock:
1. `schubkarren`
2. `mistcontainer`
3. `paddockzaeune`

Vor Paaruniversum hart prüfen:
- Schubkarren: gleiche Mulden-/Rahmen-/Rad-/Kapazitätsklasse; keine Zweiradkarre, Futterwagen oder Elektroschubkarre blind kreuzen;
- Mistcontainer: gleiche mobile/stationäre Containerklasse, Material, Volumen und Aufnahme-/Entleerungsmechanik; keine bauliche Mistlagerstätte;
- Paddockzäune: Pflicht-Subtyp nach Bau-/Material-/Elektrifizierungsprinzip; Holz-, Kunststoff-, Elektro- und mobile Panelzäune nie blind mischen;
- `mistlagerung` bleibt V1 NOT_APPLICABLE.

Aktuelle Dedup-/Fail-closed-Gates bleiben bindend:
- `stallbesen` gegen `hofbesen`;
- `boxenmatten` gegen `liegeflaechen-im-offenstall`;
- `putzboxhalter`, `boxenriegel`, bestimmte `boxengitter`-Subtypen bleiben bei fehlender Herstellerbreite 0 Paar.

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
