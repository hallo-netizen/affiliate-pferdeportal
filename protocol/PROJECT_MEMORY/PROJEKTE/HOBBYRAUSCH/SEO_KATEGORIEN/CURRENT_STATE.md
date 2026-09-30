# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-30
STATUS: BUCHBINDEN RESEARCH COMPLETE / V1.9.1 LIVE DEPLOY-READBACK FEHLER REPRODUZIERT / V1.9.2 HARD PASS / LIVE-RETEST NÄCHSTES

## Harte Abnahmeregel

**Keine Datei, kein Pluginstand und kein Produktionsschritt gilt als abnahmefähig ohne dokumentierte lokale Positiv- UND Negativsimulation.**

## Live-Befund

Der Buchbinden-READ_ONLY_PREVIEW lief bis zum echten Deployment.

Live:
`Readback fehlgeschlagen: DEPLOY_READBACK_MISMATCH | Automatischer Rollback: PASS`

Damit wurde nichts als erfolgreich abgenommen; Rollback hat den Vorzustand wiederhergestellt.

## Root Cause

V1.9.1:
Exact-Slug-Zielobjekt mit richtigem Namen, aber falschem nativen Parent → `ADOPT_EXISTING` trotz `changed_fields:[parent]` → Parent nicht geschrieben → Readback-Mismatch.

## Fix

Aktuell:
`Affiliate-Portal Kategorie-Workflow V1.9.2`

SHA-256:
`8d462ee585ee0921772c0deb56b9829b7e7819a618dfdfc441e06bd3afa79ff8`

Positiv:
- exakter reproduzierter Fehlerfall → UPDATE → DEPLOYED_AND_READBACK_PASS;
- Taxonomy + Page Parent-Korrektur PASS;
- Rollback-Restore PASS;
- Fresh-Unpack 251/251 PASS.

Negativ/fail-closed:
- V1.9.1 Regression erzeugt exakt DEPLOY_READBACK_MISMATCH + Rollback PASS;
- Slug-Konflikt mit anderem Namen bleibt BLOCKED;
- andere concept_id-Bindung bleibt BLOCKED;
- stale/manipulierter Plan bleibt BLOCKED.

## Produktionsdatei

Weiterhin derselbe fachlich geprüfte:
`HOBBY_DEPOT_BUCHBINDEN_READ_ONLY_PREVIEW_V1.json`

Kein neuer Research-Lauf erforderlich.

## NEXT ACTION

1. V1.9.2 installieren.
2. denselben READ_ONLY_PREVIEW über `Arbeitsstand übernehmen` erneut laden, damit der alte V1.9.1-Dry-Run verworfen wird;
3. `Finale Struktur freigeben`;
4. `WordPress-Vorschau erstellen`;
5. neuen geprüften Plan anwenden.

Nur bei erneutem BLOCKED/Fehler stoppen.
