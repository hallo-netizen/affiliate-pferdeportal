#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR/fixtures/design-1.50.469
OUT=/tmp/design-1.50.469
rm -rf "$OUT"
mkdir -p "$OUT"

# Exactly 22 chunks are required: part00..part21. No missing or extra source truth.
for i in $(seq -w 0 21); do
  test -f "$R/pferde-template-kit.php.xz.b64.part$i"
done
count=$(find "$R" -maxdepth 1 -type f -name 'pferde-template-kit.php.xz.b64.part*' | wc -l | tr -d ' ')
test "$count" = 22

cat "$R"/pferde-template-kit.php.xz.b64.part?? > "$OUT/pferde-template-kit.php.xz.b64"
base64 --decode "$OUT/pferde-template-kit.php.xz.b64" > "$OUT/pferde-template-kit.php.xz"
xz -t "$OUT/pferde-template-kit.php.xz"
xz -dc "$OUT/pferde-template-kit.php.xz" > "$OUT/pferde-template-kit.php"

test "$(wc -c < "$OUT/pferde-template-kit.php" | tr -d ' ')" = 1650857
sha=$(sha256sum "$OUT/pferde-template-kit.php" | awk '{print $1}')
test "$sha" = 580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5
php -l "$OUT/pferde-template-kit.php"
grep -q 'Version: 1.50.469' "$OUT/pferde-template-kit.php"
grep -q 'final class Pferde_Template_Kit' "$OUT/pferde-template-kit.php"

echo REAL_DESIGN_150469_RECONSTRUCT_SHA_PASS:$sha
