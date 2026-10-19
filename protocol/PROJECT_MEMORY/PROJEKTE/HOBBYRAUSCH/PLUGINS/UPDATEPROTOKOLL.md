# HOBBYRAUSCH – PLUGINS – UPDATEPROTOKOLL

ROLLE: HISTORIE / WAS + WARUM + BELEGE, KEINE CURRENT-WAHRHEIT

Aktuelle Version, Live-Status, Blocker und NEXT ACTION ausschließlich aus der jeweiligen:
`PLUGIN_AKTEN/<PLUGIN-ID>/CURRENT.md`

## PU-20261001-001 – HD-001 Kategorie-Workflow

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

PLUGIN:
`Affiliate-Portal Kategorie-Workflow`

ART:
Eigenentwicklung / getrennte Hobby-Depot-Pluginlinie.

FACHBÜRO:
`SEO_KATEGORIEN`

VON / AUF:
Fehlerkette V1.9.1–V1.9.3 → V1.9.4.

WARUM:
Live-Deployment scheiterte im Readback beim Knoten `Techniken & Praxis`, weil WordPress Taxonomie-Namen mit `&` intern escaped speichert. Der Readback verglich zuvor Rohwert gegen Klartext.

ÄNDERUNG:
Readback normalisiert ausschließlich WordPress-Core-Termname-Escaping; echte semantische Namensabweichungen bleiben fail-closed.

ABHÄNGIGKEITEN / SCHNITTSTELLEN:
WordPress Taxonomie-Readback; kein Pferdeatelier-Runtimebezug.

ROLLBACK:
Vorherige Fehlversuche wurden automatisch erfolgreich zurückgerollt.

POSITIVTEST:
Exakter echter 7-CREATE-Buchbinden-Pfad inklusive Core-Escaping PASS.

NEGATIVTEST:
Falscher Name, doppelte Kodierung, falscher Slug/Parent/Meta bleiben BLOCKED; Rollback PASS.

REGRESSION:
Source 251/251 PASS; Fresh Installer 251/251 PASS; PHP Source 25/25; PHP Installer 17/17; Runtime-Parität 22/22.

LIVE-NACHWEIS:
V1.9.4 produktiver Deployment-Run: Schreiben + Readback PASS.

