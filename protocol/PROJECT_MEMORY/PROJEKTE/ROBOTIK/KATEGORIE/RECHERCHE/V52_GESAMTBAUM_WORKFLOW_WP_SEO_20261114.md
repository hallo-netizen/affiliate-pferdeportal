# Robotik – V52: Fachbaum acht Hauptwelten nach vollständiger Quellenprüfung; SEO nachweislich in WordPress

**14. November 2026 | Kategoriebüro (Fachplan), Recherchebüro (Master), WordPress nicht verändert.**

## 1. Welche Arbeit findet wo, wann und wie statt? – anhand echten PHP-Codes geprüft

1. **Recherchebüro:** Library `/robotik/Recherchebüro/CURRENT.json` enthält einzige führende Liste von Fundnennungen, Quellen und Entwicklungsständen. V52: weiterhin **581**, keine neuen IDs erfunden.
2. **Kategoriebüro:** fachliche Entscheidung für acht Hauptbereiche, konkrete Zielgruppen-Typseiten, jeweils 3 unterschiedliche Artikelrichtungen je flacher Inhaltskategorie; Code-freier Entwurf in GitHub/Library-Konzeptbüro. Hier KEINE SEO-Abfrage.
3. **Dann bestehende WP-Pluginlinie vorbereiten:** Korrektur des *bereits eingebetteten Importprofils* **erst nach ausdrücklicher Nutzerfreigabe**; aktuellen WP-Bestand schreibfrei prüfen. Keine neue Pluginidentität, keine eigenmächtige Änderung an veröffentlichten Seiten.
4. **SEO erfolgt in WordPress:** `Robotik Kategorie → DataForSEO` in derselben Original-Plugin-ZIP **v0.4.2**. `class-robotik-dataforseo.php` erzeugt Begriffe in `build_preflight()` ausschließlich aus `Robotik_First_Import::plan()` – **dem im Plugin eingebetteten Plan**, NICHT aus den live vorhandenen WP-Seiten. Daher ist die kostenlose WP-Keyword-Vorprüfung **auch vor einem Seitenimport** möglich. Es gibt ein WordPress-Adminformular `Gesamte Keywordliste prüfen (kostenlos)` – 0 API-Kosten. Bezahlte DataForSEO-Aufrufe über `Keyword Overview`, `Ideas` oder `Suggestions` erfordern im WP-Backend einen ausdrücklichen Haken und Klick; sie wurden hier NICHT gestartet.
5. **Korrektur anhand der WP-SEO-Ergebnisse im Fachplan / bestehenden Pluginprofil**, erneut schreibfreie Vorschau `Robotik Kategorie → Erstimport → Gesamtbaum prüfen`. Erst bei ausdrücklicher Freigabe kontrollierte Übernahme in WordPress mit echtem Readback. Der momentane feste 0.4.2-Plan deckt **nur die alten 72 Robotertyp-Seiten + 89 Inhaltskategorien** ab, nicht V52. SEO dort **ohne aktualisiertes Profil würde den neuen Baum NICHT prüfen**.
6. Magazin, Glossar, Finder, Modellregister und Anzeigenmarkt bleiben **gemeinsam**, eigenständige Säulen. Industrie bleibt unter Gewerbe nachgeordnet, Handwerk bleibt kaufnahe Gewerbe-Zielgruppe; keine Pflicht-Gemeinschaftsseite für unterschiedliche Privat-/Gewerbe-Suchintention.

**Beweispfade (Original-ZIP):** `robotik-kategorie-workflow/robotik-kategorie-workflow.php` lädt `Robotik_DataForSEO::boot()`; `includes/class-robotik-dataforseo.php` Zeilen 27–28 (WordPress-Menü), 104–126 (Begriffe aus eingebettetem Fachplan), 225–238 (kostenloser Vorabcheck und ausdrücklich freizugebender kostenpflichtiger Aufruf); `includes/class-robotik-first-import.php` Zeilen 24–31 (`plan()`), 224–244 (WP-Vorschau und Erstimport).

**Korrektur zu V51:** Die Darstellung „SEO nach Fachabschluss extern / gesondertes Plugin außerhalb WordPress“ ist **falsch**. SEO ist **ein vorhandener Backend-Bereich des bestehenden Kategorieplugins in WordPress**. Das Arbeitsbüro plant fachlich; Keywordrecherche/-prüfung findet im WordPress-Backend statt, sofern das angepasste Profil vorliegt.

## 2. 9 bestehende neue Funktionskandidaten: im Acht-Bereiche-Fachbaum V52 eingearbeitet

