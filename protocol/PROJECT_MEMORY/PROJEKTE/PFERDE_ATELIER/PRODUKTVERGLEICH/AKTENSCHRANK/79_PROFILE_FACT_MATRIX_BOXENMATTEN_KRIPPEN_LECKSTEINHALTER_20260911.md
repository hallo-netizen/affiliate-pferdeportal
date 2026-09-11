# PRODUKTVERGLEICH – PROFILE / FACT MATRIX BOXENMATTEN / KRIPPEN / LECKSTEINHALTER V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Registry-Gruppen:
- `boxenmatten`;
- `krippen-fuer-pferdeboxen`;
- `lecksteinhalter-fuer-boxen`.

Keine Gruppe wird nur über den Einsatzort Box normalisiert. Produktklasse, Bauart, Material, Kapazität und Montage bleiben Pflicht.
Finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin aus aktuellem Product Knowledge.

---

## 1. Boxenmatten

Portal-Key / technischer Key:
`boxenmatten`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Source-bound Produktklasse:
`INTERLOCKING_RUBBER_HORSE_BOX_MAT_18_20MM`.

Pflichtmerkmale:
- Gummi-/Elastomer-Stallmatte;
- ausdrücklich für Pferdeboxen geeignet;
- Puzzle-/Interlock-Verbindung;
- Stärke 18–20 mm;
- flächiger fertiger Oberbelag;
- keine Bodenraster-/Paddockplatte.

Explizite Cross-Group-Hard-Rule zu Akte 70:
Viele aktuelle Produkte werden vom Hersteller **gleichzeitig** für `Box` und `Liegefläche/Offenstall` freigegeben. Darum darf `boxenmatten` **nicht** denselben Produktvergleich ein zweites Mal nur unter anderem Standort-Key erzeugen.

Für einen eigenen Boxenmatten-Vergleich muss mindestens eines source-bound vorliegen:
1. konkrete boxenspezifische Produkt-/Konfigurationsvariante, die nicht bereits im Offenstall-Liegeflächenpaar verwendet wird; oder
2. klar gebundener eigener Nutzer-/SEO-Intent `INDIVIDUAL_HORSE_BOX_FLOORING`, der im späteren SEO-Gate einen eigenständigen Vergleich rechtfertigt, plus Cross-Group-Dedup gegen `liegeflaechen-im-offenstall`.

Ohne diese Differenzierung: **0 neuer Vergleich trotz vorhandener Produktevidence**.

### Aktuelle Hersteller-Evidence

Gummiwerk KRAIBURG Elastik / BELMONDO:
- `BELMONDO Classic`;
- ausdrücklich für Box und Liegefläche;
- 18 mm;
- 1 x 1 m;
- vierseitige Puzzleverbindung;
- vulkanisierter Gummi;
- Hufeisenprofil mit Deckschicht;
- schwimmende Verlegung auf befestigtem Untergrund;
- befahrbar innerhalb der veröffentlichten Herstellervorgaben.

Quellen:
https://kraiburg-belmondo.de/produkte/stallmatten-fuer-box-und-liegeflaeche/belmondo-classic/
https://kraiburg-belmondo.de/produkte/stallmatten-fuer-box-und-liegeflaeche/belmondo-classic/technische-daten/

MRH Mülsen GmbH / sagu® matting:
- `Stallmatten 960 × 960 × 20 mm Puzzle`;
- ausdrücklich als Boxenmatte/Pferdeboxenmatte geführt;
- zugleich für Offenstall/Laufstall und weitere Bereiche freigegeben;
- 960 x 960 mm;
- 20 mm;
- Gummimatte mit Puzzle-System.

Quelle:
https://www.sagu-muelsen.de/sagu-matting-stallmatten/stallmatten-960-960-20-puzzle.html

### Faktenmatrix V1

1. `flooring_class`;
2. `individual_box_use`;
3. `open_stable_use`;
4. `cross_group_overlap`;
5. `material`;
6. `thickness_mm`;
7. `width_mm`;
8. `length_mm`;
9. `connection_system`;
10. `surface_profile`;
11. `underside_profile`;
12. `installation_substrate_requirement`;
13. `installation_method`;
14. `vehicle_traffic_claim`;
15. `liquid_absorption_or_drainage_design`;
16. `cleaning_method`;
17. `manufacturer_grip_cushioning_insulation_claims`;
18. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `boxenmatten`;
- `flooring_class = INTERLOCKING_RUBBER_HORSE_BOX_MAT_18_20MM`;
- individuelle Pferdebox-Eignung source-bound;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle;
- **zusätzlich zwingend:** `cross_group_dedup_pass = true` gegen `liegeflaechen-im-offenstall`.

