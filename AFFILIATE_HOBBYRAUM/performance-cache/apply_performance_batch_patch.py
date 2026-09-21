#!/usr/bin/env python3
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else 'affiliate-portal-router')

def rep(path,old,new,label):
    p=root/path
    s=p.read_text(encoding='utf-8')
    if s.count(old)!=1:
        raise SystemExit(f'FAIL {label}: source match count={s.count(old)}')
    p.write_text(s.replace(old,new,1),encoding='utf-8')
    print('PASS patch',label)

rep(Path('includes/trait-ppar-control-contract.php'),
"trait PPAR_Control_Contract_Trait {\n    private $control_decision_cache = array();\n",
"trait PPAR_Control_Contract_Trait {\n    private $control_decision_cache = array();\n    private $control_decision_portal_cache_loaded = array();\n\n    private function control_request_local_read_cache_allowed() {\n        if ((function_exists('is_admin') && is_admin())\n            || (defined('DOING_CRON') && DOING_CRON)\n            || (defined('REST_REQUEST') && REST_REQUEST)\n            || (defined('WP_CLI') && WP_CLI)\n            || (function_exists('wp_doing_ajax') && wp_doing_ajax())) { return false; }\n        return true;\n    }\n\n    private function control_default_decision() {\n        return array('exists'=>false,'status'=>'automatic','reason'=>'','payload'=>array(),'user_id'=>0,'created_at'=>0,'updated_at'=>0);\n    }\n\n    private function control_normalize_decision_row($row) {\n        if (!is_array($row)) { return $this->control_default_decision(); }\n        $payload=json_decode((string)($row['payload']??''),true);\n        return array('exists'=>true,'id'=>absint($row['id']??0),'status'=>sanitize_key((string)($row['status']??'automatic')),'reason'=>sanitize_text_field((string)($row['reason']??'')),'payload'=>is_array($payload)?$payload:array(),'user_id'=>absint($row['user_id']??0),'created_at'=>absint($row['created_at']??0),'updated_at'=>absint($row['updated_at']??0));\n    }\n\n    private function control_prime_portal_decision_cache($portal_key) {\n        $portal_key=sanitize_key((string)$portal_key);\n        if($portal_key===''||!$this->control_request_local_read_cache_allowed()) return false;\n        if(!empty($this->control_decision_portal_cache_loaded[$portal_key])) return true;\n        global $wpdb;\n        $rows=$wpdb->get_results($wpdb->prepare(\"SELECT * FROM {$this->control_decisions_table()} WHERE portal_key=%s\",$portal_key),ARRAY_A);\n        if(!is_array($rows)) return false;\n        foreach($rows as $row){ if(!is_array($row)) continue; $key=strtolower(sanitize_text_field((string)($row['decision_key']??''))); if(preg_match('/^[a-f0-9]{64}$/',$key)) $this->control_decision_cache[$key]=$this->control_normalize_decision_row($row); }\n        $this->control_decision_portal_cache_loaded[$portal_key]=1;\n        return true;\n    }\n",
'control portal batch helpers')

rep(Path('includes/trait-ppar-control-contract.php'),
"""    private function control_clear_decision_cache($portal_key = '', $scope_type = '', $scope_key = '') {
        if ($portal_key === '' || $scope_type === '' || $scope_key === '') {
            $this->control_decision_cache = array();
            return;
        }
        $key = $this->control_decision_key($portal_key, $scope_type, $scope_key);
        unset($this->control_decision_cache[$key]);
    }
""",
"""    private function control_clear_decision_cache($portal_key = '', $scope_type = '', $scope_key = '') {
        if ($portal_key === '' || $scope_type === '' || $scope_key === '') {
            $this->control_decision_cache = array();
            $this->control_decision_portal_cache_loaded = array();
            return;
        }
        $portal_key = sanitize_key((string) $portal_key);
        $key = $this->control_decision_key($portal_key, $scope_type, $scope_key);
        unset($this->control_decision_cache[$key], $this->control_decision_portal_cache_loaded[$portal_key]);
    }
""",'control portal batch invalidation')

