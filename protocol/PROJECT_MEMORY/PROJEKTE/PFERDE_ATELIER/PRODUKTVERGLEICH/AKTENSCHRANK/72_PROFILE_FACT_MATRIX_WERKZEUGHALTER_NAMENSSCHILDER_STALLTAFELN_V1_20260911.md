# PRODUKTVERGLEICH – PROFILE / FACT MATRIX WERKZEUGHALTER / NAMENSSCHILDER / STALLTAFELN V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Registry-Gruppen:
- `werkzeughalter-im-stall`;
- `namensschilder-fuer-pferdeboxen`;
- `stalltafeln`.

Die drei Organisationsgruppen werden nicht über den gemeinsamen Einsatzort Stall vermischt.
- Werkzeughalter = physische Geräteaufnahme für Stallwerkzeug;
- Namensschild = dauerhaft personalisierte Identifikation einer einzelnen Pferdebox/eines Pferdes;
- Stalltafel = wiederbeschreibbare allgemeine Informationstafel an Box/Stallplatz.

Futterplan-Tafeln bleiben im separaten Key `futterkarten-und-boxenschilder`.
Zentrale Planungs-Whiteboards bleiben im separaten Key `whiteboards-fuer-stallplanung`.
Finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin aus aktuellem Product Knowledge.

---

## 1. Werkzeughalter im Stall

Portal-Key:
`werkzeughalter-im-stall`

Technischer Key:
`werkzeughalter-im-stall`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound Cross-Brand-V1-Klasse:
`WALL_MOUNTED_MULTI_TOOL_HOLDER_FOR_LONG_HANDLED_STABLE_TOOLS`.

Pflichtmerkmale:
- stationäre Wandmontage;
- Aufnahme mehrerer langstieliger Stallgeräte;
- Hersteller nennt mindestens Besen, Schaufeln, Gabeln oder vergleichbare Stallgeräte;
- kein reiner Trensen-/Sattel-/Deckenhalter;
- kein einzelner Universalhaken.

Ausgeschlossen bzw. separate Klassen:
- Trensenhalter;
- Sattelhalter;
- Deckenhalter;
- Stallbutler-Halter für genau ein Gerätesystem;
- einzelner Haken;
- Werkzeugschrank/-wagen;
- magnetische Werkstatt-Leiste ohne ausdrücklich gebundene Stallgeräteklasse.

### Aktuelle Hersteller-/Direktprodukt-Evidence

Growi / Großewinkelmann GmbH & Co. KG:
- `Growi-Gerätehalter`, Art.-Nr. `10076200`;
- Profi-Gerätehalter;
- feuerverzinkt;
- passend für ca. 5 Geräte;
- seitlicher Auslass zur Entnahme;
- Herstellerbereich Stallausrüstung/Stallbedarf/Schaufeln und Besen.

Herstellerquelle:
https://www.growi.de/stall-weidetechnik/stallausruestung/stallbedarf/schaufeln-besen/growi-geraetehalter

Loesdau / Pferdesporthaus Loesdau GmbH & Co. KG:
- `Loesdau Gerätehalter mit 4 Klammern`, Art.-Nr. `92420 00001`;
- Platz für 4 Schaufeln, Gabeln, Besen etc.;
- zusätzlich 3 Haken;
- Montage-Set inklusive;
- ca. 50 x 5,5 x 4,5 cm.

Direktprodukt-/Herstellerquelle:
https://www.loesdau.de/loesdau-geraetehalter-mit-4-klammern-92420.html

### Faktenmatrix V1

1. `tool_holder_class`;
2. `mounting_class`;
3. `primary_tool_slots`;
4. `additional_hook_count`;
5. `supported_tool_types`;
6. `holder_mechanism` – Einhängung/Klammer/Öffnung source-bound;
7. `material`;
8. `surface_finish`;
9. `width_mm`;
10. `height_mm`;
11. `depth_mm`;
12. `weight_kg`;
13. `mounting_hardware_included`;
14. `manufacturer_load_claim`;
15. `weather_or_corrosion_claim`;
16. `warranty`.

