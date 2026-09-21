#!/usr/bin/env bash
set -euo pipefail
NONCE="$(cat /tmp/nonce)"
wp option delete pste_e2e_provider_counts --path=/tmp/wordpress >/dev/null 2>&1 || true
wp option delete pste_e2e_paa_ready_count --path=/tmp/wordpress >/dev/null 2>&1 || true
wp option update pste_e2e_provider_mode stress_prepare_100 --path=/tmp/wordpress >/dev/null

curl -fsS -b /tmp/pste-cookies.txt -c /tmp/pste-cookies.txt   --data-urlencode 'action=pste_breadth_research_start'   --data-urlencode "nonce=$NONCE"   --data-urlencode 'target_usable=1'   --data-urlencode 'max_items=1'   --data-urlencode 'confirm_cost=1'   http://127.0.0.1:8090/wp-admin/admin-ajax.php >/tmp/cancel-start.json
QUEUE_UUID="$(php -r '$x=json_decode(file_get_contents("/tmp/cancel-start.json"),true);if(!is_array($x)||empty($x["success"]))exit(2);echo $x["data"]["queue"]["queue_uuid"]??"";')"
test -n "$QUEUE_UUID"

seen_prepare=0
for i in $(seq 1 300); do
  curl -fsS -b /tmp/pste-cookies.txt     --data-urlencode 'action=pste_breadth_research_status'     --data-urlencode "nonce=$NONCE"     --data-urlencode "queue_uuid=$QUEUE_UUID"     http://127.0.0.1:8090/wp-admin/admin-ajax.php >/tmp/cancel-pre-status.json
  STAGE="$(php -r '$x=json_decode(file_get_contents("/tmp/cancel-pre-status.json"),true);echo $x["data"]["queue"]["child"]["finalize_stage"]??"";')"
  CURSOR="$(php -r '$x=json_decode(file_get_contents("/tmp/cancel-pre-status.json"),true);echo (int)($x["data"]["queue"]["child"]["finalize_prepare_cursor"]??0);')"
  TOTAL="$(php -r '$x=json_decode(file_get_contents("/tmp/cancel-pre-status.json"),true);echo (int)($x["data"]["queue"]["child"]["finalize_prepare_total"]??0);')"
  DHEALTH="$(php -r '$x=json_decode(file_get_contents("/tmp/cancel-pre-status.json"),true);echo $x["data"]["driver"]["health_code"]??"";')"
  if [ "$DHEALTH" = "PSTE_DRIVER_STEP_OVERDUE" ]; then echo CANCEL_PROOF_STEP_OVERDUE_BEFORE_CANCEL; cat /tmp/cancel-pre-status.json; exit 1; fi
  if [ "$STAGE" = "PREPARE_CANDIDATES" ] && [ "$TOTAL" -ge 100 ]; then
    seen_prepare=1
    echo "PASS_CANCEL_PROOF_REACHED_PREPARE cursor=$CURSOR total=$TOTAL"
    break
  fi
  sleep 0.2
done
test "$seen_prepare" -eq 1

curl -fsS -b /tmp/pste-cookies.txt   --data-urlencode 'action=pste_breadth_research_cancel'   --data-urlencode "nonce=$NONCE"   --data-urlencode "queue_uuid=$QUEUE_UUID"   http://127.0.0.1:8090/wp-admin/admin-ajax.php >/tmp/cancel-response.json
grep -q '"success":true' /tmp/cancel-response.json

cancelled=0
for i in $(seq 1 120); do
  curl -fsS -b /tmp/pste-cookies.txt     --data-urlencode 'action=pste_breadth_research_status'     --data-urlencode "nonce=$NONCE"     --data-urlencode "queue_uuid=$QUEUE_UUID"     http://127.0.0.1:8090/wp-admin/admin-ajax.php >/tmp/cancel-status.json
  QSTATE="$(php -r '$x=json_decode(file_get_contents("/tmp/cancel-status.json"),true);echo $x["data"]["queue"]["status"]??"INVALID";')"
  DSTATE="$(php -r '$x=json_decode(file_get_contents("/tmp/cancel-status.json"),true);echo $x["data"]["driver"]["status"]??"INVALID";')"
  DHEALTH="$(php -r '$x=json_decode(file_get_contents("/tmp/cancel-status.json"),true);echo $x["data"]["driver"]["health_code"]??"";')"
  AGE="$(php -r '$x=json_decode(file_get_contents("/tmp/cancel-status.json"),true);echo (int)($x["data"]["driver"]["active_step_age_seconds"]??0);')"
  if [ "$DHEALTH" = "PSTE_DRIVER_STEP_OVERDUE" ] || [ "$AGE" -gt 20 ]; then
    echo CANCEL_PROOF_DRIVER_STUCK
    cat /tmp/cancel-status.json
    exit 1
  fi
  if [ "$QSTATE" = "CANCELLED" ] && [ "$DSTATE" = "IDLE" ]; then cancelled=1; break; fi
  sleep 0.25
done
test "$cancelled" -eq 1 || { echo CANCEL_PROOF_DID_NOT_SETTLE; cat /tmp/cancel-status.json; exit 1; }
php -r '$x=json_decode(file_get_contents("/tmp/cancel-status.json"),true);$q=$x["data"]["queue"]??[];if(!empty($q["cancel_requested"]))exit(2);if(($q["completion_reason"]??"")!=="CANCELLED_BY_USER")exit(3);if(isset($q["child"])&&$q["child"]!==null)exit(4);echo "PASS_SAFE_CANCEL_DURING_PREPARE_SETTLES_CLEANLY\n";'

wp option delete pste_e2e_provider_counts --path=/tmp/wordpress >/dev/null 2>&1 || true
wp option delete pste_e2e_paa_ready_count --path=/tmp/wordpress >/dev/null 2>&1 || true
wp option update pste_e2e_provider_mode stress_prepare_100 --path=/tmp/wordpress >/dev/null
