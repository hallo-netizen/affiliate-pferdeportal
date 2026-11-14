# Robotik V50 – 16 Humanoiden-Seiten gegen reale Suchergebnisse und WordPress-Importentwurf geprüft
**Stand 14.11.2026. Fachlich entscheidungsreifer Seitenplan, aber ausdrücklich kein Google-SEO-PASS und keine WordPress-Änderung.**

## 1. Drei gesicherte Sachstände

1. **Aktuelles Konzept:** Acht Hauptkategorien in festgelegter Reihenfolge Haushalt, Garten, Freizeit, Sport, Bildung, Pflege, Humanoide, Gewerbe. Industrie ist der eigenständige, untergeordnete Landingpage-Komplex unter Gewerbe. Humanoide haben sechs nach Nutzung differenzierte Unterbereiche. Kaufbarkeit ist kein Kriterium; Ideen, Projekte, Prototypen und Modelle sind zulässig, mit gekennzeichnetem Entwicklungsstand.
2. **WordPress: echte Inventur vs. Wunschbestand trennen.** Der echte Bestandsexport vom **09.11.2026**, generiert auf `https://robotik.oliver-beil.de/` durch das vorhandene WordPress-Kategorieplugin, listet **2 Seiten** („Beispielseite“, „Datenschutzerklärung“), **1 Beitrag**, **1 Kategorie**. Er enthält keine fachlichen Humanoiden- oder Robotik-Seitentexte. Ein aktueller Abruf der Website sowie `/wp-json/wp/v2/pages` scheiterte extern. Deshalb ist keine aktuelle Live-Text-/Canonical-/Slug-Prüfung möglich.
3. **Original-Entwurf maschinell geprüft:** `ROBOTIK_ERSTIMPORT_WP_SEITEN_ENTWUERFE.xml` enthält genau **104 als `draft` markierte WP-Seiten**, darunter 72 geschützte Robotertypseiten. **Alle 104 `content:encoded`-Haupttexte sind leer**. Es gibt also echte Vergleichstitel und Parent-Beziehungen, aber keine 104 fertigen Texte. Die XML ist keine Bestätigung eines erfolgreichen Live-Imports. Altseiten, IDs, Slugs, Parents, Plugins: 0 geändert.

## 2. Suchtrefferprüfung – was sie belegt und was nicht

- Zu den **16 V49-Suchabsichten** wurden aktuelle öffentlich auffindbare deutschsprachige Web-Suchtreffer und möglichst amtliche Forschungs-/Originalherstellerseiten geprüft. Es wurden **keine monatlichen Keywordvolumina oder Google-Rankings** gemessen und **keine vollständigen deutschen Google-Top-10-Ergebnisse** für jede Phrase mit tatsächlichen WP-URLs verglichen. Trefferseiten sind Indikatoren für unterschiedliche Nutzerbedürfnisse, **kein SEO-Erfolgsgarant**.
- Ein eigener **humanoider** Robotertyp in der Humanoiden-Kategorie konkurriert dann nicht unmittelbar mit einer kontextfremden Seite, wenn Aufbau/Bauform, Modellbeispiele und Hauptfragen tatsächlich getrennt werden. Eine andere Überschrift allein verhindert Kannibalisierung NICHT.
- Fachentscheidung: **12 eigenständige redaktionelle Zielseiten behalten; 4 eigenständige Zukunftsthemen zunächst als sichtbar markierte Kapitel in passende Bereiche aufnehmen**, nicht löschen. Zukunftsthemen werden **nicht wegen fehlender Kaufbarkeit**, sondern wegen aktuell nicht eigenständiger Suchintention bzw. zu großer Inhaltsnähe nicht als separate WP-Endseiten empfohlen.

## 3. Überblick: konkrete Entscheidung zu allen 16 Endseitenthemen

