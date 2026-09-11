# PRODUKTVERGLEICH – PROFILE / FACT MATRIX HUFSCHLAGRÄUMER / REITPLATZBEWÄSSERUNG MOBIL / WEIDEPFLEGEGERÄTE V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Autoritative Registry-Folge:
- `p169 hufschlagraeumer`;
- `p170 reitplatzbewaesserung-mobil`;
- `p171 weidepflegegeraete`;
- danach `p172 nachsaat-fuer-pferdeweiden`;
- danach `p173 weideschleppen`;
- danach `p174 unkrautstecher`.

Daraus folgt zwingend:
- Hufschlagräumer werden nach realer Antriebs-/Mechanikklasse getrennt; Handgerät, batteriegetriebenes Standalone-Gerät und Planer-Anbaugerät sind keine identische Produktklasse;
- p170 enthält nur mobile selbsttätig einziehende Beregnungswagen/-systeme und niemals die feste p163-Beregnung;
- `weidepflegegeraete` p171 wird nicht als beliebiger Sammelbegriff geöffnet. Erste V1-Unterklasse ist ein reiner mechanischer Grünlandstriegel ohne montiertes Sägerät;
- Nachsaat-/Sägerät-Konfigurationen gehören p172, passive Ketten-/Gussstern-Weideschleppen p173;
- finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin aus aktuellem Product Knowledge.

---

## 1. Hufschlagräumer

Portal-Key / technischer Key:
`hufschlagraeumer`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Oberklasse:
`STANDALONE_HOOF_TRACK_LEVELER_FOR_RIDING_ARENA`.

Pflicht-Subtypen vor einem konkreten Pairing:
- `MANUAL_PULL_HOOF_TRACK_LEVELER`;
- `BATTERY_POWERED_SELF_DRIVEN_HOOF_TRACK_LEVELER`;
- Planer-Anbaugeräte sind eine separate Zubehörklasse und werden nicht mit Standalone-Geräten gepaart.

Pflichtmerkmale:
- ausdrücklich zum Zurückführen/Planieren des an Bande oder Reitplatzumrandung aufgebauten Hufschlags;
- eigenständiges Gerät oder klar definierter Zubehör-Subtyp;
- Antriebsart source-bound;
- Führungs-/Abstandsmechanik und Planierschild source-bound;
- Gewicht/Arbeitsbreite soweit veröffentlicht gebunden.

Ausgeschlossen bzw. separate Klassen:
- kompletter Reitplatzplaner;
- Reitplatzschleppe;
- einfacher Rechen/Schaufel;
- Hufschlagräumer als Bestandteil eines Planers, wenn das Vergleichsobjekt der komplette Planer wäre;
- elektrisches Standalone-Gerät gegen Handgerät als direktes Produktpaar.

### Aktuelle Evidence

Reitsand GmbH / equotec – `Hand-Hufschlagräumer handy`:
- eigenständiger manueller Hufschlagräumer;
- pulverbeschichteter Stahl;
- gekantetes Planierschild;
- Neigung individuell verstellbar;
- ca. 1,0 m breit, ca. 1,20 m Gesamthöhe;
- ca. 7 kg;
- Führung an Reithallenbande/Reitplatzeinfassung möglich, Nutzung auch auf freier Fläche beschrieben.

Hersteller-/Produktquellen:
https://reitsand-gmbh.de/handhufschlagraeumer/
https://www.reitsand-shop.de/equotec-hand-hufschlagraeumer-handy.html

Concept Reitplatzbau – `E-Hufschlagräumer`:
- eigenständiges batteriegetriebenes Gerät;
- AGM-Antriebsbatterie mit Ladeeinrichtung/Ladezustandsanzeige;
- wartungsfreier Elektromotor;
- Geschwindigkeit am Drehgriff regelbar;
- Vorwärts-/Rückwärtsfahrt;
- individuell verstellbares Planierschild;
- Abstands-/Bandenschutzrad;
- ca. 135 kg laut aktueller Produktseite;
- für mehrere Reitbodenklassen einschließlich Sand, Sand/Vlies, Holz-Sticks und Ebbe-Flut beschrieben.

