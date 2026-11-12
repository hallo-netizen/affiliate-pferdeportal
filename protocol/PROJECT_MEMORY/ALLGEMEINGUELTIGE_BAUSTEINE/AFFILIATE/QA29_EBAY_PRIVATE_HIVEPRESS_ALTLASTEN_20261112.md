# QA29 – private eBay-HivePress-Altanzeigen trotz stillgelegtem PRIVATE-Import (12.11.2026)

**Status:** Vollständiges KISS-Plugin **6.72.334**, lokal geprüft, **nicht auf Live-WordPress installiert**. Nutzer hatte 6.72.333 bewusst noch NICHT installiert; 6.72.334 enthält dessen eBay-Einzelsteuerung und die zuvor benutzerbestätigte Amazon-Ausgabe.

## Nachweis der Ursache im unveränderten 6.72.333
- Die eigene **readme.txt** sagt bei **V6.72.234** ausdrücklich, dass die vorherige automatische Admin-Init-Bereinigung entfernt wurde und bestehende PRIVATE-Datenbank-Altlasten **NICHT** gelöscht werden. Der PRIVATE-eBay-Import wurde nur stillgelegt.
- In der Hauptdatei blieb nur `the_posts → ebay_filter_stale_posts`; dessen Code filtert ausschließlich `hp_listing` mit nichtleerem `_ppar_ebay_item_id`. Altlasten ohne diesen Marker können ihn umgehen; direkte HivePress-Aufrufe und fremde Suchabfragen müssen diesen WordPress-Filter nicht verwenden. Welche konkrete Header-Suche verwendet wird, ist im Affiliate-Plugin **nicht nachgewiesen**.
- Ein zweiter verbliebener Weg `ebay_run_retire_private_legacy_listings_tick` war nur in `reconcile` des kanonischen eBay-Laufs erreichbar, setzte maximal 25 veröffentlichte Posteinträge auf **draft** und löschte sie nicht. Der Live-Lauf befand sich bei `refresh_remote`, wo dieser Weg nicht läuft. Damit blieben WordPress-Posts, Suchtreffer und direkte URLs bestehen.

## Radikale KISS-Vereinfachung in EINER vollständigen ZIP
- Die **bestehende** `ebay_private_post_ownership` bleibt **einzige Herkunftsprüfung**: import-eigene `_ppar_ebay_*`-Markierung, inkl. alter Formate. Zu schwaches „Zielkategorie-Metafeld allein genügt“ ausdrücklich herausgenommen. Eine normale Anzeige mit manuellem eBay-Link ist **niemals** ausreichend als Löschbeweis.
- Die alte nur im eBay-Rechercheworker durchgeführte PRIVATE-Draft-Routine **entfernt**. eBay-BUSINESS-Recherche und alte PRIVATE-Bereinigung haben damit klar getrennte Zuständigkeiten.
- **Einmalig im bereits vorhandenen eBay-WordPress-Backend**: ein administratorgeschützter Knopf **„Private eBay-Altanzeigen endgültig entfernen“**. Nach bewusster Bestätigung prüft er ausschließlich nachweislich importierte `hp_listing`-Einträge, löscht diese mit dem nativen WordPress `wp_delete_post($id,true)`, automatisch in begrenzten 40er-Paketen bis zum Abschluss. Er prüft alle Poststatus, auch Entwürfe und Papierkorb. Fehler stoppen eindeutig, unbewiesene Einträge bleiben.
- **Keine zweite eBay-Zeitsteuerung, kein neuer Cron, keine neue Tabelle, keine neue Import-/Suchmaschine, kein Frontend-Umbau.** WordPress-Kern, K0, Amazon, idealo, eBay-BUSINESS-Speicherstände, GitHub-Heartbeat unverändert.

