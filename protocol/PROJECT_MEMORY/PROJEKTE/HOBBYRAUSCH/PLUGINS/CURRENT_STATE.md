# HOBBYRAUSCH – PLUGINS – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-22
STATUS: AKTIV / INVENTAR- UND ROUTING-CURRENT / KEINE KOPIE VON EINZELPLUGIN-STATUS

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

## EXAKT EINE NEXT ACTION

Für die Kategorie-Verschlankung:
`../SEO_KATEGORIEN/CURRENT_STATE.md` → dortige NEXT ACTION.
