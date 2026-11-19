# Pferdeatelier Affiliate/eBay – QA12 6.72.323, KISS-Backend und ausführliches Laufprotokoll

**Stand 11.11.2026 – ISOLIERTE TESTVERSION, KEIN LIVE-/CURRENT-RELEASE.**

## Ausgangslage anhand der echten Nutzer-Screenshots und des übermittelten vollständigen Backend-Seitentextes

- Die eBay-Fachseite zeigt schon vor dem gewünschten Statusbereich ausführliche Provider-, Vertrags-, Katalog-, Cron-, technische URL- und 8 alte Suchprofile als Roh-JSON; danach folgen mehrere lange technische Prüfabschnitte und bis zu 100 Prüfkandidaten auf der Hauptseite. Das ist für normale Bedienung überladen.
- Letzter gezeigter neuer kanonischer Lauf: `09c34988-...`, Phase `reconcile_local`, angezeigtes `0/298` bei **432 separat gespeicherten eBay-Freigaben**. `0/298` in einem noch ungeprüften neuen Lauf ist kein Nachweis von Löschen oder echter öffentlicher Nullversorgung; diese Fehlinterpretation muss in der Ansicht verhindert werden.
- QA11 hatte lediglich eine interne begrenzte Liste von 12 eBay-Schlussfehlern ohne vollständigen für Administratoren einsehbaren Lauf-/Fehlerbericht. Kurz-Historie (10 Run-Einträge) bewahrte keine individuellen Fehlerprotokolle. Frühere Aussagen „umfassende Protokollierung vorhanden“ waren falsch.

## QA12: Was sich ändert

1. **Schlankes Backend:** Standardseite zeigt nur die wichtigsten Werte, tatsächlichen Laufstatus, korrekten Fortschritt, Produktabdeckung, Produktverfügbarkeit, Fehlermeldungen und den bestehenden Stopp-/Fortsetzen-Knopf. Überlange Erklärungen, Rohsuchprofile, Katalog-/Betriebsprofil, Provider-Tests, Auswahl-/Materialisierungshistorie und die Prüfkandidaten-Tabelle sind auf vorhandener Seite **nur nach bewusstem Klick** sichtbar. Die teure Abfrage der 100 Prüfkandidaten läuft bei normalem Seitenaufruf überhaupt nicht mehr. Keine neue Menüseite; alle Funktionen bleiben über **Einstellungen/Werkzeuge**, **Technische Details**, **Prüfkandidaten** erreichbar.
2. **Korrekte 0/298-Einordnung:** Solange für den neuen Run die erforderliche Abdeckung noch nicht berechnet ist, zeigt das Backend **„Noch kein neuer Gesamtnachweis“** statt einer irreführenden Nullabdeckung. Bisherige eBay-Freigaben bleiben unverändert gespeichert.
3. **Echter Stillstand sichtbar:** Sind tatsächlicher Fortschritt und Worker-Tick länger als drei Minuten unverändert, erscheint eine klare rote Meldung. Ist nur der Fortschritt drei Minuten alt, während der Worker weiter aufgerufen wird, erscheint eine Warnung. Die reine Statusabfrage startet weiterhin **keinen** Worker.
4. **Persistenter Lauf-/Fehlerbericht:** Die einzige bestehende kanonische eBay-Zustandsspeicherung bleibt maßgeblich. Nach **erfolgreich verifiziertem Speichern** werden relevante Zustandsänderungen zusätzlich in private, nicht automatisch geladene WordPress-Optionen je **Laufkennung** geschrieben, aufgeteilt in **100 Ereignisse pro Option**. Neue Läufe behalten die vorherigen Protokolle; keine automatische Löschung. Keine neue WordPress-Tabelle, kein Dateiverzeichnis im öffentlichen Uploads-Pfad, kein eigener Background-Worker.
5. **Was tatsächlich protokolliert wird:** Zeitpunkt, unverwechselbare Laufkennung, Status, Haupt- und Teilphase, echte Fortschrittsschritte, Worker-Ticks, Recherche-/Auswahlzähler, vorliegende Familie-Abdeckung, Blockgründe, Fehlercodes, vorhandene Einzelfehler/Post-IDs, erneute Versuche, öffentlich bestätigter Checkpoint und veröffentlichte Anzahl, eigenständig gespeicherte Verfügbarkeitsprüfungen inkl. Fehlzähler. Es werden **keine API-Secrets, OAuth-Tokens, Zugangsdaten oder vollständigen fremden Produktdaten** gespeichert.
6. **Admin-Downloads:** CSV und JSON für den aktuellen Lauf sowie ein CSV-Export aller vorhandenen Laufprotokolle, inklusive früherer Laufkennungen. Kein öffentlicher Link: Adminberechtigung + WordPress-Sicherheitsprüfung nötig. Alte vor QA12 nur als Kurzgeschichte gespeicherte Läufe werden **ausdrücklich als Kurzbericht** gekennzeichnet; es werden keine erfundenen Einzelereignisse hinzugefügt.
7. **Fehler beim Protokollspeichern:** Nach fehlgeschlagener verifizierter Protokollspeicherung setzt die Adminseite eine deutlich sichtbare Warnung. Ein Logfehler löscht keine Produkte und blockiert nicht den eigentlichen Lauf; vollständig protokollierte Historie darf bei einer DB-Störung ausdrücklich nicht behauptet werden.

