# PRODUKTVERGLEICH – PROFILE / FACT MATRIX SATTELDECKEN / SCHABRACKEN / SATTELGURTE V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Drei Registry-Gruppen bleiben fachlich getrennt:
- `satteldecken`;
- `schabracken`;
- `sattelgurte`.

Akte 55/57 und Batch B bleiben bindend:
- `satteldecken` ist nicht synonym zu `schabracken`;
- Schabracken werden mindestens nach Satteltyp/Disziplin normalisiert;
- Sattelgurte werden mindestens nach Disziplin, Lang-/Kurzgurt und Funktions-/Formklasse normalisiert;
- finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin.

---

## 1. Satteldecken

Portal-Key:
`satteldecken`

Technischer Key:
`satteldecken`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Gebundene Klasse:
`CLOSE_FIT_SADDLE_BLANKET`.

Waldhausen trennt im aktuellen Herstellerkatalog ausdrücklich Schabracken, Satteldecken und Sattelpads. Die Hersteller-Fachbeschreibung bindet `Satteldecke` als Unterlage, die im Gegensatz zur über die Sattelfläche hinausragenden Schabracke genau unter den Sattel passt.

Ausschluss:
- Schabracke / Saddle Square, die über die Sattelfläche hinausragt -> `schabracken`;
- Korrekturpad / Gelpad / Half Pad;
- Westernpad;
- Lammfell-/Sattelkissen, sofern nicht vom Hersteller als echte Satteldecke derselben Klasse geführt;
- reine Decke ohne Sattelunterlagenfunktion.

Pflicht-Untertyp vor Paarung:
`saddle_discipline`.

Mindestens:
- `DRESSAGE`;
- `ALL_PURPOSE/VSS`.

Keine Kreuzpaarung verschiedener Satteltypen/Disziplinformen.

### Aktuelle Hersteller-Evidence

Waldhausen:
- `Satteldecke STAR`, Dressur-Variante `115001-D`;
- anatomischer Schnitt;
- 300 g/m² Wattierung;
- 8 mm Spezialschaum;
- Obermaterial 75 % Polyester / 25 % Baumwolle;
- Futter 100 % Polyester;
- separate VSS-Variante vorhanden.

Herstellerquellen:
https://www.waldhausen.com/pferde/sattelunterlagen/satteldecken/
https://www.waldhausen.com/satteldecke-star/115001-d/
https://www.waldhausen.com/pferde/sattelunterlagen/

Loesdau Eigenprodukt / Herstellerangabe Pferdesporthaus Loesdau GmbH & Co. KG:
- `Loesdau Satteldecke Allround`, Art.-Nr. `57117 00017`, Warmblut/Dressur;
- anatomisch geformt;
- verstellbare Strupfenschlaufen;
- Dressur Warmblut ca. 54 x 55 cm;
- Material 65 % Polyester / 35 % Baumwolle;
- Füllung 100 % Polyester;
- zusätzliche Vielseitigkeitsvarianten derselben Produktfamilie vorhanden.

Hersteller-/Direktproduktquelle:
https://www.loesdau.de/loesdau-satteldecke-allround-black-warmblut-dressur-57117-00017.html

### Faktenmatrix V1

1. `saddle_underlay_class`;
2. `saddle_discipline`;
3. `manufacturer_size_or_shape`;
4. `dimensions_cm`;
5. `anatomical_cut`;
6. `upper_material`;
7. `lining_material`;
8. `filling_material`;
9. `padding_weight_g_m2`;
10. `foam_thickness_mm`;
11. `girth_or_billet_loop_system`;
12. `manufacturer_function_claims`;
13. `care`;
14. `warranty`.

Nicht veröffentlichte Werte bleiben `NOT_IN_SOURCE`.

### Pairing-Regeln

- gleiche Gruppe `satteldecken`;
- `saddle_underlay_class = CLOSE_FIT_SADDLE_BLANKET`;
- identische normalisierte `saddle_discipline`;
- keine Schabracke/Saddle-Square im Paaruniversum;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Größe/Form muss im Dossier sichtbar bleiben. Eine konkrete Variantenpaarung darf nur erfolgen, wenn die Varianten für denselben Satteltyp sinnvoll gegenüberstellbar sind.

### Decision-Policy

- Klasse/Disziplin: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Material, Füllung, Wattierung und Schaumdicke: sachliche Unterschiede;
- Herstellerclaims zu Atmungsaktivität, Schweißaufnahme, Druckausgleich oder Stoßdämpfung nur als Herstellerangabe; keine freie Wirksamkeitsrangfolge;
- anatomischer Schnitt/Schlaufen nicht automatisch als bessere Passform oder weniger Verrutschen bewerten;
- keine Aussage zur Sattelpassform des individuellen Pferdes aus Produktdaten ableiten.

