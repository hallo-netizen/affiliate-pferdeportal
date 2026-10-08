# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-10-08
STATUS: V1.13.3 LIVE-SYNC EVENTS-REISEN [name] TERMINAL ROLLED_BACK / FEHLER LOKAL 1:1 REPRODUZIERT / V1.13.4 FULL LOCAL POSITIVE+NEGATIVE WORKFLOW FRESH-ZIP HARD PASS / ZIELPROFIL UNVERÄNDERT / KEIN LIVE-SYNC / FRISCHER V1.13.4-DRYRUN OFFEN

## Plugin

ID:
`HD-001-KATEGORIE-WORKFLOW`

Name:
`Affiliate-Portal Kategorie-Workflow`

Art:
Eigenentwicklung / allgemeingültiger Kategorie-Workflow mit Hobby-Depot-Profil.

Fachbüro:
`SEO_KATEGORIEN`

## Letzter autoritativ bestätigter Live-Stand

V1.9.9:
Buchbinden + vier Content-Kategorien + zugeordneter Testartikel real im Frontend bestätigt.

Für V1.12.0 existiert KEIN realer Hobby-Depot-Live-PASS.

## Aktuelle technische Basis

Plugin-Version:
`1.12.0`

Lokales Release-Artefakt:
`HD001_V1.12.0_FIXED_THREE_PILLAR_TARGET_TREE_POSNEG_HARDPASS.zip`

SHA-256:
`f77f676ef4e8df8d44e3cf0d1e61b52883d402924cb8d14033c24dd6645c03d1`

Lokaler Prüfbericht:
`HD001_V1.12.0_FINAL_LOCAL_POSNEG_REPORT.txt`

Der ZIP-Hash wurde am 2026-10-07 erneut aus dem vorhandenen Artefakt geprüft.
Plugin-Header und `APKW_VERSION` = `1.12.0`.

## Was V1.12.0 technisch beweist

- versioniertes 3-Säulen-Zielprofil;
- generischer Target-Tree-Runner;
- Soll/Ist-Sync;
- Add / Rename / Move;
- Merge/Alias-Unterstützung;
- Archive/Inaktiv statt Hard Delete;
- stabile IDs bei gleicher Objektidentität;
- atomare Aktivierung nach Write + Readback;
- Rollback bei Readback-Manipulation;
- Cross-Pillar Keyword-/Intent-Kannibalisierung fail-closed;
- UNKNOWN/NONE-Themen bleiben redaktionell erhalten;
- Treibholz/Treibholz sammeln dedupliziert;
- DataForSEO darf im Target-Tree-Weg Struktur nicht erzeugen/verschieben;
- generisches Nicht-Hobby-Profil lokal validiert.

Lokale Evidence aus dem exakten Release-Artefakt:
- PHP-Lint 55/55 PASS;
- Legacy Regression 270/270 PASS;
- V1.10 Portal-Suiten PASS;
- realer 908/844-Gesamtlauf PASS;
- 420/420 physische Zielobjekte Readback PASS;
- zweiter identischer Lauf: 0 Post-/Term-Writes;
- Add/Rename/Move mit ID-Erhalt PASS;
- Remove→Archive PASS;
- Rollback PASS;
- Buchbinden-Renderer/4 Leafs/stabile IDs PASS;
- Fresh-Unpack/ZIP-Integrität PASS.

## Aktueller Finalisierungskandidat

Plugin-Version:
`1.13.1`

Artefakt:
`HD001_V1.13.1_PRACTICAL_FINAL_TARGET_ONE_SYNC_HARDPASS.zip`

SHA-256:
`94dca6cfc6c792cf2b866fc76fef1bff12551f9b375b38a1a511a91876b1a7b5`

Prüfbericht:
`HD001_V1.13.1_FINAL_LOCAL_POSNEG_REPORT.txt`

Prüfbericht SHA-256:
`f2649cbd1f132b1e48dfcf95cd05db805e024bf3d29c8b0d4d3aebda0594cd2d`

Zielprofil:
`HD001_V1.13.1_PRACTICAL_TARGET_PROFILE_20261008.json`

Profil SHA-256:
`f5c6d9e5be7ee6184c50ded9db40549f4b1e2d2a8c29672f4eb7aa172ea8e014`

Zweck:
ein letzter realer Soll/Ist-Dry-Run gegen Hobby Depot und danach mit demselben geprüften Plugin genau ein kontrollierter Sync.

### Finaler Zielstand

- eingefrorener Master: 841 Identitäten;
- 340 CORE;
- 501 Finder/Editorial;
- 103 Basis-Logikknoten;
- 440 aufgelöste Logikknoten;
- 431 physische Zielobjekte;
- 404 Pages;
- 4 category;
- 15 journal_cat;
- 8 hp_listing_category;
- 9 relations.

