# PRODUKTVERGLEICH – PROFILE / FACT MATRIX NACHSaat PFERDEWEIDEN / WEIDESCHLEPPEN / UNKRAUTSTECHER V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Autoritative Registry-Folge:
- `p172 nachsaat-fuer-pferdeweiden`;
- `p173 weideschleppen`;
- `p174 unkrautstecher`;
- danach `p175 weidewalzen`;
- danach `p176 solar-weidepumpen`;
- `p177 weidebrunnen` = gemäß finaler 175er Disposition `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`.

Daraus folgt zwingend:
- p172 wird in V1 als **Saatgutmischung zur Nachsaat bestehender Pferdeweiden** profiliert, nicht als Nachsaatmaschine;
- Maschinen-/Striegelkonfigurationen bleiben in den Gerätekeys p171/p173 bzw. eigener technischer Unterklasse; Saatgut und Maschine werden nie gegeneinander verglichen;
- p173 wird als passive Gussstern-/Netz-Grünlandegge bzw. Wiesenschleppe profiliert und strikt vom Federzinken-Grünlandstriegel p171 getrennt;
- p174 wird in der Weideausstattung zuerst als **langstieliger Ampfer-/Pfahlwurzelstecher für Grünland/Weide** geöffnet, nicht als allgemeiner Garten-Löwenzahnstecher;
- finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin aus aktuellem Product Knowledge.

---

## 1. Nachsaat für Pferdeweiden

Portal-Key / technischer Key:
`nachsaat-fuer-pferdeweiden`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound V1-Klasse:
`HORSE_PASTURE_RESEEDING_GRASS_SEED_MIX`.

Pflichtmerkmale:
- physisches Saatgutprodukt;
- ausdrücklich für Pferdeweiden/Pferdegrünland;
- ausdrücklich für Nachsaat, Durchsaat oder Übersaat bestehender Bestände;
- keine reine Neuanlage-Mischung als direktes Paar;
- Arten-/Mischungszusammensetzung und Saatmengenempfehlung source-bound;
- aktueller Produkt-/Mischungsstatus.

Ausgeschlossen bzw. separate Klassen:
- Nachsaat-/Sämaschine;
- Grünlandstriegel mit aufgebautem Sägerät;
- reine Neuanlage-Pferdeweidenmischung;
- Kräuterergänzung ohne vollständige Nachsaatfunktion;
- allgemeine Rasen-/Sportplatzmischung;
- Sondermischung mit anderem Hauptintent wie Rennbahn, Heu oder gezielte Spezialernährung, sofern Nachsaat nicht der gleiche Nutzerintent ist.

### Aktuelle Hersteller-Evidence

Feldsaaten Freudenberger – `ProGreen® PF 30 Pferdeweide Nachsaat`:
- ausdrücklich zur Nachsaat lückiger/stark beanspruchter Pferdeweiden;
- Gebinde 10 kg;
- Saatstärke 30–40 kg/ha;
- Zusammensetzung laut aktueller Herstellerseite:
  - 40 % Deutsches Weidelgras Futtertyp spät;
  - 20 % Deutsches Weidelgras Futtertyp mittel;
  - 18 % Wiesenlieschgras;
  - 12 % Deutsches Weidelgras Rasentyp;
  - 10 % Wiesenrispe Futtertyp;
- Art.-Nr. 40705.

Herstellerquelle:
https://www.freudenberger.net/landwirtschaft/produkte/mischung/progreen-pf-30-pferdeweide-nachsaat

Deutsche Saatveredelung AG – `COUNTRY Horse 2118 Nachsaat Pferdegreen`:
- ausdrücklich Nachsaatmischung für Pferdeweiden;
- aktuelle HTML-Zusammensetzung:
  - 40 % Deutsches Weidelgras Rasentyp;
  - 20 % Deutsches Weidelgras früh;
  - 20 % Deutsches Weidelgras mittel;
  - 20 % Wiesenlieschgras;
