# Pferdeatelier eBay – QA19: Ursache der fachlichen Namenserkennung katalogweit behoben (TEST)

**Stand:** 11.11.2026. Ausgangsbasis 6.72.328 QA18, unverändert installierte Liveversion unbekannt. Keine Live-Installation, kein Zurücksetzen, keine neue eBay-Abfrage oder Datenmigration.

## Tatsächliche Ursache im Original

Der vorhandene eine BUSINESS-Klassifikator kannte konkrete Namen und die wenigen zuvor manuell hinterlegten Aliaswörter, erkannte aber nicht verlässlich abweichende **deutsche zusammengesetzte Produktnamen** bei vorhandenem passendem Verwendungszweck. `Rückfahrkamera für Pferdeanhänger` und `Funk Rückfahrkamera Pferdeanhänger 12V` wurden für `Anhängerkameras` selbst bei passender eBay-Kategorie mit `ebay_business_concept_missing` abgewiesen. Das Problem betraf keine spezielle Kamera-Vorschrift, sondern das allgemeine Verhältnis von **verkauftem Gegenstand** und **Anwendungszusammenhang**.

## Änderung – in einer bestehenden Datei, im bestehenden Klassifikator

Nur `affiliate-portal-router/includes/trait-ppar-ebay.php`, **eine einzige Erkennung für sämtliche 283 eBay-Pflicht-Produktfamilien**:

1. `ebay_business_product_alias_in_primary` verwendet zusätzlich **dieselbe allgemeine Wortbildungsregel** für alle vorhandenen Katalogtitel: Wenn ein anders zusammengesetzter Produktname denselben Hauptgegenstand bezeichnet und der eBay-Angebotstitel den nötigen Anwendungskontext **unabhängig belegt**, kann die vorhandene zugeordnete Produktfamilie bestätigt werden. Für redaktionell relationale Katalogtitel (z. B. „Kameras im Stall“) müssen Produkt und Ort/Verwendung im echten Angebot vorhanden sein. **Nie** werden allein aus Suchbegriffen oder Beschreibungen Produkte erfunden.
2. **Verkauftes Objekt vor Referenz:** „Kamera-Abdeckung für Pferdeanhänger“ und „Stallkamera-Abdeckung“ sind keine Kameras. Eine Zubehörart, die erst nach dem Hauptwort genannt wird, darf nicht durch die allgemeine Kompositumregel als Hauptprodukt durchrutschen. Das ist derselbe bestehende Erkennungspfad, kein neuer Controller.
3. **Explizite Ausstattung zwingend:** Eine Katalogfamilie „X mit Y“ erfordert ein belegtes Y aus Angebotstitel/Produktart oder Merkmalen; „X ohne Y“ ist nicht diese Familie. Die spätere bereits vorhandene Auswahlprüfung kann diese Entscheidung nicht wieder übergehen. Geprüft u. a. Pferdeanhänger mit/ohne Sattelkammer sowie Torgriffe mit/ohne Feder.
4. Bestehende **katalogseitige Synonyme** und das bereits vor QA19 enthaltene, geprüfte Erkennen von Dressursattel, Reitsattel, Reitplatzplaner bleiben erhalten. Keine neue Suchmaschine, kein weiterer Suchlauf, keine neuen Datenbanktabellen, keine neuen Abfragen an eBay und keine neue Plugin-Architektur.

**Nicht verändert:** 283 fachliche eBay-Warenziele, 15 redaktionelle Ausschlüsse und alle WP-Seiten, eBay `EBAY_DE`/BUSINESS, Spielzeug-, Fremdwaren-, Inhalts-, Bild-/Link-/Preis- und Aktualitätskontrollen, getrennte Recherche und Verfügbarkeit, Qualitätsentscheidung aus QA18, gespeicherte Produkte/Run-UUIDs, Frontend/SAFE-Ausgabe.

## Direkte reproduzierbare Tests

- **283/283** Katalogfamilien mit eigenem Titel: richtige eindeutige Zuordnung; zusätzlich weitere Negativ- und Kreuztests insgesamt **1.711/1.711 PASS** (falscher Produkttyp, Spielzeug, Poster, alleiniger Beschreibungskontext, abweichende Gruppe). Vorherige zwei Fälle *Englische Trensen → Trensen* und *Batterie-Weidezaungeräte → Weidezaungeräte* sind korrekte Ober-/Untergruppenbeziehungen und werden als solche geprüft, nicht als Fehler kaschiert.
- Konkrete Kamera-Gegenprobe: `Rückfahrkamera für Pferdeanhänger` und `Funk Rückfahrkamera Pferdeanhänger 12V` **PASS**; `Kamera für Pferdeanhänger`, `Stallkamera`, `Weidekamera` **PASS**; `Rückfahrkamera für PKW`, `Kamera-Abdeckung für Pferdeanhänger`, `Kamera-Schutzhülle für Pferdeanhänger`, `Stallkamera-Abdeckung` **nicht freigegeben**. Ausstattungs-Gegenproben mit/ohne Sattelkammer und mit/ohne Feder bestanden.
- **10/10** bereits im Katalog definierte eBay-Suchnamen und Synonyme werden korrekt zugeordnet.
- **35/35** QA18-Regressionsfälle (darunter EBAY_DE/BUSINESS und Verkäuferbewertung) erneut PASS.
- **23/23** PHP-Dateien erfolgreich auf Syntax geprüft.
- **Nur eine Quell-Datei geändert**. Reproduzierbare Unterlagen: `EBAY_QA19_EINHEITLICHE_PRODUKTERKENNUNG_283.patch`, `QA19_CATALOG_AND_SAFETY_TEST.php`, `QA19_RESULTS.json`, `qa19_alias_audit.php`, `qa19_alias_results.json`.

## Ehrliche Grenze / Freigabe

**Es wurde nicht behauptet, dass 283 beliebige eBay-Bezeichnungen verstanden werden.** Die gemeinsame Kompositum-/Kontext-Regel erfasst deutsche Wortbildungen katalogweit; fachlich echte andere Wörter wie „Pylone“ gegenüber „Bodenarbeitskegel“ brauchen weiterhin **nachgewiesene, katalogseitig definierte Synonyme**. Die aufgeführten 1.711 Prüfungen sind ausführbare PHP-Tests mit konstruierten Titeln, **keine 1.711 echten eBay-Angebote**. Originalartikel und Ablehnungsmarker fehlen im bisherigen CSV. Es gab keinen realen WordPress-/eBay-API-/MariaDB-Lauf und keine neue öffentliche Produktkachel. **Kein produktives Update freigegeben.**

**Nächster sachlicher Schritt:** In derselben getrennten WordPress-Testinstallation den vorhandenen gespeicherten Kandidatenbestand einmal mit dieser geänderten **einen** Erkennung erneut bewerten, Ablehnungsgründe und echte Kategorie-Kacheln prüfen; eine erneut fehlende Aliasbezeichnung nur nach dokumentiertem echtem Angebotstitel in das bestehende Katalogfeld aufnehmen. Keine 283er Suche auf Verdacht, keine neue Pipeline.