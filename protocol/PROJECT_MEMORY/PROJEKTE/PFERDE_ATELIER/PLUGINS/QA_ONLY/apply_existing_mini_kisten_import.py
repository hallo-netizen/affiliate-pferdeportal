#!/usr/bin/env python3
"""Patch only existing PSTE_Mini_Workflow methods of the archived v22 ZIP.
No new runtime class, gate, database, external worker or changed K0/PSERC.
Produces QA files only, NEVER an installation approval.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import difflib
import sys

ROOT = Path("protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/PLUGINS")
SOURCE = ROOT / "INSTALLATIONS_PAKETE/PSTE-0.57.144.22-NUR-TEST.zip"
TARGET = "Portal SEO Topic Engine/includes/class-pste-mini-workflow.php"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/pste-kisten-qa")
OUT.mkdir(parents=True, exist_ok=True)

replacement = r"""    public static function validateResult(array $original,array $received,callable $loadCurrent): array {
        if(($original['contract']??'')!==self::CONTRACT||($received['contract']??'')!==self::CONTRACT||
            ($original['batch_id']??'')!==($received['batch_id']??''))throw new RuntimeException('PSTE_MINI_WRONG_BATCH');
        if(array_key_exists('title_governance',$received)&&$received['title_governance']!==self::titleGovernance())
            throw new RuntimeException('PSTE_MINI_TITLE_RULES_CHANGED');
        $before=$original['items']??null;$after=$received['items']??null;
        if(!is_array($before)||!is_array($after)||count($before)!==count($after)||!array_is_list($after))
            throw new RuntimeException('PSTE_MINI_ITEM_COUNT_CHANGED');

        // KISS: one transport owner. An individual broken answer goes into the existing
        // option's clarification box; other source-bound answers are not re-judged.
        $finished=[];$held=[];$stats=['JA'=>0,'NEIN'=>0,'VIELLEICHT'=>0,'titles'=>0,'clarification'=>0];
        foreach($before as $i=>$frozen){
            if(!is_array($frozen)||trim((string)($frozen['pool_key']??''))==='')
                throw new RuntimeException('PSTE_MINI_ORIGINAL_BATCH_INVALID');
            // The existing DB reader owns infrastructure failures. A database outage is
            // NOT an editorial issue and must still stop safe writes for this batch.
            $current=$loadCurrent((string)$frozen['pool_key']);
            try {
                $item=$after[$i]??null;
                if(!is_array($item))throw new RuntimeException('PSTE_MINI_ITEM_INVALID');
                $keys=array_keys($item);sort($keys);$allowed=array_keys($frozen);sort($allowed);
                if($keys!==$allowed)throw new RuntimeException('PSTE_MINI_ITEM_FIELDS_CHANGED');
                foreach(['id','pool_key','raw_query','source_sha256'] as $field){
                    if(!array_key_exists($field,$item)||$item[$field]!==$frozen[$field])
                        throw new RuntimeException('PSTE_MINI_SOURCE_CHANGED_'.$field);
                }
                $payload=is_array($current)?json_decode((string)($current['payload_json']??''),true):null;
                $raw=is_array($payload)?PSTE_Editorializer::sourceQuery($payload):'';
                $actual=hash('sha256',(int)($current['id']??0).'|'.(string)($current['pool_key']??'').'|'.$raw);
                if(!is_array($current)||!hash_equals((string)$frozen['source_sha256'],$actual))
                    throw new RuntimeException('PSTE_MINI_DATABASE_SOURCE_CHANGED');
                $decision=$item['decision']??null;
                if(!is_string($decision)||!in_array($decision,['JA','NEIN','VIELLEICHT'],true))
                    throw new RuntimeException('PSTE_MINI_DECISION_REQUIRED');
                $titles=$item['titles']??null;
                if(!is_array($titles)||!array_is_list($titles))throw new RuntimeException('PSTE_MINI_TITLES_INVALID');
                if($decision!=='JA'&&$titles)throw new RuntimeException('PSTE_MINI_NON_JA_HAS_TITLES');
                if($decision==='JA'&&!$titles)throw new RuntimeException('PSTE_MINI_JA_WITHOUT_TITLE');
                $clean=[];
                foreach($titles as $title){
                    if(!is_array($title)||count($title)!==2||!array_key_exists('intent',$title)||!array_key_exists('title',$title)||!is_string($title['intent'])||!is_string($title['title']))
                        throw new RuntimeException('PSTE_MINI_TITLE_SHAPE_INVALID');
                    $intent=trim($title['intent']);$text=trim($title['title']);
                    // Only transport format, not a second linguistic/SEO/title decision.
                    if($intent===''||$text===''||strlen($intent)>240||strlen($text)>300||
                        preg_match('/[<>\x00-\x1f\x7f]/u',$intent.$text))
                        throw new RuntimeException('PSTE_MINI_TITLE_TEXT_INVALID');
                    $clean[]=['intent'=>$intent,'title'=>$text];
                }
                $finished[(string)$frozen['pool_key']]=['raw_query'=>$frozen['raw_query'],
                    'decision'=>$decision,'titles'=>$clean,'batch_id'=>$original['batch_id'],
                    'recorded_utc'=>gmdate('c')];
                $stats[$decision]++;$stats['titles']+=count($clean);
            } catch(RuntimeException $e) {
                $code=(string)$e->getMessage();
                // Source/answer mismatch is isolated; unknown exceptions or broken
                // infrastructure are not silently reclassified as editorial outcomes.
                $itemErrors=['PSTE_MINI_ITEM_INVALID','PSTE_MINI_ITEM_FIELDS_CHANGED',
                    'PSTE_MINI_SOURCE_CHANGED_','PSTE_MINI_DATABASE_SOURCE_CHANGED',
                    'PSTE_MINI_DECISION_REQUIRED','PSTE_MINI_TITLES_INVALID',
                    'PSTE_MINI_NON_JA_HAS_TITLES','PSTE_MINI_JA_WITHOUT_TITLE',
                    'PSTE_MINI_TITLE_SHAPE_INVALID','PSTE_MINI_TITLE_TEXT_INVALID'];
                $known=false;
                foreach($itemErrors as $prefix)if(str_starts_with($code,$prefix)){$known=true;break;}
                if(!$known)throw $e;
                $held[]=['pool_key'=>(string)$frozen['pool_key'],
                    'reason_code'=>$code,'next_action'=>'RETRY_SAME_EXTERNAL_OWNER'];
                $stats['clarification']++;
            }
        }
        return ['completed'=>$finished,'clarification'=>$held,'stats'=>$stats];
    }

