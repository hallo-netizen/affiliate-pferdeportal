<?php
if (!defined('ABSPATH')) { exit; }

final class APKW_Admin {
    private const PAGE_SLUG='apkw-category-workflow';
    private const MAX_UPLOAD_BYTES=20971520;
    private const PREFLIGHT_TTL=900;

    public static function init():void{
        add_action('admin_menu',[__CLASS__,'menu']);
        add_action('admin_post_apkw_run_global_coverage',[__CLASS__,'run_global_coverage']);
        add_action('admin_post_apkw_run_detail_research',[__CLASS__,'run_detail_research']);
        add_action('admin_post_apkw_sign_initial_review',[__CLASS__,'sign_initial_review']);
        add_action('admin_post_apkw_sign_global_gap_review',[__CLASS__,'sign_global_gap_review']);
        add_action('admin_post_apkw_sign_final_review',[__CLASS__,'sign_final_review']);
    }
    public static function menu():void{add_management_page('Kategorie-Workflow','Kategorie-Workflow','manage_options',self::PAGE_SLUG,[__CLASS__,'render']);}

    public static function render():void{
        if(!current_user_can('manage_options'))wp_die('Keine Berechtigung.','Zugriff verweigert',['response'=>403]);
        $notice=null;$error=null;$connection=null;$preflight=null;$preflight_token=null;$detail_preflight=null;$detail_token=null;$report=null;

        if($_SERVER['REQUEST_METHOD']==='POST'&&isset($_POST['apkw_save_settings'])){
            check_admin_referer('apkw_save_settings','apkw_settings_nonce');
            APKW_Settings::save(['login'=>wp_unslash((string)($_POST['apkw_login']??'')),'password'=>wp_unslash((string)($_POST['apkw_password']??'')),'location_name'=>wp_unslash((string)($_POST['apkw_location_name']??'Germany')),'language_code'=>wp_unslash((string)($_POST['apkw_language_code']??'de'))]);$notice='Einstellungen gespeichert.';
        }
        if($_SERVER['REQUEST_METHOD']==='POST'&&isset($_POST['apkw_test_connection'])){
            check_admin_referer('apkw_test_connection','apkw_connection_nonce');
            try{$connection=APKW_DataForSEO::test_connection();}catch(Throwable $e){$error=$e->getMessage();}
        }
        if($_SERVER['REQUEST_METHOD']==='POST'&&isset($_POST['apkw_preflight_draft'])){
            check_admin_referer('apkw_preflight_draft','apkw_preflight_nonce');
            try{[$draft,$raw]=self::read_upload('draft_package');$preflight=APKW_Research::preflight_draft($draft);if(!$preflight['valid'])throw new RuntimeException('Vorprüfung BLOCKED: '.implode(', ',array_column($preflight['errors'],'code')));$preflight_token=bin2hex(random_bytes(16));set_transient('apkw_preflight_'.$preflight_token,['draft'=>$draft,'raw_sha256'=>hash('sha256',$raw),'created_at_utc'=>gmdate('c')],self::PREFLIGHT_TTL);}catch(Throwable $e){$error=$e->getMessage();}
        }
        if($_SERVER['REQUEST_METHOD']==='POST'&&isset($_POST['apkw_preflight_detail'])){
            check_admin_referer('apkw_preflight_detail','apkw_detail_nonce');
            try{[$draft,$draft_raw]=self::read_upload('detail_draft_package');[$global,$global_raw]=self::read_upload('global_coverage_package');$detail_preflight=APKW_Research::preflight_detail($draft,$global);if(!$detail_preflight['valid'])throw new RuntimeException('Detail-Vorprüfung BLOCKED: '.implode(', ',array_column($detail_preflight['errors'],'code')));$detail_token=bin2hex(random_bytes(16));set_transient('apkw_detail_'.$detail_token,['draft'=>$draft,'global'=>$global,'draft_sha256'=>hash('sha256',$draft_raw),'global_sha256'=>hash('sha256',$global_raw),'created_at_utc'=>gmdate('c')],self::PREFLIGHT_TTL);}catch(Throwable $e){$error=$e->getMessage();}
        }
        if($_SERVER['REQUEST_METHOD']==='POST'&&isset($_POST['apkw_validate_final'])){
            check_admin_referer('apkw_validate_final','apkw_final_nonce');
            try{[$research,$research_raw]=self::read_upload('research_package');[$package,$raw]=self::read_upload('structure_package');$rv=APKW_Research::verify_package($research);if(!$rv['valid'])throw new RuntimeException('Research-Paket ungültig: '.implode(', ',$rv['errors']));$bv=APKW_Research::verify_binding($package,$research);if(!$bv['valid'])throw new RuntimeException('Research-Bindung ungültig: '.implode(', ',$bv['errors']));$validation=APKW_Validator::validate($package);$evidence=APKW_ResearchEvidence::analyze($package,$research,$validation);$comparison=APKW_Comparator::compare($package,$validation);$report=self::report($package,$raw,$research,$research_raw,$rv,$bv,$validation,$evidence,$comparison);}catch(Throwable $e){$error=$e->getMessage();}
        }

        $credentials=APKW_Settings::credentials();$defaults=APKW_Settings::defaults();
        ?>
        <div class="wrap"><h1>Kategorie-Workflow</h1>
        <div class="notice notice-info inline"><p><strong>Verbindlicher Ablauf:</strong> Projektkonzept → 3-Säulen-Erstentwurf → sichtbare Erstprüfung + Hashfreigabe → 1× Global-Coverage → Hauptthemen-Korrektur → sichtbare Global-Gap-Prüfung + Hashfreigabe → Detailresearch → Korrekturlauf → read-only Gesamtprüfung → sichtbare Finalprüfung + Hashfreigabe → FINAL.</p></div>
        <div class="notice notice-warning inline"><p><strong>Keine Portal-Schreibfunktion.</strong> Keine Seiten, Kategorien oder HivePress-Terme werden angelegt, geändert oder gelöscht.</p></div>
        <?php if($notice):?><div class="notice notice-success inline"><p><?php echo esc_html($notice);?></p></div><?php endif;?>
        <?php if($error):?><div class="notice notice-error inline"><p><?php echo esc_html($error);?></p></div><?php endif;?>

        <h2>1. DataForSEO einrichten und kostenlos testen</h2>
        <form method="post"><?php wp_nonce_field('apkw_save_settings','apkw_settings_nonce');?><table class="form-table"><tbody>
        <tr><th><label for="apkw_login">API Login</label></th><td><input class="regular-text" id="apkw_login" name="apkw_login" type="text" value="<?php echo esc_attr(APKW_Settings::constants_active()?'':$credentials['login']);?>" <?php disabled(APKW_Settings::constants_active());?>></td></tr>
        <tr><th><label for="apkw_password">API Passwort</label></th><td><input class="regular-text" id="apkw_password" name="apkw_password" type="password" value="" placeholder="<?php echo esc_attr($credentials['password']!==''?'gespeichert – leer lassen zum Beibehalten':'');?>" <?php disabled(APKW_Settings::constants_active());?>></td></tr>
        <tr><th><label for="apkw_location_name">Standard-Zielmarkt</label></th><td><input class="regular-text" id="apkw_location_name" name="apkw_location_name" value="<?php echo esc_attr($defaults['location_name']);?>"></td></tr>
        <tr><th><label for="apkw_language_code">Standard-Sprache</label></th><td><input class="small-text" id="apkw_language_code" name="apkw_language_code" value="<?php echo esc_attr($defaults['language_code']);?>"></td></tr>
        </tbody></table><?php submit_button('Einstellungen speichern','secondary','apkw_save_settings');?></form>
        <form method="post"><?php wp_nonce_field('apkw_test_connection','apkw_connection_nonce');?><?php submit_button('DataForSEO-Verbindung kostenlos testen','secondary','apkw_test_connection');?></form>
        <?php if(is_array($connection)):?><div class="notice notice-success inline"><p><strong>PASS:</strong> API erreichbar, Zugangsdaten gültig. Provider-Kosten dieses Tests: <?php echo esc_html(number_format((float)$connection['cost_usd'],4,'.',''));?> USD.</p></div><?php endif;?>
        <p><em>Der Verbindungstest nutzt ausschließlich DataForSEO <code>/v3/appendix/user_data</code>. Dieser Test führt keine Keyword-Recherche aus.</em></p>

        <hr><h2>2. Projektweite Hauptthemen-Coverage</h2>
        <p>Der Chat/Master liefert zuerst den dreisäuligen <code>RESEARCH_DRAFT</code>. Nach der sichtbaren Erstprüfung muss der Nutzer genau dieses Paket hier serverseitig signieren. Ein bloß eingetragener Status oder Hash ist ungültig.</p>
        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php'));?>" enctype="multipart/form-data"><input type="hidden" name="action" value="apkw_sign_initial_review"><?php wp_nonce_field('apkw_sign_initial_review','apkw_sign_initial_nonce');?><input type="hidden" name="MAX_FILE_SIZE" value="<?php echo esc_attr((string)self::MAX_UPLOAD_BYTES);?>"><p><label><strong>Noch nicht freigegebener RESEARCH_DRAFT.json:</strong><br><input type="file" name="initial_review_draft" accept="application/json,.json" required></label></p><p><label><input type="checkbox" name="apkw_visible_review_confirmation" value="1" required> Ich bestätige ausdrücklich, dass ich genau den sichtbaren vollständigen Drei-Säulen-Baum geprüft und freigegeben habe.</label></p><p><label><strong>Review-Scope SHA-256 aus der sichtbaren Chat-Prüfung:</strong><br><input class="large-text code" name="apkw_expected_review_scope_sha256" pattern="[a-f0-9]{64}" required></label></p><p><label><strong>Kurze Freigabe-Zusammenfassung:</strong><br><input class="large-text" name="apkw_review_summary" required></label></p><?php submit_button('Erst-Sichtfreigabe serverseitig signieren','secondary');?></form>
        <p><em>Erst das heruntergeladene, serverseitig signierte Paket darf in den kostenfreien Preflight und danach in den einmaligen Paid-Global-Call.</em></p>
        <form method="post" enctype="multipart/form-data"><?php wp_nonce_field('apkw_preflight_draft','apkw_preflight_nonce');?><input type="hidden" name="MAX_FILE_SIZE" value="<?php echo esc_attr((string)self::MAX_UPLOAD_BYTES);?>"><p><label><strong>RESEARCH_DRAFT.json:</strong><br><input type="file" name="draft_package" accept="application/json,.json" required></label></p><?php submit_button('Kostenfreien Global-Coverage-Prüfplan erzeugen','primary','apkw_preflight_draft');?></form>
        <?php if(is_array($preflight)&&$preflight_token): self::render_global_preflight($preflight,$preflight_token,$defaults); endif;?>

        <hr><h2>3. Detailresearch nach Hauptthemen-Korrektur</h2>
        <p>Nach Global-Coverage korrigiert Chat/Master den Baum und dokumentiert jeden relevanten Global-Fund. Vor Detailresearch muss auch dieser exakte Stand sichtbar geprüft und anschließend hier serverseitig signiert werden.</p>
        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php'));?>" enctype="multipart/form-data"><input type="hidden" name="action" value="apkw_sign_global_gap_review"><?php wp_nonce_field('apkw_sign_global_gap_review','apkw_sign_global_gap_nonce');?><input type="hidden" name="MAX_FILE_SIZE" value="<?php echo esc_attr((string)self::MAX_UPLOAD_BYTES);?>"><p><label><strong>Korrigierter RESEARCH_DRAFT.json:</strong><br><input type="file" name="global_gap_draft" accept="application/json,.json" required></label></p><p><label><strong>Zugehöriges Global-Coverage-Paket.json:</strong><br><input type="file" name="global_gap_package" accept="application/json,.json" required></label></p><p><label><input type="checkbox" name="apkw_visible_review_confirmation" value="1" required> Ich bestätige ausdrücklich den sichtbaren korrigierten Gesamtbaum und sämtliche Global-Gap-Entscheidungen.</label></p><p><label><strong>Review-Scope SHA-256 aus der sichtbaren Chat-Prüfung:</strong><br><input class="large-text code" name="apkw_expected_review_scope_sha256" pattern="[a-f0-9]{64}" required></label></p><p><label><strong>Kurze Freigabe-Zusammenfassung:</strong><br><input class="large-text" name="apkw_review_summary" required></label></p><?php submit_button('Global-Gap-Sichtfreigabe serverseitig signieren','secondary');?></form>
        <p>Die bereits bezahlte Global-Coverage wird beim anschließenden Detailresearch wiederverwendet und <strong>nicht erneut abgerufen</strong>.</p>
        <form method="post" enctype="multipart/form-data"><?php wp_nonce_field('apkw_preflight_detail','apkw_detail_nonce');?><input type="hidden" name="MAX_FILE_SIZE" value="<?php echo esc_attr((string)self::MAX_UPLOAD_BYTES);?>"><p><label><strong>Korrigierter RESEARCH_DRAFT.json:</strong><br><input type="file" name="detail_draft_package" accept="application/json,.json" required></label></p><p><label><strong>Global-Coverage-Paket.json:</strong><br><input type="file" name="global_coverage_package" accept="application/json,.json" required></label></p><?php submit_button('Kostenfreien Detail-Prüfplan erzeugen','primary','apkw_preflight_detail');?></form>
        <?php if(is_array($detail_preflight)&&$detail_token): self::render_detail_preflight($detail_preflight,$detail_token,$defaults); endif;?>

        <hr><h2>4. Korrigierte Struktur prüfen und Sichtprüfung vorbereiten</h2>
        <form method="post" enctype="multipart/form-data"><?php wp_nonce_field('apkw_validate_final','apkw_final_nonce');?><input type="hidden" name="MAX_FILE_SIZE" value="<?php echo esc_attr((string)self::MAX_UPLOAD_BYTES);?>"><p><label><strong>Originales Research-Paket:</strong><br><input type="file" name="research_package" accept="application/json,.json" required></label></p><p><label><strong>Finales Strukturpaket aus Chat/Master:</strong><br><input type="file" name="structure_package" accept="application/json,.json" required></label></p><?php submit_button('Struktur read-only prüfen','primary','apkw_validate_final');?></form>
        <?php if(is_array($report))self::render_report($report);?>
        <h3>Finale Sichtfreigabe signieren</h3><p>Nur wenn die read-only Prüfung <code>READY_FOR_VISIBLE_SIGHT_REVIEW</code> ergeben hat und der exakt gleiche Baum anschließend vollständig sichtbar freigegeben wurde.</p>
        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php'));?>" enctype="multipart/form-data"><input type="hidden" name="action" value="apkw_sign_final_review"><?php wp_nonce_field('apkw_sign_final_review','apkw_sign_final_nonce');?><input type="hidden" name="MAX_FILE_SIZE" value="<?php echo esc_attr((string)self::MAX_UPLOAD_BYTES);?>"><p><label><strong>READ_ONLY_PREVIEW-Strukturpaket:</strong><br><input type="file" name="final_review_structure" accept="application/json,.json" required></label></p><p><label><strong>Zugehöriges Research-Paket:</strong><br><input type="file" name="final_review_research" accept="application/json,.json" required></label></p><p><label><input type="checkbox" name="apkw_visible_review_confirmation" value="1" required> Ich bestätige ausdrücklich die sichtbare Finalprüfung genau dieses vollständigen Drei-Säulen-Baums.</label></p><p><label><strong>Review-Scope SHA-256 aus der sichtbaren Chat-Prüfung:</strong><br><input class="large-text code" name="apkw_expected_review_scope_sha256" pattern="[a-f0-9]{64}" required></label></p><p><label><strong>Kurze Freigabe-Zusammenfassung:</strong><br><input class="large-text" name="apkw_review_summary" required></label></p><?php submit_button('Finale Sichtfreigabe serverseitig signieren','secondary');?></form>
        </div><?php
    }

