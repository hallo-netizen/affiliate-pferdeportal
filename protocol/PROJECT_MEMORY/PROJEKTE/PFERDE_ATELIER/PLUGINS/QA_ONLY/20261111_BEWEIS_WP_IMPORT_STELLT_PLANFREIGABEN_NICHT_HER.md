# Verbindliche Quellcode- und Laufzeitprüfung: Repariert der Import dreier WordPress-Artikel den fehlenden Plan? (11.11.2026)

**Antwort: Nein. Keine drei fiktiven Artikel als scheinbare Reparatur importieren.**

## Originaler Code des zuletzt gelieferten WordPress-Teststands
- PSTE **0.57.144.40**: `includes/class-pste-repository.php`, Methode `compilerPlanningTopicCount()` um Zeile 2311. Sie liest ausschließlich die PSTE-eigene Tabelle `wp_pste_topic_pool` mit `planning_suitability='YES'` und `context_state IN ('CURRENT','NOT_REQUIRED')` und zählt nur K0-Routen. Es existiert in dieser Methode keine Abfrage der WordPress-Beitragstabelle `wp_posts`.
- Gleiche Quelle, `compilerPlanningTopicPage()` um Zeile 2326. Die tatsächlichen planbaren Themen werden ebenfalls ausschließlich aus `wp_pste_topic_pool` geladen.
- `includes/class-pste-admin.php` um Zeilen 1896–1956: Der „Kurze Dienstweg“ sucht genau diese planbaren Themen; falls keines gefunden wird, wirft er **`PSTE_SHORTPATH_NO_ELIGIBLE_SELECTED_TOPICS`**. Ein WP-Artikelimport kann diese Prüfung nicht in READY ändern.
- PSERC **0.28.67**: `includes/class-pserc-plan-compile-job.php` ab INVENTORY, NORMALIZE und CANDIDATE. WordPress-Beiträge werden als bestehender Inhalt/Abgleich eingelesen; sie ersetzen keine fehlenden PSTE-Freigaben und können zusätzlich als Doppelungen bewertet werden.
- PSTE `includes/class-pste-compiler-read-capability.php` `requireFreshPlanningSources()`: Ein geänderter WordPress-Inventarstand kann vielmehr die Bestandsbindung ungültig machen. Darum ist ein WP-Import **nicht neutral** für den Redaktionsplan.

## Tatsächliche ausführbare Gegenprobe mit Originalfunktion
PHP mit geladenem `PSTE_Repository::compilerPlanningTopicCount()` aus der unveränderten originalen .40-Pluginquelldatei ausgeführt; nur `$wpdb` wurde lokal durch eine reine Lesetest-Attrappe ersetzt, ohne echte Datenbankzugriffe:
```
simulated_wp_posts=0 planning_ready=0
simulated_wp_posts=3 planning_ready=0
PASS: planning read excludes wp_posts entirely
```
Kein echter WP-Server wurde verändert; dies ist die **Funktionsprüfung**, nicht eine End-to-End-Abnahme.

## Ergebnis/Was folgt daraus
Eine WordPress-Importdatei mit den drei fertigen Texten **würde drei Beiträge anlegen**, aber **nicht** `planning_suitability` oder den K0-Hand-off im Themenpool reparieren. Sie löst damit die vom Nutzer gemeinte WordPress-Freigabe-Störung **nachweislich nicht**. Deshalb wurde **kein** fingierter Artikeltext erstellt, **keine** XML-Importdatei erzeugt und **keine** falsche Reparaturbestätigung gegeben.

**KISS-Richtung:** Drei Originalartikel-Metadatensätze sind als signierter 5-Felder-Batch vom 10.11.2026 vorhanden. Für deren Artikelerstellung können sie **ohne erneuten PSTE/PSERC-Lauf** in die vorhandene K0-Eingangskette gelangen, jedoch sind weitere legitime K0-Redaktions-/Recherchebelege nötig. Die Wiederherstellung des **zukünftig automatisch funktionierenden** WordPress-Workflows ist ein eigener Schritt: verlorene Freigaben dürfen nicht durch erfundene Artikel simuliert werden; das nur lokale Anti-5k-Plugin .40/.67 ist noch nicht WordPress-Ende-zu-Ende geprüft. Keine DB-Manipulation ohne gesonderten Auftrag.

**Status:** `WP_IMPORT_NOT_A_WORKFLOW_REPAIR_PROVED`; `NO_ARTICLE_DUMMY`; `NO_IMPORT`; `NO_DATABASE_TOUCH`.
