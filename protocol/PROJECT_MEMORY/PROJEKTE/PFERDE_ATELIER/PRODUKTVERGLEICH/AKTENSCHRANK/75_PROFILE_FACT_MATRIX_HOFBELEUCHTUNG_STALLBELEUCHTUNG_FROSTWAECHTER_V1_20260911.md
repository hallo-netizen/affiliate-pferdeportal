# PRODUKTVERGLEICH – PROFILE / FACT MATRIX HOFBELEUCHTUNG / STALLBELEUCHTUNG / FROSTWÄCHTER V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Registry-Gruppen:
- `hofbeleuchtung`;
- `stallbeleuchtung`;
- `frostwaechter`.

Die drei Gruppen werden nicht über den gemeinsamen Einsatzort Hof/Stall vermischt.
- Hofbeleuchtung = Außenbeleuchtung für Hof-/Zugangs-/Arbeitsflächen;
- Stallbeleuchtung = Leuchte mit source-bound Eignung für Tierstall-/landwirtschaftliche Innenumgebung;
- Frostwächter = elektrische Frostsicherung innerhalb einer exakt gebundenen Installationsklasse.

Außen-IP-Schutz ersetzt keine Stall-/Ammoniak-/D-Kennzeichen-Eignung.
Eine allgemeine Elektroheizung ersetzt keine Tierstallfreigabe.
Finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin aus aktuellem Product Knowledge.

---

## 1. Hofbeleuchtung

Portal-Key:
`hofbeleuchtung`

Technischer Key:
`hofbeleuchtung`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound Cross-Brand-V1-Klasse:
`FIXED_OUTDOOR_LED_FLOODLIGHT_100W_IP65`.

Pflichtmerkmale:
- fest montierbarer LED-Außenstrahler;
- 100 W Nennleistung;
- Schutzart IP65 ohne Bewegungsmelder;
- Wand-/Bügelmontage;
- für Außenbereich/Hof-/Zugangs-/Arbeitsflächen source-bound geeignet;
- kein mobiler Arbeitsstrahler.

Ausgeschlossen bzw. separate Klassen:
- Leuchte mit Bewegungsmelder, wenn dadurch die Schutzart/Konstruktion abweicht;
- mobile Baustellen-/Arbeitsleuchte;
- Stall-/Feuchtraum-Linearlampe;
- Hallenstrahler/High-Bay als andere Abstrahl-/Montageklasse;
- Solarleuchte;
- Straßen-/Mastleuchte;
- dekorative Fassadenleuchte mit anderer Leistungsklasse.

### Aktuelle Hersteller-Evidence

Albert Kerbl GmbH:
- `LED-Außenstrahler`, 100-W-Variante Art.-Nr. `345684`;
- 100 W;
- 8.000 lm;
- 6.000 K;
- IP65 ohne Bewegungsmelder;
- Aluminiumdruckguss;
- verstellbarer Montage-/Klemmbügel;
- 1 m Anschlusskabel;
- Hersteller nennt Ställe, Scheunen, Überdachungen und Hof als Einsatzbereiche;
- GS-geprüft.

Herstellerquellen:
https://www.kerbl.com/de/product/led-aussenstrahler/164636/104974
https://www.kerbl.com/de/produkt/led-aussenstrahler-947055

Theben AG:
- `theLeda B100 dual WH`, Art.-Nr. `1020678`;
- 100 W;
- 13.900 lm;
- 3.000/4.000 K umschaltbar;
- Außenbereich;
- Wandmontage;
- IP65 laut aktueller Produktfamilien-/Herstellerbeschreibung;
- Edelstahl-Montagebügel;
- Aluminiumkühlkörper;
- Hersteller nennt u. a. Hof, Carport, Garage, Laderampe und Hallenumfeld als Anwendungen der B-Serie.

Herstellerquellen:
https://www.theben.de/de/theleda-b100-dual-wh-1020678
https://www.theben.de/unternehmen/news/neuer-led-strahler-theleda-b-dual-robust-flexibel-einfach-montiert/

### Faktenmatrix V1

1. `lighting_class`;
2. `mounting_class`;
3. `outdoor_use`;
4. `rated_power_w`;
5. `luminous_flux_lm`;
6. `luminous_efficacy_lm_w`;
7. `color_temperature_k`;
8. `color_temperature_selectable`;
9. `cri`;
10. `beam_angle_deg`;
11. `ip_rating`;
12. `ik_rating`;
13. `housing_material`;
14. `cover_material`;
15. `mounting_bracket_material`;
16. `adjustable_angle`;
17. `motion_sensor_included`;
18. `cable_length_cm`;
19. `lifetime_l70_h`;
20. `certification`;
21. `warranty`.

