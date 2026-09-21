from pathlib import Path
p=Path("/tmp/candidate133/affiliate-portal-router/pferdeportal-affiliate-router.php")
s=p.read_text()
s=s.replace("Version: 6.72.132","Version: 6.72.133",1)
s=s.replace("const VERSION = '6.72.132';","const VERSION = '6.72.133';",1)
old="""    private function select_campaign_for_slot($context, $slot_type, $forced_campaign_id = '') {
        $candidates = $this->ranked_campaigns_for_slot($context, $slot_type, $forced_campaign_id);
        $candidates = $this->category_product_strict_relevance_tier_v672104($candidates, $slot_type);
        if (empty($candidates)) { return null; }
        $index = $this->category_product_slot_index($slot_type);
        return $index > 0 ? ($candidates[$index - 1] ?? null) : $candidates[0];
    }
"""
new="""    private function category_product_provider_mix_v672133($candidates, $slot_type) {
        $candidates = array_values((array) $candidates);
        if (!$candidates || !preg_match('/^category_product_[123]$/', sanitize_key((string) $slot_type))) {
            return $candidates;
        }

        $best_specificity = (int) ($candidates[0]['specificity'] ?? 0);
        $best_matches = (int) ($candidates[0]['matches'] ?? 0);
        $equal = array();
        $rest = array();
        foreach ($candidates as $candidate) {
            if ((int) ($candidate['specificity'] ?? 0) === $best_specificity
                && (int) ($candidate['matches'] ?? 0) === $best_matches) {
                $equal[] = $candidate;
            } else {
                $rest[] = $candidate;
            }
        }

        $provider_buckets = array();
        $provider_order = array();
        foreach ($equal as $candidate) {
            $campaign = is_array($candidate['campaign'] ?? null) ? $candidate['campaign'] : array();
            $provider = sanitize_key((string) ($campaign['network'] ?? ''));
            if ($provider === '') { $provider = '_unknown'; }
            if (!isset($provider_buckets[$provider])) {
                $provider_buckets[$provider] = array();
                $provider_order[] = $provider;
            }
            $provider_buckets[$provider][] = $candidate;
        }

        if (count($provider_order) < 2) {
            return $candidates;
        }

        $mixed = array();
        while (true) {
            $added = false;
            foreach ($provider_order as $provider) {
                if (!empty($provider_buckets[$provider])) {
                    $mixed[] = array_shift($provider_buckets[$provider]);
                    $added = true;
                }
            }
            if (!$added) { break; }
        }
        foreach ($rest as $candidate) { $mixed[] = $candidate; }
        return array_values($mixed);
    }

    private function select_campaign_for_slot($context, $slot_type, $forced_campaign_id = '') {
        $candidates = $this->ranked_campaigns_for_slot($context, $slot_type, $forced_campaign_id);
        $candidates = $this->category_product_strict_relevance_tier_v672104($candidates, $slot_type);
        if ($forced_campaign_id === '') {
            $candidates = $this->category_product_provider_mix_v672133($candidates, $slot_type);
        }
        if (empty($candidates)) { return null; }
        $index = $this->category_product_slot_index($slot_type);
        return $index > 0 ? ($candidates[$index - 1] ?? null) : $candidates[0];
    }
"""
if old not in s:
    raise SystemExit("select block not found")
s=s.replace(old,new,1)
p.write_text(s)
r=Path("/tmp/candidate133/affiliate-portal-router/readme.txt")
rs=r.read_text().replace("V6.72.132 ","V6.72.133 ",1)
r.write_text(rs)
