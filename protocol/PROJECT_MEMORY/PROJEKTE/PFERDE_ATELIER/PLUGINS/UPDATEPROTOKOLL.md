# PFERDE-ATELIER – PLUGIN-UPDATEPROTOKOLL

STAND: 2026-09-30
STATUS: APPEND-ONLY-CHRONIK

## ROLLE

Diese Datei protokolliert **tatsächlich ausgeführte** Plugin-Updates, Deaktivierungen, Reaktivierungen, Ersetzungen und Löschungen des Pferde-Ateliers.

Sie ist keine Release-Hauptquelle und keine zweite Fachchronik.

## ID-SCHEMA

`PU-YYYYMMDD-NNN`

Fortlaufend pro Kalendertag ab `001`.

## PFLICHTBLOCK

```text
## PU-YYYYMMDD-NNN – <Pluginname>
DATUM:
PLUGIN_ID:
ART: UPDATE | DEAKTIVIERUNG | REAKTIVIERUNG | ERSATZ | LÖSCHUNG
HERKUNFT: EIGEN | DRITTANBIETER
FACHBÜRO:
VON_VERSION:
AUF_VERSION:
UPDATEQUELLE:
WARUM:
ABHÄNGIGKEITEN:
FEHLERQUELLEN_GEPRÜFT:
BACKUP_ROLLBACK_REF:
POSITIVTEST:
NEGATIVTEST:
FACH_REGRESSION:
WORDPRESS_LIVEKONTROLLE:
ERGEBNIS: PASS | FAIL | ROLLBACK | BLOCKED
FACHBÜRO_REF:
NOTIZ:
```

## BASELINE – KEIN UPDATE

### INVENTAR-BASELINE-20260912

Am 12.09.2026 wurden sechs WordPress-Screenshots inventarisiert.

- 55 sichtbare Pluginzeilen;
- 28 Eigenentwicklungszeilen / 27 unterschiedliche Eigen-/Projektplugins;
- 4 sichtbar inaktive Zeilen;
- mehrere sichtbare Drittanbieter-Updatehinweise.

**Es wurde dabei kein Plugin verändert.** Deshalb existiert für die Baseline bewusst keine `PU-*`-ID.

Vollständiger Bestand: `PLUGINREGISTER.md`.

## STATUS-SYNC 2026-09-24 – KEIN NEUES PU-EREIGNIS

Die Kategorie-/Pluginstände wurden am 24.09.2026 in PLUGINS und den betroffenen Fachbüros auf die bereits bewiesene technische Current-Autorität nachgeführt.

Diese Änderung ist **nur Dokumentationssynchronisierung**. Es wurde durch diesen Campus-Nachtrag kein Plugin installiert, ersetzt, deaktiviert, reaktiviert oder gelöscht. Deshalb wird bewusst **keine erfundene PU-ID** angelegt.

## REGEL FÜR FACHBÜROS

Nach einem relevanten Update genügt im zuständigen Fachbüro der Rückverweis:

`PLUGIN_UPDATE_REF: PU-YYYYMMDD-NNN`

Fachliche Release-/Testbelege bleiben dort, wo sie autoritativ hingehören. Das vollständige Updateereignis wird hier nicht ein zweites Mal im Fachbüro kopiert.


## PU-20260930-001 – Affiliate-Zentrale (Portal-kompatibel)

