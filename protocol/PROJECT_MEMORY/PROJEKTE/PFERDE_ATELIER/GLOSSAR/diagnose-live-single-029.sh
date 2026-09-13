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

echo '=== UGE BREADCRUMB / TOP SPACING ==='
grep -nE 'render_breadcrumbs|uge-breadcrumbs|uge-glossary-home #primary|uge-glossary-category #primary|uge-glossary-term #primary' "$P/includes/class-uge-frontend.php" || true

bash "$R/reconstruct-design-1.50.469.sh"
D=/tmp/design-1.50.469/pferde-template-kit.php
echo '=== REAL DESIGN BREADCRUMB FUNCTIONS / CSS ==='
grep -niE -A24 -B12 'breadcrumb|breadcrumbs' "$D" | head -n 900 || true
