# Pferdeatelier eBay – KISS zusammengeführter Gesamtworkflow, 10.11.2026

**Staging/QA, NICHT installieren, keine WordPress-Änderung, keine GitHub-Current-Freigabe.** Original: direkt geprüfte ZIP 6.72.319. Der pausierte WordPress-Lauf wurde nicht berührt.

## Umsetzung (eine Arbeitskopie, keine zweite Engine)

1. Gespeicherte und noch sicher gültige eBay-Angebote laufen durch die **vorhandene kanonische BUSINESS-Klassifikation, Auswahl und Veröffentlichung**. Keine zusätzliche Veröffentlichung, Tabelle, API oder Scheduler.
2. Ein **bereits mitten in business_prune angehaltener 319-Lauf** bekommt eine einmalige, eng begrenzte Bestandsprüfung mit Cursor innerhalb seines bestehenden Auswahlzustands. Bei bestätigten neuen Familien verwendet er den bestehenden Materialisierungsweg; bei keinen Treffern geht die bestehende Prune-Phase ohne Wiederholung weiter. Neue Läufe haben ihren Bestandscheck bereits in der Vorbereitung und wiederholen ihn nicht.
3. Der vorherige parallele 319-Controller (fünf PHP-Controllerfunktionen, drei darin eingebettete JS-Helfer und faktisch unerreichbarer AJAX-Hook) wurde nach internem Referenzaudit entfernt. **Seine fachliche Funktion ist im kanonischen Ablauf erhalten**; die alte WP-Option `ppar_ebay_local_reuse_v319` bleibt **gespeichert und lesbar**. Ein neuer AJAX-Endpunkt wird nicht eingerichtet. Admin: ein Fortsetzen-Knopf, kein extra Bestandsstart.
4. Der gemeinsame Fortschrittsfingerabdruck berücksichtigt den Nachhol-Cursor; kein falscher Stillstand. Fehler bei einer Familie bleiben lokal, ein ungültiger Gesamtkatalog ist eine sichere Stop-Bedingung.
5. **Schreibbestätigung:** `ebay_run_save` liest jeden zentralen Checkpoint nach; bei verweigertem Speichern wird kein Erfolg/Fortschritt gemeldet. Beim Übergang zu einem neuen Lauf entfällt das bisherige **Löschen vor erfolgreichem Ersatzspeichern**. Credential-Optionen, Produktquellen, alte Run-/History-Optionen und öffentliche Daten sind nicht geändert.

## Harter Vergleich

66/66 Originaldateien erhalten. Genau vier PHP-Dateien verändert (`pferdeportal-affiliate-router.php`, `includes/class-ppar-admin-kiss.php`, `includes/trait-ppar-ebay.php`, `includes/trait-ppar-ebay-run.php`); **43/43 Nicht-PHP-Dateien bytegenau unverändert**, inklusive Kataloge, Assets und historischer Sicherungen. Keine neue PHP-Datei, Datenbanktabelle, Quelle oder Cron.

## Nachweise

- PHP-Lint 23/23 bestanden; integrierte Bestandsauswahl 16/16; Resume-Migration 22/22; zentraler Ablauf 10/10; echte Fortschrittszählung 8/8; Persistenz inkl. verweigertem Schreiben 11/11.
- Historische Fach-Regression 49/49, kanonische Workflow-Simulation, 14 HTTP-Szenarien, Bootstrap 341 Methoden/143 Hooks, unveränderte Frontend-Gates erfolgreich.
- Testkopie: persönliche Library `/pferdeatelier/PLUGINS/QA/EBAY_319_KISS_EIN_WORKFLOW_STAGING_NICHT_INSTALLIEREN_20261110.zip`; SHA256 `13d576f095a72dc2b0ffd2039daa8a78e234d8c43a3c2a14dcdb0f2904b7ea18`.
- Exakter Codevergleich: `/pferdeatelier/PLUGINS/QA/EBAY_319_KISS_EIN_WORKFLOW_20261110.patch`; SHA256 `f408f37ebc2c890c08cb8492e58cc6160e598581dff3a3ea1df106d7e7a501c5`.
- Vollständiger QA-Bericht: `/pferdeatelier/PLUGINS/QA/EBAY_319_KISS_EIN_WORKFLOW_QA_20261110.md`, 503-Zeilen-Log `EBAY_319_KISS_EIN_WORKFLOW_ABNAHME_20261110.log`, dazu Testfälle gesichert.

## Nicht freigegebene Grenze

Es existiert **keine** eigene reale WordPress-End-to-End-Abnahme inklusive WordPress-Persistenz, echten eBay-Quellen und sichtbarer richtiger Produktseite. Deshalb nur isoliertes Staging, **kein 100%-Funktionsversprechen für die Installation**, kein Plugin-Update und keine Wiederaufnahme des pausierten echten Jobs. Vor produktiver Freigabe braucht es eine isolierte WordPress-Testkopie mit einem passenden, einem unpassenden Angebot und einem simulierten Schreibfehler. Kein unabhängiger zweiter Workflow.
