<?php
if (!defined('ABSPATH')) exit;
/** Separate insurance world, same established central category plugin. Never replays C2.2/C2.3. */
final class APKW_Insurance_94_AddOnly {
    private const STATE='apkw_ins_94_state_v1';
    private const BASE='apkw_ins_94_base_v1';
    private const LOCK='apkw_ins_94_lock_v1';
    private const SNAP='apkw_target_tree_active_snapshot_v1';
    private const REV='apkw_target_tree_active_revision_v1';
    private const BATCH=15;
    private const EXPECTED=94;
    private static ?array $jobs=null;
    public static function init():void {
        add_action('admin_menu',[__CLASS__,'menu'],40);
        add_action('admin_post_apkw_ins_94_start',[__CLASS__,'start']);
        add_action('wp_ajax_apkw_ins_94_tick',[__CLASS__,'tick']);
    }
    public static function menu():void {
        add_submenu_page(APKW_FinalTargetAdmin::PAGE_SLUG,'Versicherungen – 94 Ergänzungen','Versicherungen','manage_options','apkw-insurance-94',[__CLASS__,'render']);
    }
    private static function manifest():array {
        $f=APKW_DIR.'profiles/hab-und-bewahr-insurance-94.json';
        if (!is_readable($f)) throw new RuntimeException('Versicherungsprofil nicht gefunden.');
        $d=json_decode((string)file_get_contents($f),true);
        if (!is_array($d)||($d['contract']??'')!=='HB_INSURANCE_94_COMPACT_ADD_ONLY_V1') throw new RuntimeException('Versicherungsprofil ungültig.');
        if(($d['status']??'')!=='FACHLICHE_KOMPAKTFASSUNG__NICHT_IMPORTFREIGEGEBEN')throw new RuntimeException('Versicherungsprofil nicht als fachliche Kompaktfassung markiert.');
        if(($d['source_blob_sha']??'')!=='a74e6b3c62a49115bc58bc4fb233ca882dd87306')
            throw new RuntimeException('Versicherung: unbestätigte Quellvorlage.');
        return $d;
    }
    public static function jobs():array {
        if (self::$jobs!==null) return self::$jobs;
        $d=self::manifest();$pages=$d['pages']??[];$cats=$d['flat_categories']??[];
        if (count($pages)!==26||count($cats)!==68) throw new RuntimeException('Versicherung: Anzahl unvollständig.');
        $coverage=$d['insurance_coverage']??[];
        if(!is_array($coverage)||count($coverage)!==105)throw new RuntimeException('Versicherung: 105 Arten nicht vollständig zugeordnet.');
        $covSeen=[];$validOwners=[];foreach($pages as $p)if(($p['level']??'')==='R3')$validOwners[(string)$p['key']]=true;
        foreach($coverage as $item){
            $name=(string)($item['original_insurance']??'');$owner=(string)($item['topic_page_key']??'');
            if($name===''||isset($covSeen[$name])||!isset($validOwners[$owner]))throw new RuntimeException('Versicherung: Typenabdeckung doppelt, leer oder ownerlos.');
            $covSeen[$name]=true;
        }
        if(count($validOwners)!==20)throw new RuntimeException('Versicherung: 20 gebündelte Themen-Owner fehlen.');
        $all=[];$seen=[];$slugs=['page'=>[],'category'=>[]];$levels=['R1'=>0,'R2'=>0,'R3'=>0];$parents=[];$r3owners=[];$topics=[];
        foreach($pages as $p){
            $key=(string)($p['key']??'');$level=(string)($p['level']??'');$parent=$p['parent']??null;$slug=(string)($p['slug']??'');$name=(string)($p['title']??'');
            if(!isset($levels[$level])||$key===''||$name===''||$slug===''||isset($seen[$key])||isset($slugs['page'][$slug])||
               ($level==='R1'&&$parent!==null)||($level!=='R1'&&(!is_string($parent)||!isset($seen[$parent]))))
                throw new RuntimeException('Versicherung: Seitenbaum nicht eindeutig oder ungeordnet.');
            $expected=$level==='R1'?null:($level==='R2'?'R1':'R2');
            if($expected!==null&&($parents[$parent]??'')!==$expected)throw new RuntimeException('Versicherung: falsche Seitentiefe.');
            $id=($level==='R1'?'core:world:insurance':($level==='R2'?'core:area:insurance:':'core:subarea:insurance:').$slug);
            $seen[$key]=true;$slugs['page'][$slug]=true;$levels[$level]++;$parents[$key]=$level;
            if($level==='R3')$r3owners[$key]=0;
            $all[]=['key'=>$key,'node_id'=>$id,'level'=>$level,'type'=>'page','name'=>$name,'slug'=>$slug,'parent'=>$parent];
        }
        foreach($cats as $c){
            $key=(string)($c['key']??'');$parent=(string)($c['parent']??'');$slug=(string)($c['slug']??'');$name=(string)($c['name']??'');
            if(!array_key_exists($parent,$r3owners)||$key===''||$slug===''||$name===''||isset($seen[$key])||
                isset($slugs['category'][$slug])||(!isset($c['coarse_capacity_domains'])||!is_array($c['coarse_capacity_domains'])||count(array_unique($c['coarse_capacity_domains']))<3)||
                (int)($c['term_parent']??-1)!==0)
                throw new RuntimeException('Versicherung: Beitragskategorie ungültig.');
            if(!empty($c['article_titles'])||!empty($c['articles']))
                throw new RuntimeException('Versicherung: keine Artikelerstellung im Kategoriebüro.');
            $seen[$key]=true;$slugs['category'][$slug]=true;$r3owners[$parent]++;
            $all[]=['key'=>$key,'node_id'=>'core:leaf:insurance:'.$slug,'level'=>'TERM','type'=>'category',
              'name'=>$name,'slug'=>$slug,'parent'=>$parent];
        }
        if($levels!==['R1'=>1,'R2'=>5,'R3'=>20]||count($all)!==self::EXPECTED||count(array_filter($r3owners,fn($n)=>$n>=3))!==20)
            throw new RuntimeException('Versicherung: 1/5/20/68-Struktur verletzt.');
        return self::$jobs=$all;
    }
    public static function state():array { $x=get_option(self::STATE,[]);return is_array($x)?$x:[]; }
    private static function save(array $s):void {update_option(self::STATE,$s,false);}
    private static function revision(string $base):string {return $base.'+INS-'.substr(hash('sha256',implode('|',array_column(self::jobs(),'node_id'))),0,16);}
    private static function lock():bool {
        $old=(int)get_option(self::LOCK,0);
        if($old&&time()-$old<180)return false;
        if($old)delete_option(self::LOCK);
        return add_option(self::LOCK,time(),'','no');
    }
    private static function unlock():void {delete_option(self::LOCK);}
    /** Zero-write complete physical baseline and prospective collision check. */
    public static function preflight():array {
        if(self::state()||get_option(self::BASE,null)!==null)throw new RuntimeException('Versicherung: bestehender Lauf; erneuter Start gesperrt.');
        $c22=APKW_C22_472_AddOnly::state();
        if(($c22['status']??'')!=='COMPLETE')throw new RuntimeException('Versicherung: C2.2-472 nicht abgeschlossen.');
        // The older 471-category import must complete BEFORE a seventh world
        // changes the active target-tree revision. Never create an import-order trap.
        $c23=APKW_C23_471_AddOnly::state();
        if(($c23['status']??'')!=='COMPLETE')
            throw new RuntimeException('Versicherung: zuerst 471 Bestandskategorien (C2.3) abschließen.');
        $c23check=APKW_C23_471_AddOnly::completion_audit();
        if(empty($c23check['valid'])||(int)($c23check['new_categories']??0)!==471)
            throw new RuntimeException('Versicherung: Schutzprüfung des 471er-Bestands fehlt.');
        $snap=APKW_TargetTreeSync::active_snapshot();$rev=APKW_TargetTreeSync::active_revision();
        if(!$rev||($snap['revision']??'')!==$rev||empty($snap['nodes'])||empty($snap['mapping']))
            throw new RuntimeException('Versicherung: kein konsistenter aktiver Zielbaum.');
        if((int)($snap['settings']['expected_world_count']??0)!==6)
            throw new RuntimeException('Versicherung: unerwartete Zahl vorhandener Hauptwelten.');
        $s=APKW_TargetTreeSync::state();
        if(in_array((string)($s['status']??''),['WRITING','READBACK','ROLLBACK_PENDING'],true))
            throw new RuntimeException('Versicherung: anderer Zielbaumlauf noch aktiv.');
        $known=[];foreach($snap['nodes'] as $node)if(isset($node['node_id']))$known[(string)$node['node_id']]=true;
        $pageSlugs=[];$termSlugs=[];
        foreach(self::jobs() as $job){
            if(isset($known[$job['node_id']])||isset($snap['mapping'][$job['node_id']]))
                throw new RuntimeException('Versicherung: bereits belegte Zielbaum-ID.');
            if($job['type']==='page')$pageSlugs[]=$job['slug'];else $termSlugs[]=$job['slug'];
        }
        $term=get_terms(['taxonomy'=>'category','hide_empty'=>false,'slug'=>$termSlugs,'number'=>1]);
        if(is_wp_error($term)||!empty($term))throw new RuntimeException('Versicherung: WordPress-Kategorie-Slug bereits belegt.');
        // Flat WordPress categories reject duplicate names even when the new
        // proposed slug differs. Detect this before the first write.
        foreach(self::jobs() as $job){
            if($job['type']!=='category')continue;
            $existing=term_exists($job['name'],'category',0);
            if(is_wp_error($existing)||!empty($existing))
                throw new RuntimeException('Versicherung: WordPress-Kategoriename bereits belegt: '.$job['name']);
        }
        foreach($pageSlugs as $slug){
            $pages=get_posts(['post_type'=>'page','post_status'=>'any','numberposts'=>1,'fields'=>'ids',
                'name'=>$slug,'suppress_filters'=>true]);
            if(!is_array($pages)||$pages)throw new RuntimeException('Versicherung: WordPress-Seitenslug bereits belegt: '.$slug);
        }
        return ['valid'=>true,'writes'=>0,'new_pages'=>26,'new_categories'=>68,
            'old_revision'=>$rev,'base_sha256'=>hash('sha256',serialize($snap)), 'snapshot'=>$snap];
    }
    public static function dry_run():array {
        $p=self::preflight();unset($p['snapshot']);return $p;
    }
    public static function start():void {
        try{
            if(!current_user_can('manage_options'))throw new RuntimeException('Nur Administratoren.');
            check_admin_referer('apkw_ins_94_start');
            if(empty($_POST['apkw_ins_94_confirm']))throw new RuntimeException('Versicherung: gesonderte Importfreigabe fehlt.');
            if(!self::lock())throw new RuntimeException('Versicherung: anderer Vorgang aktiv.');
            try{
                $p=self::preflight();update_option(self::BASE,$p['snapshot'],false);
                self::save(['status'=>'WRITING','contract'=>'HB_INSURANCE_94_COMPACT_ADD_ONLY_V1',
                    'base_revision'=>$p['old_revision'],'base_sha256'=>$p['base_sha256'],
                    'write_index'=>0,'created'=>[],'mapping'=>[],'total'=>self::EXPECTED,'error'=>'']);
            }finally{self::unlock();}
            wp_safe_redirect(admin_url('admin.php?page=apkw-insurance-94&started=1'));exit;
        }catch(Throwable $e){wp_die(esc_html($e->getMessage()),'Versicherung BLOCKIERT',['response'=>409]);}
    }
    private static function ensure_base(array $s):array {
        $base=APKW_TargetTreeSync::active_snapshot();
        if(APKW_TargetTreeSync::active_revision()!==(string)$s['base_revision']||
           ($base['revision']??'')!==(string)$s['base_revision']||
           !hash_equals((string)$s['base_sha256'],hash('sha256',serialize($base))))
           throw new RuntimeException('Versicherung: Ausgangsbestand wurde verändert.');
        return $base;
    }
    private static function write(array &$s):void {
        self::ensure_base($s);$jobs=self::jobs();$done=0;
        while($done<self::BATCH&&(int)$s['write_index']<self::EXPECTED){
            $job=$jobs[(int)$s['write_index']];$parent=$job['parent'];
            $parid=0;
            if($parent!==null){
                $pkey=null;foreach($jobs as $k)if($k['key']===$parent){$pkey=$k['node_id'];break;}
                $parid=(int)($s['mapping'][$pkey]['object_id']??0);
                if($parid<1)throw new RuntimeException('Versicherung: neue Elternseite fehlt.');
            }
            if($job['type']==='page'){
                $id=APKW_TargetWriter::target_tree_insert_page(['post_title'=>$job['name'],'post_name'=>$job['slug'],
                    'post_parent'=>$parid,'post_status'=>'publish']);$ref=['kind'=>'page','id'=>$id];
            }else{
                $id=APKW_TargetWriter::target_tree_insert_term('category',['name'=>$job['name'],
                    'slug'=>$job['slug'],'parent'=>0]);$ref=['kind'=>'term','id'=>$id,'taxonomy'=>'category'];
            }
            $s['created'][]=$ref;$s['mapping'][$job['node_id']]=['object_id'=>$id,'object_type'=>$job['type'],
                'adapter'=>$job['type']==='page'?'wordpress_post':'wordpress_taxonomy'];
            if($job['type']==='category')$s['mapping'][$job['node_id']]['taxonomy']='category';
            // Save newly created IDs before any secondary metadata writes can throw.
            $s['write_index']++;self::save($s);
            $pnode='';foreach($jobs as $item)if($item['key']===$parent){$pnode=$item['node_id'];break;}
            $meta=['_apkw_target_node_id'=>$job['node_id'],'_apkw_concept_id'=>$job['node_id'],
                '_apkw_parent_concept_id'=>$pnode,'_apkw_target_pillar'=>'core',
                '_apkw_portal_block'=>'content','_apkw_portal_root'=>$job['level']==='R1'?'1':'0',
                '_apkw_target_active'=>'1','_apkw_target_revision'=>self::revision($s['base_revision']),
                '_apkw_seo_index_approved'=>'0'];
            foreach($meta as $key=>$val)APKW_TargetWriter::target_tree_set_meta($ref,$job['type'],$key,$val);
            $done++;
        }
        if((int)$s['write_index']===self::EXPECTED){$s['status']='VERIFY';self::save($s);}
    }
    private static function verify(array $s):void {
        if(count($s['created'])!==self::EXPECTED||count($s['mapping'])!==self::EXPECTED)
            throw new RuntimeException('Versicherung: physische Objektliste unvollständig.');
        foreach(self::jobs() as $job){
            $id=(int)($s['mapping'][$job['node_id']]['object_id']??0);
            if($id<1)throw new RuntimeException('Versicherung: fehlende WordPress-ID.');
            if($job['type']==='page'){
                $p=get_post($id);if(!is_object($p)||($p->post_type??'')!=='page'||
                    ($p->post_status??'')!=='publish'||(string)($p->post_name??'')!==$job['slug'])
                    throw new RuntimeException('Versicherung: neue Seite nicht identisch.');
                $parent=0;if($job['parent']!==null)foreach(self::jobs() as $x)if($x['key']===$job['parent']){
                    $parent=(int)($s['mapping'][$x['node_id']]['object_id']??0);break;}
                if((int)($p->post_parent??-1)!==$parent)throw new RuntimeException('Versicherung: Seiteneltern falsch.');
                if((string)get_post_meta($id,'_apkw_target_node_id',true)!==$job['node_id'])
                    throw new RuntimeException('Versicherung: Seitenmeta fehlt.');
            }else{
                $t=get_term($id,'category');if(!is_object($t)||is_wp_error($t)||
                    ($t->taxonomy??'')!=='category'||(string)($t->slug??'')!==$job['slug']||
                    html_entity_decode((string)($t->name??''),ENT_QUOTES|ENT_HTML5,'UTF-8')!==$job['name']||
                    (int)($t->parent??-1)!==0||get_term_meta($id,'_apkw_target_node_id',true)!==$job['node_id'])
                    throw new RuntimeException('Versicherung: WordPress-Term nicht identisch.');
            }
        }
    }
    private static function finish(array &$s):void {
        $base=self::ensure_base($s);self::verify($s);$stage=$base;$nodes=[];
        foreach(self::jobs() as $job)$nodes[$job['key']]=$job['node_id'];
        foreach(self::jobs() as $job){
            $stage['nodes'][]=['node_id'=>$job['node_id'],'pillar'=>'core','object_type'=>$job['type'],
                'parent_id'=>$job['parent']===null?'':$nodes[$job['parent']],
                'display_name'=>$job['name'],'slug'=>$job['slug'],'status'=>'active',
                'seo_owner'=>false,'seo_seed'=>'','intent_key'=>'','primary_keyword'=>'',
                'insurance_add_only'=>true];
            $stage['mapping'][$job['node_id']]=$s['mapping'][$job['node_id']];
        }
        $stage['revision']=self::revision($s['base_revision']);
        $stage['settings']['expected_world_count']=7;
        $stage['project']['insurance_94_applied_at_utc']=gmdate('c');
        $stage['completed_at_utc']=gmdate('c');
        $check=APKW_FinalTargetAdmin::frontend_readback($stage);
        if(empty($check['valid']))throw new RuntimeException('Versicherung: Staging-Navigation nicht geprüft: '.implode(',',(array)($check['errors']??[])));
        update_option(self::SNAP,$stage,false);update_option(self::REV,$stage['revision'],false);
        $live=APKW_FinalTargetAdmin::frontend_readback();
        if(empty($live['valid']))throw new RuntimeException('Versicherung: finale Navigation nicht gültig.');
        if(class_exists('APKW_FrontendStructure'))APKW_FrontendStructure::invalidate_cache();
        $s['status']='COMPLETE';$s['completed_at_utc']=gmdate('c');$s['result']=['new_pages'=>26,
            'new_categories'=>68,'protected_baseline'=>'UNCHANGED','physical_readback'=>'PASS'];self::save($s);
    }
    private static function owns_created(int $id,string $kind):bool {
        // An insert can succeed and the first metadata write can fail.
        // In that case use the journalled physical ID AND exact new slug/name,
        // but never delete an unrelated object bearing different metadata.
        foreach(self::jobs() as $j){
            if(($j['type']==='page'?'page':'term')!==$kind)continue;
            $node=$j['node_id'];$bound=$kind==='page'
                ?(string)get_post_meta($id,'_apkw_target_node_id',true)
                :(string)get_term_meta($id,'_apkw_target_node_id',true);
            if($bound!==''&&$bound!==$node)continue;
            $s=self::state();if((int)($s['mapping'][$node]['object_id']??0)!==$id)continue;
            if($kind==='page'){
                $p=get_post($id);
                if(is_object($p)&&(string)($p->post_name??'')===$j['slug']&&
                   (string)($p->post_title??'')===$j['name'])return true;
            }else{
                $t=get_term($id,'category');
                if(is_object($t)&&!is_wp_error($t)&&(string)($t->slug??'')===$j['slug']&&
                   html_entity_decode((string)($t->name??''),ENT_QUOTES|ENT_HTML5,'UTF-8')===$j['name'])return true;
            }
        }
        return false;
    }
    private static function rollback(array &$s):void {
        $base=get_option(self::BASE,null);
        if(!is_array($base)||($base['revision']??'')!==(string)$s['base_revision']||
            !hash_equals((string)$s['base_sha256'],hash('sha256',serialize($base))))
            throw new RuntimeException('Versicherung: geschützte Sicherung ungültig.');
        $snap=APKW_TargetTreeSync::active_snapshot();$rev=APKW_TargetTreeSync::active_revision();
        $new=self::revision((string)$s['base_revision']);
        if(!in_array($rev,[$s['base_revision'],$new],true)||
            !in_array((string)($snap['revision']??''),[$s['base_revision'],$new],true))
            throw new RuntimeException('Versicherung: fremde Revision, Rückbau blockiert.');
        if($rev!==$s['base_revision']||($snap['revision']??'')!==$s['base_revision']){
            update_option(self::SNAP,$base,false);update_option(self::REV,$s['base_revision'],false);
        }
        $n=0;while($n<self::BATCH&&$s['created']){
            $ref=end($s['created']);$id=(int)($ref['id']??0);
            if($ref['kind']==='term'){
                $obj=get_term($id,'category');
                if(!is_object($obj)||is_wp_error($obj)||(int)($obj->count??0)!==0||
                    !self::owns_created($id,'term'))
                    throw new RuntimeException('Versicherung: belegter/ungeklärter Term, Löschung untersagt.');
            }else{
                $obj=get_post($id);
                if(!is_object($obj)||!self::owns_created($id,'page'))
                    throw new RuntimeException('Versicherung: fremde Seite, Löschung untersagt.');
                $children=get_posts(['post_type'=>'any','post_status'=>'any','post_parent'=>$id,'numberposts'=>1,'fields'=>'ids']);
                if($children){
                    $mine=array_column($s['created'],'id');
                    if(array_diff($children,$mine))throw new RuntimeException('Versicherung: Seite hat fremde Kinder; Löschung untersagt.');
                }
            }
            APKW_TargetWriter::target_tree_delete_object($ref);
            array_pop($s['created']);$n++;self::save($s);
        }
        if(!$s['created']){$s['status']='ROLLED_BACK';$s['rolled_back_at_utc']=gmdate('c');self::save($s);}
    }
    public static function run_batch():array {
        if(!self::lock())throw new RuntimeException('Versicherung: Import läuft bereits.');
        try{
            $s=self::state();if(!in_array((string)($s['status']??''),['WRITING','VERIFY','ROLLBACK_PENDING'],true))return $s;
            try{
                if($s['status']==='WRITING')self::write($s);
                if($s['status']==='VERIFY')self::finish($s);
            }catch(Throwable $e){$s['error']=$e->getMessage();$s['status']='ROLLBACK_PENDING';self::save($s);}
            if($s['status']==='ROLLBACK_PENDING'){
                try{self::rollback($s);}catch(Throwable $e){$s['status']='ROLLBACK_FAILED';$s['error'].=' | Rückbau: '.$e->getMessage();self::save($s);}
            }
            return $s;
        }finally{self::unlock();}
    }
    public static function tick():void {
        try{
            if(!current_user_can('manage_options'))throw new RuntimeException('Administratorrechte erforderlich.');
            check_ajax_referer('apkw_ins_94_tick');
            $s=self::run_batch();wp_send_json_success(['status'=>$s['status']??'UNKNOWN','done'=>$s['write_index']??0,
                'total'=>self::EXPECTED,'error'=>$s['error']??'']);
        }catch(Throwable $e){wp_send_json_error(['error'=>$e->getMessage()],409);}
    }
    public static function render():void {
        if(!current_user_can('manage_options'))wp_die('Administratorrechte erforderlich.');
        $s=self::state();echo '<div class="wrap"><h1>Versicherungen – neue Kategorien</h1>';
        echo '<p>Neue Hauptseite mit 5 Bereichen, 20 gebündelten Themenseiten und 68 flachen Beitragskategorien. Bestehende Seiten, Kategorien und Beiträge bleiben unangetastet.</p>';
        if(!$s){
            try{$p=self::dry_run();echo '<p><strong>Vorschau: PASS</strong> – 26 Seiten, 68 Kategorien, null Schreibvorgänge. Ausgangsrevision geprüft.</p>';
                echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
                echo '<input type="hidden" name="action" value="apkw_ins_94_start">';
                wp_nonce_field('apkw_ins_94_start');
                echo '<p><label><input type="checkbox" name="apkw_ins_94_confirm" value="1" required> Import der 94 neuen Objekte ausdrücklich freigeben</label></p>';
                submit_button('Versicherungen zusätzlich anlegen');echo '</form>';
            }catch(Throwable $e){echo '<p><strong>BLOCKIERT:</strong> '.esc_html($e->getMessage()).'</p>';}
        }else{
            echo '<p><strong>Status:</strong> '.esc_html((string)($s['status']??''));
            echo ' | '.(int)($s['write_index']??0).' / 94 | '.esc_html((string)($s['error']??'')).'</p>';
            if(in_array((string)($s['status']??''),['WRITING','VERIFY','ROLLBACK_PENDING'],true)){
                $nonce=wp_create_nonce('apkw_ins_94_tick');
                echo '<p id="apkw-ins-result">Lauf wird in kleinen, abgesicherten Schritten fortgesetzt.</p>';
                echo '<script>(function(){var u='.json_encode(admin_url('admin-ajax.php')).';var nonce='.json_encode($nonce).';';
                echo 'function tick(){var body=new URLSearchParams({action:"apkw_ins_94_tick",_ajax_nonce:nonce});fetch(u,{method:"POST",credentials:"same-origin",body:body}).then(function(r){return r.json()}).then(function(x){if(!x.success)throw Error(x.data&&x.data.error||"Fehler");var s=x.data;document.getElementById("apkw-ins-result").textContent=s.done+" / "+s.total+" – "+s.status;if(["WRITING","VERIFY","ROLLBACK_PENDING"].includes(s.status)){tick()}else{location.reload()}}).catch(function(e){document.getElementById("apkw-ins-result").textContent="Angehalten: "+e.message+" – Seite neu laden."})}tick()})();</script>';
            }
        }
        echo '</div>';
    }
}