#!/usr/bin/env bash
set -euo pipefail
ROOT=/tmp/v652-httpdiag; WP=$ROOT/wp; rm -rf "$ROOT"; mkdir -p "$WP"
wp core download --version=7.0.1 --path="$WP" --force --allow-root >/dev/null
wp config create --path="$WP" --dbname=v651gate --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --skip-check --allow-root >/dev/null
wp db reset --yes --path="$WP" --allow-root >/dev/null
wp core install --path="$WP" --url=http://127.0.0.1:8111 --title=HTTPDiag --admin_user=a --admin_password='GateOnly-20260822!' --admin_email=a@example.invalid --skip-email --allow-root >/dev/null
wp option update siteurl http://127.0.0.1:8112 --path="$WP" --allow-root >/dev/null
mkdir -p "$WP/wp-content/mu-plugins"
cat > "$WP/ping.php" <<'PHP'
<?php file_put_contents('/tmp/v652-httpdiag-hit.log',date('c')." ".$_SERVER['REQUEST_METHOD']."\n",FILE_APPEND); echo 'pong';
PHP
cat > "$WP/wp-content/mu-plugins/httpdiag.php" <<'PHP'
<?php add_action('init',function(){if(($_GET['httpdiag']??'')!=='1')return; $out=[]; foreach([0.01,0.1,1.0] as $t){$r=wp_remote_post('http://127.0.0.1:8112/ping.php',['timeout'=>$t,'blocking'=>false]);$out[(string)$t]=is_wp_error($r)?['error'=>$r->get_error_code(),'message'=>$r->get_error_message()]:$r;} header('Content-Type: application/json'); echo wp_json_encode($out); exit;},PHP_INT_MAX);
PHP
rm -f /tmp/v652-httpdiag-hit.log
php -S 127.0.0.1:8112 -t "$WP" > "$ROOT/target.log" 2>&1 & P2=$!
php -S 127.0.0.1:8111 -t "$WP" > "$ROOT/source.log" 2>&1 & P1=$!
trap 'kill "$P1" "$P2" 2>/dev/null || true' EXIT
sleep 1
curl --fail --silent --show-error 'http://127.0.0.1:8111/?httpdiag=1' > "$ROOT/result.json"
sleep 2
php -m | sort > "$ROOT/php_modules.txt"
echo '=== MODULE CURL ==='; grep -i '^curl$' "$ROOT/php_modules.txt" || true
echo '=== RESULT ==='; cat "$ROOT/result.json"; echo
echo '=== HITS ==='; cat /tmp/v652-httpdiag-hit.log 2>/dev/null || true
echo '=== TARGET ==='; cat "$ROOT/target.log"
hits=$(wc -l < /tmp/v652-httpdiag-hit.log 2>/dev/null || echo 0)
[ "$hits" -ge 1 ] || { echo 'WP_HTTP_NONBLOCKING=FAIL'; exit 1; }
echo "WP_HTTP_NONBLOCKING=PASS HITS=$hits"
