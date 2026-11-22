# Pferdeatelier Design-Büro – aktueller Stand

Stand: 22.11.2026

## Verbindliche Basis

Aktuelles Designplugin: **1.50.632 – LIVE PASS**

Archivpfad:
`/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.632_LIVE_PASS.zip`

Prüfnachweis:
`/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.632_LIVE_PASS_PRUEFNACHWEIS.json`

## Abgenommener Zustand

- 1.50.628: konsolidierte Basis aus Template-Kit + Breadcrumb-Helfer + Canonical Table Contract.
- 1.50.629: Journal-Unterseiten – Überschrift ins Hero, Banner nach oben, Paginierung oben/unten.
- 1.50.630: Journal – Banner auf Inhaltsbreite, Amazon-Kachel in Kartenraster, Paginierungsdesign, Ziel 8 Beiträge + 1 Amazon-Kachel.
- 1.50.631: Paginierungsdesign vom Nutzer PASS bestätigt; Beitragszahl weiterhin fehlerhaft.
- 1.50.632: harte 8-Beiträge-Begrenzung mit synchroner Seitenlogik; Nutzer hat anschließend **PASS** bestätigt.
- Journal-Design insgesamt: **PASS**.
- Glossar und Pferderassen waren von diesem Journal-Umbau ausgeschlossen.
- Hero, Banner, Amazon-Kachel und Paginierung sind im aktuellen Stand visuell abgenommen.
- Aktuelle Journal-Grenze: maximal **8 echte Beiträge pro Seite**; Amazon-Kachel zusätzlich im Raster.

## Regel für weitere Änderungen

Alle weiteren Designänderungen bauen ausschließlich auf **1.50.632 LIVE PASS** auf.
Keine Rückkehr zu 1.50.631 oder älter, außer ausdrücklich als Fallback.
Performance-Arbeiten bleiben getrennt vom Design.

## Live

1.50.632 ist nach Nutzerprüfung für Live freigegeben.
Nach Live-Installation dient 1.50.632 als gemeinsame Basis für Live und Test.


## 2026-11-22 – 1.50.633 Einzelbeitrag rechte Begleitspalte – NUR TEST

- Ausgangsbasis: **1.50.632 LIVE PASS**. Diese bleibt der letzte abgenommene Live-Fallback.
- Scope: ausschließlich klassische WordPress-Einzelbeiträge (`post`).
- Desktop + Tablet ab 768 px: rechte Begleitspalte nach Hab-&-Bewahr-Vorbild.
- Mobil unter 768 px: keine aktive Sidebar; alle Originalelemente bleiben bzw. werden beim Verkleinern an exakt ihre ursprünglichen DOM-Stellen zurückgesetzt.
- Rechte Spalte nutzt ausschließlich bereits gerenderte Originalelemente:
  - vorhandene Amazon-Anzeige wird bevorzugt; falls im Artikel keine vorhandene Amazon-Anzeige existiert, wird die vorhandene Artikelanzeige verwendet,
  - vorhandener Produktblock mit bis zu drei durch die Affiliate-Zentrale bereits geprüften Produkten,
  - Astras vorhandene gleichkategorische Empfehlung; rechts wird genau ein weiterführender Beitrag gezeigt.
- Keine neue Affiliate-URL, keine neue Produktauswahl, keine neue Empfehlungsquery, kein neuer Shortcode, keine Änderung am Affiliate-Router.
- Kein Sticky-Verhalten.
- Diff gegen 1.50.632: 507 gemeinsame Dateien, 506 byteidentisch; nur `pferde-template-kit.php` geändert; keine Datei hinzugefügt oder entfernt.
- PHP 9/9 PASS, JavaScript-Syntax PASS, ZIP-CRC PASS.
- Artefakt: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.633_EINZELBEITRAG_SIDEBAR_NUR_TEST.zip`
- Prüfnachweis: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.633_PRUEFNACHWEIS.json`
- Status: **NUR TEST**. Visuelle Abnahme Desktop/Tablet steht aus; 1.50.632 bleibt bis dahin LIVE PASS.


