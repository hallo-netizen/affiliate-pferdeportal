# K0 START

## Befehl

`K0:start`

## Eingangsautorität — HARDLOCK

Vor dem ersten frischen K0-Schreibversuch dürfen **nur** diese Quellen Auftragsidentität oder Startstatus bestimmen:

- der aktuell angehängte gültige Upload;
- `K0_START_HERE.md`;
- `K0_CURRENT_STATE.json`;
- `K0_GOAL_CONTRACT.json`.

`control/startmaster0107/**`, `runtime_inbox/**`, Protocol/History, frühere `real_runs/**` und frühere Produktionspakete sind **keine K0-Auftrags- oder Batch-Autorität** und dürfen für den neuen Upload nicht gelesen, ausgewählt oder als Blocker verwendet werden.

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

## Produktionsweg

`Upload -> K0:start -> Recherche -> Writer -> vollständige Regeln -> LanguageTool 6.8 -> finale Regeln -> SYSTEM4_WORDPRESS_HANDOFF_V1 -> Verifikation -> Datei`

Portalzuordnung automatisch.

## Auftragsautorität — HARDLOCK

Diese Regel gilt **allgemein für jeden gültigen K0-Upload**, unabhängig von Thema, Artikeltyp oder Kategorie:

- der aktuell angehängte gültige Upload ist die einzige Auftragsidentität für den neu gestarteten Lauf;
- bei **N >= 1** Upload-Einträgen wird der bestehende K0-Einzelartikelweg **genau N-mal** ausgeführt; der Writer selbst bleibt unverändert Einzelartikel-basiert;
- jeder Upload-Eintrag wird in ursprünglicher Reihenfolge in genau einen frischen Ordner `real_runs/k0/<fresh-run>/` übernommen;
- jeder Einzelrun erhält eine eigene `WORDPRESS_INTAKE.json` mit `item_count = 1`, exakt dem unveränderten Fünf-Felder-Eintrag des Uploads und neu berechnetem `batch_sha256`; Titel, Keyword, Kategorie, Artikeltyp und `plan_slot` dürfen dabei nicht verändert werden;
- technischer Startmechanismus ist der **bestehende GitHub-Dateistart**: diese Einzelrun-`WORDPRESS_INTAKE.json` mit `create_file` schreiben;
- existiert für genau dieses aktuelle Upload-Item bereits ein hashgültiger, identischer Einzelrun-Intake, wird er **nicht überschrieben**; der Lauf wird unmittelbar beim ersten fehlenden Artefakt fortgesetzt;
- nach vorhandenem oder erfolgreich geschriebenem Einzelrun-Intake ist der **unmittelbar nächste Schritt**: Recherche für genau dieses Item und danach `AUTHORING_CONTEXT.json` im selben Run schreiben;
- zwischen `WORDPRESS_INTAKE.json` und `AUTHORING_CONTEXT.json` werden **keine** alten Aufträge, Testanbindungen, Produktionsfreigaben, `control/startmaster0107/**`, `runtime_inbox/**`, frühere Runs oder Produktionspakete geprüft;
- der Commit jedes `AUTHORING_CONTEXT.json` startet unverändert `.github/workflows/k0-authoring-context.yml`; dieser Workflow erzeugt `WRITER_JOB.json` für genau einen Artikel;
- ein erfolgreich geschriebenes `WORDPRESS_INTAKE.json` ist **kein Abschluss und kein Blocker**; fehlender `workflow_dispatch`-/Run-Button ist **kein Blocker**;
- erst ein tatsächlich fehlgeschlagener Recherche- oder GitHub-Schreibversuch im aktuellen frischen Run darf als technischer Startblocker gelten;
- die GitHub-Produktionsanbindung darf **niemals aus Vermutung als nicht verfügbar erklärt werden**; Verfügbarkeit wird ausschließlich durch einen tatsächlichen Aufruf der vorhandenen GitHub-Dateischreibfunktion festgestellt;
- sind GitHub-Aktionen im Chat nicht direkt als eigene Werkzeuge sichtbar, ist das **kein Nichtverfügbarkeitsnachweis**: über den vorhandenen Tool-Router/Code-Mode zuerst die GitHub-Aktionen entdecken und `mcp__GitHub__create_file` bzw. `mcp__GitHub__update_file` verwenden;
- erst wenn diese Werkzeug-Suche **keine** GitHub-Dateischreibaktion liefert oder deren tatsächlicher Aufruf fehlschlägt, darf `GITHUB_WRITE_UNAVAILABLE` als technischer Blocker gelten;
- solange die GitHub-Dateischreibfunktion verfügbar ist, ist der Produktionsstart **ausführbar** und muss ausgeführt werden; ein Chat darf nicht mit `0 von N produziert` abbrechen, ohne mindestens den konkreten Schreibversuch des aktuellen Uploads ausgeführt zu haben;
- der gültige aktuelle Upload startet und bestimmt ausschließlich seine frischen Einzelruns;
- Ablauf je Artikel: `WORDPRESS_INTAKE.json` -> Recherche -> `AUTHORING_CONTEXT.json` -> vorhandener GitHub-Workflow -> `WRITER_JOB.json` -> bestehende Qualitätsstrecke;
- erst wenn alle N Einzelruns verifiziert sind, werden die N WordPress-Singles mit dem bestehenden `engine/wordpress_batch_export.py` in **ursprünglicher Upload-Reihenfolge** zu genau einer WordPress-Batchdatei zusammengeführt;
- ein Mehrfach-Upload darf **nicht** als Mehrfach-Writer-Run an `k0_writer_station` oder `k0-authoring-context.yml` übergeben werden;
- vor dieser Bindung dürfen frühere Runs oder Produktionsstände nicht als Startzustand gelesen oder bewertet werden;
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
