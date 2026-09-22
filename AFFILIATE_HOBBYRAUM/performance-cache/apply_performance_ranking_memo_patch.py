#!/usr/bin/env python3
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else 'affiliate-portal-router')
p=root/'pferdeportal-affiliate-router.php'
s=p.read_text(encoding='utf-8')

needle="final class Pferdeportal_Affiliate_Router {\n"
insert="""final class Pferdeportal_Affiliate_Router {
    private $ranked_campaigns_request_cache = array();

    private function ranked_campaigns_request_cache_allowed() {
        if ((function_exists('is_admin') && is_admin())
            || (defined('DOING_CRON') && DOING_CRON)
            || (defined('REST_REQUEST') && REST_REQUEST)
            || (defined('WP_CLI') && WP_CLI)
            || (function_exists('wp_doing_ajax') && wp_doing_ajax())) {
            return false;
        }
        return true;
    }

    private function ranked_campaigns_request_cache_key($context, $slot_type, $forced_campaign_id) {
        return hash('sha256', serialize(array(
            is_array($context) ? $context : array(),
            (string) $slot_type,
            (string) $forced_campaign_id,
        )));
    }

"""
if s.count(needle)!=1: raise SystemExit('FAIL class declaration match')
s=s.replace(needle,insert,1)

sig="    private function ranked_campaigns_for_slot($context, $slot_type, $forced_campaign_id = '') {\n"
if s.count(sig)!=1: raise SystemExit('FAIL ranking function signature match')
wrapper="""    private function ranked_campaigns_for_slot($context, $slot_type, $forced_campaign_id = '') {
        if (!$this->ranked_campaigns_request_cache_allowed()) {
            return $this->ranked_campaigns_for_slot_uncached($context, $slot_type, $forced_campaign_id);
        }
        $cache_key = $this->ranked_campaigns_request_cache_key($context, $slot_type, $forced_campaign_id);
        if (array_key_exists($cache_key, $this->ranked_campaigns_request_cache)) {
            return $this->ranked_campaigns_request_cache[$cache_key];
        }
        $result = $this->ranked_campaigns_for_slot_uncached($context, $slot_type, $forced_campaign_id);
        $this->ranked_campaigns_request_cache[$cache_key] = $result;
        return $result;
    }

    private function ranked_campaigns_for_slot_uncached($context, $slot_type, $forced_campaign_id = '') {
"""
s=s.replace(sig,wrapper,1)
p.write_text(s,encoding='utf-8')
print('PERFORMANCE_RANKING_MEMO_PATCH_PASS')
