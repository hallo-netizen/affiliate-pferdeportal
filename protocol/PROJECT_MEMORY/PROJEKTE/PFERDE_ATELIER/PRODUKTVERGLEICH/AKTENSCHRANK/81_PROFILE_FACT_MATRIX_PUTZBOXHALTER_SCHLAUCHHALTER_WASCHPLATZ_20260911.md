# PRODUKTVERGLEICH – PROFILE / FACT MATRIX PUTZBOXHALTER / SCHLAUCHHALTER / WASCHPLATZ V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Registry-Gruppen:
- `putzboxhalter`;
- `schlauchhalter-am-putzplatz`;
- `waschplatz-fuer-pferde`.

Putzboxhalter, Schlauchhalter und Pferdedusche/Waschplatz sind getrennte Produktklassen. Ein vollständiger Waschplatz als Bau-/Planungsleistung darf nicht mit einer einzelnen Duschkomponente gleichgesetzt werden.
Finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin aus aktuellem Product Knowledge.

---

## 1. Putzboxhalter

Portal-Key / technischer Key:
`putzboxhalter`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound V1-Klasse:
`HANG_ON_HORSE_BOX_EDGE_GROOMING_BOX_HOLDER`.

Pflichtmerkmale:
- eigenständige Halterung für eine Putzbox/Putzkiste;
- an Boxenwand/-kante einhängbar;
- kein fahrbarer Sattelwagen;
- kein Sattelhalter mit zusätzlicher Putzboxablage;
- konkrete Putzbox-/Größenkompatibilität source-bound.

Ausgeschlossen bzw. separate Klassen:
- Sattelcaddy/Sattelbutler mit integrierter Putzboxhalterung;
- fahrbarer Stallwagen;
- festes Regal;
- Putzbox selbst;
- einfache Ablage ohne Box-Haltefunktion.

### Aktuelle Evidence

SHOWMASTER / Krämer Pferdesport:
- `Putzboxhalter Wall`, Art.-Nr. 450792;
- wird über die Boxenkante gehängt;
- nimmt die Putzbox in einer eigenständigen Halterung auf;
- hochklappbar und mit Elastikbändern an Boxenstäben fixierbar;
- Größenvarianten passend zu Putzbox Madrid bzw. Lissabon.

Quelle:
https://www.kraemer.at/Stalleinrichtung/Stallzubehoer-Reitplatzzubehoer/Putzboxhalter-Wall

Gegenbelegte andere Klassen:
- Waldhausen `Stall-Carry`: Sattelhalter + Zaumhaken + Ablage + Putzboxhalterung, also Mehrfunktions-Stallwagen;
- VOSS.farming `Sattelcaddy Apollo`: fahrbarer Sattelcaddy mit integrierter Putzboxhalterung.

Quellen:
https://agrarzone.de/56387/waldhausen-stall-carry-sattelhalter-mit-ablage-schwarz
https://www.weidezaun.info/voss-farming-sattelcaddy-apollo-mit-putzboxhalterung.html

### Faktenmatrix V1

1. `holder_class`;
2. `mounting_class`;
3. `box_edge_mounting`;
4. `foldable`;
5. `retention_system`;
6. `compatible_grooming_box_models`;
7. `compatible_box_width_mm`;
8. `holder_width_mm`;
9. `holder_depth_mm`;
10. `holder_height_mm`;
11. `material`;
12. `surface_finish`;
13. `elastic_retainers`;
14. `mounting_hardware_required`;
15. `weight_kg`;
16. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `putzboxhalter`;
- `holder_class = HANG_ON_HORSE_BOX_EDGE_GROOMING_BOX_HOLDER`;
- eigenständige Halterung, kein Multifunktionswagen;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

**Fail-closed:**
Aktuell ist nur eine sauber belegte eigenständige Boxkantenhalter-Familie vorhanden. Deshalb **0 Cross-Brand-Paare**, bis eine zweite unabhängige Herstellerfamilie derselben Bauklasse source-bound belegt ist.

### Decision-Policy

- Klasse/Montage: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Passform, Falt-/Fixiermechanik und Material: sachliche Unterschiede;
- keine fahrbaren Sattelcaddys als vermeintlich gleiche Putzboxhalter einschleusen;
- keine freie Aussage zu Stabilität/Haltbarkeit ohne Prüfevidenz.

---

## 2. Schlauchhalter am Putzplatz

