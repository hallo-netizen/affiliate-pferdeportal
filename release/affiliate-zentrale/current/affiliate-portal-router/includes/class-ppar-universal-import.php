<?php
if (!defined('ABSPATH')) { exit; }

/** Ein Uploadfeld, starke Provider-Erkennung, keine geratenen Importwege. */
final class PPAR_Affiliate_Universal_Import {
    const ACTION='ppar_universal_manual_import';
    const NONCE_ACTION='ppar_universal_manual_import';
    const NONCE_FIELD='ppar_universal_import_nonce';
    const LAST_OPTION='ppar_universal_import_last_v1';
    const DS24_INVENTORY_OPTION='ppar_digistore24_manual_inventory_v1';
    const MAX_SAMPLE_BYTES=1048576;
    const MAX_DS24_DECOMPRESSED_BYTES=33554432;
    private static $booted=false;

    public static function bootstrap() {
        if (self::$booted) return;
        self::$booted=true;
        add_action('admin_post_'.self::ACTION,array(__CLASS__,'handle_upload'));
    }

    public static function render_form() {
        if (!current_user_can('manage_options')) return;
        $notice=sanitize_key((string)($_GET['ppar_universal_import']??''));
        $message=rawurldecode((string)($_GET['ppar_universal_message']??''));
        $last=get_option(self::LAST_OPTION,array()); $last=is_array($last)?$last:array(); ?>
        <section class="postbox" style="padding:16px;margin:18px 0;max-width:900px">
            <h2 style="margin-top:0">Datei importieren</h2>
            <p>Eine Datei hochladen. Die Affiliate-Zentrale erkennt den Anbieter aus belastbaren Datei- und Inhaltssignaturen. Unklare Dateien werden ohne Änderung abgewiesen.</p>
            <?php if($notice==='success'): ?><div class="notice notice-success inline"><p><?php echo esc_html($message); ?></p></div><?php endif; ?>
            <?php if($notice==='failed'): ?><div class="notice notice-error inline"><p><?php echo esc_html($message); ?></p></div><?php endif; ?>
            <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" enctype="multipart/form-data">
                <input type="hidden" name="action" value="<?php echo esc_attr(self::ACTION); ?>"><?php wp_nonce_field(self::NONCE_ACTION,self::NONCE_FIELD); ?>
                <p><input type="file" name="affiliate_import_file" accept=".csv,.csv.gz,.json,.txt,.gz" required></p>
                <p><button class="button button-primary" type="submit">Datei prüfen &amp; importieren</button></p>
                <p class="description">Digistore24-Partnerschaftsexport, idealo-Standardfeed sowie eindeutig erkennbare Awin-/ADCELL-Werbemitteldateien. Der Upload veröffentlicht nichts ungeprüft.</p>
            </form>
            <?php if(!empty($last['provider'])&&!empty($last['imported_at'])): ?><p class="description"><strong>Letzter Import:</strong> <?php echo esc_html((string)$last['provider']); ?> · <?php echo esc_html(wp_date('d.m.Y H:i',absint($last['imported_at']))); ?><?php if(!empty($last['message'])): ?> · <?php echo esc_html((string)$last['message']); ?><?php endif; ?></p><?php endif; ?>
        </section><?php
    }

