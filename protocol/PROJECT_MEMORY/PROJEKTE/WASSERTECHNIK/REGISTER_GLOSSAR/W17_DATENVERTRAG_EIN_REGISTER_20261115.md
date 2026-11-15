# WASSERTECHNIK W17 – Datenvertrag für EIN zentrales Fachregister
Datum 15.11.2026 · **Jetzt tatsächlich implementiert als strukturiertes JSON**, ohne WordPress-Schreiben, ohne neues Plugin.

## Problem und Lösung
W4–W16 enthalten Produktnamen und Quellen in unterschiedlich aufgebauten Dateien. Das erschwert die spätere Suche, das Fach-/Glossarverzeichnis, ein Anbieterregister, die kontrollierte SEO-Übernahme und das Zusammenführen doppelter Technikbezeichnungen.

**Einmaliger Forschungs- und Fachregister-Owner** ist daher ab W17:
`REGISTER_GLOSSAR/W17_ZENTRALES_FACHREGISTER_V1_20261115.json`
Dies ist ein **schreibfreier Forschungsdatenstand** und kein neuer WordPress-Importer. Der alte W16-Index bleibt nachvollziehbare Herkunft, wird aber nicht parallel zum neuen W17-Register fortgeschrieben. Historische Quellen und GitHub-SHAs sind im zentralen Register dokumentiert.

## Gleiche Grundstruktur für alle Datensätze
| Feld | Inhalt / Regel |
|---|---|
| `id` | stabile ID: bestehende W4-/W12-/W14-/W15-/W16-IDs bleiben; W17 neue `W17-Pxx`; Glossar `W17-Gxx`; Anbieterrubrik `W17-Rxx`; niemals IDs aus Menüposition ableiten |
| `typ` | **genau einer**: `produkt`, `glossar`, `anbieterrubrik` |
| `name`, `definition`, `synonyme` | sprechender Name, kurze sachliche Erklärung, abweichende Fachwörter; bei Bestand ohne geprüfte Kurzdefinition `null` statt Erfindung |
| `kanonisch_id` | eigene ID bei eigenständigem Datensatz; bei **nachgewiesener fachlicher Doppelung** Zeiger auf dieselbe kanonische Produktfamilie |
| `fachbereich` | originales Quellfachgebiet als erklärendes Label, **keine automatisch neue WP-Hauptkategorie** |
| `merkmale` | gleiche Filterfelder `funktionen[]`, `wasserarten[]`, `einsatzorte[]`, `zielgruppen[]`, `technologien[]` für ALLE drei Datensatztypen; ausschliesslich normierte Vokabeln für die ersten vier Filter |
| `merkmale_status` | `fachlich_geprueft`, `nach_quellbereich_vorlaeufig`, `noch_zu_bestimmen` – verhindert, dass automatische Zuordnung als Fachabnahme ausgegeben wird |
| `technikstand` | `marktprodukt`, `prototyp`, `studie`, `ungeklaert`, `nicht_anwendbar` (Glossar und Rubriken) |
| `bearbeitungsstand` | `bestand_w4`, `recherche_offen`, `grenzfall`, `alias`, `prototyp`, `glossar_entwurf`, `anbieterrubrik_entwurf` |
| `freigabe` | `bestehender_w4_fachowner` oder `nicht_freigegeben`; **keine automatische WordPress-Seite aus Produktliste** |
| `quellen[]` | strukturierte URL, Quellenart, Kenntnisstand – leeres Array bei fehlendem Originalbeleg |
| `seo` | bisherige W4-Owner-ID (sonst null), SEO-Status, ggf. später Searchvolumen, niemals fehlende Daten als null Suchanfragen deuten |
| `artikelkategorien[]` | ausschließlich produktbezogene, fachlich sinnvolle Kategorien; mindestens drei inhaltlich **verschiedene** mögliche Artikelideen pro Kategorie; bei Glossar/Register leer |
| `verknuepfungen[]` | stabile Referenzen zu Produkten, Glossar, Anbieter-Rubriken; kein weiterer SEO-Owner für einen bloßen Querverweis |
| `aktualisiert` | das Datum der Registeraufnahme; nicht mit Hersteller-Veröffentlichungsdatum verwechseln |

