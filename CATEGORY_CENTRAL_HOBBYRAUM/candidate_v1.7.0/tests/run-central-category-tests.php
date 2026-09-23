<?php
declare(strict_types=1);
define('ABSPATH', __DIR__);
define('APKW_MASTER_CONTRACT_ID', 'ALLGEMEINGUELTIGER_KATEGORIE_MASTER_016_WORKFLOW_HARDLOCK');

$GLOBALS['apkw_test_options'] = [];
function get_option($name, $default=false){ return array_key_exists($name,$GLOBALS['apkw_test_options']) ? $GLOBALS['apkw_test_options'][$name] : $default; }
function add_option($name,$value,$deprecated='',$autoload='yes'){ if(array_key_exists($name,$GLOBALS['apkw_test_options'])) return false; $GLOBALS['apkw_test_options'][$name]=$value; return true; }
function update_option($name,$value,$autoload=null){ $GLOBALS['apkw_test_options'][$name]=$value; return true; }
function wp_json_encode($value,$flags=0,$depth=512){ return json_encode($value,$flags,$depth); }

final class APKW_Validator {
    public static function validate(array $package): array {
        if (!empty($package['force_invalid'])) {
            return ['valid'=>false,'errors'=>[['code'=>'FORCED_INVALID']],'nodes'=>[]];
        }
        return ['valid'=>true,'errors'=>[],'nodes'=>$package['nodes'] ?? []];
    }
}

require_once __DIR__.'/../includes/class-apkw-central-category-registry.php';

function fail_test(string $m): void { fwrite(STDERR, "FAIL: $m\n"); exit(1); }
function ok(bool $v,string $m): void { if(!$v) fail_test($m); echo "PASS: $m\n"; }
function throws(callable $fn,string $needle,string $m): void {
    try { $fn(); } catch(Throwable $e) { ok(str_contains($e->getMessage(),$needle),$m.' ['.$e->getMessage().']'); return; }
    fail_test($m.' (no exception)');
}
function node(string $id,string $name,string $slug,string $status='FINAL_APPROVED'): array {
    return ['concept_id'=>$id,'name'=>$name,'slug'=>$slug,'block'=>'content','level'=>1,'status'=>$status,'active'=>true];
}
function pkg(array $nodes): array {
    return ['mode'=>'FINAL_APPROVED','master_contract_id'=>APKW_MASTER_CONTRACT_ID,'package_id'=>'pkg-'.count($nodes),'nodes'=>$nodes];
}

$s0=APKW_Central_Category_Registry::status();
ok($s0['generation']===0,'empty registry generation 0');
ok($s0['node_count']===0,'empty registry has zero nodes');

$p1=pkg([node('c2','Trensen','trensen'),node('c1','Sättel','saettel')]);
$pr1=APKW_Central_Category_Registry::preview_package($p1);
ok($pr1['snapshot']['generation']===1,'first preview generation 1');
ok($pr1['diff']['added']===['c1','c2'],'first preview exact added ids');
$r1=APKW_Central_Category_Registry::commit_package($p1,$pr1['expected_previous_sha256'],'Initiale zentrale Übernahme',false,7);
ok($r1['status']==='PASS_COMMITTED','first commit pass');
ok(APKW_Central_Category_Registry::status()['generation']===1,'first commit generation stored');
ok(APKW_Central_Category_Registry::fallback()===null,'first commit has no fallback yet');

$p1_reordered=['nodes'=>[array_reverse(node('c1','Sättel','saettel'),true),array_reverse(node('c2','Trensen','trensen'),true)],'package_id'=>'pkg-2','master_contract_id'=>APKW_MASTER_CONTRACT_ID,'mode'=>'FINAL_APPROVED'];
$pr_same=APKW_Central_Category_Registry::preview_package($p1_reordered);
ok($pr_same['diff']['added']===[] && $pr_same['diff']['removed']===[] && $pr_same['diff']['changed']===[],'deterministic node hash independent of key/order');

$p2=pkg([node('c1','Pferdesättel','pferdesaettel'),node('c3','Paddockbau','paddockbau')]);
$pr2=APKW_Central_Category_Registry::preview_package($p2);
ok($pr2['diff']['added']===['c3'],'second preview identifies add');
ok($pr2['diff']['removed']===['c2'],'second preview identifies delete');
ok($pr2['diff']['changed']===['c1'],'second preview identifies change');
throws(fn()=>APKW_Central_Category_Registry::commit_package($p2,$pr2['expected_previous_sha256'],'Delete without confirm',false,7),'DELETION_CONFIRMATION_REQUIRED','delete blocked without explicit confirmation');
throws(fn()=>APKW_Central_Category_Registry::commit_package($p2,str_repeat('f',64),'stale',true,7),'STALE_PREVIEW','stale preview blocked');

$r2=APKW_Central_Category_Registry::commit_package($p2,$pr2['expected_previous_sha256'],'Neue Struktur inklusive Entfernung',true,7);
ok($r2['snapshot']['generation']===2,'second commit generation 2');
ok(APKW_Central_Category_Registry::fallback()['generation']===1,'fallback preserves generation 1');
ok(count(APKW_Central_Category_Registry::change_log())===2,'two changes logged');

$hash1=$r1['snapshot']['category_set_sha256'];
$rb=APKW_Central_Category_Registry::rollback_to_fallback('Rollback-Test',7);
ok($rb['status']==='PASS_ROLLED_BACK','rollback pass');
ok($rb['snapshot']['generation']===3,'rollback creates new generation');
ok($rb['snapshot']['category_set_sha256']===$hash1,'rollback restores previous category set exactly');
ok(count(APKW_Central_Category_Registry::change_log())===3,'rollback logged');

$bad=$p1; $bad['mode']='READ_ONLY_PREVIEW';
throws(fn()=>APKW_Central_Category_Registry::preview_package($bad),'mode=FINAL_APPROVED','non-final package blocked');
$invalid=$p1; $invalid['force_invalid']=true;
throws(fn()=>APKW_Central_Category_Registry::preview_package($invalid),'FORCED_INVALID','validator failure blocks');

echo "CENTRAL_CATEGORY_REGISTRY_POSITIVE_NEGATIVE_ROLLBACK_PASS\n";
