# PRODUKTVERGLEICH – PROFILE / FACT MATRIX UNTERSTAND-BELEUCHTUNG / BOXENTÜREN / BOXENRIEGEL / BOXENGITTER V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Registry-Gruppen:
- `unterstand-beleuchtung`;
- `boxentueren`;
- `boxenriegel`;
- `boxengitter`.

Keine Gruppe wird nur über den Einsatzort Stall/Unterstand normalisiert. Konstruktionsklasse und konkrete Produktvariante bleiben Pflicht.
Finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin aus aktuellem Product Knowledge.

---

## 1. Unterstand-Beleuchtung

Portal-Key / technischer Key:
`unterstand-beleuchtung`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound Cross-Brand-V1-Klasse:
`OFFGRID_SOLAR_SHED_BARN_LIGHTING_SYSTEM_WITH_SEPARATE_PANEL`.

Pflichtmerkmale:
- netzunabhängiges Solar-Beleuchtungssystem;
- separates Solarmodul außerhalb bzw. im Sonnenbereich;
- Leuchte für Schuppen/Scheune/Stall/Unterstand oder vergleichbaren überdachten Nutzraum source-bound;
- Akku-/Speicherbetrieb;
- fest installierbare Leuchteneinheit;
- kein 230-V-Hofstrahler und keine ammoniakgeprüfte Stall-Linearlampe als gleiche Klasse.

Ausgeschlossen bzw. separate Klassen:
- `hofbeleuchtung` mit netzgespeistem Außenstrahler;
- `stallbeleuchtung` mit ammoniak-/IP69K-gebundener Tierstall-Linearlampe;
- dekorative Solar-Gartenleuchte;
- mobile Taschen-/Arbeitslampe;
- Solar-Weidezaungerät;
- reine Solarpanel-Komponente ohne Beleuchtungssystem.

### Aktuelle Hersteller-/Direktprodukt-Evidence

GEO-Technik:
- `Solar Beleuchtung-Set für Lagerschuppen Stall`;
- ausdrücklich für Schuppen/Tierstall;
- monokristallines Solarmodul 50 W;
- 12-V-System;
- zwei LED-Anbauleuchten mit je 6 W;
- Solar-Gel-Akku und Laderegler;
- Wandschalter;
- 25 m Kabel;
- Betriebsdauer bei vollem Akku laut Anbieter bis 13 Stunden.

Quelle:
https://www.geo-technik.de/Solar-Beleuchtung-Set-fuer-Lagerschuppen-Stall

Solaraluma:
- `Pro Solar Barn Light` / 2000-Lumen-Klasse;
- getrenntes Solarmodul und lineare Leuchte;
- 45-W-Solarmodul laut Produktdaten;
- ca. 39-Zoll-Linearleuchte;
- ca. 5-m-Verbindungskabel;
- explizit für Barn/Shed/Workshop und bild-/textseitig Pferdestall-Anwendung;
- lokale/off-grid Beleuchtung ohne Haushaltsnetz.

Quelle:
https://solaraluma.com/products/solar-barn-light

### Faktenmatrix V1

1. `lighting_system_class`;
2. `offgrid`;
3. `solar_panel_separate`;
4. `solar_panel_power_w`;
5. `system_voltage_v`;
6. `battery_chemistry`;
7. `battery_capacity_wh_or_ah`;
8. `luminaire_count`;
9. `luminaire_class`;
10. `rated_light_power_w`;
11. `luminous_flux_lm`;
12. `color_temperature_k`;
13. `ip_rating_luminaire`;
14. `ip_rating_connectors`;
15. `cable_length_m`;
16. `switch_class`;
17. `motion_sensor`;
18. `remote_control`;
19. `runtime_claim_h`;
20. `runtime_claim_conditions`;
21. `animal_barn_use_claim`;
22. `ammonia_resistance_claim`;
23. `mounting_hardware_included`;
24. `warranty`.

Watt-Äquivalent, Lumen, Laufzeit und Akkureserve werden nur bei klarer Mess-/Betriebsbedingung direkt verglichen.