- Aussaatform `Nachsaat`;
- Aussaatstärke/Durchsaat 20–25 kg/ha;
- Übersaat 5–7 kg/ha, mehrmalig;
- Aussaatzeit März bis September;
- DSV weist selbst darauf hin, dass Mischungszusammensetzungen bei Sortennichtverfügbarkeit geändert werden können; deshalb muss die Zusammensetzung bei Refresh neu gebunden werden.

Herstellerquelle:
https://www.dsv-saaten.de/sorte/1338

### Faktenmatrix V1

1. `seed_mix_class`;
2. `horse_pasture_use_explicit`;
3. `reseeding_use_explicit`;
4. `new_sowing_use_explicit`;
5. `overseeding_use_explicit`;
6. `drill_reseeding_use_explicit`;
7. `package_weight_kg`;
8. `recommended_reseeding_rate_min_kg_ha`;
9. `recommended_reseeding_rate_max_kg_ha`;
10. `recommended_overseeding_rate_min_kg_ha`;
11. `recommended_overseeding_rate_max_kg_ha`;
12. `seeding_window_start_month`;
13. `seeding_window_end_month`;
14. `species_count`;
15. `perennial_ryegrass_total_pct`;
16. `perennial_ryegrass_turf_type_pct`;
17. `perennial_ryegrass_early_pct`;
18. `perennial_ryegrass_medium_pct`;
19. `perennial_ryegrass_late_pct`;
20. `timothy_pct`;
21. `meadow_bluegrass_pct`;
22. `other_species_pct`;
23. `composition_revision_date_or_status`;
24. `current_lifecycle`.

### Pairing-Regeln

- gleiche Gruppe `nachsaat-fuer-pferdeweiden`;
- `seed_mix_class = HORSE_PASTURE_RESEEDING_GRASS_SEED_MIX`;
- Nachsaat bestehender Pferdeweiden als gleicher Hauptintent;
- Saatmengen immer nach gleicher Aussaatform vergleichen: Nachsaat/Durchsaat != Übersaat;
- aktuelle Zusammensetzung beider Mischungen source-bound;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

**Fail-closed:**
Freudenberger PF 30 und DSV COUNTRY Horse 2118 belegen dieselbe Nachsaat-Produktklasse. Ihre Saatmengen dürfen nur auf gleicher Aussaatform verglichen werden; die DSV-Übersaat-Angabe 5–7 kg/ha ist nicht direkt mit Freudenbergers allgemeiner Nachsaat-Saatstärke 30–40 kg/ha gleichzusetzen. Mischungsanteile bleiben bei jedem Refresh neu zu prüfen, weil Hersteller Zusammensetzungen ändern können.

### Decision-Policy

- Pferdeweide-/Nachsaat-Grundintent: `PAIRING_EQUAL_NO_PREFERENCE`;
- Artenzusammensetzung, Saatmengen, Aussaatform, Aussaatfenster und Gebinde: sachliche Unterschiede;
- keine freie Aussage zu Fruktan, Hufreheprophylaxe, Gesundheit, Futterwert, Schmackhaftigkeit, Trittfestigkeit oder Ertrag als Produktsieg ohne vergleichbare unabhängige Evidenz;
- Herstellerclaims getrennt kennzeichnen;
- Neuanlage nicht gegen Nachsaat ranken.

---

## 2. Weideschleppen

Portal-Key / technischer Key:
`weideschleppen`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound V1-Klasse:
`3M_THREE_POINT_THREE_ROW_CAST_STAR_GRASSLAND_DRAG_HARROW`.

Pflichtmerkmale:
- passive Grünland-/Wiesenegge bzw. Wiesenschleppe;
- 3,0-m-Arbeitsbreitenklasse;
- Dreipunktanbau;
- dreireihiges Gussstern-/Netzsystem;
- keine Federzinken-Striegelarchitektur;
- ausdrücklich für Wiesen/Grünland;
- Arbeits-/Transportbreite, Gewicht und Gussstern-/Reihenklasse source-bound.

