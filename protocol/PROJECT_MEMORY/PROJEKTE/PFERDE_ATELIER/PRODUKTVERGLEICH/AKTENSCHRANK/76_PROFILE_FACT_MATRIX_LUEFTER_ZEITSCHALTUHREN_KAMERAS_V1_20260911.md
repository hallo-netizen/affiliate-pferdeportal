# PRODUKTVERGLEICH – PROFILE / FACT MATRIX LÜFTER / ZEITSCHALTUHREN / KAMERAS V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Registry-Gruppen:
- `luefter-im-stall`;
- `zeitschaltuhren-im-stall`;
- `kameras-im-stall`.

Die drei Gruppen werden nur innerhalb exakt gebundener Bau-/Nutzungsklassen gepaart.
`wasserleitungen-im-stall` wird gemäß finaler V1-Disposition zwischen Lüfter und Zeitschaltuhr bewusst übersprungen (`PRODUCT_COMPARISON_V1_NOT_APPLICABLE`).
Finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin aus aktuellem Product Knowledge.

---

## 1. Lüfter im Stall

Portal-Key:
`luefter-im-stall`

Technischer Key:
`luefter-im-stall`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound V1-Klasse:
`LARGE_DAIRY_BARN_AXIAL_CIRCULATION_FAN_130_140CM`.

Pflichtmerkmale:
- axialer Umluft-/Kühlventilator;
- ausdrücklich für Milchvieh-/Tierstall ausgelegt;
- großer Ventilatordurchmesser ca. 130–140 cm;
- stationäre Montage im Stall;
- primärer Zweck Luftzirkulation/gezielter Luftstrom im Tierbereich;
- keine reine Abluft-/Wanddurchbruchklasse.

Ausgeschlossen bzw. separate Klassen:
- Haushalts-/Werkstattventilator;
- mobiler Boden-/Standventilator;
- kleiner 40–92-cm-Korbventilator;
- Decken-Helikopter-/HVLS-Ventilator;
- reiner Abluft-/Panel-/Rohrventilator;
- Luftschlauch-/Rohrbelüftungssystem;
- Ventilator ohne source-bound Tierstall-/Landwirtschaftseignung.

Pflichtgates vor konkreter Paarfreigabe:
- `motor_class`;
- `speed_control_class`;
- `mounting_class`;
- `fan_diameter_mm`;
- konkrete Produkt-/Motorvariante.

### Aktuelle Hersteller-Evidence

Vostermans Ventilation / Multifan:
- `Multifan Korbventilator 130 cm` / Dairy Fan;
- 130 cm;
- speziell für Milchviehstall-/landwirtschaftliche Anwendung;
- max. Luftvolumen der Korbventilator-Baureihe bis 46.300 m³/h;
- Hersteller nennt 130-cm-Ausführung als Milchviehventilator;
- IP55-Motor laut Herstellerbroschüre der Dairy-Fan-Klasse;
- verschiedene Motor-/Regeltechnologien verfügbar.

Herstellerquellen:
https://www.vostermans.com/de/ventilation/axialventilatoren/korbventilatoren
https://www.vostermans.com/de/ventilation/milchvieh

Munters / Euroemme:
- `Saturn Breeze`, 55-Zoll-Klasse;
- großer Umluftventilator speziell für moderne Milchviehställe;
- bis 51.000 m³/h bei 0 Pa;
- Direct-Drive-Motor;
- E-line EC-Motor mit variabler 0–10-V-Regelung;
- korrosionsbeständige Verbundmaterialien;
- für kontinuierlichen Betrieb im Milchviehstall.

Herstellerquelle:
https://www.munters.com/de-at/produkte-cms/ventilatoren/saturn-breeze/

### Faktenmatrix V1

1. `fan_class`;
2. `animal_barn_use`;
3. `livestock_class`;
4. `fan_diameter_mm`;
5. `airflow_m3_h_at_0pa`;
6. `throw_distance_m`;
7. `motor_class`;
8. `motor_ip_rating`;
9. `motor_power_w`;
10. `speed_control_class`;
11. `control_signal`;
12. `direct_drive`;
13. `mounting_class`;
14. `minimum_mounting_height_mm`;
15. `guard_mesh_class`;
16. `housing_material`;
17. `blade_material`;
18. `corrosion_resistance_claim`;
19. `noise_db_and_distance`;
20. `energy_efficiency_claim_or_value`;
21. `ambient_temperature_range`;
22. `continuous_operation_claim`;
23. `warranty`.

