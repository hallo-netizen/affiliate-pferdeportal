# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-09
STATUS: V1.14.8 = EINZIGE FREIGEGEBENE TECHNISCHE BASIS / V1.14.9+1.14.10 VERWORFEN / PILOT 2.7 NUR ÜBER BESTEHENDEN V2-OVERVIEW-BACKENDPFAD

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

## Rollen- und Größenlogik – CURRENT 2.7

Publikationsrollen:
- ORIENTATION_UNIVERSE;
- HOBBY_HUB;
- EDITORIAL_TOPIC;
- ARTICLE_ONLY;
- FINDER_ONLY;
- OUT_OF_SCOPE.

Unterste Content-Kategorie:
- mindestens 3 eigenständige sinnvolle Beitragsintentionen = startfähig;
- 4+ = klar tragfähig;
- Synonyme/Formulierungsvarianten zählen nicht mehrfach;
- keine künstliche Gesamtobergrenze je HOBBY_HUB;
- bestehende sinnvolle Leafs bleiben erhalten.

HOBBY_HUB:
- Pflichtabdeckung Einstieg & Grundlagen;
- Pflichtabdeckung FAQ;
- Ausrüstung & Kosten als eigener Leaf, sobald 3 eigenständige Beiträge möglich sind;
- Vertiefung/Fachwissen muss sichtbar abgedeckt sein, aber vorhandene Fach-Leafs dürfen dies bereits erfüllen;
- zusätzliche hobbiespezifische Leafs ab 3 eigenständigen Beitragsintentionen.

Zweite CORE-/Mega-Menü-Ebene:
- maximal 10 direkte sichtbare Kinder pro Welt;
- Fertigen und Technik liegen im aktuellen Zielbaum bei 11 und müssen vor dem nächsten Sollprofil neu geordnet werden.

## DataForSEO-Vertrag

DataForSEO darf:
- Nachfrageband;
- Primärkeyword;
- Synonyme;
- Longtail-Tiefe;
- Keyword-/Intent-Überschneidung;
- konkrete FAQ-/Frageintents;
- zusätzliche Leaf-Kandidaten unter einem bereits feststehenden HOBBY_HUB;
- Clustering und Deduplizierung dieser Leaf-/Artikelkandidaten

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

Historischer Stand der Rule-1.6-Phase, durch Zielvertrag 2.7 für die Produktionspraxis ersetzt:
- jede vorhandene kanonische Ebene war im Drill-down sichtbar;
- Welt → Zwischenbereich → Hobby → Content-Kategorie → Beiträge;
- damalige Prüfgröße 10–11 Zwischenbereiche pro Welt;
- damalige Prüfgröße 3–6 Content-Kategorien je HOBBY_HUB;
- damalige Idealgröße 5–12 Beitragsintentionen je Leaf.
Diese Zahlen bleiben historische Evidence und sind keine aktuelle Produktionsgrenze mehr.

Aktueller V1.14.1/1.14.2-Zielbaum erfüllt diese neue verbindliche Regel NICHT vollständig:
- aktive Zwischenbereiche: 6 / 9 / 9 / 5 / 9 / 6 / 8 / 8;
- nur Buchbinden besitzt derzeit die Content-Kategorieebene;
- deshalb ist V1.14.2 nicht mehr als Sync-Ziel freigegeben.

## HISTORISCH: AUSGEWOGENE WELT-/ZWISCHENSTRUKTUR – RULE-1.6-PHASE

Beleg:
`HD001_BALANCED_WORLD_INTERMEDIATE_TARGET_20261008.json`

Historische Rule-1.6-Evidence:
- alle vorhandenen Ebenen sollten im Drill-down sichtbar sein;
- damals galten bis etwa 10–11 Zwischenbereiche und 3–6 Leafs/5–12 Intents als Prüfgrößen.
Diese Größen sind durch Zielvertrag 2.7 ersetzt. Aktuell gilt max. 10 auf der zweiten Mega-Menü-Ebene und mindestens 3 eigenständige Beiträge pro Content-Leaf ohne künstliche Leaf-Gesamtobergrenze.

