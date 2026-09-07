#!/usr/bin/env bash
set -euo pipefail
umask 077

# KISS-Komplettsicherung Pferde Atelier.
# Nimmt den vorhandenen WordPress-Vollbackupstand, GitHub komplett und das Projektarchiv.
# Ohne unabhängige Offsite-Kopie kein BACKUP_PASS.

GITHUB_REPO_URL="${GITHUB_REPO_URL:-https://github.com/hallo-netizen/affiliate-pferdeportal.git}"
WP_BACKUP_DIR="${WP_BACKUP_DIR:?WP_BACKUP_DIR missing}"
PROJECT_ARCHIVE_DIR="${PROJECT_ARCHIVE_DIR:?PROJECT_ARCHIVE_DIR missing}"
BACKUP_OUTPUT_DIR="${BACKUP_OUTPUT_DIR:?BACKUP_OUTPUT_DIR missing}"
OFFSITE_DIR="${OFFSITE_DIR:?OFFSITE_DIR missing}"
BACKUP_PASSPHRASE_FILE="${BACKUP_PASSPHRASE_FILE:?BACKUP_PASSPHRASE_FILE missing}"
KEEP_LOCAL="${KEEP_LOCAL:-4}"

fail(){ echo "BACKUP_FAIL:$1" >&2; exit 1; }

for cmd in git zip gpg sha256sum find sort awk cp mkdir mktemp date unzip; do
  command -v "$cmd" >/dev/null 2>&1 || fail "TOOL_MISSING_${cmd}"
done

[[ -d "$WP_BACKUP_DIR" ]] || fail "WP_BACKUP_DIR_MISSING"
[[ -d "$PROJECT_ARCHIVE_DIR" ]] || fail "PROJECT_ARCHIVE_DIR_MISSING"
[[ -r "$BACKUP_PASSPHRASE_FILE" ]] || fail "PASSPHRASE_MISSING"
[[ -d "$OFFSITE_DIR" && -w "$OFFSITE_DIR" ]] || fail "OFFSITE_NOT_MOUNTED"
mkdir -p "$BACKUP_OUTPUT_DIR"

wp_file="$(find "$WP_BACKUP_DIR" -maxdepth 1 -type f -name '*.wpress' -printf '%T@ %p\n' 2>/dev/null | sort -nr | awk 'NR==1{sub(/^[^ ]+ /,"");print;exit}')"
[[ -n "$wp_file" && -r "$wp_file" ]] || fail "WP_FULL_BACKUP_MISSING"

stamp="$(date -u +%Y-%m-%d_%H%M%S)"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
payload="$work/PFERDE_ATELIER_BACKUP_$stamp"
mkdir -p "$payload/GITHUB" "$payload/WORDPRESS" "$payload/PROJEKTARCHIV"

git clone --mirror "$GITHUB_REPO_URL" "$payload/GITHUB/affiliate-pferdeportal.git" >/dev/null 2>&1 || fail "GITHUB_MIRROR_FAILED"
git -C "$payload/GITHUB/affiliate-pferdeportal.git" fsck --full >/dev/null 2>&1 || fail "GITHUB_MIRROR_INVALID"

cp -p "$wp_file" "$payload/WORDPRESS/wordpress-full.wpress" || fail "WP_BACKUP_COPY_FAILED"
cp -a "$PROJECT_ARCHIVE_DIR"/. "$payload/PROJEKTARCHIV"/ || fail "PROJECT_ARCHIVE_COPY_FAILED"

repo_head="$(git -C "$payload/GITHUB/affiliate-pferdeportal.git" for-each-ref --format='%(objectname)' refs/heads/main | head -n1)"
wp_sha="$(sha256sum "$payload/WORDPRESS/wordpress-full.wpress" | awk '{print $1}')"
archive_count="$(find "$payload/PROJEKTARCHIV" -type f | wc -l | tr -d ' ')"

cat > "$payload/BACKUP_INFO.txt" <<EOF
status=BACKUP_PASS
created_at_utc=$stamp
repository=$GITHUB_REPO_URL
main_sha=$repo_head
wordpress_source=$(basename "$wp_file")
wordpress_sha256=$wp_sha
project_archive_files=$archive_count
components=GITHUB,WORDPRESS,PROJEKTARCHIV
EOF

(
  cd "$work"
  zip -0 -q -r "PFERDE_ATELIER_BACKUP_$stamp.zip" "PFERDE_ATELIER_BACKUP_$stamp"
) || fail "PACKAGE_BUILD_FAILED"

plain="$work/PFERDE_ATELIER_BACKUP_$stamp.zip"
enc="$BACKUP_OUTPUT_DIR/PFERDE_ATELIER_BACKUP_$stamp.zip.gpg"

gpg --batch --yes --pinentry-mode loopback \
  --passphrase-file "$BACKUP_PASSPHRASE_FILE" \
  --symmetric --cipher-algo AES256 \
  --output "$enc" "$plain" >/dev/null 2>&1 || fail "ENCRYPTION_FAILED"

sha="$(sha256sum "$enc" | awk '{print $1}')"
size="$(wc -c < "$enc" | tr -d ' ')"

cp -p "$enc" "$OFFSITE_DIR/$(basename "$enc")" || fail "OFFSITE_COPY_FAILED"
printf '%s  %s\n' "$sha" "$(basename "$enc")" > "$OFFSITE_DIR/$(basename "$enc").sha256"

cat > "$BACKUP_OUTPUT_DIR/latest.json.tmp" <<EOF
{"status":"BACKUP_PASS","created_at":"$stamp UTC","filename":"$(basename "$enc")","size_bytes":$size,"sha256":"$sha"}
EOF
mv "$BACKUP_OUTPUT_DIR/latest.json.tmp" "$BACKUP_OUTPUT_DIR/latest.json"
cp -p "$BACKUP_OUTPUT_DIR/latest.json" "$OFFSITE_DIR/latest.json"

find "$BACKUP_OUTPUT_DIR" -maxdepth 1 -type f -name 'PFERDE_ATELIER_BACKUP_*.zip.gpg' -printf '%T@ %p\n' \
  | sort -nr | awk -v keep="$KEEP_LOCAL" 'NR>keep{sub(/^[^ ]+ /,"");print}' \
  | while IFS= read -r old; do [[ -n "$old" ]] && rm -f -- "$old"; done

echo "BACKUP_PASS"
echo "FILE=$enc"
echo "SHA256=$sha"
