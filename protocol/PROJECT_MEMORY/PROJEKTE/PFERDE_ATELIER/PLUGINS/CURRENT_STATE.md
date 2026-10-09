## PLUGIN-/PERFORMANCE-CURRENT 2026-10-09 – FRISCH GEBUNDEN 6.72.211 BLOCK 8

**Dieser Block supersediert alle später in dieser Datei verbliebenen historischen Affiliate-/Performance-NEXT-ACTION-Blöcke.**

### Aktueller belastbarer Stand

Technische Affiliate-Current frisch geprüft:
- technische Autorität: `affiliate-release-current:control/release-governance/CURRENT_RELEASE.json`;
- Generation **304**;
- Affiliate-Zentrale **6.72.211 CANDIDATE_LOCAL_HARDTEST_PASS**;
- `release_allowed=false`;
- Source-Manifest **9f15bf679f44456c18c32aa6e04504e87248bc2748cfbca880532318915d311f**;
- letzter Source-Implementierungsstand: `164cb789abcbfcffe70975fd463182041c5c923a`;
- nachfolgende Affiliate-Branch-Änderung betrifft nur Fehlerprotokoll-Nachholung, keinen Plugin-Source.

Gebündelter Affiliate-Performanceblock bis **Block 8**:
- AFF-ERR-064 lokal behoben;
- fremde AJAX-Requests: Affiliate-Hooks **207 → 75**;
- doppelte öffentliche Frontend-Campaign-Abfrage **2 → 1**;
- wiederholte Campaign-Meta-Normalisierung halbiert;
- Content-Context und Kategorie-Context request-lokal wiederverwendet;
- Admin-/Workerpfade unverändert;
- PHP-Lint **22/22 PASS**;
- lokale Positiv-/Negativ-/Regressionsevidence **PASS**:
  `release/affiliate-zentrale/evidence/affiliate_router_v672211_frontend_context_cache_block8_20261008.md`.

Unverändert:
- keine Architekturänderung;
- keine Workflowänderung;
- keine Änderung an Ranking, Provider-Auswahl, Slots, Veto, Publish, Kategorie, Design oder Tracking;
- kein Release;
- keine Installation.

Der **exakte WordPress/MariaDB-Gate für genau diesen 6.72.211-Manifeststand ist OPEN**. Historische Actions-Runner 6.72.170/171/210 brechen vor WordPress an ihren fest verdrahteten Altversionsprüfungen ab und sind kein gültiger aktueller Gate; sie werden nicht umgebaut.

Template-Kit **1.50.578** bleibt als aktiver WordPress-Readback belegt. Der vollständige aktuelle Source ist weiterhin nicht autoritativ gebunden; Template-Dateien bleiben unangetastet.

### ERSTER OFFENER BLOCKER

**Exact 6.72.211 / Manifest 9f15bf… noch nicht im echten WordPress-7.1.2/MariaDB-10.11-Positiv-/Negativ-/Regressionstest durchgelaufen.**

### GENAU EINE NEXT ACTION

`RUN_EXACT_6_72_211_WORDPRESS_MARIADB_POS_NEG_REGRESSION_WITHOUT_WORKFLOW_CHANGE`

Bis PASS:
- kein Release;
- keine Installation;
- keine weitere Affiliate-Version;
- keine Template-Änderung;
- keine neue Test-/Workflowarchitektur.

---

## PLUGIN-/PERFORMANCE-CURRENT 2026-10-08 – FRISCHECHECK / NEUER GEBÜNDELTER OPTIMIERUNGSSCOPE

### Geltende Autoritäten

- Zielvertrag für Aufräumen/DB/Performance: `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/ZV-PLUGINS-CLEANUP-001.md`.
- ergänzender Performance-Zielvertrag: `affiliate-release-current:protocol/AFFILIATE_RELEASE_PERFORMANCE_OPTIMIZATION_TARGET_20260924.md`.
- Affiliate-Fach-/Releasewahrheit bleibt ausschließlich:
  `affiliate-release-current:control/release-governance/CURRENT_RELEASE.json`.
- Affiliate-Fehlerwahrheit:
  `affiliate-release-current:protocol/AFFILIATE_RELEASE_ERROR_REGISTER.md`.
- Performance-WAS/WARUM-/Arbeitsprotokoll:
  `affiliate-release-current:protocol/AFFILIATE_RELEASE_PERFORMANCE_CLEANUP_PROTOCOL_20260922.md`.
- TEXT-/PSTE-/PSERC-Status bleibt ausschließlich im zuständigen TEXT-Current; dieser Block erzeugt dafür keine zweite Wahrheit.

### Frischer belastbarer Stand

Affiliate-Current frisch gelesen:
- Generation **296**;
- Affiliate-Zentrale **6.72.210 RELEASED**, `release_allowed=true`;
- finaler Installer SHA-256 `43ca6033a0f8dc929f777fc6580f2b41dfd711c6f561db99658f402cc5af88a1`;
- Source-Manifest `8b3552ff93d482525e41bd0d279a609d8dd538bf672313ba29574a07f33992bf`;
- formaler Release-Check Run `37788785260` PASS.
Die technische Affiliate-Releasewahrheit wird hier **nicht kopiert oder ersetzt**; für jede spätere Änderung muss die technische Current erneut frisch gelesen werden.

Letzter expliziter Template-Kit-WordPress-Readback in diesem Büro:
- Affiliate Portal Template Kit **1.50.578 aktiv**.

Aktueller Performance-Readback 08.10.2026:
- `/ausruestung/`: 420 Queries / 1,557568 s;
- `/stall/`: 419 / 1,660128 s;
- `/weide/`: 419 / 1,586224 s;
- `.../pferdesaettel/`: 654 / 2,948636 s.
Gegen 01.10. sind die Queryzahlen deutlich höher (302/299/302/320), die Laufzeit aber nicht überall schlechter; Pferdesättel ist schneller. Deshalb kein Queryzahl-Fix auf Verdacht.
Der Diagnosemodus besitzt keine owner-genaue SQL-Aufschlüsselung (`db_query_timing.available=false`) und meldet keinen persistenten Object Cache.

Header-/AJAX-Suche:
- reale Verlangsamung vom Nutzer bestätigt;
- Relevanssi Live Ajax Search war aktiv;
- Haupt-Relevanssi wurde testweise wieder installiert/aktiviert;
- **keine erkennbare Geschwindigkeitsverbesserung**;
- fehlendes Relevanssi ist damit nicht als Hauptursache belegt;
- Suchursache weiter offen, keine Kausalbehauptung.

Affiliate:
- neuer realer Fehler `AFF-ERR-064`: `Undefined variable $required_creative_type` in aktuellem Renderer;
- Current-6.72.210-Source bestätigt fehlende lokale Initialisierung in `render_affiliate_slot_for_context()`;
- noch **kein Fix**, kein Installer, kein PASS.

### Nutzer-Hardlock für den neuen Scope

Komplettes praktisch sinnvolles Optimierungspotential umsetzen, einschließlich möglicher Template-Änderungen/-Löschungen, aber:
- **keine Rücknahme irgendeiner Funktion**;
- keine Rücknahme vorhandener Performancefixes;
- große zusammengehörige Blöcke statt Microfix-/Plugin-Serie;
- keine neue Architektur;
- vor Installation lokal POSITIV + NEGATIV + Regression/Funktionsgleichheit;
- Löschen nur bei Beweis, dass keine Funktion/Abhängigkeit verloren geht.

Große Blöcke:
1. Runtime / Query Ownership;
2. Header-Suche / AJAX;
3. Template / Frontend / DOM;
4. Affiliate-Zentrale inkl. AFF-ERR-064;
5. Plugin-/Asset-/Storage-Konsolidierung und Abschlussmessung.

### Erster offener Blocker

