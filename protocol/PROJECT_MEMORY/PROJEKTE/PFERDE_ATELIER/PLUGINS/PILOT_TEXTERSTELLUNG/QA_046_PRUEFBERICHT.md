# Pferdeatelier – interne Kategoriezuordnung, echte Daten, Einzel-Owner (QA 046)

**Stand:** 14.11.2026. **Ergebnis: KEINE INSTALLATIONSFREIGABE.** Der verlangte Mehrheitsanteil ist mit der getesteten internen Lockerung nicht erreicht. Der Versuch wird nicht als fertiges Plugin ausgegeben.

## 1. Was wurde wirklich geprüft?

- **61 echte unveränderte Themen, Titel und Original-IDs** aus `texterstellung-diagnose-20261114-143548.json` (14.11.2026).
- **1.165 originale, historisch validierte Pferdeatelier-Kategorieeinträge** mit **264 Produktfamilien** aus `PSTE_PORTAL_CATEGORY_MAP_V1`. Diese Quelle stammt aus einer älteren Portalkategorie-Erfassung; es handelt sich **nicht um eine aktuelle direkte WordPress-Datenbankabfrage**. Der separate WordPress-Baseline-Bericht vom 09.11. nennt ebenfalls 1.165 Kategorieblätter.
- Der ursprüngliche PSTE-Kategorie-Worker, seine echten Artikelart-Regeln, der unveränderte Journal-Klassifikator und die Originaldateien der vorherigen 0.4.5-Arbeitskopie.
- Nicht künstlich ergänzt: keine Kategorienamen, Artikelarten, Ziel-IDs, Keyword-Antworten, Artikelplätze oder WordPress-Beiträge. Ein bestehender 10-Fälle-Techniktest benutzt ausdrücklich *nachgebildete* WP-Funktionen und zählt **nicht** als reale Produktion.

## 2. Minimale interne Umsetzung als **nicht installierte QA-Arbeitskopie**

- Nur die bisherige Funktion `PSTE_Admin::existingRoomCategoryProposal()` im Original-Worker angepasst. Als Teil **derselben einen redaktionellen Entscheidung** erkennt er eine vorhandene Produktfamilie nur, wenn ihre sinntragenden Wörter vollständig im ursprünglichen Keyword vorkommen und genau eine Familie passt.
- Erst danach verwendet er die **bestehende** PSTE-Artikelart-Regel, ohne Keyword, Titel oder alte SEO-Freigabe zu ändern. Kein neuer Worker, keine neue Kategorie, keine zusätzliche Tabelle, kein neues K0-Gate.
- Manuelle Sperren, veraltete Quellen und bereits bestätigte Entscheidungen bleiben unangetastet. Der erneute Aufruf entscheidet bestätigte Themen nicht noch einmal.
- Der Patch ist **experimentell**: Er ist an der bisherigen offenen Kategorie-Bearbeitung angesetzt, aber keine produktionsfertige Bestätigung der vollständigen Einmal-Entscheidungskette. Nicht auf WordPress installieren.

## 3. Tatsächliches Ergebnis mit den 61 Originalthemen

| Messwert | Ergebnis |
|---|---:|
| Echte unveränderte Themen | 61 |
| Echte historische Kategorieeinträge | 1.165 |
| Verschiedene Produktfamilien | 264 |
| Nach strenger neuer Regel **eindeutig erkennbare Themenfamilien** | **9** |
| Ohne solche eindeutige Produktfamilie | **52** |
| Von den 9 zusätzlich eindeutiger Artikelart-Kandidat | 8 |
| Von den 9 bereits im ursprünglichen Bericht als `PASS` geführt | **7** |
| Zwei weitere: „günstige Regendecken“ (Artikelart unklar), „Regendecken Sale“ (ursprünglich separat `HELD`) | 2 |
| Nachgewiesene neue K0-bereite Artikel | **0** |
| Echte WordPress-Entwürfe im Test | **0** |

**Wichtig:** Neun passende Produktfamilien sind **keine** neun neuen Produktionsfreigaben. Die echten sieben alten PASS sind darin enthalten. Der Kategorien-Fallback erreicht das Ziel „Mehrzahl statt Minderheit“ nicht.

**Alter Magazin-Worker:** Von 61 ursprünglichen Kurz-Keywords erkennt er **kein** Thema eindeutig als Magazin; von den 61 bereits genehmigten Titeln erkennt er genau **einen** Fall („Kolik“) nach seiner bisherigen Regel. Die getrennte Titelgestaltung darf nicht zu einer zweiten redaktionellen Entscheidung werden.

## 4. Warum bloß „weniger streng“ hier falsch wäre

