<?php
if ( ! defined( 'ABSPATH' ) ) {
    fwrite( STDERR, "ABSPATH_MISSING\n" );
    exit( 1 );
}

function upc_real_assert( $condition, $label ) {
    if ( ! $condition ) {
        fwrite( STDERR, "FAIL: {$label}\n" );
        exit( 1 );
    }
    fwrite( STDOUT, "PASS: {$label}\n" );
}

$fixture_path = __DIR__ . '/fixtures/pv-reg-001.json';
$fixture = json_decode( file_get_contents( $fixture_path ), true );
upc_real_assert( is_array( $fixture ), 'load PV-REG-001 fixture' );

$knowledge = upk_repository();
$compare   = upc_repository();
upc_real_assert( ! is_wp_error( $compare ), 'comparison repository available' );

$product_ids = array();

foreach ( $fixture['products'] as $product ) {
    $product_id = $knowledge->create_product(
        array(
            'manufacturer'             => $product['manufacturer'],
            'model_name'               => $product['model_name'],
            'product_group_key'        => $product['product_group_key'],
            'manufacturer_product_url' => $product['manufacturer_product_url'],
            'lifecycle_status'         => $product['lifecycle_status'],
            'last_verified_at'         => $product['last_verified_at'],
        )
    );
    upc_real_assert( is_int( $product_id ) && $product_id > 0, 'create real product ' . $product['manufacturer'] );

    foreach ( $product['facts'] as $fact ) {
        $fact_id = $knowledge->add_fact(
            UPK_Repository::SUBJECT_PRODUCT,
            $product_id,
            array(
                'fact_key'     => $fact['fact_key'],
                'fact_value'   => $fact['fact_value'],
                'source_url'   => $fact['source_url'],
                'source_type'  => $fact['source_type'],
                'verified_at'  => $fact['verified_at'],
                'fact_status'  => $fact['fact_status'],
            )
        );
        upc_real_assert( is_int( $fact_id ) && $fact_id > 0, 'store real fact ' . $product['manufacturer'] . ' / ' . $fact['fact_key'] );
    }

    $product_ids[] = $product_id;
}

$comparison_id = $compare->create_comparison(
    array(
        'comparison_key'     => strtolower( $fixture['dossier_id'] ),
        'comparison_type'    => $fixture['comparison_type'],
        'subject_ids'        => $product_ids,
        'working_title'      => $fixture['working_title'],
        'comparability_note' => $fixture['comparability_note'],
    )
);
upc_real_assert( is_int( $comparison_id ) && $comparison_id > 0, 'create PV-REG-001 comparison' );

$feature_count = $compare->set_features( $comparison_id, $fixture['features'] );
upc_real_assert( 14 === $feature_count, 'bind all 14 required dossier features' );

$valid = $compare->validate_required_facts( $comparison_id );
upc_real_assert( true === $valid, 'required facts complete including explicit NOT_IN_SOURCE / SOURCE_CONFLICT states' );

$bundle = $compare->get_comparison_bundle( $comparison_id );
upc_real_assert( ! is_wp_error( $bundle ), 'read full real dossier bundle' );
upc_real_assert( 14 === count( $bundle['feature_matrix'] ), 'read 14-row feature matrix' );
upc_real_assert( 2 === count( $bundle['items'] ), 'read two real products' );
upc_real_assert( 'WeatherBeeta' === $bundle['items'][0]['knowledge']['manufacturer'], 'preserve WeatherBeeta identity' );
upc_real_assert( 'LeMieux' === $bundle['items'][1]['knowledge']['manufacturer'], 'preserve LeMieux identity' );

$matrix_by_key = array();
foreach ( $bundle['feature_matrix'] as $row ) {
    $matrix_by_key[ $row['fact_key'] ] = $row;
}

$conflict = $matrix_by_key['waterproofness']['cells'][1]['facts'][0];
upc_real_assert( 'SOURCE_CONFLICT' === $conflict['fact_status'], 'preserve manufacturer source conflict' );
upc_real_assert(
    false !== strpos( $conflict['fact_value'], '10k/10.000 mm' )
    && false !== strpos( $conflict['fact_value'], '3.000 mm' ),
    'preserve conflicting values without smoothing'
);

$not_in_source_a = $matrix_by_key['care']['cells'][0]['facts'][0];
$not_in_source_b = $matrix_by_key['tail_flap']['cells'][1]['facts'][0];
upc_real_assert( 'NOT_IN_SOURCE' === $not_in_source_a['fact_status'], 'preserve WeatherBeeta NOT_IN_SOURCE' );
upc_real_assert( 'NOT_IN_SOURCE' === $not_in_source_b['fact_status'], 'preserve LeMieux NOT_IN_SOURCE' );

