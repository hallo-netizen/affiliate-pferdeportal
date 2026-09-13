#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.10-rc6.sh"
rm -rf /tmp/uge0210rc6boot
cp -a /tmp/uge0210rc6 /tmp/uge0210rc6boot
SRC="$R/exact-0.2.6-test/02_boot.sh"
sed -e 's#/tmp/uge026#/tmp/uge0210rc6boot#g' -e 's/0\.2\.6/0.2.10-rc6/g' -e 's/UGE026/UGE0210RC6/g' -e 's/uge026/uge0210rc6/g' "$SRC" > /tmp/boot-0210-rc6.sh
chmod +x /tmp/boot-0210-rc6.sh
bash /tmp/boot-0210-rc6.sh
bash "$R/exact-0.2.5-test/03_seed.sh"

# Preserve the complete historical frontend contract, but bind its breadcrumb
# assertions to the new Pferde Design breadcrumb class. All non-breadcrumb checks
# remain byte-for-byte the old regression.
sed 's/uge-breadcrumbs/pftk-content-breadcrumb/g' "$R/exact-0.2.5-test/04_frontend.sh" > /tmp/frontend-0210-rc6.sh
chmod +x /tmp/frontend-0210-rc6.sh
bash /tmp/frontend-0210-rc6.sh
bash "$R/exact-0.2.5-test/05_regression.sh"

test "$(docker exec wp wp plugin list --name=universal-glossary-engine --field=version --allow-root)" = 0.2.10-rc6

# Trigger atomic cluster after seed created the Gesundheit taxonomy target.
docker exec wp wp option delete uge_pferde_content_pack_0210 --allow-root >/dev/null 2>&1 || true
docker exec wp wp eval --allow-root 'UGE_Pferde_Content_Pack::maybe_install();'
test "$(docker exec wp wp option get uge_pferde_content_pack_0210 --allow-root)" = done

for slug in hufrehe strahlfaeule hufabszess; do
  ID=$(docker exec wp wp post list --allow-root --post_type=uge_term --name="$slug" --post_status=publish --field=ID)
  test -n "$ID"
  HTML=$(docker exec wp wp post get "$ID" --allow-root --field=post_content)
  printf '%s' "$HTML" | grep -q '/glossar/gesundheit/'
  if printf '%s' "$HTML" | grep -Eqi '<h[2-6][ >]'; then echo UNNEEDED_SUBHEADING_FOUND:$slug >&2; exit 1; fi
  case "$slug" in
    hufrehe) A=strahlfaeule; B=hufabszess;;
    strahlfaeule) A=hufrehe; B=hufabszess;;
    hufabszess) A=hufrehe; B=strahlfaeule;;
  esac
  printf '%s' "$HTML" | grep -q "/glossar/begriff/$A/"
  printf '%s' "$HTML" | grep -q "/glossar/begriff/$B/"
  test "$(curl -sS -o /tmp/$slug -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/$slug/)" = 200
  grep -q 'class="uge-related-links"' /tmp/$slug
  grep -q "/glossar/begriff/$A/" /tmp/$slug
  grep -q "/glossar/begriff/$B/" /tmp/$slug
  grep -q 'class="uge-glossary-category-link"' /tmp/$slug
  grep -q '/glossar/gesundheit/' /tmp/$slug
  grep -q 'id="uge-pftk-breadcrumb-payload"' /tmp/$slug
  ! grep -q 'class="uge-breadcrumbs"' /tmp/$slug
done

test "$(curl -sS -o /tmp/cat-rc6 -w '%{http_code}' http://127.0.0.1:8080/glossar/gesundheit/)" = 200
grep -q 'id="uge-pftk-breadcrumb-payload"' /tmp/cat-rc6
! grep -q 'class="uge-breadcrumbs"' /tmp/cat-rc6

PACK=$(docker exec wp wp post list --allow-root --post_type=uge_term --post_status=publish --fields=post_title,post_content --format=json)
if printf '%s' "$PACK" | grep -Eqi 'haflinger|friese|hannoveraner|trakehner|isländer|islaender|fjordpferd|quarter horse'; then
  echo HORSE_BREED_LEAK_IN_GLOSSARY >&2; exit 1
fi

curl -fsS http://127.0.0.1:8080/glossar/ -o /tmp/home-rc6
! grep -Fq 'Begriffe schnell finden, fachlich einordnen und verständlich nachschlagen.' /tmp/home-rc6

echo UGE0210RC6_OLD_REGRESSION_PASS
echo UGE0210RC6_RELATED_CLUSTER_LINKS_PASS
echo UGE0210RC6_PFERDE_BREADCRUMB_PAYLOAD_SERVER_PASS
echo UGE0210RC6_NO_HORSE_BREEDS_PASS
