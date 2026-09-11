# PRODUKTVERGLEICH – PROFILE / FACT MATRIX HIGH-NECK-DECKEN V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Bindung

Portal-Registry-Key:
`pferdedecken-high-neck-decken`

Geplanter technischer `product_group_key`:
`high-neck-decken`

Vergleichstyp:
`PRODUCT`

## Harte Produktklassengrenze

Ein Produkt gehört nur dann in diese Gruppe, wenn der Hersteller die Decke selbst ausdrücklich als **High Neck** / höheren integrierten Halsausschnitt führt.

Nicht automatisch gleichwertig und deshalb ausgeschlossen:
- `Wug`;
- `Big Neck`;
- `Full Neck`;
- `Combo Neck`;
- `Detach-A-Neck` / separates Halsteil;
- Standard Neck.

`Big Neck` beschreibt bei Bucas eine Passform-/Weitenklasse und ist nicht automatisch High Neck. `Wug` wird nicht aus Namensähnlichkeit zu High Neck umetikettiert.

## Aktuelle Hersteller-Evidence

### Bucas – Freedom Turnout High Neck

Aktuelle Herstellerfamilie:
- Freedom Turnout Light = 0 g;
- Freedom Turnout 150 = 150 g;
- Freedom Turnout 300 = 300 g;
- Hersteller führt die Freedom Turnout ausdrücklich in Classic Cut, High Neck und Full Neck.

Aktuelles konkretes High-Neck-Produkt:
`Freedom Turnout High Neck 150`, Code 596xx-62 je Größe.

Gebundene Herstellerfakten u. a.:
- 150 g Isolierung;
- High-neck cut;
- Ripstop-Außenmaterial;
- 600 Denier auf aktueller Freedom-Familienseite;
- wasserdicht > 5000 mm Wassersäule;
- atmungsaktiv > 3000 g/24h/m²;
- Overlap T-bar Frontverschluss;
- Dermo-care/Silk-feel-Futter je Produkt-/Familienseite;
- Kreuzgurte;
- Befestigungspunkte für Beingurte;
- Schweiflatz;
- Fillet string.

Herstellerquellen:
https://bucas.com/p/freedom-turnout-7-2/
https://webshop.bucas.com/products/freedom-turnout-high-neck-150-145-navy-silver-59645-62.html
https://bucas.com/wp-content/uploads/2025/01/Catalogue-2025-DE-Digital.pdf

### WeatherBeeta – ComFiTec Plus Dynamic Turnout High Neck

Aktuelles konkretes Produkt:
`ComFiTec Plus Dynamic Turnout High Neck 220G`, SKU 1029005000.

Gebundene Herstellerfakten u. a.:
- High Neck wird vom Hersteller als eigene Halsform zwischen Standard Neck und voller Halsabdeckung beschrieben;
- 220 g Polyfill;
- 1200D Ripstop-Außenmaterial;
- PFC-free Guard-Tec;
- Wasserdichtigkeit nach Herstellerprüfung 2000 mm+;
- Atmungsaktivität 3000 g/m²+;
- 210T glattes Innenfutter;
- Memory-Foam-Widerristentlastung;
- Quick-Clip-Frontverschluss;
- Full-wrap 3-piece tail flap;
- liner-kompatibel;
- 3 Jahre Turnout-Garantie laut Hersteller.

Aktuelle Herstellerfamilie führt High Neck neben Standard Neck und Detach-A-Neck als getrennte Halsform; 0-g-/100-g-/220-g-Familien werden getrennt nach Füllung geführt.

Herstellerquellen:
https://www.weatherbeeta.com/plus-dynamic-landing-page
https://www.weatherbeeta.com/weatherbeeta-comfitec-plus-dynamic-turnout-high-neck-220g-1029005000-9c3f50

## Gemeinsame Faktenmatrix V1

Pflichtfakten:
1. `fill_weight` – Füllgewicht in g;
2. `neck_style` – muss source-bound `HIGH_NECK` sein;
3. `outer_material_denier` – Herstellerangabe Material/Denier;
4. `waterproofness` – deklarierter Wert/Status + Messdefinition, falls veröffentlicht;
5. `breathability` – deklarierter Wert/Status + Messdefinition, falls veröffentlicht;
6. `lining` – Innenfutter laut Hersteller;
7. `liner_compatibility` – ja/nein/nicht belegt;
8. `front_closure` – Verschlusssystem;
9. `movement_cut` – Schulterfalte/Gusset/Schnittkonstruktion, nur Herstellerfakt;
10. `cross_surcingles` – Art/Anzahl soweit Hersteller veröffentlicht;
11. `leg_straps_tail_cord` – Beingurte/Schweifriemen/Fillet string;
12. `tail_flap` – Schweiflatz-Konstruktion;
13. `sizes` – veröffentlichte Größen;
14. `warranty` – nur ausdrücklich deklarierte Garantie;
15. `care` – nur ausdrücklich deklarierte Pflegeangabe.