rep(Path('includes/trait-ppar-control-contract.php'),
"""        if (!in_array($scope_type, $this->control_allowed_scope_types(), true) || $scope_key === '') {
            return array('exists'=>false,'status'=>'automatic','reason'=>'','payload'=>array(),'user_id'=>0,'created_at'=>0,'updated_at'=>0);
        }
        $key = $this->control_decision_key($portal_key, $scope_type, $scope_key);
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
""",
"""        if (!in_array($scope_type, $this->control_allowed_scope_types(), true) || $scope_key === '') {
            return $this->control_default_decision();
        }
        $key = $this->control_decision_key($portal_key, $scope_type, $scope_key);
        if (array_key_exists($key, $this->control_decision_cache)) {
            return $this->control_decision_cache[$key];
        }
        if ($this->control_prime_portal_decision_cache($portal_key)) {
            if (array_key_exists($key, $this->control_decision_cache)) {
                return $this->control_decision_cache[$key];
            }
            $result = $this->control_default_decision();
            $this->control_decision_cache[$key] = $result;
            return $result;
        }
        $row = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->control_decisions_table()} WHERE decision_key=%s", $key), ARRAY_A);
        $result = is_array($row) ? $this->control_normalize_decision_row($row) : $this->control_default_decision();
        $this->control_decision_cache[$key] = $result;
        return $result;
""",'control portal batch read')

rep(Path('includes/trait-ppar-ebay.php'),
"trait PPAR_Ebay_Trait {\n    private $ebay_business_campaign_source_row_cache = array();\n",
"trait PPAR_Ebay_Trait {\n    private $ebay_business_campaign_source_row_cache = array();\n    private $ebay_business_campaign_source_row_cache_primed = false;\n",
'ebay batch flag')

marker="""    private function ebay_request_local_read_cache_allowed() {
        if ((function_exists('is_admin') && is_admin())
            || (defined('DOING_CRON') && DOING_CRON)
            || (defined('REST_REQUEST') && REST_REQUEST)
            || (defined('WP_CLI') && WP_CLI)
            || (function_exists('wp_doing_ajax') && wp_doing_ajax())) {
            return false;
        }
        return true;
    }

"""
helper=marker+"""    private function ebay_prime_business_campaign_source_row_cache() {
        if ($this->ebay_business_campaign_source_row_cache_primed || !$this->ebay_request_local_read_cache_allowed() || !method_exists($this, 'get_campaigns')) { return; }
        $hashes=array();
        foreach((array)$this->get_campaigns() as $campaign){
            if(!is_array($campaign)||sanitize_key((string)($campaign['network']??''))!=='ebay') continue;
            $post_id=absint($campaign['post_id']??0);
            if($post_id<=0||absint(get_post_meta($post_id,'_ppar_ebay_business_auto',true))!==1) continue;
            $hash=strtolower(sanitize_text_field((string)get_post_meta($post_id,'_ppar_creative_identity_hash',true)));
            if(preg_match('/^[a-f0-9]{64}$/',$hash)) $hashes[$hash]=true;
        }
        $hashes=array_keys($hashes);
        if(!$hashes){$this->ebay_business_campaign_source_row_cache_primed=true;return;}
        global $wpdb; $table=$this->ebay_items_table(); $all_ok=true;
        foreach(array_chunk($hashes,1000) as $chunk){
            $ph=implode(',',array_fill(0,count($chunk),'%s'));
            $sql=$wpdb->prepare("SELECT * FROM {$table} WHERE seller_account_type='BUSINESS' AND creative_identity_hash IN ({$ph}) ORDER BY id DESC",$chunk);
            $rows=$wpdb->get_results($sql,ARRAY_A);
            if(!is_array($rows)){$all_ok=false;continue;}
            foreach($chunk as $hash){$this->ebay_business_campaign_source_row_cache['BUSINESS|'.$hash]=array();}
            foreach($rows as $row){if(!is_array($row))continue;$hash=strtolower(sanitize_text_field((string)($row['creative_identity_hash']??'')));$key='BUSINESS|'.$hash;if(preg_match('/^[a-f0-9]{64}$/',$hash)&&array_key_exists($key,$this->ebay_business_campaign_source_row_cache)&&!$this->ebay_business_campaign_source_row_cache[$key])$this->ebay_business_campaign_source_row_cache[$key]=$row;}
        }
        if($all_ok)$this->ebay_business_campaign_source_row_cache_primed=true;
    }

"""
rep(Path('includes/trait-ppar-ebay.php'),marker,helper,'ebay batch helper')

