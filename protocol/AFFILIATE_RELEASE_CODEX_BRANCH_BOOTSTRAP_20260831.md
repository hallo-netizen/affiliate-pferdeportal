# AFFILIATE_ZENTRALE — Codex branch bootstrap

Stand: 2026-08-31
Repository: `hallo-netizen/affiliate-pferdeportal`
Required remote branch: `affiliate-release-current`
Workstream: `AFFILIATE_ZENTRALE`

## Purpose

This file only resolves the Codex Cloud checkout case where the repository opens on a local branch such as `work` and the already-existing remote branch `affiliate-release-current` has not been fetched locally yet.

Fetching the existing remote branch and creating a **local tracking branch with the exact same name** is authorized bootstrap. It does **not** create a new remote workstream/release branch and does not relax governance.

## Execute exactly

```bash
set -euo pipefail

# No implementation changes may exist before changing to the bound branch.
test -z "$(git status --porcelain)"

# The required branch must already exist on origin. Never invent a substitute.
git ls-remote --exit-code --heads origin refs/heads/affiliate-release-current >/dev/null

# Fetch only the already-existing bound remote branch.
git fetch --no-tags origin \
  refs/heads/affiliate-release-current:refs/remotes/origin/affiliate-release-current

# Reuse an existing local branch if present; otherwise create only the local
# tracking branch for the already-existing remote branch of the same name.
if git show-ref --verify --quiet refs/heads/affiliate-release-current; then
  git switch affiliate-release-current
else
  git switch --create affiliate-release-current --track origin/affiliate-release-current
fi

# No merge/rebase divergence is allowed.
git merge --ff-only origin/affiliate-release-current

test "$(git branch --show-current)" = "affiliate-release-current"
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/affiliate-release-current)"

python3 control/release-governance/release_guard.py governance-check
```

If any command fails, fail closed and report the exact command/error. Do not create any differently named branch and do not open a PR.

After PASS, immediately execute the repository-native task:

`protocol/AFFILIATE_RELEASE_CODEX_DS24_IMPLEMENT_FROM_REPO_20260831.md`

Do not stop merely because the initial Codex checkout branch was `work`; the branch check applies after this bootstrap has fetched and checked out the already-existing bound remote branch.
