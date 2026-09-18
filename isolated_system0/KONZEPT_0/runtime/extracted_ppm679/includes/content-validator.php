<?php
if (!defined('ABSPATH')) { return; }

final class PPM679_Content_Validator {
    const VERSION='6.7.9';
    const MIN_WORDS=750;
    const MIN_PARAGRAPHS=16;
    const MIN_H2=4;
    const MIN_TABLE_BODY_ROWS=4;
    const MIN_FACT_PACK_COVERAGE_RATIO=0.75;
    const MIN_TRACE_LEXICAL_SUPPORT_RATIO=0.80;
    const MAX_DUPLICATE_SENTENCE_RATIO=0.02;
    const MAX_INTRO_PAIR_SIMILARITY=0.55;
    const VALIDATION_CONTRACT_V5='SECTION_REQUIREMENTS_V1';

    public static function check($generated,$item,$context,$server_state_hash='') {
        $type=(string)($item['article_type']??'');
        $html=(string)($generated['content_html']??'');
        $content_hash=hash('sha256',$html);
        $definition=PPM679_Article_Type_Validator::type_definition($type);
        $validation_contract=(string)($item['validation_contract_version']??'');
        $known_gate=PPM679_Known_Error_Gate::evaluate($generated,$item,$context,$server_state_hash);
        $structure_gate=PPM679_Content_Structure_Language_Gate::evaluate($generated,$item,$context,$server_state_hash);
        if ($validation_contract===self::VALIDATION_CONTRACT_V5) {
            $base=self::check_v5($generated,$item,$definition,$context,$server_state_hash,$content_hash);
            return PPM679_Fail_Closed_Aggregator::merge_content_validation_with_structure($base,$known_gate,$structure_gate,$context);
        }
        if ($validation_contract!=='') {
            $error=self::err('BLOCKED_VALIDATION_CONTRACT_VERSION_UNKNOWN','CONTENT_VALIDATOR_REQUIRES_EXPLICIT_SUPPORTED_VERSION','item.validation_contract_version',array('absent for legacy',self::VALIDATION_CONTRACT_V5),$validation_contract,'Ein unbekannter Validierungsvertrag darf nicht auf einen anderen Prüfpfad zurückfallen.',$context,$server_state_hash);
            $base=array(
                'ok'=>false,
                'technical_status'=>'BLOCKED_TECHNICAL_CHECK',
                'content_quality_status'=>'BLOCKED_CONTENT_QUALITY_CHECK',
                'content_hash'=>$content_hash,
                'errors'=>array($error),
                'technical_errors'=>array($error),
                'content_quality_errors'=>array(),
                'checks'=>array('content_hash'=>$content_hash,'validation_contract_version'=>$validation_contract)
            );
            return PPM679_Fail_Closed_Aggregator::merge_content_validation_with_structure($base,$known_gate,$structure_gate,$context);
        }

        $technical=self::technical_check($generated,$item,$definition,$context,$server_state_hash,$content_hash);
        $quality=self::quality_check($generated,$item,$definition,$context,$server_state_hash,$content_hash,true);
        $errors=array_merge($technical['errors'],$quality['errors']);
        $base=array(
            'ok'=>$technical['ok']&&$quality['ok'],
            'technical_status'=>$technical['ok']?'TECHNICAL_CHECK_OK':'BLOCKED_TECHNICAL_CHECK',
            'content_quality_status'=>$quality['ok']?'CONTENT_QUALITY_CHECK_OK':'BLOCKED_CONTENT_QUALITY_CHECK',
            'content_hash'=>$content_hash,
            'errors'=>$errors,
            'technical_errors'=>$technical['errors'],
            'content_quality_errors'=>$quality['errors'],
            'checks'=>array_merge($technical['checks'],$quality['checks'],array('content_hash'=>$content_hash))
        );
        return PPM679_Fail_Closed_Aggregator::merge_content_validation_with_structure($base,$known_gate,$structure_gate,$context);
    }

    public static function check_gold_reference($generated,$context='gold_reference_regression',$server_state_hash='',$item=array()) {
        $html=(string)($generated['content_html']??'');
        $content_hash=hash('sha256',$html);
        $quality=self::quality_check($generated,array(),array(),$context,$server_state_hash,$content_hash,false);
        $base=array(
            'ok'=>$quality['ok'],
            'technical_status'=>$quality['ok']?'TECHNICAL_CHECK_OK':'BLOCKED_TECHNICAL_CHECK',
            'content_quality_status'=>$quality['ok']?'CONTENT_QUALITY_CHECK_OK':'BLOCKED_CONTENT_QUALITY_CHECK',
            'content_hash'=>$content_hash,
            'errors'=>$quality['errors'],
            'technical_errors'=>array(),
            'content_quality_errors'=>$quality['errors'],
            'checks'=>array_merge($quality['checks'],array('content_hash'=>$content_hash))
        );
        $gold_item=is_array($item)?$item:array();
        if (!isset($gold_item['article_type'])) { $gold_item['article_type']=$generated['article_type']??'FAQ'; }
        $known_gate=PPM679_Known_Error_Gate::evaluate($generated,$gold_item,$context,$server_state_hash);
        $structure_gate=PPM679_Content_Structure_Language_Gate::evaluate($generated,$gold_item,$context,$server_state_hash);
        return PPM679_Fail_Closed_Aggregator::merge_content_validation_with_structure($base,$known_gate,$structure_gate,$context);
    }

    private static function technical_check($generated,$item,$definition,$context,$server_state_hash,$content_hash) {
        $errors=array();
        $type=(string)($item['article_type']??'');
        $title=(string)($generated['title']??'');
        $html=(string)($generated['content_html']??'');
        if (!is_array($definition)) {
            $errors[]=self::err('BLOCKED_CONTENT_TYPE_DEFINITION_MISSING','GENERATED_CONTENT_REQUIRES_ACTIVE_TYPE_DEFINITION','article_type',$type,null,'Für den erzeugten Inhalt fehlt die aktive Typdefinition.',$context,$server_state_hash);
            return array('ok'=>false,'errors'=>$errors,'checks'=>array('content_hash'=>$content_hash));
        }

        $declared_hash=(string)($generated['content_hash']??'');
        if ($declared_hash==='' || !hash_equals($content_hash,$declared_hash)) {
            $errors[]=self::err('BLOCKED_CONTENT_HASH_MISMATCH','VALIDATION_MUST_USE_EXACT_FINAL_CONTENT_HASH','content.content_hash',$content_hash,$declared_hash,'Der Validator prüft nicht exakt denselben finalen Inhalt, der als Kandidat gebunden wurde.',$context,$server_state_hash);
        }

        $table_count=preg_match_all('/<table\b[^>]*class=("|\')[^"\']*\bcomparison-table\b[^"\']*\1[^>]*>/iu',$html,$unused);
        if ((int)$table_count!==1) {
            $errors[]=self::err('BLOCKED_CONTENT_TABLE_COUNT','GENERATED_ARTICLE_MUST_CONTAIN_EXACTLY_ONE_CANONICAL_TABLE','content.table_count',1,(int)$table_count,'Der Entwurf enthält nicht genau eine kanonische Vergleichstabelle.',$context,$server_state_hash);
        }

        $link_count=preg_match_all('/<a\s+[^>]*href=/iu',$html,$unused);
        if ((int)$link_count!==3) {
            $errors[]=self::err('BLOCKED_CONTENT_VISIBLE_LINK_COUNT','GENERATED_ARTICLE_MUST_CONTAIN_EXACTLY_THREE_VISIBLE_LINKS','content.visible_link_count',3,(int)$link_count,'Der Entwurf enthält nicht genau drei sichtbare, rollenbezogene Links.',$context,$server_state_hash);
        }

        $required_blocks=isset($definition['required_blocks'])&&is_array($definition['required_blocks'])?$definition['required_blocks']:array();
        foreach ($required_blocks as $block) {
            if (!preg_match('/<[^>]+\bdata-block=("|\')'.preg_quote((string)$block,'/').'\1[^>]*>/iu',$html)) {
                $errors[]=self::err('BLOCKED_CONTENT_REQUIRED_BLOCK_MISSING','TYPE_REQUIRED_BLOCK_MUST_EXIST','content.blocks.'.(string)$block,'present',false,'Ein vom fertigen Beitragstyp vorgeschriebener Inhaltsblock fehlt.',$context,$server_state_hash);
            }
        }

        if ($type==='FAQ' && substr($title,-1)!=='?') {
            $errors[]=self::err('BLOCKED_CONTENT_FAQ_TITLE_QUESTION_MARK','FAQ_TITLE_MUST_END_WITH_QUESTION_MARK','content.title','question mark at end',$title,'Der FAQ-Titel erfüllt den freigegebenen Titelvertrag nicht.',$context,$server_state_hash);
        }
        if (((PPM679_Article_Type_Validator::type_definition($type)['title_contract']['colon_forbidden']??true)===true) && strpos($title,':')!==false) {
            $errors[]=self::err('BLOCKED_CONTENT_TITLE_COLON','ARTICLE_TITLE_MUST_NOT_CONTAIN_COLON','content.title','no colon',$title,'Der Titel enthält einen nach dem Typvertrag verbotenen Doppelpunkt.',$context,$server_state_hash);
        }
        $keyword=trim((string)($item['target_keyword']??''));
        if ($keyword!=='' && stripos($title,$keyword)===false) {
            $errors[]=self::err('BLOCKED_CONTENT_TARGET_KEYWORD_TITLE','TITLE_MUST_CONTAIN_TARGET_KEYWORD','content.title',$keyword,$title,'Das gebundene Zielkeyword fehlt im Titel.',$context,$server_state_hash);
        }

        if (preg_match('/\b(PASS|CERTIFIED|APPROVED|READY|RELEASED|PRODUCTION_READY)\b/i',$html,$match)) {
            $errors[]=self::err('BLOCKED_CONTENT_FORBIDDEN_MACHINE_STATUS_WORD','GENERATED_CONTENT_MUST_NOT_EMBED_MACHINE_RELEASE_STATUS','content.html','no forbidden machine status word',$match[0],'Der Entwurf enthält ein technisches Freigabewort, das nicht in Nutzerinhalt gehört.',$context,$server_state_hash);
        }

        return array(
            'ok'=>!$errors,
            'errors'=>$errors,
            'checks'=>array(
                'technical_content_hash'=>$content_hash,
                'table_count'=>(int)$table_count,
                'visible_link_count'=>(int)$link_count,
                'required_blocks'=>$required_blocks
            )
        );
    }

