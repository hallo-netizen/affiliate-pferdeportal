# PRODUKTVERGLEICH – PROFILE / FACT MATRIX GEBISSE / GEBISSLOSE ZÄUMUNGEN / ZÜGEL V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Die drei Registry-Gruppen bleiben getrennt:
- `gebisse`;
- `gebisslose-zaeumungen`;
- `zuegel`.

Gleicher Registry-Key reicht in keiner dieser Gruppen für Pairing. Vor einem Kandidatenuniversum müssen Wirk-/Konstruktionsklasse bzw. Zügeltyp maschinenfest gebunden sein. Finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin aus aktuellem Product Knowledge.

---

## 1. Gebisse

Portal-Key:
`gebisse`

Technischer Key:
`gebisse`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

`Gebiss` ist nur Oberbegriff.

Pflichtfelder vor Paarung:
- `bit_ring_or_sidepiece_class`;
- `mouthpiece_joint_class`;
- `mouthpiece_thickness_mm`;
- `leverage_class`.

Erste source-bound Cross-Brand-V1-Klasse:
`LOOSE_RING_DOUBLE_JOINTED_SNAFFLE_16MM_NO_LEVERAGE`.

Normalisierte Pflichtwerte:
- `bit_ring_or_sidepiece_class = LOOSE_RING/WASSERTRENSE`;
- `mouthpiece_joint_class = DOUBLE_JOINTED`;
- `mouthpiece_thickness_mm = 16`;
- `leverage_class = DIRECT_NO_LEVERAGE`.

Ausgeschlossen bzw. separate Klassen:
- Olivenkopf/D-Ring/feste Seitenteile;
- einfach gebrochen;
- Stangengebiss;
- Pelham/Kandare/3-Ring/Multi-Ring/Aufziehtrense/Baucher/andere Hebel- oder Druckmechanik;
- Lock-Up-/Arretiermechanik;
- Unterlegtrense nur bei abweichender Stärke/Funktion;
- andere Stärken, solange konkrete Variantenpaarung nicht dieselbe normalisierte Stärkeklasse bindet.

Material und anatomische Mundstückform dürfen innerhalb derselben Kernklasse Vergleichsfakten sein, sofern Ringart, Gelenkklasse, Stärke und Hebelklasse gleich bleiben.

### Aktuelle Hersteller-Evidence

Herm. Sprenger Metallwarenfabrik GmbH & Co. KG:
- `Trensengebiss 16 mm`;
- herkömmliche doppelt gebrochene Wassertrense;
- Ringart Wassertrense / lose Ringe;
- 16 mm;
- Materialien Edelstahl rostfrei oder Kupfer Plus;
- Weiten 115/125/135/145 mm;
- Ring-Ø 55 oder 70 mm;
- Verwendung Trensen;
- LPO-Angabe veröffentlicht.

Herstellerquelle:
https://www.sprenger.de/products/trensengebiss-16-mm

Waldhausen:
- `Wassertrense anatomisch, doppelt gebrochen`, Art.-Nr. z. B. `6520716-12`;
- Wassertrense mit durchlaufenden/losen Ringen;
- doppelt gebrochen;
- Edelstahl;
- Stärke 16 mm;
- Ring-Ø 70 mm;
- Weiten 12,5/13,5/14,5 cm;
- anatomisch geformtes Mundstück.

Herstellerquellen:
https://www.waldhausen.com/wassertrense-anatomisch-doppelt-gebrochen/6520716-12/
https://www.waldhausen.com/gebisssortiment

### Faktenmatrix V1

