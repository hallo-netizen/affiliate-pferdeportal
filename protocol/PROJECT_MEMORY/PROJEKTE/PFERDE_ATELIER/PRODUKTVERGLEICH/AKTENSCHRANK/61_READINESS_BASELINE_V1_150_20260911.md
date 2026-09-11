# PRODUKTVERGLEICH – READINESS BASELINE V1 / 150 PRODUKTGRUPPEN

Stand: 2026-09-11
Status: HARD READ-ONLY BASELINE / KEIN PLUGINBAU

## Fachliche Ausgangslage

Nach `60_FINAL_COVERAGE_DISPOSITION_175_V1_20260911.md`:
- 150 Registry-Keys besitzen konkrete Produkt-Evidence und sind grundsätzlich `PRODUCT_COMPARISON V1`-fähig;
- 25 Registry-Keys sind für V1 fachlich fail-closed `NOT_APPLICABLE`;
- 0 Coverage-Gruppen sind ungeklärt.

## Exakter technischer Gegencheck UPC 0.8.6

Geprüfte Fresh-ZIP:
`universal-product-comparison-0.8.6-prototype.zip`

SHA-256:
`6ad160d18fb0973463c214de4356447923cbb728e222725e5407868e580c24f6`

`config/pferde-atelier/group-registry.json`:
- 175 Gruppen.

`config/pferde-atelier/comparison-profiles.json`:
- exakt **7** vorhandene Profile/Policies:
  1. `regendecken`
  2. `winterdecken`
  3. `uebergangsdecken`
  4. `stalldecken`
  5. `unterdecken`
  6. `schermaschinen`
  7. `steigbuegel`

Damit besitzen **143 der 150 fachlich grundsätzlich V1-fähigen Registry-Gruppen noch kein aktuelles maschinenfestes Vergleichsprofil/Decision-Policy im 0.8.6-Kandidaten**.

Das ist kein neu entdeckter Codefehler. Es ist der erwartete nächste Daten-/Fachbindungsblock des V2-Ziels.

## Product-Knowledge-Grenze

UPK 0.5.1 WordPress-Live-Batch über die alte Recherchebasis:
- 17/17 alte Gruppen verarbeitet;
- 9 `pairing-ready` laut Batchsummary;
- aber nur alte 17-Gruppen-/102-Kandidaten-Basis;
- keine Markt-Vollständigkeit und keine 175er Readiness.

Die genaue globale aktuelle Live-Paarzahl wurde nicht belegt und wird nicht erfunden.

## Nächster korrekter Arbeitsweg

Nicht Paare manuell festlegen.
Nicht SEO starten.
Nicht 143 Dummy-Profile generieren.

Stattdessen je V1-Gruppe in Registry-Reihenfolge:
1. gemeinsame source-bound Faktenmatrix bestimmen;
2. Nutzungsklasse/pairing-equal-Regeln binden;
3. Decision-Policy je Fact-Key binden;
4. Produktidentitäten/Fakten darauf prüfen;
5. erst anschließend als Datenblock in Product Knowledge/Profile/Policy materialisieren;
6. Plugin berechnet daraus selbst alle zulässigen Cross-Brand-Paare.

Erste V1-fähige Registry-Gruppe ohne aktuelles 0.8.6-Profil:
`pferdedecken-high-neck-decken` / technischer `product_group_key = high-neck-decken`.

## Harte Grenze

`143 PROFILE/POLICY offen` bedeutet nicht 143 Pluginfehler und erzeugt keine Plugin-Orgie.
Profile werden fachlich in Blöcken vorbereitet; erst eine tatsächlich sinnvolle gebündelte Materialisierung kann einen neuen Releasekandidaten auslösen.

Kein SEO.
Kein Merge.
Kein Publish.
