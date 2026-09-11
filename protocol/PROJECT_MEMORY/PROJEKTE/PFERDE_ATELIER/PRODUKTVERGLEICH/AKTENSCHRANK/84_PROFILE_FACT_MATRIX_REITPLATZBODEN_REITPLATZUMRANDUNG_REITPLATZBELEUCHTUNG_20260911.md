# PRODUKTVERGLEICH – PROFILE / FACT MATRIX REITPLATZBODEN / REITPLATZUMRANDUNG / REITPLATZBELEUCHTUNG V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Registry-Gruppen:
- `reitplatzboden`;
- `reitplatzumrandung`;
- `reitplatzbeleuchtung`.

Zwischen `reitplatzboden` und `reitplatzumrandung` liegt `reitplatzdrainage` (p160). Dieser Key bleibt gemäß finaler 175er Disposition `PRODUCT_COMPARISON_V1_NOT_APPLICABLE` und wird bewusst übersprungen.

Tretschicht-Zuschlagstoff, Reitplatzumrandung und Beleuchtung sind strikt getrennte Produkt-/Systemklassen. Bauleistung, Materialprodukt und Beleuchtungsplanung dürfen nicht gegeneinander oder als Synonyme behandelt werden.

Finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin aus aktuellem Product Knowledge.

---

## 1. Reitplatzboden

Portal-Key / technischer Key:
`reitplatzboden`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Der Registry-Key ist ein Boden-Oberbegriff. Erste source-bound V1-Unterklasse:
`GEOTEXTILE_FIBER_ARENA_FOOTING_ADDITIVE_FOR_SAND_TOP_LAYER`.

Pflichtmerkmale:
- physischer Zuschlagstoff für Reitplatz-/Reithallen-Tretschicht;
- Textilfaser, Geotextil oder Vlies/Faser-Mischung;
- zum Einmischen in sandbasierte Tretschicht;
- ausdrücklich für Reitsportboden geeignet;
- kein kompletter Reitplatzbau;
- keine Drainage-/Trennschichtplatte.

Ausgeschlossen bzw. separate Klassen:
- Reitsand ohne Zuschlagstoff;
- komplette vorgemischte Sand-Tretschicht;
- Naturfaserklasse Jute/Sisal/Viskose gegen synthetische Geotextilklasse, wenn Materialart Nutzerintent ist;
- Reitplatzmatte/Trennschichtgitter;
- Drainage;
- Bau-/Einbauleistung;
- Holzschnitzel/Hackschnitzel als andere Zuschlagstoffklasse.

### Aktuelle Hersteller-Evidence

EHG GmbH:
- `innoReit-tex® Reitplatzfaser synthetic`;
- Spezialfaser aus 100 % Polyester;
- Faserlänge ca. 30 mm;
- zum Einmischen in die Tretschicht;
- auch als Vlieshäcksel-/Fasermischungen verfügbar;
- verschiedene Mischungsanteile/Varianten.

Herstellerquelle:
https://www.kunststoffmatte.eu/produkte/zuschlagstoffe-fuer-reitboden/reitplatzfaser

tegra GmbH:
- `GEOPAD`;
- Spinnvlies-/Geotextil-Zuschlagstoff für Tretschichten;
- definierte Partikelgröße/Zugabemenge laut Anbieter;
- wird vor Ort in die Tretschicht eingearbeitet;
- für Hallenböden, Dressurvierecke und Springplätze.

Herstellerquelle:
https://www.derreitboden.de/zusatzstoffe-und-pflegegeraete/zusatzstoffe-fuer-tretschichten/

ecora / `protex Geotextil` zusätzlicher Klassenbeleg:
- spezielle Mischung aus Textilfasern und Textilvlies;
- Zuschlagstoff für Reitplatz-/Reithallen-Tretschichten;
- Indoor/Outdoor.

Herstellerquelle:
https://www.ecora.de/de/portfolio/protex-geotextil/

### Faktenmatrix V1

