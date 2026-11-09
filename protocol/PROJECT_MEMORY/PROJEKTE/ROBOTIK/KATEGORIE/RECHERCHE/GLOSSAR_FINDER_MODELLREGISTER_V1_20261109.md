# ROBOTIK – Glossar, Finder und Modellregister: geprüfte Vorbilder und Konzept
Stand 09.11.2026 · ENTWURF. Kein Plugin, keine neuen WP-URLs, keine Datenbank.

## Originale Campus-Konzepte geprüft
- `PROJEKTE/PFERDE_ATELIER/WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/GLOSSAR_STRUKTUR.md`: ein Begriff/eine ID; Synonyme beim Hauptbegriff; eigene Begriffseite nur bei eigenständigem Definitions-Intent; starke CORE-Seite als Hauptziel; 150–200 individuelle Wörter, Quellen, Prüfdatum, keine Text-Duplikate.
- `PROJEKTE/EIGENTUMSSCHUTZ/WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/GLOSSAR_STRUKTUR.md`: dieselbe Glossarlogik mit eigenen Themenwelten; Glossar nie Ersatz für Kategorie/Ratgeber; 6/12/24-Monatsprüfung.
- `PROJEKTE/HOBBYRAUSCH/GLOSSAR/KONZEPT_GLOSSAR.md` und `GLOSSAR/CURRENT_STATE.md`: eine A–Z-Suche, Weltfilter/Pagination als **Ansichten**, keine zweite Kategorie-Taxonomie, Meta/Verwandte Begriffe/Quellen.
- `PROJEKTE/PFERDE_ATELIER/WISSENSDATENBANK/AKTENSCHRAENKE/PFERDERASSEN/START_HERE.md` und `BEITRAGSART_PFERDERASSE_ENTWURF.md`: standardisierte, individuelle quellengebundene Einzelprofile; gleiche Abschnittsform, jedes Profil eigenständige Fakten und Unterschiede.
- `PROJEKTE/HOBBYRAUSCH/WISSENSDATENBANK/HOBBYREGISTER.md`, `HOBBYREGISTER_SCHEMA_F_V1.md`: EIN Register mit stabilen Identitäten, Eigenschaften nur einmal pflegen, lesende Filter/Ansichten; unbekannte Werte nicht erraten; bei identischem Hobby-Intent Vorrang der CORE-Seite.
- `PROJEKTE/HOBBYRAUSCH/KONZEPT/VORARBEITEN_HOBBYFINDER/KONZEPT_MASTER.md` und `KATEGORIEPLUGIN_HANDOFF.md`: Bedürfnisse und konkrete Interessen sind zwei Einstiege in DENSELBEN zentralen Bestand, keine zweiten Welt-Kategorien.

## Externe fachliche Grundlage
- IFR (ISO 8373:2021): Roboter, industrieller Roboter, Serviceroboter und medizinischer Roboter sind **unterschiedlich definiert**. https://ifr.org/industrial-robots ; https://ifr.org/service-robots
- IFR Klassifikation beruflicher und privater Serviceroboter nach **Anwendung**, nicht nur Bauart. https://ifr.org/wr-service-robots
- Robotik-Technikbegriffe werden international normiert (ISO 8373:2021); wir formulieren sie **selbst neu** und kopieren keinen geschützten Normtext. https://www.iso.org/standard/75539.html
- Praktische Produktfinder verwenden je Aufgabe/Typ konkrete technische Merkmale, etwa **Traglast und Reichweite**; für andere Robotikarten sind diese Merkmale NICHT sinnvoll. Beispiel: https://roboticsinmfg.com/tools/payload-reach
- Öffentliche Roboterkataloge zeigen, dass Produktmodelle sinnvoll vergleichbar sind, wenn Quelle und Datenstand je Merkmal belegt werden; leere/ungesicherte Angaben müssen offen bleiben. Beispiele https://droid.monster/ und https://robotobservatory.com/robots (keine Quellenautorität für einzelne Fakten, Primärquellen bleiben maßgeblich).

## Empfehlung A: Roboter-Glossar – JA
**Standort:** redaktioneller Bereich `Magazin → Wissen & Glossar`, jedoch EINE zentrale A–Z-Hauptseite. Keine neue CORE-Hauptwelt.