Harte Weltenkorrektur:
- alle acht `core:world:*` = physische Rootseiten / CORE-Ebene 1;
- `Hobbywelten` = reine View-/Übersichtsseite;
- 8 Relations von Hobbywelten zu den acht Welten;
- kein `core:hub → core:world:*`-Parent mehr.

### Sicherheitsgrenzen

- `APKW_TARGET_TREE_MANUAL_ONLY = true`;
- Installation/Update/Admin-Aufruf startet keinen Sync;
- Dry-Run hat 0 DataForSEO-/Provider-Aufrufe;
- Dry-Run hat 0 Strukturwrites;
- Apply benötigt gespeicherten Dry-Run-Fingerprint;
- Live-State wird direkt vor Apply erneut geprüft;
- Drift → Apply BLOCKED und neuer Dry-Run nötig;
- Sync bounded per AJAX + Cron-Fallback;
- automatische Archivierung nur für Objekte mit echtem `_apkw_target_node_id`;
- Legacy-Artikel-/Kategoriestrukturen ohne Target-Binding werden nicht automatisch archiviert;
- Foreign Slug/Name collision = BLOCKED;
- unveränderte Meta-Werte werden nicht neu geschrieben.

### Lokale harte Abnahme

- aktuelle Regression 270/270 PASS;
- V1.13.1 Final-Target-Suite 24/24 PASS;
- V1.12-Baseline→V1.13.1 Migration 11/11 PASS;
- Fresh ZIP PHP 33/33 PASS.

Baseline-Migration simuliert:
- V1.12: 420 physische Zielobjekte;
- V1.13.1 Dry-Run: 12 CREATE / 419 UPDATE / 1 ARCHIVE;
- einmaliger Sync COMPLETE;
- danach: 431 UNCHANGED;
- echte Post-Strukturwrites: 12 Inserts / 9 Updates / 0 Deletes;
- Term-Strukturwrites: 0 / 0 / 0.

V1.12.6 bleibt nur historische read-only Kalibrierung.
Keine weiteren V2-Batches.

## Fachliche Fortschreibung NACH V1.12.0

Die V1.12.0-Technik bleibt Basis, aber das gebündelte Hobby-Depot-Zielprofil ist NICHT der endgültige neue Installationsbaum.

Nach V1.12.0 wurde verbindlich vorgeschaltet:
`HOBBY_MASTER V2`.

Neue fachliche Regeln:
- große bekannte Hobbys als wirtschaftliche Anker integrieren;
- mittlere Hobbys als Rückgrat;
- Nischen als SEO-/Longtail-Stärke;
- großer interner Bestand, kleine sichtbare Navigation;
- Rollen ORIENTATION_UNIVERSE / HOBBY_HUB / EDITORIAL_TOPIC / ARTICLE_ONLY / FINDER_ONLY / OUT_OF_SCOPE;
- Größenprüfung vor Zielbaum;
- Monetarisierung beeinflusst CORE-Priorität, nicht Erhalt;
- DataForSEO ist SEO-Evidenz, keine Strukturautorität;
- acht Hauptwelten sind oberste fachliche CORE-Ebene.

## Bekannter V1.12-Profilfehler gegenüber der neuen Fachregel

Das V1.12-Hobby-Profil modelliert:
`core:hub (Hobbywelten) → core:world:gestalten/fertigen/...`

Das ist fachlich inzwischen verworfen.

Verbindlich:
Die acht Welten sind CORE-Ebene 1.
`Hobbywelten` ist nur Übersicht/View/Einstieg und kein Parent.

Dieser Fehler wird NICHT durch manuelles Patchen des alten Livebaums gelöst, sondern im späteren V2-Zielbaum-Delta.

## ERSTER REALER LIVE-BEFUND V1.13.1 – HISTORISCHER ROLLBACK-ZUSTAND

Dry-Run:
PASS / 12 CREATE / 419 UPDATE / 1 ARCHIVE / 0 Writes / 0 Provider-Calls.

Aber:
ein historischer Zielbaum-Sync ist noch `ROLLBACK_PENDING`.

Real:
- alte Revision `HD-TARGET-3P-V1-20261007+313e8ac433c0b154`;
- 620 Rollback-Aktionen offen;
- alter Readbackfehler `directory:events-reisen [name]`;
- Runner `RUNNING / EXISTING_TARGET_TREE_RESUME`;
- kein aktiver finaler Snapshot.