| ID | Humanoide-Unterbereich | Kernfrage/H1 | Redaktionelle Entscheidung |
|---|---|---|---|
| HU01 | Haushalt | Humanoide Roboter für den Haushalt | **Eigene Seite** |
| HU02 | Haushalt | Humanoide Küchenrobotik: Geschirr und Kochen | **Zukunftskapitel** |
| HU03 | Pflege | Humanoide Fernassistenz in der häuslichen Pflege | **Eigene Seite** |
| HU04 | Pflege | Humanoide Begleitroboter in Pflegeeinrichtungen | **Eigene Seite** |
| HU05 | Pflege | Zukunftskonzept: humanoide körperliche Pflegehilfe | **Zukunftskapitel** |
| HU06 | Arbeit | Humanoide Roboter in Lager und Logistik | **Eigene Seite** |
| HU07 | Arbeit | Humanoide Roboter in der Produktion | **Eigene Seite** |
| HU08 | Arbeit | Humanoide Roboter an Empfang und Rezeption | **Eigene Seite** |
| HU09 | Arbeit | Zukunftskonzept: humanoide Restaurantbedienung | **Zukunftskapitel** |
| HU10 | Arbeit | Humanoide Roboter im Handwerk: Forschung und Chancen | **Eigene Seite** |
| HU11 | Bildung | Humanoide Forschungsroboter und Entwicklerplattformen | **Eigene Seite** |
| HU12 | Bildung | Humanoide Lernroboter für Schulen | **Eigene Seite** |
| HU13 | Unterhaltung | Humanoide Roboter für Messe, Show und Event | **Eigene Seite** |
| HU14 | Unterhaltung | Humanoide Gesprächs- und Begleitroboter | **Eigene Seite** |
| HU15 | Intimrobotik | Robotische Intimpuppen: was ist wirklich beweglich? | **Eigene Seite** |
| HU16 | Intimrobotik | Zukunftskonzept: selbstständig bewegliche Partnerroboter | **Zukunftskapitel** |

## 4. Einzelfallabgleich: Suchabsicht, vorhandene WP-Titel und Suchtreffer

### HU01 – Humanoide Roboter für den Haushalt
- **Entscheidung:** EIGENE_FACHSEITE. **Entwurfs-SEO-Titel:** Humanoide Haushaltsassistenten: Modelle, Aufgaben und Grenzen.
- **Eindeutige Informationsaufgabe:** Wohnung, Alltagsaufgaben, tatsächliche Modelle und Fernhilfe.
- **Verglichene vorhandene WP-Entwurfsbezeichnungen / neue Kontextseiten:** Haushalt (WXR-Hub); Haushalt > Aufräumroboter H06 (V46, noch kein Live-WP).
- **Zielgruppen-Einstieg:** Haushalt: Orientierungskarte zu humanoiden Haushaltsassistenten.
- **Besondere Fehlergrenze:** Bestellung/Vorbestellung ist nicht gleich praktisch autonomer Haushaltsbetrieb.
- **Gefundene externe Referenzen:** https://www.mdr.de/wissen/naturwissenschaften-technik/humanoide-roboter-hilfe-im-haushalt-tesla-neo-neura-100.html · https://www.1x.tech/neo.
- **Inhaltstiefe aus V49:** 3 individuelle redaktionelle Rubriken mit jeweils 3 verschiedenen Beitragsthemen; vollständig übernommen, kein WordPress-Beitrag erzeugt.

### HU02 – Humanoide Küchenrobotik: Geschirr und Kochen
- **Entscheidung:** ZUKUNFTSKAPITEL. **Entwurfs-SEO-Titel:** Humanoide Küchenhelfer – Zukunft und Forschungsstand.
- **Eindeutige Informationsaufgabe:** Geschirr einräumen ist demonstriert, eigenständiges autonomes Kochen nicht.
- **Verglichene vorhandene WP-Entwurfsbezeichnungen / neue Kontextseiten:** HU01; Haushalt > Kochroboter H02 (V46).
- **Zielgruppen-Einstieg:** Unter HU01 als eigenständiges Zukunftskapitel, ggf. später eigene Seite.
- **Besondere Fehlergrenze:** Nicht als fertiger Haushaltskochroboter darstellen; im Suchfeld überlappt HU01.
- **Gefundene externe Referenzen:** https://www.figure.ai/news/helix-02 · https://www.mdr.de/wissen/naturwissenschaften-technik/humanoide-roboter-hilfe-im-haushalt-tesla-neo-neura-100.html.
- **Inhaltstiefe aus V49:** 3 individuelle redaktionelle Rubriken mit jeweils 3 verschiedenen Beitragsthemen; vollständig übernommen, kein WordPress-Beitrag erzeugt.

