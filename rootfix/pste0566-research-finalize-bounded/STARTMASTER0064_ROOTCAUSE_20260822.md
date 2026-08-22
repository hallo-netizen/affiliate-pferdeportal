# STARTMASTER0064 – Single Research 3/3 endless FINALIZE root cause

Scope: root-cause checkpoint only; no code change.

Live symptom: one normal single-family research run reaches 3/3 provider steps and USD 0.048 cost, remains RUNNING, reports incomplete AJAX transport recovery and waits for internal coordination instead of terminating.

Correction: a normal single-run cancel did not historically exist. Its absence is a separate usability/safety TODO and is NOT the cause of this endless-run defect.

Confirmed source path:
- after provider step 3, PSTE_Research_Job enters FINALIZE and calls PSTE_Runner::finalizeResearchJob in one AJAX advance;
- finalizeResearchJob performs Sandbox research admission and portal-context refresh before returning;
- PSTE 0.51 introduced a request-bounded record-local Sandbox architecture for the real 549-record / ~58 MiB legacy Sandbox;
- however PSTE_Semantic_Review_Sandbox::stored() in the normal research-finalize path still loads the complete legacy PSTE_OPTION_SEMANTIC_SANDBOX option;
- persistRegistry() still rewrites the complete legacy registry with update_option() and then invalidates the record-local store as STALE_LEGACY_CHANGED;
- the normal research FINALIZE therefore bypasses the record-local runtime protection and remains monolithic/unbounded;
- transport/coordination recovery keeps transient conditions RUNNING but this local FINALIZE has no durable progress/stall convergence contract, allowing a large-state timeout/transport-recovery cycle to surface as persistent RUNNING.

Historical parity proof:
- class-pste-runner.php: 0.55.0 == 0.56.4 == 0.56.5 sha256 da40452236c407bbfed0126935fb89218f56b17ff2e86472a0e787915cd3aabd
- class-pste-semantic-review-sandbox.php: 0.55.0 == 0.56.4 == 0.56.5 sha256 bc1f8b2a2776a14528b7757e3c359509460a36deff28c760f8c4b61d4f9f15c5
- class-pste-research-job.php: 0.55.0 == 0.56.4 sha256 426c922d355a47b637b31a41cf3fb480c3d872fdf4baef607d40baf19592b355; 0.56.5 delta adds only breadth-stop cancellation and does not alter normal FINALIZE.

Allowed repair scope only: request-bounded durable normal Research-FINALIZE, record-local Sandbox persistence for research-finalize admissions, durable progress/convergence, no provider replay.

Forbidden in this repair: DataForSEO queries, topic/family/category/title/article-type/SEO semantics, Sandbox manual-review UX, single-run cancel, text machine, PSERC semantics, PPM semantics, design, article writes, publish.

STARTMASTER0064 local master SHA-256: cf3d5250c3cbb01dfbd8b2e6a49552998e67d3b48c68199b2916c30309689606
Fresh manifest: 6301/6301 PASS. Base STARTMASTER0063: 6281/6281 byte-identical.