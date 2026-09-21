#!/usr/bin/env bash
set -euo pipefail
NONCE="$(cat /tmp/nonce)"

curl -fsS -b /tmp/pste-cookies.txt -c /tmp/pste-cookies.txt   --data-urlencode 'action=pste_breadth_research_start'   --data-urlencode "nonce=$NONCE"   --data-urlencode 'target_usable=1'   --data-urlencode 'max_items=1'   --data-urlencode 'confirm_cost=1'   http://127.0.0.1:8090/wp-admin/admin-ajax.php > /tmp/stress-breadth-start.json

STRESS_QUEUE_UUID="$(php -r '$x=json_decode(file_get_contents("/tmp/stress-breadth-start.json"),true);if(!is_array($x)||empty($x["success"]))exit(2);echo $x["data"]["queue"]["queue_uuid"]??"";')"
test -n "$STRESS_QUEUE_UUID"

terminal=0
prepare_intermediate=0
prepare_total_max=0

for i in $(seq 1 480); do
  curl -fsS -b /tmp/pste-cookies.txt     --data-urlencode 'action=pste_breadth_research_status'     --data-urlencode "nonce=$NONCE"     --data-urlencode "queue_uuid=$STRESS_QUEUE_UUID"     http://127.0.0.1:8090/wp-admin/admin-ajax.php > /tmp/stress-breadth-status.json

  QSTATE="$(php -r '$x=json_decode(file_get_contents("/tmp/stress-breadth-status.json"),true);echo $x["data"]["queue"]["status"]??"INVALID";')"
  DSTATE="$(php -r '$x=json_decode(file_get_contents("/tmp/stress-breadth-status.json"),true);echo $x["data"]["driver"]["status"]??"INVALID";')"
  STAGE="$(php -r '$x=json_decode(file_get_contents("/tmp/stress-breadth-status.json"),true);echo $x["data"]["queue"]["child"]["finalize_stage"]??"";')"
  CURSOR="$(php -r '$x=json_decode(file_get_contents("/tmp/stress-breadth-status.json"),true);echo (int)($x["data"]["queue"]["child"]["finalize_prepare_cursor"]??0);')"
  TOTAL="$(php -r '$x=json_decode(file_get_contents("/tmp/stress-breadth-status.json"),true);echo (int)($x["data"]["queue"]["child"]["finalize_prepare_total"]??0);')"

  if [ "$TOTAL" -gt "$prepare_total_max" ]; then prepare_total_max="$TOTAL"; fi
  if [ "$STAGE" = "PREPARE_CANDIDATES" ] && [ "$TOTAL" -ge 100 ] && [ "$CURSOR" -gt 0 ] && [ "$CURSOR" -lt "$TOTAL" ]; then
    prepare_intermediate=1
    cp /tmp/stress-breadth-status.json /tmp/stress-prepare-intermediate.json
  fi

  if [ "$DSTATE" = "BLOCKED" ]; then
    echo STRESS_PREPARE_DRIVER_BLOCKED
    cat /tmp/stress-breadth-status.json
    exit 1
  fi
  if [ "$QSTATE" = "PAUSED_ERROR" ] || [ "$QSTATE" = "OUTCOME_UNKNOWN" ] || [ "$QSTATE" = "CANCELLED" ]; then
    echo STRESS_PREPARE_QUEUE_TERMINAL_ERROR_"$QSTATE"
    cat /tmp/stress-breadth-status.json
    exit 1
  fi
  if [ "$QSTATE" = "COMPLETE" ]; then terminal=1; break; fi
  if [ $((i % 20)) -eq 0 ]; then
    echo "STRESS_PROGRESS i=$i q=$QSTATE d=$DSTATE stage=$STAGE cursor=$CURSOR total=$TOTAL"
  fi
  sleep 0.5
done

test "$terminal" -eq 1
test "$prepare_total_max" -ge 100
test "$prepare_intermediate" -eq 1
cp /tmp/stress-breadth-status.json /tmp/stress-breadth-final.json
echo "PASS_STRESS_PREPARE_MULTI_REQUEST total=$prepare_total_max"

wp option delete pste_e2e_provider_counts --path=/tmp/wordpress >/dev/null 2>&1 || true
wp option delete pste_e2e_paa_ready_count --path=/tmp/wordpress >/dev/null 2>&1 || true
wp option update pste_e2e_provider_mode normal --path=/tmp/wordpress >/dev/null