### HU03 – Humanoide Fernassistenz in der häuslichen Pflege
- **Entscheidung:** EIGENE_FACHSEITE. **Entwurfs-SEO-Titel:** Humanoide Fernpflege-Roboter für das eigene Zuhause.
- **Eindeutige Informationsaufgabe:** Pflege im Privathaushalt, Fernsteuerung, Einwilligung und Sicherheit.
- **Verglichene vorhandene WP-Entwurfsbezeichnungen / neue Kontextseiten:** Pflege (WXR-Hub); Schultelepräsenz (WXR-Typ); Pflege > Telepräsenz P01 (V46).
- **Zielgruppen-Einstieg:** Pflege > Unterstützung: Link direkt zur HU03.
- **Besondere Fehlergrenze:** EU-Forschungsprojekt, kein fertiges selbstständig pflegendes System.
- **Gefundene externe Referenzen:** https://geriatrie.charite.de/metas/meldung/artikel/detail/robody_humanoider_teleroboter_fuer_die_pflege · https://cordis.europa.eu/project/id/101329100/de.
- **Inhaltstiefe aus V49:** 3 individuelle redaktionelle Rubriken mit jeweils 3 verschiedenen Beitragsthemen; vollständig übernommen, kein WordPress-Beitrag erzeugt.

### HU04 – Humanoide Begleitroboter in Pflegeeinrichtungen
- **Entscheidung:** EIGENE_FACHSEITE. **Entwurfs-SEO-Titel:** Humanoide Roboter zur Begleitung im Pflegeheim.
- **Eindeutige Informationsaufgabe:** Betreuung, Gespräch/Orientierung statt körperlicher Pflege; Datenschutz Einrichtung.
- **Verglichene vorhandene WP-Entwurfsbezeichnungen / neue Kontextseiten:** Therapieroboter (WXR-Typ); Humanoide > Unterhaltung/Gespräch HU14.
- **Zielgruppen-Einstieg:** Pflege > Betreuung: Link direkt HU04.
- **Besondere Fehlergrenze:** uMe: Interaktion real; kein Beleg autonomer medizinischer Pflege.
- **Gefundene externe Referenzen:** https://www1.wdr.de/nrw/essen/Essen-Messe-Altenpflege-100.html · https://unitedrobotics.group/en/robots/ume.
- **Inhaltstiefe aus V49:** 3 individuelle redaktionelle Rubriken mit jeweils 3 verschiedenen Beitragsthemen; vollständig übernommen, kein WordPress-Beitrag erzeugt.

### HU05 – Zukunftskonzept: humanoide körperliche Pflegehilfe
- **Entscheidung:** ZUKUNFTSKAPITEL. **Entwurfs-SEO-Titel:** Humanoide Hebe- und Umlageroboter – mögliche Zukunft.
- **Eindeutige Informationsaufgabe:** Sichere Patientenübernahme und körperliche Assistenz sind nicht real verifiziert.
- **Verglichene vorhandene WP-Entwurfsbezeichnungen / neue Kontextseiten:** Pflege (WXR-Hub); HU03; Ankleidehilfe/Duschassistenz (V46).
- **Zielgruppen-Einstieg:** Als Zukunftskapitel unter Humanoide > Pflege (HU03/HU04 getrennt).
- **Besondere Fehlergrenze:** Keine Behauptung medizinischer Zulassung/Patientenhebung.
- **Gefundene externe Referenzen:** https://cordis.europa.eu/project/id/101329100/de · https://www.fraunhofer.de/de/forschung/artikel-2026/humanoide-robotik.html.
- **Inhaltstiefe aus V49:** 3 individuelle redaktionelle Rubriken mit jeweils 3 verschiedenen Beitragsthemen; vollständig übernommen, kein WordPress-Beitrag erzeugt.

