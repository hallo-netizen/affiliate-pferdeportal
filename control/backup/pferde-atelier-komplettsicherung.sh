#!/usr/bin/env bash
set -Eeuo pipefail

# Pferde-Atelier Komplettsicherung
# 1 Lauf -> 1 datiertes Paket -> PASS/FAIL
#
# Einmalig setzen:
#   export WP_MODE="ssh"       # ssh oder local
#   export WP_SSH="user@host"  # nur bei ssh
#   export WP_PATH="/pfad/zur/wordpress-installation"
#
# Optional:
#   export BACKUP_ROOT="$HOME/PFERDE_ATELIER_BACKUPS"

REPO="hallo-netizen/affiliate-pferdeportal"
REPO_URL="https://github.com/${REPO}.git"
WP_MODE="${WP_MODE:-ssh}"
WP_SSH="${WP_SSH:-}"
WP_PATH="${WP_PATH:-}"
BACKUP_ROOT="${BACKUP_ROOT:-$HOME/PFERDE_ATELIER_BACKUPS}"

STAMP="$(date +%Y-%m-%d_%H-%M-%S)"
NAME="PFERDE_ATELIER_BACKUP_${STAMP}"
WORKDIR="$(mktemp -d)"
PKGDIR="${WORKDIR}/${NAME}"
FINAL="${BACKUP_ROOT}/${NAME}.tar.gz"

cleanup() { rm -rf "${WORKDIR}"; }
trap cleanup EXIT

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

need() {
  command -v "$1" >/dev/null 2>&1 || fail "Benoetigtes Programm fehlt: $1"
}

need git
need gh
need tar

mkdir -p "${PKGDIR}/git" "${PKGDIR}/github-settings" "${PKGDIR}/wordpress"
mkdir -p "${BACKUP_ROOT}"

gh auth status >/dev/null 2>&1 || fail "GitHub CLI ist nicht angemeldet. Einmal 'gh auth login' ausfuehren."
[[ -n "${WP_PATH}" ]] || fail "WP_PATH fehlt. Ohne WordPress-Teil gibt es bewusst keinen Teil-PASS."

echo "[1/4] GitHub komplett sichern ..."
git clone --mirror "${REPO_URL}" "${PKGDIR}/git/affiliate-pferdeportal.git" >/dev/null 2>&1
git -C "${PKGDIR}/git/affiliate-pferdeportal.git" fsck --full >/dev/null
git -C "${PKGDIR}/git/affiliate-pferdeportal.git" show-ref > "${PKGDIR}/git/refs.txt"
git -C "${PKGDIR}/git/affiliate-pferdeportal.git" rev-parse HEAD > "${PKGDIR}/git/main_head.txt"

echo "[2/4] GitHub-Einstellungen sichern ..."
gh api "repos/${REPO}" > "${PKGDIR}/github-settings/repository.json"
gh api "repos/${REPO}/rulesets" > "${PKGDIR}/github-settings/rulesets.json" || true
gh api "repos/${REPO}/actions/permissions" > "${PKGDIR}/github-settings/actions_permissions.json" || true
gh api "repos/${REPO}/actions/permissions/workflow" > "${PKGDIR}/github-settings/workflow_permissions.json" || true
gh api "repos/${REPO}/environments" > "${PKGDIR}/github-settings/environments.json" || true

echo "[3/4] WordPress komplett sichern ..."
case "${WP_MODE}" in
  local)
    need wp
    [[ -d "${WP_PATH}" ]] || fail "WP_PATH existiert lokal nicht: ${WP_PATH}"
    wp --path="${WP_PATH}" db export "${PKGDIR}/wordpress/database.sql" --quiet
    tar -C "${WP_PATH}" -czf "${PKGDIR}/wordpress/wordpress-files.tar.gz" .
    ;;
  ssh)
    need ssh
    need scp
    [[ -n "${WP_SSH}" ]] || fail "WP_SSH fehlt fuer WP_MODE=ssh"
    REMOTE_TMP="/tmp/pferde_atelier_backup_${STAMP}"
    ssh "${WP_SSH}" "set -e; mkdir -p '${REMOTE_TMP}'; wp --path='${WP_PATH}' db export '${REMOTE_TMP}/database.sql' --quiet; tar -C '${WP_PATH}' -czf '${REMOTE_TMP}/wordpress-files.tar.gz' ."
    scp "${WP_SSH}:${REMOTE_TMP}/database.sql" "${PKGDIR}/wordpress/database.sql" >/dev/null
    scp "${WP_SSH}:${REMOTE_TMP}/wordpress-files.tar.gz" "${PKGDIR}/wordpress/wordpress-files.tar.gz" >/dev/null
    ssh "${WP_SSH}" "rm -rf '${REMOTE_TMP}'"
    ;;
  *)
    fail "WP_MODE muss 'ssh' oder 'local' sein."
    ;;
esac

[[ -s "${PKGDIR}/wordpress/database.sql" ]] || fail "WordPress-Datenbank fehlt oder ist leer."
[[ -s "${PKGDIR}/wordpress/wordpress-files.tar.gz" ]] || fail "WordPress-Dateisicherung fehlt oder ist leer."
[[ -s "${PKGDIR}/git/refs.txt" ]] || fail "Git-Refs fehlen."
[[ -d "${PKGDIR}/git/affiliate-pferdeportal.git/objects" ]] || fail "Git-Mirror unvollstaendig."
[[ -s "${PKGDIR}/github-settings/repository.json" ]] || fail "GitHub-Repository-Metadaten fehlen."

GIT_HEAD="$(cat "${PKGDIR}/git/main_head.txt")"

cat > "${PKGDIR}/BACKUP_INFO.txt" <<EOF
PFERDE-ATELIER KOMPLETTSICHERUNG
Datum: ${STAMP}
Repository: ${REPO}
Git-HEAD: ${GIT_HEAD}
WordPress-Modus: ${WP_MODE}

Enthalten:
- kompletter Git-Mirror mit Historie, Branches und Tags
- exportierbare GitHub-Repository-Einstellungen
- komplette WordPress-Datenbank
- komplette WordPress-Dateien

Pruefung:
- git fsck: PASS
- Git-Refs vorhanden: PASS
- WordPress-Datenbank vorhanden: PASS
- WordPress-Dateien vorhanden: PASS
- GitHub-Metadaten vorhanden: PASS

Gesamt: PASS
EOF

echo "[4/4] Ein Sicherungspaket bauen ..."
tar -C "${WORKDIR}" -czf "${FINAL}" "${NAME}"
[[ -s "${FINAL}" ]] || fail "Sicherungspaket wurde nicht erstellt."

echo
echo "PASS"
echo "Sicherung: ${FINAL}"
echo "Git-HEAD: ${GIT_HEAD}"
