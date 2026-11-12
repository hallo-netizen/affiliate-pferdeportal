# PSERC 0.28.59: sichtbarer Fortschritt nach BLOCKED – vor Installation simuliert, 10.11.2026

## Echter Anwenderbefund
Auf der **WordPress-Testseite** mit **PSERC 0.28.58** zeigt der Screenshot zuerst den gespeicherten Fehler `PSERC_PLAN_LIVE_EDITORIAL_PLAN_CHANGED_BEFORE_ACTIVATE`. Nach erneutem Klick ist die Schaltfläche grau, aber die Ansicht zeigt **keinen neuen Fortschritt**. Der Anwender kann daher nicht erkennen, ob der Vorgang arbeitet, gestoppt wurde oder hängen geblieben ist. Der vorherige Ablaufstatus wurde in der Oberfläche durch die rote Fehlermeldung ersetzt; das ist **kein Nachweis gelöschter Daten**.

## Ursache – tatsächlicher .58-PHP-Code
`includes/class-pserc-admin.php`, `PSERC_Admin::page()`: Der DOM-Bereich `id="pserc-plan-text"` wird **ausschließlich im Nicht-BLOCKED-Zweig ausgegeben**. Gleichzeitig hängt `renderJobScript()` den bestehenden AJAX-Fortschritt immer an diese ID und prüft sie nur mit `if(status)`; bei BLOCKED ist sie `null`. Beim Anklicken wird der Knopf deaktiviert. Bei BLOCKED oder Netzwerkfehler beendet das JS den Lauf, **aktiviert den Knopf aber nicht erneut**. Der Hintergrundplan und K0-Export waren nicht die Ursache dieses Sichtbarkeitsfehlers.

## Kleinstmögliche .59-Korrektur (kein Neubau)
- **Nur bestehende Admin-PHP-Datei** in einer isolierten Kopie des auf TEST installierten .58 geändert; dazu Versionskopf und unverändertes bestehendes Paketintegritätsmanifest neu gebunden.
- Den **einen vorhandenen** Statusbereich immer ausgeben, ausdrücklich auch nach `BLOCKED`. Vorherige Fehlermeldung und zuletzt gespeicherte Themen-/Geeignet-/Geprüft-/READY-Zahlen bleiben sichtbar.
- Vor dem AJAX-Klick sofort `START ANGEFORDERT`, danach pro Antwort `LÄUFT` samt echter Phase und echten Zählern; abschließend `GESTOPPT`, `VERBINDUNG UNTERBROCHEN` oder `FERTIG`.
- Bei Abbruch/Verbindungsfehler dieselbe Schaltfläche wieder freischalten; alter gespeicherter Status bleibt erkennbar.
- **Keine neuen AJAX-Endpunkte, Worker, Tabellen, Optionen, Datenmigrationen oder Datenlöschungen.** Keine Änderungen an `class-pserc-plan-compile-job.php`, `class-pserc-plan-dependency-fingerprint.php`, `class-pserc-plan-snapshot-store.php`, der bisherigen Exportfunktion, K0, PSTE, PSERC-Reader oder den alten Hooks.

## Tatsächlich ausgeführte Simulation – keine bloßen Codebehauptungen
1. PHP-Admin `PSERC_Admin::page()` mit synthetischem früherem BLOCKED-Job und gültigem, nun veraltetem altem Snapshot ausgeführt: genau ein Fortschrittselement und alter Fehler sichtbar **PASS**.
2. Derselbe originale PHP-Admin mit RUNNING-Job ausgeführt: Fortschrittselement vorhanden, alte Backend-Nach-K0-Importfunktion weiterhin vorhanden **PASS**.
3. Browser mit echten von PHP erzeugten Seiten und simulierten JSON-AJAX-Antworten: `RUNNING→TOPICS→BLOCKED`, alter Fehler bleibt sichtbar, **erneuter Klick ohne Reload möglich – PASS**.
4. Browser `BLOCKED` bereits beim START, sofortige Anzeige und Reaktivierung des Knopfs **PASS**.
5. Browser AJAX HTTP 500: verständliche Verbindungsanzeige, Knopf wieder benutzbar **PASS**.
6. Browser `RUNNING→COMPLETE`: Seite aktualisiert nach Abschluss **PASS**.
7. Originale PHP-Planbindungs-Gegenproben gegen .59: **9 PASS**, inklusive echte Quelle/Baseline-Änderung weiterhin gesperrt.
8. `PSERC_Package_Integrity::validate()`: **PASS 61/61 Dateien**; PHP-Syntax **43/43 PASS**; ZIP-CRC **PASS**, exakt **63 identische ZIP-Pfade**, genau 3 Änderungen (Admin, Version, Integritätsmanifest).

**Private QA-Testdatei:** `/pferdeatelier/PLUGINS/QA/PSERC-0.28.59-KISS-FORTSCHRITT-NUR-TEST.zip` (265002 Bytes), SHA256 `3882380893597aff22f95acfa0e692bc05c97417e227863bfcfa3f77e969e42c`.

## Beweisgrenze und nächster Schritt
Der **sichtbare Fortschritt** ist in einem echten Browser gegen tatsächliches PHP-Ausgabe-HTML und reproduzierte AJAX-Verläufe erfolgreich simuliert. **Keine echte WP-DB-/AJAX-Testinstallation**; es ist daher **nicht bewiesen**, dass der ursprüngliche ACTIVATE-Fehler auf der Testseite bereits fachlich beseitigt ist. Das alte K0-Dateiformat ist technisch gleich geblieben, aber mindestens **ein READY-Artikel aus WordPress** bleibt ungeprüft.

**Ein einziger gezielter echter Test:** Nur auf WordPress-TEST die .59 (Upgrade der .58) verwenden und bestehenden Button einmal klicken. Bereits während des Laufs sollte Status/Phase/Zähler sichtbar wechseln. Bei Abschluss besteht der bisherige K0-Handoff-Download; bei Sperre ist deren **aktuelle Ursache** sichtbar. Keine Keyword-Neuimporte, keine K0-Produktionsänderung und kein Löschen alter Daten.

**Wichtig:** Diese QA-Korrektur ist eine **sichtbare UI-Reparatur, keine neue Produktionsarchitektur**; sie garantiert weder 1 READY noch beseitigt sie ohne WordPress-Beleg echte Planänderungen. Großflächige Code-Löschungen erst nach kompletter Funktions-/Datenabhängigkeitsprüfung.
