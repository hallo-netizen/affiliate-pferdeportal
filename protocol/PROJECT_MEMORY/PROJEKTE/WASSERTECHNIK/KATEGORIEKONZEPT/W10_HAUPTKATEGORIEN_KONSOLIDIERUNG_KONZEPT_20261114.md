# Wassertechnik W10 – 7 Hauptbereiche, keine künstliche Menüfüllung
Stand 14.11.2026 · **FAHREMPFEHLUNG / NOCH NICHT FREIGEGEBEN, KEINE WP-ÄNDERUNG**

## Ursache und echte Datenbasis
W7 hat **8 Käufer-Hauptbereiche plus Industrie** als neunten sichtbaren Hauptmenüpunkt umgesetzt; das verletzt die vom Nutzer verbindlich genannte **6–8-Hauptkategorien-Vorgabe**. Das Mega-Menü ist aufgrund einiger isolierter kleiner Bereiche ungleichmäßig: Brunnen hat nur 3 Produktlinks / 1 Gruppenüberschrift, Wasseranalyse 8 / 2, Bewässerung 6 / 2, Wassertanks 6 / 2 und Abwassertechnik 8 / 2. Dies ist **vor allem ein Struktur- und Menükonzeptfehler**, kein Beleg, dass Wassertechnik insgesamt zu wenig Produkte besitzt.

Einzige aktuelle Quelle: `W7_MEGAMENUE_ANZEIGEVORSCHAU_20261114.json` mit **79 konkreten Produktlinks**, davon **71 Käuferthemen + 8 separate industriebezogene Produktseiten**. W4-Fachbaum, W5-SEO-Ergebnisse, W6-Importliste und 105 produktbezogene WP-Inhaltskategorien behalten ihre Bedeutung.

## Empfehlung: genau sieben fachlich sinnvolle Hauptbereiche
| Menü und inhaltlicher Hauptbereich | Frühere W7-Bereiche | Bereits vorhandene Produkte | Visuell sinnvolle Mega-Menü-Blöcke |
| --- | --- | ---: | --- |
| Wasseraufbereitung | Wasseraufbereitung | 19 | Hauswasserfilter, Trinkwasserfilter, Osmoseanlagen, Filterzubehör, Aufbereitungsanlagen (3 Spalten) |
| Wasseranalyse | Wasseranalyse | 8 | Labortests (3), Schnelltests & Probenahme (2), Messgeräte (3), **nur visuelle Unterteilung der vorhandenen Testsets**, keine neue WP-Seite |
| Brunnen & Bewässerung | Brunnen + Bewässerung | 9 | Brunnenbauteile (3), Bewässerungssysteme (2), Schlauch (1), Steuerung (3), 2–3 Spalten |
| Pumpen & Druck | Pumpen & Druck | 12 | Pumpen (5), Druckversorgung (3), Steuerung & Zubehör (4), 3 Spalten |
| Regenwasser & Wassertanks | Regenwasser + Wassertanks | 15 | Regenspeicher (3), Filter & Förderung (3), Nutzung & Rückhalt (3), Tankarten (4), Tankzubehör (2), 3 Spalten |
| Abwassertechnik | Abwassertechnik | 8 | Rückstau & Heben (2), Rohre & Zugänge (3), Aufbereitung & Speicherung (3), **nur visuelle Unterteilung vorhandener Entwässerung**, 2 Spalten |
| Industrie & Großanlagen | Industrie & Großanlagen | 8 | 4 Gruppen mit tatsächlichen Industrie-Produktlinks: Industrielle Wasseraufbereitung (3), Kühlwasser (1), Industrie-Pumpen (2), Messung/Dosierung (2). Die 2 Industrie-Landings ohne eigene Industrie-Produktseiten sind über den Industrie-Hub zugänglich; keine leeren Mega-Menü-Spalten |

**Kontrolle:** 19+8+9+12+15+8+8 = **79 Produkte**, jedes genau einmal. **Sieben** sichtbare Hauptmenüpunkte, davon sechs auf Privatkunden/kleine Betriebe ausgerichtet plus Industrie als nachgeordneter Informationszugang. Nicht 9 sichtbare Bereiche. Die zwei geplanten Zusammenlegungen erhalten Brunnen, Bewässerung, Regenwasser und Wassertanks als fachliche **Untergruppen**, statt sie zu verstecken.