Korrigierte Rollenbasis:
- Batch 003 enthielt einen Zähl-/Rollenfehler;
- FPV-Drohnen und RC-Flugzeuge sind nach realer Assessment-Evidence MACRO_REVIEW / ORIENTATION_UNIVERSE, nicht HOBBY_HUB;
- Batch 004–019 sind historische Evidence, keine aktuelle Produktionsautorität;
- aktuelle Produktionsquellen: Batch 001–003 + Expansion19.

Aktuelle CORE-Abdeckung:
- 359 aktuelle CORE-Identitäten;
- 60 davon besitzen eine aktuelle produktionsgültige Rollenentscheidung aus diesen Quellen;
- **299 sind noch nach Regeln 1.6 global zu revalidieren**.

## GLOBALER CORE-RECHECK – ZWISCHENSTAND

Aktuelle feste Prüfmenge:
`HD001_CURRENT_CORE_359_NAMES_20261008.json`

Neu geprüft:
- 359 aktuelle CORE-Identitäten als feste Prüfmenge gebunden;
- 161 besitzen jetzt eine aktuelle Rollenentscheidung nach 1.6;
- davon wurden die 75 historischen aktuellen HOBBY_HUBs aus Batch 005–019 vollständig auf die fehlende Content-Ebene nachgezogen;
- Ergebnis dieser 84 Hubs: **397 sichtbare Content-Kategorien**, Capacity jeweils 5–12 Intents;
- 0 Capacity-Verstöße in den Nachprüfungen;
- bekannte alte Demotion-/Aliasfälle werden nicht blind als CORE-HUB weitergeführt;
- historische Batch-Summaries werden nicht als Wahrheit verwendet; Einzelentscheidungen und vorhandene Evidence haben Vorrang.

Detail-Evidence:
- Batch 004: `HOBBY_MASTER_V2_BATCH_004_RULE16_RECONSTRUCTION_20261008.json`;
- Batch 005: `HOBBY_MASTER_V2_BATCH_005_RULE16_RECONSTRUCTION_20261008.json`;
- Batch 006/007/009: `HOBBY_MASTER_V2_BATCH_006_007_009_RULE16_RECONSTRUCTION_20261008.json`;
- Batch 010: `HOBBY_MASTER_V2_BATCH_010_RULE16_RECONSTRUCTION_20261008.json`;
- Batch 011: `HOBBY_MASTER_V2_BATCH_011_RULE16_RECONSTRUCTION_20261008.json`;
- Batch 012: A/B1/B2;
- Batch 013: `HOBBY_MASTER_V2_BATCH_013_RULE16_RECHECK_20261008.json`;
- Batch 014/015: Einzel-Hub-Rechecks;
- Batch 016/017/019: `HD001_BATCH016_017_019_RULE16_VALIDATION_SUMMARY_20261008.json` + lokal validierte Detail-Evidence SHA-256 `d5ed61305fe2e057baba1e20a8743567778cbebc7c5be91ef995ea7659ee2f9b`.

Damit ist die frühere 299er-Blackbox reduziert:
- **161 entschieden**;
- **198 aktuelle CORE-Identitäten noch offen**.

## CORE-RECHECK – AKTUELL

- feste Prüfmenge: 359 aktuelle CORE-Identitäten;
- 161 nach Regel 1.6 entschieden;
- 84 historische aktuelle HOBBY_HUBs nachgeprüft;
- daraus 397 sichtbare Content-Kategorien;
- alle geprüften Leafs im Bereich 5–12;
- verbleibend: 198 aktuelle CORE-Identitäten.

## GLOBALER CORE-RECHECK – FORTSCHRITT

Feste Prüfmenge:
359 aktuelle CORE-Identitäten.

Bereits entschieden:
- vorher 161;
- neuer Block Gestalten + Genuss: 17;
- aktuell **178 entschieden**;
- **181 offen**.

Neuer Beleg:
`HD001_GLOBAL_CORE_RECHECK_RULE16_GESTALTEN_GENUSS_20261008.json`

Ergebnis neuer Block:
- 16 HOBBY_HUB;
- 1 ORIENTATION_UNIVERSE (Fermentation);
- 80 sichtbare Content-Kategorien;
- jede Leaf-Kategorie 5 eigenständige Intents;
- 0 Capacity-Verstöße;
- 0 Provider-Aufrufe;
- 0 WordPress-Writes.

Zusammen mit den bereits rekonstruierten historischen Hubs sind aktuell **477 sichtbare Content-Kategorien** in Rule-1.6-Recheck-Evidence dokumentiert.

