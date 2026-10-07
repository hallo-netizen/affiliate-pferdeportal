#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../.." && pwd)"
WP_PATH="${1:-${WP_PATH:-}}"
WP_CLI="${WP_CLI:-wp}"

fail() {
  echo "FAIL $*" >&2
  exit 1
}

[ -n "$WP_PATH" ] || fail "WP_PATH fehlt. Aufruf: $0 /pfad/zur/wordpress-installation"
[ -d "$WP_PATH" ] || fail "WordPress-Pfad existiert nicht: $WP_PATH"
command -v php >/dev/null 2>&1 || fail "php fehlt"
command -v python3 >/dev/null 2>&1 || fail "python3 fehlt"
command -v "$WP_CLI" >/dev/null 2>&1 || [ -x "$WP_CLI" ] || fail "WP-CLI fehlt: $WP_CLI"

cd "$REPO_ROOT"

python3 control/release-governance/release_guard.py governance-check
python3 control/release-governance/release_guard.py source-check
python3 control/release-governance/release_guard.py start --branch affiliate-release-current

php release/affiliate-zentrale/evidence/worktests/test_adcell_banner_import_basis_v672199.php

"$WP_CLI" eval '
if (!class_exists("Pferdeportal_Affiliate_Router")) {
    fwrite(STDERR, "FAIL plugin_not_loaded\n");
    exit(2);
}
if (Pferdeportal_Affiliate_Router::VERSION !== "6.72.199") {
    fwrite(STDERR, "FAIL wrong_version ".Pferdeportal_Affiliate_Router::VERSION."\n");
    exit(2);
}
echo "PASS exact_6_72_199_plugin_loaded\n";
' --path="$WP_PATH"

python3 - "$REPO_ROOT" "$WP_PATH" <<'PY'
from pathlib import Path
import hashlib, sys

repo = Path(sys.argv[1])
wp = Path(sys.argv[2])
manifest = repo / 'release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt'
source_container = repo / 'release/affiliate-zentrale/current'
installed_root = wp / 'wp-content/plugins/affiliate-portal-router'

if not manifest.is_file():
    raise SystemExit('FAIL source_manifest_missing')
if not installed_root.is_dir():
    raise SystemExit('FAIL installed_plugin_root_missing')

expected = {}
for raw in manifest.read_text(encoding='utf-8').splitlines():
    if not raw.strip():
        continue
    digest, rel = raw.split(None, 1)
    expected[rel.strip()] = digest

installed = {}
for p in installed_root.rglob('*'):
    if p.is_file():
        rel = 'affiliate-portal-router/' + p.relative_to(installed_root).as_posix()
        installed[rel] = hashlib.sha256(p.read_bytes()).hexdigest()

if set(installed) != set(expected):
    missing = sorted(set(expected) - set(installed))
    extra = sorted(set(installed) - set(expected))
    raise SystemExit('FAIL installed_source_file_list missing=' + ','.join(missing) + ' extra=' + ','.join(extra))

bad = [rel for rel, digest in expected.items() if installed.get(rel) != digest]
if bad:
    raise SystemExit('FAIL installed_source_hash ' + ','.join(sorted(bad)))

print(f'PASS installed_plugin_byte_identity_{len(expected)}_of_{len(expected)}')
PY

tests=(
  "release/affiliate-zentrale/evidence/worktests/test_adcell_banner_import_basis_e2e_v672199.php"
  "release/affiliate-zentrale/evidence/worktests/test_adcell_banner_basis_upgrade_v672199_e2e.php"
  "release/affiliate-zentrale/evidence/worktests/test_direct_partner_manual_banner_v672199_e2e.php"
)

for test_file in "${tests[@]}"; do
  echo "RUN $test_file"
  "$WP_CLI" eval-file "$REPO_ROOT/$test_file" --path="$WP_PATH"
done

echo "AFFILIATE_6_72_199_BANNER_IMPORT_BASIS_WORDPRESS_MARIADB_COMPLETE"