### Pairing-Regeln

- gleiche Gruppe `unterstand-beleuchtung`;
- `lighting_system_class = OFFGRID_SOLAR_SHED_BARN_LIGHTING_SYSTEM_WITH_SEPARATE_PANEL`;
- getrenntes Solarpanel;
- feste Leuchteneinheit für überdachten Nutz-/Stall-/Schuppenbereich;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

### Decision-Policy

- Off-grid-/Solar-/Einsatzklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Panelleistung, Leuchtenzahl, Lichtstrom, Akku, Kabel, Sensorik und Laufzeit: sachliche Unterschiede;
- keine freie Aussage zu ausreichender Stallbeleuchtungsstärke, Tierwohl, Brandschutz, Winterautonomie oder Ammoniakbeständigkeit;
- Herstellerclaims zu Laufzeit nur mit Bedingungen wiedergeben;
- keine Tierzonenfreigabe allein aus dem Wort `Barn/Stall` ableiten.

---

## 2. Boxentüren

Portal-Key / technischer Key:
`boxentueren`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound Cross-Brand-V1-Klasse:
`SINGLE_LEAF_SLIDING_HORSE_BOX_DOOR_120_130CM_PASSAGE_CLASS`.

Pflichtmerkmale:
- eigenständige Schiebetür für Pferdebox/Pferdestall;
- einflügelig;
- lichte Durchgangsbreite bzw. Einbaubreite ca. 120 cm;
- komplette Tür mit Schiebelauf-/Schienenlösung;
- keine komplette Pferdeboxenfront als Vergleichsobjekt;
- kein zweiflügeliges Stalltor.

Ausgeschlossen bzw. separate Klassen:
- Drehtür;
- halbhohe Boxendrehtür;
- komplette Frontwand mit integrierter Tür;
- zweiflügeliges Schiebetor;
- Außenstollentür/-tor mit anderer Wetter-/Gebäudeklasse;
- reine Laufschiene oder Beschlagset.

### Aktuelle Hersteller-Evidence

Großewinkelmann GmbH & Co. KG / GROWI:
- `Schiebetür für Wandmontage`, Art.-Nr. 10011360 (Douglasie) bzw. 10011370 (Bongossi);
- Pferdebox-Schiebetür zum Anschrauben/Dübeln an vorhandene Mauern oder Boxenwände;
- Türbreite 1300 mm;
- Gesamthöhe ca. 2300 mm;
- C-Profilschiene 3000 mm;
- zwei Laufwagen, Stopper und Schienenhalter;
- Holzfüllung je Variante.

Quellen:
https://www.growi.de/stall-weidetechnik/pferdeboxen/zubehoer-pferdeboxen/schiebetuer-wandmontage-douglasie
https://www.growi.de/stall-weidetechnik/pferdeboxen/zubehoer-pferdeboxen/schiebetuer-wandmontage-bongossi

Rutjes Pferdeboxen:
- `Schiebetür für Pferdestall | Kunststoff`;
- ein Flügel;
- 32-mm-Kunststoffbretter;
- Produktmaß ca. 130 x 225 cm;
- Einbaumaß ca. 120 x 220 cm;
- Pferdestall-/Pferdebox-Schiebetür;
- kundenspezifische Anpassungen möglich.

Quelle:
https://www.rutjespferdeboxen.de/produkt/schiebetur-pferdestall/

### Faktenmatrix V1

1. `door_class`;
2. `opening_mechanism`;
3. `leaf_count`;
4. `horse_box_use`;
5. `door_width_mm`;
6. `door_height_mm`;
7. `clear_opening_width_mm`;
8. `clear_opening_height_mm`;
9. `frame_material`;
10. `filling_material`;
11. `filling_thickness_mm`;
12. `upper_grid_present`;
13. `track_profile_class`;
14. `track_length_mm`;
15. `trolley_count`;
16. `stopper_included`;
17. `wall_mounting_class`;
18. `locking_mechanism`;
19. `opening_direction_or_side`;
20. `custom_size_available`;
21. `surface_finish`;
22. `weight_kg`;
23. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `boxentueren`;
- `opening_mechanism = SLIDING`;
- `leaf_count = 1`;
- Pferdebox-/Pferdestall-Tür;
- Passage-/Einbaubreite ca. 120 cm;
- konkrete Füllungs-/Gittervariante im Product Knowledge gebunden;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Keine Cross-System-Kompatibilität der Schienen, Laufwagen oder Wandanschlüsse behaupten.

