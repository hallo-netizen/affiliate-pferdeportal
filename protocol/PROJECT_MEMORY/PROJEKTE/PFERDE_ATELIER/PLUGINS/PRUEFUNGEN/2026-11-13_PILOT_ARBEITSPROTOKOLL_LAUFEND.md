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
