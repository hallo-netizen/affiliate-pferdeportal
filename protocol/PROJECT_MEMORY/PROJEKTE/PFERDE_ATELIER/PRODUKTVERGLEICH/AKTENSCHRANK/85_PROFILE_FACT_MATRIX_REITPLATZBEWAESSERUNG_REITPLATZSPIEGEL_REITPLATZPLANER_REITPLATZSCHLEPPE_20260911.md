# PRODUKTVERGLEICH – PROFILE / FACT MATRIX REITPLATZBEWÄSSERUNG / REITPLATZSPIEGEL / REITPLATZPLANER / REITPLATZSCHLEPPE V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Autoritative Registry-Folge hinter Akte 84:
- `p163 reitplatzbewaesserung`;
- `p164 reitplatzspiegel`;
- `p165 reitplatzplaner`;
- `p166 reitplatzschleppe`;
- `p167 bahnplaner` = gemäß finaler 175er Disposition `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`;
- `p168 sandverteiler` = gemäß finaler 175er Disposition `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`;
- `p169 hufschlagraeumer`;
- `p170 reitplatzbewaesserung-mobil`.

Damit gilt zwingend:
- `reitplatzbewaesserung` wird in V1 als **fest installierte Reitplatzberegnung** profiliert;
- mobile Bewässerungswagen/Beregnungstrommeln gehören ausschließlich in `reitplatzbewaesserung-mobil` und dürfen p163 nicht duplizieren;
- `reitplatzplaner` und `reitplatzschleppe` werden nicht anhand der Händlerbezeichnung, sondern anhand ihrer realen mechanischen Bau-/Arbeitsklasse getrennt;
- `bahnplaner` wird nicht als Synonym reaktiviert, sondern bleibt V1-NOT-APPLICABLE;
- finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin aus aktuellem Product Knowledge.

---

## 1. Reitplatzbewässerung

Portal-Key / technischer Key:
`reitplatzbewaesserung`

Vergleichstyp:
`PRODUCT_SYSTEM`

### Harte Produktklassengrenze

Erste source-bound V1-Klasse:
`FIXED_PROGRAMMABLE_20X40_ARENA_SPRINKLER_COMPLETE_SYSTEM`.

Pflichtmerkmale:
- fest installierte Beregnungsanlage für Reitplatz/Reithalle;
- konkrete 20 x 40 m-Konfiguration;
- Komplettsystem mit Rohr-/Leitungs- und Steuerungskomponenten;
- mindestens sechs definierte Regnerpositionen;
- programmierbare elektrische/elektronische Steuerung;
- Wasserbedarf und erforderlicher Fließdruck source-bound;
- keine mobile Beregnungseinheit.

Ausgeschlossen bzw. separate Klassen:
- mobile Bewässerungswagen, Schlauchregner, Beregnungstrommeln -> `reitplatzbewaesserung-mobil`;
- einzelner Regner ohne Anlagenkonfiguration;
- Pumpe allein;
- Ebbe-Flut-/Unterflurbodensysteme;
- reine Planungs-/Montagedienstleistung;
- allgemeine Garten-/Sportplatzanlage ohne gebundene Reitplatzkonfiguration.

### Aktuelle Hersteller-/Anbieter-Evidence

Ridcon GmbH – `Wetman Station 2.0 FLEX Paket 1`:
- Komplettset für 20 x 40 m Reithalle/Reitplatz;
- sechs Beregner;
- zwei Leitungssegmente;
- ca. 2,4 m³/h verfügbare Wassermenge bei 3,5 bar;
- Steuercomputer, manuell oder smart programmierbar;
- Winterentleerung per Druckluftanschluss;
- Rohr-/Schlauch-, Steuerleitungs- und Montagekomponenten im Set.

Herstellerquellen:
https://www.ridcon.de/reitplatzberegnung-und-reithallenberegnung/
https://shop.ridcon.de/products/wetman-station-2-0-flex-paket-1-fur-20x40m-2-4m-wasser