1. `bit_ring_or_sidepiece_class`;
2. `mouthpiece_joint_class`;
3. `mouthpiece_thickness_mm`;
4. `mouthpiece_width_mm`;
5. `ring_diameter_mm`;
6. `leverage_class`;
7. `mouthpiece_material`;
8. `sidepiece_material`;
9. `anatomical_mouthpiece_shape`;
10. `locking_or_special_mechanism`;
11. `manufacturer_intended_use`;
12. `competition_approval_or_standard`;
13. `manufacturer_pressure_acceptance_salivation_claims`;
14. `care`;
15. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `gebisse`;
- gleiche normalisierte Ring-/Seitenteilklasse;
- gleiche Gelenkklasse;
- gleiche Stärkeklasse für konkrete V1-Varianten;
- gleiche Hebelklasse;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Eine gemeinsame Bezeichnung `Wassertrense` reicht nicht, wenn Gelenk, Stärke oder Sondermechanik abweichen. Ebenso darf ein Marken-/Materialunterschied allein keine neue Wirkklasse erfinden.

### Decision-Policy

- Ring-/Seitenteilklasse, Gelenkklasse, Stärke und Hebelklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Weite und Ringdurchmesser: sachliche Variantenfakten, keine Qualitätswertung;
- Material/anatomische Form: sachliche Unterschiede;
- Herstellerclaims zu Druckverteilung, Akzeptanz, Speichelfluss, Kautätigkeit, Anlehnung oder Hilfengebung nur als Herstellerclaim;
- keine freie Aussage `sanfter`, `schärfer`, `maulfreundlicher`, `besser angenommen` oder `bessere Kontrolle`;
- keine individuelle Gebiss-/Passformempfehlung ohne Pferde-/Maulprüfung;
- Wettkampfzulassung nur exakt im veröffentlichten Regel-/Herstellerkontext wiedergeben.

---

## 2. Gebisslose Zäumungen

Portal-Key:
`gebisslose-zaeumungen`

Technischer Key:
`gebisslose-zaeumungen`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

`Gebisslos` beschreibt nur das Fehlen eines Gebisses und ist **keine** ausreichende Wirkklasse.

Pflichtfelder vor Paarung:
- `bitless_mechanism_class`;
- `rein_attachment_type`;
- `leverage_or_cross_under`;
- `reins_included`.

Erste source-bound Cross-Brand-V1-Klasse:
`SIDE_PULL_LATERAL_NO_LEVERAGE`.

Normalisierte Pflichtwerte:
- Zügelbefestigung seitlich am Nasenriemen/Sidepull;
- keine Hebelanzüge;
- keine Kreuzriemen-Unterkiefer-/Genickmechanik im gebundenen Produktmodus.

Ausgeschlossen bzw. separate Klassen:
- mechanische Hackamore mit Hebelanzügen;
- Cross-under/Kreuzkehl-/Jaw-crossed-Konfiguration;
- Rad-/Wheel-System mit eigener Wirkmechanik;
- Lindel oder andere Systeme ohne harte Zuordnung zur selben Sidepull-Klasse;
- Reithalfter/Traininghalfter ohne ausdrückliche Reit-/Zäumungsfunktion.

Multifunktionszäume dürfen nur dann in diese Klasse, wenn die **konkrete Sidepull-Konfiguration** im Product Knowledge als Modus/Variante maschinenfest gebunden ist. Der Familienname allein reicht nicht.

### Aktuelle Hersteller-Evidence

Joh's Stübben GmbH & Co. KG:
- `Freedom II Bitless`;
- Hersteller bindet das Produkt ausdrücklich als `bitless sidepull bridle`;
- direkte Zügeleinwirkung über seitlichen Druck am Nasenriemen;
- weich gepolsterter Nasenriemen;
- anatomisch optimierte Kopfstückkonstruktion;
- Zügel nicht im Lieferumfang.

Herstellerquelle:
https://www.stuebben.com/products/bridle-freedom-ii-bitless-with-crystals

Kavalkade GmbH:
- `Trense Light Gebisslos engl.`, SKU `19102`;
- ausdrücklich gebisslos **mit seitlichen Ringen**;
- geöltes Leder;
- Nasenriemen und anatomisches Genickstück weich gepolstert;
- damit source-bound Sidepull-/seitliche-Ring-Klasse.

Herstellerquelle:
https://www.kavalkade.de/trense-light-gebisslos-engl.html

