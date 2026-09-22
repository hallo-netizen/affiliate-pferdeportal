#!/usr/bin/env bash
set -euo pipefail
NONCE="$(cat /tmp/nonce)"

# Normal provider volume: this proof is about durable wave continuation, not provider stress.
wp option delete pste_e2e_provider_counts --path=/tmp/wordpress >/dev/null 2>&1 || true
wp option delete pste_e2e_paa_ready_count --path=/tmp/wordpress >/dev/null 2>&1 || true
wp option update pste_e2e_provider_mode normal --path=/tmp/wordpress >/dev/null

curl -fsS -b /tmp/pste-cookies.txt -c /tmp/pste-cookies.txt   --data-urlencode 'action=pste_breadth_research_start'   --data-urlencode "nonce=$NONCE"   --data-urlencode 'target_usable=40'   --data-urlencode 'max_items=40'   --data-urlencode 'confirm_cost=1'   http://127.0.0.1:8090/wp-admin/admin-ajax.php >/tmp/continue-start-1.json

Q1="$(php -r '$x=json_decode(file_get_contents("/tmp/continue-start-1.json"),true);if(!is_array($x)||empty($x["success"]))exit(2);echo $x["data"]["queue"]["queue_uuid"]??"";')"
test -n "$Q1"

progress=0
for i in $(seq 1 240); do
  curl -fsS -b /tmp/pste-cookies.txt     --data-urlencode 'action=pste_breadth_research_status'     --data-urlencode "nonce=$NONCE"     --data-urlencode "queue_uuid=$Q1"     http://127.0.0.1:8090/wp-admin/admin-ajax.php >/tmp/continue-progress.json

  QSTATE="$(php -r '$x=json_decode(file_get_contents("/tmp/continue-progress.json"),true);echo $x["data"]["queue"]["status"]??"INVALID";')"
  DSTATE="$(php -r '$x=json_decode(file_get_contents("/tmp/continue-progress.json"),true);echo $x["data"]["driver"]["status"]??"INVALID";')"
  DHEALTH="$(php -r '$x=json_decode(file_get_contents("/tmp/continue-progress.json"),true);echo $x["data"]["driver"]["health_code"]??"";')"
  USABLE="$(php -r '$x=json_decode(file_get_contents("/tmp/continue-progress.json"),true);echo (int)($x["data"]["queue"]["usable_candidate_count"]??0);')"
  COMPLETE="$(php -r '$x=json_decode(file_get_contents("/tmp/continue-progress.json"),true);echo (int)($x["data"]["queue"]["completed_count"]??0);')"
  BACKLOG="$(php -r '$x=json_decode(file_get_contents("/tmp/continue-progress.json"),true);echo !empty($x["data"]["queue"]["local_backlog_complete"])?"1":"0";')"

  if [ "$DSTATE" = "BLOCKED" ] || [ "$DHEALTH" = "PSTE_DRIVER_STEP_OVERDUE" ]; then
    echo CONTINUATION_PROOF_DRIVER_BLOCKED
    cat /tmp/continue-progress.json
    exit 1
  fi
  if [ "$QSTATE" != "RUNNING" ]; then
    echo CONTINUATION_PROOF_WAVE_TERMINATED_BEFORE_PROGRESS
    cat /tmp/continue-progress.json
    exit 1
  fi
  if [ "$BACKLOG" = "1" ] && [ "$USABLE" -gt 0 ] && [ "$COMPLETE" -gt 0 ]; then
    progress=1
    echo "PASS_CONTINUATION_PROOF_PROGRESS_BEFORE_CANCEL usable=$USABLE complete=$COMPLETE"
    break
  fi
  sleep 1
done
test "$progress" -eq 1
OLD_USABLE="$(php -r '$x=json_decode(file_get_contents("/tmp/continue-progress.json"),true);echo (int)$x["data"]["queue"]["usable_candidate_count"];')"

curl -fsS -b /tmp/pste-cookies.txt   --data-urlencode 'action=pste_breadth_research_cancel'   --data-urlencode "nonce=$NONCE"   --data-urlencode "queue_uuid=$Q1"   http://127.0.0.1:8090/wp-admin/admin-ajax.php >/tmp/continue-cancel.json
grep -q '"success":true' /tmp/continue-cancel.json