---

## 2. Schabracken

Portal-Key:
`schabracken`

Technischer Key:
`schabracken`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Gebundene Oberklasse:
`SADDLE_PAD_SQUARE/SHABRACKE`.

Pflicht-Untertyp vor Paarung:
`saddle_discipline`.

Mindestens getrennt:
- `DRESSAGE`;
- `ALL_PURPOSE/VSS`;
- `JUMPING/CLOSE_CONTACT`.

Keine Kreuzpaarung Dressur gegen Springen/VSS nur wegen gemeinsamer Portalgruppe.

Für V1 ist als erste belastbare Cross-Brand-Klasse source-bound gebunden:
`DRESSAGE_SADDLE_PAD`.

### Aktuelle Hersteller-Evidence

LeMieux:
- aktuelle Dressage-Pad-Kategorie mit eigenständigen Dressage Squares;
- konkretes aktuelles Produkt `Essence Dressage Square White`, Product Code `IT07972`;
- Soft-Shell-Obermaterial;
- Self-Cool-Futter;
- 3D-Carbon-Mesh-Wirbelsäulenbereich;
- High-Wither-Form;
- elastische Sattelstraps;
- Gurt-Schutzbereich und verdeckte Gurtkanäle;
- Größen Small/Medium, Large, X-Large je Verfügbarkeit.

Herstellerquellen:
https://www.lemieux.com/us/horse-saddle-pads/dressage-pads
https://www.lemieux.com/us/horse-saddle-pads/dressage-pads/finesse-dressage-square-white

Waldhausen:
- aktuelle Schabracken-Kategorie führt separate Dressur- und VSS-Größen;
- konkretes Produkt `Schabracke Classic`, Art.-Nr. `1116801-D` für Dressur;
- 280 g/m² Wattierung;
- 10 mm Schaum;
- Obermaterial 75 % Polyester / 25 % Baumwolle;
- Futter 100 % Polyester;
- öffnende Gurtschlaufen, einfache oder unterteilte Führung.

Herstellerquellen:
https://www.waldhausen.com/pferde/sattelunterlagen/schabracken/
https://www.waldhausen.com/schabracke-classic/1116801-d/

### Faktenmatrix V1

1. `saddle_pad_class`;
2. `saddle_discipline`;
3. `manufacturer_size_or_shape`;
4. `upper_material`;
5. `lining_material`;
6. `filling_material`;
7. `padding_weight_g_m2`;
8. `foam_thickness_mm`;
9. `wither_or_spine_design`;
10. `saddle_attachment_system`;
11. `girth_loop_system`;
12. `manufacturer_function_claims`;
13. `care`;
14. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `schabracken`;
- gleiche normalisierte `saddle_discipline` zwingend;
- aktuelle V1-Belegklasse: `DRESSAGE_SADDLE_PAD`;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Material, Füllstärke, Wirbelsäulenkonstruktion und Befestigung dürfen sich unterscheiden; sie sind Vergleichsfakten und keine automatische Pairing-Sperre innerhalb derselben Disziplin-/Produktklasse.

### Decision-Policy

- Produktklasse/Disziplin: `PAIRING_EQUAL_NO_PREFERENCE`;
- Material/Füllung/Maße/Konstruktion: sachliche Unterschiede;
- Atmungsaktivität, Kühlung, Feuchtigkeitstransport, Druck-/Stoßabsorption ausschließlich source-bound als Herstellerclaim; keine freie Rangfolge zwischen unterschiedlich definierten Herstellerclaims;
- High-Wither-/Wirbelsäulendesign nicht automatisch als bessere Passform bewerten;
- keine medizinische oder sattelpassformbezogene Empfehlung aus Produktdaten ableiten.

---

## 3. Sattelgurte

Portal-Key:
`sattelgurte`

Technischer Key:
`sattelgurte`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Sattelgurte sind kein einheitliches Paaruniversum.

Pflichtfelder vor Paarung:
- `saddle_discipline`;
- `girth_length_class` = SHORT/DRESSAGE oder LONG;
- `girth_shape_class`.

Für V1 als erste belastbare Cross-Brand-Klasse gebunden:
`ANATOMICAL_DRESSAGE_SHORT_GIRTH`.

Ausschluss/Kreuzpaarungsverbot:
- Dressur-Kurzgurt gegen langen Spring-/Vielseitigkeitsgurt;
- gerader Standardgurt gegen anatomische Spezialklasse, wenn die Form der eigentliche Vergleichsintent ist;
- Westerngurt;
- Stollengurt gegen normalen Kurzgurt;
- baumlos-spezifische Spezialanwendung nur dann zusammenführen, wenn die allgemeine Dressurgurtklasse ebenfalls ausdrücklich gilt.