| Fund-ID | Künftiger fachlicher Pfad | Status |
|---|---|---|
| ROB-0220 | Garten → Mückenfangroboter | Forschungsprototyp, kein nachgewiesenes Seriengerät; Garten-Privatnutzen nur Einsatzidee |
| ROB-0408 | Pflege → Haarpflege → Haarwaschroboter | Forschungs- und Demonstratorsystem; keine nachgewiesene allgemeine klinische Auslieferung |
| ROB-0424 | Pflege → Mobilität → Blindenführroboter | Forschungs-/Versuchsstand; tatsächlicher Hilfsbedarf und Erprobungsbedingungen erläutern |
| ROB-0571 | Garten → Teichpflegeroboter | Forschungs-/Feldtests; private Teichnutzung als Szenario, keine Privatmarktbehauptung |
| ROB-0568 | Sport → Reaktionstrainer | Sport-Forschungsprototyp; keine Kaufbarkeitspflicht |
| ROB-0440 | Sport → Kletterwand-Routenroboter | Patent-/Konzeptidee, keine getestete Griff-Montage behaupten |
| ROB-0457 | Gewerbe → Elektronik-Reparaturroboter | Reparatur-Praxisbeleg nach ABB/Repartly; Aufgabengrenzen erläutern |
| ROB-0473 | Gewerbe → Biotoppflege-Roboter | Forschungsprojekt, keine Serienverfügbarkeit behaupten |
| ROB-0562 | Haushalt → Geschirrspüler-Einräumroboter | Nachgewiesene Forschungsteilaufgaben, keine fertige Haushaltsmaschine |

**Zusätzlicher zehnter Typ aus der Dreier-Grenzfallprüfung:** ROB-0570 → **Pflege → Haarpflege → Haarpflegeroboter**. Physisches weiches Fingerkämmen und Haar-Greifen ist eine andere Aufgabe als **Haarwaschroboter**; IEEE 2025 belegt einen Forschungsprototyp, keine Serienlieferung. Beide zusammen begründen die gemeinsame neue Seite `Pflege > Haarpflege` als Fach-Zwischenbereich. Quelle: https://ieeexplore.ieee.org/abstract/document/10973945

Für alle zehn Vorschläge sind jeweils **drei eigene flache Inhaltsrubriken mit je drei unterschiedlichen Artikelthemen** protokolliert: **30 Rubriken, 90 Themenansätze**. Kein Text und keine WP-Kategorie wurde erstellt. Die 10 Typen sind **nicht bereits importiert oder SEO-geprüft**.

## 3. Drei bisher offene Grenzfälle endgültig fachlich entschieden

- **ROB-0448 – kein eigener „Toilettenassistenzroboter“:** Die zitierte Studie beschreibt einen multifunktionalen **Pflegerollstuhl mit WC-Funktion** und weiteren Mobilitäts-/Körperpflegefunktionen. Sensorbasierte Selbstnavigation ist ausdrücklich noch in Entwicklung. Fachliche Verwendung: Pflege > Mobilität als Vergleich/Forschungs-Kapitel über multifunktionale Pflegerollstühle, **kein als nachgewiesen autonomer Toilettenroboter verkleideter Core-Typ**. Originalstudie: https://link.springer.com/article/10.1186/s12984-025-01751-4
- **ROB-0570 – eigene Seite:** Robotisches Haar-Kämmen/Greifen getrennt von robotischer Haarwäsche; Forschung nicht aus Kaufbarkeitsgründen ausfiltern. https://ieeexplore.ieee.org/abstract/document/10973945
- **ROB-0509 – keine eigenständige CORE-Roboterseite:** Die Herstellerbeschreibung zeigt die selbstreinigende Katzentoilette als **sensorgestützten Rotations-/Siebautomaten**. Das Werbewort „Litter-Robot“ beweist keine eigenständig navigierende oder manipulierende Robotik. Sachliches Haushalt/Haustier-**Vergleichskapitel** und ggf. Glossar-Einordnung; keine künstliche zusätzliche Robotertypseite. https://www.litter-robot.com/eu/de/how-it-works.html

## 4. Abschlussprüfung des gesamten Fachbaums – Zahlen und harte Grenzen

**Verbindliche Hauptnavigation:** **Haushalt · Garten · Freizeit · Sport · Bildung · Pflege · Humanoide · Gewerbe** (Gewerbe steht als achtes/letztes; Industrie unter Gewerbe als gesonderter Landingpagezugang).

