# HBD-DESIGN – Nachgeholtes Fehlerprotokoll Bildzuordnung / Ebene 2 (19.10.2026)

## HBD-DES-20261022-01 – R1-Hero zu dunkel statt heller Benchmark
**Fehler (Nutzer-Live-Screenshot 21.10., 17:42):** Einbruch & Diebstahl ist links dunkelgrau/schwarz. Verbindliche richtige Vorlage: HELLES „Heizung & Temperatur“-Panorama mit H1 und Claim IM Bild.
**Ursache an 0.1.62 physisch belegt:** `includes/world-layout.php::hbdp_world_hero_tone()` ordnet Einbruch/Wasser/Versicherung weiterhin `dark` zu, gekoppelt an schwarzen CSS-Verlauf.
**Korrektur 0.1.63 lokal:** Alle sieben R1 `light`; vorhandene Bilddateien und Kategorieknoten byteidentisch. Physisches ZIP SHA256 `934ff35a16d89ee59f21a0a43564394ffd1b0cbdef2e9ba5f3b4eb6dd45c3635`.
**Test/Status:** PHP-Lint/ZIP, gezielter Quellcodebeleg; **LOCAL CLOSED / LIVE OFFEN**. Kein neuer WP-Screenshot nach 0.1.63.

## HBD-DES-20261022-02 – R3 mit separatem Foto statt R2-Panorama
**Fehler (Nutzer-Live-Screenshot):** Brunnenpumpe mit großer H1 über abgesetztem Foto; R2 „Heizung & Temperatur“ ist korrekt und soll NICHT umgestaltet werden.
**Ursache 0.1.62 belegt:** Der `templates/site.php`-Defaultzweig rendert R3 als generischen `hbdp-hub` mit eigenem `hbdp-focus-destination-photo`, während R2 den originalen `hbdp-area-demo-hero`-Renderer hat.
**Korrektur 0.1.63 lokal:** Zusätzlicher `includes/r3-topic-hero.php` und enger Dispatcher nur für R3 `page` mit R2-Parent; R3 verwendet vorhandenes konkretes Bild und die R2-Panorama-Markupklasse mit H1+Claim im Foto, Beitragskategorien werden mit Icons gezeigt.
**Test/Status:** PHP-Mock Brunnenpumpe und Hausratversicherung 2/2 PASS; Chromium 390/1024/1440px je R3 = 6/6 PASS, 230/260px, Cover, kein horizontaler Überlauf. **LOCAL CLOSED / LIVE OFFEN**. Vollständige WordPress-R1/R2/R3-Regression nicht belegt.

## HBD-DES-20261022-03 – Blaue Altleiste Magazin/Dienstleister auf R3 trotz alter Fixes
**Fehler (Nutzer-Live-Screenshot):** Mitten in den Versicherungskategorien noch blaue Zeile „Magazin Dienstleister“, obwohl in älteren Versionen wiederholt als behoben gemeldet.
**Nachgewiesene Ursache der Fixlücke:** `assets/area-shortcuts-clean.js` war nur auf Home/R1/R2 geladen und prüfte ausschließlich alte Klassennamen; der R3-`hbdp-hub` wurde nicht bedient. **Die ursprüngliche WordPress-Komponente, welche die Leiste injiziert, wurde im tatsächlichen Live-DOM bislang nicht nachgewiesen** – nicht behaupten, sie entfernt zu haben.
**Korrektur 0.1.63 lokal:** Skript auch auf R3 laden, neue `.hbdp-r3-page`-Wache; nur Container aus EXAKT zwei Altlinks entfernen; zulässige individuelle Magazinlinks und reguläre Inhalte geschützt.
**Tests/Status:** synthetisch eingefügte Zweilink-Leiste in Chromium entfernt, legitimer Magazinlink bleibt erhalten (6 Browserfälle). **LOCAL TEILPASS / LIVE OFFEN**; DOM-Nachweis und tatsächliche Live-Wiederholungsfreiheit erst nach Installation möglich.

