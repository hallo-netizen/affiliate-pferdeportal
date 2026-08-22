# V103 Workflow Lock

- V103 is based only on audited V102 source/master state.
- `main` remains untouched.
- Scope: visible gap after a table only inside `body.single-post ... section[data-block="table"]`.
- Legacy/non-semantic tables stay on V83/V101 and must not be restyled.
- Horse `assets/single-post-locked-v15083.css` must remain byte-identical to V102.
- V100 Journal runtime must remain outside this change.
- Before release: real direct-table production source, real wrapper production source, legacy reference, negative non-semantic case, 1440/1200/900/390 browser geometry, PHP lint, fresh-unpack parity and master manifest must all PASS.
- Unknown or partial state = BLOCKED; no live PASS before user visual confirmation.
