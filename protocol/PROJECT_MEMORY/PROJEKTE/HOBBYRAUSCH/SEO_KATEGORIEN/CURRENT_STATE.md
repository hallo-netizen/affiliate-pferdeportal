# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-08
STATUS: REGELN 2.6/1.6 BEREINIGT / WELT-ZWISCHENSTRUKTUR FACHLICH GEPRÜFT / 299 CURRENT-CORE-ROLLENRECHECK PENDING / KEIN WORDPRESS-WRITE / KEIN PLUGIN-FIX

## Ziel

Zentraler Hobbybestand
→ HOBBY_MASTER V2
→ Scope-/Identitäts-/Größen-/Rollenprüfung
→ 8 geschützte Hauptwelten
→ variable Seitenhierarchie + Content-Kategorien + Magazin + HivePress
→ DataForSEO-SEO-Anreicherung
→ globale Ownership-Prüfung
→ WordPress/HivePress Soll/Ist-Sync
→ Frontend-Readback.

## Geschützte Grundstruktur

Drei Säulen:
- CORE = Hauptportal;
- EDITORIAL = Magazin;
- DIRECTORY = HivePress/Anbieter.

Acht Hauptwelten:
Gestalten / Fertigen / Technik / Forschen / Pflanzen / Tiere / Bewegen / Sammeln.

### Harte Ebenenregel

Die acht Hauptwelten sind die oberste fachliche CORE-Ebene.

`Hobbywelten` ist nur Übersicht/Ansicht/Einstieg und darf NICHT als struktureller Parent über den acht Welten stehen.

Das vorhandene V1.12-Profil mit `core:hub → core:world:...` ist deshalb nur Baseline/Evidence und muss im späteren Zielbaum-Delta korrigiert werden.

## Portfolio- und Navigationslogik

Ziel:
- wirtschaftliche Anker durch große bekannte Hobbys;
- stabiles Mittelfeld;
- Nischen als Longtail/SEO-Differenzierung;
- ohne Navigationsexplosion.

Bekanntheit/Monetarisierungsstärke sind Präsentations-/Prioritätsmerkmale, keine zweite Taxonomie.

Der interne Master darf groß sein.
Die sichtbare Navigation bleibt klein.
Beliebte Hobbys, ungewöhnlich, zuhause, günstig usw. sind Views auf dieselben kanonischen Owner.

## Hobby-Master V2

Persistente Bewertungsbasis:
`/hobby rausch/HOBBY_DEPOT_HOBBY_MASTER_V2_20261007.json`

Current-Zeiger:
`../KONZEPT/VORARBEITEN_HOBBYFINDER/HOBBY_MASTER_V2_CURRENT.md`

Bestand:
- 908 Rohzeilen;
- 844 exakte Namen;
- 841 kanonische Identitäten;
- 329 bestehende V1.12-Monetarisierungs-/CORE-Regeln migriert;
- 286 DIRECT;
- 43 ASSISTED;
- 512 UNKNOWN und weiterhin erhalten.
- zusätzlich 19 Research-Queue-Kandidaten, noch NICHT Teil der 841 Identitäten;
- davon Fotografie durch Pilotbefund für provisorischen Master-Intake vorbereitet, aber noch kein Zielbaumknoten.

Die Rohliste ist Candidate Pool/Provenienz, keine Taxonomie.

## Maschinenlesbare V2-Bewertung

Regelvertrag:
`HOBBY_MASTER_V2_ASSESSMENT_RULES_20261007.json`

Kontrollierter erster Lauf:
`HOBBY_MASTER_V2_BATCH_001_RESULTS_20261007.json`

Research-Queue-Intake:
`HOBBY_MASTER_V2_RESEARCH_INTAKE_20261007.json`

Vorbereitetes Master-Intake-Delta:
`HOBBY_MASTER_V2_INTAKE_DELTA_001_20261007.json`

Batch 001 – autoritativ final:
- Quelle: `HOBBY_MASTER_V2_BATCH_001_FINAL_ASSESSMENT_20261007.json`;
- 16/16 fachlich geschlossen;
- 7 HOBBY_HUB;
- 3 ORIENTATION_UNIVERSE;
- 6 EDITORIAL_TOPIC;
- 0 unresolved;
- 0 Zielbaum-Writes.

## V2-Korrektur: jede unterste Kategorie einzeln prüfen

Verbindlich seit Regelversion 1.4:
- Gesamtzahl der Artikel eines Hobbys reicht NICHT;
- jede unterste Kategorie muss separat 5–12 echte, unterschiedliche Artikelintents tragen;
- 0–3 = keine eigene Leaf-Kategorie;
- 4 = Ausnahmeprüfung;
- 13–14 = oberhalb des Idealbereichs / prüfen;
- ab etwa 15 = Teilung prüfen.

Kleine valide Hobbys dürfen gemeinsam über Übersichten, gemeinsame Leafs oder Magazin-Cluster sichtbar werden.
Ihre kanonischen Hobby-Identitäten bleiben trotzdem getrennt.

Fachvorprüfung:
`HOBBY_MASTER_V2_BATCH_001_SUBJECT_PREFLIGHT_20261007.json`

DataForSEO-Auftrag:
`HOBBY_MASTER_V2_BATCH_001_DATAFORSEO_REQUEST_20261007.json`

Konzeptaudit:
`HOBBY_MASTER_V2_CONCEPT_AUDIT_20261007.md`

## Rollen- und Größenlogik

Publikationsrollen:
- ORIENTATION_UNIVERSE;
- HOBBY_HUB;
- EDITORIAL_TOPIC;
- ARTICLE_ONLY;
- FINDER_ONLY;
- OUT_OF_SCOPE.

Leaf:
- unter 4 zusammenlegen / keine eigene Leaf-Kategorie;
- 4 Grenzfall;
- 5–12 Idealbereich;
- 13–14 oberhalb des Idealbereichs / prüfen;
- ab etwa 15 Teilung prüfen.

Hobby-Hub:
- 3–6 Zielbereich;
- 7–9 oberhalb des typischen Bereichs / prüfen;
- ab etwa 10 Macro-/Split-Prüfung.