## HBD-DES-20261022-04 – Falsch als abgeschlossen gemeldete globale Hero-Freigabe 0.1.62
**Fehler:** Lokaler 0.1.62-R2-Versicherungs-Simulationstest wurde als Lösung für „alle Heros und Magazin/Dienstleister“ dargestellt; reale Nutzer-Screenshots widerlegten die globale Aussage. R1- und R3-Routen waren nicht gleichwertig getestet.
**Korrektur/Warum:** 0.1.63 reproduziert getrennt alte R3 und Versicherungs-R3, prüft eine positive/negative DOM-Leiste und gleiche R2-CSS-Formatierung; ein WordPress-Test der fünf realen repräsentativen Seiten bleibt zwingend. Bereits vorhandene R2-Benchmark unverändert schützen. Kein neues Kategorieplugin, keine neue Theme-Architektur.
**Status:** Testlücke dokumentiert; **LOCAL TEILPASS / LIVE OFFEN**.

**Aktueller Status und GENAU EINE NEXT ACTION ausschließlich in `DESIGN/CURRENT_STATE.md`. Fehlerquelle ist nur Chronik, niemals Current.**

## HB-DES-20261020-INS-01 – 7. Welt bricht wegen festem 6-Spalten-Desktop-CSS um
**Realbeleg:** Nutzer-Screenshot 20.10.2026 18:54, Desktop-Menü mit 6 alten Welten oben, „Versicherungen“ in eigener zweiter Zeile und aufgeklapptem 5-Bereiche-Menü darunter.
**Quellcodebeleg:** gespeicherte originale Designplugin-ZIP 0.1.57 (explizit NICHT installierter Bilder-WIP): `templates/site.php` erzeugt Welt-Navigation per dynamischer Weltliste, `hbdp_main_navigation` rendert Megamenü bis 5 Spalten und zeigt 4 direkte R3 pro R2 + „Alle Themen“ beim Überlauf, aber `assets/style.css` erzwingt Desktop `.hbdp-mainnav{grid-template-columns:repeat(6,minmax(0,1fr))}`. Die sechs Spalten sind kein inhaltliches Sechs-Welten-Limit.
**Korrekturgrenze:** Im tatsächlich installierten bestehenden DESIGNplugin Desktop-Header mit exakt 7 Spalten/geeigneter Schriftbreite reparieren; ursprünglichen Mobilregeln, fünf Megamenüspalten und Hub-Klickpfade beibehalten. Nicht durchs Kategorieplugin CSS überschreiben, kein Zweitplugin, kein blindes Installieren des unfertigen Design-0.1.57-Bilderpakets.
**Status:** Ursache am archivierten Quellstand + Screenshot belegt, aktuelle physische Designplugin-Version und WP-Frontend-Regression nach Korrektur OFFEN.

**Rolle dieses Dokuments:** Fehlergeschichte, Ursachen und Nachweise. **Kein Current**. Aktuelle Version, PASS-Status und genau eine NEXT ACTION ausschließlich aus `DESIGN/CURRENT_STATE.md`.

## HBD-DESIGN-BILD-20261019-01 – Fachlich falsche oder unscharfe Kachelbilder
**Befund:** Mehrere vom Nutzer real gezeigte Ebene-2-Themenbilder thematisch falsch oder unscharf: u. a. `Haus & Wohnung → Tresore` (altes unscharfes Safefoto), `Selbstschutz bei Einbruch` (unpassende Gebäude-/Fahrzeugmotive), `Wertsachen & Schadenfall` (Graffiti statt Schadensdokumentation), `Rauchmelder` (Heizraum-/Wandmelder statt Deckenrauchmelder), weitere fachfremde Bilder. Teilweise wurde ein Ersatzmotiv nur anhand Dateiname oder Stichwort ausgewählt. **Ursache für konkrete alte Fehlzuordnungen:** keywordbasierte/Gruppen-Fallbacks statt eindeutiger Zuordnung zu `Welt::Bereich::Thema`, zusätzlich zu kleiner/schwacher Bildbestand und ein falscher fotografischer Akzeptanztest. Nicht jeder einzelne Fehler hat denselben belegten Grund.
**Korrektur/Beleg:** Originales Plugin 0.1.42 mit 173/265 bereits belegten Themen NICHT gelöscht. Neuere installierbare 0.1.43 ordnet 186/265 eindeutig zu, 79 ohne Foto statt fremdem Fallback; sieben weitere nicht begründbare Tausche/visuelle Dubletten explizit gestoppt. In 0.1.43 `data/area-image-mapping-v1.json` + 19 bestehende Einzel-Foto-Assets; Haupt-PHP nur Versionierung. Foto-Originale nicht generell neu erzeugt.
**Test:** Originalfunktion `hbdp_area_child_photo` frisch lokal 265/265 PASS; alle 186 referenzierten Bilddateien im ZIP; technische Chromium-HTML/CSS-Boxentests 108/108 PASS. Negative Tests: unbekanntes Thema führt zu `''`, wiederholt verwendete identische Szene wird unterdrückt; ZIP mit CRC-Test PASS.
**Status:** **TEILWEISE LOCAL CLOSED / LIVE OFFEN**. Vollständige **redaktionelle** Foto-Eignung aller 186 und 79 fehlende passende Themenbilder sind **OPEN**. Technischer Test = kein Beweis für geeignete Fotomotive.

