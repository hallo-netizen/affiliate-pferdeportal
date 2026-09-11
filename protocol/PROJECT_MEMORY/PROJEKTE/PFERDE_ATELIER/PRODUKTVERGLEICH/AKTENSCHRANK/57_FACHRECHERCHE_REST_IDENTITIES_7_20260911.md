# PRODUKTVERGLEICH – FACHRECHERCHE REST IDENTITIES 7

Stand: 2026-09-11
Status: SOURCE-BOUND FACHRECHERCHE / NICHT PRODUCT KNOWLEDGE / NICHT SEO-FREIGEGEBEN

## Ziel

Bearbeitet werden ausschließlich:
- `isolierte-wasserleitungen` (`SECOND_MANUFACTURER_REQUIRED`);
- `satteldecken`;
- `boxengitter`;
- `reitplatzschleppe`;
- `weide-wassertanks`;
- `anhaengerkupplungen`;
- `verladetraining-zubehoer` (`EXACT_PRODUCT_IDENTITY_REQUIRED`).

## 1. Isolierte Wasserleitungen

### SUEVIA
Bereits gebunden:
- Thermo-Rohr, doppelwandiges isoliertes PE-System für Tränkenmontage/Wasserzuführung, pferdegeeignete Größen.

### LA BUVETTE
Aktuelle direkte Herstellerkomponente:
- `GAINE MOUSSE ISOLANTE 1 METRE`, Ref. A456;
- Hersteller führt sie als Schutz/Isolation für Tränken-/Leitungsbereich und Zubehör der THERMOLAC-Systeme;
- THERMOLAC 40/75 GV sind vom Hersteller ausdrücklich auch für Pferde geeignet.

Herstellerquellen:
https://www.labuvette.fr/thermolac-75-gv.html
https://www.labuvette.fr/thermolac-75-ga.html

Normalisierung bleibt:
`PASSIVE_THERMAL_WATER_LINE/TUBE_INSULATION`.
Heizkabel und komplette Tränken bleiben ausgeschlossen.

Research-Status:
`2_INDEPENDENT_PASSIVE_INSULATION_FAMILIES_BOUND / DIMENSION + MATERIAL + INSTALLATION_FACT_MATRIX_OFFEN`.

Folge:
`SECOND_MANUFACTURER_REQUIRED -> EVIDENCE_PRESENT`.

## 2. Satteldecken

### Waldhausen
Aktuelle Herstellerkategorie trennt ausdrücklich:
- Schabracken;
- Satteldecken;
- Sattelpads;
- Westernpads;
- Lammfelle.

Konkretes aktuelles Produkt:
- `Satteldecke STAR`.

Herstellerquellen:
https://www.waldhausen.com/pferde/sattelunterlagen/
https://www.waldhausen.com/pferde/sattelunterlagen/satteldecken/

Hersteller erklärt die Fachgrenze ausdrücklich: Satteldecke passt genau unter den Sattel, Schabracke geht über die Sattelfläche hinaus.

Research-Status:
`EXACT_SADDLE_BLANKET_PRODUCT_IDENTITY_BOUND / SECOND_FAMILY + FACT_MATRIX_SPÄTER_OFFEN`.

Folge:
`EXACT_PRODUCT_IDENTITY_REQUIRED -> EVIDENCE_PRESENT`.

## 3. Boxengitter

Normalisierte Klasse:
`FIXED/INTEGRATED_METAL_HORSE_BOX_GRID_ELEMENT`.

### Growi
Aktuelles eigenständiges Gitterelement:
- Element für Sicherheits-Fressgitter;
- 1800 x 290 mm;
- lichter Gitterabstand 50 mm;
- Montage als Gitterelement an Pferdebox-/Fressgitter-Hardware.

Herstellerquelle:
https://www.growi.de/stall-weidetechnik/pferdeboxen/fressgitter/sicherheits-pferdefressgitter-180cm-lang

Zusätzlich belegen aktuelle Pferdeboxen wie Dorino/Nabila integrierte feste Gitterfelder mit 50-mm-Abstand.

### Röwer & Rüb
Aktuelles eigenständiges Gitterelement:
- Sozialkontaktöffnung mit herausnehmbarem festem Stahlrohr-Gittereinsatz für Pferdebox-Trennwände;
- stabile Verankerung/Federbolzen;
- Nachrüstung bestehender Trennwände möglich.

Herstellerquelle:
https://www.roewer-rueb.com/produkte/zubehoer/sozialkontaktoeffnung/

Grenze:
Fressgitter und Sozialkontaktgitter sind verschiedene Funktionssubtypen und werden nicht direkt gekreuzt. Belegt ist die reale Serienproduktklasse `Pferdebox-Gitterelement`.

Research-Status:
`2_FAMILIES_WITH_EXACT_HORSE_BOX_GRID_ELEMENTS / FUNCTION_SUBTYPE + DIMENSION + BAR_SPACING_FACT_MATRIX_OFFEN`.

Folge:
`EXACT_PRODUCT_IDENTITY_REQUIRED -> EVIDENCE_PRESENT`.

## 4. Reitplatzschleppe

### Röwer & Rüb
Aktuelles exaktes Produkt:
- Reitbahnschleppe;
- für obere Tretschicht;
- Winkelschienen, gerundetes Planschild, Bandenräumer/-rollrad;
- höhenverstellbarer Eggenrahmen/Federzinken;
- Arbeitsbreiten 2,00 / 2,50 / 3,00 m;
- für Schlepper ab 30 PS.