    private static function render_global_preflight(array $p,string $token,array $defaults):void{
        ?><div class="notice notice-success inline"><p><strong>Vorprüfung PASS.</strong> Noch kein kostenpflichtiger Keyword-Aufruf ausgeführt.</p></div>
        <table class="widefat striped" style="max-width:900px"><tbody>
        <tr><th>Projekt</th><td><?php echo esc_html($p['project_name']);?></td></tr><tr><th>Projektweite Discovery-Seeds</th><td><?php echo esc_html((string)$p['global_discovery_seed_count']);?></td></tr><tr><th>Jetzt geplanter DataForSEO-Aufruf</th><td><strong>1</strong> – ausschließlich projektweite Hauptthemen-Coverage</td></tr>
        </tbody></table>
        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php'));?>"><input type="hidden" name="action" value="apkw_run_global_coverage"><input type="hidden" name="apkw_preflight_token" value="<?php echo esc_attr($token);?>"><?php wp_nonce_field('apkw_run_global_coverage','apkw_global_nonce');?><table class="form-table"><tbody><tr><th><label for="apkw_global_location">Zielmarkt</label></th><td><input class="regular-text" id="apkw_global_location" name="apkw_location_name" value="<?php echo esc_attr($defaults['location_name']);?>" required></td></tr><tr><th><label for="apkw_global_language">Sprache</label></th><td><input class="small-text" id="apkw_global_language" name="apkw_language_code" value="<?php echo esc_attr($defaults['language_code']);?>" required></td></tr><tr><th><label for="apkw_global_limit">Coverage-Ergebnisse</label></th><td><input id="apkw_global_limit" name="apkw_global_limit" type="number" min="50" max="1000" value="1000"></td></tr><tr><th>SERP-Metadaten</th><td><label><input name="apkw_include_serp" type="checkbox" value="1"> mitnehmen</label></td></tr></tbody></table><p><label><input type="checkbox" name="apkw_paid_confirmation" value="1" required> Ich bestätige genau 1 kostenpflichtigen DataForSEO-Aufruf für die projektweite Coverage.</label></p><?php submit_button('Global-Coverage starten und Paket laden','primary');?></form><?php
    }