Alle Felder **bei jeder** Entität vorhanden, Datentyp und Filtervokabular bleiben gleich. Mehrere Filterwerte sind Arrays. Unbekannt = leeres Array oder `null`, **nie** erfundene Ausprägung. Neue passende Facetten werden einmal im globalen Vokabular ergänzt; bestehende Namen nicht stillschweigend umbenennen.

## Vier kontrollierte Kernfilter
`funktionen`: wasser_gewinnen, speichern, foerdern, verteilen, aufbereiten, desinfizieren, messen, steuern, schuetzen, wiederverwenden, entsorgen, waerme_uebertragen, reinigen.

`wasserarten`: trinkwasser, grundwasser, oberflaechenwasser, regenwasser, brauchwasser, grauwasser, abwasser, prozesswasser, pool_und_teichwasser, meerwasser.

`einsatzorte`: haus, garten, kleingewerbe, gastro_lebensmittel, vereine, landwirtschaft, camping_mobil, labor, industrie, kommune, medizin, oeffentliches_bad.

`zielgruppen`: privat, kleinbetrieb, verein, industrie, kommune.

Hinweis: `industrie`, `kommune`, `labor`, `medizin` in Quellen sind **Such-/Einsatzkontexte**, keine pauschalen Kauf-/Affiliate-Freigaben. Anbieter-Rubriken sind **nur Rubrikvorschläge**, keine erfundenen tatsächlich existierenden Anbieter.

## Drei Ausgabemöglichkeiten aus demselben Register
1. **Produktverzeichnis / Seitenplanung:** Filter `typ=produkt`; nach fachlichem Kanonisierungs- und SEO-Check letzte WP-Seitenebene `konkrete Produktart / System`; Produktkategorien darunter nur redaktionelle Beitragskategorien mit mindestens drei klar unterscheidbaren Artikeln. Kein Schattendatensatz fürs Menü.
2. **Glossar:** Filter `typ=glossar`; ein Fachbegriff mit verständlicher Definition und Produktreferenzen, **keine** künstliche technische Produktseite für einen Fachbegriff.
3. **HivePress-/Anbieterregister:** Filter `typ=anbieterrubrik`; Anbieter-/Dienstleistungstypen können später mit Produkten/Technologien verknüpft werden, aber vorerst **keine** einzelnen Firmen, Adressen, Bewertungen oder kommerziellen Behauptungen. Ein Anbieter erhält später einen separaten realen Verzeichniseintrag nur nach Verifizierung.

## KISS-Workflow: nur eine Entscheidung je Sachverhalt
Neuer Fund → **einmal** ins Register eintragen → gegen `kanonisch_id` fachlich auf Gleichheit prüfen → Produkt / Glossar / Anbieterrubrik **einmalig** zuweisen → Produkt wenn geeignet mit individuell passenden Kategorien und je 3+ Artikelansätzen vervollständigen → nach späterer SEO-/Importfreigabe über die **vorhandene** WT001-Pluginidentität übernehmen. Keine unabhängigen Nebenregister, keine versteckten nachgelagerten SEO-Entscheider, keine doppelten Provider-/API-Recherchen.

**Einziger Zustand dieser Version:** strukturiert und statisch prüfbar; noch kein WordPress-Import oder Live-Filter UI. Alle bisherigen W4-Owner sowie neuen W12/W14/W15/W16-Forschungsnamen, die W17-Neurecherche, Glossar und Register-Rubrikvorschläge bleiben im selben JSON. Der bisherige Fachbaum bleibt maßgeblich für alle aktuell angelegten WordPress-Seiten, bis ausdrücklich freigegeben umgestellt.
