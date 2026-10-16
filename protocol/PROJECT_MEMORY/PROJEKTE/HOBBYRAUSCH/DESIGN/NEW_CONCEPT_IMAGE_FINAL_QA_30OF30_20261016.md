# HOBBYRAUSCH – FINAL QA 30/30 NEW-CONCEPT IMAGES

STAND: 2026-10-16
STATUS: **30/30 VISUAL PASS / IMAGE-ONLY PLUGIN CANDIDATE TECHNICAL PASS**

## Scope
This QA applies only to the 30 categories that were rebuilt under the new standalone-source concept. The frozen runtime remains Template Kit 1.50.650. No PHP/CSS/template/routing/mapping/card/architecture changes are part of this candidate.

## Visual QA
All 30 current standalone source images were opened and inspected as full sources, then again as the real target crops:
- 30/30 Hero crops at 600×320;
- 30/30 Preview crops at 200×107.

PASS criteria:
- category semantics clearly recognizable;
- single continuous scene / standalone source;
- no collage or raster source in release;
- no image-in-image;
- no wrong fallback;
- main motif remains recognizable after both target crops;
- no visible upscaling;
- no exact image duplicate;
- collision pairs remain visually distinct.

Result: **30/30 PASS**.

Collision examples explicitly checked:
- Holz ↔ Heimwerken;
- Papierkunst ↔ Schrift & Lettering;
- Textilgestaltung ↔ Leder;
- Guss & Formen ↔ Keramik & Glas;
- Mechanik & Uhren ↔ Messen & Analysieren;
- Robotik & Automation ↔ Technik & Medien;
- Astronomie ↔ Wetter & Umwelt;
- Gärtnern ↔ Essbare Pflanzen;
- Miniaturen & Szenen ↔ Moos & Miniaturgärten;
- Ameisen & Insekten ↔ Wirbellose.

Technical duplicate screen on the 30 Hero crops:
- exact SHA duplicates: **0**;
- minimum 256-bit dHash Hamming distance among all Hero pairs: **104**.

## Final image-only build
Artifact:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_HOBBY_DEPOT_NEW_IMAGES_30_VISUALPASS.zip`

SHA-256:
`cbc9789925660ada90a32e1d9726c4b6086c9d8308a8d097009573afab66ddc8`

Persisted Library path:
`/hobby rausch/releases/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_HOBBY_DEPOT_NEW_IMAGES_30_VISUALPASS.zip`

Final stage archive:
`/hobby rausch/releases/HOBBY_DEPOT_NEW_IMAGES_30_STAGE_FINAL.zip`

Stage SHA-256:
`12d50d3f9bfc7e62b4f7f04a140c3e07e8e5d7dfdd49e1974187535acd788545`

## Independent local 1:1 verification against pristine 1.50.650
Positive PASS:
- base files: **981**;
- candidate files: **981**;
- files added: **0**;
- files removed: **0**;
- changed files: exactly **60**;
- changed files are exclusively WEBP image targets;
- 30 Heroes exactly **600×320**;
- 30 Previews exactly **200×107**;
- bad dimensions: **0**;
- `hub2-image-map.json` byte-identical;
- PHP files: **55/55 byte-identical**;
- PHP syntax: **55/55 PASS** in build pass;
- ZIP roundtrip: **PASS**.

Negative simulations PASS:
- deleting one expected target is detected;
- changing the hero mapping is detected.

## Release meaning
This is a **visual+technical PASS image-only candidate for the 30 rebuilt categories on frozen 1.50.650**.
It is not a claim that every unrelated global Hobbyrausch design/card backlog item is complete.
