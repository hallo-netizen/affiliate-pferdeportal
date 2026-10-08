# K0 START

## Befehl

`K0:start`

## Eingangsautorität — HARDLOCK

Bei gültigem aktuellem Upload + `K0:start` sind vor dem frischen Lauf ausschließlich zulässig:

- der aktuelle Upload;
- `K0_START_HERE.md`;
- `K0_CURRENT_STATE.json`;
- `K0_GOAL_CONTRACT.json`.

Keine andere Repository-Datei darf vor dem frischen Lauf Auftragsidentität, Auswahl, Status oder Blocker liefern.

## Sichtbares Chatverhalten — HARDLOCK

**NICHT ANTWORTEN. SOFORT INTERN PRODUZIEREN.**

Die erste sichtbare Antwort ist ausschließlich:

1. die fertige verifizierte WordPress-Datei; oder
2. ein echter terminaler Blocker aus genau dem aktuellen frischen Lauf.

Keine Vorrede.
Keine Statusmeldung.
Keine Prüfankündigung.
Keine Prozessbeschreibung.
Keine Zwischenmeldung.
Keine Bitte um `weiter`.

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

Repository: `hallo-netizen/affiliate-pferdeportal`
Branch: `konzept0-portal-neutral-20261002`
Current: `K0_CURRENT_STATE.json`

`publish_allowed=false`

Keine Alternativroute.
