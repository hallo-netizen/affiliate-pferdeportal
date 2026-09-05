# BILD – MASTERDATEIEN-INVENTAR

STAND: 2026-09-05
REGEL: Kein Bestandteil einer Masterdatei wird still verworfen.

## Quelle BILD-MASTER-001

Datei:
`MASTERDATEI_BILDSYSTEM_NEU_049(1).zip`

SHA-256:
`c4fb8798a99b423be0b9e8428411abf4a6fc490ec02de6f259caf2286142820c`

Größe:
49.510 Bytes

Enthält exakt:

1. `PFERDE_ATELIER_BILDZENTRALE_2.4.9_LOKALE_VORSCHAU_REPARIERT.zip`
   - Größe 48.301 Bytes
   - SHA-256 `265edaf3cee55b751b5f107e96c50dfcada99450bd94a07339e3234ae0bc47a1`
   - Zuordnung: HISTORISCHER CODEBELEG 2.4.9

2. `STATUS_BILDSYSTEM_NEU_049.txt`
   - Größe 1.399 Bytes
   - Zuordnung: HISTORISCHES FEHLER-/FIX-/TESTPROTOKOLL
   - Inhalt: lokaler Magnific-Vorschau-Fix, Begründung, positive Tests, Live-Prüfschritte.

## Quelle BILD-CODE-002

Datei:
`PFERDE_ATELIER_BILDZENTRALE_2.4.9_LOKALE_VORSCHAU_REPARIERT(1).zip`

SHA-256:
`265edaf3cee55b751b5f107e96c50dfcada99450bd94a07339e3234ae0bc47a1`

Identisch mit der eingebetteten Plugin-ZIP aus BILD-MASTER-001.

Enthält:
- Verzeichnis `pferde-atelier-bildzentrale/`
- `pferde-atelier-bildzentrale.php`
- PHP-Dateigröße: 242.591 Bytes
- PHP SHA-256: `079fe4efc6fa53ffd09c3c7490f1873f249509df17548224ead42ba7389c71c2`
- Plugin-Version: 2.4.9

Zuordnung:
HISTORISCHER VOLLSTÄNDIGER CODEBELEG.

Funktionsinventar:
Pixabay, Pexels, Magnific, Provider-Tests, Suche, Batch, Promptaufbau, KI-Tasks, Recovery, Webhook, lokale Medien, Featured-/Content-Bilder, Undo/History, Variationslogik, Lizenz-/Credit-Logik, Qualitätsaudit, Warteschlangen-/Dashboard-Funktionen, Zugriffsprüfungen.

## Quelle BILD-DATEN-003

Datei:
`pferde-atelier-bildzentrale-vor-migration-2026-08-05-074723.json`

SHA-256:
`b21061c016ec6c8e6d964f8484d8dfeb1dfd9e647247735d27c631a1d289a8f8`

Format:
`pabz-pre-migration-export-v1`

Export:
2026-08-05T07:47:23Z

Quelle:
Pferde Atelier Bildzentrale 2.4.9

Zuordnung:
HISTORISCHER VOR-MIGRATIONS-DATENSTAND.

Enthält und wird verwertet als:

- Provider-Verbindungsparameter: vorhanden; Werte NICHT öffentlich speichern.
- Magnific-Styleguide: historischer Prompt-/Designbeleg.
- Ausschlussbegriffe: historischer Regelbeleg.
- Prompt-Regelversion: 2.3.0.
- Magnific Task-Map: 44 Zuordnungen.
- Magnific Registry v2: 31 Beiträge / 31 Registry-Tasks.
- Status davon: 30 COMPLETED, 1 IN_PROGRESS zum Exportzeitpunkt.
- Variationsplan: bei allen 31 Registry-Tasks vorhanden.
- Variationshistorie v1: 37 Einträge.
- Zielbeitrag: historisch gespeichert.
- ausgewähltes Magnific-Bild: historisch gespeichert.
- AI-generated-/Mediathek-Zuordnungsdaten: historischer Produktionsbeleg.
- Hinweis im Export selbst: Datei enthält Zugangsdaten und ist nicht für öffentliche Ablage bestimmt.

Der eine historisch nicht abgeschlossene Registry-Eintrag:
- Post 10383
- damaliger Status `IN_PROGRESS`
- späterer Endstatus aus diesen Akten nicht belegt.

## Quelle BILD-KONFIG-004

Datei:
`bildzentrale-einstellungen-2026-08-06-061903.json`

SHA-256:
`cf170b45bc587a52a77a1b0cef464f74158811caefe3995e59af4556694300ae`

Format:
`pabz-settings-export-v1`

Export:
2026-08-06T06:19:03Z

Plugin-Version im Export:
2.6.6

Zuordnung:
SPÄTERER KONFIGURATIONSBELEG.

Enthält und wird verwertet als:

- Provider-Verbindungen: vorhanden; Werte NICHT öffentlich speichern.
- Legacy-Artikelregeln.
- Prompt-Regelversion 2.3.0.
- Profil `article`.
- Profil `category`.
- Profil `hivepress`.
- Farbregeln.
- Subject-Regeln.
- Negative Prompts.
- Ausgabeformate.
- Qualitäts-/Zielgrößen.
- WordPress-Taxonomie-/Meta-Zuordnung.
- HivePress-Taxonomie-/Meta-Zuordnung.

Offener Widerspruch:
Profil `category` beschreibt im Prompt 16:9, speichert technisch aber 3:1 / 1200 × 400.
Nicht auflösen, bis Beleg vorliegt.

## Quelle BILD-LIVE-005

Quelle:
Nutzerbestätigung 2026-09-05 direkt aus aktuell eingesetztem WordPress-Plugin.

Version:
**2.6.9**

Beschreibung:
Allgemeingültige Bildzentrale für Beiträge, WordPress-Taxonomien und optionale HivePress-Taxonomien mit Pixabay, Pexels und Magnific, sicheren Profilen, Export/Import und Readback-Fallback.

Zuordnung:
AKTUELLER PRODUKTIVER LIVE-STAND.

Beleggrenze:
Version und Beschreibung sind belastbar.
Die exakten 2.6.9-Pluginbytes wurden noch nicht als Datei übergeben.

## Nichts-verloren-Regel

Wenn weitere Masterdateien eintreffen:
- niemals nur „neueste Datei behalten“;
- jeden enthaltenen Bestandteil erfassen;
- Dubletten über Hash erkennen;
- aktive Wahrheit, Historie, Fehlerbeleg, Testbeleg, Datenbeleg, Architekturbeleg oder UNGEKLÄRT zuweisen;
- nichts löschen, solange die Zuordnung nicht abgeschlossen ist.
