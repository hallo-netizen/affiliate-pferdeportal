#!/usr/bin/env python3
from pathlib import Path
import hashlib
import sys

EXPECTED_SHA256 = "c2fd6d86cd9d8c8398f19185fa64f6d4cd020cfcf748ef86ca974d8f853f990a"
TARGET_VERSION = "6.72.153"
# 2026-09-25: revalidate against current authoritative 6.72.152 source tree; no semantic change.\n
if len(sys.argv) != 2:
    raise SystemExit("usage: apply_runtime_reuse_patch.py <plugin-root>")

root = Path(sys.argv[1])
main = root / "pferdeportal-affiliate-router.php"
raw = main.read_bytes()
actual = hashlib.sha256(raw).hexdigest()
if actual != EXPECTED_SHA256:
    raise SystemExit(f"FAIL exact 6.72.152 source hash mismatch: {actual}")

text = raw.decode("utf-8")

def replace_once(old, new, label):
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"FAIL {label}: expected 1 exact match, got {count}")
    text = text.replace(old, new, 1)

replace_once(
"""final class Pferdeportal_Affiliate_Router {
    private $ranked_campaigns_request_cache = array();
""",
"""final class Pferdeportal_Affiliate_Router {
    private $ranked_campaigns_request_cache = array();
    private $runtime_contract_slot_rule_request_cache = array();
""",
"request cache property"
)

replace_once(
"""        $campaign['product_identifiers'] = $this->affiliate_normalize_product_identifiers($campaign['product_identifiers'] ?? array());
        return $campaign;
""",
"""        $campaign['product_identifiers'] = $this->affiliate_normalize_product_identifiers($campaign['product_identifiers'] ?? array());

        // V6.72.153 performance-only: campaign_from_post() already performs the
        // immutable request-local normalization work. Mark and retain those
        // scalar values once so public ranking does not sanitize the same
        // campaign again for every slot.
        $campaign['_ppar_runtime_normalized'] = 1;
        $campaign['_ppar_norm_id'] = (string) $campaign['id'];
        $campaign['_ppar_norm_network'] = sanitize_key((string) ($campaign['network'] ?? 'manual'));
        $campaign['_ppar_norm_creative_type'] = sanitize_key((string) ($campaign['creative_type'] ?? 'banner'));
        $campaign['_ppar_norm_render_mode'] = sanitize_key((string) ($campaign['render_mode'] ?? 'image_link'));
        $campaign['_ppar_norm_programme_status'] = sanitize_key((string) ($campaign['programme_status'] ?? 'unknown'));
        $campaign['_ppar_norm_assignment_mode'] = sanitize_key((string) ($campaign['assignment_mode'] ?? 'page_tree'));
        return $campaign;
""",
"campaign normalization reuse"
)

replace_once(
"""    private function runtime_contract_slot_rule($slot_type) {
        $slot_type = sanitize_key((string) $slot_type);
        if ($slot_type === '' || !method_exists($this, 'output_portal_registry') || !method_exists($this, 'output_slot_matrix')) { return array(); }
        foreach ((array) $this->output_portal_registry() as $portal) {
            if (!is_array($portal) || empty($portal['enabled'])) { continue; }
            $matrix = $this->output_slot_matrix($portal);
            if (is_array($matrix) && !empty($matrix[$slot_type]) && is_array($matrix[$slot_type])) { return $matrix[$slot_type]; }
        }
        return array();
    }
""",
"""    private function runtime_contract_slot_rule($slot_type) {
        $slot_type = sanitize_key((string) $slot_type);
        if ($slot_type === '' || !method_exists($this, 'output_portal_registry') || !method_exists($this, 'output_slot_matrix')) { return array(); }
        $use_cache = $this->ranked_campaigns_request_cache_allowed();
        if ($use_cache && array_key_exists($slot_type, $this->runtime_contract_slot_rule_request_cache)) {
            return $this->runtime_contract_slot_rule_request_cache[$slot_type];
        }
        $rule = array();
        foreach ((array) $this->output_portal_registry() as $portal) {
            if (!is_array($portal) || empty($portal['enabled'])) { continue; }
            $matrix = $this->output_slot_matrix($portal);
            if (is_array($matrix) && !empty($matrix[$slot_type]) && is_array($matrix[$slot_type])) {
                $rule = $matrix[$slot_type];
                break;
            }
        }
        if ($use_cache) {
            $this->runtime_contract_slot_rule_request_cache[$slot_type] = $rule;
        }
        return $rule;
    }
""",
"slot rule request cache"
)

replace_once(
"""            $runtime_campaign = $campaign;
            $runtime_campaign['_ppar_runtime_normalized'] = 1;
            $runtime_campaign['_ppar_runtime_normalized_slot_type'] = 1;
            $runtime_campaign['_ppar_norm_id'] = sanitize_key((string) ($campaign['id'] ?? ''));
            $runtime_campaign['_ppar_norm_network'] = sanitize_key((string) ($campaign['network'] ?? 'manual'));
            $runtime_campaign['_ppar_norm_creative_type'] = sanitize_key((string) ($campaign['creative_type'] ?? 'banner'));
            $runtime_campaign['_ppar_norm_render_mode'] = sanitize_key((string) ($campaign['render_mode'] ?? 'image_link'));
            $runtime_campaign['_ppar_norm_programme_status'] = sanitize_key((string) ($campaign['programme_status'] ?? 'unknown'));
            $runtime_campaign['_ppar_norm_assignment_mode'] = sanitize_key((string) ($campaign['assignment_mode'] ?? 'page_tree'));
""",
"""            $runtime_campaign = $campaign;
            $runtime_campaign['_ppar_runtime_normalized_slot_type'] = 1;
            if (empty($runtime_campaign['_ppar_runtime_normalized'])) {
                // Defensive fallback for non-standard callers that did not come
                // through campaign_from_post(). Semantics stay identical.
                $runtime_campaign['_ppar_runtime_normalized'] = 1;
                $runtime_campaign['_ppar_norm_id'] = sanitize_key((string) ($campaign['id'] ?? ''));
                $runtime_campaign['_ppar_norm_network'] = sanitize_key((string) ($campaign['network'] ?? 'manual'));
                $runtime_campaign['_ppar_norm_creative_type'] = sanitize_key((string) ($campaign['creative_type'] ?? 'banner'));
                $runtime_campaign['_ppar_norm_render_mode'] = sanitize_key((string) ($campaign['render_mode'] ?? 'image_link'));
                $runtime_campaign['_ppar_norm_programme_status'] = sanitize_key((string) ($campaign['programme_status'] ?? 'unknown'));
                $runtime_campaign['_ppar_norm_assignment_mode'] = sanitize_key((string) ($campaign['assignment_mode'] ?? 'page_tree'));
            }
""",
"ranking normalization reuse"
)

replace_once(
"""        $assign_mode = sanitize_key((string)($campaign['assignment_mode'] ?? 'page_tree'));
""",
"""        $assign_mode = isset($campaign['_ppar_norm_assignment_mode']) ? (string) $campaign['_ppar_norm_assignment_mode'] : sanitize_key((string)($campaign['assignment_mode'] ?? 'page_tree'));
""",
"complete assignment reuse"
)

replace_once(" * Version: 6.72.152\n", f" * Version: {TARGET_VERSION}\n", "header version")
replace_once("    const VERSION = '6.72.152';\n", f"    const VERSION = '{TARGET_VERSION}';\n", "runtime version")

main.write_text(text, encoding="utf-8", newline="\n")
print("PASS applied 6.72.153 performance-only runtime reuse patch")
print("SHA256", hashlib.sha256(main.read_bytes()).hexdigest())
