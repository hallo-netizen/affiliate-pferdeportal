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
