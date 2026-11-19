# 19.11.2026 – Texterstellung 0.4.24.4: ORIGINALFEHLER REPRODUZIERT, BEGRENZT REPARIERT

**Original-LIVE-Fehlerrückmeldung des Betreibers:** Beim Klick `Recherche-Einrichtung abschließen` wurde `PSTE_EDITORIAL_RULESET_RAW_KEYWORD_INVARIANT_FAILED` angezeigt, gespeicherter Migrationsfortschritt erhalten. Frühere Aussagen zu „vollständigen“ Tests waren unbegründet: die bisherige Simulation enthielt keine Null-Themen-Migration.

## Exakte nachgestellte Ursache im Original 0.4.24.3
- In `original/pste/includes/class-pste-safe-migration-job.php` war `EDITORIAL_INIT` bei `editorial_total=0` direkt nach `EDITORIAL_VARIANT_PLAN` gesprungen und **hat `EDITORIAL_RAW_BASELINE_BATCH` übersprungen**.
- In `original/pste/includes/class-pste-repository.php` prüft `editorialMigrationVerifyComplete()` den übersprungenen Vergleichswert zwingend gegen die echte Leerkette.
- Die unveränderte Originalfunktion wurde mit Nullzeilen ausgeführt und warf **exakt den live gemeldeten Fehlercode**.
- **Grenze:** Live-WordPress-Themenanzahl und Fehlerphase liegen nicht als aktuelle DB-Auswertung vor; derselbe Fehlercode ist auch bei realen Rohdatenabweichungen möglich. Kein unbedingter Kausalbeweis für die Live-Datenbank.

## Fix ohne Neubau und ohne Umgehung
Neues WordPress-Plugin `Texterstellung_Hobbydepot_0.4.24.4_MIGRATION_NULLBESTAND_FIX.zip`, SHA256 `8ee94512c7b8e9dc84d82bdc65b9641aea7057825528709b1546f369eb7e8e69`, 504008 Bytes, Ordner `texterstellung-hobbydepot/`.
- Nur 3 alte Dateien geändert (84/87 bytegleich): vorhandener Migrationsjob führt künftig den normalen Rohdaten-Baseline-Schritt **immer** aus; vorhandene Repository-Verifikation erlaubt die fehlende Altfassung-Baseline **nur** für 0 Themen, Cursor=0, exakt richtige Leerkette und überprüft danach die Datenbestände unverändert; Pluginheader 0.4.24.4.
- Gespeicherter `PAUSED_ERROR`-Job kann **mit unveränderter UUID** über den vorhandenen Fortsetzen-Button weitergeführt werden. Keine Neuanlage der Aufträge, kein automatischer Recherchestart.
- Andere Datenabweichungen, geänderter Themenbestand, falsche Kette und falsche Cursor weiterhin **BLOCKED**. Keine Änderung an DataForSEO, K0, MINI, Rechercheentscheidungen, Entwurfsimport oder Publishschutz.
- 12 Original-PHP-Funktionstests PASS, insbesondere **alter PAUSED_ERROR mit 0 Themen → ENDSTATUS COMPLETE** in WordPress-/MySQL-Mocks; 2 Testfälle am wirklich aus PHP gerenderten JS + AJAX PASS; 78/78 PHP Syntax, 8/8 JSON, ZIP 87/87, Version und WordPress-Ordner korrekt.
- **KEIN authentifizierter WordPress-Endlauf** und kein Nachweis, dass die Live-Datenbank tatsächlich 0 Themen hat. Nicht als 100%-Livefix behaupten.

## Ablage und Bedienung
- Erfolgreich im echten Pluginbüro `/Hobby Depot/Plugin-Büro/Texterstellung_Hobbydepot_0.4.24.4_MIGRATION_NULLBESTAND_FIX.zip` gespeichert.
- Fachbüro identische ZIP `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/`.
- Protokoll `/Hobby Depot/Plugin-Büro/Texterstellung_0.4.24.4_PRUEFBERICHT.md`; getrennte eigene Datei `/Hobby Depot/Plugin-Büro/Texterstellung-CURRENT.md` auf 0.4.24.4 aktualisiert. Alte 0.4.24.3 im Archiv belassen.
- **Nächster einzelner Nutzerweg:** Backup sicherstellen → ZIP 0.4.24.4 in WordPress über **Ersetzen** einspielen → `Texterstellung → Recherche → Vorhandene Einrichtung fortsetzen` einmal drücken. Ohne DataForSEO-Kosten. Wenn es stoppt: **nicht blind wiederholen**, echte Jobphase/Zeilenanzahl aus dem Bestand ermitteln. Keine zusätzliche vorzeitige Pluginversion.
