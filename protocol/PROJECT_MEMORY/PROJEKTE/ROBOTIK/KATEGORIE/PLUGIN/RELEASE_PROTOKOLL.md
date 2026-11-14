# Robotik-Pluginbüro – einziges Release-/Prüfprotokoll
Stand 09.11.2026. **Protokoll nach jedem neuen Plugin im selben Commit mit Installer und CURRENT_STATE.md fortschreiben.**

| Version | Datei im Archiv | Änderung | Prüfstatus | WordPress |
| --- | --- | --- | --- | --- |
| 0.1.0 | `VERSIONEN/0.1.0.zip` | Neutrale JSON-Planungsoberfläche, ohne Import | Historischer ZIP-/PHP-PASS | Archiv; keine eigene belegte Live-Abnahme |
| 0.2.0 | `VERSIONEN/0.2.0.zip` | Produktseitenrollen, Parent-/Kategorieprüfung | Historische lokale Tests (16 Struktur- und weitere Admin-Tests), PHP/ZIP-PASS | Nutzer-Screenshot: grüne formale Prüfung; ersetzt durch 0.3.0 |
| **0.4.9 (V63)** | **`VERSIONEN/0.4.9.zip`**, identisch zu **`CURRENT.zip`** | Einmalige geschützte **68 Seiten (nur Entwurf) + 159 Rubriken** aus realem V62-WP-Abgleich; 16 SEO-HOLD-Seiten und 48 Rubriken gesperrt; alte 115/90 unangetastet, kein alter Import | **7/7 PHP-Lint, ZIP CRC, 15/15 WordPress-Mocks inkl. 227er Vollimport, Unterbrechung und Rückvergleich PASS; SHA256 `1829a6b7cf3d243f361431736ebd027949724b293aac40306db60df00f4ff8b0`** | **TEST; keine Live-WP-Änderung, explizite Freigabe erforderlich** |
| **0.4.8 (V62)** | **`VERSIONEN/0.4.8.zip`**, identisch zu **`CURRENT.zip`** | Alle 8 Welten/188 geplante Seiten + 296 Rubriken nur lesend gegen echte WordPress-Inventur prüfen; „Humanoide“ als fehlende Konzept-Hauptwelt ergänzt; 26 redaktionelle Suchideen, 16 SEO-HOLDs offengehalten; EIN JSON-Gesamtbericht, kein neuer Writer | **6/6 PHP-Lint, 16/16 lokale WP-Mockfälle, ZIP CRC, 7/7 alte ZIP-Dateien bytegleich; SHA256 `d42b046f3d27b52c68a63ebaaf6775b6c73935124223d14d247cdac5666cf7ff`** | **TEST: WP-Live-Ist-Abgleich offen; alter Erstimport 104/89 unangetastet und NICHT für V62 verwenden** |
| **0.4.7 (V60)** | **`VERSIONEN/0.4.7.zip`**, identisch zu **`CURRENT.zip`** | Task-Status **40101 Internal SE Server Error** und HTTP500/50000 zentral erkennen; echten gespeicherten 9/38-Lauf mit 8 Ergebnissen + 1 vorheriger Lücke ohne erneute API-Belastung fortsetzen; weitere bestätigte Anbieterfehler überspringen, andere Fehler blockieren | **5/5 PHP-Lint PASS, ZIP CRC PASS, 23 lokale WordPress-/Anbieter-Tests PASS, Original-Importer/Publikation und 2 Assets bytegleich; SHA256 `1b40052cb8d959de30bc950839d2d58d9b964d9e60cf9a1faf5f058ba44574eb`** | **TEST, WordPress-/API-Live-Abnahme offen** |
| **0.4.6 (V59)** | **`VERSIONEN/0.4.6.zip`**, identisch mit **`CURRENT.zip`** | Nach HTTP500 beim vierten Auftrag (Freizeit) **ohne Wiederholung des gescheiterten Auftrags** weiterarbeiten; drei erfolgreich bezahlte Schritte, Run-ID und Budget erhalten, als Lücken ausgewiesene Fehler und vorsichtige Budgetreserve | **5/5 PHP-Lint PASS; ZIP CRC PASS; WordPress-Mock 3/38 → 38/38 mit offen ausgewiesenen Ausfällen PASS; Kosten-/Wiederholungssperre PASS. SHA256 `1c6517a1bab3efea1214fdb3336de975c1a357049a2969dd72c21081595cbb2b`.** | **Nur TEST; Live-Installation/-API und Datenlücken noch offen** |
| **0.4.5 (V58)** | **`VERSIONEN/0.4.5.zip`**, identisch mit **`CURRENT.zip`** | **Einmalige ausdrücklich kostenbestätigte manuelle Wiederaufnahme des bereits beim Anbieter mit 50000 abgebrochenen ersten von 38 SEO-Aufträgen. Originalaufgaben, Budget, WP-Import und Veröffentlichung unverändert.** | **5/5 PHP-Lint, ZIP CRC, 7 Sperrbedingungen und 6 Admin-Mock-Szenarien PASS; SHA256 `3dc302127eba6150cafb920304a12159cc494b13beca1fa5d64c9c619ed5f1fe`.** | **Nur TEST, kein WordPress- oder API-Live-PASS. Mögliche Zusatzkosten ausdrücklich bestätigen.** |
| **0.4.4 (V57)** | **`VERSIONEN/0.4.4.zip`**, identisch zu **`CURRENT.zip`** | **Eine gebündelte einmalige SEO-Gesamtabfrage mit 437 Übersichtswerten, 8 Keyword-Ideas-Welten, 16 SERP-HOLD-Paaren / 29 deduplizierten Google-Suchen; ein gemeinsamer JSON-Bericht, Budget-Stopp und kein Auto-Retry** | **5/5 PHP-Lint PASS, ZIP CRC PASS, 38/38 WordPress-Mock-Aufgaben PASS, Budget- und Fehler-Negativtests PASS. SHA256 d7fcee60a1c3adc831b0226a6cf2413e84daaaea5732fd240fd5b3ea5f9dea10.** | **TEST; echter WP-Live-Lauf, echte DataForSEO-Abfrage und 141er-Import nicht ausgeführt.** |
| **0.3.0** | **`VERSIONEN/0.3.0.zip`** | **Manuell lesender WordPress-Inventarcheck; ein Gesamtbericht, optional HivePress** | **ZIP-CRC PASS, PHP-Lint 2/2 PASS; 7.926 Byte, SHA256 `3c31aaaf86379a054034a80c8aeb3eaebdf616baa953ac079793f6495f1ecd30`; kein ungeprüfter Altportal-Code** | **09.11.2026: „installiert“ vom Nutzer gemeldet; echter WP-Bestandsscan/Export OFFEN** |

## Welche Datei gilt?
`PLUGIN/CURRENT.zip` und `PLUGIN/VERSIONEN/0.4.4.zip` sind jetzt exakt derselbe TEST-Installer; die alte 0.3.0 ist im Versionsarchiv. Die Vorgänger bleiben unverändert im Versionsarchiv. Es gibt **keine** zweite aktive Plugin-Identität und keinen alternativen Current-Zweig.

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
