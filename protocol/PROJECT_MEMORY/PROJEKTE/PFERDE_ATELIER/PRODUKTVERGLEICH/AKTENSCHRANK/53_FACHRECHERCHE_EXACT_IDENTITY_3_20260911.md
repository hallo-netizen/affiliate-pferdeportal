# PRODUKTVERGLEICH – FACHRECHERCHE EXACT IDENTITY 3

Stand: 2026-09-11
Status: SOURCE-BOUND FACHRECHERCHE / NICHT PRODUCT KNOWLEDGE / NICHT SEO-FREIGEGEBEN

## Ziel

Bearbeitet werden die drei nach Akte 51 neu sichtbar gewordenen `EXACT_PRODUCT_IDENTITY_REQUIRED`-Fälle:
- `hoflader-zubehoer`;
- `anhaengerbeleuchtung`;
- `wasserleitungen-im-stall`.

Keine künstliche Produktklasse. Keine finale Paarentscheidung außerhalb des Plugins.

## 1. Hoflader Zubehör

Registry-Key: `hoflader-zubehoer`

### Weidemann

Batch J bindet bereits konkrete aktuelle Hoflader-Anbaugeräte, u. a.:
- Leichtgutschaufel;
- Erdschaufel;
- Greifschaufel;
- 4-in-1-Schaufel;
- Krokodilgebiss;
- Palettengabel;
- Futterdosierschaufel;
- Futterschiebeschild;
- Ballenspieß;
- Rundballenzange;
- Schlegelmäher;
- Gummischieber;
- Kehrmaschine;
- Schneeschild;
- Bodenplaner;
- Einstreugerät.

Herstellerquelle:
https://www.weidemann.de/produkte/hoflader/hoftrac-1160/anh%C3%A4nge/tab

### Schäffer

Aktuelles offizielles Werkzeugprogramm bindet konkrete Produktidentitäten, u. a.:
- Erdschaufel;
- Greifschaufel;
- Großraumschaufel;
- Hochkippschaufel;
- Palettengabel;
- Ballenspieß;
- Ballenzange für Rundballen;
- Krokodilgebiss;
- Einstreugerät;
- Futterdosiergerät;
- Schmutz- und Futterschieber;
- Reitbahnplaner.

Herstellerquelle:
https://www.schaeffer.de/werkzeuge/

### Normalisierung

`Hoflader Zubehör` bleibt als Portal-Obergruppe breit, aber die konkrete Produktidentität ist für mehrere gleiche Subtypen jetzt bei mindestens zwei unabhängigen Herstellerfamilien gebunden.

Direkte Paarung nur innerhalb identischer Funktionsklasse, z. B.:
- `PALLET_FORK` gegen `PALLET_FORK`;
- `EARTH_BUCKET` gegen `EARTH_BUCKET`;
- `GRAB_BUCKET` gegen `GRAB_BUCKET`;
- `BALE_SPIKE` gegen `BALE_SPIKE`;
- `ROUND_BALE_GRAB` gegen `ROUND_BALE_GRAB`;
- `CROCODILE_GRAB` gegen `CROCODILE_GRAB`;
- `BEDDING_DEVICE` gegen `BEDDING_DEVICE`.

Keine Kreuzpaarung verschiedener Anbaugeräte.

Research-Status:
`2_FAMILIES_WITH_EXACT_MATCHING_LOADER_ATTACHMENT_SUBTYPES / COMPATIBILITY + DIMENSION + LOAD_FACT_MATRIX_OFFEN`.

Coverage-Folge:
`PARTIAL_AMBIGUOUS -> EVIDENCE_PRESENT`.

## 2. Anhängerbeleuchtung

Registry-Key: `anhaengerbeleuchtung`

### Aspöck Systems

Aktuelle Trailer-Lichtfamilien:
- MultiLED V;
- MultiLED IV;
- Multipoint II;
- Earpoint LED.

Hersteller bindet die Produkte ausdrücklich an Anhänger-/Trailer-Beleuchtung.

Herstellerquellen:
https://www.aspoeck.com/de/produkte-services/trailer
https://www.aspoeck.com/de/produkte-services/trailer/multiled-iv

