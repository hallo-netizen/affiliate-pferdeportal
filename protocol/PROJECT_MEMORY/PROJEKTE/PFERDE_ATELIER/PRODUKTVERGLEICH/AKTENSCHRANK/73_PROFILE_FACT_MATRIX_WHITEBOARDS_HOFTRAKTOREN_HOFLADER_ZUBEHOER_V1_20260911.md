# PRODUKTVERGLEICH – PROFILE / FACT MATRIX WHITEBOARDS / HOFTRAKTOREN / HOFLADER-ZUBEHÖR V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Registry-Gruppen:
- `whiteboards-fuer-stallplanung`;
- `hoftraktoren`;
- `hoflader-zubehoer`.

Die Gruppen werden nur innerhalb einer exakt gebundenen Nutzungs-/Konstruktionsklasse gepaart.
Finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin aus aktuellem Product Knowledge.

---

## 1. Whiteboards für Stallplanung

Portal-Key:
`whiteboards-fuer-stallplanung`

Technischer Key:
`whiteboards-fuer-stallplanung`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound Cross-Brand-V1-Klasse:
`MULTI_HORSE_WEEKLY_STABLE_PLANNING_WHITEBOARD`.

Pflichtmerkmale:
- physisches Whiteboard/Planboard für Stallorganisation;
- mehrere Pferde bzw. Stallteam als Planungsumfang;
- Wochen-/Tagesraster für wiederkehrende Stallaufgaben oder Pferdeaktivitäten;
- beschreibbar und wieder abwischbar;
- zentrale Stallplanung, nicht nur eine einzelne Pferdebox.

Ausgeschlossen bzw. separate Klassen:
- Einzelbox-Stalltafel -> `stalltafeln`;
- Einzelpferd-Futtertafel -> `futterkarten-und-boxenschilder`;
- statisches Namensschild;
- rein digitales Stallmanagement/App/Touchscreen;
- allgemeines Büro-Whiteboard ohne gebundene Stallplanungs-/Pferdeplanungskonfiguration;
- Monats-/Jahreskalender ohne gleiche Wochen-/Pferde-Matrix.

### Aktuelle Hersteller-/Direktprodukt-Evidence

Kentucky Horsewear / Grooming Deluxe:
- `Stallplaner mit magnetischem Rahmen`, Ref. `82221-100X84`;
- 100 x 84 cm;
- explizit pro Pferd und pro Tag für die kommende Woche;
- Bereiche für Hufschmiedtermine, tägliche Aufgaben und Notizen;
- magnetische Oberfläche;
- mit Whiteboard-Stiften beschreibbar und abwischbar;
- Bambusrahmen.

Herstellerquelle:
https://www.kentucky-horsewear.com/lu-de/eur/82221-100x84/stallplaner-magnetisch-mit-rahmen-100x84cm/

Equi Boutique / Jule Reimers:
- `individuelle Stalltafel / Whiteboard / Futterplan mit Logo`;
- Hersteller beschreibt ausdrücklich ein Whiteboard zur Organisation des Stallalltags bei vielen Pferden;
- als Wochenplaner für den Stall individuell konfigurierbar;
- Aufgabenlisten, Fütterungspläne, Tierarzttermine und weitere Stallinformationen möglich;
- abwischbar;
- Größen von 50 x 50 cm bis 200 x 100 cm in der aktuellen Auswahl, weitere Größen laut Anbieter möglich;
- optionale Lochbohrungen.

Direktproduktquelle:
https://equi-boutique.de/products/stalltafel-whiteboard

### Faktenmatrix V1

1. `planning_board_class`;
2. `horse_scope`;
3. `weekly_grid`;
4. `daily_columns`;
5. `horse_rows_or_capacity`;
6. `customizable_layout`;
7. `magnetic_surface`;
8. `rewritable`;
9. `wipe_clean_method`;
10. `width_mm`;
11. `height_mm`;
12. `frame_material`;
13. `board_material`;
14. `mounting_method`;
15. `mounting_holes_available`;
16. `included_marker_or_accessories`;
17. `outdoor_use_claim`;
18. `warranty`.

Nicht veröffentlichte Pferdekapazität, Kratzfestigkeit oder Wetterbeständigkeit bleiben `NOT_IN_SOURCE`.

### Pairing-Regeln