"""
def replace_method(source: str, method_name: str, after_marker: str, new_method: str) -> str:
    start = source.index("    public static function " + method_name + "(")
    stop = source.index(after_marker, start)
    return source[:start] + new_method + source[stop:]

with ZipFile(SOURCE) as zin:
    original = zin.read(TARGET).decode("utf-8")
    entries = [(info, zin.read(info.filename)) for info in zin.infolist()]

patched = replace_method(
    original, "validateResult",
    "    /** Replaces only title strings for an already imported batch",
    replacement
)
assert patched != original
# Preserve the pre-existing store; only add the KLAERUNG box, no new database.
a = "$state += ['completed'=>[], 'active'=>null, 'last_report'=>[]];"
b = "$state += ['completed'=>[], 'active'=>null, 'last_report'=>[], 'clarification'=>[]];"
assert patched.count(a) == 1
patched = patched.replace(a, b)

a = """            foreach($checked['completed'] as $key=>$value){
                if(isset($state['completed'][$key]))throw new RuntimeException('PSTE_MINI_KEY_ALREADY_COMPLETED');
                $state['completed'][$key]=$value;
            }
            $state['active']=null;
            $state['last_report']=['keywords'=>count($checked['completed']),'titles'=>(int)$checked['stats']['titles'],
                'breakdown'=>$checked['stats'],'recorded_utc'=>gmdate('c')];"""
b = """            foreach($checked['completed'] as $key=>$value){
                if(isset($state['completed'][$key]))throw new RuntimeException('PSTE_MINI_KEY_ALREADY_COMPLETED');
                $state['completed'][$key]=$value;
                unset($state['clarification'][$key]);
            }
            foreach($checked['clarification'] as $entry){
                $key=(string)($entry['pool_key']??'');
                if($key!=='')$state['clarification'][$key]=$entry;
            }
            $state['active']=null; // Clarification topics remain exportable: only completed is excluded.
            $state['last_report']=['keywords'=>count($checked['completed']),
                'clarification'=>count($checked['clarification']),
                'titles'=>(int)$checked['stats']['titles'],
                'breakdown'=>$checked['stats'],'recorded_utc'=>gmdate('c')];"""
assert patched.count(a) == 1
patched = patched.replace(a,b)

a = "'status'=>'STAGED_NOT_EDITORIALLY_APPROVED',"
b = "'status'=>'STAGED_NOT_EDITORIALLY_APPROVED',\n                'clarification'=>array_values((array)($state['clarification']??[])),"
assert patched.count(a) == 1
patched = patched.replace(a,b)
a = "echo '<p><strong>Erledigte Keywords:</strong> '"
b = "echo '<p><strong>Klärfälle:</strong> '.esc_html((string)count((array)($state['clarification']??[]))).'</p>';\n        echo '<p><strong>Erledigte Keywords:</strong> '"
assert patched.count(a) == 1
patched = patched.replace(a,b)
assert patched.count("function validateResult(") == 1

# The already existing PSERC active plan is a READ-ONLY SOURCE, not a second
# semantic reviewer. Add one method in the same MINI class; no extra worker/class.
pserc_reader = (ROOT / "QA_ONLY/pste_kisten_pserc_plan_method.inc").read_text(encoding="utf-8")
anchor = "    public static function renderManualBrief(): void {"
assert patched.count(anchor) == 1
patched = patched.replace(anchor, pserc_reader + anchor)
parkhaus_reader = (ROOT / "QA_ONLY/pste_kisten_complete_parkhaus_method.inc").read_text(encoding="utf-8")
assert patched.count(anchor) == 1
patched = patched.replace(anchor, parkhaus_reader + anchor)
# Export the current existing plan with the existing MINI batch; a missing/stale
# PSERC plan is visibly incomplete and must never count as editorial FREI.
old = """                $batch=self::createBatch($selected,'mini-'.gmdate('YmdHis').'-'.substr(bin2hex(random_bytes(6)),0,12));
                $state['active']=$batch;self::storeState($state); // A lost download is retryable."""
