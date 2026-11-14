# Robotik V64 – C-Vertrag und gleichmäßig gefülltes Megamenü (14.11.2026)

## Ausgangslage – belegte Ursachen, keine Vermutungen
- Die 0.2.3-Strukturdesign-PHP aus der Robotik-Library wurde direkt geprüft, ebenso die CSS und die echte V62-WP-Inventur/188-Seiten-Sollstruktur. GitHub-Beleg 12.11.: `DESIGN/NAVIGATION_EBENEN_AUDIT_20261112.md` hatte **104/104** Links im damaligen 7-Welten-Megamenü; keine fehlenden Seiten im lokalen Mock.
- Aktuelle PHP hat `ROOTS=['haushalt','garten','freizeit','sport','bildung','pflege','gewerbe']` und **lässt die achte neue Welt „Humanoide“ aus**. Muss bei Designweiterentwicklung korrigiert werden.
- Das alte Menü zeichnet jedes direkte Kind einer Hauptwelt **als Spaltenüberschrift**; nur wenn diese Seite wiederum Kindseiten besitzt, folgt darunter eine Liste. Direkte Produktseiten sehen deshalb wie „leere“ Rubriküberschriften aus. CSS nutzt `repeat(auto-fit,minmax(170px,1fr))` mit `align-items:start`, **ohne Höhenausgleich**; ungleichmäßige Spalten sind damit ein Codeeffekt.
- Die Vorversion nimmt WP-Drafts für angemeldete Admins in die Menüausgabe auf, öffentlich nur veröffentlichte Seiten. **Test-Entwürfe verzerren also das eingeloggte Menü**. Öffentliche Navigationsdarstellung muss nur veröffentlichte Links verwenden; ein Admin-Entwurfsmodus darf getrennt und ausdrücklich sein.
- V62-Soll: **8 Welten; 47 Gruppen, 141 Produkttypen, 296 zugehörige WP-Beitragskategorien**. Von 141 Produkten besitzen 55 eine Rubrik, 17 zwei und 69 drei; jede Rubrik hat 3 bis 4 *unterschiedliche Themenrichtungen*, noch **keine Garantie für 3–5 veröffentlichbare Artikel**. 16 ungeklärte Robotertypen und 48 Rubriken bleiben SEO-HOLD. Altes V63-Readback 16/227 war **während** des Imports; kein Endnachweis.
- Kritisch: Die WordPress-**Beitragskategorien** liegen inhaltlich **unter der konkreten Produktseite** und sind nicht automatisch weitere WP-Seiten und daher keine Ebene, die der Header künstlich anzeigen müsste. Sie sind für die jeweilige Produktseite vorgesehen.

## Lösung A – Empfehlung: Menülayout vom Fachbaum trennen
1. WP-Fachbaum und stabile vorhandene Seiten-IDs, Unterseiten, Kategorien und URLs **unangetastet lassen**. Seitenstruktur fachlich gestalten; Menüdarstellung eigenständig.
2. Jede 2.-Ebene-**Gruppenseite** als Überschrift und ihre direkten **konkreten Robotertypen** als Links darunter. Direkte konkrete Robotertypen ohne Unterseiten **nicht** als einzelne leere Spaltenüberschriften zeichnen, sondern ohne erfundene WP-Zwischenseite unter einer **rein optischen, nicht anklickbaren** Gruppe `Weitere Robotertypen` sammeln. Jeder echte Link nur einmal, alle veröffentlichten Seiten weiter erreichbar.
3. Pro Mega-Flyout **2–4 gleich breite Spalten** abhängig von Gesamtzahl der Links; Ausgleich nach tatsächlicher Höhe/Textlänge und Umbruch (nicht nur nach Zahl der Obergruppen). Desktop kompakte Spalten, gleiche Abstände/Überschriftgrößen; große Gewerbegruppen auf 4 Spalten verteilen; schmale Bereiche entsprechend auf 2–3. Keine leeren Platzhalter, erzwungenen vierte Kategorien oder 0-Inhalt-Kacheln.
4. **Achte Hauptwelt Humanoide** in Kopfmenü aufnehmen. Gewerbe > Industrie bleibt bewusstes Sondermodell mit vier Landingpages, tiefe Struktur über die jeweiligen Landingpages erreichbar.
5. **Nur veröffentlichte Seiten** im öffentlichen sowie normalen Admin-Menü. Entwürfe getrennt und gekennzeichnet in einer bewusst aktivierten Backend-/Vorschauansicht, nicht im normalen Header.
6. Auf der **untersten Robotertypseite** die passenden WordPress-Rubriken als echte Vertiefung mit aussagekräftiger Benennung ausgeben; keine 296 Rubriken in die Kopfzeile legen. Inhalte und Produktseiten zuerst redaktionell abnehmen, keine leeren Taxonomiearchive blind veröffentlichen.
7. **Mobil** einspaltig je Welt mit aufklappbaren Zwischenbereichen, Link zum Weltüberblick, sämtliche veröffentlichten Ziele erreichbar. Nicht das Desktop-Megagrid verkleinert darstellen.
8. WordPress-Inhalte, URL-Struktur, Kategorie-Plugin, Magazin/Glossar/Roboterfinder/HivePress, Footer und SEO-/Affiliate-Funktionen **nicht ändern**. Implementation ausschließlich im bestehenden Designplugin `robotik-strukturdesign`, erst nach Freigabe der sichtbaren Änderung.