Nicht veröffentlichte Beleuchtungsstärke auf einer konkreten Hoffläche, Blendungswerte, Energieverbrauch im Jahresbetrieb oder Korrosionsbeständigkeit bleiben `NOT_IN_SOURCE`.

### Pairing-Regeln

- gleiche Gruppe `hofbeleuchtung`;
- `lighting_class = FIXED_OUTDOOR_LED_FLOODLIGHT`;
- 100-W-Leistungsklasse;
- IP65 ohne Sensor-Sondervariante;
- fest montierte Bügel-/Wandklasse;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Farbtemperatur, Lichtstrom, Bügel-/Gehäusekonstruktion und Zusatzfunktionen sind Vergleichsfakten. Ein Bewegungsmelder-Modell wird nicht still gegen die sensorlose IP65-Klasse gepaart.

### Decision-Policy

- Klasse/Leistung/Schutzart/Montage: `PAIRING_EQUAL_NO_PREFERENCE`;
- Lichtstrom, Lichtausbeute, Farbtemperatur, CRI, Abstrahlwinkel, Material und Lebensdauer: sachliche Unterschiede;
- keine freie Aussage zu Blendfreiheit, Sicht-/Arbeitssicherheit, realer Energieersparnis oder Lebensdauer;
- Herstellerclaims zu Effizienz/Haltbarkeit bleiben Herstellerclaims;
- höherer Lumenwert ist kein automatischer Gesamtsieger ohne Beleuchtungsplanung.

---

## 2. Stallbeleuchtung

Portal-Key:
`stallbeleuchtung`

Technischer Key:
`stallbeleuchtung`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound Cross-Brand-V1-Klasse:
`AMMONIA_RESISTANT_IP69K_LINEAR_LED_BARN_LIGHT_40W`.

Pflichtmerkmale:
- lineare LED-Feuchtraum-/Stallleuchte;
- 40 W;
- ammoniakbeständig source-bound;
- explizite Tierstall-/landwirtschaftliche Eignung;
- IP69K;
- Hochdruckreinigung geeignet;
- PMMA-basierte Gehäuse-/Diffusorkonstruktion;
- keine reine Außenleuchte ohne Stallchemie-/Ammoniakeignung.

Ausgeschlossen bzw. separate Klassen:
- Hof-Außenstrahler ohne Ammoniakbeleg;
- Standard-IP65-Feuchtraumleuchte ohne Tierstall-/Ammoniakeignung;
- High-Bay/Hallenstrahler als andere Bauklasse;
- Infrarot-/Wärmelampe;
- 20-/60-W-Varianten als konkrete andere Leistungsklasse;
- Leuchte ohne source-bound Hochdruckreinigungs-/Stallfreigabe.

### Aktuelle Hersteller-Evidence

Fritz Göbel:
- `LED Stallleuchte Feuchtraumleuchte 40W 150cm`, Art.-Nr. `60650`;
- 40 W;
- 6.000 lm;
- 4.000 K;
- 150 lm/W;
- IP69K;
- PMMA;
- ammoniakbeständig;
- IK09;
- DLG-Zertifikat/Herstellerangabe für Landwirtschaft, Ställe, Reithallen und Scheunen;
- hochdruckreinigergeeignet;
- 1.500 mm Länge.

Herstellerquelle:
https://www.fritzgoebel.de/stallbedarf/produkte/stall-hofzubehoer/led-strahler/led-stallleuchte-feuchtraumleuchte-40w-150cm-2407.html

Albert Kerbl GmbH:
- `LED-Feuchtraumleuchte FarmTUBE`, 40-W-Variante Art.-Nr. `345641`;
- 40 W;
- 6.000 lm;
- 6.000 K;
- 150 lm/W;
- IP69K;
- PMMA-Gehäuse mit Edelstahlabdeckungen;
- ammoniakbeständig, DLG-geprüft;
- ausdrücklich für Tierställe entwickelt;
- hochdruckreinigungsgeeignet;
- D-Kennzeichen gemäß DIN EN 60598-2-24;
- 1.220 mm Länge;
- dimmbar 1–10 V;
- 5 Jahre Garantie.

Herstellerquelle:
https://www.kerbl.com/de/produkt/led-feuchtraumleuchte-farmtube-947212

### Faktenmatrix V1

