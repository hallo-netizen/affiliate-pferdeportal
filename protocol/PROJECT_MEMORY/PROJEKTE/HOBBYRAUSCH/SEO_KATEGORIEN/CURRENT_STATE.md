# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-07
STATUS: REGELN 1.4 KISS / ECHTE DATAFORSEO-EVIDENCE VORHANDEN / V1.12.5 LIVE-READBACK WAR STALE V1.12.3-EXPORT / ROOT CAUSE GEFUNDEN / V1.12.6 STALE-EXPORT-FAILCLOSED LOKAL HARD PASS / NEUER REALER EXPORT OFFEN / KEIN ZIELBAUM-WRITE

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

Batch 001 – aktueller V1.12.5-Replay:
- 16 reproduzierbar ausgewählte Master-Identitäten;
- 34 ideale Leafs;
- Buchbinden = HOBBY_HUB_CANDIDATE mit 4 idealen Leafs und 5 / 6 / 6 / 6 fachlich eigenständigen Artikelintents;
- Airbrush, Bean-to-Bar-Schokolade, Aeroponik, Ameisenhaltung, 3D-Bogenschießen und Wabikusa = kapazitätsseitig typischer Hubbereich, aber Scope/Identität noch offen;
- 3D-Druck, Amateurastronomie und Filzen = MACRO_REVIEW;
- Treibholz sammeln = EDITORIAL_TOPIC_CANDIDATE;
- fünf kleine/spezielle Themen = AGGREGATION_REVIEW;
- keine automatische Promotion aus DIRECT/ASSISTED;
- 0 Zielbaum-Writes zulässig.

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

## ERSTER OFFENER BLOCKER

`HD001_V2_BATCH001_V126_REAL_EXPORT_READBACK_PENDING`

Der fachliche KISS-Recalc selbst ist lokal mit der echten gespeicherten Datei vollständig PASS.

Offen ist nur noch der reale Export-Nachweis des gehärteten Download-Gates.

## EXAKT EINE NEXT ACTION

HD-001 V1.12.6 in Hobby Depot installieren und direkt `Ergebnis als JSON herunterladen` klicken.

Kein DataForSEO starten.
Kein Reset.
Keine Tiefenprüfung nötig.

Der Download selbst muss jetzt:
- Plugin-Version 1.12.6 ausgeben;
- 34 ideale Leafs;
- 1 Hub-Kandidat;
- 0 neue Provider-Aufrufe;
- 0 neue Kosten;
- 0 Strukturwrites.

Danach genau dieses JSON readback-prüfen.

Noch kein Zielbaum-Delta.
Noch kein Kategorien-Sync.
