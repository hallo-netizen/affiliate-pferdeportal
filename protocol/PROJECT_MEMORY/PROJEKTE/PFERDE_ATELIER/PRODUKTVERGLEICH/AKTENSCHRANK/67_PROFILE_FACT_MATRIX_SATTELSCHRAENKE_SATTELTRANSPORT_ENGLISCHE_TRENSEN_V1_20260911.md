# PRODUKTVERGLEICH – PROFILE / FACT MATRIX SATTELSCHRÄNKE / SATTELTRANSPORT / ENGLISCHE TRENSEN V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Drei Registry-Gruppen bleiben fachlich getrennt:
- `sattelschraenke`;
- `satteltransport`;
- `englische-trensen`.

Research Batch B bleibt nur Candidate Evidence. Vor Pairing werden Funktionsklasse und Nutzungsebene hart normalisiert. Finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin aus aktuellem Product Knowledge.

---

## 1. Sattelschränke

Portal-Key:
`sattelschraenke`

Technischer Key:
`sattelschraenke`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Gebundene V1-Klasse:
`STATIONARY_METAL_SADDLE_CABINET`.

Pflichtfeld vor Paarung:
`cabinet_mobility_class`.

Für diese V1-Klasse gilt:
`STATIONARY`.

Ausgeschlossen bzw. separate Unterklasse:
- fahrbarer Sattelschrank;
- Turnierschrank/Turnierwagen;
- Kunststoff-Transport-/Turnierschrank;
- Aufsatzschrank ohne eigenständige Sattelaufbewahrungsfunktion;
- offene Sattelhalter/Sattelständer ohne Schrankkorpus.

Growi führt stationäre 600-mm-Sattelschränke und daneben ausdrücklich fahrbare/Turnier-Ausführungen. Diese werden nicht gekreuzt.

### Aktuelle Hersteller-Evidence

Growi / Großewinkelmann GmbH & Co. KG:
- stationärer `Growi Sattelschrank 600 x 600 mm` in mehreren Höhen;
- konkrete 1,06-m-Variante Art.-Nr. `10050020`;
- 1060 x 600 x 600 mm;
- 37 kg;
- verstellbarer Einlegeboden;
- ein Sattelhalter Profi;
- zwei Trensenhalter;
- Zylinderschloss;
- weitere stationäre Varianten bis 1900 mm Höhe.

Herstellerquellen:
https://www.growi.de/stall-weidetechnik/sattelschraenke/600-mm-breite
https://www.growi.de/stall-weidetechnik/sattelschraenke/600-mm-breite/growi-sattelschrank-600-x-600-mm-zylinderschloss-standard-1-06-m1
https://www.growi.de/stall-weidetechnik/sattelschraenke/turnierschraenke

Albert Kerbl GmbH:
- `Sattelschrank`, Art.-Nr. `32707` und `326132`;
- stationärer Bausatz aus verzinktem Stahlblech;
- 60 x 60 cm Grundfläche;
- Höhen 106 bzw. 150 cm;
- Gewichte 30 bzw. 38 kg;
- Ablagefach;
- zwei Sattelhalter;
- Haken/Halter für Trensenzäume;
- Luftschlitze;
- abschließbar;
- stapelbar.

Herstellerquelle:
https://www.kerbl.com/de/produkt/sattelschrank-13449

### Faktenmatrix V1

1. `cabinet_class`;
2. `cabinet_mobility_class`;
3. `assembly_state` – Bausatz/fertig montiert nur source-bound;
4. `material`;
5. `width_mm`;
6. `depth_mm`;
7. `height_mm`;
8. `weight_kg`;
9. `saddle_holder_count`;
10. `saddle_holder_type`;
11. `bridle_holder_count`;
12. `shelf_count_or_storage_configuration`;
13. `ventilation_openings`;
14. `lock_type`;
15. `stackable`;
16. `manufacturer_intended_use`;
17. `warranty`.

Nicht veröffentlichte Diebstahlwiderstands-, Feuchte-, Belastungs- oder Korrosionswerte bleiben `NOT_IN_SOURCE`.

### Pairing-Regeln

- gleiche Gruppe `sattelschraenke`;
- `cabinet_class = SADDLE_CABINET`;
- `cabinet_mobility_class = STATIONARY`;
- Metall-Schrankklasse;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Varianten mit unterschiedlichen Höhen/Ausstattungen dürfen nur als konkrete Varianten verglichen werden, wenn die Produktidentität maschinenfest gebunden ist. Fahrbare und stationäre Schränke werden nicht im selben Paaruniversum vermischt.

### Decision-Policy

- Klasse/Mobilität: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Gewicht, Material und Ausstattungsanzahl: sachliche Unterschiede;
- Schlossart nur sachlich; keine freie Aussage zu Einbruchschutz/Sicherheitsniveau;
- Luftschlitze nur als vorhandene Konstruktion bzw. Herstellerclaim, keine freie Feuchte-/Schimmelwirkung ableiten;
- verzinktes Stahlblech nicht automatisch als langlebiger/korrosionsbeständiger Sieger werten;
- Bausatz vs. fertig montiert nur als Liefer-/Montagefakt.

