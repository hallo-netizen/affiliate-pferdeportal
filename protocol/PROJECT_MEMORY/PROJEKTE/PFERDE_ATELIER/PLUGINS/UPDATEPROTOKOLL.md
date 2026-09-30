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