new = """                $batch=self::createBatch($selected,'mini-'.gmdate('YmdHis').'-'.substr(bin2hex(random_bytes(6)),0,12));
                $batch['parkhaus_snapshot']=self::readParkhausForMini();
                $batch['parkhaus_complete']=!empty($batch['parkhaus_snapshot']['complete']);
                $batch['parkhaus_sha256']=(string)($batch['parkhaus_snapshot']['sha256']??'');
                $state['active']=$batch;self::storeState($state); // A lost download is retryable."""
assert patched.count(old) == 1
patched = patched.replace(old,new)

(OUT/"class-pste-mini-workflow.php").write_text(patched,encoding="utf-8")
(OUT/"PSTE_KISTEN_EIN_IMPORT_OWNER_QA.diff").write_text(
    ''.join(difflib.unified_diff(original.splitlines(True),patched.splitlines(True),
        fromfile="a/includes/class-pste-mini-workflow.php",
        tofile="b/includes/class-pste-mini-workflow.php")),encoding="utf-8"
)
with ZipFile(OUT/"PSTE-KISTEN-GESAMT-QA-NICHT-INSTALLIEREN.zip","w") as zout:
    for info, data in entries:
        if info.filename == TARGET:
            zout.writestr(info,patched.encode("utf-8"))
        else:
            zout.writestr(info,data)
print("QA patch in original existing mini workflow; no new PHP class; no K0/PSERC files changed")
print("ZIP unchanged entry names",len(entries),"changed",TARGET)
print("No semantic quality or real WP end-to-end is proven by this stage")