    private static function render_detail_preflight(array $p,string $token,array $defaults):void{
        ?><div class="notice notice-success inline"><p><strong>Detail-Vorprüfung PASS.</strong> Global-Coverage ist gültig gebunden; noch keine Detail-API-Aufrufe ausgeführt.</p></div>
        <table class="widefat striped" style="max-width:900px"><tbody>
        <tr><th>Projekt</th><td><?php echo esc_html($p['project_name']);?></td></tr><tr><th>Research-Cluster</th><td><?php echo esc_html((string)$p['cluster_count']);?></td></tr><tr><th>Exakte Kategorienamen/Keywords</th><td><?php echo esc_html((string)$p['planned_overview_keyword_count']);?></td></tr><tr><th>Jetzt geplante Detail-Aufrufe</th><td><strong><?php echo esc_html((string)$p['planned_detail_paid_calls']['total']);?></strong> (<?php echo esc_html((string)$p['planned_detail_paid_calls']['cluster_keyword_ideas']);?> Cluster + <?php echo esc_html((string)$p['planned_detail_paid_calls']['keyword_overview']);?> Overview; <strong>0 erneute Global-Coverage</strong>)</td></tr>
        </tbody></table>
        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php'));?>"><input type="hidden" name="action" value="apkw_run_detail_research"><input type="hidden" name="apkw_detail_token" value="<?php echo esc_attr($token);?>"><?php wp_nonce_field('apkw_run_detail_research','apkw_detail_run_nonce');?><table class="form-table"><tbody><tr><th><label for="apkw_detail_location">Zielmarkt</label></th><td><input class="regular-text" id="apkw_detail_location" name="apkw_location_name" value="<?php echo esc_attr($defaults['location_name']);?>" required></td></tr><tr><th><label for="apkw_detail_language">Sprache</label></th><td><input class="small-text" id="apkw_detail_language" name="apkw_language_code" value="<?php echo esc_attr($defaults['language_code']);?>" required></td></tr><tr><th><label for="apkw_cluster_limit">Ergebnisse je Cluster</label></th><td><input id="apkw_cluster_limit" name="apkw_cluster_limit" type="number" min="10" max="1000" value="300"></td></tr><tr><th>SERP-Metadaten</th><td><label><input name="apkw_include_serp" type="checkbox" value="1"> mitnehmen</label></td></tr></tbody></table><p><label><input type="checkbox" name="apkw_paid_confirmation" value="1" required> Ich bestätige die oben ausgewiesene Anzahl kostenpflichtiger Detail-Aufrufe.</label></p><?php submit_button('Detailresearch starten und Research-Paket laden','primary');?></form><?php
    }

