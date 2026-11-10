# Affiliate – Änderungsregister seit den Portal-Kopien am 26.10.2026

**Stand: 10.11.2026.** Dieses Dokument ist eine **Übergabereferenz** für Hobbydepot (HD-009) und Hab & Bewahr (HAB-004), **kein Software-Release**.

## Unveränderliche Trennung
- **Pferdeatelier:** Ursprung des Affiliate-Systems; spätere eBay-QA-Entwicklung bis **6.72.321 QA9** ist **nur Test**, keine nachgewiesene funktionierende WordPress-Live-Version.
- **Hobbydepot (HD-009):** eigene Kopie von Pferdeatelier, Kopierbasis laut dokumentierter Übergabe **6.72.211**; danach eigene Pluginversionen. 
- **Hab & Bewahr (HAB-004):** eigene, abgeleitete Kopie mit eigenen Versionen, Daten und Design. 
- Keine Live-Plugins, Produktdaten, Affiliate-IDs, Konten oder Zuordnungen übertragen. Nie das Pferdeatelier-ZIP direkt in den anderen Portalen installieren.

## Chronologisches Änderungsregister
| Arbeitsstand | Was wurde geändert und warum? | Übernahmerelevanz | Beleg und Realtestgrenze |
|---|---|---|---|
| **6.72.308** (06.–07.11.) | eBay-Produktsuche begrenzt, doppelte Qualitätsprüfung vermieden, öffentliche Quellen-/Kreativdaten gebündelt, unnötige schwere Statusarbeit vermieden; Löschungen bei DB-Lesefehlern geschützt. | Gemeinsame eBay-Methoden nur nach Vergleich der jeweiligen Portalquelle. | Schon am 07.11. in beiden Affiliate-Büros als Referenz erfasst; Quelldiff im Repository. Kein WordPress-Livebeweis. |
| **311–312** (09.11.) | Cursor-/Timeout-/Retry-Zustände korrigiert, Wiederaufnahme ohne falsches Fortschritts-Reset; Einzelstörungen dürfen nicht alle Familien blockieren. | Wenn identischer Controller im anderen Portal vorhanden. | Historische Regressionen, nicht live freigegeben. |
| **313–314** (09.11.) | Startberechtigung zwischen Oberfläche und Worker angeglichen; „queued“ nicht als erfolgreich abgeschlossener Lauf ausgegeben. | Admin-Steuerung und Zustandsanzeige. | Historische lokale Tests. |
| **315** (09.11.) | „0/298“ der erneuten Nachsuche von realer Gesamt-/öffentlicher Abdeckung getrennt. | Gemeinsame Anzeigen-/Statuslogik nur bei gleicher Abdeckungsfunktion. | Quellbericht 315. |
| **319, QA1–2** (10.11.) | Zweiten parallelen Bestandscontroller entfernt, vorhandene Kandidaten im einen Auswahlweg wiederverwendet; Einzeldefekte isoliert, Mehrfachzuordnung und letzter guter Bestand geschützt. | **KISS-Kernregel**; keinesfalls fremde Kategorien/Kampagnen übernehmen. | QA2- und QA5-Berichte im QA-PR; reine PHP-Tests. |
| **QA3–5** (10.11.) | Gezielte statt vollständige Datenbanklesung, gebündelte öffentliche Prüfungen, Nachsuche-Bereinigung nur betroffener Familien, Backend-Menüs reduziert ohne Fachfunktionen zu löschen. | Leistung und Backend-Verschlankung nach jeweils eigenem Quellvergleich. | QA5-Gesamtbericht; noch kein echter WP-Abnahmelauf. |
| **QA6–7 / 6.72.320** (10.11.) | Neun nicht verwendete Methoden, eine doppelte Bedingung, zweite identische Speicherlesung, privaten ungenutzten Wrapper entfernt. Sicherheit und vollständige Speicherung erhalten. Konsistente Plugin-Versionsnummer 6.72.320. | Nur nach vollständiger Referenzprüfung auf jedem anderen Portal, keine ungeprüften Löschungen. | 61 PHP-Fachprüfungen, 23 PHP-Syntaxprüfungen; keine reale Veröffentlichung bewiesen. |
| **QA8** (10.11.) | Manuelle Pause wird als Leerlauf statt als wiederholbarer Fehler gemeldet; endlose Aufrufe bei Pause verhindert. | Nur bei identischem externen Taktgeber und Stoppverhalten. | Reproduzierbarer PHP-Test, im QA9-Stand enthalten. |
| **QA9 / 6.72.321** (10.11.) | **Recherche, frühere sichere Veröffentlichung und getrennte zweistündliche Verfügbarkeitskontrolle**; bestehende Angebote nutzen, ohne gesamten Lauf fertigzustellen; nachweislich beendete Produkte ausblenden. Vorheriger Recherchebestand und Checkpoints nicht löschen. 6h-Frischegrenze beibehalten. | **Konzeptreferenz**, keine direkte Codeübernahme. Beide Portale haben eigene Ausgangsbasis. | 61 bestehende + 19 neue PHP-Tests und ZIP-Prüfung; **keine echte WordPress-End-to-End-Abnahme**. |
| **Neuer offener Befund** (10.11., nach QA9) | Nutzer meldet **sehr langsames WordPress-Backend**. In QA9 startet die neue Verfügbarkeitsaufgabe bereits nach 60s und kann 5 Produkte je Paket mit Fortsetzung alle 90s bearbeiten; mögliche zusätzliche Serverlast. Die konkrete Dauer/Ursache ist **ohne Servermessung nicht bewiesen**. | **Warnung vor Übernahme:** Zeitplan, Lastgrenzen und echte WP-Leistung erst prüfen; keine ungetestete Cron-/Frontend-Übertragung. | Quellprüfung der QA9-Zeitplanung; **noch nicht behoben**. |

## Belege und Übernahmekontrolle
- eBay QA2–QA9 mit vollständigem Änderungspatch, Prüfberichten und Testskripten: [Pferdeatelier QA-PR #748](https://github.com/hallo-netizen/affiliate-pferdeportal/pull/748), branch `qa/pferdeatelier-ebay-319-qa5-evidence-20261110`.
- QA9-Basis: `Pferdeatelier_Affiliate_6.72.321_QA9_KISS_NUR_STAGING_TEST.zip` in der persönlichen Plugin-Library unter `/pferdeatelier/PLUGINS/QA/`; SHA256 `4a84696bdd10d5c32f3ab5d4e4583fc9029ef673403f43eebfe2217ffd72e47a`.
- GitHub enthält die QA-Berichte und vollständige Text-Patches, **nicht** das installierbare QA9-ZIP.
- Alte Suchergebnisse, bereits geprüfte Angebote, Kategorien, Zuordnungen, gespeicherte Laufcursor, Checkpoints, Historien und andere Provider dürfen **nicht** durch portiertes Material überschrieben werden.
- Jede spätere Übernahme in **jedem** anderen Portal benötigt eigenen Quellvergleich, eigenen Versionssprung, eigenes Prüfergebnis und eigene Freigabe. Bereits vorhandene lokale Lösungen nicht duplizieren.
- Dieses Register beschreibt den bekannten Änderungsstand; es behauptet **nicht**, dass jede historische Arbeitskopie auf der realen WordPress-Testseite bestanden hat.

**Status:** Protokoll vollständig als Dokumentation der hier greifbaren Arbeitsstände; Übernahme in HD-009 oder HAB-004 **nicht durchgeführt**, weiterhin getrennte Plugins.