## DataForSEO-Vertrag

DataForSEO darf:
- Nachfrageband;
- Primärkeyword;
- Synonyme;
- Longtail-Tiefe;
- Keyword-/Intent-Überschneidung

belegen bzw. innerhalb definierter Kandidaten optimieren.

DataForSEO darf NICHT bestimmen:
- Hauptwelt;
- Parent;
- structural_role;
- neue Zwischenkategorie;
- CORE-Promotion.

## Monetarisierung

Monetarisierung beeinflusst CORE-Priorität, Sichtbarkeit und kommerzielle Tiefe.

Nicht monetarisierbare valide Hobbys werden NICHT gelöscht.
Sie bleiben EDITORIAL-/ARTICLE-/FINDER-Kandidaten.

## Dubletten und Ownership

Prüfung gemeinsam über CORE / EDITORIAL / DIRECTORY.

Treibholz + Treibholz sammeln = eine Identität.

Pro primärem Intent genau ein SEO-Owner.
Andere Säulen dürfen Relation/Filter/Verweis sein, keine konkurrierende Zielseite.

## Technischer V1.12.0–V1.12.6-Stand

Die komplette Batch-001-Fehlerkette wurde weitergeführt.

### Reale hochgeladene Readback-Datei nach V1.12.5

`hobby-master-v2-assessment-20261007-190209-utc.json`

SHA-256:
`086456f70d8896c51a97a27f7dcdc29906ad90534f9322aa6f1f5a7b519d69ae`

Interne Metadaten:
- plugin_version = 1.12.3;
- result version = 1.1;
- generated_at_utc = 2026-10-07T18:02:17+00:00;
- DataForSEO paid_calls = 39;
- Kosten ca. 0.9738 USD;
- Strukturwrites = 0;
- Summary = 0 Hub-Kandidaten / 2 ideale Leafs.

Damit ist bewiesen:
Der Download war KEIN neuer V1.12.5-Recalc-Readback, sondern bytegleich das alte gespeicherte V1.12.3-Ergebnis.

### Root Cause

V1.12.5 führte die kostenlose KISS-Neuberechnung nur beim Rendern der V2-Adminseite aus.

Der Download-Handler selbst exportierte lediglich `last_result()`.

Folge:
Ein alter Browser-Tab bzw. ein direkter Download nach Plugin-Update konnte weiterhin den unveränderten V1.12.3-Stand ausliefern.

### V1.12.6 – KISS-Fix

Der Download ist jetzt selbst die letzte fail-closed Grenze:

1. gespeichertes Ergebnis laden;
2. fehlt `capacity_recalculation.version = 1.0`, kostenlose KISS-Neuberechnung ausführen;
3. neues Ergebnis speichern;
4. erst danach exportieren;
5. bei Fehler: Download BLOCKED statt altes JSON.

Kein DataForSEO-Aufruf.
Keine neuen Kosten.
Keine Strukturwrites.

Artefakt:
`HD001_V1.12.6_STALE_EXPORT_FAILCLOSED_HARDPASS.zip`

SHA-256:
`788b49529216555cba8cd74aae2a3a469f5f386e7ea2dc3d0449555910d55dca`

Prüfbericht:
`HD001_V1.12.6_FINAL_LOCAL_POSNEG_REPORT.txt`

SHA-256:
`c9442f08b722e93a24fee697cec09d77e67f1ad9cd23cda9067a5185e90b042e`

### Harte lokale Prüfung mit exakt der realen stale Datei

Direkter V1.12.6-Download-Replay:
- plugin_version 1.12.6;
- 16 Kandidaten;
- 34 ideale Leafs;
- 1 HOBBY_HUB_CANDIDATE;
- 1 EDITORIAL_TOPIC_CANDIDATE;
- 5 AGGREGATION_REVIEW;
- 3 MACRO_REVIEW;
- 6 EVIDENCE_REQUIRED;
- 0 Zielbaum-Writes;
- 0 Provider-Calls hinzugefügt;
- 0 Provider-Kosten hinzugefügt;
- 0 WordPress-Strukturwrites.

Zusätzlich:
- PHP-Lint 31/31 PASS;
- ZIP-Integrität PASS;
- idempotenter zweiter Download PASS;
- kein gespeichertes Ergebnis → BLOCKED PASS;
- Delta gegen V1.12.5 nur Header/README/Admin-Export-Gate/Kommentar.

Beleg:
`HOBBY_MASTER_V2_BATCH_001_V126_STALE_EXPORT_READBACK_20261007.md`

## BATCH 001 – FACHLICHER ABSCHLUSS

Autoritative einzige Abschlussdatei:
`HOBBY_MASTER_V2_BATCH_001_FINAL_ASSESSMENT_20261007.json`

Ergebnis:
- 7 HOBBY_HUB;
- 3 ORIENTATION_UNIVERSE;
- 6 EDITORIAL_TOPIC;
- 0 ARTICLE_ONLY;
- 0 FINDER_ONLY;
- 0 OUT_OF_SCOPE;
- 0 ungeklärte Rollen;
- 0 Zielbaum-Writes.

Die spätere Datei `HOBBY_MASTER_V2_BATCH_001_FINAL_FACHBEWERTUNG_20261008.json` ist nur historische Arbeitskopie und verweist jetzt auf diese autoritative Abschlussdatei.

## BATCH 002 – VORBEREITET

Deterministische Auswahlregel:
erste 16 noch nicht final bewerteten kanonischen Identitäten in stabiler Master-Reihenfolge.

Auswahl:
Amateurfunk, CB-Funk, Software Defined Radio, Satellitenfunk, Satellitenempfang, Wettersonden-Tracking, Funkpeilung, Morsefunk, Elektronikbasteln, Mikrocontroller-Projekte, Arduino, Raspberry-Pi-Projekte, Robotik, Heimrobotik, Roboterbau, BattleBots-Modellbau.

Vorbereitet:
- 16 Kandidaten;
- 51 vorgeschlagene Leafs;
- 304 fachlich unterschiedliche Artikelintents;
- 304 deduplizierte DataForSEO-Keywords;
- exakt 1 geplanter `keyword_overview`-Aufruf;
- automatische Depth-Recherche = AUS;
- Strukturwrites = 0.