## HBD-DESIGN-QA-20261019-02 – Falsche „alle Bilder fertig/PASS“-Aussagen und Prüfung falscher Teilmenge
**Befund:** Wiederholte pauschale Freigaben von 0.1.37–0.1.42 trotz Nutzer-Screenshots mit falschen Bildern. Frühe Tests simulierten bei `Haus & Wohnung` drei statt der **sieben** tatsächlich sichtbaren Unterkategorien. Später wurden 265 Unterthemen mit 36 Bereichen mit bereits weitgehend bebilderten Hero-/Bereichsseiten verwechselt. Der zwischenzeitliche Auditstand 82/265 entstand durch **Aussortieren von Zuordnungen** und ist keine Aussage über verschwundene Dateien.
**Korrektur/WARUM:** Strikte Trennung von 6 Welten, 36 Ebene-2-Bereichen und 265 Ebene-3-Themen; erneuter Frischecheck des 0.1.43-ZIPs. 0.1.42 hatte 173 Fotozuordnungen; 0.1.43 186. Die anderen 79 Themen sind **nicht automatisch fehlende Heros**. Kein Pauschallöschen, keine pauschale Neu-Bilderstellung.
**Test:** Aktuelles gesamtes 265er-JSON nach Welt/Bereich/Thema geprüft, 36 unterschiedliche Bereiche, 186 vorhandene Bilddateien; reale WordPress-Kategorien-/Cache-Readbacks und menschliche Einzelmotiv-Freigabe weiterhin nicht vorliegend.
**Status:** Fehlbericht ausdrücklich **NACHGEHOLT**, umfassende Live-Abnahme **OPEN**.

## HBD-DESIGN-DUP-20261019-03 – Unterschiedliche Dateinamen, optisch gleiche Bilder
**Befund:** Bei Technik/Vandalismus mehrfaches Verschieben derselben Motive in andere Kacheln statt eigenständiger passender Fotos; Nutzer-Screenshots belegen erneut gleiche Szenen. Dateinamen allein sind kein Identitätsnachweis.
**Korrektur:** Bildidentität im Bereich über Inhalts-Hash/dHash gegenprüfen; sieben erneute Kandidaten wegen tatsächlicher Dubletten nicht übernehmen; pro Bereich identische Zuordnung beim Rendern unterdrücken.
**Tests:** Laut lokalem 0.1.43-Releaseprotokoll 0 exakte SHA- oder dHash<=3-Dubletten innerhalb der 36 Bereichen. Negative PHP-Laufzeitkontrolle am 19.10.: zweite gleiche `Tresore`-Bildzuweisung im selben Bereich gibt leer zurück.
**Status:** **LOCAL CLOSED / LIVE OFFEN**; keine Garantie für echte WordPress-Liveanzeige ohne Caches.

