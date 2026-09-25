#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v651/runner/run-v651-full-release-wrapper.sh
[ "$(git hash-object "$BASE")" = "c8bd8cb46c0232f91f08f66eb0f5d415d96d8686" ] || { echo 'BLOCKED: base wrapper blob mismatch'; exit 1; }
echo 'd51e3a4e00b78bdbe567a1a47e87a44c10d750cb9d8c9740e6d27ffc19a8ec11  .github/v651/runner/02_step1_patch_strip_runner.patch' | sha256sum -c -
echo '3cdc47659b7b16bb86d8a081ffb70a36af08d076daf9907c6024e795ed0e895a  .github/v651/runner/03_portable_production_patch_runner.patch' | sha256sum -c -
echo 'cd167e5e3d819f0b8a11d39e3a04fda9412b6c03f90560fd89c1d656971b0962  .github/v651/runner/04_v649_superseded_contract_runner.patch' | sha256sum -c -
[ "$(git hash-object .github/v651/runner/05_v645_transport_contract_runner.patch)" = "53122c11d894ca4977344101c57efd9099c1bb4f" ] || { echo 'BLOCKED: V6.45 transport-contract patch blob mismatch'; exit 1; }
[ "$(git hash-object .github/v651/runner/06_v643_transport_contract_runner.patch)" = "d40ae205a9f115076ccd410a0fe06da55f2c14ba" ] || { echo 'BLOCKED: V6.43 transport-contract patch blob mismatch'; exit 1; }
[ "$(git hash-object .github/v651/runner/07_cleanup_rootfix_and_v650_contract_runner.patch)" = "4452fa78addda9a7e8812b2ecde9ca5b59d1519f" ] || { echo 'BLOCKED: cleanup/V6.50 contract runner patch blob mismatch'; exit 1; }
[ "$(git hash-object .github/v651/runner/08_r5_v651_successor_contract_runner.patch)" = "400c8a50bfe37fbf92afa0dec5ea6bb205f734c1" ] || { echo 'BLOCKED: R5 V6.51 successor-contract patch blob mismatch'; exit 1; }
TMP=/tmp/run-v651-full-release-wrapper-v3-expanded.sh
python3 - <<'PY'
from pathlib import Path
src=Path('.github/v651/runner/run-v651-full-release-wrapper.sh').read_text()
needle="echo 'acdc81cf383ff8ed306738018a8d2126265d4f328053e356b9ae8fc82d3282f6  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\n\nphp -l"
insert="echo 'acdc81cf383ff8ed306738018a8d2126265d4f328053e356b9ae8fc82d3282f6  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\necho 'd51e3a4e00b78bdbe567a1a47e87a44c10d750cb9d8c9740e6d27ffc19a8ec11  .github/v651/runner/02_step1_patch_strip_runner.patch' | sha256sum -c -\npatch -p0 --forward --batch < .github/v651/runner/02_step1_patch_strip_runner.patch\necho '1b7b6ad07a8cefc60c4d142c0ca0a2628f37c46e82cf7d027df810bc4b95bdf9  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\necho '3cdc47659b7b16bb86d8a081ffb70a36af08d076daf9907c6024e795ed0e895a  .github/v651/runner/03_portable_production_patch_runner.patch' | sha256sum -c -\npatch -p0 --forward --batch < .github/v651/runner/03_portable_production_patch_runner.patch\necho 'f83f140e3433c133d667814a93ef0ff570d42ff11cf9786fe900f0acf7da9c7b  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\necho 'cd167e5e3d819f0b8a11d39e3a04fda9412b6c03f90560fd89c1d656971b0962  .github/v651/runner/04_v649_superseded_contract_runner.patch' | sha256sum -c -\npatch -p0 --forward --batch < .github/v651/runner/04_v649_superseded_contract_runner.patch\necho 'cdeb246a11af1634b91302d5b5d1438288588b42333322b91953d48bd465c9e2  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\n[ \"$(git hash-object .github/v651/runner/05_v645_transport_contract_runner.patch)\" = \"53122c11d894ca4977344101c57efd9099c1bb4f\" ] || { echo 'BLOCKED: V6.45 transport-contract patch blob mismatch'; exit 1; }\npatch -p0 --forward --batch < .github/v651/runner/05_v645_transport_contract_runner.patch\necho 'c8386a4a07c35082a2ca470ab27cfabaca4dd9574c95971cdaa85ca84a46c486  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\n[ \"$(git hash-object .github/v651/runner/06_v643_transport_contract_runner.patch)\" = \"d40ae205a9f115076ccd410a0fe06da55f2c14ba\" ] || { echo 'BLOCKED: V6.43 transport-contract patch blob mismatch'; exit 1; }\npatch -p0 --forward --batch < .github/v651/runner/06_v643_transport_contract_runner.patch\necho 'bd1f2e3605306d51b678ad481c947de5c27fbcb6a4e1ee1745c02e906c11d8be  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\n[ \"$(git hash-object .github/v651/runner/07_cleanup_rootfix_and_v650_contract_runner.patch)\" = \"4452fa78addda9a7e8812b2ecde9ca5b59d1519f\" ] || { echo 'BLOCKED: cleanup/V6.50 contract runner patch blob mismatch'; exit 1; }\npatch -p0 --forward --batch < .github/v651/runner/07_cleanup_rootfix_and_v650_contract_runner.patch\necho '320e8d172b59f018acef67e78b46a28006cf18f26af45e08330f43b06789f522  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\n[ \"$(git hash-object .github/v651/runner/08_r5_v651_successor_contract_runner.patch)\" = \"400c8a50bfe37fbf92afa0dec5ea6bb205f734c1\" ] || { echo 'BLOCKED: R5 V6.51 successor-contract patch blob mismatch'; exit 1; }\npatch -p0 --forward --batch < .github/v651/runner/08_r5_v651_successor_contract_runner.patch\necho '0e8ac3fa514ac9cf9e25bbe095f84bafa2ea5d002ad7c8aed0995eea9931e698  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\n\nphp -l"
if needle not in src:
    raise SystemExit('BLOCKED: wrapper insertion anchor missing')
