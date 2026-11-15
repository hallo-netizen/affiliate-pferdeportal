# Robotik-Pluginbüro – einziges Release-/Prüfprotokoll

## AKTUELL 15.11.2026 – 0.4.13 löst 0.4.12 ab
- `PLUGIN/CURRENT.zip` = `PLUGIN/VERSIONEN/0.4.13.zip`, GitHub-Dateikennung `a8149236e98debdb93f6657d9e07447700aecf54`. Das Paket ist PHP- und ZIP-geprüft, kein echter WordPress-Live-PASS.
- V79 ergänzt **einmalig und ohne neuen Worker** die im vorherigen Sammelablauf vergessene **104er Originalseiten-Veröffentlichung**, bevor die 68 neuen Seiten an die Reihe kommen. Bestehende 227er und 64er Aufgaben bleiben unverändert; keine doppelte Zustimmung, keine Google-Adressen-Sperre. Auch unter 0.4.12 gespeicherte Zwischenzustände werden korrigiert.
- **GitHub CI PASS:** https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43704446763. Releasebeleg: `V79_104_ALTSEITEN_SICHTBARKEIT_20261115.md`. Frühere Angaben zu 0.4.12 sind historisch.

## Aktuelle installierbare Version 15.11.2026 – 0.4.12 (V78)
- **`CURRENT.zip` ist identisch mit `VERSIONEN/0.4.12.zip`**, GitHub-Blob `6f55d9890a77e38e908f8c002396129d685f3a4f`, 180.769 Bytes. **Nicht mehr 0.4.11 installieren**.
- 0.4.12 bündelt V63 (gespeicherte 227 Aufgaben), V65 (68 Veröffentlichungen) und V77 (16+48 Nachtrag = 64 Aufgaben) in **einer einzigen ausdrücklich genehmigten Ausführung** und einem einzigen Abschlussbericht. Kein neuer Writer, kein doppelter Import, keine Google-URL-Sperre, kein API-Aufruf.
- **Echte GitHub-CI-Abnahme SUCCESS:** <https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43701031122> – 10/10 PHP, ZIP, fünf Code-Dateien exakt; 16+48 Besitzerprüfung und durchgehender simulierter 227→68→64-Lauf inklusive Wiederaufnahme von 16/227 sowie negativem Änderungsfall. **WordPress-Live-Abnahme noch offen**.
- **Einzige Anleitung:** `V78_RELEASE_VERIFIZIERT_20261115.md`. Alles Folgende ist historisches Versionsprotokoll, keine zusätzliche Aktion.

## Aktuelle Version 15.11.2026: 0.4.11
**Installierbar:** `PLUGIN/CURRENT.zip` = `PLUGIN/VERSIONEN/0.4.11.zip`. Quellstand und Tests: `PLUGIN/V77_RELEASE_VERIFIZIERT_20261115.md`. Ältere Aussagen über `CURRENT.zip` gehören zum jeweiligen historischen Versionseintrag und sind keine Installationsanweisung.

Stand 09.11.2026. **Protokoll nach jedem neuen Plugin im selben Commit mit Installer und CURRENT_STATE.md fortschreiben.**

