# PRODUKTVERGLEICH – PROFILE / FACT MATRIX SPERRRIEMEN / REITHALFTER V1

Stand: 2026-09-11
Status: SOURCE-BOUND PROFILSPEC / NICHT MATERIALISIERT / NICHT SEO-FREIGEGEBEN

## Gemeinsame Hard Rule

Registry-Gruppen:
- `sperrriemen`;
- `reithalfter`.

Beide Gruppen sind **kompatibilitätsgebundenes Trensenzubehör**. Gleiche Produktbezeichnung oder gleiche Funktion reicht nicht für Cross-Brand-Pairing.

Pflicht vor jeder Paarbildung:
- konkrete Produkt-/Variantenidentität;
- konkrete Konstruktionsklasse;
- `compatible_bridle_system` bzw. belegte Kompatibilitätsmenge;
- Cross-Brand-Paar nur bei fachlich belegter Kompatibilitätsüberschneidung oder bei ausdrücklich systemunabhängiger Eignung.

Fehlt der Kompatibilitätsbeleg, ist das Ergebnis `NO_ELIGIBLE_COMPARISONS`, nicht eine freie Paarung.

---

## 1. Sperrriemen

Portal-Key:
`sperrriemen`

Technischer Key:
`sperrriemen`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

Gebundene Klasse:
`REPLACEMENT_FLASH_STRAP_FOR_COMBINED_NOSEBAND`.

Ausgeschlossen:
- kompletter Nasenriemen/Reithalfter;
- Kehlriemen;
- Gebissriemen;
- Kinnriemen/Kinnkette;
- Sporenriemen;
- integrierter Spezialriemen, der nicht als eigenständiges Ersatzteil geführt wird.

Pflichtfelder vor Pairing:
- `accessory_class`;
- `compatible_bridle_system`;
- `size_class`;
- `material`;
- `buckle_material`.

### Aktuelle Hersteller-/Direktprodukt-Evidence

Waldhausen:
- `Waldhausen S-Line Sperrriemen für Reithalfter`, Modell `98019` / Variante z. B. `9801901-WB`;
- eigenständiges Ersatzteil;
- europäisches Leder;
- Edelstahlschnalle;
- Größen PON und VB/WB;
- S-Line-Zubehör laut Hersteller auch mit X-Line kombinierbar.

Herstellerquelle:
https://www.waldhausen.com/waldhausen-s-line-sperrriemen-fuer-reithalfter/98019/

MONTIVUM / Pferdesporthaus Loesdau GmbH & Co. KG:
- `MONTIVUM Sperrriemen`, Art.-Nr. `59171`;
- Qualitätsleder;
- rostfreie Edelstahlschnalle;
- ausdrücklich passend für MONTIVUM-Trensen mit kombiniertem Reithalfter;
- zwei Größenvarianten im aktuellen Sortiment.

Direktprodukt-/Herstellerquelle:
https://www.loesdau.de/montivum-sperrriemen-59171.html

Zusätzlicher Marktbeleg ohne automatische Pairing-Freigabe:
- Loesdau/Florid `Sperrriemen`, Art.-Nr. `5917`, Qualitätsleder + Edelstahlschnalle, für kombinierte Reithalfter.

Quelle:
https://www.loesdau.de/sperrriemen-5917.html

### Faktenmatrix V1

1. `accessory_class`;
2. `compatible_bridle_system`;
3. `compatibility_scope` – spezifische Serien / ausdrücklich allgemein;
4. `size_class`;
5. `length_mm`;
6. `width_mm`;
7. `material`;
8. `buckle_material`;
9. `buckle_finish`;
10. `available_colors`;
11. `manufacturer_compatibility_claim`;
12. `care`;
13. `warranty`.

Nicht veröffentlichte Maße oder eine vermeintliche Universalpassform bleiben `NOT_IN_SOURCE`.

### Pairing-Regeln

- gleiche Gruppe `sperrriemen`;
- `accessory_class = REPLACEMENT_FLASH_STRAP_FOR_COMBINED_NOSEBAND`;
- gleiche oder belegbar überlappende Kompatibilitätsmenge;
- gleiche sinnvolle Größenklasse;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

**Fail-closed Sonderregel:**
Waldhausen S-Line/X-Line und MONTIVUM dürfen allein aufgrund gleicher Funktion **nicht** als konkretes Cross-Brand-Paar freigegeben werden, weil die aktuellen Quellen unterschiedliche Systembindungen nennen und keine gemeinsame Host-Kompatibilität belegen.

### Decision-Policy

- Klasse/Kompatibilität: `PAIRING_EQUAL_OR_OVERLAP_REQUIRED_NO_PREFERENCE`;
- Material, Schnalle, Größe/Farbe: sachliche Unterschiede;
- keine freie Aussage zu Haltbarkeit, Sicherheit, Druckwirkung oder Pferdekomfort;
- keine Universalität aus ähnlichen Abmessungen oder Optik ableiten.

---

## 2. Reithalfter

Portal-Key:
`reithalfter`

Technischer Key:
`reithalfter`

Vergleichstyp:
`PRODUCT`

### Harte Produktklassengrenze

`Reithalfter` ist Oberbegriff; englisch, englisch-kombiniert, schwedisch, hannoversch, mexikanisch und Spezialformen werden nicht gekreuzt.

Erste source-bound V1-Klasse:
`ENGLISH_COMBINED_REPLACEMENT_NOSEBAND_WITH_FLASH`.