Kontrollbeleg für Nicht-Vermischung:
Kavalkade führt separat `Cross Light` mit kreuzenden Riemen am Unterkiefer; Stübben führt separat mechanische Hackamore. Diese Mechanismen bleiben außerhalb der Sidepull-V1-Klasse.

Herstellerquellen:
https://www.kavalkade.de/trense-cross-light-gebisslos-engl.html
https://www.stuebben.com/products/2294-hackamore

### Faktenmatrix V1

1. `bitless_mechanism_class`;
2. `rein_attachment_type`;
3. `leverage_or_cross_under`;
4. `reins_included`;
5. `main_material`;
6. `noseband_material`;
7. `noseband_padding`;
8. `noseband_width_mm`;
9. `headpiece_design`;
10. `headpiece_padding`;
11. `hardware_material`;
12. `available_sizes`;
13. `available_colors`;
14. `manufacturer_pressure_or_comfort_claims`;
15. `care`;
16. `warranty`.

Nicht veröffentlichte Druckwerte oder biomechanische Wirkstärken bleiben `NOT_IN_SOURCE`.

### Pairing-Regeln

- gleiche Gruppe `gebisslose-zaeumungen`;
- `bitless_mechanism_class = SIDE_PULL_LATERAL_NO_LEVERAGE`;
- keine Cross-under- oder Hebelmechanik;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Lieferumfang Zügel muss im Dossier sichtbar sein, blockiert aber nicht automatisch die fachliche Produktklasse. Bei multifunktionalen Produkten ist die konkrete Sidepull-Konfiguration zwingend.

### Decision-Policy

- Wirk-/Mechanikklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Material, Polsterung, Kopfstück, Größen und Lieferumfang nur sachlich;
- keine freie Aussage zu Druckentlastung, Komfort, Pferdefreundlichkeit, Kontrolle oder Verständlichkeit;
- Herstellerclaims nur als Herstellerclaim;
- Sidepull, Cross-under und Hackamore niemals als gleichwirkend darstellen;
- keine individuelle Zäumungsempfehlung ohne Passform-/Pferdekontext.

---

## 3. Zügel

Portal-Key:
`zuegel`

Technischer Key:
`zuegel`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Zügel sind nur innerhalb derselben Bau-/Griffklasse sinnvoll direkt vergleichbar.

Pflichtfelder vor Paarung:
- `rein_class`;
- `grip_stop_class`;
- `width_mm`;
- `attachment_system`.

Erste source-bound Cross-Brand-V1-Klasse:
`WEB_REIN_WITH_LEATHER_STOPS_AND_MARTINGALE_STOPS_19MM`.

Die Art der Lederstege – einfach/doppelt – und das vordere Befestigungssystem bleiben sichtbare Vergleichsfakten. Für konkrete Varianten darf das Plugin zusätzlich enger normalisieren, wenn Suchintent oder Product Knowledge genau diese Konstruktion verlangt.

Ausgeschlossen bzw. separate Klassen:
- Gummizügel;
- reine Lederzügel;
- Kandarenzügel;
- Schlaufzügel;
- Thiedemann-/Spezialzügel;
- Langzügel;
- extra lange Sonderklasse ohne gleichen Nutzungskontext.

### Aktuelle Hersteller-Evidence

G. Passier & Sohn GmbH:
- `Gurtzügel mit doppelten Lederstegen und Martingalschiebern zum Knöpfen`, Art.-Nr. `922`;
- Länge je Seite Pony 125 cm / Warmblut 140 cm;
- Breite 19 mm;
- Farben Schwarz/Havanna/Teak;
- Beschläge Edelstahl oder Messing je Variante.

Herstellerquellen:
https://www.passier.com/de/Zuegel~c6640
https://www.passier.com/_Katalog/Passier_Katalog_2026.pdf

