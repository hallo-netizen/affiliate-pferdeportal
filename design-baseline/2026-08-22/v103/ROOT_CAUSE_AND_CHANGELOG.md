# V103 – Tabellen-Sichtabstand Neubeiträge

Live-Rückmeldung nach V102: keine sichtbare Änderung.

## Reproduzierte Ursache

V102 nahm nur `article.ppm-generated > section[data-block="table"] > .pm-table-wrap.wp-block-table + p` an.

Der exakt betroffene Beitrag **„Welche Regendecke mit Abschwitzfunktion ist die beste?“** liegt im realen Produktionspaket dagegen als `article[data-article-type="Vergleich"]` mit **direkter** `section[data-block="table"] > table.comparison-table + p` vor. V102 kann diese Form nicht treffen.

Die zweite reale Neubeitragsform besitzt `.pm-table-wrap.wp-block-table`. Dort war bereits ein 28-px-Abstand vorhanden. V102 verschob lediglich 28 px vom Wrapper auf den Absatz und war deshalb geometrisch ohne sichtbaren Effekt.

## Verbindlicher Sollwert

Die live freigegebenen Altbeiträge bleiben Referenz. Mit dem unveränderten Single-Post-CSS ergibt Tabelle → folgende H2 durch `margin-top:1.65em` responsiv:

- 1440 px: 54.44 px
- 1200 px: 47.52 px
- 900 px: 44.55 px
- 390 px: 44.55 px

V103 gibt dem unmittelbar folgenden Absatz in einem semantischen `section[data-block="table"]` exakt denselben Rhythmus: `clamp(44.55px, 3.96vw, 54.45px)`.

Unterstützte reale Formen: direkte Tabelle, `figure.wp-block-table`, `.wp-block-table`/`.pm-table-wrap.wp-block-table`, `.comparison-table-wrap`.

Legacy-/nicht-semantische Tabellen, V100 Journal, Suche, Anzeigenmarkt, Inhalt, Titel und Beitragsarten bleiben unverändert.