Der **exakt aktuelle vollständige Template-Kit-1.50.578-Sourcebestand** ist im für diesen Abschluss frisch geprüften autoritativen GitHub-Weg nicht als technische Current-Quelle gebunden. Historische Extracts reichen nicht für sichere Änderungen/Löschungen.

### GENAU EINE NEXT ACTION

`BIND_EXACT_TEMPLATE_KIT_1_50_578_SOURCE_THEN_RUN_LOCAL_POS_NEG_PERFORMANCE_BASELINE`

Bedeutung:
- exakten aktuellen 1.50.578-Vollstand binden;
- aktuelle Affiliate-6.72.210-Source erneut frisch lesen;
- **vor jedem Sourcewrite** einen gemeinsamen lokalen Baseline-Harness aufbauen, der normale Seiten + Header-AJAX reproduziert;
- Query-/Hook-Arbeit einem Besitzer/Callpath zuordnen;
- bestehende Suchwelten, Ranking, Provider, Slots, Veto, Publish, Design und Navigation als Positiv-/Negativ-Funktionsvertrag festhalten;
- danach erst den ersten gebündelten Performanceblock ändern.

### Abschlussregel für diesen Stand

In diesem Chat wurde **kein Plugin-Code geändert, kein Installer gebaut und nichts live installiert**.
Es wurden nur Readbacks/Root-Cause-Grenzen geprüft und die fehlende Dokumentation nachgezogen.
Die alten dynamischen NEXT-ACTION-Aussagen weiter unten (z. B. 6.72.172 installieren) sind historisch/supersediert und dürfen nicht mehr als aktuelle Arbeitsanweisung verwendet werden.

---

## TEXT-/SEO-PLUGIN-DELTA 2026-10-08 – 0.57.59 LIVE FEHLER / 0.57.61 + 0.28.34 FINALER LOKALER E2E-KANDIDAT

Inventar-/Betriebsreadback; Fach-/NEXT-ACTION-Autorität bleibt `../TEXT/CURRENT_STATE.md`.

- PSTE **0.57.59 live** durch Nutzer-Screenshot belegt.
- 0.57.59: stale-Erstklick behoben, aber reale Restfehler: unnötiger erneuter Bestandslauf/Endloop-Verhalten, READY-Titel nicht sichtbar, Ausschlussgründe 4488 → ca. 32/33 nicht transparent.
- finaler lokaler Kandidat **PSTE 0.57.61**: `PSTE-0.57.61-ENDLOOP-READY-VISIBILITY-EVIDENCE-REENTRY-HARDPASS.zip`.
- SHA-256 `81fbbf808f0ccfd5bb2f8aa29dea37c676f9324adbd054598a5901dffaa2e407`.
- 117 Dateien / PHP 79/79 / JSON 37/37 / Fresh-Unpack 117/117.
- READY-Liste sichtbar, Ursachenaggregation sichtbar, normaler Seitenaufruf passiv, READY idempotent, Reload ohne Neustart, targeted 110-Reentry ohne Provider/Vollscan.
- Zwischenpaket PSTE 0.57.60 **DO NOT INSTALL**; finaler Bootstrap wurde erst danach live-drift-tolerant fertiggestellt.

- finaler Companion-Kandidat **PSERC 0.28.34**, Build `0.28.34-stable-pste-capability-fingerprint`.
- Installer `PSERC-0.28.34-STABLE-PSTE-CAPABILITY-FINGERPRINT-HARDPASS.zip` / SHA-256 `df4fd8fb640e05455f5f0f64edb5e508c011551326ff9da5061ad91ac6f5efd0`.
- Plan-Fingerprint hängt nicht mehr an roher PSTE-Version; reine PSTE-UI/Orchestratorupdates invalidieren PSERC nicht mehr künstlich.
- 0.28.34 noch nicht live readback-bestätigt; keine PU-ID.

- finaler Testreport `PFERDE_ATELIER_PSTE_05761_PSERC_02834_END_TO_END_HARDPASS_TESTREPORT.json`, SHA-256 `82c377475dc7f2a99d9cbdd5dc50f06da3b35bd2c8215aef0ccf8cf0b04983ea`.
- NEXT ausschließlich `../TEXT/CURRENT_STATE.md`.

## TEXT-/SEO-PLUGIN-DELTA 2026-10-08 – 0.57.58 LIVE FAIL / 0.57.59 ROOTFIX

Dieser Block ist Inventar-/Betriebsreadback; Fach-/NEXT-ACTION-Autorität bleibt `../TEXT/CURRENT_STATE.md`.

- **PSTE 0.57.58 live belegt** durch Nutzer-Screenshot.
- erster Automatik-Klick live: **GESTOPPT / `PSTE_SITE_STRUCTURE_STALE`**.
- 0.57.58 deshalb **nicht final**, sondern live fehlgeschlagen.
- neuer lokaler Kandidat **PSTE 0.57.59**.
- Installer `PSTE-0.57.59-AUTOMATIK-STALE-BASELINE-COMPACT-REBIND-HARDPASS.zip`.
- SHA-256 `a3808c0834b2d60a332a6dc3178403988fb1a80b0c62943173c1b9e5c050c2e8`.
- exakt 4 Dateien geändert / 112 von 116 byteidentisch zu 0.57.58.
- stale-first-click explizit in neuer Positiv-/Negativmatrix: PASS; kompakter Rebind selbst 0 Topic-Pool-Zeilen / 0 Provider.
- vollständiger Report `PFERDE_ATELIER_PSTE_05759_LIVE_STALE_FIRST_CLICK_ROOTFIX_HARDPASS_TESTREPORT.json` / SHA-256 `a7093902217d0905c97fdfba1bc2e15a8764063d32ef1e4cf5cc12abb903cc7f`.
- PSTE 0.57.59 **noch nicht live**; keine PU-ID dafür.
- PSERC 0.28.33 wurde für diesen PSTE-Fehler **nicht geändert**. Sein aktueller Live-Installationsstatus ist aus diesem Screenshot nicht unabhängig ablesbar.

## TEXT-/SEO-PLUGIN-DELTA 2026-10-08 – FINALER LOKALER CLEANUP-HARDPASS

Dieser Block ist Inventar-/Betriebsreadback; Fach-/NEXT-ACTION-Autorität bleibt `../TEXT/CURRENT_STATE.md`.

- PA-E-019 Portal SEO Themenengine: lokaler finaler Kandidat **0.57.58**.
- Installer `PSTE-0.57.58-KISS-FINAL-CLEANUP-HARDPASS.zip` / SHA-256 `1ea1f3fd8223395a1424e990a7cc418853c3ab301939c794a2580304b9ce66a5`.
- gegenüber 0.57.57 exakt 3 Dateien geändert, 113/116 byteidentisch; alte separate Diagnoseoberflächen entfernt/konsolidiert, Funktionskern erhalten.
- PHP 79/79, JSON 36/36, Fresh-Unpack 116/116, Static 40/40, Automatik 9/9, Kurzer Dienstweg 10/10 PASS.
- **0.57.58 noch nicht live installiert/readback-bestätigt; keine PU-ID.**

- PA-E-017 Portal SEO Redaktionsplan Compiler: lokaler finaler Kandidat **0.28.33** / Build `0.28.33-evidence-contract-sync`.
- Installer `PSERC-0.28.33-EVIDENCE-CONTRACT-SYNC-HARDPASS.zip` / SHA-256 `dc197e4af35605660b9187c051cf1b0b535bc1aeb6677cd9d69ea0f1e784e36e`.
- gegenüber 0.28.32 exakt 3 Dateien geändert, 60/63 byteidentisch; Evidence-Vertrags-JSON exakt an Runtime-Gate synchronisiert; Binding `331dfa4b384e15f08c2be0f3fd498b57a58e4c20ed854adfb7b36b0f465b0a28`.
- PHP 43/43, JSON 17/17, Fresh-Unpack 63/63, Package Integrity und Positiv-/Negativmatrix PASS.
- **0.28.33 noch nicht live installiert/readback-bestätigt; keine PU-ID.**