Quellenlücke bleibt `NOT_IN_SOURCE`; sie wird nicht geschätzt.

## Pairing-Regeln

Vor Bildung eines zulässigen Kandidatenpaares zwingend:

1. beide Produkte `product_group_key = high-neck-decken`;
2. beide Produkte source-bound `neck_style = HIGH_NECK`;
3. beide Produkte gleiche normalisierte `fill_weight` in Gramm;
4. unterschiedliche Herstellerfamilien;
5. Lifecycle nach aktueller UPC-Regel pairable;
6. keine Produktidentität nur aus Shop-/SEO-Namensähnlichkeit.

Wichtig:
Die Profilregel erzeugt **kein manuell festgeschriebenes Paar**. Sie definiert nur die fachliche Eignungsgrenze; das Plugin bildet später aus aktuellem Product Knowledge selbst alle zulässigen Cross-Brand-Paare.

Wenn aktuell keine zwei Herstellerprodukte mit gleichem Füllgewicht vorhanden sind, ist das korrekte Ergebnis **0 zulässige Paare**, nicht eine Lockerung auf unterschiedliche Wärme-/Füllklassen.

## Decision-Policy V1

Global verboten:
- Gesamtsieger;
- Ranking/Punkte/Sterne;
- Qualitäts-/Komfort-/Haltbarkeitsurteil ohne gebundene Evidenz;
- Affiliate-Verfügbarkeit als Fachargument;
- Passformurteil aus Größenliste;
- High Neck als pauschal „besser“ als andere Halsformen.

Merkmalsregeln:
- `fill_weight`: `PAIRING_EQUAL_NO_PREFERENCE`;
- `neck_style`: `REQUIRED_CLASS_HIGH_NECK_NO_PREFERENCE`;
- `outer_material_denier`: höhere deklarierte Zahl darf nur als Zahlenunterschied genannt werden; keine Haltbarkeits-/Robustheitsableitung;
- `waterproofness`: nur sachlicher Unterschied, keine Überlegenheit ohne gleiche Messmethode;
- `breathability`: nur sachlicher Unterschied, keine Überlegenheit ohne gleiche Messmethode;
- `lining`: nur sachlicher Unterschied;
- `liner_compatibility`: nur sachlicher Unterschied;
- `front_closure`: nur sachlicher Unterschied;
- `movement_cut`: nur sachlicher Unterschied, keine Passform-/Beweglichkeitsüberlegenheit ableiten;
- `cross_surcingles`: nur sachlicher Unterschied;
- `leg_straps_tail_cord`: nur sachlicher Unterschied;
- `tail_flap`: nur sachlicher Unterschied;
- `sizes`: nur sachlicher Unterschied, keine Passform-/Reichweitenwertung ohne Normalisierung;
- `warranty`: nur sachlicher Unterschied, kein Qualitätsurteil;
- `care`: nur sachlicher Unterschied.

## Technische Materialisierungsgrenze

UPC 0.8.6 unterstützt `pairing_equal`, aber dieses Dokument ist noch **keine** Änderung an `comparison-profiles.json`.
Vor technischer Materialisierung muss die Gruppen-/Product-Knowledge-Bindung sicherstellen, dass nur source-bound echte High-Neck-Produkte überhaupt `product_group_key = high-neck-decken` erhalten.

Insbesondere werden die in alter Research-Evidence erwähnten Horseware-`Wug`-Produkte **nicht** als High-Neck-Produkte übernommen.

## Ergebnis

`high-neck-decken` besitzt jetzt eine source-bound fachliche Profil-/Faktenmatrix-Spezifikation.

Noch nicht behauptet:
- Product Knowledge vollständig;
- markt-vollständig;
- Pairing-Ready;
- konkrete A-vs-B-Paarfreigabe;
- SEO-PASS;
- Pluginmaterialisierung.

Kein Merge.
Kein Publish.