DATUM: 2026-09-30  
PLUGIN_ID: PA-E-003  
ART: ERSATZ  
HERKUNFT: EIGEN  
FACHBÜRO: AFFILIATE  
VON_VERSION: 6.72.165  
AUF_VERSION: 6.72.165  
UPDATEQUELLE: `AFFILIATE_ZENTRALE_V6.72.165_STORAGE_ROOTFIX_FUNCTION_PRESERVING_HARD_PASS.zip`  
WARUM: vorhandene eBay-Housekeeping-Bedingung erkannte den normalen endgültig beendeten Zustand `output_state=inactive + status=purged_ended` nicht; dadurch konnten alte große Rohpayloads trotz bestehender 180-Tage-Housekeepingregel liegenbleiben. Nachhaltiger Storage-Fix ohne Änderung der fachlichen Affiliatefunktion.  
ABHÄNGIGKEITEN: bestehende Performanceoptimierungen der Affiliate-Zentrale; eBay-Lifecycle/Housekeeping; Provider-/Ranking-/Slot-/Veto-/Outputlogik darf unverändert bleiben.  
FEHLERQUELLEN_GEPRÜFT: Affiliate-Release-Governance + aktuelle Performancearbeit; Storage-Fix auf Housekeeping-Predicate begrenzt.  
BACKUP_ROLLBACK_REF: exakter 6.72.165-Fallback SHA-256 `0170c89cf7381bc4a99c379277b529a7056bf61ec47683c027fef7c536fafb21`.  
POSITIVTEST: normaler alter `ended / inactive / purged_ended`-Datensatz wird nach Altersgrenze für Payload-Kompaktion erfasst; bereits bestehende historische `none`-/`purged_ended`-Fälle bleiben erfasst.  
NEGATIVTEST: aktive/verfügbare, junge, listing-verknüpfte und bereits kompaktierte Datensätze bleiben ausgeschlossen.  
FACH_REGRESSION: Hauptdatei und eBay-Runtime gegenüber exaktem 6.72.165-Performancepaket unverändert; Änderung nur in `includes/trait-ppar-housekeeping.php`; PHP-Lint 21/21 PASS; Fresh-Unpack/Predicate-Tests PASS.  
WORDPRESS_LIVEKONTROLLE: Nutzer bestätigt Installation; aktuelle WordPress-Pluginliste zeigt Affiliate-Zentrale aktiv als 6.72.165. Wegen absichtlich unveränderter Versionsnummer ist die konkrete neue Housekeeping-Codezeile aus der Pluginliste allein nicht bytegenau beweisbar.  
ERGEBNIS: PASS  
FACHBÜRO_REF: Affiliate-Governance bleibt technische Autorität; dieser Eintrag dokumentiert ausschließlich das tatsächlich ausgeführte WordPress-Ersatzereignis.  
NOTIZ: Gleichversionierter Ersatz war für Nachvollziehbarkeit ungünstig. Künftige fachlich relevante Plugin-Releases wieder fortlaufend versionieren; keine Miniversion pro Einzelbefund.

## PU-20260930-002 – Portal SEO Themenengine

DATUM: 2026-09-30  
PLUGIN_ID: PA-E-019  
ART: UPDATE  
HERKUNFT: EIGEN  
FACHBÜRO: TEXT  
VON_VERSION: 0.57.12  
AUF_VERSION: 0.57.13  
UPDATEQUELLE: `PSTE-0.57.13-DATABASE_STORAGE_CLEANUP_PERFORMANCE_SAFE_HARD_PASS.zip`; Kandidaten-SHA-256 `bb5f3cc84dc00fa85e2c0ddf48c8994a4788c2595c6d98f0d440780377060248`  
WARUM: vorhandene PSTE-Speicherstände verlustfrei verdichten und erneutes unnötiges Datenwachstum begrenzen, ohne Recherche-, Kategorie-, Produktions-, Recovery-, Rollback- oder Performancefunktion abzusenken.  
ABHÄNGIGKEITEN: Topic-Pool und Keyword-Autoritäten; Research-/Run-Snapshots; Candidate-Payloads; Parkarchive; Sandbox-/Rollbackdaten; PSERC-0.28.27-Bindung; bestehende Performancepfade.  
FEHLERQUELLEN_GEPRÜFT: finaler Kandidat nach Verwerfen früherer Zwischenstände mit zu breitem Storage-Loading, unvollständigen Active-Work-Sperren und später gefundener `.orig`-Backup-Datei vollständig neu gebaut und neu getestet.  
BACKUP_ROLLBACK_REF: Legacy-Restore-/Rollbackpfad des finalen 0.57.13-Kandidaten; 0.57.12 bleibt technischer Rückfallbezug.  
POSITIVTEST: Storage Core 22/22 PASS; Public Storage API 8/8 PASS; Rollback Restore 17/17 PASS; Restore Mode 7/7 PASS; Atomic Lock 3/3 PASS.  
NEGATIVTEST: Maintenance/Active-Work Guards 10/10 PASS; aktive Arbeit darf nicht verdichtet werden; Topic-Pool und Legacy-Sandbox-Rollbackautorität bleiben unangetastet.  
FACH_REGRESSION: Fresh-Unpack PHP-Lint 78/78 PASS; PSERC-0.28.27-Bindung PASS; Contracts/Fixtures fachlich unverändert; keine neue Frontendlast.  
WORDPRESS_LIVEKONTROLLE: Nutzer bestätigt Installation; aktuelle WordPress-Pluginliste zeigt Portal SEO Themenengine aktiv als Version 0.57.13. Die Pluginliste bestätigt Version/Aktivstatus, nicht unabhängig den exakten Live-Bytebestand.  
ERGEBNIS: PASS  
FACHBÜRO_REF: TEXT; dort nur Rückverweis auf `PLUGIN_UPDATE_REF: PU-20260930-002`.  
NOTIZ: Installation ist abgeschlossen. PSTE-Altbestände wurden noch nicht bereinigt; nächste Aktion ist ausschließlich die eingebaute begrenzte Speicherpflege, keine manuelle DB-Löschung.