- gleiche Gruppe `whiteboards-fuer-stallplanung`;
- `planning_board_class = MULTI_HORSE_WEEKLY_STABLE_PLANNING_WHITEBOARD`;
- physisches wiederbeschreibbares Board;
- Mehrpferde-/Stallteam-Planung;
- Wochenraster bzw. konkret gebundene Wochenkonfiguration;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Bei frei konfigurierbaren Boards muss die konkrete Wochen-/Mehrpferde-Konfiguration im Product Knowledge gebunden sein. Die bloße Produktfamilie reicht nicht.

### Decision-Policy

- Klasse/Planungsumfang/Wochenfunktion: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Magnetfunktion, Rahmen, Individualisierung, Montage und Zubehör: sachliche Unterschiede;
- keine freie Aussage zu Zeitersparnis, Fehlervermeidung, Teamkommunikation, Haltbarkeit oder Outdoor-Eignung;
- Anbieterclaims zu Organisationseffizienz bleiben Herstellerclaims;
- keine digitale Lösung gegen ein physisches Board paaren.

---

## 2. Hoftraktoren

Portal-Key:
`hoftraktoren`

Technischer Key:
`hoftraktoren`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound Cross-Brand-V1-Klasse:
`COMPACT_DIESEL_TRACTOR_24_26_HP_STAGE_V_MANUAL_CAT1`.

Pflichtmerkmale:
- kompakter Traktor/Kleintraktor;
- 3-Zylinder-Dieselmotor;
- Stage V;
- Nennleistung 24–26 PS;
- mechanisches Schaltgetriebe;
- Heckhubwerk Kategorie 1 bzw. 1N;
- Nutzung für leichte Hof-/Grundstücks-/Kommunal-/Mäh-/Landschaftsarbeiten source-bound.

Ausgeschlossen bzw. separate Klassen:
- Hoflader/Radlader/Teleskoplader;
- UTV/ATV;
- Rasentraktor ohne vergleichbares Heckhubwerk;
- hydrostatische Variante gegen mechanische Variante, wenn Getriebeart Teil des konkreten Nutzerintents ist;
- deutlich höhere Leistungsklasse;
- rein elektrische Traktoren;
- Kommunalgerät ohne Traktor-Grundklasse.

### Aktuelle Hersteller-Evidence

Kubota / EK1-261:
- 3-Zylinder Mitsubishi-Diesel;
- Stage V;
- Herstellerseiten nennen rund 24–24,8 PS;
- mechanisches 9V/3R-Getriebe;
- Heckkraftheber Kategorie 1N;
- Arbeitshydraulik 20 l/min;
- leichte Arbeiten, Mähen, Landschaftsbau und kommunale Arbeiten als Herstelleranwendungen.

Herstellerquellen:
https://ek.kubota-eu.com/kubota-ek1-series-ch-de
https://kdg.kubota-eu.com/groundcare/series/ek1/

Quellenhinweis:
Die aktuelle Kubota-Seite enthält bei der Hubkraft unterschiedliche Bezugs-/Zahlenangaben in Fließtext und Tabelle. Hubkraft wird deshalb für diese V1-Spec **nicht** als direktes Gewinner-/Decision-Feld verwendet, bis Messpunkt/Definition eindeutig source-bound normalisiert ist.

ISEKI / TM 3267 AL ECO Bügel:
- ISEKI 3-Zylinder-Diesel;
- 1.498 cm³;
- 25,7 PS nach ECE R120;
- Stage V;
- Schaltgetriebe;
- 4 Vorwärts-/4 Rückwärtsgänge je Gruppe, 2 Gruppen laut Herstellerdaten;
- Heckzapfwelle 540 U/min;
- Heckhubwerk Kat. 1;
- durchgängige Hubkraft am Koppelpunkt 600 kg;
- Arbeitshydraulik 20,8 l/min;
- Breite 1.099–1.260 mm je Bereifung;
- Gewicht 870 kg mit Standardbereifung.

Herstellerquelle:
https://www.iseki.de/produkte/tm-32-kompakt/uebersicht

### Faktenmatrix V1

