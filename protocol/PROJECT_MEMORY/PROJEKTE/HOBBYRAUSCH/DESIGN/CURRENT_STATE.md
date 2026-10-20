# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-20
STATUS: **1.50.705 HOBBYFINDER DESIGN LOCAL HARD PASS / LIVE-DESIGN-READBACK OFFEN**

Zielvertrag: **ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.5 / 2026-10-19**

## Basis

1.50.705 basiert direkt auf **1.50.704**.

Unverändert:
- stabile Laufzeitklasse `Hobby_Depot_Profile_V150699`;
- 862er Finderbestand über HD-007;
- 8 Schritte und Rankinglogik;
- 6 Ergebnisse;
- vier Kurzprofilfelder;
- echte CORE-Ziele ausschließlich über HD-004;
- keine zweite Hobby-Datenbank;
- Startseiten-/Hub-/Kategorie-/Footer-/Affiliate-/SEO-Grundstruktur.

## Live-Baseline 1.50.704

Der erste echte Frontend-Test zeigte zunächst keinen Finder, weil die WordPress-Seite unter
`/magazin/hobbyfinder/`
lag.

Nach Umstellung auf die vorgesehene Route
`/hobbyfinder/`
erschien der Finder korrekt. Der Nutzer hat den Finder anschließend vollständig durchgeklickt und als funktionierend bestätigt.

## Designauftrag 1.50.705

Umgesetzt:
- blaues Finder-Sonderfarbschema entfernt;
- bestehende Portal-Akzentfarbe Grün/Petrol für Progress, Auswahl, Buttons, Links und aktive Zustände verwendet;
- pro Antwortkachel ein schlichtes Linien-Icon;
- aktive Kachel klar grün markiert;
- kompakter Hero auf dem ersten Finder-Schritt;
- H1: **„Finde dein Hobby“**;
- kurze Subline statt der bisherigen langen Formulierung;
- `Zur Startseite` und `Neu starten` auf jedem Finder-Zustand;
- Ergebniskarten ziehen vorhandene Kategorie-/Zielbilder heran, wenn ein echtes Zielobjekt und ein vorhandenes Bild auflösbar sind;
- niemals erfundene Bild- oder Ziel-URL;
- ohne echtes Bild bleibt ein neutraler Welt-Icon-Fallback.

## Lokale QA 1.50.705

- PHP: **135/135 PASS**;
- JavaScript: **Syntax PASS**;
- Runtime: **862/862 PASS**;
- Finder-Scorefunktion gegenüber 1.50.704 unverändert: **PASS**;
- 41/41 Antwortoptionen besitzen eine Icon-Zuordnung;
- Bildauflösung Positivtest: **3/3 PASS**;
- unaufgelöstes Ziel bleibt ohne erfundene URL/Bild: **PASS**;
- ZIP: **PASS**.

## Artefakt

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.705_HOBBYFINDER_DESIGN_LOCALPASS.zip`

SHA-256:
`e56a3b170a888c876ece8e60969be52746a4245b464946d7af1912bc7eb067e5`

Größe:
58,685,530 Bytes.

## Abhängigkeit

- **HD-007 1.0.0 bleibt unverändert aktiv**;
- HD-004 bleibt alleinige Quelle für echte CORE-Zielobjekte/-URLs.

## ERSTER OFFENER BLOCKER

**Visuelle Live-Abnahme von 1.50.705 im echten WordPress-Frontend.**

## EXAKT EINE NEXT ACTION

**Nur HD-003 auf 1.50.705 aktualisieren. Danach `/hobbyfinder/` öffnen und Startbildschirm, grüne Auswahlzustände, Icons, Navigation und Ergebnisbilder prüfen.**
