# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-11
STATUS: AKTIV

## AKTUELL

175/175 fachlich disponiert:
- 150 V1-fähige Produkt-Evidence-Gruppen;
- 25 `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`;
- 0 ungeklärte Coverage-Gruppen.

UPC 0.8.6 besitzt technisch weiterhin nur 7 maschinenfeste Vergleichsprofile/Decision-Policies; **143/150 sind technisch noch offen**.

Seit der Readiness-Baseline sind source-bound, aber **nicht materialisiert**, weitere Profilspecs für **39 Gruppen** erstellt.

Belege:
`AKTENSCHRANK/60_FINAL_COVERAGE_DISPOSITION_175_V1_20260911.md`
`AKTENSCHRANK/61_READINESS_BASELINE_V1_150_20260911.md`
`AKTENSCHRANK/62_...` bis `AKTENSCHRANK/75_...`.

Jüngste Blöcke:
- 73: Whiteboards / Hoftraktoren / Hoflader-Zubehör;
- 74: Hofbesen / Hofabsperrungen / Rampen;
- 75: Hofbeleuchtung / Stallbeleuchtung / Frostwächter.

Technischer 0.8.6-Stand bleibt unverändert lokal hart grün. WordPress-Live für 0.8.6 ist offen.

## BRANCH

`hobbyroom/productvergleich-workflow-v070-20260908`

## NEXT ACTION

Registry nach `frostwaechter` frisch direkt aus Portalstruktur + finaler V1-Disposition geprüft.

Explizit überspringen:
- `wasserleitungen-im-stall` -> `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`.

Nächster fachlich zulässiger Profilblock:
1. `luefter-im-stall`
2. `zeitschaltuhren-im-stall`
3. `kameras-im-stall`

Für den Dreierblock source-bound binden:
- konkrete Produkt-/Konstruktionsklasse;
- gemeinsame Faktenmatrix;
- Nutzungsklasse/Pairing-Regeln;
- Decision-Policy je Fact-Key;
- aktuelle Herstellerprodukte dagegen prüfen.

Vor Paaruniversum hart prüfen:
- Lüfter: Stall-/Landwirtschaftseignung, Montageart, Luftleistung, Schutzart und Regelklasse; keine Haushaltsventilatoren einschleusen;
- Zeitschaltuhren: physische Schaltklasse, Kanalzahl, Installationsart, Schaltleistung und Schutzart; keine reine App/Cloud-Automation gegen Hardware;
- Kameras: Innen/Außen-/Stallklasse, IP-Schutz, Netz/WLAN, Speicherung, Nachtsicht und Datenschutz-/Cloudabhängigkeit getrennt halten; keine Baby-/Wohnraumkamera allein wegen Bildfunktion einschleusen.

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