rep(Path('includes/trait-ppar-ebay.php'),
"""        $cache_key = 'BUSINESS|' . $hash;
        $use_cache = $this->ebay_request_local_read_cache_allowed();
        if ($use_cache && array_key_exists($cache_key, $this->ebay_business_campaign_source_row_cache)) {
            return $this->ebay_business_campaign_source_row_cache[$cache_key];
        }
""",
"""        $cache_key = 'BUSINESS|' . $hash;
        $use_cache = $this->ebay_request_local_read_cache_allowed();
        if ($use_cache) {
            $this->ebay_prime_business_campaign_source_row_cache();
            if (array_key_exists($cache_key, $this->ebay_business_campaign_source_row_cache)) {
                return $this->ebay_business_campaign_source_row_cache[$cache_key];
            }
        }
""",'ebay batch read')

rep(Path('includes/trait-ppar-output-objects.php'),
"trait PPAR_Output_Objects_Trait {\n    private $output_creative_row_cache = array();\n",
"trait PPAR_Output_Objects_Trait {\n    private $output_creative_row_cache = array();\n    private $output_creative_row_cache_primed = false;\n",
'creative batch flag')

marker="""    private function output_request_local_read_cache_allowed() {
        if ((function_exists('is_admin') && is_admin())
            || (defined('DOING_CRON') && DOING_CRON)
            || (defined('REST_REQUEST') && REST_REQUEST)
            || (defined('WP_CLI') && WP_CLI)
            || (function_exists('wp_doing_ajax') && wp_doing_ajax())) {
            return false;
        }
        return true;
    }

"""
helper=marker+"""    private function output_prime_creative_row_cache() {
        if($this->output_creative_row_cache_primed||!$this->output_request_local_read_cache_allowed()||!method_exists($this,'get_campaigns')) return;
        $hashes=array();
        foreach((array)$this->get_campaigns() as $campaign){if(!is_array($campaign))continue;$post_id=absint($campaign['post_id']??0);if($post_id<=0)continue;$hash=strtolower(sanitize_text_field((string)get_post_meta($post_id,'_ppar_creative_identity_hash',true)));if(preg_match('/^[a-f0-9]{64}$/',$hash))$hashes[$hash]=true;}
        $hashes=array_keys($hashes);
        if(!$hashes){$this->output_creative_row_cache_primed=true;return;}
        global $wpdb;$table=$this->creative_library_table();$all_ok=true;
        foreach(array_chunk($hashes,1000) as $chunk){$ph=implode(',',array_fill(0,count($chunk),'%s'));$sql=$wpdb->prepare("SELECT * FROM {$table} WHERE identity_hash IN ({$ph}) ORDER BY id DESC",$chunk);$rows=$wpdb->get_results($sql,ARRAY_A);if(!is_array($rows)){$all_ok=false;continue;}foreach($chunk as $hash)$this->output_creative_row_cache[$hash]=null;foreach($rows as $row){if(!is_array($row))continue;$hash=strtolower(sanitize_text_field((string)($row['identity_hash']??'')));if(preg_match('/^[a-f0-9]{64}$/',$hash)&&array_key_exists($hash,$this->output_creative_row_cache)&&$this->output_creative_row_cache[$hash]===null)$this->output_creative_row_cache[$hash]=$row;}}
        if($all_ok)$this->output_creative_row_cache_primed=true;
    }

"""
rep(Path('includes/trait-ppar-output-objects.php'),marker,helper,'creative batch helper')

rep(Path('includes/trait-ppar-output-objects.php'),
"""        $identity_hash = sanitize_text_field((string) $identity_hash);
        $use_cache = $this->output_request_local_read_cache_allowed();
        if ($use_cache && array_key_exists($identity_hash, $this->output_creative_row_cache)) {
            return $this->output_creative_row_cache[$identity_hash];
        }
""",
"""        $identity_hash = strtolower(sanitize_text_field((string) $identity_hash));
        $use_cache = $this->output_request_local_read_cache_allowed();
        if ($use_cache) {
            $this->output_prime_creative_row_cache();
            if (array_key_exists($identity_hash, $this->output_creative_row_cache)) {
                return $this->output_creative_row_cache[$identity_hash];
            }
        }
""",'creative batch read')
print('PERFORMANCE_BATCH_PATCH_PASS')
