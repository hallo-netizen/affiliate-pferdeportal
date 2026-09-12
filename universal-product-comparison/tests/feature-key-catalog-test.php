<?php

define( 'ABSPATH', __DIR__ . '/' );

class WP_Error {
    private $code;
    public function __construct( $code, $message = '' ) { $this->code = $code; }
    public function get_error_code() { return $this->code; }
}
function is_wp_error( $value ) { return $value instanceof WP_Error; }

function feature_catalog_assert( $condition, $label ) {
    if ( ! $condition ) {
        fwrite( STDERR, "FAIL: {$label}\n" );
        exit( 1 );
    }
    fwrite( STDOUT, "PASS: {$label}\n" );
}

require_once dirname( __DIR__ ) . '/src/class-upc-feature-key-catalog.php';

$path = dirname( __DIR__ ) . '/config/pferde-atelier/feature-key-catalog.json';
$catalog = UPC_Feature_Key_Catalog::load( $path );
feature_catalog_assert( ! is_wp_error( $catalog ), 'canonical catalog loads' );
feature_catalog_assert( 143 === $catalog->count(), 'exactly 143 researched feature labels bound' );

$meta = $catalog->metadata();
feature_catalog_assert( 68 === (int) $meta['dossier_count'], '68 dossier source bound' );
feature_catalog_assert( 900 === (int) $meta['matrix_row_count'], '900 dossier matrix rows bound' );
feature_catalog_assert( '3b03a99ed042e2c5bcc8f37df83c03c3c6a9bb12b93bd5e05676b222adefa478' === (string) $meta['source_file_sha256'], 'research workbook sha256 bound' );
feature_catalog_assert( 'cec9b55bcb7fd074c005597aa0ee716c3a4e0efb7c188f7ea8f7666471d57d6e' === (string) $meta['matrix_sha256'], 'research matrix sha256 bound' );

$legacy = array(
    'Füllgewicht' => 'fill_weight',
    'Außenmaterial/Denier' => 'outer_material_denier',
    'Wasserdichtigkeit' => 'waterproofness',
    'Atmungsaktivität' => 'breathability',
    'Hals-/Halsteilkonzept' => 'neck_system',
    'Liner-Kompatibilität' => 'liner_compatibility',
    'Frontverschluss' => 'front_closure',
    'Bewegungs-/Schnittkonstruktion' => 'movement_cut',
    'Kreuzgurte' => 'cross_surcingles',
    'Beingurte/Schweifriemen' => 'leg_straps_tail_cord',
    'Schweiflatz' => 'tail_flap',
    'Größen' => 'sizes',
    'Garantie' => 'warranty',
    'Pflege' => 'care',
);
foreach ( $legacy as $label => $expected ) {
    feature_catalog_assert( $expected === $catalog->resolve( $label ), 'legacy key preserved: ' . $label );
}

feature_catalog_assert( 'zulaessiges_gesamtgewicht' === $catalog->resolve( 'zulässiges Gesamtgewicht' ), 'new researched key resolves deterministically' );
feature_catalog_assert( 'uebertragung_wlan_lte_hotspot' === $catalog->resolve( 'Übertragung WLAN/LTE/Hotspot' ), 'unicode researched key resolves deterministically' );

$result = $catalog->resolve( 'Farbe' );
feature_catalog_assert( is_wp_error( $result ) && 'UPC_FEATURE_LABEL_UNKNOWN' === $result->get_error_code(), 'unknown new label blocked fail closed' );
$result = $catalog->resolve( '' );
feature_catalog_assert( is_wp_error( $result ) && 'UPC_FEATURE_LABEL_MISSING' === $result->get_error_code(), 'empty label blocked' );

$tmp = tempnam( sys_get_temp_dir(), 'upc-feature-catalog-' );
file_put_contents( $tmp, json_encode( array(
    'schema_version' => '1',
    'project_key' => 'pferde-atelier',
    'feature_count' => 2,
    'features' => array(
        array( 'label' => 'A', 'fact_key' => 'same_key' ),
        array( 'label' => 'B', 'fact_key' => 'same_key' ),
    ),
) ) );
$bad = UPC_Feature_Key_Catalog::load( $tmp );
unlink( $tmp );
feature_catalog_assert( is_wp_error( $bad ) && 'UPC_FEATURE_KEY_DUPLICATE' === $bad->get_error_code(), 'duplicate fact key blocked' );

fwrite( STDOUT, "UPC_FEATURE_KEY_CATALOG_GESAMT_PASS\n" );
