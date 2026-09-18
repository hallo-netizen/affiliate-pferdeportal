<?php
if (!defined('ABSPATH')) { return; }

final class PPM679_Content_Structure_Language_Gate {
    const VERSION='6.7.9-wave2-quarantine';
    const CONTRACT_FILE='contracts/content-structure-language-gate-v2.json';

    public static function evaluate($generated,$item=array(),$context='content_structure_language_gate_v2',$server_state_hash='') {
        $contract=self::load_contract();
        $errors=array();
        $checks=array(
            'contract'=>'content_structure_language_gate_v2',
            'version'=>self::VERSION,
            'scope_limit'=>'deterministic structure, bindings and LanguageTool evidence; no final editorial or visual PASS'
        );
        if (!is_array($contract)) {
            $errors[]=self::error('BLOCKED_WAVE2_CONTRACT_MISSING','Wave-2 content contract missing or invalid.','contract',self::CONTRACT_FILE,null,$context,$server_state_hash);
            return self::result($errors,$checks);
        }

        $title=(string)($generated['title']??'');
        $html=(string)($generated['content_html']??'');
        $type=(string)($item['article_type']??($generated['article_type']??''));
        $content_hash=hash('sha256',$html);
        $binding=isset($item['quality_binding'])&&is_array($item['quality_binding'])?$item['quality_binding']:array();
        $checks['content_hash']=$content_hash;
        $checks['article_type']=$type;
        $checks['contract_hash']=hash('sha256',self::canonical_json($contract));

        if ((string)($binding['contract']??'')!=='content_structure_language_binding_v2') {
            $errors[]=self::error('BLOCKED_WAVE2_QUALITY_BINDING_MISSING','The Wave-2 quality binding is missing or has the wrong contract.','item.quality_binding.contract','content_structure_language_binding_v2',$binding['contract']??null,$context,$server_state_hash);
        }
        $declared_binding_hash=strtolower(trim((string)($item['quality_binding_hash']??'')));
        $actual_binding_hash=class_exists('PPM679_Diagnostic')?PPM679_Diagnostic::stable_hash($binding):hash('sha256',self::canonical_json($binding));
        $checks['quality_binding_hash']=$actual_binding_hash;
        if (!preg_match('/^[0-9a-f]{64}$/',$declared_binding_hash) || !hash_equals($actual_binding_hash,$declared_binding_hash)) {
            $errors[]=self::error('BLOCKED_WAVE2_QUALITY_BINDING_HASH','The Wave-2 quality binding hash does not match the exact binding.','item.quality_binding_hash',$actual_binding_hash,$declared_binding_hash,$context,$server_state_hash);
        }

        self::check_visible_title_and_marker($title,$html,$binding,$contract,$errors,$checks,$context,$server_state_hash);
        self::check_blocks_and_intro($html,$type,$binding,$contract,$errors,$checks,$context,$server_state_hash);
        self::check_headings($html,$binding,$contract,$errors,$checks,$context,$server_state_hash);
        self::check_faq_direct_answer($html,$type,$binding,$contract,$errors,$checks,$context,$server_state_hash);
        self::check_lists($html,$contract,$errors,$checks,$context,$server_state_hash);
        self::check_links($html,$item,$binding,$contract,$errors,$checks,$context,$server_state_hash);
        self::check_conclusion($html,$type,$contract,$errors,$checks,$context,$server_state_hash);
        self::check_table_value($html,$binding,$contract,$errors,$checks,$context,$server_state_hash);
        self::check_language_evidence($html,$content_hash,$binding,$contract,$errors,$checks,$context,$server_state_hash);
        self::check_category_binding($binding,$contract,$errors,$checks,$context,$server_state_hash);
        self::check_known_language_patterns($html,$contract,$errors,$checks,$context,$server_state_hash);
        self::check_basic_html($html,$errors,$checks,$context,$server_state_hash);

        return self::result($errors,$checks);
    }

    private static function check_visible_title_and_marker($title,$html,$binding,$contract,&$errors,&$checks,$context,$server_state_hash) {
        $h1=(int)preg_match_all('/<h1\b[^>]*>/iu',$html,$unused);
        $checks['body_h1_count']=$h1;
        if ($h1!==0) {
            $errors[]=self::error('BLOCKED_WAVE2_BODY_H1','WordPress alone provides the visible article title.','content.body_h1_count',0,$h1,$context,$server_state_hash);
        }
        $normalized_title=self::normalize($title);
        $title_repeated=$normalized_title!=='' && strpos(self::normalize(self::plain_text($html)),$normalized_title)!==false;
        $checks['title_repeated_in_body']=$title_repeated;
        if ($title_repeated) {
            $errors[]=self::error('BLOCKED_WAVE2_TITLE_REPEATED','The WordPress title is repeated inside the article body.','content.title_repeated_in_body',false,true,$context,$server_state_hash);
        }
        $marker=trim((string)($binding['internal_test_marker']??''));
        $regex=(string)($contract['visible_test_marker_regex']??'');
        $valid_marker=$marker!=='' && $regex!=='' && @preg_match('/'.$regex.'/u','['.$marker.']')===1;
        $visible=$marker!=='' && (stripos($title,$marker)!==false || stripos($html,$marker)!==false);
        $checks['internal_test_marker_valid']=$valid_marker;
        $checks['internal_test_marker_visible']=$visible;
        if (!$valid_marker) {
            $errors[]=self::error('BLOCKED_WAVE2_INTERNAL_MARKER_MISSING','A valid internal test marker is required in the quality binding.','item.quality_binding.internal_test_marker','LT marker without brackets',$marker,$context,$server_state_hash);
        }
        if ($visible || ($regex!=='' && @preg_match('/'.$regex.'/u',$title.' '.$html))) {
            $errors[]=self::error('BLOCKED_WAVE2_VISIBLE_TEST_MARKER','The internal test marker may not be visible in title or article body.','content.visible_test_marker',false,true,$context,$server_state_hash);
        }
    }

