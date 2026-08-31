# AFFILIATE_ZENTRALE — Codex Cloud base/bootstrap

Stand: 2026-08-31
Repository: `hallo-netizen/affiliate-pferdeportal`
Verified clone URL: `https://github.com/hallo-netizen/affiliate-pferdeportal.git`
Required GitHub base branch: `affiliate-release-current`
Workstream: `AFFILIATE_ZENTRALE`

## Purpose

Codex Cloud may expose its isolated writable checkout under a synthetic local branch name such as `work`. That local name is **not** the GitHub base-branch authority.

For this Affiliate task, the checkout is valid only when its untouched HEAD is byte-identical to the current GitHub head of `affiliate-release-current`.

Do not switch to STARTMASTER. Do not run `control/cloud-entry-gate/cloud_entry.py`. Do not create another branch.

## Execute exactly before implementation

```bash
set -euo pipefail

test -z "$(git status --porcelain)"

EXPECTED_REMOTE_A='https://github.com/hallo-netizen/affiliate-pferdeportal.git'
EXPECTED_REMOTE_B='https://github.com/hallo-netizen/affiliate-pferdeportal'
BOUND_BRANCH='affiliate-release-current'

if ! git remote get-url origin >/dev/null 2>&1; then
  git remote add origin "$EXPECTED_REMOTE_A"
else
  CURRENT_REMOTE="$(git remote get-url origin)"
  test "$CURRENT_REMOTE" = "$EXPECTED_REMOTE_A" -o "$CURRENT_REMOTE" = "$EXPECTED_REMOTE_B"
fi

git ls-remote --exit-code --heads origin "refs/heads/$BOUND_BRANCH" >/dev/null
git fetch --no-tags origin \
  "refs/heads/$BOUND_BRANCH:refs/remotes/origin/$BOUND_BRANCH"

LOCAL_BRANCH="$(git branch --show-current)"
case "$LOCAL_BRANCH" in
  "$BOUND_BRANCH"|work) ;;
  *) echo "AFFILIATE_CODEX_LOCAL_BRANCH_UNEXPECTED:$LOCAL_BRANCH" >&2; exit 2 ;;
esac

HEAD_SHA="$(git rev-parse HEAD)"
BOUND_SHA="$(git rev-parse "origin/$BOUND_BRANCH")"
test "$HEAD_SHA" = "$BOUND_SHA"

# Do not switch branches. `work` is permitted only as Codex's synthetic local
# worktree name after the exact HEAD/base identity check above.
python3 control/release-governance/release_guard.py governance-check
python3 control/release-governance/release_guard.py source-check
python3 control/release-governance/release_guard.py start --branch "$BOUND_BRANCH"
```

If any command fails, fail closed and report the exact command/error. Do not invoke STARTMASTER/H8, do not create another branch, and do not open a PR.

After PASS, immediately execute:

`protocol/AFFILIATE_RELEASE_CODEX_DS24_IMPLEMENT_FROM_REPO_20260831.md`

## Completion handling

Keep all implementation changes in the existing Codex worktree. Do not create a side branch. The GitHub base for the task remains `affiliate-release-current` even if Codex internally names the writable worktree `work`.