RELEASE:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.9.4_TERM_NAME_READBACK_FIX_HARD_PASS.zip`

INSTALLER SHA-256:
`85990b87f0ef35530b616df7716547cb20974d1c77ca21aa7b3e0edec723f249`

SOURCE SHA-256:
`12dcce406d842bd7b8a6cde5af6a54dff2a4bbff3e27528c04231898a8f02e01`

CURRENT:
`PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`

---

## PU-20261001-002 – HD-002 Hobby Depot SEO Themenengine

PLUGIN-ID:
`HD-002-TEXT-SEO`

PLUGIN:
`Hobby Depot SEO Themenengine`

ART:
Eigenentwicklung / eigenständige Hobby-Depot-Linie; Pferdeatelier-PSTE nur frühere Referenzbasis, keine Runtime-Abhängigkeit.

FACHBÜRO:
`TEXT_REDAKTION`

VON / AUF:
V0.1.1 → V0.1.4 über die belegten Zwischenstände V0.1.2 und V0.1.3.

WARUM:
- automatischer read-only Owner-Handoff aus deployed HD-001 nötig;
- gültiger `NOT_AVAILABLE`-Redaktionsplan wurde in 0.1.2 als fehlender Hash blockiert;
- 0.1.3 konnte den PHP-Worker fortsetzen, bewies aber den realen ersten Admin-Reentry nicht vollständig;
- 0.1.4 setzt exakt den bekannten recoverablen BLOCKED-State beim Öffnen der Übersicht serverseitig zurück auf RUNNING.

ABHÄNGIGKEITEN / SCHNITTSTELLEN:
Read-only Handoff aus HD-001; eigener HDTE-Speicher; keine Schreiboperation in HD-001.

POSITIVTEST:
Kompletter echter Pfad lokal:
deployed HD-001 → Owner-Sync → Baseline → Admin-Reentry → jeder Folgeschritt eigener Request → finale Freshness-Gates → COMPLETE.

Zusätzlich:
Legacy-Job ohne Planfeld, kompletter Neuablauf, 4-Themen-Stresslauf und vorhandener Redaktionsplan → COMPLETE.

NEGATIVTEST:
Malformed NOT_AVAILABLE, vorhandener echter Plan im falschen Recovery-State, Structure-Mismatch, falscher Fehler/Phase, fehlender echter Hash, manipulierte Stage, finale Strukturdrift, upstream nicht deployed → fail-closed.

REGRESSION / PAKET:
PHP Source 80/80 PASS; PHP Fresh Installer 80/80 PASS; Source↔Installer 135/135 byteidentisch.

LIVE-GRENZE:
V0.1.4 lokal vollständig abgenommen, live noch NICHT abgenommen. Live bleibt der gespeicherte Portalabgleich bis zum erfolgreichen Upgrade sichtbar bei `HDTE_CONTEXT_STAGE_PLAN_HASH_MISSING`.

RELEASE:
`HOBBY_DEPOT_SEO_THEMENENGINE_V0.1.4_SERVER_SIDE_RESUME_FULL_WORKFLOW_HARD_PASS.zip`

INSTALLER SHA-256:
`02d52e326cce990833fb6661885d3ba5e30ab6461af76e8b0a2ebdcc3b78c12d`

SOURCE SHA-256:
`0ec35019433040ef1ff0f1567a2252c78f763eaa59b6f342b24d98c749f32a72`

EVIDENCE:
`HDTE_V0.1.4_COMPLETE_WORKFLOW_POS_NEG_EVIDENCE.txt`

CURRENT:
`PLUGIN_AKTEN/HD-002-TEXT-SEO/CURRENT.md`


---

## PU-20261005-003 – HD-001 Portalweite Gesamtbaum-Engine V1.10.0 (Entwicklungsstand, kein Release)

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

PLUGIN:
`Affiliate-Portal Kategorie-Workflow`

ART:
Eigenentwicklung / Hobby-Depot-Linie.

FACHBÜRO:
`SEO_KATEGORIEN`

VON / AUF:
V1.9.9 live bestätigter Content-Pilot → V1.10.0 lokale portalweite Arbeitskopie.

WARUM:
Buchbinden war nur der technische Pilot. Das Ziel ist der vollständige Hobby-Depot-Kategorienbaum aus Konzept + echtem Hobbybestand + DataForSEO, inklusive acht Hauptwelten, Content, Magazin und HivePress.

ÄNDERUNG:
- portalweite Rohkandidaten-Discovery;
- bounded DataForSEO Overview-Batches;
- Core-Keyword/Synonym-Dedupe;
- canonical Seed-Auswahl;
- evidenzbasierte Weltzuordnung über per-Hobby Suggestions;
- exakt acht Konzeptwelten;
- variable Concept-Batches;
- getrennte Content-/Magazin-/HivePress-Stränge;
- Admin-Import/Resume;
- kein Publish während Discovery.

ABHÄNGIGKEITEN / SCHNITTSTELLEN:
Der bereits erfasste echte HD-002-Gesamtbestand soll ausschließlich read-only als Kandidatenquelle übernommen werden.
Keine Schreibverbindung zu HD-002.

POSITIVTEST:
270/270 Altregression; Portal Discovery; World Routing; Concept Auto World; Eight Worlds E2E; Portal Scale; Admin Portal; Portal Resume jeweils PASS.

NEGATIVTEST:
Portal Negative PASS; ambige Weltzuordnung und ungültige Portalprofile fail-closed.

SKALIERUNGSBELEG:
844 synthetische Kandidaten in 2 Overview-Batches; 34 Concept-Batches bei Größe 25.
Nur Maschinenbeweis, kein realer Hobbybestand.

OFFENER BLOCKER:
`HD001_V1100_REAL_HD002_INVENTORY_INPUT_NOT_BOUND`.

RELEASE:
KEIN RELEASE.
Kein Upload-/Deploymentkandidat vor vollständigem realem Gesamtbestand→DataForSEO→Gesamtbaum→Frontend Positiv-/Negativ-E2E.

ARTEFAKT:
Kein isoliertes V1.10.0 `CURRENT.zip` ersetzen, solange der vollständige reale E2E fehlt.

PACKAGING-HINWEIS:
Arbeitskopie-Header = 1.10.0; `README.txt` trägt noch 1.9.6 und ist vor einem späteren Release zu bereinigen.

CURRENT:
`PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`

---

## PU-20261007-004 – HD-001 V1.12.0 Target-Tree-Basis + V2-Fachfortschreibung

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

PLUGIN:
`Affiliate-Portal Kategorie-Workflow`

ART:
Eigenentwicklung / allgemeingültiger Workflow mit Projektprofil.

FACHBÜRO:
`SEO_KATEGORIEN`

VON / AUF:
V1.11.x dynamische Strukturentwicklung → V1.12.0 versionierter Target-Tree-Weg.

WARUM:
Die dynamische Strukturerfindung erzeugte fachlich falsche/instabile Ergebnisse, u. a. fehlendes Monetarisierungs-Gate, unzureichende Alias-/Dublettenbehandlung und unvollständige drei Säulen. V1.12 trennt fachlichen Zielbaum und technische Synchronisierung.

ÄNDERUNG:
- versioniertes Projektprofil;
- generischer CORE/EDITORIAL/DIRECTORY-Target-Tree;
- DataForSEO im neuen Weg nur für Keyword-/SEO-Anreicherung, nicht als Strukturautorität;
- globale Cross-Pillar-Ownership;
- Add/Rename/Move/Merge/Archive per Soll/Ist;
- stabile IDs;
- atomare Aktivierung nach Readback;
- Rollback;
- UNKNOWN/NONE bleibt redaktionell erhalten.

RELEASE-ARTEFAKT:
`HD001_V1.12.0_FIXED_THREE_PILLAR_TARGET_TREE_POSNEG_HARDPASS.zip`

SHA-256:
`f77f676ef4e8df8d44e3cf0d1e61b52883d402924cb8d14033c24dd6645c03d1`

POSITIVTEST:
- PHP 55/55;
- Legacy 270/270;
- Portal-Suiten PASS;
- realer 908/844-Lauf PASS;
- 420/420 physische Zielobjekte Readback;
- Idempotenz;
- Add/Rename/Move mit ID-Erhalt;
- Buchbinden-Pilot stabil.

NEGATIVTEST:
- Cross-Pillar Keyword-/Intent-Kannibalisierung BLOCKED;
- UNKNOWN→CORE ohne Regel BLOCKED;
- Verlust nicht monetarisierbarer Themen BLOCKED;
- Readback-Tamper → Rollback PASS.

LIVE-GRENZE:
V1.12.0 NICHT live abgenommen.

FACHFORTSCHREIBUNG NACH DEM TECHNISCHEN PASS:
HOBBY_MASTER V2 wurde vorgeschaltet. Große bekannte Hobbys werden als wirtschaftliche Anker integriert, Nischen bleiben als Longtail erhalten, Größen-/Rollenlogik entscheidet die Publikationsebene. Acht Welten bleiben Hauptstruktur und sind oberste CORE-Ebene. `Hobbywelten` ist nur View/Einstieg.

FOLGE:
Das im V1.12-ZIP enthaltene Hobby-Depot-Profil ist keine aktuelle Installationsfreigabe. Erst HOBBY_MASTER-V2-Bewertung → Zielbaum-Delta → erneuter kompletter POS/NEG-Test.

CURRENT:
`PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`


---

## PU-20261007-005 – HD-001 V2-Bewertungsgate vor Pluginfortschreibung

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

ART:
Fach-/Integrationsfortschreibung, KEINE Plugin-Codeänderung.

WARUM:
Die V2-Current verlangte bereits eine maschinenlesbare Masterbewertung, aber Auswahl, Fail-closed-Entscheidung und Research-Queue-Intake waren noch nicht eindeutig genug gebunden.

ÄNDERUNG:
- maschinenlesbarer Bewertungsvertrag angelegt;
- reproduzierbaren Batch 001 definiert und ausgeführt;
- 19er Research Queue separat durch Identitäts-/Intake-Prüfung geführt;
- erstes provisorisches Master-Intake-Delta für Fotografie vorbereitet;
- Plugin- und Deployment-Gate bleibt geschlossen.

BATCH-ERGEBNIS:
- 16 Kandidaten;
- 16/16 ID-Eindeutigkeit PASS;
- 4 aktuelle Alias-/Kanonikbindungen bestätigt;
- 12 semantische Identitäts-/Unterformprüfungen offen;
- 0 Zielbaum-Writes;
- 15 Fälle mit fehlender Evidenz;
- Buchbinden fachlich weiter HOBBY_HUB, V2-Gesamtabnahme dennoch offen.

NEUER BLOCKER:
`HD001_V2_BATCH001_EVIDENCE_INCOMPLETE_MASTER_NOT_ASSESSED`

PLUGIN-CODE:
UNVERÄNDERT V1.12.0.

LIVE:
UNVERÄNDERT kein V1.12-Live-PASS und kein Deploymentauftrag.

CURRENT:
`PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`


---

## PU-20261007-006 – HD-001 V2-Fachgate pro Leaf / DataForSEO-Abgleich vorbereitet

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

ART:
Fach-/Integrationsfortschreibung, KEINE Plugin-Codeänderung.

WARUM:
Die vollständige Konzeptnachprüfung zeigte, dass Batch 001 die Content Capacity noch zu grob betrachtete. Verbindlich ist die Prüfung jeder untersten Kategorie auf 5–12 distinct Artikelintents. Zusätzlich muss die Zusammenfassung kleiner valider Hobbys ausdrücklich unterstützt werden.

ÄNDERUNG AUSSERHALB DES PLUGIN-CODES:
- Bewertungsregeln auf V1.1 fortgeschrieben;
- per-Leaf-Capacity gebunden;
- Aggregation kleiner Themen ohne Identitätsverlust gebunden;
- fachliche Batch-001-Vorprüfung erzeugt;
- exakten DataForSEO-Request für Batch 001 vorbereitet;
- bestehenden Buchbinden-DataForSEO-Befund gegen V2 neu bewertet.

KORREKTUR ZU PU-20261007-005:
Buchbinden bleibt als bestehender Live-/Technikpilot erhalten.
Es ist aber NOCH KEIN endgültiger V2-HOBBY_HUB-PASS.
Reale vorhandene Evidence:
Einstieg 4 / Ausrüstung 5 / Material 3 / Techniken-Praxis 4 distinct Gruppen.

NEUER BLOCKER:
`HD001_V2_BATCH001_DATAFORSEO_LIVE_VALIDATION_PENDING`

PLUGIN-CODE:
UNVERÄNDERT V1.12.0.

LIVE:
UNVERÄNDERT kein V1.12-Live-PASS und kein Deploymentauftrag.

CURRENT:
`PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`


---

## PU-20261007-007 – HD-001 V1.12.1 read-only HOBBY_MASTER-V2-Bewertung

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

VON / AUF:
V1.12.0 Zielbaum-Baseline → V1.12.1 read-only Bewertungskandidat.

WARUM:
DataForSEO gehört bereits in den bestehenden WordPress-Pluginweg. Die neue HOBBY_MASTER-V2-Bewertung musste deshalb in HD-001 selbst eingebunden werden, ohne den fachlich überholten V1.12-Zielbaum zu schreiben.

KORREKTUR ZU PU-20261007-006:
Die dort notierte harte Staffel `13–15 Split / 16+ erforderlich` war eine Zwischeninterpretation und NICHT vom Konzept gedeckt.
Verbindlich ist:
- unter 4 zusammenlegen;
- 4 Grenzfall;
- 5–12 ideal;
- 13–14 oberhalb ideal, keine automatische Teilung;
- ab etwa 15 Teilung fachlich prüfen;
- Hobby-Hub typischerweise 3–6 Leafs; ab etwa 10 eigenständigen Unterbereichen Macro-/Split-Prüfung.

UMSETZUNG:
- WordPress-Unterseite `Kategorien → V2-Hobbybewertung`;
- Batch 001 eingebunden: 16 Hobbys / 34 vorgeschlagene Leafs / 263 Artikelintents;
- genau 1 DataForSEO Keyword-Overview-Aufruf geplant;
- DataForSEO dient nur Evidenz/Dedupe;
- Cross-Hobby-/Ownership-Overlap wird markiert;
- 0 Strukturwrites;
- Target-Tree-Autorun und manueller Target-Tree-Refresh in diesem Kandidaten deaktiviert.

ARTEFAKT:
`HD001_V1.12.1_HOBBY_MASTER_V2_READONLY_ASSESSMENT_HARDPASS.zip`

SHA-256:
`959bc80217aac9b90ac107e6b315908b084704d09777ae9be990c2825245d33d`

PRÜFBERICHT:
`HD001_V1.12.1_FINAL_LOCAL_POSNEG_REPORT.txt`
SHA-256:
`3f34f58d0d7d35d0ac290e2926ac706f5fd6ff84e5a314d6ecde554204c89ac2`

TEST:
- PHP 59/59 PASS;
- Legacy Regression 270/270 PASS;
- V1.12 POS/NEG PASS;
- realer 908/844/841-Lauf PASS;
- V1.12.1 Grenz-/Negativtests PASS;
- 0 Strukturwrites PASS.

LIVE-GRENZE:
Noch kein realer Hobby-Depot-DataForSEO-Batchlauf.
Kein Zielbaum-Deployment.

NEXT:
V1.12.1 in Hobby Depot installieren und Batch 001 real im WordPress-Backend ausführen.

CURRENT:
`PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`


---

## PU-20261007-008 – HD-001 V1.12.2 DataForSEO-Tiefenprüfung nach realem Batch 001

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

VON / AUF:
V1.12.1 initialer read-only Overview-Lauf → V1.12.2 read-only Tiefenprüfung.

REALER AUSGANGSBEFUND:
- 16 Hobbys / 34 Leafs / 263 Artikelintents;
- 1 echter Keyword-Overview;
- 106 / 263 exakte Keywords returned;
- 157 exakte Seeds PENDING;
- Kosten 0.02472 USD;
- 0 Strukturwrites;
- Result SHA-256 `5857319ea29c2477159c9eddefe691e7a6e5fdb0d0c8161314f75b1474b51fe9`.

FEHLER IN V1.12.1:
Der exakte Overview wurde technisch als vollständige Evidenzstufe behandelt.
Dadurch entstand `0 Hub-Kandidaten`, obwohl Regelvertrag 1.2 anschließend Suggestions/Ideas zur Tiefenprüfung verlangt.
Fehlende exakte Overview-Zeilen sind kein belastbarer Negativbeleg.

V1.12.2:
- verwendet den gespeicherten V1.12.1-Lauf weiter;
- wiederholt den bezahlten Gesamt-Overview nicht;
- 37 offene fachlich definierte Cluster;
- 37 Keyword-Ideas-Aufrufe;
- 1 abschließender gebündelter Keyword-Overview;
- exakt 38 zusätzliche Calls;
- max. 15 distinct Gruppen je Cluster;
- erneute Core-Keyword-Dedupe;
- erneute Batch-Ownership-Prüfung;
- 0 Strukturwrites.

ARTEFAKT:
`HD001_V1.12.2_V2_DATAFORSEO_DEPTH_READONLY_HARDPASS.zip`

SHA-256:
`233f3b5a71f6080d98e8748795cedb0b684c5e1a16407ec509919fa3d1f7e17f`

PRÜFBERICHT:
`HD001_V1.12.2_FINAL_LOCAL_POSNEG_REPORT.txt`

PRÜFBERICHT SHA-256:
`1e7197feb74e9b3a070a4201f79a0416f46dfef960fdab556d59f21c4cb55048`

TEST:
- Fresh PHP 62/62 PASS;
- Legacy 270/270 PASS;
- V1.12 POS/NEG PASS;
- realer 908/844/841-Test PASS;
- V1.12.1 Assessment Regression PASS;
- realer Batch-001-Result-Readback PASS;
- exakt 38 Follow-up-Calls im Preflight PASS;
- Provider-Ausfall fail-closed PASS;
- 0 Strukturwrites PASS.

NEXT:
V1.12.2 in Hobby Depot installieren und die angezeigte 38-Call-Tiefenprüfung ausführen.

CURRENT:
`PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`


---

## PU-20261007-009 – HD-001 V1.12.3 timeout-sichere resumable Tiefenprüfung

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

PROBLEM:
V1.12.2 führte die fachlich korrekten 38 zusätzlichen DataForSEO-Aufrufe in einem einzigen WordPress-Request aus.
Live kam es dadurch zum Timeout.

KORREKTUR:
V1.12.3 ändert NICHT das Konzept und NICHT den 38-Call-Plan.
Geändert wird ausschließlich die Ausführung:
- einmalige Kostenbestätigung;
- danach automatische AJAX-Fortsetzung;
- maximal 2 Keyword-Ideas-Aufrufe pro HTTP-Request;
- finaler Overview eigener Request;
- Checkpoint nach jedem erfolgreichen Paid Call;
- Timeout/Browserabbruch verliert keine bereits bezahlte Evidence;
- Reload setzt automatisch am gespeicherten Cursor fort;
- keine erneute Kostenbestätigung beim Resume;
- Providerfehler fail-closed;
- 0 Strukturwrites.

ARTEFAKT:
`HD001_V1.12.3_V2_DATAFORSEO_RESUMABLE_TIMEOUTSAFE_HARDPASS.zip`
SHA-256:
`bcb33caa3f481661654460db21cc1d407eb020124e85ab5941094f89ce2827a3`

PRÜFBERICHT:
`HD001_V1.12.3_FINAL_LOCAL_POSNEG_REPORT.txt`
SHA-256:
`4b04319e0efc78d128af0d23141eff83751ed38256b9acdc81a8b9ef4977165e`

TEST:
- PHP 64/64 PASS;
- Legacy 270/270 PASS;
- V1.12 POS/NEG PASS;
- realer 908/844/841-Test PASS;
- V1.12.1/V1.12.2 Regression PASS;
- 38 Calls in 20 begrenzten HTTP-Schritten PASS;
- Timeout-Checkpoint + Resume PASS;
- 0 Strukturwrites PASS.

NEXT:
V1.12.3 installieren und die Tiefenprüfung einmal starten.


---

## PU-20261007-010 – HD-001 V1.12.4 Zero-Cost-Relevanz-Neuauswertung

PROBLEM:
V1.12.3 zählte rohe Keyword-Ideas-Gruppen als zusätzliche Artikelintents. Dadurch konnten fachfremde Treffer die Content-Capacity aufblasen.

KORREKTUR:
- Fachlogik definiert die Artikelintents.
- DataForSEO-Rohzeilen dürfen nur bereits definierte PENDING-Intents bestätigen.
- Provider-Zeilen erzeugen keine neuen Artikel.
- Bestehende V1.12.3-Daten werden automatisch neu ausgewertet.
- 0 neue DataForSEO-Aufrufe.
- 0 neue Kosten.
- 0 Strukturwrites.

ARTEFAKT:
`HD001_V1.12.4_V2_RELEVANCE_RECALC_ZERO_COST_HARDPASS.zip`
SHA-256:
`5ceffaa03eda90b45a235cf844ff2ddae3bef553f2a61f4ec32ea38eefcf75f6`

TEST:
PHP 66/66 PASS; Legacy 270/270 PASS; Fremdkeyword-Test PASS; realer Result-Replay PASS; 0 neue Calls/Kosten/Writes PASS.


---

## PU-20261007-011 – HD-001 V1.12.5 KISS Content Capacity / kein automatischer Depth-Weg

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

PROBLEM:
Die Fehlerkette V1.12.1–V1.12.4 band Content Capacity weiterhin zu stark an einzelne DataForSEO-Longtail-Treffer bzw. an Keyword-Ideas-Tiefendaten.

ROOT CAUSE:
Content Capacity und SEO-Evidenz wurden vermischt.

KORREKTUR:
- Fachlogik definiert und zählt eigenständige Artikelintents pro unterster Kategorie.
- DataForSEO reichert diese Intents an.
- Exaktes Core-Keyword-/Synonym-Evidence darf Dubletten zusammenführen.
- Eine fehlende exakte DataForSEO-Zeile löscht keinen fachlich eigenständigen Intent.
- Keyword-Ideas-/Suggestions-Rohzeilen erzeugen keine neuen Artikel.
- automatische Depth-Recherche ist im Normalweg deaktiviert.
- bestehende reale DataForSEO-Evidence wird kostenlos neu ausgewertet.

ARTEFAKT:
`HD001_V1.12.5_KISS_CONTENT_CAPACITY_ZERO_DEPTH_HARDPASS.zip`

SHA-256:
`68d521a9835bcbf2b2658dd0bd8d0a5163e6e1d656bf51855e20f830958a7af9`

PRÜFBERICHT:
`HD001_V1.12.5_FINAL_LOCAL_POSNEG_REPORT.txt`

SHA-256:
`8a6768b4222dd086f3ff124579684feeed6f11f45f268d5596631de326002075`

REAL-RESULT-REPLAY:
- 16 Kandidaten;
- 34 ideale Leafs;
- 1 HOBBY_HUB_CANDIDATE;
- 1 EDITORIAL_TOPIC_CANDIDATE;
- 5 AGGREGATION_REVIEW;
- 3 MACRO_REVIEW;
- 6 EVIDENCE_REQUIRED;
- 0 Zielbaum-Writes.

TEST:
- PHP Source 68/68 PASS;
- Legacy 270/270 PASS;
- V1.12 POS/NEG PASS;
- realer 908/844/841-Test PASS;
- V1.12.1 Regression PASS;
- echter V1.12.3-Result-Replay PASS;
- Missing-Provider-Row-Negativtest PASS;
- Exact-Core-Keyword-Dedupe PASS;
- automatische Depth-Recherche 0 Calls PASS;
- 0 neue Kosten PASS;
- 0 Strukturwrites PASS;
- Recalc idempotent PASS;
- Fresh Release PHP 31/31 PASS.

NEXT:
Genau ein realer WordPress-Readback mit V1.12.5. Keine weitere DataForSEO-Recherche.


---

## PU-20261007-012 – HD-001 V1.12.6 stale Export fail-closed

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

REALER BEFUND:
Der nach V1.12.5 hochgeladene Download war bytegleich mit dem alten V1.12.3-Ergebnis:
`086456f70d8896c51a97a27f7dcdc29906ad90534f9322aa6f1f5a7b519d69ae`.

ROOT CAUSE:
V1.12.5 recalculierte Altresultate nur beim Rendern der Adminseite. Der Download-Handler selbst exportierte `last_result()` ohne Recalc.

FIX:
V1.12.6 recalculiert vor jedem Export fail-closed, falls die KISS-Neuberechnung noch nicht gespeichert ist.

SICHERHEIT:
- 0 Provider-Aufrufe;
- 0 neue Provider-Kosten;
- 0 Strukturwrites;
- Recalc-Fehler blockiert den Download statt stale JSON auszugeben.

ARTEFAKT:
`HD001_V1.12.6_STALE_EXPORT_FAILCLOSED_HARDPASS.zip`

SHA-256:
`788b49529216555cba8cd74aae2a3a469f5f386e7ea2dc3d0449555910d55dca`

TEST:
- PHP 31/31 PASS;
- ZIP PASS;
- exakte reale stale Datei direkt über Download-Handler → 34 ideale Leafs / 1 Hub-Kandidat PASS;
- idempotenter zweiter Export PASS;
- fehlendes Ergebnis BLOCKED PASS.

NEXT:
Ein realer Export-Readback mit V1.12.6.

## PU-20261008-013 – HD-001 V1.13.1 praktischer Finalzielbaum / ein Sync

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

VON / AUF:
V1.12.6 read-only Kalibrierung → V1.13.1 manual-only Finalisierung.

WARUM:
Die 16er-Batchserie war als Produktionsweg unpraktikabel. Zusätzlich zeigte die Abschlussprüfung, dass der erste praktische Zielprofilentwurf die acht Hauptwelten noch fälschlich unter `Hobbywelten` führte.

VERBINDLICHE KORREKTUR:
- 841er Master = Inventar, nicht 841 Pflichtkategorien;
- 340 CORE / 501 Finder-Editorial;
- acht Hauptwelten = physische CORE-Rootseiten;
- Hobbywelten = View/Übersicht, kein Parent;
- Leafs nicht vorab erzwingen;
- Batch 004+ gestrichen;
- DataForSEO nicht mehr als flächendeckende Bewertungsserie.

ARTEFAKT:
`HD001_V1.13.1_PRACTICAL_FINAL_TARGET_ONE_SYNC_HARDPASS.zip`

SHA-256:
`94dca6cfc6c792cf2b866fc76fef1bff12551f9b375b38a1a511a91876b1a7b5`

ZIELPROFIL:
`HD001_V1.13.1_PRACTICAL_TARGET_PROFILE_20261008.json`
SHA-256:
`f5c6d9e5be7ee6184c50ded9db40549f4b1e2d2a8c29672f4eb7aa172ea8e014`

FINAL:
- 440 aufgelöste Logikknoten;
- 431 physische Zielobjekte;
- 404 Pages;
- 8 Welt-Roots;
- 8 Hobbywelten-Relations.

SICHERHEIT:
- manual-only;
- Dry-Run 0 Provider-Calls / 0 Writes;
- Apply nur mit unverändertem Dry-Run-Fingerprint;
- Live-Drift blockiert;
- Retirement nur für echte Target-Bindings;
- Legacy-Content bleibt erhalten.

TEST:
270/270 Regression PASS;
24/24 Final-Target PASS;
11/11 Baseline-Migration PASS;
33/33 Release-PHP PASS.

LIVE-GRENZE:
Noch kein Live-Sync.
NEXT = genau ein realer read-only Live-Dry-Run.

## PU-20261008-014 – V1.13.1 echter Live-Dry-Run zeigt alten Rollback-Restzustand

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

REALER DRY-RUN:
PASS / 841 Inventar / 340 CORE / 501 Finder-Editorial / 431 Zielobjekte / 12 CREATE / 419 UPDATE / 1 ARCHIVE / 0 Provider-Calls / 0 Writes.

WICHTIGER RESTBEFUND:
Im selben Readback ist ein historischer V1.12-Zielbaumlauf noch `ROLLBACK_PENDING`.

DETAIL:
- Revision `HD-TARGET-3P-V1-20261007+313e8ac433c0b154`;
- 620 Rollback-Aktionen offen;
- alter Readbackfehler `directory:events-reisen [name]`;
- Runner RUNNING / EXISTING_TARGET_TREE_RESUME;
- kein aktiver finaler Snapshot.

SICHERHEIT:
V1.13.1 bietet während des laufenden Rollbacks keinen Final-Apply an.
Die Finaler-Zielbaum-Seite setzt den Rollback automatisch bounded fort.
Nach terminalem Rollback ist ein neuer Dry-Run zwingend, da sich der Live-Fingerprint geändert hat.
Apply besitzt zusätzlich einen frischen Fingerprint-Recheck.

NEXT:
Finaler-Zielbaum-Seite offen lassen bis Rollback terminal → neuer Dry-Run → neuer JSON-Readback.
Noch kein Sync.


---

## PU-20261008-015 – HD-001 V1.14.0 Struktur / Target-Navigation / Magazin

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

VON / AUF:
V1.13.4 fachlich nicht final → V1.14.0 lokal vollständig geprüfter Struktur-/Navigations-/Magazin-Kandidat.

WARUM:
Die Frontend-Sichtprüfung von V1.13.4 zeigte trotz technischem Sync-PASS fachliche Portalfehler:
- Header mischte Legacy-Seiten mit dem kanonischen Target;
- Editorial-Themen konnten sichtbar in CORE leaken;
- Treibholz/Treibholz sammeln erschien als Legacy-Dublette;
- Magazin-Navigation wurde nicht vollständig projiziert;
- mehrere fachlich getrennte Zwischenbereiche waren zusammengezogen.

KORREKTUR:
- Header ausschließlich aus aktivem Target-Snapshot;
- ungebundene Legacy-Seiten aus kanonischer Navigation ausgeschlossen;
- Treibholz/Treibholz sammeln bleibt eine bestätigte Editorial-Identität;
- feste Magazin-Navigation vollständig;
- fachliche Splits u. a. Schrift/Lettering vs Papierkunst, Metall vs Schmuck, Leder vs Textil, Elektronik vs Funk, Smart Home, Moos/Miniaturgärten, Ameisen/Insekten vs Wirbellose;
- keine leeren Symmetrieäste;
- 841 Identitäten / 340 CORE / 501 Finder-Editorial erhalten.

ARTEFAKT:
`HD001_V1.14.0_STRUCTURE_NAV_MAGAZIN_FULL_POSNEG_HARDPASS.zip`

SHA-256:
`87246ecd24b1facc5c3b80c0e3593b2a0bd9391143ef6f190d6786ecfa62cda3`

ZIELPROFIL SHA-256:
`6dda22c63fb23593b2eee8d8fbc067e9f732430cad70d5c0576bca40b95a474c`

LOKALER ZIELSTAND:
- 59 aktive Zwischenbereiche;
- 446 Logikknoten;
- 437 physische Zielobjekte;
- 410 Pages;
- 96 Header-Navigationseinträge.

POSITIV:
- Fresh-ZIP 362 CREATE + 75 ADOPT;
- 437/437 Readback COMPLETE;
- 410/410 Page-Frontend PASS;
- Header-Navigation PASS;
- Magazin-Navigation PASS;
- zweiter Lauf 437 UNCHANGED.

MIGRATION V1.13.4:
12 CREATE + 425 UPDATE + 5 ARCHIVE → COMPLETE → 437 UNCHANGED.
Archiviert werden nur fünf ersetzte kombinierte Strukturknoten; keine Hobbyseite.

NEGATIV:
Readback-/Page-/Term-Fehlerrollback, Ambiguity, Foreign-Slug, Invalid-Profile, Missing-Taxonomy = PASS/fail-closed.

OFFEN:
19 bekannte/große Expansion-/Ankerkandidaten sind weiterhin nur Research Queue und nicht final nach Regeln 1.5 bewertet.
Keine Blind-Promotion und kein Live-Sync.

NEXT:
19 Expansion-Anker final bewerten → begründetes Delta binden oder bewusst Editorial/Finder/Out-of-scope schließen → vollständigen lokalen POS/NEG-E2E des daraus finalen Kandidaten → erst dann Live-Dry-Run.


---

## PU-20261008-016 – HD-001 V1.14.1 Expansion19 finaler Zielstand

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

VON / AUF:
V1.14.0 / 841 Identitäten / 340 CORE → V1.14.1 / 860 Identitäten / 359 CORE.

WARUM:
Die 19 bekannten/großen Expansion-Anker wurden nach Regeln 1.5 final bewertet und mussten ohne Blind-Promotion in Master und Zielprofil gebunden werden.

FACHLICH:
- 19/19 IN_SCOPE;
- 12 HOBBY_HUB;
- 7 ORIENTATION_UNIVERSE;
- Monetarisierung aller 19 bleibt UNKNOWN bis zu echtem Provider-Match;
- keine Rolle aus Monetarisierung abgeleitet;
- keine globale Content-Kategorieebene erzeugt.

STRUKTUR:
- 60 aktive Zwischenbereiche;
- `Essbare Pflanzen` wird durch `Gemüseanbau` real belegt und deshalb aktiviert;
- `Heimwerken` und `Gärtnern` bleiben direkte Welt-Kinder ohne künstlichen Zwischenbereich;
- direkte Hobbyseiten werden nicht als Zwischenbereich im Header gezeigt.

TECHNISCHE KORREKTUR:
- Research-/Expansion-Kandidaten können deterministisch zusätzlich zum Rohinventar gebunden werden;
- UNKNOWN-Monetarisierung darf eine fachlich begründete CORE-Rolle nicht blockieren, solange Editorial-Erhalt vorhanden ist;
- falsche DIRECT/ASSISTED-Behauptung ohne Monetarisierungspfad bleibt fail-closed;
- starre 841-Zählannahmen aus Dry-Run/Admin entfernt.

LOKALER ZIELSTAND:
- 860 Identitäten;
- 359 CORE / 501 Finder-Editorial;
- 60 aktive Zwischenbereiche;
- 466 aktive Logikknoten;
- 457 physische Ziele;
- 430 Pages;
- 97 Header-Einträge.

POSITIV:
- Fresh Dry-Run 457 CREATE / 0 Provider / 0 Writes;
- Fresh Sync 457/457 COMPLETE;
- zweiter identischer Sync 457 UNCHANGED;
- Migration V1.14.0 → V1.14.1: 20 CREATE + 437 UPDATE + 0 ARCHIVE / COMPLETE;
- danach 457 UNCHANGED;
- 430/430 Page-Frontend PASS;
- Header 97/97, Hubs, Front, Footer, Final-Readback PASS.

NEGATIV:
Readback-/Page-/Term-Rollback, Ambiguity, Foreign-Slug, Missing-Taxonomy, Duplicate-Slug, Monetarisierungs-Falschbehauptung, fehlende Editorial-Sicherung und Blind-Promotion = PASS/fail-closed.

ARTEFAKT:
`HD001_V1.14.1_EXPANSION19_FINAL_POSNEG_HARDPASS.zip`

SHA-256:
`64735c31f474a782cc324c68218aade99ccfca4b54ab08091d5f28cfcecae95e`

PROFIL SHA-256:
`cd40cee8f1bceffae7c41b8bf2124965d49046caa2e27242af2122168a8412d0`

MASTER SHA-256:
`adf01a7ac9ae8a30813e9d27391d0732583671dd6c39b5cca19d33576dd8308f`

EVIDENCE:
`SEO_KATEGORIEN/HD001_V1_14_1_EXPANSION19_FULL_LOCAL_HARDPASS_20261008.json`

NEXT:
Exaktes V1.14.1-Artefakt → ein read-only Live-Dry-Run → JSON-Readback prüfen.
Kein Sync vorher.


---

## PU-20261008-017 – HD-001 V1.14.1 Live-Dry-Run PASS

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

ERGEBNIS:
- PASS / valid=true;
- 860 Identitäten;
- 359 CORE / 501 Finder-Editorial;
- 457 physische Zielobjekte;
- Live-Delta: 32 CREATE + 425 UPDATE + 5 ARCHIVE;
- 0 ADOPT;
- 0 Provider-Aufrufe;
- 0 WordPress-Writes im Dry-Run.

ARCHIVE:
Nur die fünf bekannten ersetzten Kombi-Zwischenknoten:
- Elektronik & Funk;
- Insekten & Wirbellose;
- Leder & Textil;
- Metall & Schmuck;
- Schrift & Papier.

Keine Hobbyseite wird archiviert.

INTERPRETATION:
Der produktive Bestand steht vor dem Sync noch auf dem alten V1.13.4-Zielstand. Daher enthält der Dry-Run zugleich die bekannte V1.14.0-Strukturmigration und das V1.14.1-Expansion19-Delta.

NEXT:
Geprüften Zielbaum genau einmal synchronisieren → post-sync JSON-Readback prüfen → erst danach Live-PASS.


---

## PU-20261008-018 – HD-001 V1.14.2 Stale-COMPLETE UI-Gate Fix

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

BEFUND:
Der reale Live-Dry-Run von V1.14.1 war PASS, aber die Finaler-Zielbaum-Seite zeigte keinen Apply-Button.

URSACHE:
Die UI behandelte jeden gespeicherten Target-Sync mit `status=COMPLETE` als Abschluss des aktuellen Zielstands.
Der gespeicherte COMPLETE-State gehörte tatsächlich zur alten Revision V1.13.1/V1.13.4.
Dadurch wurde Abschnitt 2 trotz gültigem neuem V1.14.1-Dry-Run ausgeblendet.

FIX:
V1.14.2 vergleicht zusätzlich die Revision:
`state.revision === plan.profile_revision`.
Nur dann gilt der aktuelle Zielstand als COMPLETE.

SICHERHEIT:
- Target-Profil byteidentisch zu V1.14.1;
- Hobby-Master byteidentisch zu V1.14.1;
- Apply führt vor Writes weiterhin frischen Dry-Run + Fingerprint-Recheck aus;
- PHP 33/33 PASS;
- ZIP-Integrität PASS;
- Gate-Simulation: stale COMPLETE => Apply sichtbar; current COMPLETE => Apply verborgen; RUNNING => Apply verborgen.

ARTEFAKT:
`HD001_V1.14.2_STALE_COMPLETE_UI_GATE_FIX.zip`

SHA-256:
`b5bf0f6201a8158dc968530009d22195e8cc4a27b5421d84010840dafd282dbe`

NEXT:
V1.14.2 installieren → Delta-Dry-Run einmal neu → nur bei 32 CREATE / 425 UPDATE / 5 ARCHIVE und sichtbarem Abschnitt 2 einmal synchronisieren.


---

## PU-20261008-019 – HD-001 V1.14.3 Rule16 Visible Full Local Hard Pass

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

GRUND:
Nach Abschluss des fachlichen Rule-1.6-Zielbaums wurden im technischen Hard-Test vier konkrete Abweichungen gefunden und ursächlich korrigiert:
- Profil-Endzählungen mussten nach 5 Alias-Zusammenführungen / 22 Demotionen auf 855 kanonische Identitäten und 332 finale CORE-Identitäten gebunden werden;
- 28 bestehende Hobbyseiten benötigten legacy_ids für identitätserhaltende Migration statt CREATE+ARCHIVE;
- Dry-Run durfte diese physisch bereits beanspruchten Legacy-Objekte nicht zusätzlich als ARCHIVE zählen;
- bereits archivierte Target-Objekte durften im Folgelauf nicht erneut beschrieben werden.

ERGEBNIS:
- 1.723 physische Zielobjekte;
- 408 Pages;
- 1.292 category;
- 15 journal_cat;
- 8 hp_listing_category;
- 9 Relations;
- 279/279 HOBBY_HUBs mit sichtbarer Content-Kategorieebene;
- Migration gegen V1.14.1-Profil: 1.293 CREATE + 430 UPDATE + 27 ARCHIVE;
- Sync COMPLETE / Readback 1.723/1.723;
- zweiter Dry-Run 1.723 UNCHANGED / 0 ARCHIVE;
- zweiter Sync 1.723 UNCHANGED / 0 ARCHIVE / 0 Writes;
- Frontend PASS;
- Negativsuite PASS;
- PHP 33/33 PASS;
- 0 Provider;
- 0 WordPress-Writes in der lokalen Prüfung.

ARTEFAKT:
`HD001_V1.14.3_RULE16_VISIBLE_FINAL_HARDPASS.zip`

SHA-256:
`deaee48b4f7310d94a5975b3dd471b0374d369745b1b7dd48c512ae514d7c7de`

PROFIL SHA-256:
`6578a1aa4dccf554bb685a36e564c32af897c85bb1aac06d0401c5fc683622b6`

EVIDENCE:
`SEO_KATEGORIEN/HD001_V1_14_3_RULE16_VISIBLE_FULL_LOCAL_HARDPASS_20261008.json`

NEXT:
V1.14.3 installieren → genau einen read-only Live-Dry-Run → JSON-Readback prüfen.
Kein Sync vorher.


---

## PU-20261008-020 – HD-001 Abschluss-/Frischecheck V1.14.3

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

ART:
Dokumentations-/Autoritätsabgleich nach Abschlussprüfung. Keine Plugin-Codeänderung, keine neue Version, keine WordPress-Änderung.

ANLASS:
Der Abschluss-/Nachholcheck zeigte vier veraltete oder missverständliche Dokumentationsstellen, obwohl die SEO-Kategorien-Current bereits korrekt auf V1.14.3 / Live-Dry-Run pending stand.

NACHGEHOLT:
- Konzept-Current: veraltetes `TECHNICAL_OBJECT_PLAN_PENDING` beendet; operative Fortsetzung eindeutig an `SEO_KATEGORIEN/CURRENT_STATE.md` geroutet;
- zentrales Fehlerregister: HD-001-Wegweiser von V1.14.1 auf V1.14.3 / Live-Dry-Run pending aktualisiert;
- Plugin-Current: alte V1.12.0-/V1.13.1-Blöcke ausdrücklich als historisch markiert;
- isoliertes Manifest: V1.14.3-Artefakt, V1.14.3-Zielprofil, 1.723 Zielobjekte, 1.292 Content-Kategorien und lokale Hard-Pass-Evidence korrekt nachgezogen.

UNVERÄNDERT:
- Zielvertrag 2.6;
- Assessment Rules 1.6;
- Fach-Sollprofil;
- Plugin-Binary V1.14.3;
- SHA-256 des ZIP: `deaee48b4f7310d94a5975b3dd471b0374d369745b1b7dd48c512ae514d7c7de`;
- erster offener Blocker: `HD001_V1_14_3_LIVE_DRYRUN_PENDING`;
- exakt eine NEXT ACTION: V1.14.3 installieren und genau einen read-only Live-Dry-Run ausführen; kein Sync vorher.

ERGEBNIS:
Dokumentations-/Autoritätsabgleich PASS. Keine zweite aktuelle Statuswahrheit für den operativen SEO-/Kategoriepfad.


---

## PU-20261009-021 – HD-001 V1.14.3 Live-Dry-Run PASS / One Live Sync Released

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

ART:
Live-read-only Abgleich + Abschluss-/Frischecheck. Keine Plugin-Codeänderung, keine neue Version, keine WordPress-Schreibaktion.

LIVE-EVIDENCE:
`SEO_KATEGORIEN/HD001_V1_14_3_LIVE_DRYRUN_PASS_20261009.json`

ERGEBNIS:
- Plugin 1.14.3;
- Live-Dry-Run PASS / valid=true;
- 855 kanonische Identitäten;
- 332 CORE;
- 523 Editorial/Finder;
- 1.737 Logikknoten;
- 1.723 physische Zielobjekte;
- exakt 1.293 CREATE + 430 UPDATE + 27 ARCHIVE + 0 ADOPT;
- 22 Archive = EDITORIAL_TOPIC;
- 5 Archive = ALIAS_ONLY;
- 0 unerwartete HOBBY_HUB-Archive;
- 0 Provider-Aufrufe;
- 0 WordPress-Writes;
- Live-Delta entspricht exakt dem lokalen V1.14.3-Hard-Pass.

PRE-SYNC-HINWEIS:
Der im Export enthaltene Frontend-/Sync-Readback gehört noch zum alten V1.14.1-Livezustand mit 457 Zielobjekten. Der Headerfehler ist deshalb PRE-SYNC-Evidence und kein V1.14.3-Post-Sync-Fehler.

NACHHOLCHECK:
- Fehlerregister auf LIVE-SYNC PENDING aktualisiert;
- Konzept-Current von veraltetem TECHNICAL_OBJECT_PLAN_PENDING bereinigt;
- Zielvertrag 2.6 und Assessment Rules 1.6 unverändert;
- keine Architektur-/Workflowänderung.

BLOCKER:
`HD001_V1_14_3_LIVE_SYNC_PENDING`

NEXT:
Den bereits akzeptierten V1.14.3-Zielbaum genau einmal live synchronisieren. Danach sofort Post-Sync-JSON herunterladen und 1.723/1.723 + Frontend/Header prüfen. Kein zweiter Lauf vor dieser Prüfung.


---

## PU-20261009-022 – HD-001 Übergabe-/Single-Truth-Nachholcheck

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

ART:
Dokumentations-/Routingkorrektur vor Übergabe. Keine Plugin-Codeänderung, keine Versionserhöhung, keine WordPress-Schreibaktion.

BEFUND:
Die zuständige operative SEO-Kategorien-Current stand bereits korrekt auf V1.14.3 Live-Dry-Run PASS / ONE LIVE SYNC RELEASED / Post-Sync-Readback pending.
Die separate Konzept-Current enthielt jedoch noch den veralteten operativen Blocker `HD001_TECHNICAL_OBJECT_PLAN_PENDING`.

KORREKTUR:
- Konzept-Current auf abgeschlossenen Fach-/Regelstand 2.6/1.6 begrenzt;
- dynamische HD-001-Live-/Sync-Fortsetzung ausschließlich an `SEO_KATEGORIEN/CURRENT_STATE.md` geroutet;
- keine zweite operative Status-/Blocker-/NEXT-ACTION-Wahrheit mehr.

UNVERÄNDERT:
- Zielvertrag 2.6;
- Assessment Rules 1.6;
- Fach-Sollprofil;
- V1.14.3-Binary und SHA-256;
- Live-Dry-Run PASS;
- aktueller Blocker `HD001_V1_14_3_LIVE_SYNC_PENDING`;
- NEXT: akzeptierten V1.14.3-Zielbaum genau einmal live synchronisieren, dann Post-Sync-JSON prüfen.

ERGEBNIS:
Single-Truth-Nachholcheck PASS.


---

## PU-20261009-023 – HD-001 Konzept-Current Altstände entfernt

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

ART:
Single-Truth-Nachholkorrektur vor Übergabe. Keine Plugin-Codeänderung, keine WordPress-Schreibaktion.

BEFUND:
In `KONZEPT/CURRENT_STATE.md` standen trotz korrekter finaler Fachsektion noch ältere Zwischenstandsblöcke mit `299 offen` bzw. `198 offen`.

KORREKTUR:
Diese überholten Zwischenstandsblöcke wurden entfernt.
Das Konzeptbüro hält nur noch den abgeschlossenen Fach-/Regelstand und routet operative HD-001-Livearbeit ausschließlich an `SEO_KATEGORIEN/CURRENT_STATE.md`.

ERGEBNIS:
Keine konkurrierende operative Current-/Blocker-/NEXT-ACTION-Wahrheit mehr.


---

## PU-20261009-024 – HD-001 Rule 2.7 Fail-Closed Final Candidate

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

ART:
Profil-/Zielbaumkorrektur auf unveränderter 1.14.8-Codebasis. Keine neue Pluginarchitektur.

VON / AUF:
1.14.8 + Rule-2.7-Komplettprofil 2148 Zielobjekte → 1.14.8 + Rule-2.7-Fail-Closed-Profil 2102 Zielobjekte.

WARUM:
Im Nachholcheck wurden 46 neu erzeugte `Ausrüstung & Kosten`-Leafs gefunden, deren Supporting Intents nur generische Templates waren. Nach Zielvertrag 2.7 darf ein optionaler Leaf nur bei >=3 eigenständigen sinnvollen Beitragsintentionen nach Ownership-Dedupe bestehen.

ÄNDERUNG:
- exakt `profiles/hobby-depot-v1.json` geändert;
- 46 unbelegte optionale `Ausrüstung & Kosten`-Leafs entfernt;
- bestehende sinnvolle Leafs unverändert;
- FAQ-/Einstiegsabdeckung erhalten;
- Technik 9 über `RC & Modelltechnik`;
- 12 Magazin-Kacheln erhalten;
- PHP-Code unverändert.

ARTEFAKT:
`HD001_V1.14.8_RULE27_FAILCLOSED_COMPLETE_ONE_SYNC_HARDPASS.zip`

SHA-256:
`0ae09fa5d75656416a0e4e7c1bb4fab74e01e776c2e36b13b8b6734a9efc5c0c`

POSITIV – FRISCH WIEDERHOLT:
- ZIP-Integrität PASS;
- PHP 33/33 PASS;
- Live-Baseline-Dry-Run PASS: 373 CREATE / 0 ADOPT / 1729 UPDATE / 6 ARCHIVE;
- Full Sync COMPLETE;
- 2102/2102 Readback;
- Frontend PASS;
- 279/279 HOBBY_HUBs PASS;
- Header PASS;
- zweiter Dry-Run 2102 UNCHANGED / 0 Delta.

NEGATIV / REUSE:
Der PHP-Code ist byteidentisch zum zuvor voll geprüften 1.14.8-/Rule-2.7-Kandidaten; Paketdiff zeigt ausschließlich das Zielprofil. Die bestehenden fail-closed Code-Negativtests werden deshalb wiederverwendet. Der neue Profile-Dry-Run selbst validiert Parent/Slug/Depth/Category-Unter-Category vor Writes.

LIVE:
Der derzeit sichtbare 2148er Dry-Run ist überholt und darf NICHT synchronisiert werden.

ROLLBACK:
Vor Live-Sync weiterhin Dry-Run + Fingerprint-Recheck + bounded Readback/Rollback.

NEXT:
Fail-closed ZIP installieren und genau einen neuen read-only Live-Dry-Run ausführen. Noch kein Sync.

ARTEFAKTPFLICHT:
`CURRENT.zip` im Campus bleibt NICHT synchronisiert; kein lokaler Binärdatei-Uploadweg im verfügbaren GitHub-Connector. Manifest wurde nachgezogen, Binary nicht erfunden.


---

## PU-20261009-025 – HD-001 finaler Rule-2.7-Live-PASS + optimierter Wiederverwendungsworkflow

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

ART:
Finale lokale Gesamtprüfung, produktiver One-Sync-Readback und Ableitung eines optimierten Workflows für neue Themen.

AUSGANGSPROBLEM:
Der Arbeitsstrang hatte zu viele Zwischenprofile/Pluginuploads erzeugt, weil fachliche Modellierung, lokale Abnahme und Live-Ausrollung zu früh vermischt wurden.

LETZTE FACHLICHE NACHHOLFEHLER:
- 279/279-HOBBY_HUB-Gate war zu eng; 51 weitere terminale CORE-Seiten blieben ohne Leafs;
- 46 generische Ausrüstung-&-Kosten-Leafs waren nicht mit >=3 hobbyindividuellen Intents belegt;
- PENDING/UNASSESSED-Rollen wurden zu lange mitgeschleppt;
- Hobbyfinder war nicht direkt Hauptkategorie; Alleine/Zu zweit lagen falsch, Gruppe fehlte;
- 22 stale Editorial-Verweise auf `editorial:group:entdecken`;
- altes 3–6-Leaf-Gate;
- AJAX-HTML-Fehler führte zu `Unexpected token '<'`;
- injizierter Metadaten-Write-Fehler zeigte einen unvollständigen Rollback.

FINALER LOKALER HARD-PASS:
- Kategorienbaum 43/43 PASS;
- 1920 CORE-Content-Kategorien;
- 330/330 terminale CORE-Seiten mit Content-Ebene;
- 255 neue Leafs jeweils >=3 Supporting Intents;
- positive + negative E2E 14/14 PASS;
- Resume, Readback, Idempotenz, Drift und exakter Rollback PASS;
- PHP 33/33 PASS;
- ZIP PASS.

ARTEFAKT:
`HD001_V1.14.8_RULE27_FINAL_VERIFIED_E2E_20261009.zip`

SHA-256:
`709134631895a901bcb4fc5f5d71889d317954d9928c0ed20700883990a5a52c`

LIVE:
- Dry-Run PASS / 2357 Ziele / 256 CREATE / 2101 UPDATE / 1 ARCHIVE;
- Sync COMPLETE / TARGET_TREE_SYNC_AND_READBACK_PASS;
- 256 created / 2100 updated / 1 unchanged / 1 archived;
- 2357/2357 Readback;
- Frontend PASS;
- 330/330 Kategorie-Gate;
- 0 failures;
- 0 unbound CORE pages.

OPTIMIERUNG FÜR NEUE THEMEN:
Erst vollständiger Zielvertrag + komplette fachliche Datenstruktur + vollständiger lokaler POS/NEG-E2E-Hard-Pass. Erst danach genau ein Release-ZIP, ein Live-Dry-Run, ein Sync und ein Readback. Keine Zwischen-ZIPs und keine Blindfix-Schleife.

WIEDERVERWENDBARE ÜBERGABE:
`../PROJEKTLEITUNG/HOBBYRAUSCH_UEBERGABE_OPTIMIERTER_WORKFLOW_NEUES_THEMA_20261009.md`

ERGEBNIS:
HD-001 LIVE-PASS / Kategorienlauf abgeschlossen.


---

## PU-20261011-026 – HD-003 Hobby Depot Design / Template Kit 1.50.601

PLUGIN-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

NAME:
`Affiliate Portal Template Kit – Hobby Depot Profil`

ART:
Projektbezogene Design-/Renderer-Weiterentwicklung auf bestehender Template-Kit-Basis. Keine Änderung an HD-001-Strukturautorität oder Affiliate-Providerlogik.

VON / AUF:
Hobby-Depot-Designkandidaten 1.50.593–1.50.600 → 1.50.601.

WARUM:
Die realen WordPress-Readbacks zeigten nacheinander Blogloop-Einbettung, Abweichungen vom freigegebenen Entwurf, unvollständige Startseitenbereiche, Hero-Responsive-Probleme, Mega-Menü-Hover-Lücke, zu kleine/unscharfe Weltbilder und fachlich unpassende Bildmotive.

THEME:
ListingHive ist die technische Theme-Basis der gesamten Hobby-Depot-Seite. Das Designplugin unterdrückt im Hobby-Depot-Rahmen einen zweiten sichtbaren Themeheader/-footer.

1.50.601 – SCOPE:
- Header/Topbar visual polish;
- 8 reale CORE-Welten;
- Mega-Menü pro Welt;
- stärkere Untermenü-Typografie;
- vollständiger Mittel-/Magazinbereich;
- kein TEST-Fallback;
- drei redaktionelle Mittelkarten;
- kontrollierte, unterschiedliche Weltassets;
- `Tiere` nicht als Hund/Pfote;
- Editorial-Karten ohne doppelte Weltfotos;
- Affiliate-Produkte/Banner/Mietflächen unverändert conditional.

POSITIV:
- 8/8 Welten;
- 3/3 Editorial-Karten;
- 5/5 reale Magazin-Themenseiten;
- Affiliate belegt sichtbar;
- 16 Responsive-Breiten 320–1600 px;
- Hero-CTAs sichtbar/innerhalb;
- Mega-Menü Trigger → Unterpunkt stabil;
- ListingHive-Shell-Unterdrückung;
- kein horizontaler Overflow.

NEGATIV:
- Affiliate leer vollständig abwesend;
- kein TEST-Fallback;
- kein Shop-/Community-/Newsletter-Noise;
- kein zweiter ListingHive-Header/Footer;
- Mega-Menü-Gap = 0 px.

FRESH:
- ZIP-Integrität PASS;
- PHP-Lint 9/9 PASS;
- SHA-256:
  `6b9fff2fa237d09d7cef2f31a2db7a50619d97cc6314a665265dbb08832dd952`.

ROLLBACK:
Kein Blindfix. Bei Liveabweichung erst realen Zustand reproduzieren und nur belegtes Delta reparieren; nötigenfalls auf zuletzt installierten funktionierenden Hobby-Depot-Template-Kit-Stand zurück.

LIVE:
OFFEN. Kein Live-PASS.

NEXT:
1.50.601 installieren und vollständige Startseite Desktop/Tablet/Mobile live prüfen. Erst danach Hub Ebene 1.


### NACHHOLUNG ARTEFAKTPFLICHT HD-003

Das geforderte `ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip` konnte in diesem Chat **nicht** in den GitHub-Campus geschrieben werden.

Grund:
Der verfügbare GitHub-Connector kann Repository-Text/Git-Objekte schreiben, besitzt aber keinen direkten Binärtransfer vom lokalen 8,9-MB-Sandbox-ZIP in einen GitHub-Blob. Eine manuelle Base64-Rekonstruktion über den Chat wird wegen Integritäts-/Größenrisiko nicht als belastbarer Weg verwendet.

Folge:
- kein falsches CURRENT.zip;
- MANIFEST vorhanden;
- SHA/Evidence vorhanden;
- Chat-Artefakt vorhanden;
- Plugin-Artefaktsynchronisierung bleibt formell BLOCKED bis ein belastbarer Binäruploadweg verfügbar ist.


---

## PU-20261011-027 – HD-003 Hobby Depot Design / Template Kit 1.50.610

PLUGIN-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

VON / AUF:
1.50.601 → 1.50.610.

WARUM:
Der reale Live-Readback 1.50.601 zeigte:
- Logo als Alt-Text statt Grafik;
- Hero-Bildschriftzug rechts abgeschnitten/nicht sauber responsiv;
- Header und Body optisch zu einheitlich;
- Startseite im Monetarisierungsbereich noch nicht vollständig;
- leere Affiliateplätze im eingeloggten Arbeitszustand unsichtbar;
- direkt verkaufbare Werbefläche brauchte eine eigene öffentliche Sichtbarkeitsregel;
- kleine Weltbilder weiterhin weich;
- Tiere-Motiv fachlich/gestalterisch unbrauchbar und mit dekorativem Rahmen.

ÄNDERUNG:
- Logo bleibt unverändert auf freigegebenem v150600-Asset.
- Topbar-Inhalt bleibt unverändert und mittig.
- Body weiß; Header warm-off-white; keine Anzeige im Header.
- Hero-Schriftzug bleibt im Bild, mit separatem Desktop-/Mobile-Safe-Crop.
- 8 Weltbilder komplett neu als native 1400×620-Quellen; Motive fachlich gegen die 8 realen Welten geprüft und hero-ready.
- Tiere neu: Aquaristik/Terraristik/Insekten/Futtertiere/Imkerei-Bezug, ohne Rahmen.
- Affiliate-Produkte/Banner öffentlich leer unsichtbar, eingeloggt leer als Arbeitsplatz sichtbar.
- Direkt verkaufbarer Werbeplatz maximal einmal pro Seite/Kategorie/Beitrag; unverkauft öffentlich „Werbeplatz verfügbar“, verkauft als Anzeige/Werbung.
- Breiter Affiliate-Banner im Content.
- Startseitenreihenfolge final: Hero → 8 Welten → Editorial → Banner → Magazin/Themen → Produkte → verkaufbarer Werbeplatz → Footer.
- KISS-Meta-Titel/Description-Schicht mit optionalem Override; kein zusätzliches SEO-Plugin nötig.

POSITIV:
- 8/8 Welten;
- 8/8 neue Weltmotive 1400×620, unterschiedliche Hashes;
- 3/3 Editorial-Karten;
- 5/5 Magazin-Themenseiten;
- eingeloggt 3 leere Produktplätze + 1 leerer Bannerplatz sichtbar;
- belegte Affiliate-Inhalte sichtbar;
- unverkaufter und gebuchter Direktwerbeplatz korrekt;
- Hero-Schriftzug Desktop/Mobile vorhanden;
- Logo/Topbar/Headerregeln PASS.

NEGATIV:
- öffentlich unbelegte Affiliate-Produkte/Banner abwesend;
- Direktwerbeplatz nicht doppelt;
- keine Anzeige im Header;
- kein TEST-Fallback;
- kein Shop-/Community-/Newsletter-Noise.

FRESH:
- ZIP-Integrität PASS;
- PHP 9/9 PASS;
- SHA-256:
  `c26ff929fa02a451dd4b7e7b9e6b2aa4dd42c2752bd261f13c134401389512a3`.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.610_HOBBY_DEPOT_HOMEPAGE_FINAL_LOCALPASS.zip`

