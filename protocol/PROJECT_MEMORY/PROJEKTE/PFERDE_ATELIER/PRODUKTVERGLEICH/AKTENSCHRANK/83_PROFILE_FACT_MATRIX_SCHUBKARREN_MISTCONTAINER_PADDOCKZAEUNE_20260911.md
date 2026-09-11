# PRODUKTVERGLEICH – PROFILE / FACT MATRIX SCHUBKARREN / MISTCONTAINER / PADDOCKZÄUNE V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Registry-Gruppen:
- `schubkarren`;
- `mistcontainer`;
- `paddockzaeune`.

Zwischen `mistcontainer` und `paddockzaeune` liegt `mistlagerung` (p157). Dieser Key bleibt gemäß finaler 175er Disposition `PRODUCT_COMPARISON_V1_NOT_APPLICABLE` und wird bewusst nicht in V1 gezwungen.

Schubkarre = handgeführtes Einrad-Transportgerät. Mistcontainer = großvolumiges roll-/aufnehmbares Transport-/Sammelgerät. Paddockzaun = festes Zaunsystem. Diese Klassen werden nicht über Hof-/Stallnutzung vermischt.

Finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin aus aktuellem Product Knowledge.

---

## 1. Schubkarren

Portal-Key / technischer Key:
`schubkarren`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound Cross-Brand-V1-Klasse:
`ONE_WHEEL_200L_PE_STABLE_WHEELBARROW_GALVANIZED_FRAME_PNEUMATIC_TIRE`.

Pflichtmerkmale:
- handgeführte Einrad-Schubkarre/Stallkarre;
- 200 l Muldenvolumen;
- PE-/Kunststoffmulde;
- verzinkter bzw. feuerverzinkter Stahlrahmen;
- ein luftbereiftes/pneumatisches Rad;
- für Hof-/Pferdestall-/Entmistungsarbeiten source-bound;
- kein elektrischer Antrieb.

Ausgeschlossen bzw. separate Klassen:
- Zweirad-Schubkarre;
- Kippkarre/Muldenkipper;
- GFK-Mistkarre/Schweizerkarre mit zwei Rädern;
- elektrische Schubkarre;
- Futterwagen;
- 80–120-l Gartenkarre;
- Stahlblechmulde als andere Materialklasse.

### Aktuelle Evidence

YERD / Motorgeräte Fischer GmbH:
- `YERD Basics Einrad-Schubkarre 200 Liter`, Art.-Nr. 8206624;
- 200-l-PE-Tiefbettmulde;
- ein Rad;
- 32-mm-Stahlrohrrahmen, feuerverzinkt;
- Luftbereifung 4PR;
- ca. 1780 x 630 x 770 mm;
- Tragkraft 200 kg laut Herstellerseite;
- ausdrücklich zum Entmisten von Pferdeställen geeignet.

Herstellerquelle:
https://yerd.de/Einradschubkarre-200-Liter-verzinkt

ROTO SLOVENIJA d.o.o.:
- `ROTO Schubkarre TNT1 (G)`, 200-l-Variante;
- Einrad-Schubkarre;
- Kunststoffmulde;
- verzinkter Rahmen;
- pneumatisches Rad;
- 200 l;
- ca. 1550 x 760 x 760 mm;
- ausdrücklich für Hof/Pferdestall angeboten.

Direktproduktquelle:
https://www.stroeh.de/shop/Stall-Weide/Stallbedarf/Schubkarren/Roto-Schubkarre-verzinkt-200-L-Einrad

### Faktenmatrix V1

1. `wheelbarrow_class`;
2. `horse_stable_use`;
3. `wheel_count`;
4. `volume_l`;
5. `tub_material`;
6. `frame_material`;
7. `frame_finish`;
8. `frame_tube_diameter_mm`;
9. `wheel_type`;
10. `wheel_diameter_mm`;
11. `wheel_width_mm`;
12. `wheel_rim_material`;
13. `overall_length_mm`;
14. `overall_width_mm`;
15. `overall_height_mm`;
16. `empty_weight_kg`;
17. `rated_payload_kg`;
18. `tipping_bar`;
19. `handle_grip_material`;
20. `temperature_range_claim`;
21. `replacement_wheel_available`;
22. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `schubkarren`;
- `wheelbarrow_class = ONE_WHEEL_200L_PE_STABLE_WHEELBARROW_GALVANIZED_FRAME_PNEUMATIC_TIRE`;
- 200-l-Klasse;
- PE-Mulde;
- 1 Rad, Luftbereifung;
- verzinkter Stahlrahmen;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