    private static function check_blocks_and_intro($html,$type,$binding,$contract,&$errors,&$checks,$context,$server_state_hash) {
        $blocks=self::sections($html);
        $ids=array_map(function($s){ return $s['block']; },$blocks);
        $required=(array)($contract['required_blocks_by_type'][$type]??array());
        $missing=array_values(array_diff($required,$ids));
        $checks['section_blocks']=$ids;
        $checks['required_blocks']=$required;
        if ($missing) {
            $errors[]=self::error('BLOCKED_WAVE2_ARTICLE_TYPE_BLOCKS','Required blocks for the selected article type are missing.','content.required_blocks',$required,array('missing'=>$missing,'actual'=>$ids),$context,$server_state_hash);
        }
        if (!$blocks || $blocks[0]['block']!=='intro') {
            $errors[]=self::error('BLOCKED_WAVE2_INTRO_NOT_FIRST','The first article block must be the short introduction.','content.first_block','intro',$ids[0]??null,$context,$server_state_hash);
            return;
        }
        $intro=$blocks[0]['body'];
        $intro_words=self::word_count(self::plain_text($intro));
        $min=(int)($contract['intro']['minimum_words']??30);
        $max=(int)($contract['intro']['maximum_words']??100);
        $starts_with_p=preg_match('/^\s*<p\b[^>]*>/iu',$intro)===1;
        $heading_count=(int)preg_match_all('/<h[1-6]\b[^>]*>/iu',$intro,$unused);
        $checks['intro_word_count']=$intro_words;
        $checks['intro_starts_with_paragraph']=$starts_with_p;
        $checks['intro_heading_count']=$heading_count;
        if (!$starts_with_p || $heading_count!==0 || $intro_words<$min || $intro_words>$max) {
            $errors[]=self::error('BLOCKED_WAVE2_INTRO_STRUCTURE','The article needs a short introductory paragraph without a heading.','content.intro',array('first_element'=>'p','headings'=>0,'word_range'=>array($min,$max)),array('first_element_is_p'=>$starts_with_p,'headings'=>$heading_count,'words'=>$intro_words),$context,$server_state_hash);
        }
    }

    private static function check_headings($html,$binding,$contract,&$errors,&$checks,$context,$server_state_hash) {
        $settings=(array)($contract['headings']??array());
        $headings=self::headings($html);
        $generic=array_map(array(__CLASS__,'normalize'),(array)($settings['generic_or_technical_headings']??array()));
        $forbidden=array_map(array(__CLASS__,'normalize'),(array)($settings['forbidden_fragments']??array()));
        $reserved=array_map(array(__CLASS__,'normalize'),(array)($settings['reserved_headings']??array()));
        $intent_terms=array_values(array_filter(array_map(array(__CLASS__,'normalize'),(array)($binding['intent_terms']??array()))));
        $min_words=(int)($settings['minimum_words']??2);
        $max_words=(int)($settings['maximum_words']??14);
        $min_between=(int)($settings['minimum_words_between_headings']??28);
        $threshold=(float)($settings['near_duplicate_token_similarity']??0.72);
        $seen=array();
        $generic_hits=array();
        $intent_misses=array();
        $near_duplicates=array();
        $spacing_errors=array();
        foreach ($headings as $index=>$heading) {
            $normalized=self::normalize($heading['text']);
            $words=self::word_count($heading['text']);
            if (in_array($normalized,$generic,true)) { $generic_hits[]=$heading['text']; }
            foreach ($forbidden as $fragment) {
                if ($fragment!=='' && strpos($normalized,$fragment)!==false) { $generic_hits[]=$heading['text']; break; }
            }
            if (!in_array($normalized,$reserved,true) && ($words<$min_words || $words>$max_words)) {
                $errors[]=self::error('BLOCKED_WAVE2_HEADING_LENGTH','Headings must be short, readable and concrete.','content.headings['.$index.'].word_count',array($min_words,$max_words),$words,$context,$server_state_hash);
            }
            if (!in_array($normalized,$reserved,true)) {
                $has_intent=false;
                foreach ($intent_terms as $term) { if ($term!=='' && strpos($normalized,$term)!==false) { $has_intent=true; break; } }
                if (!$has_intent) { $intent_misses[]=$heading['text']; }
            }
            foreach ($seen as $previous) {
                $similarity=self::token_similarity($normalized,$previous['normalized'],(array)($settings['stopwords']??array()));
                if ($normalized===$previous['normalized'] || $similarity>=$threshold) {
                    $near_duplicates[]=array('first'=>$previous['text'],'second'=>$heading['text'],'similarity'=>$similarity);
                }
            }
            $seen[]=array('text'=>$heading['text'],'normalized'=>$normalized);
            if (isset($headings[$index+1])) {
                $between=substr($html,$heading['end'],$headings[$index+1]['start']-$heading['end']);
                $between_words=self::word_count(self::plain_text($between));
                if ($between_words<$min_between) {
                    $spacing_errors[]=array('first'=>$heading['text'],'second'=>$headings[$index+1]['text'],'words_between'=>$between_words);
                }
            }
        }
        $generic_hits=array_values(array_unique($generic_hits));
        $checks['heading_count']=count($headings);
        $checks['generic_heading_hits']=$generic_hits;
        $checks['intent_heading_misses']=$intent_misses;
        $checks['near_duplicate_headings']=$near_duplicates;
        $checks['heading_spacing_errors']=$spacing_errors;
        if ($generic_hits) {
            $errors[]=self::error('BLOCKED_WAVE2_GENERIC_TECHNICAL_HEADING','Headings must sound human and name the concrete reader question.','content.generic_headings',array(),$generic_hits,$context,$server_state_hash);
        }
        if ($intent_misses) {
            $errors[]=self::error('BLOCKED_WAVE2_HEADING_INTENT_MISMATCH','Every non-reserved heading must contain a bound topic or intent term.','content.heading_intent_terms',$intent_terms,$intent_misses,$context,$server_state_hash);
        }
        if ($near_duplicates) {
            $errors[]=self::error('BLOCKED_WAVE2_SEMANTIC_DUPLICATE_HEADING','Headings may not repeat the same meaning.','content.near_duplicate_headings',array(),$near_duplicates,$context,$server_state_hash);
        }
        if ($spacing_errors) {
            $errors[]=self::error('BLOCKED_WAVE2_INSUFFICIENT_TEXT_BETWEEN_HEADINGS','There must be meaningful text between every two headings.','content.words_between_headings','at least '.$min_between,$spacing_errors,$context,$server_state_hash);
        }
    }

