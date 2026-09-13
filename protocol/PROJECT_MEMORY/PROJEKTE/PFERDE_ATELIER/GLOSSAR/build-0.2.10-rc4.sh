#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.10-rc3.sh"
rm -rf /tmp/uge0210rc4
cp -a /tmp/uge0210rc3 /tmp/uge0210rc4
P=/tmp/uge0210rc4/universal-glossary-engine
python3 - <<'PY'
from pathlib import Path
p=Path('/tmp/uge0210rc4/universal-glossary-engine/universal-glossary-engine.php')
s=p.read_text()
assert s.count('Version: 0.2.10-rc3')==1
assert s.count("define('UGE_VERSION', '0.2.10-rc3');")==1
s=s.replace('Version: 0.2.10-rc3','Version: 0.2.10-rc4')
s=s.replace("define('UGE_VERSION', '0.2.10-rc3');","define('UGE_VERSION', '0.2.10-rc4');")
p.write_text(s)

# Replace the Pferde pack with an atomic cluster implementation: create every
# related term as draft first, wire every relationship/internal link, verify the
# complete graph, and only then publish all pack-owned terms in one batch.
p=Path('/tmp/uge0210rc4/universal-glossary-engine/includes/class-uge-pferde-content-pack.php')
p.write_text(r'''<?php
if (!defined('ABSPATH')) { exit; }
final class UGE_Pferde_Content_Pack {
    private const OPTION = 'uge_pferde_content_pack_0210';
    private const OWNED = '_uge_pack_0210_owned';
    public static function init(): void { add_action('init', [__CLASS__, 'maybe_install'], 120); }

    private static function items(string $base, string $category_url): array {
        return [
            'hufrehe' => [
                'title'=>'Hufrehe',
                'definition'=>'Hufrehe ist eine schmerzhafte Erkrankung der Huflederhaut, bei der die Verbindung zwischen Hufwand und Hufbein geschädigt werden kann.',
                'content'=>'<p>Bei der Hufrehe kommt es zu Veränderungen im empfindlichen Aufhängeapparat des Hufes. Das Pferd zeigt häufig deutliche Schmerzen und entlastet die betroffenen Hufe.</p><p>Zur Einordnung gehören <a href="'.$base.'begriff/strahlfaeule/">Strahlfäule</a> und <a href="'.$base.'begriff/hufabszess/">Hufabszess</a>. Weitere Begriffe stehen im Bereich <a href="'.$category_url.'">Gesundheit</a>.</p>',
                'synonyms'=>'Laminitis','related'=>['strahlfaeule','hufabszess'],
                'meta_title'=>'Hufrehe beim Pferd – Glossar','meta_description'=>'Hufrehe beim Pferd kurz erklärt: Bedeutung, Einordnung und verwandte Begriffe im Pferde-Atelier-Glossar.',
            ],
            'strahlfaeule' => [
                'title'=>'Strahlfäule',
                'definition'=>'Strahlfäule bezeichnet eine Zersetzung des Strahlhorns im Huf, die häufig mit feuchtem Milieu, Verschmutzung und mangelnder Hufhygiene zusammenhängt.',
                'content'=>'<p>Typisch sind weiches oder zerfallendes Strahlhorn und ein auffälliger Geruch. Entscheidend ist, Ursache und Ausmaß am Huf fachgerecht beurteilen zu lassen.</p><p>Im Zusammenhang stehen <a href="'.$base.'begriff/hufrehe/">Hufrehe</a> und <a href="'.$base.'begriff/hufabszess/">Hufabszess</a>. Weitere Begriffe finden sich unter <a href="'.$category_url.'">Gesundheit</a>.</p>',
                'synonyms'=>'','related'=>['hufrehe','hufabszess'],
                'meta_title'=>'Strahlfäule beim Pferd – Glossar','meta_description'=>'Strahlfäule beim Pferd kurz erklärt: Bedeutung und interne Verweise zu verwandten Hufbegriffen.',
            ],
            'hufabszess' => [
                'title'=>'Hufabszess',
                'definition'=>'Ein Hufabszess ist eine örtlich begrenzte eitrige Entzündung innerhalb der Hufkapsel, die häufig plötzlich starke Lahmheit verursacht.',
                'content'=>'<p>Der entstehende Druck in der festen Hufkapsel kann sehr schmerzhaft sein. Die genaue Lokalisation und Behandlung gehören in fachkundige Hände.</p><p>Zur weiteren Einordnung siehe <a href="'.$base.'begriff/hufrehe/">Hufrehe</a> und <a href="'.$base.'begriff/strahlfaeule/">Strahlfäule</a>. Weitere Glossarbegriffe stehen im Bereich <a href="'.$category_url.'">Gesundheit</a>.</p>',
                'synonyms'=>'Hufgeschwür','related'=>['hufrehe','strahlfaeule'],
                'meta_title'=>'Hufabszess beim Pferd – Glossar','meta_description'=>'Hufabszess beim Pferd kurz erklärt: Definition, Einordnung und verwandte Begriffe im Pferde-Atelier-Glossar.',
            ],
        ];
    }

    public static function maybe_install(): void {
        if (get_option(self::OPTION, '') === 'done') { return; }
        if (!class_exists('Pferde_Template_Kit') || !post_type_exists(UGE_Core::POST_TYPE) || !taxonomy_exists(UGE_Core::TAXONOMY)) { return; }
        $portal = get_page_by_path('gesundheit', OBJECT, 'page');
        if (!$portal instanceof WP_Post || $portal->post_status !== 'publish') { return; }
        if (method_exists('Pferde_Template_Kit','affiliate_page_type') && (string)Pferde_Template_Kit::affiliate_page_type($portal->ID) !== 'category') { return; }
        $group = get_term_by('slug','gesundheit',UGE_Core::TAXONOMY);
        if (!$group instanceof WP_Term) {
            $made=wp_insert_term('Gesundheit',UGE_Core::TAXONOMY,['slug'=>'gesundheit']);
            if (is_wp_error($made)) { return; }
            $group=get_term((int)$made['term_id'],UGE_Core::TAXONOMY);
        }
        if (!$group instanceof WP_Term) { return; }
        $base=trailingslashit(home_url('/glossar/')); $category_url=$base.'gesundheit/'; $items=self::items($base,$category_url); $ids=[];

        // Phase 1: every member exists as draft before any member is published.
        foreach ($items as $slug=>$item) {
            $existing=get_page_by_path($slug,OBJECT,UGE_Core::POST_TYPE);
            if ($existing instanceof WP_Post && get_post_meta($existing->ID,self::OWNED,true)!=='1') { return; }
            if ($existing instanceof WP_Post) { $ids[$slug]=(int)$existing->ID; continue; }
            $id=wp_insert_post(['post_type'=>UGE_Core::POST_TYPE,'post_status'=>'draft','post_title'=>$item['title'],'post_name'=>$slug],true);
            if (is_wp_error($id)||!$id) { return; }
            update_post_meta((int)$id,self::OWNED,'1'); $ids[$slug]=(int)$id;
        }
        if (count($ids)!==count($items)) { return; }

        // Phase 2: content + complete related graph + category link for every item.
        foreach ($items as $slug=>$item) {
            foreach ($item['related'] as $related_slug) { if (!isset($ids[$related_slug])) { return; } }
            $id=$ids[$slug];
            wp_update_post(['ID'=>$id,'post_title'=>$item['title'],'post_name'=>$slug,'post_content'=>$item['content'],'post_status'=>'draft']);
            wp_set_object_terms($id,[(int)$group->term_id],UGE_Core::TAXONOMY,false);
            update_post_meta($id,UGE_Core::meta_key('short_definition'),$item['definition']);
            update_post_meta($id,UGE_Core::meta_key('synonyms'),$item['synonyms']);
            $related_titles=array_map(static fn($rs)=>get_the_title($ids[$rs]),$item['related']);
            update_post_meta($id,UGE_Core::meta_key('related_terms'),implode(', ',$related_titles));
            update_post_meta($id,UGE_Core::meta_key('primary_category_id'),(string)$portal->ID);
            update_post_meta($id,UGE_Core::meta_key('seo_title'),$item['meta_title']);
            update_post_meta($id,UGE_Core::meta_key('seo_description'),$item['meta_description']);
        }

        // Phase 3 hard closure: each relation target exists, each relation has an
        // inline link, and every article links to the category. No H2/H3 are used.
        foreach ($items as $slug=>$item) {
            $post=get_post($ids[$slug]); if (!$post instanceof WP_Post) { return; }
            if (preg_match('/<h[2-6]\b/i',(string)$post->post_content)) { return; }
            if (!str_contains((string)$post->post_content,$category_url)) { return; }
            foreach ($item['related'] as $rs) {
                if (!str_contains((string)$post->post_content,$base.'begriff/'.$rs.'/')) { return; }
            }
        }

        // Phase 4: publish the complete closed cluster only after every check passed.
        foreach ($ids as $id) { wp_update_post(['ID'=>$id,'post_status'=>'publish']); }
        foreach ($ids as $id) { $p=get_post($id); if (!$p instanceof WP_Post || $p->post_status!=='publish') { return; } }
        update_option(self::OPTION,'done',false);
    }
}
''')