LIVE:
OFFEN. Kein Live-PASS.

NEXT:
1.50.610 installieren und vollständige Startseite Desktop/Tablet/Mobile live prüfen. Erst danach Hub Ebene 1.


---

## PU-20261011-028 – HD-003 Hobby Depot Design / Template Kit 1.50.611

VON / AUF:
1.50.610 → 1.50.611.

WARUM:
Letzter visueller Startseiten-Feinschliff vor Hub Ebene 1.

ÄNDERUNG:
- linke Hero-Textfläche weiß;
- 1-px-Hero-Rahmen;
- 22 px Abstand zwischen Header und Hero auf Desktop, 14 px Mobile;
- Hauptnavigation Desktop 10 px nach unten auf optische Claim-Achse;
- Hero-Headline links: „Entdecke dein nächstes Hobby.“;
- eingebrannter Bildspruch bleibt unverändert.

TEST:
- PHP 9/9 PASS;
- ZIP-Integrität PASS;
- exakte Regelchecks PASS.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.611_HOBBY_DEPOT_HERO_HEADER_FINAL_LOCALPASS.zip`

SHA-256:
`3f5c74845c1264823a5ca70c09d90fdc0d2ec4815858f6bd9eb84a29f73b2668`

LIVE:
OFFEN.

NEXT:
1.50.611 installieren und Startseite Desktop/Tablet/Mobile live prüfen.


---

## PU-20261011-029 – HD-003 Hobby Depot Design / Template Kit 1.50.612

VON / AUF:
1.50.611 → 1.50.612.

WARUM:
1.50.611 war live sichtbar wirkungslos bzw. teilweise alt, obwohl Quelltextänderungen im ZIP vorhanden waren.

ROOT CAUSE:
- alte Hobby-Depot-Renderklasse/-datei v150610 wurde weiterverwendet;
- wesentliche Assetnamen/-pfade wurden wiederverwendet;
- Startseiten-Weltkarten durften alte große WordPress-Featured-Images vor den kontrollierten neuen Weltassets verwenden.

KORREKTUR:
- neue Renderklasse/-datei v150612;
- neues Fronttemplate v150612;
- neues Assetverzeichnis `assets/hobby-depot-v150612/`;
- neue Dateinamen plus `?ver=1.50.612`;
- alte Hobby-Depot-Renderdatei und altes Hobby-Assetverzeichnis aus dem Release entfernt;
- Startseiten-Weltkarten hart an die kontrollierten 1400×620-Assets gebunden;
- einmalige verfügbare Cache-Purge-Wege beim erkannten Releasewechsel im Backend;
- HTML-Releasemarker `data-hd-release="1.50.612"`.

SICHTBARER DESIGNSTAND:
- Headline: „Entdecke dein nächstes Hobby.“;
- Bildspruch bleibt „Mehr Zeit für das, was dich begeistert.“;
- Hero links weiß;
- 1 px Hero-Rahmen;
- 24 px Abstand oben Desktop / 14 px Mobile;
- Navigation Desktop physisch 10 px tiefer;
- Logo unveränderte Bildbytes, aber neuer cache-sicherer URL;
- Topbar-Inhalt unverändert.

BILDER:
8 neue kontrollierte Motive, je 1400×620:
Gestalten Frau, Fertigen Mann, Technik aktive Hände, Forschen Mann, Pflanzen Frau, Tiere andere Frau, Bewegen Mann, Sammeln aktive Hände.
Kein Motiv ohne mindestens Hände.

FRESH TEST:
- PHP 9/9 PASS;
- POS/NEG Render PASS;
- alte große Featured Images können Weltkarten nicht mehr überschreiben;
- 8/8 neue Assets gebunden;
- ZIP-Integrität PASS.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.612_HOBBY_DEPOT_REAL_FRONTEND_FIX_LOCALPASS.zip`

SHA-256:
`cb82af1fa9ab0aabb980fdcd903efe05e4bf75c10c036f108fb3450fec22fda3`

LIVE:
OFFEN.

NEXT:
1.50.612 installieren und Startseite live prüfen.


---

## PU-20261011-030 – HD-003 Hobby Depot Design / Template Kit 1.50.613

VON / AUF:
1.50.612 → 1.50.613.

WARUM:
Der Live-Readback war insgesamt deutlich verbessert, zeigte aber noch vier konkrete Punkte:
- Hauptnavigation weiterhin zu hoch;
- Hobbyfinder/Magazin/Wissen farblich nicht vollkommen einheitlich;
- direkt verkaufbarer Werbeplatz auf der Startseite nicht klar genug sichtbar;
- nächste Arbeitsebene soll direkt mit verbindlichem Breadcrumb-/Hub-/Monetarisierungstemplate beginnen.

ÄNDERUNG STARTSEITE:
- Desktopnavigation real weitere 14 px nach unten;
- Hobbyfinder, Magazin und Wissen & Glossar einheitlich `#f5f1e9`;
- genau ein öffentlich sichtbarer Direktwerbeplatz unmittelbar nach dieser Dreiergruppe;
- unverkauft mit „Hier könnte Ihre Werbung stehen.“ / „Werbeplatz verfügbar“;
- Affiliate-Banner/Produkte öffentlich leer weiterhin unsichtbar, eingeloggt als Arbeitsplätze sichtbar.

ÄNDERUNG HUB-/KATEGORIEPFAD:
- neues eigenes Contenttemplate;
- Breadcrumb auf jeder unterstützten Seite/Kategorie außer Startseite, immer auf derselben Achse;
- Titel-/Introbereich oben analog zum Portalprinzip;
- erste Welt-Hubs nutzen exakt dasselbe kontrollierte 1400×620-Weltasset wie die jeweilige Startseitenkarte;
- vorhandene direkte nächste Ebene vollständig als Kacheln;
- Affiliate-Banner;
- Beitragsvorschau;
- Affiliate-Produkte;
- maximal ein direkt verkaufbarer Werbeplatz.

UNTERSTÜTZTE CORE-TYPEN:
`hub1`, `hub2`, `category`, `leaf`; zusätzlich WordPress-Kategoriearchive und `journal_cat`.

FRESH TEST:
- PHP 10/10 PASS;
- ZIP-Integrität PASS;
- Homepage POS/NEG PASS;
- eingeloggt/öffentlich Affiliate PASS;
- Direktwerbeplatz count=1 PASS;
- Hub1 Breadcrumb/Hero/Kindebene/Banner/Beiträge/Produkte/Direktwerbung PASS;
- Kategorie Breadcrumb/Banner/Beiträge/Produkte/Direktwerbung PASS.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.613_HOBBY_DEPOT_HUB1_BREADCRUMB_MONETIZATION_LOCALPASS.zip`

SHA-256:
`56aa6f55542570d2383bd6fff92aaddcf155cf103cf14faccf80994636250d34`

LIVE:
OFFEN.

NEXT:
1.50.613 installieren und Startseite plus eine erste Welt-Hubseite live prüfen.


---

## PU-20261011-031 – HD-003 Hobby Depot Design / Template Kit 1.50.614

VON / AUF:
1.50.613 → 1.50.614.

WARUM:
Live-Readback 1.50.613 zeigte:
- Topbar noch nicht klar genug abgesetzt;
- Navigation weiter zu hoch;
- Hubtext sollte nach bewährtem Pferdeatelier-Prinzip integriert werden;
- bei ungeraden Unterkategorie-Anzahlen blieb optisch zu viel Leerfläche;
- Affiliateflächen wirkten zu technisch/getrennt;
- verkaufbarer Werbeplatz musste prominenter und verkaufsfähiger werden.

ÄNDERUNG:
- Topbar dunkel im Footer-Farbton, Inhalt unverändert.
- Navigation Desktop weiter nach unten.
- Pferdeatelier-Kategorietextprinzip übernommen:
  - manuelle Texte geschützt;
  - automatische Fallbacktexte aus Titel, Ebene, Parent/Children und Themenprofil;
  - ab ca. 130 Wörtern sichtbarer Lead ca. 55 Wörter;
  - Vertiefung unter „Mehr erfahren“;
  - „Was du hier findest“ bleibt sichtbar;
  - vollständiger Text im initialen HTML.
- Gestalten besitzt einen konkreten Referenz-/Beispieltext.
- Unterkategorie-Raster intern 6 Spalten:
  - normal 3 Karten;
  - Rest 2 = 50/50;
  - Rest 1 = volle letzte Reihe.
- Direktwerbung direkt nach Unterkategorien, mit Bildcollage, „Hier könnte Ihre Werbung stehen.“ und CTA „Werbemöglichkeiten & Preise“.
- Affiliate-Banner und Affiliate-Produkte optisch nativ in den Content integriert, weiterhin als Anzeige/Partner gekennzeichnet.

FRESH TEST:
- ZIP-Integrität PASS;
- PHP 10/10 PASS;
- Intro-Accordion/Integrität PASS;
- Rasterregeln PASS;
- Monetarisierungsreihenfolge PASS;
- Weltassets 8/8 1400×620;
- Logo byteidentisch zum Vorgänger.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.614_HOBBY_DEPOT_NATIVE_HUB_MONETIZATION_LOCALPASS.zip`

SHA-256:
`57c371a32a2cc4c84edbfef0819e017ca15fc5007f27a228180e44de8edbda58`

LIVE:
OFFEN.

NEXT:
1.50.614 installieren und Startseite + Gestalten live prüfen.


---

## PU-20261011-032 – HD-003 Hobby Depot Design / Template Kit 1.50.615

VON / AUF:
1.50.614 → 1.50.615.

WARUM:
Live-Readback zeigte bei mittlerer Fensterbreite eine rechts abgeschnittene Hauptnavigation. Zusätzlich sollen obere Hobby-Depot-Hubs visueller arbeiten als Pferdeatelier, ohne die tieferen Ebenen wieder zu überladen.

ÄNDERUNG NAVIGATION:
- vollständige 8-Welten-Zeile nur noch oberhalb 1320 px;
- 761–1320 px frühzeitiger Hamburger-/Dropdownmodus;
- 4-spaltig, unter 980 px 2-spaltig;
- Mobilepfad separat;
- keine horizontale Desktopzeile mehr, die rechts abgeschnitten werden kann.

ÄNDERUNG HUBKARTEN:
- Hub1 und Hub2 erhalten kompakte Fotos;
- echtes Child-Featured-Image gewinnt;
- fehlt es, wird ein kontrollierter Crop des zugehörigen 1400×620-Weltmotivs verwendet;
- tiefe Category-/Leafebenen bleiben ohne Bildzwang;
- kein neuer Medien-/Strukturworkflow.

FRESH TEST:
- PHP 10/10 PASS;
- ZIP-Integrität PASS;
- Breakpoint-/Hamburger-/Dropdown-CSS PASS;
- Featured-Image-Priorität PASS;
- Weltasset-Fallback PASS;
- tiefe Kategorie ohne Fotokarte PASS.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.615_HOBBY_DEPOT_PHOTO_HUB_RESPONSIVE_NAV_LOCALPASS.zip`

SHA-256:
`17d03f5704d8f140a86f4bbbdc4109cf564522a663660d0bd333be456dc3fda6`

LIVE:
OFFEN.

NEXT:
1.50.615 installieren und Startseite + Gestalten bei großer, mittlerer und mobiler Breite live prüfen.


---

## PU-20261011-033 – HD-003 Hobby Depot Design / Template Kit 1.50.616

VON / AUF:
1.50.615 → 1.50.616.

LIVE-BEFUND:
- Navigation zu tief und optisch an der Trennlinie;
- Verdacht auf veränderte Schriftgröße;
- Hub1 mit doppeltem sichtbarem Text;
- Gestalten-Unterkategorien mehrfach mit demselben Bild;
- Direktwerbung als 4er-Collage statt starkem Einzelmotiv.

KORREKTUR:
- Navigation Desktop 22 px → 8 px;
- Vollnavigation erst >1560 px;
- relevante Schriftgrößen gegen 1.50.614 geprüft: unverändert;
- Hub1-Zusatztext nur noch geschlossen unter „Mehr über <Welt> erfahren“;
- Gestalten 7 unterschiedliche Kategorie-Fallbackbilder;
- Parent-Weltbild-Fallback entfernt;
- Direktwerbung exakt 1 Foto;
- Text über dem Foto;
- Brushstroke hinter „Hier könnte Ihre Werbung stehen.“;
- CTA „Werbemöglichkeiten & Preise“.

TEST:
- PHP 10/10 PASS;
- ZIP PASS;
- 7/7 Bildhashes unterschiedlich;
- Parent-Fallback NEGATIV PASS;
- Rental <img> count = 1 PASS;
- Typography-Diff PASS.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.616_HOBBY_DEPOT_HUB_CLEANUP_AD_BRUSH_NAV_FIX_LOCALPASS.zip`

SHA-256:
`6ae738653de1dd1677bc4e6a5e58540cc7efddc6ccd5ddf8f28a2b5bbda5e0cd`

LIVE:
OFFEN.

NEXT:
1.50.616 installieren und Gestalten bei Desktop / Side-by-Side / Mobile prüfen.


---

## PU-20261011-034 – HD-003 1.50.617

LIVE-BEFUND 1.50.616:
Navigation auf Mid faktisch weg, Logo zu klein, Hub-Fold ohne saubere Absätze/mit Kastenwirkung, Druck & Fotografie ohne Bild, Bildformate uneinheitlich, 7er-Raster unruhig, Affiliate wieder als externe Blöcke, Rental zu dunkel.

FIX:
- Mid-Navigation sichtbar 4×2;
- Logo groß;
- Full-width neutraler Fold mit Absätzen;
- 7 unique 600×320 Gestalten-Bilder;
- 7er-Raster 3+2+2;
- Affiliate in Nächste-Ebene-Bereich;
- Rental ein Foto + Brush + weißer CTA.

TEST:
PHP 10/10; ZIP PASS; Chromium 1600/1024/390 PASS; 0 horizontal overflow.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.617_HOBBY_DEPOT_HUB_GRID_NAV_AFFILIATE_INTEGRATED_LOCALPASS.zip`

SHA:
`5f6e5ddf30662a10ecdfc37b35aaca82ad0ba578d59cde20b463d11314624764`

NEXT:
1.50.617 installieren und Gestalten live prüfen.


---

## PU-20261011-HD004 – Hobby Depot Kategorie-Kern 1.0.0

PLUGIN-ID:
`HD-004-KATEGORIE-KERN`

ZWECK:
Read-only Normalbetriebs-Kern für zentrales Kategorie-Register und journal_cat.

ARTEFAKT:
`HOBBY_DEPOT_KATEGORIE_KERN_HD004_V1.0.0_READONLY_LOCALPASS.zip`

SHA-256:
`f3be1e10b093a24f41981c9386ce8ca208294bb0583b6bcc4a1f5295fb5c0bfb`

LOCAL:
- PHP PASS;
- ZIP PASS;
- Runtime API PASS;
- Snapshot/Mapping PASS;
- journal_cat PASS;
- keine Strukturwrites;
- kein DataForSEO-/Providerpfad.

NEXT:
HD-004 installieren/aktivieren → HD-001 nur deaktivieren → Live-Smoke-Test. Löschen erst danach.


---

## PU-20261011-035 – HD-003 1.50.618

LIVE-SCREENSHOT-FOLGEFIX:
- Logo nicht mehr gequetscht, linksbündig;
- Navigation tiefer;
- Flyouts am Weltpunkt;
- Hero/Fold ohne Wiederholung;
- kompakte 132×70-Querformat-Thumbnails;
- Affiliate-Banner/Produkte direkt im Next-Level-Raster;
- neuer Direktwerbeauftritt.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.618_HOBBY_DEPOT_LIVE_LAYOUT_MONETIZATION_FIX_LOCALPASS.zip`

SHA:
`0498a836102540f02a890ac02e415a0bf60d33418d51a2385e15efb4543ee203`

LOCAL:
PHP 10/10; Fresh PHP 10/10; ZIP PASS; DOM-/Strukturchecks PASS.

LIVE:
OFFEN.


---

## PU-20261011-036 – HD-003 1.50.619

LIVE-FIX:
- Navigation tiefer / Headerbereiche luftiger;
- Flyouts wieder Hover/Fokus/Klick;
- Unterkategorie-Bilder füllen ihren Querformatrahmen;
- 7 individuelle Gestalten-Kurzzeilen statt generischem Wiederholungstext.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.619_HOBBY_DEPOT_NAV_FLYOUT_CARD_FIX_LOCALPASS.zip`

SHA:
`dada31464533e143d875e0d7568ee6fc8bba2d79d7b8aaa2f6bac6df806d1179`

LOCAL:
PHP 10/10; ZIP PASS; 7/7 Bildhashes eindeutig; Preview mit geöffnetem Flyout geprüft.

NEXT:
1.50.619 live prüfen.


---

## PU-20261011-037 – HD-003 1.50.621

Nur Header-Mikrofix:
- Header kompakter;
- Navigation an untere Linie;
- alle 8 Nav-Baselines identisch;
- Sammeln geprüft;
- Suchfeld auf HOBBY-DEPOT-Wortmarkenlinie;
- unverändertes Logoasset intern luftiger dargestellt;
- Flyouts unverändert funktionsfähig.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.621_HOBBY_DEPOT_HEADER_ALIGNMENT_LOCALPASS.zip`

SHA:
`a51f986d945ca87e85de4ff367c73ed3e09772e48b25bd5308ad53bcc72be226`

LOCAL:
PHP 10/10; ZIP PASS; Playwright 1600/1024/960/800; overflow 0; Flyout-POS PASS.

NEXT:
nur Header live prüfen.


---

## PU-20261012-038 – HD-003 1.50.623

VON / AUF:
1.50.622 → 1.50.623.

ÄNDERUNG:
Header unverändert. Bildkarten auf allen acht ersten Welt-Hubs vervollständigt.

ABDECKUNG:
Gestalten 7, Fertigen 11, Technik 9, Forschen 5, Pflanzen 10, Tiere 7, Bewegen 8, Sammeln 8 = **65 direkte Unterkategorien**.

REGEL:
Featured Image zuerst; sonst dediziertes lokales 600×320-Motiv; kein mehrfaches Parent-Hero als Universalersatz.

TEST:
PHP 10/10 PASS; ZIP PASS; 65/65 Pfade; 65/65 Bilder geladen; 1600/1200/1024/900/760 ohne horizontalen Overflow.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.623_HOBBY_DEPOT_ALL_HUB_IMAGES_LOCALPASS.zip`

SHA:
`0b5021854f5bbb1a3ab35bcba0fc14bd522cb6679b4299276029a0f8a87b25f7`

LIVE:
OFFEN.


---

## PU-20261012-039 – HD-003 1.50.624

ÄNDERUNG:
- Navigation final an untere Headerkante gebunden;
- keine Affiliate-Produkte mehr zwischen Unterkategorie-Reihen;
- Banner füllt freie Restplätze der letzten 3er-Reihe;
- Produkte außerhalb des Kategorie-Rasters;
- alle 65 aktiven direkten Hub-Bilder eindeutig.

BILDER:
65 aktive Bilder / 65 eindeutige SHA-256-Hashes. Doppelung Genuss ↔ Essbare Pflanzen beseitigt. Unbenutzte Alias-Duplikate entfernt.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.624_HOBBY_DEPOT_NAV_BOTTOM_BANNER_FILL_NO_DUPLICATES_LOCALPASS.zip`

SHA:
`af8cb6a33c8da51d0153b9b22a7e6bb210e9cef4fe9e01545d9d31c33527b15c`

LOCAL:
PHP 10/10; ZIP PASS; Raster-/Hash-/Strukturchecks PASS.

LIVE:
OFFEN.


---

## PU-20261012-040 – HD-003 1.50.625

LIVE-BEFUND 1.50.624:
Trotz 65 byte-eindeutiger lokaler Dateien erschienen live mehrfach gleiche Bilder. Zusätzlich lag Sammeln optisch nicht exakt auf derselben Navigationslinie.

