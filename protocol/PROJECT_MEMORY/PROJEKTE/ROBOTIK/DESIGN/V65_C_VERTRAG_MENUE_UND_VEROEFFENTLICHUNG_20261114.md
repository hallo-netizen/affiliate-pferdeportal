# Robotik V65 – reale Veröffentlichung + fachlich gleichmäßigere Navigation
Stand 14.11.2026; Quellgrundlage: **tatsächlich hochgeladener WordPress-Live-Export V62 und V63-Zwischenexport 16/227**; 0.4.9-Sollmanifest V62 und die tatsächliche Original-PHP des bestehenden Designplugins 0.2.3.

## Wo stehen wir?
- V62-Liveabgleich bestätigt **115 WP-Seiten, 90 WP-Beitragskategorien**, davon 104 alte Seiten und 89 alte Rubriken eindeutig gemappt, 11+1 Fremdobjekte ausdrücklich geschützt.
- **Der bisherige V63-Abschlussbericht ist ein Zwischenstand 16/227, WRITING**, kein belegter Abschluss. Ein weiterer Live-Abschluss wurde nicht vorgelegt. Eine tatsächliche Publikation durch den Assistenten ist nicht erfolgt.
- Das C-Vertragssoll hat **8 Welten, 188 Seiten (47 Gruppen, 141 Typen), 296 Rubriken**. Davon 16 SEO-HOLD-Seiten und 48 zugehörige Rubriken NICHT importiert. Durch V63 sollen **68 neue Seiten als Entwurf und 159 Rubriken** angelegt werden.
- Verglichen: Das Designplugin 0.2.3 kennt nur **7 ROOTS** (ohne Humanoide), führt für Admins auch Drafts auf, rendert direkte Typen als einzelne leere h3-Überschriften und verteilt ungleich große Abschnitte auf CSS-Gridspalten.

## Zwei Möglichkeiten fachlich gegeneinander geprüft
**Weg 1 – weiter recherchieren und echte neue Untergruppen schaffen.** Nur sinnvoll, wenn eine bestehende Welt sehr viele unterschiedliche Typen ohne Gruppen enthält und sich eine stabile, suchintentionstreue Untergruppe mit mehreren konkreten Typseiten ergibt. Für Beitragsrubriken gilt pro Robotertyp: eigenständiges Thema plus **ungefähr 3–5 plausible Artikel**, keinesfalls bloß automatisch drei Rubriken. 55/141 Produkttypen haben derzeit nur eine WP-Rubrik; das ist nicht automatisch falsch. Manuelle Prüfkandidaten: acht Freizeit-Einzelrubriken, sieben Sport- und sieben Pflege-Einzelrubriken, insbesondere 24 gewerbliche Einzelrubriken. Bei „Knieprothesen“ und „Armorthesen“ robotischen Bezug vor jeder SEO-Priorisierung präzisieren. **Keine neuen Gruppen bloß für Optik, keine automatischen URL-/Hierarchiewechsel.**

**Weg 2 – vorhandene Struktur im Megamenü neu darstellen (empfohlen und umgesetzt).** Echte Gruppenseiten bleiben anklickbare Überschriften. Direkte Typseiten erscheinen als einzelne Links in einer bloß visuellen, nicht als WP-Seite/Kategorie angelegten Gruppe **„Weitere Robotertypen“**. 2–4 je nach Umfang ausbalancierte, tatsächlich gefüllte Spalten; Industrie-Landingpages in rekursiver Linkliste; Humanoide als 8. Root; alle veröffentlichten WP-Robotikseiten genau einmal im Menü, für Admin und Publikum gleichermaßen. Auf den konkreten Typseiten sind dessen zugeordnete Beitragskategorien unter **„Zum Robotertyp“** zu sehen – leere Archive sichtbar aber vorerst ohne leeren Link. Kein doppelter Menüeintrag.

## Ist-Verteilung der untersten Typseiten je Welt
| Welt | Typen | 1 Rubrik | 2 Rubriken | 3 Rubriken |
| --- | ---: | ---: | ---: | ---: |
| Haushalt | 18 | 2 | 1 | 15 |
| Garten | 14 | 5 | 2 | 7 |
| Freizeit | 14 | 8 | 1 | 5 |
| Sport | 17 | 7 | 1 | 9 |
| Bildung | 10 | 2 | 1 | 7 |
| Pflege | 15 | 7 | 1 | 7 |
| Humanoide | 12 | 0 | 0 | 12 |
| Gewerbe | 41 | 24 | 10 | 7 |

