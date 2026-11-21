# 19.11.2026 – Hab Texterstellung 0.4.31.5 – ORIGINAL-Prüffehler bei leerem Themenbestand

**Eingang:** `Einrichtung angehalten: PSTE_EDITORIAL_RULESET_RAW_KEYWORD_INVARIANT_FAILED. Gespeicherter Stand bleibt erhalten; Fortsetzen ist möglich.` Nach zuvor installierter 0.4.31.4 und funktionierendem Einrichtungsklick. Benutzer möchte weder Neustart noch halbfertige Pluginkopien.

## Tatsächlich nachgewiesene Ursache (isoliert, keine Behauptung über Live-DB)
- Der alte `PSTE_Safe_Migration_Job` überspringt bei `topic_count=0` die Phase `EDITORIAL_RAW_BASELINE_BATCH` und lässt `editorial_init.raw_source_chain_sha256=''`. Spätere Original-Abschlussprüfungen verwenden korrekt den ursprünglichen Seed `PSTE_Repository::editorialRawSourceChainSeed()`.
- Die vorhandene Originalmethode `editorialMigrationVerifyComplete` vergleicht beide trotzdem direkt und wirft exakt `PSTE_EDITORIAL_RULESET_RAW_KEYWORD_INVARIANT_FAILED`. Der Fehler wurde mit echter unveränderter **0.4.31.4** reproduziert.
- **Achtung:** Ein Error-Code allein sagt nicht, wie viele Datensätze die laufende WordPress-Datenbank enthält. Der lokale Nachweis betrifft ausdrücklich den leeren Fall. Nicht behaupten, der Benutzer habe sicher 0 Daten in der tatsächlichen PSTE-Thementabelle.

## Minimaler Eingriff ohne neue Architektur
- Hab-Version **0.4.31.5** aus der exakten 0.4.31.4-Installations-ZIP; nur in der **vorhandenen** Klasse `PSTE_Repository`, Methode `editorialMigrationVerifyComplete` ein bereits bestehender Seed-Sonderfall ergänzt, der nur gilt, wenn `expected===0 && cursor===0 && raw_source_chain===''`. Restliche strenge Hash-, Datenbankzählungs- und Beziehungsprüfungen **unverändert aktiv**.
- Diese Methode wird sowohl vom Originalschritt `EDITORIAL_CORE_VERIFY_FINAL` als auch `FINAL_VERIFY` verwendet. **Auch bestehende PAUSED_ERROR-Jobs mit alter leerer Quelle können ohne Reset mit identischer UUID fortfahren.**
- Genau drei vorhandene ZIP-Dateien geändert: `original/pste/includes/class-pste-repository.php`, `texterstellung.php` (Version/Anzeige), `README-TESTINSTALLATION.txt` (Version/Bedienhinweis). **84/87 Paketdateien bytegleich**. 0 neue/gelöschte Plugin-Dateien. Kategorien, MINI, K0, alle anderen Recherche-/Migrationsschritte, Pferdeatelier, Universal Blanko, Robotik und Wassertechnik **unverändert**.

## Wirklich durchgeführte Gegenprüfung
- Vorher (Original-0.4.31.4): tatsächlicher error `EXPECTED_OLD_FAILURE_REPRODUCED` beim leeren Zustand.
- Danach (0.4.31.5): 16 Prüfpunkte inklusive Nullzustand, falschem Hash, falschem Cursor, nichtleerem Fall, Zählungsdrift, echte PAUSED_ERROR-Option, gleiche Job-UUID, Fortschritt durch `EDITORIAL_CORE_VERIFY_FINAL` → `FINAL_TOPIC_VERIFY_BATCH` → `FINAL_VERIFY` → `FINALIZE`. **Nicht** der reale Abschluss auf der öffentlichen WordPress-Seite.
- Bestehende Original-AJAX-/Schutztests 19/19 bestanden, Browser-Button-Tests 28/28 bestanden. Alle **78 PHP**, **8 JSON** und **87 CRC ZIP** geprüft.
- Dateistand verifiziert: ZIP `Texterstellung_HAB_UND_BEWAHR_0.4.31.5_LEERE_THEMEN_MIGRATION_FORTSETZEN.zip`, **516790 Bytes**, SHA256 `7e80f7f08f5ca628d9cf803d6d805b0848437230ae4438d131ca280976db742a`, unverändertes WordPress-Plugin-Verzeichnis `texterstellung-hab-und-bewahr/`.

## Abgelegt
- **Nachweislich erfolgreiche Library-Uploads:** `/hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEN/04315/` mit vollständigem installierbarem WordPress-ZIP, vollständigem originalen Quelldateibestand **innerhalb der ZIP**, `RELEASE_STAND_04315.md`, `QA_04315.json`, exaktem Repository-Diff, reproduzierbarem Bauskript und Original-/Korrektur-/AJAX-/Button-Testskripten. Vorige 0.4.31.4 separat erhalten.
- Geändert wurde **nur** die eigene Hab-Variante; Universal 0.4.31.1 in den Robotik-/Wasser-Büros bleibt weiterhin eine unfreigegebene jungfräuliche Arbeitskopie.

## Einziger notwendiger Nutzerweg
Die installierte Hab-Texterstellung 0.4.31.4 **überinstallieren** mit 0.4.31.5 (nicht löschen), unter `Texterstellung → Recherche` denselben gespeicherten Migrationslauf fortsetzen. Kein Reset, keine zusätzliche kostenpflichtige Recherche, keine neue Kategorieentscheidung.

## Wahrheitsgrenze
Reale WordPress-Datenbank / Datenzahl, tatsächliche Migrationsphase und produktive K0-Annahme hier nicht ausgelesen. Wenn der Fehler trotz Version 0.4.31.5 weiter auftritt, muss der konkrete gespeicherte Stand **read-only** betrachtet werden; die Prüfung für **nichtleere** oder inkonsistente Themen bleibt absichtlich gesperrt. Keine weiteren unbewiesenen Universalpatches.