## GLOBALER CORE-RECHECK – FORTSCHRITT

Feste Prüfmenge:
359 aktuelle CORE-Identitäten.

Aktuell entschieden:
- **209 von 359**;
- **150 offen**.

Neu abgeschlossen:
- Gestalten + Genuss: 17 Identitäten / 16 HOBBY_HUB / 80 Content-Kategorien;
- Astronomie + Mikroskopie: 13 Identitäten / 10 HOBBY_HUB / 48 Content-Kategorien;
- Wetter + Naturbeobachtung + Messen: 18 Identitäten / 14 HOBBY_HUB / 58 Content-Kategorien.

Neue Evidence:
- `HD001_GLOBAL_CORE_RECHECK_RULE16_GESTALTEN_GENUSS_20261008.json`;
- `HD001_GLOBAL_CORE_RECHECK_RULE16_ASTRONOMIE_MIKROSKOPIE_20261008.json`;
- `HD001_GLOBAL_CORE_RECHECK_RULE16_WETTER_NATUR_MESSEN_20261008.json`.

Zusammen mit den bereits rekonstruierten historischen Hubs sind derzeit **583 sichtbare Content-Kategorien** in Rule-1.6-Recheck-Evidence dokumentiert.

## GLOBALER CORE-RECHECK – FORTSCHRITT

Feste Prüfmenge:
359 aktuelle CORE-Identitäten.

Aktuell entschieden:
- **272 von 359**;
- **87 offen**.

Zusätzlich abgeschlossen:
- Pflanzen: 33 Identitäten / 19 HOBBY_HUB / 85 Content-Kategorien / 2 belegte Alias-Dubletten;
- Tiere: 30 Identitäten / 22 HOBBY_HUB / 99 Content-Kategorien.

Evidence:
- `HD001_GLOBAL_CORE_RECHECK_RULE16_PFLANZEN_20261008.json`;
- `HD001_GLOBAL_CORE_RECHECK_RULE16_TIERE_20261008.json`.

Gesamter Rule-1.6-Recheck-Evidence-Stand:
- **767 sichtbare Content-Kategorien**;
- alle materialisierten Leafs 5–12 Intents;
- 0 Capacity-Verstöße;
- 0 WordPress-Writes.

## HISTORISCHER GLOBALER CORE-RECHECK – RULE 1.6 ABGESCHLOSSEN

Autoritative Abschluss-Evidence:
- `HD001_GLOBAL_CORE_359_RULE16_FINAL_AUDIT_20261008.json`;
- `HD001_FINAL_VISIBLE_FACH_SOLLPROFIL_20261008.json`;
- `HD001_REMAINING_41_HUBS_RULE16_VISIBLE_LEAF_MATERIALIZATION_20261008.json`.

Endstand:
- 359/359 aktuelle CORE-Identitäten entschieden;
- 279 HOBBY_HUB;
- 53 ORIENTATION_UNIVERSE;
- 22 EDITORIAL_TOPIC → aus CORE zu demoten, redaktionell erhalten;
- 5 ALIAS_ONLY → kein zweiter SEO-Owner;
- 332 endgültige CORE-Identitätsseiten;
- 65 aktive Zwischenbereiche in 8 Welten;
- 279/279 HOBBY_HUBs besitzen eine sichtbare Content-Kategorieebene;
- 1.292 sichtbare Content-Kategorien;
- damaliger Rule-1.6-Stand: jeder Hub 3–6 Leafs;
- damaliger Rule-1.6-Stand: jede materialisierte Leaf 5–12 eigenständige Intents;
- damaliger Rule-1.6-Stand: 0 Capacity-Verstöße.
Diese Capacity-Regel ist historische Evidence und seit Zielvertrag 2.7 keine aktuelle Produktionsgrenze.

Korrigierte späte Evidence:
- Batch 002: Mikrocontroller-Projekte = ORIENTATION/MACRO, CB-Funk und SDR je 5 Leafs;
- Batch 003 spätere Final-Evidence: Drone Soccer und Scale-Crawling = HOBBY_HUB; RC-Baumaschinen/RC-LKW/RC-Panzer je 5 Leafs.

Keine Pluginänderung und kein WordPress-Write wurden für diese fachliche Neuberechnung ausgeführt.

