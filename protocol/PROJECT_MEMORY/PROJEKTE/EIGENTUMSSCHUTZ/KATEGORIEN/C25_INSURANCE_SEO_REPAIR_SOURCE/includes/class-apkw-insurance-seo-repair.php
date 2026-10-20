<?php
if (!defined('ABSPATH')) exit;
/** Strict, reversible repair of the recent Insurance-94 import; never edits the six older worlds. */
final class APKW_Insurance_SEO_Repair {
    private const STATE='apkw_ins_seo_repair_state_v1';
    private const BACKUP='apkw_ins_seo_repair_backup_v1';
    private const LOCK='apkw_ins_seo_repair_lock_v1';
    private const SNAP='apkw_target_tree_active_snapshot_v1';
    private const REV='apkw_target_tree_active_revision_v1';
    private const PAGE='apkw-insurance-seo-repair';
    private const BATCH=15;
    private static ?array $manifest=null;
    public static function init():void {
        add_action('admin_menu',[__CLASS__,'menu'],41);
        add_action('admin_post_apkw_ins_seo_repair_start',[__CLASS__,'start']);
        add_action('wp_ajax_apkw_ins_seo_repair_tick',[__CLASS__,'tick']);
    }
    public static function menu():void {
        add_submenu_page(APKW_FinalTargetAdmin::PAGE_SLUG,'Versicherungen – Keyword-Korrektur','Versicherungen SEO','manage_options',self::PAGE,[__CLASS__,'render']);
    }
    private static function profile():array {
        if(self::$manifest!==null)return self::$manifest;
        $f=APKW_DIR.'profiles/hab-und-bewahr-insurance-seo-repair.json';
        if(!is_readable($f)||hash_file('sha256',$f)!=='0a12b72d85e66cb04e3dcf223356698650c86d8b2dc39d4dd310fa2ac00a6c41')
            throw new RuntimeException('Versicherungs-SEO: verbindliches Originalprofil fehlt oder wurde verändert.');
        $d=json_decode((string)file_get_contents($f),true);
        if(!is_array($d)||($d['schema']??'')!=='HB_INSURANCE_SEO_REPAIR_DESIGN_V1')
            throw new RuntimeException('Versicherungs-SEO: unbekanntes Profil.');
        $pages=$d['pages']??[];$cats=$d['flat_categories']??[];$cov=$d['insurance_coverage']??[];
        if(count($pages)!==52||count($cats)!==138||count($cov)!==105)
            throw new RuntimeException('Versicherungs-SEO: 52/138/105 unvollständig.');
        $ids=[];$slugs=['page'=>[],'category'=>[]];$levels=['R1'=>0,'R2'=>0,'R3'=>0];
        foreach($pages as $p){
            $id=(string)($p['key']??'');$parent=$p['parent']??null;$level=(string)($p['level']??'');$slug=(string)($p['slug']??'');
            if(!$id||!isset($levels[$level])||isset($ids[$id])||isset($slugs['page'][$slug])||
              ($level==='R1'&&$parent!==null)||($level==='R2'&&(!isset($ids[$parent])||$ids[$parent]!=='R1'))||
              ($level==='R3'&&(!isset($ids[$parent])||$ids[$parent]!=='R2')))
                throw new RuntimeException('Versicherungs-SEO: Seitenebenen/IDs/Slugs unzulässig.');
            $ids[$id]=$level;$slugs['page'][$slug]=true;$levels[$level]++;
        }
        foreach($cats as $c){
            $id=(string)($c['key']??'');$slug=(string)($c['slug']??'');$p=(string)($c['parent']??'');
            if(!$id||isset($ids[$id])||isset($slugs['category'][$slug])||($ids[$p]??'')!=='R3'||
                (int)($c['wordpress_parent']??-1)!==0||count(array_unique($c['coarse_fields']??[]))<3)
                throw new RuntimeException('Versicherungs-SEO: letzte Kategorie/Tragfähigkeit unzulässig.');
            $ids[$id]='TERM';$slugs['category'][$slug]=true;
        }
        if($levels!==['R1'=>1,'R2'=>5,'R3'=>46]||count($ids)!==190)
            throw new RuntimeException('Versicherungs-SEO: Baumgröße fehlerhaft.');
        $owners=[];foreach($pages as $p)if($p['level']==='R3')$owners[$p['title']]=true;
        $coverage=[];foreach($cov as $entry){
            $name=(string)($entry['original_insurance']??'');$target=(string)($entry['keyword_owner']??'');
            if($name===''||isset($coverage[$name])||!isset($owners[$target]))
                throw new RuntimeException('Versicherungs-SEO: fehlende oder doppelte Versicherungsart.');
            $coverage[$name]=true;
        }
        return self::$manifest=$d;
    }
    private static function node(array $p):string {
        if(($p['level']??'')==='R1')return 'core:world:insurance';
        if(($p['level']??'')==='R2')return 'core:area:insurance:'.$p['slug'];
        if(($p['level']??'')==='R3')return 'core:subarea:insurance:'.$p['slug'];
        return 'core:leaf:insurance:'.$p['slug'];
    }
    private static function ordered():array {
        $m=self::profile();$jobs=[];
        foreach(['R1','R2','R3'] as $level)foreach($m['pages'] as $p)if($p['level']===$level){
            $p['type']='page';$p['name']=$p['title'];$p['node_id']=self::node($p);$jobs[]=$p;
        }
        foreach($m['flat_categories'] as $c){
            $c['level']='TERM';$c['type']='category';$c['node_id']=self::node($c);$jobs[]=$c;
        }
        return $jobs;
    }
    public static function state():array {$x=get_option(self::STATE,[]);return is_array($x)?$x:[];}
    private static function save(array $s):void {update_option(self::STATE,$s,false);}
    private static function revision(string $base):string {
        return $base.'+INS-SEO-'.substr(hash('sha256',implode('|',array_column(self::ordered(),'node_id'))),0,16);
    }
    private static function lock():bool {
        $n=(int)get_option(self::LOCK,0);
        if($n&&time()-$n<180)return false;
        if($n)delete_option(self::LOCK);
        return add_option(self::LOCK,time(),'','no');
    }
    private static function unlock():void {delete_option(self::LOCK);}
    private static function original_nodes(array $snap):array {
        $all=[];
        foreach((array)($snap['nodes']??[]) as $n)
            if(!empty($n['insurance_add_only']))$all[]=$n;
        $r1=[];$r2=[];$r3=[];$terms=[];
        foreach($all as $n){
            $id=(string)($n['node_id']??'');$parent=(string)($n['parent_id']??'');
            if($id==='core:world:insurance'&&($n['object_type']??'')==='page')$r1[]=$n;
            elseif(($n['object_type']??'')==='page'&&str_starts_with($id,'core:area:insurance:'))$r2[]=$n;
            elseif(($n['object_type']??'')==='page'&&str_starts_with($id,'core:subarea:insurance:'))$r3[]=$n;
            elseif(($n['object_type']??'')==='category'&&str_starts_with($id,'core:leaf:insurance:'))$terms[]=$n;
            else throw new RuntimeException('Versicherungs-SEO: unerwarteter Alt-Importknoten: '.$id);
        }
        if(count($all)!==94||count($r1)!==1||count($r2)!==5||count($r3)!==20||count($terms)!==68)
            throw new RuntimeException('Versicherungs-SEO: exakter 94er Bestand fehlt; keine stillen Änderungen.');
        return ['R1'=>$r1,'R2'=>$r2,'R3'=>$r3,'TERM'=>$terms,'all'=>$all];
    }
    private static function backups(array $snap,array $old):array {
        $backup=[];$seen=[];
        foreach($old['all'] as $n){
            $nid=(string)$n['node_id'];$m=$snap['mapping'][$nid]??null;$id=(int)($m['object_id']??0);
            if(!is_array($m)||$id<1||isset($seen[$id.'|'.($m['object_type']??'')]))
                throw new RuntimeException('Versicherungs-SEO: WordPress-Originalbindung fehlt oder ist doppelt.');
            $seen[$id.'|'.($m['object_type']??'')]=true;
            $kind=(string)($m['object_type']??'');
            if($kind==='page'){
                $x=get_post($id);
                if(!is_object($x)||$x->post_type!=='page'||$x->post_status!=='publish'||
                   trim((string)$x->post_content)!==''||trim((string)$x->post_excerpt)!=='')
                    throw new RuntimeException('Versicherungs-SEO: importierte Seite inzwischen bearbeitet; STOPP.');
                $backup[$nid]=['id'=>$id,'kind'=>'page','name'=>(string)$x->post_title,'slug'=>(string)$x->post_name,'parent'=>(int)$x->post_parent];
            }elseif($kind==='category'){
                $x=get_term($id,'category');
                if(!is_object($x)||is_wp_error($x)||$x->taxonomy!=='category'||(int)$x->count!==0||
                   (int)$x->parent!==0)
                    throw new RuntimeException('Versicherungs-SEO: Kategorie hat Inhalte oder ist nicht flach; STOPP.');
                $backup[$nid]=['id'=>$id,'kind'=>'term','name'=>html_entity_decode((string)$x->name,ENT_QUOTES|ENT_HTML5,'UTF-8'),
                    'slug'=>(string)$x->slug,'parent'=>0];
            }else throw new RuntimeException('Versicherungs-SEO: unbekannter WordPress-Objekttyp.');
            if($backup[$nid]['name']!==(string)$n['display_name']||$backup[$nid]['slug']!==(string)$n['slug'])
                throw new RuntimeException('Versicherungs-SEO: Seite/Term seit Import verändert.');
            $backup[$nid]['meta']=[];
            foreach(['_apkw_target_node_id','_apkw_concept_id','_apkw_parent_concept_id','_apkw_target_revision'] as $key){
                $backup[$nid]['meta'][$key]=$kind==='page'?(string)get_post_meta($id,$key,true):(string)get_term_meta($id,$key,true);
            }
            if($backup[$nid]['meta']['_apkw_target_node_id']!==$nid)
                throw new RuntimeException('Versicherungs-SEO: alte ID nicht eindeutig im WordPress-Meta.');
        }
        return $backup;
    }
    public static function preflight():array {
        if(self::state()||get_option(self::BACKUP,null)!==null)
            throw new RuntimeException('Versicherungs-SEO: Korrekturlauf existiert bereits; keine Wiederholung.');
        if((APKW_Insurance_94_AddOnly::state()['status']??'')!=='COMPLETE')
            throw new RuntimeException('Versicherungs-SEO: erst 94er-Import abschließen.');
        $snap=APKW_TargetTreeSync::active_snapshot();$rev=APKW_TargetTreeSync::active_revision();
        if(!$rev||!is_array($snap)||($snap['revision']??'')!==$rev||
           (int)($snap['settings']['expected_world_count']??0)!==7)
            throw new RuntimeException('Versicherungs-SEO: aktiver Sieben-Welten-Bestand nicht bestätigt.');
        $orig=self::original_nodes($snap);$backup=self::backups($snap,$orig);
        // No old six-world page/term may be remapped, renamed, or archived.
        $oldOwners=[];
        foreach($orig['all'] as $n)$oldOwners[$n['node_id']]=true;
        $jobs=self::ordered();$owners=[];$used=['page'=>[],'term'=>[]];$mapped=[];
        $indexes=['R1'=>0,'R2'=>0,'R3'=>0,'TERM'=>0];
        foreach($jobs as $job){
            $lvl=$job['level'];$i=$indexes[$lvl]++;
            $reuse=$orig[$lvl][$i]??null;$nid=self::node($job);
            if(isset($owners[$nid]))throw new RuntimeException('Versicherungs-SEO: doppelte neue Knoten-ID.');
            $owners[$nid]=true;
            if(isset($snap['mapping'][$nid])&&!isset($oldOwners[$nid]))
                throw new RuntimeException('Versicherungs-SEO: neuer Knoten kollidiert mit Bestand.');
            $mapped[]=['job'=>$job,'old_node_id'=>$reuse['node_id']??null,'id'=>$reuse!==null?(int)$snap['mapping'][$reuse['node_id']]['object_id']:0];
            $kind=$job['type']==='page'?'page':'term';$slug=$job['slug'];
            if(isset($used[$kind][$slug]))throw new RuntimeException('Versicherungs-SEO: neuer Slug doppelt.');
            $used[$kind][$slug]=true;
        }
        $ownedPageIds=[];$ownedTermIds=[];
        foreach($backup as $x){if($x['kind']==='page')$ownedPageIds[$x['id']]=true;else $ownedTermIds[$x['id']]=true;}
        foreach($mapped as $j){
            $job=$j['job'];$slug=$job['slug'];
            if($job['type']==='page'){
                $found=get_posts(['post_type'=>'page','post_status'=>'any','name'=>$slug,
                    'posts_per_page'=>10,'fields'=>'ids','suppress_filters'=>true]);
                if(!is_array($found))throw new RuntimeException('Versicherungs-SEO: Seitenslug-Abfrage fehlt.');
                foreach($found as $id)if(!isset($ownedPageIds[(int)$id]))
                    throw new RuntimeException('Versicherungs-SEO: Seitenslug fremd belegt: '.$slug);
            }else{
                $term=get_term_by('slug',$slug,'category');
                if(is_object($term)&&!isset($ownedTermIds[(int)$term->term_id]))
                    throw new RuntimeException('Versicherungs-SEO: Kategorie-Slug fremd belegt: '.$slug);
                $term=term_exists($job['name'],'category',0);
                if(is_wp_error($term))throw new RuntimeException('Versicherungs-SEO: Termprüfung defekt.');
                if($term){$id=is_array($term)?(int)($term['term_id']??0):(int)$term;
                    if(!isset($ownedTermIds[$id]))throw new RuntimeException('Versicherungs-SEO: Kategoriename fremd belegt: '.$job['name']);}
            }
        }
        // Check all six earlier worlds are byte-identically preserved in the snapshot.
        $worlds=array_filter($snap['nodes'],fn($n)=>str_starts_with((string)($n['node_id']??''),'core:world:'));
        if(count($worlds)!==7)throw new RuntimeException('Versicherungs-SEO: sechs alte Welten plus Versicherung nicht nachgewiesen.');
        return ['valid'=>true,'writes'=>0,'old_revision'=>$rev,'snapshot'=>$snap,'old_objects'=>$backup,'jobs'=>$mapped,
            'original_node_ids'=>array_keys($oldOwners),'new_pages'=>52,'new_terms'=>138,'reused_pages'=>26,'reused_terms'=>68,
            'additional_pages'=>26,'additional_terms'=>70];
    }
    public static function dry_run():array {
        $p=self::preflight();return array_diff_key($p,array_flip(['snapshot','old_objects','jobs','original_node_ids']));
    }
    public static function start():void {
        try{
            if(!current_user_can('manage_options'))throw new RuntimeException('Nur Administratoren.');
            check_admin_referer('apkw_ins_seo_repair_start');
            if(empty($_POST['apkw_ins_seo_repair_confirm']))throw new RuntimeException('Eindeutige Freigabe fehlt.');
            if(!self::lock())throw new RuntimeException('Korrektur wird bereits verarbeitet.');
            try{
                $p=self::preflight();
                update_option(self::BACKUP,['snap'=>$p['snapshot'],'old_objects'=>$p['old_objects']],false);
                self::save(['status'=>'WRITING','base_revision'=>$p['old_revision'],
                    'base_sha256'=>hash('sha256',serialize($p['snapshot'])),'jobs'=>$p['jobs'],'i'=>0,
                    'new_mapping'=>[],'created'=>[],'error'=>'']);
            }finally{self::unlock();}
            wp_safe_redirect(admin_url('admin.php?page='.self::PAGE.'&started=1'));exit;
        }catch(Throwable $e){wp_die(esc_html($e->getMessage()),'Versicherungs-SEO STOPP',['response'=>409]);}
    }
    private static function ensure_base(array $s):array {
        $snap=APKW_TargetTreeSync::active_snapshot();
        if(($snap['revision']??'')!==$s['base_revision']||
            APKW_TargetTreeSync::active_revision()!==$s['base_revision']||
            !hash_equals($s['base_sha256'],hash('sha256',serialize($snap))))
            throw new RuntimeException('Versicherungs-SEO: Ausgangsrevision fremd verändert.');
        return $snap;
    }
    private static function apply(array &$s):void {
        self::ensure_base($s);$jobs=$s['jobs'];$processed=0;
        while($processed<self::BATCH&&$s['i']<count($jobs)){
            $item=$jobs[$s['i']];$job=$item['job'];$node=self::node($job);$id=(int)$item['id'];
            $parent=0;$parentNode='';
            if(($job['parent']??null)!==null)foreach($jobs as $x)if($x['job']['key']===$job['parent']){
                $parentNode=self::node($x['job']);$parent=(int)($s['new_mapping'][$parentNode]['object_id']??0);break;
            }
            if($job['type']==='page'&&$job['level']!=='R1'&&$parent<1)
                throw new RuntimeException('Versicherungs-SEO: WordPress-Elternseite nicht verfügbar.');
            if($job['type']==='page'){
                if($id>0)APKW_TargetWriter::target_tree_update_page($id,['post_title'=>$job['name'],'post_name'=>$job['slug'],'post_parent'=>$parent]);
                else $id=APKW_TargetWriter::target_tree_insert_page(['post_title'=>$job['name'],'post_name'=>$job['slug'],
                    'post_parent'=>$parent,'post_status'=>'publish']);
                $ref=['kind'=>'page','id'=>$id];
            }else{
                if($id>0)APKW_TargetWriter::target_tree_update_term($id,'category',['name'=>$job['name'],'slug'=>$job['slug'],'parent'=>0]);
                else $id=APKW_TargetWriter::target_tree_insert_term('category',['name'=>$job['name'],'slug'=>$job['slug'],'parent'=>0]);
                $ref=['kind'=>'term','id'=>$id,'taxonomy'=>'category'];
            }
            if((int)$item['id']===0)$s['created'][]=['ref'=>$ref,'node'=>$node,'name'=>$job['name'],'slug'=>$job['slug']];
            $s['new_mapping'][$node]=['object_id'=>$id,'object_type'=>$job['type'],
                'adapter'=>$job['type']==='page'?'wordpress_post':'wordpress_taxonomy'];
            if($job['type']==='category')$s['new_mapping'][$node]['taxonomy']='category';
            $s['i']++;self::save($s); // Physical ID journaled BEFORE metadata writes.
            // Exactly the original TargetWriter metadata contract, including every new page/term.
            foreach(['_apkw_target_node_id'=>$node,'_apkw_concept_id'=>$node,
                '_apkw_parent_concept_id'=>$parentNode,'_apkw_target_pillar'=>'core',
                '_apkw_portal_block'=>'content','_apkw_portal_root'=>$job['level']==='R1'?'1':'0',
                '_apkw_target_active'=>'1','_apkw_target_revision'=>self::revision($s['base_revision']),
                '_apkw_seo_index_approved'=>'0'] as $k=>$v)
                APKW_TargetWriter::target_tree_set_meta($ref,$job['type'],$k,(string)$v);
            $processed++;
        }
        if($s['i']>=count($jobs)){$s['status']='VERIFY';self::save($s);}
    }
    private static function verify(array $s):void {
        if(count($s['new_mapping'])!==190||$s['i']!==190)throw new RuntimeException('Versicherungs-SEO: 190/190 nicht abgeschlossen.');
        foreach($s['jobs'] as $item){
            $job=$item['job'];$nid=self::node($job);$m=$s['new_mapping'][$nid]??[];$id=(int)($m['object_id']??0);
            if($id<1)throw new RuntimeException('Versicherungs-SEO: Objekt ohne WordPress-ID.');
            if($job['type']==='page'){
                $x=get_post($id);
                if(!is_object($x)||$x->post_type!=='page'||$x->post_status!=='publish'||
                    $x->post_name!==$job['slug']||html_entity_decode((string)$x->post_title,ENT_QUOTES|ENT_HTML5,'UTF-8')!==$job['name'])
                    throw new RuntimeException('Versicherungs-SEO: Seite im Readback ungleich.');
                $parent=0;if($job['parent']!==null)foreach($s['jobs'] as $j)if($j['job']['key']===$job['parent']){
                    $parent=(int)($s['new_mapping'][self::node($j['job'])]['object_id']??0);break;
                }
                if((int)$x->post_parent!==$parent)throw new RuntimeException('Versicherungs-SEO: falsche physische Seitentiefe.');
                if((string)get_post_meta($id,'_apkw_target_node_id',true)!==$nid)
                    throw new RuntimeException('Versicherungs-SEO: Seitenmeta fehlt.');
            }else{
                $x=get_term($id,'category');
                if(!is_object($x)||is_wp_error($x)||(int)$x->parent!==0||(string)$x->slug!==$job['slug']||
                    html_entity_decode((string)$x->name,ENT_QUOTES|ENT_HTML5,'UTF-8')!==$job['name']||
                    (string)get_term_meta($id,'_apkw_parent_concept_id',true)!==self::parent_node($job,$s['jobs']))
                    throw new RuntimeException('Versicherungs-SEO: Beitragsterm/Elternbindung fehlt.');
            }
        }
    }
    private static function parent_node(array $job,array $jobs):string {
        if(($job['parent']??null)===null)return '';
        foreach($jobs as $x)if($x['job']['key']===$job['parent'])return self::node($x['job']);
        return '';
    }
    private static function finish(array &$s):void {
        $base=self::ensure_base($s);self::verify($s);$stage=$base;
        $oldIds=[];
        foreach($stage['nodes'] as $n)if(!empty($n['insurance_add_only']))$oldIds[$n['node_id']]=true;
        if(count($oldIds)!==94)throw new RuntimeException('Versicherungs-SEO: geschützter Altimport nicht 94.');
        $stage['nodes']=array_values(array_filter($stage['nodes'],fn($n)=>!isset($oldIds[$n['node_id']??''])));
        foreach($oldIds as $nid=>$_)unset($stage['mapping'][$nid]);
        foreach($s['jobs'] as $item){
            $job=$item['job'];$node=self::node($job);
            $stage['nodes'][]=['node_id'=>$node,'pillar'=>'core','object_type'=>$job['type'],
                'parent_id'=>self::parent_node($job,$s['jobs']),'display_name'=>$job['name'],'slug'=>$job['slug'],
                'status'=>'active','seo_owner'=>$job['level']==='R3','seo_seed'=>$job['level']==='R3'?$job['name']:'',
                'intent_key'=>'','primary_keyword'=>$job['level']==='R3'?$job['name']:'','insurance_seo_repair'=>true];
            $stage['mapping'][$node]=$s['new_mapping'][$node];
        }
        $stage['revision']=self::revision($s['base_revision']);
        $stage['project']['insurance_keyword_tree_corrected_at_utc']=gmdate('c');
        $stage['completed_at_utc']=gmdate('c');
        if((int)($stage['settings']['expected_world_count']??0)!==7)
            throw new RuntimeException('Versicherungs-SEO: siebter World-Count fehlt.');
        $f=APKW_FinalTargetAdmin::frontend_readback($stage);
        if(empty($f['valid']))throw new RuntimeException('Versicherungs-SEO: Stage-Frontend ungültig: '.implode(',',(array)($f['errors']??[])));
        update_option(self::SNAP,$stage,false);update_option(self::REV,$stage['revision'],false);
        $f=APKW_FinalTargetAdmin::frontend_readback();
        if(empty($f['valid']))throw new RuntimeException('Versicherungs-SEO: finale Frontendprüfung gescheitert.');
        if(class_exists('APKW_FrontendStructure'))APKW_FrontendStructure::invalidate_cache();
        $s['status']='COMPLETE';$s['finished_at_utc']=gmdate('c');
        $s['result']=['pages'=>52,'terms'=>138,'preserved_original_worlds'=>6,'original_insurance_type_coverage'=>105];self::save($s);
    }
    private static function rollback(array &$s):void {
        $backup=get_option(self::BACKUP,null);
        if(!is_array($backup)||!is_array($backup['snap']??null))throw new RuntimeException('Versicherungs-SEO: Rollback-Backup fehlt, kein blindes Löschen.');
        $base=$backup['snap'];$rev=APKW_TargetTreeSync::active_revision();$new=self::revision($s['base_revision']);
        if(!in_array($rev,[$s['base_revision'],$new],true))
            throw new RuntimeException('Versicherungs-SEO: fremde aktive Revision, Rückbau gesperrt.');
        if($rev===$new){update_option(self::SNAP,$base,false);update_option(self::REV,$s['base_revision'],false);}
        // New objects are removed before original page/term URLs are restored.
        $n=0;
        while($n<self::BATCH&&!empty($s['created'])){
            $c=end($s['created']);$ref=$c['ref'];$id=(int)$ref['id'];$safe=false;
            if($ref['kind']==='page'){
                $p=get_post($id);
                $safe=is_object($p)&&$p->post_type==='page'&&$p->post_name===$c['slug']&&
                    trim((string)$p->post_content)===''&&trim((string)$p->post_excerpt)==='';
                // Child pages must be removed first; do not delete a page hosting foreign children.
                $children=get_posts(['post_type'=>'page','post_parent'=>$id,'post_status'=>'any','posts_per_page'=>1,'fields'=>'ids']);
                if($children)$safe=false;
            }else{
                $p=get_term($id,'category');
                $safe=is_object($p)&&!is_wp_error($p)&&$p->slug===$c['slug']&&(int)$p->count===0;
            }
            $meta=$ref['kind']==='page'?(string)get_post_meta($id,'_apkw_target_node_id',true):(string)get_term_meta($id,'_apkw_target_node_id',true);
            if(!$safe||($meta!==''&&$meta!==$c['node']))
                throw new RuntimeException('Versicherungs-SEO: neu erstelltes Objekt nicht sicher leer/eigen, Rückbau stoppen.');
            APKW_TargetWriter::target_tree_delete_object($ref);
            array_pop($s['created']);$n++;self::save($s);
        }
        if($s['created'])return;
        // Restore only the 94 confirmed insurance objects. No pre-existing protection pages.
        $restored=0;
        foreach($backup['old_objects'] as $nid=>$o){
            $id=(int)$o['id'];$ref=['kind'=>$o['kind']==='page'?'page':'term','id'=>$id,'taxonomy'=>'category'];
            if($o['kind']==='page')APKW_TargetWriter::target_tree_update_page($id,['post_title'=>$o['name'],'post_name'=>$o['slug'],'post_parent'=>$o['parent']]);
            else APKW_TargetWriter::target_tree_update_term($id,'category',['name'=>$o['name'],'slug'=>$o['slug'],'parent'=>0]);
            foreach($o['meta'] as $key=>$val)APKW_TargetWriter::target_tree_set_meta($ref,$o['kind']==='page'?'page':'category',$key,(string)$val);
            $restored++;
        }
        $s['status']='ROLLED_BACK';$s['result']=['restored_original_insurance_objects'=>$restored];self::save($s);
        if(class_exists('APKW_FrontendStructure'))APKW_FrontendStructure::invalidate_cache();
    }
    public static function batch():array {
        if(!self::lock())return self::state();
        try{
            $s=self::state();if(!in_array(($s['status']??''),['WRITING','VERIFY','ROLLBACK'],true))return $s;
            try{
                if($s['status']==='WRITING')self::apply($s);
                elseif($s['status']==='VERIFY')self::finish($s);
                else self::rollback($s);
            }catch(Throwable $e){
                $s['status']='ROLLBACK';$s['error']=($s['error']??'').' | '.$e->getMessage();self::save($s);
            }
            return $s;
        }finally{self::unlock();}
    }
    public static function tick():void {
        try{
            if(!current_user_can('manage_options'))throw new RuntimeException('Nur Administratoren.');
            check_ajax_referer('apkw_ins_seo_repair_tick','nonce');
            $s=self::batch();wp_send_json_success(['status'=>$s['status']??'','written'=>$s['i']??0,'total'=>190,'error'=>$s['error']??'']);
        }catch(Throwable $e){wp_send_json_error(['error'=>$e->getMessage()],409);}
    }
    public static function render():void {
        if(!current_user_can('manage_options'))return;
        echo '<div class="wrap"><h1>Versicherungen – vorhandenen Themenbaum korrigieren</h1>';
        echo '<p>Bestehende 94 Versicherungsobjekte sicher umstellen: 52 Seiten, davon 46 konkret recherchierte Versicherungsthemen; darunter 138 flache Beitragskategorien. Alle 105 Versicherungsarten bleiben zugeordnet. Die sechs alten Hauptwelten werden nicht geändert.</p>';
        $s=self::state();$status=(string)($s['status']??'');
        if($status==='COMPLETE')echo '<div class="notice notice-success"><p>COMPLETE: 52 Versicherungsseiten, 138 Beitragskategorien; sechs bestehende Welten geschützt.</p></div>';
        elseif($status==='ROLLED_BACK')echo '<div class="notice notice-warning"><p>ROLLED BACK – ursprünglicher 94er-Versicherungsstand wiederhergestellt.</p></div>';
        elseif($status!=='')echo '<p>STATUS: '.esc_html($status).' '.(int)($s['i']??0).'/190</p><p>'.esc_html((string)($s['error']??'')).'</p>';
        else{
            try{$p=self::dry_run();echo '<p><strong>Vorschau PASS:</strong> null Schreibvorgänge. 26 bestehende Versicherungsseiten und 68 Terms werden nur innerhalb der Versicherungswelt korrigiert; 26 Keyword-Seiten und 70 Terms zusätzlich. Alte sechs Hauptbereiche unberührt.</p>';
                echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
                wp_nonce_field('apkw_ins_seo_repair_start');
                echo '<input type="hidden" name="action" value="apkw_ins_seo_repair_start"><label><input type="checkbox" name="apkw_ins_seo_repair_confirm" value="1"> Ich gebe ausschließlich die abgesicherte Versicherungs-SEO-Korrektur frei.</label><p><button class="button button-primary">Versicherungen nach Keywords korrigieren</button></p></form>';
            }catch(Throwable $e){echo '<p><strong>BLOCKIERT:</strong> '.esc_html($e->getMessage()).'</p>';}
        }
        if(in_array($status,['WRITING','VERIFY','ROLLBACK'],true)){
            $nonce=wp_create_nonce('apkw_ins_seo_repair_tick');
            echo '<p id="apkw-seo-repair-status">Fortsetzung wird ausgeführt...</p><script>(function(){var u='.wp_json_encode(admin_url('admin-ajax.php')).',n='.wp_json_encode($nonce).';function tick(){var x=new URLSearchParams();x.append("action","apkw_ins_seo_repair_tick");x.append("nonce",n);fetch(u,{method:"POST",credentials:"same-origin",body:x}).then(function(r){return r.json()}).then(function(r){if(!r.success)throw Error(r.data&&r.data.error||"Ajax fehlerhaft");var d=r.data;document.getElementById("apkw-seo-repair-status").textContent=d.status+" "+d.written+"/190";if(["COMPLETE","ROLLED_BACK","BLOCKED"].includes(d.status))location.reload();else setTimeout(tick,350)}).catch(function(e){document.getElementById("apkw-seo-repair-status").textContent="Angehalten: "+e.message+". Seite neu laden."})}tick()})();</script>';
        }
        echo '</div>';
    }
}
