# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-08
STATUS: REGELN 1.5 / V1.13.1 FRISCHER POST-ROLLBACK-DRYRUN PASS / 356 CREATE + 75 ADOPT / 0 DATAFORSEO / 0 WRITES / ALTER V1.12-ROLLBACK TERMINAL ROLLED_BACK / FINAL-SYNC DURCH MATERIALKUNST-KONZEPTBLOCKER GESPERRT

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

## ERSTER OFFENER BLOCKER

`HD001_V1_13_1_EMPTY_CORE_NODE_MATERIALKUNST`

Exakt:
- `core:gestalten:materialkunst` steht im frischen Zielplan als `CREATE`;
- 0 Kindknoten;
- keine kanonische Hobby-Identität;
- 0 gebundene Entity-Placements;
- keine belegte Relation.

Damit wäre `Materialkunst` ein neu angelegter strukturell leerer Zwischenknoten und widerspricht Zielvertrag 2.5:
**Keine inhaltsleeren Ebenen.**

## EXAKT EINE NEXT ACTION

Finalen Sync NICHT starten.

KISS:
`core:gestalten:materialkunst` aus dem finalen V1.13.1-Zielprofil entfernen.

Maschinenlesbarer Ein-Knoten-Patch:
`HD001_V1_13_1_TARGET_PROFILE_PATCH_001_20261008.json`.

Keine Ersatzkategorie erfinden.
Keine Hobbys umhängen.
Keine DataForSEO-Recherche.

Danach Zielprofil erneut hart prüfen → frischer finaler Live-Dry-Run → JSON-Readback.
