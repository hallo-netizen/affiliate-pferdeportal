# AFFILIATE_ZENTRALE — Codex Cloud offline bootstrap

Stand: 2026-08-31
Repository: `hallo-netizen/affiliate-pferdeportal`
Required GitHub base branch: `affiliate-release-current`
Workstream: `AFFILIATE_ZENTRALE`

## Purpose

Codex Cloud may expose the selected GitHub base branch in an isolated writable worktree named `work` and may block outbound GitHub access. Therefore this bootstrap MUST NOT use `origin`, `git ls-remote`, `git fetch`, `git pull`, or any other network call.

The local checkout is accepted only when the exact repository-bound Affiliate authority files match the Git blob identities currently committed on `affiliate-release-current`, and the Affiliate governance/source guards pass locally.

Do not switch to STARTMASTER/H8. Do not run `control/cloud-entry-gate/cloud_entry.py`. Do not create or switch branches.

## Execute exactly before implementation

```bash
set -euo pipefail

test -z "$(git status --porcelain)"

LOCAL_BRANCH="$(git branch --show-current)"
case "$LOCAL_BRANCH" in
  affiliate-release-current|work) ;;
  *) echo "AFFILIATE_CODEX_LOCAL_BRANCH_UNEXPECTED:$LOCAL_BRANCH" >&2; exit 2 ;;
esac

# Offline identity proof for the currently bound Affiliate checkout.
test "$(git hash-object release/affiliate-zentrale/AGENTS.md)" = "ac8e5e50ca417103f6fb8b447beb99ae7c41fd77"
test "$(git hash-object control/release-governance/CURRENT_RELEASE.json)" = "3167adcdb0d8fcbafa9848afe841550863855ea1"
test "$(git hash-object protocol/AFFILIATE_RELEASE_CODEX_DS24_IMPLEMENT_FROM_REPO_20260831.md)" = "334cc7a26426e7598bc9caa68d97b9215a962af0"

python3 control/release-governance/release_guard.py governance-check
python3 control/release-governance/release_guard.py source-check

# `work` is Codex's synthetic writable worktree name. Governance authority remains
# the selected GitHub base branch `affiliate-release-current`, proven above by
# exact bound-file identity; no remote/network operation is needed or allowed.
python3 control/release-governance/release_guard.py start --branch affiliate-release-current
```

If any local identity or guard check fails, fail closed and report the exact failing check. Do not invoke STARTMASTER/H8, do not create another branch, and do not open a PR.

After PASS, immediately execute:

`protocol/AFFILIATE_RELEASE_CODEX_DS24_IMPLEMENT_FROM_REPO_20260831.md`

## Completion handling

Keep implementation changes in the existing Codex worktree. Do not create a side branch. Do not perform GitHub network operations from Codex. The GitHub base for the task remains `affiliate-release-current` even if Codex internally names the writable worktree `work`.