## TECHNISCHER OBJEKTPLAN + V1.14.3 – FULL LOCAL HARD PASS

Beleg:
`HD001_V1_14_3_RULE16_VISIBLE_FULL_LOCAL_HARDPASS_20261008.json`

Finaler technischer Zielstand:
- 855 kanonische Identitäten nach 5 Alias-Zusammenführungen;
- 332 finale CORE-Identitäten;
- 523 Editorial/Finder;
- 1.737 Logikknoten;
- 1.723 physische Zielobjekte;
- 408 Pages;
- 1.292 WordPress-Content-Kategorien;
- 15 journal_cat;
- 8 hp_listing_category;
- 9 Relations;
- 65 aktive Zwischenbereiche;
- 279/279 HOBBY_HUBs mit sichtbarer Content-Kategorieebene.

Migration gegen V1.14.1-Profil:
- 1.293 CREATE;
- 430 UPDATE;
- 27 ARCHIVE;
- 0 ADOPT;
- 28 bestehende Hobbyseiten werden per legacy_ids identitätserhaltend migriert statt neu angelegt;
- Readback 1.723/1.723 COMPLETE.

Idempotenz:
- zweiter Dry-Run: 1.723 UNCHANGED / 0 ARCHIVE;
- zweiter Sync: 1.723 UNCHANGED / 0 ARCHIVE / **0 Writes**;
- dritter Dry-Run: 1.723 UNCHANGED / 0 ARCHIVE.

Frontend:
- PASS;
- Header 102;
- lokale Welt-Kinder 7 / 11 / 11 / 5 / 10 / 7 / 8 / 8;
- 65 Zwischenbereiche;
- 0 leere Zwischenbereiche;
- 279/279 Hubseiten korrekt.

Negative Tests:
- Duplicate Slug BLOCKED;
- Missing Parent BLOCKED;
- Depth Exceeded BLOCKED;
- Name Too Long BLOCKED;
- Duplicate Node ID BLOCKED.

PHP:
- 33/33 PASS.

Artefakt:
`HD001_V1.14.3_RULE16_VISIBLE_FINAL_HARDPASS.zip`

SHA-256:
`deaee48b4f7310d94a5975b3dd471b0374d369745b1b7dd48c512ae514d7c7de`

Profil SHA-256:
`6578a1aa4dccf554bb685a36e564c32af897c85bb1aac06d0401c5fc683622b6`

0 Provider-Aufrufe.
0 WordPress-Writes in der lokalen Prüfung.

## V1.14.3 LIVE-DRY-RUN – PASS

Beleg:
`HD001_V1_14_3_LIVE_DRYRUN_PASS_20261009.json`

Live read-only:
- Plugin 1.14.3;
- valid=true / errors=[];
- 855 Identitäten / 332 CORE / 523 Editorial-Finder;
- 1.737 Logikknoten / 1.723 physische Zielobjekte;
- **1.293 CREATE + 430 UPDATE + 27 ARCHIVE + 0 ADOPT**;
- exakt identisch zum lokal erwarteten V1.14.3-Migrationsdelta;
- 0 Provider-Aufrufe;
- 0 WordPress-Writes.

Archive:
- 22 EDITORIAL_TOPIC;
- 5 ALIAS_ONLY;
- **0 HOBBY_HUB-Archive**.

Der im Export enthaltene `sync_state` und `frontend_readback` gehören noch zur alten live synchronisierten V1.14.1-Revision mit 457 Zielobjekten.
Der Frontend-Fehler `HEADER_BLOCK_FILTER_NOT_CANONICAL,HEADER_LEGACY_LEAK` ist damit ein PRE-SYNC-Befund des alten Stands, kein V1.14.3-Post-Sync-Ergebnis.
Nach dem freigegebenen Sync ist der V1.14.3-Frontend-/Header-Readback zwingend erneut zu prüfen.

## POST-SYNC V1.14.3 / V1.14.4 – CURRENT

Realer Post-Sync-Readback:
`hobby-depot-final-target-readback-20261009-074655-utc.json`

V1.14.3 real:
- Dry-Run PASS;
- Sync schrieb den Zielbaum, Readback stoppte nach 39 Knoten;
- Fehler: `core:gestalten:oberflaeche-deko [name]`;
- Sync danach vollständig `ROLLED_BACK`;
- damit blieben die 1.288 neu vorgesehenen Content-Kategorien nicht live bestehen.

