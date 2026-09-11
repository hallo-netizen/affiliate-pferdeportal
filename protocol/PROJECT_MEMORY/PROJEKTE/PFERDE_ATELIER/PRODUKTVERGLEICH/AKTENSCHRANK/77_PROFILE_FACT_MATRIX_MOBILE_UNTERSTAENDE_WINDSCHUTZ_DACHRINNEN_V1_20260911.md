# PRODUKTVERGLEICH – PROFILE / FACT MATRIX MOBILE UNTERSTÄNDE / WINDSCHUTZ / DACHRINNEN V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Registry-Gruppen:
- `mobile-unterstaende`;
- `windschutz-fuer-pferde`;
- `dachrinnen-am-unterstand`.

Explizit übersprungen:
- `weideunterstaende` -> `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`;
- `unterstand-boden` -> `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`.

`mobile-unterstaende` darf **nicht** den präziseren Registry-Key `weidezelt` duplizieren. Zelt-/Planen-Unterstände bleiben aus der ersten Mobilunterstands-V1-Klasse draußen.
Finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin aus aktuellem Product Knowledge.

---

## 1. Mobile Unterstände

Portal-Key:
`mobile-unterstaende`

Technischer Key:
`mobile-unterstaende`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Gebundene V1-Oberklasse:
`RIGID_RELOCATABLE_HORSE_FIELD_SHELTER_ON_SKIDS_OR_WHEELS`.

Pflichtmerkmale:
- starrer, konstruktiver Pferde-/Weideunterstand;
- explizit mobil/versetzbar;
- Versetzsystem über Kufen/Schlitten oder Räder source-bound;
- starre Rahmen-/Wandkonstruktion;
- keine reine Zelt-/PVC-Planenkonstruktion;
- für Pferde-/Weide-/Offenstallhaltung source-bound.

Ausgeschlossen bzw. separate Klassen:
- `weidezelt` / Panelzelt / PVC-Membranzelt;
- fest auf Fundament/Betonelementen montierte Weidehütte;
- reine mobile Pferdebox ohne Unterstands-/Offenstallkonfiguration;
- Anhänger/Fahrzeug;
- Carport-/Maschinenunterstand ohne Pferdenutzung;
- bloße Panel-/Windschutz-Konstruktion ohne Dach/Unterstandsfunktion.

Pflichtgates vor konkreter Paarfreigabe:
- `mobility_mechanism` = SKIDS / WHEELS;
- `shelter_configuration`;
- `open_front_class`;
- `width_mm`, `depth_mm`, `height_mm`;
- konkrete Standard-/Kundenkonfiguration.

### Aktuelle Hersteller-Evidence

Ferox GmbH:
- aktuelle Produktklasse `Mobile Weidehütte`;
- schneller/flexibler Standortwechsel direkt auf der Weide;
- stabile Schlittenkonstruktion;
- starre Holz-/Hüttenkonstruktion;
- ausdrücklich als mobile Weidehütte/Unterstand geführt.

Herstellerquelle:
https://ferox-zaun.de/weidehuetten/

Wördekemper GmbH & Co. KG / Mobilstall:
- mobiles Pferdestall-/Weidehütten-System `REGIO`;
- feuerverzinkter Stahl und Hartholz;
- mobile Offenstall-/Weidehütten-Konfigurationen;
- Kufen ermöglichen Versetzen auf der Weide;
- individuell konfigurierbar;
- verschiedene Boden-/Innenausstattungen möglich.

Herstellerquelle:
https://mobilstall.de/mobilstallsysteme/mobiler-pferdestall/

Zusätzlicher Klassenbeleg:
Peter Rudl GmbH führt fertig montierte mobile Weidehütten auf Rädern, z. B. 5 x 2,5 m. Räder bleiben eine eigene Mobilitätsunterklasse und werden nicht still gegen Kufen gepaart.

Quelle:
https://www.rudl-gmbh.de/mobileweidehuette.php

### Faktenmatrix V1

1. `shelter_class`;
2. `horse_use_scope`;
3. `mobility_class`;
4. `mobility_mechanism`;
5. `shelter_configuration`;
6. `open_front_class`;
7. `width_mm`;
8. `depth_mm`;
9. `height_mm`;
10. `frame_material`;
11. `wall_material`;
12. `roof_material`;
13. `roof_insulation`;
14. `floor_included`;
15. `floor_options`;
16. `ventilation_opening_or_curtain`;
17. `tow_or_relocation_method`;
18. `anchoring_required`;
19. `assembly_state`;
20. `manufacturer_weather_claims`;
21. `planning_permission_claim_or_notice`;
22. `warranty`.