## Unverändert (kein Datenverlust, keine doppelte Engine)

- Originaler kanonischer eBay-Run, vorhandene Job-Cursor, bestehende Kandidaten, Produktfamilien, historische Recherchen, 6-Stunden-Frischeprüfung, rein gewerbliche eBay-DE-Herkunftssperre und bisheriger veröffentlichter Produkt-Checkpoint bleiben unverändert.
- Keine Plugin-Deinstallation, kein `delete_option`, kein Katalog-Reset, keine neuen Produkt-Suchregeln und keine Änderung an Amazon, idealo, Otto oder Portal-Design.
- Die frühere QA10 CSV-Auswertung und der QA11-Einzelfehler-/Schlussprüfungstest bleiben enthalten, nicht neu erfunden.

## Verifizierbare Datei- und Testnachweise

- **6.72.323** in WordPress-Pluginheader, interner Konstante und `readme.txt` konsistent.
- ZIP `Pferdeatelier_Affiliate_6.72.323_QA12_KISS_BACKEND_PROTOKOLL_NUR_TEST.zip`: **5.378.589 Bytes**, SHA-256 `bf7e94ad920200efb1746a693cce3b544ddf8b77d8740374d0c2de748d71f9e3`, **66/66 ZIP-Pfade/CRC bestanden, 23/23 PHP-Syntaxprüfungen bestanden**.
- Gegen QA11: **62/66 Dateien byteidentisch**; nur `includes/trait-ppar-ebay-run.php`, `includes/trait-ppar-ebay.php`, Plugin-Hauptdatei und `readme.txt` verändert.
- **61/61 frühere Fachprüfungen** an QA12-Code erneut bestanden; bestehender QA11-Schlussprüfungs-Test bestanden (PHP-Code mit gestellten WordPress-/Providerdaten).
- **14/14 konkrete QA12-Protokollfälle** anhand der echten neuen PHP-Speicher-Methoden: neuer Lauf, identisches Speichern ohne Duplikat, 103 Fortschrittsereignisse, 100er-Chunks, Fehlercode + Post-ID, Run-Supersession, historischer Run bleibt erhalten, DB-Protokollfehler führt zu Warnung, Forschungscursor erhalten, keine Secrets.
- Echter CSV-Exportcode in PHP mit **106 Zeilen** geprüft (historischer Lauf 104, neuer Lauf 1, alter Legacy-Kurzbericht 1); PHP-Warnungen auf null korrigiert.
- Vollständiger Änderungspatch, alle QA12-PHP-Testdateien, Prüf-JSON und Quellenbericht sind im QA-GitHub-Branch gespeichert.

## Ehrliche Grenze / vor produktiver Freigabe

- **Kein echter WordPress-/MariaDB-/eBay-Frontend-End-to-End-Test** durchgeführt. Backend-Geschwindigkeit nicht auf dem echten Server gemessen, Protokollierung bei realem DB-Ausfall nicht erprobt, Zeitbedarf zusätzlicher verifizierter Optionsschreibvorgänge nicht real vermessen. Die Protokolle benötigen künftig Datenbankplatz; keine stillschweigende automatische Löschung.
- QA12 speichert **ab ihrer Installation** Zustandsänderungen; sie kann keine nicht existierenden früheren Rohfehler nachträglich erzeugen. Sogar bei QA12 können PHP-Abstürze **vor** dem Speichern nicht als normales Workerereignis aufgezeichnet werden.
- **Nach Installation auf der getrennten WordPress-Testinstallation** nur prüfen: 1. Version 6.72.323 und schlanke Übersichtsseite; 2. Protokoll-CSV nach echtem Fortschritt enthält Laufkennung/Zeiten/Phasen und alte Laufkennung bleibt bei einem späteren Übergang abrufbar; 3. „Einstellungen/Werkzeuge“ und „Prüfkandidaten“ öffnen die bisherige Funktion, das normale Backend bleibt bedienbar. **Keine bestehende Recherche zurücksetzen**, keinen Lauf absichtlich neu starten nur für den Protokolltest.
- Keine Produktivfreigabe und keine Übernahme nach Hobbydepot/Hab & Bewahr ohne eigenständigen Versions-/Fachvergleich.

**Ablage:** Binär-Test-ZIP in der persönlichen Library `/pferdeatelier/PLUGINS/QA/`. GitHub speichert Quell-Patch, Belege und dieses Protokoll, nicht das binäre Plugin.