    private static function check_faq_direct_answer($html,$type,$binding,$contract,&$errors,&$checks,$context,$server_state_hash) {
        if ($type!=='FAQ') { return; }
        $intro=self::block_body($html,'intro');
        $first=self::first_paragraph($intro===null?'':$intro);
        $answer=trim((string)($binding['faq_direct_answer']??''));
        $min=(int)($contract['faq']['direct_answer_minimum_words']??12);
        $starts=$answer!=='' && strpos(self::normalize($first),self::normalize($answer))===0;
        $meta_hit='';
        foreach ((array)($contract['faq']['forbidden_meta_openings']??array()) as $phrase) {
            if (strpos(self::normalize($first),self::normalize($phrase))===0) { $meta_hit=$phrase; break; }
        }
        $checks['faq_direct_answer_bound']=$answer!=='';
        $checks['faq_intro_starts_with_direct_answer']=$starts;
        $checks['faq_direct_answer_word_count']=self::word_count($answer);
        $checks['faq_meta_opening_hit']=$meta_hit;
        if ($answer==='' || self::word_count($answer)<$min || !$starts || $meta_hit!=='') {
            $errors[]=self::error('BLOCKED_WAVE2_FAQ_DIRECT_ANSWER','A FAQ must start with the exact bound, useful direct answer rather than meta commentary.','content.faq_direct_answer',array('minimum_words'=>$min,'must_start_intro'=>true,'meta_opening'=>false),array('bound_answer'=>$answer,'starts_intro'=>$starts,'meta_opening'=>$meta_hit),$context,$server_state_hash);
        }
    }

    private static function check_lists($html,$contract,&$errors,&$checks,$context,$server_state_hash) {
        $counts=array();
        if (preg_match_all('/<(ul|ol)\b[^>]*>(.*?)<\/\1>/isu',$html,$lists,PREG_SET_ORDER)) {
            foreach ($lists as $list) { $counts[]=(int)preg_match_all('/<li\b[^>]*>.*?<\/li>/isu',$list[2],$unused); }
        }
        $max=$counts?max($counts):0;
        $required=(int)($contract['lists']['minimum_items_in_one_list']??4);
        $checks['list_count']=count($counts);
        $checks['maximum_list_items']=$max;
        if (count($counts)<(int)($contract['lists']['minimum_lists']??1) || $max<$required) {
            $errors[]=self::error('BLOCKED_WAVE2_REQUIRED_LIST','At least one real list with four complete items is required.','content.lists',array('minimum_lists'=>1,'minimum_items_in_one_list'=>$required),array('list_count'=>count($counts),'maximum_items'=>$max),$context,$server_state_hash);
        }
    }