## PU-20260930-003 – Affiliate-Zentrale (Portal-kompatibel)

DATUM: 2026-09-30  
PLUGIN_ID: PA-E-003  
ART: UPDATE  
HERKUNFT: EIGEN  
FACHBÜRO: AFFILIATE  
VON_VERSION: 6.72.165  
AUF_VERSION: 6.72.167  
UPDATEQUELLE: `release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.167.zip`; Installer-SHA-256 `998730894c4dbd677bbee04bff947df740800a6c6ab9524b747a0da5a5f8adc0`  
WARUM: eBay-Lauf-/Recovery-/Statuskomplexität stark reduzieren und erneutes unnötiges eBay-Datenwachstum begrenzen, ohne Provider-, PRIVATE/BUSINESS-, Coverage-, Qualitäts-, Affiliate-, Compliance-, Veto-, Frontend- oder Performancefunktion abzusenken.  
ABHÄNGIGKEITEN: bestehende 6.72.166-Performancepfade; eBay OAuth/Compliance; PRIVATE/BUSINESS-Ausgabe; Checkpoint/Coverage/Public-Gates; zentraler Housekeeping-Pfad.  
FEHLERQUELLEN_GEPRÜFT: `AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md`; aktuelle Release-Governance `control/release-governance/CURRENT_RELEASE.json`; 6.72.167 Full-Gate-Evidence.  
BACKUP_ROLLBACK_REF: vorheriger realer Live-Stand 6.72.165; finaler 6.72.167-Installer ist hashgebunden; 6.72.166 blieb technische Performancebasis.  
POSITIVTEST: eBay OAuth-Test unabhängig von Kanalpause; alter terminaler Lauf wird begrenzt historisiert; beendete nicht öffentliche eBay-Rohpayloads werden nach 7 Tagen verdichtet.  
NEGATIVTEST: normale Runtime bleibt bei Kanalpause fail-closed; aktive, junge, listing-gebundene und öffentliche eBay-Daten bleiben unangetastet; aktuelle Checkpoint-/Coverage-/Public-Gates bleiben erhalten.  
FACH_REGRESSION: Full Gate Run `36732596301`; WordPress 7.1.2 + MariaDB PASS; PHP-Lint 21/21 PASS; 6.72.166-Frontend-/Query-Performancepfade erhalten; Source→ZIP 27/27 byteidentisch; Fresh-Unpack PASS.  
WORDPRESS_LIVEKONTROLLE: Nutzer bestätigt Installation/Aktivstatus von 6.72.167. Danach `Speichern & OAuth prüfen` ausgeführt; eBay OAuth laut Nutzer erfolgreich.  
ERGEBNIS: PASS  
FACHBÜRO_REF: technische Release-Evidence `release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md`; aktuelle technische Releaseautorität bleibt `affiliate-release-current:control/release-governance/CURRENT_RELEASE.json`.  
NOTIZ: 6.72.168 ist bereits technisch RELEASED, aber zum Abschlusszeitpunkt noch nicht live installiert; dafür bewusst kein erfundener PU-Eintrag.

## RELEASE-VORBEREITUNG 2026-10-01 – PA-E-003 / KEIN PU-EREIGNIS

Affiliate-Zentrale **6.72.171** wurde technisch fertiggestellt und vor Übergabe lokal exakt gegen 6.72.170 geprüft.