Maschinenlesbarer Plan:
`HOBBY_MASTER_V2_BATCH_002_PREPARED_20261008.json`

Plugin-V1.12.6-Preflight lokal:
PASS / 16 / 51 / 304 / 304 / 1.


## BATCH 003 – REALER ABSCHLUSS

Realer Lauf:
- Plugin 1.12.6;
- Batch 003;
- 16 Kandidaten;
- 59 ideale Leafs;
- 325 fachlich definierte Artikelintents;
- 1 DataForSEO-Aufruf;
- 102 zurückgegebene Provider-Zeilen;
- Kosten 0.02424 USD;
- 0 Strukturwrites.

Fachlich final:
- 13 HOBBY_HUB;
- 3 ORIENTATION_UNIVERSE;
- 0 unresolved.

Damit wurden insgesamt 48 Master-Identitäten detailliert als Kalibrierung geprüft.

## PRAKTISCHE FINALISIERUNG – V1.13.1

Die 16er-Batchlogik wird nicht fortgesetzt.

Der 841er Master bleibt vollständiges Inventar.
Der finale CORE ist selektiv:
- 340 CORE-Identitäten;
- 501 Finder/Editorial-Identitäten.

### Harte Strukturkorrektur

Der erste praktische Profilentwurf war noch falsch, weil die acht Welten weiterhin unter `Hobbywelten` hingen.

V1.13.1 korrigiert das endgültig:
- die 8 Hauptwelten sind physisch CORE-Ebene 1 / Root;
- `Hobbywelten` ist nur View/Übersicht;
- 8 Relation-Knoten verlinken von Hobbywelten auf die 8 Welten;
- `Hobbywelten` ist kein Parent.

Finales Zielprofil:
`/hobby rausch/HD001_V1.13.1_PRACTICAL_TARGET_PROFILE_20261008.json`

Profil SHA-256:
`f5c6d9e5be7ee6184c50ded9db40549f4b1e2d2a8c29672f4eb7aa172ea8e014`

Final aufgelöst:
- 103 Basis-Logikknoten;
- 440 aufgelöste Logikknoten;
- 431 physische Zielobjekte;
- 404 Pages;
- 4 WordPress-Kategorien;
- 15 journal_cat;
- 8 hp_listing_category;
- 9 Relations;
- 841 Master-Identitäten vollständig aufgelöst;
- 0 Strukturkonflikte im lokalen Endtest.

### HD-001 V1.13.1

Artefakt:
`HD001_V1.13.1_PRACTICAL_FINAL_TARGET_ONE_SYNC_HARDPASS.zip`

SHA-256:
`94dca6cfc6c792cf2b866fc76fef1bff12551f9b375b38a1a511a91876b1a7b5`

Prüfbericht:
`HD001_V1.13.1_FINAL_LOCAL_POSNEG_REPORT.txt`

Prüfbericht SHA-256:
`f2649cbd1f132b1e48dfcf95cd05db805e024bf3d29c8b0d4d3aebda0594cd2d`

Sicherheitsmodus:
- MANUAL ONLY;
- kein Auto-Sync bei Installation/Update/Admin-Aufruf;
- finaler Dry-Run = 0 DataForSEO-Aufrufe;
- finaler Dry-Run = 0 WordPress-Strukturwrites;
- Apply nur nach exakt demselben gespeicherten Live-Dry-Run-Fingerprint;
- veränderter Live-Stand blockiert Apply;
- automatisches Retirement nur für echte `_apkw_target_node_id`-Bindings;
- alte Artikel-/Kategoriestrukturen ohne Target-Binding bleiben erhalten;
- Foreign-Slug-Kollision blockiert fail-closed;
- Sync läuft bounded per AJAX mit Cron-Fallback.

Lokale Abnahme:
- Regression 270/270 PASS;
- Final-Target-Suite 24/24 PASS;
- V1.12→V1.13.1-Migration 11/11 PASS;
- Release-PHP-Lint 33/33 PASS.

Simulierter voll ausgerollter V1.12-Bestand → V1.13.1:
- 12 CREATE;
- 419 UPDATE;
- 1 ARCHIVE;
- nach genau einem Sync: 431 UNCHANGED;
- keine Term-CREATE/UPDATE/DELETE-Strukturwrites.

Autoritativer Endaudit:
`HOBBY_MASTER_V2_PRACTICAL_FINAL_TARGET_AUDIT_20261008.json`

## REALER V1.13.1 LIVE-DRYRUN

Quelle:
`hobby-depot-final-target-readback-20261008-082217-utc.json`

SHA-256:
`3e1c00ea5c2d174c2ce6afcacadcf3ea9c6153b63467f1b420fa7ebc175c7a96`

Dry-Run selbst:
- plugin_version 1.13.1;
- PASS / valid=true;
- 841 Inventar;
- 340 CORE;
- 501 Finder/Editorial;
- 440 Logikknoten;
- 431 physische Zielobjekte;
- 8 Welten korrekt CORE-Level-1;
- CREATE 12;
- UPDATE 419;
- ARCHIVE 1 = alte Brettspiele;
- 0 Provider-Calls;
- 0 Kosten;
- 0 Strukturwrites.

Die 12 CREATEs sind exakt die kalibrierten Promotionen.

### ERSTER LIVE-EXPORT – HISTORISCHER RESTZUSTAND (GESCHLOSSEN)

Der JSON-Readback zeigt gleichzeitig noch einen alten V1.12-Zielbaumlauf:

- sync_state = `ROLLBACK_PENDING`;
- revision = `HD-TARGET-3P-V1-20261007+313e8ac433c0b154`;
- 620 Rollback-Aktionen stehen noch aus;
- alter Fehler: `directory:events-reisen [name]`;
- runner = RUNNING / EXISTING_TARGET_TREE_RESUME;
- Frontend-Readback = NO_ACTIVE_FINAL_SNAPSHOT.

Damit ist der V1.13.1-ZielPLAN zwar korrekt, aber der finale Sync darf noch NICHT gestartet werden.

