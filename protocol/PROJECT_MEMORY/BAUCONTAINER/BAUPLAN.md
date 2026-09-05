# BAUCONTAINER – BAUPLAN

STAND: 2026-09-05
STATUS: V1
TECHNISCHER ORT: `protocol/PROJECT_MEMORY/`

## Grundmodell

```
CAMPUS
├── PROJEKTGEBÄUDE
│   └── BÜRO / ABTEILUNG
│       └── HOBBYRAUM
└── PROJEKTÜBERGREIFENDE GEBÄUDE
    └── ALLGEMEINGÜLTIGE BAUSTEINE
```

Seitlich dazu:
- Hauptpförtner
- Handlungsverzeichnis
- Fehlerregister
- Änderungs-/Erklärungsregister
- Maschinenraum
- Paul
- Notfall-Tresor

## Organischer Flexibilitätsgrundsatz

Der Campus ist kein fertiges starres Schema, sondern ein wachsender Prozess.

Neue Erkenntnisse dürfen jederzeit:
- Räume ergänzen;
- Büros ergänzen;
- Abteilungen ergänzen;
- Projektgebäude ergänzen;
- projektübergreifende Gebäude ergänzen;
- bestehende Räume zusammenlegen;
- überholte Räume nach dokumentierter Prüfung zurückbauen.

Dabei darf nicht der gesamte Campus neu gebaut werden müssen.

Struktur folgt realem Bedarf.
Keine Räume auf Vorrat.

## Projektregel

Ein eigenständiges neues Vorhaben mit eigenem Ziel und eigener Arbeitslogik bekommt ein neues Projektgebäude.

Der Hauptpförtner routet zuerst zum Projekt, dann zum Büro.

Ein Projektgebäude ist eine logische Einheit und kann technisch im selben oder in einem eigenen Repository liegen.

## Neues Projekt / Oberwachtmeister

Bei einem neuen Projekt:

1. Hauptpförtner lesen;
2. neues Projektgebäude bestimmen/anlegen;
3. Anforderungen feststellen;
4. `ALLGEMEINGUELTIGE_BAUSTEINE/` prüfen;
5. geeignete geprüfte Bausteine übernehmen;
6. nur projektspezifische Anpassungen im neuen Projekt vornehmen.

Nicht blind das Pferde-Atelier kopieren.
Nicht vorhandene allgemeine Lösungen neu erfinden.

## Masterdateien-Grundsatz

Für alle eingehenden Masterdateien gilt:
`BAUCONTAINER/MASTERDATEIEN_REGEL.md`

Alles enthaltene Material wird inventarisiert und zugeordnet.
Nichts wird still verworfen.

## Technischer Ablagegrundsatz

Der Campus liegt aktuell unter `protocol/PROJECT_MEMORY/`.

Grund:
Der bestehende `hardlock`-Workflow überwacht Pull Requests mit Änderungen unter `protocol/**` bereits automatisch.
Damit nutzt die Gebäudeordnung vorhandene CI statt neue Workflow-/Gate-Architektur zu bauen.

## Autoritätsgrundsatz

PROJECT_MEMORY ist Wegweiser und Gedächtnis.
Es ersetzt keine bereits funktionierende technische Originalautorität.

Eine Wahrheit möglichst nur einmal pflegen.
Andere Stellen verweisen darauf.

## Pflegegrundsatz

Das Büro, das eine fachliche Änderung verursacht, pflegt auch den zugehörigen Status.

- abgeschlossener verifizierter Schritt → CURRENT_STATE;
- realer neuer Fehler → Fehlerregister;
- wichtige Änderung/Entscheidung → Änderungsregister mit WARUM;
- Gebäudeänderung → Baucontainer/Änderungsregister;
- neue Masterakte → vollständiges Büro-Inventar.

## Notfall-Tresor

Der Tresor liegt logisch außerhalb des aktiven Campus.
Er steuert keine Facharbeit.
Er enthält die vollständige Wiederherstellungsgrundlage des Campus.

Nur `TRESOR_PASS` ist Wiederherstellungsquelle.
Ältere gültige Tresorstände werden niemals überschrieben.

Konzept:
`protocol/PROJECT_MEMORY/TRESOR/`

## Maschinenraum

Bestehende technische Infrastruktur bleibt bestehen.
Keine neue Gate-/Runner-/Executor-/Controller-Architektur nur wegen der Gebäudeorganisation.

## Umbauprinzip

Jeder strukturelle Umbau wird mit WARUM dokumentiert.

Unklarer Bestand:
**nicht verschieben, nicht löschen, nicht umdeuten.**
