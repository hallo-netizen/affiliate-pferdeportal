#!/usr/bin/env bash
set -euo pipefail

: "${TRESOR_MASTER_PASSWORD:?TRESOR_MASTER_PASSWORD missing}"
: "${RECOVERY_BUNDLE_FILE:?RECOVERY_BUNDLE_FILE missing}"
: "${WORDPRESS_BACKUP_DIR:?WORDPRESS_BACKUP_DIR missing}"

REPO_SLUG="${REPO_SLUG:-${GITHUB_REPOSITORY:-}}"
SOURCE_REPO_URL="${SOURCE_REPO_URL:-}"
OUT_DIR="${OUT_DIR:-$PWD/tresor-out}"
PUBLISH="${PUBLISH:-0}"
TARGET_SHA="${TARGET_SHA:-${GITHUB_SHA:-}}"
NOW="${NOW:-$(date -u +%Y-%m-%d-%H%M)}"
TAG="tresor-${NOW}"
ASSET="PB_ONE_KOMPLETTSICHERUNG_${NOW}.tar.gz.gpg"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
umask 077

need(){ command -v "$1" >/dev/null 2>&1 || { echo "TRESOR_BLOCK:TOOL_MISSING:$1"; exit 2; }; }
for x in git gpg tar sha256sum python3; do need "$x"; done
if [[ -z "$SOURCE_REPO_URL" ]]; then
  [[ -n "$REPO_SLUG" ]] || { echo 'TRESOR_BLOCK:REPO_NOT_BOUND'; exit 2; }
  SOURCE_REPO_URL="https://x-access-token:${GH_TOKEN:?GH_TOKEN missing}@github.com/${REPO_SLUG}.git"
fi
[[ -d "$WORDPRESS_BACKUP_DIR" ]] || { echo 'TRESOR_BLOCK:WORDPRESS_BACKUP_DIR_MISSING'; exit 2; }
mkdir -p "$OUT_DIR" "$WORK/payload/git" "$WORK/payload/github" "$WORK/payload/raw" "$WORK/payload/recovery" "$WORK/payload/wordpress" "$WORK/verify"

for f in database.sql.gz wordpress-files.tar.gz WORDPRESS_MANIFEST.json WORDPRESS_COMPLETE.flag; do
  [[ -f "$WORDPRESS_BACKUP_DIR/$f" ]] || { echo "TRESOR_BLOCK:WORDPRESS_REQUIRED_FILE_MISSING:$f"; exit 2; }
done
python3 - "$WORDPRESS_BACKUP_DIR" <<'PY'
import hashlib,json,pathlib,sys
p=pathlib.Path(sys.argv[1]); m=json.loads((p/'WORDPRESS_MANIFEST.json').read_text())
for name in ('database.sql.gz','wordpress-files.tar.gz'):
    exp=(m.get('sha256') or {}).get(name)
    if not exp: raise SystemExit('TRESOR_BLOCK:WORDPRESS_MANIFEST_HASH_MISSING:'+name)
    h=hashlib.sha256((p/name).read_bytes()).hexdigest()
    if h!=exp: raise SystemExit('TRESOR_BLOCK:WORDPRESS_HASH_MISMATCH:'+name)
print('WORDPRESS_BACKUP_CONTRACT_PASS')
PY
cp "$WORDPRESS_BACKUP_DIR/database.sql.gz" "$WORK/payload/wordpress/"
cp "$WORDPRESS_BACKUP_DIR/wordpress-files.tar.gz" "$WORK/payload/wordpress/"
cp "$WORDPRESS_BACKUP_DIR/WORDPRESS_MANIFEST.json" "$WORK/payload/wordpress/"
cp "$WORDPRESS_BACKUP_DIR/WORDPRESS_COMPLETE.flag" "$WORK/payload/wordpress/"

git clone --mirror "$SOURCE_REPO_URL" "$WORK/payload/git/repository.git" >/dev/null 2>&1
if command -v git-lfs >/dev/null 2>&1 || git lfs version >/dev/null 2>&1; then
  (cd "$WORK/payload/git/repository.git" && git lfs fetch --all >/dev/null 2>&1 || true)