$writer_dossier = $compare->build_comparison_dossier( $comparison_id );
upc_real_assert( ! is_wp_error( $writer_dossier ), 'build deterministic writer dossier' );
upc_real_assert( 'READY_WITH_WARNINGS' === $writer_dossier['status'], 'real dossier exposes warnings instead of smoothing them' );
upc_real_assert( 14 === count( $writer_dossier['features'] ), 'writer dossier contains only 14 declared comparison features' );
upc_real_assert( 4 === count( $writer_dossier['warnings'] ), 'writer dossier exposes four real source warnings' );
$warning_codes = array_column( $writer_dossier['warnings'], 'code' );
upc_real_assert( in_array( 'SOURCE_CONFLICT', $warning_codes, true ), 'writer dossier exposes SOURCE_CONFLICT' );
upc_real_assert( in_array( 'NOT_IN_SOURCE', $warning_codes, true ), 'writer dossier exposes NOT_IN_SOURCE' );
upc_real_assert( ! isset( $writer_dossier['subjects'][0]['facts'] ), 'writer identity block does not duplicate product facts' );

$writer = upc_writer();
upc_real_assert( ! is_wp_error( $writer ), 'writer available' );

$without_rules = $writer->build_draft( $comparison_id );
upc_real_assert(
    is_wp_error( $without_rules ) && 'UPC_DECISION_RULE_MISSING' === $without_rules->get_error_code(),
    'writer blocks differing verified facts without approved decision rules'
);
$missing_rule_keys = $without_rules->get_error_data()['fact_keys'];
upc_real_assert( in_array( 'outer_material_denier', $missing_rule_keys, true ), 'missing denier rule exposed' );
upc_real_assert( in_array( 'neck_system', $missing_rule_keys, true ), 'missing neck-system rule exposed' );

$neutral_rule = function( $meaning, $need_fit = array(), $pros = array(), $cons = array() ) {
    return function( $feature ) use ( $meaning, $need_fit, $pros, $cons ) {
        return array(
            'meaning'          => $meaning,
            'need_fit'         => $need_fit,
            'pros_by_position' => $pros,
            'cons_by_position' => $cons,
        );
    };
};

$decision_rules = array(
    'fill_weight' => $neutral_rule(
        'Beide Hersteller beschreiben diese Modelle als ungefütterte 0-g-Decken. Aus dem Füllgewicht ergibt sich daher keine Präferenz.'
    ),
    'outer_material_denier' => $neutral_rule(
        'WeatherBeeta nennt 1200D, LeMieux 600D. Wer gezielt eine höhere angegebene Denierzahl priorisiert, findet sie beim WeatherBeeta-Modell; aus der Denierzahl allein wird keine pauschale Haltbarkeitswertung abgeleitet.',
        array(
            array(
                'need' => 'höhere angegebene Denierzahl',
                'positions' => array( 1 ),
                'reason' => 'WeatherBeeta nennt 1200D, LeMieux 600D.'
            ),
        )
    ),
    'breathability' => $neutral_rule(
        'Beide Hersteller nennen einen Wert von 3.000, verwenden aber unterschiedliche Bezeichnungen. Ohne identisch definierte Prüfmethode wird daraus keine belastbare Präferenz abgeleitet.'
    ),
    'neck_system' => $neutral_rule(
        'WeatherBeeta wird als Standard Neck beschrieben, LeMieux mit abnehmbarem Halsteil. Für Nutzer, die die Halsabdeckung je nach Bedarf verändern möchten, bietet die dokumentierte abnehmbare Lösung von LeMieux mehr direkte Flexibilität.',
        array(
            array(
                'need' => 'veränderbare Halsabdeckung',
                'positions' => array( 2 ),
                'reason' => 'LeMieux nennt ausdrücklich ein abnehmbares Halsteil.'
            ),
        ),
        array( 2 => array( 'Abnehmbares Halsteil dokumentiert.' ) )
    ),
    'liner_compatibility' => $neutral_rule(
        'Für beide Modelle ist eine Liner-Kompatibilität dokumentiert. Aus diesem Merkmal ergibt sich deshalb keine klare Präferenz.'
    ),
    'front_closure' => $neutral_rule(
        'Die Verschlusssysteme unterscheiden sich konstruktiv. WeatherBeeta nennt einen verstellbaren Quick-Clip-Verschluss mit Touch Tape, LeMieux einen 45° angewinkelten T-Bar-Verschluss. Welche Bedienart besser passt, ist eine Nutzerpräferenz und wird nicht pauschal bewertet.'
    ),
    'movement_cut' => $neutral_rule(
        'Die Hersteller beschreiben unterschiedliche Schnittkonstruktionen. Aus den vorliegenden Herstellerangaben allein lässt sich nicht belastbar ableiten, welche Konstruktion für ein konkretes Pferd besser passt.'
    ),
    'cross_surcingles' => $neutral_rule(
        'WeatherBeeta nennt zwei niedrige Kreuzgurte, LeMieux allgemein Kreuzgurte. Da die LeMieux-Quelle hier keine gleich detaillierte Mengenangabe liefert, wird kein Vorteil abgeleitet.'
    ),
    'leg_straps_tail_cord' => $neutral_rule(
        'WeatherBeeta dokumentiert verstellbare, abnehmbare Beingurte; LeMieux elastische Beingurte plus PVC-beschichteten Fillet Strap. Die passende Lösung hängt davon ab, welches Befestigungskonzept gewünscht ist.',
        array(
            array(
                'need' => 'verstellbare und abnehmbare Beingurte',
                'positions' => array( 1 ),
                'reason' => 'WeatherBeeta dokumentiert diese Eigenschaft ausdrücklich.'
            ),
            array(
                'need' => 'elastische Beingurte plus Fillet Strap',
                'positions' => array( 2 ),
                'reason' => 'LeMieux dokumentiert diese Kombination ausdrücklich.'
            ),
        )
    ),
    'sizes' => $neutral_rule(
        'Die Hersteller geben die Größen in unterschiedlichen Systemen an. Ohne zusätzliche normierte Größenabbildung wird daraus keine Reichweiten- oder Passformpräferenz abgeleitet.'
    ),
);