    private static function quality_check($generated,$item,$definition,$context,$server_state_hash,$content_hash,$require_runtime_contract) {
        $errors=array();
        $html=(string)($generated['content_html']??'');
        $type=(string)($item['article_type']??'');
        $plain=self::plain_text($html);
        $word_count=self::word_count($plain);
        $paragraph_count=(int)preg_match_all('/<p\b[^>]*>/iu',$html,$unused);
        $h2_count=(int)preg_match_all('/<h2\b[^>]*>/iu',$html,$unused);
        $table_body_rows=self::table_body_row_count($html);
        $trace_tags=self::source_trace_tags($html);

        if ($word_count<self::MIN_WORDS) {
            $errors[]=self::err('BLOCKED_CONTENT_WORD_FLOOR','COMPLETE_ARTICLE_MUST_HAVE_MINIMUM_750_WORDS','content.word_count','at least '.self::MIN_WORDS,$word_count,'Der vollständige sichtbare Artikel unterschreitet den verbindlichen Mindestumfang. Fundstelle: gesamter sichtbarer Artikeltext.',$context,$server_state_hash);
        }
        if ($paragraph_count<self::MIN_PARAGRAPHS) {
            $errors[]=self::err('BLOCKED_CONTENT_PARAGRAPH_FLOOR','COMPLETE_ARTICLE_MUST_HAVE_MINIMUM_16_PARAGRAPHS','content.paragraph_count','at least '.self::MIN_PARAGRAPHS,$paragraph_count,'Der Artikel enthält zu wenige eigenständige Absätze. Fundstelle: gesamtes finales HTML.',$context,$server_state_hash);
        }
        if ($h2_count<self::MIN_H2) {
            $errors[]=self::err('BLOCKED_CONTENT_H2_FLOOR','COMPLETE_ARTICLE_MUST_HAVE_MINIMUM_4_H2_HEADINGS','content.h2_count','at least '.self::MIN_H2,$h2_count,'Der Artikel besitzt zu wenige tragende Hauptabschnitte. Fundstelle: sämtliche H2-Überschriften.',$context,$server_state_hash);
        }
        if ($table_body_rows<self::MIN_TABLE_BODY_ROWS) {
            $errors[]=self::err('BLOCKED_CONTENT_TABLE_ROW_FLOOR','CANONICAL_TABLE_MUST_HAVE_MINIMUM_4_CONTENT_ROWS','content.table.body_row_count','at least '.self::MIN_TABLE_BODY_ROWS,$table_body_rows,'Die echte Tabelle enthält zu wenige Inhaltszeilen. Fundstelle: tbody der kanonischen Tabelle.',$context,$server_state_hash);
        }

        if ($require_runtime_contract && count($trace_tags)<3) {
            $errors[]=self::err('BLOCKED_CONTENT_SOURCE_TRACE_COUNT','ALL_FACTUAL_ARTICLE_TYPES_REQUIRE_SOURCE_TRACES','content.source_trace_count','at least 3',count($trace_tags),'Der erzeugte Entwurf enthält zu wenige gebundene Faktenspuren.',$context,$server_state_hash);
        }

        foreach ($trace_tags as $trace_index=>$trace) {
            $title=self::attribute($trace['tag'],'data-source-title');
            $hash=self::attribute($trace['tag'],'data-source-hash');
            $location='content.source_traces['.$trace_index.']@byte_'.$trace['offset'];
            if ($title==='' || $hash==='') {
                $errors[]=self::err('BLOCKED_CONTENT_SOURCE_TRACE_FIELDS','SOURCE_TRACE_REQUIRES_HASH_AND_TITLE',$location,array('data-source-title'=>'non-empty','data-source-hash'=>'valid SHA-256'),array('data-source-title'=>$title,'data-source-hash'=>$hash),'Die Faktenspur besitzt nicht alle erforderlichen Felder. Fundstelle: '.$trace['excerpt'],$context,$server_state_hash);
            }
            if ($title!=='' && self::blocked_placeholder_text($title)) {
                $errors[]=self::err('BLOCKED_CONTENT_PLACEHOLDER_SOURCE_TITLE','SOURCE_TITLE_MUST_NOT_BE_TEST_DUMMY_EXAMPLE_OR_PLACEHOLDER',$location.'.data-source-title','real source title',$title,'Die sichtbare Faktenspur verweist auf eine Test-, Dummy-, Beispiel- oder Platzhalterquelle. Fundstelle: '.$trace['excerpt'],$context,$server_state_hash);
            }
            if (!self::valid_non_repetitive_sha256($hash)) {
                $errors[]=self::err('BLOCKED_CONTENT_DUMMY_SOURCE_HASH','SOURCE_TRACE_HASH_MUST_BE_REAL_NON_REPETITIVE_SHA256',$location.'.data-source-hash','64 hexadecimal non-repetitive SHA-256',$hash,'Die Faktenspur enthält einen ungültigen oder erkennbar repetitiven Dummy-Hash. Fundstelle: '.$trace['excerpt'],$context,$server_state_hash);
            }
        }

        if ($require_runtime_contract && is_array($definition)) {
            $required_blocks=isset($definition['required_blocks'])&&is_array($definition['required_blocks'])?$definition['required_blocks']:array();
            foreach ($required_blocks as $block) {
                $body=self::block_body($html,(string)$block);
                if ($body!==null && trim(self::plain_text($body))==='') {
                    $errors[]=self::err('BLOCKED_CONTENT_REQUIRED_BLOCK_EMPTY','TYPE_REQUIRED_BLOCK_MUST_CONTAIN_VISIBLE_CONTENT','content.blocks.'.(string)$block,'non-empty visible content','empty','Ein vorhandener Pflichtbereich enthält keinen sichtbaren Inhalt. Fundstelle: data-block="'.(string)$block.'".',$context,$server_state_hash);
                }
            }
        }

        if ($require_runtime_contract && $type==='Vergleich') {
            foreach (self::comparison_source_assignment_errors($html) as $mismatch) {
                $errors[]=self::err('BLOCKED_CONTENT_SOURCE_LABEL_OPTION_MISMATCH','COMPARISON_SOURCE_LABEL_MUST_MATCH_NEAREST_OPTION_HEADING',$mismatch['field_path'],$mismatch['expected'],$mismatch['actual'],'Die Quellenbezeichnung ist einer anderen Vergleichsoption zugeordnet. Fundstelle: '.$mismatch['excerpt'],$context,$server_state_hash);
            }
        }

        $deterministic=array('errors'=>array(),'checks'=>array());
        if ($require_runtime_contract) {
            $deterministic=self::deterministic_contract_checks($generated,$item,$definition,$context,$server_state_hash,$content_hash);
            $errors=array_merge($errors,$deterministic['errors']);
        }

        return array(
            'ok'=>!$errors,
            'errors'=>$errors,
            'checks'=>array_merge(array(
                'quality_content_hash'=>$content_hash,
                'word_count'=>$word_count,
                'paragraph_count'=>$paragraph_count,
                'h2_count'=>$h2_count,
                'table_body_row_count'=>$table_body_rows,
                'source_trace_count'=>count($trace_tags)
            ),$deterministic['checks'])
        );
    }

