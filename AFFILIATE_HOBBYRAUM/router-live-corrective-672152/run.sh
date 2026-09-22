#!/usr/bin/env bash
set -euo pipefail
curl -fsSL -o /tmp/wp https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
chmod +x /tmp/wp
mkdir -p /tmp/wp-site
/tmp/wp core download --path=/tmp/wp-site --version=7.1.1 --force
/tmp/wp config create --path=/tmp/wp-site --dbname=wordpress --dbuser=wordpress --dbpass=wordpress --dbhost=127.0.0.1:3306 --skip-check
/tmp/wp core install --path=/tmp/wp-site --url=http://127.0.0.1:8080 --title='152 gate' --admin_user=admin --admin_password='fixture-12345' --admin_email=ci@example.test --skip-email
mkdir -p /tmp/wp-site/wp-content/plugins/g152
cp AFFILIATE_HOBBYRAUM/router-live-corrective-672152/gate.php /tmp/wp-site/wp-content/plugins/g152/
php -l /tmp/wp-site/wp-content/plugins/g152/gate.php
/tmp/wp plugin activate g152 --path=/tmp/wp-site
php -S 127.0.0.1:8080 -t /tmp/wp-site >/tmp/server.log 2>&1 &
PID=$!
trap 'kill $PID || true' EXIT
for i in $(seq 1 30); do curl -fsS http://127.0.0.1:8080/ >/dev/null && break || sleep 1; done
curl -fsS 'http://127.0.0.1:8080/?g152=1' >/tmp/public.json
curl -fsS 'http://127.0.0.1:8080/wp-admin/admin-post.php?action=g152_admin' >/tmp/admin.json
python3 AFFILIATE_HOBBYRAUM/router-live-corrective-672152/assert.py /tmp/public.json /tmp/admin.json
