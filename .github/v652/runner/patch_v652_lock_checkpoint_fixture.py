from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
old="update_option('v652_lock_checkpoint_before',serialize($cp),false);"
new="update_option('v652_lock_checkpoint_before',$cp,false);"
if s.count(old)!=1:
    raise SystemExit('BLOCKED: V6.52 lock checkpoint fixture anchor mismatch')
s=s.replace(old,new,1)
p.write_text(s)
