# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-11
STATUS: AKTIV

## AKTUELL

175/175 fachlich disponiert:
- 150 V1-fähige Produkt-Evidence-Gruppen;
- 25 `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`;
- 0 ungeklärte Coverage-Gruppen.

UPC 0.8.6 besitzt technisch weiterhin nur 7 maschinenfeste Vergleichsprofile/Decision-Policies; **143/150 sind technisch noch offen**.

Seit der Readiness-Baseline sind source-bound, aber **nicht materialisiert**, zusätzliche Profilspecs für **77 Gruppen** erstellt.

Belege:
- `AKTENSCHRANK/60_FINAL_COVERAGE_DISPOSITION_175_V1_20260911.md`
- `AKTENSCHRANK/61_READINESS_BASELINE_V1_150_20260911.md`
- `AKTENSCHRANK/62_...` bis `AKTENSCHRANK/87_...`
- Nachhol-/Fortsetzungsprotokoll: `PROTOKOLL_NACHHOLUNG_20260911.md`

Jüngste Fachblöcke:
- 84: Reitplatzboden / Reitplatzumrandung / Reitplatzbeleuchtung;
- 85: Reitplatzbewässerung / Reitplatzspiegel / Reitplatzplaner / Reitplatzschleppe;
- 86: Hufschlagräumer / Reitplatzbewässerung mobil / Weidepflegegeräte;
- 87: Nachsaat Pferdeweiden / Weideschleppen / Unkrautstecher.

Technischer 0.8.6-Stand bleibt unverändert: vorhandene lokale Hard-/Fresh-ZIP-/Read-only-Audit-Receipts grün; **WordPress-Live für 0.8.6 offen**. Diese technischen Tests wurden in dieser Fortsetzung nicht neu ausgeführt.

## BRANCH

`hobbyroom/productvergleich-workflow-v070-20260908`

Arbeitsweg und Rückgabeweg bleiben auf diesem Branch.
Kein Merge und kein Publish vor vollständiger Freigabe.
Fremde/parallel laufende Branches nicht überschreiben.

## NEXT ACTION

Autoritative Portalstruktur hinter Akte 87:
1. `p175 weidewalzen`
2. `p176 solar-weidepumpen`
3. `p177 weidebrunnen` = V1-NOT-APPLICABLE, zwingend überspringen
4. `p178 wassertroege-fuer-weiden`
5. danach `p179 weidetimer`

Nächster fachlich zulässiger Profilblock ausschließlich:
1. `weidewalzen`
2. `solar-weidepumpen`
3. `wassertroege-fuer-weiden`

Vor Paaruniversum hart prüfen:
- p175 nur innerhalb gleicher Walzenbauart, Arbeitsbreiten-/Befüllungs-/Anbauklasse vergleichen;
- p176 Solar-Weidepumpen nur als vollständige reale Pump-/Solar-Systemklasse mit belegter Wasserquelle, Förderhöhe/-menge und Strom-/Solarkonfiguration normalisieren;
- p177 `weidebrunnen` bleibt gemäß finaler 25er Disposition fail-closed und darf kein Produktpaar erzeugen;
- p178 Wassertröge nur innerhalb gleicher Tränke-/Trogklasse und vergleichbarer Volumen-/Material-/Frost-/Anschlusslogik paaren;
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