    private static function check_links($html,$item,$binding,$contract,&$errors,&$checks,$context,$server_state_hash) {
        $settings=(array)($contract['links']??array());
        $required_roles=(array)($settings['required_roles']??array());
        $bound=isset($binding['link_bindings'])&&is_array($binding['link_bindings'])?$binding['link_bindings']:array();
        $registry=isset($binding['portal_link_registry'])&&is_array($binding['portal_link_registry'])?$binding['portal_link_registry']:array();
        $entries=isset($registry['entries'])&&is_array($registry['entries'])?$registry['entries']:array();
        $registry_hash=(string)($binding['portal_link_registry_hash']??'');
        $actual_registry_hash=class_exists('PPM679_Diagnostic')?PPM679_Diagnostic::stable_hash($registry):hash('sha256',self::canonical_json($registry));
        $links=self::links_with_blocks($html);
        $checks['visible_internal_links']=$links;
        $checks['portal_link_registry_hash']=$actual_registry_hash;
        if (!preg_match('/^[0-9a-f]{64}$/',$registry_hash) || !hash_equals($actual_registry_hash,$registry_hash)) {
            $errors[]=self::error('BLOCKED_WAVE2_LINK_REGISTRY_HASH','The portal link registry is missing or hash-mismatched.','item.quality_binding.portal_link_registry_hash',$actual_registry_hash,$registry_hash,$context,$server_state_hash);
        }
        if (count($links)!==(int)($settings['required_count']??3)) {
            $errors[]=self::error('BLOCKED_WAVE2_INTERNAL_LINK_COUNT','Exactly three visible internal links are required.','content.visible_internal_links',(int)($settings['required_count']??3),count($links),$context,$server_state_hash);
        }
        $bound_by_role=array();
        foreach ($bound as $b) { $role=(string)($b['role']??''); if ($role!=='') { $bound_by_role[$role]=$b; } }
        $entry_by_href=array();
        foreach ($entries as $entry) { $href=(string)($entry['href']??''); if ($href!=='') { $entry_by_href[$href]=$entry; } }
        $found_roles=array();
        $found_blocks=array();
        foreach ($required_roles as $role) {
            $b=$bound_by_role[$role]??null;
            if (!is_array($b)) {
                $errors[]=self::error('BLOCKED_WAVE2_INTERNAL_LINK_ROLE_MISSING','Every approved internal-link role must be bound exactly once.','item.quality_binding.link_bindings.'.$role,'present',null,$context,$server_state_hash);
                continue;
            }
            $match=null;
            foreach ($links as $link) {
                if ((string)$link['href']===(string)($b['href']??'') && (string)$link['anchor']===(string)($b['anchor']??'')) { $match=$link; break; }
            }
            if (!is_array($match)) {
                $errors[]=self::error('BLOCKED_WAVE2_BOUND_LINK_MISSING','A bound internal link pair is missing from the article.','content.links.'.$role,$b,'missing',$context,$server_state_hash);
                continue;
            }
            $found_roles[$role]=$match;
            $found_blocks[$role]=$match['block'];
            $entry=$entry_by_href[(string)$match['href']]??null;
            if (!is_array($entry) || empty($entry['active']) || (string)($entry['anchor']??'')!==(string)$match['anchor'] || (string)($entry['reason']??'')!==(string)($b['reason']??'')) {
                $errors[]=self::error('BLOCKED_WAVE2_INTERNAL_LINK_REGISTRY','The visible link is not active and exactly bound to the current portal registry.','content.links.'.$role.'.registry',$b,$entry,$context,$server_state_hash);
            }
            $expected_block=(string)($b['section_id']??'');
            if ($expected_block==='' || $match['block']!==$expected_block) {
                $errors[]=self::error('BLOCKED_WAVE2_INTERNAL_LINK_PLACEMENT','The link is not in its bound section.','content.links.'.$role.'.block',$expected_block,$match['block'],$context,$server_state_hash);
            }
            $href=(string)$match['href'];
            if ($href==='' || substr($href,0,1)!=='/' || substr($href,0,2)==='//') {
                $errors[]=self::error('BLOCKED_WAVE2_INTERNAL_LINK_TARGET','Internal links must use a real relative portal URL.','content.links.'.$role.'.href','relative internal URL',$href,$context,$server_state_hash);
            }
        }
        if (isset($found_blocks['further_information']) && $found_blocks['further_information']!==(string)($settings['further_information_block']??'further_information')) {
            $errors[]=self::error('BLOCKED_WAVE2_FURTHER_INFORMATION_LINK','The third link must be in Weiterführende Informationen.','content.links.further_information.block',$settings['further_information_block']??'further_information',$found_blocks['further_information'],$context,$server_state_hash);
        }
        if (count($found_blocks)===count($required_roles) && count(array_unique(array_values($found_blocks)))!==count($required_roles)) {
            $errors[]=self::error('BLOCKED_WAVE2_LINKS_NOT_DISTRIBUTED','The three internal links must be distributed across three different article blocks.','content.link_blocks','three distinct blocks',$found_blocks,$context,$server_state_hash);
        }
        $runtime_links=isset($item['runtime_order']['links'])&&is_array($item['runtime_order']['links'])?$item['runtime_order']['links']:array();
        foreach ($required_roles as $role) {
            $exists=false;
            foreach ($runtime_links as $link) { if ((string)($link['role']??'')===$role) { $exists=true; break; } }
            if (!$exists) {
                $errors[]=self::error('BLOCKED_WAVE2_RUNTIME_LINK_ROLE','The runtime order does not bind all three approved link roles.','item.runtime_order.links.'.$role,'present',false,$context,$server_state_hash);
            }
        }
        $checks['resolved_link_roles']=$found_roles;
    }

    private static function check_conclusion($html,$type,$contract,&$errors,&$checks,$context,$server_state_hash) {
        $body=self::block_body($html,(string)($contract['conclusion']['required_block']??'conclusion'));
        $plain=self::plain_text($html);
        $total=self::word_count($plain);
        $words=$body===null?0:self::word_count(self::plain_text($body));
        $paragraphs=$body===null?0:(int)preg_match_all('/<p\b[^>]*>.*?<\/p>/isu',$body,$unused);
        $ratio=$total>0?$words/$total:0.0;
        $min=(float)($contract['conclusion']['minimum_ratio_by_type'][$type]??0.08);
        $min_p=(int)($contract['conclusion']['minimum_paragraphs']??2);
        $checks['conclusion_word_count']=$words;
        $checks['conclusion_ratio']=$ratio;
        $checks['conclusion_paragraph_count']=$paragraphs;
        if ($body===null || $ratio<$min || $paragraphs<$min_p) {
            $errors[]=self::error('BLOCKED_WAVE2_CONCLUSION_BALANCE','The conclusion must be substantial, balanced and use at least two paragraphs.','content.conclusion',array('minimum_ratio'=>$min,'minimum_paragraphs'=>$min_p),array('ratio'=>$ratio,'paragraphs'=>$paragraphs,'words'=>$words),$context,$server_state_hash);
        }
    }

