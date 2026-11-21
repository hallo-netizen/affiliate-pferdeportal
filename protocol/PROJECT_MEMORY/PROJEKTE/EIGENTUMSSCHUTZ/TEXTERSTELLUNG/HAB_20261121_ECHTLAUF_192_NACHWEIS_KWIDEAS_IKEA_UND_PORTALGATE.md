# Hab & Bewahr – 21.11.2026, 09:32 – echter Lauf 192 Rohkeywords, erneut 0 verwendbar

**Gesichert mit der originalen Diagnose** `texterstellung-diagnose-20261121-083212.json`, v0.4.31.15:

- API real produktiv `api.dataforseo.com`, tatsächlicher Suchbegriff **`Abholbox`** (nicht mehr `Abholbox Hab`).
- **192** rohe Suchbegriffe: **68 Suggestions, 9 Related, 100 Ideas, 15 PAA**, **163** gespeicherte Kandidaten, **0** direkt verwendbar.
- **165/165** Aliasgruppen wegen zu enger Ursprungsfamilien-Prüfung `NO_MATCH`; 162/163 Kandidaten durch fehlende Portalrelevanz `SANDBOX_REQUIRED`. Relevant aus echten Daten: `abholbox mit code` (Suchvolumen 30) ebenfalls BLOCKED.
- Die Originalfunktion `PSTE_Research_Job::discoverySeeds()` wurde auf **68+9 originalen Trefferzeilen** exakt offline nachgebildet: Die 20 gewählten Keyword-Ideas-Anschlusssuchbegriffe enthalten **17-mal IKEA**; unter den tatsächlich erhaltenen 100 Idea-Ergebnissen **99-mal IKEA** und **0-mal Abholbox**. Unter den verwendeten Seeds sind z. B. `ikea leipzig` mit Volumen 14800 und `ikea produkte` mit 1000. Kein Provideraufruf für die Simulation.
- **Zwei verschiedene Ursachen:** Anbietersuch-Expansion driftet über reine Wortlängen-/Volumenwertung weg vom Fachthema; anschließend verlangt die Portalrelevanz 2 identische Kategorienwörter und volle C23-Familieneignung, weshalb selbst `abholbox mit code` nicht bis MINI kommt.
- Bei MINI werden nur **nachweislich portalrelevante JA-Rohkandidaten** importiert. „163 Themenkandidaten gespeichert“ bedeutet daher nicht „163 für MINI freigegeben“.
- **Keine 0.4.31.16 freigegeben, keine neue Plugininstallation, keine erneute Recherche**. Die Datei mit allen 192 Originalurteilen, die deterministische Simulation und das Vollprotokoll liegen im Hab-Büro unter `/hab-und-bewahr/TEXTERSTELLUNG/NACHPRUEFUNG_ECHTLAUF_192_20261121/`.
- Ziel des nächsten **gebündelten** Fixes: 4 Recherchewege breit lassen; die vorhandene Keyword-Ideas-Anschlussauswahl ohne fachfremde Marken-/Orts-Pivots bilden; den **einzigen** Portalrelevanz-Owner weniger eng mit echten vorhandenen Sicherheitskategorien auswerten; bestehende 192 Rohdaten **ohne erneute DataForSEO-Kosten** vollständig simulieren. K0, MINI, Import unverändert. Ein erfolgreiches WordPress-/Provider-Liveergebnis wird ausdrücklich **nicht** behauptet.
