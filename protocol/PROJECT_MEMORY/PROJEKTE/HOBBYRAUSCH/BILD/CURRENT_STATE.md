# HOBBYRAUSCH – BILD / BILDZENTRALE – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-20
STATUS: **ORIGINAL PFERDEATELIER 2.7.6 BYTEGENAU VERIFIZIERT / HOBBY DEPOT 2.7.7 DARAUS ABGELEITET / LOCAL PASS / LIVE OFFEN**

## Korrektur

Der frühere Hobby-Depot-Kandidat `HOBBY_DEPOT_BILDZENTRALE_1.0.0_INSTALLIEREN.zip` war **keine belastbare Ableitung des echten Pferdeatelier-Plugins** und ist als Arbeits-/Installationsbasis verworfen.

Die Library-Kopien dieses falschen 1.0.0-Kandidaten wurden aus dem Hobby-Depot-Bildbüro und dem zentralen Plugin-Büro entfernt.

## Verifizierte Originalquelle

Quelle:
`pferde-atelier.de_wpvivid-6e9ec6d805997_2026-09-24-11-08_backup_plugin.part001.zip`

Darin:
`plugins/pferde-atelier-bildzentrale/pferde-atelier-bildzentrale.php`

Bytebeweis der Originaldatei:
- Plugin: **Allgemeine Bildzentrale**
- Version: **2.7.6**
- Größe: **383603 Bytes**
- SHA-256: `984a8d4da6594ffa93e6d4024b57cc6c22c7d1fbfec398177a19b0490c20d89b`

Dieser SHA-256 stimmt exakt mit dem bereits dokumentierten Source-Scan des installierten Pferdeatelier-Plugins überein.

Unveränderte Beweiskopie im Hobby-Depot-Bildbüro:
`/Hobby Depot/Bildzentrale/ORIGINAL_PFERDEATELIER_BILDZENTRALE_2.7.6_WPVIVID_SOURCE_VERIFIZIERT.zip`

## Aktueller Hobby-Depot-Kandidat

Plugin:
**Hobby Depot Bildzentrale 2.7.7**

Artefakt:
`HOBBY_DEPOT_BILDZENTRALE_2.7.7_AUS_ORIGINAL_2.7.6_BEREINIGT_INSTALLIEREN.zip`

ZIP SHA-256:
`c27eff9a48007a5317832cf3d6f539d49856a1e6edaf92eebd1bfdb89e030ab7`

Hauptdatei:
- Größe: **317483 Bytes**
- SHA-256: `5126d57a1a04d75e561bf7eab35227e176a04352eb70f587a4f392e463331b38`

Ablagen:
- `/Hobby Depot/Bildzentrale/HOBBY_DEPOT_BILDZENTRALE_2.7.7_AUS_ORIGINAL_2.7.6_BEREINIGT_INSTALLIEREN.zip`
- `/Hobby Depot/Plugin-Büro/HOBBY_DEPOT_BILDZENTRALE_2.7.7_AUS_ORIGINAL_2.7.6_BEREINIGT_INSTALLIEREN.zip`

Nachweis:
`/Hobby Depot/Bildzentrale/HOBBY_DEPOT_BILDZENTRALE_2.7.7_NACHWEIS.md`

## Exakter Delta-Grundsatz

Kein Neubau.

Ausgangspunkt ist ausschließlich die verifizierte Originaldatei 2.7.6.

Nach Namespace-Normalisierung:
- Originalfunktionen: 172;
- Ziel: 159;
- entfernt: 13;
- geändert: 25;
- **134 Originalfunktionen unverändert**.

Die kritischen allgemeinen Kernwege sind unverändert:
- Pixabay;
- Pexels;
- Magnific Request/Check/Recover/Import/Apply;
- WordPress-Taxonomiepfad;
- CPT-Hero-Pfad;
- HivePress-Pfad;
- Mediathekimport;
- Featured Image;
- Content Image;
- Readback;
- Undo/Rollback;
- Normalisierung;
- Import/Export;
- Provider-Normalisierung.

## Entfernt / angepasst

Vollständig entfernt:
- kompletter `pa_breed`-/Rassen-Batchweg;
- 12 Rassen-Batch-Funktionen;
- 4 Rassen-AJAX-Bindungen;
- Rassen-Batch-UI/JavaScript;
- alter Pferde-/Rassen-Hero-Prompt;
- Pferde-Motivcluster;
- Pferde-spezifische Suchregeln;
- Pferde-spezifische Alttext-/Dateinamen-Fallbacks;
- feste Testbeitrags-ID 9120;
- Pferdeatelier-Admin-/REST-Slug.

Neu gebunden:
- sichtbarer Name/Slug Hobby Depot;
- interner HDBZ-Namespace;
- neutraler Hobby-Depot-Prompt;
- Hobbywelten Gestalten, Fertigen, Technik, Forschen, Pflanzen, Tiere, Bewegen, Sammeln;
- WordPress-Kategorien `thumbnail_id`;
- HivePress `hp_listing_category` + `thumbnail_id`.

## Kompatibilitätsgrenze

Genau ein alter technischer Optionsname bleibt bewusst:
`pabz_taxonomy_image_config_v1`

Grund:
Das aktuelle Hobby-Depot-Design liest genau diesen Schlüssel read-only. Er enthält keine Pferde-Fachdaten, IDs, URLs oder Prompts. Eine Umbenennung ohne gleichzeitigen Designplugin-Umbau würde die Bildanzeige brechen.

## Bildertrommel

Im bytegenau verifizierten Original 2.7.6 existiert **kein eindeutiger Code-/UI-Bezeichner „Bildertrommel“ oder „Bildtrommel“**.

Deshalb wird hier nicht geraten, welcher allgemeine Bildweg damit gemeint sein könnte. Es wurde kein Pixabay-/Pexels-/Magnific-/Queue-/Variationsweg fälschlich nur aufgrund einer Vermutung gelöscht.

Der eindeutig belegte Pferde-Sonderautomatismus `pa_breed` ist vollständig entfernt.

## Lokale QA

- PHP-Lint: PASS;
- ZIP-Integrität: PASS;
- WordPress-Pluginpaket: exakt ein oberster Pluginordner + gültige Hauptdatei: PASS;
- interne Callback-Prüfung: 0 fehlende Callbacks;
- interne self-call-Prüfung: 0 fehlende Methoden;
- Pferdeatelier/Pferd/Horse/`pa_breed`/Rasse/Breed/Equestrian im Zielcode: 0;
- feste ID 9120: 0;
- alter Pferdeatelier-Admin-/REST-Slug: 0;
- allgemeine Kernwege gegen Original: PASS.

## Installation

Noch kein LIVE-PASS.

## ERSTER OFFENER BLOCKER

Echter WordPress-Installations- und Funktionsreadback im Hobby Depot.

## EXAKT EINE NEXT ACTION

**Nur `HOBBY_DEPOT_BILDZENTRALE_2.7.7_AUS_ORIGINAL_2.7.6_BEREINIGT_INSTALLIEREN.zip` installieren und zuerst Backend, Provider-Verbindungen, einen Beitrag und eine leere Kategorie positiv/negativ prüfen. Keine Massenbebilderung starten.**