aquatechnik – `Reitplatzbewässerungsset CLASSIC 40 x 20 m, 6 Regner, elektrisch`:
- konkrete 40 x 20 m Reitplatzanlage;
- sechs PGP-ADJ-Getrieberegner;
- elektrische programmierbare Steuerung;
- Varianten mit zwei bzw. sechs Stationen;
- 3,0 bar Fließdruck am Regner;
- PE-Rohr, Ventil-/Steuerungs- und Montagekomponenten als Komplettset;
- bei ST6-E sechs einzeln ansteuerbare Stationen; bei ST2-E zwei Stationen mit drei gleichzeitig laufenden Regnern.

Hersteller-/Produktquellen:
https://www.aquatechnik.com/produktwelten/beregnungsanlagen/reitplatz
https://www.aqua-technik-shop.de/reitplatz-classic-40x20-m-6-regner-elektr-einzelsteuerung-114-m-bei-30-bar-fliessdruck-rp4020-pp-st6-e.html
https://www.aqua-technik-shop.de/reitplatz-classic-40x20-m-6-regner-elektr-steuerung-342-m-bei-30-bar-fliessdruck-rp4020-pp-st2-e.html

### Faktenmatrix V1

1. `irrigation_system_class`;
2. `fixed_or_mobile`;
3. `arena_use`;
4. `arena_length_m`;
5. `arena_width_m`;
6. `sprinkler_count`;
7. `sprinkler_model_or_class`;
8. `station_count`;
9. `simultaneous_sprinkler_count`;
10. `required_flow_m3_h`;
11. `required_flow_pressure_bar`;
12. `sprinkler_flow_m3_h`;
13. `sprinkler_pressure_bar`;
14. `throw_range_m`;
15. `sector_range_deg`;
16. `controller_model_or_class`;
17. `program_count`;
18. `remote_control_class`;
19. `valve_class`;
20. `main_pipe_material`;
21. `main_pipe_diameter_mm`;
22. `pipe_length_m`;
23. `control_cable_length_m`;
24. `winter_drainage_class`;
25. `self_installation_supported`;
26. `complete_set_scope`;
27. `current_lifecycle`.

### Pairing-Regeln

- gleiche Gruppe `reitplatzbewaesserung`;
- `fixed_or_mobile = FIXED`;
- 20 x 40 m gegen 20 x 40 m;
- sechs Regner gegen sechs Regner;
- programmierbare automatische Steuerung;
- konkrete Station-/Parallelbetriebsstrategie muss beidseitig gebunden sein;
- erforderlicher Wasserstrom **immer zusammen mit Fließdruck** vergleichen;
- unterschiedliche Hersteller-/Anbieterfamilien;
- aktueller pairable Lifecycle.

**Fail-closed:**
Ridcon Wetman Station 2.0 FLEX Paket 1 und aquatechnik CLASSIC 40 x 20 m belegen dieselbe feste 20x40-Komplettsystemklasse. Ein konkretes Ranking/Paar wird aber erst freigegeben, wenn Stationenzahl, gleichzeitig laufende Regner, Regner-/Düsenkonfiguration, Wasserbedarf und Druckbezug auf derselben Mess-/Betriebsebene normalisiert sind. `2,4 m³/h bei 3,5 bar` darf nicht blind gegen einen aquatechnik-Wert verglichen werden, dessen Angabe je Regner, je Station oder Gesamtbetrieb betrifft.

### Decision-Policy

- Flächengröße/feste Anlagenklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Wasser-/Druckbedarf, Stationenzahl, Parallelbetrieb, Steuerung, Winterentleerung und Setumfang: sachliche Unterschiede;
- keine freie Behauptung zu Wasserersparnis, Staubreduktion, Trittsicherheit oder Gleichmäßigkeit ohne gleiche Messmethode;
- keine mobile Anlage in diese Gruppe ziehen.

---

## 2. Reitplatzspiegel

Portal-Key / technischer Key:
`reitplatzspiegel`

Vergleichstyp:
`PRODUCT_SYSTEM`

### Harte Produktklassengrenze

Erste source-bound V1-Oberklasse:
`FIXED_SAFETY_RIDING_MIRROR_SYSTEM_FOR_OUTDOOR_ARENA`.

