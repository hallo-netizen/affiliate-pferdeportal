# AFF-ERR-065: Original banner placement and public WordPress replay

Date 2026-10-13. Source manifest SHA256: f11687daa1f11d8ff98a3c0d62a720dac170dd95edddf39eba04530e858c44cf
Status: PARTIAL REGRESSION PASS; live 6.72.224 / 6.72.226 installed source and current provider rows remain unverified. NO RELEASE.

Actual 2026-10-12 original user read-only live diagnostic, article #972638:
- affiliate version 6.72.224; Template 1.50.612; 2349 campaigns, 13 banners passing mandatory eligibility
- exactly ZERO banners explicitly placed post_inline_banner
- selected_mandatory_fallback_banner_id=972835, named procavallo, 728x90, placement product_after_category_tiles ONLY
- stored plan status=no_output, first banner none, second banner none, products none, plan current=false
- eBay and idealo ranked product counts both zero, idealo feed age 499.2h
Do not interpret the 13 eligible as 13 valid topic/placed inline candidates; mandatory fallback explicitly bypasses placement but retains all safety/geometry/health gates.

Existing local WordPress/MariaDB test (no new workflow, no source or DB migration):
- Run 38386165447: original stale saved no_output + originally valid normal article banner -> preexisting rebuild PASS.
- Run 38386669511: test campaign has placement product_after_category_tiles ONLY (same as live 972835); both actual article-placed campaigns deactivated. preexisting mandatory selection + saved stale no_output rebuilt and renders exactly one original banner PASS.
- Run 38387239924: independent public WordPress bootstrap WITHOUT WP_CLI constant; frontend request-local ranking/cache and mandatory source gate select category-only banner PASS. Genuine main WP_Query loop and the_content hook output one banner DOM node PASS; 59/59 previous WP/MariaDB checks PASS. No new ZIP; package step skipped.
- Harness-only corrections during red-green: an attempted private is_enabled() call in test fixture was fixed using Reflection, and substring count 2 was shown to be TWO CSS class tokens in ONE banner element (regular + numbered class), not two banners; final test asserts data-ppar-slot="post_inline_banner" exactly once. Earlier failed harness runs are not product-code regressions.
- Isolated CI used the same static 728x90 original post_inline_banner slot rule without installing actual Template Kit 1.50.612. Test campaign is synthetic manual network, not real procavallo adcell provider. Real LIVE evidence is the original diagnostic, not the synthetic provider approval.

Result: The canonical source CURRENT handles the exact previously untested category-only banner placement and the normal public WordPress hook. No source modification is justified for this specific case. The actual deployed 6.72.224/6.72.226 PHP/option/DB difference remains the sole first blocker. Indexed originals cannot be read as raw ZIP in this runtime; do not imply actual code diff or offer a release without that proof.
