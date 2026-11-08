#!/usr/bin/env python3
"""Build HD009 0.1.31 with an opt-in cost-capped DataForSEO task worker.
Source: the unique official Hobby Depot HD009 0.1.29 FULL plugin.
Hab's verified queue and cost contract; Hobby's own HD007/HD003 data authority.
No new plugin, table, unrelated provider logic, images or frontend API calls.
"""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from tempfile import TemporaryDirectory
from hashlib import sha256
import subprocess
ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE")
SOURCE=ROOT/"HOBBY_DEPOT_AFFILIATE_HD009_0.1.29.zip"
CURRENT=ROOT/"CURRENT.zip"
OUT=ROOT/"HOBBY_DEPOT_AFFILIATE_HD009_0.1.31.zip"
EXPECTED="56aa1338e27bf0582a24e82f20184bccca782555028d9104efee96d0d2059dce"
MAIN="affiliate-portal-router/hobby-depot-affiliate-router.php"
CLASS="affiliate-portal-router/includes/class-hdar-amazon-start.php"

def one(s,a,b,label):
    n=s.count(a)
    assert n==1,(label,n,a[:100])
    return s.replace(a,b)
assert sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED,"Approved source altered; stop"
with ZipFile(SOURCE) as z:
    assert z.testzip() is None and len(z.namelist())==41
    main=z.read(MAIN).decode()
    cls=z.read(CLASS).decode()
main=one(main," * Version: 0.1.29"," * Version: 0.1.31","version header")
cls=one(cls,"'0.1.29'","'0.1.31'","asset cache")