ROOT CAUSE BILDER:
WordPress Featured Images wurden vor den kontrollierten lokalen Hubassets ausgewählt. Alte mehrfach gepflegte Featured Images überstimmten dadurch die neuen Motive.

FIX:
- kontrollierte v150625-Hubassets zuerst;
- Featured Image nur noch Fallback;
- 65 Motive auf klarere, ruhigere Einzelmotive zugeschnitten;
- 65/65 SHA-eindeutig;
- Perceptual-dHash Mindestabstand 96.

ROOT CAUSE NAV:
Pfeilbutton und alte Grid/Flex-Kaskaden beeinflussten Itemgeometrie.

FIX:
- ab 761 px eine einzige Flexzeile;
- feste Labelhöhe/-line-height;
- Pfeilbutton absolut aus dem Textfluss;
- Sammeln exakt gleiche Baseline.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.625_HOBBY_DEPOT_SIMPLE_UNIQUE_HUB_IMAGES_NAV_BASELINE_LOCALPASS.zip`

SHA:
`6aab2195365375c30c4dfcc4558dd8aa62f912289df76544b6e0cb5529960e03`

TEST:
PHP 10/10; ZIP PASS; Featured-Image-Negativtest PASS; 65/65 Assets; Playwright 1600/1200/1024/900/800/761 Baseline + Overflow PASS; Sammeln-Flyout viewport-safe.

LIVE:
OFFEN.


---

## PU-20261012-041 – HD-003 1.50.627

VON / AUF:
1.50.626 → 1.50.627.

ÄNDERUNG:
- Hauptnavigation ab 761 px als harte 8er-Einzeile; Sammeln exakt gleiche Baseline;
- 65 Hubmotive enger/gezoomter und ruhiger;
- 8 eigenständige natürliche Hero-Texte;
- `Mehr über <Welt> erfahren` auf Hauptwelten entfernt;
- 8 lange redaktionelle Seitenendtexte mit Zwischenüberschriften;
- semantische Links nur auf reale direkte Unterkategorien.

TEST:
PHP 10/10; ZIP PASS; stale class refs 0; 65/65 Bild-SHA eindeutig; dHash-Minimum 92; 8/8 Hero-Texte; 8/8 Endtexte; Link-Slugs gegen zentrales Kategorieprofil PASS; Playwright 1600/1200/1024/900/800/761 eine Nav-Baseline inkl. Sammeln, Overflow 0; 760 Mobile.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.627_HOBBY_DEPOT_HUB_COPY_IMAGES_NAV_FINAL_LOCALPASS.zip`

SHA:
`bc6690acd847dac08b646243a07f133b189b5facc5abc6ba58526a79d383d158`

LIVE:
OFFEN.


---

## PU-20261012-042 – HD-003 1.50.628

LIVE-BEFUND 1.50.627:
- Navigation jetzt gleichmäßig, aber insgesamt zu tief;
- Kartenbilder trotz besserer Motive noch zu klein lesbar;
- Seitenendtexte mit zu hoher interner Linkdichte.

KORREKTUR:
- komplette Navzeile 8 px angehoben, Baseline-Logik inkl. Sammeln unverändert;
- Bildfläche vergrößert: Desktop 200×107, Tablet 165×88, Mobile 145×78;
- interne Links am Seitenende auf max. 3 pro Hauptwelt reduziert, max. einer pro Abschnitt.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.628_HOBBY_DEPOT_NAV_RAISE_LARGER_IMAGES_LINK_CLEANUP_LOCALPASS.zip`

SHA:
`2e875f7f235e84c211143a71f19a8519314160a96d2b917e5ebd751d4a0df49b`

TEST:
PHP 10/10; ZIP PASS; 65/65 Bildassets SHA-eindeutig; 8/8 Langtexte genau 3 Links; lokale DOM/CSS-Simulation 1600/1200/1024/900/800/761 gleiche Nav-Baseline inkl. Sammeln und Overflow 0.

LIVE:
OFFEN.


ABSCHLUSSCHECK 2026-10-12:
- exaktes Artefakt lokal erneut SHA-/ZIP-/Versions-/PHP-geprüft;
- SHA identisch zur Current: `2e875f7f235e84c211143a71f19a8519314160a96d2b917e5ebd751d4a0df49b`;
- isolierte Campus-Ausgabekopie `CURRENT.zip` fehlt (GitHub 404);
- mangels sicherem Binärschreibweg in diesem Abschlusslauf keine falsche Ersatzdatei erzeugt.

---

## PU-20261012-043 – HD-003 1.50.629

LIVE-BEFUND 1.50.628:
- Navigation: PASS;
- Hero-Texte Ebene 1: PASS;
- Seitenendtexte mit max. 3 internen Links: PASS;
- Kategorie-/Link-Bilder: FAIL – zu eng hineingezoomt, zu detailreich, teilweise nur Motivteile, Thema nicht sofort erkennbar.

KORREKTUR:
- ausschließlich aktiven 65er Kategorie-/Link-Bildsatz geändert;
- überenge v150627-Richtung zurückgenommen;
- lokal geprüften einfachen/weiter gefassten v150625-Motivsatz als neue v150629-Assets gebunden;
- Kartenfläche aus 1.50.628 unverändert;
- Navigation, Texte, Monetarisierung, Taxonomie und Architektur unverändert.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.629_HOBBY_DEPOT_WIDER_CLEARER_CATEGORY_IMAGES_LOCALPASS.zip`

SHA:
`6efba12354975852d8253e6141b0bbbcaf1174f60244a0e982e4caac0659c5cb`

TEST:
PHP 10/10; ZIP PASS; V150629 Binding PASS; 65/65 Bilder 600×320; 65/65 SHA-eindeutig; Weltverteilung 7/11/9/5/10/7/8/8 PASS; Diff gegen 1.50.628 bestätigt keine Navigations-/Text-/Layoutänderung.

LIVE:
Nur Kategorie-/Link-Bilder offen.

---

## PU-20261012-044 – HD-003 1.50.634

LIVE-BEFUND:
- Navigation/Header: PASS und eingefroren;
- Hero-Bilder: nicht betroffen;
- Kategorie-Vorschaubilder: Rahmen/Passepartout weiterhin sichtbar; Motive teilweise zu nah/zu voll;
- 1.50.632 damit verworfen.

KORREKTUR:
- nur Kategorie-Vorschaubilder Ebene 1;
- 65 aktive, visuell geprüfte Motive;
- 48× v150629, 11× gezielt ausgewählte weitere v150623-Szenen, 6× v150616;
- kein globaler Rückfall auf alte Bildserie;
- kein Hub1-Fallback auf Featured Images;
- finale Bildbox ohne Margin/Padding/Border/Radius;
- Hero-Dateien unverändert;
- Navigation/Header unverändert.

SIMULATION:
- 1440 px: 200×107, Rahmengeometrie 0;
- 930 px: 165×88, Rahmengeometrie 0;
- 760 px: 145×78, Rahmengeometrie 0;
- PHP 16/16 PASS;
- ZIP PASS;
- 65/65 aktive Bilder SHA-eindeutig.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.634_HOBBY_DEPOT_CATEGORY_PREVIEWS_WIDER_CLEAR_NO_FRAME_LOCALPASS.zip`

SHA:
`b7347fd4925fb201165b8763ae8ae2f054811dfcb38a167cd6dee04b4f728b75`

LIVE:
Nur Kategorie-Vorschaubilder offen.

---

## PU-20261012-045 – HD-003 1.50.635 / Kategorieebene 2

AUSGANG:
Ebene 1 wird vorerst akzeptiert. Navigation/Header/Hero/Ebene1 sind eingefroren.

ÄNDERUNG NUR HUB2:
- kein Hero-Foto;
- H1 + kurzer Orientierungstext oben;
- reale nächste Ebene zuerst;
- Affiliate-Banner danach als eigener Bereich;
- Artikelvorschau;
- konkrete `category_product_1..3`-Produkte;
- genau ein direkt verkaufbarer Werbeplatz;
- längerer Erklärungstext am Seitenende.

PRODUKTLOGIK:
Mit zunehmender Tiefe werden nicht einfach mehr Produkte eingeblendet, sondern konkretere Slotbelegungen für den aktuellen Seitenkontext verwendet.

REGRESSION:
- 847/847 Assets byteidentisch zu 1.50.634;
- Hero-Dateien unverändert;
- Header/Nav unverändert;
- Ebene 1 unverändert;
- keine Taxonomie-/Architekturänderung.

TEST:
- PHP 19/19 PASS;
- ZIP-Integrität PASS;
- Hub2-DOM-Simulation 1440/1024/760 PASS;
- Reihenfolge: nächste Ebene → Banner → Beiträge → Produkte → Werbeplatz → Langtext;
- kein horizontaler Overflow;
- kein Hub2-Hero in der Simulation.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.635_HOBBY_DEPOT_HUB2_CONTENT_MONETIZATION_LOCALPASS.zip`

SHA:
`1cdeb892906e29505cf300125f051a68b7b7cd1ecc2099202e828a4276713615`

LIVE:
OFFEN. Nach Installation echte Hub2-Seite prüfen.

---

## PU-20261012-046 – HD-003 1.50.636 / Hub2 Verfeinerung + Testbeiträge

LIVE-BEFUND 1.50.635:
- Aufbau Hub2 grundsätzlich okay;
- oberer Text zu kurz/technisch;
- gleiche Welticons auf vielen Unterkategorien zu monoton;
- Artikelvorschau ohne Beiträge nicht beurteilbar.

ÄNDERUNG:
- längerer natürlicher Hub2-Einstieg in vollständigen Sätzen/Absätzen;
- weiterhin kein Hub2-Hero;
- thematisch unterschiedliche Icons für Unterkategorien ohne Foto;
- Hub2-Beitragsvorschau bis zu 4 Karten;
- einmaliger Seed von 4 klar markierten [TEST]-Beiträgen;
- jeder Testbeitrag mit Beitragsbild;
- Zuordnung zu allen aktuell vorhandenen WordPress-Beitragskategorien und zusätzlich journal_cat, falls Posts unterstützt werden;
- Testposts per Meta `_hd_demo_post_v150636=1` eindeutig markiert.

REGRESSION:
- 847/847 Assets byteidentisch;
- Hero/Header/Nav/Ebene1 unverändert;
- Affiliate-Slotlogik unverändert;
- keine Architektur-/Taxonomiestrukturänderung.

TEST:
- PHP 22/22 PASS;
- ZIP PASS;
- Hub2-Simulation 1440/1024/760, Overflow 0;
- 4/2/1 Artikelraster Desktop/Tablet/Mobil;
- Testpost-Assetpfade vorhanden;
- Seed einmalig/Admin-only.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.636_HOBBY_DEPOT_HUB2_REFINEMENT_TEST_POSTS_LOCALPASS.zip`

SHA:
`d8d45997b136cd7d95e0a790f88dfbb4b3207a29b5b644e415b1ac8e0a72007a`

LIVE:
OFFEN.

---

## PU-20261012-047 – HD-003 1.50.637 / Hub2 Claim + Aufklapptext + Testpost-Fix

LIVE-BEFUND 1.50.636:
- Testbeiträge auf Hub2 nicht sichtbar;
- generisches `Themenbereich` unerwünscht;
- oberer Text noch zu kurz.

ROOT CAUSE BEITRÄGE:
Hub2 verlangte weiterhin eine gleichnamige WordPress-Beitragskategorie. Fehlt diese, brach die Vorschau ab, bevor Testposts abgefragt wurden.

ÄNDERUNG:
- individueller kurzer Claim pro Hub2-Kategorie;
- ca. 170 Wörter oberer Gesamttext;
- sichtbarer Lead + aufklappbare Vertiefung direkt im Intro;
- 4 private [TEST]-Beiträge robust beim ersten eingeloggten Admin-/Frontend-Aufruf;
- alle vorhandenen Beitragskategorien + journal_cat, soweit für Posts verfügbar;
- Beitragsbilder aus vorhandenen Assets;
- eingeloggter Hub2-Demo-Fallback über `_hd_demo_post_v150637=1`, wenn keine gleichnamige Beitragskategorie existiert.

REGRESSION:
- 847/847 Assets byteidentisch zu 1.50.636;
- Hero/Header/Nav/Ebene1 unverändert;
- Affiliate-Slots unverändert;
- keine Taxonomie-/Architekturänderung.

TEST:
- PHP 25/25 PASS;
- ZIP PASS;
- 1440/1024/760: Overflow 0;
- 4 Beitragskarten;
- 0 Hub2-Hero;
- 1 aufklappbarer Intro-Bereich;
- 4/4 Beitragsbilder geladen;
- PHP-Harness: fehlende gleichnamige Beitragskategorie → 4 Demo-Karten PASS.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.637_HOBBY_DEPOT_HUB2_CLAIM_EXPAND_TEST_POST_FIX_LOCALPASS.zip`

SHA:
`84bcfad3f867356b34f19a2f61b790300f1496869b3e92a3597481e332116e65`

LIVE:
OFFEN.

---

## PU-20261012-048 – HD-003 1.50.638 / Buch-&-Papier-Hub2-Pilot

PILOT:
Nur `Fertigen → Buch & Papier`.

ÄNDERUNG:
- Claim `Papier kann mehr.`;
- fünf neue kleine klare Fotomotive für Buchbinden, Marmorpapier, Papierherstellung, Stempel schnitzen und Zines;
- 2-spaltige Fotokarten Desktop, 1-spaltig unter 1000 px;
- kurze individuelle Unterzeilen;
- Produkte direkt nach Unterkategorien;
- danach 3 größere Beiträge;
- danach Affiliate-Banner;
- danach Werbeplatz;
- kein Seitenendtext auf dem Pilot-Hub2.

PERFORMANCE:
- 5 neue WebP, jeweils 600×320;
- zusammen 66.054 Bytes;
- lazy loading im Kartenpfad.

REGRESSION:
- vorhandene Asset-Dateien aus 1.50.637 geändert: 0;
- Header/Nav/Hero/Ebene1 unverändert;
- alle anderen Hub2-Seiten unverändert;
- keine Slot-/Taxonomie-/Architekturänderung.

TEST:
- PHP 28/28 PASS;
- ZIP PASS;
- Pilot-Gate ausschließlich `buch-papier`;
- Simulation 1440/1024/760: Overflow 0;
- Reihenfolge Kategorien → Produkte → Beiträge → Banner → Werbeplatz PASS;
- kein Seitenendtext PASS;
- alle simulierten Bilder geladen.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.638_HOBBY_DEPOT_BUCH_PAPIER_PILOT_PHOTO_PRODUCT_FIRST_LOCALPASS.zip`

SHA:
`44f32edd6158b5b82452c837ffe1534008b6cbfb50e7c7da6fcd72da319e0f7a`

LIVE:
OFFEN. Nur Buch & Papier prüfen.

---

## PU-20261012-049 – HD-003 1.50.639 / Buch-&-Papier-Pilot nachgeschärft

PILOT:
Nur `Fertigen → Buch & Papier`.

ÄNDERUNG:
- kompakter Split-Hero;
- links Claim/H1/Lead/Aufklapper, rechts vorhandenes Kategorie-Vorschaubild;
- kein neues Hero-Asset;
- Claim `Papier kann mehr.` mit CSS-Pinselstrich;
- Fotokarten Desktop 3-spaltig, Tablet 2-spaltig, Mobil 1-spaltig;
- Reihenfolge unverändert: Kategorien → Produkte → 3 Beiträge → Banner → Werbeplatz;
- kein Seitenendtext.

PERFORMANCE:
- Split-Hero verwendet vorhandenes `buch-papier-v150629.webp`, 45.934 Bytes;
- keine neuen Bilddateien gegenüber 1.50.638;
- 5 Pilotkartenbilder bleiben ca. 66 KB und lazy geladen.

REGRESSION:
- 852/852 Assets byteidentisch zu 1.50.638;
- Header/Nav/Ebene1 unverändert;
- alle anderen Hub2 unverändert;
- keine Slot-/Taxonomie-/Architekturänderung.

TEST:
- PHP 31/31 PASS;
- ZIP PASS;
- Browser-Simulation:
  - 1440: 3 Kacheln, Hero 2-spaltig, Overflow 0;
  - 1024: 2 Kacheln, Hero 2-spaltig, Overflow 0;
  - 760: 1 Kachel, Hero gestapelt, Overflow 0;
- Brush-Claim gerendert;
- bestehende Assets geändert: 0.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.639_HOBBY_DEPOT_BUCH_PAPIER_SPLIT_HERO_BRUSH_3COL_LOCALPASS.zip`

SHA:
`080b56efd53102de7fde5c01f75b0a9edb53c8a3f4123c1e204b2ded5b1955f2`

LIVE:
OFFEN. Nur Buch & Papier prüfen.

---

## PU-20261012-050 – HD-003 1.50.640 / Buch-&-Papier-Pilot Detailfix

PILOT:
Nur `Fertigen → Buch & Papier`.

ÄNDERUNG:
- Split-Hero wieder exakt in den normalen Body-Container gesetzt;
- Text- und Bildachse stimmen mit den folgenden Inhaltsabschnitten überein;
- Claim `Papier kann mehr.` mit Handschrift-Systemfontstack und dynamischerem Pinselstrich;
- Hero verwendet weiterhin das vorhandene Kategorieasset;
- Bild läuft links weich in Weiß aus;
- Hero-Bild festes 600:320-Verhältnis und bleibt beim Öffnen des Aufklapptexts unverändert;
- Kachelbildformat direkt aus Ebene 1 übernommen:
  - Desktop 200×107;
  - Tablet 165×88;
  - Mobil 145×78;
- 3/2/1-Kachelraster unverändert;
- restliche Pilot-Reihenfolge unverändert.

REGRESSION:
- 852/852 Assets byteidentisch zu 1.50.639;
- keine neuen Bilder;
- Header/Nav/Ebene1/andere Hub2 unverändert;
- Slot-/Taxonomie-/Architektur unverändert.

TEST:
- PHP 34/34 PASS;
- ZIP PASS;
- 1440: Hero-Left = Section-Left 120 px, 3+2 Kacheln, 200×107, Overflow 0;
- 1024: Hero-Left = Section-Left 36 px, 2+2+1 Kacheln, 165×88, Overflow 0;
- 760: Hero-Left = Section-Left 12 px, 1-spaltig, 145×78, Overflow 0;
- Aufklapper geöffnet: Hero-Bild Delta Breite/Höhe jeweils 0.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.640_HOBBY_DEPOT_BUCH_PAPIER_BODY_ALIGN_FADE_BRUSH_LEVEL1_IMAGEFORMAT_LOCALPASS.zip`

SHA:
`588fa7fb961bc9cdf62a96f968a83034b072902c41eaddee5c92d09598ebe6bd`

LIVE:
OFFEN. Nur Buch & Papier prüfen.

---

## PU-20261012-051 – HD-003 1.50.641 / Brush-Stroke + 2px-Rahmen

PILOT:
Nur `Fertigen → Buch & Papier`.

ÄNDERUNG:
- Claim-Schrift unverändert;
- freigegebene Variante 1 als Basis für den Unterstrich;
- Unterstrich beige/Sekundärfarbe, länger, geschwungener, natürlicher, mit mehr Abstand;
- Hero-Bild rechts 2 px Rundung;
- Kategorie-Karten max. 2 px Rundung;
- Kategorie-Bilder exakt innerhalb des Rahmens, Bildslot Δ 0×0;
- übriger Pilot unverändert.

PERFORMANCE:
- 1 neues Brush-WebP: 7.114 Bytes;
- 852/852 vorhandene Assets unverändert.

TEST:
- PHP 37/37 PASS;
- ZIP PASS;
- 1440/1024/760 Overflow 0;
- Hero-Aufklapp-Delta 0×0;
- Kartenbilder innerhalb 1 px Kartenborder, kein Überstand.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.641_HOBBY_DEPOT_BRUSH_STROKE_2PX_FRAMES_LOCALPASS.zip`

SHA:
`b9acd0b3170782f5633d52d3200c58f9c798c48712d7bca36bcaed00c466b9b8`

LIVE:
OFFEN. Nur Buch & Papier prüfen.

---

## PU-20261012-052 – HD-003 1.50.642 / Mikrofix

ÄNDERUNG:
- Brush-Unterstrich ca. ein Drittel kürzer und dünner, mehr Abstand zur Schrift;
- Kategorie-Fotos Radius 0;
- Kartenrahmen Radius 1 px;
- Header-Claim optisch leicht kräftiger;
- Hero rechts bleibt 2 px.

TEST:
PHP 40/40 PASS; ZIP PASS; Bildslots 200×107 / 165×88 / 145×78 unverändert.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.642_HOBBY_DEPOT_BRUSH_SHORTER_SQUARE_PHOTOS_HEADER_CLAIM_LOCALPASS.zip`

SHA:
`3e8e4a2e9de867c5d0d55e4ef45a1156d60d382713f6f8333a3344f51ba554d7`

LIVE:
OFFEN.

---

## PU-20261012-053 – HD-003 1.50.644 / Ebene-1-Kartenpfad übernommen

LIVE-BEFUND 1.50.643:
- Header-Claim weiterhin nicht sichtbar kräftiger;
- Buch-&-Papier-Kategoriebilder/Karten weiterhin falsch;
- reale Kartenanordnung verschlechtert.

ROOT CAUSE:
Pilot nutzte weiterhin eigene `hd-bp-card`-/`hd-bp-photo`-Regeln statt den bereits funktionierenden Ebene-1-Pfad.

KORREKTUR:
- Pilot verwendet jetzt 1:1 `hd-next-grid`, `hd-next-card has-photo`, `hd-next-photo`, `hd-next-card-body`, `hd-next-copy`, `hd-row-size-*`;
- kein aktiver eigener Buch-&-Papier-Karten-/Bildwrapper mehr;
- Unterstrich 5 px höher;
- Header-Claim ohne Größenänderung durch zwei ±0,75-px-Sprite-Lagen sichtbar verdickt.

TEST:
- PHP 46/46 PASS;
- ZIP PASS;
- aktive Version/Class/Templates 1.50.644 konsistent;
- echter Chromium-Render mit kompletter Plugin-CSS-Kaskade und echten Bildern;
- 1440: 3+2 Karten;
- 900: 2+2+1;
- 760: 1-spaltig;
- 1440/1024/900/760 Overflow 0;
- Foto-Wrapper/Card-Border nach 1-px-Rahmen: Offset 0/0;
- Foto/Wrapper: X/Y/W/H Delta 0;
- Margin/Padding 0, Foto-Radius 0, object-fit cover.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.644_HOBBY_DEPOT_LEVEL1_CARD_COPY_HEADER_CLAIM_UNDERLINE_LOCALPASS.zip`

SHA:
`da5be83cfab375759448e0ae995734e3cddf739241fad4ca5841c44b203da9c0`

LIVE:
OFFEN. Nur Buch & Papier + Header-Claim prüfen.

---

## PU-20261012-054 – HD-003 1.50.645 / echter Bildquellen-Fix + Banner-Restplatz

LIVE-BEFUND 1.50.644:
- Unterstrich war gegenüber dem zuvor akzeptierten Stand unnötig höher;
- Header-Claim weiterhin nicht überzeugend kräftiger;
- Kategorie-Fotos wirkten trotz korrektem Wrapper weiter gerundet/nicht sauber im Rahmen;
- bei fünf Unterkategorien fehlte der Banner im dritten Restplatz der zweiten Reihe.

ROOT CAUSE:
Die fünf Pilot-WebPs selbst enthielten weiße/gerundete Screenshot-Ränder. Das konnte CSS nicht beseitigen.

KORREKTUR:
- Unterstrich exakt auf 1.50.643-Position zurück;
- fünf Pilotbilder rechteckig innerhalb des Motivbereichs neu ausgeschnitten, 600×320;
- Ebene-1-Markup/CSS unverändert weiterverwendet;
- 3 Karten oben, 2 links unten, Affiliate-Banner im freien dritten Slot;
- späterer Doppelbanner entfernt;
- Header-Claim über ein neues Logoasset verdickt; sichtbare Pixeländerungen ausschließlich im Claim-Band.

TEST:
- PHP 49/49 PASS;
- ZIP PASS;
- 1440/1024: 3+2+Banner;
- 900 responsive 2-spaltig; 760 1-spaltig;
- Overflow 0;
- Bild/Wrapper X/Y/W/H Δ 0;
- Quellbild-Ecken ohne weiße Rundungsmaske;
- Logo-Pixeldiff oberhalb y=300: 0 sichtbare Pixel.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.645_HOBBY_DEPOT_BP_EXACT_LEVEL1_CARDS_BANNER_CLEAN_IMAGES_CLAIM_FIX_LOCALPASS.zip`

SHA:
`03cacb5faebec8cd579b0050ce64be100819ca6e0bc861ef9bfe477f1105306c`

LIVE:
OFFEN.

---

## PU-20261012-055 – HD-003 1.50.647 / Release-Ketten-Fatal aus 1.50.646 behoben

LIVE-BEFUND 1.50.646:
WordPress kritischer Fehler direkt nach Installation.

EXAKTE URSACHE:
- Mainplugin: V150646;
- aktive Profilklasse: V150646;
- route_template: v150645 Templates;
- v150645 Templates: Aufrufe an Hobby_Depot_Profile_V150645;
- damit Runtime-Class-Fatal.

FIX 1.50.647:
Komplette aktive Kette einheitlich:
Main 1.50.647 → Profil V150647 → Front v150647 → Content v150647 → Templatecalls V150647.

INHALT:
Der beauftragte Hub2-Rollout aus 1.50.646 bleibt enthalten:
- Hero mit vorhandenem Bild + Verlauf;
- individueller Schreibschrift-/Brush-Claim;
- Aufklapptext nach bestehender Pferdeatelier-Regel;
- performance-schonende Asset-Wiederverwendung;
- Kategorien → Produkte → 3 Beiträge → Werbeplatz;
- kein unterer Hub2-Editorialblock.

TEST:
- PHP 53/53 PASS;
- ZIP PASS;
- aktive Release-Chain PASS;
- aktive Stale-V150645/V150646-Refs 0.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.647_HOBBY_DEPOT_HUB2_RELEASE_CHAIN_FATAL_FIX_LOCALPASS.zip`

SHA:
`db5427357bd251f084ab9a8545dee33d760a7b38ace686a5146543ca07210833`

LIVE:
OFFEN.

---

## PU-20261012-056 – HD-003 1.50.648 / akzeptierten 1.50.645-Hub2-Pilot exakt portalweit ausgerollt

AUSGANG:
1.50.647 technisch lauffähig, aber visuell verworfen. Basis wieder 1.50.645.

KORREKTUR:
- akzeptierten Split-Hero/Brush/Kartenpfad 1:1 wiederverwendet;
- Rollout auf alle 65 Hub2-Seiten;
- vorhandenes kontrolliertes Kategorieasset als Hero mit Weiß-Verlauf;
- 65 individuelle kurze Claims;
- Text-Fold nach Pferdeatelier-Regel 1:1: ca. 55 Wörter Lead → Mehr erfahren → Was du hier findest dauerhaft sichtbar;
- Unterkategorien immer als Fotokarten; Featured/Controlled Image zuerst, Parent-Motiv nur als Performance-Fallback;
- 3er-Raster; Restkarten links, Banner füllt freien Restplatz;
- danach Produkte → 3 Beiträge → Werbeplatz;
- kein Hub2-Seitenendtext.

PERFORMANCE / REGRESSION:
- 0 neue Bildassets;
- 859/859 Assets byteidentisch zu 1.50.645;
- Header/Nav/Ebene1 unverändert;
- keine Taxonomie-/Architekturänderung.

