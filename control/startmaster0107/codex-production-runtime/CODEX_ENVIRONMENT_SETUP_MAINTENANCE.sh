#!/usr/bin/env bash
set -euo pipefail

REPO_FULL_NAME="hallo-netizen/affiliate-pferdeportal"
REPO_URL="https://github.com/${REPO_FULL_NAME}.git"
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

# Never allow a proof from a previous cached Codex chat to survive.
rm -rf .pferde-environment
mkdir -p .pferde-environment

# External setup/maintenance is the root of trust: determine current GitHub main
# before any repository-owned production code is allowed to run.
MAIN_SHA="$(git ls-remote "$REPO_URL" refs/heads/main | awk 'NR==1 {print $1}')"
LOCAL_SHA="$(git rev-parse HEAD)"
if [[ ! "$MAIN_SHA" =~ ^[0-9a-f]{40}$ ]]; then
  echo "CODEX_MAIN_AUTHORITY_UNAVAILABLE"
  exit 2
fi
if [[ "$LOCAL_SHA" != "$MAIN_SHA" ]]; then
  echo "CODEX_CHECKOUT_NOT_CURRENT_MAIN:${LOCAL_SHA}:EXPECTED:${MAIN_SHA}"
  exit 2
fi

# Persist only the already-verified main identity for the offline agent phase.
git update-ref refs/remotes/origin/main "$MAIN_SHA"

# Fixed technical runtime dependency for ED25519 verification.
if ! python3 - <<'PY' >/dev/null 2>&1
import cryptography
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
assert cryptography.__version__ == "50.0.1"
PY
then
  python3 -m pip install --disable-pip-version-check --no-input "cryptography==50.0.1"
fi

# Repository preflight is still purely technical and content-blind.
python3 control/startmaster0107/codex-production-runtime/codex_environment_preflight.py
