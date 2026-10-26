<?php
declare(strict_types=1);

define('ABSPATH', __DIR__ . '/');

final class WP_Error {
    private string $code;
    private string $message;
    public function __construct($code = '', $message = '') {
        $this->code = (string)$code;
        $this->message = (string)$message;
    }
    public function get_error_code(): string { return $this->code; }
    public function get_error_message(): string { return $this->message; }
}
function is_wp_error($value): bool { return $value instanceof WP_Error; }
function wp_strip_all_tags($value): string { return strip_tags((string)$value); }
function remove_accents($value): string { return (string)$value; }
function sanitize_text_field($value): string { return trim(strip_tags((string)$value)); }
function sanitize_title($value): string {
    $value = strtolower(trim((string)$value));
    $value = preg_replace('/[^a-z0-9]+/', '-', $value);
    return trim((string)$value, '-');
}
function sanitize_key($value): string {
    $value = strtolower((string)$value);
    return preg_replace('/[^a-z0-9_\-]/', '', $value) ?? '';
}
function absint($value): int { return abs((int)$value); }

$GLOBALS['hd_gate_ready'] = true;
$GLOBALS['hd_gate_snapshot'] = array();
$GLOBALS['hd_gate_revision'] = 'HD-GATE4-REV';
function hd_category_registry_ready(): bool { return !empty($GLOBALS['hd_gate_ready']); }
function hd_category_registry_snapshot() { return $GLOBALS['hd_gate_snapshot']; }
function hd_category_registry_revision(): string { return (string)$GLOBALS['hd_gate_revision']; }

$pluginRoot = dirname(__DIR__) . '/WORKSOURCE/affiliate-portal-router';
require_once $pluginRoot . '/includes/class-hdar-hobby-depot-source.php';
require_once $pluginRoot . '/includes/trait-ppar-ebay.php';
require_once $pluginRoot . '/includes/trait-ppar-idealo.php';

final class HDAR_Gate4_Ebay {
    use PPAR_Ebay_Trait;
    public function catalog() { return $this->ebay_portal_catalog(); }
}
final class HDAR_Gate4_Idealo {
    use PPAR_Idealo_Trait;
    public function catalog() { return $this->idealo_portal_supply_catalog(); }
}

function fail_gate(string $message): void {
    fwrite(STDERR, "FAIL: {$message}\n");
    exit(1);
}
function ok_gate(string $message): void {
    echo "PASS: {$message}\n";
}
function assert_true($condition, string $message): void {
    if (!$condition) { fail_gate($message); }
}
function assert_error_code($value, string $code, string $message): void {
    assert_true(is_wp_error($value), $message . ' (kein WP_Error)');
    assert_true($value->get_error_code() === $code, $message . ' (Code=' . $value->get_error_code() . ')');
}
function build_snapshot(int $worldCount = 8, int $hobbiesPerWorld = 40): array {
    $nodes = array();
    for ($w = 1; $w <= $worldCount; $w++) {
        $worldId = 'core:world:w' . $w;
        $nodes[] = array(
            'node_id' => $worldId,
            'pillar' => 'core',
            'status' => 'active',
            'object_type' => 'page',
            'parent_id' => '',
            'slug' => 'welt-' . $w,
            'display_name' => 'Welt ' . $w,
        );
        for ($h = 1; $h <= $hobbiesPerWorld; $h++) {
            $hobbyId = 'core:hobby:w' . $w . '-h' . $h;
            $slug = 'hobby-' . $w . '-' . $h;
            $nodes[] = array(
                'node_id' => $hobbyId,
                'pillar' => 'core',
                'status' => 'active',
                'object_type' => 'page',
                'parent_id' => $worldId,
                'slug' => $slug,
                'display_name' => 'Hobby ' . $w . '-' . $h,
            );
            $nodes[] = array(
                'node_id' => 'core:category:w' . $w . '-h' . $h,
                'pillar' => 'core',
                'status' => 'active',
                'object_type' => 'category',
                'parent_id' => $hobbyId,
                'slug' => $slug . '-kategorie',
                'display_name' => 'Kategorie ' . $w . '-' . $h,
            );
        }
    }
    return array('revision' => 'HD-GATE4-REV', 'nodes' => $nodes);
}
function set_snapshot($snapshot, bool $ready = true): void {
    $GLOBALS['hd_gate_snapshot'] = $snapshot;
    $GLOBALS['hd_gate_ready'] = $ready;
}

$scenario = $argv[1] ?? 'positive';

