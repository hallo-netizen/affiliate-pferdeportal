# Kategorieplugin als Recherche- und Prüfhilfe für Robotik
Stand: 08.11.2026 · AUFTRAG: **konkrete Seiten- und Inhaltskategorien ERMITTELN**, noch nicht importieren.

## Technischer Ist-Stand – sauber unterschieden
**Robotik-Plugin 0.1.0:** prüft lokal im WordPress-Backend JSON-Struktur, Knotenrollen, Elternzuordnung, Duplikat-Slugs und Zyklen, speichert Entwürfe. Es recherchiert selbst **keine** Keywords, erkennt noch nicht semantisch, ob die letzte Seite tatsächlich ein spezifisches Produkt ist, und erzeugt **keine** WP-Seiten, Kategorien, Anzeigen oder Artikel.

**Bereits belegte Fähigkeiten der allgemeinen Pluginlinie („Affiliate-Portal Kategorie-Workflow“, aus dem Campus-Audit der V1.8.0):** Keyword Ideas, Keyword Suggestions, Keyword Overview von DataForSEO; projektabhängige Markt-/Spracheinstellung; Search Intent, Keyword-/Themenverantwortung, Lücken- und Überschneidungsprüfung, Affiliate-Eignung, 14-stufiger Forschungs-/Freigabeablauf. Der ursprüngliche Kategorien-Writer schreibt nur Taxonomien, keine WordPress-Seiten; spätere Portalversionen haben andere Importmodule. **Keine ungetestete alte Portalversion als Robotik-Produktionsplugin installieren.** Research-Funktionen müssen mit einem *wirklich neutralen Robotik-Profil* geprüft bzw. adaptiert werden.

## Gewünschte Zusammenarbeit: Mensch entscheidet, Plugin recherchiert und kontrolliert
1. **Marktkarte sammeln:** alle Einsatzgebiete/Produktkandidaten aus Fachquellen, Herstellerkatalogen, Branchenverbänden und tatsächlichen Angeboten; noch keine WordPress-Knoten.
2. **Produktschärfe:** Jeden Kandidaten auf eindeutige Funktion prüfen. Große Produktfamilien („Transportroboter“, „Industrieroboter“) in passende konkrete Typen auftrennen oder als reine Zwischen-Seiten klassifizieren. Marken-/Modellvarianten nicht ohne Grund zu eigenen Produkten machen.
3. **Begriffe ordnen:** Synonyme und Fachkürzel (z. B. AMR, autonomer mobiler Roboter) demselben Produkt-Owner zuordnen; echte verschiedene Funktionen trennen.
4. **Gezielte Keyword-Recherche:** DataForSEO Ideas/Suggestions/Overview **pro Produktkandidat**, deutsche Suchbegriffe und Suchabsicht ermitteln. Bezahlte API-Anfragen erst nach Vorprüfung, Dublettenabgleich und separater Freigabe; keine automatischen Kosten.
5. **Kollisionen suchen:** Prüfen, ob zwei Produkte dieselbe Suchabsicht beanspruchen, ob ein Kandidat eher Zwischenebene/Magazin/Anzeigenmarkt ist und ob er bei einem anderen Einsatzgebiet nur verlinkt werden soll. Übrige Treffer als offene Kandidaten behalten, nicht still verwerfen.
6. **Produktseiten auswählen:** Nur eindeutig abgegrenzte, in der Praxis existierende Robotertypen werden letzte WordPress-Seiten. Vorgeschlagene Haupt-/Zwischenseiten sind strukturelle Sammelpunkte, keine Produkt-Leafs.
7. **Inhaltskategorien individuell ableiten:** Fragen, Einstieg, Kosten/Miete, Auswahl/Vergleich, Einsatz, Einrichtung, Wartung, Fehler, Zubehör und Sicherheit *je Produkt prüfen*. Nur wenn **mindestens 3 verschiedene sinnvolle künftige Beiträge** erkennbar sind, darf ein eigener WP-`category`-Leaf empfohlen werden. Kein Standardpaket automatisch verteilen.
8. **Produkt-, Kategorie- und Artikelgrenzen prüfen:** Jede Inhaltskategorie hat genau eine letzte Produktseite als Parent; jeder spätere Beitrag bearbeitet ausschließlich dieses Produkt und gehört einer passenden Inhaltskategorie. Kein Sammel-Leaf für mehrere Produkte.
9. **Alle drei Säulen abgleichen:** Magazinfragen ohne Konkurrenz zum Produkt-Owner; HivePress-Kategorien nur für reale Leistungen und Angebote. Eigene Taxonomien, keine Spiegelung.
10. **Freigabepaket liefern:** Für jeden vorgeschlagenen WordPress-Knoten Quelle, Produktidentität, Parent, Suchbegriff-/Intent-Evidenz, Abgrenzung, 3+ grobe potenzielle Beitragsabsichten je Inhaltsterm, wirtschaftliche Nutzung, Status und Unklarheiten anzeigen. Erst nach fachlicher Freigabe Soll-Profil befüllen. Import ist eine **spätere** Aufgabe mit Live-Dry-Run.

## Für die nächste technische Anpassung erforderlich
- Neutrales Robotik-Research-Profil (keine fremden Taxonomie- oder Live-IDs, keine Hersteller- oder Portalvorbelegung).
- Product-Leaf-Rollenprüfung: eine `content_category` muss ausschließlich unter einer Seite mit ausdrücklich geprüfter Produktrolle liegen (das 0.1.0-Plugin kann dies noch NICHT).
- Prüfung der Artikeltragfähigkeit: 3 **verschiedene** Such-/Nutzerabsichten statt drei Varianten derselben Frage.
- Research/Redaktion streng vom WordPress-Writer getrennt; keine ungeplante Synchronisierung und keine API-Kosten.
- Listen-/Berichtsausgabe mit Vorschlägen **BEHALTEN / AUFTEILEN / UMBENENNEN / MAGAZIN / ANZEIGENMARKT / NOCH PRÜFEN / AUSSCHLIESSEN**.

## Test an drei Pilotprodukten
- **Servierroboter**: Was genau ist das Produkt? Bedien-/Transport-Funktionen trennen? Fragen nach Kauf, Miete, Betrieb, Wartung sammeln.
- **Autonomer mobiler Transportroboter (AMR)**: Suchausdrücke und Grenzen zu FTS/AGV, Palettenrobotern und Maschinenbestückung prüfen. Keine gemeinsame „Transportroboter“-Letzte-Seite, wenn sehr verschiedene Produkte.
- **Melkroboter**: Suchabsichten zu Anschaffung, laufenden Kosten, Reinigung, Wartung und Einsatz prüfen; nicht mit Fütterungsroboter mischen.

**Diese drei Beispiele sind Testaufgaben, noch keine veröffentlichungsreifen Kategorien.**

## Nachweislage
Die Plugin-Funktionen entstammen dem verifizierten Campus-Audit `HOBBYRAUSCH/SEO_KATEGORIEN/KATEGORIE_WORKFLOW_AUDIT_20260926.md`. Das Robotik-Plugin 0.1.0 wurde zusätzlich direkt auf seine gegenwärtigen Prüfregeln untersucht. Keine echten DataForSEO-Resultate oder WordPress-Live-Tests für Robotik vorhanden.