Hersteller-/Produktquellen:
https://concept-reitplatzbau.de/e-hufschlagraeumer/
https://concept-reitplatzbau.de/produkt/e-hufschlagraeumer/

### Faktenmatrix V1

1. `hoof_track_leveler_class`;
2. `drive_class`;
3. `standalone_or_attachment`;
4. `arena_use_explicit`;
5. `indoor_outdoor_use`;
6. `surface_classes`;
7. `working_width_mm`;
8. `overall_height_mm`;
9. `weight_kg`;
10. `levelling_blade_present`;
11. `levelling_blade_adjustable`;
12. `guide_wheel_present`;
13. `boundary_guidance_required`;
14. `free_area_use_supported`;
15. `battery_class`;
16. `charger_included`;
17. `speed_adjustable`;
18. `forward_reverse`;
19. `motor_class`;
20. `current_lifecycle`.

### Pairing-Regeln

- gleiche Gruppe `hufschlagraeumer`;
- identischer `drive_class`;
- identischer `standalone_or_attachment`;
- gleiche reale Hauptfunktion;
- gleiche grobe Arbeitsbreiten-/Gewichtsklasse, wenn diese den Nutzerintent prägt;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

**Fail-closed:**
Die aktuelle Evidence belegt die Registry-Gruppe und zwei reale Subtypen, aber **noch kein konkretes Cross-Brand-Paar**. equotec `handy` ist manuell; Concept E-Hufschlagräumer ist batteriegetrieben. Diese dürfen nicht gegeneinander als gleichartige A-vs-B-Produkte freigegeben werden. Ein Paar entsteht erst bei mindestens zwei unabhängigen Herstellerfamilien innerhalb desselben Subtyps.

### Decision-Policy

- gleicher Subtyp / gleiche Hauptfunktion: `PAIRING_EQUAL_NO_PREFERENCE`;
- Gewicht, Arbeitsbreite, Führungsmechanik, Schildverstellung, Batterie-/Antriebstechnik: sachliche Unterschiede;
- keine freie Aussage zu Zeitersparnis, Kraftaufwand, Sicherheit oder Pflegequalität ohne vergleichbare Messung;
- Nutzer-/Herstellerbewertungen nicht als technische Fakten behandeln.

---

## 2. Reitplatzbewässerung mobil

Portal-Key / technischer Key:
`reitplatzbewaesserung-mobil`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste V1-Klasse:
`WATER_DRIVEN_SELF_RETRACTING_MOBILE_ARENA_IRRIGATION_REEL`.

Pflichtmerkmale:
- mobil zwischen Reitplatz/Reithalle bzw. Flächen versetzbar;
- Schlauch-/Regnerwagen-System;
- Einzug/Fahrbewegung über Wasserdruck/Turbinen- oder vergleichbaren wassergetriebenen Mechanismus;
- selbsttätiger Rücklauf/Einzug;
- automatische Abschaltung am Ende;
- Arbeitsbreite/Wurfweite, Arbeitslänge/Schlauchlänge, Durchfluss und erforderlicher Fließdruck source-bound;
- kein fest installiertes Rohr-/Regnersystem.

Ausgeschlossen bzw. separate Klassen:
- feste Reitplatzberegnung -> `reitplatzbewaesserung` p163;
- Wasserfass mit Sprühbalken;
- Schlepper-Anbau-Wasserwagen;
- mobiler Dachschienenwagen trotz Herstellerbezeichnung `mobil`, wenn das System fest an Hallenschienen installiert wird;
- einfacher Gartenschlauch/Einzelregner.

### Aktuelle Evidence