### Decision-Policy

- Klasse/Volumen/Rad-/Mulden-/Rahmenklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Gewicht, Tragkraft, Radabmessung und Kippbügel: sachliche Unterschiede;
- Tragkraft nur bei identischer Herstellerdefinition direkt vergleichen;
- keine freie Aussage zu Wendigkeit, Ergonomie, Stabilität oder Lebensdauer;
- Zweirad- und Elektroklasse getrennt halten.

---

## 2. Mistcontainer

Portal-Key / technischer Key:
`mistcontainer`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound V1-Klasse:
`ROLLABLE_LOADER_LIFTABLE_STABLE_MIST_CONTAINER_1_5_2_0M3_1000KG_CLASS`.

Pflichtmerkmale:
- großvolumiger Mist-/Großraumcontainer für Stall/Hof;
- roll-/manövrierbar über eigene Räder;
- niedrige Einwurf-/Schüttkante für manuelle Befüllung;
- Aufnahme für Hoflader, Frontlader oder Schlepper verfügbar;
- mechanisches Transportieren/Entleeren mit Trägerfahrzeug möglich;
- Volumen ungefähr 1,5–2,0 m³ für die erste V1-Normalisierung;
- Tragkraftklasse um 1000 kg;
- kein stationärer Baukörper/Mistplatte.

Ausgeschlossen bzw. separate Klassen:
- 32-m³ Abroll-/Großcontainer für externe Entsorgung;
- bauliche Mistlagerstätte/Mistplatte -> `mistlagerung` NOT_APPLICABLE;
- 600–1100-l kleiner Mistbehälter ohne gleiche Großraumklasse;
- Muldenkipper/Kippkarre;
- Schubkarre/Mistkarre;
- rein stationärer Behälter ohne Roll-/Aufnahmefunktion.

### Aktuelle Hersteller-Evidence

GROWI / Großewinkelmann GmbH & Co. KG:
- `Großraumkuli für Hoflader`;
- Varianten ca. 1,25 bzw. 1,5 m³;
- Tragkraft 1000 kg in der aktuellen 1,5-m³-Klasse;
- luftbereifte Räder/Lenkrolle mit Feststeller;
- komplett feuerverzinkt;
- verschiedene Hoflader-/Euro-/Universal-Aufnahmen;
- für große Transportmengen auf Stall/Hof.

Herstellerquellen:
https://www.growi.de/stall-weidetechnik/transportgeraete/grossraumkulis
https://www.growi.de/stall-weidetechnik/transportgeraete/grossraumkulis/growi-grossraumkuli-hoflader-1300-lochplatte

Schwarz Transportgeräte GmbH:
- aktuelle Mistcontainer-Produktklasse für Hof/Stall;
- Tragkraft 1000 kg;
- Volumenvarianten 2000 / 2650 / 3300 l;
- rollbares Fahrwerk mit rhombischer Radanordnung und feststellbaren Lenkrädern;
- niedrige Schüttkante;
- robuste Aufnahmen für Hoflader/Schlepper gängiger Marken.

Aktueller Unternehmens-/Produktbeleg:
https://www.pferdebusiness.com/index.php/maschinen-und-fuhrpark/schwarz-transportgeraete-gmbh

KNEILMANN zusätzlicher Klassenbeleg:
- `Mist-Container` MC/MCS;
- Aufnahme zum Transportieren/Entladen mit Schlepper oder Hoflader;
- Stahl/Edelstahlvarianten;
- verschiedene Breiten und Ausführungen.

Herstellerquelle:
https://kneilmann-geraetebau.de/mist-container

### Faktenmatrix V1

