# V104 – Root Cause und Änderungskatalog

## Ausgangslage
V101, V102 und V103 führten live bei den betroffenen neuen Beiträgen zu keiner sichtbaren Änderung. Diese drei Stände sind deshalb keine Freigabenachweise.

## Fehler im bisherigen Prüfansatz
Der V103-Harness war als Sichtvergleich ungültig: Als „Altbeitrag-Referenz“ wurde eine Tabelle→H2-Situation gegen eine Tabelle→Absatz-Situation des Neubeitrags verglichen. Das ist kein gleichartiger DOM-/Geometrievergleich. Die daraus abgeleitete Behauptung eines passenden Sichtabstands war nicht belastbar.

Zusätzlich waren V101–V103 an konkrete, nur angenommene Markup-/Adjazenzformen gekoppelt. Der Live-FAIL beweist, dass diese Annahmen nicht als Nachweis für den tatsächlich gerenderten WordPress-DOM verwendet werden dürfen.

## V104 – Architekturkorrektur
V104 setzt den 28-px-Tabellenabstand nicht mehr als kollabierbaren CSS-Margin auf eine vermutete Struktur. Auf Einzelbeiträgen wird nach Abschluss des bestehenden Artikel-Design-Runtimes der finale Browser-DOM geprüft.

Produktionssignaturen sind `table.comparison-table` oder `table.system-129-table`. Der tatsächliche äußere Tabellenblock wird ermittelt. Nur wenn der tatsächlich folgende Inhaltsknoten ein Absatz ist, wird unmittelbar davor ein reales, nicht kollabierendes 28-px-Spacerelement eingefügt. Der äußere Tabellenblock erhält in genau diesem Fall `margin-bottom:0`, um Doppelabstände auszuschließen. Folgt H2/H3/Section statt eines Absatzes, wird nichts verändert. Plain-Legacy-/Gutenberg-Tabellen ohne Produktionssignatur bleiben unberührt.

## Prüfung
- Exakter betroffener Produktionsartikel „Welche Regendecke mit Abschwitzfunktion ist die beste?“: 17 px → 45 px sichtbarer Block→Absatz-Abstand.
- Exakte aktuelle Wrapper-Produktionsform: 28 px → 45 px.
- Adversarial: äußeres article entfernt, data-block entfernt, Tabellenblock geflattet, alle Marker bis auf comparison-table entfernt: PASS.
- Plain Gutenberg Legacy-Tabelle: unverändert PASS.
- Tabelle→H2: unverändert PASS.
- 1440/1200/900/390 px: PASS.
- Voller verfügbarer Produktionsplan-Korpus: 20/20 einzigartige tabellenhaltige Artikel PASS.
- Fresh-Unpack des fertigen Installers erneut mit demselben Browser-Harness: PASS.

## Unverändert
`assets/single-post-locked-v15083.css`, Journal-V100-Owner-Logik und `article_design_script` sind gegenüber V103 byteidentisch. Tabelleninhalt, Farben, Linien, Zellpadding, Suche, Breadcrumbs, Anzeigenmarkt, Kategorien, Titel, Textinhalt und Artikeltypregeln wurden nicht geändert.

## Freigabegrenze
V104 ist LOCAL PASS / FRESH-INSTALLER PASS. Ein Live-PASS darf erst nach sichtbarer Prüfung auf der echten WordPress-Seite behauptet werden.
