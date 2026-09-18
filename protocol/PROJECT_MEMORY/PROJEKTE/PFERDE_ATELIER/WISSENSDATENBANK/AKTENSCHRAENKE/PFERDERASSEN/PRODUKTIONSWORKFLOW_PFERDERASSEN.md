# PRODUKTIONSWORKFLOW PFERDERASSEN

STAND: 2026-09-14
STATUS: VERBINDLICH FÜR CHAT-PRODUKTION

## ZWECK
Diese Datei ist der direkte Einstieg für jeden neuen Chat, der Pferderassen-Artikel produziert. Sie beschreibt nur den Produktionsweg. Fachliche Wahrheiten liegen in den Rassendatensätzen, Textregeln im Schreibvertrag.

## AUTORITÄTEN
1. `SCHREIBVERTRAG_PFERDERASSE.md` = verbindliche Textregeln.
2. `DATEN/breed-*.json` = einzige Fachquelle je Rasse.
3. extern übergebene Keywords/Kategorien/Linkpakete = nur gültig, wenn ausdrücklich vorgegeben.
4. Der Schreiber darf formulieren, aber nicht entscheiden.

## PRODUKTIONSZIEL
Artikel werden in diesem Chat erstellt und gesammelt als maschinenlesbarer JSON-Batch ausgegeben.

Keine Veröffentlichung.
Kein WordPress-Zugriff.
Keine WordPress-XML-Ausgabe.

## START EINES NEUEN CHATS
Ein neuer Chat muss vor Produktionsbeginn in dieser Reihenfolge lesen:
1. `START_HERE.md`
2. `SCHREIBVERTRAG_PFERDERASSE.md`
3. `PRODUKTIONSWORKFLOW_PFERDERASSEN.md`
4. für jede Rasse den konkreten Datensatz unter `DATEN/`

Keine Rekonstruktion aus Erinnerung. Kein freies Nachbauen alter Regeln.

## EINGABEN PRO RASSE
Mindestens erforderlich:
- freigegebener Rassendatensatz;
- `rassengruppe_slug` für die echte WordPress-Unterkategorie;
- `KW1` und `KW2`, sofern für diesen Artikel bereits vorgegeben;
- optional ein gebundenes `LINKPAKET`.

Fehlt ein Pflichtinput, der nicht aus dem Datensatz stammt, darf der Schreiber ihn nicht selbst erfinden.

## PRODUKTION PRO RASSE
1. Schreibvertrag lesen.
2. konkreten Rassendatensatz laden.
3. Pflichtinputs prüfen.
4. Artikel exakt nach der 12-teiligen Struktur schreiben.
5. nur belegte Fakten verwenden.
6. H1-Regel einhalten.
7. `Pferd`/`Pferderasse`-Regel einhalten.
8. Keywords exakt gemäß Schreibvertrag verarbeiten.
9. nur gebundene interne Links setzen.
10. Kurztext, Meta Title und Meta Description aus dem bereits belegten Artikelinhalt ableiten; keine neuen Fakten hinzufügen.
11. Artikel gegen Schreibvertrag + Datensatz prüfen.
12. Ausgabe bleibt `ENTWURF`; der Autor vergibt keinen fachlichen PASS.

## JSON-BATCH
Für jede Rasse müssen mindestens folgende Felder enthalten sein:
- `rassename`
- `slug`
- `rassengruppe_slug`
- `titel`
- `artikeltext`
- `kurztext`
- `meta_title`
- `meta_description`

Optional zusätzlich:
- `interne_links`
- `kw1`
- `kw2`
- `source_dataset_id`
- `status`

Empfohlener Status:
`ENTWURF`

## SLUG-REGEL
- `slug` wird nur nach vorgegebener technischer Slug-Regel gebildet;
- keine dekorativen Zusätze;
- keine SEO-Erfindungen im Slug;
- Import-Chat prüft Dubletten und technische Gültigkeit erneut.

## RASSENGRUPPE
`rassengruppe_slug` bestimmt die vorgesehene echte WordPress-Unterkategorie.

Der Schreiber darf die WordPress-Unterkategorie nicht frei auswählen, wenn sie extern gebunden wurde.

Wenn keine Kategoriezuordnung vorliegt und keine verbindliche Zuordnungslogik im Datensatz existiert: BLOCK statt raten.

## INTERNE LINKS
Interne Links sind getrennt von der Kategoriezuordnung.

Der Schreiber darf keine Ziel-URL selbst recherchieren oder erfinden.

Ein `LINKPAKET` darf enthalten:
- Glossarziel
- Ziel-Slug
- Ankertext
- optional Pflicht/Optional
- optional Kategorie-/Bereichsziel

Nur diese Links dürfen gesetzt werden.

Bevorzugte Menge gemäß Schreibvertrag:
- 1–2 Glossarlinks
- höchstens 1 Kategorie-/Bereichslink
- insgesamt maximal 3 interne Links
- weniger ist zulässig

## TESTBATCH
Erster Produktionslauf: exakt 5 Rassen.

Ziel des Testbatch:
- Textqualität prüfen;
- harte Regelbindung prüfen;
- JSON-Struktur prüfen;
- Slugs/Kategorien/Pflichtfelder prüfen;
- Importstrecke anschließend separat prüfen.

Keine Hochskalierung auf den Gesamtbestand, bevor der 5er-Testbatch die externe Prüfung bestanden hat.

## NACHGELAGERTER IMPORT-WORKFLOW
Die fertige JSON-Datei geht in einen separaten Import-/Prüfchat.

Dort:
1. JSON hart validieren.
2. Dubletten prüfen.
3. Slugs prüfen.
4. `rassengruppe_slug` gegen echte WordPress-Unterkategorien prüfen.
5. Pflichtfelder prüfen.
6. einmaliger Pferderassen-Importer legt nur WordPress-Drafts an.
7. gespeicherte WordPress-Felder werden zurückgelesen.
8. Rücklesedaten werden byte-/feldbezogen gegen den JSON-Batch geprüft.
9. Fehler => kein Publish.
10. Publish ist ausdrücklich nicht Aufgabe dieses Produktionschats.

## HARTE GRENZEN
Der Produktionschat darf nicht:
- frei recherchieren;
- neue Pferderassen erfinden oder ergänzen;
- Datensatzlücken auffüllen;
- WordPress aufrufen oder verändern;
- Kategorien frei erfinden;
- Links frei erfinden;
- sich selbst fachlich PASS geben;
- Regeln spontan verbessern, erweitern oder umdeuten.

Wenn eine Regel unklar ist: bestehende Dateien lesen. Wenn danach ein Pflichtinput fehlt: BLOCK statt eigene Entscheidung.

## EINSTIEGSSATZ FÜR NEUEN CHAT
`Campus → Pferde Atelier → Wissensdatenbank → Pferderassen. Lies START_HERE.md, SCHREIBVERTRAG_PFERDERASSE.md und PRODUKTIONSWORKFLOW_PFERDERASSEN.md. Produziere ausschließlich nach diesen Dateien und den vorhandenen Rassendatensätzen.`
