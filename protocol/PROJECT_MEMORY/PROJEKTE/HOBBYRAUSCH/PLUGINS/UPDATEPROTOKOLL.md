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