Sicherheitswirkung:
- Finaler Apply wird aktuell nicht angeboten;
- die Finaler-Zielbaum-Seite setzt den alten Rollback bounded automatisch fort;
- nach terminalem Rollback muss ein neuer Dry-Run erzeugt werden;
- Apply prüft den Live-Fingerprint erneut und blockiert stale Pläne.

## REALER LIVE-BEFUND

V1.13.1 realer Final-Dry-Run:
PASS.

Delta:
- 12 CREATE;
- 419 UPDATE;
- 1 ARCHIVE;
- 431 physische Zielobjekte;
- 0 Provider-Calls;
- 0 Strukturwrites.

Damit ist der eigentliche finale Plan real bestätigt.

Im selben Export steckt noch ein alter Sync-State aus V1.12:
`ROLLBACK_PENDING` wegen `directory:events-reisen [name]`.

Der V1.13.1 Runner übernimmt diesen alten Rollback automatisch.
Kein neuer Final-Sync wurde gestartet.

## POST-ROLLBACK-FRISCHCHECK – CURRENT

Frischer Live-Dry-Run mit demselben V1.13.1-Kandidaten:
- PASS / valid=true;
- 841 Identitäten;
- 340 CORE;
- 501 Finder/Editorial;
- 440 Logikknoten;
- 431 physische Zielobjekte;
- 356 CREATE;
- 75 ADOPT;
- 0 UPDATE;
- 0 ARCHIVE;
- 0 Provider-Calls;
- 0 Strukturwrites;
- alter V1.12-Runner terminal `ROLLED_BACK`;
- kein aktiver finaler Snapshot;
- kein Final-Sync gestartet.

Fachlicher Vollabgleich:
`SEO_KATEGORIEN/HD001_V1_13_1_POST_ROLLBACK_CONCEPT_AUDIT_20261008.md`

## MATERIALKUNST-FIX – ECHTES ARTEFAKT

Original:
`HD001_V1.13.1_PRACTICAL_FINAL_TARGET_ONE_SYNC_HARDPASS.zip`
SHA-256 `94dca6cfc6c792cf2b866fc76fef1bff12551f9b375b38a1a511a91876b1a7b5`

Korrigiert:
`HD001_V1.13.1_PRACTICAL_FINAL_TARGET_ONE_SYNC_HARDPASS_MATERIALKUNST_FIX.zip`
SHA-256 `ea5aa8316b2537695f2f805d0b9cc4b0d9f973fb609c231ab7c3067de419c263`

Profil:
`HD001_V1.13.1_PRACTICAL_TARGET_PROFILE_20261008_MATERIALKUNST_FIX.json`
SHA-256 `2fe534e0d25af038c49c3eaa2b9e9c38c71daac051a217ef65a92f8b077a9b95`

Änderung:
nur `core:gestalten:materialkunst` entfernt.

Patch-Abnahme:
- exakter Ein-Knoten-Diff PASS;
- frischer PHP-Lint 33/33 PASS;
- ZIP-Integrität PASS;
- Plan-Graph-Simulation PASS;
- erwartet 430 physische Zielobjekte / 403 Pages / 355 CREATE + 75 ADOPT.

Die historischen 270/270-, 24/24- und 11/11-Entwicklungstests werden für diesen Patch NICHT fälschlich als neu ausgeführt behauptet; der Test-Harness steckt nicht im Produktions-ZIP.

Beleg:
`SEO_KATEGORIEN/HD001_V1_13_1_MATERIALKUNST_FIX_LOCAL_BUILD_20261008.json`

## KORRIGIERTER LIVE-DRYRUN – PASS

`hobby-depot-final-target-readback-20261008-100800-utc.json`

PASS:
- 439 Logikknoten;
- 430 physische Zielobjekte;
- 403 Pages;
- 4 category;
- 15 journal_cat;
- 8 hp_listing_category;
- 355 CREATE + 75 ADOPT;
- errors = [];
- 0 Provider;
- 0 Strukturwrites;
- Materialkunst nicht mehr enthalten;
- alter V1.12-Sync = ROLLED_BACK;
- kein aktiver Final-Snapshot, da Final-Sync noch offen.

## V1.13.1 FINAL-SYNC – FEHLER UND FIX

Fehler:
`Target-Tree-Readback fehlgeschlagen: core:fertigen:buch-papier [slug]`

Dry-Run:
355 CREATE + 75 ADOPT.

Tatsächlicher Sync vor Readback-Stopp:
415 created + 15 adopted.

Damit wurden exakt 60 geplante ADOPT-Seiten neu angelegt.

Root Cause:
`find_by_slug()` nutzte für Seiten `get_page_by_path($slug)`; bei hierarchischen Unterseiten reicht der Blatt-Slug dort nicht.

