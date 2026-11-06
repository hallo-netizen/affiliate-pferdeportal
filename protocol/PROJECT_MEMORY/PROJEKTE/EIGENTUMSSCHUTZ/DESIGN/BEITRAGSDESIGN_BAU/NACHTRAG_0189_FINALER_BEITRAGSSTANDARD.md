# Hab & Bewahr – Beitragsdesign 0.1.189 – Stand 06.11.2026

## Entscheidungsstand
- **Ein einziges Beitragsdesign** für alle normalen WordPress-Beiträge, unabhängig von Textart.
- H1 und die echte Breadcrumb-Navigation bleiben. **„HAB & BEWAHR · RATGEBER“ über dem Titel entfällt**, weil der zusätzliche Text keinen Informationsgewinn bringt.
- **Die Kategorie-Doppelung unter H1 entfällt**, die Kategorie bleibt als anklickbarer Breadcrumb erhalten.
- H2 bekommen ausschließlich eine **kleine salbeifarbene Linie darüber**, H3 bleiben unmarkiert. Keine großen farbigen H2-Kästen.
- Normale Listen haben ruhige salbeifarbene Punkte; nummerierte Schritte bekommen Kreiszahlen; echte Checklisten haben optional die CSS-Klasse `hb-checkliste` und grüne Häkchen. **Keine automatische Umdeutung beliebiger Listen in Checklisten.**
- Einheitliche Abstände zwischen Absätzen, H2/H3, Listen, Tabellen und Merksatz; Inhalt, SEO-Textlänge, interne Linkziele und fachliche Aussagen bleiben Sache des späteren Texterstellungssystems.
- Zweispaltiger Desktop-Beitrag, rechts Affiliate-Produkte und Banner; mobil die **gleiche** Produktgruppe nach dem ersten Fachabschnitt und Banner später. Keine Duplikate, kein öffentliches Fake-Angebot, kein sichtbares Datum, kein sichtbarer Quellenblock; die originalen redaktionellen Quellen bleiben in WordPress.
- Sonderbehandlung für akute Schadensfälle bleibt unverändert; kein Werbungseinschub vor Sofortmaßnahmen.

## Geprüftes vollständiges Update-Paket
- Datei: `HAB_UND_BEWAHR_DESIGN_0.1.189_BEITRAGSFEINSCHLIFF.zip`
- Lokaler SHA-256: `947a950273edb6bf47e76ffeef67ff51425db620adc2650c742831e73093134c`
- 84.349.647 Bytes; 430 ZIP-Einträge; Original-Identität: `hab-bewahr-design-vorschau/`, WordPress-Plugin `Hab & Bewahr – Design`.
- **Basis**: 0.1.188 `f1c92dc85dd506ecbf08b3ab369b303d7e71bcf2b22e391dae280bc7dc60baf8`.
- **Diff**: exakt 3 Bestandsdateien geändert: Plugin-Hauptdatei (Version und CSS-Caches), `includes/article-page.php`, `assets/article-design.css`. **427 von 430 bestehenden Dateien byteidentisch.**
- ZIP CRC PASS; PHP-Syntax aller 35 PHP-Dateien PASS; JS-Syntax PASS; PHP-WP-Mock PASS (echte Breadcrumb-Kategorie, kein doppelter Kopftext, keine Quellen/Publikationsdaten, keine erfundenen öffentlichen Produktangebote, kein redundantes Inhaltsverzeichnis, ein Produkt/Banner je Ausgabe); lokaler Browser PASS auf 1440 / 768 / 390 px, keine horizontalen Überläufe und kein Doppelangebot beim Breakpoint-Rückwechsel.
- **Kein echter WordPress-Livetest**. Die alte offiziell gesicherte Plugin-Current 0.1.184 bleibt vorerst unverändert; dieses Dokument ist eine Entwicklungsakte, kein stiller Ersatz des Pluginbüros.
- Ein späterer Chat darf den lokalen ZIP-Speicherpfad **nicht als Zugriffsgarantie** behandeln. Vor erneutem Build den aktuellen originalen Design-ZIP-Stand und die neueste installierte Version prüfen.

## Ablageeinschränkung
Das neue vollständige 0.1.189-Plugin wurde im aktuellen Chat als herunterladbare ZIP erzeugt. Die gesonderte Library-Ablage `/Eigentumsschutz/Design/` scheiterte am Speicherkontingent; **nicht** als dort erfolgreich gespeichert behaupten. Dieser Campus-Eintrag hält Designentscheidung, Version und Prüfbelege dauerhaft fest, enthält aber **noch keine binäre 0.1.189-CURRENT.zip**. Das offizielle HAB-001-DESIGN/CURRENT.zip bleibt unverändert, bis die neue ZIP physisch und unabhängig wiederabrufbar gesichert und die Live-Abnahme erfolgt ist.

## Nächster Schritt
Die Version 0.1.189 über das bestehende Plugin installieren, einen normalen Beitrag auf Desktop/Mobil sowie Navigation und Kategorien stichprobenartig kontrollieren, danach offizielles ZIP im Pluginbüro sichern und Current aktualisieren. K0, Affiliate-Engine und Kategoriesystem bleiben unangetastet.