TEST:
- PHP 52/52 PASS;
- ZIP PASS;
- Release-Kette vollständig V150648;
- 65/65 Claims;
- 65/65 Heroassets;
- Browser 1440/1024/900/760: Overflow 0;
- 1440/1024: 3+2+Banner;
- Bild/Slot Δ 0;
- Foto-Radius 0;
- Aufklappen: Hero-Bild Δ 0×0;
- Was-du-hier-findest außerhalb des Details und sichtbar.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.648_HOBBY_DEPOT_ALL_HUB2_EXACT_645_LAYOUT_PFERDE_RULE_PERF_LOCALPASS.zip`

SHA:
`8ffc125dcbe95d2657c29ea43ebb69e9be609268ec4c40277a34a15c49502038`

LIVE:
OFFEN.

---

## PU-20261012-057 – HD-003 1.50.649 / reine Pferdeatelier-Textregeln + B&P-Layout + unterschiedliche Kindfotos

LIVE-BEFUND 1.50.648:
- zusätzlicher separater `Was du hier findest`-Block unter dem Fold;
- mehrfach dasselbe Parent-/Hero-Motiv in Unterkategoriekarten;
- kleine Kartenuntertitel nicht zuverlässig wie beim Buch-&-Papier-Stand.

KORREKTUR:
- Basis wieder 1.50.645;
- Pferdeatelier **nur redaktionelle Textregeln** übernommen und separat im Designbüro gespeichert:
  `DESIGN/TEXTREGELN_PFERDEATELIER_KOPIE_20261012.md`;
- Texte 150–200 Wörter, natürlich, themenspezifisch, ohne Generator-/Padding-Sprache und ohne generische Schlussformel;
- Darstellung bleibt B&P: sichtbarer Lead → `Mehr zu <Kategorie> erfahren` → Rest im Aufklapper;
- kein zweiter Textblock;
- jede vorhandene Hub2-Kindseite erhält Fotokarte + kleinen Untertitel;
- Buch & Papier behält exakt seine fünf Motive/Unterzeilen;
- alle anderen Hub2-Karten: eigenes Featured Image zuerst, sonst noch unbenutztes vorhandenes kontrolliertes Foto derselben Welt;
- kein Parent-Hero als Universalbild;
- Banner füllt nur freien Restplatz;
- Produkte → 3 Beiträge → Werbeplatz → Ende.

PERFORMANCE / REGRESSION:
- 0 neue Bildassets;
- 859/859 Assets byteidentisch zu 1.50.645;
- Header/Nav/Ebene1 unverändert;
- keine Taxonomie-/Architekturänderung;
- Kartenbilder lazy.

TEST:
- reale Zielhierarchie: 65 Hub2-Seiten / 328 direkte Kindseiten;
- 65/65 Claims und Heroassets;
- generierte Texte 157–176 Wörter;
- 328/328 Kindseiten mit Foto + Untertitel;
- je Hub2-Seite keine doppelte Foto-URL;
- PHP 52/52 PASS;
- ZIP PASS;
- Release-Chain vollständig V150649;
- Browser 1440/1024/900/760 Overflow 0;
- Bild/Slot Δ 0;
- Aufklappen verändert Hero-Dimension nicht.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.649_HOBBY_DEPOT_ALL_HUB2_BP_LAYOUT_PFERDE_TEXT_RULES_UNIQUE_PHOTOS_LOCALPASS.zip`

SHA:
`a374a3003e5842f2517095e74e178765a31fdf42ae2c5a721027acd79d80975c`

LIVE:
OFFEN.

---

## PU-20261013-058 – HD-003 1.50.650 / Hub2-Bildkuratierung

LIVE-BEFUND 1.50.649:
- Text PASS;
- Aufteilung PASS;
- Hero-/Kartenbilder teilweise zu nah, überfüllt, gerahmt wirkend oder thematisch falsch.

KORREKTUR:
- Text/Layout vollständig eingefroren;
- 65/65 Hub2-Heroes deterministisch auf kontrollierte vorhandene Motive gebunden;
- 328/328 direkte Kindkarten deterministisch gemappt;
- semantische Eltern-/Kindbindung statt zufälligem Welt-Pool;
- weiter gefasste Hero-Quellen bevorzugt;
- v150631-Vignettenquellen aus Hub2 vollständig ausgeschlossen;
- keine doppelte Bilddatei innerhalb derselben Hub2-Seite;
- Buch-&-Papier-Kartenbilder unverändert;
- 0 neue Bilddateien.

TEST:
- PHP 55/55 PASS;
- ZIP PASS;
- Release-Chain V150650, alte aktive V150649-Refs 0;
- 65 Hero / 328 Karten;
- Missing 0;
- v150631 aktiv 0;
- Duplikatpfade pro Hub 0;
- 191 unterschiedliche Bestandsassets;
- 600×320 vollständig;
- Außenkanten-Frame-Heuristik 0;
- Papier & Dokumente sowie Guss & Formen mit echten 200×107-Crops visuell geprüft.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_HOBBY_DEPOT_HUB2_IMAGE_CURATED_WIDER_CLEARER_NOFRAME_LOCALPASS.zip`

SHA:
`b3bf267ccfef1ae5efbdc4efa1df40f586d5a9ae78ee7c865906b04f113ac2d6`

LIVE:
OFFEN – nur Bildqualität.

---

## PU-20261013-059 – HD-003 1.50.651 / Hub2-Hero responsive + 65 Hero-Runde

AUSGANG:
1.50.650: Text/Grundaufteilung akzeptiert, aber Hero bei Tabletbreiten gequetscht; Hero-Motive teils noch zu detailnah. Kategoriekarten bleiben separater offener Block.

KORREKTUR:
- bestehender Langtext inhaltlich unverändert;
- 65 individuelle kurze Hero-Einstiege ergänzt;
- Hero enthält nur Claim + H1 + kurzen Einstieg;
- Langtext darunter: sichtbarer Lead + `Mehr zu … erfahren`;
- >1100 px Split 38/62;
- <=1100 px gestapelt;
- 65 Hero-Pfade erneut visuell gewählt;
- 65 unique Hero-Dateien;
- v150631 vollständig aus Hero-Map ausgeschlossen;
- Papier & Dokumente ohne Münz-Hauptmotiv;
- Karten-Map unverändert zu 1.50.650.

TEST:
- PHP 58/58 PASS;
- ZIP PASS;
- Release-Chain V150651, stale V150650 im aktiven Pfad 0;
- Hero 65/65, Missing 0, unique 65;
- Teaser 65/65;
- Langtextgenerator unverändert;
- Browser 1440/1200/1100/1024/900/760/600: Overflow 0;
- <=1100 Stack PASS;
- Langtext unter Hero PASS.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.651_HOBBY_DEPOT_HUB2_HERO_LAYOUT_WIDE_SCENES_RESPONSIVE_LOCALPASS.zip`

SHA:
`ceed21dbc62fd207b891deb5272351c57f31079e22193804546e2dcf6d8f8427`

LIVE:
OFFEN – nur Hero/Responsive. Kartenbilder folgen separat.

---

## PU-20261013-060 – HD-003 1.50.651 / Live-Fail nachgetragen

LIVE-BEFUND:
1.50.651 ist **verworfen**.

Fehler:
- Hero zu hoch;
- Hero-Quellen teils Detail-Crops statt erkennbarer Szene;
- teils unscharf/hochskaliert;
- falsche semantische Hero-/Kartenmotive;
- Claim-Unterstrich verrutscht und zu lang;
- Kategoriekarten teils doppelt/ähnlich/überfüllt.

Konkrete Beispiele aus dem Live-Readback:
- Genuss → Kakteen;
- Essbare Pflanzen → Kakteen / teilweise identisches Motiv;
- Ameisen & Insekten → Blumen;
- Papier-/Postkarten-Kontext → unpassende Münzen-/Globusmotive.

ENTSCHEIDUNG:
- kein neuer Kandidat;
- Text + Grundaufteilung aus 1.50.650 bleiben eingefroren;
- 1.50.651-Hero nicht weiter ausrollen;
- vor neuem ZIP komplette lokale semantische und visuelle Hero-/Bildprüfung.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.651_HOBBY_DEPOT_HUB2_HERO_LAYOUT_WIDE_SCENES_RESPONSIVE_LOCALPASS.zip`

SHA:
`ceed21dbc62fd207b891deb5272351c57f31079e22193804546e2dcf6d8f8427`

STATUS:
**LIVE FAIL / VERWORFEN.**

## PU-20261014-061 – HD-003 WIP 1.50.653 / semantische Bildsanierung ohne Release

PLUGIN-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

PLUGIN:
Hobby Depot Design / Template Kit.

ART:
Eigenentwicklung / WIP-Fortschreibung, **kein Release**.

FACHBÜRO:
`DESIGN`

VON / AUF:
1.50.652 letzter paketierter, visuell nicht freigegebener Build → WIP 1.50.653.

WARUM:
HRD-067: vorhandene automatische/heuristische Hero- und Kartenbildzuordnung war semantisch nicht zuverlässig genug. Technische Existenz und URL-Eindeutigkeit hatten fälschlich Bildqualität suggeriert.

TATSÄCHLICHER WIP-STAND:
- 59/65 Heroes aktiv, 6 fehlen;
- 59/65 Kategorievorschauen, jeweils aus derselben Quelle wie das zugehörige Hero;
- 75/328 Karten belastbar aktiv, 253 fehlen;
- keine semantischen Fallbacks;
- fehlend bleibt fehlend.

ÄNDERUNGEN:
- reale Hero-Crops auf 600×220;
- Kategorievorschauen aus derselben Heroquelle auf 200×107;
- Karten auf 200×107;
- neue fachlich geprüfte Ersatzmotive blockweise ergänzt;
- Doppel-/Nahduplikate und Hero↔Karte-Gleichquellen geprüft;
- ungültige Renderer-Quellenkennung bei `3d-druck` und `wandern` korrigiert;
- unklare Motive wieder verworfen statt aufzufüllen.

LOKAL BELEGTER TECHNIKSTAND laut aktueller Design-/Plugin-Current:
- 61/61 PHP Syntax PASS;
- 59/59 Heroassets 600×220;
- 59/59 Kategorievorschauen 200×107;
- 75/75 aktive Karten 200×107;
- 75/75 aktive Karten-Mappings rendererkompatibel und Dateien vorhanden;
- 0 exakte oder Nah-Doppelungen innerhalb derselben Seite.

NEGATIV-/FAIL-CLOSED-VERHALTEN:
- ungeeignete oder zu ähnliche Motive werden wieder entfernt;
- kein Featured-Image-, Welt-Pool-, Icon- oder Hero-Weltfallback;
- kein ZIP solange Release-Gate nicht vollständig erfüllt ist.

LIVE:
Kein Live-PASS. Kein neuer Kandidat.

ARTEFAKT:
Kein neues isoliertes `CURRENT.zip`. Die bestehende isolierte Ausgabe wird nicht ersetzt, solange kein freigabefähiger Kandidat vorliegt.

CURRENT:
`PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md`



---

## PU-20261015-062 – HD-003 / Reparatur- und Hero-Helferserie 1.50.653–1.50.663 vollständig verworfen

PLUGIN-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

ART:
Eigenentwicklung / Reparatur- und Bildupdateversuche; **kein freigegebener Release**.

AUSGANG:
1.50.650 bleibt der letzte Grundstand mit live bestätigtem Textinhalt und bestätigter Grundaufteilung. 1.50.651 war bereits LIVE FAIL.

TATSÄCHLICHER VERLAUF:
- 1.50.653: Release-Kettenfehler; aktive Templates referenzierten alte Profilklasse → Fatal.
- 1.50.654–1.50.656: weitere Reparatur-/Ableitungsversuche nicht freigabefähig.
- 1.50.650 Runtime Restore mit neuen Bildern: lokal codegleich zur 1.50.650-Runtime, live dennoch kritischer Fehler.
- 1.50.657 Repair Installer: separater Reparaturweg; nicht verwenden.
- 1.50.658 Recovery: Recovery-Versuch; danach Backendzugriff gestört; Recovery/Repair serverseitig entfernt, Seite wieder erreichbar.
- 1.50.659: als Hero-only ausgegeben, änderte entgegen Auftrag zusätzlich Hero-Mapping → verworfen.
- 1.50.660: reiner 65er-Dateiaustausch technisch lokal korrekt, aber 30 Heroes live visuell verworfen.
- 1.50.661: falscher Pluginordner, deshalb keine echte Überinstallation.
- 1.50.662: In-Place-Identität korrigiert, Ausführung aber an `admin_init` gebunden und bei direkter Frontendprüfung wirkungslos.
- 1.50.663: Ausführungspfad technisch korrigiert und positiv/negativ geprüft; **LIVE VISUAL FAIL**, weil Grundszenen recycelt, nur anders gecroppt, Bild-in-Bild/Collagen, falsche Motive und Mehrfachbelegungen verwendet wurden.

ENDENTSCHEIDUNG:
- 1.50.651–1.50.663 nicht verwenden;
- Affiliate Portal Template Kit 1.50.650 bleibt aktiver Grundstand;
- keine weitere Runtime-/Architekturänderung;
- Bildquellen werden außerhalb eines Pluginreleases zuerst 30/30 semantisch und visuell geklärt;
- kein Plugin-Nachfolger vor vollständigem Bildquellen-Audit.

TESTSTATUS:
- technische lokale Positiv-/Negativtests einzelner Helfer sind als Evidence/Historie gültig;
- sie stellen **keinen Bildqualitäts- oder Live-PASS** dar;
- aktuell existiert **kein** freigabefähiger neuer Pluginstand.

ARTEFAKT:
Kein neues `ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip` erzeugt oder ersetzt.

ROLLBACK / SICHERER STAND:
1.50.650 Grundstand; Text und Grundaufteilung eingefroren.

FACH-CURRENT:
`../DESIGN/CURRENT_STATE.md`

PLUGIN-CURRENT:
`PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md`


## PU-20261016-063 – HD-003 / HRD-SCOPE13 gezielte Bildreparatur

PLUGIN-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

PLUGIN:
Affiliate Portal Template Kit – Hobby Depot Profil.

ART:
Eigenentwicklung / gezielter Bildreparaturkandidat auf eingefrorener 1.50.650-Basis.

FACHBÜRO:
`DESIGN`

VON / AUF:
30er-Neubildbasis auf 1.50.650 → HRD-SCOPE13-Reparaturkandidat auf derselben 1.50.650-Runtime.

WARUM:
Der Nutzer meldete exakt 13 Kategorien mit verschlechterten/falschen Bildern und ordnete eine harte Sperre an: ausschließlich diese 13 reparieren; alle anderen Kategorien nicht anfassen. Bei mehreren Kategorien war ausdrücklich der frühere Bildstand besser.

ÄNDERUNG:
- ausschließlich 13 Kategorien repariert;
- vor Neugenerierung ältere Bildstände geprüft;
- keine neue Bildgeneration notwendig;
- 7 frühere gute Vollquellen wiederhergestellt;
- 2 Kategorien auf bessere 1.50.625-Bilder zurückgesetzt;
- 4 Kategorien auf bessere WIP-1.50.653-Bilder zurückgesetzt;
- Hero und Preview je Kategorie gemeinsam ersetzt;
- keine Collage als Releasequelle.

NICHT GEÄNDERT:
- sämtliche anderen Kategorien;
- Mapping;
- PHP;
- CSS;
- Templates;
- Routing;
- Kartenlogik;
- Architektur.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_HOBBY_DEPOT_HRD_SCOPE13_REPAIR_LOCALPASS.zip`

SHA-256:
`d32805e2747f9df25e722efc7242f4df820bd273f19db2e2b8b97e5b249e1bf4`

POSITIVTEST:
- exakt 26 Bilddateien geändert = 13 Heroes + 13 Previews;
- 0 Dateien hinzugefügt;
- 0 Dateien entfernt;
- alle übrigen Dateien byte-identisch;
- Mapping byte-identisch;
- 55/55 PHP byte-identisch;
- 55/55 PHP-Syntax PASS;
- ZIP-Roundtrip PASS.

NEGATIV-/REGRESSION:
- Hard Scope gegen alle Nicht-13-Kategorien geprüft: keine Änderung;
- Collage-/falsche Ersatzquelle nicht verwendet;
- 30er-Neubildbasis außerhalb Scope13 unverändert erhalten.

LIVE-GRENZE:
Noch kein Live-PASS. Nächster Live-Schritt ausschließlich Readback der 13 HRD-Kategorien.

ISOLIERTES ARTEFAKT:
`ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip` ist noch nicht synchronisiert. Vor formaler Artefaktfreigabe exakt diesen Kandidaten synchronisieren und SHA/ZIP prüfen.

CURRENT:
`PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md`


## PU-20261016-064 – HD-003 / Mega-Menü + Hauptweltkopf + Hero→Preview

PLUGIN-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

KANDIDAT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.664_HOBBY_DEPOT_MENU_HUB1_PREVIEW_LOCALPASS.zip`

SHA-256:
`73dfdc40792b1d550aaff6343aab9e9a4ca713988e0aa0c1957825b42ed4e2f9`

ÄNDERUNG:
- Mega-Menü nicht mehr starre 3er-Grenze; gemeinsame sichtbare Zahl aus kleinstem Direktbestand, aktuell 5;
- bei größeren Welten `Mehr Kategorien`, genau eine zusätzliche kompakte Orientierungsebene;
- Hauptwelt-Hero/Textkopf responsive repariert: Desktop nebeneinander, <=1100 px gestapelt, Mobil kompakt;
- 65/65 Kategorievorschauen aus den jeweils aktuellen Hub2-Hero-Dateien neu abgeleitet.

HARD SCOPE:
- keine Kategorienstruktur geändert;
- keine Hero-Datei geändert;
- kein Hub2-Mapping geändert;
- keine Affiliate-/Routing-/Taxonomieänderung.

LOCAL:
- 65 Preview-WEBP geändert;
- 65/65 Preview 200×107;
- 0 Hero-WEBP geändert;
- 58/58 PHP-Syntax PASS;
- Mega-Menü Desktop/Tablet 8/8 gleiche Grundhöhe;
- ZIP-Integrität + Roundtrip PASS.

LIVE:
OFFEN.

---

## PU-20261016-065 – HD-001 1.14.9 / V3-Struktur-Vollaudit

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

LIVE-BASIS:
1.14.8 bleibt produktiv unverändert.

KANDIDAT:
`HD001_V1.14.9_HOBBY_DEPOT_V3_STRUCTURE_DRYRUN_LOCALPASS.zip`

SHA-256:
`a498c84e2f98ce386acbfb04eb1fee0b77c90d33b51cc1b557f477812bd165a3`

DELTA:
- Workflow-Code unverändert;
- nur Pluginversion 1.14.8 → 1.14.9;
- eingebettetes Zielprofil ersetzt durch zentral auditierten V3-Zielbaum;
- 8 Hauptwelten unverändert;
- 370 terminale Hobbyseiten;
- 2160 unterste CORE-Inhaltskategorien;
- jede terminale Hobbyseite 5–8 Inhaltskategorien;
- 2160/2160 grobe 3–5+-Beitragspotenzialprüfung PASS.

STRUKTURDELTA:
- +285 Nodes = 45 Seiten + 240 Kategorien;
- 2 fachliche Updates;
- 0 Removes.

ECHTE HD-001-LOGIK SYNTHETISCH GEGEN VOLLSTÄNDIGE LIVE-BASELINE:
- PASS;
- CREATE 282;
- ADOPT 3;
- UPDATE 2357;
- ARCHIVE 0;
- DEMOTE_EDITORIAL 0;
- Provider/DataForSEO Calls 0;
- WordPress-Writes 0.

ADOPT:
Trainspotting, Modellraketen, Pflanzenbestimmung.

NEUE RESOLVED REVISION:
`HD-TARGET-3P-RULE27-CATEGORY-GAPFIX-HOBBYFINDER-20261009+16d1bd25b2adfc26`

LIVE:
NOCH NICHT SYNCHRONISIEREN. Zuerst echter WordPress-Final-Target-Dry-Run.

---

## PU-20261016-066 – HD-003 1.50.668 / zentrales Registry-Fundament

PLUGIN-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

BASIS:
saubere 1.50.650-Runtime.

VERWORFEN:
1.50.664–1.50.667; kein weiterer Aufbau auf diesen Live-Fails.

KANDIDAT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.668_HOBBY_DEPOT_REGISTRY_FOUNDATION_LOCALPASS.zip`

SHA-256:
`0fb575aeddd19aac285188507d0753eaa554b558183d6686c2a900322c865a5a`

ÄNDERUNG:
- HD-004 wird einzige CORE-Strukturquelle für Hobby-Navigation/Karten;
- rohe WordPress-get_pages-Kinder entfernt;
- Page-/Category-Kinder getrennt;
- letzte Inhaltskategorieebene terminaler Hobbys sichtbar;
- tiefere Hub2-Ebene Icon/Text statt Fotoflut;
- Weltbild-Zufallsfallback entfernt;
- Term-Kinder ebenfalls Registry-gebunden;
- fehlende Registry fail-closed, kein stiller Rückfall auf 1.50.650.

POS/NEG:
- absichtlich falsches rohes Trainspotting unter Messen & Analysieren vorhanden;
- Registry blendet es dort zuverlässig aus;
- Messen & Analysieren = Bodenanalyse / Elektrochemie / Spektroskopie / Wasseranalyse;
- Ameisenhaltung = 7 echte Registry-Inhaltskategorien;
- fehlende Registry → 0 erratene Kinder.

BROWSER:
echtes Plugin-CSS bei 1440 / 1024 / 768 / 390 px;
0 horizontaler Overflow;
0 Fotokarten auf tiefer Ebene.

PAKET:
- 981 → 984 Dateien;
- 3 neue versionsgebundene PHP-Dateien;
- Hauptplugin geändert;
- 0 Bilder geändert;
- PHP 58/58 PASS;
- ZIP-Roundtrip 984/984 PASS.

LIVE:
Erst nach V3-Struktur-Sync/Readback und HD-004-Runtimeprüfung.



---

## PU-20261017-067 – HD-001 1.14.12 / V7.1 manual-only Dry-Run-Fix nach 1.14.9-Timeout

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

PLUGIN:
Affiliate-Portal Kategorie-Workflow.

ART:
Eigenentwicklung / sicherer manueller Dry-Run-Kandidat.

FACHBÜRO:
`SEO_KATEGORIEN`

VON / AUF:
live 1.14.9 → Kandidat 1.14.12.

WARUM:
1.14.9 konnte nach Versionswechsel den Final-Target-Runner auf normalem WordPress-`init` automatisch anstoßen und verursachte beim Nutzer Gateway Timeout.
Der erste V7-Dry-Run-Test blockierte zusätzlich korrekt, weil historische Kontrollzähler noch auf dem alten 330er Bestand standen.

KORREKTUR:
- manual-only hart aktiv;
- 0 Target-Runner-`init`-Hooks;
- Installation/Aktivierung startet keine Vollbaum-Verarbeitung;
- V7.1 korrigiert ausschließlich interne Kontrollzähler auf den tatsächlich aufgelösten V7-Endbestand;
- fachliche V7-Struktur unverändert;
- Dry-Run und Apply bleiben getrennte Adminwege.

ARTEFAKT:
`HD001_V1.14.12_HOBBY_DEPOT_V7_1_MANUAL_ONLY_LOCALPASS.zip`

SHA-256:
`2a0ac6e936628baf7aff3b0ed67bdecd60a9ca9ba23d992396fa4d0abf2b0a5f`

ZIELPROFIL:
`HOBBY_DEPOT_TARGET_PROFILE_V7_1_DRYRUNFIX_20261017`

PROFIL-SHA:
`14b7b4b66310ccf19e51e9a4e403628af8705a5ae6f1e14e03f5c87f0991bc7e`

POSITIVTEST:
- PHP 33/33 PASS;
- ZIP 47/47 PASS;
- Pluginversion 1.14.12;
- manual-only true;
- Resolver 3517 Knoten / 862 Entities / 0 Errors / 0 Warnings;
- echter Dry-Run-Algorithmus gegen simulierten alten 330er Livebestand PASS;
- CREATE 1128 / ADOPT 3 / UPDATE 2356 / ARCHIVE 1;
- Provider Calls 0;
- WordPress Structure Writes 0.

NEGATIV-/FAIL-CLOSED:
- V7 mit falschen historischen Kontrollzählern blockierte statt weiterzulaufen;
- normaler init-/Aktivierungspfad startet keinen Target-Job;
- Dry-Run ruft keinen Apply/Sync auf.

LIVE:
- Nutzer bestätigt weiterhin aktive 1.14.9;
- echter WordPress-V7.1-Dry-Run mit 1.14.12 noch offen;
- kein Apply/Sync ausgeführt.

ISOLIERTES ARTEFAKT:
`ISOLIERTE_PLUGINS/HD-001-KATEGORIE-WORKFLOW/CURRENT.zip` noch nicht synchronisiert; Manifest auf 1.14.12 nachgezogen. Kein Release-/Live-PASS vor echtem WordPress-Dry-Run.

ROLLBACK:
Kein Strukturwrite durch die lokale Simulation. Live bleibt alter 330er Snapshot bis zu ausdrücklich bestätigtem Apply.

---

## PU-20261017-068 – HD-003 1.50.669 WIP / V7.1-Mega-Renderer + Fail-closed-Bildgate

PLUGIN-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

PLUGIN:
Affiliate Portal Template Kit – Hobby Depot Profil.

ART:
Eigenentwicklung / WIP, **kein Release**.

FACHBÜRO:
`DESIGN`

VON / AUF:
live 1.50.668 → WIP 1.50.669.

VORGESCHICHTE:
1.50.664–1.50.667 wurden nach Liveprüfung verworfen; lokale Teilprüfungen hatten Mega-Menü-/Textfehler nicht zuverlässig abgebildet.

ÄNDERUNG 1.50.669:
- Registry bleibt einzige Strukturwahrheit;
- echte Zwischenbereiche = Mega-Spalten;
- direkte Hobby-/Orientierungsseiten nicht als zusätzliche Mega-Spalten;
- V7.1-Mega-Zahlen 7 / 10 / 9 / 8 / 9 / 7 / 8 / 9;
- initial 5 gleichmäßige Gruppen;
- `Mehr Kategorien` zeigt restliche Zwischenbereiche im selben Flyout;
- kein Roh-`get_pages()`-Fallback;
- terminale Content-Kategorieebene bleibt sichtbar.

POSITIV-/REGRESSION:
- V7/V7.1-Strukturinhalt 381 Hobbyseiten;
- 0 Struktur-/Route-/Render-Mismatches;
- alle 8 Mega-Menüs;
- Browserbreiten 1920 bis 390 px;
- horizontaler Overflow 0;
- PHP 61/61 PASS.

NEGATIV:
- falsches Trainspotting unter Messen & Analysieren ausgeschlossen;
- fehlende Registry → keine erratenen Kinder;
- generischer Weltbild-Fallback im aktiven WIP entfernt.

RELEASE-GATE:
Exakt sechs Hero+Preview-Paare fehlen/ersetzen:
Spotting & Verkehr; Citizen Science; Natur bestimmen; Suchen & Finden; Modellbau; Holz & Natur.

`Holz & Natur`: vorhandenes Holzmotiv semantisch FAIL / REPLACE_REQUIRED.

ARTEFAKT:
Kein finaler 1.50.669-ZIP und kein isoliertes `CURRENT.zip`, weil WIP nicht releasefähig ist.

LIVE:
1.50.668 bleibt aktiv; alter 330er Snapshot bleibt sichtbar. Kein 1.50.669-Live-PASS.