## 2026-11-22 – 1.50.633 FAIL / 1.50.634 Reparatur – NUR TEST

- 1.50.633 wurde vom Nutzer sichtbar als **FAIL** bewertet: Einzelbeitrag deutlich zerschossen, linke Inhaltsspalte zu schmal, Seitenachse im weiteren Verlauf gebrochen.
- Nachgewiesene Ursache: 1.50.633 verschob `entry-header` und `entry-content` aus Astras Original-DOM in einen neu erzeugten Layoutcontainer.
- 1.50.633 ist damit verworfen und darf nicht Live gehen.
- 1.50.634 wurde **direkt aus 1.50.632 LIVE PASS** gebaut, nicht aus 1.50.633.
- Reparaturprinzip 1.50.634:
  - Artikel, Überschrift, Hero und kompletter Fließtext bleiben vollständig in Astras Originalstruktur.
  - Rechte Spalte wird nur als Geschwister von `#primary` in der bestehenden `.ast-container`-Struktur ergänzt.
  - Vorhandene Anzeige und vorhandener Produktblock werden nur geklont; die Originale bleiben im DOM und werden nur Desktop/Tablet verborgen.
  - Weiterführender Beitrag verwendet ausschließlich den bereits von Astra ermittelten gleichkategorischen Link; keine neue Query.
  - Kein neuer Affiliate-Shortcode, keine neue Produktlogik, keine URL-Neuerzeugung, kein Sticky.
  - Mobil unter 768 px erzeugt keinen aktiven Sidebar-Zustand und bleibt beim Originalstand.
- Diff zu 1.50.632: 507 gemeinsame Dateien, 506 byteidentisch; nur `pferde-template-kit.php` geändert.
- PHP 9/9 PASS, JS-Syntax PASS, ZIP-CRC PASS, statischer Sicherheitsvertrag PASS.
- Artefakt: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.634_EINZELBEITRAG_SIDEBAR_REPARATUR_NUR_TEST.zip`
- Prüfnachweis: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.634_PRUEFNACHWEIS.json`
- **1.50.632 bleibt weiterhin der letzte LIVE-PASS-Fallback.**


## 2026-11-22 – 1.50.635 Einzelbeitrag Sidebar Korrektur – NUR TEST