| Hauptwelt | bisheriger V51-Entwurf | + neue V52-Funktionen | V52-Fachentwurf |
|---|---:|---:|---:|
| Haushalt | 17 | +1 | 18 |
| Garten | 12 | +2 | 14 |
| Freizeit | 14 | +0 | 14 |
| Sport | 15 | +2 | 17 |
| Bildung | 10 | +0 | 10 |
| Pflege | 12 | +3 | 15 |
| Humanoide | 12 | +0 | 12 |
| Gewerbe | 39 | +2 | 41 |
| **Summe** | **131** | **+10** | **141** |

- Original-Pluginprofil: **104/104 ursprüngliche WordPress-SEITEN-Planpositionen** unverändert, darunter **72/72 Robotertypen**, **89/89 ursprüngliche flache Inhaltskategorien** und 356 ursprüngliche Artikelrichtungen; keine Original-IDs, -Slugs oder -Eltern verändert.
- + **47/47 V46-**Kontextseiten im Entwurf behalten (darunter **16 weiterhin gesondert vor WP-SEO zu prüfende Kandidaten**), + **12/12 V50-**Humanoiden-Fachseiten; **vier humanoide Zukunftskapitel** bleiben Kapitel, keine Doppel-Zielseiten.
- + **10/10 V52-Typkandidaten** aus den vorhandenen Forschungsmeldungen, ohne neue Forschungs-IDs. **141/141 Endseiten-Fachpfade eindeutig**. **296 geplante Inhaltsrubriken / 977 unterschiedliche grobe Artikelrichtungen** (nicht veröffentlichte Beiträge!). Alle zehn neuen Fachrubrikgruppen erfüllen jeweils 3 × 3.
- **14 maschinelle Integritätsprüfungen bestanden**, inklusive aller alten IDs, Bestandskategorien, 8er-Reihenfolge, keine doppelten Endpfade, echte Themenprobe, nichts nach WordPress geschrieben. Prüfnachweis `V52_READBACK_VALIDIERUNG.json`.
- **Sachliche Grenzen:** Die Fachstruktur ist auf Konsistenz/Vollständigkeit geprüft, aber **keine SEO- oder Importfreigabe**. 16 alte V46-Such-/Robotik-Kollisionen bleiben als offener WordPress-SEO-Prüfbestand gekennzeichnet; frühe Entwicklungsstände bleiben ehrlich als Forschung/Patente/Konzepte. Im wirklichen WordPress live installierter Baum/Pluginversion heute nicht unabhängig ausgelesen. Kein aktueller WP-Readback behauptet.
- **Rechercheregister**: 581 Fundnennungen bleiben 581, nicht 141 eindeutige Modelle. Bereits existierende Forschungseinträge nur redaktionell neu bewertet. Original-Quellen-/Overlapgruppen unberührt.

## 5. Konkreter nächster Arbeitsschritt ohne Schleifen

**Nicht mehr separat außerhalb von WordPress SEO recherchieren.** Nach ausdrücklicher Freigabe das überprüfte V52-**Kategorienprofil** in die eine vorhandene WordPress-Pluginlinie überführen, zunächst **ohne Seiten zu schreiben**, dann im WP-Menü `Robotik Kategorie → DataForSEO` den neuen vollständigen Baum kostenlos vorprüfen (Paid nur nach gesonderter Freigabe), Ergebnis in einer einmaligen fachlichen Korrekturrunde bearbeiten, danach im gleichen Plugin Gesamtbaum-Vorschau/Live-Readback/Import nur nach ausdrücklicher Zustimmung. Keinen alten 72er SEO-Test als Prüfung des 141er Baumes ausgeben.

## Ablage

- **Einziger Research-Master**: Library `/robotik/Recherchebüro/CURRENT.json` V52 (581 Fundnennungen unverändert; nur Meta-Arbeitsstand ergänzt).
- **Fach-/SOLL-Baum**: Library `/robotik/Konzeptbüro/V52_ACHTWELTEN_GESAMTBAUM_NUR_FACHENTWURF.json` als abgeleitete Lesefassung plus identische GitHub-Version `RECHERCHE/V52_ACHTWELTEN_GESAMTBAUM_PROFIL_NUR_FACHENTWURF.json`.
- **Einzelfälle**: `RECHERCHE/V52_10_NEUE_FACHSEITEN.csv`, `RECHERCHE/V52_3_GRENZFAELLE_ENTSCHEID.csv`, `RECHERCHE/V52_READBACK_VALIDIERUNG.json`. Keine 2. führende Forschungsliste.