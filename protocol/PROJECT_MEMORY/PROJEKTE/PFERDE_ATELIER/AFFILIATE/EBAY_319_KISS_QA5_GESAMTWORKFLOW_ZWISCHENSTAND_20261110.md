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

## Gesamtfehlerhistorie – gegen alte QA-Berichte geprüft (kein weiterer Reparaturauftrag)
- **308 → 311 (08.11.):** Original statt veralteter Patchbasis; 11 veraltete/bereits vorhandene Änderungen nicht erneut eingebaut. Altzustand beim Timeout/Wiederholen korrigiert, BUSINESS- und öffentliche Sicherheit erhalten, 49/49 Fachtests.
- **312 (08.11.):** Wiederholungsversuche bei der Quellenprüfung nicht mehr fälschlich als stillstehender Gesamtlauf bewertet; 311-Paket-Durchlauf lokal simuliert. Keine zusätzliche Engine.
- **314 (09.11.):** Startbereitschaft des Backends und echte Worker-Prüfung vereinheitlicht; Auftrag angenommen ist nicht gleich Gesamtabschluss. 460 lokale Prüfungen.
- **315 (09.11.):** Anzeige 0/298 als neue *Nachsuchteilphase* von tatsächlicher veröffentlichter Gesamtabdeckung getrennt. Kein Nachweis, dass bei 0/298 Produkte gelöscht wurden.
- **318/319 (09.–10.11.):** Stopp/Fortsetzen, gespeicherte Angebote für denselben Ablauf, lokale Bestandszuordnung. In der QA5-Arbeitskopie danach den zweiten, nicht registrierten 319-Controller samt ungenutzten Hilfsfunktionen nach Referenzprüfung entfernt; historisch gespeicherter Status bleibt lesbar.
- **QA2 (10.11.):** Einzelne Produktfamilienfehler blockieren andere nicht; Mehrfachzuordnung und letzter sicherer öffentlicher Stand bleiben geschützt. Bereits 187 Familien/47 simulierte Arbeitsschritte mit Einzelstörfällen geprüft. **Nicht nochmals lösen.**
- **QA3/QA4/QA5 (10.11.):** Drei nachweisbare Last-/Doppelarbeits-Ursachen im bestehenden Weg vereinfacht: nur ausgewählte BUSINESS-IDs materialisieren, öffentliche Quellbelege gesammelt lesen (334→7 Test-Lesungen), gezielte Nachsuche nur für betroffene Familien bereinigen (41→1 Test-Abfragen). Keine zusätzliche Steuerung oder Fachregel.

### Abgrenzung GitHub-Heartbeat vom eigentlichen Produktlauf
Der externe GitHub-Taktgeber ist laut PHP-Quellcode ausdrücklich **Kontrolle/Reserve** für die intern signiert fortlaufende, zentrale Verarbeitung. Beides ruft denselben kanonischen Worker mit bestehender Sperre auf, nicht zwei fachliche eBay-Engines. Acht ältere GitHub-Runden zeigten zusammen **231 Rückgaben mit Status retryable_error**. Da die älteren Logs weder Grund noch internen Fortschrittszähler zeigen, beweist diese Zahl **weder 231 selbstständige Produktfehler noch einen feststeckenden Gesamtworkflow**. Die zuvor versuchte zusätzliche GitHub-Diagnosezeile wurde deshalb auf dem Draft PR #722 vollständig rückgebaut (Commit feeb0b6576f1cc157ca7c8cd2a63148e623aad10). Der frühere, davon unabhängige Entwurf zur korrekten Endzustandsmeldung failed bleibt bestehen, ist aber nicht live. Keine neue Diagnoseregel, kein weiterer Worker.

### Einzige noch offene Gesamtfrage
Nicht einzelne Fehlerfälle erneut simulieren. **Ein** durchgehender realer Test auf isoliertem WordPress mit Datenbank: erhaltenen Stand laden → vorhandene Angebote zuordnen → gezielt fehlende Familien nachsuchen → Einzelfehler überspringen → Pause/Fortsetzen → gesichert speichern → endgültige Abdeckung und richtige öffentliche Produktkachel nachweisen. Erst daraus Installations-/Freigabeentscheidung ableiten. Bis dahin QA5 als Teststand beibehalten; Live-Installation/aktuell laufenden WordPress-Zustand nicht durch alte GitHub-Logs oder lokale Tests behaupten.
