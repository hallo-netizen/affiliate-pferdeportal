#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PHP_BIN="${PHP_BIN:-php}"

ROUTER="$ROOT/release/affiliate-zentrale/current/affiliate-portal-router/pferdeportal-affiliate-router.php"
AUTOMATION="$ROOT/release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-automation-suite.php"
AWIN_GATE="$ROOT/release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-awin-programme-gate.php"
OUTPUT="$ROOT/release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-output-objects.php"
ARTICLES="$ROOT/release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-article-plans.php"
CREATIVE="$ROOT/release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-creative-library.php"
EBAY="$ROOT/release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-ebay.php"
SOURCE_PLAN="$ROOT/release/affiliate-zentrale/current/affiliate-portal-router/includes/class-ppar-product-source-plan.php"
ANALYTICS="$ROOT/release/affiliate-zentrale/current/affiliate-portal-router/includes/class-ppar-partner-analytics.php"
RADAR="$ROOT/release/affiliate-zentrale/current/affiliate-portal-router/includes/class-ppar-deal-radar.php"

for file in "$ROUTER" "$AUTOMATION" "$AWIN_GATE" "$OUTPUT" "$ARTICLES" "$CREATIVE" "$EBAY" "$SOURCE_PLAN" "$ANALYTICS" "$RADAR"; do
  "$PHP_BIN" -l "$file" >/dev/null
  echo "PASS: php syntax $(basename "$file")"
done

"$PHP_BIN" "$ROOT/AFFILIATE_HOBBYRAUM/test_otto_automation.php"
"$PHP_BIN" "$ROOT/AFFILIATE_HOBBYRAUM/test_banner_distribution_behavior.php"

echo "ALL DIRECT OTTO/AWIN HOBBYROOM CHECKS PASS"
