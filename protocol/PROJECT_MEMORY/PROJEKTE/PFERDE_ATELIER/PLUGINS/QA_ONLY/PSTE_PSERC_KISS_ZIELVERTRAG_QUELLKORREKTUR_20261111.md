# Pferdeatelier: verbindlicher KISS-Zielvertrag – zusammengeführte Quellenkorrektur und echte Resthürde (11.11.2026)

## Verifizierte IST-Lage aus echten WordPress-Flugschreibern
- Am 10.11.2026 waren **3 READY für die ursprüngliche Metadaten-Übergabe** (Horseware-Regendecken, kombinierte Fliegen-/Regendecken, 0g-Regendecken).
- Nach Installation von PSTE 0.57.144.37 wurde eine erneute Bestandsprüfung über **5.013/5.013** durchgeführt, mit vielen UPDATEs in `topic_pool` und `topic_history`. Die WordPress-Flugschreiber vom 11.11. zeigen `planning_ready=0` statt zuvor 8 und PSERC `ready_count=0` statt zuvor 3. Der leere PSERC-Plan wurde als `COMPLETE` aktiviert. **Kein neuer DataForSEO-Aufruf**, aber tatsächlich geänderte Bestandsbewertungen. Das ist eine fehlgeschlagene Workflow-Abnahme.
- Der alte, **unveränderte** Original-Dreierplan inklusive fünfteiliger Übergabe ist separat in `/pferdeatelier/PLUGINS/QA/PFERDEATELIER_3_ARTIKEL_ORIGINALSTAND_20261110_NUR_SICHERUNG.zip` vorhanden. Enthaltene Profile sind signiert `PRE_TYPE`, keine fertige `BOUND_TYPE`-Freigabe für den aktuellen K0-Lauf.

## Ursachen in den tatsächlich ausgelieferten Plugin-Quellen
**Fehler 1 – falsch positive Quellenkonflikte:** Die Funktion `PSTE_Normal_Metadata_Path::candidateTitleBeforeCategory` verglich den fünfteiligen `PSTE_Normalizer::intentTuple` (inkl. nicht signiertem beschreibendem `entity`-Feld) gegen die vierteilige signierte `PSTE_Intent_Profile::analyzeBeforeType`-Quelle. Ungleichheit wurde auch bei korrekter 4-Felder-Quelle als `PSTE_RETAINED_SEO_TUPLE_SOURCE_CONFLICT` behandelt. Drei echte original signierte 2026-11-10 PRE_TYPE-Profile reproduzieren den Fehler.

**Fehler 2 – Quellbeleg überschrieben:** `PSTE_Repository::persistFreshRetainedNonPass` legte einen neuen Blocked-Payload an, ohne die alte signierte und **nachprüfbar unveränderte** `intent_analysis`/`intent_profile` bei negativem Resultat zu erhalten. Die negative fachliche Bewertung darf keinen gültigen vorherigen Suchnachweis löschen.

**Fehler 3 – leerer Redaktionsplan als neuer aktiver Stand:** `PSERC_Plan_Compile_Job::tickActivate` prüfte lediglich, dass die neue Indexzahl dem Job-Zähler entsprach; **0==0** wurde als erfolgreiche Aktivierung akzeptiert. Der Start gab einen unveränderten 0-READY-Aktivstand als COMPLETE zurück.

## Ein gemeinsamer Korrektursatz (KEINE zusätzlichen Pluginebenen)
Zwei **bestehende** Plugins aktualisiert:
- **PSTE 0.57.144.38**: Vergleich exakt der vier signierten SEO-Felder; `entity` ist keine neue SEO-Entscheidung; gefälschte/mismatching 4-Felder-Quellen blockieren weiter. Negativer Rückschritt erhält alten PRE_TYPE-Beleg **nur nach** `PSTE_Intent_Profile::verifiedPreTypeForRaw`, belässt `planning_suitability=BLOCKED`, keine künstliche Freigabe.
- **PSERC 0.28.66**: `0 planning_topic` beim INIT → **BLOCKED** ohne Inventar-/Kompilierarbeit; `0 READY` vor `activate()` → **BLOCKED** und alter gültiger Stand bleibt bestehen; 0-READY Aktivstand nicht als fertig wiederverwenden. Signierter 61-Dateien-Paketvertrag neu korrekt aus dem neuen vollständigen Plugin erstellt.
- K0 **unangetastet**. 14 fachliche PSTE-SEO-Entscheidungsdateien und WordPress-Core unverändert. Keine zusätzlichen Tabellen oder zweite Protokoll-/Forschungsstrecke. Kein Wiederanlauf der 5.000 Themen Bestandteil dieses Fixes.

**Realer Quellvergleich:** PSTE gegenüber ausgelieferter .37 **3 von 121 Dateien verändert**, PSERC gegenüber ausgelieferter .65 **3 von 63 Dateien verändert** (inkl. Versionsdatei und PSERC signiertem Paketmanifest).

