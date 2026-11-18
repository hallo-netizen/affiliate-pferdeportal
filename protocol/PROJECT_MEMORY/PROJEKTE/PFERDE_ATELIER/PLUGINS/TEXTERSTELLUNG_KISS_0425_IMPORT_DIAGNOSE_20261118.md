# Pferdeatelier – Texterstellung KISS 0.4.25 – Diagnose-Fix

Datum: 18.11.2026; Status: vollständiges **Test-Plugin**, keine Livefreigabe.

## Original physisch geprüft
- Benutzerdatei: `Texterstellung-0.4.24.zip`; WordPress-Plugin `Texterstellung`, Header-Version `0.4.24`; Ordner `texterstellung/`.
- 88 ZIP-Dateien, 78 PHP; CRC OK. SHA256: `e75acd201e8dbb5791c0d9934cedf2273f6dbb7e32217cc180bf137f46a9076f`.
- Unveränderte Originalkopie in der persönlichen Dateiablage: `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/Texterstellung-0.4.24_ORIGINAL_UNVERAENDERT.zip`.

## Versionsupdate und nachgewiesener Fehler
- Bisheriger Rückimport von zwei echten K0-Artikeln: 0 importiert, 2 geblockt. Diagnose speicherte fälschlich nur `ORIGINAL_PSERC_IMPORT_BLOCKED`, weil die exakte `PSERC_SYSTEM4_...`-Kennung beim Ereignis gekürzt wurde.
- Neues vollständiges Test-Plugin: `Texterstellung-0.4.25-DIAGNOSE-PFERDEATELIER-TEST.zip` in **derselben persönlichen Dateiablage**.
- SHA256: `585f18a491c63ac9e06be1996037f3de4578512537ae786bf8f1dae9b12ea9ac`.
- Exakt vier Dateien von 88 geändert: Hauptdatei (Version und Originalfehlerübergabe), vorhandene Diagnose (sichere Original-Details und Original-Maschinencodes, 500 Ereignisse, sichtbarer letzter Fehler), ursprünglicher PSERC-Draft-Importer (nur vorhandenen WP_Error-Code zurückgeben), README. **84 Dateien unverändert.** Kein neuer Workflow, keine zweite Inhaltsentscheidung, kein K0-Eingriff.
- PSERC-Diagnose enthält nach Fehlern Kategorie, Original-Feld, vorhandene WordPress-Beitrags-ID, Konfliktart/-status, tatsächliche Rückleseabweichungen und ggf. WP_Error-Kennung. Kein Artikelinhalt/Passwort übertragen.

## QA / Reichweite
- PHP-Lint 78/78; ZIP CRC PASS; Diff 84 identische Dateien; 22/22 PHP-Integrationstests mit den **zwei echten hochgeladenen K0-Artikelpaketen** und lokal nachgebildetem WordPress bestanden: fehlende Kategorie, Kollision, WP-Insertfehler, Readback-Mismatch mit Rollback, zwei erfolgreiche Drafts und weiterhin funktionierender Statusübergang.
- **Keine echte Installation oder echter Import auf oliver-beil.de durchgeführt.** Die tatsächliche Ursache der letzten beiden geblockten Artikel ist erst nach einem neuen Importversuch und anschließender Diagnose belegt.
- Nur für isolierte WordPress-Testinstallation oliver-beil.de. pferde-atelier.de live sowie Hobbydepot/Hab & Bewahr unverändert.
- Installationsfolge: vollständige 0.4.25-ZIP über die bestehende 0.4.24 **ersetzen, nicht löschen** → ein Rückimportversuch mit unveränderter K0-JSON → Texterstellung / Diagnose / JSON herunterladen.
- Prüfbericht separat: `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/Texterstellung-0.4.25-PFERDEATELIER-DIAGNOSE-PRUEFBERICHT.md`.

## Korrektur früherer Falschaussagen
Frühere Aussagen, die 0.4.24-Datei sei nicht vorhanden oder nicht zugänglich, waren falsch. Die Datei wurde vom Nutzer am 18.11.2026 direkt bereitgestellt, geöffnet und bytegenau gesichert.
