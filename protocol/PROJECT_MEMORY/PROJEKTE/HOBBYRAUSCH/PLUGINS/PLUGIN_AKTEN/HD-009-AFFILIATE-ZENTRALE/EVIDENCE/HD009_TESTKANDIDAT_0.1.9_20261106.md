# HD-009 – Hobby Depot Affiliate-Zentrale – lokaler Testkandidat 0.1.9-dev (06.11.2026)

## Quelle und Identität

- **Vom Betreiber hochgeladene echte WordPress-Original-ZIP:** `affiliate-portal-router.zip`, 628.291 Bytes; SHA-256 `34c0a9b42c62f71025212bfba3756e48bf4c6ab21fdd000c9894a1ce2bf12cfa`.
- **Originalversion:** `0.1.7-dev`, Plugin `Hobby Depot – Affiliate-Zentrale`.
- **Gezielt erstellte Nachfolge-Testversion:** `0.1.9-dev`, vollständiges WordPress-ZIP `HOBBY_DEPOT_AFFILIATE_ZENTRALE_HD009_0.1.9_DEV_HARMONISIERT_TEST.zip`; SHA-256 `2e08b52c0f5fd84537683a6a6217a9c62f4ea0025791c0d58a108b9edca90582`; **605.968 Bytes**.
- **Reproduzierbarer Textpatch:** `EVIDENCE/HD009_0.1.7_TO_0.1.9.patch` (auf dem ursprünglichen 0.1.7-Original mit `git apply -p2` anwendbar); GitHub-Datei wurde bytegleich mit lokalem Patch verifiziert.
- Das Original behielt seine 26 regulären Dateien; die Test-ZIP hat dieselben 26 regulären Dateien, 23 PHP-Dateien, ohne Mac-Metadaten. Nur vier Dateien wurden verändert, 22 bytegleich übernommen.
- **ZIP-Ordner / WP-Pluginpfad unverändert:** `affiliate-portal-router/hobby-depot-affiliate-router.php`.

## Gezielte Codekorrekturen

1. Die vorhandenen fünf Zusatzmodule (Produktquellenplan, Admin-KISS, Deal-Radar, Partnerstatistik, DS24-Nachverarbeitung) im üblichen WordPress-Bootstrap laden/starten.
2. Vorhandene aktive Amazon-ASIN-/Tracking-Brücke aus Hobby Depot nicht durch generische vorbereitete Amazon-Registrierung überschreiben.
3. eBay-Kontolöschung: Fehlgeschlagene WordPress-Post-Löschung darf nicht als Erfolg quittiert werden. Fehler meldet 503 und speichert keinen Erfolgsbeleg; wiederholte Meldung kann erneut verarbeitet werden.
4. Bei nicht gespeichertem eBay-Löschbeleg ebenfalls keinen Erfolg quittieren.
5. Keine neuen Kategorien, keine fremden Daten, keine zusätzlichen Hooks/Queues/Tabellen für den eBay-Löschpfad, keine Änderung bestehender Pluginoptionsnamen und keine Portal-Migration.

## Tatsächlich ausgeführte Prüfungen

- **PHP-Syntax:** 23/23 bestanden (`php -l`).
- **ZIP-CRC:** bestanden; 23 reguläre PHP-Dateien.
- **Vergleich Original vs. Version:** nur vier Dateien verändert; 22 unverändert.
- **Hobby-Portaltrennung:** keine wörtlichen Marker `pferdeatelier`, `pferde-atelier`, `pferdeportal`, `hab-und-bewahr` in den 26 regulären Dateien.
- **Konstanten-/Optionsdefinitionen:** unverändert.
- **WordPress-Hook-Offline-Smoke:** 88 Hooknamen registriert, fünf Modulklassen vorhanden, Kernhooks vorhanden.
- **Provider-Regression:** aktive Amazon-Brücke bleibt exakt unverändert; eBay/idealo bleiben unverändert; vorbereitete OTTO/Kelkoo/Kaufland bleiben vorhanden.
- **eBay-Löschungs-Tests:** Fehler bei Post-Löschung; Fehler beim Löschen; Erfolg mit 204; Wiederholung ohne Doppellöschung; Fehler bei nicht gespeichertem Beleg → 503; sieben Prüffälle bestanden.
- **Gegenprüfung:** keine produktive WordPress-/Provider-Live-Abnahme.

## Verbindliche offene Grenze

Das vollständige Original der Pferdeatelier-Referenz `6.72.306` liegt **nicht** als vollständige ZIP in der aktiven Hobby-GitHub-Ablage; nur der dokumentierte Prüfbericht. Die übernommenen Korrekturen beruhen deshalb auf den tatsächlich belegten allgemeinen Fehlern. **Kein vollständiger 6.72.306-Quell-/Featureabgleich behauptet.** Die Pferde-eigene Produktfamilienliste (297) darf niemals übernommen werden.

**Zentrale GitHub-Ablage:** Die **Textbelege und der exakte Quellpatch** sind hier im HD-009-Pluginbüro gesichert. Die **komplette 0.1.9-dev-ZIP ist nur im aktuellen Chat als testbarer Download vorhanden und noch NICHT als ZIP-Blob in GitHub**. Dieser Testkandidat wird ausdrücklich nicht als freigegebene `CURRENT.zip` geführt.

**Genau ein fachliches Affiliate-Büro:** `PROJEKTE/HOBBYRAUSCH/AFFILIATE/`; technische Akte/Pluginpaket ausschließlich `PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/` und `PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/`. Keine weitere Affiliate-Pluginlinie.