- 1.50.634 sichtbar noch nicht PASS: beim Verkleinern des Browserfensters blieb die Sidebar zu lange aktiv; Amazon-Box doppelte Werbekennzeichnung/innerer Rahmen; Text/CTA brachen schlecht; Produktkacheln und weiterführender Beitrag fehlten auf dem Testartikel.
- 1.50.635 baut auf der sicheren Geschwister-Sidebar-Architektur von 1.50.634 auf; 1.50.632 bleibt letzter LIVE PASS.
- Responsive-Fix: Sidebar nur ab 1000px und nur bei realer Astra-Containerbreite >= 940px. Darunter sofort Original-Einzelbeitrag ohne Sidebar.
- Amazon/Artikelanzeige: genau ein Ocker-Kicker `WERBUNG`; interne `Anzeige`- und Disclosure-Zeilen im Sidebar-Klon ausgeblendet; keine inneren Rahmen/Boxen; Text darf vollständig umbrechen; CTA bleibt einzeilig.
- Produkte: bis zu drei Karten aus dem vorhandenen gespeicherten Artikelplan `ppar_article_delivery_plan_v1`. Zuerst finale `campaign_post_ids`; falls weniger als drei vorhanden sind, nur bereits im selben Plan mit `overall=pass` geprüfte Kandidaten. Kein neuer Produktsuchlauf. Kampagnendaten werden nur dargestellt, wenn Produkt, aktiv, Programm aktiv, Bild/URL/Titel vorhanden und nicht als unavailable/ended markiert.
- Produktkarten zeigen Provider (eBay/Amazon/idealo), Bild, Titel, optional Preis und eine einzeilige CTA. Vorhandene Affiliate-URL wird unverändert verwendet.
- Weiterführender Beitrag: Priorität auf den im Artikel explizit gesetzten K0-Linkrollen `semantic_related` bzw. `further_information`; daraus wird genau ein veröffentlichter Beitrag der verknüpften Kategorie gewählt. Nur wenn dort nichts gefunden wird, gleiche aktuelle Kategorie. Keine freie Themen-/Keyword-Empfehlungslogik.
- Originale Werbe-/Produkt-/Astra-Related-Blöcke werden nur bei aktiver Sidebar verborgen; unter 1000px wieder unverändert sichtbar.
- Kein Sticky, keine Änderung am Affiliate-Router.
- Diff gegen 1.50.634: 507 gemeinsame Dateien, 506 byteidentisch; nur `pferde-template-kit.php` geändert; keine Dateien hinzugefügt/gelöscht.
- PHP 9/9 PASS, JavaScript-Syntax PASS, ZIP-CRC PASS, statischer Responsive-/Produktplan-Vertrag PASS.
- Artefakt: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.635_EINZELBEITRAG_SIDEBAR_KORREKTUR_NUR_TEST.zip`
- Prüfnachweis: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.635_PRUEFNACHWEIS.json`
- Status: **NUR TEST**. 1.50.632 bleibt bis Nutzerabnahme der sichere Live-Fallback.


## 2026-11-22 – 1.50.635 FAIL / 1.50.636 Sichtbarkeitsfix – NUR TEST

- 1.50.635 vom Nutzer als **FAIL** gemeldet: rechte Einzelbeitrags-Sidebar auf der Testseite komplett unsichtbar.
- Ursache im exakten 1.50.635-Code nachgewiesen: `canActivate()` verlangte neben `window.innerWidth >= 1000` zusätzlich eine Breite des **noch unveränderten** Astra-Containers von mindestens 940px. Dieser Container ist vor Aktivierung weiterhin auf die normale Lesebreite begrenzt; dadurch konnte die Sidebar trotz ausreichend breitem Browser nie aktiviert werden.
- Beweis im Vertragstest: bei 1200px Browserbreite und 760px Pre-Layout-Astra-Container war 1.50.635 = FALSE; 1.50.636 = TRUE. Bei 1024px = TRUE, bei 999px = FALSE.
- 1.50.636 entfernt ausschließlich diese falsche Vorab-Containerbreiten-Sperre. Aktivierung jetzt: Browserbreite >=1000px + vorhandener Astra-Zielcontainer.
- Restliche Sidebar-Korrekturen aus 1.50.635 bleiben erhalten: genau ein Ocker-`WERBUNG`, keine zweite Anzeige-/Disclosure-Zeile, keine inneren Rahmen, Textumbruch ohne Abschneiden, einzeilige CTA, bis zu drei Produktkarten aus vorhandenem Artikelplan, ein weiterführender Beitrag aus vorhandener K0-Verknüpfung.
- Für den Testartikel `Wie kann ich Müsli für mein Pferd selbst machen?` im Export belegt: Artikelplan `ready`, ausgewähltes Produkt 16615, weitere PASS-Produkte u.a. 16613 und 17057; `semantic_related` verweist auf `mueslis-fuer-pferde-beratung`, `further_information` auf `mueslis-fuer-pferde-faq`.
- Diff gegen 1.50.635: 507 gemeinsame Dateien, 506 byteidentisch; nur `pferde-template-kit.php` geändert; keine Dateien hinzugefügt/gelöscht.
- PHP 9/9 PASS, JavaScript-Syntax PASS, ZIP-CRC PASS.
- Artefakt: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.636_EINZELBEITRAG_SIDEBAR_SICHTBARKEITSFIX_NUR_TEST.zip`
- Prüfnachweis: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.636_PRUEFNACHWEIS.json`
- Status: **NUR TEST**. 1.50.632 bleibt letzter LIVE PASS.