| Version | Datei im Archiv | Änderung | Prüfstatus | WordPress |
| --- | --- | --- | --- | --- |
| 0.1.0 | `VERSIONEN/0.1.0.zip` | Neutrale JSON-Planungsoberfläche, ohne Import | Historischer ZIP-/PHP-PASS | Archiv; keine eigene belegte Live-Abnahme |
| 0.2.0 | `VERSIONEN/0.2.0.zip` | Produktseitenrollen, Parent-/Kategorieprüfung | Historische lokale Tests (16 Struktur- und weitere Admin-Tests), PHP/ZIP-PASS | Nutzer-Screenshot: grüne formale Prüfung; ersetzt durch 0.3.0 |
| **0.4.11 (V77)** | **`VERSIONEN/0.4.11.zip`**, identisch zu **`CURRENT.zip`** | Derselbe gespeicherte 227er-Import kann nach Bestandsprüfung fortgesetzt werden; bestehende 68er-Veröffentlichung korrigiert (bereits veröffentlichte Seiten gelten als gültig); **16 fachlich freigegebene Robotertyp-Seiten + 48 Rubriken** im Anschluss ohne Google-URLs in **einem** gesicherten 64er Lauf mit ausdrücklicher Freigabe. Nur eine zentrale Import-Schreibfunktion, keine weitere Pluginidentität. | **GitHub Actions 43698916919 SUCCESS**: PHP-Lint für 9 ZIP-PHP-Dateien, ZIP-Struktur, bytegleiche ZIP/Quellen und 16+48/188+296-Live-Inventur-Mock einschließlich Negativfall. Blob `2bfaa950246b2657fc9f0d6db7151f592352f7a2`. | **INSTALLATIONSBEREIT; KEINE WordPress-Liveausführung bisher bestätigt.** |
| **0.4.10 (V65, HISTORIE)** | **`VERSIONEN/0.4.10.zip`**, identisch zu **`CURRENT.zip`** | Nach belegtem 227/227-Abschluss **68 neue Entwurfsseiten** in einem eindeutig freigegebenen, fortsetzbaren Lauf veröffentlichen; 16 SEO-HOLDs/48 Rubriken weiter gesperrt; bisherige 104 veröffentlichten Seiten sowie 248 Taxonomierubriken unverändert | **8 Backenddateien bytegleich (Import/SEO/Altveröffentlichung/Assets), 10 PHP Lint PASS, Mock 227→68→172 PASS, ZIP CRC; SHA256 `1c0852ea75a93d8344514ef3d2618c31e28a57c61a57858db8e9fcfd1e6a3361`** | **TEST, Live WordPress-Importabschluss und Publikation offen** |
| **0.4.9 (V63)** | **`VERSIONEN/0.4.9.zip`**, identisch zu **`CURRENT.zip`** | Einmalige geschützte **68 Seiten (nur Entwurf) + 159 Rubriken** aus realem V62-WP-Abgleich; 16 SEO-HOLD-Seiten und 48 Rubriken gesperrt; alte 115/90 unangetastet, kein alter Import | **7/7 PHP-Lint, ZIP CRC, 15/15 WordPress-Mocks inkl. 227er Vollimport, Unterbrechung und Rückvergleich PASS; SHA256 `1829a6b7cf3d243f361431736ebd027949724b293aac40306db60df00f4ff8b0`** | **TEST; keine Live-WP-Änderung, explizite Freigabe erforderlich** |
| **0.4.8 (V62)** | **`VERSIONEN/0.4.8.zip`**, identisch zu **`CURRENT.zip`** | Alle 8 Welten/188 geplante Seiten + 296 Rubriken nur lesend gegen echte WordPress-Inventur prüfen; „Humanoide“ als fehlende Konzept-Hauptwelt ergänzt; 26 redaktionelle Suchideen, 16 SEO-HOLDs offengehalten; EIN JSON-Gesamtbericht, kein neuer Writer | **6/6 PHP-Lint, 16/16 lokale WP-Mockfälle, ZIP CRC, 7/7 alte ZIP-Dateien bytegleich; SHA256 `d42b046f3d27b52c68a63ebaaf6775b6c73935124223d14d247cdac5666cf7ff`** | **TEST: WP-Live-Ist-Abgleich offen; alter Erstimport 104/89 unangetastet und NICHT für V62 verwenden** |
| **0.4.7 (V60)** | **`VERSIONEN/0.4.7.zip`**, identisch zu **`CURRENT.zip`** | Task-Status **40101 Internal SE Server Error** und HTTP500/50000 zentral erkennen; echten gespeicherten 9/38-Lauf mit 8 Ergebnissen + 1 vorheriger Lücke ohne erneute API-Belastung fortsetzen; weitere bestätigte Anbieterfehler überspringen, andere Fehler blockieren | **5/5 PHP-Lint PASS, ZIP CRC PASS, 23 lokale WordPress-/Anbieter-Tests PASS, Original-Importer/Publikation und 2 Assets bytegleich; SHA256 `1b40052cb8d959de30bc950839d2d58d9b964d9e60cf9a1faf5f058ba44574eb`** | **TEST, WordPress-/API-Live-Abnahme offen** |
| **0.4.6 (V59)** | **`VERSIONEN/0.4.6.zip`**, identisch mit **`CURRENT.zip`** | Nach HTTP500 beim vierten Auftrag (Freizeit) **ohne Wiederholung des gescheiterten Auftrags** weiterarbeiten; drei erfolgreich bezahlte Schritte, Run-ID und Budget erhalten, als Lücken ausgewiesene Fehler und vorsichtige Budgetreserve | **5/5 PHP-Lint PASS; ZIP CRC PASS; WordPress-Mock 3/38 → 38/38 mit offen ausgewiesenen Ausfällen PASS; Kosten-/Wiederholungssperre PASS. SHA256 `1c6517a1bab3efea1214fdb3336de975c1a357049a2969dd72c21081595cbb2b`.** | **Nur TEST; Live-Installation/-API und Datenlücken noch offen** |
| **0.4.5 (V58)** | **`VERSIONEN/0.4.5.zip`**, identisch mit **`CURRENT.zip`** | **Einmalige ausdrücklich kostenbestätigte manuelle Wiederaufnahme des bereits beim Anbieter mit 50000 abgebrochenen ersten von 38 SEO-Aufträgen. Originalaufgaben, Budget, WP-Import und Veröffentlichung unverändert.** | **5/5 PHP-Lint, ZIP CRC, 7 Sperrbedingungen und 6 Admin-Mock-Szenarien PASS; SHA256 `3dc302127eba6150cafb920304a12159cc494b13beca1fa5d64c9c619ed5f1fe`.** | **Nur TEST, kein WordPress- oder API-Live-PASS. Mögliche Zusatzkosten ausdrücklich bestätigen.** |
| **0.4.4 (V57)** | **`VERSIONEN/0.4.4.zip`**, identisch zu **`CURRENT.zip`** | **Eine gebündelte einmalige SEO-Gesamtabfrage mit 437 Übersichtswerten, 8 Keyword-Ideas-Welten, 16 SERP-HOLD-Paaren / 29 deduplizierten Google-Suchen; ein gemeinsamer JSON-Bericht, Budget-Stopp und kein Auto-Retry** | **5/5 PHP-Lint PASS, ZIP CRC PASS, 38/38 WordPress-Mock-Aufgaben PASS, Budget- und Fehler-Negativtests PASS. SHA256 d7fcee60a1c3adc831b0226a6cf2413e84daaaea5732fd240fd5b3ea5f9dea10.** | **TEST; echter WP-Live-Lauf, echte DataForSEO-Abfrage und 141er-Import nicht ausgeführt.** |
| **0.3.0** | **`VERSIONEN/0.3.0.zip`** | **Manuell lesender WordPress-Inventarcheck; ein Gesamtbericht, optional HivePress** | **ZIP-CRC PASS, PHP-Lint 2/2 PASS; 7.926 Byte, SHA256 `3c31aaaf86379a054034a80c8aeb3eaebdf616baa953ac079793f6495f1ecd30`; kein ungeprüfter Altportal-Code** | **09.11.2026: „installiert“ vom Nutzer gemeldet; echter WP-Bestandsscan/Export OFFEN** |

