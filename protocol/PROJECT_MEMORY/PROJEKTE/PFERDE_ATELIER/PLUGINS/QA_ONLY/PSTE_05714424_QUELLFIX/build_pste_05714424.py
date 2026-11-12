from pathlib import Path
import shutil
base=Path('/mnt/data/work_pste_exportfix/Portal SEO Topic Engine')
new=Path('/mnt/data/work_pste_05714424/Portal SEO Topic Engine')
if new.parent.exists():shutil.rmtree(new.parent)
shutil.copytree(base,new)
snap=new/'includes/class-pste-snapshot.php'
s=snap.read_text()
needle='    private static function extractEditorialPlanItems(array $external): array {'
assert s.count(needle)==1
method='''    /**
     * Read-only MINI parkhouse inventory. Keep every old planning row even when
     * its title has already become unreadable. Unresolved records are exported
     * for source repair, NEVER treated as confirmed complete or automatically free.
     * The strict editorialPlan() used by other PSTE workflows stays unchanged.
     */
    public static function editorialPlanForParkhaus(): array {
        $external=apply_filters('pste_read_only_editorial_plan_snapshot',null);
        if(!is_array($external))$external=get_option(PSTE_OPTION_EDITORIAL_PLAN_IMPORT,null);
        if(!is_array($external))return ['contract'=>'PSTE_EDITORIAL_PLAN_SNAPSHOT_V1',
            'status'=>'NOT_AVAILABLE','sha256'=>'NOT_AVAILABLE','items'=>[],
            'unresolved_count'=>0,'unresolved_indices'=>[]];
        $input=null;
        if(isset($external['items'])&&is_array($external['items']))$input=$external['items'];
        elseif(isset($external['articles'])&&is_array($external['articles']))$input=$external['articles'];
        elseif(isset($external['next_textmachine_metadata_batch']['items'])
            &&is_array($external['next_textmachine_metadata_batch']['items']))
            $input=$external['next_textmachine_metadata_batch']['items'];
        elseif(array_is_list($external))$input=$external;
        if($input===null||$input===[])return ['contract'=>'PSTE_EDITORIAL_PLAN_SNAPSHOT_V1',
            'status'=>'NOT_AVAILABLE','sha256'=>'NOT_AVAILABLE','items'=>[],
            'unresolved_count'=>0,'unresolved_indices'=>[]];
        $structure=self::structure();$clean=[];$unresolved=[];
        foreach(array_values($input) as $index=>$row){
            try {
                if(!is_array($row))throw new RuntimeException('PSTE_EDITORIAL_PLAN_ROW_INVALID');
                $normalized=self::normalizeEditorialPlanItemsAgainstStructure([$row],$structure);
                if(count($normalized)!==1||!is_string($normalized[0]['title']??null)
                    ||trim($normalized[0]['title'])==='')
                    throw new RuntimeException('PSTE_EDITORIAL_PLAN_ROW_UNRESOLVED');
                $clean[]=$normalized[0];
            }catch(Throwable $e){
                $unresolved[]=$index;
                // Preserve the actual persisted nested title value (rather than
                // invented titles) and field names, without mutating the WP option.
                $sourceFields=[];
                if(is_array($row))foreach(['title','production_title','article_title',
                    'primary_longtail_query','seo_title','headline'] as $field){
                    if(array_key_exists($field,$row))$sourceFields[$field]=$row[$field];
                }
                $rawJson=wp_json_encode($row,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
                if(!is_string($rawJson))throw new RuntimeException('PSTE_EDITORIAL_PLAN_ROW_ENCODING_FAILED');
                $clean[]=['status'=>'UNRESOLVED_SOURCE_TITLE','title'=>'',
                    'source_index'=>$index,'source_reference'=>'EDITORIAL_PLAN:'.$index,
                    'raw_record_sha256'=>hash('sha256',$rawJson),
                    'raw_field_names'=>is_array($row)?array_keys($row):[],
                    'raw_title_fields'=>$sourceFields,'diagnostic_reason'=>'EDITORIAL_PLAN_ORIGINAL_TITLE_NOT_READABLE'];
            }
        }
        $snapshot=self::bind('PSTE_EDITORIAL_PLAN_SNAPSHOT_V1',$clean);
        $snapshot['status']=$unresolved?'QUARANTINED':'AVAILABLE';
        $snapshot['unresolved_count']=count($unresolved);
        $snapshot['unresolved_indices']=$unresolved;
        return $snapshot;
    }

'''
s=s.replace(needle,method+needle)
snap.write_text(s)