## 2026-11-22 – 1.50.636 FAIL / 1.50.637 harter Sidebar-Fix – NUR TEST

- 1.50.636 vom Nutzer sichtbar als **FAIL** bewertet: doppelte Werbekennzeichnung, abgeschnittener Text, Amazon-CTA weiterhin umgebrochen, kein weiterführender Artikel, keine Produktkarten.
- Ursachen jetzt getrennt nachgewiesen:
  1. Werbekachel wurde als kompletter vorhandener DOM-Block geklont; dadurch kamen interne Werbe-/Layout-Chrome und alte Breitenregeln mit.
  2. Produktkarten wurden im Designplugin aus Rohmetadaten nachgebaut statt den zentralen Affiliate-Router rendern zu lassen.
  3. Weiterführungsresolver erkannte nur `/category/...`; echte K0-Verweise im Testartikel zeigen aber auf normale Portalpfade wie `/fuetterung/fuetterung-raufutter/heunetze/`.
- 1.50.637 repariert diese drei Ursachen:
  - Amazon-Sidebar-Kachel wird nicht mehr geklont. Verwendet wird nur der vorhandene echte Amazon-Link; Darstellung ist neu und sauber: genau ein Ocker-`WERBUNG`, Text `Passende Angebote zum Thema entdecken`, CTA `Bei Amazon ansehen` ausdrücklich einzeilig, kein innerer Rahmen.
  - Produktkarten kommen über die bestehenden Shortcodes `pp_affiliate_slot` für `category_product_1`, `category_product_2`, `category_product_3`. Auswahl, Provider-Mix und Tracking bleiben damit vollständig im Affiliate-Router. Das Designplugin extrahiert nur die final gerenderten Links/Bilder/Titel für die kompakte Sidebar-Darstellung.
  - Weiterführungsresolver unterstützt jetzt Kategoriepfade, direkte Beitragslinks und normale Portal-Seitenpfade. Für einen Portalpfad wird der bestehende Seiten-Slug deterministisch gegen die vorhandenen redaktionellen Kategorie-Suffixe `beratung, vergleich, anwendung, faq, pflege, kosten, lagerung` aufgelöst; daraus genau ein anderer veröffentlichter Beitrag.
  - Originale Inline-Werbung, Produktblock und Astra-Related werden nur bei aktiver Sidebar verborgen und unter 1000px wieder unverändert eingeblendet.
  - Der Artikel selbst bleibt vollständig in Astras Original-DOM; Sidebar bleibt Geschwister von `#primary`.
- Beleg Heunetz-Testartikel: Artikelplan ready; ausgewähltes Produkt 16454; PASS-Produkte u.a. 16458, 16456, 16460; K0-Verweise auf `/fuetterung/fuetterung-raufutter/` und `/fuetterung/fuetterung-raufutter/heunetze/`.
- Diff gegen 1.50.636: 507 gemeinsame Dateien, 506 byteidentisch; nur `pferde-template-kit.php` geändert.
- PHP 9/9 PASS, JavaScript-Syntax PASS, ZIP-CRC PASS, statischer Vertragscheck PASS.
- Lokaler Chromium-Visualtest konnte wegen der Container-/DBus-Umgebung nicht zuverlässig gestartet werden; deshalb ausdrücklich **kein behaupteter visueller Browser-PASS**.
- Artefakt: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.637_EINZELBEITRAG_SIDEBAR_HARTFIX_NUR_TEST.zip`
- Prüfnachweis: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.637_PRUEFNACHWEIS.json`
- Status: **NUR TEST**. Letzter LIVE PASS bleibt 1.50.632.


## 2026-11-22 – 1.50.637 nicht abgenommen / 1.50.638 responsive Sidebar – NUR TEST