    private static function deterministic_contract_checks($generated,$item,$definition,$context,$server_state_hash,$content_hash) {
        $errors=array();
        $checks=array();
        $html=(string)($generated['content_html']??'');
        $type=(string)($item['article_type']??'');
        $snapshot_id=(string)($item['source_snapshot_id']??'');
        $order=isset($item['runtime_order'])&&is_array($item['runtime_order'])?$item['runtime_order']:array();
        $pack=$snapshot_id!==''?PPM679_Storage::load_fact_pack($snapshot_id):null;
        $claims=is_array($pack)&&isset($pack['claims'])&&is_array($pack['claims'])?$pack['claims']:array();
        $claim_map=array();
        foreach ($claims as $claim) {
            $fact_id=trim((string)($claim['fact_id']??''));
            if ($fact_id!=='') { $claim_map[$fact_id]=$claim; }
        }

        $links=self::visible_links($html);
        $expected_links=isset($order['links'])&&is_array($order['links'])?$order['links']:array();
        $roles=array('parent_category','semantic_related','further_information');
        foreach ($roles as $index=>$role) {
            $actual=$links[$index]??array('href'=>'','anchor'=>'');
            $expected=$expected_links[$index]??array('href'=>'','anchor'=>'');
            $href=(string)($actual['href']??'');
            $is_internal=$href!=='' && substr($href,0,1)==='/' && substr($href,0,2)!=='//';
            if (!$is_internal || $href!==(string)($expected['href']??'') || (string)($actual['anchor']??'')!==(string)($expected['anchor']??'')) {
                $errors[]=self::err('BLOCKED_CONTENT_INTERNAL_LINK_ROLE','VISIBLE_INTERNAL_LINK_MUST_MATCH_BOUND_ROLE','content.links.'.$role,array('internal'=>true,'href'=>$expected['href']??'','anchor'=>$expected['anchor']??''),$actual,'Der sichtbare interne Link erfüllt seine gebundene Rolle nicht.',$context,$server_state_hash);
            }
        }

        $units=self::factual_units($html);
        $used_fact_ids=array();
        $supported_trace_units=0;
        $trace_units=0;
        foreach ($units as $index=>$unit) {
            $field='content.factual_units['.$index.']@byte_'.$unit['offset'];
            $refs=$unit['fact_ids'];
            if (!$refs) {
                $errors[]=self::err('BLOCKED_CONTENT_FACT_REFS_MISSING','EVERY_FACTUAL_VISIBLE_UNIT_REQUIRES_FACT_REFERENCES',$field.'.data-fact-ids','one or more bound fact ids','missing','Eine sichtbare inhaltliche Einheit besitzt keine Faktreferenz. Fundstelle: '.$unit['excerpt'],$context,$server_state_hash);
                continue;
            }
            $reference_text='';
            foreach ($refs as $fact_id) {
                $used_fact_ids[$fact_id]=true;
                if (!isset($claim_map[$fact_id])) {
                    $errors[]=self::err('BLOCKED_CONTENT_FACT_REF_UNKNOWN','FACT_REFERENCE_MUST_EXIST_IN_BOUND_FACT_PACK',$field.'.data-fact-ids','known fact id',$fact_id,'Eine sichtbare Faktreferenz existiert nicht im gebundenen Fact-Pack.',$context,$server_state_hash);
                    continue;
                }
                $claim=$claim_map[$fact_id];
                if ((string)($claim['claim_status']??'')!=='FULLY_SUPPORTED') {
                    $errors[]=self::err('BLOCKED_CONTENT_FACT_REF_NOT_VERIFIED','REFERENCED_FACT_MUST_BE_FULLY_SUPPORTED',$field.'.'.$fact_id.'.claim_status','FULLY_SUPPORTED',$claim['claim_status']??null,'Eine verwendete Faktreferenz ist nicht vollständig verifiziert.',$context,$server_state_hash);
                }
                $article_types=isset($claim['article_types'])&&is_array($claim['article_types'])?$claim['article_types']:array();
                if (!in_array($type,$article_types,true)) {
                    $errors[]=self::err('BLOCKED_CONTENT_FACT_REF_TYPE_MISMATCH','REFERENCED_FACT_MUST_APPLY_TO_ARTICLE_TYPE',$field.'.'.$fact_id.'.article_types',$type,$article_types,'Eine verwendete Faktreferenz ist für diesen Beitragstyp nicht freigegeben.',$context,$server_state_hash);
                }
                $reference_text.=' '.self::claim_reference_text($claim);
            }
            $numeric_tokens=preg_match('/^\s*\d+(?:[.,]\d+)?\s*$/u',$unit['text'])?array():self::numeric_tokens($unit['text']);
            foreach ($numeric_tokens as $number) {
                if (!self::normalized_contains($reference_text,$number)) {
                    $errors[]=self::err('BLOCKED_CONTENT_NUMERIC_CLAIM_UNSUPPORTED','VISIBLE_NUMERIC_CLAIM_MUST_EXIST_IN_REFERENCED_FACTS',$field.'.numeric_claim',$number,$unit['text'],'Eine sichtbare Zahlenangabe ist in den referenzierten Fakten nicht belegt.',$context,$server_state_hash);
                }
            }
            if ($unit['has_trace']) {
                $trace_units++;
                if (self::lexically_supported($unit['text'],$reference_text)) { $supported_trace_units++; }
            }
        }

        foreach (self::source_trace_tags($html) as $trace_index=>$trace) {
            $fact_id=self::attribute($trace['tag'],'data-fact-id');
            if ($fact_id==='' || !isset($claim_map[$fact_id])) {
                $errors[]=self::err('BLOCKED_CONTENT_TRACE_FACT_BINDING','SOURCE_TRACE_MUST_REFERENCE_BOUND_FACT','content.source_traces['.$trace_index.'].data-fact-id','known fact id',$fact_id,'Eine Faktenspur ist nicht an einen vorhandenen Fact-Pack-Fakt gebunden.',$context,$server_state_hash);
                continue;
            }
            $claim=$claim_map[$fact_id];
            $expected_title=(string)($claim['source_id']??'');
            $expected_hash=strtolower(trim((string)($claim['evidence_text_sha256']??'')));
            $actual_title=self::attribute($trace['tag'],'data-source-title');
            $actual_hash=strtolower(self::attribute($trace['tag'],'data-source-hash'));
            if ($actual_title!==$expected_title || $actual_hash!==$expected_hash) {
                $errors[]=self::err('BLOCKED_CONTENT_TRACE_CLAIM_MISMATCH','SOURCE_TRACE_FIELDS_MUST_MATCH_REFERENCED_FACT','content.source_traces['.$trace_index.']',array('source_title'=>$expected_title,'source_hash'=>$expected_hash),array('source_title'=>$actual_title,'source_hash'=>$actual_hash),'Eine Faktenspur stimmt nicht mit dem referenzierten Fact-Pack-Fakt überein.',$context,$server_state_hash);
            }
        }

        $coverage=count($claim_map)>0?count(array_intersect(array_keys($used_fact_ids),array_keys($claim_map)))/count($claim_map):0.0;
        if ($coverage<self::MIN_FACT_PACK_COVERAGE_RATIO) {
            $errors[]=self::err('BLOCKED_CONTENT_FACT_PACK_COVERAGE','ARTICLE_MUST_USE_AT_LEAST_75_PERCENT_OF_BOUND_FACT_PACK','content.fact_pack_coverage_ratio','at least '.self::MIN_FACT_PACK_COVERAGE_RATIO,$coverage,'Der sichtbare Artikel nutzt zu wenig des gebundenen Fact-Packs.',$context,$server_state_hash);
        }
        $lexical_ratio=$trace_units>0?$supported_trace_units/$trace_units:0.0;
        if ($lexical_ratio<self::MIN_TRACE_LEXICAL_SUPPORT_RATIO) {
            $errors[]=self::err('BLOCKED_CONTENT_TRACE_LEXICAL_SUPPORT','AT_LEAST_80_PERCENT_OF_TRACE_UNITS_REQUIRE_LEXICAL_FACT_SUPPORT','content.trace_lexical_support_ratio','at least '.self::MIN_TRACE_LEXICAL_SUPPORT_RATIO,$lexical_ratio,'Zu wenige Faktenspuren besitzen eine erkennbare lexikalische Verbindung zu ihrer sichtbaren Aussage.',$context,$server_state_hash);
        }

        $duplicate_ratio=self::duplicate_sentence_ratio($html);
        if ($duplicate_ratio>self::MAX_DUPLICATE_SENTENCE_RATIO) {
            $errors[]=self::err('BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO','DUPLICATE_SENTENCE_RATIO_MUST_NOT_EXCEED_2_PERCENT','content.duplicate_sentence_ratio','at most '.self::MAX_DUPLICATE_SENTENCE_RATIO,$duplicate_ratio,'Der sichtbare Artikel wiederholt zu viele vollständige Sätze.',$context,$server_state_hash);
        }
        $intro_similarity=self::maximum_intro_pair_similarity($html);
        if ($intro_similarity>self::MAX_INTRO_PAIR_SIMILARITY) {
            $errors[]=self::err('BLOCKED_CONTENT_INTRO_PAIR_SIMILARITY','INTRO_PARAGRAPH_PAIR_SIMILARITY_MUST_NOT_EXCEED_55_PERCENT','content.intro_pair_similarity','at most '.self::MAX_INTRO_PAIR_SIMILARITY,$intro_similarity,'Einleitungstexte sind untereinander zu ähnlich und wirken schablonenhaft.',$context,$server_state_hash);
        }

        $checks=array(
            'internal_link_roles'=>array('parent_category','semantic_related'),
            'factual_unit_count'=>count($units),
            'used_fact_count'=>count(array_intersect(array_keys($used_fact_ids),array_keys($claim_map))),
            'fact_pack_claim_count'=>count($claim_map),
            'fact_pack_coverage_ratio'=>$coverage,
            'trace_units'=>$trace_units,
            'trace_lexical_support_ratio'=>$lexical_ratio,
            'duplicate_sentence_ratio'=>$duplicate_ratio,
            'intro_pair_similarity'=>$intro_similarity
        );
        return array('errors'=>$errors,'checks'=>$checks);
    }