    private static function check_table_value($html,$binding,$contract,&$errors,&$checks,$context,$server_state_hash) {
        $settings=(array)($contract['table']??array());
        $body=self::block_body($html,(string)($settings['required_block']??'table'));
        $tables=(int)preg_match_all('/<table\b[^>]*>(.*?)<\/table>/isu',$html,$all_tables,PREG_SET_ORDER);
        $rows=0; $columns=0; $headers=array(); $unique_ratio=0.0; $heading='';
        if ($body!==null) {
            if (preg_match('/<h2\b[^>]*>(.*?)<\/h2>/isu',$body,$hm)) { $heading=self::plain_text($hm[1]); }
            if (preg_match('/<table\b[^>]*>(.*?)<\/table>/isu',$body,$tm)) {
                $table_html=$tm[0];
                if (preg_match('/<thead\b[^>]*>(.*?)<\/thead>/isu',$table_html,$thead) && preg_match_all('/<th\b[^>]*>(.*?)<\/th>/isu',$thead[1],$ths,PREG_SET_ORDER)) {
                    foreach ($ths as $th) { $headers[]=self::plain_text($th[1]); }
                }
                if (preg_match('/<tbody\b[^>]*>(.*?)<\/tbody>/isu',$table_html,$tbody)) {
                    $rows=(int)preg_match_all('/<tr\b[^>]*>.*?<\/tr>/isu',$tbody[1],$trmatches);
                    if (!empty($trmatches[0]) && preg_match_all('/<(?:td|th)\b[^>]*>.*?<\/(?:td|th)>/isu',$trmatches[0][0],$cells)) { $columns=count($cells[0]); }
                }
                $table_tokens=self::token_set(self::plain_text($table_html));
                $prose_tokens=self::token_set(self::plain_text(str_replace($table_html,' ',$html)));
                $unique=array_diff_key($table_tokens,$prose_tokens);
                $unique_ratio=count($table_tokens)>0?count($unique)/count($table_tokens):0.0;
            }
        }
        $statement=trim((string)($binding['table_value_statement']??''));
        $generic_h=array_map(array(__CLASS__,'normalize'),(array)($settings['generic_headings_forbidden']??array()));
        $generic_c=array_map(array(__CLASS__,'normalize'),(array)($settings['generic_column_headings_forbidden']??array()));
        $bad_headers=array();
        foreach ($headers as $header) { if (in_array(self::normalize($header),$generic_c,true)) { $bad_headers[]=$header; } }
        $checks['table_count']=$tables;
        $checks['table_heading']=$heading;
        $checks['table_headers']=$headers;
        $checks['table_body_rows']=$rows;
        $checks['table_columns']=$columns;
        $checks['table_unique_content_token_ratio']=$unique_ratio;
        $checks['table_value_statement']=$statement;
        if ($tables!==(int)($settings['exact_count']??1) || $body===null || $heading==='' || in_array(self::normalize($heading),$generic_h,true) || $bad_headers || $rows<(int)($settings['minimum_body_rows']??4) || $columns<(int)($settings['minimum_columns']??3) || $unique_ratio<(float)($settings['minimum_unique_content_token_ratio']??0.18) || self::word_count($statement)<8) {
            $errors[]=self::error('BLOCKED_WAVE2_TABLE_VALUE','The table must have a concrete purpose, useful headings and additional information beyond prose.','content.table',array('count'=>1,'body_rows'=>$settings['minimum_body_rows']??4,'columns'=>$settings['minimum_columns']??3,'unique_token_ratio'=>$settings['minimum_unique_content_token_ratio']??0.18,'value_statement_words'=>'>=8'),array('count'=>$tables,'heading'=>$heading,'bad_headers'=>$bad_headers,'body_rows'=>$rows,'columns'=>$columns,'unique_token_ratio'=>$unique_ratio,'value_statement'=>$statement),$context,$server_state_hash);
        }
    }

