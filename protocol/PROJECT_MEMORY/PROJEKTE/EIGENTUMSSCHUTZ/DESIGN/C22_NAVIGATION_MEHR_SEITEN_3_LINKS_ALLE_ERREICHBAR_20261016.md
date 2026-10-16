# HAB & BEWAHR – C2.2 Navigationsvertrag für wachsenden Kategoriebaum (Konzept, kein Live-Release)

Stand: 16.10.2026 · Quelle: C2.2-Zielvertrag, Design-Current 0.1.20, Nutzerentscheidung vom 16.10.2026.

## Leitentscheidung
**Fachlich vollständige Themenabdeckung hat Vorrang.** Der Baum darf so viele sachlich sinnvolle konkrete Seiten-3-Themen und dazu passende Artikelkategorien enthalten wie erforderlich. Die Navigation darf den Umfang begrenzen, NICHT der Kategorienplan die Navigation.

## Weg von Startseite bis Beitrag
1. **Startseite / Schutzwelten:** bestehende sechs Welten unverändert, daneben Portalwege Magazin, Dienstleister und Glossar eigenständig.
2. **Welt-Hub (Seite 1):** sämtliche echten Schutzbereiche (Seite 2) in übersichtlichen Listen/Kacheln, nicht auf drei kürzen.
3. **Bereich-Hub (Seite 2):** sämtliche konkreten Produkt-/Sachthemen (Seite 3) des Bereichs erreichen; bei großer Zahl visuell ordnen, bei Bedarf paginieren/filtern, **keine** künstliche Kind-Obergrenze.
4. **Themen-Hub (Seite 3):** nur diesem einen Produkt/Sachthema dienende flache WordPress-Artikelkategorien mit klarer Intention anzeigen, ohne starren Satz aus FAQ/Beratung/Vergleichen. Der spätere redaktionelle Ausbau liegt **unterhalb** dieser Ebene.
5. **Artikelkategorieseite:** sämtliche dazugehörigen Beiträge zugänglich, bei Umfang paginiert; diese Ebene muss konzeptionell drei oder mehr echte spätere Beiträge tragen können. Noch KEINE konkreten Beiträge für Kategorienarbeit erzeugen.
6. **Beitragsseite:** Breadcrumb und fachlich passender Rückweg zu Artikelkategorie → konkreter Themenseite → Bereich → Welt. Synonyme führen zum kanonischen Owner, keine zweite Kategorie wegen Alias.
7. **Verknüpfte Einstiege (z. B. Wohnmobil × Wasser/Diebstahl/Brand):** thematische Querverweise ohne Kopieren der Inhalte oder konkurrierende kanonische URLs.

## Mega-Menü / Flyout – feste Darstellungsregel
- Pro angezeigter Navigationsgruppe maximal **drei** direkte Unterlinks; sie sind echte Links zum richtigen Objekt, niemals lediglich nach gleichem Namen auf eine falsche Elternseite.
- Nur wenn die tatsächlich freigegebene und aktive Gruppe **mehr als drei** Kinder hat, folgt **„Weitere Kategorien“** (besser im Kontext: „Alle Themen anzeigen“), mit Link auf den **passenden Bereich-/Hub-Knoten**, der wiederum **alle** Kinder zugänglich macht.
- Bei 0, 1, 2 oder 3 Kindern erscheint **kein** überflüssiger Mehr-Link.
- Die Auswahl der drei Kurzlinks ist eine reine Navigationspriorisierung; nach Hinzufügen weiterer Themen ändern sich keine kanonischen URLs und keine Kategorienamen.
- Alle echten Kategorien bleiben per HTML-Link, Hubs und Breadcrumbs auffindbar; Inhalte sind höchstens im Flyout **nicht direkt sichtbar**, niemals generell verborgen.
- Die gegenwärtige Design-0.1.20-Anpassung „maximal drei Kurzlinks plus Weitere“ ist **lokal dokumentiert**, aber nicht live verifiziert. Deshalb hier nur fachliche Navigationsentscheidung, **kein** neuer Plugin-PASS.
- Keine zusätzliche Kategorie-/Menü-Masterdatenbank: aktive Knoten und Links nur aus der einen zentralen Kategorie-Revision lesen, mit korrekter Objektzuordnung. Nicht die 93/285-Baseline dauerhaft im Designcode einfrieren.
- Bei großen Listen auf Hubseiten Bild-/Abfrageleistung und mobile Nutzbarkeit prüfen: Paginierung oder gruppierte Listen sind Darstellungsoptionen, **keine Kategorielöschung**.

## Exakte Navigations-Prüffälle für spätere Design-Freigabe
| Anzahl gültiger Kinder | Flyout-Direktlinks | Link „Weitere“ | Bereich-Hub |
|---:|---:|---|---|
| 0 | 0 | NEIN | 0 (ggf. leerer Zustand) |
| 1 | 1 | NEIN | 1 |
| 2 | 2 | NEIN | 2 |
| 3 | 3 | NEIN | 3 |
| 4 | 3 | JA | 4 |
| 11 | 3 | JA | 11 |
| 50 | 3 | JA | 50, ggf. paginiert |
Zusatztests: nie Link auf falschen Parent; direkte Link-IDs und Ziel-URLs gegen tatsächliches Mapping prüfen; nach Revision-Update neue Kinder erreichbar, keine doppelten Links, Cache korrekt erneuert, Mobilmenü und Breadcrumbs vollständig.

## Änderungsgrenze
Weder hier noch im Designbüro WordPress-Kategorien schreiben. Änderungen nur über das bestehende zentrale Kategorie-Workflow-Plugin nach echter Revision, nichtdestruktivem Delta, Positiv-/Negativ-/Rollbacktest und Live-Readback. Bestehende Seite-3-Sammelseiten und vorhandene 285 Artikelkategorien werden NICHT unbesehen umbenannt/umgehängt; für die spätere Umstellung ist ein eigener Einzelobjekt-/Redirect- und Artikelzuordnungsplan erforderlich.
