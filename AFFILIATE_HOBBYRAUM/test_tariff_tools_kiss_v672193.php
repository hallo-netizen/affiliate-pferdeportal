<?php
if (!class_exists('Pferdeportal_Affiliate_Router')) { fwrite(STDERR,"FATAL plugin missing\n"); exit(2); }
$o=Pferdeportal_Affiliate_Router::instance();
$call=function($name,...$args)use($o){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m->invokeArgs($o,$args);};
function tt_assert($ok,$name,$detail=''){if(!$ok){fwrite(STDERR,"FAIL ".$name.($detail!==''?' '.$detail:'')."\n");exit(1);}echo "PASS ".$name.($detail!==''?' '.$detail:'')."\n";}

tt_assert(Pferdeportal_Affiliate_Router::VERSION==='6.72.193','version_672193');
tt_assert(method_exists($o,'render_tariff_tools_page'),'admin_tariff_page_exists');
tt_assert(shortcode_exists('affiliate_rechner'),'shortcode_registered');

global $wpdb;
$option='ppar_tariff_tools_v1';
delete_option($option);
$rp=new ReflectionProperty($o,'tariff_tools_request_cache');$rp->setAccessible(true);$rp->setValue($o,null);

$tables_before=(array)$wpdb->get_col('SHOW TABLES');

$credit_v1='<div class="tariff-credit-v1">Kreditrechner V1</div><script>window.pparCreditV1=true;</script>';
$insurance_v1='<iframe title="Pferdehaftpflicht" src="https://example.test/pferdehaftpflicht"></iframe>';
$now=time();
$tools=array(
    'kredit'=>array('id'=>'kredit','name'=>'Kredit','html'=>$credit_v1,'active'=>1,'created_at'=>$now,'updated_at'=>$now),
    'pferdehaftpflicht'=>array('id'=>'pferdehaftpflicht','name'=>'Pferdehaftpflicht','html'=>$insurance_v1,'active'=>1,'created_at'=>$now,'updated_at'=>$now),
);
$stored=$call('tariff_tools_store_all',$tools);
tt_assert(count($stored)===2,'two_tools_stored');

$autoload=(string)$wpdb->get_var($wpdb->prepare("SELECT autoload FROM {$wpdb->options} WHERE option_name=%s",$option));
tt_assert(!in_array(strtolower($autoload),array('yes','on','auto-on'),true),'single_option_not_autoloaded',$autoload);

$tables_after=(array)$wpdb->get_col('SHOW TABLES');
sort($tables_before);sort($tables_after);
tt_assert($tables_before===$tables_after,'no_new_table');

// Automatisch erzeugte, stabile individuelle Platzhalter.
tt_assert($call('tariff_tool_placeholder','kredit')==='[affiliate_rechner id="kredit"]','credit_placeholder_generated');
tt_assert($call('tariff_tool_placeholder','pferdehaftpflicht')==='[affiliate_rechner id="pferdehaftpflicht"]','insurance_placeholder_generated');
tt_assert($call('tariff_tool_unique_id','Kredit',$stored)==='kredit-2','duplicate_placeholder_id_is_unique');

// Saubere Writer-Liste: nur Name/ID/Platzhalter, niemals HTML-Code.
$registry=$o->tariff_tools_writer_registry(array());
tt_assert(isset($registry['kredit'],$registry['pferdehaftpflicht']),'writer_registry_contains_active_tools');
tt_assert(($registry['kredit']['placeholder']??'')==='[affiliate_rechner id="kredit"]','writer_registry_credit_placeholder');
tt_assert(!array_key_exists('html',$registry['kredit']),'writer_registry_exposes_no_html');