### Decision-Policy

- Tür-/Öffnungs-/Blattklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Füllung, Schiene, Laufwagen, Montage und Gewicht: sachliche Unterschiede;
- keine freie Aussage zu Pferdesicherheit, Leichtlauf, Lebensdauer oder Einbruchschutz;
- kundenspezifische Abweichungen nur als konkrete Variante behandeln;
- keine komplette Boxenfront gegen eine Einzeltür paaren.

---

## 3. Boxenriegel

Portal-Key / technischer Key:
`boxenriegel`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound V1-Klasse:
`VERTICAL_DOUBLE_LIFT_BOLT_FOR_HORSE_STALL_DOOR`.

Pflichtmerkmale:
- eigenständiger mechanischer Riegel/Verschluss für Stall-/Boxentür;
- vertikale Hub-/Stangenmechanik;
- obere und untere Verriegelung;
- als einzelnes Beschlagprodukt kauf-/spezifizierbar;
- keine komplette Tür oder Frontwand.

Ausgeschlossen bzw. separate Klassen:
- integrierter Riegel ohne separat identifizierbares Produkt;
- Stabverschluss für Schiebetür als andere Mechanik;
- einfaches Vorhängeschloss;
- Torfalle/Fallschloss für Weidetor;
- Fensterriegel;
- Türdrücker/Profilzylinder.

### Aktuelle Evidence

GROWI / Großewinkelmann:
- `Doppelhubriegelverschluß` für GROWI-Stalltüren;
- ca. 950 mm lang;
- Hubstange aus Flachstahl 30 x 6 mm;
- inklusive oberem und unterem Schließblech;
- aktueller Einzelbeschlag im Stalltüren-Sortiment.

Direkt-/Herstellerbeleg:
https://www.stallshop24.de/Stall/Stalleinrichtung/Tueren-Fenster/Tueren/
https://www.growi.de/media/files_public/Katalog_Growi_SW.pdf

Weitere Herstellerfamilien wie HAU oder Bräuer belegen Doppel-/Mehrpunktverschlüsse an kompletten Pferdeboxen, aber aktuell keine zweite gleichartig source-bound **separate Einzelkomponente** für diese V1-Unterklasse.

### Faktenmatrix V1

1. `latch_class`;
2. `door_use_scope`;
3. `vertical_rod`;
4. `locking_points`;
5. `overall_length_mm`;
6. `rod_material`;
7. `rod_width_mm`;
8. `rod_thickness_mm`;
9. `upper_strike_included`;
10. `lower_strike_included`;
11. `surface_finish`;
12. `mounting_hardware_included`;
13. `inside_operable`;
14. `outside_operable`;
15. `lockable`;
16. `compatible_door_system`;
17. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `boxenriegel`;
- `latch_class = VERTICAL_DOUBLE_LIFT_BOLT_FOR_HORSE_STALL_DOOR`;
- eigenständige Beschlagkomponente;
- gleiche Verriegelungsmechanik;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

**Fail-closed:**
Aktuell ist nur eine sauber separate Produktfamilie belegt. Deshalb **0 Cross-Brand-Paare**, bis ein zweiter Hersteller eine gleichartige, separat identifizierbare Komponente source-bound liefert.

### Decision-Policy

- Mechanik/Verriegelungspunkte: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Material, Bedienung, Lieferumfang und Systembindung: sachliche Unterschiede;
- keine integrierten Türverschlüsse als scheinbar identische Einzelprodukte behandeln;
- keine Sicherheitsüberlegenheit ohne normierte Prüfevidenz ableiten.

