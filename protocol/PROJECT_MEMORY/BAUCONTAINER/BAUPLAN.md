# BAUCONTAINER – BAUPLAN

STAND: 2026-09-05
STATUS: V1
TECHNISCHER ORT: `protocol/PROJECT_MEMORY/`

## Grundmodell

```
CAMPUS
├── HAUPTPFÖRTNER
├── PROJEKTGEBÄUDE
│   └── BÜRO
│       └── HOBBYRAUM
└── PROJEKTÜBERGREIFENDES GEBÄUDE
    └── ALLGEMEINGÜLTIGE BAUSTEINE
        └── MODULREGISTER
```

Seitlich:
- Handlungsverzeichnis
- Fehlerregister
- Änderungs-/Erklärungsregister
- Maschinenraum
- Paul
- Notfall-Tresor

## Organischer Grundsatz

Der Campus ist ein wachsender Prozess, kein starres Endmodell.

Er darf:
- neue Räume;
- Büros;
- Abteilungen;
- Projektgebäude;
- projektübergreifende Module

ergänzen sowie nach dokumentierter Prüfung zusammenlegen oder zurückbauen.

Kein Gesamtneubau nur wegen neuer Erkenntnisse.
Keine Räume auf Vorrat.

## Hauptwahrheits-Regel

Für jede fachliche Wahrheit gibt es möglichst genau einen Hauptort.

Besonders bei Modulen:
- allgemeiner Modul-Kern → Hauptort bei ALLGEMEINGÜLTIGE BAUSTEINE;
- projektspezifische Nutzung → Projektbüro;
- keine doppelte vollständige Modulwahrheit.

## Modulregister

`ALLGEMEINGUELTIGE_BAUSTEINE/MODULREGISTER.md`

ist der zentrale Karteikasten für Grundmodule.

Es ist:
- kein zweites Fachbüro;
- keine technische Engine;
- kein automatischer Installer.

Es beantwortet nur:
**Was existiert bereits, wo liegt die Hauptwahrheit und darf es wiederverwendet werden?**

## Modulklasse vs. Masterakte

Diese Ebenen dürfen nie verwechselt werden.

Beispiel Bild:
- BILDZENTRALE als Modul → ALLGEMEINGÜLTIG;
- Pferde-Atelier-Masterakte → kann projektspezifische Konfiguration, Daten und Historie enthalten.

Eine gemischte Masterakte macht den Modul-Kern nicht „gemischt“.

## Projektstart / Oberwachtmeister

„Oberwachtmeister“ ist nur der Name für den Projektstart-Ablauf, kein neuer dauerhafter Agent.

Ablauf:
1. Hauptpförtner;
2. Projektanforderungen;
3. Modulregister;
4. nur passende Module;
5. minimales Projektgebäude;
6. projektspezifische Config/Nutzung.

Nicht den gesamten Campus in jedes Projekt laden.

## Masterdateien

Alle Inhalte werden vollständig inventarisiert.
Siehe:
`BAUCONTAINER/MASTERDATEIEN_REGEL.md`

Default bei unklarer Modulzuordnung:
**UNGEKLÄRT**, nicht „projektbezogen“ und nicht „allgemeingültig“.

## Technischer Ablagegrundsatz

Campus unter `protocol/PROJECT_MEMORY/`, weil bestehender `hardlock` `protocol/**` bereits abdeckt.

Keine neue CI-/Gate-Architektur dafür.

## Pflegegrundsatz

- verifizierter Fachschritt → CURRENT_STATE;
- realer Fehler → Fehlerregister;
- wichtige Änderung → Änderungsregister mit WARUM;
- Gebäudestruktur → Baucontainer;
- neues/neu bewertetes Modul → Modulregister;
- Masterakte → vollständiges Büro-Inventar.

## Notfall-Tresor

Nur geprüfter `TRESOR_PASS`-Stand ist Wiederherstellungsquelle.
Alte gültige PASS-Stände nicht überschreiben.

## Umbauprinzip

Unklarer Bestand:
**nicht verschieben, nicht löschen, nicht umdeuten.**
