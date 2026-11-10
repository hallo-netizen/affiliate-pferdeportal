# ROBOTIK – Kurze Navigation & acht Hauptwelten (Fachentwurf V4)
**Stand 10.11.2026 · Noch NICHT für WordPress freigegeben · KEINE SEO-Recherche.**

## Nachprüfung der behaupteten „6–8 Hauptkategorien“
**Beleg:** `PROJEKTE/HOBBYRAUSCH/KONZEPT/KONZEPT_ZWISCHENSTAND_KATEGORIEN_UND_INTERNE_SUCHE_20260930.md` enthält den wörtlichen Konzeptstand **„Die Hauptnavigation hat ungefähr 6–8 verfügbare Slots“** sowie die Forderung nach sehr kurzen, verständlichen Namen. Das war ein **Hobbydepot-Planungsstand**, keine bisher technisch bewiesene feste Robotik-Slot-Zahl. Im späteren Hobbydepot-Zielbaum wurden **acht** Hauptwelten umgesetzt (`HOBBYRAUSCH/SEO_KATEGORIEN/KONZEPT_3_SAEULEN_ZIELBAUM_20261007.md`).
**Robotik-Entscheidung:** **acht** ist ein schlüssiges **vorläufiges Navigationsziel**; die fachliche Vollständigkeit hat Vorrang. Falls im Robotik-Design/WordPress später eine Bezeichnung nicht passt, wird die Darstellung angepasst, nicht ungeprüft ein Produkttyp gestrichen.

**Fehlerlehre Hab & Bewahr:** `EIGENTUMSSCHUTZ/KONZEPT/KATEGORIEN_NAVIGATION_PORTALSTANDARD_FEHLERLEHREN_20261017.md` und `.../ZIELVERTRAG_KATEGORIEN_MINDESTENS_3_OHNE_MAXIMUM_20261015.md` trennen **kurze Anzeigenamen von H1/Meta** und warnen vor künstlichen Mengenobergrenzen, Duplikaten/verschluckten Menüeinträgen und pauschalen Kategorie-Schablonen. Übernommen als Robotik-Regel, **nicht** deren historische 6-Welten-Struktur kopiert.

## Einzige aktuelle acht Hauptwelten (Navigation, Entwurf)
| Navigationsname | Sichtbare direkte Bereiche (Entwurf) | Alte Forschungswelten zur lückenlosen Umstellung | Produktarten aus ursprünglichem Bestand |
|---|---|---|---:|
| **Technik** | Fertigung · Software · Komponenten · Bildung | Industrie & Fertigung + Bildung & Forschung | **16** |
| **Logistik** | Transport · Lager · Lieferung | Lager & Transport | **8** |
| **Gastro & Handel** | Gastronomie · Hotel · Empfang · Handel | Gastronomie, Handel & Hotel | **6** |
| **Reinigung** | Bodenreinigung · Fassaden · Anlagen · Spezialreinigung | Reinigung & Gebäude | **6** |
| **Landwirtschaft** | Tierhaltung · Feldrobotik · Gewächshaus · Weinbau | Landwirtschaft & Tierhaltung | **7** |
| **Medizin** | Operation · Rehabilitation · Kliniklogistik · Labor · Apothekentechnik | Medizin, Pflege & Labor | **6** |
| **Bau & Sicherheit** | Baurobotik · Inspektion · Überwachung · Rettung | Bau & Infrastruktur + Inspektion, Sicherheit & Rettung | **13** |
| **Haushalt & Freizeit** | Haushalt · Garten · Sportanlagen | Haushalt & Garten | **6** |
| **GESAMT** | Ohne versteckte Bereiche; je tatsächlichem Kind mindestens eine sinnvolle Funktion | Alte 10 Forschungswelten in 8 Navigationswelten aufgenommen | **68 / 68** |