Nicht veröffentlichte Traglast, Korrosionsklasse oder Werkzeugstieldurchmesser bleiben `NOT_IN_SOURCE`.

### Pairing-Regeln

- gleiche Gruppe `werkzeughalter-im-stall`;
- `tool_holder_class = WALL_MOUNTED_MULTI_TOOL_HOLDER_FOR_LONG_HANDLED_STABLE_TOOLS`;
- mindestens vier primäre Geräteplätze für die erste V1-Unterklasse;
- Wandmontage;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Zusatzhaken, Material-/Oberflächenunterschiede oder Entnahmemechanik sind Vergleichsfakten und keine automatische Pairing-Sperre.

### Decision-Policy

- Klasse/Montage/Mehrgerätefunktion: `PAIRING_EQUAL_NO_PREFERENCE`;
- Anzahl Plätze/Haken, Maße, Material, Finish und Montageset: sachliche Unterschiede;
- keine freie Aussage zu Tragfähigkeit, Rostschutz, Sicherheit, Lebensdauer oder Bedienkomfort;
- `feuerverzinkt` wird nicht automatisch als langlebiger Sieger interpretiert;
- keine Aufnahmefähigkeit für nicht genannte Geräte erfinden.

---

## 2. Namensschilder für Pferdeboxen

Portal-Key:
`namensschilder-fuer-pferdeboxen`

Technischer Key:
`namensschilder-fuer-pferdeboxen`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound Cross-Brand-V1-Klasse:
`PERSONALIZED_SINGLE_HORSE_BOX_NAME_SIGN`.

Pflichtmerkmale:
- physisches Schild für Pferdebox/Stallplatz;
- ein einzelnes Pferd als Identitätsbezug;
- Pferdename individuell personalisierbar;
- statischer Druck/Gravur/Herstellung nach Bestellung;
- kein primär wiederbeschreibbares Informationsboard.

Ausgeschlossen bzw. separate Klassen:
- allgemeine wiederbeschreibbare Stalltafel -> `stalltafeln`;
- Futterplan-Tafel -> `futterkarten-und-boxenschilder`;
- Warn-/Verbotsschild;
- unpersonalisiertes Dekoschild;
- digitales QR-/App-Profil ohne physisches Namensschild;
- zentrale Stallbeschilderung für mehrere Pferde.

Foto, Kontaktdaten oder Zusatztext dürfen optionale Vergleichsfakten sein, sind aber keine Pflicht für die Basisklasse.

### Aktuelle Hersteller-/Direktprodukt-Evidence

Stallschild-Profi:
- `Namensschild GOLDSTÜCK fürs Pferd`;
- 10 x 25 cm;
- Pferdename Pflichtfeld;
- zusätzlicher Besitzer-/Wunschtext optional;
- verschiedene Materialien: Forex, Hart-PVC, Alu-Dibond, Acrylglas;
- wetterfest für Innen-/Außenbereich laut Anbieter;
- optional 4 Bohrungen + Schrauben.

Direktproduktquelle:
https://stallschild-profi.de/alle-produkte/boxenschilder/namensschild-goldstueck/

Regenbogenspuren:
- `Namensschild für die Pferdebox mit Foto und persönlichen Daten`;
- personalisiertes Schild mit Pferdename, Foto und Wunschdaten;
- 3 mm Alu-Dibond;
- Größen u. a. 20 x 20, 30 x 20, 30 x 30, 45 x 30, 40 x 40 cm;
- Direktdruck;
- Innen-/Außenbereich;
- Hersteller nennt UV-/Wetterbeständigkeit und 7 Jahre Garantie.

Direktproduktquelle:
https://regenbogenspuren.de/products/namensschild-pferd-foto

### Faktenmatrix V1

