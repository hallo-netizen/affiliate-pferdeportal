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

# Restore the exact historic LanguageTool 6.8 dependency before the agent phase.
# Environment provisioning is branch-independent; production authority remains
# strictly current-main-only below. No content/quality rule is implemented here.
python3 - <<'PY'
from pathlib import Path
import hashlib
import json
import shutil
import urllib.request
import zipfile

ENV = Path(".pferde-environment")
CACHE = Path.home() / ".cache" / "pferde-atelier-languagetool"
CACHE.mkdir(parents=True, exist_ok=True)

ASSET_URL = "https://github.com/jxmorris12/language_tool_python/releases/download/LanguageTool-6.8/LanguageTool-6.8.zip"
INNER_SHA = "6a7f6b67b779ae9505f7579f0c41453ea8d1bd72ae750bdc2c55ba974281467d"
INNER_SIZE = 258510816
OUTER_SHA = "187f7c2efe7762049e9f00553dafe686e269bbf62220abe2f2715fe55df8605a"
JAR_SHA = "2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8"
JAR_MANIFEST_SHA = "eb6fbf76ab6747b7a5a156390149c103f0e31e2ae14eddb28317cac0201ebe5c"
ENGINE = "LanguageTool 6.8 / Bestand 43"

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            block = fh.read(1024 * 1024)
            if not block:
                break
            h.update(block)
    return h.hexdigest()

inner = CACHE / "LanguageTool-6.8.zip"
if not inner.is_file() or inner.stat().st_size != INNER_SIZE or sha256(inner) != INNER_SHA:
    tmp = CACHE / "LanguageTool-6.8.zip.tmp"
    if tmp.exists():
        tmp.unlink()
    req = urllib.request.Request(
        ASSET_URL,
        headers={"User-Agent": "pferde-atelier-codex-languagetool-runtime"},
    )
    total = 0
    h = hashlib.sha256()
    with urllib.request.urlopen(req, timeout=120) as resp, tmp.open("wb") as out:
        while True:
            block = resp.read(1024 * 1024)
            if not block:
                break
            total += len(block)
            if total > INNER_SIZE:
                raise SystemExit("LANGUAGETOOL_DOWNLOAD_SIZE_OVERFLOW")
            h.update(block)
            out.write(block)
    if total != INNER_SIZE:
        raise SystemExit("LANGUAGETOOL_DOWNLOAD_SIZE_MISMATCH")
    if h.hexdigest() != INNER_SHA:
        raise SystemExit("LANGUAGETOOL_INNER_ZIP_HASH_MISMATCH")
    tmp.replace(inner)

# Preserve the historical Bestand-43 provenance as fixed metadata only.
# The 258 MB outer transport is not rebuilt on every Codex start. The current
# preflight binds its exact SHA while the actual executable dependency remains
# independently bound by inner ZIP, JAR, manifest, version and real execution.
outer_ref = "ARBEITSMASTER_0043_NEU_TEIL_2_LANGUAGETOOL_ABHAENGIGKEIT.zip"

runtime = ENV / "languagetool-runtime"
if runtime.exists():
    shutil.rmtree(runtime)
runtime.mkdir(parents=True)
with zipfile.ZipFile(inner) as zf:
    root = runtime.resolve()
    for info in zf.infolist():
        target = (runtime / info.filename).resolve()
        if target != root and root not in target.parents:
            raise SystemExit("LANGUAGETOOL_ZIP_PATH_ESCAPE")
    zf.extractall(runtime)

jar = runtime / "LanguageTool-6.8" / "languagetool-commandline.jar"
if not jar.is_file() or sha256(jar) != JAR_SHA:
    raise SystemExit("LANGUAGETOOL_COMMANDLINE_JAR_HASH_MISMATCH")
with zipfile.ZipFile(jar) as zf:
    jar_manifest = zf.read("META-INF/MANIFEST.MF")
if hashlib.sha256(jar_manifest).hexdigest() != JAR_MANIFEST_SHA:
    raise SystemExit("LANGUAGETOOL_COMMANDLINE_MANIFEST_HASH_MISMATCH")
if b"ComponentVersion: 6.8" not in jar_manifest:
    raise SystemExit("LANGUAGETOOL_COMPONENT_VERSION_MISMATCH")

proof = {
    "contract": "PFERDE_ATELIER_LANGUAGETOOL_RUNTIME_BINDING_V1",
    "status": "LANGUAGETOOL_RUNTIME_READY",
    "engine": ENGINE,
    "source_url": ASSET_URL,
    "outer_dependency_ref": outer_ref,
    "outer_dependency_sha256": OUTER_SHA,
    "inner_dependency_cache_ref": str(inner),
    "inner_dependency_sha256": INNER_SHA,
    "inner_dependency_size": INNER_SIZE,
    "executed_component_version": "6.8",
    "executed_commandline_jar_ref": str(jar),
    "executed_commandline_jar_sha256": JAR_SHA,
    "executed_commandline_jar_manifest_sha256": JAR_MANIFEST_SHA,
    "command_argv_template": [
        "java", "-Xmx1024m", "-jar", str(jar),
        "--json", "-l", "de-DE", "{checked_text_file}"
    ],
    "agent_network_required_for_execution": False,
    "content_semantics_inspected": False,
    "quality_authority": "NONE",
    "content_or_quality_rules_changed": False,
    "publish_allowed": False,
}
(ENV / "LANGUAGETOOL_RUNTIME.json").write_text(
    json.dumps(proof, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
PY

# Run the production preflight whenever this checkout is proven to be the
# current GitHub main commit, regardless of Codex's synthetic local branch name.
if [[ "$LOCAL_SHA" == "$MAIN_SHA" ]]; then
  python3 control/startmaster0107/codex-production-runtime/codex_environment_preflight.py
fi
