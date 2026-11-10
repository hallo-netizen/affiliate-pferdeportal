# Live-Vorbereitung: verlustfreie PSTE/PSERC-Verschlankung (10.11.2026)

STATUS: NUR QA. Keine Live-Installation, keine Daten/Optionsänderungen oder Codeentfernung.

## Gegenüberstellung
- Live (vom Betreiber bestätigt): PSTE 0.57.120, PSERC 0.28.43.
- TEST (echter Datei-Handoff mit 3 Themen geprüft): PSTE 0.57.144.32, PSERC 0.28.60.
- Die Originalpakete von Live .120 und .43 und ein aktueller Live-Datenbankexport liegen hier NICHT vor: Ein vollständiger Upgrade-/Datenkompatibilitätsbeweis fehlt. Keine Live-Freigabe.

## Quellprüfung
- PSTE .32 hat 121 Archivpfade und 83 PHP-Dateien (ca. 24.009 Zeilen), darunter registrierte Admin-/AJAX-/Cron-/GSC-/Recherche-/MINI- und Migrationsfunktionen.
- PSERC .60 hat 63 Archivpfade und 43 PHP-Dateien (ca. 5.467 Zeilen); der vorhandene K0-Metadaten-Export bleibt der einzige bewiesene Dateihandoff.
- PSTE_Admin::hideInternalCompilerMenus blendet PSERC-Menüs aus, nicht deren Funktionen. Beim Vereinfachen muss der K0-Download bequem erreichbar bleiben.
- PSERC .60 registriert in der Hauptdatei keinen Aktivierungs-, Deaktivierungs- oder Migrationshook, enthält jedoch weiterhin Legacy- und Schutzfunktionen.
- Echte PHP-Simulation von PSTE_Plugin::activate aus .32 mit einem alten Schema 11: PASS; exakt ein Bootstatus-Eintrag, Status PENDING/AWAITING_MANUAL_MIGRATION, keine DB-/Optionslöschung in dieser Aktivierungsvariante.

## Konkreter Datenverlust-/Funktionsrisikopunkt
- Die später manuell gestartete PSTE_Plugin::safeMigrationPreparation ruft cleanupRemovedLiveWorkflow auf. Diese sichert sechs alte Optionswerte in einem gehashten Archiv und entfernt nach Rücklesen die ursprünglichen sechs Optionsschlüssel durch delete_option.
- Das ist gerade KEIN Nachweis unveränderter Datenzustände. Auf LIVE weder Migration blind starten noch alte Rechercheoptionen löschen. Erst alte Daten, Archiv-Rücklese und abhängige Leser in einer Kopie prüfen.
- PSTE uninstall.php kann bei ausdrücklich gesetzter PSTE_ALLOW_DATA_DELETION=true Tabellen und Optionen löschen. Während des Upgrades beide Plugins nicht deinstallieren, sondern die geprüften Verzeichnisse mit gesichertem Rückfallstand aktualisieren.

## KISS-Oberfläche ohne Funktionsverlust
- Normalweg: Keyword/Bestand, externe einmalige Entscheidung/Titel, Kategorie/Redaktionsbüro, bisherige K0-JSON.
- Sonderfunktionen (alte Themen, Recherchen, Import, Einstellungen, Diagnosen, GSC, Speicherwartung) unter einem vorhandenen Expertenbereich erreichbar lassen, ohne PHP-Hooks zu streichen.
- Technisch nachweislich verwaiste Funktionen erst NACH Referenzprüfung in PHP, WordPress-Actions/AJAX/Cron, Options-/Tabellen-/Archiv- und Rückfallaufrufen auf einer Kopie entfernen.

## Nächste Freigabeschritte
1. Exakte Live-Originalpluginverzeichnisse .120/.43 und vollständigen aktuellen Live-Datenbestand read-only sichern und inventarisieren.
2. Eine isolierte Kopie genau dieses Live-Standes wiederherstellen. Erst auf dieser Kopie Versionssprung und etwaige manuelle Migration testen.
3. Nachweis: Null verlorene Inhalte/Recherchen/Pläne, sämtliche genutzten Funktionen erreichbar, negative Sicherheitstests PASS, dasselbe K0-V2-Format mit 5 Feldern und gültiger Kategorie.
4. Erst dann Live-Upgrade mit geprüfter Datensicherung und Rückfallplan. Keine Artikelproduktion oder WordPress-Core-Änderung.

LIVE_UPDATE_APPROVED=false; ORIGINAL_LIVE_PACKAGES_VERIFIED=false; LIVE_DB_MIGRATION_PROVEN=false; K0_TEST_EXPORT_CONFIRMED=true.
