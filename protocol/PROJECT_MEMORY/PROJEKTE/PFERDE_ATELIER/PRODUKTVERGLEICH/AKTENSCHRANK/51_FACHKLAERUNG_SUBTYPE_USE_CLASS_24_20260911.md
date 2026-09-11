# PRODUKTVERGLEICH – FACHKLÄRUNG SUBTYPE / USE CLASS 24

Stand: 2026-09-11
Status: SOURCE-BOUND FACHKLÄRUNG / NICHT PRODUCT KNOWLEDGE / NICHT SEO-FREIGEGEBEN

## Ziel

Die 24 zuletzt als `SUBTYPE_USE_CLASS_REQUIRED` gebundenen Gruppen werden nicht weiter breit recherchiert, sondern fachlich fail-closed normalisiert.

Grundregel:
- gleiche Registry-Gruppe reicht nicht für Paarbarkeit;
- ein Paar darf nur innerhalb derselben gebundenen Nutzungsklasse entstehen;
- Oberbegriffe, Systembestandteile und benachbarte Registry-Keys dürfen nicht still vermischt werden;
- finale Paarentscheidung bleibt beim PRODUKTVERGLEICH-System/Plugin.

Quellenbasis:
A/C/D/E/F/H/I/J/P/R/S sowie `47_...HORSE_USE...`, `48_...EXACT_IDENTITY...`, `49_...REST_EXACT_IDENTITY...`.

## Ergebnis je Gruppe

### 1 `pferdedecken-high-neck-decken`
Gebundene Klasse: Decken mit vom Hersteller ausdrücklich als `High Neck`/hohem integriertem Halsausschnitt geführter Ausführung.

Ausschluss:
- `Wug` nicht automatisch gleich `High Neck`;
- `Big Neck` ist Passform-/Weitenklasse und nicht automatisch Hals-Höhenklasse.

A belegt Bucas-/WeatherBeeta-High-Neck-Kandidaten. Horseware-Wug bleibt außerhalb dieser Klasse.

Folge: `EVIDENCE_PRESENT`.

### 2 `pferdebuersten`
Der Key ist ein Oberbegriff und überlappt die separaten Keys `striegel` und `kardaetschen`.
Eine künstliche Restklasse „alle anderen Bürsten“ wird nicht erfunden.

Folge: `REGISTRY_OVERLAP_KEY_AMBIGUITY`.

### 3 `striegel`
Gebundene Klasse: Striegel/Curry-Comb-Produkte zum Lösen von Schmutz/Haar bzw. Massage; keine klassische Borsten-Kardätsche.
A belegt LeMieux-Curry-Comb- und Waldhausen-Striegel-Produkte.

Folge: `EVIDENCE_PRESENT`.

### 4 `kardaetschen`
Gebundene Klasse: dichte/feinere Körper-/Finish-Bürsten (`Body Brush`/Kardätsche); keine Curry-Combs/Striegel.
A belegt LeMieux-Body-Brush- und Waldhausen-Kardätschen-Produkte.

Folge: `EVIDENCE_PRESENT`.

### 5 `offenstallraufen`
Die vorhandenen Produkte überschneiden sich mit `heuraufen`, `heuraufen-fuer-weiden`, `mobile-heuraufen` und `heuballenraufen`.
`Offenstall` beschreibt primär den Einsatzort, nicht zuverlässig eine eigenständige Konstruktion.

Folge: `REGISTRY_OVERLAP_KEY_AMBIGUITY`.

### 6 `fressstaender-im-offenstall`
Gebundene Klasse: individueller Fressstand/Fressständer mit räumlich abgegrenztem Fressplatz.

Ausschluss:
- bloßes Fressgitter;
- bloßer Fresszaun;
- allgemeine Raufenlösung.

C belegt Herstellerprogramme mit Fressständer-/Gruppenhaltungs-Hardware; nicht passende Fressgitter werden ausgeschlossen.

Folge: `EVIDENCE_PRESENT`.

### 7 `hoflader-zubehoer`
Zubehör ist kein homogener Vergleichstyp.
Pflicht-Subtyp vor Paarung, z. B.:
- Schaufel;
- Greifschaufel;
- Palettengabel;
- Ballenspieß/-zange;
- Kehrmaschine;
- Mäher;
- Futterschiebeschild.

J bindet Weidemann konkret, Schäffer bisher nur als breites Werkzeugprogramm. Nach der Subtyptrennung fehlt für einzelne Vergleichssubtypen noch die exakte zweite Produktidentität.

Folge: `EXACT_PRODUCT_IDENTITY_REQUIRED`.

### 8 `reitplatzumrandung`
Pflichttrennung:
- `MOBILE_DRESSAGE_BOUNDARY` = mobile Dressurabgrenzung/Dressurviereck;
- `FIXED_ARENA_PERIMETER` = baulich feste Umrandung.

