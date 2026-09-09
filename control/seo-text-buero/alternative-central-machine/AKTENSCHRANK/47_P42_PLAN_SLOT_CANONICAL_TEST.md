# P42 – PLAN-SLOT -> CANONICAL BINDING

Datum: 2026-09-09
Status: ABGESCHLOSSEN – PASS

## Ergebnis

Vorhandene Rollen bleiben getrennt:
- extern/Handoff: `plan_slot`
- PPM: `canonical_article_id` + `plan_item_key`

Bewiesen:
- plan_slot wird vor PPM eindeutig gegen Registry-Slot aufgelöst
- canonical_article_id stammt aus dem gematchten Slot
- plan_slot wird nicht als fremdes PPM-Planfeld weitergereicht
- keine zusätzliche Identitätskopie nötig

Die vollständige Fail-closed-Bindung wurde in P43 abgeschlossen.
