#!/usr/bin/env bash
set -euo pipefail

REPO_FULL_NAME="hallo-netizen/affiliate-pferdeportal"
REPO_URL="https://github.com/${REPO_FULL_NAME}.git"
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

# Never allow proof data from a previous cached Codex chat to survive.
rm -rf .pferde-environment
mkdir -p .pferde-environment

# Resolve current GitHub main independently of the local Codex branch name.
# Codex Cloud may expose the selected UI branch as a synthetic local branch
# (for example "work"), so production proof must not depend on the literal
# output of `git branch --show-current`.
CURRENT_BRANCH="$(git branch --show-current || true)"
MAIN_SHA="$(git ls-remote "$REPO_URL" refs/heads/main | awk 'NR==1 {print $1}')"
if [[ ! "$MAIN_SHA" =~ ^[0-9a-f]{40}$ ]]; then
  echo "CODEX_MAIN_AUTHORITY_UNAVAILABLE"
  exit 2
fi

# Materialize the verified current main identity for the offline agent phase.
git fetch --no-tags "$REPO_URL" "+${MAIN_SHA}:refs/pferde-authority/current-main"
git update-ref refs/remotes/origin/main "$MAIN_SHA"

LOCAL_SHA="$(git rev-parse HEAD)"
SYNC_MODE="IDENTITY_ONLY_CURRENT_MAIN"

# Only a literal local main branch may be rewritten. This preserves the
# existing non-main no-rewrite contract. Synthetic/detached Codex checkouts
# are never rewritten merely because of their local branch name.
if [[ "$CURRENT_BRANCH" == "main" && "$LOCAL_SHA" != "$MAIN_SHA" ]]; then
  git reset --hard "$MAIN_SHA"
  LOCAL_SHA="$(git rev-parse HEAD)"
  SYNC_MODE="HARD_SYNC_CURRENT_MAIN"
fi

# Production proof is identity-based, not local-branch-name-based. This covers
# Codex Cloud's synthetic `work`/detached checkout when it points exactly at
# the selected current main, while leaving real non-main commits untouched.
if [[ "$LOCAL_SHA" == "$MAIN_SHA" ]]; then
  cat > .pferde-environment/MAIN_SYNC.json <<JSON
{
  "contract": "PFERDE_ATELIER_CODEX_MAIN_SYNC_V1",
  "status": "PASS",
  "repository": "${REPO_FULL_NAME}",
  "sync_mode": "${SYNC_MODE}",
  "main_sha": "${MAIN_SHA}",
  "local_head_sha": "${LOCAL_SHA}",
  "origin_remote_required": false,
  "agent_network_required": false,
  "content_semantics_inspected": false,
  "quality_authority": "NONE",
  "publish_allowed": false
}
JSON
fi

# Fixed technical runtime dependency for ED25519 verification.
if ! python3 - <<'PY' >/dev/null 2>&1
import cryptography
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
assert cryptography.__version__ == "50.0.1"
PY
then
  python3 -m pip install --disable-pip-version-check --no-input "cryptography==50.0.1"
fi

# Materialize the exact pinned PPM 6.7.9 dependency for the offline agent phase.
PPM_PART_DIR="control/startmaster0107/codex-production-runtime/dependencies/ppm679"
PPM_ZIP=".pferde-environment/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
python3 - "$PPM_PART_DIR" "$PPM_ZIP" <<'PY'
import base64, hashlib, pathlib, sys
part_dir=pathlib.Path(sys.argv[1])
target=pathlib.Path(sys.argv[2])
expected_size=1614485
expected_sha="acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"
raw=b"".join(base64.b64decode((part_dir/f"ppm.{i:02d}.b64").read_bytes()) for i in range(7))
if len(raw)!=expected_size:
    raise SystemExit("PPM679_DEPENDENCY_SIZE_MISMATCH")
if hashlib.sha256(raw).hexdigest()!=expected_sha:
    raise SystemExit("PPM679_DEPENDENCY_HASH_MISMATCH")
tmp=target.with_suffix(target.suffix+".tmp")
tmp.write_bytes(raw)
tmp.replace(target)
PY

# Run the production preflight whenever this checkout is proven to be the
# current GitHub main commit, regardless of Codex's synthetic local branch name.
if [[ "$LOCAL_SHA" == "$MAIN_SHA" ]]; then
  python3 control/startmaster0107/codex-production-runtime/codex_environment_preflight.py
fi
