# HOBBYRAUSCH – BILD / BILDZENTRALE – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-20
STATUS: **ORIGINAL PFERDEATELIER 2.7.6 BYTEGENAU VERIFIZIERT / HOBBY DEPOT 2.7.8 DARAUS ABGELEITET / LOCAL PASS / LIVE OFFEN**

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
**Hobby Depot Bildzentrale 2.7.8**

Artefakt:
`HOBBY_DEPOT_BILDZENTRALE_2.7.8_VERBINDLICHER_BILDPROMPT_INSTALLIEREN.zip`

ZIP SHA-256:
`d9d8caad4c2f4057fee30f9d21607376fa110d82defed8c0f759e5c202b83342`

Hauptdatei:
- Größe: **320401 Bytes**
- SHA-256: `edda98383add25fc2d02bf35bfff433b2c5ded332cc21a0fc43a82577e6004ec`

Ablagen:
- `/Hobby Depot/Bildzentrale/HOBBY_DEPOT_BILDZENTRALE_2.7.8_VERBINDLICHER_BILDPROMPT_INSTALLIEREN.zip`
- `/Hobby Depot/Plugin-Büro/HOBBY_DEPOT_BILDZENTRALE_2.7.8_VERBINDLICHER_BILDPROMPT_INSTALLIEREN.zip`

Nachweis:
`/Hobby Depot/Bildzentrale/HOBBY_DEPOT_BILDZENTRALE_2.7.8_NACHWEIS.md`

## Bildprompt 2.7.8

Der gemeinsam festgelegte Hobby-Depot-Grundprompt ist jetzt zentral verbindlich. Er fordert ein klares, ruhiges, nicht überladenes Hauptmotiv; Tätigkeit vor Objekt, wenn sinnvoll; Menschen/Hände/Arme zur Verdeutlichung der Tätigkeit; keine dekorativen Personen; keine Collagen, Split-Bilder, Schrift, Logos oder Wasserzeichen.

Bei Beiträgen wird das konkrete Bildthema weiterhin automatisch aus dem Inhalt abgeleitet, jetzt ausdrücklich aus **Titel + Kurztext + bis zu 120 Wörtern Beitragsinhalt**. Für WordPress-Kategorien, Post-Type-Heros und HivePress wird dieselbe zentrale Bildregel zusätzlich vor die jeweiligen Profilregeln gesetzt.

Lokaler Positivtest Holzschnitzen: Titel/Kurztext/Inhalt/Hände-Regel/nicht-überladen-Regel PASS; erzeugter Prompt 2874/3000 Zeichen.

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
- allgemeine Kernwege gegen Original: PASS;
- Delta 2.7.7 → 2.7.8: 10 geänderte/neue Funktionen, ausschließlich Prompt-/Themenableitung plus Export-Versionswert;
- WordPress-Paketstruktur 2.7.8: PASS.

## Installation

Noch kein LIVE-PASS.

## ERSTER OFFENER BLOCKER

Echter WordPress-Installations- und Funktionsreadback im Hobby Depot.

## EXAKT EINE NEXT ACTION

**Nur `HOBBY_DEPOT_BILDZENTRALE_2.7.8_VERBINDLICHER_BILDPROMPT_INSTALLIEREN.zip` installieren und zuerst Backend, Provider-Verbindungen, einen Beitrag und eine leere Kategorie positiv/negativ prüfen. Keine Massenbebilderung starten.**
