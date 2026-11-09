# Robotik – gemeinsames Eigenschaftsschema V1 für alle Robotertypen
09.11.2026 · Grundschema aktiviert, Inhalte noch nicht eingehend fachlich geprüft.

## Wofür?
Das gleiche Prinzip wie Hobbyregister und Pferderassen: Jeder Robotertyp hat **eine eindeutige ID und dieselben Grundfelder**. Unterschiedliche Gerätetypen besitzen daneben **individuell passende** technische Zusatzwerte, niemals eine Liste von ausgedachten Kennzahlen. Das erlaubt bei mehr Recherche eine nachvollziehbare Zuordnung zum richtigen CORE-Owner, zum Roboterfinder und zu einem späteren Register konkreter Hersteller-Modelle.

## EINZIGE Datenspeicherung
`KATEGORIE/RECHERCHE/PRODUKTE_V2_20261108.json` ist die einzige aktuelle Robotertyp-Fachquelle. `candidates[].id` sind die stabilen `rb...`-IDs. Die bestehenden `product_candidate`, `research_group`, `concept_v1` und Quellen bleiben dort. **Keine zweite Roboterliste** und kein davon unabhängig änderbares Register; das „Büro“ hier enthält nur Eigenschaftsdefinition und Prüfregeln.

## Grundfelder `finder_traits_v1`
| Feld | Fachliche Frage | Aktuell |
| --- | --- | --- |
| `task` | Welche konkrete Arbeit erledigt der Roboter? | Nicht recherchiert |
| `work_environment` | Wo kann er wirklich eingesetzt werden: innen, außen, beides oder speziell? | Nicht recherchiert |
| `user_group` | Privat, gewerblich, Fachanwender, Bildung, Medizin etc.? | Nicht recherchiert |
| `mobility` | Stationär oder mobil, und unter welchen Bedingungen? | Nicht recherchiert |
| `control_mode` | Automatisch, unterstützt, fernbedient oder gemischt? | Nicht recherchiert |
| `human_interaction` | Interagiert er direkt mit Menschen / sind Schutzbereiche nötig? | Nicht recherchiert |
| `operational_requirements` | Platz, Strom/Ladebedarf, Netzwerk, Hygiene, Integration? | Nicht recherchiert |
| `safety_context` | Relevante Sicherheit, Datenschutz, Regulierung? | Nicht recherchiert |
| `acquisition_options` | Gibt es nachweisbare Geräteangebote, Miete oder Robotikdienstleistungen? | Nicht recherchiert |
| `fact_sources` | Hersteller-/Fachquellen pro nachgewiesenem Fakt | Noch leer |
| `status` | Syntaktisch vorbereitet, fachlich offen, geprüft, Konflikt? | Derzeit SCHEMA_ONLY_NOT_VERIFIED |

**Regel:** `NICHT_RECHERCHIERT` = unbekannt; das ist niemals gleich „nein“, „ungeeignet“ oder 0. Null Quellen = 0 bewiesene Eigenschaften. Nachrecherche pflegt dieselbe `rb...`-ID, inklusive Quelle und Prüfdatum. Konfliktfälle bleiben sichtbar; keine automatisch bestätigte Synonymzuordnung.

## Spezielle Felder nur bei fachlichem Sinn
- **Lager/Transport:** tatsächlich zulässiges Transportgut/Traglast, Übergabehöhe, Böden, Navigation, Übergabepunkte.
- **Industrie:** Arbeitsprozess, Werkzeuge, Reichweite, Takt-/Qualitätsanforderung.
- **Reinigung:** Boden-/Oberflächenart, Flächenleistung, Wasser/Chemie, Einsatzort, Verbrauchsmaterial.
- **Landwirtschaft:** Tierart/Kultur, Feld-/Stallbedingungen, Saison und Werkzeuge.
- **Gastronomie:** Verkehrswege, Transportleistung, Bedienung, Gästekontakt.
- **Medizin/Pflege:** belegte Funktion, Zulassungs-/Hygienestatus, fachliche Grenzen – keine medizinischen Versprechen.
- **Haushalt/Garten:** Fläche, Schwellen/Steigung, Wetter, Lärm, Privatsphäre.
- **Sicherheit/Inspektion:** Sensortyp, Prüfziel, Fernsteuerung, Betreiberrecht.

Zusatzfelder hängen am **gleichen Robotertyp-Datensatz**, mit Feldnamen, Messgröße, Einheit, Quelle und Verifikationsstatus. Kein allgemeiner pauschaler Gerätescore, keine überall erzwungenen Kilometer/Quadratmeter/Kilogramm.

## SEO und drei Säulen
Der Datensatz hat **einen einzigen Produkt-Owner** (CORE), später genau eine genehmigte letzte WordPress-Produktseite. Finderfilter und Modellvergleiche sind nur **Ansichten** über diese Daten. Magazin beantwortet andere Fragen, HivePress führt Anbieter/Leistungen, Werbeflächen/Produktangebote bleiben eigene Anbieter-Daten. Es gibt keine zweite indexierbare Produktseiten-Kopie.

## Kategorierollen
Erst nach Fach-/Keyword-Prüfung: Haupt-/Zwischenebene = WP-Seite; letzte Seite = **ein konkreter Robotertyp**; darunter flache, **nur diesem Typ zugeordnete** WP-Kategorien. Eine solche Kategorie braucht mindestens drei voneinander unterschiedliche sinnvolle spätere Beitragsabsichten; typischer Prüfmaßstab **3–5**, mehr zulässig; für 1–2 Themen keine neue Kategorie. Keine andere WP-Kategorie als Elternteil einer Kategorie innerhalb des Produktastes.

## Technische Umsetzungsgrenze
Die installierte Robotik-Version 0.3.0 hat noch **keinen** automatischen Master-/Trait-Leser. Die Eigenschaften im GitHub-Master sind Vorbereitung, keine neue WP-Funktion. Nur eine spätere **read-only** Anbindung an die freigegebene Masterrevision, keinen zweiten Writer bauen.