    private static function check_v5($generated,$item,$definition,$context,$server_state_hash,$content_hash) {
        $technical=self::technical_check_v5($generated,$item,$definition,$context,$server_state_hash,$content_hash);
        $quality=self::quality_check_v5($generated,$item,$definition,$context,$server_state_hash,$content_hash);
        return array(
            'ok'=>$technical['ok']&&$quality['ok'],
            'technical_status'=>$technical['ok']?'TECHNICAL_CHECK_OK':'BLOCKED_TECHNICAL_CHECK',
            'content_quality_status'=>$quality['ok']?'CONTENT_QUALITY_CHECK_OK':'BLOCKED_CONTENT_QUALITY_CHECK',
            'content_hash'=>$content_hash,
            'errors'=>array_merge($technical['errors'],$quality['errors']),
            'technical_errors'=>$technical['errors'],
            'content_quality_errors'=>$quality['errors'],
            'checks'=>array_merge($technical['checks'],$quality['checks'],array('content_hash'=>$content_hash,'validation_contract_version'=>self::VALIDATION_CONTRACT_V5))
        );
    }

    private static function technical_check_v5($generated,$item,$definition,$context,$server_state_hash,$content_hash) {
        $errors=array();
        $type=(string)($item['article_type']??'');
        $title=(string)($generated['title']??'');
        $html=(string)($generated['content_html']??'');
        if (!is_array($definition)) {
            $errors[]=self::err('BLOCKED_CONTENT_TYPE_DEFINITION_MISSING','GENERATED_CONTENT_REQUIRES_ACTIVE_TYPE_DEFINITION','article_type',$type,null,'Für den erzeugten Inhalt fehlt die aktive Typdefinition.',$context,$server_state_hash);
            return array('ok'=>false,'errors'=>$errors,'checks'=>array('content_hash'=>$content_hash));
        }
        $declared_hash=(string)($generated['content_hash']??'');
        if ($declared_hash==='' || !hash_equals($content_hash,$declared_hash)) {
            $errors[]=self::err('BLOCKED_CONTENT_HASH_MISMATCH','VALIDATION_MUST_USE_EXACT_FINAL_CONTENT_HASH','content.content_hash',$content_hash,$declared_hash,'Der Validator prüft nicht exakt denselben finalen Inhalt, der als Kandidat gebunden wurde.',$context,$server_state_hash);
        }
        $requirements=isset($item['section_requirements'])&&is_array($item['section_requirements'])?$item['section_requirements']:null;
        $declared_requirements_hash=strtolower(trim((string)($item['section_requirements_hash']??'')));
        $article=isset($item['canonical_article'])&&is_array($item['canonical_article'])?$item['canonical_article']:array();
        if (!is_array($requirements) || (string)($requirements['contract']??'')!==self::VALIDATION_CONTRACT_V5 || !isset($requirements['sections']) || !is_array($requirements['sections']) || !$requirements['sections']) {
            $errors[]=self::err('BLOCKED_VALIDATION_CONTRACT_VERSION_MISSING','V5_CONTENT_REQUIRES_COMPLETE_SECTION_REQUIREMENTS','item.section_requirements','complete SECTION_REQUIREMENTS_V1 object',$requirements,'Die bestätigten Abschnittsanforderungen fehlen oder sind unvollständig.',$context,$server_state_hash);
        } else {
            $actual_requirements_hash=PPM679_Diagnostic::stable_hash($requirements);
            if (!self::valid_non_repetitive_sha256($declared_requirements_hash) || !hash_equals($actual_requirements_hash,$declared_requirements_hash)) {
                $errors[]=self::err('BLOCKED_SECTION_REQUIREMENTS_HASH_MISMATCH','SECTION_REQUIREMENTS_HASH_MUST_MATCH_CANONICAL_JSON','item.section_requirements_hash',$actual_requirements_hash,$declared_requirements_hash,'Die Abschnittsanforderungen stimmen nicht mit ihrem kanonischen Hash überein.',$context,$server_state_hash);
            }
            if ((string)($article['validation_contract_version']??'')!==self::VALIDATION_CONTRACT_V5 || !hash_equals($declared_requirements_hash,strtolower(trim((string)($article['section_requirements_hash']??''))))) {
                $errors[]=self::err('BLOCKED_VALIDATION_CONTRACT_VERSION_UNKNOWN','CANONICAL_ARTICLE_MUST_MATCH_V5_VALIDATION_BINDING','item.canonical_article.validation_contract_version',self::VALIDATION_CONTRACT_V5,$article['validation_contract_version']??null,'Der kanonische Artikel und der Planeintrag sind nicht an denselben neuen Prüfvertrag gebunden.',$context,$server_state_hash);
            }
        }
        if ($type==='FAQ' && substr($title,-1)!=='?') {
            $errors[]=self::err('BLOCKED_CONTENT_FAQ_TITLE_QUESTION_MARK','FAQ_TITLE_MUST_END_WITH_QUESTION_MARK','content.title','question mark at end',$title,'Der FAQ-Titel erfüllt den freigegebenen Titelvertrag nicht.',$context,$server_state_hash);
        }
        if (((PPM679_Article_Type_Validator::type_definition($type)['title_contract']['colon_forbidden']??true)===true) && strpos($title,':')!==false) {
            $errors[]=self::err('BLOCKED_CONTENT_TITLE_COLON','ARTICLE_TITLE_MUST_NOT_CONTAIN_COLON','content.title','no colon',$title,'Der Titel enthält einen nach dem Typvertrag verbotenen Doppelpunkt.',$context,$server_state_hash);
        }
        $keyword=trim((string)($item['target_keyword']??''));
        if ($keyword!=='' && stripos($title,$keyword)===false) {
            $errors[]=self::err('BLOCKED_CONTENT_TARGET_KEYWORD_TITLE','TITLE_MUST_CONTAIN_TARGET_KEYWORD','content.title',$keyword,$title,'Das gebundene Zielkeyword fehlt im Titel.',$context,$server_state_hash);
        }
        if (preg_match('/\b(PASS|CERTIFIED|APPROVED|READY|RELEASED|PRODUCTION_READY)\b/i',$html,$match)) {
            $errors[]=self::err('BLOCKED_CONTENT_FORBIDDEN_MACHINE_STATUS_WORD','GENERATED_CONTENT_MUST_NOT_EMBED_MACHINE_RELEASE_STATUS','content.html','no forbidden machine status word',$match[0],'Der Entwurf enthält ein technisches Freigabewort, das nicht in Nutzerinhalt gehört.',$context,$server_state_hash);
        }
        return array('ok'=>!$errors,'errors'=>$errors,'checks'=>array('technical_content_hash'=>$content_hash,'section_requirements_hash'=>$declared_requirements_hash));
    }

