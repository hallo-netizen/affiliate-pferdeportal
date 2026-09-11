# PRODUKTVERGLEICH – FACHKLÄRUNG BATCH Y / ERSTE EXACT-PRODUCT-IDENTITY-GRUPPEN

Stand: 2026-09-11
Status: SOURCE-BOUND RESEARCH/FACHKLÄRUNG / NICHT PRODUCT KNOWLEDGE / NICHT SEO-FREIGEGEBEN

Bearbeitet werden die ersten drei Registry-Positionen aus `EXACT_PRODUCT_IDENTITY_REQUIRED`:
- `boxentueren`;
- `anbindebalken`;
- `waschplatz-fuer-pferde`.

## 1. Boxentüren

Registry-Key: `boxentueren`

### Growi
Aktuelles exaktes Produkt:
- Schiebetür für Pferdebox zur Wandmontage;
- Art.-Nr. 10011360;
- 1300 mm breit, Türrahmen 2150 mm, inkl. Schienensystem/Laufwagen/Stopper;
- Holzfüllung Douglasie.

Herstellerquelle:
https://www.growi.de/stall-weidetechnik/pferdeboxen/zubehoer-pferdeboxen/schiebetuer-wandmontage-douglasie

### HÖRMANN
Aktuelle konkrete Türtypen der Pferdeboxen:
- Drehtür Premium 1/2;
- Drehtür Classic 1/2;
- Drehtür Basic 1/2;
- Schiebetür Classic;
- Schiebetür Basic.

Herstellerquelle:
https://www.hoermann-info.de/de/reitanlagen/pferdestalleinrichtung/pferdeboxen

### Röwer & Rüb
Aktuelles Modell Hamburg mit patentierter Pferdebox-Schiebetür:
- Durchgangsbreite 1,30 m;
- integriertes/einstellbares Laufwerk;
- einhändig bedienbarer Teleskopverschluss.

Herstellerquelle:
https://www.roewer-rueb.com/produkte/pferdeboxen/modell-hamburg/

Research-Status:
`MULTI_FAMILY_EXACT_HORSE_STALL_DOOR_PRODUCTS / SLIDING_VS_HINGED + DIMENSION + MATERIAL_FACT_MATRIX_OFFEN`.

Coverage-Folge:
`PARTIAL_AMBIGUOUS -> EVIDENCE_PRESENT`.

## 2. Anbindebalken

Registry-Key: `anbindebalken`

### HAU
Aktuelles direktes Produkt:
- HAU Anbindebügel;
- für Unterteilung von Putzplätzen;
- Anbinderinge vorne/hinten;
- feuerverzinkt;
- Montage über Fußplatten.

Herstellerquelle:
https://hau-pferdesport.de/produkte/putz-und-waschplatz/anbindebuegel/

### Growi
Aktuelle konkrete Hardwareklasse:
- U-Bügel;
- Anbindepfosten mit Bügel;
- Anbindepfosten mit Holzfüllung;
- stabile feuerverzinkte Rundrohrkonstruktionen für Stall/Putzplatz.

Herstellerquellen:
https://www.growi.de/stall-weidetechnik/stallausruestung/stallbedarf/anbindungen
https://www.growi.de/stall-weidetechnik/stallausruestung/stallbedarf/anbindungen/anbindepfosten-buegel

### Sulzberger
Aktuelles exaktes Produkt:
- Anbindebügel für Putzplatz, Art. 608400;
- Rohr 2 Zoll;
- ca. 1,20 m hoch / 2,00 m lang;
- zwei Anbinderinge, Bodenplatten, verzinkt.

Herstellerquelle:
https://www.sulzberger.de/zubehoer/anbindebuegel

Fachliche Normalisierung:
Der Registry-Begriff `Anbindebalken` wird nicht wörtlich auf einen Holzbalken verengt. Die aktuelle Fachproduktklasse ist die feste horizontale Anbinde-/Trennbügel-Hardware für Putz-/Waschplätze. Reine Anbinderinge, Seile und Einzelpfosten bleiben getrennt.

Research-Status:
`AT_LEAST_2_FAMILIES_EXACT_FIXED_TIE_BAR/BRACKET_CLASS / DIMENSION + MOUNTING + MATERIAL_FACT_MATRIX_OFFEN`.

Coverage-Folge:
`PARTIAL_AMBIGUOUS -> EVIDENCE_PRESENT`.

## 3. Waschplatz für Pferde

Registry-Key: `waschplatz-fuer-pferde`

### Konkrete Pferde-Waschhardware

AVERDE:
- Pferdedusche Komplettset AVDUSASET;
- Schwenkarm, Brause, Schlauch/Zubehör;
- ausdrücklich für Pferdewaschplatz.

Quelle:
https://www.averde.de/product/stallbedarf-hofbedarf/pferdedusche/pferdedusche-komplettset-mit-schwenkarm-abspritzbrause-und-zubehoer-avdusaset.html

Rutjes:
- Pferdeabspritzdusche;
- schwenk-/verstellbarer Wandarm;
- ausdrücklich zur professionellen Waschplatzgestaltung.

Quelle:
https://www.rutjespferdeboxen.de/produkt/pferdeabspritzdusche/

Growi:
- bestehende Evidence aus Batch C/Referenzen: Pferdeabspritzdusche Variabel, Waschbox-/Putzplatz-Einsatz.

### Harte Grenze

Die konkrete Produktklasse `Pferdedusche/Schwenkarm` ist belegt.
Der Registry-Key `Waschplatz für Pferde` kann jedoch den **gesamten Waschplatz als System** meinen: Boden/Drainage, Abtrennung, Anbindung, Wassertechnik und Dusche.

Darum wird keine einzelne Dusche still zum gesamten Waschplatz umdefiniert.

Neue Primärursache:
`SUBTYPE_USE_CLASS_REQUIRED`.

Coverage bleibt:
`PARTIAL_AMBIGUOUS`.

## Ergebnis Batch Y

- `boxentueren` -> `EVIDENCE_PRESENT`;
- `anbindebalken` -> `EVIDENCE_PRESENT`;
- `waschplatz-fuer-pferde` bleibt `PARTIAL_AMBIGUOUS`, Primärursache wechselt von `EXACT_PRODUCT_IDENTITY_REQUIRED` zu `SUBTYPE_USE_CLASS_REQUIRED`.

Keine Materialisierung.
Kein SEO.
Kein Pluginbau.
Kein Merge.
Kein Publish.
