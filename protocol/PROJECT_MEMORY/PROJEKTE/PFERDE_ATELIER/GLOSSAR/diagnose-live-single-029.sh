#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.10-rc4.sh"
P=/tmp/uge0210rc4/universal-glossary-engine
T="$P/templates/single-uge-term.php"
echo '=== FRONTEND INIT / BREADCRUMB ==='
nl -ba "$P/includes/class-uge-frontend.php" | sed -n '1,170p'
echo '=== SINGLE TEMPLATE ==='
nl -ba "$T"
echo '=== RELATED CONTRACT ==='
grep -RniE 'related_terms|Verwandte|verwandt|primary-category' "$P" || true
bash "$R/reconstruct-design-1.50.469.sh"
D=/tmp/design-1.50.469/pferde-template-kit.php
echo '=== REAL DESIGN UNIVERSAL AXIS EXACT ==='
nl -ba "$D" | sed -n '15680,15770p'
echo '=== REAL DESIGN BREADCRUMB MARKUP EXACT ==='
nl -ba "$D" | sed -n '14880,14955p'