Portal-Key / technischer Key:
`schlauchhalter-am-putzplatz`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound Cross-Brand-V1-Klasse:
`CAST_IRON_WALL_HOSE_HOLDER_FOR_HORSE_STABLE_WASH_AREA`.

Pflichtmerkmale:
- passiver Schlauchhalter zur Wandmontage;
- Gusseisen;
- Nutzung am Pferdestall/Waschplatz bzw. für Pferde-Abspritzschlauch source-bound;
- keine Schlauchtrommel oder Schlauchbox;
- keine schwenkbare Pferdedusche.

Ausgeschlossen bzw. separate Klassen:
- Kunststoff-Wandschlauchhalter;
- Stahlblech-Schlauchhalter;
- automatische Schlauchtrommel;
- mobiler Schlauchwagen;
- Dusch-Schwenkarm;
- reine Dekoration ohne Schlauchhaltefunktion.

### Aktuelle Evidence

HKM Sports Equipment GmbH:
- `Schlauchhalter aus Gusseisen`, Art.-Nr. 6370;
- Wandmontage;
- Gusseisen;
- ca. 30 cm hoch, 25,5 cm breit;
- vom Hersteller für den Stallkontext geführt.

Herstellerquelle:
https://www.hkm-sports.com/de/schlauchhalter-aus-gusseisen.html

Antikas / bizness rocket GmbH:
- gusseiserner Wand-Schlauchhalter mit Pferdemotiv;
- ausdrücklich für Gartenschlauch bzw. Schlauch zum Abspritzen von Pferden/Pferdestall;
- Wandmontage;
- Gusseisen;
- Varianten je Design etwa 22–49 cm hoch und ca. 25,5 cm breit;
- konkrete Variante muss im Product Knowledge gebunden werden.

Quellen:
https://www.handgefertigtes.de/schlauchhalter-gartenschlauchhalter-pferd-malerische-schlauchaufwicklung.html
https://www.otto.de/p/antikas-schlauchhalterung-halterung-fuer-zuegel-und-stricke-schlauchhalter-gartenschlauch-pferd-S03A20KW/

### Faktenmatrix V1

1. `hose_holder_class`;
2. `wall_mounting`;
3. `horse_stable_use`;
4. `horse_washing_hose_use`;
5. `material`;
6. `finish`;
7. `width_mm`;
8. `height_mm`;
9. `depth_mm`;
10. `weight_kg`;
11. `hose_cradle_depth_mm`;
12. `mounting_hole_count`;
13. `mounting_hardware_included`;
14. `outdoor_use_claim`;
15. `additional_rope_tack_use_claim`;
16. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `schlauchhalter-am-putzplatz`;
- `hose_holder_class = CAST_IRON_WALL_HOSE_HOLDER_FOR_HORSE_STABLE_WASH_AREA`;
- Wandmontage;
- Gusseisen;
- Pferdestall-/Pferdewaschnutzung source-bound;
- unterschiedliche Herstellerfamilien;
- konkrete Variante im Product Knowledge gebunden;
- aktueller pairable Lifecycle.

### Decision-Policy

- Klasse/Material/Montage: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Gewicht, Finish und Zusatznutzung: sachliche Unterschiede;
- keine Designästhetik als technische Überlegenheit werten;
- keine Traglast/Haltbarkeit ohne Prüfevidenz ableiten;
- Kunststoff-/Metallblechhalter separat halten.

---

## 3. Waschplatz für Pferde

Portal-Key / technischer Key:
`waschplatz-fuer-pferde`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Der Registry-Key ist ein System-/Anwendungsoberbegriff. Pflicht-Subtyp vor Pairing.

Erste source-bound Cross-Brand-V1-Klasse:
`WALL_MOUNTED_TELESCOPIC_SWIVEL_HORSE_SHOWER_COMPLETE_SET`.

Pflichtmerkmale:
- Pferdedusche als Komplettset für Waschplatz;
- wandmontierter Schwenkarm;
- teleskopierbar/ausziehbar;
- feuerverzinkte Metallkonstruktion;
- Wasserschlauch inklusive;
- Dusch-/Abspritzbrause inklusive;
- Pferdenutzung ausdrücklich source-bound.

Ausgeschlossen bzw. separate Klassen:
- kompletter Waschplatzbau mit Boden/Entwässerung/Trennwand als Bauleistung;
- Waschplatzboden/-matte -> `putzplatzmatten` bzw. eigene Bodenklasse;
- Trennwand/Anbindepfosten;
- Handbrause allein;
- Schlauchhalter allein;
- Schwenkarm ohne Schlauch/Brause;
- mobile Gartendusche.