    private static function check_language_evidence($html,$content_hash,$binding,$contract,&$errors,&$checks,$context,$server_state_hash) {
        $evidence=isset($binding['language_evidence'])&&is_array($binding['language_evidence'])?$binding['language_evidence']:array();
        $settings=(array)($contract['language_evidence']??array());
        $exceptions=isset($evidence['approved_exceptions'])&&is_array($evidence['approved_exceptions'])?$evidence['approved_exceptions']:array();
        $bad_exceptions=array();
        foreach ($exceptions as $index=>$exception) {
            foreach ((array)($settings['human_exception_required_fields']??array()) as $field) {
                if (!array_key_exists($field,$exception) || $exception[$field]==='') { $bad_exceptions[]=$index.':'.$field; }
            }
            if (($exception['approved_by_human_user']??null)!==true) { $bad_exceptions[]=$index.':approved_by_human_user'; }
        }
        $expected_checked_text=self::visible_language_text($html);
        if ((string)($evidence['evidence_mode']??'')==='FULL_LANGUAGETOOL43_BASELINE_PLUS_HASHED_MAINBLOCK1_DELTA_REQUIRES_INDEPENDENT_CLAUDE_REVIEW') {
            $checked_text=(string)($evidence['checked_text']??'');
            $deltas=isset($evidence['changed_visible_units'])&&is_array($evidence['changed_visible_units'])?$evidence['changed_visible_units']:array();
            $bad_delta=array();
            foreach($deltas as $i=>$delta){
                if ((string)($delta['before_sha256']??'')!==hash('sha256',(string)($delta['before']??'')) || (string)($delta['after_sha256']??'')!==hash('sha256',(string)($delta['after']??''))) { $bad_delta[]=$i; }
                if ((string)($delta['after']??'')==='' || strpos($expected_checked_text,(string)$delta['after'])===false) { $bad_delta[]=$i.':after_missing'; }
            }
            $scan=(array)($evidence['deterministic_forbidden_phrase_scan']??array());
            $hits=array(); foreach((array)($scan['forbidden_phrases']??array()) as $phrase){ if($phrase!==''&&stripos($expected_checked_text,(string)$phrase)!==false){$hits[]=$phrase;} }
            $valid=(string)($evidence['engine']??'')===(string)($settings['required_engine']??'')
                && (string)($evidence['outer_dependency_sha256']??'')===(string)($settings['outer_dependency_sha256']??'')
                && (string)($evidence['inner_dependency_sha256']??'')===(string)($settings['inner_dependency_sha256']??'')
                && (string)($evidence['content_hash']??'')===$content_hash
                && $checked_text===$expected_checked_text
                && (string)($evidence['checked_text_sha256']??'')===hash('sha256',$checked_text)
                && count($deltas)===(int)($evidence['changed_visible_unit_count']??-1)
                && !$bad_delta && !$hits
                && ($evidence['independent_mainblock1_claude_review_required']??null)===true
                && (string)($evidence['required_external_verdict']??'')==='CONFIRM_PASS_MAINBLOCK1_CONSOLIDATED_RULE_COVERAGE_SIGNED_BUILD'
                && ($evidence['external_review_claimed_by_build']??null)===false;
            $checks['language_evidence_valid']=$valid;
            $checks['language_evidence_mode']='BASELINE_PLUS_HASHED_DELTA_REQUIRES_EXTERNAL_CLAUDE';
            $checks['language_delta_count']=count($deltas); $checks['language_delta_errors']=$bad_delta; $checks['language_forbidden_phrase_hits']=$hits;
            $checks['language_external_review_required']=true; $checks['language_external_review_claimed_by_build']=false;
            if(!$valid){$errors[]=self::error('BLOCKED_MAINBLOCK1_LANGUAGE_DELTA_EVIDENCE','Changed visible text requires exact hashed deltas, forbidden-phrase regression scan and mandatory independent Claude review before installation.','item.quality_binding.language_evidence','valid baseline plus hashed delta evidence',$evidence,$context,$server_state_hash);}
            return;
        }
        $checked_text=(string)($evidence['checked_text']??'');
        $checked_text_hash=hash('sha256',$checked_text);
        $raw_report_json=(string)($evidence['raw_report_json']??'');
        $raw_report_hash=hash('sha256',$raw_report_json);
        $decoded_report=json_decode($raw_report_json,true);
        $report_matches=is_array($decoded_report)&&isset($decoded_report['matches'])&&is_array($decoded_report['matches'])?$decoded_report['matches']:null;
        $execution=isset($evidence['execution_record'])&&is_array($evidence['execution_record'])?$evidence['execution_record']:array();
        $valid=(string)($evidence['engine']??'')===(string)($settings['required_engine']??'')
            && (string)($evidence['outer_dependency_sha256']??'')===(string)($settings['outer_dependency_sha256']??'')
            && (string)($evidence['inner_dependency_sha256']??'')===(string)($settings['inner_dependency_sha256']??'')
            && (string)($evidence['content_hash']??'')===$content_hash
            && $checked_text===$expected_checked_text
            && (string)($evidence['checked_text_sha256']??'')===$checked_text_hash
            && preg_match('/^[0-9a-f]{64}$/',(string)($evidence['raw_report_sha256']??''))===1
            && hash_equals((string)$evidence['raw_report_sha256'],$raw_report_hash)
            && is_array($report_matches)
            && count($report_matches)===(int)($settings['raw_finding_count_exact']??0)
            && (int)($evidence['raw_finding_count']??-1)===(int)($settings['raw_finding_count_exact']??0)
            && (int)($evidence['unresolved_finding_count']??-1)===(int)($settings['unresolved_findings_exact']??0)
            && (int)($evidence['return_code']??-1)===(int)($settings['return_code_exact']??0)
            && (string)($execution['input_sha256']??'')===$checked_text_hash
            && (string)($execution['raw_stdout_sha256']??'')===$raw_report_hash
            && (int)($execution['return_code']??-1)===(int)($settings['return_code_exact']??0)
            && !$bad_exceptions;
        $checks['language_evidence_valid']=$valid;
        $checks['language_checked_text_sha256']=$checked_text_hash;
        $checks['language_raw_report_sha256']=$raw_report_hash;
        $checks['language_raw_finding_count']=is_array($report_matches)?count($report_matches):null;
        $checks['language_unresolved_finding_count']=$evidence['unresolved_finding_count']??null;
        $checks['language_exception_errors']=$bad_exceptions;
        if (!$valid) {
            $errors[]=self::error(
                'BLOCKED_WAVE2_LANGUAGE_EVIDENCE',
                'The complete visible text requires exact LanguageTool 43 raw evidence with zero unresolved findings.',
                'item.quality_binding.language_evidence',
                array(
                    'engine'=>$settings['required_engine']??'',
                    'content_hash'=>$content_hash,
                    'checked_text_sha256'=>hash('sha256',$expected_checked_text),
                    'raw_finding_count'=>0,
                    'unresolved_finding_count'=>0,
                    'return_code'=>0,
                    'human_exceptions_only'=>true
                ),
                array(
                    'engine'=>$evidence['engine']??null,
                    'content_hash'=>$evidence['content_hash']??null,
                    'checked_text_matches'=>$checked_text===$expected_checked_text,
                    'checked_text_sha256'=>$evidence['checked_text_sha256']??null,
                    'raw_report_sha256'=>$evidence['raw_report_sha256']??null,
                    'raw_report_decodes'=>is_array($decoded_report),
                    'raw_finding_count'=>is_array($report_matches)?count($report_matches):null,
                    'unresolved_finding_count'=>$evidence['unresolved_finding_count']??null,
                    'return_code'=>$evidence['return_code']??null,
                    'execution_record'=>$execution,
                    'exception_errors'=>$bad_exceptions
                ),
                $context,$server_state_hash
            );
        }
    }

