#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v652/runner/run-v652-full-release-wrapper-v12.sh
[ "$(git hash-object "$BASE")" = "141280f70b077be77c5933c10a7709679b39aa5c" ] || { echo 'BLOCKED: V6.52 v12 wrapper blob mismatch'; exit 1; }
printf '%s\n' \
 'd45372c8ec92f0d7c65943c4c787512dd83f1d2adfca86001099c6e93e7c042f  .github/v652/runner/transform_v651_gate_to_v652.py.gz.b64.00' \
 'fd7485c7b49e4b4f20a4dbf96865e6b53080443b9baa5c9a4975272eaa690069  .github/v652/runner/transform_v651_gate_to_v652.py.gz.b64.01' \
 '85e00c5805aa0c8d8831c127c107650da535b4e70d0e12d1e34fc6f259aaf659  .github/v652/runner/transform_v651_gate_to_v652.py.gz.b64.02' | sha256sum -c -
cat .github/v652/runner/transform_v651_gate_to_v652.py.gz.b64.0{0,1,2} > /tmp/v652-transform.b64
echo 'a0ec112e855cd7dd7b1d53a1964a134716febf4777b927cd298b441bdbdd8e3d  /tmp/v652-transform.b64' | sha256sum -c -
base64 -d /tmp/v652-transform.b64 > /tmp/v652-transform.py.gz
echo 'abc70b24bda0fd021ce8ea046a04370dcd7e315dba2522cc2b1603245f9915f7  /tmp/v652-transform.py.gz' | sha256sum -c -
gzip -dc /tmp/v652-transform.py.gz > /tmp/transform_v651_gate_to_v652.py
echo '20eb937d72297aa5a12e53529333467cfaa8fec4a1c4bf6f1d779c5a8b25173e  /tmp/transform_v651_gate_to_v652.py' | sha256sum -c -
python3 -m py_compile /tmp/transform_v651_gate_to_v652.py
TMP=/tmp/run-v652-full-release-wrapper-v14-expanded.sh
python3 - "$BASE" "$TMP" <<'PY'
from pathlib import Path
import sys
s=Path(sys.argv[1]).read_text()
start='[ "$(git hash-object .github/v652/runner/14_v652_gate_runner.patch.b64.00)" = "ec2ba24e08af1ea4782640596dd9b6aca5027630" ]'
end="echo '4d142e919eadde2143faad380617f9d43317a6bdcd652d70d415a8aff55476b4  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -"
i=s.find(start); j=s.find(end,i)
if i < 0 or j < 0: raise SystemExit('BLOCKED: obsolete V6.52 post13 block not found exactly')
j += len(end)
replacement="python3 /tmp/transform_v651_gate_to_v652.py .github/v651_gate/run-v651-full-release.sh\necho 'e63287d0766ff1b6bde32b089027c649f2734e4ddc68241af10a6c03adc7f9c0  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -"
Path(sys.argv[2]).write_text(s[:i]+replacement+s[j:])
PY
bash -n "$TMP"
chmod +x "$TMP"
"$TMP"
