# Hab & Bewahr RC35 – One-owner original HTML href evidence (13.11.2026)

## Actual bug evidenced from the installed RC34 source chain
- The original HTML \`<a href=...>\` is preserved as tracking_url; its entire HTML string is stored in payload.html.
- Existing \`output_destination_semantic_text()\` returned empty for stored \`tracking_checked\` and \`tracking_fallback\` links without inspecting meaningful source URL tokens.
- A published public Tarifcheck partner link explicitly shows \`deep=kfz-versicherung\` inside an a.partner-versicherung.de tracking URL. The importer's \`creative_library_destination_from_tracking()\` only looks for URL-valued redirect parameter names, not this product-specific deep= token.
- A separate link resolver discarded *successful same-domain redirects* even when the final page path changed.
- HTML anchor visible text was preserved in original payload.html but never considered by the insurance matching rule.
- This establishes a concrete **code defect**, but it does **not** prove that every one of the 160 private banner codes contains these exact clues.

## Single-path implementation
- \`output_destination_semantic_text()\` reads verified Tarifcheck partner's deep value and genuine first-party landing path from the already saved original href.
- \`hb_rc31_insurance_banner_plan()\` uses the existing original HTML anchor text and matched verified Hab category tree, including the singular/plural "Versicherung(en)" variant, **once**.
- Existing \`creative_library_resolve_tracking_destination_import()\` retains genuine completed same-host redirects instead of throwing the landing page away.
- No new worker, no second writer, no frontend content analysis, no extra HTTP, no guessed replacement banner, no fabricated target, no reimport.
- Genuine image/link/authorization veto remains.
- Existing RC34 Reconcile in backend can revisit original verified records; final proof needs actual private WordPress after install.

## Proof status
- Build/QA stored in \`RC35_HTML_LINK_KISS\`, complete RC23–RC35 automated original-PHP test required. The first successful local test uses **documented public link grammar** and synthetic partner-id, not any user's personal affiliate ID.
- A live, authenticated 160-original review is unavailable via public GitHub; do not report all 160 as solved until actual backend check.
