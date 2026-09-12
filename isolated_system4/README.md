# SYSTEM 4 — TRUE SINGLE ROOM

Status: **BLOCKED / isolated prototype / test only.** No merge, no production publish.

## Current verified history
A real 7/7 article generation and batch gate completed successfully. The failure was only the old output handoff, which attempted repository transport after article production.

## Current output repair
The production/checker core is unchanged. Only the final file handoff is replaced.

New bound output chain:

7/7 FULL PASS -> batch gate -> validated canonical `SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json` -> local `handoff_transport.py inline-pack` -> complete inline envelope in the terminal Codex result -> parent Chat `inline-unpack` -> SHA/length/schema/canonical equality -> direct ChatGPT download.

There is no handoff branch, no push, no repository file persistence, no user download from Codex/GitHub and no second WordPress transformation.

## Final WordPress boundary for the current article production
The existing WordPress signature switch is temporarily OFF. Therefore the current System-4 article output performs **no signing and no ENDSTEMPEL step**.

The exact file delivered in the parent Chat is also the exact direct WordPress upload file.

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
Codex is reserved for one explicitly approved real bound 7-article production run only. Diagnostics, regression and output-path proof must be completed outside Codex first.

## NEXT ACTION
1. Hard local positive/negative regression of the direct inline output path on the exact repaired code.
2. Verify that no production/checker core file changed.
3. Stop. Do not start another Codex production run without explicit user approval.
4. Only after approval, one fresh real 7/7 production run may use the already-proven inline handoff and return the final file to this chat.
