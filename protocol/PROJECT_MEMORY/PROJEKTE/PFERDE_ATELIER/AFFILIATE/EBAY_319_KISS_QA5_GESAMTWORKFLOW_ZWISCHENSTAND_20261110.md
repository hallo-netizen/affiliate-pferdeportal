# Pferdeatelier Affiliate/eBay – KISS-Zwischenstand QA5

Datum: 10. November 2026. **Isolierte Arbeitskopie; KEINE Live-Installation; KEINE Current-Freigabe.**

## Gesamtziel (unverändert)
Ein zentraler eBay-Arbeitsablauf, eine fachliche Auswahl, gesicherte Angebotsdaten und Mehrfachzuordnungen, sichere Veröffentlichung auf der konkreten Produktseite, begrenzte gezielte Nachsuche, Anhalten/Fortsetzen. Keine zweite Engine, keine neuen Tabellen, kein Verlust von Zugangsdaten, bisherigen Recherchen, Sicherungen oder Portal-Funktionen. Fehler bei einzelnen Produkten dürfen den Rest nicht stoppen; globale Datensicherheitsfehler bleiben hart.

## Stand aus der bereits gesicherten QA4-Kopie (nicht erneut entwickelt)
- Zentraler Ablauf statt des zweiten 319-Bestandscontrollers; alte gespeicherte Status-Option bleibt erhalten.
- Kandidaten aus gespeichertem Bestand verwenden, fachliche Klassifikation zentral, Mehrfachfamilien nur nach unabhängiger Prüfung.
- Sichere Checkpoints, Pause/Fortsetzen, letzter guter öffentlicher Stand; einzelne technische Lesefehler sind keine eBay-Markt-Nichtverfügbarkeit.
- Business-Materialisierung verarbeitet nur ausgewählte IDs, öffentliche Abdeckungsprüfung liest Quell- und Creative-Belege in Gruppen.
- Menüs auf Übersicht + fünf Bereiche gebündelt; keine fachliche Seite gelöscht.

## NEU in QA5 – eine belegte Vereinfachung des laufenden zentralen Wegs
Die abschließende `ebay_selection_prune_business_batch`-Bereinigung liest beim gezielten Gapfill nur die **Produktkonzepte, die in diesem Teilplan bearbeitet werden sollen**. Bisher wurden alle BUSINESS-Quellzeilen gelesen, obwohl fachfremde Zeilen direkt übersprungen wurden. Gleiche zentrale Methode, gleicher Cursor, gleiche Prüfungen und Veröffentlichung, keine neue Entscheidung, kein neuer Worker. Für Vollauswahl und leere Ziellisten wird der alte SQL-Pfad beibehalten.

**Vorher/Nachher-Nachweis:** Originale PHP-Methode QA4 und neue PHP-Methode QA5 gegen denselben reproduzierbaren Bestand von 2.000 BUSINESS-Beispielzeilen. 9 Szenarien erfolgreich verglichen: gezielte Nachsuche (41 → 1 SQL-Abfrage; 2.000 → 29 gelesene Zeilen), leere Zielliste, Wiederaufnahme (21 → 1), einzelne Zielklasse, Ziele vor Ende des Katalogs, Checkpoint, Vollbereinigung und Datenbankfehler. **Exakt gleiche Aktionen und Abschlüsse**; bei weniger gelesenen Endzeilen endet der rein interne Aufräum-Cursor früher. Das ist ausdrücklich keine reale WordPress-Messung.

Die acht vorhandenen Regressionsskripte und 23 PHP-Syntaxprüfungen bestehen, einschließlich Tests für 49 historische Fachfälle, Stopp/Wiederaufnahme, Speicherung und Einzelfehler.

## Harte Dateikontrolle
- Ausgang: `EBAY_319_KISS_EIN_WORKFLOW_QA4_LESEN_STATT_EINZELABFRAGEN_NICHT_INSTALLIEREN_20261110.zip`.
- QA5-ZIP: `EBAY_319_KISS_EIN_WORKFLOW_QA5_PRUNE_NICHT_INSTALLIEREN_20261110.zip`.
- QA5-SHA256 `561e5a4ef7148b351579aec8f67073bbf0805c5d1e1bc79d2d7b8c9444c26dc3`.
- 66/66 Dateien, ZIP-CRC bestanden; 65/66 byteidentisch mit QA4. **Nur `includes/trait-ppar-ebay.php` geändert.** Kataloge, Bilder, historische Recovery-Datei und Dateien für andere Provider unverändert. Kein `delete_option`, kein WordPress-Dateneingriff, keine Zugangsdaten-Migration.
- Reproduzierbare Belege: `EBAY_319_KISS_QA5_PRUNE_NUR_ZIELFAMILIEN_20261110.patch`, `qa5_prune_parity.php`, `ebay_QA5_test.py`, `EBAY_319_KISS_QA5_PRUNE_PARITAET_20261110.json`, `EBAY_319_KISS_QA5_REGRESSION.log`.

## Offener Freigabeblock – nicht mit weiteren Simulationen verwechseln
Die verfügbare Umgebung enthält kein vollständiges WordPress mit Datenbank; ein Download der WordPress-Quellen ist hier mangels DNS-Zugriff nicht möglich. Deshalb ist **keine echte Speicherung auf WordPress und keine reale Produktanzeige** nachgewiesen. **Keine Installationsfreigabe.** Produktiver Lauf und vorhandene Zugangsdaten auf der Website wurden nicht verändert. Ein isolierter WordPress-Praxistest bleibt erforderlich, bevor der Gesamtworkflow als fertig bezeichnet werden darf.