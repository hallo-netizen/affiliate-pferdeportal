# SYSTEM 4 — TRUE SINGLE ROOM

Status: **BLOCKED / isolated prototype / test only.** No merge, no production publish.

## Current blocker
The real 7/7 article generation and batch gate completed successfully on production head `eaa83db95c4f40e345114696ed96596b6b920912`, but the required parent-ChatGPT file handoff FAILED. Codex created `SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json` and reported SHA256 `7dd9d71d9096c89a7538c2deed4dd845b2ff8980b51617c7600b81fc2f64428f`, but exposed it only as a Codex-task-local `sandbox:/mnt/data/...` reference. Those exact bytes are not recoverable through the current parent chat, so the overall workflow is NOT PASS.

## Current repair
The handoff is now a hard workflow gate. `handoff_transport.py` defines an exact JSON validator plus Base64 transport envelope with SHA/length readback. The bound path is:

7/7 FULL PASS -> batch gate -> validated `SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json` -> `handoff_transport.py pack` -> temporary branch `system4-parent-chat-handoff` only -> exact commit/path fetch by parent Chat -> `handoff_transport.py unpack` -> parent-chat SHA256 equality -> direct ChatGPT download -> transport branch reset to source head.

The production PR branch must not carry article/output transport content.

## WordPress boundary
The parent-chat handoff is UTF-8 JSON for `WORDPRESS_PREIMPORT_REVIEW` and contains the exact seven checked bodies, immutable WordPress metadata, per-article production context, LT 6.8 PASS evidence and PPM 6.7.9 PASS evidence. It is verified against Portal SEO Editorial Plan Compiler 0.28.22 / PPM 6.7.9 expectations.

It deliberately sets `direct_wordpress_upload_ready=false`. The later direct WordPress upload still requires a valid PSERC import envelope containing `fact_pack_bundle`, `production_plan`, and authentic `workflow_release`. No upload/publish PASS is claimed yet.

## Current whole path
WordPress JSON metadata batch -> indexed ingress item 0..6 -> one persistent canonical state per article -> research -> facts -> draft -> `controller.py fullcheck` -> same-article `controller.py repair` when required -> `fullcheck` -> output gate -> 7-item batch gate -> exact JSON handoff -> temporary transport branch -> parent-chat SHA readback -> direct download -> WordPress pre-import review.

## Article/checker state
The last real run reached article/batch production PASS before the failed old handoff boundary. LanguageTool 6.8, PPM 6.7.9, metadata/publish/link/content gates and batch integrity remained mandatory. No WordPress import or publish was performed.

## Codex economy
Codex is reserved for a real bound article-production run only. Diagnostics, architecture, preflight, transport tests, signing and WordPress work must not consume Codex when they can be performed outside Codex.

## NEXT ACTION
1. Finish the non-Codex exact-head regression including the new handoff transport and complete zero-to-file positive/negative run.
2. Prove one real dummy GitHub-transport -> parent-chat download roundtrip and cleanup without Codex.
3. Only after both are PASS, run one new real 7/7 Codex production job on the exact then-current head; the old successful article bodies cannot be recovered from the expired task-local sandbox.
4. Immediately fetch/unpack/verify the resulting handoff and expose it as the direct ChatGPT download.
5. Then perform the WordPress pre-import/package validation. No publish.