I belegt Growi mobile Produkte und OTTO als feste System-/Bauklasse. Keine Kreuzpaarung.

Folge: `EVIDENCE_PRESENT`.

### 9 `reitplatzbewaesserung`
Der separate Registry-Key `reitplatzbewaesserung-mobil` erzwingt hier die Normalisierung auf fest integrierte Reitplatzbewässerung.

Gebundene Klasse:
`FIXED_INTEGRATED_ARENA_IRRIGATION`.

I bindet OTTO-Ebbe&Flut als fest integriertes System. Mobile Beregnungswagen bleiben im separaten Mobil-Key.

Folge: `EVIDENCE_PRESENT`.

### 10 `weidetraenken`
`Weide` beschreibt Einsatzort; dieselben Produkte können zugleich automatisch, frostgeschützt oder als Trog klassifiziert sein. Es existieren separate Registry-Keys für `automatische-traenken` und frostsichere Tränken.

Ohne Registry-Vorrangregel würde dasselbe Produkt in mehreren Paaruniversen auftauchen.

Folge: `REGISTRY_OVERLAP_KEY_AMBIGUITY`.

### 11 `slowfeeder`
Gebundene Klasse: Produkte, deren primärer Mechanismus die Raufutteraufnahme verlangsamt, ohne zeitgesteuerte Freigabe als Hauptprinzip.

Ausschluss:
- zeitgesteuerter Heuzugang;
- klassische Raufe ohne Slow-Feeding-Mechanismus;
- Heubedampfer.

E bindet Haygain Forager als konkrete Slow-Feeder-Klasse.

Folge: `EVIDENCE_PRESENT`.

### 12 `heuraufen`
Generischer Oberbegriff mit Überschneidung zu Offenstall-, Weide-, Mobil- und Ballenraufen.
Keine künstliche universelle Raufe-Klasse.

Folge: `REGISTRY_OVERLAP_KEY_AMBIGUITY`.

### 13 `heuballenraufen`
Gebundene Klasse: Raufe, deren bestimmungsgemäße Kapazität/Geometrie auf ganzen Rund-/Quader-/Großballen beruht.
Kleine Boxen-/Wandraufen bleiben ausgeschlossen.
E/C binden entsprechende Großballen-/Raufenfamilien.

Folge: `EVIDENCE_PRESENT`.

### 14 `heuspender`
Pflicht-Subtypen:
- `PASSIVE_HAY_DISPENSER`;
- `TIMED_HAY_ACCESS/DISPENSER`.

Keine Kreuzpaarung zwischen passiver Ausgabe und zeitgesteuertem Zugang.
E bindet Haygain-Systeme und macht die Funktionsgrenze sichtbar.

Folge: `EVIDENCE_PRESENT`.

### 15 `spurenelemente`
Pflicht-Subtyp nach primärem Nährstoff-/Elementzweck:
- Zink;
- Eisen;
- Mangan;
- Multi-Spurenelemente.

Einzel-Zink wird nicht gegen Eisen oder breiten Mikronährstoffkomplex gepaart.
F bindet AGROBS- und St.-Hippolyt-Kandidaten.

Folge: `EVIDENCE_PRESENT`.

### 16 `diaetfutter`
Der Key bleibt nur mit Pflicht-Untertyp zulässig, z. B.:
- Magen/Verdauung;
- Stoffwechsel/stärke-zuckerreduziert;
- PSSM-orientierte Herstellerklasse.

Keine Krankheitsdiagnose/-empfehlung durch UPC. Paarung nur innerhalb gleichen Hersteller-deklarierten Ernährungszwecks und gleicher Produktart.
F bindet mehrere konkrete Herstellerfamilien.

Folge: `EVIDENCE_PRESENT`.

### 17 `automatische-traenken`
`Automatisch` beschreibt Nachfüllmechanismus, während andere Registry-Keys Einsatzort/Frostschutz/Tränkentyp beschreiben.
Dies erzeugt Cross-Key-Doppelbelegung derselben Produkte.

Folge: `REGISTRY_OVERLAP_KEY_AMBIGUITY`.

### 18 `verladetraining-zubehoer`
Der Portalbestand enthält zusätzlich den separaten Key `verladehilfen`.
Trainingshilfe, mechanische Verladehilfe, Rampe und Anhänger-Hardware dürfen nicht vermischt werden.
Ohne Registry-Vorrangregel bleibt die Grenze zwischen `verladetraining-zubehoer` und `verladehilfen` nicht eindeutig.

Folge: `REGISTRY_OVERLAP_KEY_AMBIGUITY`.

