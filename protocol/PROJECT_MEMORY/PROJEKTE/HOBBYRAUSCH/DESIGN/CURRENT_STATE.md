# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-21
STATUS: **1.50.709 HD-001 AUTOFOOTER ROOTFIX EXAKT REPRODUZIERT / LIVE-READBACK OFFEN**

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

## 21.10.2026 – Footer-Ursache exakt nachgewiesen

Die vorherige 1.50.708-Annahme „nativer Theme-Footer“ war falsch und wird verworfen.

Exakter Befund gegen den aktuellen Hobby-Depot-Stand:
- HD-001 / `affiliate-portal-kategorie-workflow` 1.14.16 registriert `APKW_FrontendStructure::output_auto_footer` an `wp_footer` mit Priorität 50.
- Diese Methode gibt `<div class="apkw-auto-footer">` plus eigenes CSS mit `background:#fff`, oberer Border und Abstand aus.
- Mit dem echten Hobby-Depot-V7.1-Profil reproduziert der aktuelle HD-001-Code exakt zwei Links: `Zeit, Budget & Platz` und `Anbieter`.
- Die Glossar-Shell rendert zuerst den dunklen HD-003-Footer und ruft danach `wp_footer()` auf. Deshalb erscheint der HD-001-Autofooter sichtbar darunter.
- Ursache ist damit **HD-001-Autofooter**, nicht Footer-Importer und nicht Theme-Footer.

## 1.50.709 – eigentlicher Rootfix

Basis: 1.50.707; die falschen 1.50.708-Theme-Unterdrückungen werden nicht übernommen.

Änderung:
- HD-003 registriert am von HD-001 selbst vorgesehenen Filter `apkw_auto_footer_enabled` mit Priorität 9999 und liefert `false`.
- Dadurch wird nur die automatische sichtbare HD-001-Footer-Ausgabe abgeschaltet.
- HD-001 `footer_entries()` und Shortcode/API bleiben unverändert verfügbar.
- keine Kategorie-, Zielbaum-, SEO-, Finder-, Glossar- oder Datenbankänderung.
- dunkler HD-003-Footer bleibt der einzige sichtbare Footer.

Exakte Vorher-/Nachher-Simulation mit aktuellem HD-001 1.14.16 und realem V7.1-Profil:
- Negativkontrolle reproduziert `.apkw-auto-footer`: PASS;
- weißer Hintergrund + obere Linie: PASS;
- exakt `Zeit, Budget & Platz`: PASS;
- exakt `Anbieter`: PASS;
- exakt zwei Autofooter-Links: PASS;
- HD-001-Hook `wp_footer`, Priorität 50: PASS;
- HD-003-Filter `apkw_auto_footer_enabled`, Priorität 9999: PASS;
- nach Filter: `.apkw-auto-footer` 0 Treffer: PASS;
- `Zeit, Budget & Platz` 0 Treffer: PASS;
- `Anbieter`-Autofooterlink 0 Treffer: PASS;
- dunkler HD-003-Footer exakt einmal: PASS;
- Hobbyfinder-Footerlink entfernt: PASS;
- `© 2026 Hobby Depot` vorhanden: PASS.

Weitere QA:
- Glossar 1.0.13 wählt mit alter V150699 und neuer V150709 exakt V150709: PASS;
- PHP-Lint: 138/138 PASS;
- falsche 1.50.708-Theme-Suppressoren nicht enthalten: PASS;
- ZIP CRC/Fresh-Unpack: PASS.

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.709_HD001_AUTOFOOTER_ROOTFIX_VERIFIED.zip`

SHA-256:
`32ed94f5e45b5ae59064b19208ca90d32a74a2e33a8f15c3007bebd7228bf6cb`

Größe:
58,829,084 Bytes.
## ERSTER OFFENER BLOCKER

**Nur noch der echte Live-Readback von 1.50.709.**

## EXAKT EINE NEXT ACTION

**HD-003 1.50.709 über die aktuell aktive Designplugin-Version installieren und prüfen: weiße Leiste `Zeit, Budget & Platz / Anbieter` muss weg sein; dunkler Footer muss mit größerer Schrift, ohne Hobbyfinder und mit Copyright stehen bleiben.**
