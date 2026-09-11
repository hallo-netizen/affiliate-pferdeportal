# PRODUKTVERGLEICH – PROFILE / FACT MATRIX LIEGEFLÄCHEN / OFFENSTALL-BODENBEFESTIGUNG / FRESSSTÄNDER V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Drei Registry-Gruppen bleiben fachlich getrennt:
- `liegeflaechen-im-offenstall`;
- `offenstall-bodenbefestigung`;
- `fressstaender-im-offenstall`.

Keine Standort-Synonyme erfinden:
- Liegefläche = fertiger Stall-/Liegebelag für den unmittelbaren Pferdebereich;
- Bodenbefestigung = tragendes/lastverteilendes Flächenbefestigungssystem für Auslauf/Paddock/Wege;
- Fressständer = räumlich abgegrenzter individueller Fressplatz in Gruppenhaltung.

Fressgitter, Fresszaun, Raufe, Liege-/Boxenmatte und Bodenraster bleiben getrennte Funktionsklassen.
Finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin aus aktuellem Product Knowledge.

---

## 1. Liegeflächen im Offenstall

Portal-Key:
`liegeflaechen-im-offenstall`

Technischer Key:
`liegeflaechen-im-offenstall`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound V1-Klasse:
`RUBBER_STALL_MAT_FOR_OPEN_STABLE_LYING_AREA`.

Pflichtmerkmale:
- Gummi-/Elastomer-Stallmatte;
- vom Hersteller ausdrücklich für Pferdestall und Liegefläche bzw. Offenstall geeignet;
- flächiger fertiger Oberbelag;
- keine primäre Funktion als tragendes Bodenraster/Paddockplatte.

Ausgeschlossen bzw. separate Klassen:
- Paddock-/Bodenraster und Flächenbefestigungsplatten -> `offenstall-bodenbefestigung`;
- reine Stallgassen-/Waschplatzmatte ohne Liege-/Offenstallfreigabe;
- Schaum-/Matratzensystem mit anderer Konstruktionsklasse;
- Einstreu selbst;
- Drainageunterbau;
- Boxenboden-/Bauleistung ohne konkretes Produkt.

### Aktuelle Hersteller-Evidence

Gummiwerk KRAIBURG Elastik GmbH & Co. KG / BELMONDO:
- `BELMONDO Basic`;
- Hersteller nennt ausdrücklich `Box` und `Liegefläche`, inklusive Beispiel Offenstall;
- vulkanisierte Gummimatte;
- 18 mm Stärke;
- 1 x 1 m;
- vierseitige Puzzleverbindung;
- Hufeisenprofil auf der Oberseite;
- schwimmende Verlegung auf befestigtem Untergrund.

Herstellerquellen:
https://kraiburg-belmondo.de/produkte/stallmatten-fuer-box-und-liegeflaeche/belmondo-basic/
https://kraiburg-belmondo.de/produkte/stallmatten-fuer-box-und-liegeflaeche/belmondo-basic/technische-daten/

MRH Mülsen GmbH / sagu® matting:
- `Stallmatte 960 × 1.900 × 20 mm Puzzle`;
- Gummimatte mit Puzzle-Kante;
- 960 x 1900 mm;
- 20 mm;
- Hersteller nennt ausdrücklich Pferdeboxen, Offenställe und Laufställe als Einsatzgebiete;
- Hersteller nennt die 20-mm-Ausführung ausdrücklich auch für den Außenbereich.

Herstellerquellen:
https://www.sagu-muelsen.de/sagu-matting-stallmatten/stallmatten-960-1900-20-puzzle.html
https://www.sagu-muelsen.de/stallmatten.html

### Faktenmatrix V1

1. `flooring_class`;
2. `horse_use_scope`;
3. `open_stable_use`;
4. `material`;
5. `thickness_mm`;
6. `width_mm`;
7. `length_mm`;
8. `connection_system`;
9. `surface_profile`;
10. `underside_profile`;
11. `installation_substrate_requirement`;
12. `installation_method`;
13. `vehicle_traffic_claim`;
14. `liquid_absorption_or_drainage_design`;
15. `manufacturer_grip_cushioning_insulation_claims`;
16. `care`;
17. `warranty`.

Nicht veröffentlichte Shore-Härte, Stoßdämpfungswerte, Reibbeiwerte, Wärmedurchgangswerte oder Nutzungsdauer bleiben `NOT_IN_SOURCE`.

### Pairing-Regeln