V1.13.1 ist dafür bereits abgesichert:
- auf der Seite `Finaler Zielbaum` wird ein bestehender ROLLBACK_PENDING-Zustand automatisch weitergetaktet;
- währenddessen wird der Sync-Button nicht angeboten;
- nach beendetem Rollback muss wegen verändertem Live-Fingerprint zwingend ein NEUER Dry-Run erfolgen;
- selbst ein veralteter gespeicherter Plan würde beim Apply durch den Fingerprint-Recheck blockiert.

Evidence:
`HD001_V1.13.1_REAL_LIVE_DRYRUN_20261008.json`

## REALER LIVE-DRY-RUN – PASS

Beleg:
`HD001_V1_13_1_REAL_LIVE_DRYRUN_20261008.md`

Realer Zielplan:
- Plugin 1.13.1;
- 841 / 340 CORE / 501 Finder-Editorial;
- 440 Logikknoten;
- 431 physische Zielobjekte;
- acht Welten Root;
- 8 Hobbywelten-Relations;
- CREATE 12;
- UPDATE 419;
- ARCHIVE 1;
- errors = [];
- 0 Provider-Aufrufe;
- 0 Kosten;
- 0 Strukturwrites.

CREATE-Liste und ARCHIVE exakt wie lokal erwartet.
ARCHIVE = alte Brettspiele.

Im Export war gleichzeitig noch der alte V1.12-Sync in `ROLLBACK_PENDING`.
V1.13.1 resumiert diesen Rollback automatisch.
Der neue finale Sync wurde noch nicht gestartet.

Der spätere Screenshot zeigt den automatischen Sync-Hinweis nicht mehr; ein frischer Export muss den terminalen Altzustand aber noch bestätigen.

## POST-ROLLBACK-FRISCHCHECK – CURRENT

Frischer Live-Export:
`hobby-depot-final-target-readback-20261008-083850-utc.json`

Bestätigt:
- Dry-Run PASS / valid=true;
- 841 / 340 CORE / 501 Finder-Editorial;
- 440 Logikknoten;
- 431 physische Zielobjekte;
- 356 CREATE;
- 75 ADOPT;
- 0 UPDATE;
- 0 ARCHIVE;
- 0 Provider-Aufrufe;
- 0 Kosten;
- 0 WordPress-Strukturwrites;
- alter V1.12-Runner terminal `ROLLED_BACK`;
- `rollback_actions = []`;
- noch kein aktiver finaler Snapshot;
- noch kein neuer Final-Sync.

Vollständiger Strukturabgleich gegen Zielvertrag 2.5 / Regeln 1.5:
PASS für Ebenen, acht Root-Welten, Hobbywelten-View, Parent-Konsistenz, Säulentrennung, Tiefe, 4 Buchbinden-Content-Kategorien, 8 Directory-Kategorien sowie eindeutige Node-IDs/Slugs.

Neuer Konzeptaudit:
`HD001_V1_13_1_POST_ROLLBACK_CONCEPT_AUDIT_20261008.md`

## MATERIALKUNST-KORREKTUR – UMGESETZT

Echtes Originalartefakt gebunden und Hash gegen Manifest bestätigt:
`HD001_V1.13.1_PRACTICAL_FINAL_TARGET_ONE_SYNC_HARDPASS.zip`
SHA-256:
`94dca6cfc6c792cf2b866fc76fef1bff12551f9b375b38a1a511a91876b1a7b5`

Im echten Plugin wurde ausschließlich
`core:gestalten:materialkunst`
aus
`profiles/hobby-depot-v1.json`
entfernt.

Korrigiertes Artefakt:
`HD001_V1.13.1_PRACTICAL_FINAL_TARGET_ONE_SYNC_HARDPASS_MATERIALKUNST_FIX.zip`
SHA-256:
`ea5aa8316b2537695f2f805d0b9cc4b0d9f973fb609c231ab7c3067de419c263`

Korrigiertes Profil:
`HD001_V1.13.1_PRACTICAL_TARGET_PROFILE_20261008_MATERIALKUNST_FIX.json`
SHA-256:
`2fe534e0d25af038c49c3eaa2b9e9c38c71daac051a217ef65a92f8b077a9b95`

Patch-Abnahme:
- exakt 1 Paketdatei geändert;
- exakt 1 Zielknoten entfernt;
- 0 Zielknoten hinzugefügt;
- 0 Hobby-Umhängungen;
- 33/33 PHP-Lint PASS nach frischem Unzip;
- ZIP-Integrität PASS;
- 0 doppelte Basis-Node-IDs;
- 0 fehlende Basis-Parents;
- Materialkunst 0-mal im korrigierten Profil;
- Plan-Graph-Simulation PASS.

Erwarteter Zielstand ohne weiteren Live-Drift:
- 102 Basis-Logikknoten;
- 439 aufgelöste Logikknoten;
- 430 physische Zielobjekte;
- 403 Pages;
- 4 category;
- 15 journal_cat;
- 8 hp_listing_category;
- 355 CREATE + 75 ADOPT.

Beleg:
`HD001_V1_13_1_MATERIALKUNST_FIX_LOCAL_BUILD_20261008.json`

## KORRIGIERTER LIVE-DRYRUN – PASS

Frischer Export:
`hobby-depot-final-target-readback-20261008-100800-utc.json`

Bestätigt:
- plugin_version 1.13.1;
- status PASS / valid=true;
- 841 Identitäten;
- 340 CORE / 501 Finder-Editorial;
- 439 Logikknoten;
- 430 physische Zielobjekte;
- 403 Pages;
- 4 category;
- 15 journal_cat;
- 8 hp_listing_category;
- 355 CREATE;
- 75 ADOPT;
- 0 UPDATE;
- 0 ARCHIVE;
- errors = [];
- 0 Provider-Aufrufe;
- 0 Kosten;
- 0 WordPress-Strukturwrites;
- `Materialkunst` nicht mehr im Zielplan;
- 0 fehlende Parents;
- 0 Zyklen;
- 0 doppelte Node-IDs/Slugs;
- 0 Kategorie-unter-Kategorie;
- alter V1.12-Sync terminal `ROLLED_BACK`;
- `rollback_actions = []`;
- kein aktiver finaler Snapshot, weil der Final-Sync noch nicht ausgeführt wurde.

