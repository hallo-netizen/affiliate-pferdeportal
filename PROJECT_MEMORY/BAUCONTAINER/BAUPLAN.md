# BAUCONTAINER – BAUPLAN

STAND: 2026-09-05
STATUS: V1

## Grundmodell

```
CAMPUS
└── PROJEKTGEBÄUDE
    └── BÜRO / ABTEILUNG
        └── HOBBYRAUM
```

Seitlich dazu:
- Hauptpförtner
- Handlungsverzeichnis
- Fehlerregister
- Änderungs-/Erklärungsregister
- Maschinenraum
- Paul

## Flexibilitätsgrundsatz

Das Gebäude ist modular.

Neue Räume, Büros, Abteilungen und komplette Projekte können jederzeit ergänzt oder zurückgebaut werden, ohne bestehende Fachbereiche grundsätzlich umzubauen.

## Projektregel

Ein eigenständiges neues Vorhaben mit eigenem Ziel und eigener Arbeitslogik bekommt ein neues Projektgebäude.

Der Campus-Pförtner bleibt der zentrale Einstieg und routet zuerst zum Projekt, dann zum Büro.

Ein Projektgebäude ist zunächst eine **logische Einheit**.
Technisch darf es später:
- im selben Repository liegen oder
- in einem eigenen Repository liegen.

Der Campus hält nur den eindeutigen Weg dorthin fest.
Ein neues Projekt darf deshalb nicht dazu zwingen, bestehende Projektgebäude umzubauen.

## Raumregel

- neues Thema innerhalb eines bestehenden Aufgabenbereichs → vorhandenes Büro;
- neue dauerhafte Funktion → neues Büro;
- größerer dauerhafter Teilbereich → neue Abteilung;
- eigenständiges Vorhaben → neues Projektgebäude.

Keine Räume „auf Vorrat“ bauen.

## Autoritätsgrundsatz

PROJECT_MEMORY ist Wegweiser und Gedächtnis.
Es ersetzt keine bereits funktionierende technische Originalautorität.

Eine Wahrheit möglichst nur einmal pflegen.
Andere Stellen verweisen darauf.

## Pflegegrundsatz

Das Büro, das eine fachliche Änderung verursacht, pflegt auch den zugehörigen Status.

- abgeschlossener verifizierter Schritt → CURRENT_STATE aktualisieren;
- realer neuer Fehler → Fehlerregister-Verweis aktualisieren;
- wichtige Änderung/Entscheidung → Änderungsregister mit WARUM aktualisieren;
- Änderung am Gebäude selbst → Baucontainer/Änderungsregister aktualisieren.

Damit entsteht kein separates Verwaltungsbüro.

## Maschinenraum

Bestehende technische Infrastruktur bleibt bestehen.
Keine neue Gate-/Runner-/Executor-/Controller-Architektur nur wegen der Gebäudeorganisation.

## Umbauprinzip

Jeder strukturelle Umbau wird im Änderungsregister mit WARUM dokumentiert.

Unklarer Bestand:
**nicht verschieben, nicht löschen, nicht umdeuten.**
