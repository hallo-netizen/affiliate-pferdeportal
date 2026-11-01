# HOBBYRAUSCH – PLUGINS – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-11-01
STATUS: AKTIV / PLUGINABLAGE BLOCKED / INVENTAR- UND ROUTING-CURRENT

## Regel

Für jedes einzelne Plugin gilt ausschließlich dessen Plugin-Akte als aktuelle technische Wahrheit.

## HD-001 – Kategorie-Workflow

Plugin-Wahrheit:
`PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`

Rolle:
schwerer Bearbeitungs-/Dry-Run-/Sync-/Rollback-Workflow; künftig nicht zwingend dauerhaft aktiv.

## HD-002 – Text/SEO

Plugin-Wahrheit:
`PLUGIN_AKTEN/HD-002-TEXT-SEO/CURRENT.md`

Vor späterem Liveeinsatz muss eine direkte HD-001-Runtime-Abhängigkeit auf den neutralen Kategorie-Registry-Vertrag geprüft/umgestellt werden.

## HD-003 – Design

Plugin-Wahrheit:
`PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md`

Fach-Current:
`../DESIGN/CURRENT_STATE.md`

## HD-004 – Kategorie-Kern

Plugin-Wahrheit:
`PLUGIN_AKTEN/HD-004-KATEGORIE-KERN/CURRENT.md`

Rolle:
schlanker read-only Normalbetriebs-Kern für `journal_cat` + zentrales Kategorie-Snapshot-API.

Fach-Current:
`../SEO_KATEGORIEN/CURRENT_STATE.md`

## HD-005 – Glossar Core

Plugin-Wahrheit:
`PLUGIN_AKTEN/HD-005-GLOSSAR-CORE/CURRENT.md`

Fach-Current:
`../GLOSSAR/CURRENT_STATE.md`

## HD-006 – Bildzentrale

Plugin-Wahrheit:
`PLUGIN_AKTEN/HD-006-BILDZENTRALE/CURRENT.md`

Fach-Current:
`../BILD/CURRENT_STATE.md`

## HD-007 – Hobbyregister Core

Plugin-Wahrheit:
`PLUGIN_AKTEN/HD-007-HOBBYREGISTER-CORE/CURRENT.md`

Rolle:
schlanker read-only Laufzeitkern für das zentrale Hobbyregister und die Hobbyfinder-Lese-API; keine zweite fachliche Datenhaltung.

Fach-Current:
`../WISSENSDATENBANK/CURRENT_STATE.md`

## HD-008 – SEO-Metadaten

Plugin-Wahrheit:
`PLUGIN_AKTEN/HD-008-SEO-METADATEN/CURRENT.md`

Rolle:
schlanke automatische SEO-Titel-/Meta-Description-Ausgabe.

Fach-Current:
`../SEO/CURRENT_STATE.md`

## HD-009 – Affiliate-Zentrale

Plugin-Wahrheit:
`PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/CURRENT.md`

Rolle:
bereinigte Hobby-Depot-Portierung der Affiliate-Zentrale; technische Arbeitsquelle branchgebunden, keine Pferdeatelier-Statusübernahme.

Fach-Current:
`../AFFILIATE/CURRENT_STATE.md`


## Nachholprüfung vom 01.11.2026

Die technisch gültigen Einzelstände bleiben ausschließlich in `PLUGIN_AKTEN/<PLUGIN-ID>/CURRENT.md`. Der konkrete Nachholnachweis steht in `EVIDENCE_PLUGINABLAGE_20261101.md` und ist **keine zweite Current-Autorität**.

**Gesamtablage: BLOCKED.** In den geprüften `ISOLIERTE_PLUGINS`-Ordnern ist nur für HD-009 ein `CURRENT.zip` nachweisbar. Für HD-001, HD-003, HD-004, HD-005, HD-006, HD-007 und HD-008 (SEO-Metadaten) fehlen dort die vollständigen ZIP-Dateien; HD-002 besitzt am geprüften Zielort noch keinen isolierten Ordner. HD-008 Anzeigenfüller besitzt eine zusätzliche Akte mit ungeklärter ID-Kollision.

Bei HD-003 existiert ein Library-Dateieintrag zur **1.50.785**, jedoch konnte dessen ZIP-Inhalt am 01.11.2026 nicht erneut ausgelesen werden. **Keine Beförderung des ungeprüften ZIPs zu Campus-CURRENT, kein Live-PASS.**

## EXAKT EINE NEXT ACTION

**HD-003 1.50.785 aus einer zulässigen Rohdateiquelle unabhängig wiederöffnen und bytegenau prüfen.** Erst bei echtem ZIP-/Versions-/Hash-PASS darf die vollständige ZIP über den vorgesehenen Campus-Prüfweg als `ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip` übernommen werden. Weitere Plugin-ZIPs danach nach ihren einzelnen Akten abgleichen; niemals alte Versionen als Ersatz verwenden.