**Warum so und nicht pauschal 6 oder 10?** Die ursprünglichen **zehn** Hauptwelten wurden **ohne Verlust** der stabilen 68 Produkt-IDs neu gruppiert; das große Sachgebiet Bildung und Lernrobotik bleibt unter **Technik → Bildung**, nicht unter Haushaltsrobotik. Robotiksoftware und Robotik-Komponenten werden unter **Technik** ausdrücklich sichtbar, nicht in einem Magazin-Technikbereich versteckt. Sportgeräte werden unter **Haushalt & Freizeit → Sportanlagen** vorläufig aufgefangen, statt wegen EINEM belegten Golfball-Sammelroboter einen künstlich leeren neunten Hauptwelt-Kasten zu schaffen. Bau, Anlagenkontrolle und Rettung leben unter **Bau & Sicherheit** mit **getrennten** Zwischenbereichen.

**Rollenoffenheit:** Der Begriff „Gastro & Handel“ ist ein kurzes Menüwort für Gastronomie, Hotel und Handel, nicht der Anbieter-/Service-Anzeigenmarkt. „Technik“ ist der **Produktkatalog** für Maschinen, Software und Komponenten, nicht dasselbe wie Magazinartikel „Robotiktechnik verstehen“. Bei Bau/Sicherheit sind Eigentumsschutzartikel von Hab & Bewahr keine zweiten Robotikproduktseiten.

### KISS und ein kanonischer Master
- **Aktuelle Navigationsvorlage** ist `KATEGORIE/RECHERCHE/PRODUKTE_V2_20261108.json` **Revision 10**, Feld **`navigation_v1`** mit acht Welten. `worlds_v1` (zehn Welten) und alte Dokumente sind **Recherchehistorie**, **keine zweite aktive Navigation**.
- Alle **68** unveränderten Ausgangstypen tragen darin `candidates[].nav_short_v1`: **ein kurzer Navigationsname**, Bezug zur achtteiligen Hauptwelt, und der bisherige volle Produktname als Arbeitstitel/H1-Grundlage.
- **15** zuvor fachlich vertiefte Produkt-/Nischentypen tragen `research_frontier_v1[].niche_content_v3.nav_short_v1` und **49** deutlich gekürzte produktbezogene Inhaltskategorien. Ihre früheren Arbeitstitel sind bei jeder Kategorie unter `working_title_v3` erhalten; die 3–4 individuell geprüften redaktionellen Themenansätze wurden **nicht geändert**.
- Die ursprünglichen **68** Produkttypen besitzen insgesamt **151** kurze Vorschläge für produktbezogene Inhaltskategorien: **15 Pilottypen mit 45**, weitere **53 mit 106**. Die zugrunde liegenden 453 groben Themenansätze verbleiben in den bestehenden Forschungsbelegen. Die neuen `content_nav_short_v1`-Einträge **verweisen** auf diese, statt 453 Themen ein zweites Mal zu speichern.
- **Summe: 200 kurz benannte Kandidaten für spätere WordPress-Inhaltskategorien** (151 ursprüngliche Produktwelt + 49 spätere Nischenpilotwelt). Die Anzahl ist **keine** Festlegung auf genau 200 WordPress-Kategorien; bei weiterer Fach-/SEO-Prüfung können einzelne Kandidaten zusammenfallen oder neue sinnvolle hinzukommen.

## Harte Namensregel für alle Seiten-, Menü- und Inhaltskategorien
1. **1–2 inhaltstragende Wörter** als `display_name`/Nav-Label. Keine ganzen Sätze, keine Fragen und kein Fülltext wie „Alles über“, „Tipps für“, „Wie ...“, „Wissenswertes zu“, „Ratgeber für ...“.
2. Fachlich eindeutige **Komposita** sind sinnvoll: „Schweißroboter“, „Sicherheitssteuerung“, „Kanalsanierung“. Bei einer Abkürzung wie AMR gehört die Erläuterung in den Seitentext/Glossar und gegebenenfalls in die H1/Meta.
3. Der kurze Menütitel darf absichtlich vom **präzisen vollständigen H1-Titel**, Intro, SEO-Title und Meta-Beschreibung abweichen. Beispiele:
   - `Technik → Fertigung → Lichtbogenschweißroboter → Sicherheit`; H1 z. B. „Sicherheit beim Betrieb von Lichtbogenschweißrobotern“.
   - `Landwirtschaft → Gewächshaus → Bestäubungsroboter → Pflanzen`; H1 z. B. „Geeignete Pflanzen und Blüten für Bestäubungsroboter“.
   - `Reinigung → Spezialreinigung → Netzreinigungsroboter → Bedienung`; H1 spezifiziert „Aquakultur-Netzreinigungsroboter“.
   - `Technik → Software → Flottenmanagementsoftware → Schnittstellen` nur dann, wenn Schnittstellen tatsächlich eine eigenständige Inhaltskategorie mit drei tragfähigen Beiträgen sind; andere Kategorien nicht blind kopieren.
