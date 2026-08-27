# PSTE 0.56.15 – Article-Type-Safe Natural Title Rootfix

Date: 2026-08-27

## Proven live trigger
Fresh PSERC 0.28.5 snapshot `seo-redaktionsplan-metadaten-snapshot-929e4de1be8bd4fdf5b46c445d7389ebc5231a1e8e81719fc0af35a7db1d69ff.json` on PSTE 0.56.14 reported:
- READY_FOR_METADATA_HANDOFF = 1
- BLOCKED_QUESTION_TITLE_NOT_FAQ = 4
- REVIEW_REQUIRED_TITLE_COMPATIBILITY = 0
- observed READY title: `Die wichtigsten Fragen zu Bahnplaner für Pferde`

## Root cause
0.56.14 solved batch-level wording concentration, but its automatic Beratung portfolio still allowed W-question surfaces and exact-keyword insertion after case-governing prepositions. This conflicts with the already-bound Beratung/FAQ title boundary and can produce visibly broken German while preserving the exact keyword.

## Root fix
- Automatic Beratung title candidates must be structurally non-question surfaces.
- Exact target keywords cannot be inserted after case-governing prepositions that can require inflection.
- Batch diversity remains generic and runs only on structurally valid candidates.
- Persisted automatic 0.56.14 Beratung surfaces can be repaired title-only/read-model-only.
- Manual title overrides remain untouched.
- No single-word blacklist is used.

## Scope
Compared with verified PSTE 0.56.14: 215 -> 216 files, 211 existing files byte-identical. Only these paths differ:
- `CHANGELOG_0.56.15.md` (new)
- `includes/class-pste-repository.php`
- `includes/class-pste-title-composer.php`
- `includes/class-pste-title-diversity.php`
- `portal-seo-topic-engine.php`

The existing title validator, German reviewer, editorial quality gate and title pipeline are byte-identical to 0.56.14.

No changes to Textmaschine, article body/content, research, PSERC, PPM 6.7.9, LanguageTool, HTML, links, tables, CSS or design. No WordPress post/term/meta write surface added.

## Verification
- PHP lint: 73/73 PASS
- exact current 4 Beratung cases: 4/4 pipeline + batch diversity + protected binding PASS
- 0.56.14 live-failure regression: PASS
- 10 real Beratung generalization matrix: PASS
- non-Beratung parity vs 0.56.14: byte-identical test output
- protected field/content/design sentinels: byte-equal
- installer ZIP extract-vs-build: 216/216 byte-identical

Installer SHA-256: `56a9ebf641cf88f07c9b3600ba2aba0395abf8a861550fb68fa45640f1a766ec`
Verification report SHA-256: `301f7d31a04d93235eb9a945606f21185ef3c1103658a84ff2b7cf7043049f62`

## Live status
`WORDPRESS_05615_LIVE_E2E = OPEN_REQUIRES_INSTALL_AND_FRESH_PSERC_SNAPSHOT`
No production or publish claim is made before that live readback.