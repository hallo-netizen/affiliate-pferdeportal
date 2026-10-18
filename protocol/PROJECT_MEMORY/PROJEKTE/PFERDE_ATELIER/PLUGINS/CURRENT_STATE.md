# PFERDE-ATELIER – PLUGINS – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

> **Einzige aktuelle Zustandsautorität dieses Scopes.** Status, erster offener Blocker und NEXT ACTION werden nur hier gepflegt.  
> `HOBBYRAUM.md` ist lediglich abgeleitete Ausführungsfläche.


STAND: 2026-10-18 (PSTE 0.57.106 lokaler Installations-/Fortschrittsstatus PASS; Live-E2E weiterhin nicht geprüft)
STATUS: **AKTIV / SEO-WORKFLOW PPA-005/PPA-006 BLOCKED (LIVE-GESAMTWEG NICHT BELEGT)**

## AUTORITÄT
Diese Datei ist die einzige aktuelle Standzusammenfassung des PLUGINS-Büros.

- Inventar / Artefaktstatus → `REGISTER.md`
- Änderungs-/Updatevorgänge → `UPDATEPROTOKOLL.md`
- Ausführungsdetails/Locks → `HOBBYRAUM.md` (abgeleitet, nicht autoritativ)
- Sync-Regeln → `SYNC_VERTRAG.md`

## AKTUELL BELASTBAR SYNCHRONISIERT – HEUTE RELEVANT

- PPA-002 Pferde Atelier Design **1.50.541** / WordPress-LIVE PASS / SHA `f93870321df4a989e8ceeb71d6a9b4a0780831184f3b9a36f1e6e29b5e8a6ee6`.
- PPA-003 Bildzentrale **2.7.6** / local hard PASS / Pferde-LIVE-Funktion PASS / SHA `12edc4405560ac3b149cf76a0b6e65694337b1533c0ea5e3a777d3b6c98ccbf0`.
- PPA-011 Pferderassen Manager **0.2.7** / WordPress-LIVE PASS.
- PPA-012 Universal Glossary Engine **1.4.7** / WordPress-LIVE PASS / 92er Endbestand bestätigt.
- PPA-014 WordPress Speicheranalyse **1.1.0** / local hard PASS / LIVE offen.
- PPA-015 Rassentexte-Textpflege **1.1.0** / WordPress-LIVE PASS / einmaliger Auftrag abgeschlossen.

Andere bereits synchronisierte Pluginstände und bestehende Inventarlücken stehen ausschließlich im `REGISTER.md`.

## KORREKTUR PPA-013

`PPA-013` war eine irrtümlich angelegte zweite ID für `Pferde Atelier Design`. Kanonische ID ist `PPA-002`. Die alte PPA-013-Kopie wurde aus dem aktiven Plugin-Schrank entfernt und unter `/Campus-Plugins/PFERDE_ATELIER/ARCHIV/PPA-013` abgelegt. Sie ist **nicht CURRENT**.

## PPA-005 NEUER LOKALER TESTKANDIDAT – 18.10.2026

- **Tatsächlicher, aus bestehendem Original gebauter WordPress-Plugin-ZIP-Kandidat**: Library `/Pferdeatelier/PFERDEATELIER_SEO_THEMENENGINE_0.57.105_KISS_LOKALTEST.zip` (kein bloßer Patch), SHA-256 `f202f396b3d2c2e7e3c3be2b32680be03531319d7a7f6e3cb53c487b745aae6e`, 569786 Bytes.
- Bytegenaue Ausgangsquelle: PSTE 0.57.102, SHA-256 `ddc05f0f2e05ba21a2acd0a139ac2e6788c6fcfb4b1226a75335a2eaea9d3ba5`, aus vorhandener Pferdeatelier-Bibliothek erfolgreich lokal gelesen. **117/117 Originaldateien vorhanden, genau vier bestehende PHP-Dateien geändert**: Hauptdatei (Version), Normal-Metadata-Path, Journal-Semantic-Router und Article-Type-Extension-Router. Alle anderen Bytes bleiben unverändert. Kein neues Plugin oder Tabellenumbau.
- Lokal geprüft: PHP-8.4-Syntax sämtlicher 79 PHP-Dateien, fehlerfreie ZIP-Integrität, echte alte Titel- und Signaturklassen mit WordPress-Kategoriereadback-Stubs; Positivtests bestehender Fach-/Magazin-Kategorien, falscher Familienhinweis, echte fehlende Kategorie ausschließlich nach Titel-PASS, kein Produktionshandoff bei fehlender Kategorie; Negativtests Relevanz, Preis-/Vergleichsintention und Medizin-Risikohalt.
- **Nur lokaler Testkandidat**, nicht installiert, keine vollständige WordPress-/MariaDB-5014-E2E-Prüfung, **keine Live-Freigabe**. Den bisherigen Quellpatch nicht zusätzlich auf diesen bereits gebauten Kandidaten anwenden. PSERC und PPM unberührt.
- **Zusätzliche reproduzierte Installationsprüfung 18.10.2026**: tatsächliche ZIP unverändert (SHA-256 wie oben) als `PFERDEATELIER_SEO_THEMENENGINE_0.57.105_INSTALLIERBAR_GEPRUEFT.zip` zusätzlich in `/Pferdeatelier/` abgelegt. `unzip -t` PASS, 117 Dateien / 79 PHP-Dateien Syntax PASS, PHP-8.4 WordPress-Bootstrap-Simulation einschließlich Hook-Registrierung und `register_activation_hook` PASS, Aktivierung beim Neuinstallationsfall sicher `PENDING` ohne Content-/Kategorieänderung PASS, Aktualisierung einer bestehenden READY-Installation behält READY bei und schreibt nur Boot-Status PASS. Positiv-/Negativ-Regression der bestehenden Fach-/Magazin-/Risikoklassen PASS. **Installierbares Paket zum WordPress-Test vorhanden; kein behaupteter Live-WP-/5014-Produktions-E2E-PASS**. Nutzer soll nur dieses installierbare ZIP erhalten, nicht den unfreigegeben bezeichneten Testkandidaten.