    public static function sign_initial_review():void{
        self::require_review_actor('apkw_sign_initial_review','apkw_sign_initial_nonce');
        try{
            [$draft]=self::read_upload('initial_review_draft');
            if(isset($draft['initial_human_sight_review'])) throw new RuntimeException('Initialpaket enthält bereits eine Freigabe. Für eine neue Freigabe muss der unsignierte aktuelle Sichtstand verwendet werden.');
            $preflight=APKW_Research::preflight_draft($draft,false);
            self::require_visible_scope_match(APKW_Validator::initial_review_scope_hash($draft));
            if(!$preflight['valid']) throw new RuntimeException('Initialer Strukturstand BLOCKED: '.implode(', ',array_column($preflight['errors'],'code')));
            $draft['initial_human_sight_review']=APKW_Validator::create_signed_review_receipt($draft,'initial',self::review_summary(),get_current_user_id());
            $gate=APKW_Validator::validate_initial_review_gate($draft);
            if(!$gate['valid']) throw new RuntimeException('Serverseitige Initialfreigabe konnte nicht verifiziert werden: '.implode(', ',array_column($gate['errors'],'code')));
            self::download_json($draft,'kategorie-research-draft-initial-freigegeben-'.gmdate('Ymd-His').'-utc.json');
        }catch(Throwable $e){wp_die(esc_html($e->getMessage()),'Initiale Sichtfreigabe BLOCKED',['response'=>400]);}
    }

