# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-07
STATUS: BATCH 001 REALER V1.12.3 DEPTH-LAUF ABGESCHLOSSEN / FREMDTREFFER-ZÄHLFEHLER ERKANNT / REGELN 1.3 / V1.12.4 ZERO-COST-NEUAUSWERTUNG LOKAL HARD PASS / KEIN ZIELBAUM-WRITE

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

Verbindlich seit Regelversion 1.3:
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

## Technischer V1.12.0–V1.12.4-Stand

V1.12.0 bleibt technische Zielbaum-Baseline.

Realer Batch 001:
- V1.12.1 initialer Overview: 263 fachlich vorgeschlagene Artikelintents, 106 exakte Provider-Zeilen;
- V1.12.3 Tiefenlauf vollständig abgeschlossen;
- insgesamt 39 DataForSEO-Aufrufe;
- Gesamtkosten ca. 0.9738 USD;
- weiterhin 0 WordPress-/HivePress-Strukturwrites.

Dabei wurde ein Auswertungsfehler sichtbar:
V1.12.3 zählte rohe Keyword-Ideas-Gruppen als zusätzliche Artikelintents.
Dadurch konnten fachfremde Provider-Treffer die Leaf-Kapazität künstlich aufblasen.

Korrektur in Regelvertrag 1.3:
- Fachlogik definiert die Artikelintents;
- DataForSEO liefert nur Evidenz für diese bereits definierten Intents;
- Provider-Zeilen erzeugen keine neuen Artikel;
- gleiche Core-Keywords zählen weiterhin nur einmal.

HD-001 V1.12.4 korrigiert ausschließlich die vorhandene Auswertung:
- keine neuen DataForSEO-Aufrufe;
- keine neuen Kosten;
- vorhandene COMPLETE-Tiefendaten werden automatisch neu ausgewertet;
- ein Depth-Treffer kann nur einen bereits vorhandenen PENDING-Artikelintent bestätigen;
- unpassende Provider-Treffer bleiben Roh-Evidenz und zählen nicht;
- 0 Strukturwrites.

Lokales Artefakt:
`HD001_V1.12.4_V2_RELEVANCE_RECALC_ZERO_COST_HARDPASS.zip`

SHA-256:
`5ceffaa03eda90b45a235cf844ff2ddae3bef553f2a61f4ec32ea38eefcf75f6`

Prüfbericht:
`HD001_V1.12.4_FINAL_LOCAL_POSNEG_REPORT.txt`

Prüfbericht SHA-256:
`6b8938a5a5b46b1876a564f69f26f60048963e1fc1e5edbd879b7531bc643bb3`

Fresh-Unpack:
- PHP 66/66 PASS;
- Legacy Regression 270/270 PASS;
- Fremdkeyword-/Relevanztest PASS;
- realer V1.12.3-Result-Replay PASS;
- 0 zusätzliche Provider-Calls PASS;
- 0 zusätzliche Provider-Kosten PASS;
- 0 Strukturwrites PASS.

Realer Result-Replay nach Korrektur:
- 541 gespeicherte Depth-Gruppen geprüft;
- 2 davon bestätigen tatsächlich bisher PENDING fachlich definierte Artikelintents;
- 539 erzeugen keinen zusätzlichen Artikel;
- Batch-Summary danach: 0 Hub-Kandidaten / 1 Editorial-Thema / 5 Aggregation-Reviews / 3 Macro-Reviews / 7 Evidence-Required;
- ideale Leafs: 2;
- Zielbaum-Writes weiterhin 0.

## ERSTER OFFENER BLOCKER

`HD001_V2_BATCH001_V124_ZERO_COST_RECALC_PENDING`

Der kostenpflichtige DataForSEO-Teil ist abgeschlossen.
Offen ist nur die korrigierte Neuauswertung derselben bereits gespeicherten Daten.

## EXAKT EINE NEXT ACTION

HD-001 V1.12.4 in Hobby Depot installieren und einmal `Kategorien → V2-Hobbybewertung` öffnen.

Die Neuauswertung läuft beim Öffnen automatisch:
- 0 DataForSEO-Aufrufe;
- 0 neue Kosten;
- 0 Kategorien-/Zielbaum-Writes.

Danach das neu heruntergeladene Ergebnis-JSON prüfen.

Noch kein Zielbaum-Delta.
Noch kein Kategorien-Sync.
