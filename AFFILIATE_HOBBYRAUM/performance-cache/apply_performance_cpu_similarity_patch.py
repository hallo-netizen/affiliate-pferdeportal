#!/usr/bin/env python3
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else 'affiliate-portal-router')

def rep(path, old, new, label, count=1):
    p=root/path
    s=p.read_text(encoding='utf-8')
    got=s.count(old)
    if got!=count:
        raise SystemExit(f'FAIL {label}: expected {count} matches, got {got}')
    p.write_text(s.replace(old,new,count),encoding='utf-8')
    print('PASS patch',label)

rep(Path('includes/trait-ppar-ebay.php'),
"trait PPAR_Ebay_Trait {\n",
"""trait PPAR_Ebay_Trait {
    private $ebay_topic_similarity_signature_cache = array();

    /**
     * Exact-safe prefilter for the existing >=92% similar_text duplicate rule.
     * It never replaces the rule: it only proves when 92% is mathematically
     * impossible from string length / character multiplicity. All remaining
     * pairs still use PHP similar_text() with the unchanged 92.0 threshold.
     */
    private function ebay_topic_similarity_signature($value) {
        $value = (string) $value;
        if (isset($this->ebay_topic_similarity_signature_cache[$value])) {
            return $this->ebay_topic_similarity_signature_cache[$value];
        }
        $length = strlen($value);
        $freq = array();
        for ($i = 0; $i < $length; $i++) {
            $char = $value[$i];
            if (!isset($freq[$char])) { $freq[$char] = 0; }
            $freq[$char]++;
        }
        return $this->ebay_topic_similarity_signature_cache[$value] = array('length'=>$length, 'freq'=>$freq);
    }

    private function ebay_topic_titles_duplicate_v672146($title, $known) {
        $title = (string) $title;
        $known = (string) $known;
        if ($title === '' || $known === '') { return false; }
        if ($title === $known) { return true; }
        $a = $this->ebay_topic_similarity_signature($title);
        $b = $this->ebay_topic_similarity_signature($known);
        $la = absint($a['length'] ?? 0);
        $lb = absint($b['length'] ?? 0);
        if ($la <= 0 || $lb <= 0) { return false; }
        $min_len = min($la, $lb);
        if ((200.0 * $min_len / ($la + $lb)) < 92.0) { return false; }
        $fa = is_array($a['freq'] ?? null) ? $a['freq'] : array();
        $fb = is_array($b['freq'] ?? null) ? $b['freq'] : array();
        if (count($fa) > count($fb)) { $tmp=$fa; $fa=$fb; $fb=$tmp; }
        $common = 0;
        foreach ($fa as $char=>$count) {
            if (isset($fb[$char])) { $common += min(absint($count), absint($fb[$char])); }
        }
        if ((200.0 * $common / ($la + $lb)) < 92.0) { return false; }
        similar_text($title, $known, $pct);
        return $pct >= 92.0;
    }

""",
'ebay exact-safe similarity prefilter')

oldloop="""            $duplicate = false;
            foreach ($seen_titles as $known) {
                if ($title === '' || $known === '') { continue; }
                similar_text($title, $known, $pct);
                if ($pct >= 92.0) { $duplicate = true; break; }
            }
"""
newloop="""            $duplicate = false;
            foreach ($seen_titles as $known) {
                if ($this->ebay_topic_titles_duplicate_v672146($title, $known)) { $duplicate = true; break; }
            }
"""
rep(Path('includes/trait-ppar-ebay.php'),oldloop,newloop,'both quadratic similar_text loops',2)
print('PERFORMANCE_CPU_SIMILARITY_PATCH_PASS')
