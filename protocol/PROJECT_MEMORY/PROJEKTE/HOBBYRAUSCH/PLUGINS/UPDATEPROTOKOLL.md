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
