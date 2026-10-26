# Hobby Depot Affiliate – Porting Workbench

STATUS: PORTING / SOURCE CLEANUP PASS / AMAZON WIRED / NOT INSTALLABLE
UPDATED: 2026-10-26

## Authority and source

- Hobby Depot scope: `HOBBYRAUSCH_AFFILIATE`.
- Isolated work branch: `hobbyrausch-affiliate-current`.
- Canonical Pferdeatelier reference authority remains the committed 6.72.211 source tree on `affiliate-release-current`; it is a technical reference only, never Hobby Depot Current.
- The later user-tested Pferdeatelier 6.72.276 artifact is used only for documented generic delta comparison, never as Hobby Depot authority.

## Completed in the isolated workbench

- Provider/engine base copied without horse catalog, horse portal structure, historical horse product recovery data or horse readme.
- Horse/source-domain runtime paths removed from main plugin, automation, output-object routing, tariff examples and frontend CSS.
- Full workbench source marker check is zero for the blocked horse-domain markers used by this porting gate.
- eBay product research is bound fail-closed to the active HD-004 Hobby Depot category registry.
- idealo iPN/feed matching is bound fail-closed to the active HD-004 Hobby Depot category registry.
- Amazon Creators API adapter uses OAuth client credentials + SearchItems and is now connected to:
  - central provider access state,
  - credential save/test flow,
  - HD-004 Hobby Depot concept discovery,
  - bounded product synchronization,
  - ASIN-based product campaigns,
  - existing central campaign/output paths.
- Amazon secrets are never committed here. Non-empty wp-config constants override stored settings and are not copied back into WordPress options.
- Existing Amazon campaigns fail closed when the provider is not enabled, not credential-complete, not connection-tested or centrally paused/vetoed.

## Still open before an install candidate

1. Static/PHP syntax verification of the latest source after the Amazon wiring.
2. Positive and negative provider simulations for Amazon, eBay and idealo.
3. Real credential migration/round-trip test in a WordPress test runtime without exposing secrets.
4. Generic 6.72.276 delta reconciliation where it is portal-neutral; horse/race/banner-specific deltas stay excluded.
5. Full regression/E2E through provider → research/import → campaign → slot/output → frontend readback.
6. Only after all gates pass: manifest, SHA-256 and isolated installable `CURRENT.zip`.

## Governance note

Campus binding PR #564 exists, but its required repository gate currently fails because the trusted Campus base cannot find `control/paul-scope-gate/paul_scope_gate.py`. The security workflow is not bypassed or modified from this workbench.

Credentials, tokens and partner secrets are not stored in this document.