    public static function handle_upload() {
        if(!current_user_can('manage_options')) wp_die('Keine Berechtigung.');
        check_admin_referer(self::NONCE_ACTION,self::NONCE_FIELD);
        $file=$_FILES['affiliate_import_file']??null;
        if(!is_array($file)||(int)($file['error']??UPLOAD_ERR_NO_FILE)!==UPLOAD_ERR_OK||empty($file['tmp_name'])||!is_uploaded_file($file['tmp_name'])) self::redirect('failed','Dateiupload fehlgeschlagen.');
        $size=(int)($file['size']??0); $limit=function_exists('wp_max_upload_size')?(int)wp_max_upload_size():0;
        if($size<=0||($limit>0&&$size>$limit)) self::redirect('failed','Die Datei ist leer oder größer als das Server-Uploadlimit.');
        $name=sanitize_file_name((string)($file['name']??'import'));
        if(!preg_match('/\.(?:csv|json|txt|csv\.gz|gz)$/i',$name)) self::redirect('failed','Zulässig sind CSV, CSV.GZ, JSON oder TXT.');
        $sample=self::read_text((string)$file['tmp_name'],$name,self::MAX_SAMPLE_BYTES); if(is_wp_error($sample)) self::redirect('failed',$sample->get_error_message());
        $detected=self::detect_provider($name,$sample); if(is_wp_error($detected)) self::redirect('failed',$detected->get_error_message());
        $kind=(string)$detected['kind'];
        if($kind==='digistore24_partnerships') {
            $result=self::import_digistore24_partnerships((string)$file['tmp_name'],$name); if(is_wp_error($result)) self::redirect('failed',$result->get_error_message());
            self::remember('Digistore24',(string)$result['message'],(string)$result['sha256']); self::redirect('success',(string)$result['message']);
        }
        if($kind==='idealo_feed') self::delegate_idealo($file);
        if(in_array($kind,array('awin_creatives','adcell_creatives'),true)) self::delegate_creatives($file,$kind==='awin_creatives'?'awin':'adcell',$name);
        if($kind==='ebay_detected') self::redirect('failed','eBay-Datei erkannt. Der bestehende eBay-Produktpfad ist API-basiert; die Datei wird nicht in einen falschen Importpfad umgeleitet.');
        self::redirect('failed','Anbieter erkannt, aber für dieses Dateiformat existiert kein freigegebener manueller Importpfad.');
    }

    private static function read_text($path,$name,$limit) {
        if(!is_readable($path)) return new WP_Error('universal_import_unreadable','Importdatei ist nicht lesbar.');
        $gzip=preg_match('/\.gz$/i',(string)$name)===1; $body='';
        if($gzip) {
            if(!function_exists('gzopen')) return new WP_Error('universal_import_gzip_missing','GZIP-Unterstützung fehlt auf dem Server.');
            $h=@gzopen($path,'rb'); if(!$h) return new WP_Error('universal_import_gzip_open','GZIP-Datei konnte nicht geöffnet werden.');
            while(!gzeof($h)&&strlen($body)<$limit){$chunk=gzread($h,min(262144,$limit-strlen($body)));if($chunk===false){gzclose($h);return new WP_Error('universal_import_gzip_read','GZIP-Datei konnte nicht gelesen werden.');}$body.=$chunk;} gzclose($h);
        } else $body=(string)@file_get_contents($path,false,null,0,$limit);
        if($body==='') return new WP_Error('universal_import_empty','Datei enthält keine lesbaren Daten.');
        return self::encoding($body);
    }

    private static function read_full_ds24($path,$name) {
        if(!preg_match('/\.gz$/i',(string)$name)) {
            $size=@filesize($path); if($size!==false&&$size>self::MAX_DS24_DECOMPRESSED_BYTES) return new WP_Error('universal_import_too_large','Digistore24-Partnerschaftsdatei überschreitet 32 MiB.');
            $body=(string)@file_get_contents($path); return $body===''?new WP_Error('universal_import_empty','Datei ist leer.'):self::encoding($body);
        }
        if(!function_exists('gzopen')) return new WP_Error('universal_import_gzip_missing','GZIP-Unterstützung fehlt auf dem Server.');
        $h=@gzopen($path,'rb'); if(!$h) return new WP_Error('universal_import_gzip_open','GZIP-Datei konnte nicht geöffnet werden.');
        $body=''; $hard=self::MAX_DS24_DECOMPRESSED_BYTES;
        while(!gzeof($h)&&strlen($body)<=$hard){
            $remaining=($hard+1)-strlen($body);
            $chunk=gzread($h,min(262144,$remaining));
            if($chunk===false){gzclose($h);return new WP_Error('universal_import_gzip_read','GZIP-Datei konnte nicht gelesen werden.');}
            $body.=$chunk;
        }
        gzclose($h);
        if(strlen($body)>$hard) return new WP_Error('universal_import_too_large','Digistore24-Partnerschaftsdatei überschreitet dekomprimiert 32 MiB.');
        if($body==='') return new WP_Error('universal_import_empty','Datei ist leer.');
        return self::encoding($body);
    }

