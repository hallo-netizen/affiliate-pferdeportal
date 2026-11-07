#!/usr/bin/env bash
set -euo pipefail
echo "E2E STEP: isolated WordPress + real MariaDB + 3 original plugin ZIPs"
sudo apt-get update -qq >/dev/null
sudo DEBIAN_FRONTEND=noninteractive apt-get install -qq -y mariadb-server php-mysql curl unzip >/dev/null
sudo service mariadb start
sudo mysql -e "CREATE DATABASE IF NOT EXISTS hd009_e2e CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; CREATE USER IF NOT EXISTS 'hd009'@'localhost' IDENTIFIED BY 'onlytest123'; GRANT ALL PRIVILEGES ON hd009_e2e.* TO 'hd009'@'localhost'; FLUSH PRIVILEGES;"
mkdir -p /tmp/hobby-real-wp
cd /tmp/hobby-real-wp
curl -fsSL -o wp-cli.phar https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
wp() { php /tmp/hobby-real-wp/wp-cli.phar --allow-root "$@"; }
wp core download --path=/tmp/hobby-real-wp/site --quiet
cd /tmp/hobby-real-wp/site
wp config create --dbname=hd009_e2e --dbuser=hd009 --dbpass=onlytest123 --dbhost=localhost --quiet
wp core install --url=http://127.0.0.1:8989 --title='Hobby Depot Isolated Test' --admin_user=e2e --admin_password=only-test-12345 --admin_email=test@example.invalid --skip-email --quiet
wp theme install twentytwentyfive --activate --quiet
mkdir -p wp-content/mu-plugins/
R="$GITHUB_WORKSPACE/protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS"
unzip -q "$R/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip" -d wp-content/plugins/
unzip -q "$R/HD-007-HOBBYREGISTER-CORE/CURRENT.zip" -d wp-content/plugins/
unzip -q "$R/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip" -d wp-content/plugins/
wp plugin activate affiliate-portal-router --quiet
wp plugin activate affiliate-portal-template-kit --quiet
wp plugin activate hd-hobbyregister-core --quiet
cat >wp-content/mu-plugins/hdar-e2e-gloss.php <<'PHP'
<?php
add_action('init',function(){ if(!post_type_exists('uge_term')) register_post_type('uge_term',array('public'=>true,'rewrite'=>array('slug'=>'glossar')));},8);
PHP
wp option update ppar_enabled 1 >/dev/null
wp option update hdar_launch_partners_v1 amazon_idealo >/dev/null
wp eval 'update_option("ppar_amazon_search_v1",array("enabled"=>1,"tracking_id"=>"hobbydepot-21"),false);'
wp rewrite structure '/%postname%/' >/dev/null
wp rewrite flush --hard --quiet || :
echo "E2E STEP: actual config"
wp eval 'echo "ppar_enabled=".get_option("ppar_enabled")." launch=".HDAR_Amazon_Start::launch_active()." amazon=".json_encode(get_option("ppar_amazon_search_v1"))." register_ready=".(HD_Hobbyregister_Core_Stable127::ready()?"yes":"no")."\n";'
PARENT=$(wp post create --post_type=page --post_title='Gestalten' --post_name=gestalten --post_status=publish --porcelain)
LEAF=$(wp post create --post_type=page --post_parent="$PARENT" --post_title='Malen & Zeichnen' --post_name=malen-zeichnen --post_status=publish --post_content='[affiliate_portal_kategorie]' --porcelain)
GLOSS=$(wp post create --post_type=uge_term --post_title='Modellbau' --post_name=modellbau --post_status=publish --post_content='Modellbau Hobby Glossartext' --porcelain)
export HDAR_LEAF="$LEAF" HDAR_GLOSS="$GLOSS"
cat >/tmp/hobby-real-wp/trace.php <<'PHP'
<?php
$p=(int)getenv('HDAR_LEAF'); $g=(int)getenv('HDAR_GLOSS');
$x=Hobby_Depot_Affiliate_Router::instance(); $r=new ReflectionClass($x);
$ctx=$r->getMethod('get_content_context')->invoke($x,$p);
echo "ACTUAL_LEAF_CONTEXT=".json_encode(array_intersect_key($ctx,array_flip(['post_id','post_type','primary_name','primary_slug'])),JSON_UNESCAPED_UNICODE)."\n";
$fx=$r->getMethod('render_affiliate_slot_for_context');
$out=$fx->invoke($x,$p,$ctx,'product_after_category_tiles','portal_context','');
echo "ACTUAL_DIRECT_SLOT=".json_encode(array('bytes'=>strlen($out),'CI'=>strpos($out,'hdar-ci-amazon-banner')!==false,'start'=>substr($out,0,200)))."\n";
$filtered=apply_filters('pftk_leaf_page_affiliate_slot_html','',$p,'product_after_category_tiles',array());
echo "ACTUAL_DESIGN_FILTER=".json_encode(array('bytes'=>strlen($filtered),'CI'=>strpos($filtered,'hdar-ci-amazon-banner')!==false,'start'=>substr($filtered,0,200)))."\n";
$cg=$r->getMethod('get_content_context')->invoke($x,$g);
$og=$fx->invoke($x,$g,$cg,'glossary_single_desktop_banner','portal_context','');
echo "ACTUAL_GLOSS_SLOT=".json_encode(array('bytes'=>strlen($og),'CI'=>strpos($og,'hdar-ci-amazon-banner')!==false,'topic'=>$cg['primary_name']??''))."\n";
PHP
echo "E2E STEP: real router/filter context, no synthetic context allowed"
wp eval-file /tmp/hobby-real-wp/trace.php
php -S 127.0.0.1:8989 -t /tmp/hobby-real-wp/site >/tmp/hobby-real-wp/server.log 2>&1 &
sleep 2
set +e
curl -fsS --max-time 35 -o /tmp/hobby-real-wp/leaf.html -w "LEAF HTTP %{http_code} bytes %{size_download}\n" "http://127.0.0.1:8989/?page_id=$LEAF"
curl -fsS --max-time 35 -o /tmp/hobby-real-wp/gloss.html -w "GLOSS HTTP %{http_code} bytes %{size_download}\n" "http://127.0.0.1:8989/?p=$GLOSS&post_type=uge_term"
curl -fsS --max-time 35 -o /tmp/hobby-real-wp/register.html -w "REGISTER HTTP %{http_code} bytes %{size_download}\n" "http://127.0.0.1:8989/hobbyregister/airbrush-modellbau/"
set -e
for key in leaf gloss register; do
  echo "RENDERED_HTML $key:"
  if test -f "/tmp/hobby-real-wp/$key.html"; then
    grep -oE 'hdar-ci-amazon-banner|hdar-ci-register|hdar-ci-logo-original|data-hd-register-profile|affiliate_no_real_creative|data-ppar-slot="[^"]+"|There has been a critical error' "/tmp/hobby-real-wp/$key.html" | sort | uniq -c | head -30 || :
  fi
done
echo "SERVER_LOG_TAIL"
tail -n 35 /tmp/hobby-real-wp/server.log
echo "E2E DONE"