---

## 4. Boxengitter

Portal-Key / technischer Key:
`boxengitter`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Der Registry-Key ist ein Oberbegriff. Pflicht-Subtyp vor Pairing.

Aktuell source-bound belegte Unterklassen:
1. `SMALL_FIXED_GRID_INSERT_FOR_HORSE_BOX_PARTITION_500X500`;
2. `LARGE_TOP_GRID_FOR_MASONRY_HORSE_BOX_WALL_1000H`.

Diese beiden Unterklassen dürfen **nicht** gegeneinander gepaart werden.

### Aktuelle Evidence

Rutjes Pferdeboxen:
- `Gittereinsatz für Pferdeboxen`;
- Einbaumaß 50 x 50 cm;
- feuerverzinkter Stahl;
- U-Profil;
- für Trenn-/Außenwände;
- geeignet für 32-mm-Bretter.

Quelle:
https://www.rutjespferdeboxen.de/produkt/gittereinsatz-fur-pferdeboxen/

GROWI / Großewinkelmann:
- `Aufsatzgitter für gemauerte Wände`;
- Varianten 2510–3000 mm bzw. 3010–4000 mm breit;
- 1000 mm hoch;
- 3/4-Zoll-Rohre;
- lichter Gitterabstand 50 mm;
- Rahmen aus Quadratrohr 50 x 50 x 3 mm und U-Eisen 50 x 40 x 4 mm;
- für vorhandene gemauerte Pferdeboxwände.

Quellen:
https://www.growi.de/stall-weidetechnik/pferdeboxen/zubehoer-pferdeboxen/aufsatzgitter-gemauerte-waende
https://www.growi.de/stall-weidetechnik/pferdeboxen/zubehoer-pferdeboxen/aufsatzgitter-gemauerte-waende1

### Faktenmatrix V1

1. `grid_subtype`;
2. `installation_location`;
3. `horse_box_use`;
4. `width_mm`;
5. `height_mm`;
6. `frame_profile`;
7. `bar_profile_or_diameter_mm`;
8. `clear_bar_spacing_mm`;
9. `material`;
10. `surface_finish`;
11. `board_thickness_compatibility_mm`;
12. `masonry_wall_mounting`;
13. `mounting_hardware_included`;
14. `custom_size_available`;
15. `weight_kg`;
16. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `boxengitter`;
- gleicher `grid_subtype` zwingend;
- gleiche Einbauart und ähnliche Größenklasse;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

**Fail-closed:**
Der aktuelle Rutjes-500x500-Gittereinsatz und das GROWI-Aufsatzgitter sind unterschiedliche Unterklassen und erzeugen **kein Paar**. Für Cross-Brand-Pairing muss pro Unterklasse eine zweite unabhängige Herstellerfamilie source-bound belegt werden.

### Decision-Policy

- Unterklasse/Einbauart: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Profile, Stababstand, Material und Montage: sachliche Unterschiede;
- keine Aussage zu Sozialkontakt, Sicherheit, Stabilität oder Verletzungsrisiko als freies Ranking;
- keine komplette Trennwand oder Boxenfront als `Boxengitter` einschleusen.

## Globale Negativprüfung

Muss fail-closed bleiben:
- Unterstand-Solarlicht vs. 100-W-Hofstrahler;
- Unterstand-Solarlicht vs. ammoniakbeständige Stall-Linearlampe;
- Schiebetür vs. Drehtür;
- Einzeltür vs. komplette Boxenfront;
- Doppelhubriegel-Einzelbeschlag vs. integrierter Schiebetür-Stabverschluss;
- 500x500-Gittereinsatz vs. 2,5–4-m-Aufsatzgitter;
- Gittereinsatz vs. komplette Boxentrennwand.

## Materialisierungsstatus

Diese Akte ist nur source-bound Fachvorarbeit.
Keine Änderung an UPC 0.8.6.
Kein Product-Knowledge-Import.
Kein SEO-/Providerlauf.
Kein Merge.
Kein Publish.
