# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-08
STATUS: AKTIV / 0.7.0 WORDPRESS-LIVEABNAHME

## AKTUELLER AUFTRAG

Den jetzt lokal vollständig geprüften bidirektionalen Produktvergleichs-Gesamtworkflow einmal real in WordPress abnehmen.

## GEBUNDENER WORKFLOW

`SEO ↔ Produktwissen → Vergleichbarkeit → Nachfrage/Kannibalisierung → Dossier → Audit`

Harte Regeln:
- genau 2 Produkte je Produktvergleich;
- unterschiedliche Hersteller;
- keine erfundenen Produktidentitäten oder Fakten;
- SEO darf konkrete Produkt-/Paar-Nachfrage entdecken;
- Produktwissen darf technisch sinnvolle Paare zur SEO-Prüfung geben;
- unbekannte konkrete SEO-Produkte → Produktrecherche, nicht Ersatzprodukt;
- vorhandener SEO-Bestand/Cache zuerst;
- Provider nur für danach echte SEO-Lücken;
- Teilresultat nie Gesamt-PASS;
- keine Writer-/Draft-/Publish-Arbeit in dieser Prüfstufe.

## TESTKANDIDAT

Plugin:
`Universal Product Comparison 0.7.0-prototype`

ZIP SHA-256:
`b6563940f96d0e9134109779f8046b5e8b9e1109bc9965d9d01deb5c75ed610d`

Technischer Isolationsbranch:
`hobbyroom/productvergleich-workflow-v070-20260908`

Kein main-Merge.

## LOKALER BELEG

PASS:
- PHP-Lint 31/31;
- 0.6 SEO-Regressions;
- 0.6 Dossier-Regressions;
- bidirektionale SEO-/Produktrecherche-Erkennung positiv/negativ;
- Pairing positiv/negativ;
- Profil-Drift negativ;
- kompletter Workflow positiv/negativ;
- Bootstrap/Single-Door;
- echte PSTE-Themenmap 81 Themen / False-Pair-Guard;
- statischer Gesamtworkflow-Release-Gate;
- fertige ZIP frisch entpackt und vollständig erneut geprüft;
- Source ↔ Fresh-ZIP byte-identisch.

## NEXT ACTION

**Einziger nächster Nutzertest:**

WordPress → Plugins → `Universal Product Comparison` mit 0.7.0 ersetzen.

Danach:
WordPress → **Produktvergleich → Vergleichsplanung** → **Regendecken** → **Gesamtworkflow starten**.

Danach Screenshot/Ergebnis zurückgeben.

Erst diesen realen Zustand prüfen. Kein neuer Pluginstand, kein Writer, kein Draft, kein Publish vor dieser Abnahme.

## RÜCKGABEWEG

Realbefund hier im PRODUKTVERGLEICH-Büro auswerten.
Bei Fehler: zuerst gegen den gesamten gebundenen Workflow prüfen, dann kleinster KISS-Fix im Hobbyraum; keine neue Architektur und keine Zwischen-ZIP.
