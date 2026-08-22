# Test Evidence – PSERC 0.28.3

- Source package integrity: PASS, 112 required files.
- Fresh-unpack package integrity: PASS.
- Source ↔ Fresh: 113/113 files byte-identical.
- PHP syntax Fresh: 40/40 PASS.
- Legacy signed Workflow-Supervisor release: PASS.
- New-key signed Workflow-Supervisor release: PASS (stored-release authenticity preflight).
- Wrong signing key id: BLOCKED.
- Manipulated signature: BLOCKED.
- Current five Beratung positions: PSERC→PPM intake bridge PASS; `content_or_design_modified=false` for all five.
- Protected production hashes before/after identical:
  - Redaktionsplan snapshot: `c435e7cb9bcd0e6b49eba6a9780deec18906b437723d0353b1e003accce05bb5`
  - Fact-packs tree: `faefc56ab6d10609cd362699d58fe25c345457d80c14af473baa3a2d6c3135de`
  - Articles tree: `a8dd607ad69b76675d6fb2896d4170756b69f56b6b66a9d8eee24bb85a46590a`
  - Language evidence tree: `314814a773cf57e77f965855d799a31cef9d4e484fc4f0e45b92bfa0c3ab40f3`
  - Gates tree: `d6d2755fd36bbe3adc71f2de456e90b3f2781dddbf9d798fd01480dfd38dccc6`
  - PPM waves tree: `c2ef20ce9eb2c7d9e7d378a804160e17b17629654a248dbd9218317f724fd783`

Pre-existing production evidence blocker: `SUPERVISOR_START_GATE_READY_ITEM_NOT_PROVEN` occurs identically under PSERC 0.28.2 and 0.28.3 because the saved current compiler manifest has `items: []`. This was not altered or bypassed in the key-repair block.

Installer SHA-256: `b95260918e9068643cab87c5b9488929883ee3b45932648eaf8e06d736c47b05`.

No publish. No WordPress write.