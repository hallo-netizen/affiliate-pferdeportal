# V99 Workflow Lock

1. Referenz für Journal-Unterkategorie-Beitragskarten ist ausschließlich die bestätigte Journal-Root-Karte.
2. Ein lokaler Test darf nicht nur CSS-Tokens prüfen. Er muss die Zielkarte und die Referenzkarte mit identischem Inhalt im Browser rendern und Geometrie vergleichen.
3. Pflichtmaße Desktop: Bild 205 px; Bild->sichtbarer Labeltext 20 px; Label->Titel 7 px; Titelreserve 2.55em; Titel->Auszug 10 px; Auszug-Abstand 17 px; CTA min. 150x42 px; CTA->Unterkante 20 px plus Rahmen.
4. Pflicht-Pixeltest: Bei identischem Inhalt muss die vollständige Referenz-/Zielkarte pixelidentisch sein, soweit derselbe Bildplatzhalter und dieselben Fonts verwendet werden.
5. Scope fail-closed: nur exakt registrierte Journal-Unterkategorien. Fremde Kategorien müssen im Negativtest ohne Journal-Klasse, künstliches Meta, Journal-CTA und Journal-CSS bleiben.
6. Journal-Root-Styleblöcke und Single-Post-Tabellen-CSS müssen bei einem reinen Unterkategorie-Fix byteidentisch bleiben.
7. Kein Installer ohne Source->Fresh-Unpack Bytegleichheit, CURRENT_PLUGIN_SOURCE->embedded Installer Bytegleichheit, Master-Manifest und ZIP-Test.
8. Live-PASS darf erst nach Nutzer-Screenshot erklärt werden.