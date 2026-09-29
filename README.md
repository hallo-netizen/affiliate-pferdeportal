# Pferde Atelier – Konzept 9

Greenfield-Arbeitsraum. Dieser Branch enthält nur K9.

Grundidee: Recherche, Schreiben, Prüfung und Reparatur sind eigenständige Produktionsstationen. Ein Stationslauf muss vollständig abgeschlossen und gespeichert sein, bevor sein Ergebnis als Eingang einer anderen Station gilt. Zwischen Stationen gibt es keine automatische Fortsetzung.

Ein Abbruch wird nicht durch Rekonstruktion eines Gesamtworkflows behandelt: Ein offener Stationsauftrag bleibt `runtime/CURRENT_JOB.json`. Derselbe Stationsstart liefert exakt diesen Auftrag erneut. Ein Teilpaket kann nicht akzeptiert werden.

K9 liest oder importiert keine Zustände, Module oder Laufpfade aus K4–K8. Bestehende Konzepte werden nicht verändert.
