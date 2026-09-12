<?php
if (!defined('ABSPATH')) { exit; }
get_header();
while (have_posts()) : the_post();
    $groups = wp_get_post_terms(get_the_ID(), UGE_Core::TAXONOMY);
    $group_name = (!is_wp_error($groups) && !empty($groups)) ? $groups[0]->name : UGE_Config::get()['label'];
    $definition = UGE_Core::term_value(get_the_ID(), 'short_definition');
    $synonyms = UGE_Core::term_value(get_the_ID(), 'synonyms');
    $related = UGE_Core::term_value(get_the_ID(), 'related_terms');
    ?>
    <main class="uge uge-single" id="primary">
        <article class="uge-single-card">
            <div class="uge-kicker"><?php echo esc_html($group_name); ?></div>
            <h1><?php the_title(); ?></h1>
            <?php if ($definition !== '') : ?><p class="uge-definition"><?php echo esc_html($definition); ?></p><?php endif; ?>
            <div class="uge-content"><?php the_content(); ?></div>
            <?php if ($synonyms !== '') : ?><p><strong>Synonyme:</strong> <?php echo esc_html($synonyms); ?></p><?php endif; ?>
            <?php if ($related !== '') : ?><p><strong>Verwandte Begriffe:</strong> <?php echo esc_html($related); ?></p><?php endif; ?>
        </article>
    </main>
    <?php
endwhile;
get_footer();
