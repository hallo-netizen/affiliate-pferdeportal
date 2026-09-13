#!/usr/bin/env bash
set -euo pipefail

F=/tmp/u/universal-glossary-engine/includes/class-uge-frontend.php
HOME_URL=http://127.0.0.1:8080/glossar/

# 1) A rendered card link is only valid when it resolves to a real glossary article,
# not merely to an HTTP-200 blank/foreign page.
curl -fsS "$HOME_URL" -o /tmp/accept-home
python3 - <<'PY'
import re
s=open('/tmp/accept-home',encoding='utf8').read()
links=sorted(set(re.findall(r'href="(http://127\.0\.0\.1:8080/glossar/begriff/[^\"]+/)"',s)))
assert links, 'no glossary term links on home'
open('/tmp/accept-term-links','w').write('\n'.join(links)+'\n')
PY
while IFS= read -r url; do
  code=$(curl -sS -o /tmp/accept-term -w '%{http_code}' "$url")
  test "$code" = 200
  grep -q '<article class="uge-single-wrap"' /tmp/accept-term
  grep -q '<h1' /tmp/accept-term
  ! grep -qiE 'fatal error|critical error' /tmp/accept-term
done </tmp/accept-term-links

echo UGE025_ACCEPT_REAL_TERM_PAGE_PASS

# 2) The glossary home owns removal of Astra's desktop #primary top margin.
# This must be narrowly scoped to the glossary home only.
grep -Fq 'body.uge-glossary-home.ast-plain-container.ast-no-sidebar #primary{margin-top:0!important' "$F"

# 3) Glossary breadcrumbs must follow the Pferde-Atelier breadcrumb axis/typography,
# not the 1320px glossary content axis.
grep -Fq 'width:min(calc(100vw - 32px),var(--pftk-breadcrumb-axis-width,900px))' "$F"
grep -Fq 'font-size:14px' "$F"

# 4) Mobile hero image must size from the viewport/container, not from a fixed 240px height.
! grep -Fq '.uge-hero-image{position:relative!important;order:1;height:240px!important' "$F"
grep -Fq '.uge-hero-image{position:relative!important;order:1;width:100%!important;max-width:100%!important;height:auto!important;aspect-ratio:16/9' "$F"

echo UGE025_FRONTEND_ACCEPTANCE_PASS
