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

### Ergänzung: reale Backend-Bilder 17:35–17:40 Uhr

- Suchlauf **läuft weiter**: 340 → 360 Pakete, 345 → 365 echte Fortschrittsschritte in fünf Minuten. **154/298** gespeicherte öffentliche Kategorieabdeckung, **144 offen**; **232 gespeicherte Freigaben**, keineswegs 232 garantiert sichtbare Kacheln. Bereits mindestens eine eBay-Kachel ist auf der gezeigten Kategorie sichtbar.
- **Verfügbarkeitsstatus lautet weiterhin „noch nicht geprüft“**: Ein erfolgreicher Arbeitsdurchlauf der neuen QA9-2h-Prüfung ist **nicht belegt**. Sie als nachgewiesene Ursache der enormen Backend-Langsamkeit zu bezeichnen, wäre falsch.
- QA9-Quellbefund: Das Backend pollt den Status alle **45 Sekunden**; nach 180 Sekunden Stillstand kann die Statusfunktion **synchron einen echten kanonischen eBay-Arbeitsschritt** ausführen. Dieser Nebenweg muss beim nächsten KISS-Leistungsumbau getrennt werden. Laufende Selbstfortsetzung der Recherche und 90-Sekunden-Fortsetzungen der neuen Verfügbarkeit dürfen nicht denselben kleinen Server überlasten.
- **Status:** Prüfbefund / geplanter nächster Umbau, **noch keine gelieferte Reparatur, keine reale Antwortzeitmessung**. Andere Portale vor jeder Übernahme getrennt vergleichen, nicht die eBay-Such- oder Shopdaten des Pferdeateliers kopieren.
- Ausführliche Quellstellen und Bildbefunde im Bericht `EBAY_QA9_KISS_GETRENNT_20261110.md` im [eBay-QA-PR #748](https://github.com/hallo-netizen/affiliate-pferdeportal/pull/748).

### Ergänzung: reales Backend-Folgefoto 17:48 Uhr

Weiterer Nutzerscreenshot, 10.11.2026: Kanonischer eBay-Gesamtlauf bleibt `running / gapfill_discovery`. Seit dem letzten Screenshot **360 → 399 Pakete** und **365 → 404 echte Fortschrittsschritte**. Die **gespeicherte öffentliche Abdeckung bleibt 154/298**, **144 Familien offen**; **232 gespeicherte Freigaben** unverändert. Die Verfügbarkeitsprüfung zeigt weiterhin **„noch nicht geprüft“**. Der aktuelle Screenshot enthält keinen Nachweis einer erfolgreicher Prüfung oder einen gemessenen Performancewert.

**Übernahmewarnung HD-009 und HAB-004:** Die neue separate Verfügbarkeitsarbeit ist nicht als real WordPress-erprobt anzusehen. Vor Portierung Serverlast, lesende Statusabfrage, tatsächliche Anzeige und Produktaktualität gegen die jeweils eigene Installation prüfen. Keine fremden Produktergebnisse, APIs, Bestände oder Versionen übernehmen. Als Beobachtung protokolliert, **noch keine Fehlerreparatur**.

### 10.11.2026 – Marktnachweis und Reihenfolge bei 298 eBay-Familien

Quellenabgleich am tatsächlichen Pferdeatelier QA9-Code: Der Pflichtfamilienkatalog enthält **324 definierte Familien minus 26 explizite Nicht-Waren = 298 eigene Pferdeatelier-Produktseiten**, **nicht** 298 eBay-Kategorien. Bereits am 09.11. gespeicherter 187-Familien-Bericht: **86 keine Treffer im konkreten begrenzten Suchausschnitt**, **98 Treffer gefunden, aber abgelehnt**, **3 angenommene Treffer ohne öffentliche Abdeckung**. Bei **81/86** null treffenden Suchanfragen wurde automatisch „Pferd“ angefügt; das zweite exakte Suchwort existiert in QA9 bereits. Im Screenshot 17:48 sind **144 Familien öffentlich offen**, **154/298** abgedeckt; dies ist ein anderer Stand.

**Konkrete KISS-Ursache für Zeitverlust:** `ebay_run_tick_coverage` führt bei offenen Familien zuerst zu `gapfill_discovery` (neue eBay-Abfrage). Die erneute Auswahl und Wiederverwendung gespeicherter Kandidaten erfolgt erst in `gapfill_select`. Die neue Suche kann daher vor der erneuten Prüfung bereits vorhandener brauchbarer Kandidaten ablaufen. Öffentliche Abdeckung bleibt während reiner Discovery-Aufrufe unverändert; das allein ist kein fehlgeschlagener eBay-Aufruf. Ein sicherer Umbau muss **vor einer weiteren gezielten Marktsuche gespeicherte, fachlich geeignete Angebote im bestehenden zentralen Auswahl-/Freigabeweg prüfen**, dabei die bislang im Selector angehängte Prune-/Bereinigungslogik und den letzten gültigen Checkpoint vor verfrühter Entfernung schützen.

**Stichprobe aktuell zugänglicher eBay-Angebote** (nicht zwingend Teil der aktuell offenen 144 Familien): gewerbliche [Reitplatzplaner](https://www.ebay.de/b/Reitplatzplaner/bn_7005726853), gewerbliche [LED-Rückleuchten für Pferdeanhänger](https://www.ebay.de/itm/166851846902); privat angebotene 1,5er Pferdeanhänger im sichtbaren Marktplatz zeigen den Unterschied zur ausschließlich gewerblichen API-Filterung. Der Plugin-Browse-Abruf verarbeitet je Profil **eine Ergebnisseite mit höchstens 30 Artikeln**, nur Business und lieferbar nach Deutschland. Eine leere API-Antwort ist **kein sicherer Nachweis**, dass keine Ware auf eBay existiert.

**Prüfbeleg vollständig in** [Pferdeatelier-Ursachenbericht der QA9-Prüfstrecke](https://github.com/hallo-netizen/affiliate-pferdeportal/blob/qa/pferdeatelier-ebay-319-qa5-evidence-20261110/protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/AFFILIATE/EBAY_298_ABDECKUNG_MARKT_SUCHERGEBNISSE_URSACHEN_20261110.md). **Keine neue ZIP, kein bereits behobener Gesamtfehler, kein Produktiv- oder Fremdportal-Eingriff.** Die Ergebnisse dienen als **Übertragungsreferenz**, nicht als ungeprüfter HD-/HAB-Code-Fix.

### 10.11.2026 – Historienkorrektur: QA2–QA9 bereits umgesetzt, kein neuer Bestandsrecherche-Umbau

Nach Prüfung der ursprünglichen QA7- und QA9-Installations-ZIPs und aller erreichbaren QA2–QA9-Berichte **ist die seit Tagen erneut empfohlene Bestandswiederverwendung schon implementiert**. `ebay_business_reuse_stored_for_concept` wird im vorhandenen `gapfill_select` aufgerufen; zweiter exakter Suchbegriff (316), Mehrfachzuordnung, Pause-/Retry-Fix, Einzel-Fehlerisolation und frühe QA9-Veröffentlichung sind ebenfalls bereits gebaut. **Diese Schritte nicht erneut als noch nicht umgesetzt planen.** Erst die echte WordPress-Wirkung ist offen.

Realer neuester CSV-Export desselben 3e9e-Run (138 offene Familien): **94 mit Treffern, aber keine angenommen; 43 ohne Suchtreffer; 1 technisch offen.** Er enthält 1.329 Treffer im Suchausschnitt und 610 **`ebay_marketplace_mismatch`-Ablehnungsereignisse** (bei 68 Familien). Der strikte EBAY_DE-Herkunftsfilter war **schon am 07.11.** in den Upstream-Referenzen begründet. `deliveryCountry:DE` ist dafür kein Ersatz. Die bewusste Regel **nicht** blind lockern; die Ablehnung in den jeweiligen Portalquellen vergleichen. Die QA7-vs-QA9-Versionen enthalten die **identischen** vier Kernmethoden für Artikelannahme, eBay-Suche, gespeicherte Bestandswiederverwendung und Suchwortvarianten.

**Korrektur:** „Erst eBay suchen, danach erstmals vorhandene Produkte berücksichtigen“ war zu pauschal. Im bereits implementierten `gapfill_select` werden bekannte geeignete Quellen wiederverwendet; der Initiallauf hat außerdem bereits 299 aktiv/materialisiert. Die aktuelle `gapfill_discovery` aktualisiert öffentliche Abdeckung nicht schrittweise. Das ist für sich kein Produkt-/Workflow-Ausfall.

[Vollständiger Ursachen- und Doppelarbeitsabgleich auf dem eBay-QA-Zweig](https://github.com/hallo-netizen/affiliate-pferdeportal/blob/qa/pferdeatelier-ebay-319-qa5-evidence-20261110/protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/AFFILIATE/EBAY_ABDECKUNG_BESTAND_AUDIT_KEINE_DOPPELARBEIT_20261110.md). **Nur Bericht, keine neue ZIP, keine Änderung an HD/HAB-Plugins.**