## Drei Säulen und SEO-Vertrag
- Unterste **WordPress-Seitenebene** bleibt konkrete Produktart/technisches System. Die 105 zugehörigen **WP-Beitragskategorien** behalten jeweils exakt diesen Produktbezug; sie erscheinen auf Produktseiten, **nicht** als zusätzliche Mega-Menüebene.
- Kategorienamen/Zahl sind nicht starr; ungefähr 3–5 eigenständige Artikelideen nur **weiche** Orientierung, kein hartes Gate.
- Keine neuen SEO-Owner, Beitragskategorien oder Produktseiten nur zur visuellen Füllung. Die W4/W5-Recherche wird nicht pauschal erneut bezahlt; kein zweiter Import-Worker, kein WordPress-Core-Umbau.
- **Wichtige technische Unterscheidung:** Wenn lediglich sieben Navigationsreiter angezeigt werden, bleiben zunächst die **neun alten WP-Hauptseiten** und deren vorhandene URLs bestehen. Das ist keine vollständige Umstellung des echten WP-Hauptseitenbaums. Eine echte Reduzierung auf **7 WP-Hauptseiten** erfordert **einen** gemeinsamen, kontrollierten Seitenbaum-Umbau mit neuer Eltern-/Kindzuordnung, gleichzeitiger Aktualisierung der zentralen Import-/Menüquelle und Weiterleitungen aller betroffenen alten URLs; keine stillen Slugwechsel, kein halbseitiger Umbau. Das zugehörige Risiko (WP-URL-Änderung) ist vor einer Implementierungsfreigabe offen zu benennen.
- Die Seite ist laut Nutzer derzeit gesperrt / Frontend zugänglich; kein konkreter Google-Indexzustand für die neu publizierten Seiten behauptet. Nicht behaupten, URL-Wechsel seien garantiert risikolos.

## Gezielt recherchierte echte Produktlücken – nur Kandidaten, keine sofortige Seite
1. **Brunnen:** Brunnenkopf/Brunnenkappe, Brunnenrohr; Hersteller-/Fachbeleg https://www.hdg-gmbh.com/produkte/brunnenbau-zubehoer/ . Vor Aufnahme eigenständige Kaufabsicht/Redaktionsfragen und Überschneidung mit vorhandenem Brunnenfilterrohr prüfen.
2. **Bewässerung:** Viereckregner, Tropfrohr, Beregnungsventil, Schlauchaufbewahrung als reale Produkttypen; Quelle https://www.gardena.com/de/produkte/bewaesserung . Nur neue **konkrete** Produktart mit anderen Nutzungsfragen als vorhandenes Tropfbewässerungsset / Versenkregner / Gartenschlauch.
3. **Abwassertechnik:** Fettabscheider und Leichtflüssigkeits-/Ölabscheider sind tatsächlich eigenständige Anlagen für auch kleinere betriebliche Einsätze; Beleg https://www.aco-haustechnik.de/produkte/fettabscheider/ und https://www.aco.at/produkt-katalog/abwasserbehandlung . WP-Owner erst nach fachlicher SEO-Trennprüfung, nicht zum Menü-Auffüllen.
4. **Wassertanks und Wasseranalyse:** Hersteller-/Produkttyp-Lücken gezielt prüfen (Tank-Entnahmeventile, Schwimmerventile; Leitfähigkeits-/Trübungsmessung). **Hier noch keine ausreichend geprüfte eigenständige Quell- und Keyword-Zuordnung**, daher keine automatische neue WP-Seite.

Diese Beispiele beweisen nur **existierende Produkttypen**, weder deren Suchvolumen noch ihre Eignung als getrennte SEO-Seite. Die ursprünglichen 79 Links bleiben bis zur Entscheidung vollständig erhalten.

## Ein einziger nächster Umsetzungsblock nach Freigabe
1. **Eine Gesamtentscheidung:** die sieben fachlichen Hauptbereiche plus 2 Fusionen als neue Navigations- und – wenn verlangt – echte WP-Hauptseitenstruktur genehmigen, inklusive einmaligem URL-/Redirect-Konzept; keine 1:1 bloße Kosmetik als vollständige Baumkorrektur ausgeben.
2. In der **bestehenden WT001/Designsteuerung** nur eine zusammenhängende Übernahme: zentrale Fachzuordnung, gegebenenfalls echte WP-Eltern/URLs und Weiterleitungen, sieben Menü-Auslöser, ausgewogenes Mega-Menü, keine leeren Linkgruppen. **Keine weiteren Mini-Plugins**.
3. **Eine** wirkliche Desktop-/Mobil- und WordPress-Pfad-Gesamtabnahme. Neue Produkte erst anschließend gezielt bei belegtem eigenständigem Bedarf, nicht als künstliche Füllung.

**Status: W10 Konzept vorliegend, NICHT implementiert. Keine Website-, Plugin-, W4/W5/W6/W7-Daten- oder SEO-API-Änderungen.**