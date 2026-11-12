# Robotik – Recherche V40: konkrete Entwicklungsfunktionen und Dublettenabgleich
**12.11.2026 | Fortsetzung V39 | Forschungsbericht, kein WordPress-Import**

## Zielvorgabe
Informationsportal, **kein Onlineshop**: Kaufbarkeit ist **kein Kriterium zur Ablehnung** einer relevanten Robotertyp-Informationsseite. Realer Entwicklungsstand offen darstellen: Konzept, Teilaufbau, Laborprototyp, Feldtest, Vorbestellung, regionaler oder verfügbarer Verkauf. **Keine erfundenen Fähigkeiten/Marktreifen.** Pro produktbezogenem Seitenende genau EINE funktional unterscheidbare Roboteraufgabe; darunter sinnvolle und je mit **mindestens drei tatsächlich verschiedenen Artikelansätzen** unterlegte Fachkategorien. Keine erzwungenen Standardkategorien. Magazin/Glossar/Register/Finder/Anzeigen jeweils gemeinsam, sauber abgegrenzt.

## Verbindlich gesicherter Arbeitsstand
Einzige führende Forschungsdatei in der Library:
`/robotik/Recherchebüro/CURRENT.json` **V40 – 573 Fundnennungen**.
**Bestandskontrolle programmatisch PASS:** Vorher **561** Fundnennungen/561 IDs, danach **573** / 573 eindeutige IDs; **alle 561 ursprünglichen Records mit ALLEN Originalfeldern und -werten erhalten**. Hinzu kamen **12 neue Forschungs-IDs ROB-0562 bis ROB-0573**. Bei weiteren **23 alten Forschungs-IDs** wurde ausschließlich das Zusatzfeld `v40_followup` angehängt; keine alten Aussagen gelöscht. **573 Funde sind NICHT 573 WP-Produktseiten**. Der schon früher gegen das Originalplugin geprüfte Import umfasst **72 Produktseiten** in 7 Hauptkategorien; an WP, Slugs, Eltern, Plugins und gekauften Keywordkontingenten wurde **nichts** geändert.

## Zwölf neue Quellenfunde mit ehrlichem Status
| ID | Vorläufige Zuordnung | Roboterfunktion | Verifizierte Primärquelle / Reifegrad | Abgrenzung / Risiko |
| --- | --- | --- | --- | --- |
| ROB-0562 | Haushalt | Geschirrspüler-Einräumroboter | 2026 Roboterforschung mit physischer Geschirrhandhabung: https://www.max-robotics.com/en/research/publications/cmu42tbzo01ajpd42mhutzdf3 | Spezialisierte Aufgabe statt allgemeiner ROB-0075-Heimassistenz; KEIN lieferbares Gerät |
| ROB-0563 | Haushalt | Fahrender Wertstoff-Behälterroboter | UC Irvine SmartCan 2025/26 funktionsfähiger *fahrender* Prototyp https://projects.eng.uci.edu/projects/2025-2026/smartcan | **Wichtige Korrektur:** fährt erkannte Gegenstände an; fertiges Aufheben/Sortieren durch Robotergreifer nicht belegt; nicht ROB-0096 Mülltonnentransport |
| ROB-0564 | Haushalt | Treppenstufen-Reinigungsroboter | Universitätsprojekt zu Stufentritt, Setzstufe, Nase https://www.robo.lab.uec.ac.jp/en/project/stairs-cleaning/ | ROB-0365/0499 treppensteigende Staubsauger sind bekannt; neu nur bei tatsächlich anderem Arbeitsumfang |
| ROB-0565 | Pflege | Robotische Bade-/Waschhilfe | Facharbeit 2026, kombinierte Robotik-Badehilfe mit Pilotversuchen https://www.mdpi.com/2075-1702/14/4/431 | Nicht mit Haarwaschroboter ROB-0408, Ankleidehilfe ROB-0077, Toilettenassistenz ROB-0448 verdoppeln |
| ROB-0566 | Bildung | Handschrift-Lernhilfe mit körperlicher Führung | IEEE Robotics and Automation Letters 2026; TeachingBot Forschung mit 30 Testpersonen https://scholars.ln.edu.hk/en/publications/teachingbot-robot-teacher-for-human-handwriting/ | Pädagogische Handführung ≠ Zeichenplotter ROB-0065; generischen Lernroboter ROB-0059 schneiden |
| ROB-0567 | Bildung | Experimentierroboter für naturwissenschaftliche Bildung | NIST LEGOLAS Kit, im Hochschulunterricht eingesetzt; 2026 aktualisierte NIST-Seite https://www.nist.gov/programs-projects/low-cost-robot-science-kit-education | Reale Experimentierfunktion ≠ nur Programmierbausatz, aber ROB-0553 Robotikbausätze und ROB-0380 Chemielabor-Experimentierroboter überschneiden sich |
| ROB-0568 | Sport | Reaktiver Kampfsport-Übungsroboter | Peer-reviewed Sporttechnik-Prototyp 2026 https://www.mdpi.com/2076-0825/15/10/502 | Lern-/Trainingsgerät im geregelten Sport, keinerlei Anleitung zu Angriffen oder Verletzungen; kein Serienkauf |
| ROB-0569 | Sport | Eigenständig spielender Billardroboter | Hochschule Bielefeld Mai 2026 physisch gebauter Billard-Spieltisch https://www.hsbi.de/presse/pressemitteilungen/studierende-der-hsbi-entwickeln-vollautomatisierten-billardtisch-am-campus-guetersloh | Nicht Schachroboter und keine bloße Videospiel-KI; Forschungsdemonstrator, kein Händlerangebot |
| ROB-0570 | Pflege | Haarpflege-/Kämmroboter mit sanfter Roboterhand | IEEE HRI 2025 Forschung zu Kämmen/Haarhandhabung https://ieeexplore.ieee.org/abstract/document/10973945 | Andere Aufgaben als ROB-0408 Haarwäsche, aber ggf. ein gemeinsamer Haarpflege-Owner |
| ROB-0571 | Garten | Schwimmender Teich-Algen-/Oberflächenpflege-Roboter | AURABot Konzept: https://bir-ashy.vercel.app/hardware/aurabot | **Teilaufbau, keine bestätigte selbstständige Einsatzfähigkeit:** Elektronik/Antrieb/Sammelbehälter laut Projekt noch nicht fertig; kein fertiger Roboter; Abgrenzung zu ROB-0164 Poolroboter und ROB-0046 Oberflächenmüllsammler |
| ROB-0572 | Freizeit | Lernender Robotik-Pianist | Royal Society Journal 2026: Roboterhand spielt kurze nach Gehör erkannte Melodien auf physischer Tastatur https://doi.org/10.1098/rsif.2025.0909 | Bestehender Forschungsbestand ROB-0180 Geige, ROB-0410 Schlagzeug; kann auch zu EINER Musikerroboter-Familie gehören |
| ROB-0573 | Bildung | Sozialer Leselern-/Sprachroboter | KIT-Projekt zu Roboterunterstützung beim Lesen 2026/27 https://sarai.iar.kit.edu/289.php | Unterrichtsfunktion unterscheidbar, aber **möglicherweise gleiche Sozial-/Lernroboterplattform** wie ROB-0059, keine künstliche weitere WP-Seite |

