#!/usr/bin/env bash
set -euo pipefail
code=$(curl -sS -o /tmp/home -w '%{http_code}' http://127.0.0.1:8080/glossar/); test "$code" = 200
python3 - <<'PY'
import re
s=open('/tmp/home',encoding='utf8').read()
print('DIAG_HOME_LEN',len(s))
print('DIAG_HAS_UGE', 'class="uge"' in s)
print('DIAG_HAS_HERO_CLASS', 'class="uge-hero' in s)
print('DIAG_HAS_EMBEDDED_HERO', 'glossar-hero-books-stall.webp' in s)
print('DIAG_H1_COUNT',len(re.findall(r'<h1(?:\s|>)',s,re.I)))
for needle in ['uge-hero','glossar-hero-books-stall.webp','uge-tools','uge-topic-grid']:
    i=s.find(needle); print('DIAG_POS',needle,i, s[max(0,i-180):i+280] if i>=0 else '')
assert len(re.findall(r'<h1(?:\s|>)',s,re.I)) == 1
assert 'glossar-hero-books-stall.webp' in s
assert 'site-content .ast-container{padding-top:0' not in s
grid=re.search(r'<nav class="uge-topic-grid"[^>]*>(.*?)</nav>',s,re.S); assert grid
a=grid.group(1)
labels=['Rassen &amp; Zucht','Anatomie','Gesundheit','Haltung &amp; Fütterung','Verhalten','Reiten &amp; Ausbildung','Pferdesport','Ausrüstung &amp; Stall','Geschichte &amp; Kultur','Kauf, Recht &amp; Versicherung']
for x in labels: assert x in a,x
assert '>Glossar<' not in a
assert a.count('class="uge-topic-icon"') == 10
assert 'justify-items:center' in s
assert 'q.length<2' in s
assert 'AD-home_banner' in s
print('HOME_10_ICONS_LAYOUT_PASS')
PY
asset=$(grep -oE 'https?[^" ]+glossar-hero-books-stall\.webp' /tmp/home | head -1); test -n "$asset"
curl -fsS "$asset" -o /tmp/hero.webp
test "$(sha256sum /tmp/hero.webp | cut -d' ' -f1)" = 85594735583ee25d318b6a7a98dfdcae2097e95b708107db5feb62edcf3fbdda
nonce=$(python3 - <<'PY'
import re
s=open('/tmp/home',encoding='utf8').read(); m=re.search(r'data-uge-nonce="([^"]+)"',s); assert m; print(m.group(1))
PY
)
curl -fsS -X POST http://127.0.0.1:8080/wp-admin/admin-ajax.php --data action=uge_search --data-urlencode nonce="$nonce" --data-urlencode q=Hu -o /tmp/ajax.json
grep -q Hufbein /tmp/ajax.json; grep -q Hufpflege /tmp/ajax.json
! grep -q SHORT-HUFBEIN-SENTINEL /tmp/ajax.json
! grep -q FULL-HUFBEIN-SENTINEL /tmp/ajax.json
! grep -q NORMAL-POST-SENTINEL /tmp/ajax.json
! grep -q Hufentwurf /tmp/ajax.json
! grep -q 'uge-card' /tmp/ajax.json
bad=$(curl -sS -o /tmp/bad -w '%{http_code}' -X POST http://127.0.0.1:8080/wp-admin/admin-ajax.php --data action=uge_search --data nonce=bad --data q=Hu); test "$bad" != 200
test "$(curl -sS -o /tmp/term -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufbein/)" = 200
grep -q FULL-HUFBEIN-SENTINEL /tmp/term
grep -q 'Startseite' /tmp/term; grep -q 'Glossar' /tmp/term; grep -q 'Gesundheit' /tmp/term; grep -q 'Hufbein' /tmp/term
grep -q 'AD-top' /tmp/term; grep -q 'AD-inline' /tmp/term; grep -q 'AD-bottom' /tmp/term
test "$(curl -sS -o /tmp/missing -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/nicht-da/)" = 404
test "$(curl -sS -o /tmp/old -w '%{http_code}' http://127.0.0.1:8080/glossar/hufbein/)" = 301
test "$(curl -sS -o /tmp/cat -w '%{http_code}' http://127.0.0.1:8080/glossar/gesundheit/)" = 200
grep -q 'Startseite' /tmp/cat; grep -q 'Glossar' /tmp/cat; grep -q 'Gesundheit' /tmp/cat
grep -q '/glossar/begriff/hufbein/' /tmp/cat
test "$(curl -sS -o /tmp/rassen -w '%{http_code}' http://127.0.0.1:8080/glossar/rassen-zucht/)" = 200
grep -q Aalstrich /tmp/rassen
echo UGE025_FRONTEND_POSITIVE_NEGATIVE_PASS
