from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
old='6b552feb1d38d80a5265bae6642fa073417a3bf6'
new='aeac4570479ed0320e9e00bf7d534e2cfc05bc10'
if s.count(old) != 1:
    raise SystemExit('BLOCKED: V6.52 selfpump test blob-hash anchor mismatch')
p.write_text(s.replace(old,new,1))
