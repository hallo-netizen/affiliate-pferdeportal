#!/usr/bin/env python3
"""Hab RC29: improve proven product NAME recognition while preserving all
existing placements/target paths, GTIN, images and insurance exclusions.
No new architecture. Base strictly the last completely tested RC28 release.
"""
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from hashlib import sha256
ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=ROOT/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
old=P.read_bytes()
assert sha256(old).hexdigest()=="e474e25ec0f63440dfb5d69c993d0b0884431ee10cd009b589b3b6b50cc66f32", "Unexpected RC28 source; stop"
base="affiliate-portal-router/"
trait=base+"includes/trait-ppar-idealo.php"
main=base+"affiliate-portal-router.php"
readme=base+"readme.txt"
def once(s,a,b):
    n=s.count(a)
    assert n==1,("Unexpected anchor",n,a[:210])
    return s.replace(a,b,1)
with ZipFile(BytesIO(old)) as z:
    assert z.testzip() is None and len(z.namelist())==36
    files={i.filename:z.read(i.filename) for i in z.infolist()}
    t=files[trait].decode("utf-8")
    # Keep existing product catalogue intact. Only give the title matcher a
    # bounded vocabulary of *verified product synonyms* already present on
    # public idealo.de product-category pages, and naturally occurring German
    # compound product nouns (e.g. Moebeltresor -> Tresor).
    t=once(t,
        """        return $cache = array('concepts'=>$concepts,'index'=>$index,'catalog'=>$catalog);""",
        """        // Actual idealo.de catalogue terminology, not new product groups.
        // Aliases matter only for a SINGLE-TOKEN existing portal concept.
        // Generic accessories remain excluded by title-primary cutoff.
        $verified_aliases=array(
            'Wassermelder'=>array('Wassersensor','Wasserlecksensor','Wasserwarnmelder'),
            'Feuerlöscher'=>array('Pulverlöscher','Schaumlöscher','Fettbrandlöscher'),
        );
        $alias_owners=array();
        foreach ($verified_aliases as $original=>$names) {
            $family_stem=$this->idealo_match_stem($this->idealo_match_normalize($original));
            if (empty($index[$family_stem])) { continue; }
            foreach ($names as $name) {
                $alias_stem=$this->idealo_match_stem($this->idealo_match_normalize($name));
                if ($alias_stem!=='' && $alias_stem!==$family_stem) {
                    $alias_owners[$alias_stem][$family_stem]=true;
                }
            }
        }
        // General compound suffix detection is bounded to existing product
        // concepts. Do not create new categories or search families.
        $lengths=array(); foreach (array_keys($index) as $stem) {
            $len=strlen((string)$stem);
            if ($len>=6) $lengths[$len]=true;
        }
        $suffix_lengths=array_keys($lengths);
        rsort($suffix_lengths,SORT_NUMERIC);
        return $cache = array('concepts'=>$concepts,'index'=>$index,'catalog'=>$catalog,
            'alias_owners'=>$alias_owners,'suffix_lengths'=>$suffix_lengths);""")

    helper=r'''    /**
     * Keep title matching strict but understand a real product named with a
     * longer German compound noun (Moebeltresor -> Tresor), or a small
     * evidence-based synonymous product type (Wassersensor -> Wassermelder).
     * At least three nonempty prefix characters avoid accidental suffixes.
     * Run only against the existing bounded product-stem index; never create
     * new product targets. This is NOT a fuzzy/free-text match.
     */
    private function idealo_match_expand_title_stems($title_stems,$match_index) {
        $result=is_array($title_stems)?$title_stems:array();
        if (!$result) return $result;
        $index=(array)($match_index['index']??array());
        $aliases=(array)($match_index['alias_owners']??array());
        $lengths=(array)($match_index['suffix_lengths']??array());
        foreach (array_keys($title_stems) as $word) {
            $word=(string)$word;
            foreach ((array)($aliases[$word]??array()) as $family_stem=>$true) {
                if (isset($index[$family_stem])) $result[$family_stem]=true;
            }
            $size=strlen($word);
            foreach ($lengths as $length) {
                $length=(int)$length;
                if ($size < $length+3) continue;
                $suffix=substr($word,-$length);
                if (isset($index[$suffix])) $result[$suffix]=true;
            }
        }
        return $result;
    }

'''
    t=once(t,"    private function idealo_match_context_score(",helper+"    private function idealo_match_context_score(")
    t=once(t,
        "function idealo_match_context_score($concept, $title_n, $main_n, $sub_n, $catalog) {",
        "function idealo_match_context_score($concept, $title_n, $main_n, $sub_n, $catalog, $expanded_title_stems = null) {")
    t=once(t,
        """        $title_stems = array();
        foreach ($this->idealo_match_tokens($title_n) as $token) { $title_stems[$this->idealo_match_stem($token)] = true; }
        $required =""",
        """        $title_stems = is_array($expanded_title_stems) ? $expanded_title_stems : array();
        if (!is_array($expanded_title_stems)) {
            foreach ($this->idealo_match_tokens($title_n) as $token) { $title_stems[$this->idealo_match_stem($token)] = true; }
        }
        $required =""")
    # Proven bug: idealo_match_primary_tokens() used idealo_match_tokens(),
    # which already removed "fuer"/"mit". Accessory titles could be falsely
    # treated as genuine devices. Cut raw words BEFORE stopword filtering.
    t=once(t,
        """        $tokens = $this->idealo_match_tokens($text); $out = array();
        foreach ($tokens as $idx => $token) {
            if (isset($bounds[$token])) { return $idx === 0 ? array() : $out; }
            $out[] = $token;
        }
        return $out;""",
        """        $raw = preg_split('/\\s+/', $this->idealo_match_normalize($text));
        $head = array();
        foreach ((array)$raw as $word) {
            if (isset($bounds[$word])) { break; }
            $head[] = $word;
        }
        return $head ? $this->idealo_match_tokens(implode(' ', $head)) : array();""")
    t=once(t,
        """        $product_stems = array(); foreach ($primary as $token) { $product_stems[$this->idealo_match_stem($token)] = true; }
        $candidate_ids = array();""",
        """        $product_stems = array(); foreach ($primary as $token) { $product_stems[$this->idealo_match_stem($token)] = true; }
        $product_stems=$this->idealo_match_expand_title_stems($product_stems,$mi);
        $candidate_ids = array();""")
    t=once(t,
        "$context=$this->idealo_match_context_score($concept,$title_n,$main_n,$sub_n,$mi['catalog']);",
        "$context=$this->idealo_match_context_score($concept,$title_n,$main_n,$sub_n,$mi['catalog'],$product_stems);")
    files[trait]=t.encode("utf-8")
    m=files[main].decode()
    m=once(m,"Version: 0.1.25-rc28","Version: 0.1.26-rc29")
    files[main]=m.encode()
    rd=files[readme].decode()
    rd=once(rd,"Stable tag: 0.1.25-rc28","Stable tag: 0.1.26-rc29")
    files[readme]=rd.encode()
    changed={trait,main,readme}
    assert all(files[n]==z.read(n) for n in z.namelist() if n not in changed)
    out=BytesIO()
    with ZipFile(out,"w") as dest:
        for item in z.infolist():dest.writestr(item,files[item.filename])
    final=out.getvalue()
with ZipFile(BytesIO(final)) as verify:
    assert verify.testzip() is None and len(verify.namelist())==36
    assert b"Version: 0.1.26-rc29" in verify.read(main)
    assert b"idealo_match_expand_title_stems" in verify.read(trait)
P.write_bytes(final)
print("RC29_KISS_BUILD_PASS",len(final),sha256(final).hexdigest())
