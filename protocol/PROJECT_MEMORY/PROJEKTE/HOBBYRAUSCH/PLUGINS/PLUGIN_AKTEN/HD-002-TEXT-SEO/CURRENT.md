# HD-002 – HOBBY DEPOT SEO THEMENENGINE – CURRENT

STAND: 2026-10-01
STATUS: V0.1.2 LIVE BLOCKED HDTE_CONTEXT_STAGE_PLAN_HASH_MISSING / V0.1.3 COMPLETE-WORKFLOW POSITIV+NEGATIV HARD PASS / LIVE-UPGRADE NÄCHSTES

## Harte Abnahmeregel

**Keine Abnahme mehr über Teiltests.**
Für diesen Workflow muss der komplette reale Pfad lokal positiv UND negativ simuliert sein:
deployed HD-001 Owner-Handoff → HDTE Auto-Sync → Baseline → request-begrenzter Portalabgleich → finale Freshness-Gates → COMPLETE.

## Live-Stand

Installiert live:
`Hobby Depot SEO Themenengine 0.1.2`

Owner-Handoff wurde erfolgreich automatisch übernommen und der Gesamtbestand erfasst.

Live danach:
`Portalabgleich läuft automatisch request-begrenzt weiter. BLOCKED · HDTE_CONTEXT_STAGE_PLAN_HASH_MISSING`

Der Block liegt in:
`STAGE_EDITORIAL_PLAN_SNAPSHOT`.

## Root Cause

Ohne importierten Redaktionsplan liefert der bestehende HDTE-Vertrag absichtlich:

- contract: `HDTE_EDITORIAL_PLAN_SNAPSHOT_V1`
- status: `NOT_AVAILABLE`
- sha256: `NOT_AVAILABLE`
- items: leer.

V0.1.2 behandelte den gültigen Sentinel `NOT_AVAILABLE` fälschlich wie einen fehlenden 64-Hex-Hash und blockierte deshalb.

## Fix V0.1.3

Plugin:
`Hobby Depot SEO Themenengine 0.1.3`

Installer:
`HOBBY_DEPOT_SEO_THEMENENGINE_V0.1.3_PORTALABGLEICH_FULL_WORKFLOW_HARD_PASS.zip`

Installer SHA-256:
`5b3063577beb3e5dfb03799b6245f2b9aaf90f338c70e86708674e5999762b2a`

Source:
`QUELLCODE_HDTE_V0.1.3_PORTALABGLEICH_FULL_WORKFLOW_HARD_PASS.zip`

V0.1.3 akzeptiert einen nicht vorhandenen Redaktionsplan ausschließlich wenn:
- Contract korrekt;
- status exakt `NOT_AVAILABLE`;
- sha256 exakt `NOT_AVAILABLE`;
- Baseline ebenfalls exakt `NOT_AVAILABLE`;
- items exakt leer.

Alle abweichenden/malformed Zustände bleiben fail-closed.

Zusätzlich kann exakt der bereits live vorhandene V8-Job
`BLOCKED / STAGE_EDITORIAL_PLAN_SNAPSHOT / HDTE_CONTEXT_STAGE_PLAN_HASH_MISSING`
in-place weitergeführt werden.
Kein neuer Gesamtbestand und kein neuer Owner-Handoff nötig.

## Komplette lokale Positivsimulation

### Exakter Livezustand
- HD-001 deployed;
- 7 Owner;
- 11 ARTICLE_ONLY / 11 gebunden;
- 4 nutzbare Content-Kategorien;
- 1 Buchbinden-Themenfamilie;
- 0 aktuelle Themen im Portalabgleich;
- kein Redaktionsplan.

Fresh Installer V0.1.3:
Owner-Sync → Baseline → Inventory Stage → Plan Stage → Registry Stage → Sandbox Store → Sandbox IDs → Context Index → Final Structure → Final Inventory → Final Editorial Plan → **COMPLETE**.

### Echter Upgrade-/Resume-Fall
Jeder Schritt in eigenem PHP-Prozess/Request:

V0.1.2:
`BLOCKED / STAGE_EDITORIAL_PLAN_SNAPSHOT / HDTE_CONTEXT_STAGE_PLAN_HASH_MISSING`.

Danach gleiche persistierte Job-/Option-Daten unter frisch entpackter V0.1.3:
ohne neue Baseline, ohne neuen Handoff:
→ Stage Plan
→ Registry
→ Sandbox
→ Context Index
→ Final Structure
→ Final Inventory
→ Final Plan
→ **COMPLETE**.

### Nichtleerer Stresslauf
4 Themen einschließlich Payload-Audit + Portal-Context-Batch:
4/4 verarbeitet → **COMPLETE**.

### Redaktionsplan vorhanden
Normal hash-gebundener vorhandener Plan:
→ **COMPLETE**.

## Negative Volltests

Frisch entpackter Installer:
- HD-001 nicht deployed → `HDTE_UPSTREAM_CATEGORY_WORKFLOW_NOT_DEPLOYED`;
- NOT_AVAILABLE mit nichtleeren Items → `HDTE_CONTEXT_STAGE_PLAN_NOT_AVAILABLE_ITEMS_PRESENT`;
- verfügbarer Plan ohne Hash → `HDTE_CONTEXT_STAGE_PLAN_HASH_MISSING`;
- staged Plan nach Write manipuliert → Stage-Readback/Length-Mismatch BLOCKED;
- Live-Struktur vor Abschluss verändert → `HDTE_CONTEXT_REFRESH_STALE_FINAL_STRUCTURE`.

Admin-Reentry:
exakter aktuelle BLOCKED-Job wird als `CURRENT_PLAN_ABSENCE_REENTRY_PENDING` erkannt und an den vorhandenen automatischen AJAX-Worker weitergereicht.

## Paketprüfung

- PHP Source: 80/80 PASS;
- PHP Fresh Installer: 80/80 PASS;
- Source ↔ Fresh Installer: 135/135 Dateien byteidentisch;
- geändert ggü. 0.1.2: exakt 4 Dateien:
  - Hauptplugin/Version;
  - Admin-Reentry;
  - Context-Index Sentinel-Validierung;
  - Context-Refresh In-place-Recovery.
- Repository, Research Archive, Sandbox Record Store, Storage Maintenance, Safe Migration und Owner-Handoff bleiben byteidentisch.

Evidence:
`HDTE_V0.1.3_FULL_WORKFLOW_POS_NEG_EVIDENCE.txt`

## NEXT ACTION

V0.1.3 über V0.1.2 installieren.

Danach nur:
`Hobby Depot Themenengine → Übersicht`

Der vorhandene BLOCKED-Portalabgleich wird automatisch request-begrenzt weitergeführt.
Keine neue Bestandserfassung.
Kein neuer Owner-Handoff.
Kein neuer Research-Lauf.

Erst bei sichtbarem `Portalabgleich COMPLETE` live abnehmen.
