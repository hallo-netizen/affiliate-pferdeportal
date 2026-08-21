# V98 – Journal-Unterkategorien: Ursache statt Abstands-Raten

## Referenz
Verbindliche Referenz ist die bestätigte Beitragskarte auf der Journal-Hauptseite. Deren Quellblock `.pftk-journal-post-copy-v150280` verwendet 20 px Innenabstand.

## Live-V97-Befund
Der V97-Screenshot zeigte trotz vorheriger Änderungen weiterhin dieselbe relative Bild-/Label-Geometrie. Der Grund war, dass das veränderte `.entry-header`-Padding nicht die reale Position des Meta-/Kategorielabels relativ zum Bild steuerte. Zusätzlich blieb das Astra-Featured-Image-Padding aktiv. Dadurch war das Bild weiterhin oben und seitlich eingerückt und unter dem Button blieb zu viel Raum.

## V98 Pferde
- Version 1.50.463 / Contract V98.
- `post_class` ergänzt ausschließlich im Hauptloop exakt registrierter Journal-Kategorien `remove-featured-img-padding` und `pftk-journal-card-v150463`.
- `.ast-post-format-` wird ausschließlich unter diesem Marker auf `padding:0` normalisiert.
- Bild -> ockerfarbenes Meta-/Kategorielabel: 20 px.
- unterer Karteninnenabstand nach dem Weiterlesen-Button: 20 px.
- Journal-Root-Styleblock byteidentisch zu V97.
- Single-Post-Tabellen-CSS byteidentisch zu V97.

## V98 Universal
- Version 2.2.34 / Contract V98.
- Journal-Term-Beitragskarten verwenden den verbindlichen 20-px-Journal-Innenabstand.
- andere Gridtypen bleiben unverändert.

## Scope
Ausdrücklich unverändert: Tabellen, Journal-Hauptseite, Breadcrumbs, Suche, Anzeigenmarkt, Einzelbeiträge und andere Kartenraster.