Pflichtmerkmale:
- Spiegel-/Spiegelsystem ausdrücklich für Außenreitplatz geeignet;
- fest montiert oder über dafür vorgesehenes freistehendes System montierbar;
- sicherheitsrelevanter Spiegelaufbau source-bound;
- Außen-/Witterungseignung source-bound;
- Abmessungen und Montageart für konkretes Pairing gebunden.

Ausgeschlossen bzw. separate Klassen:
- einfacher Wohn-/Werkstattspiegel;
- reiner Indoor-Reithallenspiegel ohne belegte Außeneignung;
- mobile/rollbare Spiegelanlage;
- einzelne allgemeine Spiegelplatte ohne gebundenes Reitplatz-Montagesystem, sofern das konkrete Pairing ein Komplettsystem voraussetzt;
- bloße Herstellerclaims ohne identifizierbare Produkt-/Systemfamilie.

### Aktuelle Hersteller-Evidence

FOSK Mirrors – Außenreitplatz-/EasyFix-Supersafe-Systeme:
- direkt vom Hersteller für Außenreitplätze angeboten;
- wetter-, wind- und UV-beständige Außenlösungen;
- FOSK Supersafe-Spiegelelemente;
- Außenformate u. a. 160 cm, 295 cm und 410 cm;
- feste Unterkonstruktion oder sturmfestes Stahlgestell je Situation;
- mehrere Sicherheits-/Spiegelaufbauten, darunter Easy Fix Supersafe.

Herstellerquelle:
https://reithallenspiegel.de/reithallenspiegel-aussenreitplatz/

EasyMirror GmbH – Reitplatzspiegel:
- ausdrücklich für Reitplätze im Außenbereich;
- glasfreie, splitterfreie Spiegelplatten;
- wetter- und frostfest laut Hersteller;
- zuschneid-/bohrbar;
- große Formate und Spiegelbänder möglich;
- optional wetterfester Aluminiumrahmen;
- freistehend oder am Bestand montierbar.

Herstellerquelle:
https://easymirror.de/pages/reitplatzspiegel

Zusätzlicher bestehender Herstellerbeleg aus Akte 46:
Growi führt aktuelle Reithallenspiegel mit 6-mm-MIROX-Safe-Spiegelglas und mehreren Größen; Growi beschreibt Reitspiegel im aktuellen Reitplatzwissen auch für Außenbereich. Für ein konkretes Außenplatz-Pairing muss die Außeneignung jedoch am exakten Growi-Modell gebunden werden und darf nicht nur aus einer allgemeinen Blogaussage übernommen werden.

Herstellerquellen:
https://www.growi.de/stall-weidetechnik/reitplatz/reithalllenspiegel
https://www.growi.de/blog/reitplatzwissen/trainingszubehoer/

### Faktenmatrix V1

1. `riding_mirror_class`;
2. `outdoor_use_explicit`;
3. `mirror_material_class`;
4. `safety_glass_or_glass_free_class`;
5. `mirror_thickness_mm`;
6. `panel_width_mm`;
7. `panel_height_mm`;
8. `mirror_area_m2`;
9. `panel_weight_kg`;
10. `frame_material`;
11. `backing_material`;
12. `safety_film_class`;
13. `impact_absorbing_layer_class`;
14. `anti_fog_claim`;
15. `uv_resistance_claim`;
16. `frost_resistance_claim`;
17. `wind_load_or_storm_class`;
18. `fixed_wall_mount_supported`;
19. `free_standing_mount_supported`;
20. `tilt_adjustment_deg`;
21. `custom_size_supported`;
22. `safety_standard_or_certificate`;
23. `warranty_years`;
24. `current_lifecycle`.

### Pairing-Regeln

- gleiche Gruppe `reitplatzspiegel`;
- Außeneignung am konkreten Produkt/System ausdrücklich belegt;
- gleiche Nutzungsposition: Hufschlag/Bande bzw. Front-/Langseiten-Spiegel nicht frei mischen;
- Dimensionen innerhalb einer vorab definierten Größenklasse;
- Montageart gebunden;
- Spiegelmaterial darf sachlicher Unterschied sein, muss aber als `mirror_material_class` sichtbar bleiben;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