1. `mist_container_class`;
2. `stable_yard_use`;
3. `volume_l`;
4. `rated_payload_kg`;
5. `container_material`;
6. `surface_finish`;
7. `overall_width_mm`;
8. `overall_depth_mm`;
9. `rear_side_height_mm`;
10. `loading_edge_height_mm`;
11. `empty_weight_kg`;
12. `wheel_count`;
13. `wheel_arrangement_class`;
14. `wheel_type`;
15. `caster_brake`;
16. `manual_push_handles`;
17. `loader_attachment_available`;
18. `loader_attachment_types`;
19. `universal_mount_plate`;
20. `front_wall_flap_available`;
21. `lid_available`;
22. `dumping_method`;
23. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `mistcontainer`;
- `mist_container_class = ROLLABLE_LOADER_LIFTABLE_STABLE_MIST_CONTAINER`;
- Volumenklasse ca. 1,5–2,0 m³ für ein konkretes Erstpaar;
- Tragkraftklasse um 1000 kg;
- rollbar und Trägerfahrzeug-Aufnahme source-bound;
- konkrete Aufnahmevariante im Product Knowledge gebunden;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

**Fail-closed:**
GROWI 1,5 m³ und Schwarz 2,0 m³ belegen die gemeinsame Großraumklasse, sind aber unterschiedliche Kapazitätsstufen. Ein konkretes Pairing ist nur zulässig, wenn der spätere Nutzer-/SEO-Intent diese Volumenbandbreite als gleiche Entscheidungsebene bestätigt; ansonsten getrennte Volumen-Subklassen.

### Decision-Policy

- Container-/Transport-/Aufnahmeklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Volumen, Tragkraft, Abmessungen, Einwurfhöhe, Räder, Material und Aufnahme: sachliche Unterschiede;
- keine freie Aussage zu Zeitersparnis, Stabilität, Sicherheit oder Wirtschaftlichkeit;
- baurechtliche/Mistlagerungs-Konformität nicht aus dem Transportcontainer ableiten;
- `mistlagerung` bleibt separater NOT_APPLICABLE-Infrastrukturkey.

---

## 3. Paddockzäune

Portal-Key / technischer Key:
`paddockzaeune`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Der Registry-Key ist ein Zaun-Oberbegriff. Pflicht-Subtyp vor Pairing.

Erste source-bound V1-Klasse:
`FIXED_PVC_VINYL_POST_AND_RAIL_HORSE_PADDOCK_FENCE_3_RAIL`.

Pflichtmerkmale:
- fest montiertes Pfosten-Riegel-Zaunsystem;
- PVC/Vinyl/Kunststoff als Hauptmaterial;
- ausdrücklich für Pferdepaddock/Pferdekoppel geeignet;
- konkrete 3-Riegel-Konfiguration für das erste V1-Paar;
- keine mobile Panelkonstruktion;
- Elektrifizierung höchstens optionale Zusatzfunktion, nicht primäre Zaunmechanik.

Ausgeschlossen bzw. separate Klassen:
- Holzzaun;
- Recyclingkunststoffzaun mit anderer Material-/Konstruktionsklasse, wenn nicht als gleiche V1-Unterklasse normalisiert;
- Elektroband-/Litze-/Seilzaun als primäres Zaunsystem;
- mobile Weide-/Paddockpanels;
- Metallrohrzaun;
- Reitplatz-Dressurumrandung mit nur einem Riegel;
- Tor als Einzelprodukt.

### Aktuelle Hersteller-Evidence

Rutjes Pferdeboxen:
- Kunststoff-Weide-/Koppelzaun ausdrücklich auch für Paddock und Reitplatz;
- lieferbar mit zwei oder drei Zaunlatten/Riegeln;
- weiß oder schwarz;
- Kunststoff-Pfosten-/Riegelsystem;
- optionale Elektrifizierung mit Isolatoren/Litze möglich.

Herstellerquellen:
https://www.rutjespferdeboxen.de/produkt-kategorie/pferdezaun/kunststoff-zaun/
https://www.rutjespferdeboxen.de/produkt/kunststoffzaun-schwarz/

