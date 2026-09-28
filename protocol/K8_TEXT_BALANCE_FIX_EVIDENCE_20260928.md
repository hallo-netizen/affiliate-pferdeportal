# K8 TEXT BALANCE FIX EVIDENCE — 2026-09-28

Scope: text-rule correction only.

Proven on temporary branch workflow before this evidence file:
- real K8 writer target_min_words = 750
- real K8 writer target_min_paragraphs = 16
- normal H2 range remains exactly 60..120 words
- conclusion target remains 0.12
- conclusion hard maximum = 0.18
- conclusion maximum paragraphs = 3
- oversized conclusion rejected by K8 section balance
- short normal H2 section rejected
- WRITE_DRAFT acceptance rejects an oversized conclusion
- same balance validator is called after same-article repair
- no LT 6.8, PPM 6.7.9, PSERC, ENDSTEMPEL, workflow order, architecture or publish change
- generated article output files are not modified by this change
