# Wassertechnik W6 – schreibfreie WordPress-Gesamtvorschau
Stand: 14.11.2026 | **Kein Import, keine Änderung an WordPress, kein neues Plugin, keine API-Kosten.**

## 1. Quellen und Grenze
- Einzige fachliche Quelle: W4 `GESAMTFACHBAUM_W4_20261114.json`; W5 ist nur SEO-Priorisierung und enthält 218/218 zugeordnete Begriffe.
- Echter WordPress-Snapshot `wassertechnik-bestand.json` vom **14.11.2026, 12:28:47 UTC**, Site `https://wasser.oliver-beil.de/`, WT001 **0.1.1 zum Exportzeitpunkt**.
- Gesicherte WP-Objekte: **2 Seiten** (Beispielseite, Datenschutzerklärung), **1 Beitrag** (Hallo Welt!), **1 Kategorie** (Allgemein). Keine Wassertechnik-Objekte. HivePress im Snapshot nicht konfiguriert.
- Dieser Snapshot ist keine erneute Live-Abfrage, kein Beleg für spätere Änderungen. Kein Export neu angefordert, kein WP-Schreibzugriff.

## 2. Eine vollständige Vorschau
- **218 eindeutige Fach-Owner**, davon **113 geplante WP-Seiten** (8 Hauptbereiche, 19 Zwischenebenen, 1 Industrie-Einstieg, 6 Industrie-Landings, 79 Produktseiten) und **105 geplante WP-Beitragskategorien**.
- **79/79 Produktseiten** zu W4-Seitenpfaden zugeordnet, **105/105 Kategorien** über eindeutige vorgeschlagene Slugs jeweils genau einem Produktzweig zugeordnet.
- W4 hat **356 grobe Beitragsthemen**, die **nicht** als fertige WordPress-Beiträge oder Journalartikel ausgegeben werden.
- In der einen Prüfung: **0 doppelte Seitenpfade, 0 doppelte Rubrik-Slugs, 0 fehlende Elternseiten, 0 Kategorien ohne Produktbezug, 0 Überschneidungen mit den gemeldeten WP-Standardslugs, 0 Rubriken mit weniger als drei Themenideen**.
- `W6_WORDPRESS_IMPORTVORSCHAU_218_20261114.json` enthält alle **218** Vorschauzeilen mit Owner, Objektart, Elternzuordnung, Zielpfad bzw. Rubrikslug und W5-SEO-Priorität. Die bestehenden Fach- und Keywordquellen bleiben unverändert.
- **Achtung:** Die Rubriken sind WordPress-**Beitragskategorien**, keine Unterseiten. Der Produktpfad in der Datei ist eine redaktionelle Zuordnung; er ist **keine behauptete WordPress-Kategorie-Permalinkstruktur**.
- Bei **zwei Industrie-Landings ohne zugehörigen Produktzweig** sind die Slugs `industrielles-abwasser` und `kommunale-grossanlagen` nur aus den W4-Titeln für die spätere Übernahme vorgeschlagen, nicht in WP vorhanden.

## 3. Redaktionelle Reihenfolge: 27 vorhandene W4-Produktseiten
**P1 – 13 Produktzweige mit Suchvolumen ≥ 1.000 und Anbieter-Kauf-/Vergleichsabsicht:**
- Tauchpumpe – 18100 Suchanfragen/Monat, transactional; `pumpen-druck/pumpen/tauchpumpe`
- Gartenschlauch – 18100 Suchanfragen/Monat, transactional; `bewaesserung/gartenschlauch`
- Gartenpumpe – 12100 Suchanfragen/Monat, transactional; `pumpen-druck/pumpen/gartenpumpe`
- Schmutzwasserpumpe – 12100 Suchanfragen/Monat, transactional; `pumpen-druck/pumpen/schmutzwasserpumpe`
- Rückschlagventil – 12100 Suchanfragen/Monat, transactional; `pumpen-druck/steuerung-zubehoer/rueckschlagventil`
- Tiefbrunnenpumpe – 5400 Suchanfragen/Monat, transactional; `pumpen-druck/pumpen/tiefbrunnenpumpe`
- Bewässerungscomputer – 5400 Suchanfragen/Monat, transactional; `bewaesserung/steuerung/bewaesserungscomputer`
- Abwasserrohr – 5400 Suchanfragen/Monat, transactional; `abwassertechnik/entwaesserung/abwasserrohr`
- pH-Messgerät – 4400 Suchanfragen/Monat, transactional; `wasseranalyse/messgeraete/ph-messgeraet`
- Zisternenpumpe – 1900 Suchanfragen/Monat, transactional; `regenwasser/filter-foerderung/zisternenpumpe`
- Druckbehälter – 1300 Suchanfragen/Monat, transactional; `pumpen-druck/druckversorgung/druckbehaelter`
- Wasserhahnfilter – 1000 Suchanfragen/Monat, transactional; `wasseraufbereitung/trinkwasserfilter/wasserhahnfilter`
- Abwassertank – 1000 Suchanfragen/Monat, transactional; `abwassertechnik/aufbereitung-speicherung/abwassertank`