## FEHLGESCHLAGENER FINAL-SYNC – URSACHE GEKLÄRT

Readback:
`hobby-depot-final-target-readback-20261008-101334-utc.json`

Befund:
- Sync-Status `ROLLBACK_PENDING`;
- Fehler: `core:fertigen:buch-papier [slug]`;
- 430 Zielknoten geschrieben;
- 415 als created;
- nur 15 als adopted;
- Dry-Run hatte 355 CREATE + 75 ADOPT geplant;
- damit wurden 60 vorhandene Unterseiten beim Sync nicht wiedergefunden und fälschlich neu angelegt;
- 231 Rollback-Aktionen sind offen.

Ursache:
Der Sync suchte Seiten per `get_page_by_path($slug)`.
Bei hierarchischen Unterseiten benötigt WordPress dort den vollständigen Pfad.
Der Dry-Run suchte dagegen global nach dem Blatt-Slug und fand die vorhandenen Seiten korrekt.

Fix:
V1.13.2 verwendet auch im Sync die begrenzte globale Slug-Suche und bleibt bei Mehrdeutigkeit fail-closed.

Artefakt:
`HD001_V1.13.2_ADOPT_CHILD_SLUG_FIX_HARDPASS.zip`
SHA-256:
`d9cb80d8e5635fd94ac390dc0be75757d1a7a964b0ce0cb1cf893934eed35cc7`

Prüfung:
- 33/33 PHP-Lint PASS;
- Unterseiten-Slug-Adoption PASS;
- Mehrdeutigkeit BLOCKED/PASS;
- Missing-Slug NULL/PASS;
- Zielprofil unverändert;
- Materialkunst bleibt entfernt.

Beleg:
`HD001_V1_13_2_ADOPT_CHILD_SLUG_FIX_20261008.json`

## V1.13.2 NACH ROLLBACK – LIVE PASS, ABER LOKALE PARITÄTSPRÜFUNG FINDET ZWEITEN SYNC-FEHLER

Frischer V1.13.2-Readback:
`hobby-depot-final-target-readback-20261008-105008-utc.json`

Live bestätigt:
- Dry-Run PASS;
- 355 CREATE + 75 ADOPT;
- 430 Zielobjekte;
- alter V1.13.1-Fehlsync vollständig `ROLLED_BACK`;
- `rollback_actions = []`.

Lokaler Vollvergleich Dry-Run vs Sync:
V1.13.2 hatte noch eine zweite Abweichung.
Der Dry-Run sucht vorhandene Legacy-Objekte über
`_apkw_concept_id = current node_id`
plus Legacy-IDs.
Der Sync suchte dort nur Legacy-IDs und fiel sonst auf Slug zurück.

Folge:
11 umbenannte ADOPT-Altseiten hätten trotz PASS-Dry-Run beim Sync kollidieren können.

## V1.13.3 – FULL-SYNC-PARITY LOKAL PASS

Fix:
Sync verwendet jetzt exakt dieselbe concept_id-Suchlogik wie der Dry-Run:
current node_id + legacy_ids → erst danach Slug-Fallback.

Lokaler Volltest mit dem echten 430-Knoten-Plan:
- erster Lauf: 355 CREATE + 75 ADOPT;
- 430/430 Readback PASS;
- Status COMPLETE;
- zweiter identischer Lauf: 430 UNCHANGED;
- Rollback: ROLLED_BACK und semantisch vollständig wiederhergestellt;
- 11 umbenannte Legacy-ADOPTs ausdrücklich geprüft;
- Mehrdeutigkeit bleibt fail-closed;
- PHP-Lint 33/33 PASS;
- ZIP-Integrität PASS;
- Zielprofil unverändert.

Artefakt:
`HD001_V1.13.3_FULL_SYNC_PARITY_HARDPASS.zip`
SHA-256:
`f255b06fb38c7b903de2c7741dea4e02fb9620ad3a6651fbf5963f402c33820b`

Beleg:
`HD001_V1_13_3_FULL_SYNC_PARITY_LOCAL_20261008.json`

## V1.13.3 LIVE-FEHLER – TERMINAL ROLLED_BACK

Readback:
`hobby-depot-final-target-readback-20261008-110911-utc.json`

Bestätigt:
- Plugin 1.13.3;
- Sync terminal `ROLLED_BACK`;
- 355 created + 75 adopted;
- Fehler nach 63 Readbacks:
  `directory:events-reisen [name]`;
- kein aktiver finaler Snapshot.

## V1.13.4 – KOMPLETTER LOKALER WORKFLOW POSITIV + NEGATIV HARD PASS

Der reale V1.13.3-Fehler wurde mit dem exakten V1.13.3-ZIP lokal 1:1 reproduziert:
355 CREATE + 75 ADOPT → Readback 63 → `Events & Reisen [name]` → ROLLED_BACK.

Root Cause:
Taxonomie-Namen wurden im Dry-Run/Sync roh verglichen.
WordPress/HivePress kann sichtbare Termnamen entity-kodiert liefern, z. B.
`Events &amp; Reisen`.
Frontend dekodierte bereits korrekt; Dry-Run/Sync noch nicht.

V1.13.4:
nur Term-Namenslesen vor Vergleich dekodiert.
Zielprofil unverändert.
Materialkunst bleibt entfernt.

Fresh-ZIP-Volltest:
- initialer Dry-Run 355 CREATE + 75 ADOPT / 0 Provider / 0 Writes;
- unmittelbar frischer Pre-Sync-Fingerprint identisch;
- erster Sync 355 created + 75 adopted;
- 430/430 Struktur-Readback PASS;
- Status COMPLETE;
- 430 aktives Mapping;
- 403/403 Page-Frontend-Readbacks PASS;
- Hobbywelten/Core-Hub PASS;
- Magazin-Hub + Menügruppen PASS;
- Anbieter/HivePress-Hub PASS;
- Front-Hub-Links PASS;
- Footer PASS;
- FinalTargetAdmin Frontend-Readback PASS;
- nächster Dry-Run 430 UNCHANGED;
- zweiter Sync 430 UNCHANGED + 430/430 Readback PASS.