### 19 `anhaengerbeleuchtung`
Gebundene Nutzungsklasse:
`AFTERMARKET/REPLACEMENT_TRAILER_LIGHTING_COMPONENT`.

Ausschluss:
- bloß serienmäßige Leuchtenausstattung eines Anhängermodells;
- Fahrzeug-Scheinwerfer ohne Anhängerbezug.

H belegt die fachliche Trennnotwendigkeit, aber noch keine ausreichend gebundene konkrete Produktidentität für diese enge Klasse.

Folge: `EXACT_PRODUCT_IDENTITY_REQUIRED`.

### 20 `wasserleitungen-im-stall`
Pflichttrennung aus P:
- Wasserverteil-/Ringleitungssystem;
- Rohrheizkabel/Frostschutz;
- Rohr/Leitung/Isolierung selbst.

Da separate Keys `isolierte-wasserleitungen` und Frostschutzgruppen existieren, werden Heizkabel nicht als eigentliche `Wasserleitung` materialisiert.
Für den verbleibenden Kern `STALL_WATER_DISTRIBUTION_PIPE/SYSTEM` fehlt noch eine sauber serienmäßig gebundene Produktidentität.

Folge: `EXACT_PRODUCT_IDENTITY_REQUIRED`.

### 21 `mobile-heuraufen`
Pflicht-Mobilitätsklasse:
- handbewegliche Kleinraufe;
- traktor-/dreipunktversetzbare Großballenraufe;
- fahrbare/gezogene Raufe.

R bindet mindestens PATURA/Kerbl als traktor-/dreipunktversetzbare Pferderaufen. Nur innerhalb derselben Mobilitätsklasse paaren.

Folge: `EVIDENCE_PRESENT`.

### 22 `frostwaechter`
Pflicht-Installationsklasse:
- `NON_ANIMAL/TECHNICAL_ROOM_FROST_GUARD`;
- `ANIMAL_ZONE_STABLE_HEATER_WITH_EXPLICIT_FROST_GUARD_FUNCTION`.

P bindet echte Frostwächter/Raumfrostschutzgeräte; X bindet echte Pferdestallheizungen. Beides wird nicht gleichgesetzt.
Für Tierzone gilt fail-closed: Stallfreigabe **und** Frostwächterfunktion müssen beide belegt sein.
Der technische/Nebenraum-Frostschutz bleibt als eigene Klasse belegbar.

Folge: `EVIDENCE_PRESENT`.

### 23 `waschplatz-fuer-pferde`
Der Key wird für PRODUCT_COMPARISON V1 auf konkrete Waschhardware normalisiert:
`HORSE_SHOWER/WASHING_ARM_SYSTEM`.

Ausschluss wegen eigener Registry-/Produktklassen:
- Bodenmatte/Drainage;
- Anbindebalken/-ring;
- komplette Bauplanung des Waschplatzes.

Y bindet AVERDE, Rutjes und Growi-Pferdeduschen/Schwenkarme.

Folge: `EVIDENCE_PRESENT`.

### 24 `heunetze-fuer-staubarmes-heu`
S/Z zeigen: normale Heunetze besitzen keinen belastbaren allgemeinen Staubreduktionsbeleg; kontrollierte Pferdestudien können bei Heunetzfütterung sogar höhere Partikelexposition zeigen. `staubarm` hängt u. a. von Heubehandlung und Fütterungsmanagement ab.

Es existiert bereits der neutrale Registry-Key `heunetze`.
Ein zweiter Produktvergleichs-Key mit unbelegter Staubarm-Eigenschaft darf keine Produkte duplizieren oder eine Gesundheitswirkung implizieren.

Folge:
`PRODUCT_COMPARISON_V1_NOT_APPLICABLE` für den aktuellen Key/Claim, solange keine eigenständige belastbare Produktklasse nachgewiesen wird.

## Delta

Von 24 `SUBTYPE_USE_CLASS_REQUIRED`:
- **14** -> `EVIDENCE_PRESENT`;
- **6** -> `REGISTRY_OVERLAP_KEY_AMBIGUITY`;
- **3** -> `EXACT_PRODUCT_IDENTITY_REQUIRED`;
- **1** -> `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`.

`SUBTYPE_USE_CLASS_REQUIRED` ist damit als Primärursache auf **0** abgearbeitet.

## Harte Grenze

`EVIDENCE_PRESENT` ist weiterhin nicht `PAIRING_READY`.
Die hier definierten Subtypen/Nutzungsklassen müssen später im Product-Knowledge-/Profil-/Policy-Weg maschinenfest gebunden werden, bevor das Plugin konkrete Paarfreigaben erteilen darf.

Kein Product-Knowledge-Import.
Kein SEO-/Providerlauf.
Kein Pluginbau.
Kein Merge.
Kein Publish.
