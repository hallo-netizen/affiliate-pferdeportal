# PRODUKTVERGLEICH – PROFILE / FACT MATRIX TRENNWÄNDE / STALLDOKUMENTE / FUTTERTAFELN V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Registry-Gruppen:
- `trennwaende-im-offenstall`;
- `stallordner-und-dokumentenmappen`;
- `futterkarten-und-boxenschilder`.

Sammelbegriffe werden nicht blind gekreuzt.
Jede Gruppe erhält für V1 eine konkret gebundene Unterklasse; weitere Unterklassen dürfen nur source-bound ergänzt werden.
Finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin aus aktuellem Product Knowledge.

---

## 1. Trennwände im Offenstall

Portal-Key:
`trennwaende-im-offenstall`

Technischer Key:
`trennwaende-im-offenstall`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Gebundene Oberklasse:
`GROUP_HOUSING_PARTITION_WALL_SYSTEM_COMPONENT`.

Fachbindung aus Akte 55 bleibt zwingend:
- Trennsystem für Gruppenhaltung/Lauf-/Offenstall;
- keine Boxentrennwand, wenn nur Einzelboxennutzung belegt ist;
- kein Fressgitter;
- kein Fressstand;
- kein Tor/Paneltor;
- keine komplette Stallbauleistung ohne identifizierbare Trennwandkomponente.

Pflichtfelder vor Pairing:
- `housing_use_class`;
- `partition_function_class`;
- `mobility_class` = FIXED / MOVABLE / SLIDING / SWIVELLING;
- `construction_class`;
- `configuration_identity`.

**Fail-closed:**
Ohne identische normalisierte Beweglichkeits-/Konstruktionsklasse und konkrete Konfigurationsidentität entsteht kein Paar.

### Aktuelle Hersteller-Evidence

Röwer & Rüb GmbH:
- aktueller Produktbereich `Lauf- und Offenställe für flexible Gruppenhaltung`;
- Hersteller beschreibt Lauf-/Offenställe als individuell geplante Gruppenhaltung;
- Fressstände können mit den eigenen Trennwänden kombiniert werden;
- allgemeiner aktueller Trennwand-Produktbereich ist als flexibel kombinierbar/anpassbar ausgewiesen;
- aktuelle Seite veröffentlicht jedoch für den Gruppenhaltungs-Kontext keine einzelne SKU/Standardkonfiguration mit vollständigen Maßen.

Herstellerquellen:
https://www.roewer-rueb.com/produkte/zubehoer/laufstaelle/
https://roewer-rueb.de/produkte/pferdeboxen/

Mulder Stall und Hof:
- aktuelles Produkt `Außenstall für Gruppenhaltung mit 15 Fressplätzen`;
- konkrete Systemkonfiguration mit drei Abteilen à 4000 x 4000 mm;
- ausdrücklich vollständig geschlossene Trennwände;
- Stahlprofile 50 x 50 mm C-Profil;
- Kunststoff- oder Bambusplanken, 32 mm;
- Einsatzbereich Gruppenhaltung.

Hersteller-/Direktproduktquelle:
https://www.mulderstallundhof.de/product/aussenstall-fuer-gruppenhaltung/

Zusätzlicher source-bound Klassenbeleg:
- Horse-Tec HT-Stallsystem führt verschiebbare Trennwände für flexible Gruppen-/Offenstallhaltung; diese **MOVABLE**-Klasse darf nicht automatisch gegen FIXED-Systeme gepaart werden.

Quelle:
https://www.heuraufe.de/ht-stallsystem

### Faktenmatrix V1

1. `housing_use_class`;
2. `partition_function_class`;
3. `mobility_class`;
4. `construction_class`;
5. `configuration_identity`;
6. `height_mm`;
7. `length_mm`;
8. `frame_material`;
9. `frame_profile_mm`;
10. `infill_material`;
11. `infill_thickness_mm`;
12. `open_closed_design`;
13. `visual_contact_design`;
14. `mounting_system`;
15. `floor_or_wall_fixing`;
16. `system_compatibility`;
17. `manufacturer_safety_social_contact_claims`;
18. `warranty`.

Nicht veröffentlichte Belastbarkeit, Durchtrittfestigkeit, statische Nachweise oder Sicherheitswerte bleiben `NOT_IN_SOURCE`.

### Pairing-Regeln

- gleiche Gruppe `trennwaende-im-offenstall`;
- Gruppen-/Lauf-/Offenstallnutzung source-bound;
- identische normalisierte `mobility_class`;
- identische normalisierte `construction_class`;
- konkrete `configuration_identity` je Produktseite/Systemkomponente;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Der aktuelle Evidence-Stand belegt die Produktklasse, **aber noch kein konkretes Cross-Brand-Paar** zwischen Röwer & Rüb und Mulder, weil die konkrete Röwer-&-Rüb-Gruppenhaltungs-Trennwandkonfiguration auf der aktuellen Webquelle nicht ausreichend parametrisiert ist.

