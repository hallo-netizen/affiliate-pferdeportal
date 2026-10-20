# HOBBY DEPOT – BILDZENTRALE – ÜBERNAHMEPRÜFUNG

STAND: 2026-10-20
STATUS: **SOURCE-AUDIT ABGESCHLOSSEN / ORIGINAL 2.7.6 VERIFIZIERT / 2.7.7 BEREINIGT LOCAL PASS**

## Beweis der Quelle

Verwendet wurde nicht ein Nachbau, sondern die reale Plugin-Datei aus dem WPvivid-Pluginbackup vom 24.09.2026.

Quelle:
`pferde-atelier.de_wpvivid-6e9ec6d805997_2026-09-24-11-08_backup_plugin.part001.zip`

Datei darin:
`plugins/pferde-atelier-bildzentrale/pferde-atelier-bildzentrale.php`

Original:
- Version 2.7.6;
- 383603 Bytes;
- SHA-256 `984a8d4da6594ffa93e6d4024b57cc6c22c7d1fbfec398177a19b0490c20d89b`.

Der Hash stimmt exakt mit dem früher dokumentierten Source-Scan überein.

## Was das Original tatsächlich enthält

Allgemeiner Kern:
- Beiträge;
- WordPress-Taxonomien;
- Custom-Post-Type-Heros;
- optionale HivePress-Taxonomien;
- Pixabay;
- Pexels;
- Magnific;
- Suche/Batch;
- Mediathek;
- Featured-/Content-Bilder;
- Import/Export;
- Readback;
- Undo/History;
- Qualitätsprüfung;
- Lizenz-/Credit-Wege.

Pferde-spezifisch:
- `pa_breed`;
- serieller Rassen-Batch;
- Rassen-Hero-Regeln;
- Pferde-Prompts und Pferde-Motivcluster;
- Pferde-spezifische Such-/Alttext-/Dateinamen-Regeln;
- feste Testbeitrags-ID 9120;
- Pferdeatelier-Admin-/REST-Slugs.

## Bereinigung 2.7.7

Vollständig entfernt:
- `pa_breed`;
- zwölf Breed-/Rassen-Batch-Funktionen;
- vier zugehörige AJAX-Bindungen;
- Rassenbatch-UI und JavaScript;
- Pferde-/Rassen-Prompt;
- Pferde-Motivcluster;
- Pferde-Such-/Alttext-/Fallbacklogik;
- feste 9120-Bindung;
- Pferdeatelier-Slugs.

Projektneutral/Hobby Depot angepasst:
- HDBZ-Namespace;
- Hobby-Depot-Bezeichnung;
- neutraler Hobby-Prompt;
- acht Hobbywelten als manuelle Motivcluster;
- WordPress/HivePress-Startbindung.

## Kernnachweis

Nach reiner Namespace-Normalisierung:
- 134 Funktionen aus 2.7.6 sind bytegleich/unverändert;
- alle geprüften kritischen allgemeinen Provider-, Import-, Readback-, Undo-, Taxonomie-, CPT- und HivePress-Funktionen sind unverändert.

## Bildertrommel-Prüfung

Im Originalcode 2.7.6 gibt es keinen eindeutig benannten Code-/UI-Weg `Bildertrommel` oder `Bildtrommel`.

Deshalb wurde kein allgemeiner Bildweg auf Verdacht gelöscht.

Diese Grenze ist bewusst dokumentiert: **nicht raten**.

## Ergebnis

Installationskandidat:
`HOBBY_DEPOT_BILDZENTRALE_2.7.7_AUS_ORIGINAL_2.7.6_BEREINIGT_INSTALLIEREN.zip`

ZIP SHA-256:
`c27eff9a48007a5317832cf3d6f539d49856a1e6edaf92eebd1bfdb89e030ab7`

Kein Live-PASS vor echter WordPress-Prüfung.
