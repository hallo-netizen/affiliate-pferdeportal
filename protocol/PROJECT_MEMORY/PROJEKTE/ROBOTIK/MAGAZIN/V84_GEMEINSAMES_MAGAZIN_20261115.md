# Robotik – gemeinsames Magazin und Wissensbereiche, Fachabschluss 15.11.2026

**Fachliche Entscheidung (nicht WordPress-Livestellung):** Ein einziges Magazin für Privatkunden, Betriebe und Industrie. Auf der Website sollen **Magazin, Glossar, Roboterregister, Roboterfinder und Anzeigenmarkt als gleichrangige Einstiege** erreichbar sein. Inhaltlich sind Magazin, Glossar, Register und Finder eine gemeinsame redaktionelle Säule; die öffentliche Navigation benötigt keine Untermenü-Trennung nach Privat/Industrie.

## Nur sechs verständliche Magazinrubriken

| Rubrik | Eigenständiger Inhalt | Abgrenzung |
|---|---|---|
| **Entwicklungen** | Neue Geräte, Herstelleränderungen, Marktstart, Produktgenerationen | Keine zweite Produktseite oder ungeprüfte Verkaufszusage |
| **Forschung & Prototypen** | Labore, Forschungsanlagen, Studien, Patente und ungewöhnliche Robotik | Ein Projekt bekommt nicht automatisch eine CORE-Typseite |
| **Robotik im Alltag** | Alltagserfahrungen, gesellschaftliche Auswirkungen und Einsatzbeispiele über mehrere Typen | Einzelne Auswahl-, Wartungs- und Kaufartikel gehören zum jeweiligen CORE-Typ |
| **Sicherheit & Regeln** | Grundfragen zu Einsatz, Datenschutz, Normen und Verantwortung | Kein kopierter Gesetzestext, keine Rechtsberatung |
| **Markt & Hersteller** | Unternehmen, Messeentwicklungen, Markttrends, Robotikdienstleistungen | Einzelnes Hersteller-Modell nur im Modellregister als Stamm |
| **Technik & Wissen** | Verständliche übergreifende Funktionsweisen, echte technische Zusammenhänge | Einfache Definitionen stehen im Glossar, nicht als konkurrierende SEO-Seite |

## Die drei bewusst nicht als neue CORE-Kategorien angelegten Themen

1. **Schminkroboter:** [Aoyama Cosmetic Dresser Robot](https://www.aoyama.ac.jp/center104/2025/event_20250930_01) ist ein **Projekt** und Stoff für Forschung & Prototypen. Trotz gebauter Robotik kein stabiler eigener Typbereich im aktuellen Kategoriebaum; keine Serie behaupten.
2. **Roboterkissen:** [Yukai fufuly](https://globalstore.ux-xu.com/products/fufuly) ist ein **Produkt** und ein interessantes Thema für Robotik im Alltag und das Register. Nicht jedes vibrierende, motorisierte oder pneumatische Kissen wird als eigener Robotertyp geführt.
3. **Baustein-Sortierroboter:** [basically Sorter V2](https://basically.website/sorter-v2) ist ein **Projekt** mit realen Aufbauten, aber laut [eigener Dokumentation](https://docs.basically.website/) noch kein fertiges allgemein bestellbares Kit; Magazin Forschung & Prototypen plus einmal im Roboterregister.

**Diese drei Datensätze bleiben im einzigen Typ-Forschungsmaster erhalten** (`KATEGORIE/RECHERCHE/PRODUKTE_V2_20261108.json`), werden aber nicht durch einen neuen WordPress-Kategorienimport öffentlich gemacht. Ihre früheren V81-CORE-Artikelaufträge sind für die CORE-Texterstellung gesperrt; K0 kann sie später als Magazinartikel behandeln, falls die Redaktionsplanung dies vorsieht.

## Einfacher Seiten- und Themenvertrag

- **CORE** = Ein bestimmter Robotertyp und seine individuelle Vertiefung (z. B. Katzenkloroboter → Betrieb).
- **Magazin** = Übergreifende Entwicklung, gesellschaftliche und technische Einordnung, echte Neuigkeiten.
- **Glossar** = Ein Begriff mit Definition und fachlichen Querverweisen; keine zweite Typseite.
- **Register** = Eine eindeutige Hersteller-/Modellidentität; Kennzeichnung nur **Produkt / Projekt / Idee**.
- **Finder** = Aufgabe und Einsatzort → tatsächlich passende, bereits veröffentlichte CORE-Seiten, keine erfundenen Treffer.
- **Anzeigenmarkt** = echte Angebote und Anbieter im bestehenden HivePress, keine Affiliatebanner-Zweitliste.

Eine redaktionelle Suchfrage bekommt genau **einen** primären Owner. Querverweise sind erlaubt; Verdoppelung von Text oder URL nicht.

## Konkreter schon bearbeiteter Stand

- **Roboterregister:** 19 eindeutige Modelle/Projekte in EINER aktuellen Pilotdatei `ROBOTERREGISTER/MODELLE_PILOT_V2.json` (darunter drei Themen ohne neuen CORE-Owner); alte V1 ist nur archivierter Pilot.
- **Glossar:** Einziger vorhandener A–Z-Pool hat **558 Forschungsbegriffe**; davon **14 gezielt quellenbasiert eingeordnet**: **5 Alias-/CORE-Verweise und 9 eigene Glossar-Kurzdefinitionskandidaten**. 0 WordPress-Glossarseiten importiert. Keine 558 automatisch indexierten Dünnseiten.
- **Roboterfinder:** Ein einziger Filterplan `ROBOTERFINDER/FILTER_ABDECKUNG_V1.json`, jetzt **14 mögliche Aufgabenbereiche** statt 12. **16 neue Typen haben nur teilweise quellenbelegte Merkmale** im bestehenden Forschungs-Master; noch **0 vollständig nach Eignung geprüfte Typen** für Live-Empfehlungen.
- **Anzeigenmarkt:** Ein gemeinsames Verzeichnis mit 7 einfachen Leistungs-/Anbieterkategorien, Details in `../ANZEIGENMARKT/START_HERE.md`, noch kein echter HivePress-Import geprüft.
- **Keine neue WP-Rubrik, Glossarseite, Magazinseite, Modellausgabe oder Finder-App angelegt.** Ein finaler WordPress-Abgleich ist Voraussetzung, bevor existierende Plugins oder HivePress-Verzeichnisse dafür einmalig angeschlossen werden.

## Ab jetzt keine neue Grundlagenrecherche

Marktneuheiten werden künftig **laufend redaktionell als Entwicklungen oder Registerupdates** behandelt. Nur nachweislich dauerhafte, nicht schon abgedeckte Robotertypen rechtfertigen später einen einzigen gebündelten Kategorie-Nachtrag. Keine weitere offene Grundlagenschleife, keine neuen Masterlisten.

**Nächster technische Gesamtblock nach V84-Liveabnahme:** Bestehende WordPress-/HivePress-Seiten und bereits installierte Module read-only prüfen, dann Magazin, Glossar, Register, Finder und Anzeigenmarkt als **eine Planung für vorhandene Plugins** aufbauen. Keine ungetestete zweite Implementierung erfinden.
