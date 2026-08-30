# Production Package Release Rootfix Scope Lock

This rootfix is technical packaging/orchestration only.

MUST NOT change:
- H7 / Single-Door architecture or route semantics
- CURRENT_STARTMASTER navigation semantics
- article/content/quality/SEO/title/keyword/research rules
- LanguageTool, PPM, PSERC, PSTE domain logic
- duplicate/cannibalization/design rules
- publish behavior (publish_allowed remains false)

Allowed scope:
- ensure a user-facing upload artifact is exposed only when it is already a complete PSERC_APPROVED_PRODUCTION_PACKAGE_V1
- fail closed on production_plan_v4 or any incomplete handoff
- validate the same package contract/hash/signature requirements already enforced by H7 before presenting an artifact as upload-ready
- preserve existing signed-package creation authority; no private key material is added here