out=src.replace(needle,insert,1)
Path('/tmp/run-v651-full-release-wrapper-v3-expanded.sh').write_text(out)
PY
bash -n "$TMP"
chmod +x "$TMP"
set +e
"$TMP"
rc=$?
set -e
if [ "$rc" -ne 0 ]; then
  D=V651_RELEASE_EVIDENCE/BLOCKED_DIAGNOSTIC
  R5=/tmp/v651pkg/CODEX_V645_REALGATE_SOURCE_AND_EXACT_TASK_20260820/04_TESTS/HISTORICAL_R5_54
  mkdir -p "$D"
  if [ -d /tmp/v651-source/affiliate-portal-router ] && [ -d "$R5" ]; then
    cp -a /tmp/v651-source/affiliate-portal-router "$D/affiliate-portal-router"
    cp -a "$R5" "$D/HISTORICAL_R5_54"
    if [ -f .github/v651_gate/01_checkpoint_restart.patch ]; then cp .github/v651_gate/01_checkpoint_restart.patch "$D/01_checkpoint_restart.patch"; fi
    if [ -f .github/v651_gate/run-v651-full-release.sh ]; then cp .github/v651_gate/run-v651-full-release.sh "$D/run-v651-full-release.final.sh"; fi
    (
      cd "$D"
      find affiliate-portal-router HISTORICAL_R5_54 -type f -print0 | sort -z | xargs -0 sha256sum
      [ ! -f 01_checkpoint_restart.patch ] || sha256sum 01_checkpoint_restart.patch
      [ ! -f run-v651-full-release.final.sh ] || sha256sum run-v651-full-release.final.sh
    ) > "$D/SHA256.txt"
  fi
fi
exit "$rc"
