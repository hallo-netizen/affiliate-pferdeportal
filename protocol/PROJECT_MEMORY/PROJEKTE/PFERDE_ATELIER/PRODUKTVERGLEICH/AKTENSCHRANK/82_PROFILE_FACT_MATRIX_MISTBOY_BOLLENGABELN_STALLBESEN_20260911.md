# PRODUKTVERGLEICH – PROFILE / FACT MATRIX MISTBOY / BOLLENGABELN / STALLBESEN V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Registry-Gruppen:
- `mistboy`;
- `bollengabeln`;
- `stallbesen`.

Mistboy/Bollensammler = zweiteiliges Sammelset. Bollengabel = eigenständige Entmistungsgabel. Stallbesen = Kehrwerkzeug. Diese Klassen dürfen nicht über den gemeinsamen Stallreinigungszweck vermischt werden.

`stallbesen` besitzt einen harten Cross-Group-Overlap zu dem bereits profilierten Registry-Key `hofbesen`: aktuelle Produkte werden ausdrücklich als **Stall- und Hofbesen** geführt. Daher ist Cross-Group-Dedup zwingend; ein zweiter Vergleich nur wegen des Standort-Labels ist unzulässig.

Finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin aus aktuellem Product Knowledge.

---

## 1. Mistboy

Portal-Key / technischer Key:
`mistboy`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound Cross-Brand-V1-Klasse:
`TWO_PIECE_HORSE_MANURE_COLLECTOR_SET_SCOOP_PLUS_RAKE`.

Pflichtmerkmale:
- zweiteiliges Entmistungs-/Bollensammler-Set;
- stehende Schaufel/Sammelwanne;
- separater Rechen/Krücke zum Einschieben des Mists;
- lange Stiele für stehendes Arbeiten;
- Pferdestall/Paddock/Box/Reitplatz oder Pferdeanhänger als Nutzung source-bound;
- als Set verkauft bzw. eindeutig als zusammengehöriges Komplettsystem.

Ausgeschlossen bzw. separate Klassen:
- Bollengabel/Mistgabel allein;
- Schaufel allein;
- Rechen/Krücke allein;
- Mistboy-Kinder-/Mini-Klasse;
- XL-Shaker-/Sieb-Bollensammler als eigene Funktionsunterklasse, wenn Siebboden Teil des Nutzerintents ist;
- Schubkarre/Mistcontainer.

### Aktuelle Hersteller-Evidence

Albert Kerbl GmbH:
- `Mistboy`;
- Schaufel + multifunktionelle Krücke;
- aktuelle Varianten 75 cm bzw. 90 cm;
- Schaufel aus Kunststoff;
- Krücke je Variante Metall oder Kunststoff;
- ausdrücklich für Boxennachlese, Pferdetransporter und Paddockpflege;
- Ersatzschaufel und Ersatzkrücke einzeln erhältlich.

Herstellerquelle:
https://www.kerbl.com/de/produkt/mistboy-13699

Waldhausen GmbH & Co. KG:
- `Bollensammler`, Art.-Nr. 157700;
- ausdrücklich `Zweiteiliges Entmistungs-Set`;
- Nutzung im Stall, Anhänger und auf der Boxengasse;
- Stielhöhe ca. 80 cm.

Herstellerquelle:
https://www.waldhausen.com/bollensammler/157700/

Separate Waldhausen-Unterklasse:
- `XL Bollensammler Shaker mit Rechen`, Art.-Nr. 1577701;
- Siebschlitze im Schaufelboden zum Trennen von Dung und Spänen;
- 40 x 30 x 35 cm Schaufel, 85 cm Gesamthöhe;
- wird wegen der zusätzlichen Siebfunktion nicht still in die einfache Standardklasse eingemischt.

Herstellerquelle:
https://www.waldhausen.com/xl-bollensammler-shaker-mit-rechen/1577701/

### Faktenmatrix V1

1. `collector_set_class`;
2. `horse_stable_use`;
3. `paddock_use`;
4. `trailer_use`;
5. `set_piece_count`;
6. `scoop_included`;
7. `rake_or_crook_included`;
8. `scoop_material`;
9. `rake_material`;
10. `handle_material_scoop`;
11. `handle_material_rake`;
12. `overall_height_mm`;
13. `scoop_width_mm`;
14. `scoop_height_mm`;
15. `scoop_depth_mm`;
16. `sieve_or_shaker_function`;
17. `rake_tine_or_scraper_class`;
18. `replacement_scoop_available`;
19. `replacement_rake_available`;
20. `assembly_required`;
21. `weight_kg`;
22. `available_colors`;
23. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `mistboy`;
- `collector_set_class = TWO_PIECE_HORSE_MANURE_COLLECTOR_SET_SCOOP_PLUS_RAKE`;
- Standard-Sammelset ohne obligatorische Sieb-/Shaker-Sonderfunktion;
- vergleichbare Stiel-/Größenklasse;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

