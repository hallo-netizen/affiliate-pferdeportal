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

Fachverträge:
- `HOBBY_EIGENSCHAFTEN_SCHEMA_1_2_DELTA.md` – verbindlicher Delta-Vertrag 54 → 57;
- `HOBBYREGISTER_SCHEMA_F_V1.md` – verbindlicher Seiten-/Textvertrag für Registerprofile.

## Harte Regeln

- genau eine kanonische Hobbyidentität pro Hobby;
- Finder, Magazin, SEO-Views, Design und spätere Plugins führen **keine eigene Hobbykopie**;
- jede neue Hobbyidentität wird zuerst im zentralen Register angelegt;
- jede neue Eigenschaft wird zuerst im zentralen Eigenschaftsschema angelegt;
- Finder-/SEO-Zuordnungen sind Views/Relationen, keine neue Hobbyidentität;
- Kurzprofile gehören zum zentralen Hobbydatensatz, sind aber keine Filtereigenschaften;
- unbekannte Eigenschaft = UNKNOWN/fehlender Traitwert, niemals geratenes `false`;
- bestehende geprüfte Traitwerte werden bei Schema-Erweiterungen nicht unnötig neu klassifiziert;
- neue Klassifikationen und Kurzprofile werden im zentralen Register gespeichert;
- nach jedem Arbeitsbatch wird `CURRENT_STATE.md` mit geprüftem Zähler und nächster Aktion aktualisiert.

## Schreibweg

`Hobbyidentität → zentrale Traits → zentrales Kurzprofil → QA → Register speichern → CURRENT_STATE aktualisieren`

Kein anderer Bereich darf diesen Schreibweg durch eine eigene Hobby-Datenbank ersetzen.

## Register-Seitenweg

`kanonische Hobbyidentität → zentrale Traits + Kurzprofil → Schema F → SEO-Owner-Regel → Registerseite`

Schema F verändert die zentrale Datenwahrheit nicht.

## WordPress-Laufzeitprojektion

HD-007 `HOBBYREGISTER CORE` ist **keine zweite Datenautorität**. Es ist ausschließlich die read-only WordPress-Laufzeitprojektion des zentralen Registers.

Bestehende Bindung für 1.0.0:
- zentraler Register-SHA-256: `4deb4be2b235db450d58f02485ec40e780fc2671f9dfc6edf8cbbba0f738af78`;
- Hobbyidentitäten: 862;
- Laufzeit-API: `hd_hobbyregister_*`;
- keine Datenbankwrites, Cronjobs oder Netzwerkaufrufe.

Bei einer Änderung des zentralen Registers muss eine neue HD-007-Laufzeitprojektion explizit gegen den neuen Register-SHA erzeugt und geprüft werden. Eine stille Divergenz ist verboten.