## Echte lokale Original-PHP-/Mocks-Regression
- **185/185 PRIVATE-Testfälle PASS**. 160 nachweislich importierte PRIVATE-Posts verschiedenster Status gelöscht; 120 normale/manuelle/unbewiesene HivePress-Anzeigen und 10 normale Blogposts unberührt; Cursor/Idempotenz/Fehler/DB-Ausfall geprüft.
- **70/70 eBay-KISS-Steuerungsfälle PASS**, **13/13 GitHub-v2-Schnittstelle PASS**, **41/41 Amazon-idealo PASS** inklusive sieben echter ASIN-Diagnosebeispiele.
- **23/23 PHP-Lint PASS**, Admin-JavaScript-Syntax PASS, **66/66 ZIP-Einträge CRC PASS**. Genau vier Quelldateien im Vergleich zu 6.72.333 geändert.
- Komplette Original-ZIP **6.72.334** mit SHA256 `8bb928d11b5a092a903476750cbab71f661d45f55645c0685334b5f16ad97a4e`; samt Patch, Original-PHP-Test, Prüfprotokoll und Integrität in der persönlichen Library unter `/pferdeatelier/PLUGINS/QA/`.

## Ehrliche Freigabegrenze
**Noch kein realer WordPress-/MariaDB-Löschlauf.** Zahl und konkrete Herkunft der verbliebenen Live-Posts sind ohne aktuellen DB-Auszug unbekannt. Der Nutzer muss nach Installation **einmal** den klar benannten Admin-Knopf betätigen und die bestätigte Abschlussmeldung abwarten. Danach Header-Suche und direkte alte URLs prüfen. Sollten alte Treffer ohne nachweisbare Importmetadaten bleiben, dürfen sie nicht ohne weitere Herkunftsprüfung pauschal gelöscht werden. Kein von uns ausgeführter Datenbank-Eingriff.

**Nächster Schritt:** EINMAL vollständige 6.72.334 statt der ungenutzten 6.72.333 installieren → eBay-Fachseite → PRIVATE-Altlasten-Knopf → Abschluss → reale Header-/Permalink-Abnahme. Den bestehenden eBay-BUSINESS-Lauf weder zurücksetzen noch neu starten.

## Live-Abnahme 12.11.2026 – FEHLGESCHLAGEN, keine Löschung

Benutzer hat Plugin 6.72.334 installiert, Adminbereinigung ausgeführt und meldet wortwörtlich: **„Fertig: 0 eindeutig erkannte eBay-Altanzeigen endgültig entfernt.“** Die privaten eBay-Anzeigen sind nach seiner Sicht weiterhin im öffentlichen Suchindex bzw. über HivePress-URLs erreichbar. Somit ist QA29 **nicht live erfolgreich**; lokaler 185/185-Mock-Test ist für echte Altbestände nicht repräsentativ.

Im Original-ZIP 6.72.334 direkt bestätigt: `ebay_private_cleanup_batch()` sucht *ausschließlich* `hp_listing`-Posts mit Metaschlüsseln `_ppar_ebay_item_id`, `_ppar_ebay_seller_type`, `_ppar_ebay_affiliate_url`, `_ppar_ebay_source_hash`, `_ppar_ebay_portal_path`, `_ppar_ebay_target_term_id`. Die bestehende `ebay_private_post_ownership()` reduziert diese Kandidaten noch einmal auf belegte Plugin-Herkunft. Im Admin-Frontend wird **nur die Anzahl `deleted`** ausgegeben; die Zahl der `unproven_skipped` und die Zahl aller verbleibenden `hp_listing` werden nicht sichtbar gemacht. Deshalb ist aus `0` **nicht belegbar**, ob gar keine Kandidaten gefunden oder alle als nicht nachgewiesen übersprungen wurden. **Daraus darf nicht geschlossen werden, dass es keine Altanzeigen gibt.**

**Verbindliche nächste Diagnose vor weiterer Programmänderung:** Echte verbliebene `hp_listing`-Datensätze einschließlich aktueller Postmeta/Taxonomien und vorhandener eBay-Links aus dem aktuellen WordPress-WXR-Export oder einem gleichwertigen lesenden Bericht untersuchen; den tatsächlichen historischen Importmarker anhand mindestens eines eindeutig belegten Restposts nachweisen. Erst danach dieselbe bestehende Herkunftsentscheidung an der ursprünglichen Stelle korrigieren und erneuten Live-Abnahmetest vornehmen. Keinen pauschalen `hp_listing`-Delete, keine Löschung allein aufgrund eBay-URL, Titel oder generischer Kategorie. **Keine weitere ZIP blind installieren; QA29 als nicht abgenommen markieren.**