### Decision-Policy

- Set-/Grundfunktionsklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Material, Stielhöhe, Ersatzteile, Montage und Farben: sachliche Unterschiede;
- Sieb-/Shaker-Funktion als eigene Funktionsunterklasse führen;
- keine freie Aussage zu Rückenschonung, Arbeitsgeschwindigkeit, Haltbarkeit oder Ergonomie;
- Herstellerclaims dazu bleiben Herstellerclaims.

---

## 2. Bollengabeln

Portal-Key / technischer Key:
`bollengabeln`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound Cross-Brand-V1-Klasse:
`PLASTIC_HORSE_MANURE_FORK_HEAD_FOR_BEDDING_CLEANING`.

Pflichtmerkmale:
- eigenständiger Kunststoff-Gabelkopf zur Entmistung;
- ausdrücklich für Pferdestall/Box bzw. Einstreu geeignet;
- mehrzinkige Gabelkonstruktion;
- Stiel separat oder als konkret gebundene Variante erhältlich;
- keine Metallgabel als gleiche Materialklasse.

Ausgeschlossen bzw. separate Klassen:
- komplette Mistboy-Schaufel/Rechen-Kombination;
- Metall-/Aluminiumgabel;
- Heu-/Futtergabel mit anderer Zinken-/Nutzungsklasse;
- Mistkratzer/Rechen;
- Schaufel;
- konkrete komplett angestielte Variante gegen Kopf-only, sofern Lieferumfang Nutzerintent ist.

### Aktuelle Hersteller-Evidence

Waldhausen GmbH & Co. KG:
- `Bollengabel Pro`, Art.-Nr. 1501202;
- glasfaserverstärkter Kunststoff;
- für Entmistung von Torf- und Späneeinstreu;
- ca. 38 cm breit, 33 cm tief, 8 cm hoch;
- Stielloch ca. 2,5 cm;
- Gabelkopf als eigenständiges Produkt.

Herstellerquelle:
https://www.waldhausen.com/bollengabel-pro/15012/

Albert Kerbl GmbH:
- `Dunggabel Premium`, u. a. Art.-Nr. 323475/323476 ohne Stiel;
- Spezial-Kunststoffmischung;
- 17 Zinken;
- ausdrücklich für Ausmisten in Pferdebox/Hänger und Stallreinigung;
- Kopf-only-Varianten sowie Varianten mit Aluminiumstiel/D-Griff;
- erhöhte UV-Stabilität und veröffentlichter Temperaturbereich -20 bis +50 °C als Herstellerangabe.

Herstellerquelle:
https://www.kerbl.com/de/produkt/dunggabel-premium-13674

Weitere Kerbl-Unterklasse:
- `Dunggabel Maxi`, Art.-Nr. 326056;
- Kunststoff, 17 Zinken, ca. 38 x 30 cm;
- tieferes Design mit höherem Füllvolumen;
- bleibt als konkrete Bauvariante separat bindbar.

Herstellerquelle:
https://www.kerbl.com/de/produkt/dunggabel-maxi-13690

### Faktenmatrix V1

1. `manure_fork_class`;
2. `horse_stable_use`;
3. `bedding_types_claimed`;
4. `head_material`;
5. `reinforced_material_claim`;
6. `head_width_mm`;
7. `head_depth_mm`;
8. `head_height_mm`;
9. `tine_count`;
10. `tine_geometry`;
11. `raised_side_walls`;
12. `handle_included`;
13. `handle_socket_diameter_mm`;
14. `compatible_handle_materials`;
15. `compatible_handle_length_mm`;
16. `complete_variant_available`;
17. `weight_g_head`;
18. `temperature_range_claim`;
19. `uv_resistance_claim`;
20. `manufacturer_break_load_or_impact_test_claim`;
21. `available_colors`;
22. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `bollengabeln`;
- `manure_fork_class = PLASTIC_HORSE_MANURE_FORK_HEAD_FOR_BEDDING_CLEANING`;
- Kopf-only gegen Kopf-only für die erste V1-Klasse;
- Pferde-/Stall-Entmistung source-bound;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Komplette angestielte Ausführungen können später eine eigene konkrete Variantenklasse bilden. Metallgabeln bleiben getrennt.

### Decision-Policy

- Klasse/Material-/Lieferumfangsklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Zinken, Seitenhöhe, Stielaufnahme, Temperatur-/UV-Claims und Farben: sachliche Unterschiede;
- Bruchlast/Schlagzähigkeit nur mit identischer Prüfmethode direkt vergleichen;
- keine freie Aussage zu Ergonomie, Entmistungsleistung oder Lebensdauer;
- Mistboy-Rechen nicht als Bollengabel klassifizieren.

