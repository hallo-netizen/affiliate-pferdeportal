# Codex scoped rules — Hobby Depot category and tile images ONLY
This file applies solely when Codex operates in this directory or below.
DO NOT touch any of the Pferdeatelier or Hab & Bewahr projects, K0, article-image plugin HD-006, or production WordPress data.

For Codex's built-in image generation, invoke the official `$imagegen` skill in the ChatGPT-authenticated Codex client. Do not configure or use an API key.\n\nGoal: generate precisely ONE photorealistic standalone scene per proven missing hobby-category slug for the current Hobby Depot design plugin HD-003. A scene must have one cohesive visual subject/activity. Never generate a contact sheet, grid, collage, multi-panel image, montage, labels, logos, or multiple concepts in one image. Never generate more than one new image per target unless the first has been rejected with an explicit reason. Never share an image between different topics. Favor natural activity, including helpful hands, appropriate craft tools, and believable physical actions.

BEFORE generation:
1. Read the exact current project inventory; inspect the most recent HD-003/current ZIP and the target's WordPress page / media mapping if available.
2. Only proceed when the exact slug and world are proven and neither target already has an assigned or bundled image. Fail closed on uncertain live-state.
3. Freeze exactly one content brief for the topic with a specific photographic scene. Avoid lists of different objects and the instruction to 'represent all aspects of a category'.

AFTER generation:
4. Review the actual image visually: single continuous photo, topic immediately obvious, no multi-panel/collage, no typography or logos, no wrong tools/actions, no duplicate with a prior topic, legible when cropped to 200x107. Reject otherwise.
5. Save one original source per slug. Derive 600x320 image for both category header and existing tile image routing. An additional 200x107 preview is for QA only; the current HD-003 code rejects sub-500px images as final source.
6. Do not touch PHP, JavaScript, CSS, metadata, mapping logic, or other images. Package images using the EXISTING plugin asset destinations and verify against exact current ZIP SHA-256.
7. Verify restored ZIP has all original files byte-identical and precisely two new images of the identical approved source for that one slug. Never silently overwrite existing files.
8. Save machine-readable proof with statuses GENERATED, VISUAL_REVIEW_PASS, PACKAGED_LOCAL_PASS, LIVE_VERIFIED only when truly demonstrated. Do not claim WordPress deployment without an authenticated readback.

No API key. Codex image generation is used only within a ChatGPT-authenticated Codex session; GitHub Actions does not itself produce AI images. Avoid mock-up images for production. A technical integration fixture is only a test and MUST NOT be released or installed.