### Jokon

Aktuelles konkretes Produkt:
- Multifunktionsleuchte L 3600 für Anhänger;
- LED;
- Blinker, Brems-, Schluss-, Nebel- und Rückfahrlicht;
- 12 V;
- IP67;
- E13-Genehmigung.

Herstellerquelle:
https://www.jokon.de/produkt/multifunktionsleuchte-l-3600-horizontal-lh-anhaenger/

### Normalisierung

Die belastbare Serienproduktklasse ist enger als der Portal-Oberbegriff:
`TRAILER_MULTIFUNCTION_REAR_LIGHT_COMPONENT`.

Ausschluss:
- serienmäßige Gesamtbeleuchtung eines Anhängermodells als bloßes Ausstattungsmerkmal;
- Fahrzeug-Hauptscheinwerfer;
- Innenraumleuchten;
- Seitenmarkierung ohne gleiche Funktion.

Research-Status:
`2_INDEPENDENT_TRAILER_MULTIFUNCTION_REAR_LAMP_FAMILIES_FOUND / VOLTAGE + FUNCTION + MOUNTING + CONNECTOR + HOMOLOGATION_FACT_MATRIX_OFFEN`.

Coverage-Folge:
`PARTIAL_AMBIGUOUS -> EVIDENCE_PRESENT`.

## 3. Wasserleitungen im Stall

Registry-Key: `wasserleitungen-im-stall`

### Harte Gegenprüfung

Batch P bindet echte pferdegeeignete Stallwasser-/Frostschutzsysteme:
- SUEVIA Mod. 311 / 317 / HEATFLOW für beheizte Ringleitungen;
- Kerbl/PATURA Frostschutz-Heizleitungen/-kabel.

Aktuelle SUEVIA-Produktseiten belegen zusätzlich reale Ringleitungs-Hardware wie:
- Durchlaufrohr ¾" aus Edelstahl;
- Durchlaufrohre 1" aus Edelstahl;
- Ringleitungs-Anschluss-Sets;
- pferdegeeignete Tränken mit Ringleitungsanschluss.

Beispiele:
https://suevia.com/de/kompakt-trog-55-cm-p12115/
https://suevia.com/de/traenkebecken-mod-1220-vac2be-p1025/
https://suevia.com/de/flach-schwenktrog-1-0-m-p11487/

### Fail-closed Folgerung

Trotz konkreter Komponenten ist `Wasserleitungen im Stall` keine sauber abgegrenzte serienmäßige PRODUCT_COMPARISON-V1-Einzelproduktklasse.
Der Key umfasst Infrastruktur/Systemplanung aus:
- Rohrnetz/Leitung;
- Dimensionierung;
- Ringleitung;
- Anschlusssets;
- Tränkenanschlüsse;
- Frostschutz/Heizung;
- Isolation;
- Montage/Verbissschutz.

Zusätzlich existieren separate Registry-Keys für `isolierte-wasserleitungen` und Frostschutz-/Tränkentechnik.
Ein einzelnes Durchlaufrohr, Heizgerät oder Heizkabel wird deshalb nicht künstlich zum gesamten `Wasserleitungen im Stall`-Produkt erklärt.

Neue Primärursache:
`SERVICE_KNOWLEDGE_CHECKLIST_ARTICLE_TYPE`.

Coverage bleibt:
`PARTIAL_AMBIGUOUS`.

## Ergebnis

Von drei Exact-Identity-Fällen:
- `hoflader-zubehoer` -> `EVIDENCE_PRESENT`;
- `anhaengerbeleuchtung` -> `EVIDENCE_PRESENT`;
- `wasserleitungen-im-stall` -> bleibt `PARTIAL_AMBIGUOUS`, neue Ursache `SERVICE_KNOWLEDGE_CHECKLIST_ARTICLE_TYPE`.

Damit ist `EXACT_PRODUCT_IDENTITY_REQUIRED` wieder auf **0** abgearbeitet.

Kein Product-Knowledge-Import.
Kein SEO.
Kein Pluginbau.
Kein Merge.
Kein Publish.