Ridcon GmbH – `WetMan 32`:
- mobiler Bewässerungswagen für Reithalle/Reitplatz;
- 70 m PE-Schlauch, 1 Zoll;
- Eingangsdruck 2,5–5,5 bar;
- Turbinenantrieb 10–30 m/h;
- Wurfweite bis 16 m bei 5 bar;
- Durchfluss 1,9–4,8 m³/h;
- Sektorregner;
- automatische Abschaltung und automatische Schlauchführung;
- Gewicht 135 kg.

Herstellerquelle:
https://shop.ridcon.de/products/bew32

ProEquus – `WP 800`:
- mobile Beregnung für Reitplatz/Reithalle;
- selbsttätig eingezogener Regnerwagen über Wasserdruck;
- einstellbare Einzugs-/Fahrgeschwindigkeit;
- automatische Abschaltung von Wasserzufuhr und Einzug am Endpunkt;
- Arbeitsbreite 10–25 m;
- Arbeitslänge max. 65 m;
- Wasserverbrauch auf aktueller HTML-Seite 1,5 m³/h;
- erforderlicher Fließdruck 3,0 bar für 20 m bzw. 4,0 bar für 25 m Breite;
- 1-Zoll-Wasseranschluss laut aktueller HTML-Seite.

Anbieterquelle:
https://www.pro-equus.com/produkte/mobile-beregnung/

Zusätzliche aktuelle Markt-Evidence:
Summerwind bietet eine mobile Beregnungsanlage ausdrücklich für Reitplatz/Reithalle und weitere Flächen an; dies belegt Marktbreite, ersetzt aber keine Hersteller-/OEM-Identitätsprüfung.

Quelle:
https://www.summerwind.eu/236-2/

### Faktenmatrix V1

1. `mobile_irrigation_class`;
2. `manufacturer_family`;
3. `oem_identity_verified`;
4. `arena_use_explicit`;
5. `mobile_between_surfaces`;
6. `drive_retraction_class`;
7. `hose_length_m`;
8. `hose_diameter_inch`;
9. `working_length_m`;
10. `working_width_m`;
11. `throw_range_m`;
12. `flow_min_m3_h`;
13. `flow_max_m3_h`;
14. `required_pressure_min_bar`;
15. `required_pressure_max_bar`;
16. `pressure_reference`;
17. `sector_min_deg`;
18. `sector_max_deg`;
19. `travel_speed_min_m_h`;
20. `travel_speed_max_m_h`;
21. `automatic_shutoff`;
22. `automatic_hose_guidance`;
23. `sprinkler_class`;
24. `water_connection_class`;
25. `weight_kg`;
26. `current_lifecycle`.

### Pairing-Regeln

- gleiche Gruppe `reitplatzbewaesserung-mobil`;
- `mobile_irrigation_class = WATER_DRIVEN_SELF_RETRACTING_MOBILE_ARENA_IRRIGATION_REEL`;
- gleiche Größen-/Leistungsklasse;
- Wasserwerte immer zusammen mit zugehörigem Druck-/Arbeitsbreitenbezug;
- identische Bezugslogik für Arbeitslänge vs. Schlauchlänge;
- `manufacturer_family` muss unabhängig belegt sein;
- bei unklarer OEM-/White-Label-Identität `oem_identity_verified = false` -> kein Cross-Family-Paar;
- aktueller pairable Lifecycle.

**Fail-closed:**
Ridcon WetMan 32 und ProEquus WP 800 belegen dieselbe funktionale Geräteoberklasse, werden aber **noch nicht als unabhängiges Herstellerpaar freigegeben**, solange OEM-/Herstelleridentität des ProEquus-Modells nicht belastbar gebunden ist. Ähnliche Abmessungen, Leistungsdaten oder Modellnamen dürfen nicht als Beweis für gleiche oder verschiedene OEM-Herkunft interpretiert werden.

### Decision-Policy