- gleiche Gruppe `liegeflaechen-im-offenstall`;
- `flooring_class = RUBBER_STALL_MAT_FOR_OPEN_STABLE_LYING_AREA`;
- offene Stall-/Liegeflächeneignung source-bound vorhanden;
- keine Bodenraster-/Paddockplattenklasse;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Unterschiedliche Stärke, Puzzleformat, Oberflächenprofil und Montagevorgaben sind Vergleichsfakten, solange die Kernnutzung als Gummi-Stall-/Liegeflächenbelag gleich bleibt.

### Decision-Policy

- Klasse/Nutzung: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Stärke, Verbindung, Profile und Montage: sachliche Unterschiede;
- Trittsicherheit, Weichheit, Dämmung, Gelenkschonung, Hygiene, Einstreueinsparung oder Haltbarkeit nur als Herstellerclaim bzw. mit direkt vergleichbarer Prüfevidenz;
- keine freie Tierwohl-/Gesundheitsüberlegenheit ableiten;
- keine Aussage, dass ein Belag ohne Einstreu oder unabhängig vom Untergrund geeignet ist, wenn der Hersteller dies nicht belegt.

---

## 2. Offenstall-Bodenbefestigung

Portal-Key:
`offenstall-bodenbefestigung`

Technischer Key:
`offenstall-bodenbefestigung`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound V1-Klasse:
`RECYCLED_PLASTIC_PADDOCK_GROUND_REINFORCEMENT_GRID`.

Primärer Zweck:
Flächige Stabilisierung/Befestigung von Paddock, Auslauf oder vergleichbarer Bewegungsfläche durch ein lastverteilendes Kunststoff-Raster/Plattensystem.

Pflichtmerkmale:
- Kunststoff-/Recyclingkunststoff-Raster oder -Platte;
- Hersteller nennt Paddock/Auslauf oder vergleichbare Pferde-Bewegungsfläche;
- tragende/lastverteilende bzw. flächenstabilisierende Funktion;
- offene Raster-/Kammerkonstruktion oder technisch gleichartige Bodenbefestigungsplatte.

Ausgeschlossen bzw. separate Klassen:
- Gummi-Liegematte/Stallmatte;
- reine Tretschicht/Sand/Mineralgemisch;
- Betonstein/Pflaster ohne gleiche Systemklasse;
- reine Drainagematte ohne Flächenbefestigungsfunktion;
- Reitplatz-Komplettbau als Service;
- nur für Boxeninnenraum gedachter Belag.

### Aktuelle Hersteller-Evidence

HIT Hinrichs Innovation + Technik GmbH:
- `HIT-Bodenraster UNIVERSAL PLUS`;
- 60 x 40 x 5,5 cm;
- Querentwässerung;
- dauerelastisches, schlagzähes PE-Recyclingmaterial;
- Einsatzbereiche laut Hersteller u. a. Paddocks, Ausläufe, Rundläufe, Reitplätze und weitere Flächenbefestigungen;
- im empfohlenen Einbauzustand befahrbar mit gängigen Schleppern/Geräten.

Herstellerquelle:
https://aktivstall.de/wp-content/uploads/2018/09/HIT-FAQs-Bodenraster.pdf

HÜBNER-LEE GmbH & Co. KG:
- `TTE MultiDrainPLUS`;
- ca. 80 x 40 x 6 cm;
- 32 Kammern;
- 100 % Recyclingkunststoff;
- ca. 8,7 kg/Stück bzw. 27 kg/m² nach aktueller Produktseite;
- robuste horizontale/vertikale Verzahnung;
- Anwendungen u. a. Paddocks/Ausläufe;
- Produktseite beschreibt flächige Lastverteilung durch das Verbundsystem.

Herstellerquellen:
https://www.huebner-lee.de/index_reitsport.html
https://www.huebner-lee.de/fileadmin/user_upload/dokumente/Downloads/DE/3_Reitsport_und_Tierhaltung/Pferde/Infoblaetter/TTE-Pferde-MultiDrain-Plus-Ergaenzung.pdf

### Faktenmatrix V1

1. `ground_reinforcement_class`;
2. `horse_use_scope`;
3. `paddock_run_use`;
4. `material`;
5. `recycled_content_claim`;
6. `module_width_mm`;
7. `module_length_mm`;
8. `module_height_mm`;
9. `module_weight_kg`;
10. `weight_kg_m2`;
11. `chamber_count_or_open_area`;
12. `connection_system`;
13. `surface_profile`;
14. `drainage_design`;
15. `subbase_requirement`;
16. `fill_or_surface_layer_requirement`;
17. `vehicle_traffic_claim`;
18. `static_load_test_or_claim`;
19. `slope_limit_claim`;
20. `manufacturer_load_distribution_drainage_claims`;
21. `warranty`.

