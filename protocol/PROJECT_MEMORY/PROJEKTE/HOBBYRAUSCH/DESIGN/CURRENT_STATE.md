# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-21
STATUS: **1.50.706 FOOTER FINAL LOCAL HARD PASS / LIVE-READBACK OFFEN**

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

## 1.50.706 – Footer final

1.50.706 basiert bytegenau auf 1.50.705 und ändert ausschließlich:
- Pluginversion;
- aktiven Hobby-Depot-Footer in `class-hobby-depot-profile-v150699.php`.

Verbindliche Nutzerentscheidung:
- bisherige dunkle Footer-Farbwelt bleibt;
- bestehendes weiß reduziertes Footer-Logo bleibt;
- Hobbyfinder-Einzellink entfernt;
- `Zeit, Budget & Platz` und `Anbieter` werden im Footer nicht ausgegeben;
- alte/Theme-`.footer-navbar` wird ausgeblendet;
- Linkschrift größer: 14 px;
- Spaltenüberschriften größer: 15 px;
- Claim größer: 13.5 px;
- Copyright mit dynamischer Jahreszahl direkt im dunklen Footer;
- keine zusätzliche Trennlinie/untere helle Linkleiste.

Lokale Hard-QA:
- Footer-Render mit absichtlich vorhandenen unerwünschten Menüeinträgen: Filter PASS;
- Hobbyfinder: 0 Treffer;
- Zeit/Budget: 0 Treffer;
- Anbieter als Zusatzlink: 0 Treffer;
- Rechtliches/Informationen/Anzeigenmarkt vollständig PASS;
- Copyright `© 2026 Hobby Depot` PASS;
- gesamte Plugin-PHP-Syntax: **135/135 PASS**;
- gegenüber 1.50.705 exakt **2 vorhandene Dateien geändert**, keine entfernt;
- ZIP CRC PASS.

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.706_FOOTER_FINAL_HARDPASS.zip`

SHA-256:
`372833ff90552f708ca3d71b04cb65f7354c1977aaa7fa03108ec6c3ebd8c8e6`

Größe:
58,685,650 Bytes.

Finder-Logik/-Design aus 1.50.705 wurde durch diesen Footerauftrag nicht verändert.

## ERSTER OFFENER BLOCKER

**Echter WordPress-Live-Readback des 1.50.706-Footers.**

## EXAKT EINE NEXT ACTION

**1.50.706 über das bestehende Designplugin installieren und nur den Footer auf Desktop/Mobil prüfen: keine untere helle Zusatzleiste, kein Hobbyfinder-Link, größere Links, Copyright im dunklen Footer.**
