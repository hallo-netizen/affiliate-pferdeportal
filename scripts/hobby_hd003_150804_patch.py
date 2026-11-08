#!/usr/bin/env python3
"""Strict HD003 1.50.803 -> 1.50.804: read native WP category master on owned term tiles and hero.
Never alters WordPress data, existing media, HD007 or any non-design asset.
"""
import pathlib,zipfile,hashlib,sys
SOURCE_SHA="06e412f04fd3768477c6e825b39708baed0927be68260fce55fd316dff14d95f"
MAIN="affiliate-portal-template-kit/pferde-template-kit.php"
DESIGN="affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php"

def repl(s,old,new,description):
    n=s.count(old)
    if n!=1: raise RuntimeError(description+": expected 1 unique match but found "+str(n))
    return s.replace(old,new,1)

HELPERS=r'''
    /** Strictly one native thumbnail_id for both the current category's hero and its parent tile. */
    private static function term_master_data_v150804($term) {
        if (!$term instanceof WP_Term || (string)$term->taxonomy !== 'category' || (int)$term->term_id <= 0) { return []; }
        $id = (int)get_term_meta((int)$term->term_id, 'thumbnail_id', true);
        if ($id <= 0 || !wp_attachment_is_image($id)) { return []; }
        $full = wp_get_attachment_image_src($id, 'full');
        if (!is_array($full) || empty($full[0]) || (int)($full[1] ?? 0) <= 0 || (int)($full[2] ?? 0) <= 0) { return []; }
        return ['id'=>$id,'url'=>(string)$full[0],'width'=>(int)$full[1],'height'=>(int)$full[2]];
    }
    private static function term_master_tile_v150804($term) {
        $data = self::term_master_data_v150804($term);
        if (!$data) { return ''; }
        $img = wp_get_attachment_image((int)$data['id'], 'medium', false, [
            'alt'=>'', 'aria-hidden'=>'true', 'loading'=>'lazy', 'decoding'=>'async',
            'style'=>'display:block!important;width:100%!important;height:100%!important;object-fit:cover!important;object-position:center!important',
        ]);
        if (!is_string($img) || trim($img) === '') { return ''; }
        return '<span class="hd-next-icon hd-next-term-photo-v150804" data-hd-term-master="'.(int)$data['id'].'" style="overflow:hidden!important;border-radius:6px!important;background:#f5f1e9!important;display:flex!important;align-items:stretch!important">'.$img.'</span>';
    }
    private static function term_master_hero_v150804($term) {
        $data = self::term_master_data_v150804($term);
        if (!$data) { return ''; }
        $image = wp_get_attachment_image((int)$data['id'], 'full', false, [
            'alt'=>(string)$term->name, 'loading'=>'eager', 'decoding'=>'async', 'fetchpriority'=>'high',
            'style'=>'display:block!important;width:100%!important;height:100%!important;object-fit:cover!important;object-position:center!important'
        ]);
        if (!is_string($image) || trim($image) === '') { return ''; }
        return '<figure class="hd-category-term-master-hero-v150804" data-hd-term-master="'.(int)$data['id'].'" style="box-sizing:border-box!important;width:min(calc(100% - 24px),1200px)!important;margin:16px auto!important;height:clamp(180px,25vw,300px)!important;overflow:hidden!important;border-radius:6px!important;background:#f5f1e9!important">'.$image.'</figure>';
    }

'''
def main(args):
    if len(args)!=3: raise SystemExit("usage: patch_hd003_150804.py ORIGINAL_803.zip NEW_804.zip")
    src,dst=map(pathlib.Path,args[1:])
    raw=src.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA: raise RuntimeError("The input is NOT verified HD003 1.50.803; abort")
    with zipfile.ZipFile(src) as zin:
        if zin.testzip() is not None: raise RuntimeError("Bad source ZIP")
        orig_names=zin.namelist()
        if len(orig_names)!=1290 or orig_names.count(MAIN)!=1 or orig_names.count(DESIGN)!=1: raise RuntimeError("Unexpected source structure")
        main=zin.read(MAIN).decode('utf8')
        design=zin.read(DESIGN).decode('utf8')
        main=repl(main," * Version: 1.50.803"," * Version: 1.50.804","main header")
        main=repl(main,"const VERSION = '1.50.803'","const VERSION = '1.50.804'","main constant")
        design=repl(design,"const RELEASE = '1.50.798'","const RELEASE = '1.50.804'","design release for cache bust")

        # Preserve all existing post images, category images, photo-fallback rules and layout.
        anchor="    private static function render_category_level_term_cards_v150687($terms, $page=null, $world_slug='', $extra_class='') {"
        design=repl(design,anchor,HELPERS+anchor,"category helper insertion")

        # Third-level WP category tiles on WordPress parent pages (e.g. Sportdrachen).
        design=repl(design,
            "            $label = self::leaf_category_display_title_v150688($term);",
            "            $label = self::leaf_category_display_title_v150688($term);\n"
            "            $photo = self::term_master_tile_v150804($term);\n"
            "            $icon = $photo !== '' ? $photo : '<span class=\"hd-next-icon\">'.self::leaf_category_icon_svg_v150687($term,$page,$world_slug).'</span>';",
            "category page tile setup")
        design=repl(design,
            "<span class=\"hd-next-icon\">'.self::leaf_category_icon_svg_v150687($term,$page,$world_slug).'</span><span class=\"hd-next-copy\">",
            "'.$icon.'<span class=\"hd-next-copy\">",
            "category page tile output")

        # WordPress terms on other parent pages (do not modify photo page tiles).
        design=repl(design,
            "                $short=$desc!==''?wp_trim_words($desc,9,'…'):'';",
            "                $short=$desc!==''?wp_trim_words($desc,9,'…'):'';\n"
            "                $photo=self::term_master_tile_v150804($term);\n"
            "                $icon=$photo!==''?$photo:'<span class=\"hd-next-icon\">'.self::topic_icon_svg($term->name,$world_slug).'</span>';",
            "nested category setup")
        design=repl(design,
            "<span class=\"hd-next-icon\">'.self::topic_icon_svg($term->name,$world_slug).'</span><span class=\"hd-next-copy\">",
            "'.$icon.'<span class=\"hd-next-copy\">",
            "nested category display")

        # Native term archives showing their own child terms.
        design=repl(design,
            "            $items[]='<a class=\"hd-next-card hd-row-size-'.max(1,min(3,$rs))",
            "            $photo=self::term_master_tile_v150804($child);\n"
            "            $icon=$photo!==''?$photo:'<span class=\"hd-next-icon\">'.self::leaf_category_icon_svg_v150687($child).'</span>';\n"
            "            $items[]='<a class=\"hd-next-card hd-row-size-'.max(1,min(3,$rs))",
            "term nested tile setup")
        design=repl(design,
            "<span class=\"hd-next-icon\">'.self::leaf_category_icon_svg_v150687($child).'</span><span class=\"hd-next-copy\">",
            "'.$icon.'<span class=\"hd-next-copy\">",
            "term nested tile output")

        # Custom portal's actual term archive routes. Separate stock WP leaf-template
        # already renders exactly the same thumbnail_id and remains unchanged.
        design=repl(design,
            "                    $out.=self::render_leaf_category_intro_v150750($term);",
            "                    $out.=self::term_master_hero_v150804($term);\n"
            "                    $out.=self::render_leaf_category_intro_v150750($term);",
            "known leaf archive hero")
        design=repl(design,
            "                    $out.=self::render_direct_category_level_term_intro_v150687($term);",
            "                    $out.=self::term_master_hero_v150804($term);\n"
            "                    $out.=self::render_direct_category_level_term_intro_v150687($term);",
            "direct term archive hero")
        design=repl(design,
            "                $full=self::category_intro_for_term($term); $out.=self::render_page_intro_block(",
            "                if ((string)$term->taxonomy === 'category') { $out.=self::term_master_hero_v150804($term); }\n"
            "                $full=self::category_intro_for_term($term); $out.=self::render_page_intro_block(",
            "other category archive hero")

        dst.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(dst,"w") as zout:
            for info in zin.infolist():
                if info.filename==MAIN: b=main.encode('utf8')
                elif info.filename==DESIGN: b=design.encode('utf8')
                else: b=zin.read(info)
                zout.writestr(info,b)
    with zipfile.ZipFile(src) as zin,zipfile.ZipFile(dst) as zout:
        assert zin.namelist()==zout.namelist()
        assert len(zout.namelist())==1290 and zout.testzip() is None
        changed=[p for p in zin.namelist() if zin.read(p)!=zout.read(p)]
        if set(changed)!={MAIN,DESIGN}:raise RuntimeError("Unexpected file delta "+str(changed))
    print("PASS 1.50.803 exact SHA; ZIP 1290; ONLY 2 PHP changed; 1288 files byte-identical; no data/images rewritten; OUTPUT_SHA256",hashlib.sha256(dst.read_bytes()).hexdigest())

if __name__=="__main__": main(sys.argv)