Baurecht/Genehmigungsfreiheit ist standortabhängig und **kein** Produktfakt, sofern nicht nur als allgemeiner Herstellerhinweis gekennzeichnet. Keine Rechtsaussage aus Mobilität ableiten.

### Pairing-Regeln

- gleiche Gruppe `mobile-unterstaende`;
- `shelter_class = RIGID_RELOCATABLE_HORSE_FIELD_SHELTER`;
- starre Konstruktion, kein Weidezelt;
- gleiche `mobility_mechanism` für ein konkretes Paar;
- gleiche normalisierte Unterstands-/Frontkonfiguration;
- vergleichbare Abmessungs-/Kapazitätsklasse;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

**Fail-closed:**
Ferox und Mobilstall belegen die gemeinsame starre mobile Unterstandsklasse. Ein konkretes Cross-Brand-Paar wird erst freigegeben, wenn eine konkrete Kufen-/Front-/Größenkonfiguration beidseitig source-bound im Product Knowledge liegt.

### Decision-Policy

- Klasse/Mobilitätsmechanismus/Konfiguration: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Rahmen-/Wand-/Dachmaterial, Boden, Lüftung und Versetzart: sachliche Unterschiede;
- keine freie Aussage zu Tierwohl, Wetterfestigkeit, Lebensdauer, Genehmigungsfreiheit, Standsicherheit oder Wirtschaftlichkeit;
- Herstellerclaims bleiben Herstellerclaims;
- keine Zeltlösung gegen starre Hütte.

---

## 2. Windschutz für Pferde

Portal-Key:
`windschutz-fuer-pferde`

Technischer Key:
`windschutz-fuer-pferde`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound V1-Klasse:
`FIXED_MESH_WIND_BREAK_FOR_HORSE_STALL_OPEN_STABLE`.

Pflichtmerkmale:
- luftdurchlässiges Windschutznetz/-gewebe;
- ausdrücklich für Pferdestall, Offenstall, Paddock-/Panelbereich oder Pferdeunterstand geeignet;
- feste/verspannte Seitenabschirmung;
- Windschutz bei erhaltener Luftdurchlässigkeit;
- kein vollständig geschlossener PVC-Seitenvorhang.

Ausgeschlossen bzw. separate Klassen:
- geschlossene Seitenplane;
- Rolltor/Rollvorhang;
- Lamellenvorhang;
- feste Wand/Trennwand;
- Garten-Sichtschutznetz ohne Pferde-/Stallbeleg;
- Windschutzhecke;
- Giebel-Kombiplane mit Netz + geschlossener Plane als andere Konstruktion.

### Aktuelle Hersteller-Evidence

Albert Kerbl GmbH:
- `Windschutznetz`, Art.-Nr. `442645` / `442646`;
- für Weidepanele/Weidezelt-Seitenwände;
- Pferde/Ponys und weitere Weidetiere;
- PVC-Polyester-Gewebe;
- 420 g/m²;
- Maschenweite 2,5 x 2,5 mm;
- 0,85 mm Materialstärke;
- Varianten 350 x 155 cm bzw. 290 x 155 cm;
- Gurtset inklusive;
- UV-beständig und wasserabweisend laut Hersteller.

Herstellerquelle:
https://www.kerbl.com/de/produkt/windschutznetz-1078236

HAAS Pferdesport / Agriflex:
- `HAAS Agriflex Windschutznetz`, Art.-Nr. `N100` / `N200`;
- ausdrücklich für Pferdeboxen, Pferdestall, Offenstall-/Panel-Zelt-Kontext;
- Windschutz bei Luftaustausch;
- Maschenweite ca. 1 x 1 mm;
- Gewebegewicht ca. 260 g/m²;
- 1 m oder 2 m Breite, Meterware;
- nach Bedarf konfektionierbar;
- UV-/witterungsbeständig laut Anbieter;
- Herstellerclaim: Wind bis zu 90 % gebrochen.

Herstellerquellen:
https://www.haas-pferdesport.eu/HAAS-Agriflex-Windschutznetz-1-m-breit-unkonfektioniert/N100
https://www.haas-pferdesport.eu/Windschutz/Windschutznetz/

