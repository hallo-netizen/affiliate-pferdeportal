# HOBBYRAUSCH – HERO 1.50.660 RECOVERY VALIDATION

STAND: 2026-10-15
STATUS: **RECOVERED / 65 HEROES COMPLETE / TECHNICAL PASS / BASIS 1.50.650**

## Recovered artifact
`HOBBY_DEPOT_HERO_REPLACE_ONLY_1.50.660.zip`

Recovered SHA-256:
`bd1bbd485763cbf72b07d284c5ca81664401397704dc73e310d9c4807fc3c9af`

## Payload
- exactly **65** WEBP hero files;
- exactly **65** slugs;
- exactly **65** entries in the active 1.50.650 hero map;
- payload slug set = map slug set;
- all 65 images exactly **600×220**;
- no exact duplicate file hashes;
- one installer PHP only.

## Installer scope
The plugin explicitly changes only the 65 currently mapped Hub2 hero image files.

It does **not** change:
- template-kit PHP;
- routing;
- templates;
- CSS;
- hero mapping;
- card logic;
- architecture.

## Local simulation against pristine 1.50.650
PASS:
- active map entries: 65;
- payload files: 65;
- target files found: 65/65;
- changed files: exactly **65**;
- added files: **0**;
- removed files: **0**;
- unexpected changes: **0**;
- hero map byte-identical before/after;
- payload hash = installed target hash for all 65 files.

## Correct conclusion
The complete 65-photo hero set already existed in 1.50.660.
The later 7/30 / 13-reference / 10-blocked reconstruction path was a regression and is not the current source of truth for the finished hero photos.

## Current use
Use the recovered 1.50.660 hero-replace plugin as the image artifact on top of frozen Template Kit 1.50.650.
Do not use 1.50.661–1.50.663.
Do not restart image generation.
