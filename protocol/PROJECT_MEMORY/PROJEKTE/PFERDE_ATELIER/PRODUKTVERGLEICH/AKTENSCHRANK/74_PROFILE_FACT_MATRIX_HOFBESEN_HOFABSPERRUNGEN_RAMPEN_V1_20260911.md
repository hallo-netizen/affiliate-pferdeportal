# PRODUKTVERGLEICH – PROFILE / FACT MATRIX HOFBESEN / HOFABSPERRUNGEN / RAMPEN V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Registry-Gruppen:
- `hofbesen`;
- `hofabsperrungen`;
- `rampen-am-hof`.

Breite Oberbegriffe werden für V1 auf konkrete physische Funktionsklassen normalisiert.
Finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin aus aktuellem Product Knowledge.

---

## 1. Hofbesen

Portal-Key:
`hofbesen`

Technischer Key:
`hofbesen`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound Cross-Brand-V1-Klasse:
`50CM_ELASTON_STALL_YARD_BROOM_HEAD_WITHOUT_HANDLE`.

Pflichtmerkmale:
- Stall-/Hofbesen;
- Arbeitsbreite ca. 50 cm;
- Elaston-/vergleichbare robuste Kunstborsten;
- Besenkopf mit Stielaufnahme;
- Lieferung ohne Stiel für die erste konkrete V1-Klasse.

Ausgeschlossen bzw. separate Klassen:
- Reisstrohbesen;
- Bambusbesen;
- Straßen-/Industriebesen ohne Stall-/Hofklasse;
- Handfeger;
- Kehrmaschine;
- Besen mit integrierter Kratzkante als Sonderkonstruktion, wenn genau diese Funktion der Suchintent ist;
- 60-cm-/andere Breiten als konkrete Varianten ohne gleiche Größenklasse.

### Aktuelle Hersteller-/Direktprodukt-Evidence

Krämer Pferdesport / SHOWMASTER:
- `Stall- und Hofbesen`, Nr. `450555`;
- robuste rote Elastonborsten;
- Breite 50 cm;
- Stielhalter für 24-mm-Stiele;
- ohne Stiel.

Direktprodukt-/Herstellerquelle:
https://www.kraemer.de/Stalleinrichtung/Stallzubehoer-Reitplatzzubehoer/Sattelkammer/Stall-und-Hofbesen

sorex:
- `sorex Stall- und Hofbesen`, Art.-Nr. `92000 00001`;
- unbehandelter Holzrücken;
- Arbeitsbreite ca. 50 cm;
- Profi-Elaston-Borsten ca. 8 cm;
- Metallhalterung für Stiel, Ø 28 mm;
- ohne gebundenen Stiel in der Produktbeschreibung.

Direktproduktquelle:
https://www.loesdau.de/sorex-stall-und-hofbesen-50-cm-92000-00001.html

### Faktenmatrix V1

1. `broom_class`;
2. `working_width_mm`;
3. `bristle_material`;
4. `bristle_length_mm`;
5. `back_material`;
6. `handle_included`;
7. `handle_socket_diameter_mm`;
8. `handle_mount_material`;
9. `scraper_edge`;
10. `manufacturer_intended_surfaces`;
11. `manufacturer_dirt_type_claim`;
12. `country_of_manufacture_claim`;
13. `warranty`.

Nicht veröffentlichte Borstenhärte, Kehrleistung, Nutzungsdauer oder Flächenleistung bleiben `NOT_IN_SOURCE`.

### Pairing-Regeln

- gleiche Gruppe `hofbesen`;
- `broom_class = STALL_YARD_BROOM_HEAD`;
- Arbeitsbreite 500 mm ± kleine herstellerbedingte Toleranz;
- Kunst-/Elastonborsten;
- gleiche Lieferklasse ohne Stiel;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

### Decision-Policy

- Klasse/Breite/Lieferumfang: `PAIRING_EQUAL_NO_PREFERENCE`;
- Borstenlänge, Rückenmaterial und Stielaufnahme: sachliche Unterschiede;
- keine freie Aussage zu Kehrleistung, Haltbarkeit, Kraftaufwand oder Oberflächenschonung;
- Kundenbewertungen sind kein Fachfakt;
- `Made in Germany` ist Herkunftsangabe, kein Qualitätsranking.

---

## 2. Hofabsperrungen

Portal-Key:
`hofabsperrungen`

Technischer Key:
`hofabsperrungen`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound V1-Klasse:
`MOBILE_FREE_STANDING_TEMPORARY_ACCESS_BARRIER`.

Primärer Zweck:
Temporäre, versetzbare Absperrung von Arbeits-/Zugangs-/Verkehrsbereichen auf Hof-/Betriebsflächen.

Pflichtmerkmale:
- mobil/versetzbar;
- freistehende Füße/Standbasis;
- visuell erkennbare Barriere;
- für temporäre Absperrung von Personen-/Fahrzeugzugang bzw. Arbeitsbereichen;
- keine permanente Einfriedung.