mini=new/'includes/class-pste-mini-workflow.php';m=mini.read_text()
old='''            // The optional imported editorial plan is already a read-only PSTE source.
            $editorial=PSTE_Snapshot::editorialPlan();
            $result['sources']['EDITORIAL_PLAN']=['status'=>(string)($editorial['status']??'NOT_AVAILABLE'),
                'sha256'=>(string)($editorial['sha256']??'NOT_AVAILABLE'),
                'item_count'=>count((array)($editorial['items']??[]))];
            foreach((array)($editorial['items']??[]) as $row){
                if(!is_array($row)||!is_string($row['title']??null)
                    ||trim($row['title'])===''||trim($row['title'])==='Array')
                    throw new RuntimeException('EDITORIAL_PLAN_UNRESOLVED_ARTICLE_TITLE');
                $result['items'][]=['source'=>'EDITORIAL_PLAN','status'=>(string)($row['status']??'PLANNED'),
                    'title'=>$row['title'],'target_keyword'=>(string)($row['target_keyword']??''),
                    'plan_slot'=>(string)($row['plan_slot']??''),'article_type'=>(string)($row['article_type']??''),
                    'category'=>(string)($row['category_name']??'')];}
'''
assert m.count(old)==1
replacement='''            // Even corrupt historical editorial rows belong in the single
            // read-only export. Missing titles must not hide PSERC/PPM679 plans.
            $sourceProblems=[];
            $editorial=PSTE_Snapshot::editorialPlanForParkhaus();
            $editorialUnknown=(int)($editorial['unresolved_count']??0);
            $result['sources']['EDITORIAL_PLAN']=[
                'complete'=>$editorialUnknown===0,
                'status'=>(string)($editorial['status']??'NOT_AVAILABLE'),
                'sha256'=>(string)($editorial['sha256']??'NOT_AVAILABLE'),
                'item_count'=>count((array)($editorial['items']??[])),
                'unresolved_count'=>$editorialUnknown,
                'unresolved_indices'=>(array)($editorial['unresolved_indices']??[])];
            foreach((array)($editorial['items']??[]) as $row){
                if(!is_array($row))throw new RuntimeException('EDITORIAL_PLAN_ROW_NOT_ARRAY');
                if(($row['status']??'')==='UNRESOLVED_SOURCE_TITLE'){
                    $result['items'][]=array_merge(['source'=>'EDITORIAL_PLAN'], $row);
                    continue;
                }
                if(!is_string($row['title']??null)
                    ||trim($row['title'])===''||trim($row['title'])==='Array')
                    throw new RuntimeException('EDITORIAL_PLAN_ROW_INCONSISTENT');
                $result['items'][]=['source'=>'EDITORIAL_PLAN','status'=>(string)($row['status']??'PLANNED'),
                    'title'=>$row['title'],'target_keyword'=>(string)($row['target_keyword']??''),
                    'plan_slot'=>(string)($row['plan_slot']??''),'article_type'=>(string)($row['article_type']??''),
                    'category'=>(string)($row['category_name']??'')];
            }
            if($editorialUnknown>0)$sourceProblems[]='EDITORIAL_PLAN_UNRESOLVED:'.$editorialUnknown;
'''
m=m.replace(old,replacement)
old='''            foreach($runtimeItems as $itemId=>$item){'''
assert m.count(old)==1
m=m.replace(old,"            $runtimeMissingTitles=[];\n"+old)
old='''                if($title===''||$title==='Array')
                    throw new RuntimeException('PPM679_RUNTIME_ARTICLE_TITLE_UNRESOLVED_POST_'.$postId);
'''
assert m.count(old)==1
m=m.replace(old,'''                // Keep all occupied article identities, including unresolvable
                // post references, visible in the export, but never declare FREI.
                $titleUnresolved=$title===''||$title==='Array';
                if($titleUnresolved){$title='';$runtimeMissingTitles[]=$postId;}
''')
old="""                    'target_keyword'=>$targetKeyword,
                    'title'=>$title];
"""
assert m.count(old)==1
m=m.replace(old,"""                    'target_keyword'=>$targetKeyword,
                    'title'=>$title,
                    'title_status'=>$titleUnresolved?'UNRESOLVED_SOURCE_TITLE':'RESOLVED'];
""")
old="""            $result['sources']['PPM679_EXISTING_EDITORIAL_RUNTIME']=[
                'complete'=>true,'status'=>$runtimeOriginal===null||$runtimeOriginal===false?'NOT_PRESENT':'PRESENT',
                'item_count'=>count($runtimeItems),
                'sha256'=>hash('sha256',$beforeRuntime)];
"""
assert m.count(old)==1
m=m.replace(old,"""            $result['sources']['PPM679_EXISTING_EDITORIAL_RUNTIME']=[
                'complete'=>count($runtimeMissingTitles)===0,
                'status'=>$runtimeOriginal===null||$runtimeOriginal===false?'NOT_PRESENT':'PRESENT',
                'item_count'=>count($runtimeItems),
                'unresolved_count'=>count($runtimeMissingTitles),
                'unresolved_post_ids'=>$runtimeMissingTitles,
                'sha256'=>hash('sha256',$beforeRuntime)];
            if($runtimeMissingTitles)
                $sourceProblems[]='PPM679_RUNTIME_TITLE_UNRESOLVED:'.count($runtimeMissingTitles);
""")
old="""            if(!is_string($encoded))throw new RuntimeException('PARKHAUS_ENCODING_FAILED');
            $result['sha256']=hash('sha256',$encoded);
            $result['complete']=true;$result['reason']='';
            return $result;
"""
assert m.count(old)==1
m=m.replace(old,"""            if(!is_string($encoded))throw new RuntimeException('PARKHAUS_ENCODING_FAILED');
            if($sourceProblems){
                // A full diagnostic snapshot is usable to repair existing data,
                // but can NEVER be used as an external FREI/slot approval.
                $result['diagnostic_sha256']=hash('sha256',$encoded);
                $result['sha256']='';
                $result['complete']=false;
                $result['reason']=implode(';',$sourceProblems);
                return $result;
            }
            $result['sha256']=hash('sha256',$encoded);
            $result['complete']=true;$result['reason']='';
            return $result;
""")
mini.write_text(m)
main=new/'portal-seo-topic-engine.php'
ms=main.read_text();assert ms.count('0.57.144.23')>=2
ms=ms.replace('0.57.144.23','0.57.144.24');main.write_text(ms)
print('DONE patch .24')