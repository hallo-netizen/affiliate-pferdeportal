# PFERDE-ATELIER – PLUGIN-UPDATEPROTOKOLL

STAND: 2026-09-12
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

## REGEL FÜR FACHBÜROS

Nach einem relevanten Update genügt im zuständigen Fachbüro der Rückverweis:

`PLUGIN_UPDATE_REF: PU-YYYYMMDD-NNN`

Fachliche Release-/Testbelege bleiben dort, wo sie autoritativ hingehören. Das vollständige Updateereignis wird hier nicht ein zweites Mal im Fachbüro kopiert.
