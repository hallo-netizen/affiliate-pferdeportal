#!/usr/bin/env bash
set -euo pipefail
umask 077
BACKUP_FILE="${1:?usage: restore_check.sh BACKUP_FILE PASSPHRASE_FILE}"
PASSPHRASE_FILE="${2:?usage: restore_check.sh BACKUP_FILE PASSPHRASE_FILE}"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
gpg --batch --yes --pinentry-mode loopback --passphrase-file "$PASSPHRASE_FILE" --decrypt --output "$work/backup.zip" "$BACKUP_FILE" >/dev/null 2>&1 || { echo 'RESTORE_FAIL:DECRYPT'; exit 1; }
unzip -q "$work/backup.zip" -d "$work/unpacked" || { echo 'RESTORE_FAIL:ZIP'; exit 1; }
root="$(find "$work/unpacked" -mindepth 1 -maxdepth 1 -type d -name 'PFERDE_ATELIER_BACKUP_*' | head -n1)"
[[ -n "$root" ]] || { echo 'RESTORE_FAIL:ROOT_MISSING'; exit 1; }
[[ -d "$root/GITHUB/affiliate-pferdeportal.git" ]] || { echo 'RESTORE_FAIL:GITHUB_MISSING'; exit 1; }
[[ -f "$root/WORDPRESS/wordpress-full.wpress" ]] || { echo 'RESTORE_FAIL:WORDPRESS_MISSING'; exit 1; }
[[ -d "$root/PROJEKTARCHIV" ]] || { echo 'RESTORE_FAIL:PROJECT_ARCHIVE_MISSING'; exit 1; }
[[ -f "$root/BACKUP_INFO.txt" ]] || { echo 'RESTORE_FAIL:MANIFEST_MISSING'; exit 1; }
git -C "$root/GITHUB/affiliate-pferdeportal.git" fsck --full >/dev/null 2>&1 || { echo 'RESTORE_FAIL:GITHUB_INVALID'; exit 1; }
grep -qx 'status=BACKUP_PASS' "$root/BACKUP_INFO.txt" || { echo 'RESTORE_FAIL:PASS_MARKER_MISSING'; exit 1; }
echo 'RESTORE_STRUCTURE_PASS'
