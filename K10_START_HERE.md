# K10 – Pferdeatelier

Eigenständiger Produktionsbereich für Konzept 10.

## Harte Trennung
- K9 bleibt auf `konzept9/greenfield-20260929`.
- K10 arbeitet ausschließlich auf `konzept10-rule-ledger-20261001`.
- `publish_allowed=false`.

## Normalbetrieb
Bei beigefügter `PSERC_TEXTMACHINE_METADATA_BATCH_V2`-Datei gilt ohne weitere Diskussion:

**Artikel produzieren.**

Alle notwendigen internen Schritte laufen automatisch im Hintergrund des Arbeitsablaufs. Sie werden dem Nutzer nicht angekündigt, erklärt oder als Plan ausgegeben.

### HARTE BEDIENREGEL
Im Normalbetrieb sind vor Abschluss verboten:
- Vorreden;
- „Ich prüfe zuerst …“;
- „Ich recherchiere jetzt …“;
- Ablauf-/Planerklärungen;
- Statusmeldungen;
- Rückfragen, sofern der Auftrag aus der Datei eindeutig ist.

Die **erste sichtbare Antwort an den Nutzer** ist der fertige Artikel bzw. die fertige WordPress-Datei – oder ein unvermeidbarer terminaler Blocker.

Intern bleibt die Produktionsfolge unverändert:
`Recherche -> Schreiben -> generischer K10-Produktionsworkflow -> LanguageTool/Regeln/PSERC/ENDSTEMPEL -> verifizierte WordPress-Importdatei -> STOP`.

K10-Engine, Regeln und Architektur werden im normalen Artikelauftrag nicht verändert.

## Aktuelle Autorität
`CURRENT_STATE.json`

## Produktionsanweisung
`K10_PRODUCTION_ENTRY.md`


## AUFTRAGSAUTORITÄT – HART
Bei jedem neuen Artikelauftrag bestimmt **ausschließlich die aktuell angehängte 5-Feld-Datei** den Artikel.

- `CURRENT_STATE.json` bestimmt nur den Zustand der K10-Maschine.
- Current darf **niemals** Titel, Thema, Kategorie oder Plan-Slot für den neuen Artikel auswählen.
- Historie, letzter Lauf und frühere Anhänge dürfen **niemals** als neuer Auftrag verwendet werden.
- Nach gültigem Attachment: dessen fünf Felder übernehmen und sofort still produzieren.
- Ohne gültiges Attachment: `INPUT_REQUIRED`; niemals den letzten Artikel wiederverwenden.

Insbesondere ist es verboten, nach `K10:pferdeatelier` den Current-Stand zusammenzufassen oder den zuletzt fertigen Artikel als aktuellen Auftrag zu behandeln.


## AUTOMATISCHE BATCH-AUTORITÄT
Die aktuell hochgeladene WordPress-Datei ist vollständig und unmittelbar die Produktionsautorität – auch bei mehreren Artikeln.

- kein manuelles Aktualisieren einer PSERC-Metadatenquelle;
- kein Warten auf einen alten GitHub-Snapshot;
- `item_count >= 1` ist zulässig;
- jeder Artikel wird automatisch exakt an einen Datensatz aus dem aktuellen Upload gebunden;
- der Lauf erzeugt seine PSERC-/Metadatenbindung automatisch aus dem aktuellen Upload;
- ein alter 16er-Bestand darf einen neuen Upload niemals blockieren.

Der Nutzerablauf bleibt: **Datei hochladen -> K10:pferdeatelier -> fertige Artikeldatei.**


## ZERO VISIBLE INTERMEDIATE OUTPUT
Bei gültigem Upload und `K10:pferdeatelier` ist jede nutzersichtbare Zwischenmeldung verboten.

Verboten sind insbesondere:
- K10 erkannt / gestartet;
- Stand, Problem oder nächster Schritt;
- Hinweis, dass ein früherer Blocker weg ist;
- Test-, Current-, Repair- oder Fortschrittsmeldungen;
- Zwischenstände nach einzelnen Artikeln eines Batches.

Current, Historie und Tests dürfen nur intern gelesen werden.

Erste sichtbare Antwort:
- fertige verifizierte WordPress-Datei / fertige Artikel; oder
- echter terminaler, nicht automatisch schließbarer Blocker.

Bei Mehrartikel-Dateien muss zuerst der gesamte Batch vollständig abgearbeitet werden.


## K10-SCOPE – NICHT AUF K0 ÜBERTRAGEN
Die aktuelle Frontend-/WordPress-Kompatibilitätsbindung ist **ausschließlich K10/Pferdeatelier**.

Dazu gehören insbesondere:
- `ppm-generated`;
- `ppm-type-*`;
- `data-article-type`;
- PPM-6.7.9-Registry-Auflösung `plan_slot -> canonical_article_id`;
- `SYSTEM4_WORDPRESS_HANDOFF_V1`;
- K10-Mehrartikel-WordPress-Exporter.

Diese Elemente sind Pferdeatelier-/System4-Kompatibilitätslogik und **keine allgemeine Textmaschinenlogik**.

**HARD RULE:** Nichts davon nach K0 kopieren, importieren, referenzieren oder dort als Vorgabe übernehmen.
K0 bleibt technisch und vertraglich eigenständig.


## TABELLENAUSWAHL – NEUTRAL, KEINE TABELLENQUOTE
Bei optionalen Artikeltypen darf `OMIT_NO_ADDED_VALUE` **nicht** allein damit begründet werden, dass die Fakten bereits im Fließtext stehen.

Eine Tabelle kann Mehrwert schaffen, obwohl sie keine neuen Fakten enthält, wenn sie vorhandene Fakten sinnvoll **in Beziehung setzt**, zum Beispiel:
- Kriterien direkt gegenüberstellt;
- Entscheidungssituationen verdichtet;
- „passend / kritisch“ oder „Prüfpunkt / Konsequenz“ schnell erfassbar macht;
- mehrere unabhängige Prüfpunkte in einer echten Matrix zusammenführt.

Vor `OMIT_NO_ADDED_VALUE` gedanklich einen kompakten Kandidaten mit mindestens 4 sinnvollen Zeilen und 3 sinnvollen Spalten prüfen.

Tabelle **weglassen**, wenn:
- der Inhalt überwiegend linear oder schrittweise ist;
- eine vorhandene Liste/Checkliste denselben Scan-Nutzen bereits gleich gut liefert;
- eine 4×3-Tabelle nur mit Fülltext zustande käme;
- wichtige fachliche Nuancen durch die Tabellenform verloren gingen.

Tabelle **einbauen**, wenn die Matrix einen echten Beziehungs-/Vergleichs-/Entscheidungsnutzen bringt.

Keine Quote. Weder „möglichst viele“ noch „möglichst wenige“ Tabellen.


## TABELLEN-GRUNDSATZ – STANDARD IST TABELLE
Für `Beratung`, `FAQ` und `Pflege` gilt künftig: **Eine Tabelle gehört grundsätzlich in den Artikel.**

Weglassen ist nur mit genau einer definierten Ausnahme erlaubt:
- `LINEAR_SEQUENCE`
- `EXISTING_CHECKLIST_EQUIVALENT`
- `INSUFFICIENT_RELATIONAL_DIMENSIONS`
- `NUANCE_LOSS`

„Steht schon im Fließtext“, „nicht nötig“ oder „Text ist auch so klar“ sind **keine** ausreichenden Ausnahmen.

`Vergleich` bleibt ohne Ausnahme tabellenpflichtig.

Keine Tabellenquote. Die Regel ist: Tabelle als Normalfall, Ausnahme nur fachlich begründet.