Negativ:
- absichtlicher Readbackfehler → BLOCKED + exakter Rollback;
- Page-Insert-Fehler → exakter Rollback;
- Term-Insert-Fehler → exakter Rollback;
- mehrdeutige Binding → Dry-Run BLOCKED + Sync fail-closed;
- fremder HivePress-Slug → BLOCKED;
- kaputtes Profil → vor Write BLOCKED;
- fehlende hp_listing_category → Dry-Run + Sync vor Write BLOCKED.

Paket:
`HD001_V1.13.4_FULL_LOCAL_POSNEG_HARDPASS.zip`
SHA-256:
`4ca1fb163f2ca5082d5b264a3d1b1862ee4b94039eeadd0c9b9f98e7270eb251`

Profil SHA-256 unverändert:
`2fe534e0d25af038c49c3eaa2b9e9c38c71daac051a217ef65a92f8b077a9b95`

Fresh PHP-Lint:
33/33 PASS.

Beleg:
`HD001_V1_13_4_FULL_LOCAL_POSNEG_HARDPASS_20261008.json`

## V1.13.4 LIVE-DRYRUN – PASS

Readback:
`hobby-depot-final-target-readback-20261008-113205-utc.json`

Bestätigt:
- Plugin 1.13.4;
- status PASS / valid=true;
- 841 Identitäten;
- 340 CORE / 501 Finder-Editorial;
- 439 Logikknoten;
- 430 physische Zielobjekte;
- 355 CREATE;
- 75 ADOPT;
- 0 UPDATE / UNCHANGED / ARCHIVE;
- errors = [];
- 0 Provider-Aufrufe;
- 0 Kosten;
- 0 WordPress-Strukturwrites;
- V1.13.3-Fehlsync terminal ROLLED_BACK;
- rollback_actions = [];
- noch kein aktiver Final-Snapshot.

Dieser Live-Dry-Run entspricht exakt dem zuvor vollständig lokal positiv/negativ getesteten V1.13.4-Workflow.

## FRONTEND-/KONZEPTAUDIT NACH SICHTPRÜFUNG – FAIL

Autoritativer Audit:
`HD001_V1_13_4_FULL_RULE_CONCEPT_AUDIT_20261008.md`

Harte Befunde:
- der Zielbaum selbst besitzt die dritte Seitenebene für alle 340 CORE-Hobbys;
- die aktive Header-/Theme-Navigation zeigt aber Legacy-Seiten zusätzlich zum Zielbaum;
- dadurch ist die sichtbare Navigation zu breit und Ebenen werden vermischt;
- Betonmöbel und Dorodango sind im aktuellen Zielprofil Editorial, erscheinen aber sichtbar unter Fertigen;
- Treibholz sammeln + Alias Treibholz sind im Zielprofil eine Editorial-Identität; sichtbare CORE-Dubletten unter Sammeln sind Legacy-Leakage;
- Magazin besitzt im Zielprofil 15 journal_cat-Terme und die feste Gruppenstruktur, diese wird aber nicht in die aktive Header-Navigation projiziert;
- V1.13.4 besitzt 52 fachliche Zwischenbereiche; die Konzept-Arbeitsstruktur nennt 63. 11 Trennungen wurden zusammengezogen/entfallen;
- klar überbreite aktuelle Bereiche: RC & Drohnen 16, Leder & Textil 13, Genuss 12, Elektronik & Funk 11, Holz & Naturmaterial 10, Metall & Schmuck 9;
- nur Buchbinden besitzt aktuell die WordPress-Content-Kategorieebene. Das ist nach Zielvertrag 2.5 erlaubt und daher KEIN aktueller Regelverstoß; eine verpflichtende Kategorieebene für weitere Hobbys wäre eine bewusste Regeländerung.

## V1.14.0 – STRUKTUR / NAVIGATION / MAGAZIN LOKAL HARD PASS

Beleg:
`HD001_V1_14_0_STRUCTURE_NAV_MAGAZIN_FULL_LOCAL_HARDPASS_20261008.json`

Korrigiert:
- sichtbare Header-Navigation ausschließlich aus aktivem Target-Snapshot;
- ungebundene Legacy-Seiten leaken nicht mehr in die kanonische Navigation;
- Betonmöbel / Dorodango bleiben Editorial und erscheinen nicht unter Fertigen;
- Treibholz sammeln + Treibholz bleiben genau eine bestätigte Editorial-Identität und erscheinen nicht in CORE;
- feste Magazin-Navigation vollständig projiziert;
- zusammengezogene Zwischenbereiche fachlich getrennt;
- keine leeren Symmetrie-Kategorien erzeugt;
- Robotik- und Bonsai-Hobbyseiten bleiben physisch erhalten;
- keine unbelegten Alias-Merges / keine unbelegte BattleBots-Umbenennung.

Aktueller lokaler Zielstand:
- 841 kanonische Identitäten;
- 340 CORE / 501 Finder-Editorial;
- 59 aktive Zwischenbereiche;
- 446 Logikknoten;
- 437 physische Zielobjekte;
- 410 Page-Frontend-Readbacks;
- 96 Header-Navigationseinträge.

Zwischenbereiche je Welt:
- Gestalten 6;
- Fertigen 9;
- Technik 9;
- Forschen 5;
- Pflanzen 8;
- Tiere 6;
- Bewegen 8;
- Sammeln 8.

Nicht angelegte Konzeptäste, weil derzeit unbelegt und leere Ebenen verboten sind:
- Oberfläche & Deko;
- Citizen Science;
- Essbare Pflanzen;
- Gehegegestaltung.

Fresh-ZIP Full Positive:
- Dry-Run 362 CREATE + 75 ADOPT;
- Sync 437/437 Readback PASS / COMPLETE;
- Header-Navigation PASS;
- Magazin-Navigation PASS;
- 410/410 Seiten-Frontend PASS;
- zweiter Dry-Run 437 UNCHANGED;
- zweiter Sync 437 UNCHANGED.