**Fail-closed:**
FOSK und EasyMirror belegen zwei aktuelle Außenreitplatz-Spiegelsystemfamilien. Ein konkretes Paar wird erst freigegeben, wenn reale Abmessungen, Montage-/Standsystem und Sicherheitsaufbau für dieselbe Nutzungsklasse gebunden sind. Glasfrei gegen Verbund-/Sicherheitsglas darf verglichen werden, aber nicht so behandelt werden, als sei der Material-/Sicherheitsaufbau identisch. Growi bleibt für Außenpairing gesperrt, solange die Außeneignung nicht am konkreten Modell source-bound ist.

### Decision-Policy

- Außen-Reitspiegel-Grundfunktion: `PAIRING_EQUAL_NO_PREFERENCE`;
- Material, Sicherheitsaufbau, Gewicht, Abmessung, Montagesystem, Zertifikat und Garantie: sachliche Unterschiede;
- keine freie Aussage zu „bruchsicherer“, „sicherer“, „verzerrungsfreier“ oder Windfestigkeit ohne vergleichbaren Test-/Normbezug;
- Herstellerclaims als Claims kennzeichnen.

---

## 3. Reitplatzplaner

Portal-Key / technischer Key:
`reitplatzplaner`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound V1-Klasse:
`MULTI_STAGE_ARENA_GROOMER_WITH_TINES_AND_TRAILING_ROLLER`.

Pflichtmerkmale:
- spezialisiertes Bodenpflegegerät für Reitplatz/Reithalle;
- aktive mechanische Bearbeitung über mindestens Zinken-/Striegelelemente;
- anschließendes Glätt-/Walz-/Planierglied;
- für Sandboden und/oder Sandboden mit Zuschlagstoffen;
- Arbeitsbreite, Zug-/Anbauart und Arbeitsorgane source-bound.

Ausgeschlossen bzw. separate Klassen:
- einfache Ring-/Wiesenschleppe ohne mehrstufige Planerarchitektur -> `reitplatzschleppe`;
- reines Nivellier-/Lasergerät;
- selbstfahrender autonomer Roboter als eigene Unterklasse;
- reine Walze;
- Hufschlagräumer allein -> `hufschlagraeumer`;
- `bahnplaner` als Registry-Key bleibt V1-NOT-APPLICABLE und wird nicht als parallele Gruppe reaktiviert.

### Aktuelle Hersteller-Evidence

floor-care / LS-Lingemann – `ONE`:
- modular konfigurierbarer Reitplatzplaner;
- Traktor-3-Punkt-Anhängung;
- Arbeitsbreiten 160, 180, 200, 220, 250 cm;
- Gewicht ab 330 kg;
- Sandboden sowie Sandboden mit Zuschlagstoffen;
- zwei Reihen Federzinken;
- federbelastetes Glätterblech;
- Gitternetzwalze mit innenliegender Förderschnecke;
- Arbeitstiefe 0 bis 9 cm einstellbar;
- unterschiedliche Walzen-/Zusatzkonfigurationen.

Herstellerquelle:
https://floorcareplaner.de/bahnplaner/one/

Alfako – `Reitplatzplaner Premium`:
- aktuelles Herstellerangebot;
- für Vlieshäcksel/Sand und weitere Reitböden;
- außen und innen;
- zwei Reihen Striegelzinken;
- Netzwalze zum Glätten;
- Hersteller-Kategorieseite beschreibt zusätzlich Krümler-/Planierfunktion und eine Arbeitsbreite von 2,25 m bei 1,30 m Tiefe für die Premium-Familie.

Herstellerquellen:
https://alfako-stallausstattung.de/reitplatzplaner-premium/
https://alfako-stallausstattung.de/Reitplatz/Reitplatzplaner

### Faktenmatrix V1

1. `arena_groomer_class`;
2. `arena_surface_class`;
3. `indoor_outdoor_use`;
4. `attachment_class`;
5. `required_towing_vehicle_class`;
6. `working_width_mm`;
7. `overall_width_mm`;
8. `overall_depth_mm`;
9. `weight_kg`;
10. `tine_row_count`;
11. `tine_class`;
12. `working_depth_min_mm`;
13. `working_depth_max_mm`;
14. `working_depth_adjustable`;
15. `levelling_blade_class`;
16. `trailing_roller_class`;
17. `roller_count`;
18. `roller_options`;
19. `edge_wheel_or_band_guard`;
20. `hoof_track_attachment_available`;
21. `third_tine_row_available`;
22. `surface_additive_support`;
23. `ce_claim`;
24. `spare_parts_support_claim`;
25. `current_lifecycle`.

