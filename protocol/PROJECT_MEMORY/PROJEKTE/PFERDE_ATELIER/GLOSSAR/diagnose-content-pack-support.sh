#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.10-rc1.sh"
P=/tmp/uge0210rc1/universal-glossary-engine
for f in "$P"/includes/class-uge-transfer.php "$P"/includes/class-uge-admin.php "$P"/includes/class-uge-core.php; do
  echo "=== $f ==="
  grep -nEi 'import|export|json|wp_insert_post|wp_update_post|term_value|update_post_meta|set_object_terms|wp_set_object_terms' "$f" || true
done