fi
(cd "$WORK/payload/git/repository.git" && git bundle create "$WORK/payload/git/repository.bundle" --all)
(cd "$WORK/payload/git/repository.git" && git for-each-ref --format='%(refname) %(objectname)' refs/heads refs/tags | sort) > "$WORK/payload/git/source_refs.txt"
(cd "$WORK/payload/git/repository.git" && git fsck --full --strict >/dev/null)

if [[ -n "${GITHUB_METADATA_SOURCE_DIR:-}" ]]; then
  cp -R "$GITHUB_METADATA_SOURCE_DIR"/. "$WORK/payload/github/"
else
  need gh
  : "${GH_TOKEN:?GH_TOKEN missing}"
  api(){ gh api --paginate "$1" > "$2"; }
  gh api "repos/$REPO_SLUG" > "$WORK/payload/github/repository.json"
  api "repos/$REPO_SLUG/branches?per_page=100" "$WORK/payload/github/branches.json"
  api "repos/$REPO_SLUG/tags?per_page=100" "$WORK/payload/github/tags.json"
  api "repos/$REPO_SLUG/issues?state=all&per_page=100" "$WORK/payload/github/issues.json"
  api "repos/$REPO_SLUG/issues/comments?per_page=100" "$WORK/payload/github/issue_comments.json"
  api "repos/$REPO_SLUG/pulls?state=all&per_page=100" "$WORK/payload/github/pulls.json"
  api "repos/$REPO_SLUG/pulls/comments?per_page=100" "$WORK/payload/github/pull_review_comments.json"
  api "repos/$REPO_SLUG/labels?per_page=100" "$WORK/payload/github/labels.json"
  api "repos/$REPO_SLUG/milestones?state=all&per_page=100" "$WORK/payload/github/milestones.json"
  api "repos/$REPO_SLUG/releases?per_page=100" "$WORK/payload/github/releases.json"
  api "repos/$REPO_SLUG/rulesets?per_page=100" "$WORK/payload/github/rulesets.json"
  api "repos/$REPO_SLUG/actions/workflows?per_page=100" "$WORK/payload/github/workflows.json"
  api "repos/$REPO_SLUG/environments?per_page=100" "$WORK/payload/github/environments.json"
  api "repos/$REPO_SLUG/deployments?per_page=100" "$WORK/payload/github/deployments.json"

  mkdir -p "$WORK/payload/github/pr_reviews"
  python3 - "$WORK/payload/github/pulls.json" > "$WORK/pr_numbers.txt" <<'PY'
import json,sys
for r in json.load(open(sys.argv[1])):
    n=r.get('number')
    if n is not None: print(n)
PY
  while IFS= read -r n; do gh api --paginate "repos/$REPO_SLUG/pulls/$n/reviews?per_page=100" > "$WORK/payload/github/pr_reviews/$n.json"; done < "$WORK/pr_numbers.txt"

  mkdir -p "$WORK/payload/github/release_assets"
  python3 - "$WORK/payload/github/releases.json" > "$WORK/releases.tsv" <<'PY'
import json,sys
for r in json.load(open(sys.argv[1])):
    tag=str(r.get('tag_name') or '')
    if tag.startswith('tresor-'): continue
    for a in r.get('assets') or []:
        print(tag+'\t'+str(a.get('id'))+'\t'+str(a.get('name') or 'asset'))
PY
  while IFS=$'\t' read -r tag aid name; do
    [[ -n "$aid" ]] || continue
    safe_tag="$(printf '%s' "$tag" | tr '/ ' '__')"; mkdir -p "$WORK/payload/github/release_assets/$safe_tag"
    gh api -H 'Accept: application/octet-stream' "repos/$REPO_SLUG/releases/assets/$aid" > "$WORK/payload/github/release_assets/$safe_tag/$name"
  done < "$WORK/releases.tsv"
fi

for f in repository.json branches.json tags.json issues.json issue_comments.json pulls.json pull_review_comments.json labels.json milestones.json releases.json rulesets.json workflows.json environments.json deployments.json; do
  [[ -s "$WORK/payload/github/$f" ]] || { echo "TRESOR_BLOCK:GITHUB_METADATA_MISSING:$f"; exit 2; }
done

[[ -f "$RECOVERY_BUNDLE_FILE" ]] || { echo 'TRESOR_BLOCK:RECOVERY_BUNDLE_MISSING'; exit 2; }
cp "$RECOVERY_BUNDLE_FILE" "$WORK/payload/recovery/recovery.bundle"