### Pairing-Regeln

- gleiche Gruppe `reitplatzplaner`;
- `arena_groomer_class = MULTI_STAGE_ARENA_GROOMER_WITH_TINES_AND_TRAILING_ROLLER`;
- gleiche Bodenklasse;
- gleiche Anbau-/Zugfahrzeugklasse für ein direktes Gerätepairing;
- Arbeitsbreite in derselben Größenklasse;
- Zinken-/Walzenkonfiguration konkret gebunden;
- Optionen nicht als serienmäßige Ausstattung darstellen;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

**Fail-closed:**
floor-care ONE und Alfako Premium belegen die gemeinsame mehrstufige Reitplatzplanerklasse. Ein konkretes Pairing wird erst freigegeben, wenn Anbauart, Arbeitsbreite und konkrete Walzen-/Arbeitsorgan-Konfiguration beidseitig gebunden sind. Händler-/Herstellerbegriffe `Bahnplaner` und `Reitplatzplaner` allein entscheiden die Registry-Zuordnung nicht.

### Decision-Policy

- gleiche Boden-/Planergrundklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Arbeitsbreite, Gewicht, Arbeitstiefe, Zinken-/Walzenarchitektur, Anbauart und Optionen: sachliche Unterschiede;
- keine freie Aussage zu Bodenqualität, Verletzungsprävention, Haltbarkeit oder „besserem Reitboden“ ohne vergleichbare Prüfevidenz;
- Herstellerclaims getrennt kennzeichnen.

---

## 4. Reitplatzschleppe

Portal-Key / technischer Key:
`reitplatzschleppe`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Registry-seitig ist `reitplatzschleppe` von `reitplatzplaner` zu trennen. Erste source-bound Oberklasse:
`MECHANICAL_ARENA_DRAG_FOR_SURFACE_LEVELING`.

Die Oberklasse reicht **nicht** für ein Pairing. Pflicht-Subtypen vor einem konkreten Paar:
- `PASSIVE_RING_OR_CHAIN_DRAG`;
- `FRAME_DRAG_WITH_TINES_AND_LEVELING_BLADE`;
- weitere mechanische Bauart nur mit eigener source-bound Definition.

Pflichtmerkmale:
- physisches Schlepp-/Abziehgerät für Reitplatzboden;
- Zug-/Anbauart gebunden;
- Arbeitsbreite gebunden;
- reale Arbeitsorgane gebunden;
- keine automatische/selbstfahrende Planermaschine.

Ausgeschlossen bzw. separate Klassen:
- mehrstufiger Reitplatzplaner mit definierter Zinken-/Walzenarchitektur -> `reitplatzplaner`;
- reine Weideegge, wenn Reitplatzeignung nicht ausdrücklich belegt ist;
- Hufschlagräumer als Einzelgerät -> `hufschlagraeumer`;
- reine Walze;
- `bahnplaner` nicht als eigene V1-Gruppe reaktivieren.

### Aktuelle Produkt-Evidence

Röwer & Rüb – `Reitbahnschleppe`:
- ausdrücklich für Reitböden;
- verzinkter Rahmen;
- zwei Winkelschienen;
- gerundetes Planschild;
- Eggenrahmen mit auswechselbaren Federzinken, stufenlos höhenverstellbar;
- Bandenräumer mit Bandenrollrad;
- Arbeitsbreiten 2,00 m, 2,50 m und 3,00 m;
- für Schlepper ab 30 PS.

Herstellerquelle:
https://www.roewer-rueb.de/produkte/zubehoer/reitbahnpflege/

ATS Wollin – `Wiesenschleppe / Reitplatzschleppe`:
- ausdrücklich zum Glattziehen von Reitplätzen sowie zum Vertikutieren von Wiesen;
- Varianten 1,20 m, 1,60 m und 2,00 m;
- bei 2,00 m 103 kg, bei 1,20 m 50 kg;
- aktuelle Produkt-/Shopfamilie.

