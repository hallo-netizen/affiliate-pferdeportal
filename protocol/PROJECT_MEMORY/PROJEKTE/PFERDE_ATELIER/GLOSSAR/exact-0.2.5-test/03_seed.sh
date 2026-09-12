#!/usr/bin/env bash
set -euo pipefail
G=$(docker exec wp wp post create --allow-root --post_type=page --post_status=publish --post_title=Glossar --post_name=glossar --post_excerpt='Pferdebegriffe verständlich erklärt.' --porcelain)
HEALTH=$(docker exec wp wp post create --allow-root --post_type=page --post_status=publish --post_title=Gesundheit --post_name=gesundheit --porcelain)
FEED=$(docker exec wp wp post create --allow-root --post_type=page --post_status=publish --post_title=Fütterung --post_name=fuetterung --porcelain)
docker exec wp wp post meta update "$HEALTH" _uge_test_portal_category 1 --allow-root >/dev/null
docker exec wp wp post meta update "$FEED" _uge_test_portal_category 1 --allow-root >/dev/null
docker exec wp wp eval --allow-root "\$c=UGE_Config::get();\$c['main_page_id']=$G;\$c['rewrite_base']='glossar';\$c['term_segment']='begriff';\$c['design_profile']='auto';update_option(UGE_Config::OPTION,UGE_Config::sanitize(\$c));UGE_Core::register_content();UGE_Core::ensure_navigation_groups();flush_rewrite_rules();"
docker exec wp wp term create uge_group 'Farben & Genetik' --slug=farben-genetik --allow-root >/dev/null
docker exec wp wp term create uge_group 'Huf & Gliedmaßen' --slug=huf-gliedmassen --allow-root >/dev/null
MISSING=$(docker exec wp wp post create --allow-root --post_type=uge_term --post_status=draft --post_title='Ohne Kategorie' --post_name=ohne-kategorie --post_content='MISSING-CONTENT' --porcelain)
docker exec wp wp post update "$MISSING" --post_status=publish --allow-root >/dev/null
test "$(docker exec wp wp post get "$MISSING" --field=post_status --allow-root)" = draft
INVALID=$(docker exec wp wp post create --allow-root --post_type=uge_term --post_status=draft --post_title='Falsches Ziel' --post_name=falsches-ziel --post_content='INVALID-CONTENT' --porcelain)
docker exec wp wp post meta update "$INVALID" _uge_primary_category_id 999999 --allow-root >/dev/null
docker exec wp wp post update "$INVALID" --post_status=publish --allow-root >/dev/null
test "$(docker exec wp wp post get "$INVALID" --field=post_status --allow-root)" = draft
A=$(docker exec wp wp post create --allow-root --post_type=uge_term --post_status=draft --post_title=Aalstrich --post_name=aalstrich --post_content='FULL-AALSTRICH-SENTINEL' --porcelain)
H=$(docker exec wp wp post create --allow-root --post_type=uge_term --post_status=draft --post_title=Hufbein --post_name=hufbein --post_content='FULL-HUFBEIN-SENTINEL' --porcelain)
HP=$(docker exec wp wp post create --allow-root --post_type=uge_term --post_status=draft --post_title=Hufpflege --post_name=hufpflege --post_content='FULL-HUFPFLEGE-SENTINEL' --porcelain)
SAME=$(docker exec wp wp post create --allow-root --post_type=uge_term --post_status=draft --post_title=Gesundheit --post_name=gesundheit --post_content='CATEGORY-OVERLAP-SENTINEL' --porcelain)
D=$(docker exec wp wp post create --allow-root --post_type=uge_term --post_status=draft --post_title=Hufentwurf --post_name=hufentwurf --post_content='DRAFT-SENTINEL' --porcelain)
for id in "$A" "$H" "$HP" "$SAME" "$D"; do docker exec wp wp post meta update "$id" _uge_primary_category_id "$HEALTH" --allow-root >/dev/null; done
docker exec wp wp post meta update "$H" _uge_short_definition 'SHORT-HUFBEIN-SENTINEL' --allow-root >/dev/null
docker exec wp wp post meta update "$H" _uge_synonyms 'Hufknochen' --allow-root >/dev/null
docker exec wp wp post term add "$A" uge_group 'Farben & Genetik' --allow-root >/dev/null
docker exec wp wp post term add "$H" uge_group 'Huf & Gliedmaßen' --allow-root >/dev/null
docker exec wp wp post term add "$HP" uge_group 'Huf & Gliedmaßen' --allow-root >/dev/null
for id in "$A" "$H" "$HP" "$SAME"; do docker exec wp wp post update "$id" --post_status=publish --allow-root >/dev/null; done
test "$(docker exec wp wp post get "$SAME" --field=post_status --allow-root)" = publish
NORMAL=$(docker exec wp wp post create --allow-root --post_type=post --post_status=publish --post_title='Huf normaler Beitrag' --post_content='NORMAL-POST-SENTINEL' --porcelain)
test "$(docker exec wp wp post get "$NORMAL" --field=post_status --allow-root)" = publish
docker exec wp wp option delete uge_navigation_group_migration_v1 --allow-root >/dev/null 2>&1 || true
docker exec wp wp eval --allow-root 'UGE_Core::migrate_legacy_navigation_groups(); flush_rewrite_rules();'
echo "$D" >/tmp/draftid
echo UGE025_POLICY_AND_SEED_PASS