RAW_ARCHIVE_DIR="${RAW_ARCHIVE_DIR:-}"
[[ -n "$RAW_ARCHIVE_DIR" && -d "$RAW_ARCHIVE_DIR" ]] || { echo 'TRESOR_BLOCK:RAW_ARCHIVE_NOT_BOUND'; exit 2; }
cp -R "$RAW_ARCHIVE_DIR"/. "$WORK/payload/raw/"

(
  cd "$WORK/payload"
  find . -type f ! -name 'PAYLOAD_SHA256.txt' -print0 | sort -z | xargs -0 sha256sum > PAYLOAD_SHA256.txt
)
cat > "$WORK/payload/TRESOR_MANIFEST.json" <<JSON
{"contract":"PB_ONE_ONEFILE_TRESOR_V1","status":"TRESOR_PASS_CANDIDATE","created_utc":"${NOW}","repository":"${REPO_SLUG}","target_sha":"${TARGET_SHA}","user_flow":"GitHub Releases -> latest TRESOR_PASS asset -> download locally","previous_tresor_release_assets_embedded":false}
JSON
(
  cd "$WORK/payload"
  sha256sum TRESOR_MANIFEST.json >> PAYLOAD_SHA256.txt
)

tar -C "$WORK" -czf "$WORK/payload.tar.gz" payload
printf '%s' "$TRESOR_MASTER_PASSWORD" | gpg --batch --yes --pinentry-mode loopback --passphrase-fd 0 --symmetric --cipher-algo AES256 --s2k-digest-algo SHA512 --output "$OUT_DIR/$ASSET" "$WORK/payload.tar.gz"
sha256sum "$OUT_DIR/$ASSET" > "$OUT_DIR/$ASSET.sha256"

printf '%s' "$TRESOR_MASTER_PASSWORD" | gpg --batch --yes --pinentry-mode loopback --passphrase-fd 0 --decrypt --output "$WORK/verify/payload.tar.gz" "$OUT_DIR/$ASSET" >/dev/null 2>&1
tar -C "$WORK/verify" -xzf "$WORK/verify/payload.tar.gz"
(cd "$WORK/verify/payload" && sha256sum -c PAYLOAD_SHA256.txt >/dev/null)
git -C "$WORK/verify/payload/git/repository.git" bundle verify "$WORK/verify/payload/git/repository.bundle" >/dev/null 2>&1
git clone --mirror "$WORK/verify/payload/git/repository.bundle" "$WORK/verify/restored.git" >/dev/null 2>&1
(cd "$WORK/verify/restored.git" && git fsck --full --strict >/dev/null)
(cd "$WORK/verify/restored.git" && git for-each-ref --format='%(refname) %(objectname)' refs/heads refs/tags | sort) > "$WORK/verify/restored_refs.txt"
diff -u "$WORK/verify/payload/git/source_refs.txt" "$WORK/verify/restored_refs.txt" >/dev/null
[[ -f "$WORK/verify/payload/git/repository.git/HEAD" ]] || exit 2
[[ -f "$WORK/verify/payload/wordpress/database.sql.gz" ]] || exit 2
[[ -s "$WORK/verify/payload/recovery/recovery.bundle" ]] || exit 2

size=$(wc -c < "$OUT_DIR/$ASSET" | tr -d ' ')
if (( size >= 2147483648 )); then echo "TRESOR_BLOCK:GITHUB_RELEASE_ASSET_TOO_LARGE:$size"; exit 2; fi

if [[ "$PUBLISH" == "1" ]]; then
  need gh
  gh release view "$TAG" --repo "$REPO_SLUG" >/dev/null 2>&1 && exit 2
  SHA="$(sha256sum "$OUT_DIR/$ASSET" | awk '{print $1}')"
  gh release create "$TAG" "$OUT_DIR/$ASSET#$ASSET" --repo "$REPO_SLUG" --target "$TARGET_SHA" --title "TRESOR_PASS $NOW" --notes "TRESOR_PASS. Exact encrypted one-file recovery asset verified before upload. SHA-256: $SHA"
fi

echo "TRESOR_ONEFILE_BUILD_VERIFY_PASS:$OUT_DIR/$ASSET"