- 1.50.637 sichtbar nur teilweise verbessert, aber nicht PASS: Amazon-Bild fehlte; Produktkarten zeigten durch fehlerhafte Auswertung nur Amazon statt reale Anbieter; responsive Umschaltung/Mobil unvollständig; kein belastbarer Weiterführungsblock.
- 1.50.638 korrigiert ausschließlich diese Einzelbeitrags-Sidebar.
- Amazon: vorhandenes reales Amazon-Bild wird aus dem bestehenden Quellblock übernommen; alter Werbe-Chrome wird nicht geklont. Genau ein Ocker-`WERBUNG`; CTA `Bei Amazon ansehen` bleibt einzeilig.
- Produkte: zentraler Artikelplan hat Vorrang; danach die drei vorhandenen Router-Slots `category_product_1..3` mit `intent=portal_context`. Pro Produkt werden alle tatsächlich vorhandenen eBay-/idealo-/Amazon-Angebotslinks separat als Buttons dargestellt. Auswahlreihenfolge versucht sichtbaren Provider-Mix eBay → idealo → Amazon, ohne Anbieter zu erfinden.
- Heunetz-Evidenz aus Export: aktive eBay-Heunetz-Kampagnen und aktive idealo-Heunetz-Kampagnen sind vorhanden; Artikelplan für `Wie hoch muss ein Heunetz hängen?` ist ready.
- Weiterführung: echter anderer Post bleibt erste Wahl. Wenn für das konkrete Thema noch kein zweiter Post existiert, wird der bereits redaktionell im Artikel gesetzte Portalpfad (z. B. Heunetze/Raufutter) als sichere Weiterführung verwendet; keine erfundene Empfehlung.
- Responsive: Sidebar weiterhin nur ab 1000px. Unter 1000px Originalquellen werden vollständig freigegeben. Falls im Original mobil kein Produkt-/Related-Block existiert, werden nur diese fehlenden Empfehlungen unter dem Artikel ergänzt; der Artikel selbst bleibt einspaltig und unangetastet.
- Diff gegen 1.50.637: 507 gemeinsame Dateien, 506 byteidentisch; nur `pferde-template-kit.php` geändert; keine Datei hinzugefügt/gelöscht.
- PHP 9/9 PASS, JavaScript-Syntax PASS, ZIP-CRC PASS, statischer Vertrag PASS.
- Chromium-Visualtest in Container weiterhin technisch nicht zuverlässig startbar; daher kein behaupteter visueller Browser-PASS.
- Artefakt: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.638_EINZELBEITRAG_SIDEBAR_RESPONSIVE_NUR_TEST.zip`
- Prüfnachweis: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.638_PRUEFNACHWEIS.json`
- Status: **NUR TEST**. Letzter LIVE PASS bleibt 1.50.632.


## 2026-11-22 – 1.50.639 Einzelbeitrag: reine Darstellung vorhandener Ausgaben – NUR TEST

- 1.50.638 nicht abgenommen: Responsive weiterhin unzureichend; Nutzer fordert klare Trennung zwischen Design und Affiliate-Zuordnungs-/Verteilungslogik.
- Verbindliche Grenze ab 1.50.639:
  - Designplugin darf vorhandene Artikel-Ausgaben nur darstellen/verschieben/klonen.
  - Keine neuen Produkt-Slots, keine neue Produktauswahl, keine Provider-Mischung, keine Rohmeta-Auswertung.
  - Affiliate-Zentrale bleibt allein verantwortlich für Produktanzahl, Anbieter, Zuordnung, Verteilung und Tracking.
  - Weiterführende Ziele muessen echte Einzelbeitraege sein; keine Kategorien oder Portalpfade als Ersatz.
