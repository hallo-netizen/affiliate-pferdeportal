#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.9.sh"
P=/tmp/uge029/universal-glossary-engine
F="$P/includes/class-uge-frontend.php"
C="$P/includes/class-uge-core.php"

echo '=== TEMPLATES EXACT ==='
for t in "$P"/templates/*.php; do echo "--- $t ---"; nl -ba "$t"; done

echo '=== PRIMARY CATEGORY / CONTENT FILTERS ==='
grep -RniE 'uge-primary-category|primary_category|the_content|in_the_loop|is_main_query' "$P" || true

echo '=== HERO TEXT SOURCES ==='
grep -RniF 'Begriffe schnell finden, fachlich einordnen und verständlich nachschlagen.' "$P" || true

echo '=== BREADCRUMB AND SPACING CSS ==='
grep -oE '\.uge-breadcrumbs\{[^}]*\}|body\.uge-glossary-(home|category|term)[^}]*\}|\.uge\{[^}]*\}|\.uge-single-wrap\{[^}]*\}' "$F" || true

echo DIAGNOSE_LIVE_SINGLE_029_DONE
