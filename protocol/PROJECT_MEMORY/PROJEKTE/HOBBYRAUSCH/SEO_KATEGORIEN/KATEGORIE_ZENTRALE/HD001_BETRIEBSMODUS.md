# HD-001 – SCHLANKER BETRIEBSMODUS

## Hart geprüfter Befund

Das finale HD-001 1.14.8 enthält:
- DataForSEO-/Researchlogik;
- Dry-Run/Sync/Resume/Rollback;
- Zielbaum-Admin;
- Frontend-Projektion;
- Registrierung von `journal_cat`.

Es enthält **keinen** `uninstall.php`, keinen `register_uninstall_hook` und keinen Deaktivierungs-Cleanup.

Daraus folgt:
- Deaktivieren löscht Kategorien, Seiten, Terms, Metadaten und aktiven Target-Snapshot NICHT.
- Löschen der Plugin-Dateien führt nach dem geprüften Quellstand ebenfalls keinen eigenen Daten-Cleanup aus.
- ABER: ohne Ersatz würde `journal_cat` nicht mehr registriert und die neutrale Runtime-API fehlen.

## Neuer Normalbetrieb

1. HD-004 Kategorie-Kern installieren und aktivieren.
2. Live-Smoke-Test:
   - `journal_cat` erreichbar;
   - Magazin-Kategorien vorhanden;
   - Gestalten/andere Weltseiten weiterhin korrekt;
   - `hd_category_registry_ready() === true`.
3. Danach HD-001 deaktivieren.
4. Erneut derselbe Smoke-Test.
5. Erst bei PASS darf HD-001 optional aus WordPress gelöscht werden.

Empfehlung:
**zunächst deaktivieren, nicht löschen.**
Der Speichergewinn durch Löschen ist klein; Reaktivierung für Strukturänderungen bleibt so einfacher.

## Strukturänderungen später

Wenn Kategorien ergänzt, umbenannt, verschoben, zusammengeführt oder archiviert werden sollen:

1. exaktes HD-001 1.14.8 wieder aktivieren/installieren;
2. Änderung als Delta gegen aktuelle Revision modellieren;
3. lokale POS+NEG-Prüfung;
4. Live-Dry-Run;
5. genau ein Sync;
6. 100%-Readback;
7. HD-001 wieder deaktivieren.

HD-004 bleibt dabei aktiv und liest anschließend automatisch den neuen Snapshot.

## DataForSEO

Kein separates dauerhaft benötigtes WordPress-Strukturplugin.

DataForSEO ist Bestandteil des schweren HD-001-Workflows und wird nur für SEO-Evidence/Anreicherung benötigt, wenn eine Strukturänderung fachlich/SEO-seitig geprüft wird.

Es darf niemals Strukturautorität sein.