- Produktdarstellung Desktop/grosse Tablets: Es wird ausschließlich der bereits fertig gerenderte `.ppar-article-product-block` des Artikels geklont. Das Original wird nur solange die Sidebar aktiv ist verborgen.
- Produktdarstellung Mobil/schmal: Kein Ersatzblock mehr. Der originale `.ppar-article-product-block` bleibt unverändert sichtbar.
- Related Desktop/grosse Tablets: ausschließlich Astras bereits gerenderter echter Related-Post; keine eigene Query.
- Related Mobil/schmal: Astras Originalausgabe bleibt sichtbar und wird nur optisch als Bildkarte dargestellt. Der frühere Filter, der das Featured-Image-Markup entfernte, ist nicht mehr aktiv.
- Amazon-Sidebar: vorhandener echter Amazon-Link/Bild werden wiederverwendet; Text auf `Passende Angebote entdecken` gekürzt; sichtbare Amazon-Wortmarke + Smile; CTA `Bei Amazon ansehen` einzeilig.
- Responsive: Sidebar-Aktivierung nur bei effektiver Breite >=1000px und Contentbreite >=960px. Effektive Breite = Minimum aus innerWidth, documentElement.clientWidth, visualViewport.width und outerWidth. Dadurch wird auch ein schmal gezogenes Browserfenster trotz Zoom korrekt erkannt.
- Sicherheitsnachweis aktiver Sidebar-Pfad: 0x `category_product_1/2/3`, 0x `do_shortcode`, 0x `WP_Query`, 0x `get_posts`, 0x `url_to_postid`, 0x `get_term_by`.
- Diff gegen 1.50.638: 507 gemeinsame Dateien, 506 byteidentisch; nur `pferde-template-kit.php` geändert.
- PHP 9/9 PASS, JavaScript-Syntax PASS, ZIP-CRC PASS, statischer Vertrag PASS.
- Artefakt: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.639_EINZELBEITRAG_REINES_DESIGN_NUR_TEST.zip`
- Prüfnachweis: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.639_PRUEFNACHWEIS.json`
- Status: **NUR TEST**. Letzter LIVE PASS bleibt 1.50.632.


## 2026-11-22 – 1.50.639 FAIL / Sidebar-Umbau gestoppt

- Nutzerprüfung 1.50.639: **FAIL**.
- Sichtbare Fehler: Sidebar reagiert beim Verkleinern nicht sauber; Produkt-/Weiterführungsblöcke verschwinden erneut bzw. sind nicht stabil sichtbar.
- Entscheidung: weiterer Sidebar-Umbau **gestoppt**. Keine weitere Reparaturversion auf Basis 1.50.633–1.50.639.
- Verbindlicher Rücksetzpunkt: **1.50.632 LIVE PASS**.
- 1.50.632 bleibt der letzte vollständig abgenommene Designstand.
- Die Versionen 1.50.633 bis 1.50.639 gelten für die Einzelbeitrags-Sidebar als verworfene Testreihe und dürfen nicht Live eingesetzt werden.


## 2026-11-22 – 1.50.640 Einzelbeitrag Sidebar – sauberer Neuansatz aus 1.50.632 – NUR TEST

- Ausgangsbasis: **1.50.632 LIVE PASS**. Die verworfene Testreihe 1.50.633–1.50.639 wird nicht weiterverwendet.
- Ziel: Desktop/große Tablets rechte Begleitspalte; schmale Ansichten/Mobil bleiben im originalen einspaltigen Artikel.
- Harte Breitenregel: Sidebar erst ab 1180px. Hauptartikel bleibt 760px breit; Sidebar 280px; Abstand 32px. Der Artikel wird nicht zusammengedrückt.
- Affiliate-Sicherheit:
  - keine `category_product_1/2/3`-Aufrufe,
  - kein `do_shortcode`,
  - keine neue Produkt-/Provider-/Kategorieauswahl,
  - keine `WP_Query`, `get_posts`, `url_to_postid` oder `get_term_by` im Sidebar-Code.