1. `sign_class`;
2. `horse_scope`;
3. `horse_name_personalizable`;
4. `photo_personalizable`;
5. `owner_or_contact_personalizable`;
6. `additional_text_personalizable`;
7. `material`;
8. `material_thickness_mm`;
9. `width_mm`;
10. `height_mm`;
11. `print_or_marking_method`;
12. `mounting_holes_available`;
13. `mounting_hardware_included_or_optional`;
14. `indoor_outdoor_claim`;
15. `weather_resistance_claim`;
16. `uv_resistance_claim`;
17. `warranty`.

Nicht veröffentlichte Druckhaltbarkeit, Windlast, Kratzfestigkeit oder Befestigungsfestigkeit bleiben `NOT_IN_SOURCE`.

### Pairing-Regeln

- gleiche Gruppe `namensschilder-fuer-pferdeboxen`;
- `sign_class = PERSONALIZED_SINGLE_HORSE_BOX_NAME_SIGN`;
- Pferdename individuell bindbar;
- physisches statisches Schild;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Unterschiedliche Materialien und Größen dürfen als konkrete Varianten verglichen werden. Für eine direkte Variantenpaarung muss das Product Knowledge die tatsächlich bestellte Material-/Größenvariante binden; bloße Produktfamiliennamen reichen nicht.

### Decision-Policy

- Klasse/Personalisierbarkeit: `PAIRING_EQUAL_NO_PREFERENCE`;
- Größe, Material, Foto-/Textumfang, Montageoptionen, Druckverfahren und Garantie: sachliche Unterschiede;
- Wetter-/UV-/Haltbarkeitsclaims nur source-bound;
- keine freie Aussage zu Lesbarkeit, Wertigkeit, Lebensdauer oder Sicherheit;
- kein Dekor-/Geschmacksranking.

---

## 3. Stalltafeln

Portal-Key:
`stalltafeln`

Technischer Key:
`stalltafeln`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound Cross-Brand-V1-Klasse:
`REWRITABLE_SINGLE_HORSE_STALL_INFO_BOARD`.

Pflichtmerkmale:
- physische Informationstafel für Pferdebox/Stallplatz;
- einzelpferdbezogener bzw. einzelboxbezogener Informationszweck;
- wiederbeschreibbar oder mit wechselbarer manueller Beschriftung;
- kein fest personalisiertes Namensschild;
- kein festes Futterplan-Schema als primärer Zweck;
- kein zentrales Stallplanungs-Whiteboard.

Ausgeschlossen bzw. separate Klassen:
- statisches personalisiertes Namensschild -> `namensschilder-fuer-pferdeboxen`;
- Futterplan-Tafel -> `futterkarten-und-boxenschilder`;
- Whiteboard für zentrale Stallplanung -> `whiteboards-fuer-stallplanung`;
- Warn-/Verbots-/Sicherheitsschild;
- reine Fototafel ohne Informations-/Beschriftungsfunktion.

### Aktuelle Hersteller-/Direktprodukt-Evidence

Waldhausen:
- `Schreib- und Magnettafel`, Art.-Nr. `5724300`;
- zum Aufhängen;
- Tafelstift und zwei Pferde-Magnete inklusive;
- Kunststoff;
- abwischbar;
- ca. 29,5 x 22 cm;
- magnetische + beschreibbare Informationsfunktion.

Herstellerquelle:
https://www.waldhausen.com/schreib-und-magnettafel/5724300/

Krämer Pferdesport:
- `Stalltafel Pferd`, Nr. `4543`;
- stabiler Kunststoff;
- mit Kreide oder Klebebuchstaben beschriftbar;
- 24,5 x 32,5 cm;
- als Stalltafel/Boxenschild im aktuellen Sortiment geführt.

Direktprodukt-/Herstellerquelle:
https://www.kraemer.de/Stalleinrichtung/Stallzubehoer-Reitplatzzubehoer/Boxenschilder-Warntafeln/Stalltafel-Pferd

### Faktenmatrix V1

