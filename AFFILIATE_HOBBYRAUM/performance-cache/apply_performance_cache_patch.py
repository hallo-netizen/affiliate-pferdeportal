#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else 'affiliate-portal-router')

def replace_once(path, old, new, label):
    p = root / path
    s = p.read_text(encoding='utf-8')
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'FAIL {label}: expected exactly 1 source match, got {count}')
    p.write_text(s.replace(old, new, 1), encoding='utf-8')
    print(f'PASS patch {label}')

replace_once('includes/trait-ppar-control-contract.php',
"trait PPAR_Control_Contract_Trait {\n",
"trait PPAR_Control_Contract_Trait {\n    private $control_decision_cache = array();\n\n    private function control_clear_decision_cache($portal_key = '', $scope_type = '', $scope_key = '') {\n        if ($portal_key === '' || $scope_type === '' || $scope_key === '') {\n            $this->control_decision_cache = array();\n            return;\n        }\n        $key = $this->control_decision_key($portal_key, $scope_type, $scope_key);\n        unset($this->control_decision_cache[$key]);\n    }\n\n",
'control cache property/helper')

replace_once('includes/trait-ppar-control-contract.php',
'''        $key = $this->control_decision_key($portal_key, $scope_type, $scope_key);
        $row = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->control_decisions_table()} WHERE decision_key=%s", $key), ARRAY_A);
        if (!is_array($row)) {
            return array('exists'=>false,'status'=>'automatic','reason'=>'','payload'=>array(),'user_id'=>0,'created_at'=>0,'updated_at'=>0);
        }
        $payload = json_decode((string) ($row['payload'] ?? ''), true);
        return array(
            'exists'=>true,
            'id'=>absint($row['id'] ?? 0),
            'status'=>sanitize_key((string) ($row['status'] ?? 'automatic')),
            'reason'=>sanitize_text_field((string) ($row['reason'] ?? '')),
            'payload'=>is_array($payload) ? $payload : array(),
            'user_id'=>absint($row['user_id'] ?? 0),
            'created_at'=>absint($row['created_at'] ?? 0),
            'updated_at'=>absint($row['updated_at'] ?? 0),
        );
''',
'''        $key = $this->control_decision_key($portal_key, $scope_type, $scope_key);
        if (array_key_exists($key, $this->control_decision_cache)) {
            return $this->control_decision_cache[$key];
        }
        $row = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->control_decisions_table()} WHERE decision_key=%s", $key), ARRAY_A);
        if (!is_array($row)) {
            $result = array('exists'=>false,'status'=>'automatic','reason'=>'','payload'=>array(),'user_id'=>0,'created_at'=>0,'updated_at'=>0);
            $this->control_decision_cache[$key] = $result;
            return $result;
        }
        $payload = json_decode((string) ($row['payload'] ?? ''), true);
        $result = array(
            'exists'=>true,
            'id'=>absint($row['id'] ?? 0),
            'status'=>sanitize_key((string) ($row['status'] ?? 'automatic')),
            'reason'=>sanitize_text_field((string) ($row['reason'] ?? '')),
            'payload'=>is_array($payload) ? $payload : array(),
            'user_id'=>absint($row['user_id'] ?? 0),
            'created_at'=>absint($row['created_at'] ?? 0),
            'updated_at'=>absint($row['updated_at'] ?? 0),
        );
        $this->control_decision_cache[$key] = $result;
        return $result;
''', 'control get request cache')

replace_once('includes/trait-ppar-control-contract.php',
'''        if ($id <= 0) {
            return new WP_Error('control_decision_save_failed', 'Chefentscheidung konnte nicht gespeichert werden.');
        }
        $this->control_log_event($event_type, $portal_key, $scope_type, $scope_key, (string) ($existing['status'] ?? 'automatic'), $status, $reason, $payload, $user_id);
''',
'''        if ($id <= 0) {
            return new WP_Error('control_decision_save_failed', 'Chefentscheidung konnte nicht gespeichert werden.');
        }
        $this->control_clear_decision_cache($portal_key, $scope_type, $scope_key);
        $this->control_log_event($event_type, $portal_key, $scope_type, $scope_key, (string) ($existing['status'] ?? 'automatic'), $status, $reason, $payload, $user_id);
''', 'control write invalidation')

