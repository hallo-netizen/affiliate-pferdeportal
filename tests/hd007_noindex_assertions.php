<?php
// Execute the actual patched class against the original 862 records, with minimal WP shims.
define('ABSPATH', __DIR__);
function sanitize_title($s) {
    $s = iconv('UTF-8','ASCII//TRANSLIT//IGNORE',(string)$s);
    $s = strtolower($s);
    return trim((string)preg_replace('/[^a-z0-9]+/','-',$s),'-');
}
final class HD_Hobbyregister_Core_Stable127 {
    private static $rows = null;
    public static function records() {
        if (self::$rows === null) {
            $path = __DIR__ . '/../dist/unpacked/hd-hobbyregister-core/data/hobby-register.json';
            $data = json_decode(file_get_contents($path),true,512,JSON_THROW_ON_ERROR);
            self::$rows = $data['records'];
        }
        return self::$rows;
    }
}
require __DIR__ . '/../dist/unpacked/hd-hobbyregister-core/includes/class-hd-hobbyregister-frontend.php';
function check($value,$description) {
    if (!$value) { fwrite(STDERR,"FAIL: $description\n"); exit(1); }
    echo "PASS: $description\n";
}
function meta_for($path) {
    $_SERVER['REQUEST_URI']=$path;
    ob_start();
    HD_Hobbyregister_Frontend_Stable127::head_meta();
    return ob_get_clean();
}
check(str_contains(meta_for('/hobbyregister/3d-druck/'),'noindex,follow'),'CORE 3D-Druck: noindex');
check(str_contains(meta_for('/hobbyregister/airbrush/'),'noindex,follow'),'CORE Airbrush: noindex');
check(str_contains(meta_for('/hobbyregister/alte-computer/'),'noindex,follow'),'CORE alte Computer: noindex');
check(meta_for('/hobbyregister/air-dry-clay/')==='','NICHE Air-Dry Clay: no plugin noindex');
check(meta_for('/hobbyregister/alabasterschnitzen/')==='','NICHE Alabasterschnitzen: no plugin noindex');
check(meta_for('/hobbyregister/algenkultur/')==='','NICHE Algenkultur: no plugin noindex');
check(meta_for('/hobbyregister/nicht-vorhanden/')==='','UNKNOWN: no plugin noindex');
check(meta_for('/hobbyregister/')==='','REGISTER index: no plugin noindex');
check(meta_for('/magazin/')==='','UNRELATED page: unchanged');
$method=new ReflectionMethod(HD_Hobbyregister_Frontend_Stable127::class,'profile_has_core_owner');
check($method->invoke(null,['source_identity'=>['current_terminal_hobby_page'=>false,'target_node_id'=>'core:entity:123']])===false,'flag false despite target');
check($method->invoke(null,['source_identity'=>['current_terminal_hobby_page'=>true,'target_node_id'=>null]])===false,'flag true without target');
check($method->invoke(null,['source_identity'=>['current_terminal_hobby_page'=>'true','target_node_id'=>'core:entity:123']])===false,'nonboolean flag excluded');
check($method->invoke(null,['source_identity'=>['current_terminal_hobby_page'=>true,'target_node_id'=>'core:entity:123']])===true,'valid CORE owner positive');
check($method->invoke(null,null)===false,'invalid record excluded');
$yes=0;$no=0;$seen=[];
foreach(HD_Hobbyregister_Core_Stable127::records() as $row) {
    $src=$row['source_identity']??[];
    $expected=(($src['current_terminal_hobby_page']??false)===true &&
        is_string($src['target_node_id']??null) && $src['target_node_id']!=='');
    $actual=$method->invoke(null,$row);
    check($expected===$actual,'ownership record '.$row['registry_id']);
    if($actual){$yes++;}else{$no++;}
    $slug=sanitize_title($row['canonical_name']);
    if(isset($seen[$slug]) && $seen[$slug]!==$row['registry_id']) {
        fwrite(STDERR,"WARN: preexisting slug collision $slug\n");
    }
    $seen[$slug]=$row['registry_id'];
}
check($yes>0 && $no>0 && $yes+$no===862,'all 862 registry IDs covered');
echo "TOTAL: 862 tested, CORE noindex $yes, register indexable $no\n";
echo "PHP RUNTIME SIMULATION PASS\n";