## Physische Paket-QA aus den endgültigen ZIPS
Die zwei finalen WordPress-Test-ZIPs wurden selbst in leere Verzeichnisse entpackt und **genau deren Inhalte** in den lokalen Quellen- und negativen Fällen geprüft:
- ZIP CRC, vollständige Dateiidentität gegen gepatchte Quelldateien, 126/126 PHP-Dateien Syntax PASS.
- Original `PSERC_Package_Integrity::validate` gegen Paket 0.28.66: **61/61, PASS**.
- Original `PSTE_Normal_Metadata_Path::candidateTitleBeforeCategory` gegen 3 real signierte Archive-Profile mit tatsächlich 5-teiligem Originaltupel: **27 Prüfungen PASS**, einschließlich falschem Quellenprofil/tamper BLOCKED.
- Original `PSTE_Repository::persistFreshRetainedNonPass` gegen originale 3 signierte Belege + **simulierten** WordPress-Speicher: **21 Prüfungen PASS**, alter Beleg bleibt, kein READY bei Nichtbestehen.
- Original `PSERC_Plan_Compile_Job::tickActivate`: **11 Prüfungen PASS**, null ready schützt alten aktiven, beschädigter Status blockiert; WP-Speicher simuliert.
- Original `PSERC_Plan_Compile_Job::tick('INIT')`: **3 Prüfungen PASS**, null Planung startet keine Index-/Themenverarbeitung, WP-Speicher simuliert.
- Vollworkflow-Simulation **64/64 PASS** mit historischen echten 3 Quellen **aber simuliertem DataForSEO-HTTP, simuliertem WP und simuliertem K0-Writersink**. **Kein echter K0- oder WordPress-Lauf**. Diese Ziffern allein dürfen **nicht** als Live-GO bezeichnet werden.

**Exakte ZIP-Bytes:**
- `PSTE-0.57.144.38-KISS-KORREKTUR-NUR-WP-TEST.zip`, 651858 Bytes SHA256 `150af6138cca79f931e9d2f68d723184d08c180d59d2531b501e8724fdcd6117`.
- `PSERC-0.28.66-KISS-KORREKTUR-NUR-WP-TEST.zip`, 269536 Bytes SHA256 `e7868ab35af555765f3e7db5675a22219be83783967e14c32dd8e974fce22487`.
- **Ein gemeinsames Ablagearchiv**, KEIN WordPress-Plugin: `PFERDEATELIER-KISS-GEMEINSAMER-WORKFLOW-TESTPAKET-20261111.zip`, 919232 Bytes SHA256 `30035370a2f1ae64dabc6d59a994d6d368a3bb22ede5d6e7abadca7715a2b115`. Beinhaltet beide getrennten WP-ZIPs, historische unveränderte 3-Artikel-Sicherung, Prüfbericht und zwei Quellcode-Diffs. Alles dauerhaft unter `/pferdeatelier/PLUGINS/QA/` gespeichert.

## RESTHÜRDE – WICHTIG, nicht noch eine kaputte Freigabe erfinden
**Die bereits durch .37 beschädigte echte WordPress-TEST-Datenbank hat laut letztem Bericht aktuell `planning_ready=0`.** Diese beiden Codekorrekturen verhindern weitere falsche Konflikte/Nullaktivierung, **stellen aber den alten validen READY=3-Datenstand NICHT rückwirkend automatisch wieder her**. Es gibt keinen von diesem Chat ausgeführten WordPress-/MySQL-Zugriff. Ein voller 5.000er-Audit ist weder nötig noch erlaubt; **nicht erneut die Produktionsautomatik starten**.

Vor einem ernsthaften K0-Handoff:
1. Auf **getrennter TEST-WP** ausschließlich gezielt die 3 ehemaligen Quellthemen lesen: `horseware regendecken`, `fliegen regendecke pferd`, `regendecke pferd 0g`. Mit dem Original-Dreierplan die **exakte** Raw-Identität, Provenienz, Sprach-/Titelbelege, Kategorie/Slot und noch gespeicherte ältere PSERC-Generation nachweisen.
2. Nur nach live bestätigter Herkunft **gezielt** die 3 originalen Signaturen durch den vorhandenen normalen Quellen-/Planfreigabeweg anbinden, ohne alte Hashes künstlich neu zu setzen und ohne 5.000er-Recheck. Ist ein erforderlicher Beleg verloren, muss genau dieser als fehlend markiert werden. Keine automatische Rückschreibung eines 2026-11-10-Exports gegen einen neuen 2026-11-11-Bestand.
3. Reale Abnahme: 3 READY, korrekte signierte `BOUND_TYPE`-Suchintention aus bestehendem SEO-Owner, WordPress-sicherer neuer PSERC-Metadatenexport, **K0 unverändert**.

**Abnahmegrenzen:** `SOURCE_ROOT_FIX_LOCAL_QA_PASS`, `REAL_WP_RECOVERY_STILL_OPEN`, `NO_PRODUCTION_APPROVAL`. Der Nutzer muss jetzt nicht blind installieren oder erneut 5.000 Themen prüfen. Weiteres reales Live-WP-Vorgehen erst nach belegtem aktuellen Datenstand.
