<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Read-only comparison archive.
 * No post/content/meta writes and no TEXT/SEO dependency.
 */
class UPC_Archive {
    private $repository;

    public function __construct( $repository ) {
        $this->repository = $repository;
    }

    public function build_view( $project_key, $category_slug ) {
        $config = UPC_Project_Config::load_publishing( $project_key );
        if ( is_wp_error( $config ) ) {
            return $config;
        }

        $binding = $this->find_category_binding( $config, $category_slug );
        if ( is_wp_error( $binding ) ) {
            return $binding;
        }

        $term = get_term_by( 'slug', $binding['slug'], 'category' );
        if ( ! $term || is_wp_error( $term ) ) {
            return new WP_Error( 'UPC_ARCHIVE_CATEGORY_NOT_FOUND', 'Bound comparison category does not exist.' );
        }

        $posts = get_posts(
            array(
                'post_type'      => 'post',
                'post_status'    => 'publish',
                'posts_per_page' => -1,
                'orderby'        => array( 'menu_order' => 'ASC', 'date' => 'DESC', 'ID' => 'ASC' ),
                'category'       => (int) $term->term_id,
            )
        );

        $items = array();
        $products = array();

        foreach ( $posts as $post ) {
            $comparison_id = absint( get_post_meta( $post->ID, '_upc_comparison_id', true ) );

            if ( $comparison_id <= 0 ) {
                $items[] = array(
                    'post_id'         => (int) $post->ID,
                    'title'           => get_the_title( $post ),
                    'permalink'       => get_permalink( $post ),
                    'archive_type'    => 'product_group',
                    'comparison_type' => '',
                    'product_keys'    => array(),
                    'search_text'     => $this->normalize_search( get_the_title( $post ) ),
                );
                continue;
            }

            $bundle = $this->repository->get_comparison_bundle( $comparison_id );
            if ( is_wp_error( $bundle ) ) {
                return new WP_Error(
                    'UPC_ARCHIVE_BROKEN_COMPARISON_REFERENCE',
                    'Published comparison post points to an invalid comparison.',
                    array( 'post_id' => (int) $post->ID, 'comparison_id' => $comparison_id )
                );
            }

            $comparison_type = strtoupper( (string) $bundle['comparison_type'] );
            if ( ! in_array( $comparison_type, array( UPC_Repository::TYPE_PRODUCT, UPC_Repository::TYPE_VARIANT ), true ) ) {
                return new WP_Error(
                    'UPC_ARCHIVE_UNKNOWN_COMPARISON_TYPE',
                    'Published comparison post has an unsupported comparison type.',
                    array( 'post_id' => (int) $post->ID )
                );
            }

            $product_keys = array();
            $search_parts = array( get_the_title( $post ) );

            foreach ( $bundle['items'] as $comparison_item ) {
                $product = $this->base_product_identity( $comparison_item );
                if ( is_wp_error( $product ) ) {
                    return $product;
                }

                $product_key = $this->product_key( $product );
                $product_keys[] = $product_key;
                $search_parts[] = $product['manufacturer'];
                $search_parts[] = $product['model_name'];

                if ( UPC_Repository::TYPE_VARIANT === $comparison_type ) {
                    $search_parts[] = (string) ( $comparison_item['knowledge']['variant_name'] ?? '' );
                }

                if ( ! isset( $products[ $product_key ] ) ) {
                    $products[ $product_key ] = array(
                        'key'          => $product_key,
                        'manufacturer' => $product['manufacturer'],
                        'model_name'   => $product['model_name'],
                        'label'        => trim( $product['manufacturer'] . ' ' . $product['model_name'] ),
                        'post_ids'     => array(),
                    );
                }
                $products[ $product_key ]['post_ids'][ (int) $post->ID ] = (int) $post->ID;
            }

            $items[] = array(
                'post_id'         => (int) $post->ID,
                'title'           => get_the_title( $post ),
                'permalink'       => get_permalink( $post ),
                'archive_type'    => 'product_comparison',
                'comparison_type' => strtolower( $comparison_type ),
                'product_keys'    => array_values( array_unique( $product_keys ) ),
                'search_text'     => $this->normalize_search( implode( ' ', $search_parts ) ),
            );
        }

        foreach ( $products as &$product ) {
            $product['post_ids'] = array_values( $product['post_ids'] );
            $product['comparison_count'] = count( $product['post_ids'] );
        }
        unset( $product );

        uasort(
            $products,
            function( $left, $right ) {
                return strcasecmp( $left['label'], $right['label'] );
            }
        );

        return array(
            'project_key'   => sanitize_key( $project_key ),
            'category_slug' => $binding['slug'],
            'category_name' => $binding['name'],
            'product_group_key' => $binding['_product_group_key'],
            'items'          => $items,
            'products'       => array_values( $products ),
        );
    }

