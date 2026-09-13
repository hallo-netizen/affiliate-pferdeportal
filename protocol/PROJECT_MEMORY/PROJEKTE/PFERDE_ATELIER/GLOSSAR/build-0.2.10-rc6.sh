#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.10-rc5.sh"
rm -rf /tmp/uge0210rc6
cp -a /tmp/uge0210rc5 /tmp/uge0210rc6
P=/tmp/uge0210rc6/universal-glossary-engine
python3 - <<'PY'
from pathlib import Path

# New material bytes => new RC version. RC5 remains immutable.
p=Path('/tmp/uge0210rc6/universal-glossary-engine/universal-glossary-engine.php')
s=p.read_text()
assert s.count('Version: 0.2.10-rc5')==1
assert s.count("define('UGE_VERSION', '0.2.10-rc5');")==1
s=s.replace('Version: 0.2.10-rc5','Version: 0.2.10-rc6')
s=s.replace("define('UGE_VERSION', '0.2.10-rc5');","define('UGE_VERSION', '0.2.10-rc6');")
p.write_text(s)

f=Path('/tmp/uge0210rc6/universal-glossary-engine/includes/class-uge-frontend.php')
s=f.read_text()

# Glossar category/single breadcrumbs must use the locked Pferde Design breadcrumb
# axis instead of a second content-local UGE breadcrumb system.
hook="        add_action('wp_footer', [__CLASS__, 'home_interactions'], 60);\n"
assert s.count(hook)==1
s=s.replace(hook,"        add_action('wp_footer', [__CLASS__, 'render_design_breadcrumb_payload'], 19);\n"+hook)

needle="    public static function render_breadcrumbs(?WP_Term $term=null, ?WP_Post $post=null): string {\n"
assert s.count(needle)==1
methods=r'''    public static function resolve_related_term(string $label): ?WP_Post {
        $label = trim(wp_strip_all_tags($label));
        if ($label === '') { return null; }
        $matches = get_posts([
            'post_type' => UGE_Core::POST_TYPE,
            'post_status' => 'publish',
            'posts_per_page' => 3,
            'orderby' => 'ID',
            'order' => 'ASC',
            'title' => $label,
            'suppress_filters' => false,
        ]);
        $exact = [];
        foreach ($matches as $candidate) {
            if ($candidate instanceof WP_Post && trim(wp_strip_all_tags($candidate->post_title)) === $label) { $exact[] = $candidate; }
        }
        if (count($exact) === 1) { return $exact[0]; }
        if (count($exact) > 1) { return null; }
        $by_slug = get_page_by_path(sanitize_title($label), OBJECT, UGE_Core::POST_TYPE);
        return ($by_slug instanceof WP_Post && $by_slug->post_status === 'publish') ? $by_slug : null;
    }

    public static function render_design_breadcrumb_payload(): void {
        if (is_admin() || is_feed() || self::is_home_page()) { return; }
        $term = is_tax(UGE_Core::TAXONOMY) ? get_queried_object() : null;
        $post = self::requested_term_post();
        if (!$term instanceof WP_Term && !$post instanceof WP_Post) { return; }
        if ($post instanceof WP_Post) {
            $nav = UGE_Core::navigation_group_for_post($post->ID);
            $term = $nav instanceof WP_Term ? $nav : null;
        }
        $parts = [
            ['name'=>'Startseite','url'=>home_url('/')],
            ['name'=>'Glossar','url'=>self::home_url()],
        ];
        if ($term instanceof WP_Term) {
            $url = get_term_link($term, UGE_Core::TAXONOMY);
            $parts[] = ['name'=>$term->name,'url'=>$post instanceof WP_Post && !is_wp_error($url) ? (string)$url : ''];
        }
        if ($post instanceof WP_Post) { $parts[] = ['name'=>$post->post_title,'url'=>'']; }
        $visible=[];
        foreach ($parts as $part) {
            $name=trim((string)$part['name']); $url=trim((string)$part['url']);
            if ($name==='') { continue; }
            $visible[]=$url==='' ? '<span class="pftk-content-breadcrumb-current" aria-current="page">'.esc_html($name).'</span>' : '<a href="'.esc_url($url).'">'.esc_html($name).'</a>';
        }
        if (count($visible)<2) { return; }
        $nav='<nav class="pftk-content-breadcrumb" aria-label="Breadcrumb">'.implode('<span class="pftk-content-breadcrumb-separator" aria-hidden="true">›&nbsp;</span>',$visible).'</nav>';
        echo '<div id="uge-pftk-breadcrumb-payload" hidden><div class="pftk-universal-breadcrumb-wrap pftk-breadcrumb-mounted uge-pftk-breadcrumb-mounted">'.$nav.'</div></div>';
        echo '<style id="uge-pftk-breadcrumb-contract">'
            .'body.uge-glossary-category .site-content,body.uge-glossary-term .site-content{padding-top:var(--pftk-navigation-content-gap,18px)!important}'
            .'body.uge-glossary-category .ast-container,body.uge-glossary-term .ast-container{padding-top:0!important}'
            .'.pftk-universal-breadcrumb-wrap.pftk-breadcrumb-mounted{box-sizing:border-box!important;position:relative!important;width:min(calc(100vw - 32px),var(--pftk-breadcrumb-axis-width,900px))!important;max-width:none!important;margin:0 auto var(--pftk-breadcrumb-title-gap,10px)!important;transform:none!important;padding:0!important;clear:both!important}'
            .'.pftk-universal-breadcrumb-wrap.pftk-breadcrumb-mounted .pftk-content-breadcrumb{display:flex;flex-wrap:wrap;align-items:center;column-gap:7px;row-gap:5px;margin:0!important;font-size:14px;line-height:1.5;color:#72786F}'
            .'.pftk-universal-breadcrumb-wrap .pftk-content-breadcrumb-separator{display:inline-flex;align-items:center;margin-left:2px;margin-right:3px;color:#92988F!important}'
            .'.pftk-universal-breadcrumb-wrap .pftk-content-breadcrumb a,.pftk-universal-breadcrumb-wrap .pftk-content-breadcrumb a:visited{color:#72786F!important;font-weight:400!important;text-decoration:none!important}'
            .'.pftk-universal-breadcrumb-wrap .pftk-content-breadcrumb-current{color:#4F5650!important;font-weight:500!important;text-decoration:none!important}'
            .'body.uge-glossary-category .site-content>.pftk-breadcrumb-mounted+.ast-container,body.uge-glossary-term .site-content>.pftk-breadcrumb-mounted+.ast-container{margin-top:0!important;padding-top:0!important}'
            .'@media(max-width:921px){body.uge-glossary-category .site-content,body.uge-glossary-term .site-content{--pftk-navigation-content-gap:14px}}'
            .'@media(max-width:544px){body.uge-glossary-category .site-content,body.uge-glossary-term .site-content{--pftk-navigation-content-gap:10px}}'
            .'</style>';
        echo '<script>(function(){function mount(){var p=document.getElementById("uge-pftk-breadcrumb-payload");var s=document.querySelector(".site-content");if(!p||!s)return;if(s.querySelector(":scope > .pftk-breadcrumb-mounted")){p.remove();return;}var w=p.firstElementChild;if(!w)return;s.insertBefore(w,s.firstChild);p.remove();}if(document.readyState==="loading"){document.addEventListener("DOMContentLoaded",mount,{once:true});}else{mount();}})();</script>';
    }

'''
s=s.replace(needle,methods+needle)