## HBD-DESIGN-TEXT-20261018-04 – Fließtext als falsche Bildunterschrift
**Befund:** Die redaktionelle Ausgabe kopierte Sätze aus `sections[].detail` als Bildunterschrift; u. a. „Lass die Eignung von Zylinder, Türblatt, Bandseite und Rahmen zusammen prüfen.“. Der Satz ist sprachlich unpassend und vom Nutzer nachgewiesen.
**Korrektur:** Seit 0.1.42 `editorial_photo_titles` und `editorial_captions` mit 72 eigenständigen Paaren, konkreten beanstandeten Satz überarbeitet. 0.1.43 hat dieselbe Renderlogik.
**Test:** 0.1.42-Renderebene lokal geprüft; 0.1.43 gegen 0.1.42 im PHP-Renderer unverändert. **Keine vollständige menschliche Redaktion aller Absätze belegt.**
**Status:** **LOCAL CLOSED / LIVE OFFEN**.

## HBD-DESIGN-UI-20261018-05 – Blaue „Magazin / Dienstleister“-Leiste samt Trennlinie
**Befund:** Wiederholte Live-Screenshots zeigen blau/weiße Altleiste und Rahmen/Trennlinie, trotz gegenteiliger Aussagen aus lokalen Tests.
**Nachgewiesene alte Codeursache:** parallele historische Inline-Linkbereinigung entfernte teils nur innere Links, ließ Border-Container stehen; Startseite hatte Cleaner zunächst gar nicht eingebunden. 0.1.36 und 0.1.38 bereinigten diese in demselben Designplugin lokal.
**Test:** CSS-/DOM-Nachstelltests lokal; **kein aktueller echter Live-WordPress-DOM-Readback**, auch nicht für 0.1.43.
**Status:** **LOCAL CLOSED / LIVE OFFEN**.

## HBD-DESIGN-LAYOUT-20261018-06 – Hero-Crop, Formate, Startseiten- und Fachtextbildrahmen
**Befund:** Vom Nutzer beanstandet: aufgezoomte/unscharfe Heroes, Mobile-Formatabweichungen, randlose/übergroße Fachtextbilder, Startseitenhero-Body-Breiten- und Farbkanten. Wiederholte Screenshots beweisen, dass frühere „PASS“-Behauptungen die echte Darstellung nicht ausreichend deckten.
**Korrektur:** 0.1.36 Body-Heros/Breadcrumbs, 0.1.38 kleinere Fachtextbilder und Startseiten-Hero/Blockbreiten, 0.1.39 Bildrahmen und Texte, 0.1.43 lässt CSS/JS/Templates gegenüber 0.1.42 unverändert.
**Test:** lokale Browser-CSS-Kachelansichten, nicht alle Live-Bereiche auf realer WP-Instanz.
**Status:** **LOCAL TEILPASS / LIVE OFFEN**. Kein abschließender Nutzer-PASS für alle Seiten.

## HBD-DESIGN-GRENZE-20261019-07 – Unzulässige Collagen statt Einzelmotivfotos
**Befund:** Während Fotoarbeit entstanden mehrfach Webseiten-Mockups und mehrteilige Collagen statt geforderter Szenenfotos, wodurch keine brauchbare Abnahme der Zielbilddatei entstand.
**Entscheidung/WARUM:** Für bestehendes Designplugin nur bereits vorhandene, inhaltlich geprüfte **Einzelfotos** verwenden; keine Collagen als Kachelfotos, keine Blind-Upgrades durch Upscaling. Der neueste 0.1.43-Release hat laut geprüftem ZIP-Diff ausschließlich einzelne bereits vorhandene Fotos ergänzt, kein neues Bild generiert.
**Status:** **LOCAL CLOSED für 0.1.43, zukünftiger Regressionstest verpflichtend**.

---