    private static function quality_check_v5($generated,$item,$definition,$context,$server_state_hash,$content_hash) {
        $errors=array();
        $checks=array();
        $html=(string)($generated['content_html']??'');
        $type=(string)($item['article_type']??'');
        $requirements=isset($item['section_requirements'])&&is_array($item['section_requirements'])?$item['section_requirements']:array();
        $blueprints=isset($requirements['sections'])&&is_array($requirements['sections'])?$requirements['sections']:array();
        usort($blueprints,function($a,$b){ return ((int)($a['order']??0))<=>((int)($b['order']??0)); });
        $sections=self::v5_sections($html);
        $actual_ids=array();
        $duplicates=array();
        foreach ($sections as $section) {
            $id=$section['section_id'];
            if (in_array($id,$actual_ids,true)) { $duplicates[$id]=true; }
            $actual_ids[]=$id;
        }
        foreach (array_keys($duplicates) as $id) {
            $errors[]=self::err('BLOCKED_CONTENT_SECTION_DUPLICATE','V5_SECTION_ID_MUST_BE_UNIQUE','content.sections.'.$id,'exactly once','duplicate','Ein Abschnittsbezeichner kommt mehrfach vor.',$context,$server_state_hash);
        }
        $expected_ids=array();
        foreach ($blueprints as $blueprint) { $expected_ids[]=(string)($blueprint['section_id']??''); }
        foreach ($expected_ids as $id) {
            if ($id==='' || !in_array($id,$actual_ids,true)) {
                $errors[]=self::err('BLOCKED_CONTENT_REQUIRED_SECTION_MISSING','EVERY_BOUND_V5_SECTION_MUST_EXIST','content.sections.'.$id,'present exactly once',false,'Ein gebundener Pflichtabschnitt fehlt.',$context,$server_state_hash);
            }
        }
        if ($expected_ids!==$actual_ids) {
            $errors[]=self::err('BLOCKED_CONTENT_SECTION_ORDER','V5_SECTIONS_MUST_EXACTLY_MATCH_BOUND_ORDER','content.section_order',$expected_ids,$actual_ids,'Abschnitte fehlen, sind unerwartet oder stehen nicht in der gebundenen Reihenfolge.',$context,$server_state_hash);
        }

        $section_map=array();
        foreach ($sections as $section) { if (!isset($section_map[$section['section_id']])) { $section_map[$section['section_id']]=$section; } }
        $required_fact_ids=array();
        $link_permitted_sections=array();
        foreach ($blueprints as $blueprint) {
            $id=(string)($blueprint['section_id']??'');
            foreach (isset($blueprint['required_concepts'])&&is_array($blueprint['required_concepts'])?$blueprint['required_concepts']:array() as $concept) {
                foreach (isset($concept['source_refs'])&&is_array($concept['source_refs'])?$concept['source_refs']:array() as $ref) {
                    $fact_id=trim((string)($ref['source_id']??''));
                    if ($fact_id!=='') { $required_fact_ids[$fact_id]=true; }
                }
            }
            $obligations=isset($blueprint['content_obligations'])&&is_array($blueprint['content_obligations'])?$blueprint['content_obligations']:array();
            if (!empty($obligations['link_roles']) && is_array($obligations['link_roles'])) { $link_permitted_sections[$id]=true; }
            if (!isset($section_map[$id])) { continue; }
            $body=$section_map[$id]['body'];
            if (!empty($obligations['heading_required'])) {
                $h2_count=(int)preg_match_all('/<h2\b[^>]*>(.*?)<\/h2>/isu',$body,$h2_matches);
                $heading_text=$h2_count===1?self::plain_text($h2_matches[1][0]):'';
                if ($h2_count!==1 || $heading_text==='') {
                    $errors[]=self::err('BLOCKED_CONTENT_REQUIRED_SECTION_MISSING','V5_REQUIRED_SECTION_REQUIRES_EXACTLY_ONE_NONEMPTY_H2','content.sections.'.$id.'.h2',1,$h2_count,'Ein Pflichtabschnitt besitzt nicht genau eine nichtleere H2-Überschrift.',$context,$server_state_hash);
                }
            }
            if (!empty($obligations['paragraph_required'])) {
                $paragraph_count=(int)preg_match_all('/<p\b[^>]*>.*?<\/p>/isu',$body,$paragraph_matches);
                $nonempty=0;
                foreach ($paragraph_matches[0]??array() as $paragraph) { if (self::plain_text($paragraph)!=='') { $nonempty++; } }
                if ($nonempty<1) {
                    $errors[]=self::err('BLOCKED_CONTENT_REQUIRED_SECTION_MISSING','V5_REQUIRED_SECTION_REQUIRES_NONEMPTY_PARAGRAPH','content.sections.'.$id.'.paragraphs','at least 1',0,'Ein Pflichtabschnitt enthält keinen nichtleeren Absatz.',$context,$server_state_hash);
                }
            }
            if (!empty($obligations['list_roles']) && is_array($obligations['list_roles'])) {
                $list_items=(int)preg_match_all('/<li\b[^>]*>.*?<\/li>/isu',$body,$unused);
                if ($list_items<1) {
                    $errors[]=self::err('BLOCKED_CONTENT_REQUIRED_SECTION_MISSING','V5_SECTION_WITH_LIST_ROLE_REQUIRES_LIST_ITEM','content.sections.'.$id.'.list_items','at least 1',$list_items,'Ein Abschnitt mit gebundener Listenrolle enthält keinen Listenpunkt.',$context,$server_state_hash);
                }
            }
            $table_policy=(string)($obligations['table_policy']??'');
            $tables=(int)preg_match_all('/<table\b[^>]*>(.*?)<\/table>/isu',$body,$table_matches);
            if ($table_policy==='REQUIRED' && $tables!==1) {
                $errors[]=self::err('BLOCKED_CONTENT_REQUIRED_TABLE_MISSING','V5_REQUIRED_TABLE_SECTION_MUST_CONTAIN_EXACTLY_ONE_TABLE','content.sections.'.$id.'.tables',1,$tables,'Der gebundene Tabellenabschnitt enthält nicht genau eine Tabelle.',$context,$server_state_hash);
            } elseif ($table_policy==='FORBIDDEN' && $tables!==0) {
                $errors[]=self::err('BLOCKED_CONTENT_FORBIDDEN_TABLE_PRESENT','V5_FORBIDDEN_TABLE_SECTION_MUST_CONTAIN_NO_TABLE','content.sections.'.$id.'.tables',0,$tables,'Ein Abschnitt enthält entgegen dem Vertrag eine Tabelle.',$context,$server_state_hash);
            } elseif ($table_policy!=='REQUIRED' && $table_policy!=='FORBIDDEN') {
                $errors[]=self::err('BLOCKED_CONTENT_TABLE_STRUCTURE','V5_TABLE_POLICY_MUST_BE_EXPLICIT','content.sections.'.$id.'.table_policy',array('REQUIRED','FORBIDDEN'),$table_policy,'Die Tabellenregel ist unbekannt und darf nicht erraten werden.',$context,$server_state_hash);
            }
            if ($table_policy==='REQUIRED' && $tables===1) {
                $table_html=$table_matches[0][0];
                $has_thead=(bool)preg_match('/<thead\b[^>]*>.*?<\/thead>/isu',$table_html);
                $has_tbody=(bool)preg_match('/<tbody\b[^>]*>(.*?)<\/tbody>/isu',$table_html,$tbody_match);
                $row_count=$has_tbody?(int)preg_match_all('/<tr\b[^>]*>.*?<\/tr>/isu',$tbody_match[1],$row_matches):0;
                $column_count=0;
                if ($has_tbody && !empty($row_matches[0])) { $column_count=(int)preg_match_all('/<(?:th|td)\b[^>]*>.*?<\/(?:th|td)>/isu',$row_matches[0][0],$unused); }
                if (!$has_thead || !$has_tbody || $row_count<2 || $column_count<2) {
                    $errors[]=self::err('BLOCKED_CONTENT_TABLE_STRUCTURE','V5_TABLE_REQUIRES_THEAD_TBODY_TWO_ROWS_TWO_COLUMNS','content.sections.'.$id.'.table',array('thead'=>true,'tbody'=>true,'body_rows'=>'>=2','columns'=>'>=2'),array('thead'=>$has_thead,'tbody'=>$has_tbody,'body_rows'=>$row_count,'columns'=>$column_count),'Die semantische Tabellenstruktur ist unvollständig.',$context,$server_state_hash);
                }
            }
            $section_units=self::v5_factual_units($body);
            $fact_bound=false;
            foreach ($section_units as $unit) { if ($unit['fact_ids']) { $fact_bound=true; break; } }
            if (!$fact_bound) {
                $errors[]=self::err('BLOCKED_CONTENT_FACT_REFS_MISSING','EVERY_V5_SECTION_REQUIRES_FACT_BOUND_VISIBLE_UNIT','content.sections.'.$id.'.factual_units','at least one fact-bound unit',0,'Ein Pflichtabschnitt enthält keine faktgebundene sichtbare Einheit.',$context,$server_state_hash);
            }
        }

        $snapshot_id=(string)($item['source_snapshot_id']??'');
        $pack=$snapshot_id!==''?PPM679_Storage::load_fact_pack($snapshot_id):null;
        $claims=is_array($pack)&&isset($pack['claims'])&&is_array($pack['claims'])?$pack['claims']:array();
        $claim_map=array();
        foreach ($claims as $claim) { $fact_id=trim((string)($claim['fact_id']??'')); if ($fact_id!=='') { $claim_map[$fact_id]=$claim; } }
        $order=isset($item['runtime_order'])&&is_array($item['runtime_order'])?$item['runtime_order']:array();
        $allowed=array_flip(array_map('strval',isset($order['allowed_fact_ids'])&&is_array($order['allowed_fact_ids'])?$order['allowed_fact_ids']:array()));
        $units=self::v5_factual_units($html);
        $used_fact_ids=array();
        foreach ($units as $index=>$unit) {
            $field='content.factual_units['.$index.']@byte_'.$unit['offset'];
            if (!$unit['fact_ids']) {
                $errors[]=self::err('BLOCKED_CONTENT_FACT_REFS_MISSING','EVERY_V5_FACTUAL_VISIBLE_UNIT_REQUIRES_FACT_REFERENCES',$field.'.data-fact-ids','one or more bound fact ids','missing','Eine sichtbare inhaltliche Einheit besitzt keine Faktreferenz. Fundstelle: '.$unit['excerpt'],$context,$server_state_hash);
                continue;
            }
            $reference_text='';
            foreach ($unit['fact_ids'] as $fact_id) {
                $used_fact_ids[$fact_id]=true;
                if (!isset($allowed[$fact_id])) {
                    $errors[]=self::err('BLOCKED_CONTENT_FACT_REF_UNKNOWN','V5_FACT_REFERENCE_MUST_BE_ALLOWED_BY_RUNTIME_ORDER',$field.'.data-fact-ids','allowed fact id',$fact_id,'Eine Faktreferenz liegt außerhalb der erlaubten Obergrenze des Auftrags.',$context,$server_state_hash);
                }
                if (!isset($claim_map[$fact_id])) {
                    $errors[]=self::err('BLOCKED_CONTENT_FACT_REF_UNKNOWN','FACT_REFERENCE_MUST_EXIST_IN_BOUND_FACT_PACK',$field.'.data-fact-ids','known fact id',$fact_id,'Eine sichtbare Faktreferenz existiert nicht im gebundenen Fact-Pack.',$context,$server_state_hash);
                    continue;
                }
                $claim=$claim_map[$fact_id];
                if ((string)($claim['claim_status']??'')!=='FULLY_SUPPORTED') {
                    $errors[]=self::err('BLOCKED_CONTENT_FACT_REF_NOT_VERIFIED','REFERENCED_FACT_MUST_BE_FULLY_SUPPORTED',$field.'.'.$fact_id.'.claim_status','FULLY_SUPPORTED',$claim['claim_status']??null,'Eine verwendete Faktreferenz ist nicht vollständig verifiziert.',$context,$server_state_hash);
                }
                $article_types=isset($claim['article_types'])&&is_array($claim['article_types'])?$claim['article_types']:array();
                if (!in_array($type,$article_types,true)) {
                    $errors[]=self::err('BLOCKED_CONTENT_FACT_REF_TYPE_MISMATCH','REFERENCED_FACT_MUST_APPLY_TO_ARTICLE_TYPE',$field.'.'.$fact_id.'.article_types',$type,$article_types,'Eine verwendete Faktreferenz ist für diesen Beitragstyp nicht freigegeben.',$context,$server_state_hash);
                }
                $reference_text.=' '.self::claim_reference_text($claim);
            }
            $numeric_tokens=preg_match('/^\s*\d+(?:[.,]\d+)?\s*$/u',$unit['text'])?array():self::numeric_tokens($unit['text']);
            foreach ($numeric_tokens as $number) {
                if (!self::normalized_contains($reference_text,$number)) {
                    $errors[]=self::err('BLOCKED_CONTENT_NUMERIC_CLAIM_UNSUPPORTED','VISIBLE_NUMERIC_CLAIM_MUST_EXIST_IN_REFERENCED_FACTS',$field.'.numeric_claim',$number,$unit['text'],'Eine sichtbare Zahlenangabe ist in den referenzierten Fakten nicht belegt.',$context,$server_state_hash);
                }
            }
        }
        $missing_required=array_values(array_diff(array_keys($required_fact_ids),array_keys($used_fact_ids)));
        if ($missing_required) {
            $errors[]=self::err('BLOCKED_CONTENT_FACT_PACK_COVERAGE','V5_REQUIRED_FACT_COVERAGE_MUST_BE_100_PERCENT','content.required_fact_coverage','all required fact ids',array('missing'=>$missing_required),'Nicht alle durch die Abschnittsanforderungen ausgewählten Fakten werden sichtbar verwendet.',$context,$server_state_hash);
        }

        $expected_links=isset($order['links'])&&is_array($order['links'])?$order['links']:array();
        $expected_pairs=array();
        foreach ($expected_links as $link) { $expected_pairs[(string)($link['href']??'')."\n".(string)($link['anchor']??'')]=true; }
        $found_permitted=array();
        foreach ($sections as $section) {
            foreach (self::visible_links($section['body']) as $link) {
                $href=(string)($link['href']??'');
                $anchor=(string)($link['anchor']??'');
                if ($href==='' || substr($href,0,1)!=='/' || substr($href,0,2)==='//') { continue; }
                $pair=$href."\n".$anchor;
                if (!isset($expected_pairs[$pair])) {
                    $errors[]=self::err('BLOCKED_CONTENT_UNBOUND_INTERNAL_LINK','EVERY_VISIBLE_INTERNAL_LINK_MUST_MATCH_BOUND_PAIR','content.links',array_keys($expected_pairs),$link,'Ein sichtbarer interner Link ist nicht exakt im Auftrag gebunden.',$context,$server_state_hash);
                } elseif (isset($link_permitted_sections[$section['section_id']])) {
                    $found_permitted[$pair]=true;
                }
            }
        }
        foreach (array_keys($expected_pairs) as $pair) {
            if (!isset($found_permitted[$pair])) {
                list($href,$anchor)=explode("\n",$pair,2);
                $errors[]=self::err('BLOCKED_CONTENT_BOUND_LINK_MISSING','EVERY_BOUND_LINK_PAIR_MUST_OCCUR_IN_PERMITTED_SECTION','content.links',array('href'=>$href,'anchor'=>$anchor),'missing','Ein gebundenes Linkpaar fehlt in einem dafür zugelassenen Abschnitt.',$context,$server_state_hash);
            }
        }

        $duplicate_ratio=self::duplicate_sentence_ratio_v5($html);
        if ($duplicate_ratio>self::MAX_DUPLICATE_SENTENCE_RATIO) {
            $errors[]=self::err('BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO','DUPLICATE_SENTENCE_RATIO_MUST_NOT_EXCEED_2_PERCENT','content.duplicate_sentence_ratio','at most '.self::MAX_DUPLICATE_SENTENCE_RATIO,$duplicate_ratio,'Der sichtbare Artikel wiederholt zu viele vollständige Sätze.',$context,$server_state_hash);
        }
        $first_section_similarity=!empty($sections)?self::maximum_section_pair_similarity($sections[0]['body']):0.0;
        if ($first_section_similarity>self::MAX_INTRO_PAIR_SIMILARITY) {
            $errors[]=self::err('BLOCKED_CONTENT_INTRO_PAIR_SIMILARITY','FIRST_SECTION_PARAGRAPH_PAIR_SIMILARITY_MUST_NOT_EXCEED_55_PERCENT','content.first_section_pair_similarity','at most '.self::MAX_INTRO_PAIR_SIMILARITY,$first_section_similarity,'Absätze des ersten Abschnitts sind untereinander zu ähnlich.',$context,$server_state_hash);
        }
        $plain=self::plain_text($html);
        $checks=array(
            'quality_content_hash'=>$content_hash,
            'word_count_report_only'=>self::word_count($plain),
            'paragraph_count_report_only'=>(int)preg_match_all('/<p\b[^>]*>/iu',$html,$unused),
            'h2_count_report_only'=>(int)preg_match_all('/<h2\b[^>]*>/iu',$html,$unused),
            'section_count'=>count($sections),
            'required_section_count'=>count($blueprints),
            'factual_unit_count'=>count($units),
            'required_fact_count'=>count($required_fact_ids),
            'used_required_fact_count'=>count(array_intersect(array_keys($required_fact_ids),array_keys($used_fact_ids))),
            'duplicate_sentence_ratio'=>$duplicate_ratio,
            'first_section_pair_similarity'=>$first_section_similarity
        );
        return array('ok'=>!$errors,'errors'=>$errors,'checks'=>$checks);
    }