Luftleistung, Wurfweite, Geräusch und Energieeffizienz dürfen nur mit identischer Mess-/Betriebsbedingung direkt verglichen werden.

### Pairing-Regeln

- gleiche Gruppe `luefter-im-stall`;
- `fan_class = LARGE_DAIRY_BARN_AXIAL_CIRCULATION_FAN`;
- Durchmesserklasse 130–140 cm;
- ausdrückliche Milchvieh-/Tierstallnutzung;
- stationäre Umluft-/Kühlfunktion;
- konkrete `motor_class` und `speed_control_class` im Product Knowledge gebunden;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

**Fail-closed:**
Die aktuellen Herstellerfamilien belegen die gemeinsame Produktklasse. Ein konkretes Vostermans-vs.-Munters-Paar wird erst freigegeben, wenn die konkrete Vostermans-Motor-/Regelvariante maschinenfest gegen eine konkrete Saturn-Breeze-Variante gebunden ist.

### Decision-Policy

- Klasse/Nutzung/Durchmesser: `PAIRING_EQUAL_NO_PREFERENCE`;
- Luftleistung, Motor, Regelung, Montage, Material und Garantie: sachliche Unterschiede;
- keine freie Aussage zu Hitzestress, Tiergesundheit, Milchleistung, Energieersparnis, Geräuschkomfort oder realer Reichweite;
- Herstellerclaims bleiben Herstellerclaims;
- keine Luftleistungswerte mit unterschiedlichen Messbedingungen zu einem Ranking verrechnen.

---

## 2. Zeitschaltuhren im Stall

Portal-Key:
`zeitschaltuhren-im-stall`

Technischer Key:
`zeitschaltuhren-im-stall`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound Cross-Brand-V1-Klasse:
`ANALOG_PLUG_IN_DAILY_TIMER_IP44_16A_15MIN`.

Pflichtmerkmale:
- analoge/mechanische Steckdosen-Zeitschaltuhr;
- 1 Kanal;
- Tagesprogramm 24 h;
- 15-Minuten-Schaltraster;
- 230 V;
- 16 A bei ohmscher Last;
- IP44;
- Schuko-Steckdosen-Zwischenstecker;
- Innen-/Außennutzung gemäß Hersteller.

Ausgeschlossen bzw. separate Klassen:
- digitale Wochenzeitschaltuhr;
- Hutschienen-/DIN-Rail-Zeitschaltuhr;
- WLAN-/Smart-Plug-/Cloud-Timer;
- astronomische Zeitschaltuhr;
- mehrkanalige Steuerung;
- 1-Minuten-Digitaltimer;
- IP20-Innenraumtimer.

Der Registry-Einsatzort Stall erzeugt **keine** Tierstall-/Ammoniak-/Feuerstaubfreigabe. Die tatsächliche Installationsumgebung muss zur Herstellerfreigabe passen.

### Aktuelle Hersteller-Evidence

Hugo Brennenstuhl GmbH & Co. KG:
- `Mechanische Zeitschaltuhr MZ 44 DE IP44`, Art.-Nr. `1506460`;
- 24-Stunden-Tagesprogramm;
- 96 Ein-/Ausschaltzeiten pro Tag;
- 15 Minuten minimaler Schaltabstand;
- 230 V;
- 16 A;
- IP44;
- innen/außen;
- Schutzabdeckung;
- Steckdose mit erhöhtem Berührungsschutz.

Herstellerquelle:
https://www.brennenstuhl.com/de-DE/produkte/zeitschaltuhren/mechanische-zeitschaltuhr-mz-44-de-ip44

Theben AG:
- `theben-timer 26 IP 44`, Art.-Nr. `0260855`;
- analoge Steckdosenschaltuhr;
- 1 Kanal;
- Tagesprogramm;
- 96 Schaltsegmente;
- 15 Minuten kürzeste Schaltzeit;
- 230 V AC / 50 Hz;
- 16 A bei cos φ = 1;
- IP44;
- Schutzklasse II;
- Schuko-Steckdosen-Zwischenstecker.

Herstellerquellen:
https://www.theben.de/de/theben-timer-26-ip-44-0260855
https://www.theben.de/produkt/0260855/datenblatt

### Faktenmatrix V1

