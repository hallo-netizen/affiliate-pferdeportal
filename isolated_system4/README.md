# SYSTEM 4 — TRUE SINGLE ROOM

Status: **BLOCKED / isolated prototype / test only.** No merge, no production publish.

## Current verified history
The real 7/7 article generation and batch gate already completed successfully on production head `eaa83db95c4f40e345114696ed96596b6b920912`. The old run failed only at the parent-ChatGPT file handoff because Codex exposed the file only through a task-local `sandbox:/mnt/data/...` path. Those exact old article bytes are no longer recoverable in the parent chat, so a fresh production run will still be required after the repaired output path is fully proven.

## Current output repair
The handoff/transport chain already exists and remains the bound path:

7/7 FULL PASS -> batch gate -> validated `SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json` -> `handoff_transport.py pack` -> temporary branch `system4-parent-chat-handoff` -> exact commit/path fetch by parent Chat -> `handoff_transport.py unpack` -> parent-chat SHA256 equality -> direct ChatGPT download -> transport branch reset.

The production PR branch must not carry article/output transport content.

## Final WordPress boundary for the current article production
The existing WordPress signature switch is temporarily OFF. Therefore the current System-4 article output performs **no signing and no ENDSTEMPEL step**.

The exact file delivered in the parent Chat is also the exact direct WordPress upload file. No second transformation occurs after the parent-chat readback.

The final JSON must state:
- `WORDPRESS_DIRECT_IMPORT`
- `direct_wordpress_upload_ready=true`
- `direct_upload_block_reason=null`
- `required_downstream_components=[]`
- `publish_allowed=false`

System 4 does not modify the WordPress plugin or the signature switch.

## Article/checker state
LanguageTool 6.8, PPM 6.7.9, metadata/publish/link/content gates and batch integrity remain mandatory and unchanged. Same-draft repair remains bound through `controller.py repair -> fullcheck`. No checker, Textmaschine rule, SEO rule, metadata rule or publish rule is weakened by the output repair.

## Codex economy
Codex is reserved for the real bound 7-article production run only. Diagnostics, regression, transport and output-path proof must be completed outside Codex first.

## NEXT ACTION
1. Run the exact-head non-Codex regression for the repaired direct-upload output contract, including positive and negative handoff tests.
2. Prove one real dummy `system4-parent-chat-handoff` roundtrip: pack -> branch -> exact parent fetch -> unpack -> SHA/bytes equal -> branch cleanup/reset.
3. Only after both PASS, run one fresh real 7/7 Codex production job on that exact head; the old successful article bytes are unrecoverable.
4. Immediately fetch/unpack/verify the resulting final JSON and expose exactly that file as the single ChatGPT download.
5. User uploads that same JSON unchanged to WordPress. No signing. No ENDSTEMPEL. No auto-publish.