    public function render( $project_key, $category_slug ) {
        $view = $this->build_view( $project_key, $category_slug );
        if ( is_wp_error( $view ) ) {
            return $view;
        }

        $scope_id = 'upc-archive-' . substr(
            hash( 'sha256', $view['project_key'] . '|' . $view['category_slug'] ),
            0,
            12
        );

        $out = array();
        $out[] = '<section id="' . esc_attr( $scope_id ) . '" class="upc-archive" data-upc-archive>';
        $out[] = '<nav class="upc-archive__filters" aria-label="Vergleichsfilter">';
        $out[] = '<button type="button" data-upc-filter="all" aria-pressed="true">Alle</button>';
        $out[] = '<button type="button" data-upc-filter="product_group" aria-pressed="false">Produktgruppenvergleiche</button>';
        $out[] = '<button type="button" data-upc-filter="product_comparison" aria-pressed="false">Produktvergleiche</button>';
        $out[] = '</nav>';

        $out[] = '<div class="upc-archive__product-subfilters" data-upc-subfilters hidden>';
        $out[] = '<button type="button" data-upc-subfilter="all" aria-pressed="true">Alle Produkte</button>';
        $out[] = '<button type="button" data-upc-subfilter="product" aria-pressed="false">Produkte</button>';
        $out[] = '<button type="button" data-upc-subfilter="variant" aria-pressed="false">Varianten</button>';
        $out[] = '</div>';

        $out[] = '<label class="upc-archive__search"><span>Produkt suchen</span><input type="search" data-upc-search autocomplete="off"></label>';

        $out[] = '<details class="upc-archive__product-index">';
        $out[] = '<summary>Produkte mit Vergleichen</summary>';
        if ( empty( $view['products'] ) ) {
            $out[] = '<p>Keine konkreten Produkte mit Vergleich vorhanden.</p>';
        } else {
            $out[] = '<ul>';
            foreach ( $view['products'] as $product ) {
                $out[] = '<li><button type="button" data-upc-product="' . esc_attr( $product['key'] ) . '">' .
                    esc_html( $product['label'] ) . ' (' . (int) $product['comparison_count'] . ')</button></li>';
            }
            $out[] = '</ul>';
        }
        $out[] = '</details>';

        $out[] = '<div class="upc-archive__results" data-upc-results>';
        foreach ( $view['items'] as $item ) {
            $out[] = '<article class="upc-archive__item" data-upc-item' .
                ' data-upc-type="' . esc_attr( $item['archive_type'] ) . '"' .
                ' data-upc-comparison-type="' . esc_attr( $item['comparison_type'] ) . '"' .
                ' data-upc-products="' . esc_attr( implode( ' ', $item['product_keys'] ) ) . '"' .
                ' data-upc-search-text="' . esc_attr( $item['search_text'] ) . '">';
            $out[] = '<p class="upc-archive__type">' . esc_html( $this->type_label( $item ) ) . '</p>';
            $out[] = '<h2 class="upc-archive__title"><a href="' . esc_url( $item['permalink'] ) . '">' . esc_html( $item['title'] ) . '</a></h2>';
            $out[] = '</article>';
        }
        $out[] = '<p data-upc-empty hidden>Keine passenden Vergleiche gefunden.</p>';
        $out[] = '</div>';
        $out[] = '</section>';

        wp_enqueue_script(
            'upc-comparison-archive',
            plugins_url( 'assets/archive.js', UPC_PLUGIN_FILE ),
            array(),
            UPC_VERSION,
            true
        );

        return implode( "\n", $out );
    }

    private function find_category_binding( array $config, $category_slug ) {
        $category_slug = sanitize_title( $category_slug );
        foreach ( $config['category_map'] as $group_key => $binding ) {
            if ( sanitize_title( (string) ( $binding['slug'] ?? '' ) ) === $category_slug ) {
                $binding['_product_group_key'] = sanitize_key( $group_key );
                return $binding;
            }
        }
        return new WP_Error( 'UPC_ARCHIVE_CATEGORY_NOT_BOUND', 'Category is not bound to this project comparison archive.' );
    }

    private function base_product_identity( array $comparison_item ) {
        if ( UPK_Repository::SUBJECT_PRODUCT === $comparison_item['subject_type'] ) {
            return array(
                'manufacturer' => (string) $comparison_item['knowledge']['manufacturer'],
                'model_name'   => (string) $comparison_item['knowledge']['model_name'],
            );
        }

        if ( UPK_Repository::SUBJECT_VARIANT === $comparison_item['subject_type']
            && ! empty( $comparison_item['knowledge']['product'] )
        ) {
            return array(
                'manufacturer' => (string) $comparison_item['knowledge']['product']['manufacturer'],
                'model_name'   => (string) $comparison_item['knowledge']['product']['model_name'],
            );
        }

        return new WP_Error( 'UPC_ARCHIVE_PRODUCT_IDENTITY_MISSING', 'Comparison item has no resolvable base product identity.' );
    }

    private function product_key( array $product ) {
        return substr(
            hash(
                'sha256',
                strtolower(
                    remove_accents(
                        trim( $product['manufacturer'] ) . '|' . trim( $product['model_name'] )
                    )
                )
            ),
            0,
            20
        );
    }

    private function normalize_search( $value ) {
        return strtolower( remove_accents( wp_strip_all_tags( (string) $value ) ) );
    }

    private function type_label( array $item ) {
        if ( 'product_group' === $item['archive_type'] ) {
            return 'Produktgruppenvergleich';
        }
        if ( 'variant' === $item['comparison_type'] ) {
            return 'Variantenvergleich';
        }
        return 'Produktvergleich';
    }
}
