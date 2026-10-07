# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-07
STATUS: BATCH 001 ECHTE DATAFORSEO-DATEN VOLLSTÄNDIG VORHANDEN / REGELN 1.4 KISS / V1.12.5 GESAMTER BATCH-PFAD LOKAL HARD PASS / EINMALIGER LIVE-READBACK OFFEN / KEIN ZIELBAUM-WRITE

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

Batch 001:
- 16 reproduzierbar ausgewählte Master-Identitäten;
- 16/16 ID-Eindeutigkeit PASS; davon 4 aktuelle Alias-/Kanonikbindungen bestätigt, 12 semantische Identitätsprüfungen offen;
- 2 Scope-Fälle fachlich bestätigt;
- 9 Scope-Fälle nur provisional;
- 5 Scope-Fälle benötigen Evidenz;
- Buchbinden = bestehender Live-/Technikpilot bleibt erhalten, aber V2-Hub-PASS wieder OFFEN: echte DataForSEO-Evidence liefert aktuell 4 / 5 / 3 / 4 distinct Intent-Gruppen in den vier aktiven Leafs; nur Ausrüstung liegt bereits im V2-Ziel 5–12;
- Treibholz sammeln = IN_SCOPE / Sammeln / EDITORIAL, aber ARTICLE_ONLY vs. EDITORIAL_TOPIC noch offen;
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

## Technischer V1.12.0–V1.12.5-Stand

Die komplette Fehlerkette des Testbatches wurde bis zum Ende geprüft.

Reale Datenbasis:
- 16 Hobbys;
- 34 fachlich vorgeschlagene unterste Kategorien;
- 263 fachlich vorgeschlagene Artikelintents;
- historisch 39 echte DataForSEO-Aufrufe;
- historische Kosten ca. 0.9738 USD;
- 0 WordPress-/HivePress-Strukturwrites.

Die zuletzt hochgeladene Ergebnisdatei ist weiterhin ein V1.12.3-Ergebnis.
Sie ist bytegleich mit dem bereits geprüften V1.12.3-Ergebnis und enthält daher noch NICHT die spätere KISS-Neuberechnung.

### Ursache der bisherigen Schleife

V1.12.1:
fehlende exakte Longtail-Zeilen wurden zu stark als fehlende Content Capacity behandelt.

V1.12.2/V1.12.3:
Keyword-Ideas-Treffer wurden zur Tiefenmessung verwendet; dadurch konnten Provider-Rohzeilen Content Capacity künstlich erzeugen.

V1.12.4:
Rohzeilen erzeugten zwar keine neuen Artikel mehr, aber fachlich definierte Artikelintents wurden weiterhin zu stark von einem lexikalischen DataForSEO-Treffer abhängig gemacht.

### Verbindliche KISS-Lösung ab Regeln 1.4 / HD-001 V1.12.5

- Fachlogik definiert und zählt eigenständige Artikelintents.
- Jede unterste Kategorie wird separat auf diese fachlich unterschiedlichen Intents geprüft.
- DataForSEO ist der SEO-Abgleich.
- Exaktes Core-Keyword-/Synonym-Evidence darf fachliche Dubletten zusammenführen.
- Fehlt für einen fachlich eigenständigen Longtail eine exakte Provider-Zeile, bleiben nur seine SEO-Metriken offen; der Artikelintent bleibt bestehen.
- Keyword-Ideas-/Suggestions-Rohzeilen erzeugen niemals zusätzliche Artikel.
- automatische Tiefenrecherche ist im Normalweg deaktiviert.

Damit ist der kostenpflichtige 38-Call-Depth-Weg NICHT mehr Bestandteil des Normalwegs.

### V1.12.5 – vollständiger lokaler Endtest

Artefakt:
`HD001_V1.12.5_KISS_CONTENT_CAPACITY_ZERO_DEPTH_HARDPASS.zip`

SHA-256:
`68d521a9835bcbf2b2658dd0bd8d0a5163e6e1d656bf51855e20f830958a7af9`

Prüfbericht:
`HD001_V1.12.5_FINAL_LOCAL_POSNEG_REPORT.txt`

SHA-256:
`8a6768b4222dd086f3ff124579684feeed6f11f45f268d5596631de326002075`

Fresh-/Regressionstest:
- PHP Source 68/68 PASS;
- Legacy Regression 270/270 PASS;
- V1.12 POS/NEG PASS;
- realer 908/844/841-Bestand PASS;
- V1.12.1 Assessment Regression PASS;
- echtes V1.12.3-Ergebnis lokal neu ausgewertet PASS;
- fehlende 14/15 exakte Provider-Zeilen löschen einen fachlich sauberen 3-Leaf-Hub NICHT PASS;
- exaktes DataForSEO-Core-Keyword kann 5 fachliche Seeds korrekt auf 4 deduplizieren PASS;
- Provider-/Depth-Rohzeilen erzeugen 0 zusätzliche Artikel PASS;
- automatische Depth-Recherche = 0 Calls PASS;
- 0 neue Provider-Kosten PASS;
- 0 Strukturwrites PASS;
- Neuberechnung idempotent PASS;
- Fresh Release PHP 31/31 PASS.

Lokaler Replay des echten Batch-001-Ergebnisses:
- 34 ideale Leafs;
- 1 HOBBY_HUB_CANDIDATE;
- 1 EDITORIAL_TOPIC_CANDIDATE;
- 5 AGGREGATION_REVIEW;
- 3 MACRO_REVIEW;
- 6 EVIDENCE_REQUIRED;
- 0 Zielbaum-Writes.

Kapazitätsseitig im typischen Hubbereich, aber noch mit Scope-/Identitätsprüfung:
Airbrush 5 Leafs, Bean-to-Bar-Schokolade 6, Aeroponik 4, Ameisenhaltung 6, 3D-Bogenschießen 5, Wabikusa 4.

Buchbinden ist im kontrollierten Batch der vollständige HOBBY_HUB_CANDIDATE:
4 ideale Leafs mit 5 / 6 / 6 / 6 fachlich eigenständigen Artikelintents.

Beleg:
`HOBBY_MASTER_V2_BATCH_001_V125_KISS_REPLAY_20261007.md`

## ERSTER OFFENER BLOCKER

`HD001_V2_BATCH001_V125_SINGLE_LIVE_READBACK_PENDING`

Es gibt keinen offenen DataForSEO-Rechercheblocker mehr.

Der komplette Batch-001-Weg ist mit der echten gespeicherten DataForSEO-Evidence lokal bis zum Endergebnis durchsimuliert und hart getestet.

Offen ist nur der einmalige reale WordPress-Readback des exakt getesteten V1.12.5-Artefakts.

## EXAKT EINE NEXT ACTION

Einmal HD-001 V1.12.5 in Hobby Depot installieren und `Kategorien → V2-Hobbybewertung` öffnen.

V1.12.5 muss das vorhandene gespeicherte Ergebnis automatisch nach Regeln 1.4 neu berechnen.

Erwartung:
- 0 neue DataForSEO-Aufrufe;
- 0 neue DataForSEO-Kosten;
- 0 Strukturwrites;
- Result-Version 1.4 / Plugin 1.12.5;
- dieselbe fachliche Batch-Summary wie im lokalen Real-Result-Replay.

Danach Ergebnis-JSON einmal herunterladen und readback-prüfen.

Noch kein Zielbaum-Delta.
Noch kein Kategorien-Sync.