- mobile selbsttätig einziehende Grundklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Schlauch-/Arbeitslänge, Arbeitsbreite, Durchfluss, Druck, Einzugsgeschwindigkeit, Abschaltung, Gewicht: sachliche Unterschiede;
- Durchfluss niemals ohne Druck-/Düsen-/Breitenbezug ranken;
- keine freie Aussage zu Wasserersparnis, gleichmäßiger Beregnung oder Bodenqualität ohne gleiche Messmethode;
- feste p163-Anlage nie in p170 ziehen.

---

## 3. Weidepflegegeräte

Portal-Key / technischer Key:
`weidepflegegeraete`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Der Registry-Key ist ein Oberbegriff. Erste V1-Unterklasse:
`3M_THREE_POINT_FOUR_ROW_SPRING_TINE_GRASSLAND_HARROW_WITHOUT_SEEDER`.

Pflichtmerkmale:
- mechanischer Grünland-/Wiesenstriegel;
- 3,0-m-Arbeitsbreitenklasse;
- Dreipunktanbau;
- vier Zinkenreihen;
- Feder-/Striegelzinken zur Grünlandpflege;
- Basisgerät ohne montiertes Sägerät;
- ausdrücklich für Grünland/Wiesenpflege.

Ausgeschlossen bzw. separate Klassen:
- Nachsaatgerät bzw. Striegel mit gebundenem Sägerät als Vergleichskern -> `nachsaat-fuer-pferdeweiden` p172;
- passive Ketten-/Gussstern-Weideschleppe -> `weideschleppen` p173;
- Wiesenwalze;
- Mulcher;
- Mähwerk;
- Düngerstreuer;
- reine Reitplatzschleppe;
- allgemeines Gerät, dessen Grünlandeignung nicht source-bound ist.

### Aktuelle Hersteller-Evidence

Düvelsdorf – `GREEN.RAKE classic 3 m`:
- Grünland-/Wiesenstriegel;
- Arbeitsbreite 3 m;
- vierreihiges Striegelfeld;
- 10-mm-Zinken;
- 75-mm-Zinkenabstand;
- Gewicht 560 kg in 3-m-Ausführung;
- doppelte Planierschiene;
- Striegelintensität höhenverstellbar;
- robuste Grünlandpflegeklasse.

Herstellerquelle:
https://www.duevelsdorf.de/produkte/gruenlandpflege/striegel/green-rake-classic

APV – `GS 300 M1`:
- Grünlandstriegel;
- Arbeitsbreite 3 m;
- vier Zinkenreihen: zwei vordere stärkere und zwei hintere schwächere Reihen;
- vorn 40 Zinken in 10 bzw. 12 mm, hinten 60 Zinken in 8 mm;
- KAT 2 / KAT 2 N;
- Traktorleistung ab 20 kW / 27 PS;
- Tasträder;
- Basisgerät kann mit pneumatischem Sägerät kombiniert werden; für p171 ist ausschließlich die **Konfiguration ohne montiertes Sägerät** zulässig;
- gefedertes Einebnungsblech ist Zubehör und darf nicht als Serienausstattung des Basisgeräts behauptet werden.

Herstellerquelle:
https://www.apv.at/produkte/gruenland/gruenlandstriegel/gs-300-m1

Einböck `GRASS-MANAGER` belegt zusätzlich eine aktuelle reine Wiesenstriegel-Familie ohne serienmäßiges Sägerät; ein Sägerät kann optional aufgebaut werden. Für ein konkretes Pairing müssen exakte Variante/Arbeitsbreite und Basisausstattung gebunden werden.

Herstellerquelle:
https://www.einboeck.at/produkte/gruenlandpflege/gruenlandstriegel-ohne-saegeraet/grass-manager/

### Faktenmatrix V1

