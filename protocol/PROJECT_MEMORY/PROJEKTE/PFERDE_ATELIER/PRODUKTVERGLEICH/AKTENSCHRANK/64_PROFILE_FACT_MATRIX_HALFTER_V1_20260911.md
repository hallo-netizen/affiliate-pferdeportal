# PRODUKTVERGLEICH – PROFILE / FACT MATRIX HALFTER V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Vier getrennte Registry-Gruppen bleiben getrennt:
- `stallhalfter`;
- `knotenhalfter`;
- `sicherheitshalfter`;
- `fohlenhalfter`.

Kein Produkt darf nur wegen Oberbegriff `Halfter` in eine andere Funktionsklasse gezogen werden.
Keine finale Paarentscheidung außerhalb des Plugins.

---

## 1. Stallhalfter

Portal-Key:
`halfter-und-stricke-stallhalfter`

Technischer Key:
`stallhalfter`

Gebundene Klasse:
`STANDARD_STABLE_EVERYDAY_HALTER`.

Aktuelle Hersteller-Evidence:
- Waldhausen `Halfter Satin`, Modell 5025;
- Schockemöhle Sports `SP Memphis`, Produktfamilie 1311-00001.x, Soft-PP/Nylon, verstellbarer Kopf-/Nasenriemen, gepolstert;
- Albert Kerbl `ClassicSoft`, Art.-Familie 322475x, verstellbarer Nasen-/Genickriemen, Webpelzpolsterung;
- Albert Kerbl `Doria`, Art.-Familie 322819x ff., gepolstert/verstellbar.

Herstellerquellen:
https://www.waldhausen.com/pferde/halfter-stricke/halfter/
https://schockemoehle-sports.com/Halfter-SP-Memphis/1311-00001.9
https://www.kerbl.com/de/produkt/halfter-classicsoft-201345
https://www.kerbl.com/de/produkt/halfter-doria-949176

Ausgeschlossen:
- Breakaway-/Safety-Halfter;
- Knotenhalfter;
- Fohlenhalfter;
- Halfter-Fliegenmasken-Kombination als eigener Systemtyp.

Faktenmatrix:
`halter_class`, `material`, `padding_headpiece`, `padding_noseband`, `headpiece_adjustable`, `noseband_adjustable`, `throatlatch_closure`, `hardware_material`, `sizes`, `care`, `warranty`.

Pairing:
- `halter_class = STANDARD_STABLE_EVERYDAY_HALTER`;
- unterschiedliche Herstellerfamilien;
- pairable Lifecycle.

Decision:
Material/Polsterung/Verstellpunkte nur sachlich. Keine Komfort-, Haltbarkeits- oder Sicherheitsüberlegenheit aus Materialnamen ableiten.

---

## 2. Knotenhalfter

Portal-Key:
`halfter-und-stricke-knotenhalfter`

Technischer Key:
`knotenhalfter`

Gebundene Klasse:
`TRADITIONAL_KNOTTED_ROPE_HALTER`.

Aktuelle Hersteller-Evidence:
- Waldhausen `Knotenhalfter`, Modell 50411;
- Waldhausen `Knotenhalfter mit beweglichem Ring`, Modell 50409 als funktionsabweichende Untervariante;
- LeMieux `Rope Halter Navy`, Product Code IT06871001, traditionelles geknotetes Seilhalfter, One Size, verstellbar.

Herstellerquellen:
https://www.waldhausen.com/pferde/longieren-bodenarbeit/bodenarbeit/
https://www.lemieux.com/us/horsewear/headcollars-leadropes/rope-halter-dusk

Für Cross-Brand-V1 zunächst nur traditionelle Seilhalfter ohne zusätzliche Gebiss-/Zügel-/Ring-Systemfunktion.

Ausgeschlossen:
- Knotenhalfter mit Zügel als Kombisystem;
- Longierhalfter;
- normale Nylon-/Lederhalfter;
- Safety-Halfter.

Faktenmatrix:
`halter_class`, `rope_material`, `rope_diameter`, `adjustability`, `size_range`, `hardware_present`, `ring_system`, `intended_use`, `manufacturer_warnings`, `care`.

Pairing:
- `halter_class = TRADITIONAL_KNOTTED_ROPE_HALTER`;
- keine zusätzliche Ring-/Zügel-Systemfunktion;
- unterschiedliche Herstellerfamilien;
- pairable Lifecycle.