1. `footing_additive_class`;
2. `arena_use`;
3. `indoor_outdoor_use`;
4. `base_top_layer_required`;
5. `fiber_material`;
6. `geotextile_material`;
7. `fiber_length_mm`;
8. `particle_size_range_mm`;
9. `fiber_geotextile_mix_ratio`;
10. `recommended_dose_kg_m2`;
11. `recommended_dose_kg_per_t_sand`;
12. `installation_method`;
13. `pre_mixed_available`;
14. `uv_resistance_claim`;
15. `water_storage_claim`;
16. `shear_strength_claim`;
17. `elasticity_claim`;
18. `environmental_declaration`;
19. `disposal_class_claim`;
20. `test_report_available`;
21. `packaging_unit_kg`;
22. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `reitplatzboden`;
- `footing_additive_class = GEOTEXTILE_FIBER_ARENA_FOOTING_ADDITIVE_FOR_SAND_TOP_LAYER`;
- sandbasierte Tretschicht als Zielsystem;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle;
- konkrete Material-/Mischklasse muss im Product Knowledge gebunden sein.

**Fail-closed:**
EHG, tegra und ecora belegen die gemeinsame Zuschlagstoff-Oberklasse. Ein konkretes Paar wird erst freigegeben, wenn Materialzusammensetzung, Faser-/Vliesklasse und Zugabe-/Anwendungsniveau ausreichend normalisiert sind. 100-%-Polyesterfaser darf nicht blind gegen unbekannte Mischfaser oder Naturfaser gerankt werden.

### Decision-Policy

- Zuschlagstoff-/Anwendungsgrundklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Material, Faserlänge, Mischungsverhältnis, Zugabemenge, Umwelt-/Prüfnachweise: sachliche Unterschiede;
- keine freie Aussage zu Trittsicherheit, Gelenkschonung, Scherfestigkeit, Staub, Elastizität oder Lebensdauer ohne vergleichbare Prüfevidenz;
- Herstellerclaims getrennt kennzeichnen;
- keine komplette Tretschicht gegen Einzelzuschlagstoff paaren.

---

## 2. Reitplatzumrandung

Portal-Key / technischer Key:
`reitplatzumrandung`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound V1-Klasse:
`FIXED_WHITE_PVC_DRESSAGE_ARENA_BOUNDARY_SINGLE_RAIL`.

Pflichtmerkmale:
- fest montierte Reitplatz-/Dressurviereck-Umrandung;
- weißes PVC/Vinyl/Kunststoff;
- ein horizontaler Riegel/Zaunlatte;
- niedrige Dressurviereck-Höhe;
- für 20 x 40 m bzw. 20 x 60 m konfigurierbar;
- keine mobile Kegel-/Steckumrandung.

Ausgeschlossen bzw. separate Klassen:
- mobile Dressurvierecke;
- Holzumrandung;
- 2-/3-/4-Riegel-Paddock-/Koppelzaun -> `paddockzaeune`;
- geschlossene Bande;
- einzelne Dressurbuchstaben/Kegel;
- Reitplatzzaun in normaler Pferdezaunhöhe.

### Aktuelle Hersteller-Evidence

Rutjes Pferdeboxen:
- `Kunststoff Dressurviereck | Fest Montage`;
- weißes UV-beständiges dickwandiges PVC;
- ein rechteckiger Riegel;
- Pfostenabstand 4 m;
- Pfosten ca. 80 x 13 x 13 cm;
- Riegel ca. 400 x 5 x 15 cm;
- Standardhöhe ca. 35–40 cm;
- Sets 20 x 40 m bzw. 20 x 60 m.

Herstellerquelle:
https://www.rutjespferdeboxen.de/produkt/kunststoff-dressurviereck-fest-montage/

COLUMBUS Professional Horse Equipment:
- `Ranch Fence` kann ausdrücklich als Dressurviereck mit 1 Riegel konfiguriert werden;
- Vinyl-Zaunsystem;
- passende Tore/Zubehör;
- Standard weiß, weitere Farben auf Anfrage;
- Hersteller führt Dressurviereck als eigene 1-Riegel-Nutzungskonfiguration.

Herstellerquelle:
https://www.columbus-de.com/de/zaunsysteme/ranch-fence/

### Faktenmatrix V1

