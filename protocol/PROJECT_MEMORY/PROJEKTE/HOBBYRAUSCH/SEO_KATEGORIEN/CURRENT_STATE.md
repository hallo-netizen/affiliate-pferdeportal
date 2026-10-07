# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-07
STATUS: BATCH 001 REALER V1.12.1 OVERVIEW PASS / V1.12.2 DEPTH TIMEOUT LIVE ERKANNT / V1.12.3 RESUMABLE DEPTH LOKAL HARD PASS / 38-CALL-LAUF NOCH OFFEN / KEIN ZIELBAUM-WRITE

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

Verbindlich seit Regelversion 1.2:
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

## Technischer V1.12/V1.12.1/V1.12.2/V1.12.3-Stand

V1.12.0 bleibt die technische Zielbaum-Baseline.

V1.12.1 wurde real in Hobby Depot ausgeführt:
- Batch 001 = 16 Hobbys / 34 vorgeschlagene Leafs / 263 Artikelintents;
- 1 echter DataForSEO Keyword-Overview-Aufruf;
- Kosten 0.02472 USD;
- DataForSEO returned 106 / 263 exakte Keywords;
- 157 exakte Seeds blieben PENDING;
- 0 WordPress-Strukturwrites;
- Result SHA-256 `5857319ea29c2477159c9eddefe691e7a6e5fdb0d0c8161314f75b1474b51fe9`.

Wichtig:
`0 Hub-Kandidaten` aus diesem Zwischenresultat ist KEIN belastbares fachliches Negativergebnis.
Der Regelvertrag 1.2 verlangt nach der fachlichen Kandidatenbildung zusätzlich DataForSEO Suggestions/Ideas zur Tiefenprüfung und erst danach die endgültige Leaf-Zählung.

Realer Befund:
`HOBBY_MASTER_V2_BATCH_001_REAL_RESULT_20261007.md`

Maschinenlesbarer Follow-up-Plan:
`HOBBY_MASTER_V2_BATCH_001_DEPTH_PLAN_20261007.json`

V1.12.2 hat den fachlich richtigen 38-Call-Depth-Plan umgesetzt, aber alle 38 Calls in einem einzigen WordPress-Request ausgeführt. Das führte live zum Timeout.

Dafür wurde HD-001 V1.12.3 gebaut:
- derselbe gespeicherte V1.12.1-Ausgangsstand;
- dieselben 37 fachlich definierten Cluster;
- dieselben 37 Keyword-Ideas + 1 finaler Overview = 38 zusätzliche Calls;
- aber automatisch in kleinen Requests;
- maximal 2 Keyword-Ideas-Aufrufe pro HTTP-Request;
- finaler Overview immer in eigenem Request;
- Fortschritt nach JEDEM erfolgreichen kostenpflichtigen Call gespeichert;
- Seiten-/PHP-Timeout verliert bereits bezahlte Evidence nicht;
- Wiederaufruf setzt automatisch am gespeicherten Cursor fort;
- keine erneute Kostenbestätigung beim Fortsetzen;
- weiterhin 0 Strukturwrites.

Lokales V1.12.3-Artefakt:
`HD001_V1.12.3_V2_DATAFORSEO_RESUMABLE_TIMEOUTSAFE_HARDPASS.zip`

SHA-256:
`bcb33caa3f481661654460db21cc1d407eb020124e85ab5941094f89ce2827a3`

Prüfbericht:
`HD001_V1.12.3_FINAL_LOCAL_POSNEG_REPORT.txt`

Prüfbericht SHA-256:
`4b04319e0efc78d128af0d23141eff83751ed38256b9acdc81a8b9ef4977165e`

Fresh-Unpack:
- PHP 64/64 PASS;
- Legacy 270/270 PASS;
- V1.12 POS/NEG PASS;
- realer 908/844/841-Test PASS;
- V1.12.1 + V1.12.2 Regression PASS;
- kompletter 38-Call-Depth-Lauf in 20 begrenzten HTTP-Schritten PASS;
- simulierter Timeout nach einem bezahlten Call: Checkpoint bleibt erhalten PASS;
- Resume startet am gespeicherten Cursor PASS;
- 0 Strukturwrites PASS.

## ERSTER OFFENER BLOCKER

`HD001_V2_BATCH001_RESUMABLE_DEPTH_RUN_PENDING`

Der erste reale DataForSEO-Lauf ist abgeschlossen.
Er hat 106 von 263 exakten Seeds zurückgeliefert und damit die vorgesehene zweite Evidenzstufe ausgelöst.

Offen ist ausschließlich die read-only Tiefenprüfung der 37 noch offenen, fachlich bereits definierten Cluster.

## EXAKT EINE NEXT ACTION

HD-001 V1.12.3 in Hobby Depot installieren und die Tiefenprüfung EINMAL starten.

Danach arbeitet sie automatisch in kleinen gespeicherten Paketen weiter.
Bei Unterbrechung genügt Seite erneut öffnen; der gespeicherte Stand wird fortgesetzt.

Gesamtumfang bleibt unverändert:
- 37 Keyword-Ideas-Aufrufe;
- 1 abschließender Keyword-Overview;
- 38 zusätzliche DataForSEO-Aufrufe.

Danach das neue Ergebnis-JSON herunterladen und fachlich bewerten.

Noch kein Zielbaum-Delta.
Noch kein Kategorien-Sync.
Noch kein alter V1.12-Zielbaum-Refresh.