### HU06 – Humanoide Roboter in Lager und Logistik
- **Entscheidung:** EIGENE_FACHSEITE. **Entwurfs-SEO-Titel:** Humanoide Lagerroboter: Materialtransport und Praxiseinsätze.
- **Eindeutige Informationsaufgabe:** Lagereinsatz Kisten/Totes, Bewegungsabläufe, Betriebsintegration.
- **Verglichene vorhandene WP-Entwurfsbezeichnungen / neue Kontextseiten:** Gewerbe > Lagerlogistik (WXR-Hub); Palettenhubroboter (WXR-Typ).
- **Zielgruppen-Einstieg:** Gewerbe > Industrie > Anlagen/Logistik: Link HU06.
- **Besondere Fehlergrenze:** Pilot/kommerzieller Einsatz in Großlogistik ≠ für kleine Betriebe kaufbares Komplettprodukt.
- **Gefundene externe Referenzen:** https://www.agilityrobotics.com/content/digit-moves-over-100k-totes · https://investors.agilityrobotics.com/news-releases/news-release-details/agility-robotics-highlights-commercial-momentum-and-growing.
- **Inhaltstiefe aus V49:** 3 individuelle redaktionelle Rubriken mit jeweils 3 verschiedenen Beitragsthemen; vollständig übernommen, kein WordPress-Beitrag erzeugt.

### HU07 – Humanoide Roboter in der Produktion
- **Entscheidung:** EIGENE_FACHSEITE. **Entwurfs-SEO-Titel:** Humanoide Produktionsroboter: Erfahrungen aus Fabriktests.
- **Eindeutige Informationsaufgabe:** Wiederholte Greif-/Montageaufgaben und Pilotstatus, getrennt von Lagertransport.
- **Verglichene vorhandene WP-Entwurfsbezeichnungen / neue Kontextseiten:** Gewerbe > Fertigung (WXR-Hub); Schweißroboter (WXR-Typ); Bestückungsroboter (WXR-Typ).
- **Zielgruppen-Einstieg:** Gewerbe > Industrie > Fertigung: Link HU07.
- **Besondere Fehlergrenze:** BMW-Pilot nicht mit frei verfügbarem Fertigungs-Alleskönner gleichsetzen.
- **Gefundene externe Referenzen:** https://www.bmwgroup.com/de/news/allgemein/2026/humanoide-roboter-in-leipzig.html · https://www.press.bmwgroup.com/deutschland/article/detail/T0455860DE/bmw-group-setzt-erstmals-humanoide-roboter-in-der-produktion-in-deutschland-ein.
- **Inhaltstiefe aus V49:** 3 individuelle redaktionelle Rubriken mit jeweils 3 verschiedenen Beitragsthemen; vollständig übernommen, kein WordPress-Beitrag erzeugt.

### HU08 – Humanoide Roboter an Empfang und Rezeption
- **Entscheidung:** EIGENE_FACHSEITE. **Entwurfs-SEO-Titel:** Humanoide Empfangsroboter: Begrüßung und Besucherinformation.
- **Eindeutige Informationsaufgabe:** Humanoide Körperpräsenz, Begrüßung/Interaktion; branchenspezifisches Gewerbe getrennt.
- **Verglichene vorhandene WP-Entwurfsbezeichnungen / neue Kontextseiten:** Empfangsroboter (WXR-Typ); HU13; HU14.
- **Zielgruppen-Einstieg:** Gewerbe > Hotelbetrieb/Empfang: Link HU08 mit eigener Funktionserklärung.
- **Besondere Fehlergrenze:** Kollision mit bestehendem Empfangsroboter: Modelle und Bauform explizit trennen.
- **Gefundene externe Referenzen:** https://roboarca.de/roboter-fuer/service.html · https://www.heise.de/news/Realbotix-humanoide-Roboter-mit-austauschbarem-Design-11128323.html.
- **Inhaltstiefe aus V49:** 3 individuelle redaktionelle Rubriken mit jeweils 3 verschiedenen Beitragsthemen; vollständig übernommen, kein WordPress-Beitrag erzeugt.