1. `arena_boundary_class`;
2. `fixed_or_mobile`;
3. `material`;
4. `color`;
5. `rail_count`;
6. `standard_height_mm`;
7. `post_spacing_mm`;
8. `post_width_mm`;
9. `post_depth_mm`;
10. `post_height_mm`;
11. `rail_length_mm`;
12. `rail_width_mm`;
13. `rail_height_mm`;
14. `post_cap_class`;
15. `ground_mounting_class`;
16. `surface_mount_foot_available`;
17. `20x40_set_available`;
18. `20x60_set_available`;
19. `entry_opening_class`;
20. `dressage_letters_available`;
21. `uv_resistance_claim`;
22. `warranty_years`.

### Pairing-Regeln

- gleiche Gruppe `reitplatzumrandung`;
- `arena_boundary_class = FIXED_PVC_DRESSAGE_ARENA_BOUNDARY_SINGLE_RAIL`;
- fest montiert;
- 1 Riegel;
- niedrige Dressurviereck-Konfiguration;
- gleiche Platzgröße für konkretes Paar;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

**Fail-closed:**
Rutjes besitzt eine konkret spezifizierte 1-Riegel-Festkonfiguration; COLUMBUS belegt die konfigurierbare 1-Riegel-Systemfamilie. Konkretes Cross-Brand-Pairing erst, wenn bei COLUMBUS Maße/Set-Konfiguration für denselben 20x40- bzw. 20x60-Intent source-bound im Product Knowledge vorliegen.

### Decision-Policy

- Umrandungs-/Material-/Montage-/Riegelklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Pfostenabstand, Profile, Zubehör und Garantie: sachliche Unterschiede;
- keine freie Aussage zu Sicherheit, Bruchsicherheit, Turnierzulässigkeit oder Wartungsfreiheit;
- nicht mit 3-Riegel-Paddockzaun duplizieren.

---

## 3. Reitplatzbeleuchtung

Portal-Key / technischer Key:
`reitplatzbeleuchtung`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound V1-Oberklasse:
`MAST_MOUNTED_DIRECTIONAL_LED_FLOODLIGHT_FOR_OUTDOOR_RIDING_ARENA`.

Pflichtmerkmale:
- LED-Flutlicht/Strahler für Außenreitplatz;
- Mast-/Bügelmontage;
- gerichtete/asymmetrische bzw. nach vorne gelenkte Lichtverteilung für Sport-/Reitfläche;
- Outdoor-Schutzart mindestens IP66;
- dimmbar oder regelbar als konkrete Variante;
- ausdrücklich für Reitplatz/Reitsport geeignet.

Ausgeschlossen bzw. separate Klassen:
- 100-W-Hofstrahler -> `hofbeleuchtung`;
- Stall-Linearlampe -> `stallbeleuchtung`;
- allgemeiner Baustrahler;
- Beleuchtungsplanung als reine Dienstleistung;
- Lichtmast allein;
- komplette Turnier-Flutlichtanlage ohne identifizierbare Leuchtenprodukte.

### Aktuelle Hersteller-Evidence

Albert Kerbl GmbH:
- `LED-Flutlicht Comfort Pro`, Art.-Nr. 345412 in 200-W-Ausführung;
- ausdrücklich als Reitplatzleuchte geeignet;
- 200 W;
- 32.000 lm;
- 160 lm/W;
- 5700 K;
- Halbwertswinkel 150° mit breiter nach vorne gerichteter Linsenoptik;
- IP67, IK08;
- dimmbar 1–10 V / PWM / Widerstand;
- -40 bis +50 °C;
- Montagebügel, Mastadapter optional;
- 5 Jahre Garantie.

Herstellerquelle:
https://www.kerbl.com/de/produkt/led-flutlicht-comfort-pro-1018087

Lumosa GmbH:
- `Campo Sportivo`;
- LED-Flutlicht ausdrücklich für Reitplätze/Sportplätze;
- modulares System;
- IP66;
- -40 bis +50 °C;
- bis 100.000 h LED-Lebensdauer als Herstellerangabe;
- Lichtplanung nach DIN EN 12193;
- Dimmen/Szenen über LumosaTouch möglich;
- konkrete Modul-/Leistungsvariante muss vor Pairing gebunden sein.

