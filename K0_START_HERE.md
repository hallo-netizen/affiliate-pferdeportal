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

Der bestehende GitHub-Dateistart ist zwingend auszuführen.

1. Für den aktuellen Upload einen frischen Run unter `real_runs/k0/<fresh-run>/` anlegen.
2. Dort `WORDPRESS_INTAKE.json` für genau den aktuellen Upload schreiben.
3. Dort `AUTHORING_CONTEXT.json` für genau diesen Run schreiben.
4. Der Commit von `AUTHORING_CONTEXT.json` startet `.github/workflows/k0-authoring-context.yml` automatisch.
5. Danach den bestehenden K0-Produktionsweg unverändert weiterführen.

Es gibt keinen separaten Workflow-Startknopf als Voraussetzung.
`workflow_dispatch` ist für `K0:start` nicht erforderlich.
Vor dem ersten GitHub-Schreibversuch für den aktuellen Upload ist ein technischer Startblocker unzulässig.
Ein terminaler Startblocker ist nur zulässig, wenn der Schreibversuch für genau diesen frischen Run tatsächlich mit einem konkreten Fehler scheitert.

## Produktionsweg

`Upload -> K0:start -> Recherche -> Writer -> vollständige Regeln -> LanguageTool 6.8 -> finale Regeln -> SYSTEM4_WORDPRESS_HANDOFF_V1 -> Verifikation -> Datei`

Portalzuordnung automatisch.

Repository: `hallo-netizen/affiliate-pferdeportal`
Branch: `konzept0-portal-neutral-20261002`
Current: `K0_CURRENT_STATE.json`

`publish_allowed=false`

Keine Alternativroute.