- Source-Head: `ad4db0c34552667a9d398d4b74cb7d8b7130f03a`
- Source-Manifest SHA-256: `5094f6df73c172b01819294d3dd455002fa244aa9676da0ebbbb4b058530dda4`
- finaler Installer SHA-256: `dbe630c72f5273abb5c3b48223bbed00498be0a0578f18eca3f001e92bb03fba`
- Exact Local A-B Run `36839006440`: SUCCESS / Positiv+Negativ / funktional 1:1
- 2012er Snapshot A-B Run `36839006513`: SUCCESS / funktional 1:1 / Gesamt -80,01 %, Leaf -89,87 %
- finaler Full-Gate Run `36842612555`: SUCCESS / Source→ZIP 27/27 / Fresh-Unpack / Provider-, Storage-, Import- und Frontend-Gates PASS

**Bewusst keine neue PU-ID:** Zum Zeitpunkt dieses Protokolleintrags ist die WordPress-Installation von 6.72.171 noch nicht readback-bestätigt. Dieses Updateprotokoll erfindet kein ausgeführtes Live-Update. Nach Installation/Readback wird genau dann das tatsächliche PU-Ereignis ergänzt.

## LIVE-READBACK 2026-10-01 – PA-E-003 / KEIN NEUES PU-EREIGNIS

Der WordPress-Uploadvergleich des Nutzers zeigt für Affiliate-Zentrale **Aktuell 6.72.170** und für das hochgeladene falsche Paket **6.72.169**. Damit ist 6.72.170 der neue belastbare installierte Versions-Readback. Das konkrete frühere Updateereignis auf 6.72.170 wird mangels vollständiger Ausführungsdaten nicht rückwirkend als erfundene PU-ID angelegt.

Der falsche 6.72.169-Installer wurde verworfen. Nächster zulässiger Installer ist ausschließlich der final gegatete 6.72.171-Installer mit SHA-256 `dbe630c72f5273abb5c3b48223bbed00498be0a0578f18eca3f001e92bb03fba`.

## PU-20261001-001 – Portal SEO Redaktionsplan Compiler
DATUM: 2026-10-01
PLUGIN_ID: PA-E-017
ART: UPDATE
HERKUNFT: EIGEN
FACHBÜRO: TEXT
VON_VERSION: 0.28.27
AUF_VERSION: 0.28.29-kiss-storage-safe
UPDATEQUELLE: im TEXT-Arbeitsstrang lokal auf der geprüften 0.28.27-Basis gebaut
WARUM: KISS-Handoff, Storage-/Retention-Sicherheit und Entfernung eindeutig toter Paketaltlasten ohne Inhalts-/SEO-/Qualitätsfunktionsänderung
ABHÄNGIGKEITEN: PPM 6.7.9; Redaktionsplan-/Slotidentität; K9-5-Felder-Handoff
FEHLERQUELLEN_GEPRÜFT: wiederholte Import-/Slotkollisionen und schneller technischer Generationsspeicherzuwachs
BACKUP_ROLLBACK_REF: vorherige 0.28.27 bleibt Rollbackbasis; keine Löschung produktiver Inhalte
POSITIVTEST: Paketintegrität PASS; PHP-Syntax 43/43 PASS; Redaktionsplan-/Importerpfad funktionsgleich für geschützte Fälle
NEGATIVTEST: aktive/aktuelle/Rückfallgenerationen bleiben geschützt; Papierkorb-Slots blockieren keinen neuen legitimen Import
FACH_REGRESSION: keine Änderung an LT 6.8 / PPM 6.7.9 / PSERC-Fachregeln / Publish-Sperre
WORDPRESS_LIVEKONTROLLE: WordPress-Seite zeigt direkt `SEO-Redaktionsplan Metadaten-Vorschau 0.28.29-kiss-storage-safe`
ERGEBNIS: PASS
FACHBÜRO_REF: `../TEXT/CURRENT_STATE.md`
NOTIZ: PSTE-Themenverwertungsarbeit ist separat; dieses Update ist keine Themenfreigabe.

## LIVE-READBACK 2026-10-01 – PSTE / KEIN ERFUNDENES PU-EREIGNIS