Ausgeschlossen bzw. separate Klassen:
- Federzinken-Grünlandstriegel -> `weidepflegegeraete` p171;
- Nachsaatstriegel/Sägerät -> p172-Intent nicht duplizieren;
- Reitplatzschleppe ohne Grünlandhauptintent;
- Wiesenwalze -> p175;
- Schleppmatte ohne definierte 3-m-Dreipunkt-Gusssternklasse als direktes Paar;
- 4-reihige oder hydraulisch geklappte Großgeräte gegen 3-m/3-reihig nur aufgrund des Namens `Weideschleppe`.

### Aktuelle Hersteller-/Produkt-Evidence

Düvelsdorf – `Grünlandegge 3 m, 3-reihig`:
- ausdrücklich für Wiesen;
- 3,0 m Arbeitsbreite;
- 3-reihig;
- Dreipunktanbau;
- Kombisterne aus Guss und Stahlringe;
- Transportbreite 1,75 m;
- Gewicht 220 kg;
- Art.-Nr. 2517300 auf aktueller Herstellerseite.

Herstellerquelle:
https://www.duevelsdorf.de/produkte/arbeitsgeraete/gruenlandeggen/gruenlandeggen

SAPHIR Maschinenbau – `Grünlandegge Perfekt W`, konkrete 3-m-Familie `Perfekt 300 W`:
- aktuelle Herstellerfamilie mit dreireihigem W-Gusssternnetz;
- W-Gusssterne ca. 2,5 kg laut aktueller Hersteller-Produktinformation;
- beidseitige Nutzung der Sterne für schärferes Eggen bzw. Glattseite;
- Perfekt-300-W-Modell ist aktuelle 3-m-Ausführung der Familie;
- konkrete Variantendaten wie Gusssternanzahl, Anbaukategorie, Transportbreite, Gewicht und Kraftbedarf müssen vor finalem Pairing aus aktueller produktbezogener Datenquelle gemeinsam gebunden werden; nicht aus alten Katalogständen interpolieren.

Herstellerquelle:
https://www.saphir-maschinenbau.de/
Aktuelle Hersteller-Produktinformation:
https://www.saphir-maschinenbau.de/wp-content/uploads/Prospekt_Gruenlandtechnik.pdf

Aktueller Produkt-/Marktbeleg für `Perfekt 300 W`:
https://www.agrar-profi24.de/landtechnik/erntetechnik/wieseneggen/gruenlandegge-perfekt-w-wiesenegge_213895_23183

### Faktenmatrix V1

1. `grassland_drag_class`;
2. `grassland_use_explicit`;
3. `spring_tine_harrow`;
4. `cast_star_net_present`;
5. `row_count`;
6. `working_width_m`;
7. `transport_width_m`;
8. `attachment_class`;
9. `weight_kg`;
10. `cast_star_count`;
11. `cast_star_weight_kg`;
12. `cast_star_material`;
13. `ring_material`;
14. `reversible_star_use`;
15. `front_levelling_frame_class`;
16. `mechanical_folding`;
17. `hydraulic_folding`;
18. `required_tractor_power_kw`;
19. `required_tractor_power_hp`;
20. `working_speed_min_kmh`;
21. `working_speed_max_kmh`;
22. `current_lifecycle`.

### Pairing-Regeln

- gleiche Gruppe `weideschleppen`;
- `grassland_drag_class = 3M_THREE_POINT_THREE_ROW_CAST_STAR_GRASSLAND_DRAG_HARROW`;
- 3,0-m-Arbeitsbreite;
- dreireihiges Gusssternnetz;
- gleiche Dreipunkt-/Anbauklasse muss beidseitig konkret gebunden sein;
- Serienausstattung von Zubehör trennen;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

**Fail-closed:**
Düvelsdorf 3 m/3-reihig und SAPHIR Perfekt 300 W belegen dieselbe mechanische Oberklasse. Ein konkretes Paar bleibt aber gesperrt, bis bei SAPHIR die aktuelle konkrete 300-W-Variante mit Anbaukategorie, Gewicht, Gusssternanzahl und Transportbreite auf demselben Produktstand gebunden ist. Historische oder widersprüchliche Händler-/Kataloggewichte werden nicht als Siegerfeld benutzt.

### Decision-Policy

