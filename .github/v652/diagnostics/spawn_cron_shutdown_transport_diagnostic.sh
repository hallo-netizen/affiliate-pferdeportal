#!/usr/bin/env bash
set -euo pipefail
ROOT=/tmp/v652-spawn-shutdown-diag
WP=$ROOT/wp
rm -rf "$ROOT"; mkdir -p "$WP"
wp core download --version=7.0.1 --path="$WP" --force --allow-root >/dev/null
wp config create --path="$WP" --dbname=v651gate --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --skip-check --allow-root >/dev/null
wp db reset --yes --path="$WP" --allow-root >/dev/null
wp core install --path="$WP" --url=http://127.0.0.1:8131 --title='V652 Spawn Shutdown Diagnostic' --admin_user=a --admin_password='GateOnly-20260822!' --admin_email=a@example.invalid --skip-email --allow-root >/dev/null
# Prevent WP-CLI setup commands from creating an unreachable pre-server cron lock.
wp config set DISABLE_WP_CRON true --raw --path="$WP" --allow-root >/dev/null
mkdir -p "$WP/wp-content/mu-plugins"
cat > "$WP/wp-content/mu-plugins/v652-spawn-shutdown.php" <<'PHP'
<?php
remove_action('wp_loaded', '_wp_cron', 20);
add_action('v652_spawn_probe', function(){
    $n = absint(get_option('v652_spawn_probe_count', 0)) + 1;
    update_option('v652_spawn_probe_count', $n, false);
    file_put_contents('/tmp/v652-spawn-probe.log', json_encode(array('n'=>$n,'pid'=>getmypid(),'lock'=>(string)get_transient('doing_cron'),'at'=>microtime(true)))."\n", FILE_APPEND);
});
add_action('init', function(){
    $case = sanitize_key((string)($_GET['v652_case'] ?? ''));
    if (!$case) { return; }
    wp_clear_scheduled_hook('v652_spawn_probe');
    delete_transient('doing_cron');
    update_option('v652_spawn_probe_count', 0, false);
    delete_option('v652_spawn_request');
    add_filter('cron_request', function($req, $doing){
        update_option('v652_spawn_request', array('doing'=>$doing,'url'=>$req['url'] ?? '','args'=>$req['args'] ?? array()), false);
        return $req;
    }, 999, 2);
    wp_schedule_single_event(time(), 'v652_spawn_probe');
    if ($case === 'init') {
        $before=(string)get_transient('doing_cron');
        $r = spawn_cron(microtime(true));
        echo 'CASE_INIT BEFORE=' . $before . ' RETURN=' . var_export($r, true) . ' LOCK=' . (string)get_transient('doing_cron') . "\n";
        exit;
    }
    if ($case === 'shutdown') {
        $before=(string)get_transient('doing_cron');
        add_action('shutdown', function() use ($before){
            $r = spawn_cron(microtime(true));
            file_put_contents('/tmp/v652-shutdown-return.log', 'BEFORE=' . $before . ' RETURN=' . var_export($r, true) . ' LOCK=' . (string)get_transient('doing_cron') . "\n");
        }, PHP_INT_MAX);
        echo "CASE_SHUTDOWN_REGISTERED BEFORE=$before\n";
        exit;
    }
}, PHP_INT_MAX);
PHP
# Remove DISABLE_WP_CRON without loading WordPress after it becomes false.
python3 - "$WP/wp-config.php" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
lines=[ln for ln in s.splitlines() if "define( 'DISABLE_WP_CRON'" not in ln and 'define(\'DISABLE_WP_CRON\'' not in ln and 'define("DISABLE_WP_CRON"' not in ln]
p.write_text('\n'.join(lines)+'\n')
PY
rm -f /tmp/v652-spawn-probe.log /tmp/v652-shutdown-return.log
PHP_CLI_SERVER_WORKERS=4 php -S 127.0.0.1:8131 -t "$WP" > "$ROOT/server.log" 2>&1 & SP=$!
trap 'kill "$SP" 2>/dev/null || true; pkill -P "$SP" 2>/dev/null || true' EXIT
sleep 1
run_case(){
  local c=$1
  curl --fail --silent --show-error "http://127.0.0.1:8131/?v652_case=$c" > "$ROOT/$c-response.txt"
  local count=0
  for i in $(seq 1 80); do
    count=$(wp option get v652_spawn_probe_count --path="$WP" --allow-root 2>/dev/null | tr -d '\r\n ' || true)
    [ "$count" = 1 ] && break
    sleep .25
  done
  echo "CASE=$c COUNT=$count RESPONSE=$(tr '\n' ' ' < "$ROOT/$c-response.txt")"
  [ "$count" = 1 ] || return 1
}
run_case init
run_case shutdown
cron_hits=$(grep -c 'POST /wp-cron.php' "$ROOT/server.log" || true)
echo "CRON_HITS=$cron_hits"
echo '=== SHUTDOWN RETURN ==='; cat /tmp/v652-shutdown-return.log 2>/dev/null || true
echo '=== PROBE ==='; cat /tmp/v652-spawn-probe.log 2>/dev/null || true
echo '=== SERVER ==='; cat "$ROOT/server.log"
[ "$cron_hits" -ge 2 ] || exit 1
echo 'SPAWN_CRON_INIT_AND_SHUTDOWN=PASS'
