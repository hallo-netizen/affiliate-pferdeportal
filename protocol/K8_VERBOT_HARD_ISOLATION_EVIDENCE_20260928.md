# K8 VERBOT HARD ISOLATION EVIDENCE — 2026-09-28

Purpose: trigger the existing deterministic entrance hardlock for the already-tested K8 isolation candidate.

Evidence:
- K8 runtime contains zero direct references to K7 runtime names or paths.
- preserved K7 pre-director branch contains zero K8 references.
- preserved K7 GitHub-freeze branch contains zero K8 references.
- live intake entry resolves only to the K8 isolated namespace.
- wrong K8 command leaves checkpoint and allowed action unchanged.
- no change to LT 6.8, PPM 6.7.9, PSERC, ENDSTEMPEL, article rules, workflow order or publish=false.
- temporary test workflow was removed before merge.
