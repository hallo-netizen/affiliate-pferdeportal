# PRODUKTVERGLEICH – PROFILE / FACT MATRIX PFERDEBÜRSTEN / STRIEGEL / KARDÄTSCHEN V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Drei getrennte Registry-Gruppen bleiben getrennt:
- `pferdebuersten`;
- `striegel`;
- `kardaetschen`.

Die Fachklärung aus Akte 51/55 bleibt bindend:
- `pferdebuersten` ist nur Residualgruppe für echte Bürsten, die weder Striegel noch Kardätsche sind;
- `striegel` ist die Curry-Comb-/Striegel-Funktionsklasse;
- `kardaetschen` ist die Body-Brush-/Kardätschen-Funktionsklasse;
- keine finale Paarentscheidung außerhalb des Plugins.

Research-Akte A bindet LeMieux/Waldhausen als reale Herstellerfamilien; die nachfolgenden Herstellerseiten wurden für diese Profilspec frisch gegen aktuelle Produkte geprüft.

---

## 1. Pferdebürsten

Portal-Key:
`pferdebuersten`

Technischer Key:
`pferdebuersten`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Residualregel:
Ein Produkt darf nur in `pferdebuersten`, wenn es eine echte Pferde-Fellbürste ist und **nicht** bereits als `striegel`/Curry Comb oder `kardaetsche`/Body Brush klassifiziert wird.

Pflichtfeld vor Paarung:
`brush_type`.

Paarung nur bei exakt gleicher normalisierter Bürstenart.

Aktuell source-bound als erste belastbare Cross-Brand-Unterklasse:
`DANDY_BRUSH`.

Ausgeschlossen bzw. in andere Keys/Subtypen:
- Curry Comb / Striegel -> `striegel`;
- Body Brush / Kardätsche -> `kardaetschen`;
- Hufbürste;
- Mähnen-/Schweifbürste;
- Kopfbürste als eigener Spezialbereich;
- Massage-/Fellwechselwerkzeug ohne gleiche Bürstenklasse;
- Misch-/All-in-one-Werkzeug ohne eindeutige Einzelklasse.

### Aktuelle Hersteller-Evidence

LeMieux:
- `Artisan Deep Clean Dandy Brush Brown`, Product Code `IT03800001`;
- Hersteller nennt 100 % natürliche antistatische Borsten;
- äußere Borsten entfernen Schmutz und Staub;
- massiver Holzgriff;
- Pflege: abwischen / warm waschen / lufttrocknen.

Herstellerquelle:
https://www.lemieux.com/us/horsewear/grooming-care/artisan-deep-clean-dandy-brush-brown

Waldhausen:
- `Dandy brush synthetic`, Modell `38285`, konkrete Farbvariante `3828510`;
- hochwertiger Kunstleder-Bürstenrücken;
- Rücken 18 cm;
- Borsten 4,5 cm;
- aktuelle Synthetic-Serie führt Modell 38285 ausdrücklich als Dandy Brush; Serienbeschreibung bindet synthetische Borsten.

Herstellerquellen:
https://www.waldhausen.com/en/dandy-brush-synthetic/38285/
https://www.waldhausen.com/en/grooming-series/

### Faktenmatrix V1

1. `brush_type`;
2. `bristle_material`;
3. `bristle_characteristic` – nur ausdrücklich veröffentlichte Herstellerbeschreibung;
4. `bristle_length_mm`;
5. `back_or_handle_material`;
6. `back_length_mm`;
7. `overall_dimensions`;
8. `hand_grip_system` – Griff/Schlaufe/Form;
9. `flexible_body`;
10. `manufacturer_intended_use`;
11. `care`;
12. `warranty`.

Nicht veröffentlichte Härtegrade, Ergonomie- oder Reinigungswerte bleiben `NOT_IN_SOURCE`.

### Pairing-Regeln

- gleiche Gruppe `pferdebuersten`;
- identischer normalisierter `brush_type` zwingend;
- `brush_type` darf nicht `CURRY_COMB`/`STRIEGEL` oder `BODY_BRUSH`/`KARDAETSCHE` sein;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Die Regel erzeugt kein manuell festgeschriebenes Produktpaar. Weitere Residual-Bürstentypen dürfen später nur nach eigener source-bound Typbindung in dasselbe Profiluniversum aufgenommen werden.

### Decision-Policy

