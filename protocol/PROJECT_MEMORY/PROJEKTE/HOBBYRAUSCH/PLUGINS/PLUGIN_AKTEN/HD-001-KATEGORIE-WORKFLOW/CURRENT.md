# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-10-09
STATUS: V1.14.8 LIVE TECHNISCH COMPLETE / PLUGIN-ENTWICKLUNG EINGEFROREN BIS FACH-SOLL 2.7 PILOT ABGENOMMEN

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

## Historische technische Basis V1.12.0

Historische Plugin-Version:
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

## Historischer Finalisierungskandidat V1.13.1

Historische Plugin-Version:
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

## V1.13.4 LIVE-DRYRUN – PASS

`hobby-depot-final-target-readback-20261008-113205-utc.json`

- PASS / valid=true;
- 355 CREATE + 75 ADOPT;
- 430 Zielobjekte;
- errors = [];
- 0 Provider;
- 0 Strukturwrites;
- alter V1.13.3-Fehlsync = ROLLED_BACK;
- rollback_actions = [].

## REGEL-/KONZEPTAUDIT – V1.13.4 NICHT FINAL

Beleg:
`SEO_KATEGORIEN/HD001_V1_13_4_FULL_RULE_CONCEPT_AUDIT_20261008.md`

Technisch getestet heißt nicht fachlich final.
Die Sichtprüfung deckt auf:
- Header-/Theme-Navigation folgt nicht exklusiv dem Target-Snapshot;
- ungebundene Legacy-Seiten bleiben sichtbar;
- Magazine-Taxonomien werden nicht in die Header-Navigation projiziert;
- Treibholz/Treibholz sammeln leakt als Legacy-Dublette in CORE;
- mehrere konzeptionell getrennte Zwischenbereiche wurden im V1.13.4-Zielprofil zusammengezogen.

Wichtig:
Die dritte Seitenebene der 340 CORE-Hobbys existiert im Zielprofil.
Nur die darunterliegende WordPress-Kategorieebene ist aktuell fast nur beim Buchbinden-Pilot vorhanden; dies entspricht Zielvertrag 2.5 und wird nicht ohne neue Regel global vervielfacht.

## V1.14.0 – FULL LOCAL HARD PASS

Ziel:
sichtbare Navigation, Magazin und fachliche Zwischenstruktur gegen Zielvertrag 2.5 / Regeln 1.5 / 3-Säulen-Konzept korrigieren.

Ergebnis:
- Target-Snapshot-only Header;
- Legacy-/Editorial-Leaks geschlossen;
- Treibholz-Dublette aus CORE-Navigation entfernt;
- feste Magazin-Navigation komplett;
- 59 aktive Zwischenbereiche;
- keine leeren Konzeptäste;
- 841 Identitäten / 340 CORE erhalten;
- keine unbelegten Alias-Merges;
- 437 physische Ziele;
- Full Positive + Full Negative + V1.13.4-Migration PASS;
- 33/33 PHP-Lint vor und nach frischem Unzip;
- ZIP-Integrität PASS.

Artefakt:
`HD001_V1.14.0_STRUCTURE_NAV_MAGAZIN_FULL_POSNEG_HARDPASS.zip`
SHA-256:
`87246ecd24b1facc5c3b80c0e3593b2a0bd9391143ef6f190d6786ecfa62cda3`

Beleg:
`SEO_KATEGORIEN/HD001_V1_14_0_STRUCTURE_NAV_MAGAZIN_FULL_LOCAL_HARDPASS_20261008.json`

## 19 EXPANSION-ANKER – FACHLICH GESCHLOSSEN

Beleg:
`SEO_KATEGORIEN/HOBBY_MASTER_V2_EXPANSION_ANCHORS_19_FINAL_ASSESSMENT_20261008.json`

Ergebnis:
- 19/19 IN_SCOPE;
- 12 HOBBY_HUB;
- 7 ORIENTATION_UNIVERSE;
- 0 exakte/current-Alias-Kollisionen;
- Monetarisierung bei allen 19 weiterhin UNKNOWN bis zu echtem Provider-Match;
- kein Plugin-/Target-Write aus der Bewertung selbst.

## V1.14.1 EXPANSION19 – FULL LOCAL HARD PASS

