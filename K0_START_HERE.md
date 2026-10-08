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

Bei gültigem aktuellem Upload + `K0:start` ist der bestehende GitHub-Dateistart zwingend auszuführen. Es gibt keinen separaten Workflow-Startknopf und es darf nicht nach `workflow_dispatch` als Voraussetzung gesucht werden.

Der Startweg ist der bereits bestehende:
1. aus dem aktuellen Upload einen **frischen** Run unter `real_runs/k0/<fresh-run>/` anlegen;
2. dort `WORDPRESS_INTAKE.json` für genau den aktuellen Upload schreiben;
3. dort anschließend `AUTHORING_CONTEXT.json` für genau diesen Run schreiben;
4. der Commit von `AUTHORING_CONTEXT.json` startet den bestehenden Workflow `.github/workflows/k0-authoring-context.yml` automatisch;
5. danach den bestehenden K0-Weg unverändert weiterführen.

Für den Chat gilt zwingend:
- vorhandene GitHub-Dateischreibfunktionen (`create_file` / bei bestehender Datei nur `update_file`) sind der technische Startmechanismus;
- fehlender `workflow_dispatch`-/Run-Button ist **kein Blocker**;
- vor dem ersten GitHub-Schreibversuch für den aktuellen Upload darf **kein** technischer Startblocker gemeldet werden;
- ein terminaler Startblocker ist nur zulässig, wenn der GitHub-Schreibversuch für genau diesen aktuellen Run tatsächlich mit einem konkreten Fehler scheitert;
- bei erfolgreichem Schreibversuch wird ohne sichtbare Zwischenmeldung weiterproduziert.

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