1. `timer_class`;
2. `program_class`;
3. `channel_count`;
4. `mounting_connection_class`;
5. `rated_voltage_v`;
6. `frequency_hz`;
7. `rated_current_a_resistive`;
8. `rated_current_a_inductive`;
9. `max_switching_power_w`;
10. `led_load_w`;
11. `switching_segments_per_day`;
12. `minimum_switch_interval_min`;
13. `power_reserve`;
14. `manual_override`;
15. `switch_state_indicator`;
16. `ip_rating`;
17. `protection_class`;
18. `touch_protection`;
19. `operating_temperature_range`;
20. `housing_material`;
21. `warranty`.

Schaltleistung muss immer mit Lastart/cos φ bzw. Herstellerdefinition geführt werden. 16 A ohmsch ist nicht automatisch 16 A für induktive/LED-Lasten.

### Pairing-Regeln

- gleiche Gruppe `zeitschaltuhren-im-stall`;
- `timer_class = ANALOG_PLUG_IN_TIMER`;
- Tagesprogramm;
- 1 Kanal;
- 15-Minuten-Raster;
- IP44;
- 16 A ohmsche Last;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

### Decision-Policy

- Klasse/Programm/Kanal/IP/Schaltraster: `PAIRING_EQUAL_NO_PREFERENCE`;
- Lastangaben, Schutzklasse, Temperaturbereich und Bedienmerkmale: sachliche Unterschiede;
- keine freie Aussage zu elektrischer Sicherheit, Stallbrandrisiko, Lebensdauer oder Energieeinsparung;
- Lastarten nicht still gleichsetzen;
- keine Stall-/Feuerstaubfreigabe aus IP44 ableiten.

---

## 3. Kameras im Stall

Portal-Key:
`kameras-im-stall`

Technischer Key:
`kameras-im-stall`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound V1-Klasse:
`FIXED_FARM_PTZ_IP_CAMERA_WITH_LOCAL_STORAGE_AND_NIGHT_VISION`.

Pflichtmerkmale:
- fest installierbare IP-Überwachungskamera;
- Landwirtschaft/Hof/Tier-/Stallüberwachung source-bound;
- Pan-/Tilt- bzw. 360°-Schwenkfunktion;
- lokale Speicheroption auf microSD/SD;
- Nachtsicht;
- wetter-/staubgeschütztes Gehäuse mindestens IP65;
- Fernzugriff über Netzwerk/App.

Ausgeschlossen bzw. separate Klassen:
- mobile Akku-/4G-Kamera;
- Anhänger-/Rückfahrkamera;
- reine Innenraum-Baby-/Haustierkamera;
- starre Kamera ohne PTZ/360°;
- Kamera ohne lokale Speicheroption;
- reine Cloudkamera ohne lokale Speicherung;
- Wärmebildkamera;
- DVR-Komplettsystem als andere Systemklasse.

Pflichtfakten vor Paarung:
- `network_transport_class`;
- `power_supply_class`;
- `local_storage_class`;
- `pan_tilt_class`.

### Aktuelle Hersteller-Evidence

Albert Kerbl GmbH:
- `IPCam 360 FHD`, Art.-Nr. `10809`;
- Landwirtschaft/Pferdestall/Hofüberwachung source-bound;
- Full HD 1080, 2 MP;
- 355° horizontal / 90° vertikal;
- 5-fach optischer Zoom;
- IR-Nachtsicht bis 50 m;
- LAN/WLAN;
- Bewegungserkennung;
- microSD bis 32 GB;
- IP66;
- 12 V / 10 W;
- App-/Browser-Fernzugriff;
- ONVIF-kompatibel.

Herstellerquelle:
https://www.kerbl.com/de/produkt/ipcam-360-fhd-94495

Luda.Farm AB:
- `FarmCam Flex 360 8MP`, SKU `1141`;
- speziell für Farm-/Gehege-/Grundstücksüberwachung;
- 360°-Kamera;
- 8 MP / 3840 x 2160;
- Auto-Tracking;
- Nachtsicht bis 30 m, Farb- und IR-Nachtsicht;
- IP65;
- PoE, IEEE 802.3af, 48 V;
- 128-GB-microSD enthalten, lokal bis 256 GB;
- Zwei-Wege-Audio;
- Personen-/Fahrzeug-/Bewegungserkennung;
- App-/PC-basierter Zugriff.

Herstellerquelle:
https://www.luda.farm/de/products/farmcam-flex-360-8mp

### Faktenmatrix V1