1. `vehicle_class`;
2. `engine_type`;
3. `cylinder_count`;
4. `displacement_cm3`;
5. `rated_power_kw`;
6. `rated_power_hp`;
7. `emission_stage`;
8. `transmission_class`;
9. `forward_gears`;
10. `reverse_gears`;
11. `max_speed_kmh`;
12. `rear_pto_rpm`;
13. `rear_hitch_category`;
14. `rear_lift_capacity_kg`;
15. `rear_lift_measurement_point`;
16. `working_hydraulic_flow_l_min`;
17. `steering_hydraulic_flow_l_min`;
18. `overall_length_mm`;
19. `overall_width_mm`;
20. `overall_height_mm`;
21. `operating_weight_kg`;
22. `tire_options`;
23. `front_loader_or_front_lift_option`;
24. `manufacturer_intended_uses`;
25. `warranty`.

Zahlenwerte mit unterschiedlichen Normen/Messpunkten dürfen nicht direkt als besser/schlechter gewertet werden.

### Pairing-Regeln

- gleiche Gruppe `hoftraktoren`;
- `vehicle_class = COMPACT_TRACTOR`;
- Diesel, 3 Zylinder, Stage V;
- 24–26 PS;
- mechanische Getriebeklasse;
- Heckhubwerk Kat. 1/1N;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Hydrostatische Varianten, Kabinenvarianten oder abweichende Leistungsstufen sind konkrete Varianten und müssen separat im Product Knowledge gebunden werden.

### Decision-Policy

- Fahrzeug-/Leistungs-/Getriebe-/Hubwerksklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Motorvolumen, Gänge, Hydraulikfluss, Maße, Gewicht und Optionen: sachliche Unterschiede;
- Hubkraft nur bei identischem Messpunkt/Norm direkt vergleichen;
- keine freie Aussage zu Zugkraft, Verbrauch, Zuverlässigkeit, Wartungskosten, Wendigkeit oder Eignung für einen konkreten Stall;
- Herstellerclaims zu Robustheit/Produktivität bleiben Herstellerclaims;
- keine Hofladerfunktion aus optionalem Frontlader ableiten.

---

## 3. Hoflader Zubehör

Portal-Key:
`hoflader-zubehoer`

Technischer Key:
`hoflader-zubehoer`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Der Registry-Key ist ein Zubehör-Oberbegriff. Akte 51 verlangt Pflicht-Subtyp vor Pairing.

Erste source-bound Cross-Brand-V1-Klasse:
`STANDARD_ADJUSTABLE_PALLET_FORK_FOR_COMPACT_WHEEL_LOADER`.

Pflichtmerkmale:
- Anbaugerät Palettengabel;
- für Kompakt-/Hof-/Radlader-Produktprogramm des Herstellers;
- zwei Gabelzinken;
- Zinkenbreite mechanisch/verstellbar innerhalb des Rahmens;
- keine hydraulische Zinkenverstellung als Pflichtfunktion der ersten V1-Klasse;
- keine Greif-, Ballen- oder Schaufelfunktion als primärer Zweck.

Ausgeschlossen bzw. separate Subtypen:
- Schaufel;
- Greifschaufel;
- Krokodilgebiss;
- Ballenspieß;
- Rundballenzange;
- Kehrmaschine/Kehrbesen;
- Mäher;
- Futterschiebeschild;
- hydraulisch verstellbare Spezial-Palettengabel;
- klappbare Palettengabel, wenn der Nutzerintent genau diese Straßen-/Klappfunktion betrifft.

### Aktuelle Hersteller-Evidence

Weidemann:
- aktuelle `Palettengabel` im Anbaugeräteprogramm;
- Transport von Gütern auf Paletten;
- Zinken in der Breite verstellbar;
- Schutzbalken;
- Breiten je Variante 1.000–2.000 mm;
- Traglasten je Variante 2.000–5.500 kg;
- Gewichte je Variante 140–470 kg;
- für zahlreiche Hoftrac-/Rad-/Teleskopladermodelle empfohlen.

Herstellerquelle:
https://www.weidemann.de/produkte/hoflader/hoftrac-1280/anhang/326/uberblick/tab

Schäffer Maschinenfabrik GmbH:
- aktuelle `Palettengabel`;
- für Kompaktlader sowie Rad-/Teleradlader;
- optionale weitere Zinkenlängen, Rahmen und hydraulische Zinken-/Seitenverstellung;
- Standardvarianten Kompaktlader z. B. 2,5 t Kapazität, 1,00/1,20 m Zinkenlänge, 1,00/1,20 m Breite, 150–190 kg je Ausführung;
- Rad-/Teleradlader-Varianten 3,5–4,5 t mit weiteren Abmessungen.