- Vollständiger Testreport: `PFERDE_ATELIER_PSTE_05758_PSERC_02833_FINAL_HARD_TESTREPORT.json`, SHA-256 `517b4bf85ddd8b26caecefc7f8c5619f035260b82aaa150fc134d28e3f18a5d0`.
- Lokaler technischer Blocker: **keiner**. Nächster Fachschritt ausschließlich Live-Installation + Readback gemäß TEXT-Current.

## TEXT-/SEO-PLUGIN-DELTA 2026-10-08 – EXAKTE ARTEFAKTE / LOKALER HARD-PASS

Dieser Block ist Inventar-/Betriebsreadback; Fach-/NEXT-ACTION-Autorität bleibt `../TEXT/CURRENT_STATE.md`.

- Portal SEO Themenengine / PA-E-019: exakter lokaler Kandidat **0.57.57**.
- ZIP: `PSTE-0.57.57-KISS-SLIM-AUTOMATIK-KURZWEG.zip`.
- SHA-256: `c3a001cd06d20fb71d75a21d7aca3cde4436920f855e999a3c166f035de01107`.
- frisch aus Original-ZIP geprüft: 116 Dateien / 79 PHP / ZIP PASS / PHP 79/79 / JSON 36/36.
- exakter PSTE→PSERC-Fünffelder-Handoff positiv und fail-closed negativ PASS.
- Automatik und Kurzer Dienstweg lokal positiv/negativ PASS; DB-/Performance-KISS PASS.
- **kein ausgeführtes PSTE-0.57.57-WordPress-Update unabhängig belegt; daher keine PU-ID und keine LIVE-Behauptung.**

- Portal SEO Redaktionsplan Compiler / PA-E-017: exaktes Artefakt **0.28.32**.
- ZIP: `PSERC-0.28.32-PAA-RELATED-INTEGRITY-ROOTFIX.zip`.
- SHA-256: `be09a8bee9246b5fe7047242e97111ec16e11e4d4a063da806c4c7dd6d49b25d`.
- frisch geprüft: 63 Dateien / 43 PHP / ZIP PASS / PHP 43/43 / JSON 17/17 / Paketintegrität PASS.
- öffentliche Live-Package-Binding-Datei belegt am 08.10.2026 Version **0.28.32** / Build `0.28.32-paa-related-integrity-rootfix`.
- der konkrete Installationsvorgang ist im Updateprotokoll nicht vollständig als Ereignis dokumentiert; deshalb **keine retroaktive PU-ID erfinden**.

- Rest-Cleanup vor Finalabnahme: PSERC-Evidence-Vertrags-JSON mit Runtime-Gate synchronisieren; PSTE-versteckte Admin-/Diagnoseoberflächen nur bei nachgewiesener Entbehrlichkeit entfernen.
- Fachstatus/NEXT ACTION ausschließlich `../TEXT/CURRENT_STATE.md`.

## TEXT-/SEO-PLUGIN-DELTA 2026-10-05 – PSTE 0.57.39

Dieser Block ist Inventar-/Betriebsreadback; Fach-/NEXT-ACTION-Autorität bleibt `../TEXT/CURRENT_STATE.md`.

- letzter per Screenshot eindeutig sichtbarer Live-Stand: **PSTE 0.57.36**;
- 0.57.38: PSERC-Planabdeckung lokal repariert, aber durch Journal-Inventarlücke als finaler Stand supersediert;
- aktueller konsolidierter lokaler Kandidat: **PSTE 0.57.39**;
- ZIP: `PSTE-0.57.39-JOURNAL-INVENTORY-CATEGORY-ROOTFIX-HARDPASS.zip`;
- SHA-256: `10a6e28e52639071ccde56d4c96f0ae3a37aae1d93bd8e2c51368f13f8e342f9`;
- Testreport: `PSTE-0.57.39-JOURNAL-INVENTORY-CATEGORY-ROOTFIX-TESTREPORT.json`;
- Testreport-SHA-256: `005c4a4d5c9ebf1437c0c882e5f00e19d3cea078e86c1bdb54a0e6d1b0c8105e`;
- 1:1 Realfälle: Post 15974 `Wie alt werden Pferde?` → `Pferdegesundheit verstehen` / Journal; Post 16029 `Können Pferde schwimmen?` → `Pferdewissen & Grundlagen` / Journal;
- regulärer Core-Fall unverändert; unbekannte Kategorie fail-closed; Extension/Core-Term-Kollision hard-block;
- 0.57.38 PSERC-Planabdeckung bleibt byteidentisch enthalten;
- PHP 81/81, JSON 54/54, Fresh-Unpack 136/136 byteidentisch;
- **0.57.39 noch nicht live installiert/readback-bestätigt; keine PU-ID**;
- isoliertes `CURRENT.zip` wurde nicht ersetzt, weil im Chat kein bytegenauer Repository-Binärsync ausgeführt wurde. Der geprüfte Installer liegt als Arbeitsartefakt vor.

## TEXT-/SEO-PLUGIN-DELTA 2026-10-05

Dieser Block ist Inventar-/Betriebsreadback; Fach-/NEXT-ACTION-Autorität bleibt `../TEXT/CURRENT_STATE.md`.

- Portal SEO Themenengine: letzter per Screenshot eindeutig sichtbarer Live-Stand **0.57.36**.
- Lokaler Kandidat **0.57.38** behebt den PSERC-Editorial-Plan-Abdeckungsfehler und bestand 4472+16 lokal; **kein finaler Gesamtstand**.
- Neu exakt belegter offener Fehler: bestehende Journal-/Magazinartikel können im allgemeinen PSTE-WordPress-Inventar Kategorie/Familie/Artikeltyp verlieren, obwohl dieselbe Extension-Kategorie im Kandidatenrouting korrekt registriert ist.
- Reproduzierbarer Realfall: `Wie alt werden Pferde?` / WordPress Post-ID 15974; Kandidatenroute → Kategorie 1486 `Pferdegesundheit verstehen` / Journal, bestehender WordPress-Inventartreffer → `category_name=""`.
- Rootcause: `PSTE_Snapshot::inventory()` akzeptiert nur reguläre `structure()['items']`-Kategorien; Artikeltyp-Erweiterungskategorien werden dort nicht über die vorhandene Extension-Registry/-Router-Autorität ergänzt.
- **0.57.38 daher nicht installieren/freigeben als finalen Produktionsstand.**
- Nächster zulässiger Pluginstand erst nach kleinstem Journal-Inventarmapping-Fix auf 0.57.38-Basis und vollständiger lokaler 1:1 Positiv-/Negativ-/Regression-Simulation.
- Keine PU-ID für 0.57.38: kein ausgeführtes Live-Update auf 0.57.38 belegt.
- Isoliertes `CURRENT.zip` wurde für 0.57.38 **nicht** ersetzt; wegen offenem Journal-Fehler darf es auch nicht als aktueller freigegebener Stand synchronisiert werden.

## TEXT-/SEO-PLUGIN-DELTA 2026-10-04

Dieser Block ist Inventar-/Betriebsreadback; Fach-/NEXT-ACTION-Autorität für PSTE bleibt im TEXT-Bereich.

