# K0 START

## Befehl

`K0:start`

## Sichtbares Chatverhalten — HARDLOCK

Bei gültigem angehängtem K0-Handoff + `K0:start`:

**NICHT ANTWORTEN. SOFORT INTERN PRODUZIEREN.**

Verboten:
- Vorrede;
- Statusmeldung;
- Prüfankündigung;
- Prozessbeschreibung;
- Routing-Erklärung;
- Verweis auf andere Wege oder Konzepte;
- Bitte um `weiter`;
- Zwischenmeldung irgendeiner Art.

Die erste sichtbare Antwort ist ausschließlich:

1. die **fertige verifizierte WordPress-Datei**, oder
2. ein **echter terminaler Blocker**, der intern nicht lösbar ist.

## Technischer Start — HARDLOCK

Der bestehende GitHub-Dateistart ist zwingend auszuführen. Die Anzahl der Artikel im gültigen aktuellen Upload darf den Startweg nicht verändern.

Für einen Upload mit **N >= 1** Artikeln gilt:

1. Den aktuellen Upload als unveränderte Batch-Auftragsidentität binden.
2. Vor dem Writer jeden Batch-Eintrag in **genau einen frischen K0-Einzelrun** unter `real_runs/k0/<fresh-run>/` überführen.
3. Jeder Einzelrun erhält eine eigene `WORDPRESS_INTAKE.json` mit **item_count = 1** und exakt dem einen unveränderten Fünf-Felder-Eintrag aus dem aktuellen Upload.
4. Für genau diesen Einzelrun Recherche und `AUTHORING_CONTEXT.json` erzeugen.
5. Der Commit jeder `AUTHORING_CONTEXT.json` startet den bestehenden Workflow `.github/workflows/k0-authoring-context.yml` automatisch.
6. Jeden Einzelrun unverändert durch Writer, vollständige Regeln, LanguageTool 6.8, finale Regeln und WordPress-Handoff führen.
7. Erst wenn alle N Einzelruns verifiziert sind, ihre N WordPress-Singles mit dem bestehenden `engine/wordpress_batch_export.py` wieder in der **ursprünglichen Upload-Reihenfolge** zu genau einer WordPress-Batchdatei zusammenführen.
8. Die erste sichtbare Ausgabe bleibt die fertige verifizierte WordPress-Batchdatei oder ein echter terminaler Blocker aus einem konkreten aktuellen Einzelrun.

**Verboten:** einen Mehrfach-Upload direkt als einen Mehrfach-Writer-Run an `k0_writer_station` oder `k0-authoring-context.yml` zu übergeben.

Der bestehende Writer-Kern bleibt bewusst Einzelartikel-basiert und wird nicht umgebaut.

Es gibt keinen separaten Workflow-Startknopf als Voraussetzung.
`workflow_dispatch` ist für `K0:start` nicht erforderlich.
Vor dem ersten GitHub-Schreibversuch für den ersten aktuellen Einzelrun ist ein technischer Startblocker unzulässig.
Ein terminaler Startblocker ist nur zulässig, wenn ein konkreter Schreib- oder Produktionsschritt für einen Einzelrun aus genau dem aktuellen Upload tatsächlich scheitert.

## Produktionsweg

`Upload -> K0:start -> Recherche -> Writer -> vollständige Regeln -> LanguageTool 6.8 -> finale Regeln -> SYSTEM4_WORDPRESS_HANDOFF_V1 -> Verifikation -> Datei`

Portalzuordnung automatisch.

## Auftragsautorität — HARDLOCK

Diese Regel gilt **allgemein für jeden gültigen K0-Upload**, unabhängig von Thema, Artikeltyp oder Kategorie:

- der aktuell angehängte gültige Upload ist die einzige Auftragsidentität für den neu gestarteten Lauf;
- `K0_CURRENT_STATE.json`, History, frühere Runs und frühere Outputs dürfen den aktuellen Upload weder auswählen, ersetzen noch blockieren;
- ein terminaler Blocker ist nur gültig, wenn er **nach Bindung des aktuellen Uploads** aus genau diesem aktuellen Lauf/Gate stammt;
- jeder neue Upload wird fachlich neu bewertet und neu recherchiert;
- historische Texte oder Research-Artefakte dürfen nicht als Inhaltsquelle übernommen werden;
- historische Informationen sind **keine Ausschlussliste**: unabhängig neu gefundene gleiche Fakten oder Quellen bleiben zulässig.

Interne Links: exakt 3; `parent_category` und `semantic_related` liegen in zwei verschiedenen Haupttextblöcken, `further_information` ausschließlich im Block `further_information`. Intro, Fazit und Tabelle zählen nicht als Haupttext.

Repository: `hallo-netizen/affiliate-pferdeportal`

Branch: `konzept0-portal-neutral-20261002`

Current: `K0_CURRENT_STATE.json`

`publish_allowed=false`

Keine Alternativroute.