---

## 2. Satteltransport

Portal-Key:
`satteltransport`

Technischer Key:
`satteltransport`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Gebundene V1-Klasse:
`SOFT_SADDLE_CARRY_BAG`.

Primärer Zweck:
Sattel außerhalb des Reitens in einer weichen Tasche tragen und beim Transport/Lagern schützen.

Ausgeschlossen bzw. getrennte Funktionsklasse:
- am Sattel befestigte Pack-/Wanderreittasche;
- Sattelschoner ohne definierte Tragefunktion;
- Sattelwagen/Trolley;
- harter Transportkoffer/Case;
- Sattelhalter/Saddle Carrier als offener Ständer;
- Sattelschrank/Turnierschrank;
- Schabracken-/Sattelpad-Tasche.

Damit wird die deutsche Mehrdeutigkeit `Satteltasche` fail-closed aufgelöst: Packtasche am Pferd ist **nicht** Satteltragetasche.

### Aktuelle Hersteller-/Direktprodukt-Evidence

LeMieux:
- `Saddle Carry Bag Black`, Product Code `IT06831001`;
- ausdrücklich für Schutz des Sattels beim Transport;
- sattelförmig geschnitten;
- weiches Futter;
- große Reißverschlussöffnung;
- Schultertrageriemen mit zwei Clippositionen;
- Außentaschen für den Sattelgurt;
- Polyester-Pflegehinweise veröffentlicht.

Herstellerquelle:
https://www.lemieux.com/us/horsewear/stable-yard/saddle-carry-bag-black

Loesdau Eigenprodukt / Pferdesporthaus Loesdau GmbH & Co. KG:
- `Loesdau Tragetasche für Sättel`, Art.-Nr. `5063`;
- ausdrücklich zum Transport und Schutz von Sätteln;
- stabile Tragetasche;
- Reißverschluss;
- Tragegriffe.

Direktprodukt-/Sortimentsquelle:
https://www.loesdau.de/reiter/accessoires/taschen/

### Faktenmatrix V1

1. `transport_class`;
2. `saddle_compatibility` – nur ausdrücklich veröffentlichte Satteltypen/Größen;
3. `outer_material`;
4. `lining_material`;
5. `padding`;
6. `water_resistance_claim`;
7. `carry_handles`;
8. `shoulder_strap`;
9. `backpack_straps`;
10. `closure_type`;
11. `external_pockets`;
12. `girth_storage`;
13. `dimensions`;
14. `manufacturer_transport_or_protection_claim`;
15. `care`;
16. `warranty`.

Nicht veröffentlichte Polsterstärke, Wassersäule, Stoßschutzwerte oder universelle Sattelkompatibilität bleiben `NOT_IN_SOURCE`.

### Pairing-Regeln

- gleiche Gruppe `satteltransport`;
- `transport_class = SOFT_SADDLE_CARRY_BAG`;
- das Produkt muss ausdrücklich den **Sattel selbst** transportieren/schützen, nicht nur Zubehör am Sattel tragen;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Sattelkompatibilität bleibt Pflichtfakt. Produkte mit ausdrücklich inkompatiblen Satteltypen/Größen dürfen nicht als direkte Variantenpaarung freigegeben werden.

### Decision-Policy

- Transportklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Trageart, Verschluss, Taschen, Material/Futter/Polsterung nur sachlich;
- Schutzwirkung nur als Herstellerclaim, keine freie Stoß-/Kratz-/Wetterschutzrangfolge;
- keine Aussage `universell passend`, wenn der Hersteller das nicht belegt;
- Packtasche, Saddle Cover und Carry Bag niemals aufgrund des Wortes `Satteltasche` gleichsetzen.

---

## 3. Englische Trensen

Portal-Key:
`englische-trensen`

Technischer Key:
`englische-trensen`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Der Registry-Key wird nicht als Sammelbegriff für alle Kopfstücke materialisiert.

Pflichtfelder vor Paarung:
- `bridle_class`;
- `noseband_type`;
- `bit_included`;
- `reins_included`.

Erste source-bound Cross-Brand-V1-Klasse:
`ENGLISH_COMBINED_SNAFFLE_BRIDLE_WITH_REINS_NO_BIT`.

Normalisierte Pflichtwerte:
- `bridle_class = SNAFFLE_BRIDLE`;
- `noseband_type = ENGLISH_COMBINED`;
- `bit_included = false`;
- `reins_included = true`.

Ausgeschlossen bzw. eigene Klassen:
- Kandare/Double Bridle;
- gebisslose Zäumung;
- mexikanisches/Grackle-Reithalfter;
- hannoversches Reithalfter;
- Reithalfter Spezial/anatomische Spezialklasse, wenn nicht konkret als englisch kombiniert konfiguriert;
- reine Einzel-Reithalfter ohne vollständigen Trensenzaum;
- Produktkonfiguration ohne maschinenfest gebundenen Nasenriemen-/Zügelumfang.

### Aktuelle Hersteller-Evidence