### Decision-Policy

- Nutzung/Beweglichkeit/Konstruktionsklasse: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Profil, Füllung, Montage und Sichtkontaktgestaltung nur sachlich;
- keine freie Sicherheits-, Sozialkontakt-, Haltbarkeits- oder Wartungswertung;
- Herstellerclaims zu Pferdesicherheit/Komfort bleiben Herstellerclaims;
- Systemkompatibilität darf nicht aus optischer Ähnlichkeit abgeleitet werden.

---

## 2. Stallordner und Dokumentenmappen

Portal-Key:
`stallordner-und-dokumentenmappen`

Technischer Key:
`stallordner-und-dokumentenmappen`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound Cross-Brand-V1-Klasse:
`A4_PP_3_FLAP_ELASTIC_DOCUMENT_FOLDER`.

Pflichtmerkmale:
- DIN A4;
- Polypropylen-Kunststoff;
- drei Innen-/Schutzklappen;
- Elastik-/Gummizugverschluss;
- lose Dokumente ohne Lochung aufnehmen.

Ausgeschlossen bzw. separate Klassen:
- Ringordner/Lever-Arch-File;
- Ringbuch;
- Clipmappe;
- Reißverschluss-Dokumententasche;
- wasserfeste Aushangtasche;
- Hängeregister;
- digitale Stallmanagementsoftware;
- Pferdepass-Spezialmappe als eigener Registry-/Nutzungskontext.

Motiv/Farbe ist kein Pairing-Gate.

### Aktuelle Hersteller-Evidence

HERMA GmbH:
- `Sammelmappe A4 PP Pferde`, Art.-Nr. `7140`;
- DIN A4;
- Polypropylen;
- Gummi-Eckspanner;
- drei Innenklappen;
- für loses Schriftgut/Dokumente;
- abwaschbar laut Hersteller.

Herstellerquelle:
https://www.herma.de/buero-zuhause/produkt/sammelmappe-a4-pferde-7140/

Exacompta:
- `3 Flap Folders with Elastic Straps OpaK Polypropylene A4`, Ref. `55812E`;
- A4;
- PP;
- Materialstärke 5/10 mm;
- Außenmaß 24 x 32 cm;
- Kapazität 200 Blatt 80 g/m²;
- drei Klappen;
- Elastikverschluss.

Herstellerquelle:
https://www.exacompta.com/en/product/55812E/3-flap-folders-with-elastic-straps-opak-polypropylene-a4

### Faktenmatrix V1

1. `document_storage_class`;
2. `paper_format`;
3. `material`;
4. `material_thickness_mm`;
5. `flap_count`;
6. `closure_type`;
7. `capacity_sheets_80gsm`;
8. `outer_width_mm`;
9. `outer_height_mm`;
10. `outer_depth_mm`;
11. `washable_claim`;
12. `label_or_index_feature`;
13. `color_or_design`;
14. `recycled_material_claim`;
15. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `stallordner-und-dokumentenmappen`;
- `document_storage_class = A4_PP_3_FLAP_ELASTIC_DOCUMENT_FOLDER`;
- drei Klappen + Elastikverschluss zwingend;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Kapazität darf nur verglichen werden, wenn Hersteller dieselbe Papiergrammatur oder eine sauber umgerechnete, source-bound Angabe liefern. Motiv `Pferde` ist kein Qualitätsargument.

### Decision-Policy

- Klasse/Format/Mechanik: `PAIRING_EQUAL_NO_PREFERENCE`;
- Materialstärke, Maße, Kapazität, Design und Recyclingclaim sachlich;
- keine freie Aussage zu Robustheit, Wasserfestigkeit, Lebensdauer oder Stallgeeignetheit aus PP allein;
- `abwaschbar` nur als Herstellerclaim;
- keine digitale Lösung gegen physische Mappe.

---

## 3. Futterkarten und Boxenschilder

Portal-Key:
`futterkarten-und-boxenschilder`

Technischer Key:
`futterkarten-und-boxenschilder`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Erste source-bound Cross-Brand-V1-Klasse:
`SINGLE_HORSE_REWRITABLE_FEED_PLAN_BOARD`.

Pflichtmerkmale:
- physisches Schild/Tafel;
- expliziter Futterplan für ein einzelnes Pferd bzw. eine einzelne Box;
- wiederbeschreibbar/abwischbar;
- manuelle Beschriftung;
- für Stall/Box vorgesehen.

Ausgeschlossen bzw. separate Klassen:
- reines Namens-/Abstammungsschild ohne Futterplan;
- Warnschild;
- Mehrpferde-Zentralfutterplan;
- reine Papier-Futterkarte ohne feste Tafel;
- digitale Futterplan-App;
- nicht wiederbeschreibbares Individualschild.

### Aktuelle Hersteller-/Direktprodukt-Evidence

