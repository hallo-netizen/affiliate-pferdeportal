# P24 – EDITORIAL-PLAN-RUNTIME-GATE / SYSTEMWEITE DUBLETTEN

Datum: 2026-09-08
Status: GO

## Exakter Pfad

Der reale Normal-Draft-Pfad ruft vor Generierung/Write:

`PPM679_Editorial_Plan_Runtime_Gate::preflight`

Dieser ruft fest:
- `PPM679_Editorial_Plan_Registry::validate`
- `PPM679_Production_Wave_Governor::validate`
- `PPM679_Content_Inventory_Reconciler::runtime_inventory`
- `PPM679_Content_Inventory_Reconciler::reconcile`
- `PPM679_Systemwide_Duplicate_Guard::preflight`
- read-only Journal-Snapshot

## Bereits intern erzwungen

### Systemweite Dubletten/Kannibalisierung
`PPM679_Systemwide_Duplicate_Guard` bindet und prüft:
- normalisierten Titel
- canonical_article_id
- keyword_ownership_key
- bestehendes WordPress-Inventar
- Batch-interne Titel-/Ownership-Dubletten

Blocker u.a.:
`BLOCKED_BATCH_DUPLICATE_INTENT`

Regel:
`ONE_BATCH_MUST_NOT_CONTAIN_DUPLICATE_TITLE_OR_KEYWORD_OWNERSHIP`

Hard-Rule-Register:
`Duplicates and keyword ownership collisions across portal, journal and all WordPress statuses must block.`

### WordPress-Inventar
Read-only:
- publish
- draft
- trash

Kein Write in dieser Vorprüfung.

### Kanonischer Redaktionsplan
Bereits geprüft:
- vollständige Portalquelle
- eindeutige Slugs/stable IDs
- eindeutige canonical_article_id
- vollständige Planpositionen
- feste Kategorie-Slot-Regeln
- Reconciliation mit vorhandenem WordPress-Bestand
- publish_allowed=false

## Originaltests

PASS:
- PASS_V38_EDITORIAL_PLAN_JOURNAL_SYSTEMWIDE_DEDUP
- PASS_V38_EDITORIAL_PLAN_NEGATIVE_CONTROLS
- PASS_NORMAL_DRAFT_IDENTITY_REPLAY_NEGATIVE
- PASS_NORMAL_DRAFT_CARDINALITY_TYPES_NEGATIVE

Negativ u.a. bewiesen:
- Publish/Draft/Trash-Dubletten blockieren
- Batch-Dubletten blockieren
- falsche/zu große Startwelle blockiert
- Replay/Identitätsabweichung blockiert

## KISS-Folgerung

Kein neues externes Duplicate-/Cannibalization-Gate.

Dieser Pflichtbereich bleibt im vorhandenen unveränderten:
`Editorial_Plan_Runtime_Gate -> Systemwide_Duplicate_Guard`

## SEO-Abgrenzung

Keyword-Ownership ist damit bewiesen.

Noch separat zu beweisen:
die vorhandene Hard Rule
`TITLE_MUST_CONTAIN_TARGET_KEYWORD`

Dafür P25.

Keine neue SEO-Logik bauen.
Nur vorhandene Runtime-Verankerung beweisen.

## Regression

Im selben Lauf P0 bis P24 vollständig PASS.
