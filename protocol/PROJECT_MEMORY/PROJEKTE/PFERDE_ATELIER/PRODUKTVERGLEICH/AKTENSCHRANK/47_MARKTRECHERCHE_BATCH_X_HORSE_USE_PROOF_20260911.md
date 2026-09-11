# PRODUKTVERGLEICH – MARKTRECHERCHE BATCH X / HORSE-USE-PROOF

Stand: 2026-09-11
Status: SOURCE-BOUND RESEARCH / NICHT PRODUCT KNOWLEDGE / NICHT SEO-FREIGEGEBEN

## Ziel

Bearbeitet werden ausschließlich die vier in Akte 40 als `HORSE_USE_PROOF_REQUIRED` klassifizierten Gruppen:
- `frostwaechter`;
- `luefter-im-stall`;
- `mineralfutterspender`;
- `mineralbar-im-stall`.

## 1. Frostwächter

Registry-Key: `frostwaechter`

### Direkter Pferdestall-Heizungsbeleg

BaskZone bietet aktuell konkrete Pferdestallheizungen:
- BH1 Stable and Tack Room Heater;
- BH1C Stable and Tack Room Heater and Controller;
- 1,5 kW Infrarot;
- ausdrücklich für einzelne Pferdebox/Loose Box;
- professionelle Installation vorgesehen.

Herstellerquellen:
https://www.baskzone.com/product/baskzone-bh1-stable-and-tack-room-heater/
https://www.baskzone.com/product/baskzone-bh1c-stable-and-tack-room-heater-and-controller/

WMT Thermosysteme bietet aktuell die robuste Infrarot-Stallheizung `NRH`:
- Hersteller nennt ausdrücklich Pferdestallheizung;
- IP67;
- wand-/deckenmontierbar;
- robuste Stallanwendung.

Herstellerquelle:
https://www.wmt.at/en/infrarot-heizungsprodukte/infrared-stable-heating/

### Harte Abgrenzung

Damit ist **Pferdestall-Heizung als reale Produktklasse** belegt.
Nicht belegt ist jedoch, dass der Registry-Key `Frostwächter` genau diese Tierzonenheizung meint.

Die bereits in Batch P belegten TROTEC/STIEBEL/AEG-Produkte besitzen echte Frostschutz-/Frostwächterfunktion, aber keine belastbare allgemeine Pferde-Tierzonenfreigabe.
BaskZone/WMT besitzen Pferdestallfreigabe, sind aber keine automatisch identische Frostwächter-/Raumfrostschutzklasse.

Folge:
`HORSE_USE_PROOF_REQUIRED` ist nicht mehr der richtige Primärblocker.

Neue Primärursache:
`SUBTYPE_USE_CLASS_REQUIRED`.

Coverage bleibt:
`PARTIAL_AMBIGUOUS`.

## 2. Lüfter im Stall

Registry-Key: `luefter-im-stall`

### Hunter Industrial

Aktuelle direkte Herstellerkategorie `Horse Barn Ceiling Fans` bindet konkrete Modelle für Pferdeställe:
- DDI HVLS Fan;
- XP HVLS Fan;
- ECO HVLS Fan;
- TITAN HVLS Fan;
- zusätzlich Orbital Wall Fan / Pedestal / Drum Fan.

Hersteller beschreibt die Produktfamilie ausdrücklich für Pferdeställe und Stallluftzirkulation.

Herstellerquelle:
https://industrialfans.hunterfan.com/collections/horse-barn-ceiling-fans

### Classic Equine Equipment

Aktuelle Horse-Barn-Fans:
- Korbventilatoren für Pferdeställe;
- korrosionsbeständig;
- optional variable Geschwindigkeit;
- geschlossener Direktantrieb gegen Partikel;
- UL/CUL für landwirtschaftliche Nutzung.

Herstellerquelle:
https://www.classic-equine.com/products/horse-barn-accessories/barn-fans/

Research-Status:
`2_DIRECT_HORSE_BARN_FAN_FAMILIES_FOUND / FAN_TYPE + AIRFLOW + MOUNTING_FACT_MATRIX_OFFEN`.

Coverage-Folge:
`PARTIAL_AMBIGUOUS -> EVIDENCE_PRESENT`.

## 3. Mineralfutterspender

Registry-Key: `mineralfutterspender`

### PATURA Mineralstofffütterer Ref. 303650

Aktuelle Herstellerseite bindet jetzt ausdrücklich:
- geeignet für **Pferde** und **Ponys**;
- 3 Kammern für Salzblöcke und loses Mineralfutter;
- ca. 75 l;
- massive regendichte Gummiabdeckung;
- Ø 97 cm, Höhe 41 cm;
- Hersteller PATURA KG.

Herstellerquelle:
https://www.patura.com/de_DE/produkt/303650-patura-mineralstofffutterer

Damit ist der alte Batch-G-Block `HORSE_PRODUCT_NOT_YET_PROVEN` source-bound überholt.

Research-Status:
`EXACT_HORSE_MINERAL_FEEDER_PRODUCT_FOUND / FACT_MATRIX + SECOND_FAMILY_SPÄTER_OFFEN`.

Coverage-Folge:
`PARTIAL_AMBIGUOUS -> EVIDENCE_PRESENT`.

## 4. Mineralbar im Stall

Registry-Key: `mineralbar-im-stall`

### PATURA

Der aktuelle Mineralstofffütterer Ref. 303650 ist für Pferde/Ponys freigegeben und besitzt drei getrennte Kammern für unterschiedliche Mineralstoffquellen.

Herstellerquelle:
https://www.patura.com/de_DE/produkt/303650-patura-mineralstofffutterer

### Sweet Medicine Farm

Aktuelles Free-Choice-Mineral-Buffet-System:
- ausdrücklich auch für Pferde;
- separates Mehrkomponenten-Mineralangebot;
- eigener `SMF Feeder` mit einzelnen Fächern/Entscheidungsmöglichkeiten.

Produkt-/Anbieterquelle:
https://sweetmedicinefarm.com/

### Fachgrenze

Die Portalgruppe beschreibt mehrere frei verfügbare Mineralquellen im Stall. Damit existieren konkrete physische Mehrfach-Angebotssysteme.
Für Product Knowledge müssen später Zahl/Art der Fächer, Innen-/Außeneinsatz, Wetterschutz und Mineralprodukt-vs-Hardware strikt getrennt werden.

Research-Status:
`HORSE_MULTI_COMPARTMENT_FREE_CHOICE_MINERAL_SYSTEM_EVIDENCE_FOUND / SUBTYPE + FACT_MATRIX_OFFEN`.

Coverage-Folge:
`PARTIAL_AMBIGUOUS -> EVIDENCE_PRESENT`.

## Ergebnis Batch X

Von vier `HORSE_USE_PROOF_REQUIRED`-Gruppen:
- 3 wechseln zu `EVIDENCE_PRESENT`;
- `frostwaechter` bleibt `PARTIAL_AMBIGUOUS`, aber mit neuer Primärursache `SUBTYPE_USE_CLASS_REQUIRED`.

Damit verbleibt:
`HORSE_USE_PROOF_REQUIRED = 0`.

Keine Materialisierung.
Kein SEO.
Kein Pluginbau.
Kein Merge.
Kein Publish.
