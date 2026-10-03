# K0 rendering regression local evidence — 2026-10-03

Scope: structured single-post rendering only.

Observed regression:
- source-trace metadata spans participated in structured section layout;
- ordinary H2 showed unequal visual spacing;
- conclusion/Fazit amplified the gap because several source-trace spans follow the heading.

Local hard regression:
- NEGATIVE, previous CSS: normal H2 visual gap above 32 px / below 64 px; Fazit above 145 px / below 192 px.
- POSITIVE, candidate CSS: normal H2 above 32 px / below 32 px; Fazit visual spacing above 33 px / below 32 px.
- source-trace metadata: hidden from layout in POSITIVE.
- exact three-link fixture: PASS.
- negative missing-semantic-link fixture: FAIL as required.

No article content, writer rules, table logic, LanguageTool 6.8, PPM 6.7.9, WordPress handoff, canonical IDs or publish safety changed.

This protocol file also triggers the existing deterministic entrance hardlock for PR #493.
