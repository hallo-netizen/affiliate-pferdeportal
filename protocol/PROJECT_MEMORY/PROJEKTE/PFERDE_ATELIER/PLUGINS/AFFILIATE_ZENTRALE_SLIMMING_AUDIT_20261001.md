# AFFILIATE-ZENTRALE – SLIMMING-AUDIT 2026-10-01

STATUS: READ_ONLY_AUDIT / KEIN SOURCE-WRITE / KEIN PERFORMANCE-RÜCKBAU

## Autoritative Ausgangsbasis

- Release-Branch: `affiliate-release-current`
- aktueller Kandidat: **6.72.172**
- aktuelles Source-Manifest: `286fcedf2e7fa1eca441abb52d46254bf39f0d0fd6c63daa81f032d8e605e33c`
- 6.72.172 baut auf dem Performance-Stand 6.72.171 auf.
- Die 6.72.171-Request-Caches/Ranking-Optimierungen bleiben tabu.
- Aktuelle Release-NEXT-ACTION bleibt: `REAL_WORDPRESS_INSTALL_READBACK_6_72_172`.
- Dieser Audit verändert keine Release-Source und eröffnet keinen Parallel-Release-Strang.

## Ist-Größe

Aktueller Pluginbaum: ca. **6,69 MB**.

Drei große JSON-Bestände allein: ca. **3,90 MB / 58,2 %**:
1. `assets/portal-structure-v279.json` – 1.475.525 Bytes
2. `recovery/aff043-historical-product-state-20260915.json` – 1.392.218 Bytes
3. `assets/ebay-portal-catalog-v2.json` – 1.029.397 Bytes

Große PHP-Blöcke:
- `pferdeportal-affiliate-router.php` – 717.358 Bytes / ca. 10.972 Zeilen / 345 Funktionen
- `trait-ppar-ebay.php` – 691.265 Bytes / ca. 10.451 Zeilen / 326 Funktionen
- `trait-ppar-ebay-run.php` – 143.759 Bytes / ca. 2.150 Zeilen / 87 Funktionen

## Belastbare Verschlankungskandidaten

### A – aktueller echter Rootfehler / gleichzeitig Altlast
Der eBay-Katalog enthält aktuell **334 Produktziele / 1149 Artikelkategorien**, der Validator erwartet aber noch fest **329 / 1124**.

Folge:
- Portalabdeckung bricht real ab;
- dieselbe Altlast kann bei jeder legitimen Strukturänderung erneut auftreten.

Nachhaltiges Ziel:
- keine hart codierten historischen Gesamtzahlen als Laufzeitwahrheit;
- Katalog intern gegen seine realen Arrays/Hash/Schema prüfen;
- keine Lockerung von Validierung oder Safety.

### B – 1,48-MB-Portalstruktur wird im Frontend vollständig geparst
`portal_structure_product_family_for_category()` lädt beim ersten Kategoriebedarf die komplette `portal-structure-v279.json`, obwohl dort nur die Abbildung
`category_slug -> product_slug`
benötigt wird.

Zielkandidat:
- kompakter, aus der autoritativen Portalstruktur erzeugter Runtime-Index;
- gleiche 1:1-Zuordnung;
- kein zusätzliches DB-Lesen;
- A/B-Beweis gleiche Kontexte/Slots/HTML;
- vollständige Portalstruktur bleibt Autorität außerhalb des Hot Paths.

### C – historischer AFF043-Snapshot im Runtime-Paket
Der 1,39-MB-Snapshot dient einem incident-only Fallback für ehemals aktive eBay/idealo-Kampagnen.

Er darf NICHT einfach gelöscht werden.

Erst wenn ein Read-only-Audit beweist, dass kein aktueller sichtbarer Kampagnenpfad diesen Incident-Fallback mehr benötigt:
- Incident-Fallback stilllegen;
- Snapshot aus dem normalen Runtime-Paket entfernen/archivieren;
- Gegenprobe: kein Produkt verschwindet, kein inaktives Produkt wird unzulässig sichtbar.

### D – One-time/Legacy-Hooks laufen weiterhin auf normalen `init`-Requests
Belegt sind u. a.:
- `retire_ebay_legacy_cron_transport()`
- `ensure_ebay_maintenance_schedule()` als Alt-Schedule-Cleanup
- `maybe_upgrade_background_schedule_v67264()`
- `maybe_restore_v67294_banner_state()`
- `maybe_restore_published_banner_campaign_consistency_v672100()`
- `maybe_upgrade_adcell_topic_metadata_v67288()`
- weitere Migrations-/Recovery-Gates.

Ziel:
- NICHT Funktion löschen;
- abgeschlossene One-time-Migrationen über einen einzigen aktuellen Schema-/Migration-Watermark kurzschließen;
- alte Cleanup-/Recovery-Funktionen nur ausführen, solange ihr Zustand tatsächlich offen ist;
- normale Frontendrequests dürfen nach abgeschlossenem Upgrade keine historischen Reparaturen immer wieder prüfen.

### E – alte eBay-Transport-Kompatibilität
Der kanonische eBay-Transport ist inzwischen externer Heartbeat; trotzdem existieren mehrere Legacy-Wrapper und wiederholte Cron-Retire-Pfade.

Ziel:
- erst Live-Options-/Cron-Readback;
- beweisen, dass keine alte Schedule/kein kompatibler Alt-Run mehr existiert;
- danach nur nachweislich tote Wrapper entfernen oder auf einen einmaligen Migration-Gate reduzieren;
- Recovery-/Account-Deletion-/Safety-Verträge bleiben vollständig erhalten.

### F – versteckte Alt-Adminansichten
Noch registriert:
- `Affiliate-Kampagnen Altansicht`
- weitere versteckte technische Altseiten.

Nur entfernen, wenn:
- keine aktuelle KISS-Seite, Action, Nonce, Redirect oder Support-/Recovery-Funktion dorthin verweist;
- vollständiger Admin-Route-/Action-Gate PASS.

## Was ausdrücklich NICHT angefasst wird

- 6.72.171 request-lokale Ranking-/Gate-/Provider-Caches;
- Slot-Veto und Provider-Mix;
- PRIVATE/BUSINESS-Safety;
- eBay Account Deletion Compliance;
- Control/Veto;
- Banner-Relevanz-/Verteilung;
- Tracking;
- aktuelle Housekeeping-Logik aus 6.72.172;
- WordPress/HivePress native Anzeigen;
- Providerdaten oder echte Produkt-/Creative-Bestände.

## Abnahmevertrag für jede spätere Verschlankung

Jeder einzelne Cleanup muss beweisen:
1. Positivfälle identisch;
2. Negativfälle identisch/fail-closed;
3. HTML/Slot-Auswahl/Kandidatenreihenfolge unverändert, sofern der Cleanup nicht exakt einen belegten Fachfehler repariert;
4. keine neue DB-/Term-/Providerabfrage;
5. keine Performanceverschlechterung gegen 6.72.171/aktuellen Nachfolger;
6. Fresh-Unpack/Manifest/Version PASS;
7. erster FAIL = STOP, nur diesen Punkt fixen.

## Reihenfolge

1. 6.72.172 real installieren/readbacken – unverändert.
2. Aktuelle Funktionsfehler schließen:
   - Portalabdeckung/Katalog-Altzahl;
   - eBay BUSINESS-Ausspielung;
   - Banner-Fachzuordnung (z. B. Schabrackendesigner -> Schabracken);
   - eBay PRIVATE/HivePress „gezählt, aber nicht sichtbar“.
3. Danach Cleanup in kleinen, messbaren Blöcken; niemals mehrere Altlasten gleichzeitig entfernen.
