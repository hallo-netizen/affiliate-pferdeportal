#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.9.sh"
P=/tmp/uge029/universal-glossary-engine
F="$P/includes/class-uge-frontend.php"
C="$P/includes/class-uge-core.php"

echo '=== FRONTEND HOOKS / SINGLE FUNCTIONS ==='
grep -nE "template_include|the_content|is_singular|render_single|single-wrap|get_queried_object|get_post\(" "$F" || true

echo '=== CORE ROUTING / POST TYPE ==='
grep -nE "register_post_type|rewrite|query_var|parse_request|bind_explicit_request|POST_TYPE" "$C" || true

echo '=== TEMPLATES EXACT ==='
for t in "$P"/templates/*.php; do echo "--- $t ---"; nl -ba "$t"; done

echo '=== FRONTEND SELECTED FUNCTIONS EXACT ==='
python3 - "$F" <<'PY'
from pathlib import Path
import sys,re
p=Path(sys.argv[1]); s=p.read_text(); lines=s.splitlines()
for name in ['render_breadcrumbs','render_single','render_hero','render_category_page']:
    m=re.search(r'\n\s*(?:public|private) static function '+re.escape(name)+r'\b.*?(?=\n\s*(?:public|private) static function |\n\})',s,re.S)
    print('\n=== '+name+' ===')
    print(m.group(0) if m else 'NOT_FOUND')
PY

echo '=== HERO TEXT SOURCES ==='
grep -RniF 'Begriffe schnell finden, fachlich einordnen und verständlich nachschlagen.' "$P" || true
grep -RniE "post_content|render_hero|hero.*content|description" "$F" || true

echo '=== BREADCRUMB AND SPACING CSS ==='
grep -oE '\.uge-breadcrumbs\{[^}]*\}|body\.uge-glossary-(home|category|term)[^}]*\}|\.uge\{[^}]*\}|\.uge-single-wrap\{[^}]*\}' "$F" || true

echo DIAGNOSE_LIVE_SINGLE_029_DONE
