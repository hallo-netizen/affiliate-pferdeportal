# Hobby Depot Affiliate – Porting Workbench

STATUS: PORTING / SOURCE CLEANUP PASS / AMAZON WIRED / STATIC PASS / PROVIDER SIM PASS / CREDENTIAL ROUNDTRIP PASS / NOT INSTALLABLE
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

## Verified gates completed in this porting branch

1. Static/PHP syntax verification after Amazon wiring: **PASS**.
   - all 23 PHP files lint clean;
   - blocked horse-domain marker gate PASS;
   - required Hobby Depot adapter gate PASS.
2. Positive/negative provider simulations: **PASS**.
   - registry binding: 6/6 PASS (Amazon/eBay/idealo: valid HD-004 + missing-registry fail-closed);
   - access/activation boundaries: 12/12 PASS;
   - total provider simulation matrix: **18/18 PASS**.

## Still open before an install candidate

1. Full regression/E2E through provider → research/import → campaign → slot/output → frontend readback.
2. Only after all gates pass: manifest, SHA-256 and isolated installable `CURRENT.zip`.

## WordPress credential round-trip

**PASS for all three target providers.**

- Amazon: real WordPress option write/read, blank resave preserves existing secret, explicit removal clears it.
- idealo: real WordPress option write/read, blank resave preserves existing API key, explicit removal clears it.
- eBay: original central `handle_provider_access_save()` executed in WordPress with admin/nonce context; blank resave preserves existing client secret and the built-in round-trip guard passes.
- Test values are synthetic and are never printed as credentials.

## 6.72.276 portal-neutral delta reconciliation

**PASS / no additional source import required.**

The three portal-neutral behaviours documented for the user-tested 6.72.276 delta are already present in the Hobby Depot workbench:
- Journal product cards use the same fixed geometry as category product cards;
- offer CTA text resolves by provider (eBay / idealo / Amazon);
- product/offer buttons use dark green `#35422A` with ochre `#C89214` hover/focus.

Horse-, race- and source-portal-specific banner/content deltas remain excluded by design.

## Governance note

Campus binding PR #564 exists, but its required repository gate currently fails because the trusted Campus base cannot find `control/paul-scope-gate/paul_scope_gate.py`. The security workflow is not bypassed or modified from this workbench.

Credentials, tokens and partner secrets are not stored in this document.