ROLLBACK:
1.50.668 bleibt letzter aktiver Designstand.

---

## PU-20261017-069 – HD-001 1.14.13 / realen 1.14.12-Dry-Run-Blocker exakt repariert

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

PLUGIN:
Affiliate-Portal Kategorie-Workflow.

ART:
Eigenentwicklung / enger Reparaturkandidat auf unverändertem V7.1-Fachstand.

FACHBÜRO:
`SEO_KATEGORIEN`

VON / AUF:
real getestete 1.14.12 → Kandidat 1.14.13.

REALER BEFUND 1.14.12:
- Nutzer installierte 1.14.12 und startete ausschließlich den Finalen Delta-Dry-Run;
- Status BLOCKED;
- Zielobjekte 2642;
- CREATE 279 / ADOPT 4 / UPDATE 2357 / UNCHANGED 0 / ARCHIVE 0;
- LIVE_COLLISION bei Libellenbeobachtung;
- LIVE_COLLISION bei Nachtvogel-Beobachtung;
- kein Apply/Sync.

URSACHE:
- das Plugin enthielt korrekt V7.1 mit 3487 physischen Zielen;
- der Final-Dry-Run durfte aber weiterhin einen extern gesetzten alten Zielprofilpfad verwenden;
- der reale 2642er Lauf entspricht diesem alten Profilstand;
- zusätzlich wurden frühere `_apkw_target_node_id`-Bindungen der neu stabilisierten Proposal-Hobbyseiten nicht als zulässige Migrationsbindung erkannt.

KORREKTUR 1.14.13:
- Finaler Hobby-Depot-Dry-Run erzwingt für diesen Weg das eingebettete V7.1-Profil;
- 51 Proposal-Hobbyseiten erhalten ihre frühere Target-Identität als reine Legacy-/Migrationsbindung;
- Dry-Run-Matcher prüft frühere Target-Bindung vor einer Slug-Kollision;
- Sync-Matcher besitzt denselben Wiederverwendungsweg für einen später ausdrücklich bestätigten Apply;
- Fremdkollisionen und mehrdeutige Legacy-Bindungen bleiben fail-closed;
- keine Fachstruktur, kein Leaf-Inhalt und keine Architektur geändert.

ARTEFAKT:
`HD001_V1.14.13_HOBBY_DEPOT_V7_1_LIVE_COLLISION_FIX_LOCALPASS.zip`

SHA-256:
`c543ac655f12d4fcb0d5cb581b3f8a3410103988655a87bb62bab9cbd9995fa3`

EINGEBETTETES PROFIL SHA-256:
`23c707b38f1892703f959c5374b736c7b85fa4db56023a22e987debdc215911f`

LOKALER NACHWEIS:
- PHP 33/33 PASS;
- ZIP-Roundtrip PASS;
- V7.1 unverändert: 3517 logisch / 3487 physisch / 862 Entities / 383 CORE / 381 Hobby-Hubs / 2995 Content-Kategorien;
- 381/381 Einstieg, FAQ, Ausrüstung/Kosten-Abdeckung und Vergleich/Kaufberatung unverändert;
- 6–10 Content-Leafs je Hobby;
- externer Altprofil-Override simuliert: Final-Dry-Run bleibt V7.1;
- Libellenbeobachtung frühere Target-Bindung: REUSE/PASS;
- Nachtvogel-Beobachtung frühere Target-Bindung: REUSE/PASS;
- alle 51 Proposal-Altbindungen zusammen: PASS;
- echte fremde Slug-Kollision: BLOCKED;
- doppelte Legacy-Bindung: BLOCKED;
- Provider Calls 0;
- WordPress Structure Writes 0;
- Dry-Run startet keinen Apply.

LIVE:
1.14.13 noch nicht real in WordPress geprüft.
Kein Sync/Apply freigegeben.

NEXT:
1.14.13 über die aktuell installierte 1.14.12 installieren → ausschließlich Finalen Delta-Dry-Run ausführen.
Abnahme: 3487 Zielobjekte, keine beiden bisherigen Kollisionen, danach vollständiges reales Ergebnis prüfen.

---

## PU-20261017-070 – HD-001 1.14.14 / Admin-Vollreadback reproduziert und entfernt

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

VON / AUF:
1.14.13 → 1.14.14.

REALER AUSLÖSER:
Der Nutzer meldete unmittelbar nach dem Pluginwechsel extrem langsames Laden der Adminseite `Finaler Zielbaum` und erneute Gateway-Timeout-Gefahr. Gleichzeitig blieb der alte 2642er BLOCKED-Dry-Run sichtbar.

NACHPRÜFUNG 1.14.13:
Der Fehler wurde 1:1 im Admin-Renderpfad reproduziert.

Schon beim bloßen Seitenaufruf rief `render()` den kompletten Frontend-/Struktur-Readback auf.

Simulation mit V7.1-Größe:
- get_post 762;
- get_post_meta 1524;
- get_term 2995;
- get_term_meta 11980;
- get_posts 1;
- zusätzliche URL-Auflösungen.

Damit war 1.14.13 trotz vorheriger Teiltests nicht freigabefähig und wird verworfen.

ZWEITER UI-FEHLER:
Ein gespeicherter Dry-Run aus 1.14.12 wurde nach Pluginwechsel weiterhin als aktuelles Ergebnis dargestellt. Der Nutzer sah deshalb weiterhin 2642 und die alten Kollisionen, obwohl dies kein neuer 1.14.13-Lauf war.

KORREKTUR 1.14.14:
- normaler Admin-Render führt keinen Vollreadback mehr aus;
- bei COMPLETE wird ausschließlich der bereits im Sync gespeicherte Readback verwendet;
- ein gespeicherter Dry-Run einer anderen Pluginversion wird als ALT markiert und nicht als aktueller Ergebnisblock dargestellt;
- V7.1-Profilbindung und Legacy-Reuse aus 1.14.13 bleiben unverändert;
- keine Fachstruktur, keine Navigation und keine Architektur geändert.

HARD-SIM ADMIN:
- get_post 0;
- get_post_meta 0;
- get_term 0;
- get_term_meta 0;
- get_posts 0;
- alter 2642er Ergebnisblock nicht als aktuell gerendert.

HARD-SIM DRY-RUN:
Ausgang: letzter vollständig synchronisierter 2357er Zielbestand plus die zwei real beobachteten weiterhin vorhandenen Alt-Target-Seiten Libellenbeobachtung und Nachtvogel-Beobachtung.

Ergebnis:
- PASS;
- 3517 logisch;
- 3487 physisch;
- 862 Entities;
- 383 CORE;
- CREATE 1126;
- ADOPT 3;
- UPDATE 2358;
- ARCHIVE 1;
- Errors 0;
- Libellenbeobachtung vorhandene Altseite → UPDATE/reuse;
- Nachtvogel-Beobachtung vorhandene Altseite → UPDATE/reuse.

NEGATIV:
- fremd gebundener Slug → BLOCKED;
- doppelte Legacy-Target-Bindung → BLOCKED.

ARTEFAKT:
`HD001_V1.14.14_HOBBY_DEPOT_V7_1_BACKEND_LOAD_FIX_HARDPASS.zip`

SHA-256:
`fdcca9282b0edcb5e0bb557b9f1fc5ec6cfc3c127afb40b6dc531340f653642a`

TECHNIK:
- PHP 33/33 PASS;
- ZIP-Roundtrip 44/44 PASS;
- V7.1-Profil SHA unverändert `23c707b38f1892703f959c5374b736c7b85fa4db56023a22e987debdc215911f`;
- Dry-Run 0 Strukturwrites;
- kein Apply/Sync automatisch.

LIVE:
Noch offen.

NEXT:
1.14.14 installieren → Adminseite neu öffnen → ausschließlich Finalen Delta-Dry-Run ausführen → keinen Apply/Sync.

---

## PU-20261017-071 – HD-001 1.14.15 / Dry-Run-Timeout vollständig reproduziert und entfernt

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

VON / AUF:
1.14.14 → 1.14.15.

REALER AUSLÖSER:
Der Nutzer meldete nach 1.14.14 erneut Gateway-Timeout.

URSACHE 1.14.14:
Der Admin-Seitenaufruf war zwar entlastet, aber der eigentliche Final-Dry-Run blieb algorithmisch ungebremst:
- für jeden der 3487 Zielknoten wurde der gesamte passende Live-Bestand erneut durchsucht und neu indiziert;
- während der Sortierung wurde die komplette Knotentiefe bei jedem Vergleich erneut aus dem gesamten Zielbaum berechnet.

HARD-E2E-REPRO 1.14.14:
Ausgang: letzter vollständig synchronisierter 2357er Bestand, die drei bekannten ADOPT-Kandidaten und die beiden real beobachteten Altbindungen Libellenbeobachtung/Nachtvogel-Beobachtung.

Ergebnis:
- PASS fachlich, aber Laufzeit lokal 29.775 s;
- get_post_meta 402892;
- get_term_meta 11530381;
- get_posts 2;
- get_terms 6;
- damit auf dem Live-Hosting klar timeoutgefährdet.

KORREKTUR 1.14.15:
- Live-Kandidaten genau einmal nach Target-ID, Legacy-Konzept und Slug indizieren;
- Tiefenwerte einmal vorberechnen und beim Sortieren wiederverwenden;
- gespeicherten Dry-Run ohne redundantes komplettes Zielprofil ablegen;
- keine Änderung an Zielstruktur, Navigation, Legacy-Reuse oder Sicherheitsregeln.

HARD-E2E-POSITIV 1.14.15:
Gleiche Ausgangsdaten:
- Laufzeit lokal 1.113 s;
- get_post_meta 6310;
- get_term_meta 29115;
- get_posts 2;
- get_terms 6;
- PASS;
- 3517 logisch;
- 3487 physisch;
- CREATE 1126;
- ADOPT 3;
- UPDATE 2358;
- ARCHIVE 1;
- Errors 0;
- Libellenbeobachtung → vorhandene Altseite UPDATE/reuse;
- Nachtvogel-Beobachtung → vorhandene Altseite UPDATE/reuse;
- Trainspotting / Modellraketen / Pflanzenbestimmung → ADOPT.

NEGATIV:
- fremd gebundener Slug → BLOCKED;
- doppelte Legacy-Target-Bindung → BLOCKED;
- alter gespeicherter Prüflauf → nicht als aktueller Nachweis gerendert;
- normaler Admin-Aufruf → keine Vollprüfung.

ARTEFAKT:
`HD001_V1.14.15_HOBBY_DEPOT_V7_1_DRYRUN_TIMEOUT_FIX_HARDPASS.zip`

SHA-256:
`29289c8ef70469d036be42b1d3ce3401a57a15f298201d099263bba9d61f4165`

TECHNIK:
- PHP 33/33 PASS;
- ZIP 47/47 PASS;
- V7.1-Profil SHA unverändert `23c707b38f1892703f959c5374b736c7b85fa4db56023a22e987debdc215911f`;
- Provider Calls 0;
- Dry-Run 0 Strukturwrites;
- kein automatischer Apply/Sync.

LIVE:
Noch offen.

NEXT:
1.14.15 installieren → ausschließlich Finalen Delta-Dry-Run ausführen → keinen Apply/Sync.

---

## PU-20261017-072 – HD-001 1.14.15 realer 3487er Lauf / Hummelkästen + Lederprägen / Release-Sperre bis 1:1-Replay

REALER WORDPRESS-BEFUND:
- 1.14.15 ausgeführt;
- 3487 Zielobjekte;
- CREATE 1122 / ADOPT 4 / UPDATE 2359 / UNCHANGED 0 / ARCHIVE 1;
- exakt zwei LIVE_COLLISION:
  - Hummelkästen;
  - Lederprägen;
- kein Apply/Sync.

EXHAUSTIV:
1122 + 4 + 2359 = 3485.
3485 + 2 blockierte Zielobjekte = 3487.
Der reale Dry-Run hat damit den vollständigen V7.1-Zielbestand abgearbeitet.

URSACHE:
- Hummelkästen live Objekt 902484, alte Target-Bindung `core:entity:b411cdf2ea6046005a4b`;
- Lederprägen live Objekt 902560, alte Target-Bindung `core:entity:ef539e4fcf98dc1c2437`;
- diese zwei tatsächlichen alten Live-IDs fehlten in den 1.14.15-Legacy-Listen.

NACHPRÜFUNG VOR JEDEM NEUEN RELEASE:
Kein neues ZIP an Nutzer ausgegeben.
Kompletter weiterer Workflow lokal simuliert.

DABEI ZUSÄTZLICH GEFUNDEN:
Der Syncpfad hätte nach einem erfolgreichen Dry-Run noch unnötig teuer gearbeitet:
- wiederholte Tiefen-/Indexberechnung;
- große Sync-State-Persistenz nach praktisch jedem Knoten.
Dieser WIP-Pfad wurde performance-schonend korrigiert, ohne Fach-/Kategorie-/Navigationsänderung.

VOLLWORKFLOW LOKAL:
- Dry-Run PASS;
- Sync COMPLETE;
- Readback 3487/3487;
- Frontend/Struktur PASS;
- Header-Navigation PASS;
- 381/381 Hobby-Hubs PASS;
- unbound CORE pages 0;
- Post-Sync-Dry-Run 3487 UNCHANGED;
- Fremdkollision BLOCKED;
- doppelte Legacy-Bindung BLOCKED;
- Live-Drift verändert Fingerprint;
- injizierter Write-Fehler ROLLED_BACK, Ausgangs-Dry-Run danach wieder PASS;
- normaler Admin-Aufruf ohne Vollscan;
- Bootstrap 0 Writes / 0 Schedules / 0 Network.

RELEASE-GATE:
Trotz lokalem Vollworkflow kein neues Plugin, solange der aktuelle reale 1.14.15-JSON-Readback nicht wortwörtlich replayed wurde.

NEXT:
Aktuellen `Finalen Readback als JSON` aus WordPress exportieren und gegen WIP 1:1 replayen. Kein Apply/Sync.

---

## PU-20261017-073 – HD-001 1.14.16 / exakter 1:1-Replay des realen 1.14.15-Readbacks + kompletter Positiv-/Negativ-Vollworkflow

REALER INPUT:
`hobby-depot-final-target-readback-20261017-113602-utc.json`

1.14.15 REAL:
- BLOCKED;
- 3517 logisch / 3487 physisch;
- CREATE 1122 / ADOPT 4 / UPDATE 2359 / UNCHANGED 0 / ARCHIVE 1;
- exakt Hummelkästen + Lederprägen als LIVE_COLLISION;
- kein Apply/Sync.

EXAKTER REPLAY:
- tatsächlicher 1.14.15-Dry-Run-Code;
- 3486/3486 Aktionen exakt identisch;
- Reihenfolge / Objekt-IDs / Actions / Mismatches exakt identisch;
- Summary exakt identisch;
- Errors exakt identisch;
- action_exact=true;
- diffs=[].

URSACHE:
- Hummelkästen Objekt 902484 -> tatsächliche Altbindung core:entity:b411cdf2ea6046005a4b;
- Lederprägen Objekt 902560 -> tatsächliche Altbindung core:entity:ef539e4fcf98dc1c2437;
- diese beiden realen IDs fehlten in 1.14.15.

1.14.16 KORREKTUR:
- exakt diese zwei belegten Migrationsbindungen ergänzt;
- Sync-Tiefensortierung/Indizes vorberechnet;
- Readback-State gebündelt persistiert;
- Profil aus laufendem State ausgelagert;
- Write-State für Rollback-Sicherheit weiter abgesichert;
- keine Fach-, Kategorie-, Navigations- oder Architekturänderung.

POSITIV VOLLWORKFLOW:
- Dry-Run PASS;
- 3487 Ziele;
- CREATE 1122 / ADOPT 4 / UPDATE 2361 / UNCHANGED 0 / ARCHIVE 1 / Errors 0;
- tatsächlicher Runner COMPLETE;
- Readback 3487/3487;
- Headernavigation PASS / expected_count 112;
- 381/381 Hobbyseiten PASS;
- unbound CORE pages 0;
- Post-Sync-Dry-Run: 3487 UNCHANGED, sonst 0.

NEGATIV:
- Hummel foreign BLOCKED;
- Hummel duplicate legacy BLOCKED;
- Leder foreign BLOCKED;
- Leder duplicate legacy BLOCKED;
- Drift zwischen Dry-Run/Apply -> tatsächlicher Apply-Pfad lehnt ab;
- Write-Failure nach 75 Mutationen -> ROLLBACK_PENDING -> ROLLED_BACK;
- Ausgangsplan danach exakt wiederhergestellt;
- Admin render ohne Vollscan;
- manual-only bootstrap 0 Writes / 0 Schedules / 0 Network.

PERFORMANCE:
- alter Depth-Sort-Pfad ~24.26 s lokal;
- gecacht ~0.012 s;
- Runner in begrenzten kurzen Schritten;
- kein einzelner lokaler Tick nahe Timeout.

ARTEFAKT:
`HD001_V1.14.16_HOBBY_DEPOT_V7_1_EXACT_REPLAY_FULL_WORKFLOW_HARDPASS.zip`

ZIP SHA-256:
`bbee98fbf9bbfadf49f18bf64e9f64aba1a274b2266a1473ec89d87996654792`

PROFIL SHA-256:
`87275396fdd8e2e9d15b0a37a6d17a7a21889825d7cdb3f64f276005c73b99d0`

QA:
- PHP 33/33 PASS;
- ZIP 44/44 PASS;
- unzip PASS;
- roundtrip hashes 44/44 exact.

LIVE:
1.14.16 noch nicht real in WordPress dry-run geprüft.
CURRENT.zip bleibt nicht synchronisiert.
Kein Sync/Apply freigegeben.

NEXT:
1.14.16 installieren -> ausschließlich Finalen Delta-Dry-Run ausführen.
Erwartung: 3487 / CREATE 1122 / ADOPT 4 / UPDATE 2361 / UNCHANGED 0 / ARCHIVE 1 / Errors 0.
Bei Abweichung sofort STOP, kein Sync.

---

## PU-20261017-074 – HD-003 1.50.670 / Mega-Menü zwei Reihen + ausschließlich freigegebene Bildkorrekturen

PLUGIN-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

VON / AUF:
1.50.668 live → 1.50.670 Kandidat.

ANLASS:
Frontend nach V7.1 zeigte im Mega-Menü zunächst nur fünf Zwischenbereiche. `Spotting & Verkehr`, `Citizen Science` und `Natur bestimmen` wurden erst über `Mehr Kategorien` sichtbar.

NUTZERREGEL:
- zwei Reihen direkt sind okay;
- `Mehr Kategorien` erst bei einer dritten Reihe;
- Unterkategorien leicht größere Schrift;
- Bildänderungen ausschließlich an den ausdrücklich genannten Kategorien;
- alle anderen Kategorien tabu.

KORREKTUR MEGA:
- bestehende 1.50.669-WIP-Regel für echte Zwischenbereiche übernommen;
- sichtbares Limit 10 statt 5;
- bei aktuellem V7.1 damit alle 7/10/9/8/9/7/8/9 Zwischenbereiche direkt sichtbar;
- `Mehr Kategorien` bleibt nur für hypothetisch >10;
- Heimwerken/Gärtnern bleiben direkte Hobbyseiten und werden nicht zu Mega-Spalten.

BILD-SCOPE:
Nur 17 freigegebene Bereiche.
Holz & Natur ausdrücklich nicht geändert.

RÜCKFALLPRÜFUNG:
1.50.668 gegen 1.50.650, 13 relevante Dateien inklusive Bildmap: 13/13 byte-identisch.
Damit kein neuer Bild-Rückfall durch 1.50.668; Altprobleme wurden lediglich mitgeführt.

QA:
- PHP 61/61 PASS;
- PHP-Registry-Harness V7.1 PASS;
- Mega-Zahlen 7/10/9/8/9/7/8/9;
- 17 Hero 600×320;
- 17 Preview 200×107;
- 0 exakte/nahe Duplikate im benannten Set;
- Bildmap nur an 17 freigegebenen Hero-Schlüsseln geändert;
- Cards-Mapping unverändert;
- ZIP PASS;
- Roundtrip 1009/1009 identisch.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.670_HOBBY_DEPOT_MEGA2ROWS_TARGETED_IMAGES_HARDPASS.zip`

SHA-256:
`9e21fd6c402fbb1a3358a58807db8b28a322a499d8478fbffb375fadbecc0408`

LIVE:
noch offen.

NEXT:
1.50.670 installieren → gezielter Frontend-Check der Mega-Menüs und ausschließlich der benannten Bildbereiche.

---

## PU-20261017-075 – HD-003 1.50.671 / Hero-Master-Regel korrigiert, keine Collagen, nur benannter Scope

ANLASS:
Nutzerprüfung von 1.50.670 zeigte einen Grundfehler im Bildworkflow:
- Hero-Dateien nur 600×320;
- auf großen Displays unscharf;
- mehrere Kategorien zu eng / wie vergrößerte Vorschauausschnitte;
- Forderung erneut bestätigt: Hero ist Master, Vorschau wird heruntergerechnet; keine Collagen.

1.50.670:
Bildteil VERWORFEN.
Mega-Menü-Grundsatz bleibt unverändert.

1.50.671:
- Hero-Master 1600×853;
- Preview 600×320 aus exakt demselben Master;
- keine Collagen;
- kein Preview-Upscaling;
- weiter gefasste Szenen bei den ausdrücklich kritisierten Motiven.

SCOPE EXAKT:
19 Bildbereiche:
Modellbau;
Computer & Retro;
Audio & HiFi;
Spotting & Verkehr;
Citizen Science;
Natur bestimmen;
Bonsai & Miniatur;
Zimmerpflanzen;
Hydroponik & Indoor;
Terraristik;
Münzen & Geld;
Papier & Dokumente;
Technik & Medien;
Spielzeug & Spiele;
Naturfunde;
Werbung & Design;
Werkzeuge & Geräte;
Alltagsobjekte;
Suchen & Finden.

NICHT ANGEFASST:
Gestalten komplett;
Orchideen & Exoten;
Aquaristik;
Holz & Natur;
alle sonstigen Kategorien.

QA:
- PHP 61/61 PASS;
- 19/19 Hero 1600×853;
- 19/19 Preview 600×320;
- 0 exakte Hero-Duplikate;
- Hero-Map außerhalb der 19 Schlüssel unverändert;
- Cards-Map unverändert;
- Gestalten byte-identisch;
- Orchideen & Exoten byte-identisch;
- Klassenlogik gegenüber 1.50.670 außer Versionsbindung identisch;
- ZIP PASS;
- Roundtrip 1029/1029 identisch.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.671_HOBBY_DEPOT_SHARP_MASTER_HERO_TARGETED_HARDPASS.zip`

SHA-256:
`be1e2ed9d82ee290e3744fd23f2c882849e612f768a820868703c50a46c8a606`

LIVE:
noch offen.

NEXT:
1.50.671 installieren -> nur die benannten Bildbereiche prüfen.
---

## PU-20261017-076 – HD-003 1.50.672 / wiederholten AF-026-Frontend-Fatal exakt reproduziert und Release-Kette geschlossen

REALER AUSLÖSER:
Nach Installation von 1.50.671 zeigte Hobby Depot erneut den WordPress-kritischen Fehler.

EXAKTE URSACHE:
- Main lud Hobby_Depot_Profile_V150671;
- route_template() zeigte auf hobby-depot-front-v150670.php / hobby-depot-content-v150670.php;
- beide Templates riefen Hobby_Depot_Profile_V150670 auf;
- class-hobby-depot-profile-v150670.php war im 1.50.671-Paket nicht vorhanden;
- negativer Test reproduziert auf beiden Templates exakt Class "Hobby_Depot_Profile_V150670" not found.

KORREKTUR:
1.50.672 bindet Header/Version, require, class_exists/init, Profilklasse, RELEASE, Routepfade und beide Template-Klassen vollständig auf 1.50.672.

HARTE AF-026-PRÜFUNG: 7/7 PASS.

POSITIV:
- Main lädt;
- Profil lädt;
- Front-Route korrekt;
- Fronttemplate ausgeführt PASS;
- Contenttemplate ausgeführt PASS;
- Dirty-Overlay 1.50.671 -> 1.50.672 PASS.

SCOPE:
Keine Bilder und keine Mega-Menü-Logik gegenüber 1.50.671 verändert. 901/901 Assets byte-identisch.

ARTEFAKT:
AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.672_HOBBY_DEPOT_RELEASE_CHAIN_FATAL_FIX_HARDPASS.zip
SHA-256: f66e0cb03301dfd8658aeb7de4ebcff059bceb9da0760b048e9be6fa40d8c78d

QA:
- PHP 63/63 PASS;
- ZIP PASS;
- Roundtrip 1031/1031 identisch.

LIVE: offen.

NEXT:
1.50.672 installieren -> normale Hobby-Depot-Seite aufrufen -> nur bei Frontend-PASS Bildprüfung fortsetzen.

---

## PU-20261017-077 – HD-003 1.50.673 / Audio-&-HiFi Hero-/Textpilot nach Pferdeatelier-Regeln

AUSGANG:
1.50.672 real im Frontend funktionsfähig; Nutzer akzeptiert den Bildstand.

NUTZERDELTA:
- Hero-Bild auf Desktop deutlich breiter bis nahe an die Überschrift;
- links nur Claim + H1 + kurzer prägnanter Satz;
- langer Kategorietext darunter;
- generische `Bei XY geht es um ...`-Schablone beseitigen;
- Pferdeatelier-Kategorietextregeln exakt übernehmen;
- Audio & HiFi zuerst als einzelner Pilot;
- Unterkategorie-Kurzzeilen ebenfalls natürlich und individuell.

TEXTREGELQUELLE:
`TEXTREGELN_PFERDEATELIER_KOPIE_20261012.md`
SHA `721e3f77d021b3e07e29ed98c9f921d3e0669fa9`.

UMSETZUNG:
- nur Audio & HiFi;
- Desktop 34 % Copy / 66 % Bild;
- Höhe 320 px;
- <=1100 px bestehende Stapellogik unverändert;
- eigener Hero-Satz;
- 161-Wörter-Kategorietext;
- sieben individuelle Kurzzeilen für die realen Audio-Unterkategorien.

REGRESSION:
- 901/901 Assets zu 1.50.672 identisch;
- keine andere Kategorie in Text oder Layout geändert;
- Mega-Menü-Code unverändert.

QA:
- Audio Text 161 Wörter;
- Hero 20 Wörter;
- sichtbarer Langtext 68 Wörter;
- Aufklapper 73 Wörter;
- 7/7 Kurzzeilen eindeutig;
- AF-026 7/7 PASS;
- Fronttemplate PASS;
- Contenttemplate PASS;
- Dirty-Overlay 1.50.672 -> 1.50.673 PASS;
- PHP 66/66;
- ZIP PASS;
- Roundtrip 1034/1034.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.673_HOBBY_DEPOT_AUDIO_HIFI_HERO_TEXT_PILOT_HARDPASS.zip`

SHA-256:
`802d16fd6df5ccdd133bb390ff7d1eb7992640eee9f43627b4e58aa0c15846ef`

LIVE:
offen.

NEXT:
1.50.673 installieren -> ausschließlich Audio & HiFi live prüfen.

---

## PU-20261017-078 – HD-003 1.50.674 / Audio-&-HiFi Fullbleed-Hero mit Header-Beige

AUSGANG:
1.50.673 technisch funktionsfähig, aber der 34/66-Hero wurde grafisch verworfen.

NUTZERENTSCHEIDUNG:
- Bild soll als eine durchlaufende Hero-Fläche wirken;
- links weicher Übergang in helles Beige;
- Beige exakt identisch zum Header;
- kein Logo im Hero;
- Claim/Pinsel behalten;
- Audio & HiFi bleibt H1;
- kurze Zeile darunter;
- Langtext darunter.

UMSETZUNG:
nur Audio & HiFi auf Desktop.
Bildassets unverändert.

QA:
- PHP 69/69;
- aktive 1.50.674-Release-Kette konsistent;
- keine aktive 1.50.673-Stale-Referenz;
- H1/Claim/kein Logo geprüft;
- Beige #f5f1e9;
- 901/901 Assets identisch;
- ZIP PASS.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.674_HOBBY_DEPOT_AUDIO_HIFI_FULLBLEED_BEIGE_HERO_HARDPASS.zip`