### HU09 – Zukunftskonzept: humanoide Restaurantbedienung
- **Entscheidung:** ZUKUNFTSKAPITEL. **Entwurfs-SEO-Titel:** Humanoide Kellner – Roboterbedienung als Zukunftsprojekt.
- **Eindeutige Informationsaufgabe:** Greifende humanoide Tischbedienung anders als rollende Teller-Transportplattform.
- **Verglichene vorhandene WP-Entwurfsbezeichnungen / neue Kontextseiten:** Servierroboter (WXR-Typ); HU08.
- **Zielgruppen-Einstieg:** Unter Humanoide > Arbeit als Konzept-Kapitel; Gewerbe-Gastro bleibt eigene Bedienroboterseite.
- **Besondere Fehlergrenze:** Gefundene Restaurantrobotik zeigt überwiegend rollenden Serviceroboter, keinen autonomen humanoiden Kellner.
- **Gefundene externe Referenzen:** https://www.anivatar.com/de/robot-kelner · https://roboarca.de/roboter-fuer/service.html.
- **Inhaltstiefe aus V49:** 3 individuelle redaktionelle Rubriken mit jeweils 3 verschiedenen Beitragsthemen; vollständig übernommen, kein WordPress-Beitrag erzeugt.

### HU10 – Humanoide Roboter im Handwerk: Forschung und Chancen
- **Entscheidung:** EIGENE_FACHSEITE. **Entwurfs-SEO-Titel:** Humanoide Werkstatthelfer für kleine Betriebe.
- **Eindeutige Informationsaufgabe:** Kleine Werkstätten, Materialtransport, Kosten und Arbeitsschutz statt Großfabrik.
- **Verglichene vorhandene WP-Entwurfsbezeichnungen / neue Kontextseiten:** Gewerbe > Fertigung (WXR-Hub); HU06; HU07.
- **Zielgruppen-Einstieg:** Gewerbe > Handwerk: Link HU10.
- **Besondere Fehlergrenze:** Fraunhofer KMUmanoid belegt Szenarien, nicht Serien-KMU-Gerät.
- **Gefundene externe Referenzen:** https://www.ipa.fraunhofer.de/de/referenzprojekte/kmumanoid.html · https://www.iosb.fraunhofer.de/de/presse/presseinformationen/2026/start-humanoid-robots-experience-lab.html.
- **Inhaltstiefe aus V49:** 3 individuelle redaktionelle Rubriken mit jeweils 3 verschiedenen Beitragsthemen; vollständig übernommen, kein WordPress-Beitrag erzeugt.

### HU11 – Humanoide Forschungsroboter und Entwicklerplattformen
- **Entscheidung:** EIGENE_FACHSEITE. **Entwurfs-SEO-Titel:** Humanoide Entwicklungsroboter: Programmieren und Forschen.
- **Eindeutige Informationsaufgabe:** SDK, ROS, Steuerung und Laborprogrammierung auf körperlichem humanoidem System.
- **Verglichene vorhandene WP-Entwurfsbezeichnungen / neue Kontextseiten:** Lernroboter (WXR-Typ); Tischroboterarme (WXR-Typ); ROS-Lernplattformen B02 (V46).
- **Zielgruppen-Einstieg:** Bildung > Forschung/Programmieren: Link HU11.
- **Besondere Fehlergrenze:** Unitree G1 Basis und EDU-Entwicklerversion nicht verwechseln.
- **Gefundene externe Referenzen:** https://www.unitree.com/g1/ · https://shop.unitree.com/collections/humanoid-robot/products/unitree-g1.
- **Inhaltstiefe aus V49:** 3 individuelle redaktionelle Rubriken mit jeweils 3 verschiedenen Beitragsthemen; vollständig übernommen, kein WordPress-Beitrag erzeugt.

