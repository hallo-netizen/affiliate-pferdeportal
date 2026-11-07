# Pferdeatelier / PSTE / MINI – Portalweiter Abgleich, KISS (07.11.2026)

## Status dieser Chat-Fortsetzung
**Geprüfter IST-Zustand und Entscheidungsvorlage; KEINE bereits umgesetzte Integration; KEINE WordPress-Installationsfreigabe.** Zweiter externer Titelworkflow `MINI:start`, strikt getrennt von K0. Der frühere Hinweis „Beta“ war falsch und bezeichnet keinen Produktbestandteil. Keine neue Titel-/Dublettenautorität oder neuer Worker beauftragt.

## Grundlage – tatsächliche, überprüfte Quellen
- GitHub-Branch `feature/mini-title-gate-independent-v1-20261104`: `mini-title-gate/START_HERE.md`, `TITELREGELN_V1.json`, `ERGEBNIS_100_TITEL_20261106.json`, `contracts/intent-first-title-governance-v1.json`. Ergebnis 100 Originalqueries, 87 JA, 9 VIELLEICHT, 4 NEIN, 97 Titelideen. Sprachtest GitHub Action #42207349100 laut Workflow-Ergebnis `success`. **Kein bereits nachgewiesener vollständiger SEO-Bestandsabgleich/WordPress-Produktions-PASS**.
- Echte PSTE-ZIP `PSTE-0.57.144.22-NUR-TEST.zip` lokal aus dem verifizierten Installationspaket geöffnet und Funktionen gelesen:
  * `PSTE_Mini_Workflow::LIMITS = [100,500,1000,2000]`. **200 oder 300 sind aktuell keine auswählbaren MINI-Stapelgrößen**, 100 und 500 schon.
  * `PSTE_Admin::exportTitleDesk()` / `preflightTitleDeskImport()`: 100er-Titelübergabe; Import erlaubt Titel/geliefert-Markierung, **keine zusätzliche semantische Freigabe-/Dublettenspalte**.
  * `PSTE_Mini_Workflow::manualArticleBrief()`: sammelt nur für **ein einzelnes** manuelles Thema maximal 1.200 WordPress-Artikel und maximal 1.200 `planning_suitability=YES`-Themen, setzt `inventory_complete=false` beim Überschreiten und warnt ausdrücklich, dass PSERC-eigene Pläne nicht abgedeckt sind. **Kein kompletter Portalbestand für 100er/300er MINI-Stapel**.
  * `PSTE_Snapshot::inventory()`: lesen aller WordPress-`post` mit `post_status=['publish','draft']`, Titel/Kategorie/Beitragsart/Überschriften/Content-Fingerprint; **kein Volltext**, andere Zustände `future,pending,private` fehlen, ebenso `page` und ggf. andere öffentliche Inhaltsarten. Zur Anspruchserfüllung nicht einfach „alle Artikel“ behaupten.
  * `PSTE_Snapshot::editorialPlan()`: vorhandener Planleser, kann `NOT_AVAILABLE` zurückgeben, bei fehlendem importierten Plan. **Vollständigkeit und Aktualität des LIVE-Redaktionsplans nicht bewiesen**.
- In den früheren `.22`-Gegenproben wurden falsche semantische PASS gefunden: `2er` / `zwei Pferde` und `0g` / `ungefüttert`. Beleg `EVIDENCE/PSTE_05714422_INHALTLICHE_GEGENPRUEFUNG_20261107.md`.
- `pste-gesamtdiagnose-2026-11-07.json`: **5.016 Keyword-/Themen-Datensätze** in der Gesamtdiagnose. **Das ist nicht gleichbedeutend mit 5.016 veröffentlichten Artikeln**.

## Verbindliche fachliche Antwort auf die Bestandsfrage
**JA: Jede einzelne der 100/200/300 neuen Suchfragen muss gegen den gesamten für Artikelüberschneidungen relevanten Portalbestand geprüft werden:** veröffentlichte, entworfene, geplante, terminierte, private und wartende Beiträge; relevante Seiten/Glossar/weitere SEO-Inhaltstypen; sämtliche gültigen aktiven Redaktionsplan-Slots; **auch gegen die anderen neuen Suchfragen desselben Stapels**. Nicht nur innerhalb der 100/300 vergleichen. Ohne Vollständigkeitsnachweis KEINE automatische Freigabe.
**NEIN: Dafür muss nicht bei jedem 100er-Stapel der vollständige Fließtext sämtlicher Artikel an eine Sprach-KI übergeben werden.** Ein aktuelles, gesamthaftes, einmal gebundenes Suchinventar mit Artikelkennung, Titel, SEO-Suchziel, Kategorie, Beitragsart, Status, Überschriften und ggf. Kurzbeschreibung reicht für Kandidatensuche; bei möglichen Konflikten muss gezielt auf echten Artikelinhalt zugegriffen werden. Kein unzulässiges „top N = vollständig“: Alle Einträge müssen durchsuchbar bleiben. Gleiche Bedeutung kann ohne identische Wörter bestehen. Bei unklarer Abdeckung: Zurückstellen statt Freigeben.
**Aktualität**: Das gebundene Bestandsbild muss zur Entscheidung frisch sein bzw. gegen zwischenzeitliche Änderungen geprüft werden. Ergebnisse gegen alte Stände nicht blind zurückspielen. **Keine sensiblen Entwürfe in öffentliches GitHub-Repository schreiben.**

