# F-40 – Terminal published historical fingerprint

Live block: `SUPERVISOR_PROJECTION_TERMINAL_WRITE_FINGERPRINT_INVALID`, before any WordPress write.

Root cause: PPM 6.7.9 created `_ppm679_planned_write_fingerprint` from the original write payload containing exactly 14 PPM meta fields. PSERC 0.27.2 reconstructed that historical fingerprint from all metadata currently present on the published WordPress post. Later unrelated WordPress/plugin metadata therefore changed the reconstructed hash although it had never been part of the original PPM write.

Reproduction: an otherwise exact published PPM post plus neutral post-publish metadata (`_edit_last`, `_yoast_wpseo_focuskw`) reproduces the same 0.27.2 fingerprint block.

Rootfix 0.27.3: reconstruct the historical fingerprint only from the original 14 PPM write fields. All existing status, canonical ID, title, slug, content, category, provenance, expected PPM meta, fingerprint and read-only mutation checks stay fail-closed.

No content/design/prompt/title/article-type/category/quality/publish decision changes.
