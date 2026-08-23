#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v654/runner/run-v654-full-release.sh
[ "$(git hash-object "$BASE")" = "85968d2c4afbeb49b10cbc6d495c67f725bc4ff7" ] || { echo 'BLOCKED: V6.54 base release runner drift'; exit 1; }
TMP=/tmp/run-v654-full-release-v2-generated.sh
python3 - "$BASE" "$TMP" <<'PY'
from pathlib import Path
import sys
src=Path(sys.argv[1]).read_text()
old='''KEY=$(wp option get ppar_ebay_external_tick_key_v1 --path="$WP1" --allow-root)\nwp server --host=127.0.0.1 --port=8089 --path="$WP1" > "$E/05_wp_server.log" 2>&1 & SERVER_PID=$!'''
new='''# Deterministic fixture for the separate real HTTP process. The adversarial\n# wp-eval test above is a different test case and must not leak its state.\nwp eval '$p=Pferdeportal_Affiliate_Router::instance();$s=$p->ebay_settings_defaults();$s["enabled"]=true;$s["private_enabled"]=true;$s["business_enabled"]=true;$s["last_sync"]=array("finished_at"=>time());$s["last_refresh"]=array("finished_at"=>time());update_option(Pferdeportal_Affiliate_Router::OPTION_NETWORK_EBAY,$s,false);delete_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE);' --path="$WP1" --allow-root >> "$E/05_wp_setup.log" 2>&1\nwp option get ppar_network_ebay_v1 --format=json --path="$WP1" --allow-root > "$E/05_http_fixture.json"\ngrep -Fq '"enabled":true' "$E/05_http_fixture.json"\nKEY=$(wp option get ppar_ebay_external_tick_key_v1 --path="$WP1" --allow-root)\nwp server --host=127.0.0.1 --port=8089 --path="$WP1" > "$E/05_wp_server.log" 2>&1 & SERVER_PID=$!'''
if src.count(old)!=1: raise SystemExit('BLOCKED: HTTP fixture anchor drift')
src=src.replace(old,new,1)
# Real WordPress test now has deterministic global counters. Require exact count.
src=src.replace("grep -Fq 'REAL_EXTERNAL_TICK_V654_ASSERTIONS=' \"$E/05_real_external_tick.log\"; grep -Fq 'FAIL=0' \"$E/05_real_external_tick.log\"", "grep -Fxq 'REAL_EXTERNAL_TICK_V654_ASSERTIONS=37 FAIL=0' \"$E/05_real_external_tick.log\"")
src=src.replace("grep -Fq 'FAIL=0' \"$E/08_real_external_tick.log\";", "grep -Fxq 'REAL_EXTERNAL_TICK_V654_ASSERTIONS=37 FAIL=0' \"$E/08_real_external_tick.log\";")
src=src.replace("grep -Fq 'FAIL=0' \"$E/09_real_external_tick.log\";", "grep -Fxq 'REAL_EXTERNAL_TICK_V654_ASSERTIONS=37 FAIL=0' \"$E/09_real_external_tick.log\";")
Path(sys.argv[2]).write_text(src)
PY
test -f "$TMP"
bash -n "$TMP"
chmod +x "$TMP"
"$TMP"