// Backend zeigt Platzhalter sichtbar an.
wp_set_current_user(1);
ob_start();$o->render_tariff_tools_page();$admin_html=ob_get_clean();
tt_assert(strpos($admin_html,'Platzhalter für den Schreiber')!==false,'backend_writer_list_visible');
tt_assert(strpos($admin_html,'[affiliate_rechner id=&quot;kredit&quot;]')!==false || strpos($admin_html,'[affiliate_rechner id="kredit"]')!==false,'backend_credit_placeholder_visible');
tt_assert(strpos($admin_html,'[affiliate_rechner id=&quot;pferdehaftpflicht&quot;]')!==false || strpos($admin_html,'[affiliate_rechner id="pferdehaftpflicht"]')!==false,'backend_insurance_placeholder_visible');

// Request-Performance: ohne Platzhalter KEIN Optionszugriff.
$rp->setValue($o,null);
$option_reads=0;
$filter=function($pre)use(&$option_reads){$option_reads++;return $pre;};
add_filter('pre_option_'.$option,$filter,10,1);
$plain=do_shortcode('<p>Normaler Artikel ohne Rechner.</p>');
tt_assert($option_reads===0,'ordinary_content_zero_tariff_option_reads','reads='.$option_reads);

// Mehrere Rechner in einem Request: zentrale Liste genau einmal laden.
$rendered=do_shortcode('[affiliate_rechner id="kredit"][affiliate_rechner id="pferdehaftpflicht"][affiliate_rechner id="kredit"]');
tt_assert($option_reads===1,'multiple_placeholders_one_option_load','reads='.$option_reads);
tt_assert(substr_count($rendered,'Kreditrechner V1')===2,'credit_rendered_twice_from_one_load');
tt_assert(strpos($rendered,'Pferdehaftpflicht')!==false,'insurance_rendered_same_request');
tt_assert(strpos($rendered,'<script>window.pparCreditV1=true;</script>')!==false,'trusted_widget_script_not_stripped');
remove_filter('pre_option_'.$option,$filter,10);

// Zentral ändern: gleicher Artikel/Platzhalter zeigt sofort neuen Code, ohne Artikeländerung.
$credit_v2='<div class="tariff-credit-v2">Kreditrechner V2</div><script>window.pparCreditV2=true;</script>';
$tools['kredit']['name']='Kredit Vergleich';
$tools['kredit']['html']=$credit_v2;
$tools['kredit']['updated_at']=time()+1;
$call('tariff_tools_store_all',$tools);
$after_update=do_shortcode('[affiliate_rechner id="kredit"]');
tt_assert(strpos($after_update,'Kreditrechner V2')!==false,'central_code_update_immediate');
tt_assert(strpos($after_update,'Kreditrechner V1')===false,'old_code_gone_after_central_update');
tt_assert($call('tariff_tool_placeholder','kredit')==='[affiliate_rechner id="kredit"]','placeholder_stable_after_rename');

// Zentral deaktivieren: Platzhalter bleibt im Artikel, Ausgabe wird leer.
$tools['kredit']['active']=0;
$call('tariff_tools_store_all',$tools);
tt_assert(do_shortcode('[affiliate_rechner id="kredit"]')==='','inactive_tool_renders_empty');
$registry2=$o->tariff_tools_writer_registry(array());
tt_assert(!isset($registry2['kredit']) && isset($registry2['pferdehaftpflicht']),'writer_registry_only_active_tools');

// Unbekannter Platzhalter: fail-closed.
tt_assert(do_shortcode('[affiliate_rechner id="nicht-vorhanden"]')==='','unknown_tool_renders_empty');

// Reaktivieren für finalen Zustand und beweisen: kein Nachlauf erforderlich.
$tools['kredit']['active']=1;
$call('tariff_tools_store_all',$tools);
$article='<p>Text davor.</p>[affiliate_rechner id="kredit"]<p>Text danach.</p>';
$out=do_shortcode($article);
tt_assert(strpos($out,'Kreditrechner V2')!==false,'article_placeholder_auto_filled_on_render');
tt_assert(strpos($out,'Text davor.')!==false && strpos($out,'Text danach.')!==false,'article_text_unchanged_around_tool');

echo "TARIFF_TOOLS_KISS_672193_COMPLETE\n";
