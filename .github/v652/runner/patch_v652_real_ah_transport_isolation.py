from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
old="repl='function rg_tick() { return rg_plugin()->run_ebay_canonical_worker(); }'"
new="repl=\"function rg_tick() { $p=rg_plugin(); $x=$p->run_ebay_canonical_worker(); remove_action('shutdown', array($p,'run_ebay_worker_background_dispatch'), PHP_INT_MAX); return $x; }\""
if s.count(old)!=1:
    raise SystemExit('BLOCKED: V6.52 real A-H canonical-tick isolation anchor mismatch')
s=s.replace(old,new,1)
oldc=""" # transport. V6.51 keeps every A-H assertion, but its versioned successor drives
 # the exact same state machine through the canonical background worker.
"""
newc=""" # transport. V6.52 keeps every A-H assertion, but its versioned successor drives
 # one exact canonical fach-worker tick at a time and suppresses only the request-shutdown
 # transport handoff inside this deterministic concurrency fixture. Autonomous transport
 # itself is proven separately below by the real no-browser HTTP self-pump gates.
"""
if s.count(oldc)!=1:
    raise SystemExit('BLOCKED: V6.52 real A-H successor comment anchor mismatch')
s=s.replace(oldc,newc,1)
oldp="printf 'V645_REAL_AH_BROWSER_TRANSPORT=EXPECTED_RED\\nV651_REAL_AH_BACKGROUND_SUCCESSOR=PASS\\n' > \"$E/$p/V651_REAL_AH_CONTRACT.txt\""
newp="printf 'V645_REAL_AH_BROWSER_TRANSPORT=EXPECTED_RED\\nV652_REAL_AH_CANONICAL_TICK_SUCCESSOR=PASS\\nV652_REAL_AH_SHUTDOWN_TRANSPORT_ISOLATED=PASS\\n' > \"$E/$p/V651_REAL_AH_CONTRACT.txt\""
if s.count(oldp)!=1:
    raise SystemExit('BLOCKED: V6.52 real A-H contract evidence anchor mismatch')
s=s.replace(oldp,newp,1)
needle="3. Ein technischer Produktionsschritt: vorhandenen kanonischen Worker sofort persistieren und WordPress-Core spawn_cron() am Shutdown anstoßen; Pause bleibt persistent und kurz. Kein zweiter Fachworker, kein plugin-eigener HTTP-Loopback.\n"
repl=needle+"3a. Historischer A-H-Konkurrenztest bleibt deterministisch: Er führt exakt manuell einen kanonischen Fach-Worker-Tick je Prozess aus und unterdrückt nur in diesem Testprozess den Shutdown-Transport. Der autonome Shutdown-/Core-Cron-Transport wird separat real per HTTP ohne Browser geprüft.\n"
if s.count(needle)!=1:
    raise SystemExit('BLOCKED: V6.52 worklog A-H isolation anchor mismatch')
s=s.replace(needle,repl,1)
needle2="09_CONCURRENCY_LEASE_CAS_CONTRACT=YES\n"
repl2=needle2+"09A_CONCURRENCY_FIXTURE_TRANSPORT_ISOLATION_AND_SEPARATE_REAL_AUTONOMOUS_PROOF=YES\n"
if s.count(needle2)!=1:
    raise SystemExit('BLOCKED: V6.52 final gate concurrency isolation anchor mismatch')
s=s.replace(needle2,repl2,1)
p.write_text(s)
