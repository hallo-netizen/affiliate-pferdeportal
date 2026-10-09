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
- **erste interne Startaktion:** exakt diesen Upload in einem frischen K0-Run als `WORDPRESS_INTAKE.json` binden; erst danach dürfen Recherche, Authoring oder Prüfungen des neuen Laufs beginnen;
- technischer Startmechanismus ist der **bestehende GitHub-Dateistart**: `WORDPRESS_INTAKE.json` mit `create_file` schreiben; nur wenn genau diese Datei bereits existiert, `update_file` verwenden;
- nach erfolgreichem Schreiben von `WORDPRESS_INTAKE.json` **im selben K0-Auftrag sofort Recherche ausführen und anschließend `AUTHORING_CONTEXT.json` mit `create_file` schreiben**;
- ein erfolgreich geschriebenes `WORDPRESS_INTAKE.json` ist **kein Abschluss und kein Blocker**; fehlender `workflow_dispatch`-/Run-Button ist **kein Blocker**;
- erst ein tatsächlich fehlgeschlagener Recherche- oder GitHub-Schreibversuch im aktuellen frischen Run darf als technischer Startblocker gelten;
- die GitHub-Produktionsanbindung darf **niemals aus Vermutung als nicht verfügbar erklärt werden**; Verfügbarkeit wird ausschließlich durch einen tatsächlichen Aufruf der vorhandenen GitHub-Dateischreibfunktion festgestellt;
- sind GitHub-Aktionen im Chat nicht direkt als eigene Werkzeuge sichtbar, ist das **kein Nichtverfügbarkeitsnachweis**: über den vorhandenen Tool-Router/Code-Mode zuerst die GitHub-Aktionen entdecken und `mcp__GitHub__create_file` bzw. `mcp__GitHub__update_file` verwenden;
- erst wenn diese Werkzeug-Suche **keine** GitHub-Dateischreibaktion liefert oder deren tatsächlicher Aufruf fehlschlägt, darf `GITHUB_WRITE_UNAVAILABLE` als technischer Blocker gelten;
- solange die GitHub-Dateischreibfunktion verfügbar ist, ist der Produktionsstart **ausführbar** und muss ausgeführt werden; ein Chat darf nicht mit `0 von N produziert` abbrechen, ohne mindestens den konkreten Schreibversuch des aktuellen Uploads ausgeführt zu haben;
- der aktuelle Upload benötigt **keine zusätzliche Bereitstellung, Freigabe oder Übernahme als „aktueller Batch“** vor diesem Bindungsschritt;
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
