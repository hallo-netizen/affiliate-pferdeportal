# K0 START

## Befehl

`K0:start`

## Eingangsautorität — HARDLOCK

Bei gültigem aktuellem Upload + `K0:start` sind vor Bindung des frischen Laufs ausschließlich zulässig:

- der aktuelle Upload;
- `K0_START_HERE.md`;
- `K0_CURRENT_STATE.json`;
- `K0_GOAL_CONTRACT.json`.

Keine andere Repository-Datei, kein früherer Run, kein früherer Output und keine breite Repository-/Campus-Suche darf vor Bindung des aktuellen Uploads Auftragsidentität, Auswahl, Status oder Blocker liefern.

Nach Bindung des aktuellen Uploads dürfen ausschließlich die für den bestehenden K0-Produktionsweg erforderlichen aktuellen Regel-, Recherche- und Produktionsquellen gelesen werden.

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
2. ein **echter terminaler Blocker aus genau dem aktuellen frischen Lauf**, der intern nicht lösbar ist.

## Auftragsautorität — HARDLOCK

Der aktuell angehängte gültige Upload ist die einzige Auftragsidentität für den neu gestarteten Lauf.

- **Alle Einträge des aktuellen Uploads werden bearbeitet.**
- Kein zusätzliches Mengenfeld darf Einträge auswählen, reduzieren oder begrenzen.
- `K0_CURRENT_STATE.json`, History, frühere Runs und frühere Outputs dürfen den aktuellen Upload weder auswählen, ersetzen noch blockieren.
- Jeder neue Upload wird fachlich neu bewertet und neu recherchiert.
- Historische Texte oder Research-Artefakte dürfen nicht als Inhaltsquelle übernommen werden.
- Historische Informationen sind keine Ausschlussliste: unabhängig neu gefundene gleiche Fakten oder Quellen bleiben zulässig.

## GitHub-Dateistart — HARDLOCK

Für den Chat gilt zwingend:

- vorhandene GitHub-Dateischreibfunktionen (`create_file`; bei bereits bestehender Datei nur `update_file`) sind der technische Startmechanismus;
- nach erfolgreichem Schreiben von `WORDPRESS_INTAKE.json` ist **im selben K0-Auftrag unmittelbar die Recherche auszuführen und anschließend `AUTHORING_CONTEXT.json` mit `create_file` zu schreiben**;
- ein erfolgreiches `WORDPRESS_INTAKE.json` beendet den Start **nicht**;
- fehlender `workflow_dispatch`-/Run-Button ist **kein Blocker**;
- ein terminaler Blocker zwischen Intake und Authoring Context ist nur zulässig, wenn die konkrete Recherche oder der konkrete `create_file`-/`update_file`-Versuch für `AUTHORING_CONTEXT.json` tatsächlich mit einem Fehler scheitert;
- bei erfolgreichem Schreibversuch wird ohne sichtbare Zwischenmeldung weiterproduziert.

Der bestehende GitHub-Dateistart wird für **jeden Eintrag des aktuellen Uploads** vollständig ausgeführt.

Für jeden Eintrag gilt ohne sichtbaren Zwischenstopp:

1. genau diesen unveränderten Fünf-Felder-Eintrag in einem eigenen frischen K0-Einzelrun als `WORDPRESS_INTAKE.json` anlegen;
2. die bestehende Einzelrun-Schnittstelle mit `item_count = 1` beibehalten; dies ist **keine Begrenzung des Gesamtauftrags**;
3. für genau diesen Einzelrun die erforderliche Recherche durchführen und den vollständigen Regel- und Recherchekontext als `AUTHORING_CONTEXT.json` erzeugen;
4. `AUTHORING_CONTEXT.json` schreiben; dieser bestehende Dateischritt startet automatisch den vorhandenen Workflow `.github/workflows/k0-authoring-context.yml`;
5. den Einzelrun unverändert durch Writer, vollständige Regeln, LanguageTool 6.8, finale Regeln und WordPress-Handoff bis zum verifizierten WordPress-Single fortsetzen;
6. danach mit dem nächsten Eintrag des aktuellen Uploads fortfahren, ohne Rückfrage und ohne Zwischenmeldung.

### Intake → Authoring Context — NO-STOP-HARDLOCK

Ein erfolgreich geschriebener `WORDPRESS_INTAKE.json` ist **niemals** ein Abschluss, Statuspunkt, Wartepunkt oder Blocker.

Nach erfolgreichem Intake-Schreibvorgang muss im **selben laufenden K0-Auftrag und ohne Rückgabe an den Nutzer** unmittelbar weitergearbeitet werden:

`WORDPRESS_INTAKE.json -> frische Recherche -> vollständiger Regel- und Recherchekontext -> AUTHORING_CONTEXT.json -> vorhandener Dateistart`

Das Fehlen von `AUTHORING_CONTEXT.json` nach dem Intake ist der **erwartete Zwischenzustand**, kein Problem. Der K0-Start muss den fehlenden Kontext selbst erzeugen.

Verboten sind an dieser Stelle insbesondere:
- „Recherche- und Regelkontext fehlt“ als Abbruchgrund;
- „nächster Schritt: Kontext erstellen“ als sichtbare Antwort;
- Rückfrage oder Warten auf `weiter`;
- Beenden des Chats nach dem Intake-Commit.

Ein terminaler Blocker an dieser Stelle ist erst zulässig, wenn die **konkrete aktuelle Recherche oder das konkrete Schreiben von `AUTHORING_CONTEXT.json` tatsächlich versucht wurde und gescheitert ist**.

**Verboten:** einen Mehrfach-Upload direkt als Mehrfach-Writer-Run an `k0_writer_station` oder `k0-authoring-context.yml` zu übergeben.

Wenn alle Einträge verifiziert sind, werden die vorhandenen WordPress-Singles mit `engine/wordpress_batch_export.py` in der **ursprünglichen Upload-Reihenfolge** zu genau einer WordPress-Batchdatei zusammengeführt.

Es gibt keinen separaten Workflow-Startknopf als Voraussetzung.
`workflow_dispatch` ist für `K0:start` nicht erforderlich.
Vor dem ersten tatsächlichen GitHub-Schreibversuch ist ein technischer Startblocker unzulässig.
Ein terminaler Startblocker ist nur zulässig, wenn ein konkreter Schreib- oder Produktionsschritt aus genau dem aktuellen Upload tatsächlich scheitert.

## Produktionsweg

`Upload -> K0:start -> Recherche -> Writer -> vollständige Regeln -> LanguageTool 6.8 -> finale Regeln -> SYSTEM4_WORDPRESS_HANDOFF_V1 -> Verifikation -> Datei`

Portalzuordnung automatisch.

Repository: `hallo-netizen/affiliate-pferdeportal`

Branch: `konzept0-portal-neutral-20261002`

Current: `K0_CURRENT_STATE.json`

`publish_allowed=false`

Keine Alternativroute.
