# Pferdeatelier eBay – KISS Zwischenstand QA5, 10.11.2026
**STATUS: isoliertes Staging; KEIN WordPress-Release, nicht installieren.**

## Zielvertrag unverändert
Eine eBay-Steuerung, eine zentrale Produktauswahl, vorhandene Angebote zuerst; nur echte Lücken gezielt suchen; bestehende Daten, API-Zugänge, Produkte, historische Sicherungen und alle Funktionen behalten. Fehler einzelner Familien dokumentieren und Rest weiterverarbeiten. Kein zweiter Worker, keine neue Tabelle, keine Zwangsbefüllung aller 298 Familien. Pausierten Live-Lauf nicht verändern.

## Bereits erledigt und nicht erneut bearbeitet
QA4 enthält den einen zentralen Ablauf anstelle des zusätzlichen 319-Controllers, bestehende Mehrfachzuordnung, sichere Checkpoint-Speicherung, Pause/Fortsetzen, Einzelproblem-Isolation, Bestandsprüfung und bereits optimierte Datenlesung für Materialisierung und öffentliche Abdeckung. QA4 bleibt die Baseline; die hier festgehaltene Änderung betrifft nur die noch unnötig umfangreiche Bereinigung.

## QA5: gezielte Bereinigung begrenzen
In `includes/trait-ppar-ebay.php`, Methode `ebay_selection_prune_business_batch`: Bei einer begrenzten eBay-Nachsuche ruft die vorhandene Datenbankabfrage jetzt nur die Produktfamilien dieses Teilplans ab, statt vor dem späteren Skip sämtliche BUSINESS-Angebote zu laden. Normale Vollauswahl, leere Zielmengen und Fehlerbehandlung verwenden unverändert den alten Pfad. **Keinerlei neue Entscheidung oder Funktion entfernt.**

**Original-PHP-Funktion QA4 gegen QA5 mit identischem simuliertem Bestand verglichen:** neun Szenarien, alle gleichen Produktaktionen/Abschlüsse, einschließlich Fortsetzung, Leerfall, Checkpoint, normaler Vollbereinigung und Datenbankfehler. Beispiel 2.000 Angebotszeilen mit 29 betroffenen Zeilen: **41 → 1 Datenbankabfrage**, **2.000 → 29 gelesene Zeilen** (nur lokaler Test, keine Live-Laufzeit). Nach Abschluss kann der rein interne Cursor früher enden, da irrelevante Restzeilen nicht mehr gelesen werden.

**Regressions:** acht bestehende Prüfscripte erfolgreich (u. a. 49 ältere Fachfälle, Speicherung/Resume und Einzelfehler); alle 23 PHP-Dateien syntaxgeprüft. QA4 → QA5: **66/66 Dateien erhalten, 65 byteidentisch; ausschließlich `includes/trait-ppar-ebay.php` geändert.** Keine Tabellen, Einstellungen, Zugangsdaten, Kataloge oder Sicherungen verändert.

## Quellen, Persistenz und Freigabegrenze
- Quelländerung (reproduzierbarer Patch im GitHub-Büro): [QA5 Patch](./EBAY_672319_KISS_QA5_AUFRAEUMEN_NUR_ZIELFAMILIEN_20261110.patch).
- Vollständige binäre QA5-Kopie und Tests **persönliches Pluginbüro Library**: `/pferdeatelier/PLUGINS/QA/EBAY_319_KISS_EIN_WORKFLOW_QA5_PRUNE_NICHT_INSTALLIEREN_20261110.zip`, `EBAY_319_KISS_QA5_GESAMTWORKFLOW_ZWISCHENSTAND_20261110.md`, `EBAY_319_KISS_QA5_PRUNE_PARITAET_20261110.json`, `EBAY_319_KISS_QA5_REGRESSION.log`, Paritätstest und Runner.
- QA5-ZIP SHA256 `561e5a4ef7148b351579aec8f67073bbf0805c5d1e1bc79d2d7b8c9444c26dc3`. Patch SHA256 `518d2e77fbd4dd725c92e29c0b39bd5c08928ae0a3ee530c70b6bd42c698c916`.
- Auf die produktive WordPress-Installation gab es **keinen** Zugriff und keinen Live-Eingriff. Echte Datenbank-Persistenz und öffentliche Anzeige bleiben die Freigabehürde. Kein vorgetäuschter WP-End-to-End-PASS.

**Nächste Bearbeitung:** Nicht schon erledigte Aufgaben wiederholen. Erst prüfen, ob die QA5-Optimierung mit echtem WordPress auf dem isolierten Testsystem funktioniert; vor Live-Freigabe kompletten Weg bis zur konkreten Produktseite prüfen.