Decision:
Dünneres/dickeres Seil, weniger Hardware oder geringeres Gewicht niemals automatisch als besser/sicherer/feiner wirkend bewerten. Herstellerwarnungen bleiben Fakten, keine freie Trainingsberatung.

---

## 3. Sicherheitshalfter

Portal-Key:
`halfter-und-stricke-sicherheitshalfter`

Technischer Key:
`sicherheitshalfter`

Gebundene Klasse:
`NYLON_HALTER_WITH_LEATHER_BREAKAWAY_HEADPIECE`.

Aktuelle Hersteller-Evidence:
- LeMieux `Break Away Halter`, Product Code IT04277, Nylon + Leder-Druck-/Sollbruchmechanismus;
- Schockemöhle Sports `SP Memphis Breakaway`, 1311-00020.x, Soft-Nylon + austauschbares Leder-Kopfstück mit definierter Breakaway-Funktion.

Herstellerquellen:
https://www.lemieux.com/us/horsewear/headcollars-leadropes/break-away-headcollar-2023
https://schockemoehle-sports.com/Halfter-SP-Memphis-Breakaway/1311-00020.5

Faktenmatrix:
`safety_mechanism_class`, `breakaway_component`, `replaceable_breakaway_part`, `base_material`, `padding`, `adjustment_points`, `sizes`, `manufacturer_use_context`, `manufacturer_warnings`, `release_force`, `care`, `warranty`.

`release_force` bleibt `NOT_IN_SOURCE`, solange kein Hersteller einen belastbaren Kraftwert veröffentlicht.

Pairing:
- gleiche Safety-Klasse;
- unterschiedliche Herstellerfamilien;
- pairable Lifecycle.

Decision:
Keine Aussage „löst früher/sicherer aus“, wenn keine vergleichbaren Auslösekräfte vorliegen. Keine Risikoreduktion über Herstellerwortlaut hinaus. Kein Ranking.

---

## 4. Fohlenhalfter

Portal-Key:
`halfter-und-stricke-fohlenhalfter`

Technischer Key:
`fohlenhalfter`

Gebundene Klasse:
`FOAL_SIZED_ADJUSTABLE_HALTER`.

Aktuelle Hersteller-Evidence:
- Waldhausen `Fohlenhalfter Comfort`, Art. 5044401, weich gepolstert, mehrfach an Nase/Kehlriemen/Genick verstellbar;
- Waldhausen `STAR Leder Fohlenhalfter`, Modell 501301;
- Albert Kerbl `Halfter Hippo` in Größe Foal/00;
- Albert Kerbl `Foal Head-Collar Eco`, Ref. 327040/327041, Leder, verstellbar mit Wachstum.

Herstellerquellen:
https://www.waldhausen.com/fohlenhalfter-comfort/5044401/
https://www.kerbl.com/de/produkt/halfter-hippo-12675
https://www.kerbl.com/en/product/foal-head-collar-eco-12727

Faktenmatrix:
`halter_class`, `material`, `padding`, `nose_adjustment`, `headpiece_adjustment`, `throatlatch_adjustment`, `closure_type`, `hardware`, `foal_size_designation`, `growth_adjustability`, `care`, `warranty`.

Pairing:
- `halter_class = FOAL_SIZED_ADJUSTABLE_HALTER`;
- ausdrücklich Fohlen/Foal vom Hersteller;
- unterschiedliche Herstellerfamilien;
- pairable Lifecycle.

Material darf sich unterscheiden und ist Vergleichsfakt, nicht Pairing-Sperre.

Decision:
Keine Passform-/Sicherheits-/Hautverträglichkeitsüberlegenheit frei aus Material oder Anzahl Verstellpunkte ableiten. Größenbezeichnung ohne gemeinsame Maße nicht als Reichweite werten.

## Ergebnis

Vier Halfter-Gruppen besitzen jetzt source-bound Profil-/Faktenmatrix-/Pairing-/Decision-Spezifikationen.

Nicht materialisiert:
- kein Product-Knowledge-Import;
- keine Änderung an `comparison-profiles.json`;
- keine manuell festgelegten Produktpärchen;
- kein SEO.

Kein Merge.
Kein Publish.
