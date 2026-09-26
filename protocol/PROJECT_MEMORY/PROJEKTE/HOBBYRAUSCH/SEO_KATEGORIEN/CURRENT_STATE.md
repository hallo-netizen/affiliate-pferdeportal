# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-26
STATUS: KATEGORIE-WORKFLOW GEBUNDEN / INSTALLATION NOCH BLOCKED

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_SEO_KATEGORIEN`.

## Aktueller belastbarer Stand

Der vorhandene allgemeingültige Kategorie-Workflow wurde als Basis für Hobby Depot gebunden.

Belegte Basis:
- MASTER 016 R10/R9 Runtime Deployment
- Plugin V1.8.0
- Content → WordPress `category`
- Marketplace/HivePress → `hp_listing_category`
- Journal nur auf explizit gebundener Taxonomie
- DataForSEO-Research
- SEO-/Intent-/Kannibalisierungsprüfungen
- Dry-Run → Apply → Readback
- kein Auto-Delete / keine stillen Remaps

Projektinput liegt unter:
`../KONZEPT/VORARBEITEN_HOBBYFINDER/`

Technischer Audit:
`KATEGORIE_WORKFLOW_AUDIT_20260926.md`

Keine Pferde-Atelier-Fachkategorien oder Pferde-Reparaturdaten werden übernommen.
Die spätere 1.8.1-Pferde-Testkette ist nicht die Hobby-Depot-Basis.

## Erster offener Blocker

Die exakt hashgebundenen vollständigen V1.8.0-Installer-/Source-Bytes sind aus den aktuell erreichbaren Quellen noch nicht wieder gebunden.

Ein realer GitHub-Entpacktest hat bestätigt:
Der im technischen Branch erreichbare Root-Master enthält den V1.8.0-Installer NICHT und darf nicht als Ersatzbasis verwendet werden.

## NEXT ACTION

Exakten V1.8.0-Installer oder Source anhand der bekannten SHA-256 wiederbinden; danach vollständiger Projektbindungs-Scan + Regression und erst dann Installation auf Hobby Depot.
