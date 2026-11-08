# Einmaliger echter SEO-Test – Arbeitsauftrag für DEN vorhandenen externen SEO-Owner

**Das ist kein Auftrag, einen weiteren Agenten oder eine weitere Prüfung im Produkt anzulegen.** Nur der eine bereits bestimmte externe SEO-Entscheider bewertet die Suchabsicht, das verfügbare Thema und die Doppelbelegung. PSTE/WordPress/PSERC prüfen danach lediglich die technische Herkunft und den vorhandenen Platz. Kein K0-/Redaktionsplan-Umbau.

## Erforderlicher Originaleingang – nicht durch Vermutungen ersetzen

**Genau eine** aktuelle, unveränderte Exportdatei aus **TEST-WordPress** über die bereits vorhandene MINI-Funktion **„Redaktionsstand für einmalige SEO-Prüfung exportieren“**. Pflichtfelder:

- `contract=PSTE_MINI_RESULTS_FOR_EDITORIAL_V1`, `parkhaus_complete=true`.
- `seo_subjects`: pro freigegebenem MINI-Relevanzthema die tatsächlichen `pool_key`, `raw_query`, `source_sha256` aus WordPress, nicht konstruierte Prüf-IDs.
- `items`: gespeicherte ursprüngliche Titel und JA/VIELLEICHT/NEIN-Entscheidungen, nur erster vorhandener JA-Titel darf später als `approved_title` zurückgegeben werden.
- `parkhaus_snapshot`: `complete=true`, `sha256` und **alle** tatsächlichen Einträge aus `WORDPRESS`, `PSTE_PLAN`, `EDITORIAL_PLAN` (sofern verfügbar), `PSERC_ACTIVE_PLAN`, `PPM679_EXISTING_EDITORIAL_RUNTIME`, `MINI_RESERVED`.
- Der **tatsächlich gespeicherte** PPM679-Redaktionsplan darf nicht versehentlich als leer oder nicht vorhanden angenommen werden. Fehlt er, lautet das Ergebnis **QUELLE FEHLT**, nicht FREI.

**Es gibt noch KEINEN echten WordPress-Parkhausexport in diesem isolierten QA-Zweig.** Keine synthetischen Testlisten als reale Portalbelegung behandeln.

## Einziger fachlicher Auftrag

Beurteile für **jedes** echte `seo_subjects`-Thema die **ursprüngliche Suchfrage**, nicht nur den späteren Titel. Vergleiche die vollständigen vorhandenen Seiten/Artikel/Glossare, alle geplanten/gesperrten Themen und die anderen JA-Keywords **in derselben einen Auswertungsrunde**. Kennzeichne:

- **FREI**: wirklich eigene, beantwortbare Suchabsicht, kein im aktuellen Bestand bereits behandeltes oder geplantes Thema. Sachliche `intent_summary`, eindeutiger stabiler 64-stelliger hexadezimaler `intent_slot`. Gleiche Suchabsicht = gleicher Slot, **auch bei anderen Worten**. `approved_title` muss buchstabengetreu dem ersten schon gespeicherten Titel entsprechen. Nicht aus Titelunterschieden auf freie Suchabsichten schließen.
- **BELEGT**: Suchfrage wird bereits durch konkret vorhandenen Artikel/gespeicherten Plan abgedeckt. `matched_ref` verweist auf eine **wirklich im Snapshot enthaltene ID**, Format `QUELLE:ID` (z. B. `WORDPRESS:123` oder `PPM679_EXISTING_EDITORIAL_RUNTIME:echte-Artikel-ID`). Ein ähnliches Wort allein ist kein Beweis. Kein neues Artikelziel.
- **KLAERUNG**: tatsächlicher inhaltlicher Unterschied, Suchfrage, Quellenlage oder Zuordnung nicht zweifelsfrei geklärt. Nenne konkret die offene Frage als `reason`. Keine automatische Freigabe.

Veraltete/defekte externe Antwort, geänderte reale Bestandsdaten, widersprüchliche doppelte `pool_key`s und besetzte **identische** Artikelplätze werden **nur technisch** geblockt. Das ersetzt die obige inhaltliche SEO-Prüfung nicht: Der PSERC-Artikelplatz und die semantische Suchabsicht sind **nicht automatisch dieselbe Kennung**.

## Ergebnisformat – dasselbe bestehende MINI-Importformular