old="        echo self::render_breadcrumbs($term, null);\n"
assert s.count(old)==1
s=s.replace(old,'')
f.write_text(s)

t=Path('/tmp/uge0210rc6/universal-glossary-engine/templates/single-uge-term.php')
s=t.read_text()
old='<div class="uge"><?php $bc_group = $nav_group instanceof WP_Term ? $nav_group : null; echo UGE_Frontend::render_breadcrumbs($bc_group, get_post()); echo UGE_Frontend::render_navigation(false); ?></div>'
new='<div class="uge"><?php echo UGE_Frontend::render_navigation(false); ?></div>'
assert s.count(old)==1
s=s.replace(old,new)
old='$target = get_page_by_path(sanitize_title($related_label), OBJECT, UGE_Core::POST_TYPE);'
assert s.count(old)==1
s=s.replace(old,'$target = UGE_Frontend::resolve_related_term($related_label);')
t.write_text(s)
PY

grep -q 'Version: 0.2.10-rc6' "$P/universal-glossary-engine.php"
grep -q 'render_design_breadcrumb_payload' "$P/includes/class-uge-frontend.php"
grep -q 'resolve_related_term' "$P/includes/class-uge-frontend.php"
grep -q 'uge-pftk-breadcrumb-mounted' "$P/includes/class-uge-frontend.php"
! grep -q 'echo self::render_breadcrumbs($term, null);' "$P/includes/class-uge-frontend.php"
! grep -q 'render_breadcrumbs($bc_group' "$P/templates/single-uge-term.php"
grep -q 'UGE_Frontend::resolve_related_term' "$P/templates/single-uge-term.php"
find "$P" -name '*.php' -print0 | xargs -0 -n1 php -l

echo UGE0210RC6_BUILD_PASS
