from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: build_test_only_leaf_candidate_v672185.py <plugin-root>")

root = Path(sys.argv[1])
p = root / "includes" / "trait-ppar-output-objects.php"
s = p.read_text(encoding="utf-8")

old = """        $dest_tokens=$this->output_tokens($semantic);
        $ranked=array();"""
new = """        $dest_tokens=$this->output_tokens($semantic);
        // TEST-ONLY candidate: exact final URL leaf outranks the same token
        // occurring only inside a containing path segment.
        $destination_path=(string)wp_parse_url((string)($row['destination_url']??''),PHP_URL_PATH);
        $destination_leaf=rawurldecode((string)basename(rtrim($destination_path,'/')));
        $destination_leaf=preg_replace('/\\.[A-Za-z0-9]{1,8}$/','',$destination_leaf);
        $destination_leaf_norm=$this->output_text(str_replace(array('-','_'),' ',$destination_leaf));
        $ranked=array();"""
if old not in s:
    raise SystemExit("FAIL candidate insert anchor missing")
s = s.replace(old, new, 1)

old2 = """            $exact=$slug_tokens && !array_diff($slug_tokens,array_keys($matched));
            $score=$exact ? 1000 + min(90,absint($target['depth']??0)*10) : count($matched)*140;"""
new2 = """            $exact=$slug_tokens && !array_diff($slug_tokens,array_keys($matched));
            $final_leaf_exact=$exact && $destination_leaf_norm!=='' && (
                $destination_leaf_norm===$slug_norm || $destination_leaf_norm===$leaf_norm
            );
            $score=$exact ? 1000 + min(90,absint($target['depth']??0)*10) + ($final_leaf_exact?200:0) : count($matched)*140;"""
if old2 not in s:
    raise SystemExit("FAIL candidate score anchor missing")
s = s.replace(old2, new2, 1)

p.write_text(s, encoding="utf-8")
print("PASS test-only generic final-leaf candidate built")