# Conservative existing-system extension; all functions are methods of the
# original HDAR_Amazon_Start, not a second router or a foreign Hab class.
worker=r'''
    /* HD009 0.1.31 – reviewed Hobby-Depot DataForSEO task worker.
       Inspired by the independently checked Hab RC11 state machine:
       explicit opt-in, UTC cap 5, reserve BEFORE paid task_post,
       poll task_get free until done, error -> disabled, no duplicate.
       Product and category authority remains HD007 and HD003. */
    const DFS_AUTO_OPTION='hdar_amazon_dfs_auto_v1';
    const DFS_AUTO_HOOK='hdar_amazon_dfs_auto_tick_v1';
    private static function auto_state() {
        $s=get_option(self::DFS_AUTO_OPTION,array());
        if (!is_array($s)) { $s=array(); }
        return array_merge(array('enabled'=>false,'day'=>'','count'=>0,
            'status'=>'off','message'=>'Autorecherche ausgeschaltet',
            'pending'=>array(),'checked'=>array(),'scan_offset'=>0,
            'results_count'=>0,'last_tick'=>0,'last_success'=>0,
            'last_cost'=>'','last_candidate'=>''),$s);
    }
    private static function auto_save_state($s) {
        // One option is enough. No new database table or cache chain.
        update_option(self::DFS_AUTO_OPTION,$s,false);
    }
    private static function auto_ready($s=null) {
        $s=is_array($s)?$s:self::auto_state();
        $credentials=self::credentials();
        return !empty($s['enabled']) && self::launch_active() &&
          self::tracking_id()!=='' &&
          trim((string)($credentials['login']??''))!=='' &&
          trim((string)($credentials['password']??''))!=='';
    }
    public static function auto_save() {
        self::guard('hdar_amazon_auto_toggle');
        $s=self::auto_state();
        $s['enabled']=!empty($_POST['hdar_dfs_auto_enabled']);
        $s['status']=$s['enabled']?'idle':'off';
        $s['message']=$s['enabled']
          ? 'Automatische Suchaufträge freigegeben: maximal fünf neue bezahlte Aufträge pro UTC-Tag. Ergebnisse werden im bestehenden Produktbestand gespeichert, aber ohne zulässiges Produktbild nicht angezeigt.'
          : 'Autorecherche angehalten. Bereits gespeicherte Produkte bleiben erhalten.';
        self::auto_save_state($s);
        self::auto_schedule();
        self::back($s['enabled']?'auto_enabled':'auto_disabled');
    }
    public static function auto_preflight() {
        self::guard('hdar_amazon_auto_preflight');
        $s=self::auto_state();
        $copy=$s;
        // Never edit the paid scan cursor or call DataForSEO during preflight.
        $candidate=self::auto_candidate($copy);
        if (is_wp_error($candidate)) {
            $s['preflight']=$candidate->get_error_message();
        } elseif (is_array($candidate)) {
            $s['preflight']=$candidate['keyword'].' → '.$candidate['key']
              .' (Artikel: '.$candidate['title'].')';
        } else {
            $s['preflight']='Kein noch offener, sicher zugeordneter Artikel in diesem Prüflauf';
        }
        self::auto_save_state($s);
        self::back('auto_status');
    }
    public static function auto_run_now() {
        self::guard('hdar_amazon_auto_run');
        self::auto_tick('manual',false);
        self::back('auto_status');
    }
    public static function auto_poll_now() {
        self::guard('hdar_amazon_auto_poll');
        self::auto_tick('manual_poll',true);
        self::back('auto_status');
    }
    public static function auto_schedule() {
        if (!function_exists('wp_next_scheduled')) { return; }
        $s=self::auto_state();
        $next=wp_next_scheduled(self::DFS_AUTO_HOOK);
        if (!self::auto_ready($s)) {
            if ($next && function_exists('wp_clear_scheduled_hook')) {
                wp_clear_scheduled_hook(self::DFS_AUTO_HOOK);
            }
            return;
        }
        if (!$next && function_exists('wp_schedule_event')) {
            wp_schedule_event(time()+300,'hourly',self::DFS_AUTO_HOOK);
        }
    }
    private static function auto_norm($text) {
        $text=mb_strtolower(trim((string)$text),'UTF-8');
        $text=str_replace(array('ä','ö','ü','ß'),array('ae','oe','ue','ss'),$text);
        return trim(preg_replace('/\s+/',' ',preg_replace('/[^a-z0-9]+/',' ',$text)));
    }
    private static function auto_candidate_word($text) {
        $start=trim(explode(',',trim((string)$text),2)[0], " \t\n\r\0\x0B.");
        $lower=self::auto_norm($start);
        $reject=array('karton','holz','papier','material','werkzeug','computer',
          'wasser','schere','farbe','modell','schrauben','leitung','leinen',
          'lupe','kleber','buch','bogen','rute','behaelter','aufbewahrung',
          'saatgut','kamera','platz','zeit','geduld','licht','luft','erde');
        if ($lower==='' || strlen($start)<8 || strlen($start)>55 ||
            count(explode(' ',$lower))>5 ||
            in_array($lower,$reject,true) ||
            preg_match('/\b(und|oder|platz|zeit|freie|geeignete|erfahrung|kenntnisse|wind|wetter|flaeche)\b/',$lower)) {
            return '';
        }
        return $start;
    }
    private static function auto_hobby_catalog() {
        // Never ship a stale duplicate list: read the TWO existing
        // verified Hobby-Depot plugin data files, cron/admin only.
        if (!defined('WP_PLUGIN_DIR')) {
            return new WP_Error('hdar_dfs_plugins','WordPress Plugin-Verzeichnis unbekannt');
        }
        $registry=WP_PLUGIN_DIR.'/hd-hobbyregister-core/data/hobby-register.json';
        $map=WP_PLUGIN_DIR.'/affiliate-portal-template-kit/assets/hobby-depot-v150750/leaf-category-map-v150750.json';
        if (!is_readable($registry) || !is_readable($map)) {
            return new WP_Error('hdar_dfs_catalog','Geprüfter Hobbyregister-/Kategoriebaum fehlt auf dem Server. Keine bezahlte Suche.');
        }
        $r=json_decode((string)file_get_contents($registry),true);
        $m=json_decode((string)file_get_contents($map),true);
        if (!is_array($r) || !is_array($r['records']??null) ||
            count($r['records'])<800 || !is_array($m) || count($m)<300) {
            return new WP_Error('hdar_dfs_catalog','Hobbyregister-/Kategoriedaten unvollständig. Keine bezahlte Suche.');
        }
        $active=array();
        foreach ($m as $row) {
            if (!is_array($row)) { continue; }
            $slug=sanitize_title((string)($row['parent_slug']??''));
            if ($slug!=='') { $active[$slug]=true; }
        }
        $catalog=array();
        foreach ($r['records'] as $row) {
            if (!is_array($row)) { continue; }
            $slug=sanitize_title((string)($row['canonical_name']??''));
            if (!isset($active[$slug])) { continue; }
            $equipment=(string)($row['result_profile']['what_do_you_need']??'');
            $term=self::auto_candidate_word($equipment);
            if ($term==='') { continue; }
            $catalog[$slug]=array('hobby'=>(string)$row['canonical_name'],'keyword'=>$term);
        }
        if (count($active)<300 || count($catalog)<130) {
            return new WP_Error('hdar_dfs_catalog','Zu wenige fachlich eindeutige Hobby-Suchbegriffe. Keine bezahlte Suche.');
        }
        return $catalog;
    }
    private static function auto_post_hobby($post,$catalog) {
        if (!($post instanceof WP_Post) || (string)$post->post_type!=='post' ||
            (string)$post->post_status!=='publish') { return null; }
        $category_slugs=array();
        $terms=get_the_terms($post->ID,'category');
        if (is_wp_error($terms)) { return null; }
        foreach ((array)$terms as $term) {
            if (!($term instanceof WP_Term)) { continue; }
            $category_slugs[]=sanitize_title((string)$term->slug);
            foreach ((array)get_ancestors($term->term_id,'category','taxonomy') as $ancestor_id) {
                $parent=get_term(absint($ancestor_id),'category');
                if ($parent instanceof WP_Term) {
                    $category_slugs[]=sanitize_title((string)$parent->slug);
                }
            }
        }
        $post_slug=sanitize_title((string)$post->post_name);
        foreach ($catalog as $slug=>$row) {
            $matched=$slug===$post_slug;
            foreach ($category_slugs as $category_slug) {
                if ($category_slug===$slug || strpos($category_slug,$slug.'-')===0) {
                    $matched=true;break;
                }
            }
            if (!$matched) { continue; }
            // No generic product searches on loosely related opinion posts.
            $topic=self::auto_norm((string)$post->post_title);
            $needle=self::auto_norm((string)$row['keyword']);
            $hobby=self::auto_norm((string)$row['hobby']);
            if (strpos(' '.$topic.' ',' '.$needle.' ')===false &&
                strpos(' '.$topic.' ',' '.$hobby.' ')===false) { continue; }
            $hash=hash('sha256',(string)$post->post_title.'|'.$slug.'|'.$row['keyword']);
            return array('id'=>(int)$post->ID,'key'=>'post:'.(int)$post->ID,
                'keyword'=>$row['keyword'],'hobby_slug'=>$slug,
                'hash'=>$hash,'title'=>(string)$post->post_title);
        }
        return null;
    }
    private static function auto_candidate(&$state) {
        $catalog=self::auto_hobby_catalog();
        if (is_wp_error($catalog)) { return $catalog; }
        $offset=max(0,absint($state['scan_offset']??0));
        $posts=get_posts(array('post_type'=>'post','post_status'=>'publish',
            'posts_per_page'=>100,'offset'=>$offset,'orderby'=>'ID',
            'order'=>'ASC','suppress_filters'=>true));
        if (!$posts && $offset>0) {
            $offset=0;
            $posts=get_posts(array('post_type'=>'post','post_status'=>'publish',
                'posts_per_page'=>100,'offset'=>0,'orderby'=>'ID',
                'order'=>'ASC','suppress_filters'=>true));
        }
        foreach ((array)$posts as $i=>$post) {
            $state['scan_offset']=$offset+$i+1;
            $topic=self::auto_post_hobby($post,$catalog);
            if (!is_array($topic)) { continue; }
            $seen=(array)(($state['checked']??array())[(int)$post->ID]??array());
            if (($seen['hash']??'')===$topic['hash'] &&
                absint($seen['at']??0)>time()-7*DAY_IN_SECONDS) { continue; }
            $stored=self::products();
            if (!empty($stored[$topic['key']]['items'])) { continue; }
            return $topic;
        }
        if (count((array)$posts)<100) { $state['scan_offset']=0; }
        return null;
    }
    private static function auto_api($method,$url,$payload=null) {
        $cred=self::credentials();
        if (!self::auto_ready()) {
            return new WP_Error('hdar_dfs_not_ready','Automatik oder DataForSEO-/Amazon-Zugang nicht vollständig freigegeben');
        }
        if (!preg_match('~^https://api\.dataforseo\.com/v3/merchant/amazon/products/(?:task_post|task_get/advanced/[0-9a-f-]{36})$~D',$url)) {
            return new WP_Error('hdar_dfs_endpoint','Nicht erlaubter DataForSEO-Endpunkt');
        }
        $args=array('method'=>$method,'timeout'=>25,'redirection'=>0,
            'headers'=>array('Authorization'=>'Basic '.base64_encode($cred['login'].':'.$cred['password']),
            'Content-Type'=>'application/json'));
        if ($payload!==null) { $args['body']=wp_json_encode($payload); }
        $resp=wp_remote_request($url,$args);
        if (is_wp_error($resp)) { return $resp; }
        if ((int)wp_remote_retrieve_response_code($resp)!==200) {
            return new WP_Error('hdar_dfs_http','DataForSEO HTTP '.(int)wp_remote_retrieve_response_code($resp));
        }
        $out=json_decode((string)wp_remote_retrieve_body($resp),true);
        if (!is_array($out) || (int)($out['status_code']??0)!==20000 ||
            !is_array($out['tasks']??null) || !$out['tasks']) {
            return new WP_Error('hdar_dfs_response','DataForSEO-Antwort fehlerhaft');
        }
        return $out;
    }
    private static function auto_match_results($keyword,$items) {
        $words=explode(' ',self::auto_norm($keyword));
        if (!$words || !$words[0]) { return array(); }
        $matches=array();
        foreach ((array)$items as $item) {
            if (!is_array($item) || ($item['type']??'')!=='amazon_serp') { continue; }
            $url=(string)($item['url']??'');
            $host=strtolower((string)wp_parse_url($url,PHP_URL_HOST));
            if (!in_array($host,array('amazon.de','www.amazon.de'),true)) { continue; }
            $asin=strtoupper(trim((string)($item['data_asin']??'')));
            if (!preg_match('/^[A-Z0-9]{10}$/D',$asin)) { continue; }
            $title=sanitize_text_field((string)($item['title']??''));
            if ($title==='' || strlen($title)>350) { continue; }
            $tokens=' '.self::auto_norm($title).' ';
            $ok=true;
            foreach ($words as $word) {
                if (strlen($word)<2) { continue; }
                if (strpos($tokens,' '.$word.' ')===false) { $ok=false;break; }
            }
            if (!$ok || isset($matches[$asin])) { continue; }
            $matches[$asin]=array('asin'=>$asin,
                'title'=>function_exists('mb_substr')?mb_substr($title,0,160):substr($title,0,160),
                'source'=>'dataforseo_hobby_auto_v1');
            if (count($matches)>=3) { break; }
        }
        return array_values($matches);
    }
    private static function auto_tick($source='cron',$poll_only=false) {
        $s=self::auto_state();
        if (!self::auto_ready($s)) { return; }
        $lock='hdar_amazon_dfs_auto_lock_v1';
        if (get_transient($lock)) { return; }
        set_transient($lock,1,180);
        try { self::auto_do_tick($s,$source,$poll_only); }
        finally { delete_transient($lock); }
    }
    public static function auto_cron() { self::auto_tick('cron',false); }
    private static function auto_fail(&$s,$message) {
        $s['enabled']=false;
        $s['status']='error';
        $s['message']=$message.' – Automatik angehalten; keine weitere bezahlte Suche';
        self::auto_save_state($s);
        self::auto_schedule();
    }
    private static function auto_do_tick($s,$source,$poll_only) {
        $day=gmdate('Y-m-d');
        if ((string)($s['day']??'')!==$day) {
            $s['day']=$day;
            $s['count']=0;
        }
        $s['last_tick']=time();
        $s['last_source']=sanitize_key($source);
        self::auto_save_state($s);
        $pending=(array)($s['pending']??array());
        if (!empty($pending['id'])) {
            $id=(string)$pending['id'];
            if (!preg_match('/^[0-9a-f-]{36}$/D',$id) ||
                absint($pending['at']??0)<time()-48*HOUR_IN_SECONDS) {
                self::auto_fail($s,'Offener DataForSEO-Auftrag ungültig oder abgelaufen');
                return;
            }
            $reply=self::auto_api('GET',
                'https://api.dataforseo.com/v3/merchant/amazon/products/task_get/advanced/'.$id);
            if (is_wp_error($reply)) {
                self::auto_fail($s,'Ergebnisabruf gescheitert: '.$reply->get_error_message());
                return;
            }
            $task=(array)($reply['tasks'][0]??array());
            $code=(int)($task['status_code']??0);
            if ($code!==20000 && $code!==20100) {
                self::auto_fail($s,'DataForSEO-Auftrag Fehlercode '.$code);
                return;
            }
            $result=(array)($task['result']??array());
            if (!$result) {
                $s['status']='pending';
                $s['message']='Bezahlter Suchauftrag wird noch verarbeitet; nächster Abruf kostenlos';
                self::auto_save_state($s);
                return;
            }
            $target=self::target('post',absint($pending['post_id']??0));
            $catalog=self::auto_hobby_catalog();
            $post=$target?get_post(absint($pending['post_id']??0)):null;
            $topic=!is_wp_error($catalog)&&$post
                ? self::auto_post_hobby($post,$catalog) : null;
            if (!$topic || !hash_equals((string)$pending['hash'],(string)$topic['hash']) ||
                (string)$topic['keyword']!==(string)$pending['keyword']) {
                $s['pending']=array();
                self::auto_fail($s,'Artikel, Zuordnung oder geprüfter Ausrüstungsbegriff wurde inzwischen geändert');
                return;
            }
            $items=self::auto_match_results($topic['keyword'],
                (array)($result[0]['items']??array()));
            $store=self::products();
            $key=$topic['key'];
            if ($items && empty($store[$key]['items'])) {
                $store[$key]=array('label'=>$target['title'],'url'=>$target['url'],
                  'keyword'=>$topic['keyword'],'items'=>$items,
                  'source'=>'dataforseo_hobby_auto_v1',
                  'verified_at'=>time());
                update_option(self::PRODUCTS_OPTION,$store,false);
                $s['results_count']=absint($s['results_count']??0)+count($items);
            }
            $checked=(array)($s['checked']??array());
            $checked[(int)$topic['id']]=array('hash'=>$topic['hash'],'at'=>time());
            $s['checked']=array_slice($checked,-500,null,true);
            $s['pending']=array();
            $s['last_success']=time();
            $s['status']=$items?'success':'empty';
            $s['message']=$items
              ? count($items).' fachlich geprüfte ASINs gespeichert; ohne zulässiges Produktbild noch keine sichtbaren Amazon-Kacheln'
              : 'Keine ausreichend passende Amazon-Produktkennung gefunden; nichts veröffentlicht';
            self::auto_save_state($s);
            return;
        }
        if ($poll_only) {
            $s['status']='idle';
            $s['message']='Kein offener Auftrag – keine neue kostenpflichtige Suche gestartet';
            self::auto_save_state($s);
            return;
        }
        if (absint($s['count']??0)>=5) {
            $s['status']='limit';
            $s['message']='Tagesgrenze von fünf bezahlten DataForSEO-Aufträgen erreicht';
            self::auto_save_state($s);
            return;
        }
        $candidate=self::auto_candidate($s);
        if (is_wp_error($candidate)) {
            self::auto_fail($s,$candidate->get_error_message());
            return;
        }
        if (!$candidate) {
            $s['status']='idle';
            $s['message']='Keine neue, eindeutig zugeordnete und noch nicht geprüfte Hobby-Ausrüstungsfrage für einen veröffentlichten Artikel';
            self::auto_save_state($s);
            return;
        }
        // Reserve before POST: a timeout might still have been billed.
        $s['count']=absint($s['count']??0)+1;
        $s['status']='running';
        $s['last_candidate']=$candidate['keyword'].' → '.$candidate['key'];
        $s['message']='Bezahlte DataForSEO-Recherche gestartet: '.$candidate['keyword'];
        self::auto_save_state($s);
        $reply=self::auto_api('POST',
            'https://api.dataforseo.com/v3/merchant/amazon/products/task_post',
            array(array('keyword'=>$candidate['keyword'],
              'location_name'=>'Germany','language_code'=>'de_DE',
              'se_domain'=>'amazon.de','depth'=>20)));
        if (is_wp_error($reply)) {
            self::auto_fail($s,'Bezahlter Auftrag fehlgeschlagen (Tagesbudget reserviert): '.$reply->get_error_message());
            return;
        }
        $task=(array)($reply['tasks'][0]??array());
        $code=(int)($task['status_code']??0);
        $id=(string)($task['id']??'');
        if (!in_array($code,array(20100,20000),true) ||
            !preg_match('/^[0-9a-f-]{36}$/D',$id)) {
            self::auto_fail($s,'DataForSEO hat keine gültige Auftrag-ID geliefert (Code '.$code.')');
            return;
        }
        $s['pending']=array('id'=>$id,'post_id'=>$candidate['id'],
            'hash'=>$candidate['hash'],'keyword'=>$candidate['keyword'],
            'at'=>time());
        $s['status']='pending';
        $s['message']='Bezahlter Auftrag angelegt. Er wird kostenlos abgefragt; keine Doppelzahlung.';
        self::auto_save_state($s);
    }
'''
cls=one(cls,
    "        add_shortcode('hobby_amazon_produkten', array(__CLASS__, 'shortcode_products'));",
    "        add_shortcode('hobby_amazon_produkten', array(__CLASS__, 'shortcode_products'));\n"
    "        add_action('admin_post_hdar_amazon_auto_toggle', array(__CLASS__, 'auto_save'));\n"
    "        add_action('admin_post_hdar_amazon_auto_preflight', array(__CLASS__, 'auto_preflight'));\n"
    "        add_action('admin_post_hdar_amazon_auto_run', array(__CLASS__, 'auto_run_now'));\n"
    "        add_action('admin_post_hdar_amazon_auto_poll', array(__CLASS__, 'auto_poll_now'));\n"
    "        add_action('init', array(__CLASS__, 'auto_schedule'), 40);\n"
    "        add_action(self::DFS_AUTO_HOOK, array(__CLASS__, 'auto_cron'));",
    "auto hooks")