## PPA-005 KORREKTUR NACH WORDPRESS-SCREENSHOTS – 18.10.2026

- Screenshot der realen Installation 0.57.105: automatische Bestandsprüfung zeigt nach Start zunächst `BESTAND · RUNNING 0/5014`, während der ältere gespeicherte Bestands-/Fehlerstand `CANCELLED 520/5014` ausweist. Ein reales 5014-Endergebnis oder Server-Driver-Fortschritt ist damit **nicht** belegt.
- **Belegbare Quellursache für die irreführende Anzeige**: `PSTE_Admin::productionAutoState()` aus 0.57.105 wertet die laufende Bestandsqueue **vor** dem laufenden Kontext-/Portalabgleich aus. `productionAutoPortalPreflightStep()` bearbeitet jedoch den Kontext zuerst. Die Oberfläche kann deshalb `BESTAND RUNNING 0/5014` zeigen, während tatsächlich ein Kontext-Worker bearbeitet wird; bei lange nicht veränderten Statusfeldern fehlt eine ausdrückliche Anzeige über Stillstand.
- **Warum der Zähler 0 werden kann**: `PSTE_Breadth_Research_Queue::beginLogicChangedLocalRevalidation()` und `beginEvidenceRevalidation()` starten nach relevanten geänderten Entscheidungen eine neue Prüfung mit `local_backlog_cursor=0` und `local_backlog_processed=0`. Die alte vollständig bestätigte Queue bleibt dabei in `previous_completed_queue` erhalten. Die 5016 gespeicherten Themen im WordPress-Screenshot sprechen **nicht** für verlorene Themendatensätze. Die alte 520er-Pause und ein vollständig bestätigter älterer Audit sind unterschiedliche Zustände, keine unbewiesene Fortsetzung.
- **KISS-Plugin 0.57.106 – lokal installierbar geprüft**: `/Pferdeatelier/PFERDEATELIER_SEO_THEMENENGINE_0.57.106_FORTSCHRITT_ERHALTEN_INSTALLIERBAR.zip`, SHA-256 `cadafc5a3fa06407765aa309e5481c73a882f3d4435231f3af2d03c345fc42d0`, 570201 Bytes, 117 Dateien. Gegenüber 0.57.105 sind **nur** `includes/class-pste-admin.php` (Anzeige) und `portal-seo-topic-engine.php` (Version) verändert; Queue, Datenbanklogik, Fach/Magazin, PSERC und PPM bleiben **bytegleich**. Der echte aktive Kontextstatus wird jetzt vor der Queue angezeigt; alte fertig gespeicherte Vorgängerprüfungen erscheinen getrennt vom aktuellen Recheck; `180s` ohne gespeicherten Schritt wird als `STOCKT (GESPEICHERT)` markiert, **ohne** die Queue zu löschen oder neu zu starten. Die Anzeigeänderung allein beendet keine echte Wiederbewertung nach geänderter Semantik.
- **Lokale Belege**: 79 PHP-Lints PASS, ZIP-Integrität PASS, Plugin-Boot und Update bestehender READY-Installation im WP-Mock PASS; 8 Status-/Fortsetzungs-Positiv-/Negativfälle PASS, darunter die alte 0.57.105 als reproduzierter Fehler. **Kein WordPress-/MariaDB-/5014-Live-E2E und keine Freigabe des gesamten Produktionswegs behauptet.** Der Benutzer soll nur das installierbare Plugin bekommen, keine weiteren Prüfwerkzeuge.

## OFFENE INVENTARLÜCKEN

PPA-006: ältere Artefakt-/Versionsbindung im `REGISTER.md` noch offen und heute als SEO-Plugin-Arbeit betroffen; **kein neuer kanonischer Release belegt**. PPA-008 und PPA-009: offene Inventarlücken, nicht Gegenstand dieser SEO-Arbeit.

## SEO-PLUGINSTATUS / BELASTBARE GRENZE – 17.10.2026