Direkter WordPress-Versionsvergleich belegt Portal SEO Themenengine **0.57.15 aktuell**. Später ist operativ ein fortgesetzter V9-Portalabgleich ohne Neustart sichtbar, die bereitgestellten späteren Screenshots zeigen jedoch keine Versionsnummer. Deshalb wird kein höheres ausgeführtes Updateereignis rückwirkend erfunden. Der technische Resume-Fix und die Themenverwertungsgrenzen stehen in `protocol/PSTE_TOPIC_REUSE_AND_CONTEXT_RESUME_CLOSEOUT_20261001.md`.


## PU-20261001-002 – Affiliate-Zentrale (Portal-kompatibel)

DATUM: 2026-10-01  
PLUGIN_ID: PA-E-003  
ART: UPDATE  
HERKUNFT: EIGEN  
FACHBÜRO: AFFILIATE  
VON_VERSION: 6.72.171  
AUF_VERSION: 6.72.172  
UPDATEQUELLE: geprüfter Handoff-Installer `AFFILIATE_ZENTRALE_6.72.172.zip`; SHA-256 `c9fd44b97793422890a46b87dcdcbc88ce52ae26437b77173a64c9d976b73a25`  
WARUM: vorhandenen zentralen Housekeeping-Lauf so ergänzen, dass ausschließlich verwaiste, mindestens 24 Stunden alte `ppar-idealo-feed-*.tmp` im Upload-Root sicher entfernt werden können; kein neuer Hilfsrunner.  
ABHÄNGIGKEITEN: 6.72.171-Performanceoptimierungen; Affiliate-Housekeeping; Idealo-Worker-Lock.  
FEHLERQUELLEN_GEPRÜFT: aktuelle Affiliate-Release-Governance; Storage-Evidence 6.72.172; Performance-Hardlock.  
BACKUP_ROLLBACK_REF: technischer Vorstand 6.72.171; dessen Performance-Evidence bleibt unverändert gebunden.  
POSITIVTEST: exaktes TMP-Muster, Alter >=24h, reguläre Datei im direkten Upload-Root wird durch den gebundenen Housekeeping-Pfad erfasst; lokaler Housekeeping-Disk-Test PASS.  
NEGATIVTEST: aktiver Idealo-Worker-Lock, junge Dateien, Symlinks, Unterordner und abweichende Dateinamen bleiben ausgeschlossen; PHP-Lint 21/21, Fresh-Unpack 27/27 PASS.  
FACH_REGRESSION: keine Ranking-, Provider-, Slot-, Veto-, Tracking-, Publish-, Import- oder Frontendänderung; 6.72.171-Performancepfade nicht zurückgebaut.  
WORDPRESS_LIVEKONTROLLE: Nutzer bestätigt im laufenden Chat ausdrücklich, dass 6.72.172 bereits installiert ist. Ein neuer unabhängiger Screenshot/Byte-Readback wurde in diesem Abschlussblock nicht erneut erhoben; deshalb keine weitergehende Byteidentitätsbehauptung.  
ERGEBNIS: PASS  
FACHBÜRO_REF: technische Autorität bleibt `affiliate-release-current:control/release-governance/CURRENT_RELEASE.json`; Evidence `release/affiliate-zentrale/evidence/affiliate_router_v672172_idealo_temp_storage_local_gate_20261001.md`.  
NOTIZ: 6.72.173 ist derzeit nur Source-Kandidat mit offenem Full-Gate und ausdrücklich noch kein installiertes Updateereignis.

## PU-20261001-003 – Portal SEO Redaktionsplan Compiler

