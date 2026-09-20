# AFFILIATE-ZENTRALE — 6.72.123 TIMEOUT / RECOVERY-HANDOFF — 2026-09-20

Role: incident protocol + handoff evidence. **Not CURRENT authority.**
Current/status/NEXT ACTION remain exclusively in `control/release-governance/CURRENT_RELEASE.json`.

## 1. Binding target contract

Restore the Affiliate-Zentrale as one complete system, not as a chain of microfixes.

For category product output the bound workflow is:

`persisted WordPress state -> provider/campaign eligibility -> target/category binding -> category_product_1..3 -> eBay/idealo selection -> render_affiliate_slot -> final product-card HTML -> template real-content acceptance -> visible category output`.

Hard rule:
- **both parts are mandatory:** plugin code **and** persisted WordPress state;
- every repair must be checked against the **complete bound workflow**, positive and negative;
- a downgrade/reinstall of PHP files alone is not a state restoration;
- no PASS from mocks/synthetic state alone;
- no new feature work;
- protected Journal/Glossar/Pferderassen paths remain regression hardlocks;
- no more installer/version cascade while the first real failure is open.

## 2. Exact current live status

User live readback after installation of non-canonical local artifact **6.72.123**:
- **FRONTEND: timeout / not reachable**
- **BACKEND (/wp-admin): not reachable**
- therefore no WordPress-admin read-only capture is currently possible.

Failed artifact:
- filename: `AFFILIATE_ZENTRALE_V6.72.123_CATEGORY_PRODUCT_STRUCTURE_RESTORE_FULLSYSTEM_HARDTEST.zip`
- SHA-256: `c71d8fb8fc03751b0377b525e7d2b7c791ee424d7b219c3d042a41b20de7aa44`
- status: **LIVE FAIL / DO NOT REINSTALL / DO NOT PROMOTE**

Immediate causal fact that is proven:
- the site became unreachable after 6.72.123 was installed/activated.

Not proven:
- the exact internal timeout mechanism (loop, query, hook, cron, state migration, etc.) is **not yet proven** and must not be guessed while WordPress is unreachable.

## 3. Proven structural cause of the earlier recovery failures

The 6.72.109–117 line changed **persisted WordPress state**, not only PHP code. Therefore old plugin ZIPs could not recreate the earlier operational state by file replacement alone.

Already proven persistent writes include:
- 6.72.109: `ppar_banner_placement_plan_v2`;
- 6.72.110 ff.: analytics/bootstrap/cache/scheduled state;
- 6.72.114: Awin `_destination_*` / `destination_url` state;
- 6.72.115: `ppar_network_idealo_v1.output_mode=automatic`, activation sync, marker `ppar_multiprovider_category_repair_v672115`, article-plan revision/rebuild effects;
- 6.72.116: article-plan revision/rebuild/log/cron recovery mutations;
- 6.72.117: `output_mode=idealo_only`, activation resync, rebuild;
- 6.72.118-A/B: mutually incompatible recovery behavior; both blocked.

This explains why code downgrade alone repeatedly failed. It does **not** prove the internal cause of the new 6.72.123 timeout.

## 4. Complete attempt/error protocol

### Last broadly proven operational base
- **6.72.108**: last broadly proven working operational base.
- ZIP SHA-256: `d8aeb69bd67a18072996da9ca8101923e6ff6765a40c5d0d6a6f74bde3be5bb3`.
- Local historical gates: Partner/Cleos/Awin 25/25 PASS; Awin transport 21/21 PASS; regression 82/82 PASS; PHP 21/21 PASS; Fresh-Unpack 26/26.
- Canonical repo source nevertheless remained 6.72.105; source drift is still open but secondary to emergency recovery.

### 6.72.109–118 incident line
- **6.72.109**: introduced persisted dynamic banner placement; no total-system replacement authority.
- **6.72.110–113**: subsequent local/live rootfix attempts; no authoritative total-system LIVE PASS that supersedes 6.72.108.
- **6.72.114**: category/product work plus persisted Awin destination state; live category output degraded to one visible product.
- **6.72.115**: multiprovider/idealo state changes plus article-plan revision/rebuild; user reported category products disappeared.
- **6.72.116**: recovery attempt did not restore visible products.
- **6.72.117**: forced `idealo_only`; generic product placeholders/direct-ad fallback visible.
- **6.72.118-A/B**: two different artifacts with same version; contradictory marker/recovery logic; no LIVE PASS; both forbidden.

### Recovery attempts in this chat
- **6.72.119** — exact 6.72.108 code base + targeted recovery; local tests PASS; **LIVE: no visible change**. Root mistake: code/state recovery scope did not match the actual live state.
- **6.72.120** — category-only candidate; **not accepted as a reliable live recovery**; must not be used as evidence or promoted.
- **6.72.121** — attempted real category runtime repair; local synthetic E2E PASS; **LIVE: all three Productvorschau placeholders remained**.
- **6.72.122** — historical/category E2E candidate; local synthetic E2E PASS; **LIVE: all three Productvorschau placeholders remained**.
- **6.72.123** — attempted combined code + persisted-state structure restore; local simulated damaged-state workflow reported PASS; **LIVE CRITICAL FAIL: frontend timeout and wp-admin unreachable**.

Process/test failure learned from 119–123:
- local harnesses reconstructed/simulated a presumed damaged state instead of first proving the exact live state;
- PASS therefore did not establish restoration of the real WordPress instance;
- local E2E must not be called system PASS unless it starts from a read-only captured live-state fixture or a hash-bound exact equivalent.

## 5. Productvorschau diagnostic fact

The visible `Produktvorschau` cards are generated by Pferde-Template-Kit V1.50.308+ as an admin fallback when `category_product_1..3` do not return content accepted as real. They are a symptom/diagnostic surface, not the root cause of eBay/idealo failure.

## 6. Exact entry for the next chat

1. Repository: `hallo-netizen/affiliate-pferdeportal`
2. Branch: `affiliate-release-current`
3. Bürotür: `release/affiliate-zentrale/AGENTS.md`
4. **Single Current authority:** `control/release-governance/CURRENT_RELEASE.json`
5. Freshness check: branch head + Current blob + `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt`
6. First blocker: **AFF-ERR-039 — emergency live recovery; 6.72.123 timeout**
7. This protocol is evidence/handoff only, never CURRENT.

## 7. Exact NEXT ACTION

Because both frontend and backend are unreachable, the first action is **not** another plugin build and **not** another WordPress-admin test.

**Outside WordPress admin, disable the active `affiliate-portal-router` plugin directory so WordPress can boot without 6.72.123. Do not install or activate any other Affiliate ZIP.**

Completion condition for this one action:
- `/wp-admin/` loads again; and
- one public frontend page loads again.

After that completion, stop. The next bound phase is a **read-only capture of the complete live Affiliate state before any reactivation/install**, then comparison against the last safe operational contract. No repair plugin is authorized before that capture.

## 8. Do not touch

- Do not install 6.72.118, 119, 120, 121, 122 or 123 again.
- Do not promote any of them to PPA-001 CURRENT.zip.
- Do not change Journal/Glossar/Pferderassen while recovering category products.
- Do not infer timeout root cause from local code alone.
- Do not run state-changing recovery while WordPress reachability is not restored.
- Do not create another version merely to inspect state.