1. `pasture_maintenance_class`;
2. `grassland_use_explicit`;
3. `mounted_seeder_present`;
4. `seeder_optional`;
5. `attachment_category`;
6. `working_width_m`;
7. `transport_width_m`;
8. `weight_kg`;
9. `tine_row_count`;
10. `tine_count`;
11. `front_tine_diameter_mm`;
12. `rear_tine_diameter_mm`;
13. `uniform_tine_diameter_mm`;
14. `tine_spacing_mm`;
15. `tine_aggressiveness_adjustable`;
16. `tine_pressure_adjustable`;
17. `levelling_bar_present`;
18. `levelling_bar_standard_or_optional`;
19. `support_wheel_count`;
20. `required_tractor_power_kw`;
21. `required_tractor_power_hp`;
22. `folding_class`;
23. `tine_loss_protection`;
24. `current_lifecycle`.

### Pairing-Regeln

- gleiche Gruppe `weidepflegegeraete`;
- gleiche erste Unterklasse `3M_THREE_POINT_FOUR_ROW_SPRING_TINE_GRASSLAND_HARROW_WITHOUT_SEEDER`;
- 3-m-Arbeitsbreitenklasse;
- vier Zinkenreihen;
- Basiskonfiguration ohne montiertes Sägerät;
- Anbaukategorie und erforderliche Traktorleistung konkret binden;
- Serienausstattung strikt von Optionen trennen;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

**Fail-closed:**
Düvelsdorf GREEN.RAKE classic 3 m und APV GS 300 M1 belegen eine fachlich vergleichbare 3-m-Grünlandstriegelklasse. Vor finalem Pairing müssen konkrete Anbaukategorie, Basisgewicht und Ausstattungsstatus der Planier-/Einebnungskomponenten normalisiert werden. Ein optional montiertes Sägerät verschiebt die konkrete Konfiguration in den p172-Nachsaat-Intent und darf im p171-Paar nicht still mitgewertet werden.

### Decision-Policy

- reine 3-m-Grünlandstriegel-Grundfunktion ohne Sägerät: `PAIRING_EQUAL_NO_PREFERENCE`;
- Zinkenarchitektur/-stärke/-abstand, Gewicht, Anbaukategorie, Leistungsbedarf, Einstellbarkeit und Einebnungskomponenten: sachliche Unterschiede;
- keine freie Aussage zu Ertrag, Stickstofffreisetzung, Grasnarbenverbesserung oder Futterqualität als allgemeiner Produktsieg;
- Nachsaatfunktion nicht gegen reine Pflegefunktion ranken, wenn dadurch p172 dupliziert würde.

---

## Akte-86-Negativcheck

PASS:
- p169–p174 direkt gegen autoritative Registry-Folge geprüft;
- p169 Handgerät, Batterie-Standalone und Planer-Anbaugerät nicht vermischt;
- p169 wegen fehlender zweiter Herstellerfamilie im selben Subtyp aktuell 0 konkretes Paar;
- p170 strikt von fester p163-Beregnung getrennt;
- p170 OEM-/Herstellerfamilienidentität als Pflichtgate aufgenommen;
- p171 strikt von p172 Nachsaat und p173 Weideschleppen getrennt;
- für p171 konkrete erste Subklasse statt offenen Sammelbegriffs definiert;
- aktuelle HTML-Hersteller-/Produktquellen gegengeprüft; keine PDF-Faktauswertung als Beleg verwendet;
- keine finale konkrete Paarentscheidung manuell festgeschrieben;
- keine technische Materialisierung;
- kein SEO;
- kein Writer/Draft/Publish;
- kein Codex;
- kein Merge;
- kein Publish.

OFFEN:
- technische UPC-Materialisierung dieser drei Profile;
- p169 zweite unabhängige Herstellerfamilie je identischem Subtyp;
- p170 OEM-/Herstelleridentität für Cross-Family-Pairing;
- vollständige technische Positiv-/Negativ-/Mutation-/Fresh-ZIP-Prüfung erst nach gebündelter Materialisierung;
- WordPress-Live-Test UPC 0.8.6 unverändert offen.

## Nächster Registry-Einstieg nach Akte 86

1. `p172 nachsaat-fuer-pferdeweiden`;
2. `p173 weideschleppen`;
3. `p174 unkrautstecher`.

Keine Materialisierung in dieser Akte.