1. `camera_class`;
2. `farm_stable_use`;
3. `pan_horizontal_deg`;
4. `tilt_vertical_deg`;
5. `video_resolution_px`;
6. `megapixels`;
7. `frame_rate_fps`;
8. `optical_zoom`;
9. `digital_zoom`;
10. `night_vision_class`;
11. `night_vision_range_m`;
12. `color_night_vision`;
13. `network_transport_class`;
14. `wifi`;
15. `lan`;
16. `poe`;
17. `power_supply_class`;
18. `local_storage_class`;
19. `included_local_storage_gb`;
20. `max_local_storage_gb`;
21. `cloud_required`;
22. `motion_detection`;
23. `person_vehicle_detection`;
24. `auto_tracking`;
25. `audio_class`;
26. `onvif`;
27. `ip_rating`;
28. `operating_temperature_range`;
29. `app_platforms`;
30. `warranty`.

Datenschutz-/Cloud-/App-Bedingungen sind Produkteigenschaften, keine pauschale Rechtsberatung. Rechtliche Zulässigkeit einer konkreten Stallüberwachung wird nicht aus dem Produkt abgeleitet.

### Pairing-Regeln

- gleiche Gruppe `kameras-im-stall`;
- `camera_class = FIXED_FARM_PTZ_IP_CAMERA`;
- Farm-/Stall-/Tierüberwachung source-bound;
- PTZ/360°;
- lokale Speicheroption;
- Nachtsicht;
- IP65 oder höher;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

LAN/WLAN versus PoE und unterschiedliche Auflösung sind Vergleichsfakten, solange beide Produkte der fest installierten Farm-PTZ-IP-Klasse angehören. Bei Suchintent `WLAN-Kamera` oder `PoE-Kamera` muss das Plugin enger normalisieren.

### Decision-Policy

- Kamera-/Installations-/PTZ-/Speicherklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Auflösung, Zoom, Nachtsicht, Netzwerk, Speicher, Audio, Erkennung und IP-Schutz: sachliche Unterschiede;
- keine freie Aussage zu Bildqualität, Erkennungszuverlässigkeit, Sicherheit, Datenschutz, Tierwohl oder Geburtsüberwachungserfolg;
- höhere MP-/Speicherzahl ist kein automatischer Gesamtsieger;
- Cloud-/Aboabhängigkeit nur source-bound darstellen;
- keine Rechtskonformität der Überwachung behaupten.

## Globale Verbote für alle drei Gruppen

- keine Haushaltsventilatoren in Tierstallklasse;
- keine Lüfterwerte ohne gleiche Messbedingungen ranken;
- keine digitale/WLAN-/Hutschienen-Zeitschaltuhr gegen analoge IP44-Steckdosenklasse;
- keine Baby-/Wohnraum-/Anhänger-/4G-Mobilkamera gegen feste Stall-PTZ-Klasse;
- keine Stall-/Brandschutzfreigabe aus IP-Werten erfinden;
- kein Gesamtsieger;
- keine Punkte/Sterne/Rankings;
- keine Shop-/Affiliate-Verfügbarkeit als Fachargument;
- keine Sicherheits-, Tierwohl-, Datenschutz-, Energie- oder Leistungswertung ohne direkt vergleichbare Evidenz;
- Quellenlücke bleibt `NOT_IN_SOURCE`.

## Produktvalidierung gegen die Profilspec

Fresh source-bound Gegenprüfung 2026-09-11:

- `luefter-im-stall`: Vostermans Multifan 130-cm Dairy Fan + Munters Saturn Breeze 55-inch belegen zwei unabhängige große axiale Milchviehstall-Umluftventilatorfamilien. Konkrete Motor-/Regelvarianten bleiben Pflicht vor einer realen Paarfreigabe;
- `zeitschaltuhren-im-stall`: Brennenstuhl MZ 44 DE IP44 + Theben timer 26 IP44 belegen zwei unabhängige analoge 1-Kanal-Steckdosen-Tageszeitschaltuhren mit IP44, 16 A ohmscher Last und 15-Minuten-Raster;
- `kameras-im-stall`: Kerbl IPCam 360 FHD + Luda.Farm FarmCam Flex 360 8MP belegen zwei unabhängige fest installierbare Farm-/Stall-PTZ-IP-Kameras mit lokaler Speicherung, Nachtsicht und IP65+.

Das ist keine finale Paarfreigabe und keine Markt-Vollständigkeit.

## Technische Materialisierungsgrenze

Dieses Dokument ändert `comparison-profiles.json` nicht.

Die Spezifikationen aus Akten 62–76 bleiben source-bound gesammelt. Vor technischer Materialisierung muss Product Knowledge pro Produkt/Variante die Klassenbindung und Pflichtfakten tragen.

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