    public static function sign_global_gap_review():void{
        self::require_review_actor('apkw_sign_global_gap_review','apkw_sign_global_gap_nonce');
        try{
            [$draft]=self::read_upload('global_gap_draft');[$global]=self::read_upload('global_gap_package');
            unset($draft['global_gap_human_review']);
            $initial=APKW_Validator::validate_initial_review_gate($draft);
            if(!$initial['valid']) throw new RuntimeException('Initiale Sichtfreigabe ist nicht gültig: '.implode(', ',array_column($initial['errors'],'code')));
            $gv=APKW_Research::verify_global_coverage($global);if(!$gv['valid'])throw new RuntimeException('Global-Coverage-Paket ungültig: '.implode(', ',$gv['errors']));
            $draft['global_coverage_binding']=['package_id'=>(string)($global['package_id']??''),'content_sha256'=>(string)($global['content_sha256']??'')];
            $binding=APKW_Research::verify_global_binding($draft,$global);if(!$binding['valid'])throw new RuntimeException('Global-Coverage-Bindung ungültig: '.implode(', ',$binding['errors']));
            $validation=APKW_Validator::validate($draft);if(!$validation['valid'])throw new RuntimeException('Korrigierter Draft BLOCKED: '.implode(', ',array_column($validation['errors'],'code')));
            $gap=APKW_Research::global_coverage_gate($draft,$global);if(!$gap['valid'])throw new RuntimeException('Global-Gaps sind nicht vollständig entschieden: '.implode(', ',array_column($gap['errors'],'code')));
            $draft['global_gap_human_review']=APKW_Validator::create_signed_review_receipt($draft,'global_gap',self::review_summary(),get_current_user_id());
            $gate=APKW_Validator::validate_global_gap_review_gate($draft,$global);if(!$gate['valid'])throw new RuntimeException('Serverseitige Global-Gap-Freigabe konnte nicht verifiziert werden: '.implode(', ',array_column($gate['errors'],'code')));
            self::download_json($draft,'kategorie-research-draft-global-gap-freigegeben-'.gmdate('Ymd-His').'-utc.json');
        }catch(Throwable $e){wp_die(esc_html($e->getMessage()),'Global-Gap-Sichtfreigabe BLOCKED',['response'=>400]);}
    }

