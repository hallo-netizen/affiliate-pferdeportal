# Handoff an das Kategorie-Plugin

## Einstieg
Lies zuerst:
1. README.md
2. KONZEPT_MASTER.md
3. HOBBY_ROHLISTE.md

## Wichtig
Der Inhalt dieses Büros ist PLANUNGSINPUT.
Die aktuelle Gruppierung der Rohliste ist keine freigegebene Taxonomie.

## Verbotene Fehlinterpretation
Nicht aus den Zwischenüberschriften der Rohliste automatisch Hauptkategorien erzeugen.

## Gewünschte spätere Aufgabe
Wenn die Recherche ausreichend groß ist:
- Hobby-Kandidaten clustern
- Produkt-/Bedarfswelten prüfen
- Suchintentionen/Keywords clustern
- dann eine hierarchische Struktur entwickeln:
  SEITE → SEITE → SEITE → KATEGORIE → BEITRÄGE

## Zwei Wege müssen erhalten bleiben
1. Inspiration / Langeweile / Entdecken
2. konkretes Hobby / Wissen / Ausrüstung / Kauf

## Magazin
Magazin/Journal ist der zweite SEO- und Inspirationseinstieg für Bedürfniskeywords wie:
„Langeweile“, „zuhause“, „Winter“, „alleine“, „zu zweit“, „ungewöhnliche Hobbys“ usw.
Es ersetzt nicht die Haupt-Hobbyarchitektur.

## Nachtrag 2026-10-03 – verbindlicher Zielrahmen für die nächste Kategorie-Arbeitsphase

Status dieses Nachtrags: Planungs-/Zielbindung für das Kategorie-Plugin, **keine CURRENT-Autorität und keine eigene NEXT ACTION**.

### KISS-Ziel
Die komplette Portalnavigation soll möglichst in einem zusammengefassten Workflow aus dem bestehenden Konzept und DataForSEO abgeleitet, nach WordPress geschrieben und anschließend im Frontend sichtbar gemacht werden.

Zu erzeugende Bereiche:
1. Hauptportal / Hobbywelten
2. Magazin-/Journal-Kategorien
3. HivePress-/Anbieter-Kategorien

### DataForSEO-Autorität innerhalb des Konzept-Rahmens
Das Konzept bestimmt Zweck, Geschäftslogik und den Strukturrahmen. Die sichtbaren SEO-Bezeichnungen und die konkrete Hierarchie werden nicht manuell vorgegeben.

DataForSEO bestimmt auf Basis realer Suchnachfrage und Suchintentionen:
- die konkreten Bezeichnungen der Seiten und Kategorien;
- die Zuordnung von Haupt- und Unterbegriffen;
- die Hierarchie nach unten;
- die Trennung von Synonymen, Unterformen und eigenständigen Suchräumen;
- die passende Ebene eines Suchraums innerhalb von `SEITE → SEITE → SEITE → KATEGORIE → BEITRÄGE`.

Die Hierarchie muss gegen ihre unteren Ebenen geprüft werden: Ein Oberbegriff darf nur gewählt werden, wenn die darunterliegenden Cluster semantisch und suchintentionsseitig sauber darunter passen. Höheres Suchvolumen allein darf keine unpassende Parent-Bezeichnung erzwingen.

### Automatisierungsziel
Der Normalweg soll ohne manuelle Begriffswahl oder manuelle Baumkorrektur durchlaufen. Echte unauflösbare Mehrdeutigkeit darf fail-closed blockieren; sie darf nicht geraten werden.

Zusammengefasster Zielpfad:
`Konzept → DataForSEO → Clustering/Deduplizierung → Hierarchie + sichtbare Bezeichnungen → Hauptportal + Magazin + HivePress → Kannibalisierungs-/Owner-Prüfung → Dry-Run → WordPress-Write → Veröffentlichung → Frontend-Navigation → Readback`.

### Frontend-Ziel
Erfolg bedeutet nicht nur angelegte WordPress-Objekte. Der vollständige freigegebene Zielbaum muss im Frontend erreichbar und sichtbar sein. Seiten, die Teil des freigegebenen Navigationsbaums sind, dürfen nicht nur als Entwurf verbleiben. Frontend-/Navigations-Readback gehört zum Endzustand.

### Hobbyfinder-Anschluss
Der Hobbyfinder verändert den SEO-Kategoriebaum nicht. Für spätere Filter-/Finder-Funktionen muss jedes Hobby jedoch eine stabile zentrale Hobby-Identität besitzen, an die Finder-Eigenschaften und Querverweise angebunden werden können. Finder-Eigenschaften wie `drinnen`, `draußen`, `alleine`, `zu zweit` usw. sind keine automatisch erzeugten Navigationskategorien.

### Test-/Abnahme-Hardrule
Keine Abnahme, kein Upload-/Live-Kandidat und keine Deploymentempfehlung ohne dokumentierte vollständige lokale **positive und negative E2E-Simulation** des real relevanten Pfads bis einschließlich Frontend-Zielzustand, inklusive Manipulations-/Fail-closed-Fällen, Idempotenz und Readback.
