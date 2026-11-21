# Hab Texterstellung: Kategorienbestand unverändert, tatsächlicher Original-Konflikt

Stand 18.11.2026 – **Benutzeraussage: Seit dem zuletzt bestätigten Stand keine neuen Kategorien. Diese Aussage wird übernommen. Kein weiterer Export oder neue Kategorieentscheidung angefordert.**

## Prüfresultate ohne Änderungen am Plugin

- Historisches Hab WordPress-Readback: 285 eindeutige WP-Kategorien unter 93 R3-Seiten; 0 doppelte Term-IDs, 0 doppelte Slugs und 0 fehlende R3-Eltern. Alle 285 Termdatensätze haben **kein** festes `article_type`-Feld. Das Nutzerstatement ersetzt den unnötigen wiederholten Neuabgleich; das Datum der Archivdatei wird weiterhin als Herkunft dokumentiert.
- Weitere bekannte und bereits gespeicherte Versicherungskonzeptionen: C25 beschreibt 138 geplante Kategorien, davon 46 *Beratung*, 46 *Häufige Fragen* und 46 anders benannte Sachkategorien; C26 185 weitere geplante Sachkategorien ohne `article_type`-Attribut. Die Profilquellen tragen den Status **NO_WORDPRESS_WRITE/NO_IMPORT_APPROVED**. Diese Zahlen **nicht** als zusätzlich nachweislich live importierte Kategorien zählen und **nicht** als neue Kategorien im aktuellen Nutzerauftrag ausgeben.
- Der tatsächlich geprüfte originale Hab-Kategorie-Workflow bewahrt `node_id`, Term-/Page-IDs und R3-Elternbezüge, aber keine durchgängig vorab festgelegte Beitragsart. Das entspricht dem Hab-Zielvertrag: **Kategorien sind Themen; Beitragsart wird erst im Texterstellungs-/MINI-Ablauf gewählt.**
- Original-PSTE-Kategorie-Karten-Loader `PSTE_Portal_Category_Map::load()` verlangt dagegen für **jede** Karte eine feste `article_type` zusammen mit Kategorie-Slug/-Name und R3-Produktseite. Ohne Typ Fehler `PSTE_PORTAL_CATEGORY_MAP_ENTRY_INVALID`; leere Liste `PSTE_PORTAL_CATEGORY_MAP_COUNT_INVALID`. `PSTE_Snapshot::resolveCategory()` übernimmt den Karten-Typ unmittelbar.
- Die bereits durchgeführten Original-PHP-Tests belegen: Die Map akzeptiert alle fünf Typen **wenn** eine Typzuordnung als Testwert hinzugefügt wurde (5/5) und lehnt fehlenden Typ ab (1/1). Das Hinzufügen von Testtypen begründet **keinen** autoritativen Artikeltyp für einen realen Hab-Thementerm.

## Entscheidung und Konsequenz

**Nicht der Kategorienbestand fehlt.** Die zwei Betriebsmodelle unterscheiden sich in der Zeitpunktfrage: Original-PSTE verlangt den Artikeltyp vor der Recherche; Hab wählt ihn später einmalig im Redaktionsschritt. Eine fixe Zuordnung etwa aller Hab-Kategorien zu *Beratung* wäre eine neue falsche Fachentscheidung und ist verboten.

Der Nutzer verbietet neue Architektur, Fixes und neue Funktionen; daher wird dieser Konflikt **nicht** durch einen unbestellten Umbau behoben. Reines Kopieren/Auskommentieren der Pferdebereiche kann Hab nicht sicher in den Produktivbetrieb bringen. Ein vollständiger Hab-Release muss entweder eine bereits existierende dokumentierte Typpolitik nutzen (bislang nicht belegt) oder den bestehenden Entscheidungszeitpunkt minimal anpassen – Letzteres nur bei geänderter Vorgabe.

## Reproduzierbarer Dateistand, keine Änderung

- Original 0.4.31 SHA256 `07b99fa549e87d28db53f0fac0b107c92a9f0de4a3de80ad5f31fb3b7b399f7d`
- Hab-Minimal 0.4.31.1 SHA256 `3f74e5c47f79ed36571dfc9a2adb63f639bdb9aafa294c19722ad2394fbe48d4`
- Universal Blanko 0.4.31.1 SHA256 `cbbca4c2a2f1122198cb3cda927ab739ad94e9df87bf9ace28c9201a4f16dc4d`
- ZIP CRC aller drei Archive erneut PASS. Original, Hab, Blanko, K0 und Live-WordPress **unverändert**.
- Ausführliches lokales Protokoll dauerhaft gespeichert in **beiden** Datei-Büros als `PRUEFUNG_BESTAND_UNVERAENDERT_20261118.md`. Keine nicht freigegebenen Plugin-ZIPs im Chat.

**Freigabe bleibt gesperrt:** Nicht weil neue Kategorien fehlen, sondern weil die originale festgelegte Artikelart nicht zur vorhandenen Hab-Redaktionsentscheidung passt.