- Portal SEO Themenengine **0.57.32 live exportseitig belegt**.
- Live gespeicherter Einzellauf: `PAUSED_ERROR` / `PSTE_SANDBOX_DATAFLOW_PORTAL_COMPONENT_DRIFT`.
- Neuester/live geprüfter Stand: **0.57.32** – Revalidierungs-Persistenz für vorhandene Titelkandidaten.
- ZIP: `PSTE-0.57.32-TITLE-CANDIDATE-REVALIDATION-PERSISTENCE-CANDIDATE.zip`
- SHA-256: `c021ed852d89b6ae87fb4b6e347f49e6a0906b512671951044ea9a55ee06f772`.
- Tests: 0.57.30 echter Resume-Pfad FAIL (SINGLE_PARKED); 0.57.31 sicherer Drift Recovery+Advance PASS; unsicherer Providerfehler bleibt Park FAIL-CLOSED; Contract-Rootfix PASS; PHP 81/81.
- **0.57.30 verworfen; 0.57.31 noch nicht live installiert/readback-bestätigt; keine PU-ID.**
- Live-Readback 0.57.32: 695 vorhandene Titelkandidaten persistent revalidiert; 320 STRUCTURE_GAP / 372 SANDBOX_REQUIRED / 3 RETAINED_NON_PRODUCING; Export-Readback PASS.
- Fachstatus/NEXT ACTION ausschließlich: `../TEXT/CURRENT_STATE.md`.

## TEXT-/SEO-PLUGIN-DELTA 2026-10-03

Dieser Block ist Inventar-/Betriebsreadback; Fach-/NEXT-ACTION-Autorität für PSTE bleibt im TEXT-Bereich.

- Portal SEO Themenengine **0.57.28 live belegt**; Bestandsstart aktuell durch vorhandenen Einzellauf korrekt mit `PSTE_RESEARCH_JOB_ALREADY_ACTIVE` blockiert.
- Neuester lokaler Entwicklungskandidat: **0.57.29** – 0.57.28 unverändert plus fail-closed UI-Guard für bereits aktive Einzelläufe vor Bestandsaufbereitung.
- Kandidat: `PSTE-0.57.29-ACTIVE-JOB-GUARD-CANDIDATE.zip`
- SHA-256: `e5baf380157236103a5c15c0cee8da2c750daef207cd4fe9efef6f9791e7f880`.
- Basis: 0.57.27 / `414b18f99e676516464790c842eedebc71a72a701c32bb95bd2d924d45ae9c79`.
- Lokale Evidence: ZIP PASS; Fresh-Unpack PHP 81/81; 694er Replay 320 STRUCTURE_GAP / 371 SANDBOX / 3 Produktwahl-Hold / 0 NORMAL_PASS; Family-Regression 0; Strukturrouter 6/6; Produktwahl 14/14; 326er Bestand 0 künstliche Produktwahl-Treffer.
- **Kein WordPress-Update auf 0.57.28 belegt; keine PU-ID.**
- Fachstatus/NEXT ACTION ausschließlich: `../TEXT/CURRENT_STATE.md`.

## TEXT-/SEO-PLUGIN-DELTA 2026-10-02

Dieser Block ist Inventar-/Betriebsreadback; Fach-/NEXT-ACTION-Autorität für PSTE bleibt im TEXT-Bereich.

- Portal SEO Redaktionsplan Compiler: **0.28.30** im aktuellen Arbeitsstrang installiert; späterer realer PSERC-Lauf erreichte COMPLETE.
- Portal SEO Themenengine: **0.57.26 live belegt** durch Nutzer-Screenshot vom 02.10.2026.
- PSTE 0.57.26 Live-Ergebnis: Speicherpflege COMPLETE / 646,3 MB eingespart; Bestandsaufbereitung COMPLETE; 695 neue Titelkandidaten; 8 zusätzlich PSERC-prüfbar; 36 vollständig aufbereitet; keine Provider-Abfrage.
- Plugin-Updateereignis: `PU-20261002-001`.
- Fachstatus/NEXT ACTION ausschließlich: `../TEXT/CURRENT_STATE.md`.
- Isolierte Binärkopie `ISOLIERTE_PLUGINS/.../CURRENT.zip` wurde in diesem Chat **nicht** in GitHub synchronisiert; der geprüfte Installer liegt als Chat-Artefakt vor. Keine falsche Binärsynchronisierung behaupten.



STAND: 2026-10-01
STATUS: AFFILIATE 6.72.171 LIVE / 6.72.172 IDEALO-STORAGE-HANDOFF VERIFIZIERT / BACKUPS BEREINIGT / DB-VERSCHLANKUNG OFFEN

## AUTORITÄT

Diese Datei ist die einzige aktuelle Standzusammenfassung des PLUGINS-Büros.

