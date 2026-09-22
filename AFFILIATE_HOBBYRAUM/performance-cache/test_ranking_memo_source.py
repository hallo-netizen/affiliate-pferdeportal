#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys
if len(sys.argv)!=3:
    raise SystemExit("usage: test_ranking_memo_source.py BASE CANDIDATE")
base=Path(sys.argv[1]); cand=Path(sys.argv[2])
a=(base/'pferdeportal-affiliate-router.php').read_text(encoding='utf-8')
b=(cand/'pferdeportal-affiliate-router.php').read_text(encoding='utf-8')
sa="    private function ranked_campaigns_for_slot($context, $slot_type, $forced_campaign_id = '') {\n"
sb="    private function ranked_campaigns_for_slot_uncached($context, $slot_type, $forced_campaign_id = '') {\n"
end="    private function select_campaign_for_slot("
ia=a.index(sa); ea=a.index(end,ia)
ib=b.index(sb); eb=b.index(end,ib)
if a[ia+len(sa):ea] != b[ib+len(sb):eb]:
    raise SystemExit("FAIL original ranking body changed")
print("PASS original ranking body byte-identical")
def hashes(root):
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
ha=hashes(base); hb=hashes(cand)
changed=sorted(k for k in set(ha)|set(hb) if ha.get(k)!=hb.get(k))
print("CHANGED",changed)
if changed != ['pferdeportal-affiliate-router.php']:
    raise SystemExit("FAIL unexpected patch scope")
print("PASS only central router file changed")
