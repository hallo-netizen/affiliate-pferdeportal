# Pferdeatelier – konkrete Ursache Kurzweg und warum ein WP-Artikelimport nicht hilft (11.11.2026)

## Nachweis am installierten Plugin-Paket PSTE 0.57.144.40 / PSERC 0.28.67
Screenshot WordPress zeigt **`PSTE_SHORTPATH_NO_ELIGIBLE_SELECTED_TOPICS`**. In `Portal SEO Topic Engine/includes/class-pste-admin.php`, Methode `shortPathCompileExactManualSelection`, tritt genau dieser Fehler auf, wenn nach PSTE-Planbarkeit und `PSERC_SEO_Reader::normalizeCandidate` kein einziger ausgewählter Datensatz `ELIGIBLE` ist. Die Meldung beweist **nicht**, dass die drei historischen Metadatenexport-Zeilen ungültig sind.

### Belegte Ursache der Falschanweisung
`PSTE_Repository::importManualTopics` behandelt eingegebene Titel als **neue Themen-Anfragen**, erzeugt neue `candidate_id` und initialisiert Kategorie, SEO-Metriken, Suchintent und redaktionellen Titel leer. Es speichert einen neuen Lauf und Kandidaten in den **PSTE-eigenen WordPress-Tabellen** und führt anschließend den normalen PSTE-Eignungsweg aus. Die anschließend gezeigte Kurzweg-Sperre ist eine erwartbare Folge fehlender Nachweise, nicht die fehlende Existenz von Artikeln. Die Empfehlung, die drei **alten freigegebenen Exporttitel** in dieses Textfeld zu kopieren und eine fertige K0-Datei zu erwarten, war technisch falsch.

### Warum kein WP-XML mit erfundenen/dummy Artikeln
Der originale signierte Batch `PSERC_TEXTMACHINE_METADATA_BATCH_V2` enthält ausschließlich **fünf Metadatenfelder** je Artikel: `article_type, category, plan_slot, target_keyword, title`. Er enthält **keine Artikeltexte**. Ein `WordPress Importer`-XML würde **Beiträge** anlegen, aber **nicht** die separat gespeicherten PSTE-Planbarkeitsnachweise, PSERC-Freigaben oder K0-Schreibnachweise rekonstruieren. Das erzeugt falschen Fortschritt, möglicherweise unerwünschte Doppelbeiträge, und schreibt in WP-Daten. Keine Dummy-Importdatei als Scheinlösung liefern.

### KISS-Folgeschritt
1. Vorhandenes Original der **drei signierten Fünffelder-Übergaben vom 10.11.2026** verwenden, nicht nochmals in PSTE-Kurzweg eingeben.
2. Übergabe direkt an die vorhandene **K0-Eingangsprüfung**: je Datei exakt 1 Item, ohne Änderung an WP, PSTE, PSERC oder K0. **K0-Artikelproduktion nicht als fertig ausgeben**, denn zusätzlicher K0-Autoren-/Recherche-Kontext und BOUND_TYPE-Freigabe fehlen im Originalexport.
3. Nachhaltiges WP-Automatikproblem **separat** behandeln: vorherige 5.013er-Neubewertung überschrieb Freigaben, und neu installierte `.40` verhindert lediglich neuen ungewollten Komplettlauf, **stellt alte Freigaben nicht wieder her**. Keine Behauptung eines durchgängigen WordPress-PASS ohne echten Test.
4. Keine erneute 5.000er-Prüfung, keine neuen Regelwerke, keine Dummy-Behauptungen, keine manuelle Datenbankänderung.

**Status:** Plugin-Kurzweg-Fehlerzeile und Ursachencode gelesen; Fehlanweisung korrigiert; kein WordPress-Import, kein K0-Lauf, keine Freigaben vorgetäuscht.