Herstellerquelle:
https://www.schaeffer.de/produkte/53/palettengabel

### Faktenmatrix V1

1. `attachment_subtype`;
2. `loader_class_compatibility`;
3. `coupler_or_mount_system`;
4. `fork_count`;
5. `fork_length_mm`;
6. `frame_width_mm`;
7. `fork_spacing_adjustment`;
8. `hydraulic_adjustment`;
9. `side_shift`;
10. `foldable_forks`;
11. `rated_capacity_kg`;
12. `capacity_measurement_condition`;
13. `attachment_weight_kg`;
14. `material`;
15. `protective_backrest`;
16. `required_hydraulic_circuit`;
17. `recommended_loader_models`;
18. `road_use_claim_or_restriction`;
19. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `hoflader-zubehoer`;
- `attachment_subtype = PALLET_FORK`;
- gleiche normalisierte Grundklasse ohne obligatorische hydraulische Sonderfunktion;
- konkret kompatible Lader-/Aufnahmeklasse muss im Product Knowledge gebunden sein;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

**Kompatibilitätsgate:**
Ein Weidemann-Anbaugerät und ein Schäffer-Anbaugerät sind nicht deshalb austauschbar, weil beide `Palettengabel` heißen. Das Plugin darf nur konkrete Produkte vergleichen; technische Montagekompatibilität mit einer fremden Lademarke wird **nicht** behauptet. Der Vergleich betrifft Produktkonstruktion innerhalb derselben Zubehörklasse, nicht Cross-Mount-Austauschbarkeit.

### Decision-Policy

- Anbaugerät-/Funktionsklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Zinkenlänge, Rahmenbreite, Kapazität, Gewicht und Einstelloptionen: sachliche Unterschiede;
- Traglast nur bei vergleichbarer Definition/Bedingung direkt werten;
- keine freie Aussage zu Lebensdauer, Sicht, Sicherheit, Produktivität oder Verschleiß;
- Herstellerclaims zu Spezialstahl/Verschleiß bleiben Herstellerclaims;
- keine systemfremde Laderkompatibilität erfinden.

## Globale Verbote für alle drei Gruppen

- kein Einzelbox-Board gegen Mehrpferde-Stallplaner;
- kein Hoflader/UTV gegen Kompakttraktor;
- kein Zubehör-Oberbegriff ohne Pflicht-Subtyp;
- keine Cross-Brand-Anbaukompatibilität erfinden;
- kein Gesamtsieger;
- keine Punkte/Sterne/Rankings;
- keine Shop-/Affiliate-Verfügbarkeit als Fachargument;
- keine Leistungs-, Sicherheits-, Haltbarkeits-, Verbrauchs- oder Produktivitätswertung ohne direkt vergleichbare Evidenz;
- Quellenlücke bleibt `NOT_IN_SOURCE`.

## Produktvalidierung gegen die Profilspec

Fresh source-bound Gegenprüfung 2026-09-11:

- `whiteboards-fuer-stallplanung`: Kentucky/Grooming Deluxe 82221 + Equi Boutique individuelle Stalltafel belegen zwei unabhängige physische, wiederbeschreibbare Mehrpferde-Stallplanungsboards; bei Equi Boutique muss die konkrete Wochenplan-Konfiguration im Product Knowledge gebunden werden;
- `hoftraktoren`: Kubota EK1-261 + ISEKI TM 3267 AL ECO belegen zwei unabhängige Stage-V-Kompakttraktorfamilien in der 24–26-PS-/mechanischen/Kat.-1-Klasse; Hubkraft bleibt wegen unterschiedlicher Mess-/Quellenangaben kein ungeprüfter Gewinnerfakt;
- `hoflader-zubehoer`: Weidemann Palettengabel + Schäffer Palettengabel belegen zwei unabhängige Produktfamilien derselben Palettengabel-Funktionsklasse; konkrete Varianten und Laderkompatibilität bleiben Product-Knowledge-Pflicht.

Das ist keine finale Paarfreigabe und keine Markt-Vollständigkeit.

## Technische Materialisierungsgrenze

Dieses Dokument ändert `comparison-profiles.json` nicht.

Die Spezifikationen aus Akten 62–73 bleiben source-bound gesammelt. Vor technischer Materialisierung muss Product Knowledge pro Produkt/Variante die Klassenbindung und Pflichtfakten tragen.

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
