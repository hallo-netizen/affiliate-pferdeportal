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

p=Path('/tmp/uge0210rc4/universal-glossary-engine/includes/class-uge-pferde-content-pack.php')
s=p.read_text()
# Do not start creating terms until the Pferde design itself recognizes the target
# page as a portal category. This prevents partially-created drafts during seed/live
# startup before the category contract is ready.
old="""        $portal = get_page_by_path('gesundheit', OBJECT, 'page');
        if (!$portal instanceof WP_Post || $portal->post_status !== 'publish') { return; }

        $group = get_term_by('slug', 'gesundheit', UGE_Core::TAXONOMY);
"""
new="""        $portal = get_page_by_path('gesundheit', OBJECT, 'page');
        if (!$portal instanceof WP_Post || $portal->post_status !== 'publish') { return; }
        if (method_exists('Pferde_Template_Kit', 'affiliate_page_type')) {
            $portal_type = (string)Pferde_Template_Kit::affiliate_page_type($portal->ID);
            if ($portal_type !== 'category') { return; }
        }

        $group = get_term_by('slug', 'gesundheit', UGE_Core::TAXONOMY);
"""
assert s.count(old)==1
s=s.replace(old,new)

# Existing user-authored terms are sacred. Pack-owned partial terms, however,
# must be recoverable on the next request instead of being skipped forever.
old="""        foreach ($items as $item) {
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
"""
new="""        foreach ($items as $item) {
            $existing = get_page_by_path($item['slug'], OBJECT, UGE_Core::POST_TYPE);
            if ($existing instanceof WP_Post) {
                $owned = get_post_meta($existing->ID, '_uge_pack_0210_owned', true) === '1';
                if (!$owned) { continue; }
                $post_id = $existing->ID;
            } else {
                $post_id = wp_insert_post([
                    'post_type'=>UGE_Core::POST_TYPE,
                    'post_status'=>'draft',
                    'post_title'=>$item['title'],
                    'post_name'=>$item['slug'],
                    'post_content'=>$item['content'],
                ], true);
                if (is_wp_error($post_id) || !$post_id) { return; }
                update_post_meta((int)$post_id, '_uge_pack_0210_owned', '1');
            }

            wp_set_object_terms((int)$post_id, [(int)$group->term_id], UGE_Core::TAXONOMY, false);
"""
assert s.count(old)==1
s=s.replace(old,new)

# Only declare the pack complete after every intended term exists published. This
# closes the partial-install hole caught by RC3.
old="""        update_option(self::OPTION, 'done', false);
    }
}
"""
new="""        foreach ($items as $item) {
            $check = get_page_by_path($item['slug'], OBJECT, UGE_Core::POST_TYPE);
            if (!$check instanceof WP_Post || $check->post_status !== 'publish') { return; }
        }
        update_option(self::OPTION, 'done', false);
    }
}
"""
assert s.count(old)==1
s=s.replace(old,new)
p.write_text(s)
PY

grep -q 'Version: 0.2.10-rc4' "$P/universal-glossary-engine.php"
grep -q "affiliate_page_type" "$P/includes/class-uge-pferde-content-pack.php"
grep -q '_uge_pack_0210_owned' "$P/includes/class-uge-pferde-content-pack.php"
grep -q "post_status !== 'publish'" "$P/includes/class-uge-pferde-content-pack.php"
! grep -Eqi 'haflinger|friese|hannoveraner|trakehner|isländer|islaender|fjordpferd|quarter horse|warmblut|vollblut' "$P/includes/class-uge-pferde-content-pack.php"
find "$P" -name '*.php' -print0 | xargs -0 -n1 php -l

echo UGE0210RC4_BUILD_PASS
