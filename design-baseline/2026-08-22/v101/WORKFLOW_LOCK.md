# Workflow Lock V101

1. MASTER/design contract is binding.
2. V83 remains the origin of the 28-px single-post table-following-content spacing rule.
3. Any future table normalization must preserve that spacing for every supported markup shape.
4. Required positive cases: `figure.wp-block-table`, `.wp-block-table`, `.comparison-table-wrap`, direct table in `.entry-content`.
5. Required negative case: same direct table outside `body.single-post` must not receive the V101 spacing rule.
6. Wrapper owns the 28-px spacing; table inside wrapper owns 0 px bottom margin to prevent double spacing.
7. No table-style change may modify Journal root or the V100 Journal-category owner renderer.
8. Unknown state = BLOCKED, never PASS.