Ausgeschlossen bzw. separate Klassen:
- Weide-/Paddocktor;
- Tier-/Pferdepanel;
- Stalltrennwand;
- Fressgitter;
- fest einbetonierter Poller;
- Kettenpfosten-System als andere Konstruktionsklasse;
- Schrankenbaum mit Fundament/Antrieb;
- Verkehrsbake ohne zusammenhängende Barrierefunktion.

### Aktuelle Hersteller-Evidence

Schake GmbH:
- `Absperrgitter aus Kunststoff`, Art.-Nr. `33320KDRF`-Familie;
- Gesamtlänge 2,00 m;
- weiß/rot je Variante;
- integrierte drehbare Füße;
- Haken-/Ösensystem zum Verbinden;
- Hersteller nennt temporäre Abgrenzung von Arbeits-, Gefahren- und Zugangsbereichen sowie Lenkung von Personenströmen.

Herstellerquelle:
https://www.schake.com/de/produkte/bautechnik-verkehrssicherung/verkehrssicherung/absperrschrankengitter/v33320.html

Enne Plastica Group:
- `Mobile Absperrschranke` / mobile barrier;
- mobile Absperrung/Zaun für Arbeitsbereiche, Hindernisse sowie Personen-/Fahrzeugverkehr;
- leichte oder schwere Version mit leeren bzw. sandgefüllten Füßen;
- breite Struktur;
- reflektierender Streifen;
- verstellbare Füße.

Herstellerquelle:
https://www.enneplastica.com/de/prodotto/mobile-absperrschranke/

### Faktenmatrix V1

1. `barrier_class`;
2. `mobility_class`;
3. `primary_use_scope`;
4. `material`;
5. `length_mm`;
6. `height_mm`;
7. `weight_kg`;
8. `foot_design`;
9. `foot_weighting_option`;
10. `fold_or_rotation_for_storage`;
11. `interconnection_system`;
12. `reflective_marking`;
13. `visibility_colors`;
14. `weather_or_uv_claim`;
15. `standard_or_certification`;
16. `manufacturer_safety_claims`;
17. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `hofabsperrungen`;
- `barrier_class = MOBILE_FREE_STANDING_TEMPORARY_ACCESS_BARRIER`;
- mobile freistehende Ausführung;
- kein Tiergitter-/Paddocktor-/Festpoller-System;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Material, Länge, Fußsystem und Reflektierung dürfen variieren; sie sind Vergleichsfakten. Konkrete Verkehrs-/Normzulassungen dürfen nur mit identischer Normklasse direkt verglichen werden.

### Decision-Policy

- Funktions-/Mobilitätsklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Gewicht, Füße, Verbindung und Reflektierung: sachliche Unterschiede;
- keine freie Aussage zu Standfestigkeit, Aufprallsicherheit, Sichtbarkeit oder Wetterbeständigkeit;
- Norm-/Zulassungsstatus nur exakt source-bound;
- keine Eignung als Pferde-/Tierbarriere ableiten.

---

## 3. Rampen am Hof

Portal-Key:
`rampen-am-hof`

Technischer Key:
`rampen-am-hof`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound V1-Klasse:
`PORTABLE_PERFORATED_ALUMINUM_LOADING_RAMP_FOR_WHEELED_EQUIPMENT`.

Pflichtmerkmale:
- portable Auffahr-/Verladerampe;
- Aluminium;
- perforierte/gelochte bzw. rutschhemmend strukturierte Fahrfläche;
- für bereifte Fahrzeuge/Geräte/Maschinen;
- keine feste bauliche Hoframpe.

Ausgeschlossen bzw. separate Klassen:
- fest betonierte Rampe;
- Pferdeanhänger-Verladerampe als Fahrzeugbauteil;
- Rollstuhlrampe mit primärem Barrierefreiheitszweck;
- Überladebrücke für Stapler/Lkw als andere Last-/Bauklasse;
- reine Tritt-/Arbeitsplattform;
- Rampe für Kettenfahrzeuge, wenn die Vergleichsprodukte ausdrücklich nur Luft-/Gummibereifung freigeben;
- Klapprampe gegen starre Rampe, wenn Klappfunktion Teil des Nutzerintents ist.

### Aktuelle Hersteller-Evidence

Schake GmbH:
- `Auffahrrampe aus Aluminium, gelocht`, Art.-Nr. `220026`-Familie;
- portable leichte/stabile Aluminiumprofil-Rampe;
- gelochte rutschhemmende Lauffläche;
- Auflagefläche und Fixierlöcher;
- Varianten u. a. 2.000 x 260 mm mit max. Belastung 1.000 kg;
- Hersteller nennt Fahrzeuge, Maschinen und Transportgeräte als Verwendungszweck.

Herstellerquelle:
https://www.schake.com/de/produkte/bautechnik-verkehrssicherung/lager-transport/auffahrrampen/art-220026

