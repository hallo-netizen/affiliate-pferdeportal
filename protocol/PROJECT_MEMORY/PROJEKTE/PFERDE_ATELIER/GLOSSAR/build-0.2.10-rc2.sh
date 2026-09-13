#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.10-rc1.sh"
rm -rf /tmp/uge0210rc2
cp -a /tmp/uge0210rc1 /tmp/uge0210rc2
P=/tmp/uge0210rc2/universal-glossary-engine
python3 - <<'PY'
from pathlib import Path

# New bytes => new version. RC1 is consumed because it failed the full regression.
p=Path('/tmp/uge0210rc2/universal-glossary-engine/universal-glossary-engine.php')
s=p.read_text()
assert s.count('Version: 0.2.10-rc1')==1
assert s.count("define('UGE_VERSION', '0.2.10-rc1');")==1
s=s.replace('Version: 0.2.10-rc1','Version: 0.2.10-rc2')
s=s.replace("define('UGE_VERSION', '0.2.10-rc1');","define('UGE_VERSION', '0.2.10-rc2');")
# Generic bootstrap hook for the project-specific pack; other portals are untouched
# because the pack class itself requires the Pferde design runtime.
needle="require_once UGE_DIR . 'includes/class-uge-policy.php';\n"
assert s.count(needle)==1
s=s.replace(needle,needle+"require_once UGE_DIR . 'includes/class-uge-pferde-content-pack.php';\n")
needle="    UGE_Policy::init();\n"
assert s.count(needle)==1
s=s.replace(needle,needle+"    UGE_Pferde_Content_Pack::init();\n")
p.write_text(s)

# Restore the existing primary portal-category link contract even when the single
# is rendered independently of WordPress' main loop.
p=Path('/tmp/uge0210rc2/universal-glossary-engine/templates/single-uge-term.php')
s=p.read_text()
old='''            <div class="uge-content"><?php the_content(); ?></div>
            <div class="uge-ad-slot uge-ad-slot-inline"><?php do_action('uge_ad_slot', 'inline', get_the_ID()); ?></div>
'''
new='''            <div class="uge-content"><?php
                echo apply_filters('the_content', (string)$uge_post->post_content);
                $primary_target = UGE_Core::primary_category_target($uge_post->ID);
                if ($primary_target) {
                    printf(
                        '<p class="uge-primary-category">Zum Themenbereich: <a href="%s">%s</a></p>',
                        esc_url((string)$primary_target['url']),
                        esc_html((string)$primary_target['label'])
                    );
                }
            ?></div>
            <div class="uge-ad-slot uge-ad-slot-inline"><?php do_action('uge_ad_slot', 'inline', $uge_post->ID); ?></div>
'''
assert s.count(old)==1
s=s.replace(old,new)
# IDs in ad/meta calls must use the resolved direct post, not a possibly-poisoned loop global.
s=s.replace("do_action('uge_ad_slot', 'top', get_the_ID());","do_action('uge_ad_slot', 'top', $uge_post->ID);")
s=s.replace("do_action('uge_ad_slot', 'bottom', get_the_ID());","do_action('uge_ad_slot', 'bottom', $uge_post->ID);")
p.write_text(s)
PY

cat >"$P/includes/class-uge-pferde-content-pack.php" <<'PHP'
<?php
if (!defined('ABSPATH')) { exit; }

/**
 * Project content pack for Pferde Atelier.
 * The Universal Glossary Engine remains inert on other portals: no Pferde design
 * class => no content is created. Every pack key is one-shot and never overwrites
 * an already existing glossary term.
 */
final class UGE_Pferde_Content_Pack {
    private const OPTION = 'uge_pferde_content_pack_0210';

    public static function init(): void {
        add_action('init', [__CLASS__, 'maybe_install'], 120);
    }