Krämer Pferdesport GmbH & Co. KG:
- `Stalltafel mit Futterplan`, Nr. `430788`;
- 33 x 33 cm;
- Futterplan;
- Fotolasche für Pferdefoto oder Notizen;
- als Stalltafel/Boxenschild im aktuellen Sortiment geführt.

Direktproduktquelle:
https://www.kraemer.de/Stalleinrichtung/Stallzubehoer-Reitplatzzubehoer/Boxenschilder-Warntafeln/Stalltafel-mit-Futterplan

Stallschild-Profi:
- `Futterplan fürs Pferd (Motiv 2)`;
- Schild zum Selbstbeschriften mit wasserlöslichem Edding oder Kreidestift;
- Standard DIN A4, 29,7 x 21 cm;
- Beschriftung mit Schwamm/Wasser wieder entfernbar;
- individueller Futterplan für die Stallgasse/Box.

Direktproduktquelle:
https://stallschild-profi.de/alle-produkte/futterplaner-fuer-pferde/futterplan-fuers-pferd-2/

Zusätzliche aktuelle Material-/Variantenquelle:
https://stallschild-profi.de/alle-produkte/futterplaner-fuer-pferde/deine-futterplan-design-vorlage/

### Faktenmatrix V1

1. `stall_information_class`;
2. `horse_scope` – SINGLE_HORSE / MULTI_HORSE;
3. `feeding_plan_fields`;
4. `rewritable`;
5. `writing_tool_type`;
6. `wipe_clean_method`;
7. `width_mm`;
8. `height_mm`;
9. `board_material`;
10. `weather_resistance_claim`;
11. `photo_slot`;
12. `customizable_text_or_logo`;
13. `mounting_holes`;
14. `magnetic_surface`;
15. `included_writing_accessories`;
16. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `futterkarten-und-boxenschilder`;
- `stall_information_class = SINGLE_HORSE_REWRITABLE_FEED_PLAN_BOARD`;
- `horse_scope = SINGLE_HORSE`;
- wiederbeschreibbare physische Tafel;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Ein zentraler Futterplan für 10/24 Pferde darf nicht gegen ein Einzelpferd-Schild gepaart werden. Ein Namensschild ohne Futterfelder darf nicht allein wegen gleicher Montageposition eingeschleust werden.

### Decision-Policy

- Klasse/Pferdeumfang/Wiederbeschreibbarkeit: `PAIRING_EQUAL_NO_PREFERENCE`;
- Maße, Material, Foto-/Individualisierungsfelder, Montage und Zubehör sachlich;
- keine freie Aussage zu Fehlervermeidung, Fütterungssicherheit, Haltbarkeit oder Wetterfestigkeit;
- Gesundheits-/Fütterungsaussagen des Anbieters sind keine Produktleistungsbelege;
- keine fachliche Rationsbewertung aus dem Schilddesign ableiten.

## Globale Verbote für alle drei Gruppen

- keine Boxentrennwand automatisch als Offenstall-/Gruppenhaltungs-Trennwand;
- keine unterschiedlichen Trennwand-Beweglichkeitsklassen kreuzen;
- keine Ringordner/Software gegen 3-Klappen-Sammelmappe;
- kein Namensschild oder Mehrpferdeplan gegen Einzelpferd-Futtertafel;
- kein Gesamtsieger;
- keine Punkte/Sterne/Rankings;
- keine Shop-/Affiliate-Verfügbarkeit als Fachargument;
- keine Sicherheits-, Haltbarkeits-, Wetter- oder Gesundheitswertung ohne direkte Evidenz;
- Quellenlücke bleibt `NOT_IN_SOURCE`.

## Produktvalidierung gegen die Profilspec

Fresh source-bound Gegenprüfung 2026-09-11:

- `trennwaende-im-offenstall`: Röwer & Rüb sowie Mulder belegen reale Trennwandkomponenten/Systeme im Gruppenhaltungs-/Lauf-/Offenstall-Kontext; wegen unvollständig identischer Konfigurationsparameter wird **noch kein konkretes Cross-Brand-Paar behauptet**;
- `stallordner-und-dokumentenmappen`: HERMA 7140 + Exacompta 55812E belegen zwei unabhängige A4-PP-Sammelmappen mit drei Klappen und Elastikverschluss;
- `futterkarten-und-boxenschilder`: Krämer 430788 + Stallschild-Profi Futterplan Motiv 2 belegen zwei unabhängige physische Einzelpferd-Futtertafeln; konkrete Schreib-/Abwischbarkeit der Krämer-Tafel muss vor technischer Paarfreigabe im Product Knowledge source-bound vollständig vorliegen, sonst fail-closed.

Das ist keine finale Paarfreigabe und keine Markt-Vollständigkeit.

## Technische Materialisierungsgrenze

Dieses Dokument ändert `comparison-profiles.json` nicht.

Die Spezifikationen aus Akten 62–71 bleiben source-bound gesammelt. Vor technischer Materialisierung muss Product Knowledge pro Produkt/Variante die Klassenbindung und Pflichtfakten tragen.

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
