# HD009 – aktuelle Affiliate-Zentrale Hobby Depot

**07.11.2026 – 0.1.20-dev – einzige aktuelle Installationsdatei: CURRENT.zip.**

- Vollständige ZIP: 1.066.589 Bytes, SHA-256 `cd6cb75f3ef0f393f94f3f93b974f3663ffa1f449c579886ae9520bc3d920cbb`
- Git-Blob: `9d9ac298c9e32bfc54f81d80e39f1a3560200d8c`
- WordPress-Pluginordner unverändert: `affiliate-portal-router/` – vorhandenes Plugin ersetzen.
- Änderungen gegenüber 0.1.19: **nur** `assets/hdar-amazon-start.css` (Verlaufsbalken in Quadrat und Querformat, Button 2px-Rundung, kleiner und weniger dominant, Bild um 4% zurückgenommen), Pluginkopf-Version, Stylesheet-Cache-Version. Alle anderen ZIP-Dateien sind bytegleich.
- Quadratbanner weiter nach „Auf einen Blick“, vor „Hobbygruppe“. Querbanner nach „Kosten und Ausrüstung“. Mobil Quadratbanner nach Haupttext. HD003 und HD007 bleiben unverändert.
- Gleiches zum Hobby passendes Foto wird formatabhängig dargestellt. Kein neues Bild, keine doppelte Werbeautomatik, keine neue Partner- oder Produktlogik.
- Amazon-Originalgrafik bleibt unverändert und mindestens 140px breit. „Anzeige“ bleibt eindeutig.
- DataForSEO ist als **manuelle**, kostenpflichtige Admin-Recherche vorbereitet: `/v3/merchant/amazon/products/live/advanced`. API-Zugang und Live-Ergebnis nicht bestätigt; keine automatische Produktempfehlung behaupten.
- **Gegenprüfung der ZIP 0.1.20:** Quell-ZIP-Hash vor Modifikation geprüft; ZIP-CRC PASS; 24 PHP-Dateien Syntax PASS; nur drei vorgenannte Dateien geändert; DataForSEO-Endpunkt unverändert.
- **Vorherige 0.1.19:** Lokaler WordPress-/Chromium-Test Desktop/Mobil und Platzierung PASS; anschließend wurden die Platzierungen vom Betreiber auf der Live-Seite bestätigt. Für das neue CSS wurde kein weiterer echter Browser-/Live-Test behauptet.
- **Live-Update auf 0.1.20 noch offen.** Nach Installation Quadrat + Querbanner auf Desktop und Mobil prüfen.

Fachliche Regel für Kategorien vs. konkrete Produkte:
`../../../../AFFILIATE/BANNER_ZIELREGELN_20261107.md`. Historiendokumente und die 0.1.19-Tests verbleiben in der Git-Versionsgeschichte/Plugin-Akte.
