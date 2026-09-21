#!/usr/bin/env bash
set -euo pipefail
rm -f /tmp/pste-serial-owner-ready /tmp/pste-serial-owner-done /tmp/pste-serial-negative.txt /tmp/pste-serial-positive.txt
(
  wp eval '$a=new ReflectionMethod("PSTE_Research_Driver","acquireLock");$a->setAccessible(true);$r=new ReflectionMethod("PSTE_Research_Driver","releaseLock");$r->setAccessible(true);$t=$a->invoke(null);file_put_contents("/tmp/pste-serial-owner-ready",$t);$r->invoke(null,$t);sleep(6);file_put_contents("/tmp/pste-serial-owner-done","1");' --path=/tmp/wordpress
) &
owner_pid=$!
for i in $(seq 1 30); do
  test -s /tmp/pste-serial-owner-ready && break
  sleep 0.2
done
test -s /tmp/pste-serial-owner-ready
set +e
wp eval 'try{$a=new ReflectionMethod("PSTE_Research_Driver","acquireLock");$a->setAccessible(true);$a->invoke(null);echo "UNEXPECTED_SECOND_ACQUIRE\n";exit(9);}catch(Throwable $e){echo $e->getMessage()."\n";if(strpos($e->getMessage(),"PSTE_RESEARCH_DRIVER_ALREADY_RUNNING")===false)exit(8);}' --path=/tmp/wordpress > /tmp/pste-serial-negative.txt 2>&1
neg_rc=$?
set -e
test "$neg_rc" -eq 0
grep -q 'PSTE_RESEARCH_DRIVER_ALREADY_RUNNING' /tmp/pste-serial-negative.txt
test ! -e /tmp/pste-serial-owner-done
wait "$owner_pid"
test -s /tmp/pste-serial-owner-done
wp eval '$a=new ReflectionMethod("PSTE_Research_Driver","acquireLock");$a->setAccessible(true);$r=new ReflectionMethod("PSTE_Research_Driver","releaseLock");$r->setAccessible(true);$t=$a->invoke(null);echo "PASS_SERIAL_REACQUIRE_AFTER_OWNER_EXIT\n";$r->invoke(null,$t);' --path=/tmp/wordpress | tee /tmp/pste-serial-positive.txt
grep -q 'PASS_SERIAL_REACQUIRE_AFTER_OWNER_EXIT' /tmp/pste-serial-positive.txt
echo PASS_STRICT_SERIAL_DRIVER_POSITIVE_NEGATIVE