## Welche Datei gilt?
Historische Angabe (V57, nicht mehr aktueller Stand): `PLUGIN/CURRENT.zip` und `PLUGIN/VERSIONEN/0.4.4.zip` waren damals derselbe TEST-Installer; die alte 0.3.0 ist im Versionsarchiv. Die Vorgänger bleiben unverändert im Versionsarchiv. Es gibt **keine** zweite aktive Plugin-Identität und keinen alternativen Current-Zweig.

## Behauptungsgrenzen
- **DATEI PASS** = ZIP prüfbar; PHP syntaktisch richtig; genau die vorhandenen Dateien.
- **INSTALLIERT LAUT NUTZER** = Nutzer hat Installation gemeldet, kein unabhängiger Backend-Nachweis.
- **LIVE PASS** erst nach erfolgreichem WordPress-Bestandscheck und Stichproben des einen Gesamtberichts, HivePress ggf. separat; aktuell **NICHT** erreicht.
- Die geplante Keyword-/GitHub-Master-/Inhalts-/Anzeigen-Gesamtprüfung ist **noch NICHT in 0.3.0 umgesetzt**.

## Übergabe an den nächsten Chat
1. `PROJEKTE/ROBOTIK/KATEGORIE/CURRENT_STATE.md` zuerst lesen, danach diese Datei und `RECHERCHE/MASTER_ABGLEICH_20261109.md`.
2. **Keine Plugin-Neuerstellung, keine zweite Masterliste.** Nur `robotik-kategorie-workflow` weiterentwickeln.
3. **Erledigt 09.11.2026:** Nutzer hat einmaligen JSON-Gesamtbericht übermittelt. NICHT erneut anfordern; die WordPress-Site ist praktisch leer. Bestandsscan technisch nachgewiesen, fachliche/SEO-Prüfung bleibt offen.
4. Anschließend **nur lesenden** GitHub-Master-Abgleich und Research-Gap-Funktionen aus geprüfter allgemeiner Kategorie-Pluginlinie adaptieren. Nicht HAB-spezifische Altlasten/Writer übernehmen.
5. Nach jeder späteren Plugin-Version: ZIP + Changelog + `CURRENT.zip` + `CURRENT_STATE.md` atomar auf GitHub im Robotik-Pluginbüro.

**Keine WordPress-Kategorien/Seiten wurden durch das GitHub-Ablegen verändert.**

## 0.3.0 – reale Bericht-Abnahme 09.11.2026
- **WordPress-Leseprüfung erfolgreich:** JSON-Bericht mit Versionskennung 0.3.0, 2 WP-Seiten, 1 Beispielbeitrag und 1 Standardkategorie; formal 0 Issues.
- **Bewusst nicht als PASS werten:** HivePress fehlt, Magazin/Anzeigen/Master/Keyword nicht angebunden, Frontend ungeprüft.
- **Kein erneuter Bericht nötig**, bis echte Robotik-Inhalte hinzugekommen sind. Nächster Code-Schritt: revisionssicherer read-only Import der einzigen GitHub-Fachmaster-Quelle, ohne neue Dateien vom Nutzer.
