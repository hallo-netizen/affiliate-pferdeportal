#!/usr/bin/env bash
set -euo pipefail
code=$(curl -sS -o /tmp/home -w '%{http_code}' http://127.0.0.1:8080/glossar/); test "$code" = 200
python3 - <<'PY'
import re
s=open('/tmp/home',encoding='utf8').read()
assert len(re.findall(r'<h1(?:\s|>)',s,re.I)) == 1
assert 'glossar-hero-books-stall.webp' in s
assert 'site-content .ast-container{padding-top:0' not in s
assert 'entry-content{margin-top:0!important;padding-top:0!important}' not in s
grid=re.search(r'<nav class="uge-topic-grid"[^>]*>(.*?)</nav>',s,re.S); assert grid
a=grid.group(1)
labels=['Rassen &amp; Zucht','Anatomie','Gesundheit','Haltung &amp; Fütterung','Verhalten','Reiten &amp; Ausbildung','Pferdesport','Ausrüstung &amp; Stall','Geschichte &amp; Kultur','Kauf, Recht &amp; Versicherung']
for x in labels: assert x in a,x
assert '>Glossar<' not in a
assert 'Farben &amp; Genetik' not in a
assert 'Huf &amp; Gliedmaßen' not in a
assert a.count('class="uge-topic-icon"') == 10
assert 'justify-items:center' in s
assert 'q.length<2' in s
assert 'AD-home_banner' in s
# Every rendered glossary-term and topic link on the home page must point to the expected glossary routes.
links=sorted(set(re.findall(r'href="(http://127\.0\.0\.1:8080/glossar/begriff/[^\"]+/)"',s)))
assert links, 'no glossary term links on home'
open('/tmp/home-term-links','w').write('\n'.join(links)+'\n')
topics=sorted(set(re.findall(r'<a class="uge-topic[^\"]*" href="(http://127\.0\.0\.1:8080/glossar/[^\"]+/)"',a)))
assert len(topics)==10, topics
open('/tmp/home-topic-links','w').write('\n'.join(topics)+'\n')
print('HOME_10_ICONS_LAYOUT_PASS')
PY
asset=$(grep -oE 'https?[^" ]+glossar-hero-books-stall\.webp' /tmp/home | head -1); test -n "$asset"
curl -fsS "$asset" -o /tmp/hero.webp
test "$(sha256sum /tmp/hero.webp | cut -d' ' -f1)" = 85594735583ee25d318b6a7a98dfdcae2097e95b708107db5feb62edcf3fbdda
while IFS= read -r url; do test "$(curl -sS -o /dev/null -w '%{http_code}' "$url")" = 200; done </tmp/home-term-links
while IFS= read -r url; do test "$(curl -sS -o /dev/null -w '%{http_code}' "$url")" = 200; done </tmp/home-topic-links
echo UGE025_ALL_RENDERED_HOME_LINKS_PASS
nonce=$(python3 - <<'PY'
import re
s=open('/tmp/home',encoding='utf8').read(); m=re.search(r'data-uge-nonce="([^"]+)"',s); assert m; print(m.group(1))
PY
)
curl -fsS -X POST http://127.0.0.1:8080/wp-admin/admin-ajax.php --data action=uge_search --data-urlencode nonce="$nonce" --data-urlencode q=Hu -o /tmp/ajax.json
python3 - <<'PY'
import json
j=json.load(open('/tmp/ajax.json'))
assert j['success'] is True
d=j['data']; assert set(d.keys())=={'count','items'}, d.keys()
assert d['count']==len(d['items'])
assert all(set(x.keys())=={'title','url'} for x in d['items'])
titles=[x['title'] for x in d['items']]
assert 'Hufbein' in titles and 'Hufpflege' in titles
assert all('/glossar/begriff/' in x['url'] for x in d['items'])
PY
! grep -q SHORT-HUFBEIN-SENTINEL /tmp/ajax.json
! grep -q FULL-HUFBEIN-SENTINEL /tmp/ajax.json
! grep -q NORMAL-POST-SENTINEL /tmp/ajax.json
! grep -q Hufentwurf /tmp/ajax.json
! grep -q 'uge-card' /tmp/ajax.json
bad=$(curl -sS -o /tmp/bad -w '%{http_code}' -X POST http://127.0.0.1:8080/wp-admin/admin-ajax.php --data action=uge_search --data nonce=bad --data q=Hu); test "$bad" != 200
echo UGE025_AJAX_TERM_ONLY_POSITIVE_NEGATIVE_PASS
test "$(curl -sS -o /tmp/term -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufbein/)" = 200
grep -q FULL-HUFBEIN-SENTINEL /tmp/term
python3 - <<'PY'
s=open('/tmp/term',encoding='utf8').read()
pos=[s.index(x) for x in ['>Startseite</a>','>Glossar</a>','>Gesundheit</a>','>Hufbein</span>']]
assert pos==sorted(pos),pos
PY
grep -q 'AD-top' /tmp/term; grep -q 'AD-inline' /tmp/term; grep -q 'AD-bottom' /tmp/term
test "$(curl -sS -o /tmp/missing -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/nicht-da/)" = 404
test "$(curl -sS -o /tmp/old -w '%{http_code}' http://127.0.0.1:8080/glossar/hufbein/)" = 301
test "$(curl -sS -o /tmp/cat -w '%{http_code}' http://127.0.0.1:8080/glossar/gesundheit/)" = 200
python3 - <<'PY'
s=open('/tmp/cat',encoding='utf8').read()
pos=[s.index(x) for x in ['>Startseite</a>','>Glossar</a>','aria-current="page">Gesundheit</span>']]
assert pos==sorted(pos),pos
PY
grep -q '/glossar/begriff/hufbein/' /tmp/cat
# Same label is allowed: category route and glossary-term route must both remain independently reachable.
test "$(curl -sS -o /tmp/same-term -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/gesundheit/)" = 200
grep -q CATEGORY-OVERLAP-SENTINEL /tmp/same-term
! grep -q CATEGORY-OVERLAP-SENTINEL /tmp/cat
test "$(curl -sS -o /tmp/rassen -w '%{http_code}' http://127.0.0.1:8080/glossar/rassen-zucht/)" = 200
grep -q Aalstrich /tmp/rassen
echo UGE025_BREADCRUMB_ROUTE_COLLISION_PASS
echo UGE025_FRONTEND_POSITIVE_NEGATIVE_PASS