- Produkte: Desktop/große Tablets klonen ausschließlich den bereits fertig gerenderten `.ppar-article-product-block`. Auswahl, Anzahl, Anbieter und Tracking bleiben damit vollständig in der Affiliate-Zentrale.
- Mobile/schmal: Original-`.ppar-article-product-block` bleibt sichtbar. Kein Ersatz- oder Zusatzproduktblock.
- Atomarer Sichtbarkeitsschutz: Originalanzeige, Originalproduktblock und Original-Related-Block werden nur dann in breiter Ansicht verborgen, wenn die entsprechende Kopie rechts erfolgreich erzeugt wurde. Unter 1180px zeigt CSS die Originale sofort wieder.
- Weiterführende Beiträge: ausschließlich Astras bereits vorhandene echte Related-Post-Ausgabe; keine neue Related-Query und kein Kategorie-/Portalpfad-Fallback. Der erste bereits ausgewählte Beitrag wird rechts gezeigt.
- Mobile Related: Astras Originalausgabe bleibt sichtbar. Der bisherige Designfilter, der Featured-Images entfernt hat, gibt das vorhandene Astra-Bild wieder frei; Related wird als Beitragskarte mit Bild + Titel dargestellt.
- Amazon: vorhandener echter Amazon-Link wird wiederverwendet; vorhandenes Quellbild wird übernommen, wenn vorhanden. Zusätzlich sichtbare Amazon-Wortmarke mit Smile, Copy `Passende Angebote entdecken`, CTA `Bei Amazon ansehen` einzeilig.
- Diff gegen 1.50.632: 507 gemeinsame Dateien, 506 byteidentisch; nur `pferde-template-kit.php` geändert.
- PHP 9/9 PASS, JavaScript-Syntax PASS, ZIP-CRC PASS.
- Lokaler Chromium-Visualtest weiterhin wegen Container/DBus nicht zuverlässig ausführbar; deshalb kein behaupteter visueller PASS.
- Artefakt: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.640_EINZELBEITRAG_SIDEBAR_SICHER_NUR_TEST.zip`
- Prüfnachweis: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.640_PRUEFNACHWEIS.json`
- Status: **NUR TEST**. Letzter LIVE PASS bleibt 1.50.632.


## 2026-11-22 – 1.50.641: Produktanzeige aus 1.50.638 + Responsive PASS aus 1.50.640

- Nutzerhinweis bestätigt: 1.50.638 zeigte Produkte/Sidebar bereits sichtbar; Fehler entstand erst durch die Überkorrektur in 1.50.639/1.50.640, die zusätzliche Produktausgabe entfernte und nur noch auf bereits im HTML vorhandene Originalblöcke wartete.
- 1.50.641 kombiniert deshalb bewusst nur zwei bereits getestete Teile:
  1. Responsive-Verhalten aus 1.50.640 bleibt erhalten: Sidebar erst ab 1180px, Hauptartikel 760px, Sidebar 280px, Gap 32px, reale Fensterbreite inkl. outerWidth berücksichtigt.
  2. Produktdarstellung aus 1.50.638 wird wiederhergestellt: bestehende zentrale Slots category_product_1..3 werden nur aufgerufen und deren vorhandene Ausgabe dargestellt.