Mess-/Prüfwerte werden nur übernommen, wenn Quelle, Prüfkörper und Bedingungen mitgeführt werden. Keine stillen Gleichsetzungen unterschiedlicher Belastbarkeitstests.

### Pairing-Regeln

- gleiche Gruppe `offenstall-bodenbefestigung`;
- `ground_reinforcement_class = RECYCLED_PLASTIC_PADDOCK_GROUND_REINFORCEMENT_GRID`;
- Paddock-/Auslauf-/Pferdeflächen-Einsatz source-bound;
- gleiche Grundmechanik als lastverteilendes Raster-/Plattensystem;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Abweichender Einbauaufbau, Rasterhöhe, Kammergeometrie oder Füllung sind Vergleichsfakten. Ein Produkt wird nicht allein deshalb ausgeschlossen, weil ein Hersteller einen Unterbau empfiehlt und der andere eine spezielle On-Top-/Direktbauweise anbietet; diese Bauweisen müssen aber sichtbar getrennt dargestellt werden.

### Decision-Policy

- Klasse/Nutzung: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Gewicht, Kammern, Verbindung, Material und Drainage: sachliche Unterschiede;
- Tragfähigkeit nur innerhalb identischer oder sauber erklärter Testbedingungen vergleichen;
- keine freie Aussage zu Matschfreiheit, Gelenkschonung, Rutschfestigkeit, Lebensdauer, Nachhaltigkeit oder Wartungsaufwand;
- Herstellerclaims und Zertifikate getrennt von direkt vergleichbaren Zahlenwerten behandeln;
- kein pauschaler Sieger aus höherer statischer Laborlast ableiten.

---

## 3. Fressständer im Offenstall

Portal-Key:
`fressstaender-im-offenstall`

Technischer Key:
`fressstaender-im-offenstall`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Gebundene V1-Klasse:
`STATIONARY_INDIVIDUAL_GROUP_FEEDING_STAND`.

Fachbindung aus Akte 51 bleibt zwingend:
Fressstand/Fressständer = individueller Fressplatz mit räumlicher seitlicher Abgrenzung in Gruppenhaltung.

Pflichtmerkmale:
- für Gruppenhaltung;
- ein individueller Fressplatz je Stand/Segment;
- seitliche Abtrennung/Trennwand;
- stationäre Bauklasse für die erste V1-Paarung;
- Hersteller nennt Fress-/Futterstand und konkrete Standkonstruktion.

Ausgeschlossen bzw. separate Klassen:
- bloßes Fressgitter;
- bloßer Fresszaun;
- Heuraufe/Raufe;
- automatisierte Futterstation mit Zugangserkennung als andere Systemklasse;
- schwenkbarer Fressstand gegen stationären Fressstand;
- einzelne Trennwand ohne vollständige Fressstandfunktion;
- Trog allein.

### Aktuelle Hersteller-Evidence

Sulzberger Stalleinrichtungen & Pferdeboxen:
- `Futterstand (Fressstand)`, Art.-Nr. `162060`;
- ausdrücklich für individuelle Einzelfütterung in Gruppenhaltung;
- 2,20 m hoch;
- eine Trennwand, 3,00 m lang, kompletter Rahmen;
- Holzfüllung horizontal vorgesehen;
- zwei abgebogene Bruststangen;
- drei Oberrohre;
- ergänzende Douglasienholzfüllung Art. 162062 mit geschlossenem unteren Bereich und Sehschlitzen im oberen Bereich.

Herstellerquelle:
https://www.sulzberger.de/futterstaende/futterstaende

HAU GmbH & Co. KG:
- Produktfamilie `Fressstände feststehend` wird im aktuellen Herstellerprogramm getrennt von `Fressstände schwenkbar` geführt;
- feststehender HAU-Fressstand Art. `P.FSV1000A` ist im Handel mit Herstellerangaben dokumentiert;
- ca. 235 cm hoch, 300 cm lang, Achsmaß/Standbreite 80 cm;
- feuerverzinkter Stahl;
- Douglasienholzfüllung mit Sehschlitzen;
- zwei verstellbare Brustrohre;
- für Rau- und Kraftfutter in Gruppenhaltung;
- Futtertröge separat.

Hersteller-/Direktquellen:
https://hau-pferdesport.de/produkte/fuetterungstechnik/raufutter/
https://www.stallbedarf24.de/hau-fressstaender-fuer-pferde/

### Faktenmatrix V1

