# K0 START

## Befehl

`K0:start`

## Eingangsautorität — HARDLOCK

Für einen frischen K0-Start gilt:

- Der aktuell angehängte gültige Upload ist die einzige Auftragsidentität.
- `K0_START_HERE.md` bestimmt den Startweg.
- `K0_CURRENT_STATE.json` bestimmt nur den aktuellen K0-Status und darf keinen früheren Auftrag auswählen.
- `K0_GOAL_CONTRACT.json` bestimmt den Zielvertrag.
- Frühere Zustände, frühere Läufe, Historie oder frühere Produktionsartefakte dürfen den aktuellen Upload weder auswählen, ersetzen noch blockieren.

## Sichtbares Chatverhalten — HARDLOCK

Bei gültigem Upload + `K0:start`:

**NICHT ANTWORTEN. SOFORT INTERN PRODUZIEREN.**

Keine Vorrede.
Keine Statusmeldung.
Keine Prüfankündigung.
Keine Prozessbeschreibung.
Keine Routing-Erklärung.
Keine Zwischenmeldung.
Keine Bitte um `weiter`.

Die erste sichtbare Antwort ist ausschließlich:

1. die fertige verifizierte WordPress-Datei; oder
2. ein echter terminaler Blocker aus genau dem aktuellen Lauf, der intern nicht lösbar ist.

## Produktionsweg

`aktueller Upload -> K0:start -> Recherche -> Writer -> vollständige Regeln -> LanguageTool 6.8 -> finale Regeln -> SYSTEM4_WORDPRESS_HANDOFF_V1 -> Verifikation -> Datei`

Portalzuordnung automatisch.

## Auftragsautorität — HARDLOCK

- Jeder Eintrag des aktuell angehängten gültigen Uploads wird verarbeitet.
- Es gibt keine fest vorgegebene Batchgröße, Obergrenze oder mengenabhängige Startlogik.
- Die ursprüngliche Upload-Reihenfolge bleibt erhalten.
- Jeder Upload-Eintrag wird über den bestehenden unveränderten K0-Einzelartikelweg verarbeitet.
- Für jeden Upload-Eintrag wird ein eigener frischer K0-Run verwendet.
- Die `WORDPRESS_INTAKE.json` dieses Runs enthält ausschließlich den unveränderten Fünf-Felder-Eintrag des aktuellen Uploads: `article_type`, `category`, `plan_slot`, `target_keyword`, `title`.
- Titel, Keyword, Kategorie, Artikeltyp und `plan_slot` werden nicht verändert.
- Der technische Start bleibt der bestehende GitHub-Dateistart: `WORDPRESS_INTAKE.json` schreiben.
- Nach dem vorhandenen oder erfolgreich geschriebenen Intake folgt im selben Run unmittelbar die Recherche für genau diesen Upload-Eintrag und danach `AUTHORING_CONTEXT.json`.
- Der Commit von `AUTHORING_CONTEXT.json` startet unverändert `.github/workflows/k0-authoring-context.yml`; dieser Workflow erzeugt `WRITER_JOB.json` für genau diesen Einzelartikel.
- Danach läuft unverändert die bestehende Writer- und Qualitätsstrecke.
- Nach Verifikation aller zum aktuellen Upload gehörenden Einzelartikel werden die WordPress-Singles mit `engine/wordpress_batch_export.py` in ursprünglicher Upload-Reihenfolge zu einer WordPress-Datei zusammengeführt.
- Ein vorhandener Run darf nur dann fortgesetzt werden, wenn seine Auftragsidentität hashgültig und exakt identisch zu einem Eintrag des aktuell angehängten Uploads ist. Andernfalls wird er ignoriert.
- Ein erfolgreich geschriebener Intake ist kein Abschluss und kein Blocker.
- Fehlender `workflow_dispatch` oder ein fehlender Run-Button ist kein Blocker.
- Die GitHub-Dateischreibfunktion darf nicht aus Vermutung als nicht verfügbar erklärt werden. Erst ein tatsächlicher Tool-Discovery- und Schreibversuch für den aktuellen Upload darf `GITHUB_WRITE_UNAVAILABLE` begründen.
- Ein terminaler Blocker ist nur gültig, wenn er aus genau dem aktuellen Upload und dem aktuellen Lauf stammt.
- Jeder neue Upload wird fachlich neu recherchiert.
- Historische Texte oder Research-Artefakte werden nicht als Inhaltsquelle übernommen.

Interne Links: exakt 3; `parent_category` und `semantic_related` liegen in zwei verschiedenen Haupttextblöcken, `further_information` ausschließlich im Block `further_information`. Intro, Fazit und Tabelle zählen nicht als Haupttext.

Repository: `hallo-netizen/affiliate-pferdeportal`

Branch: `konzept0-portal-neutral-20261002`

Current: `K0_CURRENT_STATE.json`

`publish_allowed=false`

Keine Alternativroute.
