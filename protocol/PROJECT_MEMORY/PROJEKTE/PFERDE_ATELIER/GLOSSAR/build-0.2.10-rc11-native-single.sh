#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.10-rc7.sh"
rm -rf /tmp/uge0210rc11
cp -a /tmp/uge0210rc7 /tmp/uge0210rc11
P=/tmp/uge0210rc11/universal-glossary-engine
python3 - <<'PY'
from pathlib import Path

p=Path('/tmp/uge0210rc11/universal-glossary-engine/universal-glossary-engine.php')
s=p.read_text()
assert s.count('Version: 0.2.10-rc7')==1
assert s.count("define('UGE_VERSION', '0.2.10-rc7');")==1
s=s.replace('Version: 0.2.10-rc7','Version: 0.2.10-rc11-native-single')
s=s.replace("define('UGE_VERSION', '0.2.10-rc7');","define('UGE_VERSION', '0.2.10-rc11-native-single');")
p.write_text(s)

# FSE/Kubio fix: never replace a singular glossary request with a classic PHP
# document template that calls get_header()/get_footer(). Let the active theme/FSE
# template own the document shell and render the uge_term post natively.
p=Path('/tmp/uge0210rc11/universal-glossary-engine/includes/class-uge-frontend.php')
s=p.read_text()
old="""        if (is_singular(UGE_Core::POST_TYPE) || self::requested_term_post() instanceof WP_Post) {
            $candidate = UGE_DIR . 'templates/single-uge-term.php';
            return is_readable($candidate) ? $candidate : $template;
        }
"""
assert s.count(old)==1, s.count(old)
s=s.replace(old,'',1)
p.write_text(s)
PY

grep -q 'Version: 0.2.10-rc11-native-single' "$P/universal-glossary-engine.php"
grep -q "define('UGE_VERSION', '0.2.10-rc11-native-single');" "$P/universal-glossary-engine.php"
# Taxonomy rendering stays exactly under UGE control.
grep -q "templates/taxonomy-uge-group.php" "$P/includes/class-uge-frontend.php"
# Singular rendering must no longer select the classic UGE full-document template.
! grep -q "templates/single-uge-term.php" "$P/includes/class-uge-frontend.php"
# rc7 routing/content contracts are intentionally preserved.
grep -q "add_action('parse_request', \[__CLASS__, 'bind_explicit_request'\], 1);" "$P/includes/class-uge-core.php"
grep -q 'resolve_related_term' "$P/includes/class-uge-frontend.php"
grep -q 'render_design_breadcrumb_payload' "$P/includes/class-uge-frontend.php"
find "$P" -name '*.php' -print0 | xargs -0 -n1 php -l

echo UGE0210RC11_NATIVE_SINGLE_BUILD_PASS
