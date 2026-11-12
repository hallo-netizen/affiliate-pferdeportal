# Robotik – verpflichtender Gesamtprüfstand Kategorien (12.11.2026)

## Reale Ausgangsbasis und Korrektur der falschen alten Abschlussaussage
- **Quelle:** Original-ZIP `ROBOTIK_KATEGORIE_WORKFLOW_0.4.2_DATAFORSEO_TEST.zip`, Datei `assets/robotik-first-import-plan.json`; alter Konzeptbaum `ROBOTIK_PORTALMODELL_AKTUELL.json`, Register `/robotik/Recherchebüro/CURRENT.json` Version 34.
- **Ist-Seiten nach eingebettetem 0.4.2-Plan:** 7 Hauptseiten, 25 Zwischen-/Landeseiten, 72 konkrete Produkttypseiten, 89 WordPress-Beitragskategorien = 193 CORE-Objekte. Die 104 Seiten wurden laut früherem Betreiber-Schritt angelegt; unabhängiger Live-Readback ist nicht in diesem Chat erfolgt.
- **Ursprünglich nicht vollständig fachlich geprüft:** Haushalt 3 Produkte / 4 Beitragskategorien; Garten 7/9; Freizeit 9/10; Sport 8/9; Bildung 3/4; Pflege 8/9; Gewerbe 34/44. 63/89 Beitragskategorien mit kurzem Label „Kaufberatung“.
- **Besonders kritisch:** Gewerbe > Industrie > Produktion/Logistik/Infrastruktur/Spezialrobotik: vier Landingpages, null darunter unmittelbar angehängte Produktseiten. Konkrete Industrieprodukte existieren unter Gewerbe > Fertigung usw., benötigen eindeutige Querverweise, keine Duplikat-SEO-Seiten.
- **Alt-Konzept 221 vs Importplan 208:** 13 zusätzliche Glossar-Knoten im Konzept, nicht die fehlenden Haushalt-/Bildungsprodukte.
- **Recherche v34:** 548 Fundnennungen, NICHT 548 gesonderte kaufbare Produkttypen. 11 dokumentierte vorläufige Käufer-Hauptgruppen, 16 Käufersegmente; vollständige SEO-/WordPress-Freigabe explizit offen. Frühere Behauptung „komplette Kategorieforschung erledigt“ ist daher als falsch zu behandeln.

## Neu geprüfte gezielte Fälle
- Haushalt: selbstreinigende Katzentoilette ROB-0509 (EU-Angebot ja, Robotik-Grenzfall), getrennte Wischroboter (Markttyp ja, gesonderter DE-Lieferstatus prüfen), Aquariumglas ROB-0089 (Lieferstatus/Robotik offen), Telepräsenz (Abgrenzung privat/Schule/Pflege offen). Universelle Haushaltsassistenten ROB-0075, Wäschefalten ROB-0175 und Kochroboter nur Forschung/Magazin wegen fehlendem DE-Serienangebot.
- Bildung: reale programmierbare Roboterbausätze (Makeblock), mobile ROS-Lernplattformen (TurtleBot), Schultelepräsenz und Lerndrohnen bestehend. Tischroboterarme ROB-0503 und Roboterhunde ROB-0506 haben schon einen Freizeit-Produkt-Owner: in Bildung QUERVERLINKEN, nicht erneut als Produktseite anlegen.
- Sport: Golfbunker ROB-0053 und Badminton ROB-0524 erst Markt-/Robotik-/SEO-Prüfung; Padel/Pickleball-Sammeln sind der bestehenden Ballsammel-Funktion zuzuordnen, keine Dubletten.
- Pflege: Reha-Handschuhe ROB-0296 und Gehrehabilitation ROB-0076 gegenüber allgemeiner Therapie/Exoskeletten abgrenzen.
- Garten: Heckenschneidroboter ROB-0537 als Vorbestellung/Fernsteuerungsgrenzfall nicht automatisch importieren; vorhandene 7 Hauptprodukte bleiben. Yarbo nutzt denselben Roboterkern mit verschiedenen Aufsätzen – keine Produktpage pro bloßem Aufsatz erfinden.
- Freizeit: Porträt-Zeichenroboter ROB-0065 im bestehenden Register, Angebot und Intent noch prüfen.
- Gesamt: 21 explizit mit Quellstand/Entscheidung markierte neue/überlappende/ausscheidende Kandidaten, **keine 21 blind neuen Produktseiten**.