    private static function encoding($body) {
        $body=preg_replace('/^\xEF\xBB\xBF/','',(string)$body);
        if(function_exists('mb_check_encoding')&&!mb_check_encoding($body,'UTF-8')&&function_exists('mb_convert_encoding')) $body=mb_convert_encoding($body,'UTF-8','Windows-1252,ISO-8859-1,UTF-8');
        return $body;
    }
    private static function key($v){$v=trim((string)$v);if(function_exists('remove_accents'))$v=remove_accents($v);else $v=strtr($v,array('Ä'=>'A','Ö'=>'O','Ü'=>'U','ä'=>'a','ö'=>'o','ü'=>'u','ß'=>'ss'));return trim((string)preg_replace('/[^a-z0-9]+/','_',strtolower($v)),'_');}
    private static function delimiter($line){$best=',';$score=-1;foreach(array(';',',',"\t",'|') as $d){$c=substr_count((string)$line,$d);if($c>$score){$score=$c;$best=$d;}}return $best;}
    private static function headers($sample){$first=preg_split('/\r\n|\r|\n/',(string)$sample,2);$h=str_getcsv((string)($first[0]??''),self::delimiter($first[0]??''),'"','\\');return array_values(array_filter(array_map(array(__CLASS__,'key'),(array)$h),'strlen'));}
    private static function has($headers,$aliases){$set=array_fill_keys((array)$headers,true);foreach((array)$aliases as $a)if(isset($set[self::key($a)]))return true;return false;}

    private static function ds24_headers($h){return self::has($h,array('vendor','vendorname','anbieter'))&&self::has($h,array('produkt-id','produkt_id','product_id','productid'))&&self::has($h,array('produkt','produktname','product','product_name'))&&self::has($h,array('werbemittel-id','werbemittel_id','marketplace_entry_id','entry_id'))&&self::has($h,array('status der partnerschaft','partnerschaftsstatus','status','approval_status'))&&self::has($h,array('provision','affiliate-provision','affiliate_provision','commission','commission_rate'));}
    private static function idealo_headers($h){foreach(array('id','product_title','product_deeplink','ean','gtins_product','asins_product','main_category','sub_category','brand_name') as $x)if(!in_array($x,$h,true))return false;return in_array('image_url',$h,true)||in_array('image_url_1',$h,true);}

    private static function detect_provider($name,$sample) {
        $h=self::headers($sample); if(self::ds24_headers($h)) return array('provider'=>'digistore24','kind'=>'digistore24_partnerships','confidence'=>'exact_headers');
        $lower=strtolower((string)$sample); $signals=array();
        if(preg_match('/^productdata_[0-9]+\.csv(?:\.gz)?$/i',basename(strtolower((string)$name)))&&self::idealo_headers($h))$signals[]='idealo_feed';
        if(strpos($lower,'awin1.com')!==false||strpos($lower,'zenaps.com')!==false)$signals[]='awin_creatives';
        if(strpos($lower,'adcell.de')!==false||strpos($lower,'t.adcell.com')!==false)$signals[]='adcell_creatives';
        if(strpos($lower,'ebay.')!==false&&(strpos($lower,'itemid')!==false||strpos($lower,'item_id')!==false||strpos($lower,'epn')!==false))$signals[]='ebay_detected';
        $signals=array_values(array_unique($signals));
        if(count($signals)===1)return array('kind'=>$signals[0],'confidence'=>'strong_signature');
        if(count($signals)>1)return new WP_Error('universal_import_ambiguous','Datei enthält widersprüchliche Provider-Signaturen und wird nicht geraten.');
        return new WP_Error('universal_import_unknown','Anbieter konnte aus dieser Datei nicht sicher erkannt werden. Keine Daten wurden verändert.');
    }

    private static function aliases(){return array(
        'vendor'=>array('vendor','vendorname','anbieter'),'product_id'=>array('produkt-id','produkt_id','produktid','product-id','product_id','productid'),'product'=>array('produkt','produktname','product','product_name'),'entry_id'=>array('werbemittel-id','werbemittel_id','werbemittelid','marketplace_entry_id','entry_id'),'status'=>array('status der partnerschaft','partnerschaftsstatus','status','approval_status'),'commission'=>array('provision','affiliate-provision','affiliate_provision','commission','commission_rate'),'support_url'=>array('werbemittelseite','werbemittel-seite','werbemittel_url','support_url','affiliate_support_url'),'promolink'=>array('promolink','promo-link','promo_link','affiliate_link','tracking_link'));
    }
    private static function columns($headers){$n=array();foreach((array)$headers as $i=>$h)$n[self::key($h)]=$i;$out=array();foreach(self::aliases() as $field=>$aliases)foreach($aliases as $a){$k=self::key($a);if(array_key_exists($k,$n)){$out[$field]=$n[$k];break;}}return $out;}

