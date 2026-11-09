# Original-Kategorieplugin vor Robotik-Adaption hart geprüft
Stand: 09.11.2026

## Originalbeleg
Im bestehenden Campus unter `PROJEKTE/EIGENTUMSSCHUTZ/PLUGINS/ISOLIERTE_PLUGINS/HAB-002-KATEGORIE-WORKFLOW/CURRENT.zip` das ZIP **tatsächlich binär eingelesen und die zentrale ZIP-Dateiliste geprüft**:
- 368.530 Byte, **49 Archiv-Einträge**, ein WordPress-Plugin `affiliate-portal-kategorie-workflow/`.
- Enthält `includes/class-apkw-dataforseo.php`, `class-apkw-research.php`, `class-apkw-research-evidence.php`, `class-apkw-concept-builder.php`, `class-apkw-validator.php`, `class-apkw-comparator.php` und `class-apkw-target-tree-dry-run.php`.
- Enthält auch `class-apkw-target-tree-sync.php`, `class-apkw-target-tree-runner.php`, `class-apkw-final-target-admin.php`, `class-apkw-frontend-structure.php`.
- **HAB-spezifisch und NICHT zu kopieren:** acht `profiles/hab-und-bewahr-*.json`-Dateien, diverse `class-apkw-insurance-*.php`, `class-apkw-c22-*.php`, `class-apkw-c23-*.php`, `class-apkw-v99-add-only.php`; darin liegen alte HAB-Import-/Reparaturwellen.

## Gegen den allgemeinen Arbeitsstandard abgeglichen
`ALLGEMEINGUELTIGE_BAUSTEINE/KATEGORIENMODELL/CURRENT_STATE.md` nennt als allgemeine Entwicklungslinie V1.9.1 mit **14-stufiger read-only Kategorie-/Keywordrecherche** und davon getrenntem finalem Writer; die alte V1.8.0 konnte nach geprüftem Audit **Taxonomien, aber keine WordPress-Seiten** anlegen.

Die HAB-ZIP-Version ist eine **projektgebundene Portalversion**, keine bewiesene neutrale Robotik-Rechercheversion. Auch das bloße Vorhandensein von Dateinamen beweist noch NICHT, dass einzelne PHP-Dateien ohne Abhängigkeiten kopierbar sind oder dass der neuere Writer WordPress-Seiten richtig erzeugt.

## KISS-Entscheidung
1. **Nicht** das komplette HAB-Plugin übernehmen oder gleichzeitig neben Robotik 0.2.0 installieren.
2. **Nicht** aus 0.2.0 einen weiteren, unabhängigen „Mini-Kategorieworkflow“ neben dem allgemeinen Workflow entwickeln.
3. Die **allgemeinen Recherche- und Prüffunktionen** aus der allgemeinen Quelle auf ihr Abhängigkeitsnetz und den bestehenden 14-Stufen-Ablauf prüfen, erst dann in die **eine Robotik-Pluginidentität** einbinden. Keine alten Profile/Writer/Altportal-IDs übernehmen.
4. Die einzige fachliche Quelle bleibt `RECHERCHE/PRODUKTE_V2_20261108.json` (68 ungeprüfte Robotik-Produkttypen). Der WP-Zielbaum bleibt daraus abgeleitet, aktuell leer.
5. Integration zuerst **read-only** (aktuelle Master-Revision, Fach-/Keywordprüfung, Dubletten/Lücken). Kein stiller Import und keine API-Kosten. Danach WordPress-Seitenerzeugung gesondert gegen echte WP-Instanz prüfen: die alte generische Writerbasis konnte nur Kategorien.
6. Positive/negative Tests, identische IDs bei Updates, Dry-run/Delta und echter WordPress-/Frontend-Readback sind Freigabebedingungen.

## Status
**BESTÄTIGT:** Die 49 Original-Archiv-Einträge und enthaltenen Namensklassen/Projektprofile; historischer Workflow aus Campus-Verträgen; Robotik-Zielformat.
**NOCH NICHT BESTÄTIGT:** Abhängigkeiten der PHP-Klassen, vollständige neutrale Build-Fähigkeit, echter Robotik-WordPress-PASS und WordPress-Page-Writer.
**Erlaubter nächster Code-Schritt:** genauer Modul-/Abhängigkeits-Audit vor dem ersten nicht-schreibenden Adapter. Keine Pluginaktualisierung auf Verdacht.