Herstellerquelle:
https://www.roewer-rueb.com/produkte/zubehoer/reitbahnpflege/

Abgrenzung:
Der Key wird auf explizit vom Hersteller als Reitbahn-/Reitplatzschleppe geführte Geräte gebunden. Multifunktionale Reitplatzplaner bleiben im separaten Planner-Key.

Research-Status:
`EXACT_ARENA_DRAG_PRODUCT_IDENTITY_BOUND / SECOND_FAMILY + FACT_MATRIX_SPÄTER_OFFEN`.

Folge:
`EXACT_PRODUCT_IDENTITY_REQUIRED -> EVIDENCE_PRESENT`.

## 5. Weide-Wassertanks

Normalisierte Klasse:
`CLOSED/MOBILE_PASTURE_WATER_STORAGE_TANK_SYSTEM`.

### Joma-Tech – AquaCarrier 1000
Aktuelles Herstellerprodukt:
- mobile Wasserversorgung für Weide/Stall;
- 1000-l-IBC-Tank;
- eigene mobile Träger-/Fahrwerkslösung;
- optional Schwimmertränke und Schutzhaube;
- Hersteller nennt ausdrücklich Pferde neben weiteren Weidetieren.

Herstellerquellen:
https://www.joma-tech.de/joma-tech-aquacarrier-1000
https://www.joma-tech.de/Landtechnik/Wasserversorgung/mobile-Weidetraenke/

Grenze:
Offener Weidetrog ist kein Wassertank. Der Tank-/Speicherteil und ein angehängtes Tränkebecken bleiben in Fakten/Komponenten getrennt.

Research-Status:
`EXACT_MOBILE_PASTURE_WATER_STORAGE_PRODUCT_BOUND / SECOND_FAMILY + CAPACITY + MOBILITY_FACT_MATRIX_SPÄTER_OFFEN`.

Folge:
`EXACT_PRODUCT_IDENTITY_REQUIRED -> EVIDENCE_PRESENT`.

## 6. Anhängerkupplungen

Normalisierte Klasse:
`TRAILER_DRAWBAR_BALL_COUPLING/COUPLING_HEAD`.

### AL-KO Vehicle Technology
Aktuelle Zugkugelkupplungen u. a.:
- AK 7;
- AK 161;
- AK 270;
- AK 301;
- AK 351;
- zusätzliche WW-/Stabilisierungskupplungen.

Herstellerquelle:
https://www.alko-tech.com/de_de/fahrzeugtypen/produkte-anhaenger/kugelkupplungen

AL-KO nennt die Komponentenauswahl ausdrücklich auch für Pferdeanhänger im allgemeinen Anhängerportfolio.

### KNOTT
Aktuelles Trailertechnik-Portfolio bindet:
- Zugkugelkupplungen;
- Zugösen;
- Anhängekupplungen;
- weitere Zugeinrichtungen.

Herstellerquellen:
https://www.knott.de/geschaeftbereiche/produkte
https://www.knott.de/geschaeftbereiche/trailertechnik

Grenze:
Kupplungskopf an der Anhängerdeichsel ist nicht dieselbe Klasse wie fahrzeugseitige Nachrüst-Anhängerkupplung. Paarung nur gleiche Kupplungsart, zulässige Last, Stützlast, Deichselanschluss/Kugeldurchmesser.

Research-Status:
`2_INDEPENDENT_TRAILER_COUPLING_FAMILIES_BOUND / COUPLING_TYPE + LOAD + FITMENT_FACT_MATRIX_OFFEN`.

Folge:
`EXACT_PRODUCT_IDENTITY_REQUIRED -> EVIDENCE_PRESENT`.

## 7. Verladetraining Zubehör

Normalisierte Klasse:
`NON_STRUCTURAL_HORSE_LOADING_AID`.

### Waldhausen
Aktuelles exaktes Produkt:
- `Verladehilfe`, Modell 61782 / Art. 6178200;
- Hersteller: „ideale Hilfe beim Verladen“;
- zwei Handschlaufen;
- im aktuellen Pferde-Transportprogramm geführt.

Herstellerquellen:
https://www.waldhausen.com/verladehilfe/61782/
https://www.waldhausen.com/pferde/transport/

Ausschluss:
- Rampe;
- Brust-/Heck-/Verladestange;
- bauliche Anhängerhardware;
- allgemeines Führseil ohne explizite Verladefunktion.

Research-Status:
`EXACT_NON_STRUCTURAL_HORSE_LOADING_AID_PRODUCT_BOUND / SECOND_FAMILY + FACT_MATRIX_SPÄTER_OFFEN`.

Folge:
`EXACT_PRODUCT_IDENTITY_REQUIRED -> EVIDENCE_PRESENT`.

## Ergebnis

Alle sieben konkret recherchierbaren Restfälle wechseln zu `EVIDENCE_PRESENT`.

Damit:
- `SECOND_MANUFACTURER_REQUIRED` = 0;
- `EXACT_PRODUCT_IDENTITY_REQUIRED` = 0.

Noch offen sind danach nur Artikeltyp-/Nicht-Anwendbarkeitsfälle.

Kein Product-Knowledge-Import.
Kein SEO-/Providerlauf.
Kein Pluginbau.
Kein Merge.
Kein Publish.