    private static function parse_ds24_csv($body) {
        $body=self::encoding($body);$first=preg_split('/\r\n|\r|\n/',$body,2);$d=self::delimiter($first[0]??'');$fh=fopen('php://temp','r+');if(!$fh)return new WP_Error('ds24_csv_stream','CSV konnte nicht verarbeitet werden.');fwrite($fh,$body);rewind($fh);
        $headers=fgetcsv($fh,0,$d,'"','\\');if(!is_array($headers)){fclose($fh);return new WP_Error('ds24_csv_headers','CSV-Kopfzeile fehlt.');}$cols=self::columns($headers);foreach(array('vendor','product_id','product','entry_id','status','commission') as $r)if(!array_key_exists($r,$cols)){fclose($fh);return new WP_Error('ds24_csv_schema','Digistore24-CSV hat nicht die erwarteten Partnerschaftsspalten.');}
        $rows=array();$blocked=0;$seen=0;
        while(($v=fgetcsv($fh,0,$d,'"','\\'))!==false){if(++$seen>5000){fclose($fh);return new WP_Error('ds24_csv_row_limit','Mehr als 5.000 Partnerschaftszeilen werden nicht in einem Lauf verarbeitet.');}if(!array_filter($v,static function($x){return trim((string)$x)!=='';}))continue;$get=static function($f)use($cols,$v){return array_key_exists($f,$cols)?trim((string)($v[$cols[$f]]??'')):'';};$status=self::key($get('status'));if(!in_array($status,array('genehmigt','approved'),true)){$blocked++;continue;}$vendor=sanitize_text_field($get('vendor'));$pid=preg_replace('/\s+/','',$get('product_id'));$product=sanitize_text_field($get('product'));$eid=preg_replace('/\s+/','',$get('entry_id'));if($vendor===''||$product===''||!ctype_digit($pid)||!ctype_digit($eid)){$blocked++;continue;}if(isset($rows[$pid])){fclose($fh);return new WP_Error('ds24_csv_product_id_duplicate','Dieselbe Digistore24-Produkt-ID kommt mehrfach in der Bestandsdatei vor. Import wird vollständig abgebrochen.');}$support=$get('support_url');$promo=$get('promolink');if($support!==''&&(!filter_var($support,FILTER_VALIDATE_URL)||stripos($support,'https://')!==0))$support='';if($promo!==''&&(!filter_var($promo,FILTER_VALIDATE_URL)||stripos($promo,'https://')!==0))$promo='';$rows[$pid]=array('vendor'=>$vendor,'product_id'=>$pid,'product'=>$product,'entry_id'=>$eid,'status'=>'approved','commission'=>sanitize_text_field($get('commission')),'support_url'=>$support,'promolink'=>$promo);}
        fclose($fh);if(!$rows)return new WP_Error('ds24_csv_no_approved','Keine genehmigte Digistore24-Partnerschaft erkannt.');return array('rows'=>$rows,'blocked'=>$blocked);
    }

    private static function ds24_identity() {
        $s=get_option('ppar_network_digistore24_v1',array());$s=is_array($s)?$s:array();$key=defined('PPAR_DIGISTORE24_API_KEY')&&trim((string)PPAR_DIGISTORE24_API_KEY)!==''?trim((string)PPAR_DIGISTORE24_API_KEY):trim((string)($s['api_key']??''));$fp=strtolower(trim((string)($s['tested_key_fingerprint']??'')));$affiliate=trim((string)($s['affiliate_id']??''));
        if($key===''||!preg_match('/^[a-f0-9]{64}$/',$fp)||!hash_equals($fp,hash('sha256',$key))||!preg_match('/^[0-9A-Za-z._-]+$/',$affiliate))return new WP_Error('ds24_manual_identity_required','Digistore24-Datei erkannt. Vor dem Import muss derselbe Digistore24-Zugang unter Anbieter & APIs einmal erfolgreich read-only geprüft sein.');return array('key_fingerprint'=>$fp,'affiliate_id'=>$affiliate);
    }