    public static function sign_final_review():void{
        self::require_review_actor('apkw_sign_final_review','apkw_sign_final_nonce');
        try{
            [$package]=self::read_upload('final_review_structure');[$research]=self::read_upload('final_review_research');
            if((string)($package['mode']??'')!=='READ_ONLY_PREVIEW') throw new RuntimeException('Finale Sichtfreigabe benötigt exakt den zuvor read-only geprüften READ_ONLY_PREVIEW-Stand.');
            unset($package['human_sight_review']);
            $rv=APKW_Research::verify_package($research);if(!$rv['valid'])throw new RuntimeException('Research-Paket ungültig: '.implode(', ',$rv['errors']));
            $bv=APKW_Research::verify_binding($package,$research);if(!$bv['valid'])throw new RuntimeException('Research-Bindung ungültig: '.implode(', ',$bv['errors']));
            $validation=APKW_Validator::validate($package);$evidence=APKW_ResearchEvidence::analyze($package,$research,$validation);$comparison=APKW_Comparator::compare($package,$validation);
            if(!$validation['valid']||!$evidence['valid']||($comparison['status']??'')!=='PASS_READ_ONLY_PREVIEW') throw new RuntimeException('READ_ONLY_PREVIEW ist nicht vollständig PASS und darf nicht final freigegeben werden.');
            self::require_visible_scope_match(APKW_Validator::review_scope_hash($package));
            $package['mode']='FINAL_APPROVED';
            $package['human_sight_review']=APKW_Validator::create_signed_review_receipt($package,'final',self::review_summary(),get_current_user_id());
            $final_validation=APKW_Validator::validate($package);$final_evidence=APKW_ResearchEvidence::analyze($package,$research,$final_validation);$final_comparison=APKW_Comparator::compare($package,$final_validation);
            if(!$final_validation['valid']||!$final_evidence['valid']||($final_comparison['status']??'')!=='PASS_READ_ONLY_PREVIEW') throw new RuntimeException('FINAL_APPROVED konnte nach Serversignatur nicht vollständig verifiziert werden.');
            self::download_json($package,'kategorie-final-approved-'.gmdate('Ymd-His').'-utc.json');
        }catch(Throwable $e){wp_die(esc_html($e->getMessage()),'Finale Sichtfreigabe BLOCKED',['response'=>400]);}
    }

    private static function require_review_actor(string $action,string $nonce_field):void{
        if(!current_user_can('manage_options'))wp_die('Keine Berechtigung.','Zugriff verweigert',['response'=>403]);
        check_admin_referer($action,$nonce_field);
        if(!isset($_POST['apkw_visible_review_confirmation']))wp_die('Ausdrückliche sichtbare Nutzerfreigabe fehlt.','BLOCKED',['response'=>400]);
        if(get_current_user_id()<1)wp_die('Freigebender WordPress-Benutzer konnte nicht bestimmt werden.','BLOCKED',['response'=>400]);
    }

    private static function require_visible_scope_match(string $actual):void{
        $expected=sanitize_key(wp_unslash((string)($_POST['apkw_expected_review_scope_sha256']??'')));
        if(!preg_match('/^[a-f0-9]{64}$/',$expected)) throw new RuntimeException('Review-Scope SHA-256 aus der sichtbaren Prüfung fehlt oder ist ungültig.');
        if(!hash_equals($actual,$expected)) throw new RuntimeException('Hochgeladenes Paket entspricht nicht exakt dem sichtbar freigegebenen Review-Scope. Erneute Sichtprüfung erforderlich.');
    }

    private static function review_summary():string{
        $summary=sanitize_text_field(wp_unslash((string)($_POST['apkw_review_summary']??'')));
        if($summary==='')throw new RuntimeException('Freigabe-Zusammenfassung fehlt.');
        return $summary;
    }

    public static function run_global_coverage():void{
        if(!current_user_can('manage_options'))wp_die('Keine Berechtigung.','Zugriff verweigert',['response'=>403]);
        check_admin_referer('apkw_run_global_coverage','apkw_global_nonce');
        if(!isset($_POST['apkw_paid_confirmation']))wp_die('Kostenpflichtige Global-Coverage wurde nicht ausdrücklich bestätigt.','BLOCKED',['response'=>400]);
        $token=sanitize_key(wp_unslash((string)($_POST['apkw_preflight_token']??'')));$saved=get_transient('apkw_preflight_'.$token);
        if(!is_array($saved)||!is_array($saved['draft']??null))wp_die('Vorprüfungs-Token fehlt oder ist abgelaufen. Bitte Vorprüfung erneut ausführen.','BLOCKED',['response'=>400]);
        $location=sanitize_text_field(wp_unslash((string)($_POST['apkw_location_name']??'')));$language=sanitize_key(wp_unslash((string)($_POST['apkw_language_code']??'')));$global_limit=max(50,min(1000,absint($_POST['apkw_global_limit']??1000)));$serp=isset($_POST['apkw_include_serp']);
        try{$package=APKW_Research::build_global_coverage($saved['draft'],$location,$language,$global_limit,$serp);delete_transient('apkw_preflight_'.$token);self::download_json($package,'kategorie-global-coverage-'.sanitize_title((string)($package['project']['name']??'projekt')).'-'.gmdate('Ymd-His').'-utc.json');}catch(Throwable $e){wp_die(esc_html($e->getMessage()),'Global-Coverage fehlgeschlagen',['response'=>500]);}
    }