DATUM: 2026-10-01
PLUGIN_ID: PA-E-017
ART: UPDATE
HERKUNFT: EIGEN
FACHBÜRO: TEXT
VON_VERSION: 0.28.29-kiss-storage-safe
AUF_VERSION: 0.28.30
UPDATEQUELLE: lokal aus dem aktuellen 0.28.29-Paket gebaut; PSTE-V5-Binding-Kompatibilität ergänzt
WARUM: `PSERC_SEO_CAPABILITY_BINDING_BLOCKED` im INIT-Pfad beseitigen, ohne LT/PPM/PSERC-Fachregeln oder 5-Felder-Handoff zu ändern.
ABHÄNGIGKEITEN: PSTE Compiler-Read-Capability; PPM 6.7.9; K9 5-Felder-Handoff.
POSITIVTEST: reale Runtime-Matrix mit korrekter PSTE-Capability PASS; INIT kann in OCCUPIED übergehen.
NEGATIVTEST: falsche/fehlende Capability, falsches Schema/Hash/Schreibrecht weiterhin fail-closed BLOCK.
FACH_REGRESSION: Qualitätsgates unverändert; publish_allowed=false.
WORDPRESS_LIVEKONTROLLE: Nutzer installierte 0.28.30; unmittelbar danach bestand der gleiche Bindungsfehler weiter. Erst nach anschließendem PSTE-Reinstall verschwand der Livefehler und der PSERC-Lauf erreichte später COMPLETE.
ERGEBNIS: PASS ALS PSERC-SEITE / der erste Livefehler war durch den damals geladenen PSTE-Dateistand weiterhin sichtbar.
FACHBÜRO_REF: `../TEXT/CURRENT_STATE.md`.

## PU-20261001-004 – Portal SEO Themenengine

DATUM: 2026-10-01
PLUGIN_ID: PA-E-019
ART: UPDATE / REINSTALL MIT NEUER VERSION
HERKUNFT: EIGEN
FACHBÜRO: TEXT
VON_VERSION: 0.57.16-KANDIDAT
AUF_VERSION: 0.57.17
UPDATEQUELLE: geprüfter 0.57.16-Bestand; Funktionscode unverändert, neue eindeutige Versionskennung 0.57.17
WARUM: gleiche Versionsnummer beim Reinstall vermeiden und den tatsächlich geladenen Pluginstand eindeutig ersetzen.
ABHÄNGIGKEITEN: PSTE Compiler-Read-Capability; PSERC 0.28.30.
POSITIVTEST: PHP 79/79 PASS; PSTE Runtime-Capability PASS; PSERC-0.28.30-Bindung PASS; kompletter INIT-Positivpfad PASS.
NEGATIVTEST: fehlender/falscher Provider bzw. ungültige Capability weiterhin BLOCK; Publish-Sperre unverändert.
WORDPRESS_LIVEKONTROLLE: Nutzer installierte 0.57.17; der nachfolgende PSERC-/Snapshot-Weg erreichte real COMPLETE. Kein separat archivierter Pluginlisten-Screenshot wird daraus erfunden.
ERGEBNIS: PASS.
FACHBÜRO_REF: `../TEXT/CURRENT_STATE.md`.

## RELEASE-VORBEREITUNG 2026-10-01 – PSTE 0.57.18 / KEIN PU-EREIGNIS

Kandidat:
`PSTE-0.57.18-EXISTING-POTENTIAL-FIRST-HARD-PASS.zip`

Zweck:
sichere `AUTO_REENTRY_ELIGIBLE`-Sandbox-Kandidaten vor Retained Backlog und Provider-Recherche über den bestehenden Normal-Reentry verwerten.

Prüfung:
- PHP-Lint 79/79 PASS;
- Sandbox-Reentry Positiv PASS;
- gemischter Positiv/Negativ-Reentry PASS;
- Provider-Aufruf in Reuse-Phase BLOCK;
- keine eligible Sandbox erzeugt keinen künstlichen Kandidaten;
- Fresh-Unpack Wiederholung PASS.

Grenze:
0.57.18 ändert nicht die bereits vorhandene Keyword/Familien→Titel/Artikeltyp/Kategorie-Automatik und ist **keine belegte Gesamtlösung** für die geringe READY-Ausbeute des gespeicherten Topic-Pools.

Live:
nicht als installiert belegt. Die bereits laufende Recherchewelle wird dafür nicht unterbrochen.



## PU-20261002-001 – Portal SEO Themenengine

