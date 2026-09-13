#!/usr/bin/env bash
set -euo pipefail

TARGET_PHP_SHA=580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5
TARGET_PLUGIN_SHA=77d1d9ec05aeeac15748a49bf8ed957ac6a33868b5dec7d7d83131ae5d32a79e
mkdir -p /tmp/design-scan
: >/tmp/design-scan/results.txt
found=0
exact=0

while IFS= read -r -d '' z; do
  zsha=$(sha256sum "$z" | awk '{print $1}')
  if [ "$zsha" = "$TARGET_PLUGIN_SHA" ]; then
    echo "EXACT_PLUGIN_ZIP $z $zsha" | tee -a /tmp/design-scan/results.txt
    exact=1
  fi
  while IFS= read -r member; do
    [ -n "$member" ] || continue
    case "$member" in
      *pferde-template-kit.php|*pferde-template-kit_V*.php)
        out="/tmp/design-scan/candidate-${found}.php"
        if unzip -p "$z" "$member" >"$out" 2>/dev/null && [ -s "$out" ]; then
          sha=$(sha256sum "$out" | awk '{print $1}')
          ver=$(grep -m1 -E '^[[:space:]]*\*?[[:space:]]*Version:[[:space:]]*[0-9.]+' "$out" | sed -E 's/.*Version:[[:space:]]*//' || true)
          echo "DESIGN_SOURCE zip=$z member=$member sha=$sha version=${ver:-unknown}" | tee -a /tmp/design-scan/results.txt
          found=$((found+1))
          if [ "$sha" = "$TARGET_PHP_SHA" ]; then
            echo "EXACT_150469_PHP_FOUND $z::$member" | tee -a /tmp/design-scan/results.txt
            exact=1
          fi
        fi
        ;;
    esac
  done < <(unzip -Z1 "$z" 2>/dev/null || true)
done < <(find . -type f -name '*.zip' -print0)

echo "DESIGN_SCAN_CANDIDATES=$found EXACT=$exact"
cat /tmp/design-scan/results.txt

# Discovery is evidence, not a fake PASS. Only exact 1.50.469 bytes may turn this green.
test "$exact" = 1
echo REAL_DESIGN_EXACT_SOURCE_DISCOVERY_PASS
