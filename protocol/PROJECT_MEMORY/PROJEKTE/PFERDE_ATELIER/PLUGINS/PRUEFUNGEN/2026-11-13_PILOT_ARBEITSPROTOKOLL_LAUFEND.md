# Pferdeatelier KISS – Pilot-Arbeitsprotokoll (laufend)

**Stand:** 13.11.2026. **Arbeit im getrennten Arbeitsverzeichnis**, nicht in vorhandenen WordPress-Plugins oder Live.

## Schritt 1 – Originale gesichert und Grenze bestätigt
- Originale als nur-lesbare Vorlage: PSTE QA 0.57.144.50, SHA256 `7fc98a17e4c2319a66afd23c0ad944a07b4492e7a9982933205f29069fdcd121`, 83 PHP-Dateien; PSERC QA 0.28.71, SHA256 `fd80f7ec3451b437be0eaeedabf2142c5eb1b5130939f7b8dba3b3a2f9d2b59f`, 42 PHP-Dateien.
- Sie sind **QA-Originale**, nicht mit unbekanntem Live-Installationsstand gleichzusetzen.
- Nachgewiesen: PSTE verarbeitet SEO-Freigabe, Titel und Analytics; PSERC enthält K0-5-Felder-Grenze und Export/Import. Bestehender PSERC-Import ruft PPM679 Runtime Gate auf; nicht einfach entfernen.
- **Ziel:** separat installierbarer Pilot mit eigenem Ordner, eigenem Datenbereich, ohne Schreiben/Deaktivieren bisheriger Plugins. Sofortiges Umschalten der produktiven Worker ausdrücklich verboten.
- GitHub-Protokoll dokumentiert nur Arbeitsstand, keine offizielle neue Current-Autorität. Nach jedem relevanten Arbeitsschritt ergänzen.

**Status:** Quellenzuordnung und Pilotentwicklung laufen; keine Installation, keine WordPress-Live-Änderung, noch kein durchgängiger Echtlauf.


## Schritt 2 – Sofortartikel-Quellweg nachgewiesen und Zielvertrag ergänzt
- Tatsächlicher bestehender Einstieg in PSTE `includes/class-pste-admin.php`: `shortPathCreateExport` ab Zeile 1815; manueller Themenimport über `PSTE_Repository::importManualTopics`, ohne neuen DataForSEO-Aufruf, anschließend gezielter PSERC-Compiler nur für ausgewählte Themen. Originalcode: Kurzweg darf nicht den globalen 5.020er-Lauf starten.
- Alte Blockade: `shortPathCompileExactManualSelection` hängt im letzten Schritt ebenfalls an PSERC-/PPM-Artikelplätzen. Der bestehende Kurzweg muss beim Pilot **denselben** zentralen Themenstatus verwenden.
- Zielvertrag **Regel 19** auf GitHub ergänzt: Kurzweg erhalten, keine zweite Themenliste, sofort mit Kategorie-Abdeckung synchronisieren, Titel/K0/Rückgabeformat unverändert.
- Echte Altfreigabe-Datei hat 61 `FREI`-Fälle mit vorhandenen Titeln, aber ohne verbindliche Kategorie/Beitragsart und Planplatz. Diese Werte nicht nachträglich raten. **Sicherer Import hält unvollständige Altaufträge an**, statt sie als READY auszugeben.
- Bestehende Exportvorlage: `PSERC_TEXTMACHINE_METADATA_BATCH_V2` mit genau fünf Feldern; der aktuelle Import `PFERDE_ATELIER_WORDPRESS_IMPORT_V1` hängt über `PPM679_Editorial_Plan_Runtime_Gate::record_readback` am PPM-Plan. Neuer Pilot darf ihn nicht stillschweigend als unverändert PPM-frei behaupten.

**Stand:** GitHub-Zielvertrag und Arbeitsprotokoll fortgeschrieben. Nächster Schritt: ausschließlich neue Pilotdateien im eigenen Ordner, keine Änderungen an alten Pluginquellen.