    public static function run_detail_research():void{
        if(!current_user_can('manage_options'))wp_die('Keine Berechtigung.','Zugriff verweigert',['response'=>403]);
        check_admin_referer('apkw_run_detail_research','apkw_detail_run_nonce');
        if(!isset($_POST['apkw_paid_confirmation']))wp_die('Kostenpflichtige Detailrecherche wurde nicht ausdrücklich bestätigt.','BLOCKED',['response'=>400]);
        $token=sanitize_key(wp_unslash((string)($_POST['apkw_detail_token']??'')));$saved=get_transient('apkw_detail_'.$token);
        if(!is_array($saved)||!is_array($saved['draft']??null)||!is_array($saved['global']??null))wp_die('Detail-Vorprüfungs-Token fehlt oder ist abgelaufen. Bitte Detail-Vorprüfung erneut ausführen.','BLOCKED',['response'=>400]);
        $location=sanitize_text_field(wp_unslash((string)($_POST['apkw_location_name']??'')));$language=sanitize_key(wp_unslash((string)($_POST['apkw_language_code']??'')));$limit=max(10,min(1000,absint($_POST['apkw_cluster_limit']??300)));$serp=isset($_POST['apkw_include_serp']);
        try{$package=APKW_Research::build_from_draft($saved['draft'],$saved['global'],$location,$language,$limit,$serp);delete_transient('apkw_detail_'.$token);self::download_json($package,'kategorie-research-'.sanitize_title((string)($package['project']['name']??'projekt')).'-'.gmdate('Ymd-His').'-utc.json');}catch(Throwable $e){wp_die(esc_html($e->getMessage()),'Detailrecherche fehlgeschlagen',['response'=>500]);}
    }

    private static function download_json(array $package,string $filename):void{
        $json=wp_json_encode($package,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);if(!is_string($json))throw new RuntimeException('JSON-Paket konnte nicht serialisiert werden.');nocache_headers();header('Content-Type: application/json; charset=utf-8');header('Content-Disposition: attachment; filename="'.$filename.'"');header('Content-Length: '.strlen($json));echo $json;exit;
    }

    private static function read_upload(string $field):array{
        if(!isset($_FILES[$field])||!is_array($_FILES[$field]))throw new RuntimeException('Datei fehlt: '.$field);$file=$_FILES[$field];if((int)$file['error']!==UPLOAD_ERR_OK)throw new RuntimeException('Uploadfehler: '.(int)$file['error']);if((int)$file['size']<=0||(int)$file['size']>self::MAX_UPLOAD_BYTES)throw new RuntimeException('Dateigröße unzulässig.');if(!is_uploaded_file($file['tmp_name']))throw new RuntimeException('Upload konnte nicht verifiziert werden.');$raw=file_get_contents($file['tmp_name']);if($raw===false)throw new RuntimeException('Datei konnte nicht gelesen werden.');if(str_starts_with($raw,"\xEF\xBB\xBF"))$raw=substr($raw,3);$data=json_decode($raw,true,512,JSON_THROW_ON_ERROR);if(!is_array($data))throw new RuntimeException('JSON-Wurzel muss ein Objekt sein.');return[$data,$raw];
    }