COLUMBUS Professional Horse Equipment:
- `Ranch Fence`;
- hochwertiges Vinyl;
- ausdrücklich für Koppel, Paddock und Reitplatz;
- mit 2, 3 oder 4 Querteilen montierbar;
- passende Tore;
- zusätzliche Stromlitzen optional;
- Standardfarbe weiß, weitere Farben auf Anfrage.

Herstellerquelle:
https://www.columbus-de.com/de/zaunsysteme/ranch-fence/

Weitere aktuelle Klassenbelege:
- Ferox `Easy Fence` Kunststoff-Pferdezaun;
- Heritage Kunststoff-Pferdezäune;
- Poda Dallas Kunststoffzaun für Weide/Reitplatz/Paddock.

Quellen:
https://ferox-zaun.de/kunststoffzaune/
https://heritage-products.nl/de/kunststoffzaune-pferde.html
https://www.podazaun.de/zaeune-fuer-tiere/zaeune-fuer-pferde/riegelzaun-fuer-pferde/dallas-zaun/

### Faktenmatrix V1

1. `fence_subtype`;
2. `horse_paddock_use`;
3. `horse_pasture_use`;
4. `primary_material`;
5. `post_profile_class`;
6. `rail_profile_class`;
7. `rail_count`;
8. `fence_height_mm`;
9. `post_spacing_mm`;
10. `rail_length_mm`;
11. `post_dimensions_mm`;
12. `rail_dimensions_mm`;
13. `connection_system`;
14. `embedded_or_surface_mounting`;
15. `electric_fence_addon_possible`;
16. `electric_addon_included`;
17. `gate_system_available`;
18. `colors`;
19. `uv_resistance_claim`;
20. `recycled_content_claim`;
21. `warranty_years`;
22. `installation_service_available`.

### Pairing-Regeln

- gleiche Gruppe `paddockzaeune`;
- `fence_subtype = FIXED_PVC_VINYL_POST_AND_RAIL_HORSE_PADDOCK_FENCE`;
- konkrete `rail_count = 3`;
- Paddock-/Pferdenutzung source-bound;
- primäre PVC/Vinyl-Pfosten-Riegel-Konstruktion;
- unterschiedliche Herstellerfamilien;
- konkrete System-/Farb-/Riegelkonfiguration im Product Knowledge gebunden;
- aktueller pairable Lifecycle.

**Fail-closed:**
Rutjes und COLUMBUS belegen die gemeinsame konfigurierbare Systemklasse. Ein konkretes Cross-Brand-Paar wird erst freigegeben, wenn bei beiden eine konkrete 3-Riegel-Konfiguration mit ausreichend technischen Systemdaten source-bound im Product Knowledge liegt.

### Decision-Policy

- Zaun-/Material-/Riegelklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Profile, Abstände, Farben, Elektrifizierungsoption, Tore und Garantie: sachliche Unterschiede;
- keine freie Aussage zu Pferdesicherheit, Bruchsicherheit, Wartungsfreiheit, Lebensdauer oder Genehmigungsfragen;
- Herstellerclaims zu UV-/Witterungsbeständigkeit getrennt führen;
- keine Holz-, Elektro- oder Panelklasse blind gegen PVC/Vinyl-Pfosten-Riegelzaun paaren.

## Globale Negativprüfung

Muss fail-closed bleiben:
- Einrad-200-l-Schubkarre vs. Zweiradkarre;
- Einrad-Schubkarre vs. Kippkarre/Elektrokarre;
- Mistcontainer vs. Schubkarre/Mistkarre;
- Mistcontainer vs. bauliche Mistlagerung;
- 1,5-m³-Großraumkuli vs. 32-m³-Entsorgungscontainer;
- PVC/Vinyl-Paddockzaun vs. Holzzaun;
- fester Paddockzaun vs. mobile Panels;
- Pfosten-Riegel-System vs. primärer Elektroband-/Litzenzaun.

## Materialisierungsstatus

Diese Akte ist nur source-bound Fachvorarbeit.
Keine Änderung an UPC 0.8.6.
Kein Product-Knowledge-Import.
Kein SEO-/Providerlauf.
Kein Merge.
Kein Publish.