switch ($scenario) {
    case 'positive':
        set_snapshot(build_snapshot(8, 40), true);
        $catalog = HDAR_Hobby_Depot_Source::catalog();
        assert_true(is_array($catalog), 'gültiger HD-004-Snapshot muss Katalog liefern');
        assert_true(($catalog['counts']['worlds'] ?? 0) === 8, 'exakt 8 Welten');
        assert_true(($catalog['counts']['product_pages'] ?? 0) === 320, '320 Produkt-/Hobbyziele');
        assert_true(($catalog['counts']['article_categories'] ?? 0) === 320, '320 Artikelkategorien');
        assert_true(($catalog['counts']['business_concepts'] ?? 0) === 320, '320 Recherchekonzepte');
        assert_true(($catalog['source_revision'] ?? '') === 'HD-GATE4-REV', 'Registry-Revision muss übernommen werden');
        $ebay = (new HDAR_Gate4_Ebay())->catalog();
        assert_true(is_array($ebay) && !empty($ebay['search_rules']) && count((array)$ebay['private_bucket_profiles']) === 8, 'eBay muss gültigen Hobby-Depot-Katalog übernehmen');
        $idealo = (new HDAR_Gate4_Idealo())->catalog();
        assert_true(is_array($idealo) && count((array)($idealo['_idealo_required_ids'] ?? array())) === 320, 'idealo muss Hobby-Depot-Konzepte übernehmen');
        ok_gate('positive HD-004 -> HD-009 -> eBay/idealo');
        break;

    case 'registry_unavailable':
        set_snapshot(array(), false);
        assert_error_code(HDAR_Hobby_Depot_Source::catalog(), 'hdar_category_registry_unavailable', 'fehlende Registry muss fail-closed sein');
        ok_gate('Registry unavailable fail-closed');
        break;

    case 'snapshot_invalid':
        set_snapshot(array('revision' => 'X', 'nodes' => array()), true);
        assert_error_code(HDAR_Hobby_Depot_Source::catalog(), 'hdar_category_snapshot_invalid', 'leerer Snapshot muss fail-closed sein');
        ok_gate('invalid snapshot fail-closed');
        break;

    case 'world_count':
        set_snapshot(build_snapshot(7, 45), true);
        assert_error_code(HDAR_Hobby_Depot_Source::catalog(), 'hdar_world_count_invalid', '!=8 Welten müssen fail-closed sein');
        ok_gate('world count fail-closed');
        break;

    case 'few_hobbies':
        set_snapshot(build_snapshot(8, 20), true);
        assert_error_code(HDAR_Hobby_Depot_Source::catalog(), 'hdar_hobby_target_count_implausible', '<300 Hobbyziele müssen fail-closed sein');
        ok_gate('too few hobby targets fail-closed');
        break;

    case 'ebay_failclosed':
        set_snapshot(array(), false);
        assert_error_code((new HDAR_Gate4_Ebay())->catalog(), 'hdar_category_registry_unavailable', 'eBay muss Registry-Fehler propagieren');
        ok_gate('eBay fail-closed');
        break;

    case 'idealo_failclosed':
        set_snapshot(array(), false);
        assert_error_code((new HDAR_Gate4_Idealo())->catalog(), 'hdar_category_registry_unavailable', 'idealo muss Registry-Fehler propagieren');
        ok_gate('idealo fail-closed');
        break;

    case 'legacy_regression':
        foreach (array(
            'assets/ebay-portal-catalog-v2.json',
            'assets/portal-structure-v279.json',
            'recovery/aff043-historical-product-state-20260915.json',
        ) as $legacy) {
            assert_true(!file_exists($pluginRoot . '/' . $legacy), 'Fremdprojektdatei darf nicht zurückkehren: ' . $legacy);
        }
        $blocked = '/(Pferdeatelier|Pferde-Atelier|pferdeatelier|pferde-atelier|Horse|Equine|Pony|\\bFohlen\\b|Hengst|Stute|Wallach|Pferderass|Rasse|Breed|Sattel|Schabrack|Huf|Trense|Zaum|Halfter)/i';
        $iterator = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($pluginRoot, FilesystemIterator::SKIP_DOTS));
        foreach ($iterator as $file) {
            if (!$file->isFile() || !preg_match('/\.(php|js|css)$/i', $file->getFilename())) { continue; }
            $body = file_get_contents($file->getPathname());
            if (preg_match($blocked, (string)$body, $m)) {
                fail_gate('Pferde-/Fremdprojektmarker in ' . $file->getPathname() . ': ' . $m[0]);
            }
        }
        ok_gate('legacy/fremdproject regression');
        break;

    case 'amazon_regression':
        $registry = file_get_contents($pluginRoot . '/includes/trait-ppar-provider-registry.php');
        $main = file_get_contents($pluginRoot . '/hobby-depot-affiliate-router.php');
        assert_true(preg_match("/'amazon'\s*=>\s*array\s*\([^)]*'state'\s*=>\s*'prepared'/s", (string)$registry) === 1, 'Amazon muss prepared bleiben');
        assert_true(strpos((string)$main, 'HDAR_Amazon') === false, 'kein aktiver Amazon-Adapter im Bootstrap');
        assert_true(!file_exists($pluginRoot . '/includes/trait-hdar-amazon-creators.php'), 'kein erfundener Amazon-Adapter');
        ok_gate('Amazon remains prepared/inactive');
        break;

    default:
        fail_gate('unbekanntes Szenario ' . $scenario);
}
