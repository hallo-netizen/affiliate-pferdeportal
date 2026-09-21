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
        $idealo = method_exists($this, 'idealo_settings') ? $this->idealo_settings() : get_option(self::OPTION_NETWORK_IDEALO, array());
        $idealo = is_array($idealo) ? $idealo : array();
        $mode = method_exists($this, 'idealo_sanitize_output_mode')
            ? $this->idealo_sanitize_output_mode($idealo['output_mode'] ?? 'ebay_only')
            : sanitize_key((string) ($idealo['output_mode'] ?? 'ebay_only'));
        if (empty($idealo['enabled']) || $mode !== 'automatic') {
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

        $ebay = array();
        $idealo_candidates = array();
        $other = array();
        foreach ($equal as $candidate) {
            $campaign = is_array($candidate['campaign'] ?? null) ? $candidate['campaign'] : array();
            $network = sanitize_key((string) ($campaign['network'] ?? ''));
            if ($network === 'ebay') { $ebay[] = $candidate; }
            elseif ($network === 'idealo') { $idealo_candidates[] = $candidate; }
            else { $other[] = $candidate; }
        }

        if (!$ebay || !$idealo_candidates) {
            return $candidates;
        }

        $mixed = array();
        $mixed[] = array_shift($ebay);
        $mixed[] = array_shift($idealo_candidates);
        if ($ebay) { $mixed[] = array_shift($ebay); }
        elseif ($idealo_candidates) { $mixed[] = array_shift($idealo_candidates); }
        elseif ($other) { $mixed[] = array_shift($other); }

        foreach (array($ebay, $idealo_candidates, $other, $rest) as $bucket) {
            foreach ($bucket as $candidate) { $mixed[] = $candidate; }
        }
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