Fachbeleg:
`SEO_KATEGORIEN/HOBBY_MASTER_V2_EXPANSION_ANCHORS_19_FINAL_ASSESSMENT_20261008.json`

Delta:
`SEO_KATEGORIEN/HD001_V1_14_1_EXPANSION19_TARGET_DELTA_20261008.json`

Abnahme:
`SEO_KATEGORIEN/HD001_V1_14_1_EXPANSION19_FULL_LOCAL_HARDPASS_20261008.json`

Ergebnis:
- 860 Identitäten;
- 359 CORE / 501 Finder-Editorial;
- 60 aktive Zwischenbereiche;
- 466 aktive Logikknoten;
- 457 physische Ziele;
- 430 Pages;
- 97 Header-Einträge;
- keine künstliche globale Content-Kategorieebene;
- Essbare Pflanzen jetzt real belegt;
- Heimwerken/Gärtnern ohne künstlichen Zwischenbereich;
- UNKNOWN-Monetarisierung verhindert keine fachlich begründete CORE-Rolle, verlangt aber Editorial-Erhalt;
- Full Positive + Full Negative + V1.14.0-Migration + Frontend-Readback PASS;
- PHP 33/33 vor und nach Fresh-Unpack;
- ZIP-Integrität PASS.

Artefakt:
`HD001_V1.14.1_EXPANSION19_FINAL_POSNEG_HARDPASS.zip`

SHA-256:
`64735c31f474a782cc324c68218aade99ccfca4b54ab08091d5f28cfcecae95e`

Profil SHA-256:
`cd40cee8f1bceffae7c41b8bf2124965d49046caa2e27242af2122168a8412d0`

Master SHA-256:
`adf01a7ac9ae8a30813e9d27391d0732583671dd6c39b5cca19d33576dd8308f`

## LIVE-DRY-RUN – PASS

Beleg:
`SEO_KATEGORIEN/HD001_V1_14_1_LIVE_DRYRUN_PASS_20261008.json`

Plan:
- 32 CREATE;
- 425 UPDATE;
- 5 ARCHIVE;
- 0 ADOPT;
- 0 Provider;
- 0 Writes.

Die fünf Archive sind nur die fünf bekannten ersetzten Kombi-Zwischenknoten. Keine Hobbyseite wird archiviert.

## V1.14.2 – STALE COMPLETE UI-GATE FIX

Fehler in V1.14.1:
Ein alter gespeicherter Target-Sync mit `status=COMPLETE` blendet Abschnitt 2 aus, obwohl der aktuelle Dry-Run eine neuere `profile_revision` hat.

Fix:
`COMPLETE` gilt im Finaler-Zielbaum-Screen nur noch für dieselbe Revision wie der aktuelle Dry-Run.
Ein älterer COMPLETE-State blockiert den neuen Apply-Button nicht mehr.

Unverändert:
- Zielprofil;
- Hobby-Master;
- 860 / 359 / 501;
- 457 Zielobjekte;
- Live-Dry-Run 32 CREATE + 425 UPDATE + 5 ARCHIVE;
- Apply führt weiterhin unmittelbar vor dem Schreiben einen frischen Dry-Run und Fingerprint-Vergleich aus.

Lokale Checks:
- PHP 33/33 PASS;
- ZIP-Integrität PASS;
- Gate-Truth-Table PASS.

Artefakt:
`HD001_V1.14.2_STALE_COMPLETE_UI_GATE_FIX.zip`

SHA-256:
`b5bf0f6201a8158dc968530009d22195e8cc4a27b5421d84010840dafd282dbe`

## V1.14.3 – RULE16 VISIBLE FINAL HARD PASS

V1.14.3 enthält:
- V1.14.2 Stale-COMPLETE UI-Gate-Fix;
- eingefrorenes Rule-1.6-Zielprofil;
- 28 legacy_ids für identitätserhaltende Hobbyseiten-Migrationen;
- Dry-Run-Fix gegen doppelt gezählte Legacy-Archive;
- Idempotenz-Fix: bereits archivierte Target-Objekte werden im Folgelauf nicht erneut beschrieben.