Migration aus vollständig ausgerolltem V1.13.4:
- 12 CREATE;
- 425 UPDATE;
- 5 ARCHIVE;
- archiviert werden nur die fünf ersetzten kombinierten Strukturknoten;
- keine Hobbyseite wird dabei archiviert;
- danach 437 UNCHANGED.

Negativ:
Readback-/Page-/Term-Fehlerrollback, Ambiguity, Foreign-Slug, kaputtes Profil und fehlende HivePress-Taxonomie = PASS/fail-closed.

Artefakt:
`HD001_V1.14.0_STRUCTURE_NAV_MAGAZIN_FULL_POSNEG_HARDPASS.zip`
SHA-256:
`87246ecd24b1facc5c3b80c0e3593b2a0bd9391143ef6f190d6786ecfa62cda3`

## 19 ERWEITERUNGS-ANKER – FINAL BEWERTET

Beleg:
`HOBBY_MASTER_V2_EXPANSION_ANCHORS_19_FINAL_ASSESSMENT_20261008.json`

Ergebnis nach Regeln 1.5:
- 19/19 IN_SCOPE;
- 0 exakte/current-Alias-Kollisionen;
- 12 HOBBY_HUB;
- 7 ORIENTATION_UNIVERSE;
- 19 strukturell CORE-fähig;
- Monetarisierung aller 19 bleibt `UNKNOWN_PENDING_PROVIDER_MATCH`; daraus wurde KEINE Promotion abgeleitet;
- Content-Capacity der 12 HOBBY_HUBs fachlich als 3–6 tragfähige Cluster mit je 5–12 unterschiedlichen Intents belegt;
- diese Capacity-Cluster erzeugen jetzt ausdrücklich KEINE WordPress-Content-Kategorien;
- die separate Entscheidung zur untersten WordPress-Kategorieebene bleibt später offen;
- kein Live-Sync.

Finale Rollen:
- ORIENTATION_UNIVERSE: Fotografie, Holzwerken, Radfahren, Camping, Klettern, Gärtnern, Angeln;
- HOBBY_HUB: Malen, Zeichnen, Nähen, Stricken, Häkeln, Heimwerken, Wandern, Schwimmen, Bouldern, Gemüseanbau, Briefmarken sammeln, Plane Spotting.

Besondere Routingentscheidungen:
- Angeln: Bewegen → Outdoor; primäre Praxis ist die wiederholbare Outdoor-Freizeitaktivität, nicht Tierhaltung.
- Plane Spotting: Forschen; Beobachten/Tracking/Bestimmen/Dokumentieren, mit Ownership-Grenze zu generischer Fotografie.
- Gemüseanbau belegt erstmals den bisher leer gelassenen Konzeptast `Essbare Pflanzen`; Aktivierung wird erst im Target-Delta entschieden.
- Heimwerken und Gärtnern erhalten in dieser Bewertungsstufe KEINEN künstlich erfundenen Zwischenbereich.

## V1.14.1 – EXPANSION19 MASTER-/TARGET-DELTA LOKAL HARD PASS

Belege:
- `HD001_V1_14_1_EXPANSION19_TARGET_DELTA_20261008.json`
- `HD001_V1_14_1_EXPANSION19_FULL_LOCAL_HARDPASS_20261008.json`

Materialisiert:
- 860 kanonische Identitäten;
- 359 CORE;
- 501 Finder/Editorial;
- 60 aktive Zwischenbereiche;
- 466 aktive Logikknoten;
- 457 physische Zielobjekte;
- 430 Pages;
- 4 category;
- 15 journal_cat;
- 8 hp_listing_category;
- 9 Relations;
- 97 Header-Navigationseinträge.

Konzeptregeln eingehalten:
- keine neunte Welt;
- keine Blind-Promotion aus Monetarisierung;
- alle 19 neuen CORE-Identitäten bleiben monetarisierungsseitig UNKNOWN bis zu echtem Provider-Match und zugleich redaktionell erhalten;
- keine globale künstliche Content-Kategorieebene;
- `Essbare Pflanzen` wird erst jetzt aktiviert, weil `Gemüseanbau` den Ast real belegt;
- `Heimwerken` und `Gärtnern` bleiben direkte Welt-Kinder; kein künstlicher Ein-Kind-Zwischenbereich;
- direkte Hobbyseiten werden nicht als Zwischenbereiche in die Header-Navigation projiziert.

Lokaler POSITIV:
- Fresh Dry-Run: 457 CREATE / 0 Provider / 0 Writes;
- Fresh Sync: 457/457 Readback COMPLETE;
- zweiter identischer Sync: 457 UNCHANGED / 457 Readback COMPLETE;
- Migration V1.14.0 → V1.14.1: 20 CREATE + 437 UPDATE + 0 ARCHIVE / 457 Readback COMPLETE;
- danach 457 UNCHANGED;
- 430/430 Page-Frontend PASS;
- Header 97/97 PASS;
- Hobbywelten/Magazin/Anbieter, Frontlinks, Footer und Final-Frontend-Readback PASS.

Lokaler NEGATIV:
- Readback-/Page-/Term-Fehler → ROLLED_BACK / semantisch exakte Wiederherstellung;
- Ambiguity / Foreign-Slug / Missing-Taxonomy / Duplicate-Slug / falsche Monetarisierungsbehauptung / fehlende Editorial-Sicherung = BLOCKED/fail-closed;
- unbewerteter Zusatzkandidat bleibt Editorial und wird nicht blind CORE;
- V1.14.0-Regressionsprofil bleibt 841 / 340 / 437 PASS.

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
`HD001_V1_14_1_LIVE_DRYRUN_PASS_20261008.json`

Live-Plan:
- PASS / valid=true;
- 860 Identitäten / 359 CORE / 501 Finder-Editorial;
- 457 physische Zielobjekte;
- 32 CREATE + 425 UPDATE + 5 ARCHIVE;
- die 5 ARCHIVE sind ausschließlich die bekannten alten Sammelknoten: Elektronik & Funk, Insekten & Wirbellose, Leder & Textil, Metall & Schmuck, Schrift & Papier;
- 0 Hobby-Archive;
- 0 Provider-Aufrufe;
- 0 WordPress-Writes im Dry-Run.