Pflichtfelder vor Pairing:
- `noseband_class`;
- `flash_strap_included`;
- `flash_strap_removable`;
- `compatible_bridle_system`;
- `size_class`.

Ausgeschlossen bzw. separate Klassen:
- englisch ohne Sperrriemen;
- schwedisch kombiniert;
- hannoversch;
- mexikanisch;
- Spezial-/anatomische Wirkklassen, wenn die Grundklasse nicht ausdrücklich englisch-kombiniert ist;
- kompletter Trensenzaum statt eigenständigem Reithalfter/Wechselnasenriemen.

### Aktuelle Hersteller-/Direktprodukt-Evidence

Passier:
- `Anatomischer Wechselnasenriemen Englisch kombiniert mit Sperrriemen`, Art.-Nr. `959`;
- englisch-kombiniert;
- anatomisch geformt;
- Sperrriemen;
- Sperrriemenöse unterfüttert;
- beidseitig in passende Passier-Trensen einschnallbar;
- Passier Zaumleder;
- Größen Pony, Vollblut, Warmblut, Warmblut extra;
- Edelstahl- oder Messingbeschläge je Variante.

Herstellerquelle:
https://www.passier.com/de/Anatomischer-Wechselnasenriemen-Englisch-kombiniert-mit-Sperrriemen~p166271

MONTIVUM / Pferdesporthaus Loesdau GmbH & Co. KG:
- `MONTIVUM Englisch kombiniertes Reithalfter`, Art.-Nr. `580020`;
- eigenständiges Reithalfter zum Einbau in Trensen;
- englisch-kombiniert;
- abnehmbarer Sperrriemen;
- beidseitig verstellbar;
- Leder;
- aktuelle Größen-/Farbvarianten.

Direktprodukt-/Herstellerquelle:
https://www.loesdau.de/montivum-englisch-kombiniertes-reithalfter-580020.html

Waldhausen als zusätzlicher Klassenbeleg:
- aktuelle Reithalfter-Kategorie trennt englisch-kombiniert, schwedisch-kombiniert, hannoversch, englisch und schwedisch;
- `Waldhausen S-Line engl.komb. Reithalfter`, Art.-Nr. z. B. `9807301-WB`, als eigenständiges Ersatzteil.

Herstellerquellen:
https://www.waldhausen.com/pferde/trensenzaeume-zubehoer/reithalfter/
https://www.waldhausen.com/waldhausen-s-line-engl.komb.-reithalfter/9807301-wb/

### Faktenmatrix V1

1. `noseband_class`;
2. `flash_strap_included`;
3. `flash_strap_removable`;
4. `flash_loop_design`;
5. `compatible_bridle_system`;
6. `compatibility_scope`;
7. `size_class`;
8. `main_material`;
9. `noseband_padding`;
10. `chin_padding`;
11. `anatomical_shape`;
12. `bilateral_adjustment`;
13. `hardware_material`;
14. `available_colors`;
15. `manufacturer_fit_pressure_comfort_claims`;
16. `care`;
17. `warranty`.

### Pairing-Regeln

- gleiche Gruppe `reithalfter`;
- `noseband_class = ENGLISH_COMBINED`;
- eigenständiges Reithalfter/Wechselnasenriemen, kein kompletter Zaum;
- gleiche oder belegbar überlappende Kompatibilitätsmenge **oder** ausdrücklich systemunabhängige Einbaumöglichkeit;
- unterschiedliche Herstellerfamilien;
- aktueller pairable Lifecycle.

Anatomische Form, Polsterung und abnehmbarer Sperrriemen sind sichtbare Vergleichsfakten. Sie ersetzen den Kompatibilitätsbeleg nicht.

### Decision-Policy

- Reithalfterklasse/Kompatibilität: `PAIRING_EQUAL_OR_OVERLAP_REQUIRED_NO_PREFERENCE`;
- Sperrriemen-Ausführung, Material, Polsterung, Verstellung und Beschläge nur sachlich;
- keine freie Aussage zu Druckentlastung, Atmung, Kautätigkeit, Komfort, Passform oder Pferdefreundlichkeit;
- Herstellerclaims bleiben als solche gekennzeichnet;
- keine individuelle Verschnallungs-/Passformempfehlung aus Produktdaten.

## Produktvalidierung gegen die Profilspec

Fresh source-bound Gegenprüfung 2026-09-11:

- `sperrriemen`: mehrere reale eigenständige Ersatzprodukte sind belegt; aktuelle Waldhausen- und MONTIVUM-Produkte zeigen zugleich, warum `compatible_bridle_system` ein hartes Gate sein muss. **Kein konkretes Cross-Brand-Paar wird aus diesen beiden Produkten behauptet.**
- `reithalfter`: Passier 959, MONTIVUM 580020 und Waldhausen S-Line belegen reale englisch-kombinierte Einzel-Reithalfter/Wechselnasenriemen; konkrete Cross-Brand-Paarung bleibt von belegter Systemkompatibilität abhängig.

Damit sind beide Registry-Gruppen fachlich profilierbar, können technisch aber korrekt bei 0 zulässigen Paaren bleiben, solange Product Knowledge keine kompatible Cross-Brand-Konstellation belegt.

## Technische Materialisierungsgrenze

Dieses Dokument ändert `comparison-profiles.json` nicht.

Die Spezifikationen aus Akten 62–69 bleiben source-bound gesammelt. Vor technischer Materialisierung muss Product Knowledge pro konkretem Produkt/Variante die erforderliche Klassen- **und Kompatibilitätsbindung** source-bound tragen.

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
