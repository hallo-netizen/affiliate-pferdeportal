#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
SRC="$R/test-fresh-0.2.10-rc1.sh"
sed \
  -e 's/build-0\.2\.10-rc1\.sh/build-0.2.10-rc2.sh/g' \
  -e 's/uge0210rc1/uge0210rc2/g' \
  -e 's/0\.2\.10-rc1/0.2.10-rc2/g' \
  -e 's/UGE0210RC1/UGE0210RC2/g' \
  "$SRC" > /tmp/test-fresh-0210-rc2-base.sh
chmod +x /tmp/test-fresh-0210-rc2-base.sh
bash /tmp/test-fresh-0210-rc2-base.sh

# New user rule: every new Pferde plugin release also adds genuinely new glossary
# entries. Horse breeds are forbidden here; breed data has its own system.
for slug in hufrehe strahlfaeule hufabszess; do
  ID=$(docker exec wp wp post list --allow-root --post_type=uge_term --name="$slug" --post_status=publish --field=ID)
  test -n "$ID"
  HTML=$(docker exec wp wp post get "$ID" --allow-root --field=post_content)
  test "$(printf '%s' "$HTML" | grep -o '/glossar/' | wc -l | tr -d ' ')" -ge 3
  printf '%s' "$HTML" | grep -q '/glossar/gesundheit/'
  PRIMARY=$(docker exec wp wp eval --allow-root "echo UGE_Core::term_value($ID,'primary_category_id');")
  test -n "$PRIMARY"
  test "$(docker exec wp wp post get "$PRIMARY" --allow-root --field=post_name)" = gesundheit
done

# All three must be grouped under Gesundheit and must not contain horse-breed data.
COUNT=$(docker exec wp wp post list --allow-root --post_type=uge_term --post_status=publish --name=hufrehe,strahlfaeule,hufabszess --format=count 2>/dev/null || true)
# wp-cli name does not accept a list consistently; verify individually instead.
for slug in hufrehe strahlfaeule hufabszess; do
  ID=$(docker exec wp wp post list --allow-root --post_type=uge_term --name="$slug" --post_status=publish --field=ID)
  TERMS=$(docker exec wp wp post term list "$ID" uge_group --allow-root --field=slug)
  printf '%s\n' "$TERMS" | grep -qx gesundheit
done
PACK=$(docker exec wp wp post list --allow-root --post_type=uge_term --post_status=publish --name=hufrehe --fields=post_title,post_content --format=json; docker exec wp wp post list --allow-root --post_type=uge_term --post_status=publish --name=strahlfaeule --fields=post_title,post_content --format=json; docker exec wp wp post list --allow-root --post_type=uge_term --post_status=publish --name=hufabszess --fields=post_title,post_content --format=json)
if printf '%s' "$PACK" | grep -Eqi 'haflinger|friese|hannoveraner|trakehner|isländer|islaender|fjordpferd|quarter horse'; then
  echo HORSE_BREED_LEAK_IN_GLOSSARY_PACK >&2; exit 1
fi

# One-shot and non-destructive: deleting only the pack marker and re-running init
# must not overwrite an existing glossary contribution.
HID=$(docker exec wp wp post list --allow-root --post_type=uge_term --name=hufrehe --post_status=publish --field=ID)
docker exec wp wp post update "$HID" --allow-root --post_content='PACK-NONDESTRUCTIVE-SENTINEL' >/dev/null
docker exec wp wp option delete uge_pferde_content_pack_0210 --allow-root >/dev/null
curl -fsS http://127.0.0.1:8080/glossar/ >/dev/null
test "$(docker exec wp wp post get "$HID" --allow-root --field=post_content)" = PACK-NONDESTRUCTIVE-SENTINEL
for slug in hufrehe strahlfaeule hufabszess; do
  test "$(docker exec wp wp post list --allow-root --post_type=uge_term --name="$slug" --format=count)" = 1
done
test "$(docker exec wp wp option get uge_pferde_content_pack_0210 --allow-root)" = done

echo UGE0210RC2_NEW_GLOSSARY_CONTENT_INTERNAL_LINKS_PASS
echo UGE0210RC2_NO_HORSE_BREEDS_PASS
echo UGE0210RC2_CONTENT_PACK_NONDESTRUCTIVE_IDEMPOTENT_PASS
