#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v651/runner/run-v651-full-release-wrapper.sh
[ "$(git hash-object "$BASE")" = "c8bd8cb46c0232f91f08f66eb0f5d415d96d8686" ] || { echo 'BLOCKED: base wrapper blob mismatch'; exit 1; }
echo 'd51e3a4e00b78bdbe567a1a47e87a44c10d750cb9d8c9740e6d27ffc19a8ec11  .github/v651/runner/02_step1_patch_strip_runner.patch' | sha256sum -c -
echo '3cdc47659b7b16bb86d8a081ffb70a36af08d076daf9907c6024e795ed0e895a  .github/v651/runner/03_portable_production_patch_runner.patch' | sha256sum -c -
echo 'cd167e5e3d819f0b8a11d39e3a04fda9412b6c03f90560fd89c1d656971b0962  .github/v651/runner/04_v649_superseded_contract_runner.patch' | sha256sum -c -
TMP=/tmp/run-v651-full-release-wrapper-v3-expanded.sh
python3 - <<'PY'
from pathlib import Path
src=Path('.github/v651/runner/run-v651-full-release-wrapper.sh').read_text()
needle="echo 'acdc81cf383ff8ed306738018a8d2126265d4f328053e356b9ae8fc82d3282f6  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\n\nphp -l"
insert="echo 'acdc81cf383ff8ed306738018a8d2126265d4f328053e356b9ae8fc82d3282f6  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\necho 'd51e3a4e00b78bdbe567a1a47e87a44c10d750cb9d8c9740e6d27ffc19a8ec11  .github/v651/runner/02_step1_patch_strip_runner.patch' | sha256sum -c -\npatch -p0 --forward --batch < .github/v651/runner/02_step1_patch_strip_runner.patch\necho '1b7b6ad07a8cefc60c4d142c0ca0a2628f37c46e82cf7d027df810bc4b95bdf9  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\necho '3cdc47659b7b16bb86d8a081ffb70a36af08d076daf9907c6024e795ed0e895a  .github/v651/runner/03_portable_production_patch_runner.patch' | sha256sum -c -\npatch -p0 --forward --batch < .github/v651/runner/03_portable_production_patch_runner.patch\necho 'f83f140e3433c133d667814a93ef0ff570d42ff11cf9786fe900f0acf7da9c7b  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\necho 'cd167e5e3d819f0b8a11d39e3a04fda9412b6c03f90560fd89c1d656971b0962  .github/v651/runner/04_v649_superseded_contract_runner.patch' | sha256sum -c -\npatch -p0 --forward --batch < .github/v651/runner/04_v649_superseded_contract_runner.patch\necho 'cdeb246a11af1634b91302d5b5d1438288588b42333322b91953d48bd465c9e2  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\n\nphp -l"
if needle not in src:
    raise SystemExit('BLOCKED: wrapper insertion anchor missing')
out=src.replace(needle,insert,1)
Path('/tmp/run-v651-full-release-wrapper-v3-expanded.sh').write_text(out)
PY
bash -n "$TMP"
chmod +x "$TMP"
exec "$TMP"