**Abgeleitete Oberfläche:** Buchstabensuche, Filter nach denselben recherchierten Robotik-Einsatzwelten, Karten mit Kurzdefinition, Detailansicht nur für echte Definitionsintents, verwandte Begriffe und genau ein sinnvoller Link zur vorhandenen CORE-Produktseite oder geeigneten Magazin-Erklärung. Filter-/Such-URLs nicht als neue indexierbare Seiten erzeugen.

**Erster Begriffspool für fachliche Prüfung**, NICHT 30 sofortige WordPress-Seiten:
- Robotiktypen und Steuerung: Industrieroboter, Serviceroboter, medizinischer Roboter, Autonomiegrad, Teleoperation, Cobot, sechsachsiger Knickarm, SCARA, Delta-Roboter, mobiler Manipulator.
- Mobilität und Navigation: AMR, AGV/FTF, SLAM, LiDAR, RTK-GNSS, Hinderniserkennung, Flottenmanagement, Dockingstation, Lokalisierung, Navigation.
- Technik und Betrieb: Aktor, Endeffektor/Greifer, Freiheitsgrade, Traglast, Reichweite, Wiederholgenauigkeit, Bildverarbeitung/Machine Vision, Sicherheitsbereich, Teach-Pendant/Programmierhandgerät, ROS 2, digitaler Zwilling.
- Wirtschaft: Robot-as-a-Service (RaaS), Inbetriebnahme, Systemintegration – nur dann eigene Glossarseite, wenn die *Begriffserklärung* selbst den Suchintent besitzt.
- **Produktnamen als Abkürzungen/Begriffe:** falls Hauptintent bereits bei einer konkreten CORE-Produktseite liegt, Glossar nur als verknüpfte Kurzdefinition bzw. Alias, KEINE zweite konkurrierende Langseite.

**Daten, ausschließlich einmal gepflegt:** stabile Term-ID, Wort, Synonyme, verständliche Kurzdefinition, eigenständige Facherklärung (falls sinnvoll), Abgrenzung, Quelle, Review-Datum, primärer CORE-/Magazin-Owner, Verwandtschaft. Keine separaten Forschungslisten je Filter.

## Empfehlung B: Roboterfinder – JA, hoher unmittelbarer Nutzen
**Zweck:** Besuchern helfen, die ihren Robotertyp noch gar nicht kennen: "Welche Aufgabe möchte ich automatisieren?" Der Finder verweist auf bereits bestehende **kanonische** CORE-Produktseiten, nicht auf eigene Finder-Produkttexte.

**Einfacher Klickweg, maximal 4 bis 5 kurze Eingaben:**
1. **Was soll der Roboter erledigen?** transportieren / reinigen / servieren / bauen / prüfen / fertigen / pflegen / Haushalt / lernen ... (nur reale, belegte Aufgaben).
2. **Wo?** Wohnung/Garten / Betrieb/Lager / Gastronomie/Hotel / Landwirtschaft / Bau/Anlage / Klinik/Labor / draußen/innen.
3. **Worum geht es konkret?** z. B. Bodenfläche, Transportgut, Tiere, Bauteile; **dynamisch** nur für diese Aufgabe relevante Angaben anbieten.
4. **Welche wichtigen Bedingungen?** nur zutreffend: Last/Tragfähigkeit, Reichweite, Hindernisse, Platz, Außenwetter, öffentliche Umgebung, Hygiene, Datenschutz, Integration, Personal.
5. **Falls gewünscht:** Kauf/Miete/Dienstleistung – führt zusätzlich in bestehende passende HivePress-Servicekategorie, kein Produktduplikat.

**Ausgabe:** 1–5 passende **Roboterfunktionen/-typen** mit kurzem "Warum?" und echten Links zu den CORE-Produktseiten; nur geprüfte Merkmale benutzen, **UNKNOWN** bedeutet "noch nicht belastbar auswählbar" und keine vorgetäuschte Empfehlung. Wenn kein passender Owner existiert, "noch nicht abgedeckt" und als neuer Recherchekandidat melden. Keine frei erfundenen Wirkungsgrade oder Preisangaben.

