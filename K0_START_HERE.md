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

## GitHub-Dateistart — HARDLOCK

Der bestehende GitHub-Dateistart wird für **alle Einträge des aktuellen Uploads** vollständig ausgeführt.

Für jeden Eintrag gilt ohne sichtbaren Zwischenstopp:

1. den Eintrag als frischen K0-Produktionsauftrag in `WORDPRESS_INTAKE.json` anlegen;
2. die erforderliche Recherche durchführen und den vollständigen Regel- und Recherchekontext in `AUTHORING_CONTEXT.json` erzeugen;
3. `AUTHORING_CONTEXT.json` schreiben; dieser bestehende Dateischritt stößt den vorhandenen Produktionslauf an;
4. danach den bestehenden Produktionsweg ohne Rückfrage oder Zwischenmeldung bis zum verifizierten WordPress-Ergebnis fortsetzen.

Das Fehlen von `AUTHORING_CONTEXT.json` direkt nach dem Anlegen von `WORDPRESS_INTAKE.json` ist **kein Blocker**. Seine Erstellung ist der unmittelbar nächste verpflichtende Startschritt.

Es gibt keinen separaten Workflow-Startknopf als Voraussetzung.
`workflow_dispatch` ist für `K0:start` nicht erforderlich.
Vor dem ersten tatsächlichen GitHub-Schreibversuch ist ein technischer Startblocker unzulässig.
Ein terminaler Startblocker ist nur zulässig, wenn ein konkreter Schreib- oder Produktionsschritt aus genau dem aktuellen Upload tatsächlich scheitert.

Repository: `hallo-netizen/affiliate-pferdeportal`

Branch: `konzept0-portal-neutral-20261002`

Current: `K0_CURRENT_STATE.json`

`publish_allowed=false`

Keine Alternativroute.
