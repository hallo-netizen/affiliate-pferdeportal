# Hab & Bewahr – vollständige Grobprüfung aller 265 konkreten Themenseiten
**17.10.2026 – FACHLICHER ENTWURF ABGESCHLOSSEN, NICHT IN WORDPRESS SYNCHRONISIERT**

## Zielvertrag und tatsächlicher aktueller Zustand
- Zu prüfen waren **alle 93 bisherigen R3-Themenseiten und 172 neuen C2.2-Themenseiten** auf der letzten Seitenebene.
- FAQ sind ab sofort **Pflicht** bei jedem Thema; ebenso **Beratung** – jedoch darf eine vorhandene Auswahl-/Beratungskategorie denselben Bedarf erfüllen, damit keine Dubletten entstehen.
- Vergleiche sind fast überall sinnvoll: Systeme, Ausstattung, unterschiedliche Produktgruppen und später konkrete Kaufprodukte. Bei **zwei überwiegend sicherheits-/ablauforientierten Alt-Themen** bleibt Vergleich in die Beratung integriert, statt eine künstliche Vergleichskategorie zu erzeugen.
- Kosten, Pflege, Wartung, Montage, typische Fehler, Nachrüstung, Versicherungen, Organisation sowie neue Einsteiger-/Fortgeschrittenen-Aspekte sind **nur individuell und bei eigenständigem Mehrwert** Kategorien. Rund **3–5 mögliche spätere Einzelbeiträge** je Endkategorie genügen als Grobmaßstab. Keine Artikel-/Redaktionsplanung und keine Keyword-Pflicht.

## Gegen den echten bisherigen Bestand verglichen
| Bestand | Aktueller fachlicher Status |
|---|---|
| 93 ursprüngliche Themenseiten mit 285 historischen Artikelkategorien | Vorhanden und geschützt. Bislang **0 ausdrücklich benannte FAQ und 0 Vergleichskategorien** |
| 172 neue C2.2-Themenseiten mit 566 ursprünglichen Artikelkategorien | Erfolgreich importiert |
| 172 FAQ, 172 Vergleiche, 102 weitere optionale und 26 fachliche Ergänzungen | Als zweite Welle erfolgreich importiert (472) |
| Beratung innerhalb der 172 neuen Themen | Nach semantischer Bestandsprüfung **43 ausreichend erkennbare vorhandene Auswahl-/Beratungsbereiche; 129 zusätzliche Beratungsbereiche erforderlich** |

Die alten Themenseiten hatten nicht dieselbe Vertiefungswelle erhalten. **Das ist ein fachlicher Systemfehler der früheren Bearbeitung und keine einfache Darstellungsfrage.**

## Ergebnis – selektive Nachholung
**475 zusätzliche Kategorie-Vorschläge**, jeweils exakt einem der 265 Themen zugeordnet:

| Ergänzung | 93 alte Themen | 172 neue Themen | Gesamt |
|---|---:|---:|---:|
| FAQ | 93 | 0 | 93 |
| Beratung | 93 | 129 | 222 |
| Vergleich | 91 | 0 | 91 |
| Weitere jeweils eigenständige Perspektiven | 63 | 6 | 69 |
| **Gesamt** | **340** | **135** | **475** |

**Nicht Schema F:** **30** zunächst erörterte Zusatzkategorien bei den alten Themen und **15** bei den neuen Themen wurden nach Abgleich mit den dort bereits vorhandenen Kategorien wieder entfernt. Unter den 15 neuen waren sogar **zwei inhaltlich falsch zugeordnete Ideen**, die ausdrücklich nicht weiterverfolgt werden. Andere Themen brauchen neben FAQ, Beratung und ggf. Vergleich **keine** zusätzliche Kategorie.

## Verbindliches Sprach- und Verständlichkeitsprinzip
Beispiel **Vandalismus & Zerstörung → Außentechnik → PV, Kamera & Beleuchtung**, echte ältere Seite **WP-Page-ID 141**:

- **Kurztitel im Mega:** „PV, Kameras & Licht“
- **Ausführlicher H1:** „PV-Anlagen, Kameras und Außenbeleuchtung vor Vandalismus schützen“
- **Einführung:** „Wie Sie Photovoltaikanlagen, Kameras, Leuchten und Leitungen gegen mutwillige Beschädigung und Manipulation sichern.“
- **Bisherige Artikelkategorien, sprachlich eindeutig vorgeschlagen (nicht live geändert):**
  - Term **205**: „Überwachungskameras vor Sabotage schützen“ statt „Kameras & Licht vor Sabotage“
  - Term **273**: „PV-Anlagen und Kabel vor Beschädigung schützen“ statt „PV-Technik & Kabel“
  - Term **304**: „Außenbeleuchtung vor Vandalismus schützen“ statt „Außenbeleuchtung schützen“
- **Zusätzliche Fachkategorien nach Bedarf:** themenspezifische FAQ, Schutzberatung, Vergleich geeigneter Lösungen, regelmäßige Kontrolle exponierter Anlagen.
- Sämtliche bestehenden physischen WordPress-IDs, Slugs, URLs und Artikelzuordnungen **unverändert**. Kurztitel und H1 dürfen abweichen; Sprachkorrekturen später als gezielte Design-Ausgabe oder als identitätserhaltende Textänderung, nicht als URL-/Term-Import.

## Autoritative GitHub-Arbeitsnachweise
1. `KATEGORIEN/C23_265_THEMEN_EBENENPRUEFUNG_20261017.json`: **265 individuelle Owner**, vorhandene 285+566+472 Kategorien, fachlich belegte Pflicht- und Zusatzbereichsentscheidungen, verworfene Vorschläge, sprachliche Display-Korrekturen.
2. `KATEGORIEN/C23_475_ERGAENZUNGEN_GEBUNDENES_FACHDELTA_20261017.json`: **475 ausschließlich additive Vorschläge**, 340 gebunden an bekannte physische alte Seite-3-WP-IDs und 135 an die tatsächlich vorhandenen C2.2-Topic-Kennungen, 475 eindeutige neue Knotenkennungen, **8/8 Negativtests abgewiesen**, keine erfundenen WP-Term-IDs.
3. Zielvertrag `KONZEPT/ZIELVERTRAG_KATEGORIEN_MINDESTENS_3_OHNE_MAXIMUM_20261015.md` um die neuesten Nutzeranweisungen zu FAQ-/Beratungspflicht und individuelle Zusatzaspekte ergänzt.

## Genau eine NEXT ACTION
**Den 475er Nachholbestand im bestehenden Kategorieplugin** als **getrennten, gesicherten zusätzlichen Add-only-Durchlauf** implementieren und am Originalplugin lokal vollständig positiv und negativ simulieren – Originalimport 743 + zweite Welle 472 + 285 Altterms und vier historische Artikelbindungen dürfen **nicht verändert** werden. Alte Owner werden über ihre vorhandenen echten WordPress-Page-IDs an die bestehende Snapshotbindung angeschlossen; neuere über die bereits bekannten SHA-basierten C2.2-Topic-IDs.

**Bis die Implementation nachweislich getestet und separat freigegeben ist, keine WordPress-Schreibaktion.** Das bloße GitHub-Manifest ist noch kein installierbares Plugin und kein Importerfolg. Bestehenden Designplugin-Scope für verständliche Labels getrennt behandeln.