SHA-256:
`c40e3271bc31c822aeb076f51880d8c2ef222f27ff31a05f29b4dcc0bf2f98e9`

LIVE:
offen.

NEXT:
1.50.674 installieren -> nur Audio & HiFi live prüfen.

---

## PU-20261017-079 – HD-003 1.50.675 / Audio-Hero responsive zentralisiert, Alttextpfad getrennt

REALER AUSLÖSER:
1.50.674 live zeigte trotz lokalem Desktop-PASS:
- Text/Claim zu nah am linken Rand;
- Fullbleed nur bei >1100 px;
- darunter Bild nicht voll responsive und rechts Leerraum;
- alten langen Hero-Satz statt neuer Kurzzeile;
- Claim optisch weiter im alten Layout.

URSACHE:
- 1.50.674-Fullbleed-CSS nur in min-width:1101;
- darunter griff alte 600-px-Hub2-Regel;
- Hero-Intro wurde weiterhin automatisch aus Satz 1 des Langtexts abgeleitet.

KORREKTUR 1.50.675:
- zentrale wiederverwendbare Klasse hd-hub2-hero-fullbleed;
- aktuell ausschließlich Audio & HiFi gebunden;
- >=901 Fullbleed;
- <=900 gestapelt mit 100-%-Bildbreite;
- Innenabstand via clamp;
- Claim audio-spezifisch positioniert;
- H1 bleibt H1;
- Kurzzeile explizit vom Langtext getrennt;
- ein Bild / CSS-only / kein JS / kein Blur / kein Masking.

RESPONSIVE-SIMULATION:
1440 / 1180 / 1024 / 901 / 900 / 800 / 760 / 600 / 390.
Alle:
- overflow 0;
- media width = hero width.

RENDER-HARNESS:
- fullbleed class PASS;
- claim PASS;
- H1 PASS;
- short intro PASS;
- old hero sentence ABSENT;
- new longcopy PASS;
- more-link PASS.

REGRESSION:
901/901 Assets byte-identisch zu 1.50.674.
Keine andere Kategorie geändert.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.675_HOBBY_DEPOT_AUDIO_HIFI_RESPONSIVE_FULLBLEED_FIX_HARDPASS.zip`

SHA-256:
`aaf1bca2d7b7b55b91f9a15e22e847b67489ceca3faf3d6c1648a6779b636307`

QA:
- PHP 73/73;
- Release-Kette ohne aktive 1.50.674-Stale-Referenz;
- ZIP PASS.

LIVE:
offen.

NEXT:
1.50.675 installieren -> Audio & HiFi breit und halbbreit prüfen.

---

## PU-20261018-080 – HD-003 1.50.675 / Installer-Packaging korrigiert

REALER BEFUND:
WordPress bot beim Upload der ersten 1.50.675-ZIP keine Überinstallation des bestehenden Plugins an.

EXAKTE URSACHE:
Die ZIP begann direkt mit Plugin-Dateien wie `pferde-template-kit.php`, `includes/`, `assets/`.
Der notwendige äußere Pluginordner `affiliate-portal-template-kit/` fehlte.

VERGLEICH:
1.50.674 korrekt:
- `affiliate-portal-template-kit/`
- `affiliate-portal-template-kit/pferde-template-kit.php`

erste 1.50.675 falsch:
- `pferde-template-kit.php` direkt an ZIP-Wurzel.

KORREKTUR:
Keine Codeänderung.
Exakt dieselben 1041 Innendateien wurden unter den korrekten bestehenden Pluginordner gepackt.

NEUES ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.675_HOBBY_DEPOT_AUDIO_HIFI_RESPONSIVE_FULLBLEED_FIX_REPACKED_HARDPASS.zip`

SHA-256:
`356a8e9861f0c018e42620d311eb9985f48279b3a5d1ed26be321c63ddfa24bd`

NACHWEIS:
- 1041/1041 Innendateien byte-identisch zur technisch geprüften 1.50.675;
- Top-Level-Ordner exakt `affiliate-portal-template-kit/`;
- Main-Datei exakt `affiliate-portal-template-kit/pferde-template-kit.php`;
- Plugin Header Version 1.50.675;
- ZIP-Test ohne Fehler.

NEXT:
diese korrigierte Repack-ZIP hochladen; WordPress muss jetzt das vorhandene Affiliate Portal Template Kit zum Ersetzen erkennen.

---

## PU-20261018-081 – HD-003 1.50.676 / Audio-Claim höher, Abstand größer, Unterstrich kurz

REALER BEFUND 1.50.675:
- Claim zu nah an H1;
- Claim soll höher;
- Pinselunterstrich deutlich zu lang.

URSACHE:
Claim war als Flex-Kind quer gestreckt. Der absolute Pinselunterstrich bezog sich dadurch auf die gestreckte Breite statt auf die tatsächliche Claim-Textbreite.

KORREKTUR:
- align-self:flex-start;
- width:max-content;
- Unterstrich 74 %;
- Desktop Claim -12 px;
- größerer Abstand zur H1;
- Mobil Claim -6 px;
- keine Bild-/Text-/Kategorieänderung.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.676_HOBBY_DEPOT_AUDIO_CLAIM_SPACING_UNDERLINE_FIX_HARDPASS.zip`

SHA-256:
`7c898eaeac166e21e47ecfa946baa4ff217f462e5145a9485ec272647186ca82`

QA:
- PHP 75/75;
- 901/901 Assets identisch;
- Release-Kette sauber;
- WordPress-Pluginwurzel korrekt;
- ZIP PASS.

LIVE:
offen.
---

## PU-20261018-082 – HD-003 1.50.677 / Audio-Bild breiter, Unterstrich textlang, Kurzzeile einzeilig

LIVE-BEFUND 1.50.676:
- Höhe des Claims okay;
- Unterstrich zu kurz;
- Bild soll noch breiter wirken, ungefähr drei Viertel;
- Kurzzeile unter H1 soll niemals umbrechen.

UMSETZUNG:
- Claimposition nicht verändert;
- Pinselunterstrich 98 % der echten Claim-Breite;
- Fullbleed-Bild bleibt 100-%-Hintergrund;
- Copy-/Verlaufszone >1180 px auf 30 %, 901–1180 px auf 35 % reduziert;
- Bildposition 58/60 %;
- Hero-Kurzzeile width:max-content + white-space:nowrap;
- Mobile-Schrift skaliert bis min. 9 px nur zur Sicherung der Einzeiligkeit.

PERFORMANCE:
CSS-only, kein JS, kein Bildrequest, keine neue Abfrage.

REGRESSION:
- 901/901 Assets unverändert;
- alle anderen Kategorien unverändert;
- Mega-Menü unverändert.

ARTEFAKT:
AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.677_HOBBY_DEPOT_AUDIO_IMAGE_3Q_SINGLELINE_FIX_HARDPASS.zip

SHA-256:
e0b5b6819f91c7e43b2f6929a04ef97d83d51db34404d87b39506aff9f9c5f16

QA:
- PHP 78/78;
- Release-Kette PASS;
- ZIP PASS;
- Roundtrip 1047/1047.

LIVE:
offen.
---

## PU-20261018-083 – HD-003 1.50.678 / dynamischer Beige-Bereich nach Schriftblockbreite

LIVE-BEFUND 1.50.677:
- starres 3/4-Bildziel zu aggressiv;
- H1 kann bei breitem Fenster umbrechen;
- Textblock soll etwas höher;
- Kurzzeile muss einzeilig bleiben.

ENTSCHEIDUNG:
Nicht überall starres 40/60. Stattdessen dynamischer, begrenzter Textschutzbereich.

UMSETZUNG:
- CSS-only;
- Hero-Bild bleibt 100-%-Fullbleed;
- Text-/Beigezone width:max-content;
- Desktop min 35 %, max 48 %;
- 901–1180 min 42 %, max 58 %;
- eigener Fade-Pseudo direkt am dynamischen Textbereich;
- H1/Claim/Kurzzeile nowrap;
- Block über Padding ca. 10 px höher;
- <=900 gestapelt wie zuvor.

PERFORMANCE:
Kein JS, keine Messroutine, kein zusätzlicher Request, keine Abfrage.

REGRESSION:
- 901/901 Assets identisch;
- keine andere Kategorie verändert.

ARTEFAKT:
AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.678_HOBBY_DEPOT_DYNAMIC_TEXTSAFE_HERO_HARDPASS.zip

SHA-256:
33e35ef638c3564b03343deda6d420f20a85bb387949d017cc75f1d2d9f629f5

QA:
- PHP 81/81;
- Release-Kette PASS;
- ZIP PASS;
- Roundtrip 1050/1050.

LIVE:
offen.

---

## PU-20261018-084 – Abschluss-Nachprüfung 1.50.678 / bisheriger Local-Hard-PASS zurückgezogen

NACHPRÜFUNG:
Die im Arbeitsstand vorhandenen 1.50.678-Visual-Screenshots wurden im Rahmen der verbindlichen Abschlussprüfung erneut direkt geprüft.

BEFUND:
- Claim im lokalen Harness oben sichtbar angeschnitten;
- Hero-Bild im lokalen Harness nicht tatsächlich geladen/gerendert;
- der reale Bild/Text-Übergang war damit nicht belastbar visuell geprüft;
- eine vollständige lokale positive UND negative E2E-Simulation des realen Renderpfads ist nicht dokumentiert.

FOLGE:
- 1.50.678 bleibt technisch gebaut;
- Code-/Paketprüfungen bleiben gültig;
- Bezeichnung LOCAL HARD PASS wird zurückgezogen;
- kein Upload-/Deploymentkandidat;
- kein CURRENT.zip-Sync;
- kein Live-PASS.

NEXT:
1.50.678 im echten lokalen Plugin-Renderweg mit geladenem Audio-Hero positiv und negativ simulieren. Erst danach über WordPress-Installation entscheiden.



---

## PU-20261018-085 – HD-003 / portalweiter Hub2-Hero- und Textrollout vorbereitet

NUTZERENTSCHEIDUNG:
- Audio-&-HiFi-Hero als Zielbild abgenommen;
- dynamische Fullbleed-Hero-Regel auf alle Kategorien derselben Hub2-Ebene ausweiten;
- bisherige schematische Hub2-Kategorietexte verwerfen;
- Pferdeatelier-Textregeln für alle Hub2 verbindlich;
- ungefähr ein Drittel des 150–200-Wörter-Texts sichtbar, niemals mehr als die Hälfte;
- Rest minimalistisch aufklappbar;
- sichtbarer Text `Mehr zu <Kategorie> erfahren` entfällt;
- kleiner Chevron/Pfeil reicht, Screenreader-Beschriftung bleibt;
- Aufklapper näher an den Text;
- kein zusätzlicher Seitenendtext auf Hub2.

AKTUELLER SCOPE:
69 aktive Hub2-Seiten aus dem aktuellen V7.1-Zielbaum.

TEXTARBEIT:
- 69/69 individuelle Hub2-Texte vorbereitet;
- 150–174 Wörter je Gesamttext;
- 45–64 Wörter sichtbarer Lead;
- Audio & HiFi inhaltlich auf dem bereits individuellen Stand belassen und nur kompakter geteilt;
- alte feste `Bei <Kategorie> geht es um …`-Generatorlogik im vorbereiteten Kandidatenpfad entfernt.

HERO-ROLLOUT:
- Audio-Regel zentral für alle Hub2 vorgesehen;
- Desktop dynamischer Textschutz 35–48 %;
- 901–1180 px 42–58 %;
- H1/Claim/Kurzzeile Desktop einzeilig;
- <=900 px gestapelt;
- CSS-only, keine neue Frontend-/DB-Abfrage.

QA:
Der vorbereitete 1.50.679-Codeweg wurde synthetisch auf der zugänglichen 1.50.668-Quellkopie geprüft:
- PHP-Lint ohne Fehler;
- 69/69 Hub2-Render ohne Fehler;
- alte Schablone im Renderpfad nicht vorhanden;
- sichtbarer `Mehr zu …`-Text nicht vorhanden;
- zugängliche Aufklappbeschriftung vorhanden;
- Release-Kette im Testaufbau auf 1.50.679 geschlossen.

WICHTIGE GRENZE:
Diese synthetische Prüfung ist kein Release-PASS und kein installierbares Artefakt. Die exakten 1.50.678-Paketbytes konnten im aktuellen Arbeitsweg nicht materialisiert werden. Ein Paket auf älterer Basis würde spätere Bild-/Hero-/Responsive-Korrekturen riskieren und wird deshalb nicht freigegeben.

ZIELVERTRAG:
ZV-HOBBYRAUSCH-DESIGN-001 auf Fassung 4.7 nachgezogen.

NEXT:
1.50.679 ausschließlich aus der exakten 1.50.678-Quelle bauen und danach positiv/negativ/regressiv lokal prüfen. Vorher kein WordPress-Upload.


---

## PU-20261018-086 – HD-003 1.50.679 / 69 Hub2 aus exakter 1.50.678 gebaut

QUELLBASIS:
Exaktes Artefakt 1.50.678 materialisiert und als einzige Buildbasis verwendet.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.679_HOBBY_DEPOT_ALL_HUB2_TEXT_HERO_ROLLOUT.zip`

SHA-256:
`721a7843c862cc59b47d80e51035d589220a56ecf4a5a8caad2307e921801f4d`

UMSETZUNG:
- bestehende dynamische Fullbleed-Hero-Regel aus 1.50.678 auf alle 69 aktiven Hub2 gebunden;
- keine doppelte Hero-CSS-Schicht ergänzt;
- 69 eigenständig redigierte Hub2-Texte statt alter Generator-Schablone;
- 150–174 Wörter je Text;
- 45–64 Wörter sichtbarer Lead;
- Audio & HiFi 162 Wörter gesamt / 48 sichtbar;
- Rest über kleinen Chevron;
- sichtbarer `Mehr zu <Kategorie> erfahren`-Text entfernt;
- zugängliche Screenreader-Beschriftung erhalten;
- Aufklapper näher an den Lead gesetzt;
- zwei bei der Negativprüfung gefundene generische Claims (`Holz & Natur`, `Hydroponik & Indoor`) durch explizite Claims ersetzt.

QA:
- ZIP PASS;
- PHP 84/84 PASS;
- aktive Release-Kette 1.50.679 PASS;
- positiver Template-Test PASS;
- negativer Template-Test mit nur alter 1.50.678-Klasse scheitert erwartungsgemäß;
- 69/69 Hub2-Render PASS;
- unbekannter Hub2 erzeugt keine alte Textschablone;
- 901/901 Assets gegenüber 1.50.678 byte-identisch;
- 69/69 eigene Hero-Pfade;
- 0 Welt-/Fallback-Heroes;
- 0 doppelte Hero-Pfade.

BILD-AUDIT:
- 19 Heroes 1600×853;
- 50 Heroes 600×320.

FOLGE:
Code/Text/Render ist lokal belastbar. Portalweiter visueller Bild-PASS bleibt offen, weil die 50 vorhandenen 600×320-Heroes im neuen Fullbleed-Einsatz real auf Schärfe gelesen werden müssen.

NEXT:
1.50.679 als Testkandidat installieren. Bei sichtbarer Unschärfe nur die betroffenen 600×320-Hero-Master ersetzen; Text- und Layoutlogik nicht erneut umbauen.


---

## PU-20261018-087 – HD-003 1.50.680 / wiederholten Releaseketten-Fatal aus 1.50.679 repariert

REALER BEFUND:
Nach Installation von 1.50.679 kritischer WordPress-Fehler.

EXAKTE URSACHE:
- Main → `Hobby_Depot_Profile_V150679`;
- V150679 `route_template()` → V150678-Templates;
- V150678-Templates → `Hobby_Depot_Profile_V150678`;
- aktive Versionskette damit gemischt.

KORREKTUR:
KISS, keine Funktionsänderung:
- Main 1.50.680;
- neue Profilklasse V150680 aus exakt V150679;
- Route auf neue Front-/Contenttemplates V150680;
- beide Templates rufen ausschließlich V150680.

DELTA:
- 1 Datei geändert: `pferde-template-kit.php`;
- 3 Dateien neu: Profilklasse + 2 Templates;
- 0 entfernt;
- 901/901 Bildassets identisch;
- Texte/Hero/Mega/Kategoriebaum unverändert.

QA:
- PHP 87/87 PASS;
- ZIP PASS;
- reale Front-Route PASS;
- reale Content-Route PASS;
- beide Templates positiv mit V150680 ausgeführt PASS;
- beide Templates negativ mit nur V150679 erwartungsgemäß FAIL;
- Paketdelta exakt geprüft.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.680_HOBBY_DEPOT_RELEASE_CHAIN_FATAL_FIX.zip`

SHA-256:
`ed34fece94970fc5be1ddd9c4116f1cb5029360a99515484a2656f19b307b40a`

NEXT:
1.50.680 installieren und realen WordPress-Frontend-Readback durchführen.


---

## PU-20261018-088 – HD-003 1.50.681 / Hero-Zoom entfernt, Bildformat vereinheitlicht, Kategorietext kompakter

REALER NUTZER-READBACK 1.50.680:
- Frontend wieder erreichbar;
- alle Hub2-Heroes optisch unscharf;
- Ursache: 600×320-Bilder wurden per Cover auf die komplette Hero-Fläche hochskaliert und zusätzlich gecroppt;
- Mobil zeigte dadurch einen anderen Ausschnitt als Desktop;
- Textinhalt akzeptiert, Darstellung darunter zu luftig.

ENTSCHEIDUNG:
- keine Bilddatei künstlich aufblasen;
- vorhandene 600×320-Bilder maximal nativ darstellen;
- ein Bildformat 600:320 für Desktop/Tablet/Mobil;
- vollständiger Bildausschnitt statt Zoom/Crop;
- größere Master nur herunterrechnen;
- sichtbarer Kategorietext als ein durchgehender Absatz ohne Leerzeile;
- kein Extra-Kasten und kein zusätzlicher Vorschautext; vorhandene ca. 45–64 Wörter reichen.

UMSETZUNG 1.50.681:
- zentrale Hero-CSS bereinigt statt weitere Zoom-Regel darüberzulegen;
- `object-fit:contain`;
- Bildbreite max. 600 px;
- gleicher 600:320-Container auf allen Breakpoints;
- Beige-Fade am linken Bildrand;
- Mobile-H1 darf umbrechen und wird nicht abgeschnitten;
- Hub2-Lead als ein `p`, Abstände reduziert, Chevron näher am Text.

DELTA:
- geändert: `pferde-template-kit.php`;
- neu: V150681-Profilklasse + Front-/Contenttemplate;
- entfernt: 0;
- 901/901 Assets byte-identisch;
- Textwortlaut unverändert.

QA:
- PHP 90/90 PASS;
- ZIP PASS;
- reale Front-/Contentroute V150681 PASS;
- Template positiv V150681 PASS;
- Template negativ mit nur V150680 erwartungsgemäß FAIL;
- 69/69 Hub2-Render PASS;
- Chromium-Inline-Sichtprüfung mit echten Assets bei 1440/1024/901/900/760/390 PASS;
- 600×320-Quellen nie breiter als 600 px;
- 1600×853-Master nur verkleinert;
- 600:320-Verhältnis auf Desktop und Mobil identisch;
- kein horizontaler Overflow.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.681_HOBBY_DEPOT_NOZOOM_COMPACT_TEXT.zip`

SHA-256:
`37ac20a8f6d00e6b3ab8501b186c3087867b0c397d4d33d0d14df1ae84b85e9d`

NEXT:
1.50.681 installieren und WordPress-Readback von Imkerei & Bestäuber plus zwei weiteren Hub2 auf Desktop/Mobil.


---

## PU-20261018-089 – HD-003 1.50.682 / Metall Alternative: Original-Kategorieszene + Weiß + Rahmen

NUTZERIDEE:
Eine einzelne Hub2-Kategorie als Gegenentwurf testen:
- dasselbe Originalmotiv wie beim Kategoriebild;
- links reines Weiß;
- kein Verlauf;
- kompletter Hero in dünnem Rahmen.

PRÜFUNG METALL:
- Kategorievorschau `metall-v150634.webp`: 200×107;
- per Bildvergleich als Ableitung aus `metall-v150627.webp`: 600×320 bestätigt;
- 1.50.681-Hero nutzte bereits diese Szene, verdeckte aber links einen großen Teil durch Copy/Fade-Überlagerung; dadurch wirkte das Motiv live gezoomt.

UMSETZUNG:
- nur Metall bekommt Pilotklasse `hd-hub2-alt-framed`;
- Heroquelle explizit `metall-v150627.webp`;
- keine Überlagerung/kein Fade;
- Weiß links;
- dünner 1-px-Außenrahmen;
- Desktop nebeneinander, Mobil gestapelt;
- sichtbarer Metall-Lead hart auf einen Absatz normalisiert.

QA:
- PHP 90/90 PASS;
- ZIP PASS;
- Releasekette/Route/Template positiv PASS;
- Negativ V150681 PASS;
- Dirty Overlay PASS;
- 901/901 Assets unverändert;
- Browser 1440/1024/901/900/390 PASS;
- Bild nativ 600×320, vollständig sichtbar, kein Upscaling;
- Fade aus;
- Text/Bild kein Overlap;
- Lead 1 p / 0 br / Margins 0.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.682_METALL_ALT_WHITE_FRAME_PILOT.zip`

SHA-256:
`4f9e23ff92aaeddcacc0c1f1b051c207a7b238b15dc53f2181de855099925b72`

NEXT:
Nur Metall live vergleichen. Keine Portalübertragung vor Nutzerentscheidung.


---

## PU-20261018-090 – HD-003 1.50.684 / Metall-Standard auf alle 69 Hub2 ausgerollt

NUTZERFREIGABE:
Metall 1.50.683 wurde für Hero-Bild und Text/Kartenwirkung abgenommen.

VERBINDLICHE BILDREGEL:
- aktuelles Hero-Prinzip bleibt;
- Claim + H1 + Kurzsatz links auf gleicher Höhe wie das Bild;
- pro Hub2 bestmöglichen Original-/Masterstand derselben vorhandenen Szenerie verwenden;
- horizontalen Bildinhalt erhalten;
- Hero nur durch oberen/unteren Beschnitt flacher machen;
- kein seitlicher Zoom/Crop;
- kein Upscaling;
- Mobil dieselbe Szene.

MASTERROLLOUT:
- 69/69 aktive Hub2 mit statischem Szenenmaster;
- 45 aus größeren wiedergefundenen Originalquellen derselben Szene;
- 19 aus bereits vorhandenen 1600×853-Heroquellen;
- 5 nur nativ 600 px vorhanden: saatgut-zucht, rollen-balance, wurf-ziel, team-wettkampf, geschick-tricks.
Für diese fünf: maximale Ausgabebreite 600 px, keine Vergrößerung.

KARTENUNTERTITEL:
- 328/328 aktuell vorhandene direkte Unterkategoriekarten erhalten eine eigene konkrete Kurzzeile;
- 328 Zeilen eindeutig;
- generische Welt-Fallbacks entfernt;
- keine Hub2-Fallbacktexte mit loslegen / ausprobieren / praktische Einstiege / pauschalem verstehen;
- spätere neue, noch nicht redigierte Karte: reale manuelle Kurzzeile oder leer, kein Generator-Fülltext.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.684_HOBBY_DEPOT_ALL_HUB2_SCENE_MASTER_CARDTEXT.zip`

SHA-256:
`2756075151e1996ceaa72e9057e85f1af42c181f6356867accae0ffbd43a8920`

QA:
- exakte 1.50.683-Basis;
- PHP 96/96 PASS;
- reale Front-/Contentroute V150684 PASS;
- beide aktiven Templates positiv mit V150684 ausgeführt PASS;
- Negativtest mit ausschließlich V150683 erwartungsgemäß FAIL;
- Dirty Overlay 1.50.683 → 1.50.684 PASS;
- 69/69 Hub2-Render PASS;
- 328/328 Kartenuntertitel PASS;
- alle 69 Masterdimensionen bei 1440/1180/1024/901 geprüft: 0 Upscaling, 0 seitlicher-Crop-Risiko;
- Browser mit realen Assets 1440/1180/1024/901/900/760/390: 42/42 PASS;
- 600-px-Sonderfall auch bei 900/760 nicht vergrößert;
- bestehende Bildassets 894/894 byte-identisch;
- Delta: 1 bestehende Datei geändert, 72 Dateien neu, 0 entfernt;
- ZIP PASS;
- Roundtrip 1136/1136 byte-identisch.

ZIELVERTRAG:
ZV-HOBBYRAUSCH-DESIGN-001 auf Fassung 4.9 nachgezogen.

NEXT:
1.50.684 installieren und WordPress-Readback über mehrere Hub2/Welten. Kein weiterer Architektur- oder Textumbau vor diesem Readback.


---

## PU-20261018-091 – HD-003 1.50.685 / echte Hero-Szenerie sichtbar erhalten

LIVE-BEFUND 1.50.684:
Keramik & Glas zeigte trotz korrektem Szenenmaster weiterhin einen optisch vergrößerten/engen Hero-Ausschnitt.

URSACHE:
Nicht die Bildquelle war falsch. Der Master enthielt die volle horizontale Szene. Aber der linke Textblock plus 130–170 px Übergang verdeckte einen zu großen Teil des rechts liegenden Bildes. Dadurch wirkte die verbleibende sichtbare Szene erneut wie hineingezoomt.

FIX:
- Bildfeld ca. 72 % des Hero;
- native Breite bleibt harte Obergrenze;
- keine Bilddatei geändert;
- horizontaler Inhalt vollständig;
- nur oben/unten Crop;
- Übergang Desktop auf ca. 64 px reduziert;
- 901–1180 px auf ca. 56 px reduziert;
- Mobil unverändert vollständiges Masterverhältnis.

KERAMIK-&-GLAS-PFLICHTTEST:
Original 1672×941 → Master 1672×614 nur vertikal beschnitten.
1440/1180/1024/901: 0 Seitencrop, 0 Upscaling.
900/760/390: gleiche vollständige Szene.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.685_HERO_SCENE_VISIBILITY_FIX.zip`

SHA-256:
`a72b7baa257b09d3fc2f4112bdcb25e03bdbe8d6d120ae0d60764ee53f6c7b1e`

QA:
- PHP 99/99 PASS;
- Route/Template V150685 positiv PASS;
- V150684-Negativtest PASS;
- 69/69 Hub2-Render PASS;
- 276/276 Desktop-Geometriechecks PASS;
- 49/49 Browserfälle PASS;
- ZIP PASS;
- Roundtrip 1139/1139 PASS;
- Delta zu 1.50.684: 1 geändert, 3 neu, 0 entfernt.

ZIELVERTRAG:
Fassung 5.0.

NEXT:
1.50.685 installieren; zuerst Keramik & Glas real prüfen.


---

## PU-20261018-092 – HD-003 1.50.686 / Kettenhemdflechten Pilot für nächste Ebene

NUTZERENTSCHEIDUNG:
Die nächste Ebene soll kompakter werden. Als Pilot dient Kettenhemdflechten:
- kein Hero-Bild;
- oben mittig Icon + H1 + hochwertiger aufklappbarer Text;
- Unterkategorien testweise im 4er-Raster;
- Affiliate-Produkte/Banner früher zwischen den Inhalten;
- Beitragsvorschauen bleiben.

UMSETZUNG:
- 162-Wörter-Fachtext, davon 45 sichtbar;
- 8 Unterkategorien mit individuellen Kurzzeilen;
- Reihenfolge:
  4 Unterkategorien → category_product_1..3 → 4 Unterkategorien → product_after_category_tiles → 3 Beiträge → bestehender Werbeplatz;
- Desktop 4er-Raster, Tablet 2er, Mobil 1er;
- keine neuen Affiliate-Slotnamen erfunden.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.686_KETTENHEMDFLECHTEN_MIXED_LEVEL_PILOT.zip`