    private static function report(array $package,string $raw,array $research,string $research_raw,array $rv,array $bv,array $validation,array $evidence,array $comparison):array{
        $base_pass=($validation['valid']&&$evidence['valid']&&$comparison['status']==='PASS_READ_ONLY_PREVIEW');$mode=(string)($package['mode']??'');$combined=$base_pass?($mode==='FINAL_APPROVED'?'PASS_FINAL_APPROVED':'READY_FOR_VISIBLE_SIGHT_REVIEW'):'BLOCKED';
        return ['report'=>['format'=>'affiliate-portal-category-workflow-final-report','format_version'=>'1.4','plugin_version'=>APKW_VERSION,'generated_at_utc'=>gmdate('c'),'combined_status'=>$combined,'content_write_capability'=>APKW_CONTENT_WRITE_CAPABILITY,'package_sha256'=>hash('sha256',$raw),'research_file_sha256'=>hash('sha256',$research_raw)],'research'=>['package_id'=>(string)($research['package_id']??''),'content_sha256'=>(string)($research['content_sha256']??''),'verification'=>$rv,'binding_verification'=>$bv],'package'=>['package_id'=>(string)($package['package_id']??''),'schema_version'=>(string)($package['schema_version']??''),'node_count'=>is_array($package['nodes']??null)?count($package['nodes']):0,'mode'=>(string)($package['mode']??''),'review_scope_sha256'=>APKW_Validator::review_scope_hash($package),'human_sight_review'=>$package['human_sight_review']??null],'validation'=>['valid'=>$validation['valid'],'errors'=>$validation['errors'],'warnings'=>$validation['warnings'],'automatic_rule_report'=>$validation['automatic_rule_report']],'research_evidence'=>$evidence,'preview'=>$comparison,'safety'=>['content_writes_performed'=>false,'posts_changed'=>false,'terms_changed'=>false,'menus_changed'=>false,'external_requests_during_final_preview'=>false,'configuration_or_transient_options_may_exist'=>true]];
    }
    private static function render_report(array $report):void{
        $encoded=wp_json_encode($report,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_HEX_TAG|JSON_HEX_AMP|JSON_HEX_APOS|JSON_HEX_QUOT);?><hr><h2>Prüfergebnis</h2><p><strong>Gesamtstatus:</strong> <?php echo esc_html($report['report']['combined_status']);?></p><?php if($report['report']['combined_status']==='READY_FOR_VISIBLE_SIGHT_REVIEW'):?><div class="notice notice-info inline"><p><strong>Nächster Pflichtschritt:</strong> Diesen exakten Strukturstand im Chat sichtbar als Gesamtbaum prüfen. Erst nach gemeinsamer Freigabe darf derselbe Review-Scope als <code>FINAL_APPROVED</code> bestätigt werden.</p><p><strong>Review-Scope SHA-256:</strong> <code><?php echo esc_html($report['package']['review_scope_sha256']);?></code></p></div><?php elseif($report['report']['combined_status']==='PASS_FINAL_APPROVED'):?><div class="notice notice-success inline"><p><strong>PASS:</strong> DataForSEO-/Workflow-Prüfung und dokumentierte sichtbare Freigabe beziehen sich auf denselben unveränderten Strukturstand.</p></div><?php endif;?><p><strong>Schemaprüfung:</strong> <?php echo $report['validation']['valid']?'PASS':'BLOCKED';?></p><p><strong>DataForSEO-Evidenz:</strong> <?php echo esc_html($report['research_evidence']['status']);?></p><p><strong>Live-Bestandsvorschau:</strong> <?php echo esc_html($report['preview']['status']);?></p>
        <?php if($report['validation']['errors']){echo'<h3>Schema-/Workflow-Fehler</h3>';self::issue_table($report['validation']['errors']);}if(!empty($report['research_evidence']['errors'])){echo'<h3>Blockierende DataForSEO-/Kannibalisierungsfehler</h3>';self::issue_table($report['research_evidence']['errors']);}if($report['validation']['warnings']){echo'<h3>Workflow-Hinweise</h3>';self::issue_table($report['validation']['warnings']);}if(!empty($report['research_evidence']['warnings'])){echo'<h3>DataForSEO-Hinweise</h3>';self::issue_table($report['research_evidence']['warnings']);}?>
        <h3>Live-Vorschau</h3><table class="widefat striped"><thead><tr><th>Aktion</th><th>Block</th><th>Name</th><th>Code</th><th>Hinweis</th></tr></thead><tbody><?php foreach($report['preview']['rows'] as $row):?><tr><td><?php echo esc_html($row['action']);?></td><td><?php echo esc_html($row['block']);?></td><td><?php echo esc_html($row['name']);?></td><td><?php echo esc_html($row['code']);?></td><td><?php echo esc_html($row['message']);?></td></tr><?php endforeach;?></tbody></table><p><button type="button" class="button" id="apkw-download-report">Prüfbericht als JSON herunterladen</button></p><script>(()=>{const report=<?php echo $encoded;?>;const b=document.getElementById('apkw-download-report');if(!b)return;b.addEventListener('click',()=>{const blob=new Blob([JSON.stringify(report,null,2)],{type:'application/json;charset=utf-8'});const u=URL.createObjectURL(blob);const a=document.createElement('a');a.href=u;a.download='kategorie-workflow-final-'+new Date().toISOString().replace(/[:.]/g,'-')+'.json';document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(u);});})();</script><?php
    }
    private static function issue_table(array $issues):void{echo'<table class="widefat striped"><thead><tr><th>Code</th><th>Pfad</th><th>Hinweis</th></tr></thead><tbody>';foreach($issues as $issue)echo'<tr><td>'.esc_html((string)($issue['code']??'')).'</td><td>'.esc_html((string)($issue['path']??'')).'</td><td>'.esc_html((string)($issue['message']??'')).'</td></tr>';echo'</tbody></table>';}
}