1. `lighting_class`;
2. `animal_barn_use`;
3. `ammonia_resistant`;
4. `ammonia_test_or_certificate`;
5. `high_pressure_cleaning`;
6. `rated_power_w`;
7. `luminous_flux_lm`;
8. `luminous_efficacy_lm_w`;
9. `color_temperature_k`;
10. `cri`;
11. `beam_angle_deg`;
12. `ip_rating`;
13. `ik_rating`;
14. `d_mark_en_60598_2_24`;
15. `housing_material`;
16. `end_cap_material`;
17. `length_mm`;
18. `width_mm`;
19. `height_mm`;
20. `dimming_class`;
21. `through_wiring`;
22. `flicker_free_claim`;
23. `lifetime_l70_h`;
24. `included_mounting_hardware`;
25. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `stallbeleuchtung`;
- `lighting_class = LINEAR_LED_BARN_LIGHT`;
- 40-W-Klasse;
- Tierstall-/Landwirtschaftseignung source-bound;
- Ammoniakbeständigkeit source-bound;
- IP69K;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

D-Kennzeichen, Dimmung, Länge und Farbtemperatur dürfen variieren und bleiben sichtbare Vergleichsfakten. Keine Leuchte wird allein wegen IP69K als tierstallgeeignet behandelt, wenn der Ammoniak-/Stallbeleg fehlt.

### Decision-Policy

- Klasse/Leistung/Stall-/Ammoniak-/IP-Eignung: `PAIRING_EQUAL_NO_PREFERENCE`;
- Lichtstrom, Effizienz, Farbe, Abstrahlung, Maße, Dimmung, D-Kennzeichen und Garantie: sachliche Unterschiede;
- keine freie Aussage zu Tierwohl, Stress, Produktivität, Brandschutz, Wartungsaufwand oder realer Lebensdauer;
- DLG-/D-Kennzeichen exakt im veröffentlichten Prüf-/Normkontext wiedergeben;
- identische 150 lm/W sind nur ein Zahlenfakt und kein Qualitätsgesamturteil.

---

## 3. Frostwächter

Portal-Key:
`frostwaechter`

Technischer Key:
`frostwaechter`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Akte 51 bleibt bindend. Pflichttrennung:
- `NON_ANIMAL_TECHNICAL_ROOM_FROST_GUARD`;
- `ANIMAL_ZONE_STABLE_HEATER_WITH_EXPLICIT_FROST_GUARD_FUNCTION`.

Erste source-bound Cross-Brand-V1-Klasse:
`500W_WALL_MOUNTED_TECHNICAL_ROOM_FROST_GUARD_IP21`.

Pflichtmerkmale:
- elektrischer Frostwächter;
- 500 W;
- integrierter Thermostat mit Frostschutzbereich um ca. 5–15/16 °C;
- IP21;
- Wandmontage möglich;
- für Keller-, Neben-, Technik-/Geräteräume oder vergleichbare nicht-tierische Kleinräume source-bound.

**Nicht zulässig für diese V1-Klasse:**
- Tier-/Pferdestallzone;
- Heu-/Stroh-/Futtermittellager oder feuer-/explosionsgefährdete Umgebung;
- Außenbereich;
- Heizkabel/Rohrbegleitheizung;
- Tränken-/Wasserbehälterheizung;
- komplette Stallheizung;
- Frostschutzkomponente für Weidetränken;
- Komfort-Konvektor ohne primäre Frostwächterklasse.

Für eine spätere Tierzonenklasse müssen **beide** Punkte source-bound belegt sein:
1. ausdrückliche Tierstallfreigabe;
2. ausdrückliche Frostwächter-/Frostschutzfunktion.

### Aktuelle Hersteller-Evidence

ETHERMA Elektrowärme GmbH:
- `ETHERMA EFW`, Typ `EFW-500`, Art.-Nr. `36186` laut aktuellem Katalog;
- 500 W;
- 230 V;
- Thermostat 5–15 °C;
- IP21;
- Schutzklasse II;
- 1-m-Steckerleitung;
- Hersteller nennt Gäste-WC, Kellerraum, Wintergarten, Geräteschuppen und Technikraum;
- automatische Frostsicherung für kleine/unbeaufsichtigte Räume.

Herstellerquellen:
https://www.etherma.com/de/heizung/direktheizgeraete/bad-und-wohnraum/etherma-efw
https://www.etherma.com/en/heating/direct-heating/bathroom-and-living-room/etherma-efw

TECHNOTHERM / LUCHT LHZ Elektroheizungen GmbH & Co. KG:
- `TECHNOTHERM Frostwächter 500`, Bestellnummer `427000501` / FW-501-Familie;
- 500 W;
- Thermostat ca. 5–16 °C;
- IP21;
- Wandmontage;
- Schutzkontaktstecker;
- Metall-/Edelstahlgehäuse;
- Hersteller nennt kleine Nebenräume, Keller und Abstellräume bzw. Räume bis ca. 15 m³.