### Decision-Policy

- Klasse/Boxennutzung/Puzzleklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Stärke, Maße, Ober-/Unterseite, Montage und Befahrbarkeit: sachliche Unterschiede;
- keine freie Aussage zu Tierwohl, Trittsicherheit, Einstreueinsparung, Gelenkschonung oder Haltbarkeit;
- Herstellerclaims getrennt halten;
- kein eigener Vergleich, wenn nur dieselbe Produktklasse und dasselbe Paar wie bei Offenstall-Liegefläche erneut erzeugt würde.

---

## 2. Krippen für Pferdeboxen

Portal-Key / technischer Key:
`krippen-fuer-pferdeboxen`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound Cross-Brand-V1-Klasse:
`FIXED_PLASTIC_HORSE_WALL_FEED_TROUGH_15_16L`.

Pflichtmerkmale:
- Kunststoff-Futtertrog/Futterkrippe;
- ausdrücklich für Pferde bzw. Pferdestall geeignet;
- feste Wandmontage;
- Fassungsvermögen 15–16 Liter;
- primär Futtertrog, keine Tränke;
- keine Heuraufe und kein mobiler Einhängetrog.

Ausgeschlossen bzw. separate Klassen:
- Ecktrog als eigene Montage-/Formklasse;
- Einhängetrog/Turnierkrippe;
- Aluminium-/Metalltrog als andere Materialklasse;
- Fohlentrog mit Trennstäben;
- Futterautomat;
- Heuraufe/Heuspender;
- Wassertränke/Schwimmertränke.

### Aktuelle Hersteller-/Direktprodukt-Evidence

Albert Kerbl GmbH:
- `Futtertrog`, Art.-Nr. 3258 / 32582;
- 15 l;
- splitterfreier Kunststoff;
- rechteckig;
- 42 x 30 x 32 cm;
- fester Futterplatz an der Wand;
- für Box/Stall und Pferde source-bound;
- Variante mit oder ohne Schutzkante.

Quelle:
https://www.kerbl.com/de/produkt/futtertrog-17990

GÖBEL:
- `Kunststoff Pferde Wandtrog`;
- 16 l;
- robuster Kunststoff;
- Wandmontage;
- umlaufende Schutzkante;
- 31 x 34 x 31 cm;
- ausdrücklich für Pferd/Pony/Esel und Box/Stall-Kontext.

Direktproduktquelle:
https://www.stallbedarf24.de/goebel-kunststoff-pferde-wandtrog

### Faktenmatrix V1

1. `feed_trough_class`;
2. `horse_use`;
3. `mounting_class`;
4. `capacity_l`;
5. `shape_class`;
6. `width_mm`;
7. `depth_mm`;
8. `height_mm`;
9. `material`;
10. `food_safe_claim`;
11. `splinter_or_break_resistance_claim`;
12. `feed_retention_lip`;
13. `protective_edge`;
14. `drain_or_cleaning_plug`;
15. `mounting_holes`;
16. `mounting_hardware_included`;
17. `water_use_approved`;
18. `roughage_use_claim`;
19. `concentrate_feed_use_claim`;
20. `available_colors`;
21. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `krippen-fuer-pferdeboxen`;
- `feed_trough_class = FIXED_PLASTIC_HORSE_WALL_FEED_TROUGH`;
- 15–16-l-Kapazitätsklasse;
- feste Wandmontage;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Formunterschiede bleiben Vergleichsfakten, solange Montage, Material, Kapazität und Pferde-Futterzweck gleich bleiben.

### Decision-Policy

- Klasse/Material/Montage/Kapazitätsklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Form, Schutzkante, Stopfen und Futterfreigaben: sachliche Unterschiede;
- keine freie Aussage zu Futterverlust, Hygiene, Verletzungssicherheit oder Haltbarkeit;
- Herstellerclaims zu Bruchsicherheit/Witterungsbeständigkeit bleiben Herstellerclaims;
- Wasserfreigabe nur bei explizitem Source-Beleg.

---

## 3. Lecksteinhalter für Boxen

Portal-Key / technischer Key:
`lecksteinhalter-fuer-boxen`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound Cross-Brand-V1-Klasse:
`WALL_MOUNTED_PLASTIC_SALT_LICK_HOLDER_10KG`.