**Datenbasis:** DIESELBEN `rb...`-IDs des kanonischen Master `KATEGORIE/RECHERCHE/PRODUKTE_V2_20261108.json`. Für jeden freigegebenen Produkttyp werden höchstens die für Finder nötigen Merkmale ergänzt. Es entsteht **keine** zweite Kategorienliste, kein eigenes Pflege-Excel, keine neuen SEO-Landingpages durch Filterkombinationen.

**Stand:** Noch kein Finder-Plugin erstellen. Erst Produktfunktionen/Abgrenzungen und drei Piloten prüfen. Finder später als Ansicht über den beschlossenen Master/WordPress-Owner bauen; zur Reduktion von Doppelplugins möglichst im bestehenden Design-/Frontend-System, ohne eigenen Inhalts-Writer.

## Empfehlung C: Register – JA, ABER konkrete RoboterMODELLE statt zweite Robotertypen-Hauptseiten
**Was hier sinnvoll anders als Pferderassen ist:** Pferderassen sind selbstständige, beständige fachliche Identitäten. Bei Robotik sind "AMR", "Servierroboter" oder "Melkroboter" bereits unsere CORE-Produktseiten. Ein zweites `Robotertypenregister` mit je eigener Ratgeberseite würde diese **kannibalisieren**. Ein Register konkreter **Hersteller-Modelle** ergänzt die Produktseiten dagegen sinnvoll.

**Vorschlag für spätere Modellsteckbriefe:**
- Hersteller + Modell + genaue Variante (eine eindeutige Modell-ID, nicht automatisch jedes Update eigene Seite);
- **Bezug auf genau einen primären konkreten `rb...`-Roboterfunktion-Owner**; Mehrzwecke nur als Relationen;
- belegt: reale Aufgabe, Marktstatus/Produktbeleg, Bauart/Arbeitsumgebung, je Robotertyp geeignete technische Werte (z. B. Traglast, Reichweite, Laufzeit, Schutzart, nutzbare Fläche);
- **nicht einheitlich fordern:** ein Melkroboter hat andere relevante technische Angaben als ein Schweißroboter;
- Primärquelle/Herstellerdatenblatt, Stand/Datum je Angabe, **UNKNOWN** statt erfundener Preis/Leistung/Verfügbarkeit;
- Vor- und Nachteile **nur** bei belegten, wirklich vergleichbaren Eigenschaften; keine ungeprüften "besten Roboter"-Rankings.
- Registeransicht mit Suche, Hersteller-/Anwendungsfilter und kurzen Karten. Nur echte Informations-URLs mit eigenem Modell-Intent indexieren; andernfalls Modellsteckbrief in der Registeransicht oder als noindex-Nutzerprofil.
- Externe Angebote (Verkäufer, Leasing, Installateure) gehören ins **HivePress-Anbieterverzeichnis**, nicht in den wissenschaftlichen/technischen Modellsteckbrief.

**Vor Produktivaufbau:** zunächst etwa 10–15 **herstellerbelegte Pilotmodelle** mit je wenigstens 1–2 belastbaren Herstellerdatenblättern; Aufwand, laufende Datenpflege und tatsächliche Nutzer-/Suchintention prüfen. Kein Copy/Paste von 1000 Modellen aus Drittverzeichnissen, keine ungeprüfte Preis-Datenbank.

**Zentrale Datenregel:** Modell-Datensätze (falls später freigegeben) referenzieren vorhandene Robotik-Produkt-IDs; sie dürfen weder einen zweiten Roboterarten-Master noch SEO-Produktseiten-Kopien schaffen.

## Ranking / Umsetzung für minimierten Aufwand
1. **Jetzt planen, aber noch nicht installieren:** Glossar-Fachvertrag plus Pool; Finder-Filterfelder als Erweiterung des EINEN Produktmasters; Modellregister-Nutzwertcheck.
2. **Zuerst konzeptionelle Produkt-Fachprüfung** der 68+20 Kandidaten und 3+ Pilot-Informationsabsichten; dabei Glossarwörter und Finder-Traits als Nebenergebnis ableiten.
3. **Dann Glossar** als bestehenden, bewährten Portalbaustein übernehmen (mit neutralem Robotik-Profil und passendem Design); bis zur fachlichen Prüfung keine öffentlichen Termseiten.
4. **Dann einfacher Finder**: auf dieselben Produktseiten verweisen, ohne eigene Datenführung.
5. **Danach Modellregister** als separater lesender Blick auf reale Robotermodelle, falls die 10–15 Pilotkarten echte Qualität/Nutzen belegen.
6. **Nur EIN Hauptmaster, EINE Fachquelle, EINE Pluginidentität pro echter Funktion.** Kein automatischer Live-Import aus unbewerteten Robotiklisten. Werbung/HivePress bleiben separate, klar abgegrenzte Angebotswege.