    private static function v5_sections($html) {
        $out=array();
        if (!preg_match_all('/<section\b([^>]*)\bdata-section-id=("|\')(.*?)\2([^>]*)>(.*?)<\/section>/isu',(string)$html,$matches,PREG_SET_ORDER|PREG_OFFSET_CAPTURE)) { return $out; }
        foreach ($matches as $match) {
            $out[]=array(
                'section_id'=>trim(html_entity_decode((string)$match[3][0],ENT_QUOTES|ENT_HTML5,'UTF-8')),
                'body'=>(string)$match[5][0],
                'offset'=>(int)$match[0][1],
                'excerpt'=>self::excerpt((string)$match[0][0])
            );
        }
        return $out;
    }

    private static function v5_factual_units($html) {
        $out=array();
        if (!preg_match_all('/<(p|li|th|td)\b([^>]*)>(.*?)<\/\1>/isu',(string)$html,$matches,PREG_SET_ORDER|PREG_OFFSET_CAPTURE)) { return $out; }
        foreach ($matches as $match) {
            $attributes=(string)$match[2][0];
            if (preg_match('/\bclass=("|\')[^"\']*\b(?:ppm|pm)-ai-disclosure\b[^"\']*\1/iu',$attributes)) { continue; }
            $text=self::plain_text((string)$match[3][0]);
            if ($text==='') { continue; }
            $refs=array();
            if (preg_match('/\bdata-fact-ids=("|\')(.*?)\1/isu',$attributes,$ref_match)) {
                foreach (preg_split('/\s+/u',trim((string)$ref_match[2])) as $ref) { if ($ref!=='') { $refs[$ref]=true; } }
            }
            $out[]=array(
                'tag'=>strtolower((string)$match[1][0]),
                'text'=>$text,
                'fact_ids'=>array_keys($refs),
                'offset'=>(int)$match[0][1],
                'excerpt'=>self::excerpt((string)$match[0][0])
            );
        }
        return $out;
    }