Herstellerquellen:
https://www.technotherm.de/p/technotherm-frostwaechter/
https://www.technotherm.de/direktheizung/frostwaechter.html

### Faktenmatrix V1

1. `frost_guard_class`;
2. `installation_zone_class`;
3. `animal_zone_approved`;
4. `fire_hazard_zone_approved`;
5. `outdoor_approved`;
6. `rated_power_w`;
7. `rated_voltage_v`;
8. `thermostat_min_c`;
9. `thermostat_max_c`;
10. `room_volume_claim_m3`;
11. `ip_rating`;
12. `protection_class`;
13. `mounting_class`;
14. `housing_material`;
15. `width_mm`;
16. `height_mm`;
17. `depth_mm`;
18. `weight_kg`;
19. `plug_type`;
20. `cable_length_m`;
21. `overheat_protection`;
22. `automatic_restart`;
23. `indicator_light`;
24. `certification`;
25. `warranty`.

Nicht veröffentlichte Raumgröße, Mindestabstände oder Eignung für Staub-/Tier-/Außenumgebung bleiben `NOT_IN_SOURCE`.

### Pairing-Regeln

- gleiche Gruppe `frostwaechter`;
- `frost_guard_class = ELECTRIC_ROOM_FROST_GUARD`;
- `installation_zone_class = NON_ANIMAL_TECHNICAL_ROOM`;
- 500 W;
- IP21;
- Wandmontage möglich;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Ein technischer Frostwächter darf nicht deshalb in einen Pferdestall gestellt oder als Stallheizung verglichen werden, weil der Registry-Key unter Stallklima liegt. Einsatzfreigabe kommt ausschließlich aus der Produktquelle.

### Decision-Policy

- Klasse/Installationszone/Leistung/IP: `PAIRING_EQUAL_NO_PREFERENCE`;
- Thermostatbereich, Maße, Gehäuse, Raumvolumenclaim, Schutzklasse und Sicherheitsfunktionen: sachliche Unterschiede;
- keine freie Aussage zu Betriebssicherheit, Energieverbrauch, Frostsicherheit eines konkreten Gebäudes, Brandrisiko oder Tierstalleignung;
- Raumvolumenclaim nur als Herstellerclaim;
- kein Einsatz in Tier-/Heu-/Strohbereich ohne ausdrückliche Freigabe.

## Globale Verbote für alle drei Gruppen

- IP65-Hofstrahler nicht automatisch als Stallleuchte behandeln;
- Stallleuchte ohne Ammoniak-/Tierstallbeleg nicht in die gebundene Stallklasse aufnehmen;
- Frostwächter für Neben-/Technikraum niemals als Tierzonen-Stallheizer umdeuten;
- elektrische Sicherheits-/Installationsfreigaben nicht aus ähnlichen Daten ableiten;
- kein Gesamtsieger;
- keine Punkte/Sterne/Rankings;
- keine Shop-/Affiliate-Verfügbarkeit als Fachargument;
- keine Sicherheits-, Brandschutz-, Tierwohl-, Haltbarkeits- oder Energieverbrauchswertung ohne direkt vergleichbare Evidenz;
- Quellenlücke bleibt `NOT_IN_SOURCE`.

## Produktvalidierung gegen die Profilspec

Fresh source-bound Gegenprüfung 2026-09-11:

- `hofbeleuchtung`: Kerbl LED-Außenstrahler 100 W + Theben theLeda B100 dual belegen zwei unabhängige fest montierbare 100-W-IP65-Außenstrahler für Hof-/Außenflächen;
- `stallbeleuchtung`: Fritz Göbel 60650 + Kerbl FarmTUBE 345641 belegen zwei unabhängige 40-W-Linearlampen mit Ammoniakbeständigkeit, Tierstall-/Landwirtschaftseignung und IP69K;
- `frostwaechter`: ETHERMA EFW-500 + TECHNOTHERM Frostwächter 500 belegen zwei unabhängige 500-W-IP21-Technik-/Nebenraum-Frostwächter. **Keine Tierstall-/Heu-/Strohfreigabe wird daraus abgeleitet.**

Das ist keine finale Paarfreigabe und keine Markt-Vollständigkeit.

## Technische Materialisierungsgrenze

Dieses Dokument ändert `comparison-profiles.json` nicht.

Die Spezifikationen aus Akten 62–75 bleiben source-bound gesammelt. Vor technischer Materialisierung muss Product Knowledge pro Produkt/Variante die Klassenbindung und Pflichtfakten tragen.

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
