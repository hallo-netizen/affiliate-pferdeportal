#!/usr/bin/env bash
set -euo pipefail
WP=/tmp/wp
SITE=/tmp/wp-site

curl -fsSL -o "$WP" https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
chmod +x "$WP"
mkdir -p "$SITE"
"$WP" core download --path="$SITE" --version=7.1.1 --force
"$WP" config create --path="$SITE" --dbname=wordpress --dbuser=wordpress --dbpass=wordpress --dbhost=127.0.0.1:3306 --skip-check
"$WP" core install --path="$SITE" --url=http://127.0.0.1:8080 --title='Design V2 Gate' --admin_user=admin --admin_password='ci-pass-12345' --admin_email=ci@example.test --skip-email

mkdir -p "$SITE/wp-content/plugins/design-v2-gate"
mkdir -p "$SITE/wp-content/plugins/pa-affiliate-design-performance"
cp AFFILIATE_HOBBYRAUM/performance-design-v2/design-v2-gate.php "$SITE/wp-content/plugins/design-v2-gate/"
cp AFFILIATE_HOBBYRAUM/performance-design-v2/pa-affiliate-design-performance.php "$SITE/wp-content/plugins/pa-affiliate-design-performance/"
php -l "$SITE/wp-content/plugins/design-v2-gate/design-v2-gate.php"
php -l "$SITE/wp-content/plugins/pa-affiliate-design-performance/pa-affiliate-design-performance.php"
"$WP" plugin activate design-v2-gate --path="$SITE"
"$WP" plugin activate pa-affiliate-design-performance --path="$SITE"

"$WP" eval '
$menu_id=wp_create_nav_menu("PFTK V2 1520 Fixture");
if(is_wp_error($menu_id)){fwrite(STDERR,$menu_id->get_error_message());exit(1);}
set_theme_mod("nav_menu_locations",array("primary"=>(int)$menu_id));
for($i=1;$i<=1520;$i++){
  $id=wp_update_nav_menu_item($menu_id,0,array(
    "menu-item-title"=>"Item ".$i,
    "menu-item-url"=>home_url("/item-".$i."/"),
    "menu-item-status"=>"publish",
    "menu-item-parent-id"=>0
  ));
  if(is_wp_error($id)){fwrite(STDERR,$id->get_error_message());exit(1);}
}
update_option("pftk_v2_gate_menu_id",(int)$menu_id,false);
echo "MENU_ID=".$menu_id."\n";
' --path="$SITE"

"$WP" plugin deactivate pa-affiliate-design-performance --path="$SITE"
php -S 127.0.0.1:8080 -t "$SITE" >/tmp/server-baseline.log 2>&1 &
PID=$!
for i in $(seq 1 30); do curl -fsS http://127.0.0.1:8080/ >/dev/null && break || sleep 1; done
curl -fsS 'http://127.0.0.1:8080/?design_v2_gate=1&baseline=1' >/tmp/baseline.json
kill "$PID"

"$WP" plugin activate pa-affiliate-design-performance --path="$SITE"
php -S 127.0.0.1:8080 -t "$SITE" >/tmp/server-candidate.log 2>&1 &
PID=$!
for i in $(seq 1 30); do curl -fsS http://127.0.0.1:8080/ >/dev/null && break || sleep 1; done
curl -fsS 'http://127.0.0.1:8080/?design_v2_gate=1' >/tmp/candidate.json
curl -fsS 'http://127.0.0.1:8080/wp-admin/admin-post.php?action=design_v2_admin' >/tmp/admin.json
kill "$PID"

python3 AFFILIATE_HOBBYRAUM/performance-design-v2/assert-results.py /tmp/baseline.json /tmp/candidate.json /tmp/admin.json