    private static function duplicate_sentence_ratio_v5($html) {
        $sentences=array();
        foreach (self::v5_factual_units($html) as $unit) {
            foreach (preg_split('/(?<=[.!?])\s+/u',$unit['text']) as $sentence) {
                $normalized=self::normalized_sentence($sentence);
                if (count(self::lexical_tokens($normalized))>=4) { $sentences[]=$normalized; }
            }
        }
        if (!$sentences) { return 0.0; }
        $counts=array_count_values($sentences);
        $duplicates=0;
        foreach ($counts as $count) { if ($count>1) { $duplicates+=$count; } }
        return $duplicates/count($sentences);
    }

    private static function maximum_section_pair_similarity($section_html) {
        if (!preg_match_all('/<p\b[^>]*>(.*?)<\/p>/isu',(string)$section_html,$matches) || count($matches[1])<2) { return 0.0; }
        $sets=array();
        foreach ($matches[1] as $paragraph) { $sets[]=array_flip(self::lexical_tokens($paragraph)); }
        $maximum=0.0;
        for ($i=0;$i<count($sets);$i++) {
            for ($j=$i+1;$j<count($sets);$j++) {
                $union=$sets[$i]+$sets[$j];
                $similarity=$union?count(array_intersect_key($sets[$i],$sets[$j]))/count($union):0.0;
                if ($similarity>$maximum) { $maximum=$similarity; }
            }
        }
        return $maximum;
    }

    private static function visible_links($html) {
        $out=array();
        if (!preg_match_all('/<a\b([^>]*)>(.*?)<\/a>/isu',(string)$html,$matches,PREG_SET_ORDER)) { return $out; }
        foreach ($matches as $match) {
            $tag='<a'.$match[1].'>';
            $out[]=array('href'=>self::attribute($tag,'href'),'anchor'=>self::plain_text($match[2]));
        }
        return $out;
    }

    private static function factual_units($html) {
        $out=array();
        if (!preg_match_all('/<(p|li|td)\b([^>]*)>(.*?)<\/\1>/isu',(string)$html,$matches,PREG_SET_ORDER|PREG_OFFSET_CAPTURE)) { return $out; }
        foreach ($matches as $match) {
            $tag=strtolower((string)$match[1][0]);
            $attributes=(string)$match[2][0];
            $body=(string)$match[3][0];
            $full=(string)$match[0][0];
            if (preg_match('/\bclass=("|\')[^"\']*\b(?:ppm|pm)-ai-disclosure\b[^"\']*\1/iu',$attributes)) { continue; }
            if ($tag==='p' && preg_match('/<a\b/iu',$body)) { continue; }
            $text=self::plain_text($body);
            if ($text==='') { continue; }
            $refs=array();
            if (preg_match('/\bdata-fact-ids=("|\')(.*?)\1/isu',$attributes,$ref_match)) {
                foreach (preg_split('/\s+/u',trim((string)$ref_match[2])) as $ref) {
                    if ($ref!=='') { $refs[$ref]=true; }
                }
            }
            $out[]=array(
                'tag'=>$tag,
                'text'=>$text,
                'fact_ids'=>array_keys($refs),
                'has_trace'=>(bool)preg_match('/\bppm-source-trace\b/iu',$body),
                'offset'=>(int)$match[0][1],
                'excerpt'=>self::excerpt($full)
            );
        }
        return $out;
    }

    private static function claim_reference_text($claim) {
        $fields=array('statement','display_statement','question','check','result','why','action','display_label','locator');
        $parts=array();
        foreach ($fields as $field) {
            if (isset($claim[$field]) && is_scalar($claim[$field])) { $parts[]=(string)$claim[$field]; }
        }
        return implode(' ',$parts);
    }

    private static function numeric_tokens($text) {
        $out=array();
        if (preg_match_all('/(?<![\p{L}\p{N}])\d+(?:[.,]\d+)?(?:\s*%|\s*(?:kg|km|cm|mm|m|t|v|ah|wh|°c))?/iu',(string)$text,$matches)) {
            foreach ($matches[0] as $value) { $out[]=trim((string)$value); }
        }
        return array_values(array_unique($out));
    }

    private static function normalized_contains($haystack,$needle) {
        $normalize=function($value) {
            $value=function_exists('mb_strtolower')?mb_strtolower((string)$value,'UTF-8'):strtolower((string)$value);
            return (string)preg_replace('/\s+/u','',str_replace(',', '.', $value));
        };
        $n=$normalize($needle);
        return $n!=='' && strpos($normalize($haystack),$n)!==false;
    }