replace_once('includes/trait-ppar-ebay-account-deletion.php',
'''        $wpdb->delete($this->control_decisions_table(), array('scope_type' => $scope_type, 'scope_key' => $scope_key));
        $wpdb->delete($this->control_audit_table(), array('scope_type' => $scope_type, 'scope_key' => $scope_key));
''',
'''        $wpdb->delete($this->control_decisions_table(), array('scope_type' => $scope_type, 'scope_key' => $scope_key));
        $wpdb->delete($this->control_audit_table(), array('scope_type' => $scope_type, 'scope_key' => $scope_key));
        if (method_exists($this, 'control_clear_decision_cache')) {
            $this->control_clear_decision_cache();
        }
''', 'direct control delete invalidation')

replace_once('includes/trait-ppar-ebay.php',
"trait PPAR_Ebay_Trait {\n",
"trait PPAR_Ebay_Trait {\n    private $ebay_business_campaign_source_row_cache = array();\n\n    private function ebay_request_local_read_cache_allowed() {\n        if ((function_exists('is_admin') && is_admin())\n            || (defined('DOING_CRON') && DOING_CRON)\n            || (defined('REST_REQUEST') && REST_REQUEST)\n            || (defined('WP_CLI') && WP_CLI)\n            || (function_exists('wp_doing_ajax') && wp_doing_ajax())) {\n            return false;\n        }\n        return true;\n    }\n\n",
'ebay frontend read cache helper')

replace_once('includes/trait-ppar-ebay.php',
'''        global $wpdb;
        $row = $wpdb->get_row($wpdb->prepare(
            "SELECT * FROM {$this->ebay_items_table()} WHERE creative_identity_hash=%s AND seller_account_type='BUSINESS' ORDER BY id DESC LIMIT 1",
            $hash
        ), ARRAY_A);
        return is_array($row) ? $row : array();
''',
'''        $cache_key = 'BUSINESS|' . $hash;
        $use_cache = $this->ebay_request_local_read_cache_allowed();
        if ($use_cache && array_key_exists($cache_key, $this->ebay_business_campaign_source_row_cache)) {
            return $this->ebay_business_campaign_source_row_cache[$cache_key];
        }
        global $wpdb;
        $row = $wpdb->get_row($wpdb->prepare(
            "SELECT * FROM {$this->ebay_items_table()} WHERE creative_identity_hash=%s AND seller_account_type='BUSINESS' ORDER BY id DESC LIMIT 1",
            $hash
        ), ARRAY_A);
        $result = is_array($row) ? $row : array();
        if ($use_cache) {
            $this->ebay_business_campaign_source_row_cache[$cache_key] = $result;
        }
        return $result;
''', 'ebay business hash request cache')

replace_once('includes/trait-ppar-output-objects.php',
"trait PPAR_Output_Objects_Trait {\n",
"trait PPAR_Output_Objects_Trait {\n    private $output_creative_row_cache = array();\n\n    private function output_request_local_read_cache_allowed() {\n        if ((function_exists('is_admin') && is_admin())\n            || (defined('DOING_CRON') && DOING_CRON)\n            || (defined('REST_REQUEST') && REST_REQUEST)\n            || (defined('WP_CLI') && WP_CLI)\n            || (function_exists('wp_doing_ajax') && wp_doing_ajax())) {\n            return false;\n        }\n        return true;\n    }\n\n",
'creative frontend read cache helper')

replace_once('includes/trait-ppar-output-objects.php',
'''    private function output_creative_row($identity_hash) {
        global $wpdb;
        $table = $this->creative_library_table();
        return $wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE identity_hash=%s", sanitize_text_field((string) $identity_hash)), ARRAY_A);
    }
''',
'''    private function output_creative_row($identity_hash) {
        $identity_hash = sanitize_text_field((string) $identity_hash);
        $use_cache = $this->output_request_local_read_cache_allowed();
        if ($use_cache && array_key_exists($identity_hash, $this->output_creative_row_cache)) {
            return $this->output_creative_row_cache[$identity_hash];
        }
        global $wpdb;
        $table = $this->creative_library_table();
        $row = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE identity_hash=%s", $identity_hash), ARRAY_A);
        if ($use_cache) {
            $this->output_creative_row_cache[$identity_hash] = $row;
        }
        return $row;
    }
''', 'creative identity request cache')

print('PERFORMANCE_CACHE_PATCH_PASS')
