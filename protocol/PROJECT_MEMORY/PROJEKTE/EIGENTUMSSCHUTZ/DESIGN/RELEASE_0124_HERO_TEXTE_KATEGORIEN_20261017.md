# Hab & Bewahr – Designplugin 0.1.24: sechs Hauptkategorien

Stand: 17.10.2026
Status: **Fertiges Update des bestehenden Designplugins, lokal geprüft. WordPress-Live-Abnahme offen.**

## Ausgangspunkt und Änderungsumfang
- Bytegenau aus dem fertigen vollständigen Update 0.1.23 im **gleichen Original-Pluginordner `hab-bewahr-design-vorschau`**.
- **Sechs getrennte vollwertige, panoramische Fotos**, jeweils ca. 1916×821 Pixel als hochwertige WebP direkt in bestehenden assets/hero-*.webp. Keine Fotocollage, kein Text im Bild, keine unscharfen Miniatur-Quellen.
  - Einbruch: Wohnhaus mit Sicherheitszaun in Abenddämmerung
  - Vandalismus: beschädigter Laden und Graffiti bei Tageslicht
  - Wasser: Haus bei starkem Regen und Wasseransammlung
  - Feuer/Gase: Küche, Rauchmelder, Technikraum und Feuerlöscher am Tag
  - Wetter/Natur: weites Unwetter mit Gewitterfront über einer Landschaft
  - Technik/Ausfälle: Tageslicht, Sicherheitskamera und elektronisch gesichertes Grundstück
- **Sechs individuelle, direkte Schutzsätze** mit „du“ statt beliebigem beschreibendem Kategorietext; H1 und vollständige alte Kategorienamen/URLs unverändert.
- **Kontrast gesondert:** helle oder dunkle lokale Textverläufe nach Motiv; Text und Bild bleiben getrennt. Desktop-Hero flach; mobil eigener Ausschnitt/Schutzverlauf.
- **Unterkategorie-Bildkacheln nach Thema**, nicht mehr standardmäßig überall dasselbe Hausmotiv.
- **Banner-Rasterkorrektur:** Eine befüllte Werbekachel kann Restspalten belegen (z. B. sechs Unterkategorien plus ein **zwei Spalten breiter** Banner). Leere Werbekacheln für Besucher ohne Markup, Administrationshinweise nur für Admins; verkaufbare Partnerfläche separat.
- **Ratgeber:** Beiträge ausschließlich aus tatsächlich veröffentlichten zugehörigen WP-Kategorien. „Zum Magazin“ als echter Link nur, falls im aktiven Portalbaum eine Magazin-URL vorhanden ist; keine losen „Magazin / Dienstleister“-Links. Keine erfundenen Artikelbeispiele für Besucher.
- Vorhandener Langtext weiterhin am Seitenende, restliche Ebene/Layout, 265 Themenseiten, IDs, Slugs, URLs und Kategorieplugin **unangetastet**.
- Keine neuen Pluginidentitäten, Tabellen, Cronjobs, Kategorie-Schreiboperationen oder Frontend-HTTP-Zugriffe.

## Ausgeführte Prüfungen
- **8/8 PHP-Dateien Syntax-PASS**, ZIP-Integrität PASS, 54/54 ZIP-Dateien, 6 individuelle Hero-Bilddateien.
- **80 positive und negative Ausgabetests** mit 4–8 Unterkategorien, Admin ja/nein, Banner leer/befüllt, Partner leer/befüllt, Beiträge leer/befüllt; echte PHP-Funktion und Mock-WordPress-Aufrufe.
- **12 Browserdarstellungen lokal**: sechs Helden auf Desktop 1440 und Mobil 390. Scharfe Bildquellen, individuelle Schutzsätze, vollständige sichtbare Texte innerhalb Hero, kein seitlicher Überlauf.
- Prüfgrenze: **kein WordPress-Live-Update und kein echter Live-Frontendtest**. Providerseitige automatische Bannerbefüllung wird erst durch spätere Bannerintegration geschaltet, nicht behauptet.

## Installierbares Artefakt
`/Eigentumsschutz/Design/HAB_UND_BEWAHR_DESIGN_0.1.24_HERO_TEXTE_KATEGORIEN.zip` (persönliche Library)
Name des Plugins bleibt **Hab & Bewahr – Design**, Basename und Pluginordner unverändert.
Lokale ZIP-Größe: 3.470.841 Bytes.
SHA-256: `9d7cf4ed756293c5b81d0b62f388772f88b2526eeb3463b9a9c11cc5184de20e`.

## NEXT ACTION
Bestehendes **Hab & Bewahr – Design** Plugin in WordPress als normales Update auf **0.1.24** bringen. Danach auf den **sechs tatsächlich sichtbaren Hauptkategorieseiten** mit Desktop und Mobil Hero-Schärfe/Überblick, Satz und Textkontrast, verschiedenartige Kachelbilder, Banner-/Partnerplatz (leer/gefüllt), veröffentlichten Ratgeberbereich und unveränderten Langtext prüfen. Keine Kategorie- oder Importaktion.