### HU12 – Humanoide Lernroboter für Schulen
- **Entscheidung:** EIGENE_FACHSEITE. **Entwurfs-SEO-Titel:** Humanoide Schulroboter für Unterricht und Lernprojekte.
- **Eindeutige Informationsaufgabe:** Lehrkonzepte, Unterrichtsgruppen, Begleitung vs ROS-Labor.
- **Verglichene vorhandene WP-Entwurfsbezeichnungen / neue Kontextseiten:** Lernroboter (WXR-Typ); HU11.
- **Zielgruppen-Einstieg:** Bildung > Lernroboter: Link HU12.
- **Besondere Fehlergrenze:** Kollision mit bestehender Lernroboterseite: nur menschähnliche Plattformen und deren Didaktik.
- **Gefundene externe Referenzen:** https://unitedrobotics.group/en/robots/ume · https://irisrobotics.eu/de/humanoid-robots-and-educational-kits.
- **Inhaltstiefe aus V49:** 3 individuelle redaktionelle Rubriken mit jeweils 3 verschiedenen Beitragsthemen; vollständig übernommen, kein WordPress-Beitrag erzeugt.

### HU13 – Humanoide Roboter für Messe, Show und Event
- **Entscheidung:** EIGENE_FACHSEITE. **Entwurfs-SEO-Titel:** Humanoide Showroboter: Messen und Veranstaltungen.
- **Eindeutige Informationsaufgabe:** Miete, Operatoren, Publikum, Bühnenshow statt laufendem Empfang.
- **Verglichene vorhandene WP-Entwurfsbezeichnungen / neue Kontextseiten:** Empfangsroboter (WXR-Typ); HU08.
- **Zielgruppen-Einstieg:** Freizeit > Veranstaltungen; Gewerbe > Events: Link HU13.
- **Besondere Fehlergrenze:** Showbetrieb mit Operator nicht als unbeaufsichtigte Kundenbetreuung beschreiben.
- **Gefundene externe Referenzen:** https://wianco.com/humanoide-roboter/ · https://www.roboticrental.de/humanoide-roboter.
- **Inhaltstiefe aus V49:** 3 individuelle redaktionelle Rubriken mit jeweils 3 verschiedenen Beitragsthemen; vollständig übernommen, kein WordPress-Beitrag erzeugt.

### HU14 – Humanoide Gesprächs- und Begleitroboter
- **Entscheidung:** EIGENE_FACHSEITE. **Entwurfs-SEO-Titel:** Menschenähnliche Gesprächsroboter: Dialog und Begleitung.
- **Eindeutige Informationsaufgabe:** Mimik, Sprache, soziale Interaktion statt Wohnungs-Fernpflege oder Rezeption.
- **Verglichene vorhandene WP-Entwurfsbezeichnungen / neue Kontextseiten:** Therapieroboter (WXR-Typ); Haushalt > Begleitroboter H12 (V46); HU04; HU15.
- **Zielgruppen-Einstieg:** Haushalt > Begleitung: Link HU14 (bei tatsächlich humanoiden Modellen).
- **Besondere Fehlergrenze:** Realbotix weist laut heise Sexrobotik-Anwendung zurück; nicht mit HU15 vermengen.
- **Gefundene externe Referenzen:** https://www.heise.de/news/Realbotix-humanoide-Roboter-mit-austauschbarem-Design-11128323.html · https://www.realbotix.com/series-1.
- **Inhaltstiefe aus V49:** 3 individuelle redaktionelle Rubriken mit jeweils 3 verschiedenen Beitragsthemen; vollständig übernommen, kein WordPress-Beitrag erzeugt.