4. **Gleiche Kurzbezeichnung bei verschiedenen konkreten Produkten ist zulässig:** „Betrieb“ bei Mährobotern und bei Melkrobotern ist **kein** SEO-Duplikat. Der **Owner, Inhalt und die einzige konkrete Suchfrage** sind entscheidend. Innerhalb ein und desselben Produktastes keine fachlich gleichbedeutenden Geschwister.
5. Die letzte WordPress-*Seite* behandelt immer **eine konkrete Produktart / konkrete Roboterfunktion**, nie bloß „Software“ oder „Reinigung“. Die vertiefenden WordPress-*Kategorien* darunter behandeln nur dieses eine Produkt. Jede Kategorie braucht **mindestens drei realistisch unterschiedliche mögliche Beiträge**, typischerweise 3–5, **keine Obergrenze** für die Anzahl sinnvoller Kategorien pro Produkt. Bei 1–2 Themen bleibt der Inhalt auf der Produktseite oder in einer vorhandenen Kategorie.
6. Eine Magazinerklärung („Was ist SLAM?“) darf nicht dieselbe Geräte-Auswahl-/Kaufberatung wie die Produktseite wiederholen. HivePress gehört zum konkreten Anbieter-/Miet-/Wartungsangebot; Affiliatebanner sind ergänzende Werbung und kein eigener SEO-Produkt-Owner.
7. **Keine Keyword-/SEO-Recherche in diesem Konzeptschritt.** Das spätere spezialisierte Plugin misst Keywords und SERP-Überschneidungen. Hier wurden nur Produktfunktionen, Begriffe, fachliche Eigentümer und grobe Artikeltragfähigkeit betrachtet.
8. **Kein Plugin-Code, keine WordPress-Seiten, keine vorhandenen URLs/IDs ändern.** Der Fachmaster ist ein Entwurf. Eine WordPress-Live-Navigation ist noch nicht bestätigt.

## Feste Qualitätssicherung / Überlappungsfälle
- 68/68 ursprüngliche Typ-IDs haben genau **einen** Welt-Owner im neuen Entwurf; 15 wichtige Nischen haben genau einen vorläufigen Welt-Owner.
- Zwischenseiten heißen kurz, aber entstehen **nur bei echten Unteraufgaben**; keine leeren Hubs.
- **AMR vs FTF vs Palettentransport:** weiterhin fachlicher Grenzfall, kein stilles Mehrfachmodell.
- **Kliniktransport vs Lager-Transport:** medizinisch-funktionaler Unterschied entscheidet, nicht doppelter Kaufbeitrag.
- **Patrouillen-/Rettungsrobotik vs Hab & Bewahr:** Produkttechnik hier, Maßnahmen zum Eigentumsschutz dort.
- **Robotik-Baukasten/Lernroboter vs Hobbydepot:** konkrete Lernrobotertechnik hier, Hobbyaktivität bei Hobbydepot.
- **Robotiksoftware vs Magazin:** konkrete Programmiersoftware erwerben/auswählen hier, technisches Wissen/Normbegriff im Journal.
- **Nischen und Forschungsprojekte:** nur belegte Gerätekandidaten zur CORE-Prüfung, Herstellerankündigung ≠ lieferbares Modell; Dienstleistung ≠ käuflicher Robotertyp.

**Nächster fachlicher Schritt:** 139 Randforschungsfälle weiter ownerweise prüfen, später nur echte Produktfunktionen als finale Produktseiten freigeben; Namen der weiteren neuen Nischen nach derselben Regel. **Keine zusätzliche zentrale Datei und keine WordPress-Änderung.**