    private static function group_ds24_rows($rows) {
        $g=array();foreach((array)$rows as $pid=>$r){$eid=(string)$r['entry_id'];if(!isset($g[$eid]))$g[$eid]=array('vendor'=>(string)$r['vendor'],'product_ids'=>array(),'products'=>array(),'commissions'=>array(),'support_url'=>(string)$r['support_url'],'promolink'=>(string)$r['promolink']);if($g[$eid]['vendor']!==(string)$r['vendor'])return new WP_Error('ds24_csv_entry_vendor_conflict','Dieselbe Werbemittel-ID ist mehreren Vendoren zugeordnet. Import wird vollständig abgebrochen.');$g[$eid]['product_ids'][(string)$pid]=(string)$pid;$g[$eid]['products'][(string)$pid]=(string)$r['product'];$g[$eid]['commissions'][(string)$pid]=(string)$r['commission'];if($g[$eid]['support_url']===''&&!empty($r['support_url']))$g[$eid]['support_url']=(string)$r['support_url'];if($g[$eid]['promolink']===''&&!empty($r['promolink']))$g[$eid]['promolink']=(string)$r['promolink'];}return $g;
    }

    private static function import_digistore24_partnerships($path,$name) {
        $identity=self::ds24_identity();if(is_wp_error($identity))return $identity;$body=self::read_full_ds24($path,$name);if(is_wp_error($body))return $body;$parsed=self::parse_ds24_csv($body);if(is_wp_error($parsed))return $parsed;$groups=self::group_ds24_rows($parsed['rows']);if(is_wp_error($groups))return $groups;
        $sha=hash('sha256',$body);$now=time();$oldstore=get_option('ppar_digistore24_marketplace_v1',array());$oldstore=is_array($oldstore)?$oldstore:array();$olditems=array();foreach((array)($oldstore['items']??array()) as $it)if(is_array($it)&&!empty($it['id']))$olditems[(string)$it['id']]=$it;$newids=array_fill_keys(array_keys($groups),true);$items=array();$removed=0;
        foreach($olditems as $eid=>$it){if((string)($it['source_kind']??'')==='digistore24_manual_csv'&&!isset($newids[$eid])){$removed++;continue;}if((string)($it['source_kind']??'')!=='digistore24_manual_csv'&&!isset($newids[$eid]))$items[$eid]=$it;}
        foreach($groups as $eid=>$g){$old=$olditems[$eid]??array();$pids=array_values($g['product_ids']);sort($pids,SORT_STRING);$products=$g['products'];ksort($products,SORT_STRING);$support=(string)$g['support_url'];if($support===''&&!empty($old['support_url'])&&filter_var($old['support_url'],FILTER_VALIDATE_URL)&&stripos((string)$old['support_url'],'https://')===0)$support=(string)$old['support_url'];$promo=(string)$g['promolink'];if($promo===''&&!empty($old['promolink'])&&filter_var($old['promolink'],FILTER_VALIDATE_URL)&&stripos((string)$old['promolink'],'https://')===0)$promo=(string)$old['promolink'];$desc=array();foreach($products as $pid=>$title)$desc[]=$pid.' · '.$title;$items[$eid]=array('id'=>(string)$eid,'main_product_id'=>(string)$pids[0],'all_product_ids'=>$pids,'approval_status'=>'approved','approval_status_msg'=>'Genehmigt · manueller Digistore24-CSV-Import','headline'=>count($pids)===1?(string)reset($products):(string)$g['vendor'].' · '.count($pids).' Produkte','description'=>implode("\n",$desc),'product_category'=>'','product_category_id'=>0,'affiliate_share'=>null,'stats_stars'=>null,'stats_count_orders'=>0,'vendor'=>(string)$g['vendor'],'commissions'=>$g['commissions'],'support_url'=>$support,'promolink'=>$promo,'source_kind'=>'digistore24_manual_csv','manual_import_sha256'=>$sha,'manual_imported_at'=>$now);}
        ksort($items,SORT_STRING);$parts=get_option('ppar_digistore24_partnerships_v1',array());$parts=is_array($parts)?$parts:array();foreach($parts as $eid=>$r)if(is_array($r)&&(string)($r['source']??'')==='manual_csv'&&!isset($newids[(string)$eid]))unset($parts[$eid]);
        foreach($groups as $eid=>$g){$old=is_array($parts[$eid]??null)?$parts[$eid]:array();$pids=array_values($g['product_ids']);sort($pids,SORT_STRING);$parts[$eid]=array('confirmed'=>1,'confirmed_at'=>absint($old['confirmed_at']??0)?:$now,'key_fingerprint'=>$identity['key_fingerprint'],'affiliate_id'=>$identity['affiliate_id'],'source'=>'manual_csv','approval_status'=>'approved','product_ids'=>$pids,'vendor'=>$g['vendor'],'products'=>$g['products'],'commissions'=>$g['commissions'],'imported_at'=>$now,'import_sha256'=>$sha);}
        $vendors=array_values(array_unique(array_map(static function($r){return (string)$r['vendor'];},array_values($parsed['rows']))));sort($vendors,SORT_NATURAL|SORT_FLAG_CASE);$inventory=array('rows'=>$parsed['rows'],'product_count'=>count($parsed['rows']),'source_count'=>count($groups),'vendors'=>$vendors,'blocked'=>absint($parsed['blocked']??0),'imported_at'=>$now,'sha256'=>$sha,'key_fingerprint'=>$identity['key_fingerprint'],'affiliate_id'=>$identity['affiliate_id']);$store=array_merge($oldstore,array('items'=>array_values($items),'last_checked'=>$now,'last_status'=>'manual_import','last_message'=>count($parsed['rows']).' genehmigte Produktpartnerschaften aus Digistore24-CSV übernommen; '.count($groups).' Werbemittelquellen; '.count($vendors).' Vendoren.','blocked'=>absint($parsed['blocked']??0),'key_fingerprint'=>$identity['key_fingerprint'],'affiliate_id'=>$identity['affiliate_id']));
        update_option(self::DS24_INVENTORY_OPTION,$inventory,false);update_option('ppar_digistore24_marketplace_v1',$store,false);update_option('ppar_digistore24_partnerships_v1',$parts,false);
        $message='Digistore24 erkannt · '.count($parsed['rows']).' genehmigte Produktpartnerschaften · '.count($groups).' Werbemittelquellen · '.count($vendors).' Vendoren';if(!empty($parsed['blocked']))$message.=' · '.absint($parsed['blocked']).' nicht genehmigte/ungültige Zeilen blockiert';if($removed>0)$message.=' · '.$removed.' alte manuelle Quelle(n) aus der Inventur entfernt';$message.='. Bestehende veröffentlichte LKG-Ausgaben wurden nicht verändert.';return array('status'=>'success','message'=>$message,'sha256'=>$sha,'product_count'=>count($parsed['rows']),'source_count'=>count($groups),'vendor_count'=>count($vendors));
    }

