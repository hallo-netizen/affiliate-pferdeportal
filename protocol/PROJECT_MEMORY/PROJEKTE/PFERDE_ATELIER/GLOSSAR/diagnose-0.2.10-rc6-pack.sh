#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.10-rc6.sh"
rm -rf /tmp/uge0210rc6diag
cp -a /tmp/uge0210rc6 /tmp/uge0210rc6diag
SRC="$R/exact-0.2.6-test/02_boot.sh"
sed -e 's#/tmp/uge026#/tmp/uge0210rc6diag#g' -e 's/0\.2\.6/0.2.10-rc6/g' -e 's/UGE026/UGE0210RC6DIAG/g' -e 's/uge026/uge0210rc6diag/g' "$SRC" > /tmp/boot-0210-rc6diag.sh
chmod +x /tmp/boot-0210-rc6diag.sh
bash /tmp/boot-0210-rc6diag.sh
bash "$R/exact-0.2.5-test/03_seed.sh"

echo '=== PRECONDITIONS ==='
docker exec wp wp eval --allow-root '
echo "PACK_CLASS=".(class_exists("UGE_Pferde_Content_Pack",false)?"1":"0").PHP_EOL;
echo "DESIGN_CLASS=".(class_exists("Pferde_Template_Kit",false)?"1":"0").PHP_EOL;
echo "POST_TYPE=".(post_type_exists(UGE_Core::POST_TYPE)?"1":"0").PHP_EOL;
echo "TAX=".(taxonomy_exists(UGE_Core::TAXONOMY)?"1":"0").PHP_EOL;
$g=get_term_by("slug","gesundheit",UGE_Core::TAXONOMY); echo "GROUP="; var_export($g instanceof WP_Term ? [$g->term_id,$g->slug,$g->name] : null); echo PHP_EOL;
foreach(["hufrehe","strahlfaeule","hufabszess"] as $slug){$p=get_page_by_path($slug,OBJECT,UGE_Core::POST_TYPE);echo strtoupper($slug)."=";var_export($p instanceof WP_Post?[$p->ID,$p->post_status,get_post_meta($p->ID,"_uge_pack_0210_owned",true)]:null);echo PHP_EOL;}
echo "OPTION=".get_option("uge_pferde_content_pack_0210","MISSING").PHP_EOL;
'

docker exec wp wp option delete uge_pferde_content_pack_0210 --allow-root >/dev/null 2>&1 || true
docker exec wp wp eval --allow-root 'UGE_Pferde_Content_Pack::maybe_install(); echo "MANUAL_DONE\n";'

echo '=== AFTER MANUAL ==='
docker exec wp wp eval --allow-root '
echo "OPTION=".get_option("uge_pferde_content_pack_0210","MISSING").PHP_EOL;
foreach(["hufrehe","strahlfaeule","hufabszess"] as $slug){$p=get_page_by_path($slug,OBJECT,UGE_Core::POST_TYPE);echo strtoupper($slug)."=";var_export($p instanceof WP_Post?[$p->ID,$p->post_status,get_post_meta($p->ID,"_uge_pack_0210_owned",true),wp_get_post_terms($p->ID,UGE_Core::TAXONOMY,["fields"=>"slugs"])]:null);echo PHP_EOL;}
'

echo RC6_PACK_DIAG_DONE