## Tatsächlicher Größen-/Stapeltest, strikt synthetisch
Lokales, wiederholbares Skript `pste_portalwide_size_probe_20261107.py` nutzt echte MINI-JA-Quellen/Titel aus dem 100er-Ergebnis, **vervielfacht aber künstlich Artikel und Redaktionspläne**, verpackt und liest JSON zurück, ohne WordPress-/Agenten-Kopplung und **ohne semantische Qualitätsprüfung**:
- 1.200 Artikel + 500 Pläne + 100 Keywords: 0,432 MB
- 5.000 Artikel + 1.200 Pläne + 100 Keywords: 1,558 MB
- 5.000 Artikel + 1.200 Pläne + 300 Keywords: 1,611 MB
- 10.000 Artikel + 3.000 Pläne + 300 Keywords: 3,250 MB
Ergebnis: **Die reine Datengröße einer kompakten Gesamtliste ist grundsätzlich praktikabel**. Diese Zahlen beweisen nicht, dass der bestehende externe KI-Worker automatisch 5.000+ Datensätze semantisch fehlerfrei verarbeiten kann. **Nicht jedes einzelne Gesamtinventar blind vollständig in den KI-Textkontext laden**: vollständige lokale Suche/Index und relevante Konfliktbelege dem einen fachlichen Entscheider geben.

## KISS-Fahrplan / Arbeitsrealität
1. Vorhandenes PSTE erstellt **ein gebundenes, vollständigkeits- und aktualitätsgeprüftes Portal-Suchinventar** (inkl. WP und sämtlichen aktiven Plänen). Bestehende Datenleser nutzen; fehlende Zustände/Inhaltstypen ergänzen; kein neuer fachlicher Prüfer.
2. Vorhandener `MINI:start` Titelworker verarbeitet 100er- oder gegebenenfalls größere Pakete und nutzt dasselbe **vollständige** Portal-Suchinventar für Kandidatenauswahl, Nachfrage bei unsicherer Abdeckung und Vergleich **innerhalb des Stapels**. Einmalige finale SEO-Suchintent-Entscheidung durch genau EINE fachliche Autorität – Zuständigkeit mit bisherigem `PSTE_Planning_Readiness_Gate` überschneidungsfrei klären, sonst neue Dopplung!
3. Vorhandene geschützte Rückgabe um drei sachliche Ergebnisse erweitern: eindeutige Dublette (mit echter Artikel-/Plan-Quelle), eigenständige Suchabsicht und guter Titel, oder wegen unsicherer Abdeckung zurückstellen. WordPress übernimmt die **eine** Entscheidung, prüft nur technische Herkunft/Integrität und die Aktualität der Portal-Momentaufnahme, dann vorhandenes Fach/Magazin/Redaktionsbüro-Routing. K0, PSERC, bestehende Artikel/Content nicht verändern.
4. **Operative Grenze**: GitHub Actions kann Dateitransporte/Regeltests ausführen; ein automatisch laufender sprachlich formulierender und semantisch urteilender KI-Worker **ohne KI-API** ist im verifizierten `MINI:start` bisher **nicht end-to-end nachgewiesen**. Ohne diese Bindung keine Behauptung „vollautomatisch ohne manuelles Tun“. Ein Dateipaar pro Stapel wäre allenfalls Übergang, **nicht pro Keyword**, widerspricht aber dem Wunsch nach vollständig automatisch. Der echte Automatismus muss anhand vorhandener GitHub-Rollen und Rückkanäle unabhängig geprüft werden, bevor gebaut wird.

## Entscheidung / Grenzen
**Praktikabilität des portalweiten Vergleichs der Metadaten: JA, Größenprobe bestanden.**
**Vollständig installierbarer und fehlerfrei autonomer End-to-end-Workflow: NEIN, derzeit nicht nachgewiesen** wegen fehlender gesamthafter und aktueller Live-Portalabdeckung, Import semantischer Entscheidungen und unbelegter autonomer Sprach-KI-Ausführung. Keine neuen Plugin-ZIPs und keine Tests auf der Nutzer-Website bis diese drei Lücken in einer lokalen Gesamtprobe geschlossen sind.
