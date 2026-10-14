# HAB & BEWAHR – VERBINDLICHER KATEGORIEN-SCHNITTSTELLENVERTRAG

**Status:** Zielvertrag für künftige Plugin-Anbindungen; **kein** Nachweis einer bereits implementierten neutralen Runtime-API.

## Einziger Kategorienbestand
- WordPress-Liveobjekte und dessen aktive R3/V8-Struktur-Bindung sind operativer Bestand.
- Dieses Büro dokumentiert Struktur-Verantwortung, geprüfte Revision und Anschlussvertrag, erzeugt jedoch **keine zweite beschreibbare Datenbank**.
- Für logische Identität zählt `node_id`; WordPress-`object_id` und `object_type`/`taxonomy` werden jeweils über das aktive Mapping ermittelt, nicht aus Namen, Pfaden oder hartcodierten Zahlen geraten.
- Ein Node liefert: `node_id`, Portalsäule, Status, Name, Slug, Parent-`node_id`, `object_type`, `taxonomy`, `object_id`. Zuordnung und Hierarchie spiegeln den aktiven Stand.

## Leser (alle übrigen Plugins)
- Design, SEO-/Textproduktion, Affiliate, Bildzentrale, Magazin, Dienstleister/HivePress, Glossar und zukünftige Bausteine bekommen **denselben neutralen, read-only Zugriff**.
- Nötige Abfragen: aktive Revision; einzelner Knoten nach `node_id`; direkte Kinder eines Knotens; Vorfahren/Eltern; Mapping auf WordPress-Objekt; Rückauflösung eines WordPress-Objekts; Liste nach Portalsäule/Taxonomie; aktiven/inaktiven Status.
- Kein direkter Aufruf von Admin-/Sync-Klassen des Kategorie-Workflows; keine eigenen Kategorie-Master, fest verdrahteten IDs, Slugs, Links oder gespiegelten Stammbäume.
- Aktualisierte Revision muss bei neuen Requests ohne Neuprogrammierung in neuen Kategorie-Anzeigen, Artikelzuordnungen und Kacheln sichtbar werden. Bei fehlender Auflösung: kein erfundener Ersatzpfad; klarer nicht-fataler Zustand.

## Ein Schreiber
- Kategorieveränderung ausschließlich aus zentralem Änderungsauftrag unter Wahrung des vorhandenen Kategorie-Workflow-Prinzips.
- Unterstützte Geschäftsoperationen: ADD, RENAME, MOVE, MERGE, ARCHIVE und REMOVE (nur wo keine geschützten Referenzen verbleiben). Löschung ≠ stilles Verwaisen vorhandener Inhalte.
- Änderung: gegen aktuelle Revision prüfen → Delta → Dry-Run inklusive IDs, Slugs, URLs, Parent-/Artikel-Referenzen → ausdrückliche Freigabe → **einmal** synchronisieren → vollständigen Readback → neue Revision verfügbar machen.
- Alte Revision bei inkonsistentem Zielstand nicht teilweise publizieren; kein stiller Blind-Write durch andere Plugins.

## Nicht mit Einrichtung dieses Büros erledigt
- Kein zusätzlicher WordPress-Write; keine neue Plugin-API implementiert oder live freigegeben.
- Änderungsoperationen und konkrete Reader erst als implementiert/funktionierend bezeichnen, wenn ein realer Plugin- und WordPress-Readback sie nachweist.
- Das bereits erfolgreich abgeschlossene 546/546-R3/V8-Release darf nicht ohne konkreten neuen Änderungsauftrag erneut synchronisiert werden.
