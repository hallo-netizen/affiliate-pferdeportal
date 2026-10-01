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
