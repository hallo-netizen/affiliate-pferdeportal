# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-11
STATUS: AKTIV

## AKTUELL

175/175 fachlich disponiert:
- 150 V1-fähige Produkt-Evidence-Gruppen;
- 25 `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`;
- 0 ungeklärte Coverage-Gruppen.

UPC 0.8.6 besitzt technisch weiterhin nur 7 maschinenfeste Vergleichsprofile/Decision-Policies; **143/150 sind technisch noch offen**.

Seit der Readiness-Baseline sind source-bound, aber **nicht materialisiert**, zusätzliche Profilspecs für **71 Gruppen** erstellt.

Belege:
- `AKTENSCHRANK/60_FINAL_COVERAGE_DISPOSITION_175_V1_20260911.md`
- `AKTENSCHRANK/61_READINESS_BASELINE_V1_150_20260911.md`
- `AKTENSCHRANK/62_...` bis `AKTENSCHRANK/85_...`
- Nachhol-/Fortsetzungsprotokoll: `PROTOKOLL_NACHHOLUNG_20260911.md`

Jüngste Fachblöcke:
- 83: Schubkarren / Mistcontainer / Paddockzäune;
- 84: Reitplatzboden / Reitplatzumrandung / Reitplatzbeleuchtung;
- 85: Reitplatzbewässerung / Reitplatzspiegel / Reitplatzplaner / Reitplatzschleppe.

Technischer 0.8.6-Stand bleibt unverändert: historisch lokal hart + Fresh-ZIP + read-only Audit grün; **WordPress-Live für 0.8.6 offen**.

## BRANCH

`hobbyroom/productvergleich-workflow-v070-20260908`

Arbeitsweg und Rückgabeweg bleiben auf diesem Branch.
Kein Merge und kein Publish vor vollständiger Freigabe.
Fremde/parallel laufende Branches nicht überschreiben.

## NEXT ACTION

Die frühere p163–p165-Beschriftung mit Hindernisstangen/Sprungständern/Cavaletti war falsch und ist in `FEHLERQUELLEN.md` als `PV-GOV-20260911-002` korrigiert.

Autoritative Portalstruktur hinter Akte 85:
- `p167 bahnplaner` -> V1-NOT-APPLICABLE, überspringen;
- `p168 sandverteiler` -> V1-NOT-APPLICABLE, überspringen;
- `p169 hufschlagraeumer`;
- `p170 reitplatzbewaesserung-mobil`;
- `p171 weidepflegegeraete`.

Nächster fachlich zulässiger Profilblock ausschließlich:
1. `hufschlagraeumer`
2. `reitplatzbewaesserung-mobil`
3. `weidepflegegeraete`

Vor Paaruniversum hart prüfen:
- identische reale Nutzungsklasse/Subtyp-Bindung;
- `reitplatzbewaesserung-mobil` strikt von fest installierter `reitplatzbewaesserung` trennen;
- bei mobilen Beregnungsgeräten OEM-/Herstellerfamilie nicht aus Produktnamen ableiten;
- `weidepflegegeraete` nur über einen klar definierten ersten mechanischen Produkt-Subtyp öffnen;
- Hufschlagräumer als eigenes Produkt/Zubehör nur gegen denselben Mechanik-/Anbau-Subtyp paaren;
- fehlende Cross-Brand-Vergleichbarkeit -> 0 Paar, nicht erzwingen;
- finale konkrete Produktpaarentscheidung nicht manuell festlegen.

Aktuelle Dedup-/Fail-closed-Gates aller bisherigen Akten bleiben bindend.
Die 25 V1-NOT-APPLICABLE-Gruppen bleiben gesperrt.

Kein Pluginrelease pro Gruppe.
Erst sinnvoll gebündelte source-bound Profilspecs -> technische Materialisierung -> kompletter Positiv-/Negativ-/Mutation-/Fresh-ZIP-Test.

## BLOCK-GRENZE

Kein Research-Fund automatisch als Product Knowledge.
Kein SEO vor fachlich zulässigem Kandidatenuniversum.
Keine freie Decision-Policy ohne Fakten-/Quellenbindung.
Finale Paarentscheidung ausschließlich im Plugin aus aktuellem Product Knowledge; regelmäßige Neubewertung bleibt Pflicht.
Kein Writer/Draft/Publish aus diesem Büro.
Kein Codex.
Kein Merge.
Kein Publish.
