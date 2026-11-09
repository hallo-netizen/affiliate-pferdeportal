# Pferdeatelier / eBay BUSINESS-only – 6.72.314 Gesamtabnahme lokal (09.11.2026)

**Status: LOKALES TESTGATE PASS; PRODUKTIVE FREIGABE WEITERHIN GESPERRT.** Kein Eingriff in K0, WordPress-Live, andere Portale/Provider oder CURRENT_RELEASE.

## Gesicherte Binärdatei (persistent, erneut rückgelesen)

- **Testplugin:** `/pferdeatelier/PLUGINS/QA/Pferdeatelier_Affiliate_6.72.314_KISS_Gesamtworkflow_TEST.zip` in der persönlichen ChatGPT-Dateibibliothek.
- **SHA-256:** `2a4dc2954bf76b560583667d81c91c827fb6835754bcd58439bce1fda5f95f18`; Größe **5.348.855 Bytes**.
- Bytevergleich **neu aus Library materialisierte ZIP == lokal geprüfte ZIP: PASS**.
- **Prüfbericht:** `/pferdeatelier/PLUGINS/QA/EBAY_6.72.314_GESAMTPRUEFUNG.md`
- **PHP-Lauftests, Vorher-Nachher-Belege, Logs, Manifest:** `/pferdeatelier/PLUGINS/QA/EBAY_6.72.314_QA_BELEGE.zip`
- Original `6.72.308` bleibt unberührt, Archiv 311/312/313 bleibt erhalten.

## Root causes mit echtem Vorher-Nachher-Test

1. **Doppelte, widersprüchliche Startfreigaben:** 313 prüfte auf der Automatisierungsseite nur Credentials + gespeicherte Zustimmungen, während `ebay_run_start` weitere verbindliche Prüfungen für Geschäftsroute, Portal-Kataloggültigkeit, eBay-Deletion-Compliance nutzt. Frühere 312 prüfte sogar veraltete, nicht existierende Schlüssel und sperrte trotz gültiger Häkchen. **314 ruft für die UI dieselbe vorhandene `ebay_configuration_errors` wie der echte Start auf** sowie die bereits existierende Kanalpause-/Chef-Veto-Prüfung. Alle Gründe werden im Klartext angezeigt; KEINE Zustimmung wird gesetzt oder umgangen.
2. **Falsche „abgeschlossen“-Meldung:** 313 markierte eBay-Dispatcher-Response mit `immediate=true` als `completed`, obwohl `run_ebay_sync` nur `queued` zurückgab. Vorher reproduziert: `queued -> completed` (falsch). **314** meldet `queued/resumed/already_running` als offene Verarbeitung, nur echten `completed` als Abschluss.

KISS: gegenüber ZIP 313 nur **drei vorhandene Dateien** geändert: `trait-ppar-automation-suite.php`, Hauptplugin-Header, readme. **63/66 unverändert**, keinerlei neue Komponenten, Datenbanktabellen, Worker, Endpunkte oder Frontend-HTTP.

## Lokal auf der fertigen ZIP ausgeführt

- Alle **66 ZIP-Dateien CRC PASS**, **23/23 PHP-Syntax PASS**.
- **49/49 fachliche Original-Funktionsprüfungen** gegen BUSINESS-Hardlocks, Bestandsprüfung, sichere öffentliche Quellen, Fehlerbehandlung.
- **333 echte kanonische Worker/Phasen-Assertions** mit **311 konsekutiven simulierten Quell-Arbeitspaketen**; Cursor/Fortschritt, Unterbrechungen, Wiederaufnahme, Abschluss, Konkurrenzsperre.
- **17** eBay-HTTP/Pagination-Szenarien über reale Pluginfunktionen mit lokal simulierten Antworten (cURL28, 429,503,401,403, ungültige Folgeseite).
- **5** Tests der echten Frontend-Produktquellenfilter.
- **25** Tests der UI-Sperre **am echten eBay-Quellmethoden-Aufruf**, darunter vollständige Bestätigungen, fehlender Zugang, abweichender Katalog, Compliance-Challenge, ausgeschaltete Route, Kanalpause. UI und echter Lauf liefern dieselben Gründe.
- **13** zusätzliche Tests am echten `run_ebay_sync(true)`: `queued` als gespeicherter kanonischer Hintergrundlauf, signierter gleicher WordPress-Host (ohne Netzwerk), kein doppelter Lauf bei erneutem Start, Fehler ohne Job.
- **18** Status-/Meldungsregressionen; 313-Falschmeldung ausdrücklich vor Fix reproduziert.
- Echter Plugin-Bootstrap mit **143 registrierten WordPress-Hooks**.
- Gesamt **460 eindeutige explizite lokale Prüfungen**, wiederholte Gate-Setups nicht doppelt gerechnet.

## Nicht behaupten / Restgate

Hier keine reale WordPress/MariaDB/HivePress-Testinstallation oder produktive eBay-Browse-/getItem-API-Aufrufe, Live-Produktsichtbarkeit, Yoast-Sitemap oder vollständige reale eBay-Katalogabdeckung geprüft. Die lokale 311-Paket-Simulation enthält echte kanonische Workersteuerung, aber simulierte Fachphasen und eBay-Antworten. **Version 314 ist eine installierbare TEST-ZIP für eine isolierte Testseite; niemals produktiv freigegeben.** `CURRENT_RELEASE.json` unverändert belassen.

**User-Screenshot 09.11.:** Zentraler Zugang aktiv, Vertragsbestätigung und Datenschutz bereits angehakt. KEINE erneute Bestätigung oder Menü-Rundgänge verlangen. Ob die weiteren Pflichtbedingungen live erfüllt sind, lässt sich aus Screenshot nicht allein beweisen. Das 314-Plugin zeigt die tatsächlich fehlenden Gründe stattdessen korrekt an.

Die ZIP liegt als Binärdatei in der Library, NICHT als ZIP im GitHub-Tree. Dieses Dokument ist der langfristig lesbare Campus-Nachweis mit exaktem Pfad und Prüfsumme.