1. `feeding_stand_class`;
2. `housing_use`;
3. `mobility_class`;
4. `feeding_place_count`;
5. `height_mm`;
6. `length_mm`;
7. `stand_width_mm`;
8. `frame_material`;
9. `surface_finish`;
10. `partition_material`;
11. `partition_closed_height_mm`;
12. `visual_slot_design`;
13. `chest_bar_count`;
14. `chest_bar_adjustable`;
15. `chest_bar_shape`;
16. `rear_closure_available_or_included`;
17. `trough_included`;
18. `roughage_use`;
19. `concentrate_use`;
20. `manufacturer_feeding_behavior_or_safety_claims`;
21. `installation_requirements`;
22. `warranty`.

Nicht veröffentlichte Belastbarkeit, Mindestabstände, Sicherheitszertifizierung oder Pferdezahlkapazität bleiben `NOT_IN_SOURCE`.

### Pairing-Regeln

- gleiche Gruppe `fressstaender-im-offenstall`;
- `feeding_stand_class = STATIONARY_INDIVIDUAL_GROUP_FEEDING_STAND`;
- `mobility_class = STATIONARY`;
- Gruppenhaltungsnutzung source-bound;
- individueller räumlich abgegrenzter Fressplatz;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Stationär gegen schwenkbar bleibt ausgeschlossen. Fressgitter/Fresszaun werden nicht wegen ähnlichem Einsatzzweck eingeschleust.

### Decision-Policy

- Klasse/Mobilität/Nutzung: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Material, Wand-/Sehschlitzbau, Brustrohre, Trog- und Verschlussumfang: sachliche Unterschiede;
- keine freie Aussage zu Futterneid, Stressreduktion, Pferdesicherheit, Verletzungsrisiko oder Fresskomfort;
- Herstellerclaims zur Fressposition oder Gruppenfütterung nur als Herstellerclaim;
- keine bauliche Eignung für einen konkreten Stall aus Produktdaten ableiten.

## Globale Verbote für alle drei Gruppen

- Liegeflächenbelag nicht mit Bodenbefestigungsraster mischen;
- Bodenbefestigung nicht mit Reitplatz-Komplettbau oder bloßer Tretschicht mischen;
- Fressstand nicht mit Fressgitter/Fresszaun/Raufe verwechseln;
- kein Gesamtsieger;
- keine Punkte/Sterne/Rankings;
- keine Shop-/Affiliate-Verfügbarkeit als Fachargument;
- keine Gesundheits-, Sicherheits-, Tierwohl-, Haltbarkeits- oder Nachhaltigkeitswertung ohne direkt gebundene Evidenz;
- keine Produktidentität aus ähnlicher Bezeichnung erfinden;
- Quellenlücke bleibt `NOT_IN_SOURCE`.

## Produktvalidierung gegen die Profilspec

Fresh source-bound Gegenprüfung 2026-09-11:

- `liegeflaechen-im-offenstall`: BELMONDO Basic + sagu® matting Stallmatte 960 × 1900 × 20 mm belegen zwei unabhängige Gummi-Stallmattenfamilien mit ausdrücklich belegter Offenstall-/Liegeflächen- bzw. Offenstallnutzung;
- `offenstall-bodenbefestigung`: HIT-Bodenraster UNIVERSAL PLUS + HÜBNER-LEE TTE MultiDrainPLUS belegen zwei unabhängige Recyclingkunststoff-Raster-/Paddockplattensysteme für Paddock/Auslauf-Flächenbefestigung;
- `fressstaender-im-offenstall`: Sulzberger 162060 + HAU feststehender Fressstand belegen zwei unabhängige stationäre, räumlich abgegrenzte Fressstandfamilien für Gruppenhaltung.

Das ist keine finale Paarfreigabe, keine Markt-Vollständigkeit und keine Aussage, dass jede konkrete Variante pairable ist.

## Technische Materialisierungsgrenze

Dieses Dokument ändert `comparison-profiles.json` nicht.

Die Spezifikationen aus Akten 62–70 bleiben source-bound gesammelt. Vor technischer Materialisierung muss Product Knowledge pro konkretem Produkt/Variante die erforderliche Klassenbindung und Fakten source-bound tragen.

Erst dann darf das Plugin aus aktuellem Product Knowledge alle fachlich zulässigen Cross-Brand-Paare berechnen und regelmäßig neu bewerten.

Noch nicht behauptet:
- Product Knowledge vollständig;
- Markt vollständig;
- Pairing-Ready im technischen System;
- konkrete A-vs-B-Paarfreigabe;
- SEO-PASS;
- Pluginmaterialisierung.

Kein Merge.
Kein Publish.