## Drei-Säulen-Owner / SEO-Schutz
- CORE: konkrete Robotertypen, Auswahl, Nutzung, produktbezogene Fragen.
- JOURNAL: Glossar-Definitionen, übergreifende Technologie/Branchenfragen, Forschung, Sicherheit, Arbeitswelt.
- HIVEPRESS: Anbieter, Leistungen, Inserate, Miete, Wartung, Schulung.
- Finder ist **nur Navigation/Filter**, keine vierte redaktionelle Säule.
- Modellregister ist **eine strukturierte, verknüpfte Produktdatenansicht** (optional für echte Modellintents); nicht CORE duplizieren.
- Begriffe und Modelle werden mit bestehenden Owner-IDs abgeglichen. Erst wenn echte Inhalte/URL-Liste da sind, über tatsächliche Indexierung entscheiden; bis dahin keine pauschale SEO-Freigabe.

## Entscheidungsvorschlag
**Glossar: JA. Finder: JA. Modellregister: bedingt JA, nach 10–15-Modell-Pilot. Zweites Robotertypen-Register mit eigenen umfassenden Seiten: NEIN.**

**Ist-Stand:** Untersuchung und Konzept, keine Plugins, kein WordPress-Import, keine Glossar-/Finder-/Register-Livefunktionen. Zeitaufwendige Einzeldatei-Uploads werden ausdrücklich vermieden.

## Ergänzung 09.11.2026 – Finderergebnisse mit späteren Affiliate-Produkten
**Nutzerwunsch und Reihenfolge verbindlich dokumentiert:**
1. Finder filtert nach Nutzeraufgabe und tatsächlich recherchierten `finder_traits_v1`-Eigenschaften des **einen `rb...`-Robotertyp-Masters**. Nicht ausreichend belegte Eigenschaften werden **NICHT_RECHERCHIERT** angezeigt und dürfen den Treffer nicht falsch auf-/abwerten.
2. Auf Ergebnisseite zunächst passende Robotertypen mit Begründung und Link zur **einzigen** CORE-Produktseite.
3. **Später zusätzlich** konkrete Affiliate-Produkte/Angebote für den bereits fachlich passenden Robotertyp über das zentrale Affiliate-Plugin (nur wenn echte passende und aktuelle Partnerdaten vorliegen). Produktempfehlung zuerst, mögliche Provision niemals das Auswahlkriterium. Werbeangebote klar **„Anzeige“** kennzeichnen. Keine erfundenen Preise, kein fiktives Lager/Verfügbarkeitsversprechen.
4. Nach Bedarfswunsch zusätzlich Link zu **konkreten HivePress-Listings**, wenn ein Dienstleister/Mietangebot statt eines eigenen Gerätes benötigt wird. Ein Inserat ist **nicht dasselbe** wie ein Affiliate-Banner oder eine Produkt-Knowledge-Seite.
5. Kein zweites Produktdatenregister, kein eigenständiger Anzeigen-Writer, keine unbelegten Affiliate-API-Schnittstellen behaupten. Derzeit **Konzept für später, keine installierte Finder-/Affiliate-Funktion**.

**Gleiches Datenmodell wie Hobbyregister:** `../WISSENSDATENBANK/ROBOTERREGISTER/EIGENSCHAFTEN_SCHEMA_V1.md` (relativ zum ROBOTIK-Gebäude), konkret: `PROJEKTE/ROBOTIK/WISSENSDATENBANK/ROBOTERREGISTER/`. Stand 09.11.2026: 68/68 **Schema-Skelette**, aber noch **keine** 68 fachlich befüllten/abgenommenen Eigenschaftsprofile.
