#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v651/runner/run-v651-full-release-wrapper.sh
PATCH2=.github/v651/runner/02_step1_patch_strip_runner.patch
[ "$(git hash-object "$BASE")" = "c8bd8cb46c0232f91f08f66eb0f5d415d96d8686" ] || { echo 'BLOCKED: base wrapper blob mismatch'; exit 1; }
echo 'd51e3a4e00b78bdbe567a1a47e87a44c10d750cb9d8c9740e6d27ffc19a8ec11  .github/v651/runner/02_step1_patch_strip_runner.patch' | sha256sum -c -
TMP=/tmp/run-v651-full-release-wrapper-v3-expanded.sh
python3 - <<'PY'
from pathlib import Path
src=Path('.github/v651/runner/run-v651-full-release-wrapper.sh').read_text()
needle="echo 'acdc81cf383ff8ed306738018a8d2126265d4f328053e356b9ae8fc82d3282f6  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\n\nphp -l"
insert="echo 'acdc81cf383ff8ed306738018a8d2126265d4f328053e356b9ae8fc82d3282f6  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\necho 'd51e3a4e00b78bdbe567a1a47e87a44c10d750cb9d8c9740e6d27ffc19a8ec11  .github/v651/runner/02_step1_patch_strip_runner.patch' | sha256sum -c -\npatch -p0 --forward --batch < .github/v651/runner/02_step1_patch_strip_runner.patch\necho '1b7b6ad07a8cefc60c4d142c0ca0a2628f37c46e82cf7d027df810bc4b95bdf9  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\n\nphp -l"
if needle not in src:
    raise SystemExit('BLOCKED: wrapper insertion anchor missing')
out=src.replace(needle,insert,1)
Path('/tmp/run-v651-full-release-wrapper-v3-expanded.sh').write_text(out)
PY
bash -n "$TMP"
chmod +x "$TMP"
exec "$TMP"