1. `stall_board_class`;
2. `horse_scope`;
3. `rewritable`;
4. `writing_method`;
5. `wipe_clean_method`;
6. `magnetic_surface`;
7. `included_marker`;
8. `included_magnets`;
9. `material`;
10. `width_mm`;
11. `height_mm`;
12. `mounting_method`;
13. `preprinted_information_fields`;
14. `photo_slot`;
15. `indoor_outdoor_claim`;
16. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `stalltafeln`;
- `stall_board_class = REWRITABLE_SINGLE_HORSE_STALL_INFO_BOARD`;
- einzelpferd-/einzelboxbezogener Informationszweck;
- physische wechselbare Beschriftung;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Marker-/Magnettafel und Kreidetafel dürfen innerhalb dieser allgemeinen Einzelbox-Informationsklasse verglichen werden, wenn der Nutzerintent allgemeine Stalltafel ist. Bei Suchintent `Magnettafel` oder `Kreidetafel` muss das Plugin enger nach Schreib-/Oberflächenklasse normalisieren.

### Decision-Policy

- Klasse/Pferdeumfang/Wiederbeschreibbarkeit: `PAIRING_EQUAL_NO_PREFERENCE`;
- Beschriftungsmethode, Magnetfunktion, Zubehör, Material und Maße: sachliche Unterschiede;
- keine freie Aussage zu Lesbarkeit, Löschbarkeit, Robustheit, Wetterfestigkeit oder Informationssicherheit;
- Kundenbewertungen sind kein Fach-/Leistungsfakt;
- keine Futterplan- oder Organisationswirkung aus einer allgemeinen Tafel ableiten.

## Globale Verbote für alle drei Gruppen

- Werkzeughalter nicht mit Sattel-/Trensen-/Deckenhalter oder Einzelhaken mischen;
- Namensschild nicht mit wiederbeschreibbarer Stalltafel mischen;
- Stalltafel nicht mit Futterplantafel oder zentralem Whiteboard mischen;
- kein Gesamtsieger;
- keine Punkte/Sterne/Rankings;
- keine Shop-/Affiliate-Verfügbarkeit als Fachargument;
- keine Haltbarkeits-, Sicherheits-, Wetter-, Komfort- oder Organisationswirkung ohne gebundene Evidenz;
- Quellenlücke bleibt `NOT_IN_SOURCE`.

## Produktvalidierung gegen die Profilspec

Fresh source-bound Gegenprüfung 2026-09-11:

- `werkzeughalter-im-stall`: Growi Art. 10076200 + Loesdau Art. 92420 belegen zwei unabhängige wandmontierte Mehrgerätehalter für langstielige Stallgeräte;
- `namensschilder-fuer-pferdeboxen`: Stallschild-Profi GOLDSTÜCK + Regenbogenspuren Namensschild mit Foto/Wunschdaten belegen zwei unabhängige statisch personalisierte Einzelpferd-Boxenschilder;
- `stalltafeln`: Waldhausen 5724300 + Krämer 4543 belegen zwei unabhängige physische, wechselbar beschriftbare Einzelbox-/Pferde-Stalltafeln; Magnet-/Marker- versus Kreide-/Buchstabenmechanik bleibt sichtbarer Vergleichsfakt.

Das ist keine finale Paarfreigabe und keine Markt-Vollständigkeit.

## Technische Materialisierungsgrenze

Dieses Dokument ändert `comparison-profiles.json` nicht.

Die Spezifikationen aus Akten 62–72 bleiben source-bound gesammelt. Vor technischer Materialisierung muss Product Knowledge pro Produkt/Variante die Klassenbindung und Pflichtfakten tragen.

Erst dann darf das Plugin aus aktuellem Product Knowledge fachlich zulässige Cross-Brand-Paare berechnen und regelmäßig neu bewerten.

Noch nicht behauptet:
- Product Knowledge vollständig;
- Markt vollständig;
- Pairing-Ready im technischen System;
- konkrete A-vs-B-Paarfreigabe;
- SEO-PASS;
- Pluginmaterialisierung.

Kein Merge.
Kein Publish.