## HBD-DESIGN-20261017-MEGA – Renderingquelle, bedingte Mehrlinks und Seitenrand
STATUS: **TEILWEISE LOCAL CLOSED, LIVE OFFEN**.
Beleg: Nutzer-Live-HTML der Seite „Frost & Abwesenheit“, 16.10., referenziert `hab-bewahr-design-vorschau` 0.1.19. Hauptnavigation `hbdp-mainnav` und Hub-Kacheln `hbdp-tile` stammen aus dem Designplugin. Der vorher fälschlich reparierte Kategorie-Plugin-Renderer war nicht an der sichtbaren Ausgabe beteiligt. Original `templates/site.php` fallback `if(!$children && $parent)$children=hbdp_children($parent['id']);` gab Endkategorien fälschlich Geschwister als Kinder. Original-Megamenü vereinte alte R3/V99 und C22-Nodes ohne Kanonisierung, teilweise doppelte Frost- und vier V99/C22-Areas.
Korrektur: Designplugin 0.1.20, bestehender Plugin-Ordner, lokal getesteter Canonical-Render aller 6 Welten, 36 Bereiche, 265 alten/neuen Topics und 851 Kategoriearchive. 0.1.21 änderte ausschließlich Desktop-CSS: in Chromium bei 1200px Zeilenabstand 52px → 32px; Menü ca. 82px niedriger. **Lokal PASS, keinesfalls Live-PASS behaupten.**
Neu vom Nutzer per Screenshot 17.10. gemeldet: Megamenü am Seitenrand **abgeschnitten**; `Alle Themen`/`Weitere Kategorien` erscheinen auch ohne zusätzliche ausgeblendete Kinder. Im aktuellen Renderer wird ein Mehrlink bedingungslos ausgegeben. Nutzer hat ausdrücklich festgelegt: 5 Bereiche/Welt, 4 Themen/Bereich; ein Überblicks-/Mehrlink darf **nur bei realem Überschuss** erscheinen. Abschneiden an Viewportkante muss korrigiert und desktop/tablet/mobile realitätsnah geprüft werden. Alte Zielvertragsangaben von 3 Links wurden durch Nutzernachtrag C2.2 vom 17.10. abgelöst.
REST: beide Designfehler **OPEN**, nicht durch 0.1.21-CSS-Abstandsfix gelöst. Vor jeder Pluginfreigabe echten Design-Renderer prüfen; keine Änderung/Sync an der Kategorie-Datenbank durch Design. Tatsächlich installierte Version nach letzter Nutzer-Screenshot nicht unabhängig live ausgelesen.

# EIGENTUMSSCHUTZ – DESIGN – FEHLERQUELLEN

STAND: 2026-10-14

## Noch offene Nachweisgrenzen
- HBD-DESIGN-001: WordPress-Live-Verhalten der Design-Vorschau 0.1.0 noch nicht geprüft. Keine Aussage über Live-Kompatibilität, Seitenqualität oder Laufzeitkosten. Status OFFEN.
- HBD-DESIGN-002: Master-Logodatei nicht separat belegt; Referenzausschnitt vom 8.10. nur für vorläufige Visualisierung. Status OFFEN.
- HBD-DESIGN-003: Vier Beispiel-Fotos stammen aus einem Nutzer-Mockup, keine final lizenzierten/verifizierten redaktionellen Titelbilder. Status OFFEN.

Keine bekannten reproduzierten Live-Probleme der Vorschau; nicht mit Fehlerfreiheit gleichsetzen.


## HBD-DESIGN-004 – Getrenntes Startseitenplugin erzeugt doppelten Design-Pluginbestand (14.10.2026)
STATUS: **LOCAL CLOSED – 0.1.4 IN-PLACE-UPDATE LOKAL PASS; WORDPRESS-LIVE-MIGRATION WEITER OFFEN**.
BEFUND: `HAB_UND_BEWAHR_STARTSEITE_0.1.0.zip` besitzt eigene Plugin-Identität und eigenen Ordner, obwohl bereits das umfassendere `HAB_UND_BEWAHR_DESIGN_VORSCHAU_0.1.3_TEXTMENUE_KLARE_THEMEN.zip` existiert. Nutzer meldet zwei unterschiedliche Designplugins im WP-Backend. Falsch war die Empfehlung, ein zweites Plugin zu installieren.
URSACHE: Startseiten-Modul wurde statt eines In-Place-Updates als separates WordPress-Plugin verpackt.
KISS-KORREKTUR: Bestehenden Original-Designplugin-Quellstand beschaffen, Startseite dort integrieren und Anzeigenamen auf „Hab & Bewahr – Design“ vereinheitlichen, ursprünglichen Plugin-Basename behalten. Zweites Plugin erst deaktivieren, wenn dessen eventuelle Shortcode-Nutzung und das in-place-Update geprüft sind; nie blind löschen. Kein dritter Pluginordner. Primäre Statusquelle: `CURRENT_STATE.md`.
REGRESSIONSSCHUTZ: vor jeder Ausgabe Installationsidentität/Basename gegen bestehendes Plugin prüfen; Performance-Checks verpflichtend.