- `brush_type`: `PAIRING_EQUAL_NO_PREFERENCE`;
- `bristle_material`: sachlicher Unterschied, keine Komfort-/Haut-/Reinigungsüberlegenheit ableiten;
- `bristle_characteristic`: nur Herstellerwortlaut, keine freie Härteskala;
- `bristle_length_mm`: nur Zahlenunterschied;
- `back_or_handle_material`: nur sachlicher Unterschied;
- `back_length_mm` / `overall_dimensions`: nur sachlicher Unterschied;
- `hand_grip_system`: nur sachlicher Unterschied, keine Ergonomieüberlegenheit ohne belastbare Vergleichsevidenz;
- `flexible_body`: nur sachlicher Unterschied;
- `manufacturer_intended_use`: Herstellerzweck wiedergeben, keine freie Wirksamkeitswertung;
- `care` / `warranty`: nur sachlicher Unterschied.

---

## 2. Striegel

Portal-Key:
`striegel`

Technischer Key:
`striegel`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Gebundene V1-Klasse:
`MANUAL_CURRY_COMB`.

Striegel/Curry-Comb-Produkte dienen laut Hersteller der manuellen Fellbearbeitung zum Lösen/Entfernen von Schmutz, Staub und/oder losem Haar.

Ausgeschlossen:
- klassische Borsten-Kardätsche / Body Brush;
- Dandy-/Wurzelbürste;
- elektrische Massage-/Pflegegeräte;
- Fellwechselkamm/Shedding Blade als eigene Werkzeugklasse;
- reine Massagebürste ohne Curry-Comb-Klassifizierung.

### Aktuelle Hersteller-Evidence

LeMieux:
- `Rubber Curry Comb Red`, Product Code `IT09121001`;
- klassischer Gummistriegel mit Handschlaufe;
- strukturierte weiche Zähne lösen Schmutz und Haare;
- Hersteller empfiehlt kreisende Anwendung;
- Pflege: warm waschbar / lufttrocknen.

Herstellerquelle:
https://www.lemieux.com/us/horsewear/grooming-care/rubber-curry-comb-red

Waldhausen:
- `Rainbow curry comb`, Modell `38318`, konkrete Variante `3831836`;
- Hersteller beschreibt eine stabile Oberfläche zum Entfernen von Schmutz, Staub und losem Haar;
- Rücken 13 cm.

Herstellerquellen:
https://www.waldhausen.com/en/rainbow-curry-comb/3831836/
https://www.waldhausen.com/en/grooming-series/

### Faktenmatrix V1

1. `grooming_tool_class`;
2. `construction_material`;
3. `working_surface_type` – Zähne/Noppen/Oberfläche nur source-bound;
4. `working_surface_characteristic` – z. B. weich/stabil nur Herstellerwortlaut;
5. `back_or_body_dimensions`;
6. `hand_grip_system`;
7. `flexibility`;
8. `manufacturer_intended_use`;
9. `manufacturer_use_method`;
10. `care`;
11. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `striegel`;
- `grooming_tool_class = MANUAL_CURRY_COMB`;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Material, Oberflächenform oder Griffkonstruktion sind Vergleichsfakten und nicht automatisch Pairing-Sperren, solange beide Produkte source-bound derselben manuellen Curry-Comb-Funktionsklasse angehören.

### Decision-Policy

- `grooming_tool_class`: `REQUIRED_CLASS_MANUAL_CURRY_COMB_NO_PREFERENCE`;
- Material/Oberfläche/Griff/Flexibilität nur sachlich gegenüberstellen;
- keine Aussage „sanfter“, „gründlicher“, „massiert besser“ oder „löst mehr Haar“ ohne direkt vergleichbare Evidenz;
- Hersteller-Anwendungshinweise nicht zu Trainings-/Pflegeempfehlungen erweitern;
- keine Sicherheits-/Hautverträglichkeitswertung aus Materialnamen ableiten.

---

## 3. Kardätschen

Portal-Key:
`kardaetschen`

Technischer Key:
`kardaetschen`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Gebundene V1-Klasse:
`BODY_GROOMING_BRUSH`.

Kardätsche/Body Brush = borstenbasierte Körperbürste für die Fellpflege; keine Curry-Comb-/Striegel-Konstruktion.

Ausgeschlossen:
- Striegel/Curry Comb;
- Dandy-/Wurzel-/Scrubbing Brush als grobe Residualbürste;
- reine Staub-/Glanz-/Finish-Spezialbürste, solange nicht ausdrücklich Body Brush/Kardätsche;
- Kopf-/Huf-/Mähnen-/Schweifbürste.