### HU15 – Robotische Intimpuppen: was ist wirklich beweglich?
- **Entscheidung:** EIGENE_FACHSEITE. **Entwurfs-SEO-Titel:** Intimroboter mit beweglichem Kopf: Technik und Grenzen.
- **Eindeutige Informationsaufgabe:** Robotischer Kopf/Teilmechanik, KI-Gespräch, Abgrenzung statische Puppen.
- **Verglichene vorhandene WP-Entwurfsbezeichnungen / neue Kontextseiten:** HU14; HU16.
- **Zielgruppen-Einstieg:** Humanoide > Intimrobotik (kein anderer Hauptbereich nötig).
- **Besondere Fehlergrenze:** RealDoll Harmony: Kopf robotisch, Körper nicht frei gehend; Warteliste ≠ Lieferung.
- **Gefundene externe Referenzen:** https://www.realdoll.com/product/robot-harmony/ · https://alpha-bionic.info/sexroboter-hersteller-modelle/.
- **Inhaltstiefe aus V49:** 3 individuelle redaktionelle Rubriken mit jeweils 3 verschiedenen Beitragsthemen; vollständig übernommen, kein WordPress-Beitrag erzeugt.

### HU16 – Zukunftskonzept: selbstständig bewegliche Partnerroboter
- **Entscheidung:** ZUKUNFTSKAPITEL. **Entwurfs-SEO-Titel:** Vollbewegliche Partnerhumanoide – ein Zukunftsentwurf.
- **Eindeutige Informationsaufgabe:** Vision ganzkörperlich autonomer humanoider Partner im Unterschied zu HU15 Teilrobotik.
- **Verglichene vorhandene WP-Entwurfsbezeichnungen / neue Kontextseiten:** HU15; HU14.
- **Zielgruppen-Einstieg:** Als Zukunftskapitel in Humanoide > Intimrobotik / HU15, nicht als falsches reales Modell.
- **Besondere Fehlergrenze:** Kein nachgewiesener autonomer Ganzkörper-Sexroboter; Realbotix nicht als Sexroboter anführen.
- **Gefundene externe Referenzen:** https://www.realdoll.com/product/robot-harmony/ · https://www.heise.de/news/Realbotix-humanoide-Roboter-mit-austauschbarem-Design-11128323.html.
- **Inhaltstiefe aus V49:** 3 individuelle redaktionelle Rubriken mit jeweils 3 verschiedenen Beitragsthemen; vollständig übernommen, kein WordPress-Beitrag erzeugt.

## 5. Empfehlung zur Navigation – konkret und ohne Automatik

**Humanoide** bleibt als eigener siebter Hauptmenüpunkt, **Gewerbe** achter/letzter. Innerhalb der Humanoiden-Hauptkategorie die sechs beschlossenen Zwischenbereiche: **Haushalt, Pflege, Arbeit, Bildung, Unterhaltung, Intimrobotik**. Keine eigenständige, unnötige 8te oder 9te Zielgruppe.

- **Haushalt:** kurze Infokarte „Humanoide Haushaltsassistenten“ → HU01. HU02 als klar beschriftetes Zukunftskapitel in HU01; die eigenständige Haushalts-Kochroboter-Seite H02 bleibt ausdrücklich ein **nicht-humanoider** Gerätekontext.
- **Pflege:** unter „Humanoide Pflege“ eine **informative 2-Angebote-Übersicht** (HU03 häusliche Fernpflege und HU04 soziale Pflegeheimbegleitung) oder zwei direkte Links. Das ist nur eine Navigationsempfehlung, noch keine SEO-/WP-Freigabe für eine neue Pflege-Landingpage. HU05 als Konzeptkapitel unter Humanoide > Pflege. Nicht automatisch vom Wort „Pflege“ auf den Humanoiden-Hauptindex weiterleiten.
- **Gewerbe:** Empfang > HU08; Handwerk/Kleinbetriebe > HU10; Veranstaltungen > HU13. **Industrie bleibt getrennt:** Gewerbe > Industrie > Anlagen/Logistik → HU06; Gewerbe > Industrie > Fertigung → HU07. HU09 Zukunftsidee Restaurantkellner bleibt im humanoiden Arbeitsbereich; vorhandener Gastronomie-Servierroboter erklärt echte rollende Servierrobotik weiterhin getrennt.
- **Bildung:** Schulunterricht → HU12, Hochschulforschung/Programmierplattform → HU11. Die generische Lernroboterseite in Bildung behält ihre eigenen Leserfragen.
- **Unterhaltung/Intimrobotik:** HU13 (Shows), HU14 (menschliches Gespräch) und HU15 (robotischer Intimkopf) nach Einsatzzweck trennen. **Realbotix ist laut heise explizit kein Sexrobotik-Anbieter**; RealDoll Harmony ist nur teilweise robotisch. Vollbeweglicher Intimhumanoid HU16 als **deutlich bezeichnete Zukunftsvision** auf HU15 statt falschem Serienmodell.