### Aktuelle Hersteller-Evidence

PATURA KG:
- `Pferde-Abspritzdusche, Komplett-Set inkl. Schwenkarm`, Ref. 334102;
- schwenkbar;
- teleskopierbar von 1,50 m bis 2,50 m;
- feuerverzinkt;
- inkl. Wasserschlauch, 1/2-Zoll-Anschlüsse und Duschbrause;
- Gewicht 13,40 kg.

Herstellerquelle:
https://www.patura.com/de_DE/produkt/334102-pferde-abspritzdusche-inkl-schlauch-anschlusse-und-duschbrause

GROWI / Großewinkelmann GmbH & Co. KG:
- `Pferdeabspritzdusche Variabel`, Art.-Nr. 10059580;
- schwenkbar;
- ausziehbar 1.200–2.300 mm;
- 1/2-Zoll-Anschlüsse;
- spezielle Duschbrause für Pferde;
- 7-m-Wasserschlauch;
- Metallteile feuerverzinkt;
- Schrauben/Dübel zur Wandbefestigung im Lieferumfang.

Herstellerquelle:
https://www.growi.de/stall-weidetechnik/stallausruestung/tierpflege/pferdepflege/pferdeabspritzdusche-variabel

AVERDE GmbH & Co. KG:
- `Pferdedusche Komplettset mit Schwenkarm, Abspritzbrause und Zubehör`, Art.-Nr. AVDUSASET;
- 180° drehbarer Schwenkarm;
- ausziehbar 1,60–2,60 m;
- feuerverzinkt;
- 7-m-1/2-Zoll-Schlauch;
- Abspritzbrause;
- Kupplungen/Schlauchanschluss;
- Gesamtgewicht ca. 13,30 kg;
- Wandmontageplatte, Montageschrauben/Dübel nicht enthalten.

Herstellerquelle:
https://www.averde.de/product/stallbedarf-hofbedarf/pferdedusche/pferdedusche-komplettset-mit-schwenkarm-abspritzbrause-und-zubehoer-avdusaset.html

### Faktenmatrix V1

1. `wash_system_subtype`;
2. `horse_use`;
3. `wall_mounting`;
4. `swivel_arm`;
5. `swivel_angle_deg`;
6. `telescopic_arm`;
7. `arm_min_length_mm`;
8. `arm_max_length_mm`;
9. `arm_material`;
10. `surface_finish`;
11. `hose_included`;
12. `hose_length_m`;
13. `hose_diameter_inch`;
14. `spray_nozzle_included`;
15. `spray_pattern_adjustable`;
16. `connectors_included`;
17. `mounting_plate_included`;
18. `mounting_hardware_included`;
19. `weight_kg`;
20. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `waschplatz-fuer-pferde`;
- `wash_system_subtype = WALL_MOUNTED_TELESCOPIC_SWIVEL_HORSE_SHOWER_COMPLETE_SET`;
- Schwenkarm + Schlauch + Brause als Komplettset;
- feuerverzinkte Bauklasse;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

### Decision-Policy

- System-/Montage-/Lieferumfangsklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Auszugslänge, Drehwinkel, Schlauchlänge, Brause, Kupplungen, Montagematerial und Gewicht: sachliche Unterschiede;
- keine freie Aussage zu Pferdesicherheit, Waschkomfort, Korrosionslebensdauer oder Installationssicherheit;
- kein kompletter Waschplatzbau gegen ein Duschset paaren;
- keine Produktentscheidung aus Bau-/Entwässerungsfragen ableiten.

## Globale Negativprüfung

Muss fail-closed bleiben:
- Boxkanten-Putzboxhalter vs. Sattelcaddy/Stallwagen;
- Gusseisen-Wandschlauchhalter vs. Kunststoff-/Stahlblechhalter;
- Schlauchhalter vs. Dusch-Schwenkarm;
- Pferdedusch-Komplettset vs. Handbrause allein;
- Pferdedusch-Komplettset vs. Waschplatz-Trennwand/Anbindepfosten/Boden;
- Waschplatz-System-/Bauleistung vs. konkretes Serienprodukt.

## Materialisierungsstatus

Diese Akte ist nur source-bound Fachvorarbeit.
Keine Änderung an UPC 0.8.6.
Kein Product-Knowledge-Import.
Kein SEO-/Providerlauf.
Kein Merge.
Kein Publish.