V1.13.2:
- bounded `get_posts(... post_name__in => [$slug])`;
- >1 Treffer bleibt fail-closed;
- Zielprofil unverändert;
- Materialkunst bleibt entfernt.

Artefakt:
`HD001_V1.13.2_ADOPT_CHILD_SLUG_FIX_HARDPASS.zip`
SHA-256 `d9cb80d8e5635fd94ac390dc0be75757d1a7a964b0ce0cb1cf893934eed35cc7`

Tests:
33/33 PHP-Lint PASS + gezielter Child-Slug-/Ambiguity-/Missing-Test PASS.

## V1.13.3 FULL-SYNC-PARITY

V1.13.2 war noch nicht ausreichend:
Dry-Run und Sync unterschieden sich bei der Legacy-concept_id-Suche.

V1.13.3 gleicht die Sync-Suche vollständig an den Dry-Run an:
`_apkw_target_node_id`
→ `_apkw_concept_id` mit current node_id + legacy_ids
→ Slug-Fallback.

Lokaler Volltest mit echtem 430-Knoten-Plan:
- 355 CREATE;
- 75 ADOPT;
- 0 UPDATE;
- 430/430 Readback PASS;
- COMPLETE;
- zweiter Lauf 430 UNCHANGED;
- Rollback ROLLED_BACK;
- 11 umbenannte Legacy-ADOPTs PASS;
- Ambiguity fail-closed PASS;
- 33/33 PHP-Lint PASS;
- Zielprofil unverändert.

Artefakt:
`HD001_V1.13.3_FULL_SYNC_PARITY_HARDPASS.zip`
SHA-256 `f255b06fb38c7b903de2c7741dea4e02fb9620ad3a6651fbf5963f402c33820b`

## V1.13.3 LIVE – FEHLER

Realer Sync:
355 created + 75 adopted.
Readback stoppte nach 63 Knoten bei
`directory:events-reisen [name]`.
Danach vollständig `ROLLED_BACK`.

## V1.13.4 FULL LOCAL POS/NEG

Root Cause:
entity-kodierte Taxonomie-Namen wurden im Target-Readback roh verglichen.

Fix:
Termnamen im Dry-Run und Sync vor Vergleich dekodieren.
Page-Namen bleiben strikt.
Zielprofil unverändert.

Fresh-ZIP-Volltest:
- 355 CREATE + 75 ADOPT Dry-Run;
- Fresh-Fingerprint-Parität PASS;
- Sync 355/75;
- 430/430 Readback PASS;
- COMPLETE;
- 403/403 Page-Frontend PASS;
- alle drei Portal-Hubs PASS;
- Front-/Footer PASS;
- Admin-Frontend-Readback PASS;
- zweiter Dry-Run 430 UNCHANGED;
- zweiter Sync 430 UNCHANGED;
- Readback-/Page-/Term-Fehlerrollback PASS;
- Ambiguity/Foreign-Slug/Invalid-Profile/Missing-Taxonomy fail-closed PASS;
- 33/33 PHP-Lint;
- ZIP-Integrität PASS.

Artefakt:
`HD001_V1.13.4_FULL_LOCAL_POSNEG_HARDPASS.zip`
SHA-256 `4ca1fb163f2ca5082d5b264a3d1b1862ee4b94039eeadd0c9b9f98e7270eb251`

Prüfbericht:
`HD001_V1.13.4_FULL_LOCAL_POSNEG_HARDPASS_REPORT.txt`
SHA-256 `653b76c0f923a97181f5848ec3560579194b7c020fd5b06500134180d1564d30`

## ERSTER OFFENER BLOCKER

`HD001_V1_13_4_FRESH_LIVE_DRYRUN_PENDING`

## EXAKT EINE NEXT ACTION

Exakt V1.13.4 installieren → genau einen frischen finalen Delta-Dry-Run → JSON exportieren.
Noch keinen Live-Sync starten.

## Release-/Artefaktgrenze

V1.13.1 ist der aktuelle lokal hart geprüfte Finalisierungskandidat.

Isolierte Artefaktpflicht:
`PLUGINS/ISOLIERTE_PLUGINS/HD-001-KATEGORIE-WORKFLOW/MANIFEST.md`

Das installierbare geprüfte ZIP liegt als Gesprächs-/Library-Artefakt vor.
Das GitHub-`CURRENT.zip` ist weiterhin nicht bytegenau synchronisiert, weil der aktive GitHub-Connector keinen direkten Binärupload aus dem Container anbietet. Kein Ersatzartefakt erfinden.

Kein Live-PASS behaupten, bevor:
Dry-Run → akzeptierter Delta-Readback → einmaliger Sync → Struktur-/Frontend-Readback abgeschlossen sind.
