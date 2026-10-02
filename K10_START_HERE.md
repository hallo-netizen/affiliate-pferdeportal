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