- Zuständiger Auftrag: bestehende SEO-Themenengine **PPA-005** und SEO-Compiler **PPA-006**; keine Architekturänderung und kein drittes manuelles Plugin für diese SEO-Korrektur. K0-Autorität für die tatsächliche Artikelproduktion bleibt unberührt.
- Belegbar vorhandene, lokal unbeschädigte ZIP-Kandidaten: **PSTE 0.57.102** SHA-256 `ddc05f0f2e05ba21a2acd0a139ac2e6788c6fcfb4b1226a75335a2eaea9d3ba5`; **PSERC 0.28.40** SHA-256 `e56c3daac97d90f251acf754d00935fc05469b770a6cefa3ec29f37765c555f5`. Diese lokalen ZIPs sind **kein aktueller technischer Hauptquellen-/Live-/Release-Nachweis** und ersetzen die bisherigen isolierten CURRENT.zip nicht.
- Letzte überprüfbare Nutzerdiagnose vom **16.10.2026 16:25:40 UTC**, Run `50cdce49-683f-4084-a17a-6c56a72de9f9`: Bestandsautomatik `CANCELLED`, **520/5014**, `PSTE_EXISTING_EVIDENCE_REENTRY_REVIEW_CANDIDATE_MISMATCH`, Provideraufrufe 0. Unabhängiger globaler Compiler: `COMPLETE`, 55 Kandidaten, 1 bereit. Daraus folgt **kein Gesamtworkflow-PASS**.
- Ursächlich belegte offene Programm-/Datenabweichungen aus lokalem Quellgegencheck: redaktionelle Magazin-Weiche nicht allgemein gleichberechtigt (z. B. „Warum leckt mein Pferd viel am Salzleckstein?“ fälschlich Produkt-FAQ); neun Journal-Kategorien aus zentraler TSV nicht in der historischen WP-Produktionskategorienmenge; Start-/Rückkehrlauf durch einzelnen veralteten Nachweis blockiert; globale Datei-Bereitmeldung kann trotz abgebrochener Bestandsautomatik erscheinen. Der historische Export enthält **4501** Themen, nicht den aktuellen **5014**-Livebestand.
- **KISS-Änderung vom 18.10.2026 (NICHT installiert):** Im bestehenden 13-Datei-Quellpatch `PSTE_FOUR_WORKERS_UNIFIED_EXISTING_PLUGIN_20261017.patch` (Blob `fa875f06bbeacebb04491a7f5f8e14906a55e871`) wurden die alten Forschungsfamilien-/Familienhint-Vorabstopps und die doppelte Titelausführung gelöscht. Auch die falsche Voraussetzung, dass jeder Fragetitel gleichzeitig die FAQ- UND Magazin-Titelprüfung bestehen muss, wurde entfernt; die vorzeitige Fach-Erweiterungsannahme wurde hinter die gemeinsame Magazin-/Fach-Weiche verlegt; die Magazinentscheidung erhielt keine vorgeschlagene Forschungsfamilie mehr und ein redundanter Zwischenstatus sowie ein vorzeitiger Magazin-Vermutungsstop wurden gelöscht, sodass vorhandene geprüfte Fachwege weiterlaufen können; die Prüfung des später tatsächlich gewählten Artikeltyps bleibt weiterhin verbindlich. In-memory-Diff-Simulation mit 38 konsistenten Hunks und unveränderten Risiko-/Signaturwachen geprüft; zusätzliche PHP-Regressionen nur vorbereitet, noch nicht ausgeführt. Die älteren inkrementellen Family-Entfernungsdeltas nicht zusätzlich anwenden. Weiterhin kein Live-Test oder Release.
- **Erster operativer Blocker:** kein frischer, byte-/versionsgebundener **WordPress-/MariaDB-Live-Readback des installierten Zweier-Pluginstands und der vollständigen 5014 Einzelthemen**, daher keine echte 1:1-Gesamtworkflow-Simulation oder Releasefreigabe. Kein neues Plugin freigegeben.
- Fehler-/Testchronik und Belege: ausschließlich `UPDATEPROTOKOLL.md` Vorgang `PU-20261017-001`; bestehendes Fach-/Kategorie-Routing in `affiliate-release-current:protocol/PFERDE_ATELIER_CATEGORY_CHANGE_MASTER_20260922.md` Abschnitt 29. Diese Pfade sind **keine zweite Current-Autorität**.

## NEXT ACTION

**Genau eine:** Den aktuell installierten PSTE-/PSERC-Quellstand einschließlich der realen vollständigen 5014-Keyword- und Kategorie-/Zustandsdaten aus WordPress/MariaDB **read-only, hash- und versionsgebunden** ermitteln und den echten bestehenden Keyword→Titel→gemeinsame Kategorie→PSERC→PPM→Datei-Ablauf einschließlich Positiv-/Negativ-, Fortsetzungs- und Verlustfreiheitsprüfung auf einer identischen isolierten Kopie verifizieren. Bis zum belegten Gesamt-PASS: **BLOCKED, kein Plugin-Release, kein Auto-Publish**.