Regelprüfung gegen Zielvertrag 2.6 + Assessment Rules 1.6:
- 279/279 HOBBY_HUBs besitzen im Soll eine sichtbare Content-Kategorieebene;
- 1.292 Content-Kategorien;
- Verteilung 117×4 / 148×5 / 14×6;
- Rule16-Endaudit: 0 Capacity-Verstöße bei 5–12 Intentions als Idealbereich;
- maximale Tiefe 4;
- `Keine Kategorie unter Kategorie` ist hart verbindlich;
- Views/Filter wie zuhause/ungewöhnlich erzeugen keine zweite Hobbytaxonomie;
- fehlende Evidenz bleibt `EVIDENCE_REQUIRED`, keine Schätzung.

Zusätzlicher realer Konzeptfehler in V1.14.3:
Der Magazinbaum modellierte 12 `journal_cat → journal_cat`-Kanten und verletzte damit `Keine Kategorie unter Kategorie`.

V1.14.4 lokal korrigiert:
- Page-/Term-Namen werden vor strengem sichtbarem Namensvergleich HTML-entity-normalisiert;
- echte Namensänderungen bleiben Readbackfehler und lösen Rollback aus;
- Readbackfehler nennen künftig `expected_name` + `actual_name`;
- Kategorie-unter-Kategorie wird generisch vom Validator geblockt;
- Magazin-Gruppen sind Seiten/Views, darunter die echten Magazin-Kategorien;
- neutraler Editorial-Fallback = Hobbyfinder;
- keine automatische Zuordnung zu spezifischen Magazin-Leafs ohne Evidenz;
- keine zusätzliche Saison/Kategorie erfunden.

Fester Magazinbaum:
- Hobby finden → Hobbyfinder / Hobbywelten;
- Nach Situation → Zuhause / Draußen / Alleine / Zu zweit / Wenig Platz / Wenig Zeit;
- Nach Jahreszeit → Winter / Sommer;
- Entdecken → Ungewöhnliche Hobbys / Verrückte Hobbys / Neue Hobbys / Trends.

Lokaler V1.14.4-Hardpass:
- Dry-Run PASS: 1.296 CREATE / 427 UPDATE / 30 ARCHIVE;
- Sync COMPLETE: 1.723/1.723 Readbacks;
- Header 102/102 PASS;
- Magazin 4/4 PASS;
- Hobby finden 2/2 PASS;
- Situation 6/6, Jahreszeit 2/2, Entdecken 4/4 PASS;
- Buchbinden 4/4 PASS;
- zweiter Sync 1.723 UNCHANGED / 0 Writes;
- Negativfälle Kategorie-unter-Kategorie, fehlender Parent, doppelter Slug, Name zu lang, doppelte ID, Tiefe >4, Cross-Pillar-Parent, unbekanntes Relationsziel: alle fail-closed;
- echte Namensänderung `Oberfläche und Deko` → Readbackfehler + ROLLED_BACK;
- PHP 33/33 vor und nach Fresh-Unpack.

Artefakt:
`HD001_V1.14.4_RULES_MAGAZIN_FULL_LOCAL_HARDPASS.zip`

SHA-256:
`9ec9b0d7b2776c59262aebbed9d3e9a88a533ce11084c4e66cd011a9126da06d`

Profil SHA-256:
`08c1da1bb43add667b73ea02bbaab6d3ad3c3228de88673254d8d5ebbdb8996c`

Evidence:
`SEO_KATEGORIEN/HD001_V1_14_4_RULES_MAGAZIN_FULL_LOCAL_HARDPASS_20261009.json`

Wichtig:
Der exportierte Live-Readback speichert den tatsächlich zurückgelesenen Titel des alten Page-Name-Fehlers nicht. Deshalb wird kein exakter Live-Rückgabestring behauptet. Lokal wurde jedoch derselbe Fehlerknoten nach exakt denselben 39 Readbacks mit dem fehlenden Page-Entity-Normalisierungspfad reproduziert.

## HISTORISCHER BLOCKER – GESCHLOSSEN

`HD001_V1_14_4_LIVE_INSTALL_AND_SYNC_PENDING`