    private static function delegate_idealo($file){if(!class_exists('Pferdeportal_Affiliate_Router'))self::redirect('failed','Affiliate-Router ist nicht geladen.');$_FILES['idealo_feed']=$file;$_POST['ppar_idealo_nonce']=wp_create_nonce('ppar_idealo_import_file');$_REQUEST['ppar_idealo_nonce']=$_POST['ppar_idealo_nonce'];Pferdeportal_Affiliate_Router::instance()->handle_idealo_import_file();exit;}
    private static function delegate_creatives($file,$provider,$name){if(!class_exists('Pferdeportal_Affiliate_Router'))self::redirect('failed','Affiliate-Router ist nicht geladen.');$hash=is_readable((string)$file['tmp_name'])?hash_file('sha256',(string)$file['tmp_name']):'';$_FILES['creative_file']=$file;$_POST['provider']=sanitize_key($provider);$_POST['partner_external_id']='manual-'.substr((string)$hash,0,20);$_POST['partner_name']=ucfirst($provider).' · Dateiimport '.sanitize_file_name($name);$_POST['creative_codes']='';$_POST['ppar_creative_library_nonce']=wp_create_nonce('ppar_creative_library_import');$_REQUEST['ppar_creative_library_nonce']=$_POST['ppar_creative_library_nonce'];Pferdeportal_Affiliate_Router::instance()->handle_creative_library_import();exit;}
    private static function remember($provider,$message,$sha){update_option(self::LAST_OPTION,array('provider'=>sanitize_text_field($provider),'message'=>sanitize_text_field($message),'sha256'=>preg_replace('/[^a-f0-9]/','',strtolower($sha)),'imported_at'=>time()),false);}
    private static function redirect($status,$message){wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-kiss-providers','ppar_universal_import'=>sanitize_key($status),'ppar_universal_message'=>rawurlencode(sanitize_text_field($message))),admin_url('admin.php')));exit;}
}