### Aktuelle Hersteller-Evidence

Acavallo:
- `Anatomischer Dressursattelgurt PVC Gel`, Produktcode `AC562_BK`;
- Dressur-Kurzgurt;
- anatomisch geformt;
- PVC + Acavallo Classic Gel + Edelstahl;
- beidseitige Elastikeinsätze;
- zentraler D-Ring;
- Größen 55–80 cm;
- Hersteller nennt Anti-Rutsch- und Druckableitungs-/Druckabsorptionsfunktion.

Herstellerquelle:
https://www.acavallo.com/de-de/product/acavallo-anatomischer-dressursattelgurt-pvc-gel-acavallo

Albert Kerbl GmbH:
- `Girth`, Ref. `32442` und Längenvarianten;
- ausdrücklich Dressurgurt;
- synthetischer Gummi;
- anatomisch gebogen;
- elastische Enden auf beiden Seiten;
- Rollenschnallen;
- Längen 45–85 cm;
- zusätzlich laut Hersteller für baumlosen Freedom-Sattel geeignet.

Herstellerquelle:
https://www.kerbl.com/en/product/girth-13205

### Faktenmatrix V1

1. `girth_class`;
2. `saddle_discipline`;
3. `girth_length_class`;
4. `girth_shape_class`;
5. `available_lengths_cm`;
6. `main_material`;
7. `padding_or_gel_material`;
8. `elastic_sides`;
9. `buckle_material`;
10. `roller_buckles`;
11. `center_attachment_ring`;
12. `manufacturer_intended_use`;
13. `manufacturer_function_claims`;
14. `care`;
15. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `sattelgurte`;
- `saddle_discipline = DRESSAGE`;
- `girth_length_class = SHORT/DRESSAGE`;
- `girth_shape_class = ANATOMICAL`;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Konkrete Längenvarianten dürfen nur dann direkt gegenübergestellt werden, wenn beide Produktfamilien eine für denselben Einsatzzweck passende Länge anbieten. Materialunterschiede allein blockieren die Paarung nicht.

### Decision-Policy

- Klasse/Disziplin/Längentyp/Formklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Länge, Material, Gel/Polster, Elastik, Schnallen und D-Ring: sachliche Unterschiede;
- Bewegungsfreiheit, Druckverteilung, Hautfreundlichkeit, Anti-Rutsch, Komfort oder Haltbarkeit nur als Herstellerclaim und nicht frei zwischen Herstellern vergleichend hochrechnen;
- keine anatomische Passformempfehlung für ein konkretes Pferd ohne individuelle Sattel-/Gurtlageprüfung.

## Globale Verbote für alle drei Gruppen

- keine Vermischung Satteldecke/Schabracke/Pad;
- keine Disziplin-Kreuzpaarung;
- kein Gesamtsieger;
- keine Punkte/Sterne/Rankings;
- keine freie Passform-, Komfort-, Druck-, Kühl-, Haut- oder Haltbarkeitswertung;
- keine Shop-/Affiliate-Verfügbarkeit als Fachargument;
- keine Produktidentität aus ähnlichem Namen erfinden;
- Quellenlücke bleibt `NOT_IN_SOURCE`.

## Produktvalidierung gegen die Profilspec

Fresh source-bound Gegenprüfung 2026-09-11:

- `satteldecken`: Waldhausen Satteldecke STAR Dressur + Loesdau Satteldecke Allround Warmblut/Dressur belegen zwei unabhängige Produktfamilien derselben Dressur-Satteldeckenklasse;
- `schabracken`: LeMieux Essence Dressage Square + Waldhausen Schabracke Classic D belegen zwei unabhängige Dressur-Schabracken-/Saddle-Pad-Familien;
- `sattelgurte`: Acavallo AC562 + Kerbl Girth 32442-Familie belegen zwei unabhängige anatomische Dressur-Kurzgurt-Familien.

Das ist keine finale Paarfreigabe, keine Markt-Vollständigkeit und keine Aussage, dass jede Variantenkombination pairable ist.

## Technische Materialisierungsgrenze

Dieses Dokument ändert `comparison-profiles.json` nicht.

Die Spezifikationen aus Akten 62–66 bleiben vorerst source-bound gesammelt. Vor technischer Materialisierung muss Product Knowledge pro konkretem Produkt/Variante die erforderliche Klassenbindung und Fakten source-bound tragen.

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
