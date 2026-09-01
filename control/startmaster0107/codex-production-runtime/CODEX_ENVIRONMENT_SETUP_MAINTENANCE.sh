#!/usr/bin/env bash
set -euo pipefail

REPO_FULL_NAME="hallo-netizen/affiliate-pferdeportal"
REPO_URL="https://github.com/${REPO_FULL_NAME}.git"
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

# Never allow proof data from a previous cached Codex chat to survive.
rm -rf .pferde-environment
mkdir -p .pferde-environment

# This environment is also used for non-production branch work. Only a task
# explicitly checked out on main is synchronized to the current GitHub main.
CURRENT_BRANCH="$(git branch --show-current || true)"
if [[ "$CURRENT_BRANCH" == "main" ]]; then
  # Setup/Maintenance runs before the agent phase and has internet access.
  # Use the full repository URL; never depend on an 'origin' remote existing.
  MAIN_SHA="$(git ls-remote "$REPO_URL" refs/heads/main | awk 'NR==1 {print $1}')"
  if [[ ! "$MAIN_SHA" =~ ^[0-9a-f]{40}$ ]]; then
    echo "CODEX_MAIN_AUTHORITY_UNAVAILABLE"
    exit 2
  fi

  # Materialize the exact current main commit locally and force the worktree to it.
  # This removes stale cached-main checkouts before any project-owned code runs.
  git fetch --no-tags "$REPO_URL" "+${MAIN_SHA}:refs/pferde-authority/current-main"
  git reset --hard "$MAIN_SHA"

  LOCAL_SHA="$(git rev-parse HEAD)"
  if [[ "$LOCAL_SHA" != "$MAIN_SHA" ]]; then
    echo "CODEX_MAIN_SYNC_FAILED:${LOCAL_SHA}:EXPECTED:${MAIN_SHA}"
    exit 2
  fi

  # Persist only the already-verified identity for the offline agent phase.
  git update-ref refs/remotes/origin/main "$MAIN_SHA"

  cat > .pferde-environment/MAIN_SYNC.json <<JSON
{
  "contract": "PFERDE_ATELIER_CODEX_MAIN_SYNC_V1",
  "status": "PASS",
  "repository": "${REPO_FULL_NAME}",
  "sync_mode": "SETUP_MAINTENANCE_HARD_SYNC_CURRENT_MAIN",
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

# The production preflight is relevant only for production tasks on main.
if [[ "$CURRENT_BRANCH" == "main" ]]; then
  python3 control/startmaster0107/codex-production-runtime/codex_environment_preflight.py
fi
