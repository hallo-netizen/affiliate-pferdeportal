#!/usr/bin/env python3
"""Minimal, fail-closed HD003 1.50.798 -> 1.50.799 category-photo repair.
Only two design PHP files change. WordPress database, old images and all other code untouched.
"""
import sys,hashlib,pathlib,zipfile
SHA="05ea37f040c1189ea9fda29c2dd795740351d83fe8022f8d966a453679fec7a8"
MAIN="affiliate-portal-template-kit/pferde-template-kit.php"
DESIGN="affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php"
def replace(s,old,new,label):
    n=s.count(old)
    if n!=1: raise RuntimeError(label+" expected once, found "+str(n))
    return s.replace(old,new,1)
HELPERS=r'''
    /** One native WP term master is shared by the real page's category hero and parent tile. */
    private static function term_master_image_v150799($term) {
        if (!$term instanceof WP_Term || (string)$term->taxonomy !== 'category') { return []; }
        $id = (int)get_term_meta((int)$term->term_id, 'thumbnail_id', true);
        if ($id <= 0 || !wp_attachment_is_image($id)) { return []; }
        $src = wp_get_attachment_image_src($id, 'full');
        if (!is_array($src) || empty($src[0]) || (int)($src[1] ?? 0) <= 0 || (int)($src[2] ?? 0) <= 0) { return []; }
        return ['id'=>$id, 'url'=>(string)$src[0], 'width'=>(int)$src[1], 'height'=>(int)$src[2]];
    }
    private static function term_master_hero_v150799($term) {
        $photo = self::term_master_image_v150799($term);
        if (!$photo) { return ''; }
        return '<figure class="hd-catlevel-master-hero-v150799" data-hd-term-master="'.(int)$photo['id'].'" style="width:calc(100% - 24px);max-width:1200px;margin:16px auto 20px;overflow:hidden;border-radius:6px">'
            .'<img src="'.esc_url($photo['url']).'" alt="'.esc_attr((string)$term->name).'" width="'.(int)$photo['width'].'" height="'.(int)$photo['height'].'" style="display:block;width:100%;height:auto;aspect-ratio:3/1;object-fit:cover" loading="eager" fetchpriority="high">'
            .'</figure>';
    }
    private static function term_master_tile_v150799($term) {
        $photo = self::term_master_image_v150799($term);
        if (!$photo) { return ''; }
        $img = wp_get_attachment_image((int)$photo['id'], 'medium', false, [
            'alt'=>'', 'aria-hidden'=>'true', 'loading'=>'lazy', 'decoding'=>'async',
            'style'=>'display:block;width:100%;height:100%;object-fit:cover;border-radius:5px',
        ]);
        if (!is_string($img) || trim($img) === '') { return ''; }
        return '<span class="hd-next-icon hd-next-photo-v150799" data-hd-term-master="'.(int)$photo['id'].'" style="width:96px!important;height:70px!important;border-radius:5px!important;overflow:hidden!important;background:#edf7f6">'.$img.'</span>';
    }

'''
def main(argv):
    if len(argv)!=3: raise SystemExit("usage: patch.py SOURCE.zip TARGET.zip")
    source,target=map(pathlib.Path,argv[1:])
    if hashlib.sha256(source.read_bytes()).hexdigest()!=SHA: raise RuntimeError("Not verified current 1.50.798 ZIP")
    with zipfile.ZipFile(source) as zin:
        if zin.testzip() is not None or len(zin.namelist())!=1290: raise RuntimeError("Bad source ZIP")
        assert zin.namelist().count(MAIN)==1 and zin.namelist().count(DESIGN)==1
        main=zin.read(MAIN).decode()
        design=zin.read(DESIGN).decode()
        main=replace(main," * Version: 1.50.798"," * Version: 1.50.799","header")
        main=replace(main,"const VERSION = '1.50.798'","const VERSION = '1.50.799'","main version")
        design=replace(design,"const RELEASE = '1.50.798'","const RELEASE = '1.50.799'","design version")
        anchor="    private static function render_category_level_term_cards_v150687($terms, $page=null, $world_slug='', $extra_class='') {"
        design=replace(design,anchor,HELPERS+anchor,"helpers")
        old='''            $items[] = '<a class="hd-next-card hd-catlevel-card" href="'.esc_url($url).'"><span class="hd-next-icon">'.self::leaf_category_icon_svg_v150687($term,$page,$world_slug).'</span><span class="hd-next-copy"><strong>'.esc_html($label).'</strong>'.($line!==''?'<small>'.esc_html($line).'</small>':'').'</span><b aria-hidden="true">→</b></a>';'''
        new='''            $master_tile=self::term_master_tile_v150799($term);
            $icon=$master_tile!=='' ? $master_tile : '<span class="hd-next-icon">'.self::leaf_category_icon_svg_v150687($term,$page,$world_slug).'</span>';
            $card_class='hd-next-card hd-catlevel-card'.($master_tile!==''?' has-photo':'');
            $card_style=$master_tile!==''?' style="grid-template-columns:96px minmax(0,1fr) 16px!important"':'';
            $items[] = '<a class="'.$card_class.'"'.$card_style.' href="'.esc_url($url).'">'.$icon.'<span class="hd-next-copy"><strong>'.esc_html($label).'</strong>'.($line!==''?'<small>'.esc_html($line).'</small>':'').'</span><b aria-hidden="true">→</b></a>';'''
        design=replace(design,old,new,"real category tile")
        anchor='''        } elseif ((function_exists('is_category') && is_category()) || (function_exists('is_tax') && is_tax('journal_cat'))) {
            $term=get_queried_object();
            if($term instanceof WP_Term){'''
        design=replace(design,anchor,anchor+'''
                // Portal's custom template bypasses Astra's legacy category-image hook.
                if ((string)$term->taxonomy === 'category') { $out.=self::term_master_hero_v150799($term); }''',"actual custom category page")
        target.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(target,"w") as zout:
            for item in zin.infolist():
                newbytes=main.encode() if item.filename==MAIN else design.encode() if item.filename==DESIGN else zin.read(item)
                zout.writestr(item,newbytes)
        assert all(zin.read(n)==v for n,v in [(MAIN,zin.read(MAIN)),(DESIGN,zin.read(DESIGN))]) # unchanged source read
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None and len(z.namelist())==1290
        assert b"term_master_hero_v150799" in z.read(DESIGN)
        assert b"term_master_tile_v150799" in z.read(DESIGN)
    print("PASS strict source SHA, two-file delta, 1290 original files, WordPress data unchanged; output",target)
if __name__=="__main__":main(sys.argv)
