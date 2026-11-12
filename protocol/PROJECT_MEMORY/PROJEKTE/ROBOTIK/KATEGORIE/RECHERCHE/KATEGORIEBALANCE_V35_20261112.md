# Robotik Kategorie V35 – verbindlicher Prüfstand vom 12. November 2026

**Status:** neu recherchierter, rechnerisch geprüfter Sollvorschlag, **keine WordPress-Freigabe**, kein DataForSEO-Live-Lauf. Frühere Behauptungen „alle Lücken geschlossen“ waren falsch.

## Originalquellen tatsächlich geprüft
1. `PROJEKTE/ROBOTIK/KATEGORIE/ZIELVERTRAG.md`: drei Säulen; genau ein Produkt-Owner; Fachkategorie nur mit >= 3 unterschiedlichen Artikelrichtungen; 1–2-Wort-Titel; maximal 6–8 Hauptmenüs; keine künstlichen Füllungen.
2. `ARBEITSABLAUF.md` & `PRUEFREGELN.md`: eine Forschungsdatenquelle, zwei echte Abnahmegrenzen (Fach/WordPress), kontrollierter Delta-Writer, keine stillen Mutationen.
3. Echte Installationsstruktur `ROBOTIK_KATEGORIE_WORKFLOW_0.4.2_DATAFORSEO_TEST.zip/assets/robotik-first-import-plan.json`: exakt 104 WP-Seiten, 72 konkrete Produkttypseiten und 89 flache Beitragskategorien (sämtliche jeweils 4 vorgeschlagene unterschiedliche Richtungen, semantisch noch NICHT SEO-geprüft). Unter 89 tragen 63 den pauschalen Kurznamen `Kaufberatung`.
4. `/robotik/Recherchebüro/CURRENT.json` Version 34: 548 **Fundnennungen**, davon 545 mit Quell-URL und 3 ohne. 72 Original-Produktseiten eindeutig per `ROB-XXXX` gegen die 548 gebunden; 476 nicht in 0.4.2 importiert. Das bedeutet ausdrücklich NICHT 476 geprüfte neue Robotertypen.
5. Öffentliche Hersteller-/Händler-/Hochschulquellen für 14 zusätzliche Funktions- und Kollisionsfälle, mit differenziertem DE-/US-/Vorbestell-/B2B-Status.

## Ungleichverteilung belegter Original-Erstimport
Haushalt 3 | Garten 7 | Freizeit 9 | Sport 8 | Bildung 3 | Pflege 8 | Gewerbe 34.
Max/Min: 34 / 3 = 11,33. Die frühere pauschale Abschlussfreigabe ist falsch.

## Neue Hauptnavigation – **Alternative 8**, noch NICHT beschlossen
- Haushalt: 4 konservativ (3 importiert + motorisierte selbstreinigende Katzentoilette, ausdrücklich Robotik-/Automatikgrenzfall)
- Garten: 7
- Freizeit & Lernen: 14 (Freizeit 9 + Bildung 3 + Roboterbausätze + mobile ROS-Lernplattformen)
- Sport: 8
- Pflege: 8
- Landwirtschaft: 9 (aus dem bisherigen Gewerbe-Strang; kein neues Produkt)
- Service & Handel: 13 (Reinigung 3 + Gastro 3 + Hotel 2 + Medien 3 + Lager 2)
- Handwerk & Industrie: 12 (Fertigung 9 + Baustelle 3, Industrie-Landingpages als Querverweise)

Gesamt 75 konkrete **Plan-Kandidaten** (72 alte + 3 aus Hersteller-/Handelsquellen vertiefte) in 8 Hauptbereichen. Verhältnis 14/4 = 3,5 statt 34/3 = 11,3.
**2 nur bedingte Haushaltsfälle** (spezialisierter Wischroboter Hersteller heute nicht lieferbar; mobiler Telepräsenzroboter nur B2B-Bezug bestätigt), daher erst nach Marktprüfung möglicherweise 6. **9 weitere eindeutige fachliche Markt- und Abgrenzungskandidaten** zusätzlich geprüft, aber ohne belastbare DE-SEO-/Dubletten-Gates NICHT zu 75 hinzugezählt.

Alternative 7: `Haus & Garten` (11), `Freizeit & Lernen` (14), Sport (8), Pflege (8), Landwirtschaft (9), Service & Handel (13), Handwerk & Industrie (12). Numerisch gleichmäßiger, aber Haushalt verliert eigenständigen Hauptmenüpunkt; daher nicht favorisiert.

## Verbindliche Grenze – keine stillen Änderungen
Die Alternative 8 würde die zuletzt vom Nutzer freigegebene Navigation ändern (Landwirtschaft derzeit unter Gewerbe, Industrie darunter; Freizeit und Bildung getrennt); die alten hierarchischen WP-URLs können sich durch Parent-Umhängen ändern. **Erst nach ausdrücklicher Entscheidung**, URL-/Redirect-Plan und DataForSEO-SEO-Analyse darf eine kontrollierte Delta-Migration erstellt werden. Nie die 0.4.2-Erstimportstrecke erneut starten; Live-Plugin-Stand und SEO-Verbindung weiterhin nicht unabhängig ausgelesen.

## Autoritative Ablage
**Einzige fortgeschriebene Forschungs-Fundliste:** `/robotik/Recherchebüro/CURRENT.json` **v35**, alle 548 Originaleinträge byteinhaltlich unverändert (nur Revisionsmetadaten und v35-Auswertung ergänzt).
**Abgeleiteter Prüfentwurf, NICHT zweiter Fachmaster:** 
- `/robotik/Konzeptbüro/ROBOTIK_GESAMTBAUM_PRUEFBERICHT_V35.md` – vollständiger nachvollziehbarer Baum, fünf erste Produktkandidaten und neun Markt-/Abgrenzungsfälle, Quellenbelege, Freigabegrenzen
- `/robotik/Konzeptbüro/ROBOTIK_GESAMTBAUM_ALTERNATIVE_8_V35.json` – vollständige 72 Bestandsprodukt-IDs, neue Zuordnung, 8 Hierarchien und Prüfstatus
- `/robotik/Konzeptbüro/BESTANDSSEITEN_72_ROLLENWECHSEL.csv` – jedes alte Produkt samt unveränderter ID und vorgeschlagenem Ziel
- `/robotik/Konzeptbüro/RECHERCHE_548_REGISTER_ABGLEICH.csv` – 548 Zeilen mit Quelle, Importstatus und gekennzeichneter noch offener Fachprüfung
- `/robotik/Konzeptbüro/ROBOTIK_V35_PRUEFNACHWEIS.json` – Maschinenprüfsummen/Zählungen

**Nächster gebündelter Schritt ohne erneute Plugin-Runde:** fachliche Zustimmung zur Alternativnavigation; dann EINE kostenlose DataForSEO-Prüfvorbereitung im bestehenden 0.4.2-Plugin, explizite Zustimmung vor bezahlter Keywordrecherche; danach ein einziger geschützter Delta-Import (alte WP-IDs + Kategorien erhalten, Redirectplan, vorher/nachher Live-Readback). **Kein neuer Plugininstaller und keine WordPress-Writes in dieser Prüfrunde.**
