# HD-009 – kein zweiter Bannerweg; nativer Auto-Zielpfad + kostenloser DataForSEO-Test (07.11.2026)

## Beweiskette
- Ausgangsbasis: tatsächliche GitHub CURRENT.zip **0.1.12-dev**, SHA-256 `7ebbea15bb9f1692a949c41cc982489f5be2a2d12695e9342cac7dc8ce1550ae` (707639 Bytes).
- Korrigierte ZIP: **0.1.13-dev**, Größe **707164 Bytes**, SHA-256 `d6536031f0eca61c15a2d8c754015ed92de3ad474da9a10e961782a076681d43`, Blob `fd18e2caea3836a8054189edac67e70c9c6d10b0`. Gleicher Pluginordner `affiliate-portal-router/`, gleiche Hauptdatei.
- **Keine weitere Engine, keine zusätzliche Plugininstallation, keine Kategorieänderungen.**

## Exakter Quellbefund und minimale Korrektur
- Die bereits aus Pferdeatelier übernommene Automatik **existiert** in `includes/trait-ppar-output-objects.php` und `includes/trait-ppar-automation-suite.php`: automatische Themen-/Zielwahl, Elternpfad, Tiefenrangfolge, Format-/Slotprüfung, Sicherheitsgates. Auch `hobby-depot-affiliate-router.php` wählt vorhandene passende Kampagnen über `select_campaign_for_slot()`.
- **0.1.12-Fehler:** `includes/class-hdar-amazon-start.php` führte `hdar_banner_assign`, gesonderte Formularseite und eigenes `house_banner()` ein. `render_affiliate_slot_for_context()` unterdrückte bei aktiviertem Amazon+idealo-Modus alle Nicht-Produkt-Slots, bevor die vorhandene Auto-Bannerwahl wirken konnte.
- **0.1.13-Fix:** Alten manuellen Zusatzweg inklusive eigener Banner-Ausgabe entfernt. Werbeplätze (auch Quer-/Quadratplätze) laufen wieder durch **denselben vorhandenen zentralen Auswahlweg**. Anbieterbegrenzung für den Start bleibt Amazon+idealo; nichts von eBay/OTTO wird darüber veröffentlicht. Ohne passende gültige Kampagne kein fremder Platzhalter.
- Amazon-Direkt-Produktrecherche und gezielte ASIN-Freigabe unverändert; bestehende Provider-, Hobby- und Datenbankoptionen unverändert. Die früher beigepackten Modellbau-Motivdateien wurden nicht gelöscht, aber **nicht** als schon automatisch importierte Werbemittel ausgegeben. Für automatische Verteilung müssen eigene Motive über den bestehenden zentralen Werbemittelbestand bereitgestellt werden; kein neuer manueller Banner-Dialog.

## Kostenfreier Zugangstest für DataForSEO
- Neuer Button in **Affiliate-Zentrale → Amazon + idealo**: `DataForSEO-Verbindung kostenlos prüfen`.
- Prüft die **bereits gespeicherten** API-Credentials per authentifiziertem GET `https://api.dataforseo.com/v3/appendix/user_data`, laut offizieller API-Dokumentation ohne Berechnung. Kein Merchant-/Produkt-API-Aufruf, keine regelmäßige Abfrage.
- WordPress-Rechteprüfung, Nonce, 15-Sekunden-Limit; Erfolg nur bei HTTP 200 und API-/Taskstatus jeweils 20000. Differenzierte Fehlermeldung bei 401/403, 429, Netz-/Server-/API-Fehler. Keine API-Passwörter oder Antwortdaten in Logs/Status gespeichert.
- Website-Tracking-ID bleibt Hobbydepot-spezifisch; keine Zugangsdaten im Repo.

## Tatsächlich ausgeführte Tests
- ZIP-Integrität: **PASS**, 30 reguläre Dateien, nur Pluginroot.
- PHP 8.4 Syntaxprüfung: **24/24 PASS**.
- Static checks PASS: manueller Bannerposthandler/Formular/Renderer entfernt; bestehender nativer Banner-Zielpfad und Formatregeln weiterhin vorhanden, Start-Sperre für automatische Banner aufgehoben.
- PHP-Offline-Smoke PASS: DatenForSEO-Test mit simuliertem 200/20000-Erfolg, HTTP 401, 429 und 500; nur GET gegen kostenlosen User-Data-Endpunkt, nie ein kostenpflichtiger POST.
- **Grenze:** Nicht auf echter WordPress-Installation oder mit echten DataForSEO-Zugangsdaten ausgeführt. Bestehende Eigenbanner-Bilddateien liegen weiterhin im ZIP, gelten jedoch ohne Registrierung im vorhandenen Werbemittelbestand nicht als live automatisch verteilt.

## Einzige Büro-/Release-Zuordnung
- Fachliche Current: `HOBBYRAUSCH/AFFILIATE/CURRENT_STATE.md`.
- Technische einzige ZIP: `HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip`.
- Keine zweite Affiliate-Pluginlinie, kein konkurrierendes Büro.
