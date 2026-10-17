<?php
if (!defined('ABSPATH')) exit;
/**
 * C2.2 second wave: precisely 472 additional, FLAT native WordPress categories.
 * Uses only the existing APKW TargetWriter, never replays the original 743 jobs.
 * No posts, pages or existing terms are created, edited or unlinked by this class.
 */
final class APKW_C22_472_AddOnly {
    private const STATE='apkw_c22_472_second_wave_state_v1';
    private const BACKUP='apkw_c22_472_second_wave_base_v1';
    private const LOCK='apkw_c22_472_second_wave_lock_v1';
    private const SNAP='apkw_target_tree_active_snapshot_v1';
    private const REV='apkw_target_tree_active_revision_v1';
    private const BATCH=20;
    private static ?array $jobs=null;
    public static function init():void {
        add_action('admin_post_apkw_c22_472_start',[__CLASS__,'start']);
        add_action('wp_ajax_apkw_c22_472_tick',[__CLASS__,'tick']);
    }
    public static function state():array { $s=get_option(self::STATE,[]);return is_array($s)?$s:[]; }
    public static function active():bool {
        return in_array((string)(self::state()['status']??''),['WRITING','VERIFY','ROLLBACK','ROLLBACK_FAILED'],true);
    }
    private static function save(array $s):void { update_option(self::STATE,$s,false); }
    private static function lock():bool {
        $last=(int)get_option(self::LOCK,0);
        if($last>0&&time()-$last<180)return false;
        if($last>0)delete_option(self::LOCK);
        return add_option(self::LOCK,time(),'','no');
    }
    private static function unlock():void {delete_option(self::LOCK);}
    private static function original():array {
        $check=APKW_C22_AddOnly::completion_audit();
        if(empty($check['valid'])||!empty($check['errors'])||(int)($check['new_objects_verified_in_snapshot']??0)!==743)
            throw new RuntimeException('472: ursprüngliche 743 C2.2-Objekte nicht eindeutig vollständig abgeschlossen.');
        $snapshot=APKW_TargetTreeSync::active_snapshot();
        if(!is_array($snapshot)||!is_array($snapshot['nodes']??null)||!is_array($snapshot['mapping']??null)||
           (string)($snapshot['revision']??'')===''||
           (string)$snapshot['revision']!==(string)APKW_TargetTreeSync::active_revision())
            throw new RuntimeException('472: aktiver Snapshot oder Revision unvollständig.');
        return $snapshot;
    }
    public static function jobs():array {
        if(self::$jobs!==null)return self::$jobs;
        $file=APKW_DIR.'profiles/hab-und-bewahr-c22-472-add-only.json';
        if(!is_readable($file))throw new RuntimeException('472: Add-only-Manifest fehlt.');
        $data=json_decode((string)file_get_contents($file),true);
        if(!is_array($data)||($data['schema']??'')!=='APKW_C22_SECOND_WAVE_CATEGORY_ONLY_V1'||
           (int)($data['counts']['categories']??0)!==472||count($data['categories']??[])!==472)
            throw new RuntimeException('472: unvollständiges Manifest.');
        $seen=[];$owners=[];$kinds=['FAQ'=>0,'VERGLEICH'=>0,'OPTIONAL'=>0,'NEUER_BEREICH'=>0];$jobs=[];
        foreach($data['categories'] as $cat){
            $full=(string)($cat['full_path']??'');$label=(string)($cat['name']??'');
            $parts=explode('|',$full);$kind=(string)($cat['intent']??'');
            if(count($parts)!==4||$label===''||$parts[3]!==$label||!array_key_exists($kind,$kinds))
                throw new RuntimeException('472: Kategorie-Eintrag unvollständig.');
            $parent='core:c22:topic:'.substr(hash('sha256',implode('|',array_slice($parts,0,3))),0,20);
            $id='core:c22:category:'.substr(hash('sha256',$full),0,20);
            if($id!==($cat['node_id']??'')||$parent!==($cat['parent_id']??'')||isset($seen[$id]))
                throw new RuntimeException('472: Kategorie-Identität/Kollision.');
            $seen[$id]=true;$owners[$parent]=true;$kinds[$kind]++;
            $slugText=(string)sanitize_title($label);
            if($slugText==='')$slugText='thema';
            $slug='c22-'.trim(substr($slugText,0,55),'-').'-'.substr(hash('sha256',$full),0,10);
            $jobs[]=['node_id'=>$id,'parent_id'=>$parent,'type'=>'category','name'=>$label,'slug'=>$slug];
        }
        if(count($seen)!==472||count($owners)!==172||$kinds!==['FAQ'=>172,'VERGLEICH'=>172,'OPTIONAL'=>102,'NEUER_BEREICH'=>26])
            throw new RuntimeException('472: Themenabdeckung oder Kategorienanzahlen ungültig.');
        return self::$jobs=$jobs;
    }
    /** Post-completion integrity check; recognizes the second-wave revision. */
    public static function completion_audit():array {
        $state=self::state();$errors=[];
        if(($state['status']??'')!=='COMPLETE')return ['valid'=>false,'errors'=>['SECOND_WAVE_NOT_COMPLETE']];
        $backup=get_option(self::BACKUP,null);
        $snap=APKW_TargetTreeSync::active_snapshot();
        $rev=self::new_revision((string)($state['base_revision']??''));
        if(!is_array($backup)||!hash_equals((string)($state['base_sha256']??''),hash('sha256',serialize($backup))))
            $errors[]='SECOND_WAVE_BACKUP_MISMATCH';
        if((string)APKW_TargetTreeSync::active_revision()!==$rev||(string)($snap['revision']??'')!==$rev)
            $errors[]='SECOND_WAVE_REVISION_MISMATCH';
        if(is_array($backup)){
            $oldIdx=[];$nowIdx=[];
            foreach((array)($backup['nodes']??[]) as $node)if(is_array($node)&&isset($node['node_id']))$oldIdx[$node['node_id']]=$node;
            foreach((array)($snap['nodes']??[]) as $node)if(is_array($node)&&isset($node['node_id']))$nowIdx[$node['node_id']]=$node;
            foreach($oldIdx as $id=>$old)if(($nowIdx[$id]??null)!==$old ||
               ($backup['mapping'][$id]??null)!==($snap['mapping'][$id]??null)){
                $errors[]='SECOND_WAVE_PROTECTED_CHANGED:'.$id;break;
            }
        }
        $found=0;
        foreach(self::jobs() as $job){
            $id=$job['node_id'];$node=null;
            foreach((array)($snap['nodes']??[]) as $n)if(($n['node_id']??'')===$id){$node=$n;break;}
            if(!is_array($node)||($node['parent_id']??'')!==$job['parent_id']||
               ($node['display_name']??'')!==$job['name']||($node['slug']??'')!==$job['slug']||
               ($node['object_type']??'')!=='category'||
               ($snap['mapping'][$id]['object_type']??'')!=='category'||
               (int)($snap['mapping'][$id]['object_id']??0)<1){
                $errors[]='SECOND_WAVE_MAPPING_MISSING:'.$id;break;
            }
            $found++;
        }
        if($found!==472)$errors[]='SECOND_WAVE_INCOMPLETE';
        if(($state['result']['frontend_readback']??'')!=='PASS')$errors[]='SECOND_WAVE_PHYSICAL_READBACK_MISSING';
        return ['valid'=>!$errors,'revision'=>$rev,'new_categories'=>$found,'errors'=>$errors];
    }
    public static function preflight():array {
        if((self::state()['status']??'')==='COMPLETE')throw new RuntimeException('472: bereits abgeschlossen, kein erneuter Import.');
        if(get_option(self::BACKUP,null)!==null)throw new RuntimeException('472: vorhandener Sicherungsstand; kein zweiter Lauf.');
        $base=self::original();$jobs=self::jobs();
        $by=[];foreach($base['nodes'] as $node)if(is_array($node)&&isset($node['node_id']))$by[(string)$node['node_id']]=$node;
        $mapping=$base['mapping'];$taken=[];$slugs=[];
        foreach($jobs as $job){
            $parent=$by[$job['parent_id']]??null;
            if(!is_array($parent)||($parent['object_type']??'')!=='page'||
               !str_starts_with($job['parent_id'],'core:c22:topic:')||
               ($mapping[$job['parent_id']]['object_type']??'')!=='page'||
               (int)($mapping[$job['parent_id']]['object_id']??0)<1)
                throw new RuntimeException('472: zugehörige echte C2.2-Themenseite fehlt: '.$job['name']);
            if(isset($by[$job['node_id']])||isset($mapping[$job['node_id']]))
                throw new RuntimeException('472: bereits vorhandene Knoten-ID (niemals überschreiben).');
            $taken[$job['node_id']]=true;$slugs[]=$job['slug'];
        }
        if(count($taken)!==472||count(array_unique($slugs))!==472)
            throw new RuntimeException('472: doppelte Kategorie-IDs oder URL-Slugs.');
        // A single bounded query; never scan individual categories on every browser tick.
        $collision=get_terms(['taxonomy'=>'category','hide_empty'=>false,'slug'=>$slugs,'number'=>1]);
        if(is_wp_error($collision)||!empty($collision))throw new RuntimeException('472: mindestens ein Ziel-Slug ist bereits belegt.');
        if(APKW_C22_AddOnly::owns_runtime() && (APKW_C22_AddOnly::state()['status']??'')!=='COMPLETE')
            throw new RuntimeException('472: erste Importwelle nicht abgeschlossen.');
        $other=APKW_TargetTreeSync::state();
        if(in_array((string)($other['status']??''),['WRITING','READBACK','ROLLBACK_PENDING'],true))
            throw new RuntimeException('472: anderer Zielbaum-Sync läuft.');
        return ['revision'=>(string)$base['revision'],'snapshot'=>$base,
            'sha256'=>hash('sha256',serialize($base)),'total'=>count($jobs),
            'topics'=>172,'protected_c22_objects'=>743,'protected_historical_terms'=>285];
    }
    private static function ensure_base(array $s):array {
        $snap=APKW_TargetTreeSync::active_snapshot();
        if((string)APKW_TargetTreeSync::active_revision()!==(string)$s['base_revision']||
           (string)($snap['revision']??'')!==(string)$s['base_revision']||
           !hash_equals((string)$s['base_sha256'],hash('sha256',serialize($snap))))
            throw new RuntimeException('472: bestehender aktiver Zielbaum hat sich verändert.');
        return $snap;
    }
    public static function dry_run():array {
        $x=self::preflight();return ['valid'=>true,'writes'=>0,'new_categories'=>472,'protected_existing_objects'=>743,
            'protected_old_categories'=>285,'topic_pages'=>172,'base_revision'=>$x['revision']];
    }
    public static function start():void {
        try{
            if(!current_user_can('manage_options'))throw new RuntimeException('472: Administrator erforderlich.');
            check_admin_referer('apkw_c22_472_start');
            if(empty($_POST['apkw_c22_472_approve']))throw new RuntimeException('472: ausdrückliche Freigabe fehlt.');
            if(!self::lock())throw new RuntimeException('472: ein weiterer Vorgang ist aktiv.');
            try{
                if(self::state())throw new RuntimeException('472: vorhandener Status, kein automatischer Neustart.');
                $p=self::preflight();
                update_option(self::BACKUP,$p['snapshot'],false);
                $s=['contract'=>'HB_C22_SECOND_WAVE_472_ADD_ONLY_V1','status'=>'WRITING',
                    'base_revision'=>$p['revision'],'base_sha256'=>$p['sha256'],
                    'write_index'=>0,'mapping'=>[],'created'=>[],'error'=>'',
                    'total'=>472,'started_at_utc'=>gmdate('c')];self::save($s);
            }finally{self::unlock();}
            wp_safe_redirect(admin_url('admin.php?page=apkw-c22-kategorien&c22_472=started'));exit;
        }catch(Throwable $e){wp_die(esc_html($e->getMessage()),'472 BLOCKED',['response'=>409]);}
    }
    private static function new_revision(string $old):string {
        return $old.'+C22X-'.substr(hash('sha256',implode("\n",array_column(self::jobs(),'node_id'))),0,16);
    }
    private static function write(array &$s):void {
        $base=self::ensure_base($s);$jobs=self::jobs();$n=0;
        while($n<self::BATCH&&(int)$s['write_index']<count($jobs)){
            $job=$jobs[$s['write_index']];
            $parent=(int)($base['mapping'][$job['parent_id']]['object_id']??0);
            $p=$parent>0?get_post($parent):null;
            if(!is_object($p)||($p->post_type??'')!=='page'||($p->post_status??'')!=='publish')
                throw new RuntimeException('472: unveränderte Eltern-Themenseite physisch ungültig.');
            $id=APKW_TargetWriter::target_tree_insert_term('category',
                ['name'=>$job['name'],'slug'=>$job['slug'],'parent'=>0]);
            $ref=['kind'=>'term','id'=>$id,'taxonomy'=>'category','type'=>'category','node_id'=>$job['node_id']];
            $s['created'][]=$ref;
            $s['mapping'][$job['node_id']]=['object_id'=>$id,'object_type'=>'category',
                'adapter'=>'wordpress_taxonomy','taxonomy'=>'category'];
            // Persist actual created physical ID BEFORE writing metadata.
            self::save($s);
            $meta=['_apkw_target_node_id'=>$job['node_id'],
                '_apkw_concept_id'=>$job['node_id'],'_apkw_parent_concept_id'=>$job['parent_id'],
                '_apkw_target_pillar'=>'core','_apkw_portal_block'=>'content',
                '_apkw_portal_root'=>'0','_apkw_target_active'=>'1',
                '_apkw_target_revision'=>self::new_revision($s['base_revision']),
                '_apkw_seo_index_approved'=>'0'];
            foreach($meta as $k=>$v)APKW_TargetWriter::target_tree_set_meta($ref,'category',$k,$v);
            $s['write_index']++;self::save($s);$n++;
        }
        if($s['write_index']===472){$s['status']='VERIFY';self::save($s);}
    }
    private static function verify_terms(array $s):void {
        if(count($s['mapping'])!==472||count($s['created'])!==472)
            throw new RuntimeException('472: physische Term-Zuordnung nicht vollständig.');
        $seen=[];foreach(self::jobs() as $job){
            $id=(int)($s['mapping'][$job['node_id']]['object_id']??0);
            if($id<1||isset($seen[$id]))throw new RuntimeException('472: fehlende/doppelte physische WordPress-Term-ID.');
            $seen[$id]=true;$term=get_term($id,'category');
            if(!is_object($term)||is_wp_error($term)||($term->taxonomy??'')!=='category'||
               (string)($term->slug??'')!==$job['slug']||(int)($term->parent??-1)!==0)
                throw new RuntimeException('472: WordPress-Term ist nicht flach oder hat falschen Slug.');
            $name=function_exists('wp_specialchars_decode')?wp_specialchars_decode((string)$term->name,ENT_QUOTES):html_entity_decode((string)$term->name,ENT_QUOTES|ENT_HTML5,'UTF-8');
            $link=get_term_link($id,'category');
            if($name!==$job['name']||get_term_meta($id,'_apkw_parent_concept_id',true)!==$job['parent_id']||
               get_term_meta($id,'_apkw_target_node_id',true)!==$job['node_id']||
               is_wp_error($link)||!is_string($link)||$link==='')
                throw new RuntimeException('472: WordPress-Identität, Zuordnung oder URL fehlerhaft.');
        }
    }
    private static function finish(array &$s):void {
        $base=self::ensure_base($s);self::verify_terms($s);$stage=$base;
        $index=[];foreach($stage['nodes'] as $node)$index[$node['node_id']]=true;
        foreach(self::jobs() as $job){
            if(isset($index[$job['node_id']]))throw new RuntimeException('472: kein ADD-only wegen Knoten-Kollision.');
            $index[$job['node_id']]=true;
            $stage['nodes'][]=['node_id'=>$job['node_id'],'pillar'=>'core','object_type'=>'category',
                'parent_id'=>$job['parent_id'],'display_name'=>$job['name'],'slug'=>$job['slug'],
                'status'=>'active','seo_owner'=>false,'seo_seed'=>'','intent_key'=>'',
                'primary_keyword'=>'','c22_category_only'=>true];
            $stage['mapping'][$job['node_id']]=$s['mapping'][$job['node_id']];
        }
        $stage['revision']=self::new_revision($s['base_revision']);
        $stage['project']['c22_extra_472_applied_at_utc']=gmdate('c');
        $stage['completed_at_utc']=gmdate('c');
        $test=APKW_FinalTargetAdmin::frontend_readback($stage);
        if(empty($test['valid']))throw new RuntimeException('472: vollständige Frontend-Readbackprüfung fehlgeschlagen: '.implode(',',(array)($test['errors']??[])));
        update_option(self::SNAP,$stage,false);update_option(self::REV,$stage['revision'],false);
        if(APKW_TargetTreeSync::active_revision()!==$stage['revision'])throw new RuntimeException('472: neue Revision nach Übernahme nicht lesbar.');
        $final=APKW_FinalTargetAdmin::frontend_readback();
        if(empty($final['valid']))throw new RuntimeException('472: finale Frontend-Struktur nicht gültig.');
        if(class_exists('APKW_FrontendStructure'))APKW_FrontendStructure::invalidate_cache();
        $s['status']='COMPLETE';$s['completed_at_utc']=gmdate('c');
        $s['result']=['new_categories'=>472,'protected_c22_objects'=>743,
            'protected_old_categories'=>285,'frontend_readback'=>'PASS'];self::save($s);
    }
    private static function rollback(array &$s):void {
        $backup=get_option(self::BACKUP,null);
        if(!is_array($backup)||($backup['revision']??'')!==$s['base_revision']||
           !hash_equals((string)$s['base_sha256'],hash('sha256',serialize($backup))))
            throw new RuntimeException('472: Backup entspricht nicht dem unveränderten Ausgangsstand.');
        $rev=APKW_TargetTreeSync::active_revision();
        if(!in_array($rev,[$s['base_revision'],self::new_revision($s['base_revision'])],true))
            throw new RuntimeException('472: fremde Revision; kein ungesicherter Rückbau.');
        // Both option writes are independent; recover a crash between SNAP and REV.
        $current=APKW_TargetTreeSync::active_snapshot();
        $actual=(string)($current['revision']??'');
        if(!in_array($actual,[$s['base_revision'],self::new_revision($s['base_revision'])],true))
            throw new RuntimeException('472: fremder Snapshot; keine automatische Reparatur.');
        if($rev!==$s['base_revision']||$actual!==$s['base_revision']){
            update_option(self::SNAP,$backup,false);update_option(self::REV,$s['base_revision'],false);
        }
        $n=0;while($n<self::BATCH&&!empty($s['created'])){
            $ref=end($s['created']);$term=get_term((int)$ref['id'],'category');
            if(!is_object($term)||is_wp_error($term)||(int)$term->count!==0||
               (string)get_term_meta((int)$ref['id'],'_apkw_target_node_id',true)!==$ref['node_id'])
                throw new RuntimeException('472: neuer Term belegt, fremd verändert oder fehlt; kein Löschen.');
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
                if($s['status']==='ROLLBACK')$s['status']='ROLLBACK_FAILED';else $s['status']='ROLLBACK';
                $s['error']=trim(($s['error']??'').' | '.$e->getMessage(),' |');self::save($s);
            }
            return $s;
        }finally{self::unlock();}
    }
    public static function tick():void {
        try{if(!current_user_can('manage_options'))throw new RuntimeException('Administrator erforderlich.');
            check_ajax_referer('apkw_c22_472_tick','nonce');$s=self::run_batch();
            wp_send_json_success(['status'=>$s['status']??'NOT_STARTED','written'=>(int)($s['write_index']??0),
                'total'=>472,'error'=>$s['error']??'']);
        }catch(Throwable $e){wp_send_json_error(['error'=>$e->getMessage()],409);}
    }
    public static function render_controls():void {
        echo '<hr><h2>C2.2 – zweite Ergänzungswelle (472 zusätzliche Artikelkategorien)</h2>';
        echo '<p>Nur zusätzliche flache WordPress-Kategorien. Die ursprünglichen 743 C2.2-Objekte und der historische Bestand werden nicht erneut importiert oder geändert. Keine Artikel.</p>';
        $s=self::state();$status=$s['status']??'';
        if($status==='COMPLETE'){echo '<div class="notice notice-success inline"><p>472 Ergänzungen abgeschlossen und geprüft.</p></div>';return;}
        if($status==='ROLLED_BACK'||$status==='ROLLBACK_FAILED'){
            echo '<div class="notice notice-error inline"><p>Import angehalten: '.esc_html($s['error']??$status).'. Kein automatischer Neustart.</p></div>';return;
        }
        if(in_array($status,['WRITING','VERIFY','ROLLBACK'],true)){
            echo '<p id="apkw-c22-472-progress">Kontrollierte Übernahme: '.esc_html((string)($s['write_index']??0)).' / 472</p>';
            $ajax=esc_url(admin_url('admin-ajax.php'));$nonce=wp_create_nonce('apkw_c22_472_tick');
            echo '<script>(function(){let a='.json_encode($ajax).',n='.json_encode($nonce).';async function tick(){try{let body=new URLSearchParams({action:"apkw_c22_472_tick",nonce:n});let r=await fetch(a,{method:"POST",credentials:"same-origin",body});let o=await r.json();if(!r.ok||!o.success)throw new Error(o.data?.error||"Fehler");let d=o.data;document.getElementById("apkw-c22-472-progress").textContent=d.status+" · "+d.written+" / "+d.total+(d.error?" · "+d.error:"");if(["COMPLETE","ROLLED_BACK","ROLLBACK_FAILED"].includes(d.status)){location.reload();return;}setTimeout(tick,500);}catch(e){document.getElementById("apkw-c22-472-progress").textContent="Pausiert: "+e.message+". Zum Fortsetzen Seite neu laden.";}}tick()})();</script>';
            return;
        }
        try{$check=self::dry_run();echo '<p><strong>Vorschau ohne Schreibzugriff:</strong> 472 neue Kategorien unter 172 bestehenden Themen; ursprüngliche 743 Objekte und 285 historische Kategorien geschützt. Revision: '.esc_html($check['base_revision']).'.</p>';}
        catch(Throwable $e){echo '<div class="notice notice-error inline"><p>Freigabe gesperrt: '.esc_html($e->getMessage()).'</p></div>';return;}
        echo '<form action="'.esc_url(admin_url('admin-post.php')).'" method="post"><input type="hidden" name="action" value="apkw_c22_472_start">';
        wp_nonce_field('apkw_c22_472_start');
        echo '<p><label><input type="checkbox" name="apkw_c22_472_approve" value="1" required> Ich gebe ausschließlich den ADD-only-Import der 472 neuen Kategorien frei.</label></p>';
        submit_button('472 neue Kategorien ergänzen','primary');echo '</form>';
    }
}