Stürmer Maschinen GmbH:
- `AR 1000-2,0`, Art.-Nr. `6202022`;
- Aluminium;
- 2.000 mm lang;
- ca. 260 mm breit;
- perforierte Trittoberfläche;
- 7,6 kg pro Rampe;
- Tragkraft 1.000 kg **pro Paar**;
- geeignet für Motorrad, Quad, Gartentraktoren und Kompaktmaschinen.

Herstellerquelle:
https://www.stuermer-maschinen.de/werkstatttechnik/werkstatt-und-hebetechnik-transporthilfen/ar-1000-20-6202022/

### Faktenmatrix V1

1. `ramp_class`;
2. `construction_class`;
3. `material`;
4. `length_mm`;
5. `width_mm`;
6. `height_mm`;
7. `weight_kg_per_ramp`;
8. `quantity_in_unit`;
9. `rated_capacity_kg`;
10. `capacity_unit` – PER_RAMP / PER_PAIR / SYSTEM;
11. `capacity_test_or_axle_condition`;
12. `surface_type`;
13. `upper_support_or_hook_design`;
14. `fixing_system`;
15. `min_loading_height_mm`;
16. `max_loading_height_mm`;
17. `max_slope_claim`;
18. `wheel_or_track_compatibility`;
19. `foldable`;
20. `manufacturer_intended_equipment`;
21. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `rampen-am-hof`;
- `ramp_class = PORTABLE_LOADING_RAMP`;
- Aluminium;
- starre/perforierte Grundklasse für den ersten V1-Vergleich;
- vergleichbare Länge/Breite als konkrete Varianten;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

**Traglast-Hardgate:**
`rated_capacity_kg` darf erst direkt verglichen werden, wenn `capacity_unit` und Prüf-/Achsbedingung identisch normalisiert sind. 1.000 kg pro Paar ist nicht automatisch 1.000 kg pro Einzelrampe.

### Decision-Policy

- Rampen-/Konstruktionsklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Gewicht, Oberfläche, Fixierung und Einsatzgeräte: sachliche Unterschiede;
- Traglast nur nach identischer Einheit/Bedingung;
- keine freie Aussage zu Rutschfestigkeit, Sicherheit, Stabilität oder Handhabung;
- kein Sieger aus nominell höherer Belastungsangabe ohne gleiche Prüfdefinition;
- keine Pferde-/Anhänger-Verladesicherheit aus Hof-Geräterampen ableiten.

## Globale Verbote für alle drei Gruppen

- keine Besenkonstruktionen unterschiedlicher Grundklasse blind mischen;
- Hofabsperrung nicht als Pferdepanel/-tor interpretieren;
- mobile Geräterampe nicht mit Pferdeanhänger-/Baurampe mischen;
- Traglast-Einheiten niemals still gleichsetzen;
- kein Gesamtsieger;
- keine Punkte/Sterne/Rankings;
- keine Shop-/Affiliate-Verfügbarkeit als Fachargument;
- keine Sicherheits-, Haltbarkeits- oder Leistungswertung ohne direkt vergleichbare Evidenz;
- Quellenlücke bleibt `NOT_IN_SOURCE`.

## Produktvalidierung gegen die Profilspec

Fresh source-bound Gegenprüfung 2026-09-11:

- `hofbesen`: Krämer/SHOWMASTER 450555 + sorex 92000 belegen zwei unabhängige 50-cm-Stall-/Hofbesenköpfe mit Elastonborsten und Stielaufnahme;
- `hofabsperrungen`: Schake Kunststoff-Absperrgitter + Enne Plastica mobile Absperrschranke belegen zwei unabhängige mobile, freistehende temporäre Zugangs-/Arbeitsbereichsbarrieren; keine Tierbarrieren-Eignung wird behauptet;
- `rampen-am-hof`: Schake 220026-Familie + Stürmer AR 1000-2,0 belegen zwei unabhängige portable perforierte Aluminium-Auffahrrampen für bereifte Geräte/Fahrzeuge; konkrete Traglastwerte bleiben bis zur Einheiten-/Bedingungsnormalisierung rein sachlich.

Das ist keine finale Paarfreigabe und keine Markt-Vollständigkeit.

## Technische Materialisierungsgrenze

Dieses Dokument ändert `comparison-profiles.json` nicht.

Die Spezifikationen aus Akten 62–74 bleiben source-bound gesammelt. Vor technischer Materialisierung muss Product Knowledge pro Produkt/Variante die Klassenbindung und Pflichtfakten tragen.

Erst dann darf das Plugin aus aktuellem Product Knowledge fachlich zulässige Cross-Brand-Paare berechnen und regelmäßig neu bewerten.

Noch nicht behauptet:
- Product Knowledge vollständig;
- Markt vollständig;
- Pairing-Ready im technischen System;
- konkrete A-vs-B-Paarfreigabe;
- SEO-PASS;
- Pluginmaterialisierung.

Kein Merge.
Kein Publish.