**Gesamt:** 141 konkrete Robotertypen; 55 mit einer Rubrik, 17 mit zwei, 69 mit drei. Alle 296 haben zumindest drei grobe Themenrichtungen; diese Richtungen sind **keine inhaltlich abgenommenen 3–5 Artikel**. Keine automatische Erweiterung oder Verschiebung.

## Konkret vorbereitete Updates: ZWEI vorhandene Pluginidentitäten
- **Kategorie-Workflow 0.4.10**, ursprünglicher Plugin-Slug unverändert: Neue Backend-Seite **Robotik Kategorie → Neue Seiten sichtbar machen**. Zeigt vollen Live-Status; erst nach ausdrücklich belegtem **227/227-Importabschluss** und nachgewiesenen 104 veröffentlichten Altseiten wird EIN kontrollierter Veröffentlichungsblock mit **68 neuen Seiten** angeboten. 16 SEO-HOLDs und 48 Rubriken ausgeschlossen, keine alten oder fremden Objekte verändert. 10er-Pakete, Zustandsübernahme, Doppelschreibschutz, Unterbrechungsfortsetzung, Abschluss-Prüfung. Bereits angelegte Kategorien bleiben, keine neuen Inhalte erfunden; die alten V63-Prüfungen akzeptieren in diesem einmaligen Publikationspfad auch `publish` statt nur `draft`.
- **Strukturdesign 0.2.4**, ursprünglicher Plugin-Slug unverändert: 8 Hauptwelten inklusive Humanoide, keine Drafts/Previewlinks in der normalen Navigation, gruppierte Einzeltypen mit ausgeglichenen Spalten und verschachtelter Industrie-Landingpage. Auf der **untersten** Robotertyp-Seite werden ausschließlich ihre eigenen WP-Beitragsrubriken ausgegeben (auch wenn sie noch keine Artikel haben). Keine WordPress-Seiten, Eltern, Kategorien, IDs, URLs, Posts, SEO oder Datenbanktabellen verändert.

## Nachweise
- Lokal auf echtem V62-Manifest (mit simuliertem WordPress-API): **104/104 veröffentlichte alte Seitenlinks genau einmal**, nach sicherer Veröffentlichung **172/172 Links genau einmal**, 8. Root „Humanoide“ korrekt sichtbar, Industrie-Landingpages erreichbar, keine Entwurf-Links. Kategorien am Produkttyp sichtbar; leere Taxonomiearchive nicht angeklickt.
- Mit echtem V62-Liveexport als Ausgangsbestand im simulierten WordPress: V63-Import **227/227 PASS**, danach neue Sammelpublikation **68/68 PASS** und echter Source-/Kategorie-Readback weiterhin PASS. 104 Altseiten und 90 Alt-/Fremdkategorien erhalten, **16/48 HOLD unverändert**, Neustart schreibt nichts, fehlerhafte Identität stoppt.
- PHP Syntaxprüfungen: alle bestanden; Chromium-Vorschau in 1440, 1024, 900 und 390 Pixel ohne horizontale Überläufe, acht Hauptwelten sichtbar. 8 bisherige Backend-Dateien (Import/SEO/Publikation/Vorschau und drei JSON-Pläne) byteidentisch. Aktuelles Frontend in echtem Browser/WordPress **NOCH NICHT LIVE ABGENOMMEN**.

## Nächste Aktion (keine Doppelarbeit)
1. V63-Importlauf im echten WordPress **auf 227/227 abschließen**, falls er noch läuft. Keine neuen 16 SEO-HOLD-Seiten importieren.
2. **Bestehende** Plugins aktualisieren: Kategorie-Workflow 0.4.10 und Strukturdesign 0.2.4. Anschließend unter **Robotik Kategorie → Neue Seiten sichtbar machen** einmal den 68er-Veröffentlichungsblock ausdrücklich freigeben.
3. Danach öffentliches Menü und konkreten Produkttyp prüfen. **Humanoide erscheint erst, wenn die reale WP-Hauptseite publiziert wurde.** Die untersten Inhaltsrubriken sind sichtbar, aber noch leer und ohne Beiträge keine sinnvollen SEO-Archive.