DATUM: 2026-10-02
PLUGIN_ID: PA-E-019
ART: UPDATE
HERKUNFT: EIGEN
FACHBÜRO: TEXT
VON_VERSION: 0.57.25
AUF_VERSION: 0.57.26
UPDATEQUELLE: `PSTE-0.57.26-STORED-MATERIAL-TO-TITLE-CANDIDATES-ROOTFIX-HARD-PASS.zip`
INSTALLER_SHA256: `d7d00c1b13144fc584a593993714721ec9a8679e7d65f017e1bc2ed10c1306d6`
WARUM: gespeicherten Recherchefundus in sichtbare Titelkandidaten überführen und falsches `PSTE_CONTEXT_QUERY_MISSING` bei leerem editorial_title beseitigen.
ABHÄNGIGKEITEN: bestehender Normal-Metadata-/Titelpfad; Topic-Pool/Sandbox; PSERC bleibt nachgelagertes Gate.
POSITIVTEST: lokaler Bestands-/Titelpfad vor Ausgabe geprüft; frischer COMPLETE-Render zeigt Start- und Exportbutton; Live-Readback erzeugt 695 Titelkandidaten, 8 zusätzlich PSERC-prüfbar, 36 vollständig aufbereitet.
NEGATIVTEST: kein Provideraufruf im Bestandslauf; keine Produktionsautorität aus Titelkandidaten; RUNNING→AJAX-COMPLETE reproduziert fehlendes dynamisches Einfügen des Exportformulars.
FACH_REGRESSION: Speicherpflege-/Sandbox-Schutz und Produktions-/Publish-Gates bleiben gebunden.
WORDPRESS_LIVEKONTROLLE: Nutzer-Screenshot zeigt Portal SEO Themenengine 0.57.26 und COMPLETE mit 695/8/36.
ERGEBNIS: PASS FÜR TITELGENERIERUNG / UI-NACHLAUF-FEHLER DOKUMENTIERT.
FACHBÜRO_REF: `../TEXT/CURRENT_STATE.md`.
NOTIZ: Kein weiteres Plugin für den UI-Nachlauf nötig; Reload rendert bei COMPLETE den Exportbutton.

## RELEASE-VORBEREITUNG 2026-10-03 – PSTE 0.57.27 / KEIN PU-EREIGNIS

Kandidat:
`PSTE-0.57.27-PRODUCTWAHL-CLASSIFICATION-CANDIDATE.zip`

SHA-256:
`414b18f99e676516464790c842eedebc71a72a701c32bb95bd2d924d45ae9c79`

Basis:
PSTE 0.57.26 / `d7d00c1b13144fc584a593993714721ec9a8679e7d65f017e1bc2ed10c1306d6`.

Zweck:
- Produktwahl als vorgelagerte Kandidatenklassifikation;
- getrennte Exporte Produktwahl/redaktionell;
- manuelle Review-Korrektur ohne Produktionsautorität.

Prüfung:
- ZIP-Integrität PASS;
- PHP-Lint 80/80 PASS;
- Produktwahl Positiv/Negativ + Manual-Override 13/13 PASS;
- 326er Realsample 0 MATCH / 0 REVIEW / 326 NO_MATCH;
- geschützter Storage-/Normalpfad unverändert;
- kein `payload_json`-Kopieren im neuen Manual-Override.

Grenze:
0.57.27 ist nicht live installiert/readback-bestätigt. Der nachgelagerte Produktionsstand registriert `Produktwahl` noch nicht. Der reale 695er Titelkandidaten-Export liegt für die Vollauswertung nicht vor.

**Bewusst keine PU-ID:** kein ausgeführtes WordPress-Update.



## RELEASE-VORBEREITUNG 2026-10-03 – PSTE 0.57.28 / KEIN PU-EREIGNIS

Kandidat:
`PSTE-0.57.28-SUSTAINABLE-FAMILY-STRUCTURE-ROUTING-CANDIDATE.zip`

SHA-256:
`a8df7248f38eaf2b23ce1fe30020b6c0aa2aef1881be9fe107c12da07ae11c41`

Basis:
PSTE 0.57.27 / `414b18f99e676516464790c842eedebc71a72a701c32bb95bd2d924d45ae9c79`.

Zweck:
- nachhaltige Reparatur des bestehenden Family-/Normalpfads für aktuelle und zukünftige Begriffe;
- echte familienlose portalrelevante Begriffe als `STRUCTURE_GAP` statt unspezifischem Sandbox-Kreisverkehr markieren;
- vorhandene Familiennähe/Mehrdeutigkeit weiterhin REVIEW;
- Produktwahl-Fälle bis Downstream-Registrierung nicht-produzierend halten.

