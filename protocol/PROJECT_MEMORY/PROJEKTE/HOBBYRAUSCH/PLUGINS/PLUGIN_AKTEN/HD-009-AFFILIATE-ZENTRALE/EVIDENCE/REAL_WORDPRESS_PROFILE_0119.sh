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
cat >wp-content/mu-plugins/hdar-profile-dom-probe.php <<'PHP'
<?php
add_action('wp_footer',static function(){
echo '<script>(function(){function probe(){var g=document.querySelector("[data-hd-register-profile] .hdr-profile-grid");if(!g)return;'
.'var a=g.querySelector("aside"),main=g.querySelector("main"),article=g.querySelector("main .hdr-article"),'
.'facts=a&&a.querySelector(".hdr-facts"),side=a&&a.querySelector(".hdar-ci-register-side"),'
.'grp=a&&a.querySelector(".hdr-sidebox"),inline=article&&article.querySelector(".hdar-ci-register-inline");'
.'var secs=article?article.querySelectorAll(":scope > section"):[],eq=null;'
.'for(var k=0;k<secs.length;k++){var h=secs[k].querySelector("h2");if(h&&/Kosten\\s+und\\s+Ausrüstung/i.test(h.textContent||"")){eq=secs[k];break;}}'
.'var rect=function(x){if(!x)return null;var r=x.getBoundingClientRect();return [Math.round(r.top),Math.round(r.bottom),Math.round(r.height)];};'
.'var o={viewport:innerWidth,sideParent:side&&side.parentElement.tagName,sideIndex:side&&a?Array.prototype.indexOf.call(a.children,side):-1,'
.'factsIndex:facts&&a?Array.prototype.indexOf.call(a.children,facts):-1,groupIndex:grp&&a?Array.prototype.indexOf.call(a.children,grp):-1,'
.'inlineAfterEquipment:!!(eq&&inline&&eq.nextElementSibling===inline),sideHidden:!side||side.hidden,inlineHidden:!inline||inline.hidden,'
.'sideGridArea:side?getComputedStyle(side).gridArea:"none",mainGridArea:main?getComputedStyle(main).gridArea:"none",'
.'mainRect:rect(main),factsRect:rect(facts),sideRect:rect(side),groupRect:rect(grp),inlineRect:rect(inline),'
.'sideAdCount:g.querySelectorAll(".hdar-ci-register-side .hdar-ci-amazon-slot").length,inlineAdCount:g.querySelectorAll(".hdar-ci-register-inline .hdar-ci-amazon-slot").length};'
.'document.body.setAttribute("data-hd009-e2e",JSON.stringify(o));}'
.'window.addEventListener("load",function(){setTimeout(probe,140);},{once:true});})();</script>';
},9999);
PHP
cat >/tmp/hobby-real-wp/site/router.php <<'PHP'
<?php
$path=parse_url($_SERVER['REQUEST_URI'],PHP_URL_PATH);
$target=__DIR__ . $path;
if ($path !== '/' && is_file($target)) { return false; }
require __DIR__ . '/index.php';
PHP
php -S 127.0.0.1:8989 -t /tmp/hobby-real-wp/site /tmp/hobby-real-wp/site/router.php >/tmp/hobby-real-wp/server.log 2>&1 &
WEB_PID=$!
sleep 2
curl -fsSL --max-time 35 -o /tmp/hobby-real-wp/register-actual.html -w "PROFILE HTTP %{http_code} size %{size_download}\n" "http://127.0.0.1:8989/hobbyregister/airbrush-modellbau/"
python3 - <<'PY'
from pathlib import Path
s=Path('/tmp/hobby-real-wp/register-actual.html').read_text()
for term in ['hdar-ci-register-side-airbrush-modellbau','hdar-ci-register-inline-airbrush-modellbau','hdr-profile-grid','Kosten und Ausrüstung']:
 print('E2E RAW HTML',term,'count',s.count(term))
assert 'hdr-profile-grid' in s,'Actual HD007 page not present'
PY
python3 "$GITHUB_WORKSPACE/protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/ASSERT_0119_BROWSER_DOM.py"
echo "REAL WP + HD007 + HD003 + HD009 0.1.19 E2E PASS"
