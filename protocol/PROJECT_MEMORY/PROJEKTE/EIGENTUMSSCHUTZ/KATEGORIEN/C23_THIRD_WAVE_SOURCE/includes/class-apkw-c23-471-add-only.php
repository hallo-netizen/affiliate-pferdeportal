<?php
if (!defined('ABSPATH')) exit;
/** C2.3 third additive wave: ONLY 471 native flat WordPress terms. Never replays 743 or 472. */
final class APKW_C23_471_AddOnly {
    private const STATE='apkw_c23_471_add_state_v1';
    private const BACKUP='apkw_c23_471_add_backup_v1';
    private const LOCK='apkw_c23_471_add_lock_v1';
    private const SNAP='apkw_target_tree_active_snapshot_v1';
    private const REV='apkw_target_tree_active_revision_v1';
    private const BATCH=20;
    private const COUNT=471;
    private static ?array $jobs=null;
    public static function init():void {
        add_action('admin_post_apkw_c23_471_start',[__CLASS__,'start']);
        add_action('wp_ajax_apkw_c23_471_tick',[__CLASS__,'tick']);
    }
    public static function state():array { $r=get_option(self::STATE,[]);return is_array($r)?$r:[]; }
    private static function save(array $r):void {update_option(self::STATE,$r,false);}
    private static function lock():bool {
        $age=(int)get_option(self::LOCK,0);
        if($age>0&&time()-$age<180)return false;
        if($age>0)delete_option(self::LOCK);
        return add_option(self::LOCK,time(),'','no');
    }
    private static function unlock():void {delete_option(self::LOCK);}
    public static function jobs():array {
        if(self::$jobs!==null)return self::$jobs;
        $fn=APKW_DIR.'profiles/hab-und-bewahr-c23-471-add-only.json';
        if(!is_readable($fn))throw new RuntimeException('C2.3: Manifestdatei fehlt.');
        $d=json_decode((string)file_get_contents($fn),true);
        if(!is_array($d)||($d['schema']??'')!=='APKW_C23_471_CATEGORY_ADD_ONLY_V1'||
           (int)($d['total']??0)!==self::COUNT||count($d['categories']??[])!==self::COUNT)
           throw new RuntimeException('C2.3: Manifest unvollständig.');
        $counts=['FAQ'=>0,'BERATUNG'=>0,'VERGLEICH'=>0,'INDIVIDUELL'=>0];$ident=[];$labels=[];$owners=[];$out=[];
        foreach($d['categories'] as $x){
            $id=(string)($x['node_id']??'');$key=(string)($x['owner_key']??'');
            $name=(string)($x['name']??'');$facet=(string)($x['facet']??'');$owner=$x['owner']??null;
            if($name===''||!is_array($owner)||!array_key_exists($facet,$counts))throw new RuntimeException('C2.3: unvollständiger Themenbezug.');
            $expected='core:c23:category:'.substr(hash('sha256',$key.'|'.$name),0,20);
            if($id!==$expected||isset($ident[$id])||isset($labels[$name]))throw new RuntimeException('C2.3: ID oder Name doppelt/falsch.');
            $ident[$id]=true;$labels[$name]=true;$counts[$facet]++;
            if(($owner['kind']??'')==='legacy'){
                if($key!=='r3-wp-page3-'.(int)($owner['physical_wp_page3_id']??0)||
                   empty($owner['expected_wp_title'])||count($owner['historical_terms']??[])<3)
                    throw new RuntimeException('C2.3: alter WP-Owner nicht sicher zugeordnet.');
            }elseif(($owner['kind']??'')==='c22'){
                if($key!=='c22-topic-index-'.(int)($owner['source_topic_index']??-1)||
                   !str_starts_with((string)($owner['node_id']??''),'core:c22:topic:'))
                    throw new RuntimeException('C2.3: neuer Themenknoten nicht gebunden.');
            }else throw new RuntimeException('C2.3: unbekannter Owner-Typ.');
            $slugLabel=(string)sanitize_title($name);
            if($slugLabel==='')$slugLabel='thema';
            $slug='c23-'.trim(substr($slugLabel,0,55),'-').'-'.substr(hash('sha256',$key.'|'.$name),0,10);
            $out[]=['node_id'=>$id,'owner_key'=>$key,'owner'=>$owner,'type'=>'category',
                'name'=>$name,'slug'=>$slug,'facet'=>$facet];
            $owners[$key]=true;
        }
        if($counts!==['FAQ'=>93,'BERATUNG'=>220,'VERGLEICH'=>91,'INDIVIDUELL'=>67]||
           count($owners)!==220||count($ident)!==self::COUNT)
            throw new RuntimeException('C2.3: Facettenzahl oder Ownerabdeckung ungültig.');
        return self::$jobs=$out;
    }
    private static function new_revision(string $base):string {
        return $base.'+C23-'.substr(hash('sha256',implode("\n",array_column(self::jobs(),'node_id'))),0,16);
    }
    /** Never calls a prior completion audit after our own completion, avoiding recursive audit loops. */
    public static function completion_audit():array {
        $s=self::state();$bad=[];
        if(($s['status']??'')!=='COMPLETE')return ['valid'=>false,'errors'=>['C23_NOT_COMPLETE']];
        $base=get_option(self::BACKUP,null);$now=APKW_TargetTreeSync::active_snapshot();
        if(!is_array($base)||!is_array($now)||
           !hash_equals((string)($s['base_sha256']??''),hash('sha256',serialize($base))))$bad[]='C23_BACKUP_INVALID';
        $target=self::new_revision((string)($s['base_revision']??''));
        if((string)APKW_TargetTreeSync::active_revision()!==$target||
           (string)($now['revision']??'')!==$target)$bad[]='C23_REVISION_MISMATCH';
        if(is_array($base)&&is_array($now)){
            $oldNodes=[];$newNodes=[];
            foreach((array)($base['nodes']??[]) as $n)if(isset($n['node_id']))$oldNodes[$n['node_id']]=$n;
            foreach((array)($now['nodes']??[]) as $n)if(isset($n['node_id']))$newNodes[$n['node_id']]=$n;
            foreach($oldNodes as $id=>$n)if(($newNodes[$id]??null)!==$n||
               (($now['mapping'][$id]??null)!==($base['mapping'][$id]??null))) {
                $bad[]='C23_OLD_NODE_CHANGED';break;
            }
            $found=0;foreach(self::jobs() as $job){
                $node=$newNodes[$job['node_id']]??null;$bind=$now['mapping'][$job['node_id']]??null;
                if(!is_array($node)||!is_array($bind)||
                   ($node['display_name']??'')!==$job['name']||($node['slug']??'')!==$job['slug']||
                   ($node['parent_id']??'')!==($s['owner_node_ids'][$job['owner_key']]??'')||
                   ($node['object_type']??'')!=='category'||
                   ($bind['object_type']??'')!=='category'||(int)($bind['object_id']??0)<1){
                   $bad[]='C23_NEW_NODE_INVALID';break;
                }$found++;
            }
            if($found!==self::COUNT)$bad[]='C23_COUNT_MISMATCH';
        }
        if(($s['result']['physical_readback']??'')!=='PASS')$bad[]='C23_PHYSICAL_READBACK_MISSING';
        return ['valid'=>!$bad,'errors'=>$bad,'revision'=>$target,'new_categories'=>self::COUNT];
    }
    public static function preflight():array {
        if(self::state())throw new RuntimeException('C2.3: Importstatus bereits vorhanden. Kein zweiter Start.');
        if(get_option(self::BACKUP,null)!==null)throw new RuntimeException('C2.3: gesicherter Lauf existiert bereits.');
        if((APKW_C22_472_AddOnly::state()['status']??'')!=='COMPLETE')
            throw new RuntimeException('C2.3: vorherige 472er-Welle nicht abgeschlossen.');
        $c22=APKW_C22_472_AddOnly::completion_audit();
        if(empty($c22['valid'])||empty($c22['new_categories'])||(int)$c22['new_categories']!==472)
            throw new RuntimeException('C2.3: vorhandener 472er-Bestand nicht vollständig bestätigt.');
        $snap=APKW_TargetTreeSync::active_snapshot();
        if(!is_array($snap)||empty($snap['nodes'])||empty($snap['mapping'])||
           ($snap['revision']??'')!==APKW_TargetTreeSync::active_revision())
            throw new RuntimeException('C2.3: ursprünglicher Snapshot/Revision nicht konsistent.');
        $idIndex=[];$nameIndex=[];$oldIdMapping=[];
        foreach($snap['nodes'] as $n)if(is_array($n)&&isset($n['node_id'])){
            $id=(string)$n['node_id'];$idIndex[$id]=$n;
            if(($n['object_type']??'')==='page'){
                $wpid=(int)($snap['mapping'][$id]['object_id']??0);
                if($wpid>0){
                    if(isset($oldIdMapping[$wpid]))throw new RuntimeException('C2.3: mehrere Parent-Seiten derselben WordPress-ID.');
                    $oldIdMapping[$wpid]=$id;
                }
            }
        }
        $ownerIds=[];$usedSlugs=[];$seenNodes=[];$checkedTerms=[];
        foreach(self::jobs() as $job){
            $owner=$job['owner'];$key=$job['owner_key'];
            if(!isset($ownerIds[$key])){
                if($owner['kind']==='legacy'){
                    $wpid=(int)$owner['physical_wp_page3_id'];$pid=$oldIdMapping[$wpid]??null;
                    if(!$pid||!str_starts_with($pid,'core:subarea:'))throw new RuntimeException('C2.3: alte physische Themenseite nicht im geschützten Zielbaum.');
                    $p=$idIndex[$pid];$expected=(string)$owner['expected_wp_title'];
                    if(($p['display_name']??'')!==$expected)throw new RuntimeException('C2.3: alte Themenseite umbenannt oder falsch zugeordnet.');
                    foreach($owner['historical_terms'] as $t){
                        $termid=(int)$t['id'];$matched=false;
                        foreach($snap['mapping'] as $nodeid=>$mapping){
                            if(($mapping['object_type']??'')==='category'&& (int)($mapping['object_id']??0)===$termid){
                                if(($idIndex[$nodeid]['display_name']??'')!==(string)$t['name']||
                                    ($idIndex[$nodeid]['slug']??'')!==(string)$t['slug'])
                                    throw new RuntimeException('C2.3: geschützte alte Kategorie geändert.');
                                $matched=true;break;
                            }
                        }
                        if(!$matched)throw new RuntimeException('C2.3: alter Kategorie-Term fehlt im Mapping.');
                        $checkedTerms[$termid]=true;
                    }
                }else{
                    $pid=(string)$owner['node_id'];$p=$idIndex[$pid]??null;
                    if(!is_array($p)||($p['object_type']??'')!=='page'||
                       ($p['display_name']??'')!==(string)$owner['subject'])
                        throw new RuntimeException('C2.3: C2.2-Themenseite nicht identisch.');
                    $wpid=(int)($snap['mapping'][$pid]['object_id']??0);
                }
                $physical=get_post($wpid);
                if(!is_object($physical)||($physical->post_type??'')!=='page'||
                   ($physical->post_status??'')!=='publish')
                   throw new RuntimeException('C2.3: Themen-Elternseite nicht veröffentlicht oder fehlt.');
                $ownerIds[$key]=$pid;
            }
            if(isset($idIndex[$job['node_id']])||isset($snap['mapping'][$job['node_id']])||isset($seenNodes[$job['node_id']]))
                throw new RuntimeException('C2.3: vorhandener oder doppelter Knoten.');
            $seenNodes[$job['node_id']]=true;$usedSlugs[]=$job['slug'];
        }
        if(count($seenNodes)!==self::COUNT||count($ownerIds)!==220||count(array_unique($usedSlugs))!==self::COUNT||
           count($checkedTerms)!==285)
            throw new RuntimeException('C2.3: alter Kategorien-/Owner-Schutz unvollständig.');
        $collision=get_terms(['taxonomy'=>'category','hide_empty'=>false,'slug'=>$usedSlugs,'number'=>1]);
        if(is_wp_error($collision)||!empty($collision))throw new RuntimeException('C2.3: bestehender WordPress-Slug bereits belegt.');
        $other=APKW_TargetTreeSync::state();
        if(in_array((string)($other['status']??''),['WRITING','READBACK','ROLLBACK_PENDING'],true))
            throw new RuntimeException('C2.3: anderer Zielbaum-Sync aktiv.');
        return ['snapshot'=>$snap,'owner_ids'=>$ownerIds,'revision'=>(string)$snap['revision'],
            'sha256'=>hash('sha256',serialize($snap)),'writes'=>0,'terms'=>self::COUNT];
    }
    public static function dry_run():array { $p=self::preflight();return ['valid'=>true,'writes'=>0,
        'new_categories'=>self::COUNT,'legacy_topic_pages'=>93,'c22_topics'=>172,
        'protected_categories'=>1323,'base_revision'=>$p['revision']]; }
    public static function start():void {
        try{
            if(!current_user_can('manage_options'))throw new RuntimeException('Administratorrechte erforderlich.');
            check_admin_referer('apkw_c23_471_start');
            if(empty($_POST['apkw_c23_471_approve']))throw new RuntimeException('C2.3: separate Freigabe fehlt.');
            if(!self::lock())throw new RuntimeException('C2.3: anderer Vorgang aktiv.');
            try{
                $p=self::preflight();update_option(self::BACKUP,$p['snapshot'],false);
                self::save(['contract'=>'HB_C23_THIRD_WAVE_471_ADD_ONLY_V1',
                    'status'=>'WRITING','base_revision'=>$p['revision'],'base_sha256'=>$p['sha256'],
                    'owner_node_ids'=>$p['owner_ids'],'write_index'=>0,'mapping'=>[],'created'=>[],
                    'error'=>'','total'=>self::COUNT,'started_at_utc'=>gmdate('c')]);
            }finally{self::unlock();}
            wp_safe_redirect(admin_url('admin.php?page=apkw-c22-kategorien&c23_471=started'));exit;
        }catch(Throwable $e){wp_die(esc_html($e->getMessage()),'C2.3 BLOCKIERT',['response'=>409]);}
    }
    private static function ensure_base(array $s):array {
        $snap=APKW_TargetTreeSync::active_snapshot();
        if((string)APKW_TargetTreeSync::active_revision()!==(string)$s['base_revision']||
           !is_array($snap)||(string)($snap['revision']??'')!==(string)$s['base_revision']||
           !hash_equals((string)$s['base_sha256'],hash('sha256',serialize($snap))))
            throw new RuntimeException('C2.3: geschützter Ausgangsstand während des Imports geändert.');
        return $snap;
    }
    private static function write(array &$s):void {
        $base=self::ensure_base($s);$jobs=self::jobs();$n=0;
        while($n<self::BATCH&&(int)$s['write_index']<self::COUNT){
            $job=$jobs[$s['write_index']];$ownerId=$s['owner_node_ids'][$job['owner_key']]??'';
            $postid=(int)($base['mapping'][$ownerId]['object_id']??0);
            if($postid<1||!isset($base['mapping'][$ownerId])||
               ($base['mapping'][$ownerId]['object_type']??'')!=='page')
                throw new RuntimeException('C2.3: Elternseiten-ID nicht konsistent.');
            $refid=APKW_TargetWriter::target_tree_insert_term('category',
                ['name'=>$job['name'],'slug'=>$job['slug'],'parent'=>0]);
            $ref=['kind'=>'term','id'=>$refid,'taxonomy'=>'category','type'=>'category','node_id'=>$job['node_id']];
            $s['created'][]=$ref;
            $s['mapping'][$job['node_id']]=['object_id'=>$refid,'object_type'=>'category',
                'adapter'=>'wordpress_taxonomy','taxonomy'=>'category'];
            // Persist physical IDs immediately before additional calls can fail.
            self::save($s);
            $meta=['_apkw_target_node_id'=>$job['node_id'],'_apkw_concept_id'=>$job['node_id'],
                '_apkw_parent_concept_id'=>$ownerId,'_apkw_target_pillar'=>'core',
                '_apkw_portal_block'=>'content','_apkw_portal_root'=>'0',
                '_apkw_target_active'=>'1','_apkw_target_revision'=>self::new_revision($s['base_revision']),
                '_apkw_seo_index_approved'=>'0'];
            foreach($meta as $k=>$v)APKW_TargetWriter::target_tree_set_meta($ref,'category',$k,$v);
            $s['write_index']++;self::save($s);$n++;
        }
        if((int)$s['write_index']===self::COUNT){$s['status']='VERIFY';self::save($s);}
    }
    private static function verify_terms(array $s):void {
        if(count($s['mapping'])!==self::COUNT||count($s['created'])!==self::COUNT)
            throw new RuntimeException('C2.3: unvollständige physische Termliste.');
        $seen=[];foreach(self::jobs() as $job){
            $id=(int)($s['mapping'][$job['node_id']]['object_id']??0);$par=$s['owner_node_ids'][$job['owner_key']]??'';
            if($id<1||isset($seen[$id]))throw new RuntimeException('C2.3: Term-ID fehlt oder doppelt.');
            $seen[$id]=true;$term=get_term($id,'category');$url=get_term_link($id,'category');
            if(!is_object($term)||is_wp_error($term)||($term->taxonomy??'')!=='category'||
               (string)($term->slug??'')!==$job['slug']||(int)($term->parent??-1)!==0||
               is_wp_error($url)||!is_string($url)||$url===''||
               get_term_meta($id,'_apkw_target_node_id',true)!==$job['node_id']||
               get_term_meta($id,'_apkw_parent_concept_id',true)!==$par)
                throw new RuntimeException('C2.3: WordPress-Term/Metadaten fehlerhaft.');
            $actual=function_exists('wp_specialchars_decode')?wp_specialchars_decode((string)$term->name,ENT_QUOTES)
                :html_entity_decode((string)$term->name,ENT_QUOTES|ENT_HTML5,'UTF-8');
            if($actual!==$job['name'])throw new RuntimeException('C2.3: WordPress-Kategoriename nicht identisch.');
        }
    }
    private static function finish(array &$s):void {
        $base=self::ensure_base($s);self::verify_terms($s);$stage=$base;
        $found=[];foreach($stage['nodes'] as $node)$found[$node['node_id']]=true;
        foreach(self::jobs() as $job){
            if(isset($found[$job['node_id']]))throw new RuntimeException('C2.3: bestehende Knoten-ID blockiert.');
            $found[$job['node_id']]=true;$parent=$s['owner_node_ids'][$job['owner_key']];
            $stage['nodes'][]=['node_id'=>$job['node_id'],'pillar'=>'core',
                'object_type'=>'category','parent_id'=>$parent,'display_name'=>$job['name'],
                'slug'=>$job['slug'],'status'=>'active','seo_owner'=>false,'seo_seed'=>'',
                'intent_key'=>'','primary_keyword'=>'','c23_category_only'=>true];
            $stage['mapping'][$job['node_id']]=$s['mapping'][$job['node_id']];
        }
        $stage['revision']=self::new_revision($s['base_revision']);
        $stage['project']['c23_extra_471_applied_at_utc']=gmdate('c');
        $stage['completed_at_utc']=gmdate('c');
        $before=APKW_FinalTargetAdmin::frontend_readback($stage);
        if(empty($before['valid']))throw new RuntimeException('C2.3: Stage-Frontend-Readback blockiert: '.implode(',',(array)($before['errors']??[])));
        update_option(self::SNAP,$stage,false);update_option(self::REV,$stage['revision'],false);
        if(APKW_TargetTreeSync::active_revision()!==$stage['revision'])throw new RuntimeException('C2.3: neue Revision nicht lesbar.');
        $after=APKW_FinalTargetAdmin::frontend_readback();
        if(empty($after['valid']))throw new RuntimeException('C2.3: finale Frontendprüfung fehlgeschlagen.');
        if(class_exists('APKW_FrontendStructure'))APKW_FrontendStructure::invalidate_cache();
        $s['status']='COMPLETE';$s['completed_at_utc']=gmdate('c');
        $s['result']=['new_categories'=>self::COUNT,'protected_previous_wp_categories'=>1323,
            'physical_readback'=>'PASS'];self::save($s);
    }
    private static function rollback(array &$s):void {
        $old=get_option(self::BACKUP,null);
        if(!is_array($old)||(string)($old['revision']??'')!==(string)$s['base_revision']||
           !hash_equals((string)$s['base_sha256'],hash('sha256',serialize($old))))
            throw new RuntimeException('C2.3: ursprüngliches Backup nicht identisch.');
        $current=APKW_TargetTreeSync::active_snapshot();$rev=APKW_TargetTreeSync::active_revision();
        $newrev=self::new_revision((string)$s['base_revision']);
        if(!in_array($rev,[$s['base_revision'],$newrev],true)||
           !in_array((string)($current['revision']??''),[$s['base_revision'],$newrev],true))
            throw new RuntimeException('C2.3: fremde Revision, sicherer Rückbau gesperrt.');
        if($rev!==$s['base_revision']||($current['revision']??'')!==$s['base_revision']){
            update_option(self::SNAP,$old,false);update_option(self::REV,$s['base_revision'],false);
        }
        $n=0;while($n<self::BATCH&&!empty($s['created'])){
            $ref=end($s['created']);$term=get_term((int)$ref['id'],'category');
            if(!is_object($term)||is_wp_error($term)||(int)$term->count!==0||
               (string)get_term_meta((int)$ref['id'],'_apkw_target_node_id',true)!==$ref['node_id'])
                throw new RuntimeException('C2.3: kein Rückbau eines fehlenden/fremd belegten Terms.');
            APKW_TargetWriter::target_tree_delete_object($ref);array_pop($s['created']);$n++;self::save($s);
        }
        if(empty($s['created'])){$s['status']='ROLLED_BACK';$s['completed_at_utc']=gmdate('c');self::save($s);}
    }
    public static function run_batch():array {
        if(!self::lock())return self::state();
        try{
            $s=self::state();if(!in_array(($s['status']??''),['WRITING','VERIFY','ROLLBACK'],true))return $s;
            try{
                if($s['status']==='WRITING')self::write($s);
                elseif($s['status']==='VERIFY')self::finish($s);
                else self::rollback($s);
            }catch(Throwable $e){
                $s['status']=($s['status']==='ROLLBACK')?'ROLLBACK_FAILED':'ROLLBACK';
                $s['error']=trim(($s['error']??'').' | '.$e->getMessage(),' |');self::save($s);
            }
            return $s;
        }finally{self::unlock();}
    }
    public static function tick():void {
        try{
            if(!current_user_can('manage_options'))throw new RuntimeException('Administrator erforderlich.');
            check_ajax_referer('apkw_c23_471_tick','nonce');$s=self::run_batch();
            wp_send_json_success(['status'=>$s['status']??'NOT_STARTED','written'=>(int)($s['write_index']??0),
                'total'=>self::COUNT,'error'=>$s['error']??'']);
        }catch(Throwable $e){wp_send_json_error(['error'=>$e->getMessage()],409);}
    }
    public static function render_controls():void {
        echo '<hr><h2>C2.3 – 471 fehlende vertiefende Artikelkategorien</h2>';
        echo '<p>Alle 265 Themenseiten wurden individuell geprüft. FAQ und Beratung für alle, Vergleiche sowie Wartung/Kosten nur bei eigenständigem Sinn. Bestehende 743 + 472 Importobjekte und 285 alte Terms bleiben erhalten. Keine Artikel.</p>';
        $s=self::state();$status=$s['status']??'';
        if($status==='COMPLETE'){
            $audit=self::completion_audit();
            if(!empty($audit['valid']))echo '<div class="notice notice-success inline"><p>471 Ergänzungen abgeschlossen und geprüft.</p></div>';
            else echo '<div class="notice notice-error inline"><p>C2.3-Abschluss nicht mehr konsistent. Bitte keinen Import wiederholen.</p></div>';
            return;
        }
        if(in_array($status,['ROLLED_BACK','ROLLBACK_FAILED'],true)){
            echo '<div class="notice notice-error inline"><p>Import gestoppt: '.esc_html($s['error']??$status).'. Kein automatischer Neustart.</p></div>';return;
        }
        if(in_array($status,['WRITING','VERIFY','ROLLBACK'],true)){
            echo '<p id="apkw-c23-471-progress">Kontrollierte Übernahme: '.esc_html((string)($s['write_index']??0)).' / 471</p>';
            $ajax=esc_url(admin_url('admin-ajax.php'));$nonce=wp_create_nonce('apkw_c23_471_tick');
            echo '<script>(function(){let a='.json_encode($ajax).',n='.json_encode($nonce).';async function tick(){try{let body=new URLSearchParams({action:"apkw_c23_471_tick",nonce:n});let r=await fetch(a,{method:"POST",credentials:"same-origin",body});let o=await r.json();if(!r.ok||!o.success)throw Error(o.data?.error||"Fehler");let d=o.data;document.getElementById("apkw-c23-471-progress").textContent=d.status+" · "+d.written+" / "+d.total+(d.error?" · "+d.error:"");if(["COMPLETE","ROLLED_BACK","ROLLBACK_FAILED"].includes(d.status)){location.reload();return;}setTimeout(tick,500);}catch(e){document.getElementById("apkw-c23-471-progress").textContent="Pausiert: "+e.message+". Zum Fortsetzen Seite neu laden.";}}tick()})();</script>';return;
        }
        try{
            $check=self::dry_run();echo '<p><strong>Vorschau ohne Schreibzugriff:</strong> 471 neue Kategorien für 93 ältere und 172 neue Themenseiten; bereits vorhandene 1.323 Kategorien geschützt. Revision: '.esc_html($check['base_revision']).'.</p>';
        }catch(Throwable $e){echo '<div class="notice notice-error inline"><p>Freigabe gesperrt: '.esc_html($e->getMessage()).'</p></div>';return;}
        echo '<form action="'.esc_url(admin_url('admin-post.php')).'" method="post"><input type="hidden" name="action" value="apkw_c23_471_start">';
        wp_nonce_field('apkw_c23_471_start');
        echo '<p><label><input type="checkbox" name="apkw_c23_471_approve" value="1" required> Ich gebe ausschließlich die 471 neuen C2.3-Kategorien frei.</label></p>';
        submit_button('471 fehlende Kategorien ergänzen','primary');echo '</form>';
    }
}