# Related terms at the bottom must be real links, never a dead text list.
p=Path('/tmp/uge0210rc4/universal-glossary-engine/templates/single-uge-term.php')
s=p.read_text()
old='<?php if ($related !== \'\') : ?><p><strong>Verwandte Begriffe:</strong> <?php echo esc_html($related); ?></p><?php endif; ?>'
new='''<?php if ($related !== '') : ?>
                        <p><strong>Verwandte Begriffe:</strong>
                        <?php
                        $related_links = [];
                        foreach (preg_split('/[,;\\n]+/', $related) ?: [] as $related_label) {
                            $related_label = trim((string)$related_label);
                            if ($related_label === '') { continue; }
                            $target = get_page_by_path(sanitize_title($related_label), OBJECT, UGE_Core::POST_TYPE);
                            if ($target instanceof WP_Post && $target->post_status === 'publish') {
                                $related_links[] = '<a href="' . esc_url(get_permalink($target)) . '">' . esc_html(get_the_title($target)) . '</a>';
                            }
                        }
                        echo implode(', ', $related_links);
                        ?>
                        </p>
                    <?php endif; ?>'''
assert s.count(old)==1, s.count(old)
s=s.replace(old,new)
p.write_text(s)
PY

grep -q 'Version: 0.2.10-rc4' "$P/universal-glossary-engine.php"
grep -q 'Phase 4: publish the complete closed cluster' "$P/includes/class-uge-pferde-content-pack.php"
grep -q 'related_links' "$P/templates/single-uge-term.php"
! grep -Eqi 'haflinger|friese|hannoveraner|trakehner|isländer|islaender|fjordpferd|quarter horse|warmblut|vollblut' "$P/includes/class-uge-pferde-content-pack.php"
find "$P" -name '*.php' -print0 | xargs -0 -n1 php -l
echo UGE0210RC4_BUILD_PASS