- **11** echte Keywords rund um Pferdeanhänger. Im geprüften Fach-Kategoriebestand gibt es viele **spezielle** Produktfamilien (z. B. 1,5er, 2er, Alu), aber **keine allgemeine Produktfamilie „Pferdeanhänger“**. Eine lockere Textähnlichkeit ordnet „Pferdeanhänger für vier Pferde“ fälschlich den **2er-Pferdeanhängern** zu.
- **11** Keywords zu Pferdeweiden. Der geprüfte Kategorienbestand enthält z. B. „Nachsaat für Pferdeweiden“, aber **keine allgemeine Produktfamilie „Weidepflege“**. „Gülle für Pferdeweiden“ darf nicht allein wegen des gemeinsamen Wortes „Pferdeweiden“ nach „Nachsaat“ geraten.
- **3** Keywords zu Wassertrögen. Vorhanden ist ein spezieller Kategorieblock **„Wassertröge für Weiden“**, aber nicht allgemein **„Wassertröge“**. „Wassertröge selber bauen“ ist ohne belegten Weide-Kontext nicht automatisch dieselbe Kategorie.
- „Magnetfeld-Gamaschen“ darf nicht wegen des gemeinsamen Wortes „Magnetfeld“ zu „Magnetfelddecken“ werden.

**Folgerung:** Es gibt **zwei** Hindernisse: Der alte Kategorie-Erkenner ist zu streng, **und** die tatsächlich vorhandene Struktur deckt manche eigenständigen Themen nicht eindeutig ab. Eine einfache Schwellwertlockerung würde falsche Artikelzuordnungen produzieren.

## 5. KISS-Lösung, die aus diesem echten Test folgt

**Ein fachlicher Entscheidungspunkt im vorhandenen PSTE-Redaktions-Worker:**

1. Bei der ersten redaktionellen Bearbeitung **Suchabsicht, passende vorhandene Kategorie und Artikelart in einem Vorgang** zuordnen. Die Suchabsicht bestimmt, ob zwei belegte unterschiedliche Themen getrennt bleiben; es wird **kein Titel gesplittet** und keine SEO-Freigabe nachträglich neu bewertet.
2. Vorhandenen Kategoriebaum **mit übergeordnetem Seitenpfad** als Kontext verwenden, damit eindeutige Produktfamilien erkannt werden – aber **niemals** ohne tatsächlich existierenden eindeutigen WordPress-Kategorieeintrag an K0 freigeben.
3. Fehlt ein solcher Eintrag, nur **einmal** den offenen Auftrag mit geplantem Bereich und Begründung in das **bereits vorhandene Redaktionsbüro** stellen. Die **separate bisherige Kategorieabdeckungs-Überwachung** sammelt solche Lücken und schlägt Gruppen vor (z. B. Pferdeanhänger / Weidepflege). Sie führt **keine zweite Themenentscheidung** aus.
4. Erst wenn die passende WordPress-Kategorie *tatsächlich existiert und eindeutig am ursprünglichen Auftrag gebunden ist*, kann K0 starten. Neue WordPress-Kategorien werden hier **nicht** ungefragt angelegt; sie würden die sichtbare Portalstruktur verändern.
5. **Zukünftig** Kategoriebezug schon beim **bestehenden** Kategorie-gesteuerten Recherche-Einstieg behalten (`PSTE_Category_Context`); die SEO-Einmalentscheidung bindet Kategorie und Artikelart **vor** der Titelübergabe. Unpassende neu entdeckte Suchabsichten gehen in den vorhandenen offenen Bestand und verschwinden nicht.

Diese Architektur ist hier **noch kein fertig bewiesener Gesamtlauf**. Ohne einen gültigen nachprüfbaren aktuellen WordPress-Kategoriebestand für die 61 und nötige Ergänzungen ist die verlangte Mehrheit nicht belegbar. Darum **keine weitere Installations-ZIP**, keine angebliche Fertigstellung.

## 6. Reproduzierbare QA-Belege

- `qa_actual_61_categories.php` und `REAL_61_CATEGORY_ONLY_RESULTS.json`: originale 61 Themen gegen originale 1.165 historische Kategorien, ohne künstliche Werte; echte Kennungen und konkrete Resultate.
- `qa_real_61_type_intent.php`: ursprüngliche Artikelart-Ontologie (8/9 vorsichtig zuordnungsfähige Artikelarten).
- `QA_OWNER_REGRESSION.php`: **10/10** technische Schutzprüfungen des Original-Owners mit *synthetischen* WordPress-Antworten (als solche ausgewiesen).
- `verify_real_046.py` → `QA_046_REAL_RESULTS.json`: 26/26 Aussagen über wirkliche Daten + separate technische Schutzprüfungen; Erfolg dieser Aussagen **bedeutet nicht** erfolgreichen Artikelworkflow.
- `QA_046_OWNER_MINIMAL_DIFF.patch`: exakter Quellunterschied, nur ein vorhandener Originalklassencode in isolierter QA verändert.
- `qa_fuzzy_margins.py`: unabhängiger Gegenversuch, wie ein großzügiger Ähnlichkeitsabgleich falsche Kategorien wählt.

**Nichts auf der bestehenden WordPress-Seite, im Frontend, bei K0 oder in GitHub-Produktivzweigen verändert.**