Finale lokale Prüfung:
- PHP 33/33 PASS;
- Zielprofil valid;
- 1.723 physische Zielobjekte;
- Migration gegen V1.14.1: 1.293 CREATE + 430 UPDATE + 27 ARCHIVE;
- Sync COMPLETE / Readback 1.723;
- zweiter Dry-Run 1.723 UNCHANGED;
- zweiter Sync 1.723 UNCHANGED / 0 ARCHIVE / 0 Writes;
- Frontend PASS;
- Negativsuite PASS/fail-closed.

Artefakt:
`HD001_V1.14.3_RULE16_VISIBLE_FINAL_HARDPASS.zip`

SHA-256:
`deaee48b4f7310d94a5975b3dd471b0374d369745b1b7dd48c512ae514d7c7de`

Profil:
`profiles/hobby-depot-v1.json`

Profil SHA-256:
`6578a1aa4dccf554bb685a36e564c32af897c85bb1aac06d0401c5fc683622b6`

Evidence:
`SEO_KATEGORIEN/HD001_V1_14_3_RULE16_VISIBLE_FULL_LOCAL_HARDPASS_20261008.json`

## V1.14.3 LIVE-DRY-RUN – PASS

Live read-only result:
- 1.293 CREATE;
- 430 UPDATE;
- 27 ARCHIVE;
- 0 ADOPT;
- 1.723 target objects;
- 0 Provider;
- 0 Writes;
- exact local migration match.

The embedded frontend readback is still bound to the old V1.14.1 live revision and is therefore PRE-SYNC evidence only.

Evidence:
`SEO_KATEGORIEN/HD001_V1_14_3_LIVE_DRYRUN_PASS_20261009.json`

## ERSTER OFFENER BLOCKER

`HD001_V1_14_3_LIVE_SYNC_PENDING`

## EXAKT EINE NEXT ACTION

Synchronize the accepted V1.14.3 target exactly once, then download and verify the post-sync JSON.
No second run before post-sync verification.

## V1.14.4 – CURRENT RELEASE CANDIDATE (2026-10-09)

Auslöser:
- realer V1.14.3-Sync endet bei `core:gestalten:oberflaeche-deko [name]` nach 39 Readbacks und rollt vollständig zurück;
- Zielvertrag 2.6 verbietet Kategorie unter Kategorie;
- V1.14.3-Magazinmodell enthält 12 solche Kanten.

Änderungen:
- HTML-Entity-Normalisierung für Page- UND Term-Namen im Dry-Run/Readback;
- echte Abweichungen bleiben strikt;
- Readbackdiagnose mit expected/actual;
- generisches Kategorie-unter-Kategorie-Gate;
- Magazin-Gruppen als Page/View statt Taxonomie-Parent;
- neutraler Editorial-Fallback Hobbyfinder;
- vier beschlossene Magazin-Gruppen unverändert.

Lokale Abnahme:
- V1.14.3-Fehler lokal am selben Knoten nach denselben 39 Readbacks reproduziert;
- V1.14.4 Dry-Run PASS;
- V1.14.4 Sync 1.723/1.723 COMPLETE;
- zweiter Sync 1.723 UNCHANGED / 0 Writes;
- Header 102/102;
- Magazin 4/4;
- Negativsuite fail-closed inkl. echter Namensänderung mit ROLLBACK;
- PHP 33/33 vor und nach Fresh-Unpack.

Artefakt:
`HD001_V1.14.4_RULES_MAGAZIN_FULL_LOCAL_HARDPASS.zip`

SHA-256:
`9ec9b0d7b2776c59262aebbed9d3e9a88a533ce11084c4e66cd011a9126da06d`

Profil SHA-256:
`08c1da1bb43add667b73ea02bbaab6d3ad3c3228de88673254d8d5ebbdb8996c`

Evidence:
`../../../SEO_KATEGORIEN/HD001_V1_14_4_RULES_MAGAZIN_FULL_LOCAL_HARDPASS_20261009.json`

LIVE-STATUS:
V1.14.4 wurde in diesem Lauf NICHT ins echte WordPress geschrieben.

NEXT ACTION:
V1.14.4 installieren → Live-Dry-Run → exakt ein kontrollierter Sync → vollständiger Post-Sync-Readback.


## FREEZE NACH V1.14.8 – KEIN WEITERER TECHNISCHER BLINDFIX