- 3-m-/3-reihige Gussstern-Grundklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Gewicht, Sternanzahl/-geometrie, Transportbreite, Anbaukategorie, Klappung, Leistungsbedarf und Rahmen-/Einebnungsarchitektur: sachliche Unterschiede;
- keine freie Aussage zu Grasnarbenqualität, Belüftung, Ertrag oder Haltbarkeit ohne vergleichbare Prüfmethode;
- p171-Federzinkenstriegel nicht duplizieren.

---

## 3. Unkrautstecher

Portal-Key / technischer Key:
`unkrautstecher`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Aufgrund der Registry-Einordnung unter Weideausstattung erste source-bound V1-Klasse:
`LONG_HANDLE_FORGED_DOCK_ROOT_WEEDER_FOR_GRASSLAND_PASTURE`.

Pflichtmerkmale:
- langstieliges manuelles Wurzelstecher-Werkzeug;
- ausdrücklich für Ampfer bzw. tiefwurzelnde Unkräuter;
- Grünland/Wiese/Weide als ausdrücklicher Einsatzbereich;
- T-Stiel/T-Griff oder funktional vergleichbare Langstiel-Hebelklasse;
- geschmiedete bzw. robuste Stahl-Stech-/Zinkenklasse;
- chemiefreie Einzelpflanzenentfernung als mechanische Hauptfunktion;
- Gesamtlänge, Zinken-/Stechtiefe, Gewicht soweit veröffentlicht source-bound.

Ausgeschlossen bzw. separate Klassen:
- allgemeiner Garten-Löwenzahnstecher ohne belegten Weide-/Grünlandintent;
- kurzer Hand-Unkrautstecher;
- Fußpedal-Greifarm-Gartenstecher als andere Mechanikklasse;
- Herbizid-/chemische Unkrautbekämpfung;
- motorisiertes Gerät;
- Flächenstriegel/-schleppe.

### Aktuelle Hersteller-/Produkt-Evidence

Albert Kerbl GmbH – `Ampferstecher`, Art.-Nr. 29099:
- ausdrücklich zur Bekämpfung von Ampfer im Grünland;
- Entfernung der ganzen Wurzel als Herstellerfunktion;
- T-Stiel;
- geschmiedeter Stahl;
- Hersteller führt das Produkt aktuell.

Herstellerquelle:
https://www.kerbl.com/de/product/ampferstecher/198266/115416

Aktueller Händler-/Produktbeleg für Maße derselben Kerbl-Art.-Nr.:
- Länge 122 cm;
- Breite 19 cm;
- Gewicht ca. 2,5 kg.

Quelle:
https://www.weidezaun.info/ampferstecher-aus-stahl-mit-t-stiel-robuster-unkrautentferner.html

KRENHOF – `Ampferstecher` / geschmiedete Handwerkzeugfamilie:
- KRENHOF führt Ampferstecher als eigene aktuelle Werkzeuggruppe;
- konkrete aktuelle Händler-/Produktbelege weisen den Original-KRENHOF-Ampferstecher für Grünland/Biolandwirtschaft aus;
- ca. 1,20 m Gesamtlänge;
- T-Stiel;
- geschmiedetes Stechblatt / gehärtete geschliffene Zinken;
- je nach aktuellem produktbezogenem Beleg ca. 2,1 kg und Zinkenlänge 17 cm; andere Händlerstände nennen abweichende Maße, daher müssen Variantennummer und Messstand vor Pairing gebunden werden.

Herstellerseite:
https://www.daswerkzeug.at/
Aktueller Produktbeleg:
https://www.siepmann.net/Ampferstecher.html

### Faktenmatrix V1

1. `weed_puller_class`;
2. `dock_control_use_explicit`;
3. `grassland_use_explicit`;
4. `pasture_use_explicit`;
5. `manual_mechanical`;
6. `handle_class`;
7. `handle_material`;
8. `overall_length_mm`;
9. `working_width_mm`;
10. `weight_kg`;
11. `head_material`;
12. `forged_steel_claim`;
13. `tine_count`;
14. `tine_length_mm`;
15. `working_depth_mm`;
16. `tine_hardened_claim`;
17. `tine_sharpened_claim`;
18. `foot_step_present`;
19. `root_removal_mechanism_class`;
20. `organic_farming_claim`;
21. `current_lifecycle`.