- aktueller belastbarer Stand, erster offener Punkt und genau eine NEXT ACTION → diese Datei
- `HOBBYRAUM.md` → nur temporäre Ausführungsfläche, keine eigene Status-/NEXT-ACTION-Autorität
- vollständiger beobachteter Pluginbestand → `PLUGINREGISTER.md`
- Update-Chronik → `UPDATEPROTOKOLL.md`
- Update-/Pflegeregeln → `REGELWERK.md`
- Fach-/Release-/LIVE-Status → zuständiges Fachbüro / technische Originalquelle
- Fehler → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md`
- dauerhaftes WAS/WARUM → `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`

## REALER WORDPRESS-READBACK 2026-09-30 – AKTUELLER BETRIEBSSTAND

Quelle: vom Nutzer bereitgestellte aktuelle WordPress-Liste „Plugins → Installierte Plugins“. Dieser Block ist Inventar-/Betriebsreadback, keine eigenständige Fach- oder Releasefreigabe.

Aktuell beobachtet:
- Affiliate Portal Template Kit (Pferde-kompatibel): **1.50.578**, aktiv.
- Affiliate-Zentrale (Portal-kompatibel): **6.72.171**, aktiv; Nutzer bestätigt am 01.10.2026 ausdrücklich, dass die Performance-Diagnose 10:30–10:31 UTC unter 6.72.171 lief. Der reale Performance-Readback ist PASS.
- Performance Diagnose Safe: **2.3.0 aktiv**; ältere **2.2.0 inaktiv**.
- Pferde Atelier – Affiliate Design Performance: **3.0.0 inaktiv**.
- Portal Production Machine: **6.7.9**, aktiv.
- Portal SEO Redaktionsplan Compiler: **0.28.27**, aktiv.
- Portal SEO Themenengine: **0.57.13**, aktiv.

Der frühere Kategorie-Stand weiter unten bleibt historische Scope-Dokumentation und darf diese reale Inventarbeobachtung nicht überschreiben.

## AKTIVER ZIELVERTRAG

Autoritative Zielquelle:
`protocol/PROJECT_MEMORY/ZIELVERTRAEGE/ZV-PLUGINS-CLEANUP-001.md`

Dauerhafte Arbeitsentscheidung/Warum:
`protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md` → `PLUGINS-001`.

Diese Current-Datei kopiert den Zielinhalt nicht; sie bindet nur aktuellen Stand, ersten offenen Punkt und NEXT ACTION.

## FRISCHE STORAGE-BASELINE 2026-10-01 11:13–11:15 UTC

Quelle: realer WordPress-Export `wordpress-speicheranalyse-20261001-111515.json`, vollständig `done=true`.

- gescannte Dateien gesamt: **16.879.899.578 Bytes**
- `wp-content/ai1wm-backups`: **13.295.750.128 Bytes**, 7 Dateien; darin zwei große `.wpress`-Backups:
  - 01.10.2026: **7.264.453.820 Bytes**
  - 29.09.2026: **6.031.295.633 Bytes**
- `wp-content/wpvividbackups`: **2.109.325.928 Bytes**, 100 Dateien
- `wp-content/uploads`: **1.042.403.409 Bytes**
- darin fünf `ppar-idealo-feed-*.tmp`: zusammen **749.350.091 Bytes**
- vier dieser idealo-TMP-Dateien waren bereits im 29.09.-Baselinebericht mit identischem Namen/Größe vorhanden; damit sind liegengebliebene Tempdateien real belegt.
- Affiliate 6.72.171 löscht den jeweils normalen idealo-Downloadpfad bei Erfolg/HTTP-Fehlern, aber der zentrale Housekeeping-Disk-Pass räumt aktuell nur `ppar-affiliate-product-images` auf und erfasst verwaiste `ppar-idealo-feed-*.tmp` im Upload-Root nicht. Das ist ein belegter Zukunftsschutz-Gap, kein Grund für pauschale Dateilöschung.
- Datenbank gesamt: **1.561.968.640 Bytes** gegenüber 1.576.435.712 Bytes am 29.09. (**-14.467.072 Bytes / ca. -0,9 %**)
- `slfo_options`: **410.746.880 Bytes** (vorher 421.232.640)
- `slfo_pste_candidates`: **409.108.480 Bytes** (unverändert)
- `slfo_pste_runs`: **366.510.080 Bytes** (unverändert)
- `slfo_pste_topic_pool`: **114.311.168 Bytes** (leicht kleiner)
- `slfo_ppar_ebay_items`: **103.219.200 Bytes** (unverändert)
- Autoload: **260.941 Bytes**; kein Autoload-Großproblem.
- TEXT-Autorität meldet laufenden PSTE-Kontextabgleich. Deshalb aktuell **keine PSTE-Themen-/Sandbox-/Run-Daten löschen oder umklassifizieren**.

Aktuell größter sicher trennbarer Hebel ist lokaler Backupbestand. Das alte All-in-One-Backup vom 29.09. plus der verbleibende WPvivid-Bestand belegen bereits **8,14 GB** potentiell entfernbaren lokalen Backup-Speicher, aber irreversible Löschung erst nach extern gesichertem aktuellen Rollback.

ERSTER OFFENER PUNKT:
**Aktuelles 01.10.-All-in-One-Backup extern sichern/verifizieren; erst dann alte lokale Backupbestände löschen. PSTE-Daten bleiben bis zum laufenden Kontext-Refresh-COMPLETE unberührt.**

GENAU EINE NEXT ACTION:
`SECURE_CURRENT_AIO_BACKUP_OFFSERVER_THEN_PURGE_OLD_LOCAL_BACKUPS`.

Danach als gebundener Folgepunkt: genau einen Affiliate-Zentrale-Storagefix für verwaiste `ppar-idealo-feed-*.tmp` bauen/hart positiv-negativ-regressiv testen und erst danach die belegten Alt-TMPs bereinigen. Keine Plugin-Orgie und kein separater Hilfsrunner.

## STORAGE-READBACK NACH BACKUP-LÖSCHUNG 2026-10-01 11:24–11:25 UTC

Quelle: realer WordPress-Export `wordpress-speicheranalyse-20261001-112548.json`, vollständig `done=true`.

- Gesamtscan: **3.584.150.125 Bytes** statt 16.879.899.578 Bytes vorher.
- Differenz: **-13.295.749.453 Bytes**.
- `wp-content/ai1wm-backups`: nur noch **675 Bytes / 5 Kleinstdateien** statt 13.295.750.128 Bytes.
- Damit wurden die großen All-in-One-`.wpress`-Backups vollständig aus dem lokalen Serverbestand entfernt.
- `wp-content/wpvividbackups`: weiterhin **2.109.325.928 Bytes / 100 Dateien**, unverändert.
- `wp-content/uploads`: weiterhin **1.042.403.409 Bytes**, unverändert.
- fünf `ppar-idealo-feed-*.tmp`: weiterhin **749.350.091 Bytes**, unverändert.
- Datenbank: weiterhin **1.561.968.640 Bytes**, unverändert.
- Schlussfolgerung: bisherige Einsparung stammt praktisch vollständig aus der All-in-One-Backup-Löschung; WPvivid, Idealo-TMP und DB sind noch offen.

ERSTER OFFENER PUNKT:
**WPvivid-Altbestand 2,109 GB ist noch vollständig vorhanden.**

GENAU EINE NEXT ACTION:
`PURGE_WPVIVID_LOCAL_BACKUPS`.

Danach: Affiliate-Temp-Zukunftsschutz + Alt-TMP-Bereinigung, Bildoptimierungsblock, anschließend DB-Retention/DB-Verschlankung und physische Reorganisation.

## STORAGE-READBACK NACH WPVIVID-BEREINIGUNG + IDEALO-ZUKUNFTSSCHUTZ 2026-10-01

Realer WordPress-Speicherexport `wordpress-speicheranalyse-20261001-114840.json`, vollständig `done=true`:
- Gesamtscan: **1.475.744.045 Bytes**;
- `wp-content/ai1wm-backups`: **675 Bytes**;
- `wp-content/wpvividbackups`: **919.848 Bytes / 77 Dateien**, überwiegend verbleibende Logdateien; die alten Backup-Payloads sind physisch entfernt;
- `wp-content/uploads`: **1.042.403.409 Bytes**;
- fünf `ppar-idealo-feed-*.tmp`: weiterhin **749.350.091 Bytes**;
- Datenbank weiterhin **1.561.968.640 Bytes**; Datenbank-Verschlankung ist noch nicht ausgeführt.

Affiliate-Zentrale:
- Live bleibt **6.72.171** bis zu neuem WordPress-Readback.
- Kandidat **6.72.172** schließt ausschließlich den belegten Idealo-Temp-Retention-Gap im bestehenden Housekeeping.
- lokaler Positiv-/Negativtest: PASS;
- kompletter Housekeeping-Disk-Durchlauf: PASS;
- exakter Handoff-Installer `AFFILIATE_ZENTRALE_6.72.172.zip`;
- Handoff-SHA-256: `c9fd44b97793422890a46b87dcdcbc88ce52ae26437b77173a64c9d976b73a25`;
- 27/27 Source-Identität PASS; Fresh-Unpack 27/27 PASS; PHP-Lint 21/21 PASS; Header/Runtime 6.72.172 PASS;
- technische Autorität: `affiliate-release-current:control/release-governance/CURRENT_RELEASE.json`;
- Repository-Binärsync bleibt wegen fehlendem bytegenauem Binär-Uploadweg formal offen; der geprüfte Handoff-Installer ist davon getrennt.
- alte hardcodierte 6.72.170/171-CI-Jobs sind kein 6.72.172-Fehler: Governance/Source/Tree/Start PASS; Abbruch erst an fest verdrahtetem Versions-`grep`. Workflows wurden nicht umgebaut.

Datenbank:
- PSTE bleibt bis `PSTE_CONTEXT_REFRESH_COMPLETE` strikt unangetastet;
- aktueller TEXT-Blocker ist weiterhin `PSTE_CONTEXT_REFRESH_NOT_COMPLETE`;
- PSERC besitzt bereits Generation-Retention/Storage-Maintenance; keine neue Architektur erforderlich;
- Affiliate-Housekeeping besitzt bereits bounded DB-Retention und eBay-Payload-Kompaktion; diese Pfade werden nach Idealo-Live-Readback im DB-Block gezielt verwendet/vermessen.

ERSTER OFFENER PUNKT:
**Den exakt geprüften Affiliate-Zentrale-6.72.172-Handoff installieren und den aktiven Versionsstand in WordPress zurücklesen.**

GENAU EINE NEXT ACTION:
`INSTALL_AND_READBACK_AFFILIATE_6_72_172`.

Erst danach: zentralen Housekeeping-Lauf ausführen, Storage erneut messen und belegen, dass die fünf Idealo-TMPs verschwunden sind. Anschließend DB-Verschlankung: PSERC/Affiliate bereits mögliche Retention zuerst; PSTE erst nach Context-Refresh-COMPLETE; danach physische Tabellenreorganisation und erneute Speicher-/Performance-Messung.

## HARDLOCK – KEIN PERFORMANCE-RÜCKBAU 2026-10-01

Für jede kommende Affiliate-Funktionsreparatur (eBay-Ausspielung, Portalabdeckung, Banner-Zuordnung, Tarifcheck/CHECK24) gilt verbindlich:

- Ausgangsbasis ist ausschließlich der **frisch gelesene kanonische Current-Sourcebaum** auf `affiliate-release-current`.
- Aktuellster Kandidat: **6.72.172**, aufgebaut auf dem freigegebenen Performance-Stand **6.72.171**.
- Die 6.72.171-Performanceoptimierungen in `pferdeportal-affiliate-router.php`, `includes/trait-ppar-automation-suite.php` und `includes/trait-ppar-ebay.php` dürfen nicht entfernt, überschrieben oder durch Altcode ersetzt werden.
- Die 6.72.172-Storageänderung in `includes/trait-ppar-housekeeping.php` bleibt ebenfalls erhalten.
- Kein Cherry-Pick/Copy aus 6.72.170 oder älter, kein Alt-ZIP als Basis, keine Rekonstruktion.
- Vor jedem Source-Write erneut Current, Branch-HEAD, Manifest und betroffene Datei-Hashes lesen.
- Funktionsfix nur als **kleinstes Delta auf dem aktuellen Baum**.
- Regression muss neben dem Fach-PASS zwingend die 6.72.171-Performance-Semantik prüfen: identische Slot-Auswahl/HTML/Kandidatenreihenfolge, request-lokale Caches weiter aktiv, Admin/Worker uncached wie bisher.
- Bei Performanceverschlechterung oder Verlust eines belegten Cachepfads: FAIL, kein Installer.

## NEUER REALER AFFILIATE-AUSGABEFEHLER 2026-10-01

Nutzer-Readback:
- eBay-Produktanzeigen werden im Frontend erneut nicht sichtbar ausgespielt;
- vorhandene Banner werden nicht zuverlässig automatisch dem fachlich passenden Ziel zugeordnet;
- konkreter reproduzierbarer Fall: vorhandener Banner „Schabrackendesigner“ erscheint nicht auf der Produktseite/Kategorie „Schabracken“.

Read-only technische Einordnung:
- der historische reale WordPress-Bestand belegt für „Schabracken“ eine aktive eBay-BUSINESS-Kampagne mit exakter Zielbindung `page:schabracken` und den drei `category_product_1..3`-Placements; der Grundfehler ist daher nicht „Schabracken existiert nicht“ oder „nie zugeordnet“;
- die aktuelle Banner-Automatik besitzt vor dem Zielranking ein Fachdomain-Gate. Ein Creative wie „Schabrackendesigner“ kann dort bereits auf REVIEW enden, wenn die Creative-Evidence keinen generischen Pferdebegriff enthält, obwohl „Schabracken“ selbst ein exaktes reales Portalziel ist. Dieser Pfad ist im aktuellen Sourcecode belegt und muss nach Live-Readback eng regressiv geprüft werden;
- eBay besitzt zusätzlich einen Safe-Public-Checkpoint. Bei vorhandenem sicheren Checkpoint dürfen nur die dort enthaltenen BUSINESS-Campaign-IDs öffentlich erscheinen. Der aktuelle produktive Checkpoint-Inhalt ist noch nicht read-only belegt; deshalb wird die eBay-Ursache nicht geraten.

HARD RULE:
- Affiliate 6.72.172 bleibt der aktuelle Storage-only Kandidat; keine Banner-/eBay-Fachänderung in dieses Paket mischen.
- Nach Installation/Readback von 6.72.172 wird VOR weiterer Storage-Housekeeping-Arbeit zuerst der reale read-only `Portalabdeckung`-Snapshot für „Schabracken“ ausgewertet und der tatsächliche Banner-Datensatz „Schabrackendesigner“ geprüft.
- Erst den ersten exakt belegten eBay-Gatefehler fixen; keine Ranking-/Provider-/Checkpoint-Neukonstruktion auf Verdacht.
- Bannerfix nur eng: exakte reale Produktthemen müssen als fachliche Evidence zählen können, ohne negative Fachsignale oder Veto/Safety zu lockern.
- Positiv-/Negativ-/Realrouter-Regression zwingend vor neuem Installer.

Gebundener Folgepunkt nach `INSTALL_AND_READBACK_AFFILIATE_6_72_172`:
`READ_ONLY_DIAGNOSE_SCHABRACKEN_EBAY_AND_SCHABRACKENDESIGNER_THEN_FIX_FIRST_PROVEN_OUTPUT_GATE`.

## NEUER REALER EBAY-PRIVATE/HIVEPRESS-FEHLER 2026-10-01

Nutzer-Readback:
- Im HivePress-Bereich „Private Anzeigen“ werden eBay-Privatanzeigen gezählt, aber es sind keine eBay-Anzeigen sichtbar.

Read-only Codebefund im aktuellen kanonischen 6.72.172-Baum:
- HivePress kann Kategorie-/Nachfahrenzahlen bereits aus der Taxonomie ermitteln.
- Die eigentliche sichtbare Ergebnisliste wird danach zusätzlich durch `ebay_filter_stale_posts()` gefiltert.
- Für eBay-PRIVATE prüft dieser Finalfilter u. a. den sicheren Public-Checkpoint (`private_listing_ids`), Source-Row, Seller-Typ INDIVIDUAL, Source-/Policy-State, Inhalts-Policy, Lifecycle, Control-Gate und Endzeit.
- Dadurch ist der beobachtete Zustand „gezählt, aber 0 sichtbar“ technisch möglich, wenn der Rohbestand existiert, aber der finale Sichtbarkeitsvertrag alle eBay-Posts verwirft.
- Die konkrete live blockierende Bedingung ist noch nicht read-only belegt; nicht raten.

Nachhaltiger Zielvertrag:
1. Gültige eBay-PRIVATE-Listings im Teilbaum „Private Anzeigen“ müssen sichtbar sein.
2. Ungültige/stale/blocked Listings bleiben fail-closed unsichtbar.
3. Kategorie-/Trefferzahlen dürfen nicht dauerhaft einen anderen Sichtbarkeitszustand behaupten als der finale Listing-Loop.
4. Native HivePress-Anzeigen bleiben vollständig unverändert.
5. Keine Öffnung von eBay-PRIVATE außerhalb des erlaubten „Private Anzeigen“-Teilbaums.
6. Keine Rücknahme der 6.72.171-Performance-Caches.
7. Positiv/Negativ/Performance-Test muss mindestens abdecken:
   - parent „Private Anzeigen“ mit sichtbaren gültigen eBay-INDIVIDUAL-Listings;
   - direkte Unterkategorie mit sichtbaren gültigen eBay-Listings;
   - allgemeiner Anzeigenmarkt zeigt keine eBay-PRIVATE-Listings;
   - native HivePress-Anzeige bleibt sichtbar;
   - stale/ended/blocked/checkpoint-nicht-freigegeben bleibt unsichtbar;
   - Count/Loop-Konsistenz für den geprüften sichtbaren Bestand;
   - keine zusätzliche ungebremste DB-/Term-Auflösung auf normalen Portalrequests.

Reihenfolge:
- 6.72.172 unverändert installieren/readbacken; kein Mischfix in das geprüfte Storage-Paket.
- Danach read-only den ersten live blockierenden PRIVATE-Gatepfad belegen.
- Genau diesen ersten belegten Fehler als kleinstes Delta auf dem dann aktuellen Sourcebaum reparieren.
- Danach kompletter eBay-PRIVATE Positiv-/Negativ-/Performance-Regressionslauf.

## BILDOPTIMIERUNG ALS GEBUNDENER AUFRÄUMBLOCK 2026-10-01

Aus der frischen Speicheranalyse:
- 375 Attachments;
- 2.992 WebP-Dateien mit zusammen ca. 142,1 MB;
- 737 PNG-Dateien mit zusammen ca. 135,6 MB;
- 427 JPG-Dateien mit zusammen ca. 25,6 MB.
Damit ist WebP bereits breit im Einsatz; eine pauschale Neu-Konvertierung ist nicht begründet.
- Die WordPress-Medienmetadaten belegen bei typischen Artikelbildern Original + mehrere abgeleitete Größen (u.a. 300, 768, 1024 sowie HivePress-spezifische Größen). Deshalb liegt das relevante Optimierungspotenzial eher in unnötigen Original-/Dublettenbeständen, überflüssigen Größen und korrekter Frontend-Auslieferung als in einem neuen Bildformat-Plugin.
- Der aktuelle Speicherreport zeigt mindestens drei exakte Bild-Dubletten-Gruppen mit ca. 8,5 MB unmittelbar belegtem Einsparpotenzial; keine pauschale Löschung ohne Referenzprüfung.
- Historische Performance-Evidence zeigt Artikel-LCP mehrfach auf dem Featured Image; Bildauslieferung bleibt deshalb eigener Performance-Prüfpunkt.
- Kein neues Bildoptimierungsplugin installieren. Erst bestehende Bildzentrale/WordPress-Größen, Referenzen und Auslieferung prüfen.
- Bildoptimierung wird vor der finalen Performance-Abnahme erledigt, aber nach Backup-/Tempbereinigung und parallel zur DB-Verschlankung.

## AUFRÄUM-/PERFORMANCE-PRÜFSTAND 2026-10-01

Technische Affiliate-Releasewahrheit:
`affiliate-release-current:control/release-governance/CURRENT_RELEASE.json`.

Belastbarer Stand für PA-E-003:
- letzter ausdrücklich versionsbezogener WordPress-Readback: Affiliate-Zentrale **6.72.170 aktiv** (01.10.2026, WordPress-Uploadvergleich);
- danach wurden 6.72.168–6.72.170 im laufenden Performance-/Storage-Strang technisch weiterentwickelt und reale Performance-Diagnosen geliefert; die Diagnose-Datei selbst enthält keine Plugin-Versionsnummer und wird deshalb nicht als separater Versions-Readback ausgegeben;
- realer Performancebefund vor 6.72.171: Top-Kategorie `/ausruestung/` ca. **1,65 s**, während tiefere Kategorieprodukt-Seiten wie Trensen/Pferdesättel weiter bei ca. **8,6–9,1 s** lagen;
- Ursache: die drei öffentlichen `category_product_1..3`-Slots wiederholten große Teile desselben slot-unabhängigen Kontext-Rankings und mehrerer reiner Gates/Providerprüfungen;
- **6.72.171** teilt dieses slot-unabhängige Ranking pro Seite und cached nur request-lokal reine, identische Prüfungen; Slot-Placement, Control/Veto, Provider-Mix und finale Auswahl bleiben pro Slot erhalten;
- Source-Head des getesteten Runtime-Baums: `ad4db0c34552667a9d398d4b74cb7d8b7130f03a`;
- Source-Manifest SHA-256: `5094f6df73c172b01819294d3dd455002fa244aa9676da0ebbbb4b058530dda4`;
- Exact Local A-B Run `36839006440`: SUCCESS, funktionale 1:1-Gleichheit + Positiv/Negativ PASS, Median **393,694 ms → 365,895 ms**;
- 2012er Snapshot Exact Local A-B Run `36839006513`: SUCCESS, identische Auswahl/HTML/Kandidatenzahlen, Gesamt **1248,595 ms → 249,597 ms (-80,01 %)**, Hub **-71,20 %**, Leaf/Unterkategorie **-89,87 %**;
- final lokal frisch gebauter Installer: `AFFILIATE_ZENTRALE_6.72.171.zip`;
- Installer SHA-256: `dbe630c72f5273abb5c3b48223bbed00498be0a0578f18eca3f001e92bb03fba`;
- 27/27 Source-Dateien byteidentisch zum getesteten GitHub-Baum; PHP-Lint 21/21 PASS; Fresh-Unpack erneut PASS;
- Exact-A/B-Evidence: `release/affiliate-zentrale/evidence/affiliate_router_v672171_category_product_performance_rootfix_20261001.md`;
- finaler Full-Gate Run `36842612555`: **SUCCESS**;
- finale Release-Evidence: `release/affiliate-zentrale/evidence/affiliate_router_v672171_full_release_gate_20261001.md`;
- technische Release-Autorität: **6.72.171 RELEASED / release_allowed=true**;
- neue reale Performance-Diagnose Safe 2.3.0 vom **01.10.2026 10:30–10:31 UTC** liegt vor; Messmodus `PASSIVE_NO_FILTERS`;
- die Diagnose führt `affiliate-portal-router/pferdeportal-affiliate-router.php` als **aktiv** auf, enthält aber selbst **keine Plugin-Versionsnummer**;
- reale Zeiten dieser Diagnose: `/ausruestung/` **1,560219 s**, `/ausruestung/ausruestung-sattel/` **2,308272 s**, `.../pferdesaettel/` **4,634054 s**, `.../trensen/` **4,537820 s**;
- gegen den zuvor dokumentierten 6.72.170-Befund (~1,65 s / ~8,85 s / ~9,09 s / ~8,62 s) sind alle vier Vergleichsseiten schneller; die drei tiefen Kategorieproduktseiten verbessern sich um ca. **73,9 % / 49,0 % / 47,4 %**;
- alle vier Vergleichsrequests liefern **HTTP 200** und `last_php_error = null`;
- diese Messung belegt die reale Performanceverbesserung und den aktiven Affiliate-Router, darf aber ohne separaten Versions-Readback nicht allein als exakter **6.72.171-Versionbeleg** ausgegeben werden;
- isolierter Repository-`CURRENT.zip`-Sync bleibt separat BLOCKED, solange der verfügbare Dokumentationsweg keinen bytegenauen Binärtransfer belegt; keine Ersatz-ZIP erfinden.

Der frühere NEXT `FRESH_STORAGE_BASELINE_THEN_RETENTION_CLASSIFICATION` ist durch die frische Baseline oben erledigt und supersediert.

### PSTE-KANDIDATENDELTA NACH ABSCHLUSSPRÜFUNG 2026-09-30

Bei der Abschlussprüfung wurde in einem früheren 0.57.13-Paket eine ungewollte Backup-Datei `includes/class-pste-sandbox-record-store.php.orig` entdeckt. Dieser Kandidat wurde **vor Installation verworfen**.

Final neu gebaut und frisch geprüft:
- ZIP SHA-256: `bb5f3cc84dc00fa85e2c0ddf48c8994a4788c2595c6d98f0d440780377060248`
- Version: `0.57.13`
- Fresh PHP-Lint: `78/78 PASS`
- Storage Core: `22/22 PASS`
- Maintenance + Active-Work Guards: `10/10 PASS`
- Public Storage API: `8/8 PASS`
- Rollback Restore: `17/17 PASS`
- Restore Mode: `7/7 PASS`
- Atomic Lock: `3/3 PASS`
- PSERC-0.28.27-Bindung: `PASS`
- Stray-Backup-Dateien `*.orig/*.bak/*~`: `0`
- Diff gegen 0.57.12: 2 neue Storage-Dateien, 6 geänderte Runtime/Admin-Dateien, 1 entfernte ungenutzte `.orig`-Datei; Contracts/Fixtures unverändert.

Der Nutzer bestätigt die Installation; der WordPress-Readback zeigt **Portal SEO Themenengine 0.57.13 aktiv**. Die Pluginliste beweist Version/Aktivstatus, aber nicht unabhängig den exakten Live-Bytebestand.

## ABSCHLUSS-/ARTEFAKTSTATUS

Die nach Abschlussregel geforderten isolierten `CURRENT.zip`-Binärartefakte konnten über den in diesem Chat verfügbaren GitHub-Schreibweg nicht bytegenau ins Repository übertragen werden. Es wurden deshalb keine ZIPs rekonstruiert.

Dauerhafte Blockerbelege:
- `ISOLIERTE_PLUGINS/PA-E-003/MANIFEST.md`
- `ISOLIERTE_PLUGINS/PA-E-019/MANIFEST.md`

Dies ändert die technische NEXT ACTION nicht. Der formale Plugin-Artefakt-Sync bleibt jedoch BLOCKED, bis ein autorisierter Binär-Uploadweg verfügbar ist.

## KATEGORIE-CLOSEOUT-SYNC 2026-09-24

Reine Dokumentations-Nachführung aus der technischen Current-Autorität `affiliate-release-current:control/release-governance/CURRENT_RELEASE.json`. Keine Pluginänderung und kein WordPress-Write durch diese Bürosynchronisierung.

Kategorie-/Strukturscope: **PASS / CLOSED**.
Finale Nachweise:
- `Category Integration Final Closeout` Run `36005442270` = SUCCESS
- `Category Integration Hard Baseline` Run `36005442188` = SUCCESS

Aktuell gebundene Kategorie-relevante Pluginstände:
- Affiliate Portal Template Kit: **1.50.559** – 1149er Kategorie-/Breadcrumb-Readback PASS
- Affiliate-Zentrale: **6.72.152** – Portalstruktur/Katalog 1149 PASS
- Allgemeine Bildzentrale: **2.7.6** – keine statische Vollkopie, kein Kategorie-Delta erforderlich
- Portal Link Policy Runtime Verifier: **1.0.0** – kein statisches Vollkopie-Delta erforderlich
- Portal Production Center: **1.1.1** – 1149 / 9 / 5790 + Build-Integrity PASS
- Portal Production Link Policy Gate: **1.0.1** – dynamischer/source-getriebener Kategoriepfad
- Portal Production Machine: **6.7.9** – Kategorieintegration 25/25 + 125/125 Slots PASS
- Portal SEO Redaktionsplan Compiler: **0.28.23** – vollständiger 1149-Strukturgate PASS
- Portal SEO Themenengine: **0.57.12** – LIVE_READBACK_PASS_CLOSED; `pferde putztasche` Readback PASS
- Portal Category Structure Repair Guard: **1.0.1** – kein statisches Vollkopie-Delta erforderlich

HARD RULE: Keine Kategorie-/Strukturarbeit erneut öffnen, solange keine neue harte Evidenz eines echten Kategorie-/Strukturdefekts vorliegt.

## BEOBACHTETER WORDPRESS-BESTAND 2026-09-12

Quelle: sechs vom Nutzer bereitgestellte Screenshots der WordPress-Seite `Plugins → Installierte Plugins`.

- **55 Pluginzeilen** sichtbar.
- **28 Zeilen Eigenentwicklungen/Projektentwicklungen**, entsprechend **27 unterschiedlichen Plugins**.
- Grund für die Abweichung: `Portal SEO Redaktionsplan Compiler` ist zweimal vorhanden (`0.28.20` aktiv, `0.28.16` inaktiv).
- **4 sichtbar inaktive Pluginzeilen**: HivePress Geolocation, HivePress Messages, Minimal Coming Soon & Maintenance Mode, Portal SEO Redaktionsplan Compiler 0.28.16.
- Es wurde in diesem Inventarlauf **kein Plugin aktualisiert, deaktiviert, aktiviert oder gelöscht**.

## INVENTARDELTA 2026-09-23 – NUR KATEGORIE-SCOPE

Quelle: Nutzer-Readback der real installierten WordPress-Plugins am 23.09.2026. Dieses Delta aktualisiert **nur** die für die Pferdeportal-Kategorieintegration relevanten beobachteten Versionen. Es ist keine Release-/LIVE-Freigabe.

Beobachtet:
- Affiliate Portal Template Kit (Pferde-kompatibel): **1.50.559**
- Affiliate-Zentrale (Portal-kompatibel): **6.72.152**
- Allgemeine Bildzentrale: **2.7.6**
- Portal Link Policy Runtime Verifier: **1.0.0**
- Portal Production Center: **1.1.1**
- Portal Production Link Policy Gate: **1.0.1**
- Portal Production Machine: **6.7.9**
- Portal SEO Redaktionsplan Compiler: **0.28.23**
- Portal SEO Themenengine: **0.57.12**
- Portal Category Structure Repair Guard: **1.0.1**

Für Fach-/Release-/LIVE-Status weiterhin zwingend zum zuständigen Fachbüro bzw. zur technischen Hauptquelle routen. Die Kategorieintegration selbst hat ihre technische Current-Autorität auf `affiliate-release-current:control/release-governance/CURRENT_RELEASE.json`.

## SICHTBARE UPDATE-HINWEISE IM SNAPSHOT

Nur als Beobachtung, **keine Update-Freigabe**:

- HivePress Authentication: installiert 1.1.4 → Hinweis auf 1.1.5.
- Kubio: installiert 2.9.0 (build 517) → Hinweis auf 2.9.1.
- Relevanssi: installiert 4.28.2 → Hinweis auf 4.28.3.
- Site Kit by Google: installiert 1.185.0 → Hinweis auf 1.187.0.
- WordPress Importer: installiert 0.9.5 → Hinweis auf 0.9.6.
- WPvivid Backup Plugin: installiert 0.9.132 → Hinweis auf 0.9.135.

## HISTORISCHER ABGLEICH AUS SNAPSHOT 2026-09-12 – DURCH DELTA OBEN TEILWEISE ÜBERHOLT

Der WordPress-Snapshot zeigt bei mehreren Eigenentwicklungen neuere installierte Versionen als ältere Campus-/Artefaktbelege. Dieses Büro überschreibt die Fachwahrheit deshalb **nicht automatisch**.

Offene Abgleiche:

- Affiliate-Zentrale: historischer 12.09.-Drift ist für den Kategorie-Scope durch den 24.09.-Closeout überholt; aktueller gebundener Stand **6.72.152**.
- Portal SEO Redaktionsplan Compiler: Kategorie-Scope aktuell **0.28.23**; der separat beobachtete inaktive Altstand 0.28.16 bleibt nur als möglicher Aufräumpunkt bestehen.
- Universal Product Comparison: WordPress beobachtet `0.8.5-prototype`; PRODUKTVERGLEICH-CURRENT_STATE enthält älteren Testkandidaten → Fachbüro frisch abgleichen.
- Universal Product Knowledge: WordPress beobachtet `0.5.1-prototype`; frühere Produktvergleichsbelege referenzieren 0.5.0 → Fachbüro frisch abgleichen.

Diese Punkte sind **Inventardrift**, nicht automatisch Fehler und nicht automatisch Release-PASS.

## AUFRÄUMLOGIK

Aktuell eindeutigster Eigenentwicklungs-Altbestand: inaktiver `Portal SEO Redaktionsplan Compiler 0.28.16` neben aktivem 0.28.20. **Entfernung trotzdem erst nach TEXT-Abhängigkeits-/Rollbackprüfung.**

Weitere Audit-/Diagnose-/Exporter-Plugins sind im `PLUGINREGISTER.md` als Prüf-/Aufräumkandidaten gekennzeichnet. Bewertung allein berechtigt niemals zur Löschung.

## EINE-WAHRHEIT-GRENZE

PLUGINS verwaltet Inventar, betriebliche Zuordnung, Bewertung und Update-Ereignis-ID.  
Es wird **keine zweite Fach-, Release-, LIVE-, Fehler- oder Modulwahrheit** geführt.