Prüfung:
- ZIP-Integrität PASS;
- Fresh-Unpack PHP-Lint 81/81 PASS;
- realer 694er Read-only-Replay: 320 STRUCTURE_GAP / 371 SANDBOX_REQUIRED / 3 RETAINED_NON_PRODUCING / 0 NORMAL_PASS;
- 0 bestehende Family-MATCH-Regressionen;
- 3 zusätzliche konservative Family-Matches;
- Strukturrouter 6/6 Positiv/Negativ/Zukunft PASS;
- Produktwahl 14/14 PASS;
- 326er Realsample 0 Produktwahl-MATCH;
- geschützte Repository-/Storage-/Admin-/Provider-/Titel-/Intentpfade gegenüber 0.57.27 unverändert.

Grenze:
Nicht live installiert. Keine PU-ID, keine Release-/Live-Freigabe, keine neue Provider-Recherche, kein Publish.



## RELEASE-VORBEREITUNG 2026-10-04 – PSTE 0.57.30 / KEIN PU-EREIGNIS

Kandidat:
`PSTE-0.57.30-SANDBOX-DATAFLOW-ROOTFIX-CANDIDATE.zip`

SHA-256:
`c2f0e9e05f2ffddeea2c7ee022dd18ad04f9f5820ebbab4eabfab1253c235aa4`

Basis:
PSTE 0.57.29.

WARUM:
Live gespeicherter Einzellauf hängt bei `PSTE_SANDBOX_DATAFLOW_PORTAL_COMPONENT_DRIFT`. Der V2-Producer berechnete korrekte Komponentenhashes, aber `applyToRecord()` persistierte die gebundenen Komponenten nur beim Legacy-Vertrag.

FIX:
V2-Komponenten transient an `applyToRecord()`, vor Persistenz hash-validieren, genau einmal am Record speichern, transienten Transport vor `sandbox_dataflow`-Persistenz entfernen.

POSITIVTEST:
Vorherfehler auf 0.57.29 exakt reproduziert; 0.57.30 Record-Bindung PASS.

NEGATIVTEST:
Nachträgliche Mutation der Portal-Komponente blockiert weiterhin exakt mit `PSTE_SANDBOX_DATAFLOW_PORTAL_COMPONENT_DRIFT`.

REGRESSION:
UI-Guard 5/5; PHP 81/81; ZIP PASS; nur Contract + Versionsdatei geändert; Familien-/Produktwahl-/Normalpfad-/Driver-/Storage-Fachlogik unverändert.

LIVE:
Noch nicht installiert/readback-bestätigt. Keine PU-ID.


## RELEASE-VORBEREITUNG 2026-10-05 – PSTE 0.57.38 / KEIN PU-EREIGNIS / NICHT FINAL

Kandidat:
`PSTE-0.57.38-EDITORIAL-PLAN-COVERAGE-ROOTFIX-HARDPASS.zip`

SHA-256:
`6a6df39e6f66d612fcf998cf3e232bb58056d222ba06679a82af3cfabd288bf8`

Zweck:
- realen PSERC-5-Felder-Batch `next_textmachine_metadata_batch.items` als Editorial-Plan-Abdeckung in PSTE lesen;
- bereits geplante/geschriebene 16 Artikel nicht erneut planbar machen.

Belegte Tests:
- echter 4472er Export + echter 16er PSERC-Batch;
- alt 0/16 Plan-Treffer, 0.57.38 16/16;
- 0 falsche zusätzliche Cross-Topic-Treffer;
- PHP 81/81; JSON 54/54; Fresh-Unpack byteidentisch.

Nachträglich vor Live-Abnahme gefundener Blocker:
- bestehende Journal-/Magazinartikel werden im allgemeinen WordPress-Inventar nicht über die vorhandene Extension-Kategorieautorität aufgelöst;
- Realfall `Wie alt werden Pferde?` / Post-ID 15974 erscheint inventarseitig ohne Kategorie, obwohl Kandidatenrouting Kategorie 1486 `Pferdegesundheit verstehen` / Journal eindeutig kennt;
- Rootcause: `PSTE_Snapshot::inventory()` bindet nur reguläre `structure()['items']`-Kategorien.

Ergebnis:
**NICHT FINAL / KEINE LIVE-ABNAHME / KEINE PU-ID.**
0.57.38 ist technische Basis für genau einen konsolidierten Folgefix; kein weiteres Einzelflick-Release vor vollständiger 1:1 Positiv-/Negativ-/Regression-Simulation.
