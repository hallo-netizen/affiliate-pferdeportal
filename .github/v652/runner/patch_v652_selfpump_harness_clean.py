from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
old='''background_selfpump_gate(){ local src="$1" p="$2" out="$E/$p/V652_BACKGROUND_SELFPUMP"; mkdir -p "$out"; setup_wp\n rm -rf "$WP/wp-content/plugins/affiliate-portal-router"; cp -a "$src" "$WP/wp-content/plugins/affiliate-portal-router"; wp plugin activate affiliate-portal-router --path="$WP" --allow-root >/dev/null || return 1\n wp option update home http://127.0.0.1:8099 --path="$WP" --allow-root >/dev/null || return 1\n wp option update siteurl http://127.0.0.1:8099 --path="$WP" --allow-root >/dev/null || return 1\n mkdir -p "$WP/wp-content/mu-plugins"\n'''
new='''background_selfpump_gate(){ local src="$1" p="$2" out="$E/$p/V652_BACKGROUND_SELFPUMP"; mkdir -p "$out"; setup_wp\n # Harness hardening: WP-CLI must not create an unreachable pre-server cron lock.\n wp config set DISABLE_WP_CRON true --raw --path="$WP" --allow-root >/dev/null || return 1\n wp transient delete doing_cron --path="$WP" --allow-root >/dev/null 2>&1 || true\n rm -rf "$WP/wp-content/plugins/affiliate-portal-router"; cp -a "$src" "$WP/wp-content/plugins/affiliate-portal-router"; wp plugin activate affiliate-portal-router --path="$WP" --allow-root >/dev/null || return 1\n wp option update home http://127.0.0.1:8099 --path="$WP" --allow-root >/dev/null || return 1\n wp option update siteurl http://127.0.0.1:8099 --path="$WP" --allow-root >/dev/null || return 1\n mkdir -p "$WP/wp-content/mu-plugins"\n'''
if s.count(old)!=1: raise SystemExit('BLOCKED: selfpump harness setup anchor mismatch')
s=s.replace(old,new,1)
old2='''PHPV652MU\n php -S 127.0.0.1:8099 -t "$WP" > "$out/server.log" 2>&1 & local spid=$!; sleep 1\n'''
new2='''PHPV652MU\n # Remove the setup-only guard without bootstrapping WordPress again.\n python3 - "$WP/wp-config.php" <<'PYV652CRONCFG'\nfrom pathlib import Path\nimport sys\np=Path(sys.argv[1]); lines=p.read_text().splitlines()\nlines=[ln for ln in lines if 'DISABLE_WP_CRON' not in ln]\np.write_text('\\n'.join(lines)+'\\n')\nPYV652CRONCFG\n PHP_CLI_SERVER_WORKERS=4 php -S 127.0.0.1:8099 -t "$WP" > "$out/server.log" 2>&1 & local spid=$!; sleep 1\n'''
if s.count(old2)!=1: raise SystemExit('BLOCKED: selfpump harness server anchor mismatch')
s=s.replace(old2,new2,1)
p.write_text(s)
