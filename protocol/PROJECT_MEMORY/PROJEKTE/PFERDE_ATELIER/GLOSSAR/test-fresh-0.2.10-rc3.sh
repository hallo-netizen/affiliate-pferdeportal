#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.10-rc4.sh"
rm -rf /tmp/uge0210rc4boot
cp -a /tmp/uge0210rc4 /tmp/uge0210rc4boot
SRC="$R/exact-0.2.6-test/02_boot.sh"
sed -e 's#/tmp/uge026#/tmp/uge0210rc4boot#g' -e 's/0\.2\.6/0.2.10-rc4/g' -e 's/UGE026/UGE0210RC4/g' -e 's/uge026/uge0210rc4/g' "$SRC" > /tmp/boot-0210-rc4.sh
chmod +x /tmp/boot-0210-rc4.sh
bash /tmp/boot-0210-rc4.sh
bash "$R/exact-0.2.5-test/03_seed.sh"
bash "$R/exact-0.2.5-test/04_frontend.sh"
bash "$R/exact-0.2.5-test/05_regression.sh"

test "$(docker exec wp wp plugin list --name=universal-glossary-engine --field=version --allow-root)" = 0.2.10-rc4

# Trigger pack only after seed has marked Gesundheit as a real portal category.
docker exec wp wp option delete uge_pferde_content_pack_0210 --allow-root >/dev/null 2>&1 || true
docker exec wp wp eval --allow-root 'UGE_Pferde_Content_Pack::maybe_install();'
test "$(docker exec wp wp option get uge_pferde_content_pack_0210 --allow-root)" = done

# Every related term in the pack exists now, is published now, and each article
# has direct inline links to BOTH related terms plus the category.
for slug in hufrehe strahlfaeule hufabszess; do
  ID=$(docker exec wp wp post list --allow-root --post_type=uge_term --name="$slug" --post_status=publish --field=ID)
  test -n "$ID"
  HTML=$(docker exec wp wp post get "$ID" --allow-root --field=post_content)
  printf '%s' "$HTML" | grep -q '/glossar/gesundheit/'
  if printf '%s' "$HTML" | grep -Eqi '<h[2-6][ >]'; then echo UNNEEDED_SUBHEADING_FOUND:$slug >&2; exit 1; fi
  REL=$(docker exec wp wp eval --allow-root "echo UGE_Core::term_value($ID,'related_terms');")
  test -n "$REL"
  case "$slug" in
    hufrehe) A=strahlfaeule; B=hufabszess;;
    strahlfaeule) A=hufrehe; B=hufabszess;;
    hufabszess) A=hufrehe; B=strahlfaeule;;
  esac
  printf '%s' "$HTML" | grep -q "/glossar/begriff/$A/"
  printf '%s' "$HTML" | grep -q "/glossar/begriff/$B/"
  test "$(curl -sS -o /tmp/$slug -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/$slug/)" = 200
  grep -q 'class="uge-primary-category"' /tmp/$slug
  grep -q '<strong>Verwandte Begriffe:</strong>' /tmp/$slug
  grep -q "/glossar/begriff/$A/" /tmp/$slug
  grep -q "/glossar/begriff/$B/" /tmp/$slug
done

# Pferderassen remain forbidden in Glossar content packs.
PACK=$(docker exec wp wp post list --allow-root --post_type=uge_term --post_status=publish --fields=post_title,post_content --format=json)
if printf '%s' "$PACK" | grep -Eqi 'haflinger|friese|hannoveraner|trakehner|isländer|islaender|fjordpferd|quarter horse'; then
  echo HORSE_BREED_LEAK_IN_GLOSSARY >&2; exit 1
fi

# Old rejected fallback text stays absent.
curl -fsS http://127.0.0.1:8080/glossar/ -o /tmp/home
! grep -Fq 'Begriffe schnell finden, fachlich einordnen und verständlich nachschlagen.' /tmp/home

echo UGE0210RC4_RELATED_CLUSTER_ATOMIC_PASS
echo UGE0210RC4_RELATED_LINKS_AND_CATEGORY_LINK_PASS
echo UGE0210RC4_NO_UNNEEDED_SUBHEADINGS_PASS
echo UGE0210RC4_NO_HORSE_BREEDS_PASS