    public static function maybe_install(): void {
        if (get_option(self::OPTION, '') === 'done') { return; }
        if (!class_exists('Pferde_Template_Kit')) { return; }
        if (!post_type_exists(UGE_Core::POST_TYPE) || !taxonomy_exists(UGE_Core::TAXONOMY)) { return; }

        $portal = get_page_by_path('gesundheit', OBJECT, 'page');
        if (!$portal instanceof WP_Post || $portal->post_status !== 'publish') { return; }

        $group = get_term_by('slug', 'gesundheit', UGE_Core::TAXONOMY);
        if (!$group instanceof WP_Term) {
            $created = wp_insert_term('Gesundheit', UGE_Core::TAXONOMY, ['slug'=>'gesundheit']);
            if (is_wp_error($created)) { return; }
            $group = get_term((int)$created['term_id'], UGE_Core::TAXONOMY);
        }
        if (!$group instanceof WP_Term) { return; }

        $base = trailingslashit(home_url('/glossar/'));
        $category_url = $base . 'gesundheit/';
        $items = [
            [
                'slug'=>'hufrehe',
                'title'=>'Hufrehe',
                'definition'=>'Hufrehe ist eine schmerzhafte Erkrankung der Huflederhaut, bei der die Verbindung zwischen Hufwand und Hufbein geschädigt werden kann.',
                'content'=>'<p>Bei der Hufrehe kommt es zu Veränderungen im empfindlichen Aufhängeapparat des Hufes. Das Pferd zeigt häufig deutliche Schmerzen und entlastet die betroffenen Hufe.</p><p>Für die Einordnung sind auch die Begriffe <a href="'.$base.'begriff/strahlfaeule/">Strahlfäule</a> und <a href="'.$base.'begriff/hufabszess/">Hufabszess</a> hilfreich. Weitere Begriffe stehen im Bereich <a href="'.$category_url.'">Gesundheit</a>.</p>',
                'synonyms'=>'Laminitis',
                'related'=>'Strahlfäule, Hufabszess',
                'meta_title'=>'Hufrehe beim Pferd – Glossar',
                'meta_description'=>'Kurze Erklärung zur Hufrehe beim Pferd: Bedeutung, Einordnung und verwandte Begriffe im Pferde-Atelier-Glossar.',
            ],
            [
                'slug'=>'strahlfaeule',
                'title'=>'Strahlfäule',
                'definition'=>'Strahlfäule bezeichnet eine Zersetzung des Strahlhorns im Huf, die häufig mit feuchtem Milieu, Verschmutzung und mangelnder Hufhygiene zusammenhängt.',
                'content'=>'<p>Typisch sind weiches oder zerfallendes Strahlhorn und ein auffälliger Geruch. Entscheidend ist, Ursache und Ausmaß am Huf fachgerecht beurteilen zu lassen.</p><p>Im Zusammenhang stehen unter anderem <a href="'.$base.'begriff/hufrehe/">Hufrehe</a> und <a href="'.$base.'begriff/hufabszess/">Hufabszess</a>. Weitere Begriffe finden sich unter <a href="'.$category_url.'">Gesundheit</a>.</p>',
                'synonyms'=>'',
                'related'=>'Hufrehe, Hufabszess',
                'meta_title'=>'Strahlfäule beim Pferd – Glossar',
                'meta_description'=>'Strahlfäule beim Pferd kurz erklärt: Bedeutung, typische Einordnung und interne Verweise zu verwandten Hufbegriffen.',
            ],
            [
                'slug'=>'hufabszess',
                'title'=>'Hufabszess',
                'definition'=>'Ein Hufabszess ist eine örtlich begrenzte eitrige Entzündung innerhalb der Hufkapsel, die häufig plötzlich starke Lahmheit verursacht.',
                'content'=>'<p>Der entstehende Druck in der festen Hufkapsel kann sehr schmerzhaft sein. Die genaue Lokalisation und Behandlung gehören in fachkundige Hände.</p><p>Zur weiteren Einordnung siehe <a href="'.$base.'begriff/hufrehe/">Hufrehe</a> und <a href="'.$base.'begriff/strahlfaeule/">Strahlfäule</a>. Weitere Glossarbegriffe stehen im Bereich <a href="'.$category_url.'">Gesundheit</a>.</p>',
                'synonyms'=>'Hufgeschwür',
                'related'=>'Hufrehe, Strahlfäule',
                'meta_title'=>'Hufabszess beim Pferd – Glossar',
                'meta_description'=>'Hufabszess beim Pferd kurz erklärt: Definition, Einordnung und verwandte Begriffe im Pferde-Atelier-Glossar.',
            ],
        ];

        foreach ($items as $item) {
            $existing = get_page_by_path($item['slug'], OBJECT, UGE_Core::POST_TYPE);
            if ($existing instanceof WP_Post) { continue; }

            $post_id = wp_insert_post([
                'post_type'=>UGE_Core::POST_TYPE,
                'post_status'=>'draft',
                'post_title'=>$item['title'],
                'post_name'=>$item['slug'],
                'post_content'=>$item['content'],
            ], true);
            if (is_wp_error($post_id) || !$post_id) { return; }

            wp_set_object_terms((int)$post_id, [(int)$group->term_id], UGE_Core::TAXONOMY, false);
            update_post_meta((int)$post_id, UGE_Core::meta_key('short_definition'), $item['definition']);
            update_post_meta((int)$post_id, UGE_Core::meta_key('synonyms'), $item['synonyms']);
            update_post_meta((int)$post_id, UGE_Core::meta_key('related_terms'), $item['related']);
            update_post_meta((int)$post_id, UGE_Core::meta_key('primary_category_id'), (string)$portal->ID);
            $schema = UGE_Config::field_schema();
            if (isset($schema['meta_title'])) { update_post_meta((int)$post_id, UGE_Core::meta_key('meta_title'), $item['meta_title']); }
            if (isset($schema['meta_description'])) { update_post_meta((int)$post_id, UGE_Core::meta_key('meta_description'), $item['meta_description']); }
            if (isset($schema['seo_title'])) { update_post_meta((int)$post_id, UGE_Core::meta_key('seo_title'), $item['meta_title']); }
            if (isset($schema['seo_description'])) { update_post_meta((int)$post_id, UGE_Core::meta_key('seo_description'), $item['meta_description']); }
            wp_update_post(['ID'=>(int)$post_id,'post_status'=>'publish']);
            $saved = get_post((int)$post_id);
            if (!$saved instanceof WP_Post || $saved->post_status !== 'publish') { return; }
        }

        update_option(self::OPTION, 'done', false);
    }
}
PHP

# Guards: no horse breed names/data; this pack is hoof-health only.
grep -q 'Version: 0.2.10-rc2' "$P/universal-glossary-engine.php"
grep -q 'UGE_Pferde_Content_Pack::init' "$P/universal-glossary-engine.php"
grep -q 'uge-primary-category' "$P/templates/single-uge-term.php"
grep -q "'slug'=>'hufrehe'" "$P/includes/class-uge-pferde-content-pack.php"
grep -q "'slug'=>'strahlfaeule'" "$P/includes/class-uge-pferde-content-pack.php"
grep -q "'slug'=>'hufabszess'" "$P/includes/class-uge-pferde-content-pack.php"
! grep -Eqi 'haflinger|friese|hannoveraner|trakehner|isländer|islaender|fjordpferd|quarter horse|warmblut|vollblut' "$P/includes/class-uge-pferde-content-pack.php"
find "$P" -name '*.php' -print0 | xargs -0 -n1 php -l

echo UGE0210RC2_BUILD_PASS
