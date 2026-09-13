#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.10-rc4.sh"
rm -rf /tmp/uge0210rc5
cp -a /tmp/uge0210rc4 /tmp/uge0210rc5
P=/tmp/uge0210rc5/universal-glossary-engine
python3 - <<'PY'
from pathlib import Path

# New bytes => new version. RC4 is consumed.
p=Path('/tmp/uge0210rc5/universal-glossary-engine/universal-glossary-engine.php')
s=p.read_text()
assert s.count('Version: 0.2.10-rc4')==1
assert s.count("define('UGE_VERSION', '0.2.10-rc4');")==1
s=s.replace('Version: 0.2.10-rc4','Version: 0.2.10-rc5')
s=s.replace("define('UGE_VERSION', '0.2.10-rc4');","define('UGE_VERSION', '0.2.10-rc5');")
p.write_text(s)

# Project content pack must depend on the Glossar category itself, not on a
# separate Pferde portal page hierarchy. That distinction matters in live and in
# the exact real-design harness.
p=Path('/tmp/uge0210rc5/universal-glossary-engine/includes/class-uge-pferde-content-pack.php')
s=p.read_text()
old="""        $portal = get_page_by_path('gesundheit', OBJECT, 'page');
        if (!$portal instanceof WP_Post || $portal->post_status !== 'publish') { return; }
        if (method_exists('Pferde_Template_Kit','affiliate_page_type') && (string)Pferde_Template_Kit::affiliate_page_type($portal->ID) !== 'category') { return; }
        $group = get_term_by('slug','gesundheit',UGE_Core::TAXONOMY);
"""
new="""        $group = get_term_by('slug','gesundheit',UGE_Core::TAXONOMY);
"""
assert s.count(old)==1
s=s.replace(old,new)
old="""            update_post_meta($id,UGE_Core::meta_key('primary_category_id'),(string)$portal->ID);
"""
assert s.count(old)==1
s=s.replace(old,'')
p.write_text(s)

# Single renderer: related terms must be real links, and the matching Glossar
# category must be linked directly from taxonomy truth. Never emit a dead related
# list and never use the unrelated Pferde portal hierarchy for this requirement.
p=Path('/tmp/uge0210rc5/universal-glossary-engine/templates/single-uge-term.php')
s=p.read_text()
old='''<?php if ($related !== '') : ?>
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
new='''<?php
                    $related_links = [];
                    if ($related !== '') {
                        foreach (preg_split('/[,;\\n]+/', $related) ?: [] as $related_label) {
                            $related_label = trim((string)$related_label);
                            if ($related_label === '') { continue; }
                            $target = get_page_by_path(sanitize_title($related_label), OBJECT, UGE_Core::POST_TYPE);
                            if ($target instanceof WP_Post && $target->post_status === 'publish') {
                                $related_links[] = '<a href="' . esc_url(get_permalink($target)) . '">' . esc_html(get_the_title($target)) . '</a>';
                            }
                        }
                    }
                    if ($related_links) {
                        echo '<p class="uge-related-links"><strong>Verwandte Begriffe:</strong> ' . implode(', ', $related_links) . '</p>';
                    }
                    $glossary_groups = wp_get_post_terms($uge_post->ID, UGE_Core::TAXONOMY);
                    if (!is_wp_error($glossary_groups) && $glossary_groups) {
                        $glossary_group = UGE_Core::navigation_group_for_post($uge_post->ID);
                        if (!$glossary_group instanceof WP_Term) { $glossary_group = $glossary_groups[0]; }
                        $group_url = get_term_link($glossary_group, UGE_Core::TAXONOMY);
                        if (!is_wp_error($group_url)) {
                            echo '<p class="uge-glossary-category-link"><strong>Glossar-Bereich:</strong> <a href="' . esc_url($group_url) . '">' . esc_html($glossary_group->name) . '</a></p>';
                        }
                    }
                    ?>'''
assert s.count(old)==1
s=s.replace(old,new)
p.write_text(s)
PY

grep -q 'Version: 0.2.10-rc5' "$P/universal-glossary-engine.php"
! grep -q 'affiliate_page_type' "$P/includes/class-uge-pferde-content-pack.php"
! grep -q 'primary_category_id' "$P/includes/class-uge-pferde-content-pack.php"
grep -q 'uge-related-links' "$P/templates/single-uge-term.php"
grep -q 'uge-glossary-category-link' "$P/templates/single-uge-term.php"
find "$P" -name '*.php' -print0 | xargs -0 -n1 php -l

echo UGE0210RC5_BUILD_PASS