**P2 – 14 Produktzweige mit Suchvolumen ≥ 1.000 und Anbieter-Informationsabsicht:**
- Regentonne – 49500 Suchanfragen/Monat, informational; `regenwasser/regenspeicher/regentonne`
- Hauswasserwerk – 22200 Suchanfragen/Monat, informational; `pumpen-druck/druckversorgung/hauswasserwerk`
- Enthärtungsanlage – 9900 Suchanfragen/Monat, informational; `wasseraufbereitung/aufbereitungsanlagen/enthaertungsanlage`
- Hebeanlage – 9900 Suchanfragen/Monat, informational; `abwassertechnik/entwaesserung/hebeanlage`
- Revisionsschacht – 5400 Suchanfragen/Monat, informational; `abwassertechnik/entwaesserung/revisionsschacht`
- Bodenablauf – 3600 Suchanfragen/Monat, informational; `abwassertechnik/entwaesserung/bodenablauf`
- Kleinkläranlage – 2900 Suchanfragen/Monat, informational; `abwassertechnik/aufbereitung-speicherung/kleinklaeranlage`
- Systemtrenner – 2900 Suchanfragen/Monat, informational; `wasseraufbereitung/aufbereitungsanlagen/systemtrenner`
- Druckerhöhungsanlage – 1300 Suchanfragen/Monat, informational; `pumpen-druck/druckversorgung/druckerhoehungsanlage`
- Versenkregner – 1300 Suchanfragen/Monat, informational; `bewaesserung/bewaesserungssysteme/versenkregner`
- Fallrohrfilter – 1000 Suchanfragen/Monat, informational; `regenwasser/filter-foerderung/fallrohrfilter`
- Bodenfeuchtesensor – 1000 Suchanfragen/Monat, informational; `bewaesserung/steuerung/bodenfeuchtesensor`
- IBC-Wassertank – 1000 Suchanfragen/Monat, informational; `wassertanks/tankarten/ibc-wassertank`
- Tankdurchführung – 1000 Suchanfragen/Monat, informational; `wassertanks/tankdurchfuehrung`

**P3** sind alle übrigen vorhandenen Fach-Owner. Fehlende Volumina werden niemals als fehlende Nachfrage bewertet. Keine SEO-Rankingchance vorgetäuscht; organische Difficulty weiterhin nicht gemessen.

## 4. Drei Überschneidungen gemeinsam behandelt
1. **Rückspülfilter:** Manuell vs. automatisch sind im W4 anhand Bedienung und Technik fachlich getrennt. W5 hat für beide unterschiedliche konkrete Begriffe, aber keinen Beleg für voneinander getrennte Google-SERPs. **Beide W4-Owner vorläufig beibehalten; kein automatisches Zusammenlegen oder zusätzliche Seite.**
2. **Osmose:** Untertisch ist Einbaukontext; Direct-Flow ist tankloses Fördersystem; Drucktank ist Speicherbetrieb. W5: alle drei als transaktional klassifiziert, keine SERP-Überschneidung gemessen. **Bestehende Seiten als Kandidaten beibehalten, Inhalte strikt nach Aufgabe trennen, keine zusätzliche Parallelseite. Endgültige SEO-Trennung weiterhin fachlich offen.**
3. **Labortests:** Allgemeines Trinkwasser-Testpaket und gezieltes Schadstoff-Analysepaket unterscheiden sich nach Prüfanlass und Parametern. W5 meldet für beide kommerzielle Suchabsicht, aber kein Suchvolumen und keinen SERP-Vergleich. **Beide W4-Kandidaten beibehalten, keine automatische Zusammenlegung, letzte Intent-Abgrenzung offen.**

**Kein Anlass für ein neues Plugin, keinen weiteren DataForSEO-Gesamtlauf und keine separate Miniprüfung.** Diese drei Hinweise gehören zur einen Import-/Redaktionsabnahme.

## 5. Konkrete Importgrenze
- WordPress: **0 Schreibaktionen, 0 Löschungen, 0 neue Plugins**.
- Später **ADD-only** für freigegebene fehlende WP-Ziele; vorhandene Standardseiten nicht löschen oder verändern.
- Vor Freigabe ist die alte WP-Bestandsaufnahme bei Bedarf **einmal im selben Gesamtvorgang** gegen den dann tatsächlichen Stand abzugleichen, um doppelte Anlage zu verhindern.
- Die Freigabe bezieht sich ausschließlich auf die **W4-Struktur**, nicht auf Veröffentlichung von 356 Themen, HivePress-Anzeigen, Journal, Affiliate-Kacheln oder andere Portale.
- **Nächster Schritt:** W6-Gesamtvorschau und fachliche Grenzfälle als einen einzigen Freigabegegenstand behandeln; erst danach einmaliger schreibender ADD-only-Import, echte WP-Rücklesung nach dem Import (noch nicht erfolgt).
