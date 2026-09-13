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

echo '=== FRONTEND AROUND SINGLE ==='
python3 - "$F" <<'PY'
from pathlib import Path
import sys,re
p=Path(sys.argv[1]); lines=p.read_text().splitlines()
need=('render_single','uge-single-wrap','template_include','the_content')
hits=sorted({i for i,l in enumerate(lines) if any(x in l for x in need)})
seen=set()
for i in hits:
    a=max(0,i-35); b=min(len(lines),i+80)
    key=(a,b)
    if key in seen: continue
    seen.add(key)
    print(f'--- lines {a+1}-{b} ---')
    for n in range(a,b): print(f'{n+1:04d}: {lines[n]}')
PY

echo '=== HERO TEXT SOURCES ==='
grep -RniF 'Begriffe schnell finden, fachlich einordnen und verständlich nachschlagen.' "$P" || true
grep -RniE "post_content|render_hero|hero.*content|description" "$F" || true

echo DIAGNOSE_LIVE_SINGLE_029_DONE
