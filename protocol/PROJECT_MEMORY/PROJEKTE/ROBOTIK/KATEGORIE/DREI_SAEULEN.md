# DREI SÄULEN – ROBOTIK / STRUKTURVORLAGE

## 1. CORE – Hauptportal (oben)
Ziel: Robotikarten, Einsatzgebiete, praktische Lösungen, Produkte und Zubehör auffindbar machen.
Standard als **Vorschlag, nicht bereits beschlossener Baum**: WordPress-Seite → Unterseite → ggf. konkrete Themenseite → flache WordPress-Inhaltskategorie → spätere Beiträge.
Die genaue Tiefe hängt vom fertigen Konzept ab. Alle tatsächlich vorhandenen Ebenen müssen im sichtbaren Navigationsweg erreichbar sein.

## 2. EDITORIAL – Magazin / Journal (Informationsebene)
Ziel: Einordnung, Alltag, Entscheidungshilfe, Hintergründe, Trends, Sicherheit, Praxisfragen.
Eigene, klare Magazinrubriken. Wiederholte Themen aus CORE vermeiden; lieber von Magazinbeiträgen zum zuständigen Sachthema führen.
Ein Glossar oder Wissensbereich kann später unter dieser Säule mit eigener Navigation ergänzt werden.

## 3. DIRECTORY – Anzeigenmarkt / HivePress
Ziel: passende Anbieter, Service, Beratung, Wartung, Vermietung, Schulungen oder andere Roboter-Dienstleistungen.
Eigene Anbieter-/Inseratskategorien; nicht 1:1 alle Hauptportal-Kategorien spiegeln.
HivePress-Taxonomie erst einrichten, wenn WordPress und HivePress vorhanden sind.

## Verbindungen
Nur **bewusste Links** zwischen Säulen, keine gemeinsame Importliste, keine geteilten WordPress-IDs. Jedes Suchthema hat einen kanonischen fachlichen Haupt-Owner.

## Leerstand
CORE = 0 | EDITORIAL = 0 | DIRECTORY = 0. Die Fachentscheidung über konkrete Robotikbereiche steht noch aus.

## Festlegung zu CORE (08.11.2026)
Die oberste Ebene und Zwischenebenen sind WordPress-Seiten. Die letzte WordPress-Seite benennt einen konkreten Robotertyp als Produkt. Nur unter dieser Seite liegen *flache* WordPress-Inhaltskategorien (etwa Kosten, Fragen, Wartung, Auswahl), und unter ihnen einzelne Beiträge zu exakt diesem Robotertyp. Kein Artikel direkt in einer übergeordneten Sammelkategorie; keine automatische Standardliste von Leafs. Eine Rolle als Magazin-/Anzeigenrubrik verändert die Produkt-Hierarchie nicht.

Die erste Marktfeldrecherche samt Produktkandidaten steht in `RECHERCHE/ERSTLANDKARTE_20261108.md`; diese Kandidaten sind KEIN freigegebener Zielbaum und werden noch nicht in WordPress synchronisiert.

## Erweiterte Wissens-/Finderschicht – Konzeptprüfung 09.11.2026
Die **drei Säulen bleiben unverändert**:
- `Wissen & Glossar` ist eine **Rubrik des Magazins**. Definierte echte Fachbegriffe bekommen bei eigenständigem Definitionsbedarf eine eindeutige Begriffsseite; Kurzdefinitionen von Robotertypen verlinken auf deren bestehende CORE-Owner. Synonyme bleiben Metadaten, keine zweiten URLs.
- `Roboterfinder` ist **kein viertes Portal**, sondern ein Fragen-/Filter-Einstieg nach konkreter Aufgabe, Umgebung und nur passenden Anforderungen. Ergebnis verweist auf freigegebene CORE-Produkte und gegebenenfalls existierende DIRECTORY-Leistungen; **kein zweiter Fachmaster oder zweite Produktseite**.
- Ein eventuelles `Robotermodelle-Register` enthält erst **konkrete Hersteller-Modelle und eindeutig belegte technische Eigenschaften**, niemals eine zweite Ratgeberkopie der 68 Robotertypseiten. Indexierungsentscheidung pro Modell-Suchintent, zunächst nur Pilot.
Die geprüfte Begründung steht ausschließlich in `RECHERCHE/GLOSSAR_FINDER_MODELLREGISTER_V1_20261109.md`. Noch NICHT als WordPress-Seiten oder Plugins realisiert.
