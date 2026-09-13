#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.10-rc4.sh"
P=/tmp/uge0210rc4/universal-glossary-engine
T="$P/templates/single-uge-term.php"
echo '=== SINGLE TEMPLATE ==='
nl -ba "$T"
echo '=== RELATED CONTRACT ==='
grep -RniE 'related_terms|Verwandte|verwandt|primary-category' "$P" || true
echo '=== FIELD SCHEMA ==='
grep -nA100 -B10 'field_schema' "$P/includes/class-uge-config.php" || true