Nur eine JSON-Antwort für den **bestehenden** `PSTE_MINI_SEO_DECISIONS_V1`-Zweig in `importTitleCorrections()`; kein neues Formular, kein Textartikel, kein WordPress-SEO-Zweitcheck:

```json
{
  "contract": "PSTE_MINI_SEO_DECISIONS_V1",
  "owner": "EXTERNAL_SINGLE_SEO_EDITOR",
  "snapshot_sha256": "<UNVERÄNDERTER SHA256 AUS parkhaus_snapshot.sha256>",
  "items": [
    {
      "pool_key": "<ORIGINAL>",
      "raw_query": "<ORIGINAL>",
      "source_sha256": "<ORIGINAL AUS seo_subjects>",
      "box": "KLAERUNG",
      "intent_summary": "Die konkrete Suchabsicht wurde mit dem aktuellen Portalbestand verglichen.",
      "intent_slot": "",
      "matched_ref": "",
      "approved_title": "",
      "reason": "Konkrete Klärfrage; kein Beispiel ist eine echte Entscheidung."
    }
  ]
}
```

Der dargestellte JSON-Eintrag ist **nur Form**, **kein** echtes Urteil. Bei FREI/BELEGT müssen Felder gemäß obiger Regel angepasst werden. Alle Quellen-IDs und Fingerabdrücke unverändert übernehmen, keine unbekannten zusätzlichen Felder erforderlich.

## Einmalige fachliche Kompetenzprobe

Original-100-Datei `QA_ONLY/MINI_100_ORIGINAL_EXTERNAL_TITLES_20261106.json`; daraus **87 JA**. Prüfbeispiele:

- **7/85** günstige Regendecken: keine zwei neuen Artikel für dieselbe Preisfrage.
- **82/84** Regendecke 0g und ungefüttert: keine bloß umformulierte Dopplung.
- **9/11/86** Test-/Vergleichsregendecken: nicht drei freie identische Vergleiche.
- **76** „pferd decken“: Zucht oder Eindecken. Nicht durch zwei neue Titel zu zwei Artikeln machen.
- **62** „pferd“: zu breit ohne geklärte tatsächliche Suchfrage.
- **87/93** Schleich-Spielzeug vs. echter Transportanhänger; **98/94** Miete vs. Gebrauchtkauf; **96/93** vier statt zwei Pferde: keine automatische Verschmelzung verschiedener Suchantworten.
- **94/99** Gebrauchtanhänger kaufen / Schwachstellen: mögliche Überlappung begründen, nicht nur wegen anderer Titel freigeben.

**Eine fachliche Abnahme dieses Owners einmal vor dem realen Einlauf**, danach keine zweite semantische Dauerprüfung. Wo Ergebnisse ernsthaft unklar sind, dem gleichen Owner zur Korrektur vorlegen; bereits gültige andere Themen bleiben unverändert.

## Testfolge

1. Echten WordPress-Export **lesend** erzeugen; vollständigen Originalstand aufheben.
2. Vor dem Ownerlauf die mitgelieferte Quellen-/Vollständigkeitsprüfung ausführen. Fehlender Bestand = **STOP**, kein SEO-Urteil.
3. **Einmal** genau diesen bestehenden SEO-Owner mit dem vollständigen Export beauftragen; tatsächliche Ergebnisdatei separat sichern.
4. Einmaliger Abnahmetest prüft Owner-Arbeit an konkreten Gegenthemen. Zusätzlich maschinell **nur** Herkunft, Vollständigkeit, Versionsbindung und existierende IDs kontrollieren.
5. Erst danach kontrollierter Rückimport/Weitergabe in bestehendem TEST-WordPress; kein Live, kein neuer K0-Lauf. PSERC-K0-Grenze nur auf fünf Metadatenfelder und vorhandene Sicherheitsregeln prüfen.

## Stopp und KISS

Es wird **keine** zweite SEO-Bewertung in WordPress, PSERC oder K0 installiert; diese Offline-Abnahme prüft nur, ob **der eine** SEO-Worker zuverlässig ist. Kein Produktions-/Merge-/Installationsrecht aus bloßem Test-PASS ableiten. Technische Tests mit echten 100 Rohkeywords, aber fiktiven externen SEO-Urteilen, sind **keine** fachliche Abnahme.

**Checkpoint 2:** Der fachliche Prüfauftrag ist im Plugin-Büro abgelegt; die echte aktuelle WP-Quelldatei und die reale Antwort existieren hier noch nicht.
