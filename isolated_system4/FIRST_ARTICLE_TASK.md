# SYSTEM 4 — FIRST GENERATED ARTICLE TEST

Goal: generate the first real article through the isolated System 4 workflow using the first item from the real 7/7 WordPress metadata snapshot.

This is still TEST ONLY. No merge, no production publish, no legacy workflow reuse.

## Input
`isolated_system4/live_fixture/wordpress_snapshot.json`

## Hard isolation
- Work only with `isolated_system4/**` repository code.
- Runtime workspace and generated article files must live only in a temporary directory outside the repository.
- Do not modify repository files.
- Do not call STARTMASTER, legacy Cloud Entry, PPM/PSERC/PSTE runtime, old workers, gates, handoffs, signers or concepts 1–3.
- Do not publish.

## Fixed execution
1. Create a fresh temporary workspace and output directory.
2. Run:
   `python3 isolated_system4/codex_entry.py start isolated_system4/live_fixture/wordpress_snapshot.json <workspace>`
3. Read only `<workspace>/state.json` to obtain the bound article metadata.
4. Create research text and fact text for that bound topic. Keep claims conservative and general; do not invent precise statistics, laws, medical claims or manufacturer facts.
5. Bind research with:
   `python3 isolated_system4/controller.py research <workspace> <research-file>`
6. Bind facts with:
   `python3 isolated_system4/controller.py facts <workspace> <facts-file>`
7. Write a genuinely new German advice article for the bound title/keyword. Requirements for this test article:
   - exact H1 must equal the bound WordPress title;
   - target keyword must appear naturally;
   - at least 2 H2 headings;
   - useful, coherent prose;
   - no mention of System 4, Codex, prompts or WordPress in the article;
   - no unsafe HTML;
   - aim for roughly 450–650 words.
8. Submit the draft:
   `python3 isolated_system4/controller.py draft <workspace> <draft-file>`
9. Run:
   `python3 isolated_system4/controller.py check <workspace>`
10. If and only if the controller returns `REPAIR_REQUIRED`, edit only the same draft file to correct the reported `last_error`, resubmit with `draft`, then re-run `check`. Do not alter metadata, research, facts, routing or controller code.
11. After `OUTPUT_GATE_REQUIRED`, run:
   `python3 isolated_system4/controller.py release <workspace> <output-dir>`
12. Verify from the produced release data and WXR that:
   - `publish_allowed=false`;
   - WordPress status is `draft`;
   - title equals the bound title;
   - released article hash matches the checked draft.

## Required return
Return:
- terminal `SYSTEM4_FIRST_GENERATED_ARTICLE_PASS` or the first actual System 4 blocker;
- the controller status sequence;
- final article markdown verbatim;
- final draft SHA256;
- WordPress WXR SHA256;
- revision count.

Do not commit generated article/output files to the repository.