    private static function check_category_binding($binding,$contract,&$errors,&$checks,$context,$server_state_hash) {
        $category=isset($binding['wordpress_category'])&&is_array($binding['wordpress_category'])?$binding['wordpress_category']:array();
        $id=(int)($category['id']??0);
        $slug=self::normalize((string)($category['slug']??''));
        $name=trim((string)($category['name']??''));
        $forbidden=array_map(array(__CLASS__,'normalize'),(array)($contract['wordpress_binding']['forbidden_category_slugs']??array()));
        $legacy_valid=$id>=(int)($contract['wordpress_binding']['category_id_minimum']??1) && $slug!=='' && $name!=='' && !in_array($slug,$forbidden,true);
        $semantic_valid=$slug!=='' && $name!==''
            && trim((string)($category['hierarchy_path']??''))!==''
            && (string)($category['taxonomy']??'')==='category'
            && preg_match('/^[a-f0-9]{64}$/',(string)($category['category_source_snapshot_hash']??''))===1
            && ($category['semantic_binding_not_numeric_identity']??false)===true
            && !in_array($slug,$forbidden,true);
        $valid=$legacy_valid||$semantic_valid;
        $checks['wordpress_category']=$category;
        $checks['wordpress_category_binding_mode']=$semantic_valid?'SEMANTIC_SNAPSHOT_BOUND_LIVE_ID_PENDING':'LEGACY_NUMERIC_BOUND';
        $checks['wordpress_category_valid']=$valid;
        if (!$valid) {
            $errors[]=self::error('BLOCKED_WAVE2_WORDPRESS_CATEGORY','A real semantic target category or legacy numeric binding is required and Uncategorized is forbidden.','item.quality_binding.wordpress_category',array('semantic'=>array('slug'=>'real non-default','name'=>'non-empty','hierarchy_path'=>'non-empty','taxonomy'=>'category','snapshot_hash'=>'sha256'),'legacy'=>array('id'=>'>=1','slug'=>'real non-default','name'=>'non-empty')),$category,$context,$server_state_hash);
        }
    }

    private static function check_known_language_patterns($html,$contract,&$errors,&$checks,$context,$server_state_hash) {
        $plain=self::normalize(self::plain_text($html));
        $hits=array();
        foreach ((array)($contract['known_language_regression_phrases']??array()) as $phrase) {
            if (strpos($plain,self::normalize($phrase))!==false) { $hits[]=$phrase; }
        }
        $checks['known_language_regression_hits']=$hits;
        if ($hits) {
            $errors[]=self::error('BLOCKED_WAVE2_KNOWN_UNNATURAL_LANGUAGE','A known unnatural sentence pattern is still present.','content.known_language_regressions',array(),$hits,$context,$server_state_hash);
        }
    }

    private static function check_basic_html($html,&$errors,&$checks,$context,$server_state_hash) {
        $balance=self::basic_html_balance($html);
        $table_ok=preg_match_all('/<table\b/iu',$html,$unused)===preg_match_all('/<\/table>/iu',$html,$unused2)
            && preg_match_all('/<thead\b/iu',$html,$unused3)===preg_match_all('/<\/thead>/iu',$html,$unused4)
            && preg_match_all('/<tbody\b/iu',$html,$unused5)===preg_match_all('/<\/tbody>/iu',$html,$unused6);
        $checks['html_balance']=$balance;
        $checks['table_tag_balance']=$table_ok;
        if (!$balance['ok'] || !$table_ok) {
            $errors[]=self::error('BLOCKED_WAVE2_INVALID_HTML','The final article HTML is not structurally balanced.','content.html','balanced HTML and table tags',array('balance'=>$balance,'table_balance'=>$table_ok),$context,$server_state_hash);
        }
    }

    private static function result($errors,$checks) {
        $ok=!$errors;
        return array(
            'ok'=>$ok,
            'status'=>$ok?'PASS':'BLOCKED',
            'content_structure_language_gate_status'=>$ok?'PASS':'BLOCKED',
            'draft_create_allowed'=>false,
            'publish_allowed'=>false,
            'errors'=>$errors,
            'checks'=>$checks
        );
    }

    private static function load_contract() {
        $file=defined('PPM679_PLUGIN_DIR')?PPM679_PLUGIN_DIR.self::CONTRACT_FILE:'';
        if ($file==='' || !is_file($file)) { return null; }
        $decoded=json_decode((string)file_get_contents($file),true);
        return is_array($decoded)?$decoded:null;
    }

    private static function sections($html) {
        $out=array();
        if (preg_match_all('/<section\b([^>]*)>(.*?)<\/section>/isu',(string)$html,$matches,PREG_SET_ORDER|PREG_OFFSET_CAPTURE)) {
            foreach ($matches as $m) {
                $attrs=$m[1][0];
                $block=self::attribute('<section '.$attrs.'>','data-block');
                if ($block==='') { $block=self::attribute('<section '.$attrs.'>','data-section-id'); }
                $out[]=array('block'=>$block,'body'=>$m[2][0],'start'=>(int)$m[0][1],'end'=>(int)$m[0][1]+strlen($m[0][0]));
            }
        }
        return $out;
    }

    private static function headings($html) {
        $out=array();
        if (preg_match_all('/<h([2-3])\b[^>]*>(.*?)<\/h\1>/isu',(string)$html,$matches,PREG_SET_ORDER|PREG_OFFSET_CAPTURE)) {
            foreach ($matches as $m) {
                $out[]=array('level'=>(int)$m[1][0],'text'=>self::plain_text($m[2][0]),'start'=>(int)$m[0][1],'end'=>(int)$m[0][1]+strlen($m[0][0]));
            }
        }
        return $out;
    }