Die Live-Seite steht vor dem Sync noch auf dem alten V1.13.4-Zielstand. Deshalb ist der Frontend-Readback vor dem Sync erwartbar noch nicht kanonisch.

## LIVE-DRY-RUN – PASS / UI-GATE-BEFUND

Der hochgeladene Live-Readback bestätigt:
- Plugin 1.14.1;
- Dry-Run PASS / valid=true;
- 860 Identitäten / 359 CORE / 501 Finder-Editorial;
- 457 physische Ziele;
- 32 CREATE + 425 UPDATE + 5 ARCHIVE;
- 0 Provider-Aufrufe;
- 0 WordPress-Writes;
- die 5 Archive sind nur die bekannten ersetzten Kombi-Zwischenknoten.

Screenshot + Codeprüfung zeigen einen realen UI-Fehler in V1.14.1:
Die Finaler-Zielbaum-Seite setzt `$complete` allein aus dem alten gespeicherten Sync-State `status=COMPLETE`.
Der alte COMPLETE-State gehört aber zur alten Revision V1.13.1/V1.13.4.
Dadurch wird der Apply-Button für den neuen V1.14.1-Dry-Run fälschlich ausgeblendet.

V1.14.2 korrigiert ausschließlich dieses Gate:
- COMPLETE zählt in der Finalansicht nur, wenn `state.revision === plan.profile_revision`;
- ein alter COMPLETE-State wird als veraltet erkannt;
- bei gültigem neuem Dry-Run erscheint der Apply-Button wieder;
- Target-Profil und Hobby-Master sind byteidentisch zu V1.14.1.

Lokale Prüfung V1.14.2:
- PHP 33/33 PASS;
- ZIP-Integrität PASS;
- altes COMPLETE + neuer Plan => Apply sichtbar PASS;
- gleiches COMPLETE + gleicher Plan => Apply verborgen PASS;
- laufender Sync => Apply verborgen PASS;
- Profil-SHA unverändert: cd40cee8f1bceffae7c41b8bf2124965d49046caa2e27242af2122168a8412d0;
- Master-SHA unverändert: adf01a7ac9ae8a30813e9d27391d0732583671dd6c39b5cca19d33576dd8308f.

Artefakt:
`HD001_V1.14.2_STALE_COMPLETE_UI_GATE_FIX.zip`

SHA-256:
`b5bf0f6201a8158dc968530009d22195e8cc4a27b5421d84010840dafd282dbe`

## REGELKORREKTUR 2026-10-08

Autoritativ:
- Zielvertrag 2.6;
- Assessment Rules 1.6;
- 3-Säulen-Konzept mit Sichtbarkeits-/Hub-Regel;
- Audit: `HD001_BALANCED_VISIBLE_LEVELS_AUDIT_20261008.json`.

Verbindlich:
- jede vorhandene kanonische Ebene ist im Drill-down sichtbar;
- Welt → Zwischenbereich → Hobby → Content-Kategorie → Beiträge;
- globale Headernavigation darf klein bleiben, darf aber keine vorhandene Kindebene auf den Landingpages verstecken;
- bis etwa 10–11 fachlich klare Zwischenbereiche pro Welt sind zulässig;
- keine künstliche Verdichtung nur für eine dünne Navigation;
- keine leeren Symmetrieäste;
- HOBBY_HUB benötigt 3–6 tragfähige sichtbare Content-Kategorien;
- jede Leaf-Kategorie ideal 5–12 eigenständige Beitragsintentionen;
- reguläre HOBBY_HUB-Beiträge nicht direkt unter dem Hobby.

Aktueller V1.14.1/1.14.2-Zielbaum erfüllt diese neue verbindliche Regel NICHT vollständig:
- aktive Zwischenbereiche: 6 / 9 / 9 / 5 / 9 / 6 / 8 / 8;
- nur Buchbinden besitzt derzeit die Content-Kategorieebene;
- deshalb ist V1.14.2 nicht mehr als Sync-Ziel freigegeben.

## AUSGEWOGENE WELT-/ZWISCHENSTRUKTUR – FACHLICH GEPRÜFT

Beleg:
`HD001_BALANCED_WORLD_INTERMEDIATE_TARGET_20261008.json`

Wichtig:
- alle vorhandenen Ebenen bleiben im Drill-down sichtbar;
- keine künstliche Maximalzahl; bis etwa 10–11 Zwischenbereiche zulässig;
- keine leeren Symmetrieäste;
- Welt-/Zwischenstruktur ist fachlich als Arbeitsziel geprüft;
- HOBBY_HUB benötigt weiterhin 3–6 sichtbare Content-Kategorien mit je ideal 5–12 eigenständigen Beitragsintentionen.

Korrigierte Rollenbasis:
- Batch 003 enthielt einen Zähl-/Rollenfehler;
- FPV-Drohnen und RC-Flugzeuge sind nach realer Assessment-Evidence MACRO_REVIEW / ORIENTATION_UNIVERSE, nicht HOBBY_HUB;
- Batch 004–019 sind historische Evidence, keine aktuelle Produktionsautorität;
- aktuelle Produktionsquellen: Batch 001–003 + Expansion19.

Aktuelle CORE-Abdeckung:
- 359 aktuelle CORE-Identitäten;
- 60 davon besitzen eine aktuelle produktionsgültige Rollenentscheidung aus diesen Quellen;
- **299 sind noch nach Regeln 1.6 global zu revalidieren**.

## ERSTER OFFENER BLOCKER

`HD001_GLOBAL_CORE_ROLE_RECHECK_299_PENDING`

## EXAKT EINE NEXT ACTION

Die 299 aktuellen CORE-Identitäten in **einem globalen Recheck** nach Regeln 1.6 prüfen.
Historische Batch-004–019-Evidence darf dabei wiederverwendet werden, aber nicht blind als Entscheidung gelten.

Danach:
- HOBBY_HUBs verbindlich festlegen;
- deren sichtbare Content-Kategorieebene materialisieren;
- erst danach neues Sollprofil.

Bis dahin:
- kein Plugin-Fix;
- kein WordPress-Write;
- kein Sync.
