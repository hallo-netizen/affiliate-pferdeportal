# BÜRO TEXTSYSTEM 4A

STAND: 2026-09-13
STATUS: AKTIV / ISOLIERTER GEGENPROTOTYP

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Das isolierte Architektur- und Testbüro für **Konzept 4a – Universelle Artikelkapsel**. Es prüft, ob der komplette Pferde-Atelier-Artikelworkflow mit weniger Laufzeitgrenzen als System 4 umgesetzt werden kann, ohne Inhalt, Design oder Qualitätsregeln anzutasten.

**HIER BIST DU RICHTIG, WENN …**  
der Weg vom gebundenen WordPress-/SEO-Produktionsanstoß bis zur fertigen, direkt importierbaren JSON-Datei im Elternchat untersucht, gebaut oder hart getestet wird.

**DU DARFST …**  
den vorhandenen produktiven Fach-/Regelbestand READ-ONLY verwenden, einen isolierten 4a-Hobbyraum bauen und positive/negative Tests durchführen.

**DU DARFST NICHT …**  
Textmaschine, PPM 6.7.9, LanguageTool 6.8, PSERC/PSTE, SEO-, Link-, Tabellen-, Metadaten-, Design-, Theme-/CSS- oder WordPress-Plugin-Regeln ändern; System 4/PR #238 verändern; Main mergen; veröffentlichen; einen Ersatzprüfer oder künstliches PASS bauen.

**ALS NÄCHSTES …**  
`CURRENT_STATE.md` → `HOBBYRAUM.md` → `ZIELVERTRAG.md` → `PROTOKOLL.md`.

## KERNIDEE

Ein Artikel besitzt vom Eingang bis zum Ausgang **genau einen kanonischen Zustand**. Genau ein Controller darf diesen Zustand fortschalten. Codex arbeitet fachlich, darf aber weder Route noch nächsten Schritt bestimmen. Prüfer sind reine Messinstrumente und liefern nur PASS oder konkrete Findings.

Zielkette:

`Produktionsanstoß/Metadaten -> Artikelkapsel -> Recherche -> Rechercheprüfung -> Fakten/Fact-Pack -> Faktenprüfung -> Text -> echte Vollprüfung -> Same-Article-Repair -> artikelübergreifende Prüfung -> universelle WordPress-JSON -> Elternchat`

## HARTE GRENZEN

1. **Keine Außensteuerung.** Eingangsmetadaten dürfen keine Route, Regeln, Prompts, Toolchain, Publish- oder Next-State-Angaben enthalten.
2. **Eine Zustandsautorität.** Nur der 4a-Controller darf `phase` verändern.
3. **Keine Prüf-Simulation.** Echte bestehende Prüfer bleiben alleinige PASS-Autorität.
4. **Inhalt READ-ONLY-Regelbestand.** Keine neue Autoren-/Textregel.
5. **Design READ-ONLY.** Kein Restyling und keine nachträgliche HTML-Reparatur.
6. **Qualität unverändert.** Bestehende Fach-/SEO-/PPM-/LT-/PSERC-/PSTE-Regeln bleiben verbindlich.
7. **1 bis unendlich.** Der Kern darf weder Artikelzahl noch konkrete Beitragsart hardcoden.
8. **Neue Beitragsarten.** Der Controller kennt keine fachlichen Sonderregeln. Er liest ausschließlich autoritative Beitragsart-Regeln; unbekannte/nicht freigegebene Arten blockieren fail-closed.
9. **Kein Auto-Publish.** `publish_allowed=false` bleibt unveränderlich.
10. **Ein finaler Ausgang.** Nach finalem PASS wird genau eine kanonische JSON-Datei für den verifizierten WordPress-Importer erzeugt und bytegleich an den Elternchat zurückgegeben.

## ABGRENZUNG ZU SYSTEM 4

System 4 ist kein Gegner und wird nicht ersetzt. 4a übernimmt nur bewährte Erkenntnisse: kanonischer Artikelzustand, Codex als ein fachlicher Worker, Same-Article-Repair, echte Prüfer, Research-/Fact-Evidence und Batch-Distinctness.

4a muss zusätzlich beweisen:
- keine feste `7`-Bindung;
- keine feste `Beratung`-Bindung im Transport/Controller;
- kein widersprüchlicher Signing-/Direct-Import-Endpfad;
- kein neuer Workflow-Besitzer zwischen Artikel-PASS und finaler Datei;
- neue Beitragsarten ohne Umbau des Controllers.

## ERFOLGSKRITERIUM

4a hat nur dann eine Existenzberechtigung, wenn es bei identischer Fach-/Design-/Qualitätsautorität **weniger echte Zustands-/Übergabegrenzen** als System 4 besitzt und 1/3/25/1000 Artikel sowie unterschiedliche freigegebene Beitragsarten positiv und negativ nachweisbar verarbeitet.
