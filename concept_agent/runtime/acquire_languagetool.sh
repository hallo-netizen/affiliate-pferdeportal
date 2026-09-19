#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-/tmp/concept-agent-lt68}"
ZIP="$ROOT/LanguageTool-6.8.zip"
URL="https://github.com/jxmorris12/language_tool_python/releases/download/LanguageTool-6.8/LanguageTool-6.8.zip"
ZIP_SHA="6a7f6b67b779ae9505f7579f0c41453ea8d1bd72ae750bdc2c55ba974281467d"
JAR_SHA="2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8"
mkdir -p "$ROOT"
curl --fail --location --retry 3 "$URL" -o "$ZIP"
echo "$ZIP_SHA  $ZIP" | sha256sum -c -
unzip -q -o "$ZIP" -d "$ROOT"
JAR="$ROOT/LanguageTool-6.8/languagetool-commandline.jar"
test -f "$JAR"
echo "$JAR_SHA  $JAR" | sha256sum -c -
printf '%s\n' "$JAR"
