#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v651/runner/run-v651-full-release-wrapper.sh
[ "$(git hash-object "$BASE")" = "c8bd8cb46c0232f91f08f66eb0f5d415d96d8686" ] || { echo 'BLOCKED: V6.51 base wrapper blob mismatch'; exit 1; }
TMP=/tmp/run-v652-full-release-wrapper-v12-expanded.sh
cp "$BASE" "$TMP"
python3 - "$TMP" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text()
needle="echo 'acdc81cf383ff8ed306738018a8d2126265d4f328053e356b9ae8fc82d3282f6  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\n\nphp -l .github/v651_gate/test_architecture_v651.php"
insert=r'''echo 'acdc81cf383ff8ed306738018a8d2126265d4f328053e356b9ae8fc82d3282f6  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -
echo 'd51e3a4e00b78bdbe567a1a47e87a44c10d750cb9d8c9740e6d27ffc19a8ec11  .github/v651/runner/02_step1_patch_strip_runner.patch' | sha256sum -c -
patch -p0 --forward --batch < .github/v651/runner/02_step1_patch_strip_runner.patch
echo '1b7b6ad07a8cefc60c4d142c0ca0a2628f37c46e82cf7d027df810bc4b95bdf9  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -
echo '3cdc47659b7b16bb86d8a081ffb70a36af08d076daf9907c6024e795ed0e895a  .github/v651/runner/03_portable_production_patch_runner.patch' | sha256sum -c -
patch -p0 --forward --batch < .github/v651/runner/03_portable_production_patch_runner.patch
echo 'f83f140e3433c133d667814a93ef0ff570d42ff11cf9786fe900f0acf7da9c7b  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -
echo 'cd167e5e3d819f0b8a11d39e3a04fda9412b6c03f90560fd89c1d656971b0962  .github/v651/runner/04_v649_superseded_contract_runner.patch' | sha256sum -c -
patch -p0 --forward --batch < .github/v651/runner/04_v649_superseded_contract_runner.patch
echo 'cdeb246a11af1634b91302d5b5d1438288588b42333322b91953d48bd465c9e2  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -
[ "$(git hash-object .github/v651/runner/05_v645_transport_contract_runner.patch)" = "53122c11d894ca4977344101c57efd9099c1bb4f" ] || { echo 'BLOCKED: V6.45 transport-contract patch blob mismatch'; exit 1; }
patch -p0 --forward --batch < .github/v651/runner/05_v645_transport_contract_runner.patch
echo 'c8386a4a07c35082a2ca470ab27cfabaca4dd9574c95971cdaa85ca84a46c486  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -
[ "$(git hash-object .github/v651/runner/06_v643_transport_contract_runner.patch)" = "d40ae205a9f115076ccd410a0fe06da55f2c14ba" ] || { echo 'BLOCKED: V6.43 transport-contract patch blob mismatch'; exit 1; }
patch -p0 --forward --batch < .github/v651/runner/06_v643_transport_contract_runner.patch
echo 'bd1f2e3605306d51b678ad481c947de5c27fbcb6a4e1ee1745c02e906c11d8be  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -
[ "$(git hash-object .github/v651/runner/07_cleanup_rootfix_and_v650_contract_runner.patch)" = "4452fa78addda9a7e8812b2ecde9ca5b59d1519f" ] || { echo 'BLOCKED: cleanup/V6.50 contract runner patch blob mismatch'; exit 1; }
patch -p0 --forward --batch < .github/v651/runner/07_cleanup_rootfix_and_v650_contract_runner.patch
echo '320e8d172b59f018acef67e78b46a28006cf18f26af45e08330f43b06789f522  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -
[ "$(git hash-object .github/v651/runner/08_r5_v651_successor_contract_runner.patch)" = "400c8a50bfe37fbf92afa0dec5ea6bb205f734c1" ] || { echo 'BLOCKED: R5 V6.51 successor-contract patch blob mismatch'; exit 1; }
patch -p0 --forward --batch < .github/v651/runner/08_r5_v651_successor_contract_runner.patch
echo '0e8ac3fa514ac9cf9e25bbe095f84bafa2ea5d002ad7c8aed0995eea9931e698  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -
[ "$(git hash-object .github/v651/runner/09_real_gate_version_parameterization_runner.patch)" = "df34f3ad40cfeebb083a76eea3f968c26df5604d" ] || { echo 'BLOCKED: real-gate version parameterization patch blob mismatch'; exit 1; }
patch -p0 --forward --batch < .github/v651/runner/09_real_gate_version_parameterization_runner.patch
echo '5b024809f96d1fa1e61461aa6aca35e8ab60bcfa3a9c531a77bf3d21c6623721  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -
[ "$(git hash-object .github/v651/runner/10_real_ah_v651_successor_runner.patch)" = "9e4bf451f3c8f448a61c603cc7f30116fc7c44f4" ] || { echo 'BLOCKED: real A-H V6.51 successor patch blob mismatch'; exit 1; }
patch -p0 --forward --batch < .github/v651/runner/10_real_ah_v651_successor_runner.patch
echo '625b5549e9742dd3b619af55ea1a8a1a33e50cb6c6f7762f4f51ecf89b0d61e1  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -
[ "$(git hash-object .github/v651/runner/11_real_ah_runtime_seed_contract_runner.patch)" = "3681b80c8819cd01c1db9e3de9b7185fd536a238" ] || { echo 'BLOCKED: real A-H runtime seed patch blob mismatch'; exit 1; }
patch -p0 --forward --batch < .github/v651/runner/11_real_ah_runtime_seed_contract_runner.patch
echo 'dacce5b47155af5722688ccbecb2d58cb9d51131c5747d04c38d96cc30e02ff7  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -
[ "$(git hash-object .github/v651/runner/12_real_v649_checkpoint_successor_runner.patch)" = "84ac4eaa0796f429041d03dfd56bc85dda2992e4" ] || { echo 'BLOCKED: real V6.49 checkpoint successor patch blob mismatch'; exit 1; }
patch -p0 --forward --batch < .github/v651/runner/12_real_v649_checkpoint_successor_runner.patch
echo '61706d7d596ab61de03f18e331d7d922ea48c50958fb083893cf92dfed14bf74  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -
[ "$(git hash-object .github/v651/runner/13_real_db_reset_isolation_runner.patch)" = "cbf75091f866054e0757b8559972e21cc01c73e4" ] || { echo 'BLOCKED: real DB reset isolation patch blob mismatch'; exit 1; }
patch -p0 --forward --batch < .github/v651/runner/13_real_db_reset_isolation_runner.patch
echo '391ef9fe9cfff8c907dc2d4964775665adc3c7b48d5240521812f56e24b273b8  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -
[ "$(git hash-object .github/v652/runner/14_v652_gate_runner.patch.b64.00)" = "ec2ba24e08af1ea4782640596dd9b6aca5027630" ] || { echo 'BLOCKED: V6.52 gate chunk 00 mismatch'; exit 1; }
[ "$(git hash-object .github/v652/runner/14_v652_gate_runner.patch.b64.01)" = "d4671b49dbf1d59dc25ae9267288e23aeab93f80" ] || { echo 'BLOCKED: V6.52 gate chunk 01 mismatch'; exit 1; }
[ "$(git hash-object .github/v652/runner/14_v652_gate_runner.patch.b64.02)" = "4fd66c7eaa6c8d341106ff28e5ed6e8037c2467c" ] || { echo 'BLOCKED: V6.52 gate chunk 02 mismatch'; exit 1; }
[ "$(git hash-object .github/v652/runner/14_v652_gate_runner.patch.b64.03)" = "10e3f6101e6fa6815bcc779ef64d3591fe96dc6e" ] || { echo 'BLOCKED: V6.52 gate chunk 03 mismatch'; exit 1; }
[ "$(git hash-object .github/v652/runner/14_v652_gate_runner.patch.b64.04)" = "73713ed58ea262f7d6946486a06e09ebb070b16b" ] || { echo 'BLOCKED: V6.52 gate chunk 04 mismatch'; exit 1; }
[ "$(git hash-object .github/v652/runner/14_v652_gate_runner.patch.b64.05)" = "67e5014d510ef1aa103b0129d65ba82ab9ca2472" ] || { echo 'BLOCKED: V6.52 gate chunk 05 mismatch'; exit 1; }
[ "$(git hash-object .github/v652/runner/14_v652_gate_runner.patch.b64.06)" = "e1936201343a68ae6573c3242fd250e36394b787" ] || { echo 'BLOCKED: V6.52 gate chunk 06 mismatch'; exit 1; }
cat .github/v652/runner/14_v652_gate_runner.patch.b64.0{0,1,2,3,4,5,6} > /tmp/v652-gate-runner.patch.b64
base64 -d /tmp/v652-gate-runner.patch.b64 > /tmp/v652-gate-runner.patch
echo '196ac087f7b9bb07892b74f204f1c0c42016dd4fbd6e0b6ca5b339965f36d87e  /tmp/v652-gate-runner.patch' | sha256sum -c -
patch -p0 --forward --batch < /tmp/v652-gate-runner.patch
echo '4d142e919eadde2143faad380617f9d43317a6bdcd652d70d415a8aff55476b4  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -

php -l .github/v651_gate/test_architecture_v651.php'''
if needle not in s:
    raise SystemExit('BLOCKED: direct V6.51 gate insertion anchor missing')
p.write_text(s.replace(needle,insert,1))
PY
bash -n "$TMP"
chmod +x "$TMP"
set +e
"$TMP"
rc=$?
set -e
if [ "$rc" -ne 0 ]; then
  D=V652_RELEASE_EVIDENCE/BLOCKED_DIAGNOSTIC_V12
  mkdir -p "$D"
  [ ! -d /tmp/v652-source/affiliate-portal-router ] || cp -a /tmp/v652-source/affiliate-portal-router "$D/affiliate-portal-router"
  [ ! -f .github/v651_gate/run-v651-full-release.sh ] || cp .github/v651_gate/run-v651-full-release.sh "$D/run-v652-full-release.final.sh"
  (cd "$D" && find . -type f -print0 | sort -z | xargs -0 sha256sum) > "$D/SHA256.txt" || true
fi
exit "$rc"
