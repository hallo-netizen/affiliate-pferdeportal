# HOBBY DEPOT – ZENTRALES HOBBYREGISTER

<!-- STATIC_DATA_CONTRACT_V1 -->

## Rolle

Dies ist der feste Registervertrag für den **einen zentralen Hobbybestand** von Hobby Depot.

Er ist **keine zweite Current-Autorität** und enthält bewusst keine kopierte dynamische Hobbyliste.

Dynamischer Status, offene Arbeit und NEXT ACTION:
`CURRENT_STATE.md`

Persistente zentrale Daten:
- `/Hobby Depot/Hobby-Klassifikation/HOBBY_KLASSIFIKATIONSREGISTER_V1.json`
- `/Hobby Depot/Hobby-Klassifikation/HOBBY_EIGENSCHAFTEN_SCHEMA_V1.json`
- `/Hobby Depot/Hobby-Klassifikation/HOBBY_KURZPROFIL_SCHEMA_V1.json`

## Harte Regeln

- genau eine kanonische Hobbyidentität pro Hobby;
- Finder, Magazin, SEO-Views, Design und spätere Plugins führen **keine eigene Hobbykopie**;
- jede neue Hobbyidentität wird zuerst im zentralen Register angelegt;
- jede neue Eigenschaft wird zuerst im zentralen Eigenschaftsschema angelegt;
- Finder-/SEO-Zuordnungen sind Views/Relationen, keine neue Hobbyidentität;
- Kurzprofile gehören zum zentralen Hobbydatensatz, sind aber keine Filtereigenschaften;
- unbekannte Eigenschaft = UNKNOWN/fehlender Traitwert, niemals geratenes `false`;
- neue Klassifikationen und Kurzprofile werden im zentralen Register gespeichert;
- nach jedem Arbeitsbatch wird `CURRENT_STATE.md` mit geprüftem Zähler und nächster Aktion aktualisiert.

## Schreibweg

`Hobbyidentität → zentrale Traits → zentrales Kurzprofil → QA → Register speichern → CURRENT_STATE aktualisieren`

Kein anderer Bereich darf diesen Schreibweg durch eine eigene Hobby-Datenbank ersetzen.