## Vorschlag Navigation und Gleichmäßigkeit
1. **7 sichtbare Hauptkategorien vorläufig beibehalten**; besonders Haushalt und Bildung auf real belegte Unterbereiche erweitern, keine leeren künstlichen Kategorien. Gewerbe bleibt breiter, weil es sehr viele professionelle Einsatzgebiete bündelt.
2. Haushalt sinnvoll nach Reinigung, Haustiere, ggf. Alltagsassistenz/Kommunikation (letztere **erst bei belegt eigenen kaufbaren Typen**); Bildung nach Programmieren, Praxisrobotik, Schultelepräsenz.
3. Optional acht Hauptbereiche durch **Landwirtschaft separat** mit 9 Produkten (Gewerbe dann 25). ABER das widerspricht der zuvor ausdrücklich festgelegten Unterordnung unter Gewerbe und würde veröffentlichte URLs ändern. Ohne neue Entscheidung NICHT umstellen.
4. Alternative Haus + Garten zu „Haus & Garten“ vereinigt und Landwirtschaft als eigene Welt bleibt wegen rein optischer Gleichverteilung und URL-Änderung nicht empfohlen.

## Technischer KISS-Weg
- **Kein erneuter 0.4.2-Erstimport!** Der echte Code von `class-robotik-first-import.php` blockiert bei bereits veröffentlichten Bestandseiten den Dry-Run; kein sicheres Add-only-Delta vorhanden.
- Erst **ein fachliches freigegebenes Delta**, Quelle der einzige Forschungs-Master; SEO-/Suchintentionen im vorhandenen `Robotik Kategorie → DataForSEO` prüfen, keine kostenpflichtigen Aufrufe ohne gesonderte Freigabe.
- Dann **EIN Update derselben Kategorie-Pluginlinie** mit geschütztem Add-only-/Readback-Sync vorbereiten (keine neuen IDs für alte Seiten, keine stille Parent-Änderung, keine Duplikate). Die 89 flachen Beitragskategorien gehören später auf die passenden Produktseiten; Industrie-Landingpages nur auf existierende Typen verlinken. Keine weitere Designrunde vor Klärung.
- **Heute wurde kein WordPress- oder Plugin-Schreibvorgang ausgeführt.** Der Prüfstand liegt in der Library unter `/robotik/Konzeptbüro/ROBOTIK_GESAMTKATEGORIE_AUDIT_20261112.md` und gleichnamiger JSON; `ROBOTIK_GESAMTKATEGORIE_AUDIT_VALIDIERUNG_20261112.json` enthält maschinelle Bestandszählung. Das sind Prüfdokumente, KEIN neuer unabhängiger Forschungs-Master.

## Herangezogene Herstellerbelege
- DE Katzentoilette: https://www.litter-robot.com/eu/de/litter-robot-4.html
- DE Wischroboter bisher als nicht lieferbar: https://www.irobot.de/de_DE/irobot-braava-jet-m6/M613340.html
- US-Haushaltskochroboter: https://www.posha.com/private-chef
- Kalifornische Wäschefaltrobotik: https://www.weaverobotics.com/
- Bildung Roboterarm: https://de.dobot-robots.com/products/education/magician.html
- Bildungsfahrplattform: https://docs.robotis.com/docs/systems/turtlebot3/overview/
- Schullern-Roboterhund: https://learning.petoi.com/bittle-x
- Modulares Gartenrobotergerät: https://eu.yarbo.com/collections/modules

**WICHTIG:** Dies ist ein fachlicher Audit mit Lücken- und Grenzentscheidungen, keine abgeschlossene Markt-Sättigungs- oder SEO-Recherche und kein Live-Import-PASS.
