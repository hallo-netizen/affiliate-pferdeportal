# HOBBY DEPOT – ZENTRALES HOBBYREGISTER

<!-- STATIC_DATA_CONTRACT_V1 -->

## Rolle

Fester Registervertrag für den **einen zentralen Hobbybestand** von Hobby Depot.

Dynamischer Status und NEXT ACTION:
`CURRENT_STATE.md`

Persistente Basisdaten:
- `/Hobby Depot/Hobby-Klassifikation/HOBBY_KLASSIFIKATIONSREGISTER_V1.json`
- `/Hobby Depot/Hobby-Klassifikation/HOBBY_EIGENSCHAFTEN_SCHEMA_V1.json`
- `/Hobby Depot/Hobby-Klassifikation/HOBBY_KURZPROFIL_SCHEMA_V1.json`

Fachverträge:
- `HOBBY_EIGENSCHAFTEN_SCHEMA_1_2_DELTA.md`
- `HOBBYREGISTER_SCHEMA_F_V1.md`

Exakte Schema-1.2-Erweiterungswerte und Audit:
- `EVIDENCE/HOBBY_SCHEMA12_VALUES_PART_01.json`
- `EVIDENCE/HOBBY_SCHEMA12_VALUES_PART_02.json`
- `EVIDENCE/HOBBY_SCHEMA12_VALUES_PART_03.json`
- `EVIDENCE/HOBBY_SCHEMA12_VALUES_PART_04.json`
- `EVIDENCE/HOBBY_SCHEMA12_FULL_862_AUDIT_20261022.json`

Diese Dateien sind **keine zweite Hobby-Datenbank**: Sie enthalten ausschließlich die drei Schema-1.2-Erweiterungswerte, keyed auf die bestehenden Registry-IDs.

## Harte Regeln

- genau eine kanonische Hobbyidentität pro Hobby;
- Finder, Magazin, SEO-Views, Design und Plugins führen keine eigene Hobbykopie;
- jede neue Hobbyidentität zuerst ins zentrale Register;
- jede neue Eigenschaft zuerst ins zentrale Eigenschaftsschema;
- UNKNOWN niemals als false oder niedrigen Wert raten;
- bestehende geprüfte Traits bei Erweiterungen nicht unnötig neu klassifizieren;
- Schema F erzeugt Darstellung/Text, keine neue Datenwahrheit.

## Datenstand

- 862 Hobbyidentitäten;
- Schema 1.2: 57 Traits;
- 862/862 mit 57/57 klassifiziert;
- 4/4 Kurzprofilfelder je Hobby;
- Voll-Audit PASS.

## Schreibweg

`Hobbyidentität → zentrale Traits → Kurzprofil → QA → Register → Schema F → SEO-Owner-Regel → Registerseite`

## WordPress-Laufzeitprojektion

HD-007 `HOBBYREGISTER CORE` bleibt read-only Projektion.
Bei einer neuen physischen Registerrevision muss HD-007 explizit gegen deren neuen Register-SHA erzeugt und geprüft werden. Stille Divergenz ist verboten.