- Sicherheitsgrenze: Das Designplugin schreibt oder ändert keine Affiliate-Regel, keine Kategoriezuordnung, keine Produktzuordnung, keine Provider-/Ranking-/Verteilungsregel und keine Trackinglogik. Es nutzt nur die vorhandenen zentralen Slot-Ausgaben.
- Mobil: Wenn kein vorhandener Produktblock im Artikel-HTML steht, werden dieselben zentralen Produkt-Ausgaben unter dem Artikel sichtbar gemacht; kein anderer Auswahlweg.
- Weiterführend: ausschließlich echte veröffentlichte Posts. Kategorie-Links aus dem Artikel dienen nur als Quelle zum Auffinden eines passenden veröffentlichten Beitrags; das sichtbare Ziel ist immer ein Beitrag, niemals eine Kategorie oder Seite.
- Amazon: sichtbare Wortmarke + Bild (wenn vorhanden), Text `Passende Angebote entdecken`, CTA einzeilig.
- Diff 1.50.640 -> 1.50.641: 507 Dateien / 507 Dateien; 506 byteidentisch; nur `affiliate-portal-template-kit/pferde-template-kit.php` geändert; keine Datei hinzugefügt/gelöscht.
- PHP 9/9 PASS, Sidebar-JavaScript-Syntax PASS, ZIP-CRC PASS.
- Artefakt: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.641_SIDEBAR_PRODUKTE_RESTORE_RESPONSIVE_PASS_NUR_TEST.zip`
- Prüfnachweis: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.641_PRUEFNACHWEIS.json`
- Status: **NUR TEST**. Responsive 1.50.640 wurde vom Nutzer bereits als PASS bestätigt; Produkt/Weiterlesen in 1.50.641 noch visuell abzunehmen.


## 2026-11-22 – 1.50.642 Weiterführende Beiträge – NUR TEST

- Nutzerprüfung 1.50.641: **fast PASS**. Responsive PASS, Amazon/Produkte sichtbar; einzig weiterführende Beiträge fehlen.
- 1.50.642 ändert ausschließlich den Weiterführungsbereich. Produktdarstellung, Amazon-Karte und Responsive-Aktivierung sind gegenüber 1.50.641 unverändert.
- Ursache des leeren Blocks: In der WordPress-Exportdatei enthält z. B. `mueslis-fuer-pferde-faq` nur den aktuellen Beitrag; ebenso `heunetze-faq`. Eine ausschließlich auf die Blattkategorie begrenzte Related-Suche kann dort keinen zweiten Beitrag liefern.
- Neue Reihenfolge für maximal zwei sichtbare Empfehlungen:
  1. bereits direkt als echter veröffentlichter Post verlinkter Beitrag,
  2. anderer veröffentlichter Post aus bereits verlinkter Related-/FAQ-Kategorie bzw. aktueller Beitragskategorie,
  3. nur wenn dort nichts vorhanden ist: andere veröffentlichte Posts aus demselben bereits im Artikel gesetzten Hauptthema (z. B. /fuetterung/), gewichtet gegen Titel/Inhalt des aktuellen Artikels.
- Sichtbares Ziel ist immer ein veröffentlichter WordPress-Beitrag; Kategorien und Seiten werden niemals als Weiterführungsziel ausgegeben.
- Maximal 2 Karten, jeweils Beitragsbild + Titel. Desktop/große Tablets rechts unter den Produkten; schmale/mobile Ansicht unter dem Artikel, falls kein Astra-Related-Block vorhanden ist.
- Sicherheitsgrenze: keine Änderung an Affiliate-Regeln, Produktzuordnung, Provider-/Ranking-/Verteilung, Tracking oder Kategoriezuordnungen.
- Diff 1.50.641 -> 1.50.642: 507 Dateien / 507 Dateien; 506 byteidentisch; nur `affiliate-portal-template-kit/pferde-template-kit.php` geändert; keine Datei hinzugefügt/gelöscht.
- Unverändert nach Hash-/Blockvergleich: Responsive-`viewportWidth/canActivate`, `buildProducts`, `buildAd`.
- PHP 9/9 PASS, Sidebar-JavaScript-Syntax PASS, ZIP-CRC PASS.
- Artefakt: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.642_WEITERFUEHRENDE_BEITRAEGE_NUR_TEST.zip`
- Prüfnachweis: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.642_PRUEFNACHWEIS.json`
- Status: **NUR TEST**. 1.50.641 bleibt der zuletzt sichtbar nahezu abgenommene Teststand; 1.50.632 bleibt letzter vollständiger LIVE PASS.
