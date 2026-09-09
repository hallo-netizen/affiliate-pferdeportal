# P42 – PLAN-SLOT -> CANONICAL BINDING

Datum: 2026-09-09
Status: TEST AKTIV

## KISS-Ziel

Keine neue Identität.
Keine neue Binding-Schicht.

Bestehende Rollen:
- extern/Handoff: plan_slot
- PPM: canonical_article_id + plan_item_key

## Zu beweisen

- plan_slot wird vor PPM eindeutig gegen genau einen Registry-Slot aufgelöst
- canonical_article_id stammt aus genau diesem gematchten Slot
- plan_slot wird vor production_plan_v4 entfernt
- PPM lehnt fremdes plan_slot-Feld ab
- keine zusätzliche Identitätskopie nötig
