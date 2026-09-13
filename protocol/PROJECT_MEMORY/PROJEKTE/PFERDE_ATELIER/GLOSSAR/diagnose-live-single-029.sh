#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.9.sh"
P=/tmp/uge029/universal-glossary-engine
C="$P/includes/class-uge-core.php"
POL="$P/includes/class-uge-policy.php"
echo '=== PRIMARY CATEGORY TARGET CONTRACT ==='
grep -nA45 -B3 'function primary_category_target' "$C"
echo '=== PRIMARY CATEGORY OUTPUT CONTRACT ==='
grep -nA30 -B3 'function append_primary_category_link' "$POL"
