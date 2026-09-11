# PRODUKTVERGLEICH – PROFILE / FACT MATRIX DECKENZUBEHÖR V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## 1. Deckengurte

Portal-Registry-Key:
`pferdedecken-deckengurte`

Geplanter technischer `product_group_key`:
`deckengurte`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

V1-Paarung zunächst nur innerhalb:
`UNIVERSAL_ELASTIC_RUG_SURCINGLE`.

Source-bound Kandidaten derselben Klasse:
- Albert Kerbl `Deckengurt elastisch`, Art.-Nr. 32346;
- WeatherBeeta `Elastic Rug Surcingle`.

Herstellerquellen:
https://www.kerbl.com/de/produkt/deckengurt-elastisch-13506
https://www.weatherbeeta.com/weatherbeeta-elastic-rug-surcingle-1022460000-2dc2c7

Nicht in dieses Cross-Brand-Paaruniversum:
- Horseware Rambo Safety Surcingles = OEM-Sicherheitssystem-Ersatz;
- Kentucky Show Rug Surcingle = OEM-/deckenspezifischer Ersatzgurt;
- Sattel-/Longiergurte;
- Brustverschlüsse;
- Bein-/Schweifriemen.

OEM-Ersatzteile dürfen nur bei nachgewiesen gleicher System-/Kompatibilitätsklasse verglichen werden. Markenfremde Systemkompatibilität wird nicht angenommen.

### Faktenmatrix

Pflicht-/Vergleichsfakten:
1. `surcingle_class`;
2. `adjustment_min_cm`;
3. `adjustment_max_cm`;
4. `max_stretched_length_cm`, falls Hersteller veröffentlicht;
5. `width_cm`;
6. `material`;
7. `elasticity`;
8. `closure_type`;
9. `rug_use`;
10. `cooler_use`;
11. `size_compatibility`;
12. `care`;
13. `warranty`.

Quellenlücke bleibt `NOT_IN_SOURCE`.

### Pairing-Regeln

- gleiche Gruppe `deckengurte`;
- `surcingle_class = UNIVERSAL_ELASTIC_RUG_SURCINGLE`;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle;
- keine OEM-Systemteile in Universal-Klasse.

Einstellbereich, Breite oder maximale Dehnung sind Vergleichsfakten, keine automatische Paar-Sperre.

### Decision-Policy

Verboten:
- Gesamtsieger/Ranking/Punkte/Sterne;
- „stabiler“, „sicherer“, „komfortabler“ aus Material/Breite/Dehnung ableiten;
- längerer Einstellbereich automatisch als besser bewerten;
- OEM-Kompatibilität erfinden.

Alle gebundenen Fakten werden sachlich gegenübergestellt. Präferenz nur über später explizit gebundene Need-/Decision-Regel, nicht frei.

---

## 2. Deckentaschen und Aufbewahrung

Portal-Registry-Key:
`pferdedecken-deckentaschen-und-aufbewahrung`

Geplanter technischer `product_group_key`:
`deckentaschen-und-aufbewahrung`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

V1-Klasse:
`STANDALONE_RUG_STORAGE_BAG`.

Source-bound Kandidaten:
- Kentucky Horsewear `Rug Bag`, Ref. 82109-01-F;
- WeatherBeeta `Rug/Blanket Storage Bag`, SKU 1003185000.

Herstellerquellen:
https://www.kentucky-horsewear.com/lv-en/eur/82109-01-f/rug-bag-black/
https://www.weatherbeeta.com/weatherbeeta-rug-blanket-storage-bag-1003185000-297d58

Nicht als eigenständiges Produkt zählen:
- bloße Originalverpackung;
- eine nur mit einer Decke mitgelieferte Tasche ohne eigene Produktidentität;
- allgemeine Turnier-/Tacktasche ohne Deckenbezug;
- Deckenhalter/-stange.

### Faktenmatrix

1. `storage_form`;
2. `rug_capacity_count`, falls veröffentlicht;
3. `volume_l`, falls veröffentlicht;
4. `dimensions_cm`;
5. `weight`, falls veröffentlicht;
6. `outer_material`;
7. `outer_denier`;
8. `water_protection`;
9. `breathability`, nur wenn ausdrücklich belegt;
10. `closure_type`;
11. `carry_handles_straps`;
12. `hanging_attachment`;
13. `primary_use_storage`;
14. `primary_use_transport`;
15. `primary_use_stall_hanging`;
16. `care`;
17. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `deckentaschen-und-aufbewahrung`;
- `storage_form = STANDALONE_RUG_STORAGE_BAG`;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Kapazität und Aufhängesystem dürfen sich unterscheiden; genau diese Unterschiede sind sachliche Vergleichsmerkmale und keine automatische fachliche Inkompatibilität.

### Decision-Policy

Verboten:
- größere Kapazität automatisch als besser;
- höheres Denier automatisch als haltbarer/besser;
- `waterproof`/`water-resistant` ohne gleiche Herstellerdefinition gleichsetzen;
- Stallaufhängung automatisch als Vorteil, wenn Nutzerbedarf nicht gebunden ist;
- Gesamtsieger/Ranking/Punkte/Sterne.

Nur source-bound Unterschiede darstellen. Quellenlücken erzeugen keine Präferenz.

## Ergebnis

Zwei weitere V1-Gruppen besitzen jetzt source-bound Faktenmatrix + Nutzungsklasse + Pairing-Regel + Decision-Policy-Spezifikation.

Noch nicht materialisiert:
- kein Product Knowledge;
- keine Änderung an `comparison-profiles.json`;
- keine finale Paarfreigabe;
- kein SEO.

Kein Merge.
Kein Publish.
