<?php
/**
 * Hab & Bewahr – Ein gemeinsames Beitragsdesign für normale WordPress-Beiträge.
 * Keine Änderungen an Beiträgen, Kategorien oder K0.
 */
if (!defined('ABSPATH')) exit;

function hbdp_article_slot_html($kind, $post_id) {
    if (!is_singular('post')) return '';
    $hook = $kind === 'banner' ? 'hbdp_article_auto_banner_html' : 'hbdp_article_product_cards_html';
    $ids = wp_get_post_categories((int)$post_id);
    $output = apply_filters($hook, '', (int)$post_id, $ids);
    if (!is_string($output) || trim($output) === '') {
        if (!current_user_can('manage_options')) return '';
        $label = $kind === 'banner' ? 'Bannerplatz' : 'Produktplatz';
        return '<aside class="hb-article-slot-empty" aria-label="Nur für Administratoren">Entwurf · '.$label.' – noch kein passendes Angebot verbunden</aside>';
    }
    $safe = wp_kses_post($output);
    if (class_exists('WP_HTML_Tag_Processor')) {
        $processor = new WP_HTML_Tag_Processor($safe);
        while ($processor->next_tag('a')) {
            $existing = (string)$processor->get_attribute('rel');
            $processor->set_attribute('rel', trim($existing.' sponsored nofollow'));
        }
        $safe = $processor->get_updated_html();
    }
    if (trim($safe) === '') return '';
    $class = $kind === 'banner' ? 'hb-article-ad--banner' : 'hb-article-ad--product';
    return '<aside class="hb-article-ad '.esc_attr($class).'" aria-label="Anzeige"><span class="hb-article-ad-label">Anzeige</span><div class="hb-article-ad-content">'.$safe.'</div></aside>';
}

add_shortcode('hb_produkte', static function () {
    return is_singular('post') ? hbdp_article_slot_html('product', get_queried_object_id()) : '';
});
add_shortcode('hb_banner', static function () {
    return is_singular('post') ? hbdp_article_slot_html('banner', get_queried_object_id()) : '';
});

function hbdp_article_clean_content($post) {
    $html = apply_filters('the_content', (string)$post->post_content);
    // Ersetze ausschließlich den bekannten Musterimport-Platzhalter, nicht freie redaktionelle Texte.
    $pattern = '~<div(?=[^>]*\bhb-affiliate-platzhalter\b)(?=[^>]*\bhb-(produktplatz|bannerplatz)\b)[^>]*>.*?</div>~is';
    $html = preg_replace_callback($pattern, static function ($hit) use ($post) {
        $kind = strtolower($hit[1]) === 'bannerplatz' ? 'banner' : 'product';
        return hbdp_article_slot_html($kind, (int)$post->ID);
    }, $html);
    // Nicht verlinkte Redaktionsnotizen gehören nicht ins öffentliche Frontend.
    $html = preg_replace('~<p[^>]*class="[^"]*\bhb-interne-links-redaktionell-offen\b[^"]*"[^>]*>.*?</p>~is', '', $html);
    return $html;
}

function hbdp_render_article_page() {
    $post = get_queried_object();
    if (!($post instanceof WP_Post) || $post->post_type !== 'post') return;
    $categories = get_the_category($post->ID);
    $category = is_array($categories) && !empty($categories) ? reset($categories) : null;
    $has_cat = $category instanceof WP_Term;
    ?>
    <main id="hauptinhalt" class="hbdp-frame hbdp-section hbdp-article hb-article-layout">
      <nav class="hb-article-breadcrumb hbdp-crumb" aria-label="Pfadnavigation">
        <a href="<?php echo esc_url(home_url('/')); ?>">Startseite</a>
        <span aria-hidden="true">/</span>
        <?php if ($has_cat) : ?>
          <a href="<?php echo esc_url(get_category_link($category->term_id)); ?>"><?php echo esc_html($category->name); ?></a>
          <span aria-hidden="true">/</span>
        <?php endif; ?>
        <span aria-current="page"><?php echo esc_html(get_the_title($post)); ?></span>
      </nav>

      <header class="hb-article-header">
        <div class="hb-article-eyebrow">HAB & BEWAHR <span aria-hidden="true">·</span> RATGEBER</div>
        <h1><?php echo esc_html(get_the_title($post)); ?></h1>
        <p class="hb-article-byline">
          <?php echo esc_html(get_the_date('j. F Y', $post)); ?>
          <?php if ($has_cat) : ?><span aria-hidden="true"> · </span><?php echo esc_html($category->name); ?><?php endif; ?>
        </p>
      </header>

      <?php if (has_post_thumbnail($post->ID)) : ?>
        <figure class="hb-article-photo"><?php echo get_the_post_thumbnail($post->ID, 'large', array('loading' => 'eager', 'decoding' => 'async')); ?></figure>
      <?php endif; ?>

      <div class="hb-article-reading hab-und-bewahr-beitrag">
        <?php echo hbdp_article_clean_content($post); // WordPress-post_content inklusive Block-/Shortcode-Filter. ?>
      </div>
    </main>
    <?php
}