**Kontrolle der Originale / keine Neufunde wegen neuem Modell:** Nachrecherchiert wurden 23 bestehende IDs, darunter ROB-0175 (Weave bestätigt eingeschränkte California-Auslieferung, 2026: https://www.weaverobotics.com/isaac-0), ROB-0497 (Terrassenreinigungsroboter längst im Register: https://trac.technology/orbit), ROB-0475 (Dachrinnen-Robotik bereits im Register, Patent keine Produktreife: https://patents.justia.com/patent/20260250957), ROB-0537 (EU-TrimBot-Heckenschneideforschung, bereits erfasst: https://cordis.europa.eu/project/id/688007/de), ROB-0066 (autonomer Tischtennis-Spielgegner in Nature 2026: https://www.nature.com/articles/s41586-026-10338-5), ROB-0005 (Pflanzenbestäubung), ROB-0408 (Haarwäsche), ROB-0553 (Bausätze), ROB-0554 (mobile Lernplattform), ROB-0089 (Aquarienglas), ROB-0559 (Wohnungs-Aufräumen), ROB-0075 (allgemeine Heimassistenz), ROB-0560 (Kochassistenz), ROB-0561 (Torwartroboter). **Diese bestehenden Funktionen wurden NICHT als neue IDs zweitangelegt.**

## Forschungs-/Bilanzkontrolle: Wo sind die zwölf zusätzlichen Funde?
- **Haushalt: 3** Forschungsfunde (Geschirr, Wertstoffbehälter, Treppenstufen).
- **Bildung: 3** (Handschrift, experimentelle Naturwissenschaft, Lesebegleitung).
- **Sport: 2** (reaktive Trainingsgeräte, Billard).
- **Pflege: 2** (Baden, Haarpflege).
- **Garten: 1** (Teich-Algenkonzept).
- **Freizeit: 1** (Robotiker an Tastatur).
- **Gewerbe: 0 neue Forschungs-IDs** in dieser gezielt auf unterbesetzte Gruppen ausgerichteten Runde.

Diese Liste enthält bewusst auch **offene Owner-/Funktionsgrenzen**; daher: **NICHT zwölf zusätzliche freigegebene Produkttypen**, **NICHT zehn neue sichere WP-Seiten**. Die vorige Bestandszählung (72) bleibt 3/7/9/8/3/8/34 für Haushalt/Garten/Freizeit/Sport/Bildung/Pflege/Gewerbe. Die kaufnahe V38-Hypothese (78) und die zwölf V40-Funde sind nicht zusammenzuzählen, bevor die insgesamt bestehenden 573 Forschungsnennungen jeweils nach **Funktions-Owner** und thematischer WP-Tiefe abgegrenzt sind.

## Konkreter Inhaltstiefentest – Forschung und Konzepte dürfen echte Kategorien haben
**Roboter zum Spülmaschinen-Einräumen (Forschung):**
- **Geschirrarten:** Gläser und Teller, unterschiedliche Formen, Besteck-Greifen.
- **Handhabung:** Schmutz/Feuchtigkeit, Greifkräfte, bewegliche Körbe.
- **Entwicklung:** Laborversuche, Grenzen in fremden Küchen, Integrationsfragen.
Alle neun Stichworte sind **unterschiedliche grobe Fachansätze**, keine geschriebenen Beiträge oder belegten Nutzerzahlen. Die Rubriken werden nicht pauschal auf andere Roboter geklont.

**Treppenstufen-Reiniger (Prototyp):**
- **Treppenarten:** glatte Stufen, Stufenkanten, Setzstufen.
- **Fortbewegung:** Absturzerkennung, unterschiedliche Stufenhöhen, Hindernisse.
- **Entwicklung:** Testumgebung, Zuverlässigkeitsgrenzen, Trennung zum Treppensauger.

**Badehilferoboter (Prototyp):**
- **Unterstützung:** Rückenpflege, Arme/Beine, Transfer zur Badeeinrichtung.
- **Sicherheit:** nasse Umgebung, Kräfte am Körper, manuelle Eingriffe.
- **Forschung:** Laboraufbau, Testumfang, fehlende Alltags-/Klinikfreigabe.

**Handschrift-Lehrroboter (Prototyp):**
- **Lernaufgaben:** Buchstaben nachfahren, Handschriftstile, individuelle Bewegung.
- **Technik:** haptische Hilfen, Feedback und Messung, variable Unterstützung.
- **Einsatz:** Unterrichtsgruppen, Lernfortschrittsmessung, Altersgruppen.

**Billardroboter (Prototyp):**
- **Spiele:** Aufstellung und Regeln, Spiel gegen Menschen, Übungsbetrieb.
- **Technik:** optische Spielerkennung, Rechenstrategie, Bewegungsmechanik.
- **Entwicklung:** HSBI-Projekt, Transport bei Demonstration, Grenzen und nächste Forschungsziele.

**Wichtige methodische Anmerkung:** Diese Rubrikthemen zeigen nur sachlich plausibles Informationspotenzial. **Die Veröffentlichung und die endgültigen WP-Inhaltskategorien bleiben der späteren Prüfung vorbehalten.**

## Ergebnis für die Neuordnung der sieben Hauptwelten
1. **Recherche V40 erzielt echte thematische Vertiefung insbesondere in Haushalt/Bildung/Pflege/Sport**, ohne unzulässig behauptete Serienprodukte. Entwickler- und Forschungsprojekte machen zuvor ausgeschlossene Felder sichtbar.
2. **Anzahl und fachlich passende Seiten sind noch nicht deckungsgleich.** Der belastbare 72er Bestand ist nicht still geändert. Die 7er Neuordnungsvariante aus V38 („Haus & Garten“, „Freizeit & Lernen“, „Sport“, „Pflege“, „Landwirtschaft“, „Service & Handel“, „Handwerk & Industrie“) ist bei den **72 geschützten Alt-Typen** 10/12/8/8/9/13/12 und weiterhin rechnerisch ausgeglichen. **Ob man sie braucht**, ist erst nach gezielter Eigenfunktions- und Vertiefungsbewertung der zusätzlich recherchierten Zukunftsthemen entscheidbar.
3. Kein neues Hauptmenü anlegen, keine neuen WordPress-Seiten oder Eltern-IDs schreiben; fachliche Vorschläge sind keine stillschweigende Umsetzungsfreigabe. Keine Verfälschung durch Marktreife-Gates oder SEO-/Affiliatezwang.

## Nächster gezielter Prüfschritt
Die aktuell erfassten 573 Recherche-Nennungen (Funde, nicht eindeutige Produkte) zunächst **nach Funktion gruppieren**, besonders:
- Haushalt: generische Haushaltsassistenz gegenüber Geschirr, Wäsche, Bad, Abfall, Treppen.
- Bildung: generischer Lernroboter gegenüber Handführung, Wissenschaftsexperiment, Roboterbau und ROS-Entwicklung.
- Pflege: Badehilfe, Haarpflege, Essen, Ankleiden, Mobilität – nach **echtem Zweck** und Sicherheit.
- Garten: Gartenpflege, Teich/Pool, Bestäubung, Terrassenreinigung, Forschungsheckenschnitt.
- Sport: Spielfähige Gegner, Balltraining, Platzpflege, spezielle Übungsgeräte.
Anschließend für jeden fachlich eigenständigen Typ auf der letzten WP-Ebene **eigene Inhaltsthemen prüfen** und eine eindeutige Typzahl pro Hauptwelt ermitteln, ohne doppelte Namen. Danach erst die 7/8-Hauptwelten-Alternativen nochmals vergleichen; SEO-Titel/Keywords später separat, keine bezahlten API-Calls.

**Ablage:** Diese abgeleitete GitHub-Fachnotiz ist NICHT der zweite Produkt-Master. Führende Datenquelle bleibt die in der Library aktualisierte `/robotik/Recherchebüro/CURRENT.json` V40.