### Aktuelle Hersteller-Evidence

LeMieux:
- `Flexi Soft Body Brush Black`, Product Code `IT04844001`;
- synthetische Borsten;
- flexible Bauform;
- ergonomisch geformter Körper;
- elastische Handschlaufe;
- Pflege: abwischen / warm waschen / lufttrocknen.

Herstellerquelle:
https://www.lemieux.com/us/horsewear/grooming-care/flexi-soft-body-brush-black-26457

Waldhausen:
- `Body brush synthetic` / deutsche Produktklasse `Kardätsche Synthetic`, Modell `38286`, konkrete Variante `3828610`;
- mitteldicke synthetische Borsten;
- hochwertiger Kunstleder-Bürstenrücken;
- Rücken 18 cm;
- Borsten 2,5 cm.

Herstellerquellen:
https://www.waldhausen.com/en/body-brush-synthetic/3828610/
https://www.waldhausen.com/en/grooming-series/

### Faktenmatrix V1

1. `grooming_tool_class`;
2. `bristle_material`;
3. `bristle_characteristic` – nur Herstellerwortlaut;
4. `bristle_length_mm`;
5. `back_or_body_material`;
6. `back_length_mm`;
7. `overall_dimensions`;
8. `hand_grip_system`;
9. `flexible_body`;
10. `manufacturer_intended_use`;
11. `care`;
12. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `kardaetschen`;
- `grooming_tool_class = BODY_GROOMING_BRUSH`;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Naturhaar versus Synthetik, Borstenlänge, Flexkörper oder Griffart dürfen sich unterscheiden; sie sind Vergleichsfakten und keine automatische fachliche Inkompatibilität.

### Decision-Policy

- `grooming_tool_class`: `REQUIRED_CLASS_BODY_GROOMING_BRUSH_NO_PREFERENCE`;
- Borstenmaterial/-länge nur sachlich;
- keine freie Aussage zu Weichheit, Hautverträglichkeit, Glanz, Reinigungsleistung oder Komfort;
- Flexibilität/Griffart nicht automatisch als ergonomisch überlegen bewerten;
- Maße nicht als bessere Handhabung werten;
- `care` / `warranty` nur sachlich.

## Globale Verbote für alle drei Gruppen

- kein Gesamtsieger;
- kein Ranking, Punkte oder Sterne;
- keine Qualitäts-, Komfort-, Haltbarkeits-, Hautverträglichkeits- oder Reinigungsleistungswertung ohne gebundene direkte Evidenz;
- keine Shop-/Affiliate-Verfügbarkeit als Fachargument;
- keine Paarung nur wegen Oberbegriff `Putzbürste`;
- keine Produktidentität aus Namensähnlichkeit erfinden.

Quellenlücke bleibt `NOT_IN_SOURCE`.

## Produktvalidierung gegen die Profilspec

Fresh source-bound Gegenprüfung 2026-09-11:

- `pferdebuersten` / `DANDY_BRUSH`: LeMieux + Waldhausen besitzen aktuelle konkrete Produktidentitäten derselben Dandy-Brush-Klasse;
- `striegel` / `MANUAL_CURRY_COMB`: LeMieux + Waldhausen besitzen aktuelle konkrete Curry-Comb-Produktidentitäten;
- `kardaetschen` / `BODY_GROOMING_BRUSH`: LeMieux + Waldhausen besitzen aktuelle konkrete Body-Brush/Kardätschen-Produktidentitäten.

Damit ist für jede der drei Gruppen mindestens eine reale Cross-Brand-Funktionsklasse fachlich belegbar. Das ist **keine** finale Paarfreigabe und keine Markt-Vollständigkeit.

## Technische Materialisierungsgrenze

Dieses Dokument ändert `comparison-profiles.json` nicht.
Die drei Spezifikationen werden zusammen mit den bereits vorbereiteten Akten 62–64 erst in einem sinnvollen gebündelten Datenblock technisch materialisiert.

Vor Materialisierung muss Product Knowledge je Produkt mindestens die jeweilige Klassenbindung und die source-bound Fakten tragen. Erst danach darf das Plugin aus aktuellem Product Knowledge alle fachlich zulässigen Cross-Brand-Paare berechnen.

Noch nicht behauptet:
- Product Knowledge vollständig;
- Markt vollständig;
- Pairing-Ready im technischen System;
- konkrete A-vs-B-Paarfreigabe;
- SEO-PASS;
- Pluginmaterialisierung.

Kein Merge.
Kein Publish.