## HISTORISCHE NEXT ACTION – ERLEDIGT

Der damalige V1.14.4-Live-Schritt ist durch den späteren V1.14.8-Live-Lauf überholt. Nicht mehr als aktuelle Handlungsanweisung verwenden.


## V1.14.8 LIVE – TECHNISCH COMPLETE, FACHLICH NICHT ABGENOMMEN

Realer Post-Sync-Readback:
`hobby-depot-final-target-readback-20261009-114254-utc.json`

Bewiesen:
- plugin_version 1.14.8;
- Dry-Run PASS;
- 1.723 Zielobjekte;
- CREATE 0;
- UPDATE 0;
- UNCHANGED 1.723;
- ARCHIVE 0;
- DEMOTE_EDITORIAL 52;
- Runner COMPLETE;
- Readback 1.723/1.723;
- interner Frontend-Readback valid=true;
- interner Hobby-Hub-Gate 279/279;
- 0 unbound Core pages nach Demotion.

Damit ist die 52er-Legacy-Demotion technisch abgeschlossen.

ABER:
Der reale sichtbare Seitenbefund zeigt, dass die untersten Kategorien nicht auf allen Hobbyseiten zuverlässig sichtbar sind.
Zusätzlich zeigt die fachliche Sichtprüfung, dass die 1.292 vorhandenen Content-Kategorien zwar fachliche Cluster bilden, aber universelle Nutzerbedürfnisse wie Einstieg, FAQ und Ausrüstung/Kosten nicht systematisch abdecken.

Daher:
**kein fachlicher Portal-PASS.**
Ein interner Renderer-PASS ist nicht länger ausreichend für sichtbare Frontend-Abnahme.

## NEUE CURRENT-REGEL – ZIELVERTRAG 2.7

Autoritativ:
`ZIELVERTRAG_HD001_AUTOMATISCHE_SEO_HIERARCHIE_20261003.md`
Fassung 2.7.

Kern:
- sichtbare Mega-Menü-Zwischenebene max. 10 Kinder je Welt;
- aktueller Live-Header: Fertigen 10, Technik 11; nur Technik muss vor dem nächsten Zielbaum reduziert werden;
- strukturelle Direktknoten wie Heimwerken/Gärtnern können auf Landingpages zusätzlich existieren und zählen nicht als Mega-Menü-Zwischenkategorie;
- unterste Content-Ebene ohne künstliche Gesamtobergrenze;
- bestehende sinnvolle Leafs bleiben;
- 3 eigenständige Beiträge reichen als startfähige Mindestkapazität;
- universelle Prüffelder: Einstieg & Grundlagen, FAQ, Ausrüstung & Kosten, Praxis/Vertiefung;
- Vertiefung nicht duplizieren, wenn bestehende Fach-Leafs erfahrene Nutzer bereits bedienen;
- DataForSEO darf Leaf-/FAQ-Kandidaten unter festem Hobby vorschlagen und clustern;
- Magazin wird als eigenständige flexible Kachel-/SEO-Säule ausgebaut.

## ERSTER OFFENER BLOCKER

`HD001_PILOT27_DATAFORSEO_LIVE_PENDING`

## EXAKT EINE NEXT ACTION

Kein weiterer Plugin-Patch.

Zuerst fachlich:
1. Fertigen bleibt mit 10 sichtbaren Mega-Menü-Zwischenkategorien unverändert;
2. Technik: RC-Boote + RC-Flug & Drohnen + RC-Fahrzeuge als gemeinsame zweite Ebene RC & Modelltechnik prüfen/simulieren → 9 sichtbare Mega-Menü-Kinder;
3. verbindlicher Pilot: Buchbinden, Balance Board, Glasmalerei, Lasergravieren, Fledermausbeobachtung, Hydrokultur, Riffaquaristik, Briefmarken sammeln, Geocaching, Imkerei;
4. Bestands-Leafs erhalten;
5. universelle Lücken nach Regel 2.7 ergänzen;
6. zusätzliche hobbiespezifische Leafs mit mindestens 3 echten Beitragsintentionen bestimmen;
7. DataForSEO für konkrete Fragen/Keywords/Leaf-Kandidaten verwenden;
8. echten Browser-/Theme-Pilot prüfen;
9. erst danach neues Sollprofil und technische Umsetzung.