Pflichtmerkmale:
- Kunststoff-Lecksteinhalter;
- für Salz-/Minerallecksteine;
- 10-kg-Klasse;
- Wandmontage möglich;
- Pferde-/Stallnutzung source-bound;
- runde und/oder eckige Standard-Lecksteine.

Ausgeschlossen bzw. separate Klassen:
- kleine 2-kg-Halter wie Kerbl 324803;
- Metall-/Edelstahlhalter;
- hängende Spiel-/Likit-Halter;
- Leckschale;
- Leckstein selbst;
- Bodenhalter ohne Wandmontage.

### Aktuelle Hersteller-Evidence

PATURA:
- `Kunststoff-Lecksteinhalter für eckige oder runde Lecksteine`, Art.-Nr. 333200;
- für 10-kg-Steine;
- Kunststoff;
- Anschraub-Montage an Wandflächen;
- Stall/Weidehütte/Freigelände;
- eckige bzw. runde Modellvariante.

Direktproduktquelle:
https://www.stallbedarf24.de/patura-kunststoff-lecksteinhalter-fuer-eckige-oder-runde-lecksteine/

GÖBEL:
- `Salzlecksteinhalter Kunststoff`, Art.-Nr. 20523-GOE;
- für Lecksteine bis 10 kg;
- runde und eckige Formate;
- Kunststoff;
- Stall-/Weidenutzung;
- ca. 20 x 20,5 x 22 cm;
- mehrere Farben.

Direktproduktquelle:
https://www.stallbedarf24.de/goebel-salzlecksteinhalter-kunststoff/20523-goe

Lister:
- `Lecksteinhhalter SL 3 / SL 3 FLEX / SL 3 ECO`;
- robuste Kunststoffklasse;
- Wand- oder Rohrbefestigung;
- für runde und eckige Salzlecksteine;
- Maße je SL-3-Klasse ca. 203 mm breit x 215 mm tief;
- Herstellerkatalog bindet die Produktfamilie im Lecksteinhalter-Programm.

Quelle:
https://www.stallbedarf24.de/media/8f/a4/98/1759903361/lister-gesamtkatalog_onlineversion.pdf

### Faktenmatrix V1

1. `lick_holder_class`;
2. `material`;
3. `max_lick_weight_kg`;
4. `round_lick_compatible`;
5. `rectangular_lick_compatible`;
6. `width_mm`;
7. `depth_mm`;
8. `height_mm`;
9. `wall_mounting`;
10. `pipe_mounting`;
11. `mounting_holes`;
12. `mounting_hardware_included`;
13. `uv_resistance_claim`;
14. `weather_resistance_claim`;
15. `bite_resistance_claim`;
16. `food_contact_or_material_claim`;
17. `available_colors`;
18. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `lecksteinhalter-fuer-boxen`;
- `lick_holder_class = WALL_MOUNTED_PLASTIC_SALT_LICK_HOLDER_10KG`;
- 10-kg-Kapazitätsklasse;
- Wandmontage source-bound;
- konkrete runde/eckige Variante im Product Knowledge gebunden;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

### Decision-Policy

- Klasse/Material/Kapazität/Montage: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Formkompatibilität, Zusatzbefestigung und Farben: sachliche Unterschiede;
- keine freie Aussage zu Haltbarkeit, Hygiene, Witterungsfestigkeit oder Verbisssicherheit;
- 2-kg-Halter nicht gegen 10-kg-Halter paaren;
- Metall-/Edelstahlklasse separat halten.

## Globale Negativprüfung

Muss fail-closed bleiben:
- Boxenmatte als bloßes Duplikat desselben Offenstall-Liegeflächenpaars;
- Gummimatte vs. Bodenraster;
- Wandtrog vs. Einhängetrog/Heuraufe/Tränke;
- 15–16-l-Wandtrog vs. große Gruppenfütterungsrinne;
- 2-kg-Lecksteinhalter vs. 10-kg-Halter;
- Kunststoff-Lecksteinhalter vs. Metall-/Edelstahlklasse;
- Lecksteinhalter vs. Leckstein selbst.

## Materialisierungsstatus

Diese Akte ist nur source-bound Fachvorarbeit.
Keine Änderung an UPC 0.8.6.
Kein Product-Knowledge-Import.
Kein SEO-/Providerlauf.
Kein Merge.
Kein Publish.
