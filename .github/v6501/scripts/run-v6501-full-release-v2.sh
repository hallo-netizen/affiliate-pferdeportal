#!/usr/bin/env bash
set -euo pipefail
SRC_SCRIPT="${GITHUB_WORKSPACE:-$(pwd)}/.github/v6501/scripts/run-v6501-full-release.sh"
TMP=/tmp/run-v6501-full-release-v2.expanded.sh
cp "$SRC_SCRIPT" "$TMP"
python3 - "$TMP" <<'PY'
import sys
p=sys.argv[1]
s=open(p,encoding='utf-8').read()
old="mapfile -t changed < <(diff -qr \"$V650BASE\" \"$SRC\" | sed -E 's#^Files .*/affiliate-portal-router/([^ ]+) and .* differ$#\\1#' | sort);"
new="mapfile -t changed < <(diff -qr \"$V650BASE\" \"$SRC\" | awk -v prefix=\"$SRC/\" '$1==\"Files\" && $3==\"and\" && $5==\"differ\" {p=$4; sub(\"^\" prefix,\"\",p); print p}' | sort);"
if old not in s:
    raise SystemExit('scope parser anchor missing')
s=s.replace(old,new,1)
open(p,'w',encoding='utf-8').write(s)
PY
bash -n "$TMP"
exec bash "$TMP"
