# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-10-05
STATUS: V1.9.8 FULL-HIERARCHY LOCAL HARD PASS / LIVE-READBACK OFFEN

## Live

Während der lokalen V1.9.8-Arbeit kein Live-Write.
V1.9.7 NICHT installieren.

## V1.9.8

Finaler lokaler Kandidat auf derselben Pluginlinie.

Gelöst:
- Full-Hierarchy Builder mit variablen 1–3 Page-Ebenen;
- keine feste Root+4-Grenze im neuen Weg;
- WordPress-native Page-Hierarchie;
- technischer unsichtbarer Page→Taxonomy-Bridge;
- echte Leaf-Terme darunter;
- wiederholbare Leaf-Namen je getrenntem Hobby;
- eigenes `journal_cat` für Magazin;
- eigenes `hp_listing_category` für HivePress;
- Delta-Erweiterbarkeit ohne Gesamtumbau;
- Publish + Frontend-Endstate-Readback;
- Idempotenz.

## Harte lokale Prüfung

- Legacy Regression 270/270 PASS;
- Full Builder PASS;
- Multi-Hobby/Flex PASS;
- kompletter POSITIV-E2E PASS;
- kompletter NEGATIV-E2E PASS;
- Fresh-Unpack gleiche Ergebnisse;
- Runtime-Parität 25/25 PASS;
- Installer PHP 19/19 PASS.

POSITIV endet bei sichtbarem Frontendzustand.
NEGATIV blockiert u. a. Parent-Fehler, unbelegte Keywords, Duplicate-Owner, stilles Entfernen, Bridge-Tamper, Parent-Drift, neue Kategorie ohne Research und Post-Approval-Mutation.

## Artefakte

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.9.8_FULL_HIERARCHY_E2E_HARD_PASS.zip`
SHA-256:
`60ea8d4c235805d66e6795223b1bfbd392cc0109556cfbf5631d9d0109b4585c`

Source:
`QUELLCODE_KATEGORIE_WORKFLOW_V1.9.8_FULL_HIERARCHY_E2E_HARD_PASS.zip`
SHA-256:
`340af0e4927971c746d97ba2aad8bab1e7efc269c70e12d21319734e7a363c10`

## Beleggrenze

Noch kein Live-PASS für V1.9.8.

## ERSTER BLOCKER

`HD001_V198_LIVE_INSTALL_AND_FRONTEND_READBACK_OPEN`

## NEXT ACTION

V1.9.8 installieren → vorhandenen Buchbinden-Stand publish/republish → realen WordPress-/Frontend-Readback prüfen.
