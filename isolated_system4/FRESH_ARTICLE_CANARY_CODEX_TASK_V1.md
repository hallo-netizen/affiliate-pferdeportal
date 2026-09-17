# SYSTEM 4A — FRESH OFF-DOMAIN CODEX CANARY V1

TEST ONLY. No merge. No publish. No repository file modifications.

## Purpose
Prove that the worker really generates a new article after the start gate. No prepared horse-domain article, PPM candidate body, repository article body or legacy fixture may be reused.

## Fixed topic
- Title: `Warum beschlägt ein Badezimmerspiegel nach dem Duschen?`
- Target keyword: `Badezimmerspiegel beschlägt`
- Domain: Alltag/Physik/Haushalt
- Horse-domain content is forbidden.

## Hard execution sequence
1. Create a fresh temporary workspace OUTSIDE the repository, e.g. `/tmp/system4-fresh-canary-codex`.
2. Run:
   `PYTHONPATH=isolated_system4 python3 isolated_system4/fresh_article_canary_v1.py prepare /tmp/system4-fresh-canary-codex`
3. Run the fixed machine source loader:
   `python3 isolated_system4/fresh_article_canary_source_loader_v1.py /tmp/system4-fresh-canary-codex`
4. From this point the worker MUST NOT use free web search or fetch any additional source. Read only:
   - `/tmp/system4-fresh-canary-codex/challenge.json`
   - `/tmp/system4-fresh-canary-codex/source_manifest.json`
   - `/tmp/system4-fresh-canary-codex/sources/*.txt`
   - `isolated_system4/FRESH_ARTICLE_CANARY_V1.json`
5. Do NOT read or reuse any article body from the repository, PPM package, live fixtures, proof files or old artifacts. In particular do not use any body from `g9-single-faq-approved-candidate-v1.json`, `full_local_acceptance.py`, `FIRST_FULL_RULE_TEST_ARTICLE_PROOF.json`, historical handoffs or WordPress article files.
6. Create these NEW files in the temp workspace only:

### research.json
Contract exactly `SYSTEM4_RESEARCH_EVIDENCE_V1`.
Use the sealed source IDs from `source_manifest.json`. Include source title/URL, retrieved evidence text and evidence SHA256. Research must explain the topic from the sealed sources; do not invent unsupported factual claims.

### facts.json
Contract exactly `SYSTEM4_FACTS_EVIDENCE_V1`.
Create factual claims bound to source IDs and exact evidence snippets/hashes from the accepted research. Claims must be sufficient to support the generated article.

### article.html
Write a genuinely new German FAQ article for the fixed topic. It must contain the exact topic wording or unmistakable equivalent, explain condensation/air moisture/surface temperature clearly, be useful and readable, and contain no horse-domain terms from `FRESH_ARTICLE_CANARY_V1.json`.
Do not imitate or copy any repository article.

### worker_provenance.json
Contract exactly `SYSTEM4_FRESH_WORKER_PROVENANCE_V1` and include:
- `challenge_nonce`: exact nonce from challenge.json
- `generated_after_start_gate`: true
- `prewritten_fixture_used`: false
- `generation_mode`: `LIVE_WORKER_GENERATION`
- `article_sha256`: SHA256 of stripped UTF-8 `article.html`, exactly as the verifier computes it
- `worker`: `CODEX_CLOUD_PR260`
- `publish_allowed`: false

7. Run:
   `PYTHONPATH=isolated_system4 python3 isolated_system4/fresh_article_canary_v1.py verify /tmp/system4-fresh-canary-codex`
8. If verification fails, correct ONLY the temp worker outputs and rerun verification. Never modify the verifier/spec or any repository file to obtain PASS.

## Terminal response
Return:
- exact current PR head SHA
- source loader PASS/FAIL
- canary verifier PASS/FAIL
- SHA256 of article.html
- the final `article.html` verbatim
- explicit statement `repository_files_modified=false`
- explicit statement `publish_allowed=false`

PASS is forbidden unless the actual verifier prints `SYSTEM4_FRESH_ARTICLE_CANARY_PASS:<sha>`.