### Faktenmatrix V1

1. `wind_break_class`;
2. `horse_stable_use`;
3. `open_stable_use`;
4. `material`;
5. `fabric_weight_g_m2`;
6. `material_thickness_mm`;
7. `mesh_width_mm`;
8. `mesh_height_mm`;
9. `product_width_mm`;
10. `product_length_mm`;
11. `custom_length_available`;
12. `edge_finish`;
13. `eyelet_spacing_mm`;
14. `strap_or_fastening_set_included`;
15. `wind_reduction_claim_percent`;
16. `air_permeability_claim`;
17. `uv_resistance_claim`;
18. `weather_resistance_claim`;
19. `water_repellent_claim`;
20. `available_colors`;
21. `warranty`.

Windreduktionswerte dürfen nur mit identischem Prüfverfahren direkt verglichen werden. Ein Prozentclaim ohne Prüfstandard bleibt Herstellerclaim.

### Pairing-Regeln

- gleiche Gruppe `windschutz-fuer-pferde`;
- `wind_break_class = FIXED_MESH_WIND_BREAK`;
- Pferde-/Stall-/Offenstallnutzung source-bound;
- luftdurchlässiges Netz, keine geschlossene Plane;
- konkrete Konfektion/Größe im Product Knowledge gebunden;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

### Decision-Policy

- Klasse/Nutzung/Netzbauart: `PAIRING_EQUAL_NO_PREFERENCE`;
- Gewebegewicht, Maschenweite, Maße, Befestigung und UV-/Wetterclaims: sachliche Unterschiede;
- keine freie Aussage zu Zugfreiheit, Atemwegsgesundheit, Stabilität, Windlast oder Lebensdauer;
- Hersteller-Windprozentwerte ohne gemeinsame Prüfmethode nicht ranken;
- keine geschlossene Plane als gleichwertiges Netz behandeln.

---

## 3. Dachrinnen am Unterstand

Portal-Key:
`dachrinnen-am-unterstand`

Technischer Key:
`dachrinnen-am-unterstand`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound Cross-Brand-V1-Klasse:
`HALF_ROUND_PLASTIC_GUTTER_RG100`.

Pflichtmerkmale:
- halbrunde Dachrinne;
- Kunststoff;
- Richtgröße RG 100;
- Systemprodukt mit passenden Haltern/Verbindern/Endstücken/Fallrohranschlüssen;
- für kleine bis mittlere Dachentwässerung geeignet;
- keine Metallrinne.

Ausgeschlossen bzw. separate Klassen:
- Titanzink-/Aluminium-/Kupferrinne;
- Kastenrinne;
- RG 75/125/150 als konkrete andere Größenklasse;
- Regenkette;
- Dachrinne eines Weidezelts als proprietäres Zwischenzelt-Zubehör ohne allgemeine RG100-Systemklasse;
- Fallrohr allein;
- Rinnenhalter allein.

Der Registry-Einsatzort `Unterstand` ist eine Anwendung; die hydraulische Eignung muss nach Dachgrundfläche und Systemdimensionierung geprüft werden. Keine pauschale Passform für jeden Unterstand.

### Aktuelle Hersteller-Evidence

Marley Deutschland GmbH:
- `Dachrinne halbrund`;
- schlagzäher, cadmiumfreier Kunststoff;
- halbrundes System;
- RG 100 verfügbar;
- Verbindungsschale mit Nocke-Nut-System;
- verschiedene Rinnenhalter/Rinneneisen;
- passende Systemkomponenten;
- Hersteller führt das System u. a. für Carports/Garagen und Dachentwässerung.

Herstellerquellen:
https://marley.de/products/dachrinne-halbrund
https://marley.de/collections/halbrunde-dachrinnen

SAREI Haus- und Dachtechnik GmbH:
- `Dachrinne aus Kunststoff halbrund` / RG 100;
- PVC;
- Länge 2,0 m laut Produktdatenblatt der Kunststoffvariante;
- RG 100;
- passender Rinneneinhangstutzen/Fallrohr;
- Produktdatenblatt nennt RG100 bis 60 m² Dachgrundfläche für die dort definierte Systemkonfiguration;
- Rinnenverbinder, Rinnenträger und Endstücke als Systemkomponenten.