### Pairing-Regeln

- gleiche Gruppe `unkrautstecher`;
- `weed_puller_class = LONG_HANDLE_FORGED_DOCK_ROOT_WEEDER_FOR_GRASSLAND_PASTURE`;
- ausdrücklicher Grünland-/Weide-/Ampferintent;
- gleiche Langstiel-/Zinken-/Hebelmechanik;
- Variantennummer bzw. konkrete Produktidentität bei Maße-/Gewichtsvergleich gebunden;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

**Fail-closed:**
Kerbl 29099 und KRENHOF Ampferstecher belegen dieselbe weidespezifische Wurzelstecherklasse. Ein konkretes Paar darf Maße, Gewicht oder Zinkenlänge erst verwenden, wenn die konkrete KRENHOF-Variante und der jeweilige aktuelle Datenstand widerspruchsfrei gebunden sind. Allgemeine Gartenstecher von GARDENA/WOLF/Fiskars bleiben für diese erste V1-Weideklasse ausgeschlossen, auch wenn sie ebenfalls Unkraut im Stehen entfernen.

### Decision-Policy

- Grünland-/Ampfer-/Langstiel-Wurzelstecher-Grundklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Gewicht, Zinkenanzahl/-tiefe, Material, Tritt-/Hebelarchitektur und Ersatzstielverfügbarkeit: sachliche Unterschiede;
- keine freie Aussage zu vollständiger Wurzelentfernung, Arbeitserleichterung, Rückenschonung oder Wirksamkeit als Produktsieg ohne vergleichbare Prüfung;
- Biobetrieb-/chemiefrei-Claims nur als Hersteller-/Einsatzclaim führen.

---

## Akte-87-Negativcheck

PASS:
- p172–p177 direkt gegen autoritative Registry-Folge geprüft;
- p172 Saatgutprodukt klar von Nachsaatmaschine/Grünlandtechnik getrennt;
- Freudenberger und DSV auf aktuelle Hersteller-HTML-Fakten zu Nachsaatintent, Zusammensetzung und Saatmengen geprüft;
- p173 Gussstern-/Netz-Weideschleppe strikt von p171 Federzinken-Grünlandstriegel getrennt;
- SAPHIR-Produktdaten mit potentiell wechselnden Händler-/Katalogständen nicht blind als harte aktuelle Variantensiegerwerte übernommen;
- p174 Registry-Kontext Weideausstattung berücksichtigt und erste Klasse auf Ampfer-/Pfahlwurzelstecher für Grünland/Weide eingegrenzt;
- allgemeine Garten-Unkrautstecher trotz ähnlicher Bezeichnung nicht in die erste p174-Klasse gezogen;
- p177 `weidebrunnen` bleibt V1-NOT-APPLICABLE;
- keine finale konkrete Paarentscheidung manuell festgeschrieben;
- keine technische Materialisierung;
- kein SEO;
- kein Writer/Draft/Publish;
- kein Codex;
- kein Merge;
- kein Publish.

OFFEN:
- technische UPC-Materialisierung dieser drei Profile;
- SAPHIR Perfekt 300 W konkrete aktuelle Variantendaten auf einem konsistenten Produktstand binden;
- KRENHOF konkrete Varianten-/Maßdaten vor Nutzung als Entscheidungskriterien normalisieren;
- vollständige technische Positiv-/Negativ-/Mutation-/Fresh-ZIP-Prüfung erst nach gebündelter Materialisierung;
- WordPress-Live-Test UPC 0.8.6 unverändert offen.

## Nächster Registry-Einstieg nach Akte 87

1. `p175 weidewalzen`;
2. `p176 solar-weidepumpen`;
3. `p177 weidebrunnen` -> V1-NOT-APPLICABLE, überspringen.

Vor dem nächsten Block den nächsten fachlich zulässigen Key hinter p177 frisch aus der Registry lesen.

Keine Materialisierung in dieser Akte.