Waldhausen:
- `Waldhausen Gurtzügel`, Art.-Nr. z. B. `9563701-WB`;
- Gurtzügel mit Lederstegen und Martingalschieber;
- Breite 19 mm;
- PON 260 cm Gesamtlänge, WB 290 cm Gesamtlänge;
- Edelstahlschnallen;
- aktuelle eigenständige Produktfamilie.

Herstellerquelle:
https://www.waldhausen.com/waldhausen-gurtzuegel/9563701-wb/

### Faktenmatrix V1

1. `rein_class`;
2. `grip_stop_class`;
3. `leather_stop_count_or_pattern`;
4. `martingale_stops`;
5. `width_mm`;
6. `length_per_side_mm`;
7. `total_length_mm`;
8. `main_material`;
9. `leather_elements`;
10. `attachment_system` – Schnalle/Knopf/Haken/Clip source-bound;
11. `hardware_material`;
12. `available_sizes`;
13. `available_colors`;
14. `manufacturer_grip_or_handling_claims`;
15. `care`;
16. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `zuegel`;
- `rein_class = WEB_REIN`;
- Lederstege vorhanden;
- Martingalschieber vorhanden;
- `width_mm = 19` für die erste V1-Klasse;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Einfach/doppelt ausgeführte Lederstege und Schnallen-/Knopf-/Hakenbefestigung sind als konkrete Konstruktionsunterschiede sichtbar zu halten. Eine technische Decision-Policy darf daraus ohne Evidenz keine Griff-/Sicherheitsüberlegenheit ableiten.

### Decision-Policy

- Zügelklasse, Steg-/Martingal-Grundklasse und Breite: `PAIRING_EQUAL_NO_PREFERENCE`;
- Länge, Steganordnung, Material und Befestigung: sachliche Unterschiede;
- keine freie Aussage zu Grip, Sicherheit, Kontrolle, Feinheit, Komfort oder Haltbarkeit;
- keine Spezialzügelwirkung auf normale Gurtzügel übertragen;
- Maße nur nach gemeinsamer Einheit normalisieren; Gesamtlänge vs. Länge je Seite nicht still gleichsetzen.

## Globale Verbote für alle drei Gruppen

- keine Kreuzpaarung unterschiedlicher Wirk-/Konstruktionsklassen;
- kein Gesamtsieger;
- keine Punkte/Sterne/Rankings;
- keine Shop-/Affiliate-Verfügbarkeit als Fachargument;
- keine ungebundene Druck-, Komfort-, Kontroll-, Sicherheits- oder Passformwertung;
- keine Produktidentität aus ähnlichem Namen erfinden;
- Quellenlücke bleibt `NOT_IN_SOURCE`.

## Produktvalidierung gegen die Profilspec

Fresh source-bound Gegenprüfung 2026-09-11:

- `gebisse`: Sprenger Trensengebiss 16 mm + Waldhausen Wassertrense anatomisch doppelt gebrochen 16 mm belegen zwei unabhängige lose-Ring-/doppelt-gebrochene/16-mm-Familien ohne Hebel; anatomische Mundstückform bleibt Vergleichsfakt;
- `gebisslose-zaeumungen`: Stübben Freedom II Bitless + Kavalkade Light Gebisslos belegen zwei unabhängige Sidepull-/seitliche-Ring-Familien ohne Hebel; Cross Light und mechanische Hackamore belegen die notwendige Ausschlussgrenze;
- `zuegel`: Passier Art. 922 + Waldhausen 95637 belegen zwei unabhängige 19-mm-Gurtzügel-Familien mit Lederstegen und Martingalschiebern.

Das ist keine finale Paarfreigabe, keine Markt-Vollständigkeit und keine Aussage, dass jede Variante paarbar ist.

## Technische Materialisierungsgrenze

Dieses Dokument ändert `comparison-profiles.json` nicht.

Die Spezifikationen aus Akten 62–68 bleiben source-bound gesammelt. Vor technischer Materialisierung muss Product Knowledge pro konkretem Produkt/Variante die erforderliche Klassenbindung und Fakten source-bound tragen.

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