Anbieterquelle:
https://www.ats-wollin.com/Wiesenschleppe-/-Reitplatzschleppe

### Faktenmatrix V1

1. `arena_drag_class`;
2. `drag_mechanism_class`;
3. `arena_use_explicit`;
4. `secondary_meadow_use`;
5. `attachment_class`;
6. `working_width_mm`;
7. `weight_kg`;
8. `frame_material`;
9. `galvanized_claim`;
10. `tine_class`;
11. `tine_height_adjustable`;
12. `tine_replaceable`;
13. `ring_or_chain_mat_class`;
14. `levelling_blade_present`;
15. `levelling_blade_shape`;
16. `angle_bar_count`;
17. `band_edge_cleaner_present`;
18. `band_guide_wheel_present`;
19. `required_tractor_power_hp`;
20. `current_lifecycle`.

### Pairing-Regeln

- gleiche Gruppe `reitplatzschleppe`;
- `drag_mechanism_class` muss identisch sein;
- gleiche Zug-/Anbauart;
- Arbeitsbreite in derselben Größenklasse;
- gleiche Hauptfunktion am Reitplatz;
- unterschiedliche Hersteller-/Anbieterfamilien;
- aktueller pairable Lifecycle.

**Fail-closed:**
Die aktuelle Evidence belegt die Registry-Gruppe, aber noch **kein konkretes Cross-Brand-Paar**. Röwer & Rüb beschreibt eine Rahmen-Schleppe mit Federzinken und Planschild. ATS Wollin belegt eine Wiesenschleppe/Reitplatzschleppe, deren konkrete Ring-/Ketten-/Zinkenarchitektur auf der herangezogenen Produktseite nicht ausreichend technisch gebunden ist. Solange `drag_mechanism_class` nicht beidseitig identisch source-bound ist, bleibt das Paar 0.

### Decision-Policy

- identische Schleppmechanik/Nutzungsklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Arbeitsbreite, Gewicht, Zinken-/Schild-/Randräumertechnik und Fahrzeuganforderung: sachliche Unterschiede;
- keine Wiesenschleppe allein aufgrund des Namens gegen eine technisch andere Reitbahnschleppe ranken;
- keine Gleichsetzung von `Schleppe`, `Planer` und `Bahnplaner` aus Marketingbezeichnungen.

---

## Akte-85-Negativcheck

PASS:
- Registry-IDs p163–p166 direkt gegen `portal-structure-v279.json` korrigiert;
- p170 `reitplatzbewaesserung-mobil` als eigenes Dedup-Gate berücksichtigt;
- p167 `bahnplaner` und p168 `sandverteiler` bleiben V1-NOT-APPLICABLE;
- aktuelle öffentliche Produkt-/Herstellerseiten für alle vier Gruppen gegengeprüft;
- Reitplatzspiegel-Altbefund aus Akte 46 gegen aktuelle FOSK/Growi-/Marktlage gespiegelt;
- Reitplatzplaner vs. Reitplatzschleppe mechanisch statt nach Marketingnamen getrennt;
- fehlende Subtyp-/Konfigurationsgleichheit führt fail-closed zu 0 Paar;
- keine finale konkrete Paarentscheidung manuell festgeschrieben;
- keine technische Materialisierung;
- kein SEO;
- kein Writer/Draft/Publish;
- kein Codex;
- kein Merge;
- kein Publish.

OFFEN:
- technische UPC-Materialisierung dieser vier Profile;
- vollständige technische Positiv-/Negativ-/Mutation-/Fresh-ZIP-Prüfung erst nach gebündelter Materialisierung;
- WordPress-Live-Test UPC 0.8.6 unverändert offen.

## Nächster Registry-Einstieg nach Akte 85

`p167 bahnplaner` -> V1-NOT-APPLICABLE, überspringen.
`p168 sandverteiler` -> V1-NOT-APPLICABLE, überspringen.

Nächster fachlich zulässiger Block:
1. `p169 hufschlagraeumer`;
2. `p170 reitplatzbewaesserung-mobil`;
3. `p171 weidepflegegeraete`.

Keine Materialisierung in dieser Akte.