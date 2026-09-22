#!/usr/bin/env bash
set -euo pipefail

INPUT="${1:?usage: restore_check.sh GITHUB_KOMPLETTBACKUP.zip|GITHUB_KOMPLETTBACKUP.tar.gz}"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

case "$INPUT" in
  *.zip)
    unzip -q "$INPUT" -d "$work/outer"
    ARCHIVE="$work/outer/GITHUB_KOMPLETTBACKUP.tar.gz"
    [[ -f "$ARCHIVE" ]] || { echo 'GITHUB_RESTORE_FAIL:ARCHIVE_MISSING'; exit 1; }
    if [[ -f "$work/outer/GITHUB_KOMPLETTBACKUP.tar.gz.sha256" ]]; then
      (
        cd "$work/outer"
        sha256sum -c GITHUB_KOMPLETTBACKUP.tar.gz.sha256
      ) || { echo 'GITHUB_RESTORE_FAIL:OUTER_HASH'; exit 1; }
    fi
    ;;
  *.tar.gz)
    ARCHIVE="$INPUT"
    ;;
  *)
    echo 'GITHUB_RESTORE_FAIL:UNSUPPORTED_FILE'
    exit 1
    ;;
esac

mkdir -p "$work/unpacked"
tar -xzf "$ARCHIVE" -C "$work/unpacked" || { echo 'GITHUB_RESTORE_FAIL:TAR'; exit 1; }

for req in MANIFEST.txt SHA256SUMS.txt affiliate-pferdeportal.bundle meta/repository.json meta/restore-test-status.txt; do
  [[ -e "$work/unpacked/$req" ]] || { echo "GITHUB_RESTORE_FAIL:MISSING_$req"; exit 1; }
done

(
  cd "$work/unpacked"
  sha256sum -c SHA256SUMS.txt
) || { echo 'GITHUB_RESTORE_FAIL:INNER_HASH'; exit 1; }

mkdir "$work/verifyrepo"
(
  cd "$work/verifyrepo"
  git init -q
  git bundle verify "$work/unpacked/affiliate-pferdeportal.bundle" >/dev/null
) || { echo 'GITHUB_RESTORE_FAIL:BUNDLE_VERIFY'; exit 1; }

git clone --mirror "$work/unpacked/affiliate-pferdeportal.bundle" "$work/restore.git" >/dev/null 2>&1   || { echo 'GITHUB_RESTORE_FAIL:CLONE'; exit 1; }

git -C "$work/restore.git" fsck --full --strict >/dev/null 2>&1   || { echo 'GITHUB_RESTORE_FAIL:FSCK'; exit 1; }

grep -qx 'GIT_BUNDLE_RESTORE_PASS' "$work/unpacked/meta/restore-test-status.txt"   || { echo 'GITHUB_RESTORE_FAIL:SOURCE_RESTORE_MARKER'; exit 1; }

echo 'GITHUB_REPOSITORY_RESTORE_PASS'