NACHHOLPRÜFUNG 14.10.2026: Exakte Original-ZIP `0.1.3` wirklich in der bestehenden Library gefunden und hashgleich wiedergewonnen (SHA `f7cd98459fba15fb0d2ec61cb0c837a6d4e77708ae22f910aba8efa7b0d894b8`). Einziges Update 0.1.4 mit unverändertem Plugin-Basename erzeugt, lokaler 57/57-PASS plus sieben Simulationsläufe und ZIP-Integrität; SHA `044a745463fd22ec821ba5d99001264228bef3adbc3abed04b28dfdbddbc25b0`. Doppelung wird nach echtem WP-Update und anschließendem Deaktivieren des separaten 0.1.0-Plugins beendet, NICHT automatisch. Aktueller Stand/NEXT ACTION nur in `CURRENT_STATE.md`.

## HBD-DESIGN-005 – Pluginversion 0.1.3 lud Navigations-JS auf allen Seiten
STATUS: **LOCAL CLOSED in 0.1.4; WORDPRESS-LIVE-PERFORMANCE-OFFEN**.
BEFUND: In der echt wiedergewonnenen 0.1.3-Hauptdatei war `wp_enqueue_script('hbdp-nav',...)` außerhalb der `hbdp_for_query() !== null`-Bedingung und lief site-wide. KISS-FIX: Assets nur auf vom Designplugin gerenderten Seiten und Shortcode laden; shared Header-C-CSS von home-only CSS getrennt. Vollständiges Kategorie-Menü revisions-/weltabhängig transient-gecached; keine neuen Cron-/SEO-/Kategorie-Writes. Lokal durch statische und PHP-Mock-Positiv-/Negativtests geprüft; reale WP-Benchmark ausstehend.


## HBD-DESIGN-006 – Leere Navigations- und Themenkachel-Beschriftungen nach 0.1.4 (14.10.2026)
STATUS: **LIVE 0.1.4 FAIL / LOKAL 0.1.5 FIX-PASS / WP-LIVE-RETEST OFFEN**.
EVIDENZ: Screenshot Nutzer 14.10.2026 15:25: nur Magazin und Dienstleister als Nav-Text, Weltenmenü nur Pfeile, Hochkantkacheln ohne Titel.
URSACHE: 0.1.4-Live-Snapshot-Normalisierung liest `$raw['name']`; die echte zentrale APKW-Workflow-Quelle `active_nodes` speichert `display_name`. Alle importierten Namen gingen dadurch in der Designprojektion verloren. Bestehende transient-gecachte HTML-Navigation war mit falschen Bezeichnungen bereits gespeichert. Zusätzlich verwendeten Fotokacheln fälschlich eine Welt-Schleifenvariable als eigene Bezeichnung.
KISS-FIX: In demselben Plugin 0.1.5 auf `display_name` umstellen, den Titel jeder Fotokachel aus eigenem `$item[0]` rendern; Cacheversion in Navigations-Key aufnehmen. Korrektur isoliert nur 3 ausführbare Dateien plus README, kein Daten-/Kategorie-/Workflow-Eingriff.
REGRESSIONSSCHUTZ: WordPress-Snapshot-Schema **aus dem tatsächlich installierten zentralen Kategorie-Workflow lesen**; 546-Knoten-Simulation mit den richtigen Feldnamen, Browser-Check für sechs Navigations-, sechs Welt- und sechs Fotokacheltitel plus Cache-Neufassung. Lokal 30/30 PASS, Desktop+Mobil 6/6+6/6+6/6. **Nicht als WordPress-live-PASS ausgeben.** Current und NEXT ACTION ausschließlich DESIGN/CURRENT_STATE.md.