**Technik:** **Jetzt kein Redirect und keine künstliche neue Pflege-/Gewerbe-Pflichtseite.** Im später freigegebenen WP-Plan kurze reguläre Linkkarten zu konkret passenden Humanoiden-Unterseiten; eine informative Landingpage nur, wenn sie Leserfragen selbst beantwortet und nicht als leere Türöffnerseite fungiert. WP-Parents/Slugs/Redirects/Canonical erst nach echtem aktuellen WP-Export und SEO-Abnahme festlegen.

## 6. Geschützter Arbeitsstand und Abnahmegrenzen

- **V49-Themenbestand 16/16 vollständig erhalten:** 12 eigene redaktionelle Seiten plus 4 als Kapitel eingebundene Zukunftsthemen; 6 Humanoiden-Zwischenbereiche.
- **V46 16 bestehende HOLD-Seiten außerhalb der Humanoiden-Welt bleiben separat gesperrt**. Diese Arbeit schaltet sie nicht frei. Auch keine der 12 Humanoiden-Seiten erhält automatisch eine SEO-/WordPress-Freigabe.
- **104 ursprüngliche importierbare WP-Entwurfsseiten sind unangetastet.** Bisher 72 WP-Produktseiten im geplanten XML; zwei im echten Inventurstand vom 09.11., aber kein aktueller Live-WP-Beleg. Das Gesamtprojekt hat folglich noch keine bewiesene aktuelle veröffentlichte Robotik-Seitenlandschaft.
- **Nächste objektiv notwendige Messung vor Live-Umsetzung:** frischer vorhandener Kategorie-Workflow-Export aus WordPress mit echten aktuellen Titeln/Slugs/Eltern/Status; sofern redaktionelle Texte in WP entstanden sind, diese Inhalte ebenfalls lesen; echte deutsche Google-Suchergebnispaare/Volumina und 12 Endseiten-Keywords prüfen. Erst danach Seiten, Slugs, Weiterleitungen, Canonical freigeben. Ohne Zugriff kein erfundener SEO-PASS.

## 7. Quellenübersicht für Aktualitätskontrolle

- Hersteller 1X: https://www.1x.tech/neo
- Figure Helix 02 Demo: https://www.figure.ai/news/helix-02
- EU CORDIS Robody: https://cordis.europa.eu/project/id/101329100/de
- United Robotics uMe: https://unitedrobotics.group/en/robots/ume
- Agility GXO Digit 2026: https://www.agilityrobotics.com/content/gxo-and-agility-robotics-expand-partnership-to-accelerate-deployment-of-humanoids-in-u-s-operations
- BMW Leipzig: https://www.bmwgroup.com/de/news/allgemein/2026/humanoide-roboter-in-leipzig.html
- Fraunhofer KMUmanoid: https://www.ipa.fraunhofer.de/de/referenzprojekte/kmumanoid.html
- Unitree G1: https://www.unitree.com/g1/
- Realdoll Harmony, Kopfroboter: https://www.realdoll.com/product/robot-harmony/
- heise Realbotix mit expliziter Ablehnung von Sexrobotik-Anwendungen: https://www.heise.de/news/Realbotix-humanoide-Roboter-mit-austauschbarem-Design-11128323.html
- Google hilfreiche Inhalte: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google Canonical: https://developers.google.com/search/docs/crawling-indexing/canonicalization