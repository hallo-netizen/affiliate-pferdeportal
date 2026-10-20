<?php
if (!defined('ABSPATH')) exit;
/** C2.6 – strictly additive last-level insurance categories, no new pages or hierarchy. */
final class APKW_Insurance_C26_Depth {
    private const STATE='apkw_ins_c26_depth_state_v1';
    private const BACKUP='apkw_ins_c26_depth_base_v1';
    private const LOCK='apkw_ins_c26_depth_lock_v1';
    private const SNAP='apkw_target_tree_active_snapshot_v1';
    private const REV='apkw_target_tree_active_revision_v1';
    private const PAGE='apkw-insurance-c26-depth';
    private const BATCH=15;
    private static ?array $profile=null;
    public static function init():void {
        add_action('admin_menu',[__CLASS__,'menu'],42);
        add_action('admin_post_apkw_ins_c26_start',[__CLASS__,'start']);
        add_action('wp_ajax_apkw_ins_c26_tick',[__CLASS__,'tick']);
    }
    public static function menu():void {
        add_submenu_page(APKW_FinalTargetAdmin::PAGE_SLUG,'Versicherungen – Unterkategorien','Versicherungen vertiefen','manage_options',self::PAGE,[__CLASS__,'render']);
    }
    public static function state():array {
        $s=get_option(self::STATE,[]);return is_array($s)?$s:[];
    }
    private static function save(array $s):void {update_option(self::STATE,$s,false);}
    private static function profile():array {
        if(self::$profile!==null)return self::$profile;
        $file=APKW_DIR.'profiles/hab-und-bewahr-insurance-c26-end-categories.json';
        if(!is_readable($file)||hash_file('sha256',$file)!=='4b1d2f5a85bf9e27d1f56cbbbd92f15ad5f6cece529a07d1e44c20c934e06b72')
            throw new RuntimeException('Versicherungstiefe: Original-Profil fehlt oder wurde verändert.');
        $x=json_decode((string)file_get_contents($file),true);
        if(!is_array($x)||($x['schema']??'')!=='HAB_INSURANCE_C26_END_CATEGORIES_ADD_ONLY_V1')
            throw new RuntimeException('Versicherungstiefe: Profilformat ungültig.');
        $jobs=$x['new_categories']??[];$owners=$x['owner_individual_audit']??[];
        if(count($jobs)!==185||count($owners)!==46||
            (int)($x['counts']['new_pages']??-1)!==0||
            (int)($x['counts']['new_hierarchy_layers']??-1)!==0)
            throw new RuntimeException('Versicherungstiefe: Profilumfang/Seitenvertrag verletzt.');
        $seen=[];$names=[];$ownerCount=[];
        foreach($jobs as $j){
            $nid=(string)($j['node_id']??'');$slug=(string)($j['slug']??'');$name=(string)($j['name']??'');
            $parent=(string)($j['parent_key']??'');
            if(!$nid||!str_starts_with($nid,'core:leaf:insurance-extra:')||
               !$slug||!str_starts_with($slug,'vs-')||!$name||
               !$parent||!str_starts_with($parent,'INS-SEO:R3:')||
               isset($seen[$nid])||isset($seen['slug:'.$slug])||isset($names[$name])||
               ($j['taxonomy']??'')!=='category'||(int)($j['wordpress_parent']??-1)!==0||
               count(array_unique((array)($j['coarse_independent_directions']??[])))<3)
                throw new RuntimeException('Versicherungstiefe: letzter Kategorie-Owner oder Intent ungültig.');
            $seen[$nid]=true;$seen['slug:'.$slug]=true;$names[$name]=true;
            $ownerCount[$parent]=1+($ownerCount[$parent]??0);
        }
        $seo=self::seo_profile();$r3=[];
        foreach($seo['pages'] as $p)if(($p['level']??'')==='R3')$r3[$p['key']]=(string)$p['title'];
        if(count($ownerCount)!==46||count($r3)!==46||
           array_diff(array_keys($ownerCount),array_keys($r3))||
           array_diff(array_keys($r3),array_keys($ownerCount)))
            throw new RuntimeException('Versicherungstiefe: nicht alle 46 konkreten Versicherungen geprüft.');
        foreach($owners as $o){
            $title=(string)($o['topic']??'');
            if(!in_array($title,$r3,true)||!($o['contains_faq']??false)||!($o['contains_beratung']??false)||
               (int)($o['added']??-1)<1)
                throw new RuntimeException('Versicherungstiefe: R3-Fachprüfung fehlt.');
        }
        return self::$profile=$x;
    }
    private static function seo_profile():array {
        $file=APKW_DIR.'profiles/hab-und-bewahr-insurance-seo-repair.json';
        if(!is_readable($file)||hash_file('sha256',$file)!=='0a12b72d85e66cb04e3dcf223356698650c86d8b2dc39d4dd310fa2ac00a6c41')
            throw new RuntimeException('Versicherungstiefe: abgeschlossene SEO-Keyword-Quelle stimmt nicht überein.');
        $p=json_decode((string)file_get_contents($file),true);
        if(!is_array($p)||count($p['pages']??[])!==52||count($p['flat_categories']??[])!==138)
            throw new RuntimeException('Versicherungstiefe: R3-/Kategorie-Bestandsprofil fehlt.');
        return $p;
    }
    private static function parent_node(string $owner):string {
        return 'core:subarea:insurance:'.substr($owner,strlen('INS-SEO:R3:'));
    }
    private static function revision(string $base):string {
        return $base.'+INS-DEPTH-'.substr('4b1d2f5a85bf9e27d1f56cbbbd92f15ad5f6cece529a07d1e44c20c934e06b72',0,12);
    }
    private static function lock():bool {
        $v=(int)get_option(self::LOCK,0);
        if($v>0&&time()-$v<180)return false;
        if($v)delete_option(self::LOCK);
        return add_option(self::LOCK,time(),'','no');
    }
    private static function unlock():void {delete_option(self::LOCK);}
    public static function preflight():array {
        if(self::state()||get_option(self::BACKUP,null)!==null)
            throw new RuntimeException('Versicherungstiefe: Lauf existiert bereits; keine Wiederholung.');
        if((APKW_Insurance_SEO_Repair::state()['status']??'')!=='COMPLETE')
            throw new RuntimeException('Versicherungstiefe: erst Versicherungen SEO vollständig bis COMPLETE abschließen.');
        $p=self::profile();$seo=self::seo_profile();
        $snap=APKW_TargetTreeSync::active_snapshot();$rev=APKW_TargetTreeSync::active_revision();
        if(!is_array($snap)||!$rev||($snap['revision']??'')!==$rev||
           (int)($snap['settings']['expected_world_count']??0)!==7)
            throw new RuntimeException('Versicherungstiefe: aktive Sieben-Welten-Revision fehlt.');
        $idx=[];foreach((array)($snap['nodes']??[]) as $n){
            $id=(string)($n['node_id']??'');if(isset($idx[$id]))throw new RuntimeException('Versicherungstiefe: doppelte aktive Knoten-ID.');
            $idx[$id]=$n;
        }
        $worlds=0;foreach($idx as $id=>$n)if(str_starts_with($id,'core:world:'))$worlds++;
        if($worlds!==7)throw new RuntimeException('Versicherungstiefe: sechs alte plus siebte Welt nicht vollständig.');
        $map=(array)($snap['mapping']??[]);$pages=[];
        foreach($seo['pages'] as $page)if(($page['level']??'')==='R3'){
            $node=self::parent_node((string)$page['key']);$n=$idx[$node]??[];
            $id=(int)($map[$node]['object_id']??0);
            $wp=$id>0?get_post($id):null;
            if(($n['display_name']??'')!==$page['title']||
                ($n['slug']??'')!==$page['slug']||($n['object_type']??'')!=='page'||
                $id<1||!is_object($wp)||$wp->post_type!=='page'||$wp->post_status!=='publish'||
                (string)$wp->post_name!==(string)$page['slug']||
                (string)get_post_meta($id,'_apkw_target_node_id',true)!==$node)
                throw new RuntimeException('Versicherungstiefe: Original-Keyword-Seite fehlt oder wurde verändert: '.$page['title']);
            $pages[$page['key']]=['parent_node'=>$node,'id'=>$id];
        }
        $existing=0;
        foreach($seo['flat_categories'] as $c){
            $nid='core:leaf:insurance:'.(string)$c['slug'];
            $node=$idx[$nid]??[];
            if(($node['display_name']??'')!==(string)$c['name']||
                ($node['parent_id']??'')!==self::parent_node((string)$c['parent'])||
                ($node['slug']??'')!==(string)$c['slug']||
                empty($map[$nid]['object_id']))
                throw new RuntimeException('Versicherungstiefe: bisherige Versicherungs-Endkategorie verändert.');
            $existing++;
        }
        if($existing!==138)throw new RuntimeException('Versicherungstiefe: 138 vorhandene Endkategorien nicht nachgewiesen.');
        $new=[];
        foreach($p['new_categories'] as $j){
            $nid=$j['node_id'];$owner=$pages[$j['parent_key']]??null;
            if(!$owner||isset($idx[$nid])||isset($map[$nid]))
                throw new RuntimeException('Versicherungstiefe: Kategorie-ID bereits vorhanden/falscher Owner.');
            $slug=$j['slug'];$name=$j['name'];
            if(get_term_by('slug',$slug,'category'))
                throw new RuntimeException('Versicherungstiefe: WordPress-Slug bereits vergeben: '.$slug);
            $x=term_exists($name,'category',0);
            if(is_wp_error($x)||$x)
                throw new RuntimeException('Versicherungstiefe: WordPress-Kategoriename bereits vorhanden: '.$name);
            $new[]=['job'=>$j,'parent_node'=>$owner['parent_node']];
        }
        return ['valid'=>true,'writes'=>0,'snapshot'=>$snap,'revision'=>$rev,'jobs'=>$new,'existing_terms'=>138,
                'new_terms'=>count($new),'new_pages'=>0,'changed_old_pages'=>0,'worlds_preserved'=>6];
    }
    public static function dry_run():array {
        $x=self::preflight();unset($x['snapshot'],$x['jobs']);return $x;
    }
    public static function start():void {
        try{
            if(!current_user_can('manage_options'))throw new RuntimeException('Administrator erforderlich.');
            check_admin_referer('apkw_ins_c26_start');
            if(empty($_POST['apkw_ins_c26_approve']))throw new RuntimeException('Ausdrückliche Freigabe fehlt.');
            if(!self::lock())throw new RuntimeException('Ein Import läuft bereits.');
            try{
                $p=self::preflight();
                update_option(self::BACKUP,$p['snapshot'],false);
                self::save(['status'=>'WRITING','base_revision'=>$p['revision'],
                    'base_sha'=>hash('sha256',serialize($p['snapshot'])),
                    'jobs'=>$p['jobs'],'i'=>0,'new_mapping'=>[],'created'=>[],'error'=>'']);
            }finally{self::unlock();}
            wp_safe_redirect(admin_url('admin.php?page='.self::PAGE.'&started=1'));exit;
        }catch(Throwable $e){wp_die(esc_html($e->getMessage()),'Versicherungstiefe STOPP',['response'=>409]);}
    }
    private static function ensure_base(array $s):array {
        $snap=APKW_TargetTreeSync::active_snapshot();
        if(!is_array($snap)||($snap['revision']??'')!==$s['base_revision']||
            APKW_TargetTreeSync::active_revision()!==$s['base_revision']||
            !hash_equals($s['base_sha'],hash('sha256',serialize($snap))))
            throw new RuntimeException('Versicherungstiefe: Originalrevision während Import verändert.');
        return $snap;
    }
    private static function apply(array &$s):void {
        self::ensure_base($s);
        $processed=0;
        while($processed<self::BATCH&&$s['i']<count($s['jobs'])){
            $item=$s['jobs'][$s['i']];$j=$item['job'];$node=(string)$j['node_id'];
            $id=APKW_TargetWriter::target_tree_insert_term('category',['name'=>$j['name'],'slug'=>$j['slug'],'parent'=>0]);
            $ref=['kind'=>'term','id'=>$id,'taxonomy'=>'category'];
            $s['created'][]=['id'=>$id,'node'=>$node,'name'=>$j['name'],'slug'=>$j['slug']];
            $s['new_mapping'][$node]=['object_id'=>$id,'object_type'=>'category','adapter'=>'wordpress_taxonomy','taxonomy'=>'category'];
            $s['i']++;self::save($s); // Persist physical ID before metadata / next write.
            foreach(['_apkw_target_node_id'=>$node,'_apkw_concept_id'=>$node,
                '_apkw_parent_concept_id'=>$item['parent_node'],'_apkw_target_pillar'=>'core',
                '_apkw_portal_block'=>'content','_apkw_portal_root'=>'0',
                '_apkw_target_active'=>'1','_apkw_target_revision'=>self::revision($s['base_revision']),
                '_apkw_seo_index_approved'=>'0'] as $k=>$v)
                APKW_TargetWriter::target_tree_set_meta($ref,'category',$k,(string)$v);
            $processed++;
        }
        if($s['i']===count($s['jobs'])){$s['status']='VERIFY';self::save($s);}
    }
    private static function verify(array $s):void {
        $expected=count($s['jobs']);
        if($expected!==185||count($s['new_mapping'])!==$expected||$s['i']!==$expected)
            throw new RuntimeException('Versicherungstiefe: physischer Import unvollständig.');
        foreach($s['jobs'] as $item){
            $j=$item['job'];$n=$j['node_id'];$tid=(int)($s['new_mapping'][$n]['object_id']??0);
            $t=$tid?get_term($tid,'category'):null;
            if(!is_object($t)||is_wp_error($t)||(int)$t->parent!==0||(string)$t->slug!==$j['slug']||
                html_entity_decode((string)$t->name,ENT_QUOTES|ENT_HTML5,'UTF-8')!==$j['name']||
                (string)get_term_meta($tid,'_apkw_target_node_id',true)!==$n||
                (string)get_term_meta($tid,'_apkw_parent_concept_id',true)!==$item['parent_node'])
                throw new RuntimeException('Versicherungstiefe: echte WordPress-Term-/Owner-Bindung stimmt nicht.');
        }
    }
    private static function finish(array &$s):void {
        $snap=self::ensure_base($s);self::verify($s);
        foreach($s['jobs'] as $item){
            $j=$item['job'];$node=$j['node_id'];
            if(isset($snap['mapping'][$node]))throw new RuntimeException('Versicherungstiefe: fremde Knotenbindung entdeckt.');
            $snap['nodes'][]=['node_id'=>$node,'pillar'=>'core','object_type'=>'category',
                'parent_id'=>$item['parent_node'],'display_name'=>$j['name'],'slug'=>$j['slug'],
                'status'=>'active','seo_owner'=>false,'insurance_c26_depth'=>true,
                'keyword_evidence'=>'INFERRED_INTENT_NOT_VOLUME_VERIFIED'];
            $snap['mapping'][$node]=$s['new_mapping'][$node];
        }
        $snap['revision']=self::revision($s['base_revision']);
        $snap['project']['insurance_c26_categories_added_at_utc']=gmdate('c');
        $before=APKW_FinalTargetAdmin::frontend_readback($snap);
        if(empty($before['valid']))
            throw new RuntimeException('Versicherungstiefe: Frontend-Stage verweigert: '.implode(',',(array)($before['errors']??[])));
        update_option(self::SNAP,$snap,false);update_option(self::REV,$snap['revision'],false);
        $after=APKW_FinalTargetAdmin::frontend_readback();
        if(empty($after['valid']))throw new RuntimeException('Versicherungstiefe: aktiver Frontend-Readback verweigert.');
        if(class_exists('APKW_FrontendStructure'))APKW_FrontendStructure::invalidate_cache();
        $s['status']='COMPLETE';$s['result']=['added_category_terms'=>185,'total_insurance_categories'=>323,
          'existing_insurance_term_ids_preserved'=>138,'seo_topic_pages_unchanged'=>46,'old_worlds_unchanged'=>6];self::save($s);
    }
    private static function rollback(array &$s):void {
        $base=get_option(self::BACKUP,null);
        if(!is_array($base))throw new RuntimeException('Versicherungstiefe: ursprünglicher Snapshot fehlt, keine unsichere Rücknahme.');
        $current=APKW_TargetTreeSync::active_revision();
        if(!in_array($current,[$s['base_revision'],self::revision($s['base_revision'])],true))
            throw new RuntimeException('Versicherungstiefe: fremde Revision, Rückbau verweigert.');
        if($current!==$s['base_revision']){
            update_option(self::SNAP,$base,false);update_option(self::REV,$s['base_revision'],false);
        }
        $k=0;
        while($k<self::BATCH&&!empty($s['created'])){
            $created=end($s['created']);$tid=(int)$created['id'];
            $t=get_term($tid,'category');
            if(!is_object($t)||is_wp_error($t)||(int)$t->count!==0||
                (int)$t->parent!==0||(string)$t->slug!==$created['slug']||
                !in_array((string)get_term_meta($tid,'_apkw_target_node_id',true),['',$created['node']],true))
                throw new RuntimeException('Versicherungstiefe: Term inzwischen fremd belegt/verändert – nicht löschen.');
            APKW_TargetWriter::target_tree_delete_object(['kind'=>'term','id'=>$tid,'taxonomy'=>'category']);
            array_pop($s['created']);$k++;self::save($s);
        }
        if(empty($s['created'])){
            $s['status']='ROLLED_BACK';$s['result']=['old_138_and_46_preserved'=>true];self::save($s);
            if(class_exists('APKW_FrontendStructure'))APKW_FrontendStructure::invalidate_cache();
        }
    }
    public static function batch():array {
        if(!self::lock())return self::state();
        try{
            $s=self::state();if(!in_array(($s['status']??''),['WRITING','VERIFY','ROLLBACK'],true))return $s;
            try{
                if($s['status']==='WRITING')self::apply($s);
                elseif($s['status']==='VERIFY')self::finish($s);
                else self::rollback($s);
            }catch(Throwable $e){$s['status']='ROLLBACK';$s['error']=trim(($s['error']??'').' | '.$e->getMessage(),' |');self::save($s);}
            return $s;
        }finally{self::unlock();}
    }
    public static function tick():void {
        try{
            if(!current_user_can('manage_options'))throw new RuntimeException('Administrator erforderlich.');
            check_ajax_referer('apkw_ins_c26_tick','nonce');
            $s=self::batch();wp_send_json_success(['status'=>$s['status']??'',
                'written'=>(int)($s['i']??0),'total'=>185,'error'=>(string)($s['error']??'')]);
        }catch(Throwable $e){wp_send_json_error(['error'=>$e->getMessage()],409);}
    }
    public static function render():void {
        if(!current_user_can('manage_options'))return;
        echo '<div class="wrap"><h1>Versicherungen – Beitragskategorien fachlich vertiefen</h1>';
        echo '<p>46 konkrete Versicherungs-Themenseiten behalten. Individuell 185 ergänzende unterste Beitragskategorien ohne eine neue Seitenebene. Die vorhandenen 138 Kategorien bleiben unverändert. Keine Beitragsproduktion, keine neue DataForSEO-Abfrage.</p>';
        $s=self::state();$status=(string)($s['status']??'');
        if($status==='COMPLETE')echo '<div class="notice notice-success"><p>COMPLETE: 185/185 neue Kategorien; insgesamt 323 unter den 46 Versicherungsthemen. Die sechs ursprünglichen Hauptwelten unverändert.</p></div>';
        elseif($status==='ROLLED_BACK')echo '<div class="notice notice-warning"><p>ROLLED BACK – ursprüngliche 138 Versicherungskategorien unverändert erhalten.</p></div>';
        elseif($status!=='')echo '<p>STATUS: '.esc_html($status).' '.(int)($s['i']??0).'/185</p><p>'.esc_html((string)($s['error']??'')).'</p>';
        else {
            try{$p=self::dry_run();echo '<p><strong>Vorschau PASS:</strong> null Schreibvorgänge. 46 Versicherungs-Keywordseiten und 138 bestehende Endkategorien geschützt. 185 fachlich ergänzende Kategorien würden neu angelegt.</p>';
                echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
                wp_nonce_field('apkw_ins_c26_start');
                echo '<input type="hidden" name="action" value="apkw_ins_c26_start"><label><input type="checkbox" name="apkw_ins_c26_approve" value="1"> Ich gebe ausschließlich diese 185 additiven Versicherungskategorien frei.</label><p><button class="button button-primary">Unterkategorien für Versicherungen ergänzen</button></p></form>';
            }catch(Throwable $e){echo '<p><strong>BLOCKIERT:</strong> '.esc_html($e->getMessage()).'</p>';}
        }
        if(in_array($status,['WRITING','VERIFY','ROLLBACK'],true)){
            $nonce=wp_create_nonce('apkw_ins_c26_tick');
            echo '<p id="apkw-ins-c26-progress">Bearbeitung läuft...</p><script>(function(){var u='.wp_json_encode(admin_url('admin-ajax.php')).',n='.wp_json_encode($nonce).';function run(){var b=new URLSearchParams();b.append("action","apkw_ins_c26_tick");b.append("nonce",n);fetch(u,{method:"POST",credentials:"same-origin",body:b}).then(function(x){return x.json()}).then(function(x){if(!x.success)throw Error(x.data&&x.data.error||"Ajaxfehler");var s=x.data;document.getElementById("apkw-ins-c26-progress").textContent=s.status+" "+s.written+"/185";if(["COMPLETE","ROLLED_BACK"].includes(s.status))location.reload();else setTimeout(run,350)}).catch(function(e){document.getElementById("apkw-ins-c26-progress").textContent="Angehalten: "+e.message+". Seite neu laden."})}run()})();</script>';
        }
        echo '</div>';
    }
}