SHA-256:
`0fef7c270977c01e986adf82ee00f56b5602f699e12799fb18cfc1c28b919e4d`

QA:
- PHP 102/102 PASS;
- ZIP PASS;
- Main/Profil/Route/Templates V150686 PASS;
- positive Templateausführung PASS;
- V150685-Negativtest erwartungsgemäß FAIL;
- echter Pilotrender: kein Hero, 1 H1, 8 Karten;
- Reihenfolge der Module PASS;
- Browser 1440/1024/390 ohne Overflow;
- Delta zu 1.50.685: 1 geändert + 3 neu + 0 entfernt;
- Roundtrip 1142/1142 byte-identisch.

NEXT:
1.50.686 installieren und nur Kettenhemdflechten real prüfen. Keine Portalübertragung vor Abnahme.


---

## PU-20261018-093 – HD-003 1.50.687 / Detail-Ebene portalweit + zentrale Icons + Kettenhemd-Dummybeiträge

NUTZERFREIGABE:
Kettenhemdflechten 1.50.686 auf den ersten Blick okay. Pilotdesign auf alle Kategorien derselben logischen Ebene ausweiten.

ZUSATZENTSCHEIDUNG:
Icons der letzten Kategorieebene zentral semantisch steuern. Gleiche Themenrolle portalweit = gleiches Icon. Beispiel FAQ überall gleich. Aktuelle zufällige/unpassende Icons verwerfen.

SCOPE:
- 379 Page-Knoten derselben Ebene wie Kettenhemdflechten;
- 16 direkte Category-Term-Knoten derselben logischen Ebene;
- 395 Detail-Hubs insgesamt;
- 2.979 letzte Kategorien unter den 379 Pages.

DESIGN:
- kein Hero-Bild;
- mittiger Icon-/H1-/Textkopf;
- 150–200 Wörter;
- 45–62 Wörter sichtbar, Rest Chevron;
- 4er-Raster Desktop, 2 Tablet, 1 Mobil;
- erste 4 Unterkategorien → vorhandene Kategorie-Produkte → restliche Unterkategorien → vorhandener Banner → bis zu 4 Beiträge → vorhandener weiterer Werbeplatz.

TEXT:
- 395/395 Texte;
- 150–170 Wörter;
- 395/395 Volltexte unterschiedlich;
- Fachnachprüfung vor Release insbesondere für Genuss/Fermentation und Tierbereiche.

ICONS:
- zentrale Rollenregistry;
- FAQ, Vergleich, Grundlagen, Ausrüstung, Werkzeuge, Material, Sicherheit, Pflege, Dokumentation, Klima, Futter, Standort, Technik, Projekt/Finish usw.;
- kein Hash-/Zufallsprinzip;
- unbekannte Rolle fällt fachlich auf Eltern-/Themenkontext zurück.

KETTENHEMDFLECHTEN DUMMYPOSTS:
- 4 veröffentlichte Layout-Testbeiträge;
- 4 passende Unterkategoriezuordnungen;
- 4 Featured Images;
- Seeder idempotent;
- Vorschauabfrage Limit 4 aus direkten Unterkategorien.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.687_CATEGORY_LEVEL_ROLLOUT_ICONS_DUMMY_POSTS.zip`

SHA-256:
`9a881f3b3b7cf25ab2cfdc5f9a2c62b878fa5cc7513ba8678524f98b7464235b`

QA:
- PHP 105/105 PASS;
- reale Front-/Contentroute V150687 PASS;
- beide Templates positiv PASS;
- Negativtest V150686 PASS;
- Kettenhemd-Render PASS;
- zentrale Iconrollen geprüft;
- Copy-Coverage 395/395;
- 4/4 Dummybeiträge/Kategorien/Bilder PASS;
- Seeder zweiter Lauf ohne Duplikate PASS;
- Delta zu 1.50.686: 1 bestehende Datei geändert + 4 neu + 0 entfernt;
- Dirty Overlay 1.50.686 → 1.50.687 PASS;
- ZIP PASS;
- Roundtrip 1146/1146 byte-identisch.

ZIELVERTRAG:
ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.1.

NEXT:
1.50.687 installieren. Zuerst Kettenhemdflechten mit 4 Beitragsvorschauen und zentralen Icons prüfen, danach zwei weitere Detail-Hubs derselben Ebene.


---

## PU-20261018-094 – HD-003 1.50.688 / Kettenhemd-Kacheln klarer, kürzer, ohne H1-Dopplung

NUTZERBEFUND:
- `Weiter in Kettenhemdflechten` direkt unter H1 `Kettenhemdflechten` wirkt doppelt/holprig;
- Kacheltitel und Untertitel zu klein;
- Untertitel enthalten unnötige Endungen wie `sicher kennenlernen`, `sinnvoll zusammenstellen`, `praktisch einsetzen`, `richtig auswählen`;
- `Passende Ausrüstung` passt als Überschrift nicht zu jeder Kategorie;
- sichtbare Kurztexte dürfen niemals klein beginnen;
- H1 soll sichtbar natürlich `Kettenhemd flechten` statt zusammengeschrieben wirken;
- Meta-Titel später separat, jetzt ausdrücklich nicht verändern.

UMSETZUNG:
- gespeicherter WP-Titel/Slug/URL unverändert;
- sichtbare Kettenhemd-H1 zweizeilig: `Kettenhemd` / `flechten`;
- Kettenhemd-Kachelabschnitt: `Rund ums Kettenhemd`;
- andere Detail-Hubs: neutral `Themen im Überblick`, solange keine natürlich redigierte Kurzform gebunden ist;
- Produktabschnitt detail-level: `Empfehlungen`;
- Karten min. 98 px, größere ruhige Icons, Titel 16 px, Untertitel 12,5 px;
- dezente stärkere Kontur/Schatten, kein schrilles Design;
- Kettenhemd-Unterzeilen auf Sachkern gekürzt;
- FAQ-Frontendlabel `Häufige Fragen`;
- zentrale Ausgabeprüfung hebt den ersten Buchstaben sichtbarer Kurztexte an; eBay/iPhone/iPad ausgenommen.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.688_KETTENHEMD_CARD_REFINEMENT.zip`

SHA-256:
`a57ba6a8ec158191276673d309825787cfc0ec6d0c192bed358a97e193cac843`

QA:
- PHP 108/108 PASS;
- V150688 Front-/Contentroute PASS;
- Templates positiv PASS;
- Negativtest nur V150687 erwartungsgemäß FAIL;
- Render: H1-Split / Rund ums Kettenhemd / 8 Karten / Häufige Fragen / Kurztexte PASS;
- Füll-Endungen im Kettenhemd-Kartenpfad 0;
- Großschreibung Negativfall PASS;
- Delta: 1 bestehende Datei geändert + 3 neu + 0 entfernt;
- ZIP PASS;
- Roundtrip 1149/1149 byte-identisch.

NEXT:
1.50.688 installieren und Kettenhemd-Seite visuell prüfen. Meta-Titel erst im danach geplanten eigenen SEO-Schritt.


---

## PU-20261018-095 – HD-003 1.50.689 / Kettenhemd Reihenfolge + H1 einzeilig

NUTZERENTSCHEIDUNG:
- Banner direkt unter den Introtext;
- alle 8 Kacheln ohne Produktunterbrechung zusammenhalten;
- Produkte/Empfehlungen erst unter den Kacheln;
- passende Beiträge danach;
- H1 `Kettenhemd flechten` ohne Umbruch.

SCOPE:
Nur Kettenhemd-Pilot. Meta-Titel, WP-Titel/Slug/URL, Hub2 und andere Detail-Hubs bleiben unverändert.

AUSLIEFERUNG:
`HOBBY_DEPOT_TEMPLATE_KIT_UPDATE_1.50.689.zip`
- einmaliger fail-closed Delta-Updater für exakt 1.50.688;
- Backup der angefassten 1.50.688-Dateien;
- V150689 Profil + Front-/Contenttemplate neu;
- Main erst nach erfolgreichem Schreiben umgestellt;
- Readback und Selbst-Deaktivierung.

QA:
- ZIP integrity PASS;
- PHP lint PASS;
- hard assertions PASS;
- GitHub Actions Run 39139756377 SUCCESS.

NEXT:
Delta installieren/aktivieren; danach Kettenhemd real prüfen: Banner → 8 Kacheln → Empfehlungen → Beiträge und einzeilige H1.


---

## PU-20261018-095 – HD-003 1.50.690 / abgenommenen Kettenhemd-Ablauf auf Detail-Seitenrenderer ausrollen

NUTZERFREIGABE:
Kettenhemd flechten 1.50.689 = PASS.

ABGENOMMENER STANDARD:
- Banner direkt unter dem Text;
- Unterkategorien ohne Affiliate-Unterbrechung als geschlossener Block;
- Affiliate-Produkte/Empfehlungen erst danach;
- danach 3–4 passende Beiträge;
- sichtbare Kettenhemd-H1 ohne künstlichen Umbruch.

UMSETZUNG:
- One-shot-Updater auf harter Basis 1.50.689;
- Kettenhemd-only-Bedingung im gemeinsamen `render_category_level_body_v150687` wird exakt einmal entfernt;
- damit gilt der abgenommene Ablauf für alle WP_Post-basierten Detail-Hubs dieses Renderers;
- neue Profil-/Templatekette V150690;
- Backup + Readback + Selbstdeaktivierung.

ARTEFAKT:
`HOBBY_DEPOT_TEMPLATE_KIT_UPDATE_1.50.690.zip`

SHA-256:
`fcbc01893df451e56527cdcf90e6f7364cfa24d7afbc4556b69bc9b215c19809`

QA:
- PHP lint PASS;
- Build/Hard assertions PASS;
- ZIP integrity PASS;
- 1.50.689-Preflight PASS in Source-Contract;
- Runtime-Replacement count muss exakt 1 sein;
- 1.50.690-Readback-Hardchecks eingebaut.

NICHT GERATEN:
Die 16 zusätzlich dokumentierten direkten Category-Term-Knoten werden nicht ohne verifizierten Term-Renderer als PASS behauptet. Nach Installation einen solchen Term-Fall real lesen.

ZIELVERTRAG:
ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.2.

NEXT:
1.50.690 installieren; zwei andere Detail-Hubs + einen direkten Category-Term-Fall prüfen.


---

## PU-20261018-096 – HD-003 1.50.691 / vollständiges normales Template-Kit statt One-shot-Updater

NUTZERENTSCHEIDUNG:
Die Startseitenänderung soll als normales Affiliate Portal Template Kit installiert werden, damit WordPress den bestehenden Pluginordner regulär ersetzen/überschreiben kann. Kein separates Einmal-Plugin.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.691_STARTSEITE_RUHIGE_WELTBILDER.zip`

SHA-256:
`984356b9eaadb6ad2954c14bb026d4a380afdf00e06caccef5bec5be2f7288b0`

UMSETZUNG:
- vollständiger Pluginroot `affiliate-portal-template-kit/`;
- 1.50.689 Kettenhemd-Änderung enthalten;
- 1.50.690 Detail-Level-Rollout enthalten;
- aktive Kette auf V150691;
- 8 neue ruhige Startseiten-Weltbilder;
- Startseitenkarten auf neue Bildquelle umgestellt;
- Hauptkategorie-Heros ausdrücklich unverändert;
- bestehender Querbanner direkt hinter die acht Hobbywelten verschoben.

QA:
- PHP 117/117 PASS;
- ZIP PASS;
- Releasekette V150691 PASS;
- Front-/Contenttemplates V150691 PASS;
- Hero-Funktion gegen rekonstruierten 1.50.690-Stand unverändert;
- Roundtrip 1166/1166 byte-identisch.

NEXT:
Vollpaket 1.50.691 regulär über das bestehende Affiliate Portal Template Kit installieren und Startseite prüfen.


---

## PU-20261018-097 – HD-003 1.50.692 / Schuhmacherei-Textpilot

AUFTRAG:
Vor dem Gesamtrollout einen realen Musterfall zeigen, der die verschärften Textregeln beweist.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.692_SCHUHMACHEREI_TEXT_PILOT.zip`

SHA-256:
`c9a45879b268c60d2d825be0225bfe0d1e03f37f219dd6282498c53b75e2d86a`

UMSETZUNG:
- vollständiges normales Template Kit auf Basis 1.50.691;
- nur Schuhmacherei als Pilot;
- neuer 51-Wort-Lead: Was ist das Hobby, was macht man, was ist typisch;
- 164 Wörter Gesamttext ohne Navigations-/Generatorphrasen;
- Überschrift `Mehr zur Schuhmacherei`;
- neun fachlich konkrete Kacheluntertitel;
- heller Petrolblock für den sichtbaren Lead;
- keine Änderung an Startseitenbildern, Hauptkategorie-Heros oder übrigen Hobbytexten.

QA:
PHP 120/120 PASS, ZIP PASS, V150692-Kette PASS.

NEXT:
Schuhmacherei live abnehmen, danach erst Gesamtbestand nach derselben redaktionellen Logik neu schreiben.


---

## PU-20261019-098 – HD-003 Abschluss-Nachprüfung 1.50.692 / Hard-E2E-Lücke erkannt

ANLASS:
Abschluss-/Nachholprüfung vor Chatübergabe.

BEFUND:
1.50.692 ist als Schuhmacherei-Textpilot mit PHP-120/120, ZIP-PASS und aktiver V150692-Kette dokumentiert. Ein vollständiger lokaler Positiv- UND Negativ-E2E-Nachweis des real relevanten Renderpfads ist jedoch nicht dokumentiert.

FOLGE:
Nach der projektweiten Hard Rule darf 1.50.692 noch nicht als Upload-/Deploymentkandidat oder PASS ausgegeben werden.

KORREKTUR:
- Design-Current und HD-003-Current auf genau diesen Blocker und genau eine NEXT ACTION gekürzt;
- Zielvertrag auf Fassung 5.4 nachgezogen;
- Textfehler HRD-074 / AF-051 dauerhaft dokumentiert;
- isoliertes Manifest auf 1.50.692 nachgezogen;
- CURRENT.zip bewusst nicht synchronisiert.

NEXT:
Realen Schuhmacherei-Pfad lokal positiv und negativ E2E simulieren; erst nach PASS Plugin ausgeben und isolierte Ausgabe synchronisieren.


---

## PU-20261019-099 – HD-003 1.50.693 / 395er Detail-Text- und Kachelrollout

AUFTRAG:
Nach bestätigtem Schuhmacherei-Muster dieselbe Ebene vollständig nach den verschärften Textregeln ausrollen; Kacheluntertitel gleichzeitig kürzen.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.693_DETAIL_TEXT_ROLLOUT_LOCAL_HARD_PASS.zip`

SHA-256:
`558a345042c9acaa488b01ce543c2f9d7defc4406f5243ee17f90b4363975d54`

UMSETZUNG:
- 395/395 Detail-Hubs;
- sichtbarer Lead 45–60 Wörter;
- aufklappbarer Vertiefungstext 150–187 Wörter zusätzlich zum Lead;
- zwei Absätze je Vertiefungstext;
- direkte du-Ansprache bzw. natürliche direkte Imperativsprache;
- keine verbotenen Generator-/Füllphrasen;
- interne Textdoppelungen gezielt entfernt;
- semantische Fehlübernahmen aus Zwischenständen korrigiert;
- Kacheluntertitel auf kurze konkrete Inhaltsaussagen reduziert;
- Schuhmacherei-Lead unverändert;
- Startseiten-Weltbilder und Hauptkategorie-Heros unverändert.

QA:
- 395/395 Regel-/Längen-/Absatzcheck PASS;
- interner Wiederholungscheck 0 Fehler;
- PHP 123/123 PASS;
- Schuhmacherei Positivpfad PASS;
- Airbrush Kontroll-/Negativpfad PASS;
- direkter Category-Term PASS;
- V150693 Release-/Templatekette PASS;
- 8/8 Startseiten-Weltassets byte-identisch PASS;
- ZIP-Integrität PASS.

LIVE-GRENZE:
Kein Live-PASS. Echter WordPress-Frontend-Readback steht aus.

NEXT:
1.50.693 regulär installieren und repräsentative Detail-Hubs plus direkten Category-Term live prüfen.


---

## PU-20261019-100 – HD-003 1.50.695 / vollständiger 395er Benchmark-Textrollout

AUFTRAG:
Nach Freigabe von 1.50.694 als redaktionelle Benchmark den gesamten Detail-Hub-Bestand fertigstellen, ohne die Generatorfehler aus 1.50.693 zu übernehmen.

BENCHMARK:
- 1.50.694;
- insbesondere Bromelien, Tillandsien, Kakteen, Sukkulenten, Lithops, Hydrokultur, Mooskultur und fleischfressende Pflanzen;
- diese Benchmarktexte bleiben im finalen Bestand exakt unverändert.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.695_FULL_TEXT_ROLLOUT_LOCAL_PASS.zip`

SHA-256:
`8afd735e7cdd918e2daa60c62dbd5a029b168d8b06e6fd566c56fc0758dc6f8a`

UMSETZUNG:
- 395/395 Detail-Hubs;
- sichtbarer Lead 45–60 Wörter;
- unbekannte Begriffe direkt erklärt;
- Aufklapptext 150–193 Wörter zusätzlich zum Lead;
- zwei Absätze je Vertiefung;
- natürliche direkte Ansprache;
- heller Petrol-/Türkisblock allgemein;
- Kacheluntertitel nur mit echtem Zusatznutzen;
- kein `Themen im Überblick`-Fallback;
- Schuhmacherei-Lead unverändert.

QA:
- 10/10 Pilot-/Benchmarktexte exakt unverändert;
- 0 verbotene Generator-/Füllphrasen;
- 0 doppelte erste Sätze;
- 0 identische Sätze auf 3+ Seiten;
- 0 Custom-Untertitel-Echos;
- PHP 123/123 PASS;
- repräsentativer Render-Harness über alle 8 Welten PASS;
- 971/971 bestehende Bilddateien byte-identisch zu 1.50.694;
- ZIP-Integrität PASS.

LIVE-GRENZE:
Kein Live-PASS. Echter WordPress-Frontend-Readback von 1.50.695 steht aus.

NEXT:
1.50.695 regulär installieren und repräsentative Detail-Hubs aus allen 8 Welten sowie einen direkten Category-Term live prüfen.


---

## PU-20261019-100 – HD-003 1.50.696 / Schrift & Lettering Hub2-Pilot

AUFTRAG:
Das bestätigte Text-/Gestaltungsprinzip der Detail-Hubs auf die direkt darüberliegende Hub2-Ebene übertragen, zunächst als vollständiger Pilot für Schrift & Lettering.

UMSETZUNG:
- 1.50.695 als technische Basis;
- Schrift & Lettering sichtbarer Kurzüberblick neu: 51 Wörter, direkte Erklärung von Thema, Tätigkeit, Werkzeugen und Reiz;
- Kurzüberblick im hellen Petrol-/Türkisblock;
- vorhandenen guten Langtext redaktionell genutzt/ergänzt und auf 152 Wörter in exakt zwei Absätze gebracht;
- Aufklapper rendert explizite Absätze;
- reale direkte Kinder geprüft: Federkiel-Schreiben, Kalligrafie, Lettering;
- alle drei Untertitel liefern ergänzende Information statt Titelwiederholung;
- keine anderen Hub2-Texte geändert.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.696_SCHRIFT_LETTERING_PILOT.zip`

SHA-256:
`937cc9c90a2663e8c03ae4e78ca30cc998a09c33880ac508cf59fde541402ba2`

QA:
- Lead 51 Wörter PASS;
- Aufklapptext 152 Wörter / 2 Absätze PASS;
- positive Renderprüfung Schrift & Lettering PASS;
- negative Kontrollseite Papierkunst PASS;
- 3/3 reale Unterkacheln + Untertitel PASS;
- 68 andere Hub2-Editorialtexte unverändert PASS;
- 395er Detailtextmap unverändert PASS;
- 983/983 Assets byte-identisch PASS;
- PHP 126/126 PASS;
- ZIP PASS.

LIVE-GRENZE:
Kein Live-PASS. Nutzer-Sichtprüfung steht aus.

NEXT:
1.50.696 regulär installieren und die vollständige Kategorie Schrift & Lettering prüfen; bei Zustimmung Rollout auf übrige Hub2-Kategorien.


---

## PU-20261019-101 – HD-003 1.50.697 / kompletter Hub2-Text- und Grafikrollout

NUTZERFREIGABE:
Schrift & Lettering 1.50.696 = perfekte Benchmark. Auftrag: exakt dieses Prinzip auf alle Kategorien derselben Ebene ausrollen; Grafik- und Textregeln beachten.

UMSETZUNG:
- 69/69 Hub2-Kategorien;
- sichtbarer Kurzüberblick 45–60 Wörter;
- direkte Erklärung von Thema, Tätigkeit, Voraussetzungen/Material und Reiz;
- Petrol-/Türkis-Kurzblock portalweit auf Hub2;
- Aufklapptext 150–175 Wörter;
- 69/69 exakt zwei Absätze;
- natürliche direkte Ansprache;
- keine Seiten-/Kurs-/Generatorfloskeln;
- bestehende gute Langtextsubstanz erhalten und nur dort ergänzt/überarbeitet, wo Länge oder Regelkonformität es verlangten;
- 379 direkte Kindseiten vollständig geprüft;
- fehlende konkrete Kacheluntertitel ergänzt;
- 0 reine Titelwiederholungen.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.697_HUB2_TEXT_ROLLOUT_LOCAL_PASS.zip`

SHA-256:
`ac42f7fb06d8aaf7f08709b5362b911c717d35ba7d9b582c50cfa5999b5a5ec0`

QA:
- 69/69 Hub2-Renderharness PASS;
- 379/379 Subtitle-Renderharness PASS;
- Lead 45–60 PASS;
- More 150–175 PASS;
- 2 Absätze 69/69 PASS;
- verbotene Meta-/Generatorphrasen 0;
- doppelte erste Sätze 0;
- exakte Satzdoppelungen ab 3 Texten 0;
- 6-Wort-N-Gramm-Gruppen ab 4 Texten 0;
- Absatzstart-Gruppen ab 3 Texten 0;
- PHP 129/129 PASS;
- 983/983 Assets byte-identisch zu 1.50.696;
- 395er Detailtextdatei byte-identisch;
- ZIP PASS.

LIVE-GRENZE:
Kein Live-PASS vor echter WordPress-Sichtprüfung.

NEXT:
1.50.697 installieren und repräsentativ mehrere Hub2 aus allen acht Welten live prüfen.


---

## PU-20261019-102 – HD-003 1.50.698 / Hub2-Einstiege an Detail-Hub-Benchmark angeglichen

KORREKTURGRUND:
1.50.697 erfüllte Wortzahl, Absatz- und Anti-Floskeltests, aber mehrere sichtbare Hub2-Leads begannen zu früh mit Fachdetails. Für inspirationssuchende Nutzer fehlte teilweise der unmittelbare Überblick: Was ist das Themenfeld, was macht man dort und warum könnte es interessant sein?

BENCHMARK:
- freigegebene Pflanzen-Texte aus 1.50.694;
- bestätigte Schrift-&-Lettering-Übertragung aus 1.50.696;
- autoritative Textregel frisch gelesen.

UMSETZUNG:
- 69/69 sichtbare Hub2-Leads redaktionell neu geprüft;
- keine Fragenliste, kein neues starres Schema;
- jeder Lead funktioniert als natürlicher Einleitungsabsatz für Nutzer ohne Vorwissen;
- 47–58 Wörter;
- direkte Ansprache 69/69;
- gute bestehende Aufklapptexte erhalten;
- 35 nützliche Fachinformationen aus dem bisherigen Lead ausdrücklich in den Aufklapper verschoben, damit durch die stärkere Einleitung nichts verloren geht;
- Aufklapper danach 150–192 Wörter und weiterhin exakt 2 Absätze;
- Grafik unverändert: Petrolblock wie 1.50.696.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.698_HUB2_INTRO_BENCHMARK.zip`

SHA-256:
`b665cf5c782bb8835ec923ccb1289e2ff7355b5e57bc0073a38025903a61969c`

QA:
- Runtime-Reflection 69/69 PASS;
- verbotene Phrasen 0;
- Fragezeichen in Leads 0;
- doppelte erste Sätze 0;
- 6-Wort-N-Gramme 4+ 0;
- PHP 132/132 PASS;
- 395er Detailtextbestand unverändert;
- 983/983 Assets unverändert;
- ZIP PASS.

LIVE:
Noch kein Live-PASS.


---

## PU-20261019-103 – HD-003 1.50.698 Abschluss-/Nachholprüfung

ANLASS:
Abschlussprüfung vor Chatübergabe nach HOBBYRAUSCH-Hard-Rule.

FRISCHECHECK:
- START_HERE und Autoritätsplan frisch gelesen;
- zuständige Current-Autorität: `PROJEKTE/HOBBYRAUSCH/DESIGN/CURRENT_STATE.md`;
- Plugin-Wahrheit: `PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md`;
- lokales Artefakt 1.50.698 und Evidence frisch geprüft.

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.698_HUB2_INTRO_BENCHMARK.zip`
SHA-256:
`b665cf5c782bb8835ec923ccb1289e2ff7355b5e57bc0073a38025903a61969c`
Größe:
58,537,086 Bytes.

FRISCHE QA:
- ZIP-Integrität PASS;
- Plugin-Version/Releasekette 1.50.698 PASS;
- Runtime-Editorial-Audit 69/69 PASS;
- POS: Schrift & Lettering nutzt Hub2-Editorialpfad → PASS;
- NEG: Bromelien wird nicht als Hub2 behandelt → PASS;
- NEG: unbekannter Slug fail-closed → PASS;
- PHP 132/132 PASS;
- Benchmarkdatei 1.50.694 SHA-256 `e96c697721549f049d1001592823443186ef649c427c5d3e99ae745297a156e1`;
- 395er Detailtextdatei SHA-256 `18bce1b3597cc84fb60399883fc8bbb3696c110573a41162b5198665fa7b253d`;
- 983 Assets gegenüber 1.50.697 unverändert.

FORMALER ARTEFAKTPUNKT:
Im GitHub-Campus-Verzeichnis `ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/` liegt weiterhin nur `MANIFEST.md`; ein `CURRENT.zip` ist dort nicht vorhanden. Der belastbare lokale 1.50.698-ZIP ist vorhanden und geprüft, konnte in dieser Sitzung aber nicht als 58,5-MB-Binärdatei über den verfügbaren Text-/Connector-Schreibweg in den Campus synchronisiert werden. Dies ist ein formaler Plugin-Artefakt-Sync-Restpunkt, kein inhaltlicher/technischer Fehler des ZIPs.

LIVE:
Kein Live-PASS. Echter WordPress-/Frontend-Readback bleibt offen.