# Add a coherent control panel INSIDE the existing Amazon backend.
panel=r'''
        <h2>Automatische Amazon-Produktrecherche nach Hobbyregister</h2>
        <?php $auto=self::auto_state(); ?>
        <p>Quelle: die überprüften Ausrüstungsangaben aus Hobbyregister und Kategorien.
        <strong>Keine fremden Kategorien, keine Amazon-Originalbilder aus DataForSEO.</strong>
        Es werden höchstens fünf neue bezahlte Suchaufträge pro UTC-Tag gestartet; ein bereits
        bezahlter Auftrag wird kostenlos abgefragt. Treffer werden nur für nachgewiesene
        WordPress-Beiträge gespeichert. Bis ein zulässiges Produktfoto vorhanden ist,
        bleibt die Amazon-Kachel absichtlich unsichtbar.</p>
        <p><strong>Status:</strong> <?php echo esc_html((string)$auto['status']); ?> –
          <?php echo esc_html((string)$auto['message']); ?><br>
          <small>Heutige kostenpflichtige Aufträge: <?php echo (int)$auto['count']; ?>/5.
          Geprüfte ASINs: <?php echo (int)$auto['results_count']; ?>.
          Offener Auftrag: <?php echo !empty($auto['pending']['id'])?'ja':'nein'; ?>.
          Letzter Kandidat: <?php echo esc_html((string)$auto['last_candidate']); ?></small></p>
        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
          <input type="hidden" name="action" value="hdar_amazon_auto_toggle">
          <?php wp_nonce_field('hdar_amazon_auto_toggle'); ?>
          <label><input type="checkbox" name="hdar_dfs_auto_enabled" value="1"
          <?php checked(!empty($auto['enabled'])); ?>>
          Automatische kostenpflichtige Recherche ausdrücklich aktivieren (höchstens 5 neue Aufträge pro UTC-Tag, wiederkehrend)</label>
          <?php submit_button('Automatik speichern','secondary','',false); ?>
        </form>
        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="display:inline-block;margin:6px 8px 6px 0">
          <input type="hidden" name="action" value="hdar_amazon_auto_preflight">
          <?php wp_nonce_field('hdar_amazon_auto_preflight'); ?>
          <?php submit_button('Nächsten Kandidaten kostenlos prüfen','secondary','',false); ?>
        </form>
        <?php if (!empty($auto['preflight'])) : ?>
          <p><strong>Kostenfreier Prüfbericht:</strong>
            <?php echo esc_html((string)$auto['preflight']); ?></p>
        <?php endif; ?>
        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="display:inline-block;margin:6px 8px 6px 0">
          <input type="hidden" name="action" value="hdar_amazon_auto_run">
          <?php wp_nonce_field('hdar_amazon_auto_run'); ?>
          <?php submit_button('Jetzt prüfen / ggf. eine bezahlte Suche','secondary','',false); ?>
        </form>
        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="display:inline-block;margin:6px 0">
          <input type="hidden" name="action" value="hdar_amazon_auto_poll">
          <?php wp_nonce_field('hdar_amazon_auto_poll'); ?>
          <?php submit_button('Nur offenen Auftrag kostenlos abfragen','secondary','',false); ?>
        </form>
'''
cls=one(cls,"        <h2>2. DataForSEO-Zugang</h2>",panel+"\n        <h2>2. DataForSEO-Zugang</h2>","admin panel anchor")
cls=one(cls,"    public static function remove() {",worker+"\n    public static function remove() {","worker insertion")
with ZipFile(SOURCE) as z:
    n=z.namelist()
    assert n.count(MAIN)==1 and n.count(CLASS)==1
    content=BytesIO()
    with ZipFile(content,'w') as w:
        for info in z.infolist():
            value=(main.encode('utf8') if info.filename==MAIN else
                   cls.encode('utf8') if info.filename==CLASS else z.read(info.filename))
            w.writestr(info,value)
        w.comment=z.comment
data=content.getvalue()
with ZipFile(BytesIO(data)) as z:
    assert z.testzip() is None and len(z.namelist())==41
    php=[x for x in z.namelist() if x.endswith('.php')]
    assert len(php)==24
    with TemporaryDirectory() as td:
        for name in php:
            file=Path(td)/name;file.parent.mkdir(parents=True,exist_ok=True)
            file.write_bytes(z.read(name))
            result=subprocess.run(['php','-l',str(file)],capture_output=True,text=True)
            assert result.returncode==0,(name,result.stdout,result.stderr)
OUT.write_bytes(data)
CURRENT.write_bytes(data)
assert OUT.read_bytes()==CURRENT.read_bytes()
print("HD009_DFS_031_BUILD_PASS","zip_entries",41,"php",24,
      "bytes",len(data),"sha256",sha256(data).hexdigest())
