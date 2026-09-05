# BAUCONTAINER – BAUPLAN

STAND: 2026-09-05
STATUS: V1

## Grundmodell

```
CAMPUS
├── HAUPTPFÖRTNER
├── PROJEKTGEBÄUDE
│   └── BÜRO
│       └── HOBBYRAUM
└── ALLGEMEINGÜLTIGE BAUSTEINE
    └── MODULREGISTER
```

Seitlich:
- Handlungsverzeichnis
- WordPress-Register (Technologieindex, keine zweite Wahrheit)
- Fehlerregister
- Änderungs-/Erklärungsregister
- Zielverträge
- Archiv
- Baucontainer
- Hausmeister
- Maschinenraum
- Paul
- Notfall-Tresor

## Campus-Haupteingang

`../START_HERE.md` → `../HAUPTPFOERTNER.md`

Alltagssprache ist zulässig; Routing bleibt trotzdem deterministisch.

## Verbindlicher Eingangsstandard

Siehe:
`EINGANGSSTANDARD.md`

Campus-, Gebäude-, Büro- und Paul-Eingänge müssen oben sofort erklären:
**Was ist das? Wo bin ich richtig? Was darf ich? Was darf ich nicht? Wo geht es weiter?**

Grundsatz:
**Ein Klick = alles klar.**

## Verwaltungsrollen – harte Grenze

### Hauptpförtner
Nur:
- lesen;
- orientieren;
- routen;
- Stand zurückmelden.

Nie:
- Fachinhalt ändern;
- Architektur ändern;
- technische Arbeit ausführen.

### Hausmeister
Nur:
- unveränderte historische Akten ordnen/verschieben;
- Archiv-/Hausmeister-Indizes pflegen;
- Hashes/Dubletten dokumentieren;
- Aufräumbedarf melden.

Nie:
- Fachinhalte editieren;
- CURRENT_STATE/START_HERE/HOBBYRAUM umschreiben;
- Status fachlich neu bewerten;
- reparieren;
- löschen.

## Rollentrennung

Ein Chat darf mehrere Rollen nacheinander haben.

Aber:
**Rolle bestimmt Rechte.**

Beispiel:
Pförtner liest/routet → Pförtnerrolle endet → erst danach beginnt Facharbeit.

Architekturänderung:
Pförtner-/Hausmeisterrolle verlassen → ausdrücklich Baucontainer-Rolle → Bauprotokoll + Änderungsregister.

## Organischer Grundsatz

Der Campus ist ein wachsender Prozess.

Jeder Chat darf bei echtem Arbeitsbedarf die Architektur verbessern, aber nur in der Baucontainer-Rolle und mit KISS/Protokollpflicht.

Keine Räume auf Vorrat.

## Architektur beobachtet sich selbst

- `BAUPLAN.md` → aktuelle Architektur
- `BAUAENDERUNGEN.md` → dauerhafte Umbauten
- `BAUPROTOKOLL.md` → chronologisches Baugeschehen
- `ENTWICKLUNGSPROTOKOLL.md` → Ideen, Einwände, verworfene Varianten und offene Architekturgedanken
- `ARCHITEKTUR_FEHLERKISTE.md` → Architekturfehler
- `HAUSMEISTER.md` → reine Ordnungsverwaltung
- `EINGANGSSTANDARD.md` → 1-Klick-Orientierung
- `HOBBYRAUM_STANDARD.md` → ein Arbeitsraum pro Büro / FREI-AKTIV-BLOCKED
- `BAUABNAHME_20260905.md` → letzter harter Abnahmebeleg

## Hauptwahrheit

Für jede Wahrheit möglichst ein Hauptort.

Allgemeiner Modul-Kern:
ALLGEMEINGÜLTIGE BAUSTEINE.

Projektbezogene Nutzung:
Projektbüro.

## WordPress-Register

`WORDPRESS_REGISTER.md` ist ein campusweiter Technologieindex.

Es zeigt:
- vorhandene Plugin-/Installer-Artefakte;
- Dateibelege/Versionen;
- zuständige Hauptquelle.

Es entscheidet NICHT:
- Modulklasse;
- LIVE-/Release-Status;
- Fachwahrheit.

Damit bleibt es ein Wegweiser und erzeugt keine zweite Wahrheit.

## Projektstart

Hauptpförtner → Ziel/Anforderungen → Modulregister → passende Module → minimales Projektgebäude.

Neue Projektgebäude zusätzlich:
- `NEUES_PROJEKT_VORLAGE.md`;
- jedes neue Verzeichnis mit `START_HERE.md`;
- jedes Büro mit CURRENT_STATE + genau einem HOBBYRAUM;
- Arbeitsleitungen zu Handlungs-/Fehler-/Änderungs-/Zielregister;
- abschließende Positiv-/Negativ-Bauabnahme.

## Masterdateien

Alles vollständig inventarisieren.
Default bei unklarer Modulzuordnung:
**UNGEKLÄRT.**

## Zugriffsschutz

Campus-Prototyp aktuell unter `protocol/PROJECT_MEMORY/`.

Offene Empfehlung:
später eigener privater Campus-Repository.

## Notfall-Tresor

Eingang:
`../TRESOR/START_HERE.md`

Aktueller Status:
`../TRESOR/STATUS.md`

Nur geprüfter `TRESOR_PASS`-Stand ist Wiederherstellungsquelle.

## Umbauprinzip

Unklarer Bestand:
**nicht verschieben, nicht löschen, nicht umdeuten.**