$draft = $writer->build_draft( $comparison_id, $decision_rules );
upc_real_assert( ! is_wp_error( $draft ), 'build real article draft with approved decision rules' );
upc_real_assert( 'DRAFT_READY_FOR_REVIEW' === $draft['status'], 'writer returns review-only draft status' );
upc_real_assert( 0 === $draft['external_link_count'], 'writer emits no external links' );
upc_real_assert( false !== strpos( $draft['html'], '<h2>Vergleich auf einen Blick</h2>' ), 'comparison table placed high in draft' );
upc_real_assert( false !== strpos( $draft['html'], 'Bedeutung für die Entscheidung' ), 'table contains decision meaning column' );
upc_real_assert( false !== strpos( $draft['html'], 'Quellenkonflikt:' ), 'SOURCE_CONFLICT visible in article table' );
upc_real_assert( false !== strpos( $draft['html'], 'In der verwendeten Herstellerquelle nicht angegeben' ), 'NOT_IN_SOURCE visible in article table' );
upc_real_assert( false !== strpos( $draft['html'], '<h2>Vor- und Nachteile im direkten Vergleich</h2>' ), 'pros-cons section present' );
upc_real_assert( false !== strpos( $draft['html'], '<h2>Welches Produkt passt zu welchem Bedarf?</h2>' ), 'need-fit section present' );
upc_real_assert( false !== strpos( $draft['html'], 'Es gibt keinen pauschalen Sieger.' ), 'no universal winner in conclusion' );
upc_real_assert( false === strpos( $draft['html'], 'href=' ), 'article body contains no links' );

$missing_id = $compare->create_comparison(
    array(
        'comparison_key'     => 'pv-reg-001-missing-test',
        'comparison_type'    => 'PRODUCT',
        'subject_ids'        => $product_ids,
        'working_title'      => 'Missing required fact negative test',
        'comparability_note' => $fixture['comparability_note'],
    )
);
upc_real_assert( is_wp_error( $missing_id ) && 'UPC_DUPLICATE_COMPARISON' === $missing_id->get_error_code(), 'block duplicate real pair under another key' );

$second_a = $knowledge->create_product(
    array(
        'manufacturer'             => 'Fixture Maker A',
        'model_name'               => 'Missing A',
        'product_group_key'        => 'fixture-missing',
        'manufacturer_product_url' => 'https://manufacturer.example/missing-a',
        'lifecycle_status'         => 'ACTIVE',
    )
);
$second_b = $knowledge->create_product(
    array(
        'manufacturer'             => 'Fixture Maker B',
        'model_name'               => 'Missing B',
        'product_group_key'        => 'fixture-missing',
        'manufacturer_product_url' => 'https://manufacturer.example/missing-b',
        'lifecycle_status'         => 'ACTIVE',
    )
);
$missing_comparison = $compare->create_comparison(
    array(
        'comparison_key'  => 'missing-required-fact',
        'comparison_type' => 'PRODUCT',
        'subject_ids'     => array( $second_a, $second_b ),
    )
);
upc_real_assert( is_int( $missing_comparison ) && $missing_comparison > 0, 'create negative missing-fact comparison' );
$compare->set_features(
    $missing_comparison,
    array(
        array(
            'fact_key' => 'required_missing',
            'label'    => 'Required missing',
            'required' => true,
        ),
    )
);
$missing_validation = $compare->validate_required_facts( $missing_comparison );
upc_real_assert(
    is_wp_error( $missing_validation ) && 'UPC_REQUIRED_FACT_MISSING' === $missing_validation->get_error_code(),
    'block truly missing required fact'
);

$missing_dossier = $compare->build_comparison_dossier( $missing_comparison );
upc_real_assert(
    is_wp_error( $missing_dossier ) && 'UPC_REQUIRED_FACT_MISSING' === $missing_dossier->get_error_code(),
    'writer dossier fails closed on missing required fact'
);

fwrite( STDOUT, "UPC_REAL_DOSSIER_PV_REG_001_PASS\n" );