Realer Live-Readback:
`hobby-depot-final-target-readback-20261009-114254-utc.json`

Technischer Endstand des aktuellen Laufs:
- plugin_version 1.14.8;
- Runner COMPLETE;
- 1.723/1.723 Zielobjekte gelesen;
- 1.723 UNCHANGED;
- 52 EDITORIAL-DEMOTION;
- 0 unbound Core pages;
- interner Frontend-Gate 279/279.

Dieser technische COMPLETE-Status ist **kein fachlicher Gesamt-PASS**.

Offen:
- unterste Kategorieebene ist real sichtbar nicht auf allen Hobbyseiten zuverlässig vorhanden;
- bestehender Content-Zielbaum deckt die universelle Nutzerreise nicht systematisch ab;
- Zielvertrag wurde deshalb auf 2.7 fortgeschrieben.

Verbot bis zur Fachabnahme:
- keine V1.14.9 nur wegen einzelner Anzeige-/Kategoriebeobachtungen;
- kein weiterer Struktur-Sync;
- keine neue Massenkategorie-Generierung;
- keine Änderung der Bestands-Leafs.

Nächster technischer Auftrag entsteht erst aus dem fachlich abgenommenen 10-Hobby-Pilot nach Zielvertrag 2.7.



## V1.14.9 – PILOT 2.7 DATAFORSEO BACKEND / LOCAL HARD PASS

Zweck:
- kein neuer Zielbaum;
- kein Kategorienwrite;
- ausschließlich read-only DataForSEO-Research für den festgelegten 10-Hobby-Pilot;
- DataForSEO nur über den bestehenden WordPress-Backend-Client `APKW_DataForSEO`.

Backend:
`Kategorien → Pilot 2.7`

Pilot:
Buchbinden / Balance Board / Glasmalerei / Lasergravieren / Fledermausbeobachtung / Hydrokultur / Riffaquaristik / Briefmarken sammeln / Geocaching / Imkerei.

Ablauf:
- kostenlose Vorprüfung;
- exakt 10 geplante Paid-Calls;
- 1 `keyword_ideas`-Call je Hobby;
- 5 Seeds je Hobby: Hobby / Anfänger / Ausrüstung / Kosten / Fragen;
- max. 100 Provider-Ideen je Hobby;
- bounded: 1 Paid-Call je AJAX-Schritt;
- Export enthält normalisierte Keywords + Fragekandidaten;
- 0 WordPress-/HivePress-Strukturwrites.

Sicherheitsfreeze:
`APKW_TARGET_TREE_MANUAL_ONLY = true`.
Damit löst das Research-Plugin-Update bei aktuellem COMPLETE-Stand keinen neuen Target-Tree-Code-Upgrade-Sync aus.

Artefakt:
`HD001_V1.14.9_PILOT27_DATAFORSEO_READONLY_LOCAL_HARDPASS.zip`

SHA-256:
`09a8d4b5f8c213ff98b5ea3023ca8c9a6d8560ffa1a2db96f437896ff11eed26`

Pilotprofil SHA-256:
`9c1927ec4b1c98514c51a3bb1fa332d56d714185cd13a007999971c4e11bccc2`

Lokale Abnahme:
- Fresh-Unpack 34/34 PHP-Lint;
- ZIP-Integrität PASS;
- 10 Hobbys / 10 Calls PASS;
- bounded 10-Schritt-Lauf PASS;
- Idempotenz nach COMPLETE PASS;
- Drift BLOCKED;
- Providerfehler ohne Indexfortschritt PASS;
- 9-Hobby-Profil BLOCKED;
- 0 Strukturwrite-Funktionen im Pilotmodul;
- Target-Revalidation bei Code-Update durch MANUAL_ONLY blockiert.

Beleg:
`HD001_PILOT27_DATAFORSEO_BACKEND_PLAN_20261009.md`

LIVE:
V1.14.9 noch nicht installiert; DataForSEO-Pilot noch nicht ausgeführt.

NEXT ACTION:
V1.14.9 installieren → Kategorien → Pilot 2.7 → kostenlose Vorprüfung → exakt 10 Calls bestätigen → COMPLETE → Pilot-Research-JSON herunterladen.
Kein Zielbaum-/Kategorien-Sync vor Auswertung dieses JSON.