Passier:
- `Trense Juno`, Art.-Nr. `840`;
- laut aktuellem Katalog als Trense für tägliches Training;
- mit austauschbaren Reithalftern;
- konkrete englisch-kombinierte Konfiguration über Reithalfter Art.-Nr. `841`;
- Zügel Art.-Nr. `921`;
- Größen Pony, Vollblut, Warmblut, Warmblut extra;
- Farben Schwarz/Havanna;
- Edelstahl- oder Messingbeschläge.

Herstellerquellen:
https://www.passier.com/de/products/Z%C3%A4ume
https://www.passier.com/_Katalog/Passier_Katalog_2026.pdf

Waldhausen:
- `Waldhausen X-Line Trensenzaum Supersoft`, Modell `95715`, konkrete Variante z. B. `9571501-WB`;
- Leder;
- englisch kombiniertes Reithalfter;
- anatomisch geformtes Genickstück;
- gerades Stirnband;
- weich unterlegte Nasenriemen/Stirnband/Genickstück;
- Edelstahlbeschläge;
- 19-mm-Gurtzügel;
- Größen u. a. PON, VB, WB, XWB je Variante.

Herstellerquellen:
https://www.waldhausen.com/pferde/trensenzaeume-zubehoer/trensenzaeume/englisch-kombinierte-trensenzaeume/
https://www.waldhausen.com/waldhausen-x-line-trensenzaum-supersoft/95715/

### Faktenmatrix V1

1. `bridle_class`;
2. `noseband_type`;
3. `bit_included`;
4. `reins_included`;
5. `reins_type`;
6. `reins_width_mm`;
7. `main_material`;
8. `headpiece_design`;
9. `headpiece_padding`;
10. `noseband_padding`;
11. `browband_design`;
12. `hardware_material`;
13. `available_sizes`;
14. `available_colors`;
15. `replaceable_noseband_system`;
16. `manufacturer_fit_or_pressure_claims`;
17. `care`;
18. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `englische-trensen`;
- `bridle_class = SNAFFLE_BRIDLE`;
- identischer normalisierter `noseband_type = ENGLISH_COMBINED`;
- identischer Lieferumfang bezüglich Gebiss/Zügel: `bit_included = false`, `reins_included = true`;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Bei konfigurierbaren Trensen wie Passier muss die konkrete Nasenriemen-/Zügelkonfiguration als Produktvariante im Product Knowledge gebunden sein. Der bloße Familienname reicht nicht für Pairing.

### Decision-Policy

- Bridle-/Noseband-Klasse und Lieferumfang: `PAIRING_EQUAL_NO_PREFERENCE`;
- Leder, Beschläge, Zügeltyp/-breite, Polsterung, Stirnriemen und Wechselnasenriemen-System: sachliche Unterschiede;
- `anatomisch`, `weich`, `Druckverteilung`, `Jochbeinfreiheit`, `angenehm` etc. nur als Herstellerclaim;
- keine freie Aussage zu Pferdefreundlichkeit, Druckentlastung, Komfort, Passform oder Wirkung;
- keine medizinische/biomechanische Empfehlung aus Herstellerclaims ableiten;
- keine Trensenpaarung allein aufgrund Marke/Preis/Optik.

## Globale Verbote für alle drei Gruppen

- keine Kreuzpaarung verschiedener Funktionsklassen;
- kein Gesamtsieger;
- keine Punkte/Sterne/Rankings;
- keine Shop-/Affiliate-Verfügbarkeit als Fachargument;
- keine nicht belegte Schutz-, Sicherheits-, Haltbarkeits-, Komfort- oder Passformwertung;
- keine Produktidentität aus Namensähnlichkeit erfinden;
- Quellenlücke bleibt `NOT_IN_SOURCE`.

## Produktvalidierung gegen die Profilspec

Fresh source-bound Gegenprüfung 2026-09-11:

- `sattelschraenke`: Growi stationärer 600-mm-Sattelschrank + Kerbl Sattelschrank 32707/326132 belegen zwei unabhängige stationäre Metall-Sattelschrankfamilien; Growi fahrbare/Turniermodelle bleiben außerhalb dieser V1-Unterklasse;
- `satteltransport`: LeMieux Saddle Carry Bag + Loesdau Tragetasche für Sättel belegen zwei unabhängige weiche Satteltragetaschen mit explizitem Transport-/Schutzzweck; Packtaschen am Pferd bleiben ausgeschlossen;
- `englische-trensen`: Passier Juno in englisch-kombinierter Konfiguration + Waldhausen X-Line Supersoft belegen zwei unabhängige komplette englisch-kombinierte Trensenzaumfamilien mit Zügeln; die konkrete Passier-Konfiguration muss vor Pairing maschinenfest gebunden sein.

Das ist keine finale Paarfreigabe, keine Markt-Vollständigkeit und keine Aussage, dass jede Variantenkombination pairable ist.

## Technische Materialisierungsgrenze

Dieses Dokument ändert `comparison-profiles.json` nicht.

Die Spezifikationen aus Akten 62–67 bleiben source-bound gesammelt. Vor technischer Materialisierung muss Product Knowledge pro konkretem Produkt/Variante die erforderliche Klassenbindung und Fakten source-bound tragen.

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
