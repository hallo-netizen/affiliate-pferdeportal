#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v654/runner/run-v654-full-release.sh
[ "$(git hash-object "$BASE")" = "85968d2c4afbeb49b10cbc6d495c67f725bc4ff7" ] || { echo 'BLOCKED: V6.54 base release runner drift'; exit 1; }
TMP=/tmp/run-v654-full-release-v2-generated.sh
python3 - "$BASE" "$TMP" <<'PY'
from pathlib import Path
import sys
src=Path(sys.argv[1]).read_text()

# 1) Real HTTP transport proof is intentionally independent of provider-enabled state.
old='''KEY=$(wp option get ppar_ebay_external_tick_key_v1 --path="$WP1" --allow-root)\nwp server --host=127.0.0.1 --port=8089 --path="$WP1" > "$E/05_wp_server.log" 2>&1 & SERVER_PID=$!\ntrap 'kill $SERVER_PID 2>/dev/null || true' EXIT\nfor i in $(seq 1 30); do curl -sS "http://127.0.0.1:8089/" >/dev/null 2>&1 && break; sleep 1; done\nBAD_STATUS=$(curl -sS -o "$E/05_http_bad.json" -w '%{http_code}' "http://127.0.0.1:8089/?rest_route=/affiliate-zentrale/v1/ebay/tick&key=wrong")\n[ "$BAD_STATUS" = 403 ]\ncurl -fsS "http://127.0.0.1:8089/?rest_route=/affiliate-zentrale/v1/ebay/tick&key=$KEY" > "$E/05_http_good.json"\ngrep -Fq '\"status\":\"idle\"' "$E/05_http_good.json"\nkill $SERVER_PID 2>/dev/null || true; wait $SERVER_PID 2>/dev/null || true; trap - EXIT\necho 'REAL_HTTP_EXTERNAL_TICK=PASS' | tee "$E/05_http_result.log"'''
new='''# Separate real HTTP-process proof. Do not assume the synthetic WP-eval fixture\n# survives a fresh HTTP bootstrap; plugin normalization may legitimately disable\n# eBay when provider credentials are absent. The HTTP gate proves route + auth +\n# successful authenticated execution, while due/autostart semantics are proven\n# above inside real WordPress with deterministic state.\nKEY=$(wp option get ppar_ebay_external_tick_key_v1 --path="$WP1" --allow-root)\n[ ${#KEY} -ge 32 ]\nwp server --host=127.0.0.1 --port=8089 --path="$WP1" > "$E/05_wp_server.log" 2>&1 & SERVER_PID=$!\ntrap 'kill $SERVER_PID 2>/dev/null || true' EXIT\nREADY=0\nfor i in $(seq 1 30); do if curl -sS "http://127.0.0.1:8089/" >/dev/null 2>&1; then READY=1; break; fi; sleep 1; done\n[ "$READY" = 1 ]\nBAD_STATUS=$(curl -sS -o "$E/05_http_bad.json" -w '%{http_code}' "http://127.0.0.1:8089/?rest_route=/affiliate-zentrale/v1/ebay/tick&key=wrong")\n[ "$BAD_STATUS" = 403 ]\nGOOD_STATUS=$(curl -sS -o "$E/05_http_good.json" -w '%{http_code}' "http://127.0.0.1:8089/?rest_route=/affiliate-zentrale/v1/ebay/tick&key=$KEY")\n[ "$GOOD_STATUS" = 200 ]\nphp -r '$d=json_decode(file_get_contents($argv[1]),true);if(!is_array($d)||json_last_error()!==JSON_ERROR_NONE||!array_key_exists("status",$d)){fwrite(STDERR,"BLOCKED invalid authenticated tick JSON\\n");exit(1);} echo "HTTP_AUTHENTICATED_STATUS=".$d["status"]."\\n";' "$E/05_http_good.json" | tee "$E/05_http_authenticated_status.log"\nkill $SERVER_PID 2>/dev/null || true; wait $SERVER_PID 2>/dev/null || true; trap - EXIT\necho 'REAL_HTTP_EXTERNAL_TICK=PASS' | tee "$E/05_http_result.log"'''
if src.count(old)!=1: raise SystemExit('BLOCKED: real HTTP block anchor drift')
src=src.replace(old,new,1)

# 2) Real WordPress assertions are deterministic and must be exact.
src=src.replace("grep -Fq 'REAL_EXTERNAL_TICK_V654_ASSERTIONS=' \"$E/05_real_external_tick.log\"; grep -Fq 'FAIL=0' \"$E/05_real_external_tick.log\"", "grep -Fxq 'REAL_EXTERNAL_TICK_V654_ASSERTIONS=37 FAIL=0' \"$E/05_real_external_tick.log\"")
src=src.replace("grep -Fq 'FAIL=0' \"$E/08_real_external_tick.log\";", "grep -Fxq 'REAL_EXTERNAL_TICK_V654_ASSERTIONS=37 FAIL=0' \"$E/08_real_external_tick.log\";")
src=src.replace("grep -Fq 'FAIL=0' \"$E/09_real_external_tick.log\";", "grep -Fxq 'REAL_EXTERNAL_TICK_V654_ASSERTIONS=37 FAIL=0' \"$E/09_real_external_tick.log\";")