Herstellerquellen:
https://www.sportplatzbeleuchtung.de/reitplatz-2/
https://www.sportplatzbeleuchtung.de/produkte/campo-sportivo

Fischer Stalltechnik zusätzlicher Reitplatzklassenbeleg:
- `Fischer FL-Serie`;
- Reitplatz-/Rennbahn-/Außenflächen-LED-Leuchte;
- aktuelle veröffentlichte Beispielvariante 300 W / 45.000 lm / 152 lm/W;
- 3000/4000/5000 K umschaltbar;
- Mastaufnahme 48–60 mm bzw. Wandhalterung.

Quelle:
https://www.fischer-stalltechnik.com/reitplatzbeleuchtung-1/

### Faktenmatrix V1

1. `arena_light_class`;
2. `riding_arena_use`;
3. `outdoor_use`;
4. `rated_power_w`;
5. `luminous_flux_lm`;
6. `luminous_efficacy_lm_w`;
7. `color_temperature_k`;
8. `color_temperature_selectable`;
9. `cri`;
10. `optical_distribution_class`;
11. `beam_angle_deg`;
12. `glare_metric_or_claim`;
13. `ip_rating`;
14. `ik_rating`;
15. `dimming_class`;
16. `control_system`;
17. `mounting_class`;
18. `mast_adapter_diameter_mm`;
19. `operating_temperature_range`;
20. `lifetime_l70_h`;
21. `power_factor`;
22. `warranty_years`;
23. `lighting_standard_planning_support`.

### Pairing-Regeln

- gleiche Gruppe `reitplatzbeleuchtung`;
- `arena_light_class = MAST_MOUNTED_DIRECTIONAL_LED_FLOODLIGHT_FOR_OUTDOOR_RIDING_ARENA`;
- Reitplatznutzung source-bound;
- IP66 oder höher;
- gerichtete Sportflächenoptik;
- konkrete Leistungs-/Optikklasse im Product Knowledge gebunden;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

**Fail-closed:**
Kerbl, Lumosa und Fischer belegen die gemeinsame Reitplatz-Flutlichtklasse. Ein konkretes Cross-Brand-Paar wird erst freigegeben, wenn Leistung, Lichtstromband, Optik/Abstrahlung und Montagekonfiguration auf derselben Entscheidungsebene gebunden sind. 200 W darf nicht automatisch gegen 300 W oder ein unbekannt konfiguriertes Modulsystem gerankt werden.

### Decision-Policy

- Reitplatz-/Outdoor-/Montagegrundklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Leistung, Lichtstrom, Effizienz, Farbtemperatur, Optik, IP/IK, Dimmung, Steuerung und Garantie: sachliche Unterschiede;
- Lux/Gleichmäßigkeit nur aus projektbezogener Lichtplanung mit gleichen Platz-/Mastbedingungen vergleichen;
- keine freie Aussage zu Pferdewohl, Sicherheit, Blendfreiheit oder Energieeinsparung;
- Hofstrahler nicht als identische Reitplatzbeleuchtung duplizieren.

## Globale Negativprüfung

Muss fail-closed bleiben:
- Tretschicht-Zuschlagstoff vs. kompletter Sandboden;
- synthetische Geotextilklasse vs. Naturfaser ohne Materialgate;
- Reitplatzboden vs. Reitplatzdrainage/Bauleistung;
- 1-Riegel-Dressurumrandung vs. 3-Riegel-Paddockzaun;
- feste Umrandung vs. mobiles Dressurviereck;
- Reitplatzflutlicht vs. 100-W-Hofstrahler;
- 200-W-Leuchte vs. 300-W-Leuchte ohne Leistungs-/Optikgate;
- einzelne Leuchte vs. komplette Lichtplanung/Anlage.

## Materialisierungsstatus

Diese Akte ist nur source-bound Fachvorarbeit.
Keine Änderung an UPC 0.8.6.
Kein Product-Knowledge-Import.
Kein SEO-/Providerlauf.
Kein Merge.
Kein Publish.