settled=0
for i in $(seq 1 120); do
  curl -fsS -b /tmp/pste-cookies.txt     --data-urlencode 'action=pste_breadth_research_status'     --data-urlencode "nonce=$NONCE"     --data-urlencode "queue_uuid=$Q1"     http://127.0.0.1:8090/wp-admin/admin-ajax.php >/tmp/continue-cancel-status.json
  QSTATE="$(php -r '$x=json_decode(file_get_contents("/tmp/continue-cancel-status.json"),true);echo $x["data"]["queue"]["status"]??"INVALID";')"
  DSTATE="$(php -r '$x=json_decode(file_get_contents("/tmp/continue-cancel-status.json"),true);echo $x["data"]["driver"]["status"]??"INVALID";')"
  if [ "$QSTATE" = "CANCELLED" ] && [ "$DSTATE" = "IDLE" ]; then settled=1; break; fi
  sleep 0.25
done
test "$settled" -eq 1

curl -fsS -b /tmp/pste-cookies.txt -c /tmp/pste-cookies.txt   --data-urlencode 'action=pste_breadth_research_start'   --data-urlencode "nonce=$NONCE"   --data-urlencode 'target_usable=40'   --data-urlencode 'max_items=40'   --data-urlencode 'confirm_cost=1'   http://127.0.0.1:8090/wp-admin/admin-ajax.php >/tmp/continue-start-2.json

Q2="$(php -r '$x=json_decode(file_get_contents("/tmp/continue-start-2.json"),true);if(!is_array($x)||empty($x["success"]))exit(2);echo $x["data"]["queue"]["queue_uuid"]??"";')"
test -n "$Q2"
test "$Q1" != "$Q2"

Q1="$Q1" OLD_USABLE="$OLD_USABLE" php -r '
$x=json_decode(file_get_contents("/tmp/continue-start-2.json"),true);
$q=$x["data"]["queue"]??[];
$old=(int)getenv("OLD_USABLE");
if(($q["continued_from_queue_uuid"]??"")!==getenv("Q1")){fwrite(STDERR,"CONTINUATION_QUEUE_UUID_NOT_PRESERVED\n");exit(2);}
if((int)($q["continued_usable_candidate_count"]??0)<$old){fwrite(STDERR,"CONTINUATION_COUNT_NOT_PRESERVED\n");exit(3);}
if((int)($q["usable_candidate_count"]??0)<$old){fwrite(STDERR,"CONTINUATION_VISIBLE_COUNT_RESET\n");exit(4);}
if(empty($q["local_backlog_complete"])) {fwrite(STDERR,"CONTINUATION_LOCAL_BACKLOG_RESTARTED\n");exit(5);}
echo "PASS_CANCELLED_WAVE_PROGRESS_CONTINUED old=".$old." new=".(int)$q["usable_candidate_count"]."\n";
'

# Leave the fixture terminal and clean for the following stress proof.
curl -fsS -b /tmp/pste-cookies.txt   --data-urlencode 'action=pste_breadth_research_cancel'   --data-urlencode "nonce=$NONCE"   --data-urlencode "queue_uuid=$Q2"   http://127.0.0.1:8090/wp-admin/admin-ajax.php >/tmp/continue-final-cancel.json

for i in $(seq 1 120); do
  curl -fsS -b /tmp/pste-cookies.txt     --data-urlencode 'action=pste_breadth_research_status'     --data-urlencode "nonce=$NONCE"     --data-urlencode "queue_uuid=$Q2"     http://127.0.0.1:8090/wp-admin/admin-ajax.php >/tmp/continue-final-status.json
  QSTATE="$(php -r '$x=json_decode(file_get_contents("/tmp/continue-final-status.json"),true);echo $x["data"]["queue"]["status"]??"INVALID";')"
  DSTATE="$(php -r '$x=json_decode(file_get_contents("/tmp/continue-final-status.json"),true);echo $x["data"]["driver"]["status"]??"INVALID";')"
  if [ "$QSTATE" = "CANCELLED" ] && [ "$DSTATE" = "IDLE" ]; then
    echo PASS_CONTINUATION_PROOF_TERMINAL_CLEAN
    break
  fi
  sleep 0.25
done