## Warum keine künstlichen Rubriken
- C-Vertrag: Jede letzte **Seitenebene** behandelt einen klaren Robotertyp; WP-Kategorien vertiefen **dessen** Fachthemen. Ein eigener Unterbereich nur, wenn echte Leserfrage, sinnvoll unterschiedliche Inhalte und nach Daumenregel mindestens ca. **3–5 plausible Artikel** zu erwarten sind. Anzahl der Kategorien ist kein Zielwert.
- Oberer Baum soll ausgeglichen **ohne fachfremde Füllseiten** sein. Bei einzelnen dünnen Gruppen (z.B. Humanoide > Haushalt nur Haushaltsassistenten; Intimrobotik nur Intimroboter) im Menü sparsam präsentieren; langfristige fachliche Gruppierung gesondert redaktionell prüfen, **keine automatische Verschiebung von Elternseiten/URLs**.
- 55 Typen mit nur einer Rubrik sind keine automatische Fehlleistung: je nach Fachbreite auf 2 oder 3 Rubriken erweitern, **nur** wenn klar abgrenzbar und jeweils 3–5 Artikelideen möglich. Die 63 alten generischen „Kaufberatung“-Kurzlabels sind redaktionell zu präzisieren, ohne deren IDs/Zuordnungen neu anzulegen.

## Konkrete Datenprobe je Welt (V62, 2.-Ebene)
| Welt | echte Zwischenbereiche | direkte Robotertypen | Präsentation |
|---|---:|---:|---|
| Haushalt | 3 | 7 | 3 Sachgruppen + gebündelte direkte Roboter |
| Garten | 3 | 7 | 3 Sachgruppen + gebündelte direkte Roboter |
| Freizeit | 4 | 3 | 4 Sachgruppen + direkte Roboter |
| Sport | 3 | 5 | 3 Sachgruppen + direkte Roboter |
| Bildung | 2 | 4 | 2 Sachgruppen + direkte Roboter |
| Pflege | 5 | 2 | 5 Sachgruppen + direkte Roboter |
| Humanoide | 6 | 0 | 6 echte Sachgruppen |
| Gewerbe | 9 | 5 | Gewerbegruppen inkl. Industrie-Landingpage + direkte Roboter |

## Alternativen (nicht empfohlen)
- **Alle Seiten künstlich auf gleiche Baumtiefe umbauen:** verletzt Suchintention, vorhandene IDs/URLs und KISS.
- **Alle 296 WP-Rubriken im Megamenü anzeigen:** überfrachtet Navigation und zieht die unterste Fachvertiefung aus den Robotertyp-Seiten.
- **Immer nur zwei Ebenen, Rest ausschließlich auf Landingpage:** optisch ruhig, aber Nutzer findet einzelne Produkte später und vorherige 104/104-Link-Abdeckung entfällt.

## Verbindlicher Test vor irgendeinem Live-Plugin
- Original-Designplugin 0.2.3 technisch minimal anpassen; **8/8 Hauptwelten**, alle **veröffentlichten** WP-Seiten **genau einmal** im jeweiligen Welt-Megamenü erreichbar; keine Entwurfslinks, keine Phantomlinks/Phantomkategorien.
- Pro Welt Überschriften vs direkte Roboter korrekt; durchgehende Klickpfade und Produktkategorien nur auf Produktseiten; Industrie-Landingpages bleiben erreichbar.
- 1440/1024/780/390 Pixel inklusive Hover, Fokus/Tastatur, mobilem Öffnen/Schließen, langer Textlänge und „Mehr“-Bereichen testen.
- Zuerst **offline visueller Vergleich** anhand aktueller 188er-Sollstruktur, ggf. Reproduktion des öffentlichen Publish-Subset; dann **eine einzige** abgestimmte Version des bestehenden Designplugins. **Noch keine Frontend-Änderung und kein neuer Plugininstaller autorisiert.**