    private static function lexical_tokens($text) {
        $stop=array_flip(array('der','die','das','den','dem','des','ein','eine','einer','eines','einem','einen','und','oder','aber','ist','sind','war','waren','wird','werden','wurde','wurden','mit','ohne','für','von','im','in','am','an','auf','aus','zu','zum','zur','als','bei','durch','sich','es','dass','diese','dieser','dieses','diesem','diesen','sowie','auch','noch','nur','nicht'));
        $value=function_exists('mb_strtolower')?mb_strtolower(self::plain_text($text),'UTF-8'):strtolower(self::plain_text($text));
        $out=array();
        if (preg_match_all('/[\p{L}\p{N}]+/u',$value,$matches)) {
            foreach ($matches[0] as $token) {
                if (self::string_length($token)>2 && !isset($stop[$token])) { $out[$token]=true; }
            }
        }
        return array_keys($out);
    }

    private static function lexically_supported($visible,$reference) {
        $a=array_flip(self::lexical_tokens($visible));
        $b=array_flip(self::lexical_tokens($reference));
        return count(array_intersect_key($a,$b))>=2;
    }

    private static function duplicate_sentence_ratio($html) {
        $sentences=array();
        foreach (self::factual_units($html) as $unit) {
            foreach (preg_split('/(?<=[.!?])\s+/u',$unit['text']) as $sentence) {
                $normalized=self::normalized_sentence($sentence);
                if (count(self::lexical_tokens($normalized))>=4) { $sentences[]=$normalized; }
            }
        }
        if (!$sentences) { return 0.0; }
        $counts=array_count_values($sentences);
        $duplicates=0;
        foreach ($counts as $count) { if ($count>1) { $duplicates+=$count; } }
        return $duplicates/count($sentences);
    }

    private static function normalized_sentence($sentence) {
        $value=function_exists('mb_strtolower')?mb_strtolower(self::plain_text($sentence),'UTF-8'):strtolower(self::plain_text($sentence));
        return trim((string)preg_replace('/[^\p{L}\p{N}]+/u',' ',$value));
    }

    private static function maximum_intro_pair_similarity($html) {
        $intro=self::block_body($html,'intro');
        if ($intro===null || !preg_match_all('/<p\b[^>]*>(.*?)<\/p>/isu',$intro,$matches)) { return 0.0; }
        $sets=array();
        foreach ($matches[1] as $paragraph) { $sets[]=array_flip(self::lexical_tokens($paragraph)); }
        $maximum=0.0;
        for ($i=0;$i<count($sets);$i++) {
            for ($j=$i+1;$j<count($sets);$j++) {
                $union=$sets[$i]+$sets[$j];
                $similarity=$union?count(array_intersect_key($sets[$i],$sets[$j]))/count($union):0.0;
                if ($similarity>$maximum) { $maximum=$similarity; }
            }
        }
        return $maximum;
    }

    private static function string_length($value) {
        return function_exists('mb_strlen')?mb_strlen((string)$value,'UTF-8'):strlen((string)$value);
    }

    private static function plain_text($html) {
        $text=html_entity_decode(strip_tags((string)$html),ENT_QUOTES|ENT_HTML5,'UTF-8');
        return trim((string)preg_replace('/\s+/u',' ',$text));
    }

    private static function word_count($plain) {
        $count=preg_match_all('/[\p{L}\p{N}]+(?:[’\'-][\p{L}\p{N}]+)*/u',(string)$plain,$unused);
        return $count===false?0:(int)$count;
    }

    private static function table_body_row_count($html) {
        if (!preg_match('/<table\b[^>]*class=("|\')[^"\']*\bcomparison-table\b[^"\']*\1[^>]*>(.*?)<\/table>/isu',$html,$table)) { return 0; }
        $table_html=$table[2];
        if (preg_match('/<tbody\b[^>]*>(.*?)<\/tbody>/isu',$table_html,$tbody)) {
            return (int)preg_match_all('/<tr\b[^>]*>/iu',$tbody[1],$unused);
        }
        $rows=(int)preg_match_all('/<tr\b[^>]*>/iu',$table_html,$unused);
        return max(0,$rows-1);
    }

    private static function source_trace_tags($html) {
        $out=array();
        if (!preg_match_all('/<span\b[^>]*class=("|\')[^"\']*\bppm-source-trace\b[^"\']*\1[^>]*>/iu',$html,$matches,PREG_OFFSET_CAPTURE)) { return $out; }
        foreach ($matches[0] as $match) {
            $tag=(string)$match[0];
            $out[]=array(
                'tag'=>$tag,
                'offset'=>(int)$match[1],
                'excerpt'=>self::excerpt($tag)
            );
        }
        return $out;
    }

    private static function attribute($tag,$name) {
        if (preg_match('/\b'.preg_quote($name,'/').'=("|\')(.*?)\1/isu',(string)$tag,$match)) {
            return trim(html_entity_decode((string)$match[2],ENT_QUOTES|ENT_HTML5,'UTF-8'));
        }
        return '';
    }

    private static function block_body($html,$block) {
        $quoted=preg_quote($block,'/');
        if (preg_match('/<section\b[^>]*data-block=("|\')'.$quoted.'\1[^>]*>(.*?)<\/section>/isu',$html,$match)) { return $match[2]; }
        if (preg_match('/<[^>]+\bdata-block=("|\')'.$quoted.'\1[^>]*>(.*?)<\/[^>]+>/isu',$html,$match)) { return $match[2]; }
        return null;
    }

    private static function comparison_source_assignment_errors($html) {
        $errors=array();
        $body=self::block_body($html,'options');
        if ($body===null) { return $errors; }
        $parts=preg_split('/<h3\b[^>]*>(.*?)<\/h3>/isu',$body,-1,PREG_SPLIT_DELIM_CAPTURE);
        if (!is_array($parts) || count($parts)<3) { return $errors; }
        $headings=array();
        for ($i=1;$i<count($parts);$i+=2) { $headings[]=self::plain_text($parts[$i]); }
        for ($i=1;$i<count($parts);$i+=2) {
            $heading=self::plain_text($parts[$i]);
            $segment=(string)($parts[$i+1]??'');
            $traces=self::source_trace_tags($segment);
            foreach ($traces as $trace_index=>$trace) {
                $title=self::attribute($trace['tag'],'data-source-title');
                $matched=array();
                foreach ($headings as $candidate) {
                    if (self::contains_normalized($title,$candidate)) { $matched[]=$candidate; }
                }
                if ($matched && !in_array($heading,$matched,true)) {
                    $errors[]=array(
                        'field_path'=>'content.blocks.options.'.self::normalize($heading).'.source_trace['.$trace_index.']',
                        'expected'=>$heading,
                        'actual'=>array('source_title'=>$title,'matched_option'=>$matched[0]),
                        'excerpt'=>'Option „'.$heading.'“ mit Quelle „'.$title.'“'
                    );
                }
            }
        }
        return $errors;
    }

    private static function contains_normalized($haystack,$needle) {
        $h=self::normalize($haystack); $n=self::normalize($needle);
        return $n!=='' && strpos($h,$n)!==false;
    }

    private static function normalize($value) {
        $value=self::plain_text($value);
        $value=function_exists('mb_strtolower')?mb_strtolower($value,'UTF-8'):strtolower($value);
        return (string)preg_replace('/[^\p{L}\p{N}]+/u','',$value);
    }

    private static function blocked_placeholder_text($value) {
        return (bool)preg_match('/(?:^|[^\p{L}])(test(?:quelle)?|dummy|platzhalter|beispiel|lorem|fixture)(?:$|[^\p{L}])/iu',(string)$value);
    }

    private static function valid_non_repetitive_sha256($value) {
        $value=strtolower(trim((string)$value));
        if (!preg_match('/^[0-9a-f]{64}$/',$value)) { return false; }
        return !preg_match('/^([0-9a-f])\1{63}$/',$value);
    }

    private static function excerpt($value,$max=180) {
        $value=(string)preg_replace('/\s+/u',' ',(string)$value);
        if (function_exists('mb_substr')) { return mb_substr($value,0,$max,'UTF-8'); }
        return substr($value,0,$max);
    }

    private static function err($code,$rule,$path,$expected,$actual,$reason,$context,$hash) {
        return PPM679_Diagnostic::error($code,$rule,$path,$expected,$actual,$reason,$context,$hash,__CLASS__,null,array('includes/content-validator.php','contracts/article-type-templates.json','contracts/table-contract-v1.json'));
    }
}