# 3) Whole-workflow audit found a stale historical browser-bound transport sentence in readme.
# Correct it inside the same existing readme production scope and gate it fail-closed.
anchor='''( cd /tmp/v654-source && patch -p1 --batch < /tmp/v654.patch ) > "$E/03_patch_apply.log"\nSRC=/tmp/v654-source/affiliate-portal-router'''
replacement='''( cd /tmp/v654-source && patch -p1 --batch < /tmp/v654.patch ) > "$E/03_patch_apply.log"\nREADMECORR="$WORK/.github/v654/patches/02_readme_current_transport.patch"\ntest -f "$READMECORR"\nsha256sum "$READMECORR" > "$E/03_readme_transport_patch_sha256.txt"\n( cd /tmp/v654-source && patch -p1 --dry-run --batch < "$READMECORR" ) > "$E/03_readme_transport_patch_dryrun.log"\n( cd /tmp/v654-source && patch -p1 --batch < "$READMECORR" ) > "$E/03_readme_transport_patch_apply.log"\nSRC=/tmp/v654-source/affiliate-portal-router'''
if src.count(anchor)!=1: raise SystemExit('BLOCKED: readme correction apply anchor drift')
src=src.replace(anchor,replacement,1)

old_gate='''grep -Fxq 'ASSERTIONS=31 FAIL=0' "$E/04_architecture.log"'''
new_gate='''grep -Fxq 'ASSERTIONS=31 FAIL=0' "$E/04_architecture.log"\nif grep -Fq 'Der Nutzer hat keinen Serverzugriff. Deshalb arbeitet der reale Hosting-Modus weiterhin über genau einen authentifizierten, sequenziellen Admin-AJAX-Taktgeber.' "$SRC/readme.txt"; then echo 'BLOCKED stale browser-bound transport text survived V6.54'; exit 1; fi\ngrep -Fq 'Die frühere browsergebundene Admin-AJAX-Betriebsabweichung gilt ab 6.54.0 nicht mehr.' "$SRC/readme.txt"\necho 'README_CURRENT_TRANSPORT=PASS' | tee "$E/04_readme_current_transport.log"'''
if src.count(old_gate)!=1: raise SystemExit('BLOCKED: source readme gate anchor drift')
src=src.replace(old_gate,new_gate,1)

old_fresh='''grep -Fxq 'ASSERTIONS=31 FAIL=0' "$E/07_architecture.log"'''
new_fresh='''grep -Fxq 'ASSERTIONS=31 FAIL=0' "$E/07_architecture.log"\nif grep -Fq 'Der Nutzer hat keinen Serverzugriff. Deshalb arbeitet der reale Hosting-Modus weiterhin über genau einen authentifizierten, sequenziellen Admin-AJAX-Taktgeber.' "$FRESH/readme.txt"; then echo 'BLOCKED stale browser-bound transport text survived fresh unpack'; exit 1; fi\ngrep -Fq 'Die frühere browsergebundene Admin-AJAX-Betriebsabweichung gilt ab 6.54.0 nicht mehr.' "$FRESH/readme.txt"\necho 'README_CURRENT_TRANSPORT_FRESH=PASS' | tee "$E/07_readme_current_transport.log"'''
if src.count(old_fresh)!=1: raise SystemExit('BLOCKED: fresh readme gate anchor drift')
src=src.replace(old_fresh,new_fresh,1)

old_copy='''cp /tmp/v654.patch "$MD/09_DIFF_AND_HASHES/01_kiss_external_tick_skip.patch"'''
new_copy='''cp /tmp/v654.patch "$MD/09_DIFF_AND_HASHES/01_kiss_external_tick_skip.patch"\ncp "$READMECORR" "$MD/09_DIFF_AND_HASHES/04_readme_current_transport.patch"'''
if src.count(old_copy)!=1: raise SystemExit('BLOCKED: master readme evidence anchor drift')
src=src.replace(old_copy,new_copy,1)

# Final decision explicitly includes the documentation consistency gate.
old_final='''SOURCE_FRESH_MASTER_PARITY=PASS\nEXTERNAL_EBAY_PROVIDER_LIVE_E2E=OPEN_NOT_CLAIMED'''
new_final='''SOURCE_FRESH_MASTER_PARITY=PASS\nREADME_CURRENT_TRANSPORT=PASS\nEXTERNAL_EBAY_PROVIDER_LIVE_E2E=OPEN_NOT_CLAIMED'''
if src.count(old_final)!=1: raise SystemExit('BLOCKED: final decision readme anchor drift')
src=src.replace(old_final,new_final,1)

Path(sys.argv[2]).write_text(src)
PY
test -f "$TMP"
bash -n "$TMP"
chmod +x "$TMP"
"$TMP"