Herstellerquellen:
https://www.sarei.de/produkte/halbrundrinne/
https://www.sarei.de/wp-content/uploads/2025/02/Produktdatenblatt_Dachrinne_PVC_halbrund.pdf

### Faktenmatrix V1

1. `gutter_class`;
2. `shape_class`;
3. `material`;
4. `nominal_gutter_size_rg`;
5. `development_width_mm`;
6. `approx_diameter_mm`;
7. `section_length_mm`;
8. `available_lengths_mm`;
9. `connection_system`;
10. `seal_type`;
11. `holder_spacing_mm`;
12. `recommended_slope_mm_per_10m`;
13. `compatible_downpipe_dn`;
14. `roof_area_claim_m2`;
15. `roof_area_claim_conditions`;
16. `available_colors`;
17. `uv_resistance_claim`;
18. `temperature_expansion_design`;
19. `standard_or_norm`;
20. `warranty`.

Dachflächenangaben dürfen nur mit identischer System-/Fallrohr-/Niederschlagsdefinition direkt verglichen werden. Sonst bleiben sie Herstellerclaims.

### Pairing-Regeln

- gleiche Gruppe `dachrinnen-am-unterstand`;
- `gutter_class = HALF_ROUND_PLASTIC_GUTTER`;
- `nominal_gutter_size_rg = 100`;
- Systemkomponenten vorhanden;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Länge/Farbe sind Varianten. Konkrete 2-m-gegen-2-m-Paarung darf erst erfolgen, wenn die Marley-Längenvariante im Product Knowledge konkret gebunden ist. Keine stillen Systemteil-Kombinationen über Herstellergrenzen.

### Decision-Policy

- Klasse/Form/RG/Materialgruppe: `PAIRING_EQUAL_NO_PREFERENCE`;
- Länge, Verbindung, Halter, Fallrohr, Farben und Systemdetails: sachliche Unterschiede;
- keine freie Aussage zu Dichtheit, Haltbarkeit, UV-Beständigkeit, Montagefreundlichkeit oder hydraulischer Leistung;
- Dachgrundfläche nur mit gleicher Berechnungs-/Systembedingung vergleichen;
- keine Cross-Brand-Kompatibilität von Verbindern/Haltern/Fallrohren erfinden.

## Globale Verbote für alle drei Gruppen

- `mobile-unterstaende` nicht mit `weidezelt` duplizieren;
- Kufen-/Räder-/Größenkonfiguration vor realem Paar binden;
- Windschutznetz nicht mit geschlossener Plane verwechseln;
- Dachrinnenteile verschiedener Hersteller nicht als kompatibel behaupten;
- kein Gesamtsieger;
- keine Punkte/Sterne/Rankings;
- keine Shop-/Affiliate-Verfügbarkeit als Fachargument;
- keine Tierwohl-, Gesundheits-, Baurechts-, Standsicherheits-, Wetter-, Haltbarkeits- oder Hydraulikwertung ohne direkt vergleichbare Evidenz;
- Quellenlücke bleibt `NOT_IN_SOURCE`.

## Produktvalidierung gegen die Profilspec

Fresh source-bound Gegenprüfung 2026-09-11:

- `mobile-unterstaende`: Ferox mobile Weidehütte + Wördekemper Mobilstall/Weidehütte belegen zwei unabhängige starre, versetzbare Pferdeunterstandfamilien. Konkrete Kufen-/Front-/Größenkonfiguration bleibt Pflicht; Weidezelte sind ausgeschlossen;
- `windschutz-fuer-pferde`: Kerbl 442645/442646 + HAAS Agriflex N100/N200 belegen zwei unabhängige luftdurchlässige Windschutznetzfamilien mit Pferde-/Stall-/Unterstandsnutzung;
- `dachrinnen-am-unterstand`: Marley halbrunde Kunststoffrinne RG100 + SAREI halbrunde Kunststoff-/PVC-Rinne RG100 belegen zwei unabhängige RG100-Kunststoff-Dachrinnensysteme.

Das ist keine finale Paarfreigabe und keine Markt-Vollständigkeit.

## Technische Materialisierungsgrenze

Dieses Dokument ändert `comparison-profiles.json` nicht.

Die Spezifikationen aus Akten 62–77 bleiben source-bound gesammelt. Vor technischer Materialisierung muss Product Knowledge pro Produkt/Variante die Klassenbindung und Pflichtfakten tragen.

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