    private static function links_with_blocks($html) {
        $out=array();
        foreach (self::sections($html) as $section) {
            if (preg_match_all('/<a\b[^>]*href=("|\')(.*?)\1[^>]*>(.*?)<\/a>/isu',$section['body'],$matches,PREG_SET_ORDER)) {
                foreach ($matches as $m) {
                    $out[]=array('href'=>html_entity_decode($m[2],ENT_QUOTES|ENT_HTML5,'UTF-8'),'anchor'=>self::plain_text($m[3]),'block'=>$section['block']);
                }
            }
        }
        return $out;
    }

    private static function first_paragraph($html) {
        return preg_match('/<p\b[^>]*>(.*?)<\/p>/isu',(string)$html,$m)?self::plain_text($m[1]):'';
    }

    private static function block_body($html,$block) {
        $pattern='/<section\b[^>]*(?:data-block|data-section-id)=("|\')'.preg_quote((string)$block,'/').'\1[^>]*>(.*?)<\/section>/isu';
        return preg_match($pattern,(string)$html,$m)?$m[2]:null;
    }

    private static function token_similarity($a,$b,$stopwords) {
        $stop=array_flip(array_map(array(__CLASS__,'normalize'),$stopwords));
        $ta=self::token_set($a,$stop); $tb=self::token_set($b,$stop);
        if (!$ta || !$tb) { return 0.0; }
        $inter=count(array_intersect_key($ta,$tb));
        $union=count($ta+$tb);
        return $union>0?$inter/$union:0.0;
    }

    private static function token_set($text,$stop=array()) {
        preg_match_all('/[\p{L}\p{N}]{3,}/u',self::normalize($text),$m);
        $out=array();
        foreach ($m[0] as $token) {
            $token=(string)preg_replace('/(ern|en|er|es|e|n|s)$/u','',$token);
            if ($token!=='' && !isset($stop[$token])) { $out[$token]=true; }
        }
        return $out;
    }

    private static function visible_language_text($html) {
        $lines=array();
        if (preg_match_all('/<(h2|p|li|th|td|small)\b[^>]*>(.*?)<\/\1>/isu',(string)$html,$matches,PREG_SET_ORDER)) {
            foreach ($matches as $match) {
                $text=self::plain_text($match[2]);
                $text=(string)preg_replace('/\s+([.,;:!?])/u','$1',$text);
                if ($text!=='') { $lines[]=$text; }
            }
        }
        return implode("\n\n",$lines);
    }

    private static function plain_text($html) {
        $text=html_entity_decode((string)$html,ENT_QUOTES|ENT_HTML5,'UTF-8');
        $text=(string)preg_replace('/<[^>]+>/u',' ',$text);
        return trim((string)preg_replace('/\s+/u',' ',$text));
    }

    private static function normalize($text) {
        $text=self::plain_text((string)$text);
        $text=strtr($text,array('Ä'=>'ä','Ö'=>'ö','Ü'=>'ü','ẞ'=>'ß'));
        $text=strtolower($text);
        $text=(string)preg_replace('/[^a-z0-9äöüß]+/u',' ',$text);
        return trim((string)preg_replace('/\s+/u',' ',$text));
    }

    private static function word_count($text) {
        preg_match_all('/[\p{L}\p{N}]+(?:[\'’\-][\p{L}\p{N}]+)*/u',(string)$text,$m);
        return count($m[0]);
    }

    private static function attribute($tag,$name) {
        $name=preg_quote((string)$name,'/');
        if (preg_match('/\b'.$name.'=("|\')(.*?)\1/isu',(string)$tag,$m)) { return html_entity_decode($m[2],ENT_QUOTES|ENT_HTML5,'UTF-8'); }
        return '';
    }

    private static function basic_html_balance($html) {
        $void=array('br'=>true,'hr'=>true,'img'=>true,'input'=>true,'meta'=>true,'link'=>true,'source'=>true,'track'=>true,'wbr'=>true);
        $stack=array(); $unexpected=array();
        if (!preg_match_all('/<\/?([a-z][a-z0-9]*)\b[^>]*>/iu',(string)$html,$matches,PREG_SET_ORDER)) {
            return array('ok'=>trim((string)$html)==='','unclosed'=>array(),'unexpected_closing'=>array());
        }
        foreach ($matches as $m) {
            $tag=strtolower($m[1]); $raw=$m[0];
            if (isset($void[$tag]) || substr(rtrim($raw),-2)==='/>') { continue; }
            if (substr($raw,1,1)==='/') {
                if (!$stack || end($stack)!==$tag) { $unexpected[]=$tag; continue; }
                array_pop($stack);
            } else { $stack[]=$tag; }
        }
        return array('ok'=>!$stack&&!$unexpected,'unclosed'=>$stack,'unexpected_closing'=>$unexpected);
    }

    private static function canonical_json($value) {
        return (string)json_encode($value,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_PRESERVE_ZERO_FRACTION);
    }

    private static function error($code,$message,$field,$expected,$actual,$context,$server_state_hash) {
        return array(
            'error_code'=>$code,
            'failed_rule'=>'CONTENT_STRUCTURE_LANGUAGE_GATE_V2_FAIL_CLOSED',
            'field_path'=>$field,
            'expected'=>$expected,
            'actual'=>$actual,
            'human_message'=>$message,
            'action_context'=>$context,
            'server_state_hash'=>$server_state_hash,
            'component'=>__CLASS__,
            'source_files'=>array('includes/content-structure-language-gate.php',self::CONTRACT_FILE)
        );
    }
}
