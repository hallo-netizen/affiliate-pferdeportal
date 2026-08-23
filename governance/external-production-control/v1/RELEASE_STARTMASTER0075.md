# STARTMASTER0075 – External Production Control Plane V1

## Scope
Governance-only control layer outside the existing editorial/production workflow. No Fachplugin, editorial plan, READY state, article content, research/fact pack, quality gate, workflow order or publish behavior is modified.

## Release identities
- STARTMASTER: `STARTMASTER0075_EXTERNAL_PRODUCTION_CONTROL_PLANE_V1_20260823.zip`
- STARTMASTER SHA-256: `7a8281908889288881f77c5f2cc8127e0553175f1e973d6ea70a5addf8ebc7f8`
- Current handoff: `CHAT_HANDOFF_CURRENT_STARTMASTER0075_20260823.zip`
- Handoff SHA-256: `5af51dce6437b0459880aa482b20991b4f1e5938f61dc8b5890e5a1c239c6f79`
- Delivery manifest: `DELIVERY_CURRENT_STARTMASTER0075.json`
- Delivery manifest SHA-256: `e97042be7b9e1522ebacc8b13bc2f8d54718ff3e69e7430039827bdeee424625`
- Exact current next input: `PRODUCTION_PACKAGE_Boxenmatten_Beratung_PRELIVE_PASS_SANITIZATION_ROOTFIX.json`
- Next-input SHA-256: `31694dd2b5a662bf315b20a818e2b9b03f283a8279c569ef827e584c5668a679`
- Current state ID: `8fec4d82f8f55a971c2389edaed2e2015f6eacf54e00294a7f1020bd90775058`

## QA
- Fresh STARTMASTER0075 manifest: `8230/8230 PASS`
- ZIP integrity: `PASS`
- Inherited STARTMASTER0074 files: `8210/8210 byte-identical PASS`
- Control-plane QA: `18/18 PASS`
- Non-interference proof: `PASS`
- Guard SHA-256: `e223e5d00580a486bae2bccbe644fc037a0fbae4b952ba2e8788e93a8b56f1f9`
- Policy SHA-256: `15af53796e19022f9789e146d1df30b0ec2970e99d63b912a25bc344ede769ea`
- Design review SHA-256: `c34dc0dd7f22d35379fb953dfee6ac713027315a62902710914691240bb9b437`
- Non-interference proof SHA-256: `8abdf074d81cb16854a8aa54b858c0a9b0ecb3cb1c80d9719a4ba2e4798ebf0e`

## Current execution state
- checkpoint: `BOXENMATTEN_PRELIVE_PASS_SANITIZATION_ROOTFIX`
- next allowed step: `PSERC_LIVE_REPLAY_WITH_EXACT_PRELIVE_PACKAGE`
- execution source: `CURRENT_STATE_JSON_ONLY`
- local FINAL: forbidden
- publish: forbidden

## Operational rule
Every new chat starts from the current handoff/state, never from memory or historical reconstruction. Every machine checkpoint produces a fresh handoff. Every chat close is checked by the delivery gate against the binding MASTER, current state and exact next input.

`main` is intentionally untouched.
