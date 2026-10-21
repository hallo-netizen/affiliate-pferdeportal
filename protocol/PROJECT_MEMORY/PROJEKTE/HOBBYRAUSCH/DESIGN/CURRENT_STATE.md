# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-21
STATUS: **1.50.710 FOOTER EXAKTER AKTIVER RENDERER KORRIGIERT / LIVE-READBACK OFFEN**

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

## LIVE-READBACK 21.10.2026

Nutzer meldet nach Installation von 1.50.706: **Frontend-Footer unverändert**.

Lokale Gegenprüfung der tatsächlich gepackten ZIP:
- Pluginheader: 1.50.706;
- Laufzeitklasse: RELEASE 1.50.706;
- gerenderter Footer enthält **keinen Hobbyfinder-Link**;
- gerenderter Footer enthält **keinen Zeit/Budget-/Anbieter-Zusatz**;
- gerenderter Footer enthält **© 2026 Hobby Depot**;
- Links 14px, Überschriften 15px;
- ZIP enthält genau diese geänderten Dateien.

Daraus folgt: Der sichtbare Live-Footer kann nicht aus dem lokal geprüften 1.50.706-Render stammen. Vor einem weiteren Build muss deshalb der tatsächlich aktive Live-Pluginstand bzw. ein alter ausgelieferter/cachender Codepfad identifiziert werden. Keine weitere Footer-Version auf Verdacht bauen.

## 1.50.707 – neuer Laufzeitpfad gegen alten Footer-Code

706 war als Pluginversion live aktiv, aber intern weiterhin an die alte Laufzeitklasse/-datei V150699 gebunden. Dadurch konnte 706 allein nicht beweisen, dass wirklich der neue Footer-Codepfad ausgeführt wurde.

1.50.707 erzwingt deshalb einen neuen Runtime-Pfad:
- neue Datei `class-hobby-depot-profile-v150707.php`;
- neue Klasse `Hobby_Depot_Profile_V150707`;
- neue eigene Templates `hobby-depot-front-v150707.php` und `hobby-depot-content-v150707.php`;
- Hauptplugin referenziert **nicht mehr** V150699;
- Footer trägt eindeutigen Marker `data-hd-runtime="1.50.707"` und HTML-Kommentar `HD-003 RUNTIME 1.50.707`;
- Glossar-Runtime-Auflösung wurde mit gleichzeitig deklarierter alter V150699 geprüft und wählt V150707.

Footerinhalt unverändert nach Nutzerentscheidung:
- kein Hobbyfinder;
- kein Zeit/Budget-/Anbieter-Zusatz;
- Copyright im dunklen Footer;
- größere Footerlinks/Überschriften;
- Theme-Footer verborgen.

Hard-QA:
- Footer-Render mit absichtlich enthaltenen unerwünschten Menüpunkten: PASS;
- neuer Runtime-Marker: PASS;
- Hauptplugin ohne V150699-Runtime-Referenz: PASS;
- Front-/Content-Templates auf V150707: PASS;
- Glossar-Resolver bei gleichzeitig vorhandener V150699: **V150707 PASS**;
- PHP-Lint **138/138 PASS**;
- ZIP-Integrität PASS.

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.707_FOOTER_RUNTIME_HARDPASS.zip`

SHA-256:
`ad567c9b4376ed4c5ad06d95406c16957aeff7ce7b4cb9fce313835dc2880006`

Größe:
58,828,942 Bytes.

## 21.10.2026 – 1.50.710 exakter aktiver Footer-Renderer

Neue Live-Rückmeldung: 1.50.709 wirkt strukturell tatsächlich:
- weiße Zusatzzeile unten weg;
- unterer Abstand weg;
- dynamisches Copyright ist im dunklen Footer vorhanden.

Damit ist HD-003 als aktiver sichtbarer Footer-Renderer bewiesen; kein Deployment-/Owner-Problem mehr.

Exakter aktiver Code:
`Hobby_Depot_Profile_V150709::render_footer()` in HD-003.

Konkrete noch vorhandene Fehler im aktiven Renderer:
- Footer-Logo wurde per CSS `filter:brightness(0) invert(1)` weiterhin zwangsweise weiß dargestellt;
- Linkschrift nur 14 px, Spaltenüberschriften 15 px, Claim 13.5 px;
- negativer Render-Test zeigte zusätzlich: `Hobbyfinder` konnte über das importierte Menü `Informationen` erneut in den Footer gelangen.

1.50.710 korrigiert nur diesen aktiven Renderer:
- neues Runtimeprofil V150710;
- Original-Logo unverändert farbig: `filter:none`, opacity 1, Breite 215 px;
- Claim 14.5 px;
- Spaltenüberschriften 16.5 px;
- Links 16 px;
- `Hobbyfinder`, `Anbieter`, `Zeit, Budget & Platz` explizit aus dem importierten Informationsmenü ausgeschlossen;
- dunkle Footer-Farbwelt bleibt unverändert;
- Copyright bleibt im Footer;
- HD-001-Autofooter bleibt deaktiviert.

Positiv-/Negativ-Renderprüfung mit absichtlich wieder eingeschleusten unerwünschten Menüeinträgen:
- Runtime 1.50.710: PASS;
- Copyright: PASS;
- Hobbyfinder: 0 Treffer PASS;
- Zeit/Budget: 0 Treffer PASS;
- Anbieter: 0 Treffer PASS;
- Magazin bleibt vorhanden: PASS;
- dunkler Footer exakt einmal: PASS;
- Original-Logo nicht weiß gefiltert: PASS;
- Linkschrift 16 px: PASS;
- Überschriften 16.5 px: PASS;
- Claim 14.5 px: PASS;
- aktiver Main-Router lädt ausschließlich V150710: PASS;
- PHP-Lint 138/138 PASS;
- ZIP-Integrität PASS.

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.710_FOOTER_REALFIX_EXACT_RENDER.zip`

SHA-256:
`cbb321ff0c766cbef16bd362f767dcc799cbb27b1a0cc4ee7156b7c53f4cd807`

Größe:
58,829,071 Bytes.
## ERSTER OFFENER BLOCKER

**Live-Readback von 1.50.710.**

## EXAKT EINE NEXT ACTION

**1.50.710 installieren und nur den dunklen Footer prüfen: Originallogo farbig, Links/Überschriften sichtbar größer, kein Hobbyfinder, kein Zeit/Budget/Anbieter-Zusatz, Copyright bleibt.**