## VERBINDLICHE LERNREGEL FÜR FOLGEPROJEKTE

Technische Vollautomatisierung kommt erst NACH einem sichtbaren manuellen/halbautomatischen Pilot mit mindestens 10 realen Seiten.

Keine Architektur-/Plugin-Komplexität mehr aufbauen, bevor:
- Nutzerpfad;
- sichtbare Ebenen;
- Designgrenzen;
- Standardkategorien;
- individuelle Kategorien;
- echte Browserdarstellung

fachlich bestätigt sind.

Die ausführliche Retrospektive und das Magazin-/Leaf-Konzept liegen in:
`../KONZEPT/CURRENT_STATE.md`.



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


## ROOT CAUSE 1.14.9 / SICHERER RÜCKWEG ÜBER BESTEHENDEN BACKENDPFAD

Befund:
- DataForSEO selbst war nicht neu problematisch.
- V1.14.8 besitzt bereits den bewährten DataForSEO-Client und den read-only V2-Hobbybewertungsweg.
- Der aktuelle KISS-V2-Weg verwendet für fachlich definierte Intents gebündelt `keyword_overview`.
- V1.14.9 führte dagegen neu einen eigenen Pilot-2.7-Backendpfad ein und reaktivierte `dataforseo_labs/google/keyword_ideas/live`.
- Genau diese Keyword-Ideas-Tiefenlogik war historisch bereits timeoutanfällig und wurde in V1.12.5/V1.12.6 aus dem normalen KISS-Weg entfernt.
- Der 1.14.9-Lokaltest mockte den Provider und prüfte deshalb den echten HTTP-/Hostingpfad nicht. Das war ein Abnahmefehler.
- V1.14.9 und V1.14.10 laden lokal ohne Bootstrap-/admin_menu-Fatal. Die Störung war daher kein nachgewiesener allgemeiner PHP-Boot-Fatal des Plugins.
- Der neue Pilotpfad war fachlich und technisch unnötig: derselbe Research-Zweck kann über den bereits vorhandenen read-only V2-Uploadpfad erfolgen.

Verbindliche Korrektur:
- V1.14.9 und V1.14.10 NICHT weiterverwenden.
- Keine neue Pluginversion für Pilot 2.7.
- Exakten bekannten V1.14.8-Stand als technische Basis verwenden.
- Pilotdaten als V2-Bewertungsinput hochladen.
- Backendpfad: Kategorien → V2-Hobbybewertung.
- Providerweg: exakt der bestehende `keyword_overview`-Pfad.
- Keine Keyword-Ideas-Tiefenrecherche.
- Keine Strukturwrites.

Vorbereiteter Pilotinput:
`HD001_PILOT27_10_OVERVIEW_INPUT_20261009.json`
- 10 Hobbys;
- 22 reine Ergänzungs-/Prüf-Leafs;
- 98 konkrete Artikel-/Frage-/Kostenintents;
- 98 deduplizierte DataForSEO-Keywords;
- Preflight im unveränderten V1.14.8-Code: valid=true;
- exakt 1 geplanter `keyword_overview`-Call;
- structure_write_capability=false;
- lokaler Mock-Lauf: exakt 1 Provider-Call / 0 Strukturwrites.

Wichtig:
Die alte V2-Auswertung enthält noch historische 1.6-Kapazitätslabels. Diese werden für den Pilot NICHT als aktuelle Strukturentscheidung übernommen.
Nach dem Export wird ausschließlich nach Zielvertrag 2.7 ausgewertet:
- bestehende Leafs bleiben;
- ab 3 eigenständigen sinnvollen Intents startfähig;
- keine künstliche 3–6-Gesamtgrenze.

Nächster Server-Schritt erst nach Wiederherstellung:
1. V1.14.9 deaktiviert lassen;
2. bekannten V1.14.8-Stand wiederherstellen;
3. V2-Hobbybewertung öffnen;
4. vorbereiteten Pilotinput kostenlos vorprüfen;
5. erwartete Anzeige: 10 Hobbys / 22 vorgeschlagene Prüfleafs / 98 Einzelintents / 98 Keywords / 1 DataForSEO-Aufruf;
6. erst dann diesen einen read-only Overview-Aufruf bestätigen;
7. Ergebnis-JSON herunterladen;
8. kein Zielbaum-Sync.
