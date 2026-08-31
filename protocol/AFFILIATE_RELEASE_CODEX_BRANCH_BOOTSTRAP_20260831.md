# AFFILIATE_ZENTRALE — Codex branch bootstrap

Stand: 2026-08-31
Repository: `hallo-netizen/affiliate-pferdeportal`
Verified clone URL: `https://github.com/hallo-netizen/affiliate-pferdeportal.git`
Required remote branch: `affiliate-release-current`
Workstream: `AFFILIATE_ZENTRALE`

## Purpose

This file only resolves the Codex Cloud checkout case where the repository opens on a local branch such as `work`, the already-existing remote branch `affiliate-release-current` has not been fetched locally yet, and/or the isolated checkout contains no Git remote named `origin`.

The clone URL above is not inferred from chat context. It is the repository clone URL returned by GitHub for `hallo-netizen/affiliate-pferdeportal`. The repository is public and the required remote branch already exists on GitHub.

Adding this exact repository as the local `origin`, fetching the already-existing remote branch, and creating a **local tracking branch with the exact same name** is authorized bootstrap. It does **not** create a new remote workstream/release branch and does not relax governance.

## Execute exactly

```bash
set -euo pipefail

# No implementation changes may exist before changing to the bound branch.
test -z "$(git status --porcelain)"

EXPECTED_REMOTE='https://github.com/hallo-netizen/affiliate-pferdeportal.git'

# Codex isolated checkouts may contain no remote at all. In that exact case,
# bind `origin` to the verified GitHub repository. Never invent another URL.
if ! git remote get-url origin >/dev/null 2>&1; then
  git remote add origin "$EXPECTED_REMOTE"
else
  test "$(git remote get-url origin)" = "$EXPECTED_REMOTE"
fi

# The required branch must already exist on that exact origin. Never invent a substitute.
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

Do not stop merely because the initial Codex checkout branch was `work` or because the isolated checkout initially had no `origin`; the branch check applies after this bootstrap has bound the verified repository remote and checked out the already-existing bound remote branch.