## Schritt 3 – Installierbarer, strikt isolierter Pilot erstellt und lokal geprüft
- **Ein eigenständiges Plugin-Verzeichnis:** `portal-kiss-auftragszentrale-pilot`, Version `0.1.0-test`; bestehende WordPress-Plugins bleiben vollkommen unangetastet.
- **Nur isolierte Test-WP:** Aktivierung gesperrt, solange die Website nicht ausdrücklich `staging`, `development`, `local` oder per Testkonstante als Test ausgewiesen ist. Kein Autostart, kein Cron, keine Änderung des WordPress-Frontends, keine Anfrage an DataForSEO.
- **Ein neuer Pilot-Auftragsbereich:** `pkiss_pilot_orders_v1` ausschließlich auf der Testkopie. Freigegebene Themen importieren, Sofortartikel anlegen, externen Titel zuordnen, Charge verbindlich reservieren, gleiche Charge jederzeit erneut herunterladen, fertigen K0-Rücklauf als Entwurf zuordnen.
- **Daten-/Formatgrenze:** `PSERC_TEXTMACHINE_METADATA_BATCH_V2` mit genau fünf unveränderten Feldern und Original-Hash; `PFERDE_ATELIER_WORDPRESS_IMPORT_V1`/alte System4-Rückgabe als Eingabeformate.
- **Altfälle:** Die 61 tatsächlich `FREI`-Freigaben ohne Kategorie-/Beitragsart-Beleg sind sicher übernommen, aber als `METADATEN_OFFEN` gehalten. Drei echte bestehende K0-Metadatenbelege ergänzen genau die drei zugehörigen Fälle, ohne neue Fachentscheidung und ohne 64 statt 61 Aufträge zu erzeugen.
- **35/35 lokale PHP-Gegenproben PASS** mit isolierten WordPress-Funktionsnachbildungen: alter 61er Bestand, ursprünglicher 3er-K0-Handoff, echter SHA-Abgleich, Sofortartikel, Titelrückgabe, doppelte Exporte, Lock bei gleichzeitigem Zugriff, Wiederholung früherer Exportchargen, fehlerhafte Rückgabe, unveränderter Importvertrag, Entwurfsstatus, doppelter Import, zweites Portal.
- **Bestandsoriginale unverändert SHA-256:** PSTE `7fc98a17e4c2319a66afd23c0ad944a07b4492e7a9982933205f29069fdcd121`, PSERC `fd80f7ec3451b437be0eaeedabf2142c5eb1b5130939f7b8dba3b3a2f9d2b59f`.
- **Installierbare TEST-ZIP (nicht Live):** `Portal_KISS_Auftragszentrale_PILOT_0.1.0_NUR_TEST_20261113.zip`, SHA-256 `6d9fa7eb9ffb0bc7b7d1f78ee03ab33156e2ff5915bf63d13111122c80066019`, 11.259 Bytes, WP-Pluginordner mit eigener README, ZIP-Integrität PASS.
- **Getrenntes Gegenprobenpaket:** `Portal_KISS_PILOT_0.1.0_PRUEFNACHWEISE_20261113.zip`. Beide ZIPs plus `PILOT_PRUEFBERICHT_20261113.md` dauerhaft in der Files-Library unter `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/` abgelegt und zur Wiederaufnahme referenziert.

### Verbindlich OFFEN – keine fertige Komplettablösung behaupten
1. Vorhandener PSTE-Recherche-/Freigabe-Worker und **vollständiger** kurzer Dienstweg (`PSTE_Repository::importManualTopics` mit Bestands-/Kategorieprüfung) müssen **noch** in die Einplugin-Grenze aufgenommen werden. Der Pilot ermöglicht momentan nur bereits genehmigte Freigabedateien und manuell vorentschiedene Sofort-Aufträge; keine automatische neue SEO-Freigabe.
2. Externer MINI-Titelprozess selbst bleibt unverändert; Testpilot kann den fertigen Titel zuordnen, aber hat noch keine automatische Auslese des gewohnten Titel-Rückgabeformats.
3. Das tatsächliche WordPress-/K0-Ende-zu-Ende-Ergebnis steht aus. Simulierter Entwurfsimport **ist kein echter K0- oder WordPress-Test**.
4. Der Test-Importer ersetzt die alte **PPM-Buchung** intern bisher nicht in seiner vollständigen bisherigen Schutzwirkung. Ohne native PPM-/Guard-Quell-/Laufprüfung nicht als Live-Ersatz freigeben.
5. Dateiinterne Einzelfehler dürfen langfristig nicht andere gültige Rückläufe stoppen. Der Pilot stoppt bei einem ungültigen Eintrag derzeit noch die gesamte Datei; vor einer vollen Freigabe gegen Zielvertrag anpassen.
6. Kategorie-Abdeckungsfunktion in PSTE ist als Original nachgewiesen, im Pilot derzeit noch nicht als allgemeiner Report integriert.
7. Erforderlich: realer TEST-WP-Durchlauf mit vorhandenen realen drei Aufträgen und 20er-Charge, echter Kurzweg, Titel, Rückgabe, Teilabbruch und Veröffentlichungs-/Dubletten-Sperren. **Bis dahin kein Ersatz der Altplugins.**

### Nächste Handlung
**Nicht neu beginnen:** Originale + Pilot-ZIP aus der genannten Library lesen. Dann die echten PSTE-Aufrufe für Recherche, redaktionelle Freigabe, Kurzweg und Titel-Anbindung **nur dort** aufnehmen, wo sie im aktuellen Workflow wirklich gebraucht werden. Danach mit echter Test-WordPress-Datenbank anhand ursprünglicher Quellen und des unveränderten K0-Vertrags testen. Keine Live-Änderung. Kein zusätzlicher SEO-/Qualitäts-Worker.

**Status nach Schritt 3:** Testpilot gebaut und lokal geprüft; GitHub-Dokumentation aktualisiert. WordPress-Installation weiterhin nicht vorgenommen.