---

## 3. Stallbesen

Portal-Key / technischer Key:
`stallbesen`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Source-bound Produktklasse:
`ELASTON_STABLE_YARD_PUSH_BROOM_HEAD_50CM`.

Pflichtmerkmale:
- Schub-/Saal-/Stallbesenkopf;
- Arbeitsbreite ca. 50 cm;
- robuste Elaston-Kunststoffborsten;
- ausdrücklich für Stall **und/oder** Hof/Außenbereich geeignet;
- Stiel separat bzw. konkrete Stielaufnahme source-bound.

### Zwingendes Cross-Group-Dedup gegen `hofbesen`

Die Produktklasse überschneidet sich unmittelbar mit dem bereits profilierten Registry-Key `hofbesen`.
Aktuelle Produkte tragen selbst die Bezeichnung `Stall- und Hofbesen` und decken beide Einsatzorte gleichzeitig ab.

Darum gilt vor jeder Paarbildung:
`cross_group_dedup_pass = true` gegen `hofbesen`.

Wenn Produktklasse, konkrete Produkte und Such-/Nutzerintent nur denselben Besenvergleich unter einem anderen Standortwort wiederholen, muss das Ergebnis **0 neuer Vergleich** sein.

Ein eigenständiger `stallbesen`-Vergleich ist nur zulässig, wenn später source-bound eine abweichende technische Stall-Unterklasse oder ein klar eigenständiger SEO-/Nutzerintent belegt wird, ohne denselben Paarvergleich zu duplizieren.

### Aktuelle Evidence

Krämer Pferdesport / SHOWMASTER:
- `Stall- und Hofbesen`, Nr. 450555;
- 50 cm breit;
- rote Elastonborsten;
- Stielhalter für 24-mm-Stiele;
- ohne Stiel;
- Produktname bindet Stall und Hof ausdrücklich gemeinsam.

Quelle:
https://www.kraemer.de/Stalleinrichtung/Stallzubehoer-Reitplatzzubehoer/Sattelkammer/Stall-und-Hofbesen

SOREX:
- `Stall- und Hofbesen`, Art.-Nr. 92000 00001;
- ca. 50 cm Arbeitsbreite;
- Profi-Elaston-Borsten ca. 8 cm;
- unbehandelter Holzkörper;
- Metallhalter 28 mm;
- Einsatz für Stall, Hof und Außenbereiche.

Direktproduktquelle:
https://www.loesdau.de/sorex-stall-und-hofbesen-50-cm-92000-00001.html

### Faktenmatrix V1

1. `broom_class`;
2. `stable_use`;
3. `yard_use`;
4. `cross_group_overlap`;
5. `head_width_mm`;
6. `head_material`;
7. `bristle_material`;
8. `bristle_length_mm`;
9. `bristle_diameter_mm`;
10. `bristle_row_count`;
11. `handle_included`;
12. `handle_socket_diameter_mm`;
13. `handle_holder_material`;
14. `wet_dirt_use_claim`;
15. `outdoor_use_claim`;
16. `weight_g`;
17. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `stallbesen`;
- `broom_class = ELASTON_STABLE_YARD_PUSH_BROOM_HEAD_50CM`;
- 50-cm-Elastonklasse;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle;
- **zusätzlich zwingend:** `cross_group_dedup_pass = true` gegen `hofbesen`.

### Decision-Policy

- Klasse/Arbeitsbreite/Borstenmaterial: `PAIRING_EQUAL_NO_PREFERENCE`;
- Holzkörper, Borstenlänge/-stärke, Stielaufnahme und Lieferumfang: sachliche Unterschiede;
- keine freie Aussage zu Reinigungsleistung, Lebensdauer oder Nässeeignung über Herstellerangaben hinaus;
- kein zweiter Vergleich, wenn dieselben Produkte bereits unter `hofbesen` gegeneinander stehen.

## Globale Negativprüfung

Muss fail-closed bleiben:
- Mistboy/Bollensammler-Set vs. Bollengabel;
- Standard-Mistboy vs. Shaker-/Siebschaufel-Unterklasse ohne bewusstes Subtyp-Gate;
- Bollengabel-Kopf vs. komplette angestielte Variante, wenn Lieferumfang Teil des Intents ist;
- Kunststoff-Bollengabel vs. Metallgabel;
- Stallbesen vs. Hofbesen als doppelter Vergleich derselben 50-cm-Elastonprodukte;
- Haushalts-/Innenraumbesen vs. Stall-/Hofklasse.

## Materialisierungsstatus

Diese Akte ist nur source-bound Fachvorarbeit.
Keine Änderung an UPC 0.8.6.
Kein Product-Knowledge-Import.
Kein SEO-/Providerlauf.
Kein Merge.
Kein Publish.
