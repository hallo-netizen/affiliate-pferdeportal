# Pferdeatelier Texterstellung – Sicherheitsfix 0.4.27 (18.11.2026)

**Status: Nur getrennte WordPress-Testinstallation; keine Livefreigabe.**

## Beweis 0.4.26-Fehler
Bei Artikelimport registrierte Texterstellung 0.4.26 den globalen WordPress-`query`-Filter. Jeder INSERT/UPDATE-SQL-Text mit der Teilzeichenfolge `wp_posts` erzeugte `WP_POSTS_SQL_WRITE_SEEN`. Das bestehende `record()` schrieb dieses Ereignis mit `update_option` in die Datenbank. Schon der Name des gespeicherten Ereignisses enthält `wp_posts`; das SQL-UPDATE zur Protokollierung löste deshalb denselben globalen Filter immer wieder aus. **Selbstrekursion tatsächlich reproduziert:** 11 verschachtelte SQL-Updates, Lauf absichtlich begrenzt; ohne Begrenzung läuft dieser Weg immer weiter. Das ist ein schwerer, von uns eingeführter Fehler der Diagnose 0.4.26. Ein echtes Server-Fehlerlog der Störung wurde nicht geliefert; die spezifische Nutzerstörung kann damit plausibel, aber nicht serverseitig abschließend erklärt werden.

## KISS-Fix
Neue vollständige ZIP aus dem realen Pferdeatelier-Quellstand 0.4.26:
`/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/Texterstellung-0.4.27-SICHERE-GESAMTDIAGNOSE-PFERDEATELIER-TEST.zip`

- SHA256 `21790c3176aa20fbb2909f4ed3fa8af9a010c10ac1cd6075ac8d032dc8ead5ff`
- 88 Dateien, 85 byte-identisch zu 0.4.26, 3 geändert: `texterstellung.php` Versionskopf/Anzeige, `class-txe-diagnose.php`, README.
- Der globale SQL-/query-Hook wurde **physisch entfernt**.
- In WordPress-Speicherhooks werden Diagnoseereignisse **nur im Speicher gesammelt**, ohne Datenbank-Schreiben. Erst nach dem eigentlichen `wp_insert_post`-Rückgabewert erfolgt **eine** sichere Speicherung der gesammelten Ereignisse.
- Reentranzschutz für das Diagnose-Protokoll. Original-Importer, WordPress-Insert, K0, Inhalte, Redaktionsplan und Auftragslogik nicht geändert.
- 14 Diagnosebereiche erhalten. Der gelöschte SQL-Query-Hook wird nicht mehr als Beleg verwendet; erfolgreiche Post-Schreibvorgänge werden über den normalen `wp_insert_post`-Hook dokumentiert.

## Tests / offene Nachweise
- 38/38 gezielte PHP-Regressionstests bestanden mit den zwei realen K0-Artikeln und nachgebildetem WordPress, inklusive `empty_content`-Auslöser, Kollision, Rücklesen, Erfolg.
- 0 Datenbank-Logs im WordPress-Speicherfilter; kein globaler `query`-Filter mehr registriert.
- 78/78 PHP-Syntax, ZIP-CRC PASS, genau 3 veränderte Dateien.
- **Echter WordPress-Test noch offen.** Bisherige 0.4.24/0.4.25/0.4.26 ZIPs bleiben in der persönlichen Pferdeatelier-Dateiablage unverändert.

## Sichere Wiederherstellung
Falls WordPress-Admin erreichbar: auf oliver-beil.de 0.4.26 über die normale Plugin-Aktualisierung durch vollständige 0.4.27-ZIP ersetzen, *nicht löschen*. Falls der Admin aufgrund der Störung nicht mehr erreichbar ist: beim Hoster den Plugin-Ordner `wp-content/plugins/texterstellung` zunächst in `texterstellung-aus` umbenennen und erst nach wiederhergestelltem Adminzugriff die neue Version installieren. **Kein weiterer Import mit 0.4.26.** Kein Reset von Beiträgen/Plänen/Daten.
