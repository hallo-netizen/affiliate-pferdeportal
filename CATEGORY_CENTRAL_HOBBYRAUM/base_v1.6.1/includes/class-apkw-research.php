<?php
if (!defined('ABSPATH')) { exit; }

final class APKW_Research {
    public const DEFAULT_CLUSTER_LIMIT = 300;
    public const DEFAULT_GLOBAL_LIMIT = 1000;
    private const GLOBAL_RELEVANCE_REVIEW_LIMIT = 20;
    private const GLOBAL_VOLUME_REVIEW_LIMIT = 20;

    public static function preflight_draft(array $draft, bool $require_initial_review=true): array {
        $validation = APKW_Validator::validate($draft);
        $errors = $validation['errors'];
        $initial_review = APKW_Validator::validate_initial_review_gate($draft);
        if($require_initial_review && !$initial_review['valid']) foreach($initial_review['errors'] as $e) $errors[]=$e;
        if (($draft['mode'] ?? '') !== 'RESEARCH_DRAFT') {
            $errors[] = self::issue('PREFLIGHT_MODE_INVALID', 'mode', 'Für die DataForSEO-Recherche wird ein RESEARCH_DRAFT benötigt.');
        }
        $clusters = $validation['clusters'] ?? [];
        $global_seeds = self::clean_keywords($draft['project']['discovery_seed_keywords'] ?? []);
        $planned_keywords = self::planned_overview_keywords($validation['nodes'] ?? []);
        $overview_calls = $planned_keywords ? (int) ceil(count($planned_keywords) / APKW_DataForSEO::max_overview_keywords()) : 0;
        $cluster_calls = count($clusters);
        $pillar_counts = ['content'=>0,'marketplace'=>0,'magazine'=>0,'glossary'=>0];
        $content_leaf_count = 0;
        foreach (($validation['nodes'] ?? []) as $node) {
            if (!APKW_Validator::active_node($node)) { continue; }
            $b = (string) ($node['block'] ?? '');
            if (isset($pillar_counts[$b])) { $pillar_counts[$b]++; }
            if ($b === 'content' && !empty($node['is_leaf'])) { $content_leaf_count++; }
        }
        $cluster_rows=[];
        foreach ($clusters as $id=>$cluster) {
            $base_seeds = self::clean_keywords($cluster['seed_keywords'] ?? []);
            $seeds = self::cluster_research_seeds((string)$id,$cluster,$validation['nodes'] ?? []);
            if(count($seeds)>200){
                $errors[]=self::issue('CLUSTER_RESEARCH_SEED_OVERFLOW','research_clusters.'.$id.'.seed_keywords','Research-Cluster überschreitet mit kontrollierten Blatt-Primärkeywords 200 Seeds; Cluster fachlich teilen statt Seeds still zu verwerfen.');
            }
            $cluster_rows[]=['cluster_id'=>$id,'name'=>(string)($cluster['name']??''),'base_seed_count'=>count($base_seeds),'seed_count'=>count($seeds),'seed_keywords'=>$seeds,'leaf_primary_seed_count'=>max(0,count($seeds)-count($base_seeds))];
        }
        return [
            'valid'=>count($errors)===0,
            'errors'=>$errors,
            'warnings'=>$validation['warnings'] ?? [],
            'initial_sight_review_gate'=>$initial_review,
            'draft_sha256'=>self::canonical_hash($draft),
            'project_id'=>(string)($draft['project']['project_id']??''),
            'project_name'=>(string)($draft['project']['name']??''),
            'pillar_counts'=>$pillar_counts,
            'content_leaf_count'=>$content_leaf_count,
            'cluster_count'=>$cluster_calls,
            'planned_overview_keyword_count'=>count($planned_keywords),
            'planned_global_paid_calls'=>[
                'global_discovery'=>1,
                'total'=>1,
            ],
            'planned_detail_paid_calls'=>[
                'cluster_keyword_ideas'=>$cluster_calls,
                'keyword_overview'=>$overview_calls,
                'total'=>$cluster_calls+$overview_calls,
            ],
            'planned_paid_calls'=>[
                'global_discovery'=>1,
                'cluster_keyword_ideas'=>$cluster_calls,
                'keyword_overview'=>$overview_calls,
                'total'=>1+$cluster_calls+$overview_calls,
            ],
            'global_discovery_seed_count'=>count($global_seeds),
            'global_discovery_seed_keywords'=>$global_seeds,
            'clusters'=>$cluster_rows,
            'validation'=>$validation,
        ];
    }

    public static function build_global_coverage(array $draft, string $location_name, string $language_code, int $global_limit, bool $include_serp_info): array {
        self::assert_market_contract($draft,$location_name,$language_code);
        $started=gmdate('c');
        $preflight=self::preflight_draft($draft);
        if(!$preflight['valid']) throw new RuntimeException('Research-Draft ist nicht freigegeben: '.implode(', ',array_column($preflight['errors'],'code')));
        $global_limit=max(50,min(1000,$global_limit));
        $run_id=function_exists('wp_generate_uuid4')?wp_generate_uuid4():self::uuid4_fallback();
        $global_seeds=self::clean_keywords($draft['project']['discovery_seed_keywords']??[]);
        $api=APKW_DataForSEO::keyword_ideas($global_seeds,$location_name,$language_code,$global_limit,$include_serp_info,'apkw-global-'.$run_id);
        $package=[
            'format'=>'affiliate-portal-global-coverage-package',
            'schema_version'=>'1.0',
            'master_contract_id'=>APKW_MASTER_CONTRACT_ID,
            'package_id'=>'global-coverage-'.$run_id,
            'generated_at_utc'=>gmdate('c'),
            'plugin'=>['name'=>'Affiliate-Portal Kategorie-Workflow','version'=>APKW_VERSION,'content_write_capability'=>APKW_CONTENT_WRITE_CAPABILITY],
            'project'=>[
                'project_id'=>(string)($draft['project']['project_id']??''),
                'name'=>(string)($draft['project']['name']??''),
                'scope'=>(string)($draft['project']['scope']??''),
                'target_market'=>(string)($draft['project']['target_market']??''),
                'language_code'=>(string)($draft['project']['language_code']??''),
                'exclusions'=>array_values($draft['project']['exclusions']??[]),
                'discovery_seed_keywords'=>$global_seeds,
            ],
            'project_discovery_scope_sha256'=>self::project_discovery_scope_hash($draft),
            'source_draft'=>[
                'package_id'=>(string)($draft['package_id']??''),
                'content_sha256'=>$preflight['draft_sha256'],
                'package'=>$draft,
            ],
            'market'=>['location_name'=>trim($location_name),'language_code'=>trim($language_code)],
            'global_discovery'=>[
                'seed_keywords'=>$global_seeds,
                'limit'=>$global_limit,
                'request_sha256'=>$api['request_sha256'],
                'result_total_count'=>$api['result_total_count'],
                'returned_count'=>$api['returned_count'],
                'items'=>$api['normalized_items'],
                'cost_usd'=>$api['cost_usd'],
                'task_id'=>$api['task_id'],
            ],
            'provider_evidence'=>[
                'dataforseo'=>[
                    'global_keyword_ideas'=>['request'=>$api['request'],'task_id'=>$api['task_id'],'cost_usd'=>$api['cost_usd'],'raw_response'=>$api['raw_response'],'raw_response_sha256'=>$api['raw_response_sha256']],
                ],
            ],
            'coverage_review_contract'=>[
                'purpose'=>'FIND_MISSING_MAIN_TOPICS_BEFORE_CLUSTER_DEPTH',
                'selection_policy'=>'UNION_OF_TOP_PROVIDER_RELEVANCE_AND_TOP_SEARCH_VOLUME_CORE_GROUPS',
                'relevance_limit'=>self::GLOBAL_RELEVANCE_REVIEW_LIMIT,
                'volume_limit'=>self::GLOBAL_VOLUME_REVIEW_LIMIT,
                'automatic_architecture_mutation'=>false,
                'required_resolution'=>'COVERED_BY_CORRECTED_DRAFT_OR_EXPLICIT_MASTER_DECISION_BEFORE_DETAIL_RESEARCH',
            ],
            'research_summary'=>[
                'paid_calls_this_stage'=>1,
                'total_cost_usd'=>(float)$api['cost_usd'],
            ],
            'chat_handoff'=>[
                'purpose'=>'CHECK_MISSING_MAIN_TOPICS_BEFORE_EXPENSIVE_CLUSTER_DEPTH_RESEARCH',
                'next_step'=>'CHAT_MASTER_CORRECT_MAIN_TOPICS_AND_RETURN_RESEARCH_DRAFT_WITH_SAME_PROJECT_DISCOVERY_SCOPE',
            ],
            'audit_trail'=>[
                ['seq'=>1,'at_utc'=>$started,'event'=>'GLOBAL_COVERAGE_PREFLIGHT_PASS','detail'=>['draft_sha256'=>$preflight['draft_sha256'],'global_seed_count'=>count($global_seeds)]],
                ['seq'=>2,'at_utc'=>gmdate('c'),'event'=>'DATAFORSEO_GLOBAL_COVERAGE_COMPLETED','detail'=>['seed_count'=>count($global_seeds),'limit'=>$global_limit,'cost_usd'=>(float)$api['cost_usd']]],
                ['seq'=>3,'at_utc'=>gmdate('c'),'event'=>'GLOBAL_COVERAGE_PACKAGE_FINALIZED','detail'=>[]],
            ],
        ];
        $package['content_sha256']=self::canonical_hash($package);
        return $package;
    }

    public static function verify_global_coverage(array $package):array{
        $errors=[];
        if(($package['format']??'')!=='affiliate-portal-global-coverage-package')$errors[]='GLOBAL_COVERAGE_FORMAT_INVALID';
        if((string)($package['schema_version']??'')!=='1.0')$errors[]='GLOBAL_COVERAGE_SCHEMA_VERSION_INVALID';
        if((string)($package['master_contract_id']??'')!==APKW_MASTER_CONTRACT_ID)$errors[]='GLOBAL_COVERAGE_MASTER_CONTRACT_MISMATCH';
        $declared=(string)($package['content_sha256']??'');
        if(!preg_match('/^[a-f0-9]{64}$/',$declared))$errors[]='GLOBAL_COVERAGE_CONTENT_HASH_INVALID';
        $copy=$package;unset($copy['content_sha256']);$calculated=self::canonical_hash($copy);
        if($declared!==''&&!hash_equals($declared,$calculated))$errors[]='GLOBAL_COVERAGE_CONTENT_HASH_MISMATCH';
        if(!is_array($package['global_discovery']['items']??null))$errors[]='GLOBAL_COVERAGE_ITEMS_MISSING';
        $source=$package['source_draft']['package']??null;
        if(!is_array($source))$errors[]='GLOBAL_COVERAGE_SOURCE_DRAFT_MISSING';
        else {
            $source_hash=(string)($package['source_draft']['content_sha256']??'');
            if($source_hash===''||!hash_equals($source_hash,self::canonical_hash($source)))$errors[]='GLOBAL_COVERAGE_SOURCE_DRAFT_HASH_MISMATCH';
            $scope=(string)($package['project_discovery_scope_sha256']??'');
            if(!preg_match('/^[a-f0-9]{64}$/',$scope))$errors[]='GLOBAL_COVERAGE_PROJECT_SCOPE_HASH_INVALID';
            elseif(!hash_equals($scope,self::project_discovery_scope_hash($source)))$errors[]='GLOBAL_COVERAGE_PROJECT_SCOPE_HASH_MISMATCH';
            $source_project=is_array($source['project']??null)?$source['project']:[];
            $market=is_array($package['market']??null)?$package['market']:[];
            if(trim((string)($market['location_name']??''))!==trim((string)($source_project['target_market']??'')))$errors[]='GLOBAL_COVERAGE_MARKET_MISMATCH';
            if(trim((string)($market['language_code']??''))!==trim((string)($source_project['language_code']??'')))$errors[]='GLOBAL_COVERAGE_LANGUAGE_MISMATCH';
            $project=is_array($package['project']??null)?$package['project']:[];
            if(trim((string)($project['target_market']??''))!==trim((string)($source_project['target_market']??'')))$errors[]='GLOBAL_COVERAGE_PROJECT_MARKET_MISMATCH';
            if(trim((string)($project['language_code']??''))!==trim((string)($source_project['language_code']??'')))$errors[]='GLOBAL_COVERAGE_PROJECT_LANGUAGE_MISMATCH';
        }
        return ['valid'=>count($errors)===0,'errors'=>$errors,'declared_sha256'=>$declared,'calculated_sha256'=>$calculated];
    }

    public static function verify_global_binding(array $draft,array $global_package):array{
        $v=self::verify_global_coverage($global_package);$errors=$v['errors'];
        $expected_project=(string)($global_package['project']['project_id']??'');
        $actual_project=(string)($draft['project']['project_id']??'');
        if($expected_project===''||$actual_project===''||$expected_project!==$actual_project)$errors[]='GLOBAL_COVERAGE_PROJECT_MISMATCH';
        $expected_scope=(string)($global_package['project_discovery_scope_sha256']??'');
        $actual_scope=self::project_discovery_scope_hash($draft);
        if($expected_scope===''||!hash_equals($expected_scope,$actual_scope))$errors[]='GLOBAL_COVERAGE_PROJECT_SCOPE_MISMATCH';
        return ['valid'=>count($errors)===0,'errors'=>array_values(array_unique($errors)),'expected_project_id'=>$expected_project,'actual_project_id'=>$actual_project,'expected_scope_sha256'=>$expected_scope,'actual_scope_sha256'=>$actual_scope];
    }

    public static function preflight_detail(array $draft,array $global_package):array{
        $preflight=self::preflight_draft($draft,false);
        $errors=$preflight['errors'];
        $global_verification=self::verify_global_coverage($global_package);
        if(!$global_verification['valid']) foreach($global_verification['errors'] as $e)$errors[]=self::issue('GLOBAL_COVERAGE_PACKAGE_INVALID','global_coverage_package',$e);
        $global_binding=self::verify_global_binding($draft,$global_package);
        if(!$global_binding['valid']) foreach($global_binding['errors'] as $e)$errors[]=self::issue('GLOBAL_COVERAGE_BINDING_INVALID','global_coverage_package',$e);
        $global_gap_review=APKW_Validator::validate_global_gap_review_gate($draft,$global_package);
        if(!$global_gap_review['valid']) foreach($global_gap_review['errors'] as $e)$errors[]=$e;
        $gate=self::global_coverage_gate($draft,$global_package);
        foreach($gate['errors'] as $e)$errors[]=$e;
        $preflight['valid']=count($errors)===0;
        $preflight['errors']=$errors;
        $preflight['global_verification']=$global_verification;
        $preflight['global_binding']=$global_binding;
        $preflight['global_gap_sight_review_gate']=$global_gap_review;
        $preflight['global_coverage_gate']=$gate;
        return $preflight;
    }

    public static function global_coverage_gate(array $draft,array $global_package):array{
        $errors=[];$warnings=[];
        $items=is_array($global_package['global_discovery']['items']??null)?$global_package['global_discovery']['items']:[];
        $groups=self::global_review_groups($items);
        $decisions=[];
        foreach(is_array($draft['global_coverage_decisions']??null)?$draft['global_coverage_decisions']:[] as $d){
            if(!is_array($d))continue;$core=self::key((string)($d['core_keyword']??''));if($core!=='')$decisions[$core]=$d;
        }
        $coverage=self::draft_global_coverage($draft,$items);
        $rows=[];
        foreach($groups as $g){
            $core=$g['core_keyword'];$decision=$decisions[$core]??null;$covered=$coverage[$core]??[];
            $decision_code=is_array($decision)?(string)($decision['decision']??''):'';
            if($decision_code==='DEFERRED')$status='DEFERRED_BLOCKED';
            elseif(is_array($decision))$status='DECIDED';
            else $status='UNRESOLVED';
            $rows[]=$g+['status'=>$status,'covered_by'=>$covered,'decision'=>$decision];
            if($status==='UNRESOLVED')$errors[]=self::issue('GLOBAL_COVERAGE_CORE_UNRESOLVED','global_coverage_decisions.'.$core,'Projektweiter relevanter Keyword-Core benötigt auch bei Keyword-Ähnlichkeit eine ausdrückliche fachliche Entscheidung: '.$g['top_keyword']);
            if($status==='DEFERRED_BLOCKED')$errors[]=self::issue('GLOBAL_COVERAGE_CORE_DEFERRED_BLOCKS_DETAIL','global_coverage_decisions.'.$core,'DEFERRED ist kein abgeschlossener Coverage-Befund. Vor Detailresearch muss der Core eingearbeitet oder ausdrücklich OUT_OF_SCOPE/ARTICLE_ONLY entschieden werden: '.$g['top_keyword']);
        }
        if(!$groups)$errors[]=self::issue('GLOBAL_COVERAGE_NO_REVIEW_GROUPS','global_coverage_package','DataForSEO lieferte keine auswertbaren globalen Keywordgruppen; ohne belastbare Coverage-Evidenz darf die Detailrecherche nicht starten.');
        return [
            'valid'=>count($errors)===0,
            'errors'=>$errors,
            'warnings'=>$warnings,
            'review_groups'=>$rows,
            'selection_policy'=>'UNION_OF_TOP_PROVIDER_RELEVANCE_AND_TOP_SEARCH_VOLUME_CORE_GROUPS',
            'relevance_limit'=>self::GLOBAL_RELEVANCE_REVIEW_LIMIT,
            'volume_limit'=>self::GLOBAL_VOLUME_REVIEW_LIMIT,
        ];
    }

    public static function build_from_draft(array $draft, array $global_package, string $location_name, string $language_code, int $cluster_limit, bool $include_serp_info): array {
        self::assert_market_contract($draft,$location_name,$language_code);
        $started=gmdate('c');
        $preflight=self::preflight_detail($draft,$global_package);
        if(!$preflight['valid']) throw new RuntimeException('Detail-Research ist nicht freigegeben: '.implode(', ',array_column($preflight['errors'],'code')));
        $global_binding=$preflight['global_binding'];
        $cluster_limit=max(10,min(1000,$cluster_limit));
        $run_id=function_exists('wp_generate_uuid4')?wp_generate_uuid4():self::uuid4_fallback();
        $inventory=APKW_Inventory::snapshot();
        $nodes=$preflight['validation']['nodes'];
        $clusters=$preflight['validation']['clusters'];
        $global_discovery=$global_package['global_discovery'];
        $provider_global=$global_package['provider_evidence']['dataforseo']['global_keyword_ideas']??[];
        $global_cost=(float)($global_package['research_summary']['total_cost_usd']??$global_discovery['cost_usd']??0);

        $overview_keywords=self::planned_overview_keywords($nodes);
        $overview_runs=[];$overview_items=[];$provider_overview=[];$overview_cost=0.0;
        foreach(array_chunk($overview_keywords,APKW_DataForSEO::max_overview_keywords()) as $chunk_index=>$chunk){
            if(!$chunk)continue;
            $api=APKW_DataForSEO::keyword_overview($chunk,$location_name,$language_code,$include_serp_info,'apkw-overview-'.$run_id.'-'.$chunk_index);
            $overview_cost+=(float)$api['cost_usd'];
            foreach($api['normalized_items'] as $item)$overview_items[]=$item;
            $overview_runs[]=['chunk'=>$chunk_index+1,'keyword_count'=>count($chunk),'request_sha256'=>$api['request_sha256'],'returned_count'=>$api['returned_count'],'cost_usd'=>$api['cost_usd'],'task_id'=>$api['task_id']];
            $provider_overview[]=['chunk'=>$chunk_index+1,'request'=>$api['request'],'task_id'=>$api['task_id'],'cost_usd'=>$api['cost_usd'],'raw_response'=>$api['raw_response'],'raw_response_sha256'=>$api['raw_response_sha256']];
        }

        $cluster_research=[];$provider_clusters=[];$cluster_cost=0.0;
        foreach($clusters as $cluster_id=>$cluster){
            $seeds=self::cluster_research_seeds((string)$cluster_id,$cluster,$nodes);
            if(count($seeds)>200) throw new RuntimeException('Detail-Research blockiert: CLUSTER_RESEARCH_SEED_OVERFLOW '.$cluster_id);
            $api=APKW_DataForSEO::keyword_ideas($seeds,$location_name,$language_code,$cluster_limit,$include_serp_info,'apkw-cluster-'.$run_id.'-'.$cluster_id);
            $cluster_cost+=(float)$api['cost_usd'];
            $cluster_research[]=[
                'cluster_id'=>$cluster_id,'name'=>(string)$cluster['name'],'scope'=>(string)$cluster['scope'],'exclusions'=>array_values($cluster['exclusions']??[]),'seed_keywords'=>$seeds,
                'request_sha256'=>$api['request_sha256'],'result_total_count'=>$api['result_total_count'],'returned_count'=>$api['returned_count'],'items'=>$api['normalized_items'],'cost_usd'=>$api['cost_usd'],'task_id'=>$api['task_id'],
            ];
            $provider_clusters[]=['cluster_id'=>$cluster_id,'request'=>$api['request'],'task_id'=>$api['task_id'],'cost_usd'=>$api['cost_usd'],'raw_response'=>$api['raw_response'],'raw_response_sha256'=>$api['raw_response_sha256']];
        }

        $detail_calls=count($cluster_research)+count($overview_runs);
        $package=[
            'format'=>'affiliate-portal-research-package','schema_version'=>APKW_RESEARCH_SCHEMA_VERSION,'master_contract_id'=>APKW_MASTER_CONTRACT_ID,'package_id'=>'research-'.$run_id,'generated_at_utc'=>gmdate('c'),
            'plugin'=>['name'=>'Affiliate-Portal Kategorie-Workflow','version'=>APKW_VERSION,'content_write_capability'=>APKW_CONTENT_WRITE_CAPABILITY],
            'source_draft'=>['package_id'=>(string)$draft['package_id'],'content_sha256'=>$preflight['draft_sha256'],'research_scope_sha256'=>self::research_scope_hash($draft),'package'=>$draft],
            'project'=>$draft['project'],'market'=>['location_name'=>trim($location_name),'language_code'=>trim($language_code)],
            'workflow_contract'=>[
                'architecture_owner'=>'CHAT_WITH_BINDING_MASTER','research_scope'=>'TWO_STAGE_GLOBAL_COVERAGE_THEN_DECLARED_CLUSTER_DEPTH','core_pillars'=>['content','marketplace','magazine'],'glossary_role'=>'OPTIONAL_AUXILIARY_NOT_CORE_PILLAR',
                'exact_visible_name_duplicate_policy'=>'BLOCK_GLOBAL','same_primary_within_pillar'=>'BLOCK','cross_pillar_overlap'=>'SIMILAR_TOPIC_ALLOWED_WITH_DISTINCT_FUNCTIONAL_INTENT_AND_JUSTIFICATION; EXACT_VISIBLE_NAME_BLOCKED','semantic_overlap'=>'REVIEW_NOT_AUTO_MERGE',
                'global_topic_coverage'=>'GLOBAL_STAGE_BEFORE_CLUSTER_DEPTH; RELEVANCE_PLUS_VOLUME_REVIEW_GROUPS_REQUIRE_EXPLICIT_MASTER_DECISION_BEFORE_DETAIL_RESEARCH','category_naming'=>'CHECK_EXACT_METRICS_AND_STRONGER_SAME_CORE_CANDIDATES','missing_keyword_groups'=>'TOP_RELEVANCE_PLUS_VOLUME_CORE_GROUPS_REQUIRE_OWNER_OR_DECISION','longtails'=>'AT_LEAST_3_REAL_NODE_BOUND_DATAFORSEO_QUERIES_REQUIRED_FOR_FINAL_CONTENT_LEAVES; FUNCTIONAL_CONTENT_CATEGORIES_USE_SAME_GATE','search_volume'=>'SIGNAL_NOT_SOLE_DECISION','wordpress_content_writes'=>'BLOCKED','hivepress_content_writes'=>'BLOCKED',
            ],
            'existing_inventory'=>$inventory,
            'research_provider'=>['id'=>'dataforseo','adapter'=>'APKW_DataForSEO','adapter_version'=>'1.5','keyword_ideas_endpoint'=>'https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live','keyword_overview_endpoint'=>'https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_overview/live'],
            'global_coverage_binding'=>['package_id'=>(string)$global_package['package_id'],'content_sha256'=>(string)$global_package['content_sha256'],'project_discovery_scope_sha256'=>(string)$global_package['project_discovery_scope_sha256']],
            'global_coverage_package'=>$global_package,
            'global_discovery'=>$global_discovery,
            'planned_keyword_overview'=>['keyword_count'=>count($overview_keywords),'runs'=>$overview_runs,'items'=>self::dedupe_items($overview_items)],
            'cluster_research'=>['cluster_count'=>count($cluster_research),'limit_per_cluster'=>$cluster_limit,'clusters'=>$cluster_research],
            'research_summary'=>[
                'paid_calls_this_stage'=>$detail_calls,'paid_calls_total_workflow'=>1+$detail_calls,'global_discovery_calls_this_stage'=>0,'global_discovery_calls_total_workflow'=>1,'cluster_keyword_ideas_calls'=>count($cluster_research),'keyword_overview_calls'=>count($overview_runs),
                'detail_cost_usd'=>$cluster_cost+$overview_cost,'global_cost_usd'=>$global_cost,'total_workflow_cost_usd'=>$global_cost+$cluster_cost+$overview_cost,'provider_reported_cluster_cost_usd'=>$cluster_cost,'provider_reported_overview_cost_usd'=>$overview_cost,
            ],
            'provider_evidence'=>['dataforseo'=>['global_keyword_ideas'=>$provider_global,'keyword_overview'=>$provider_overview,'cluster_keyword_ideas'=>$provider_clusters]],
            'chat_handoff'=>['master_required'=>'ALLGEMEINGUELTIGER_KATEGORIE_MASTER_016_WORKFLOW_HARDLOCK.zip','expected_return_format'=>'affiliate-portal-category-package','expected_return_schema'=>APKW_CATEGORY_SCHEMA_VERSION,'expected_return_mode'=>'READ_ONLY_PREVIEW'],
            'audit_trail'=>[
                ['seq'=>1,'at_utc'=>$started,'event'=>'DETAIL_RESEARCH_DRAFT_PREFLIGHT_PASS','detail'=>['draft_sha256'=>$preflight['draft_sha256'],'planned_detail_paid_calls'=>$preflight['planned_detail_paid_calls'],'global_review_groups'=>count($preflight['global_coverage_gate']['review_groups']??[])]],
                ['seq'=>2,'at_utc'=>gmdate('c'),'event'=>'GLOBAL_COVERAGE_PACKAGE_BOUND_AND_REUSED','detail'=>['package_id'=>(string)$global_package['package_id'],'content_sha256'=>(string)$global_package['content_sha256']]],
                ['seq'=>3,'at_utc'=>$inventory['captured_at_utc'],'event'=>'INVENTORY_SNAPSHOT_CREATED','detail'=>['object_count'=>$inventory['object_count']]],
                ['seq'=>4,'at_utc'=>gmdate('c'),'event'=>'DATAFORSEO_EXACT_KEYWORD_OVERVIEW_COMPLETED','detail'=>['runs'=>count($overview_runs),'keyword_count'=>count($overview_keywords)]],
                ['seq'=>5,'at_utc'=>gmdate('c'),'event'=>'DATAFORSEO_BOUNDED_CLUSTER_RESEARCH_COMPLETED','detail'=>['clusters'=>count($cluster_research),'limit_per_cluster'=>$cluster_limit]],
                ['seq'=>6,'at_utc'=>gmdate('c'),'event'=>'RESEARCH_PACKAGE_FINALIZED','detail'=>['detail_cost_usd'=>$cluster_cost+$overview_cost,'total_workflow_cost_usd'=>$global_cost+$cluster_cost+$overview_cost]],
            ],
        ];
        $package['content_sha256']=self::canonical_hash($package);
        return $package;
    }

    public static function verify_package(array $package):array{
        $errors=[];
        if(($package['format']??'')!=='affiliate-portal-research-package')$errors[]='RESEARCH_FORMAT_INVALID';
        if((string)($package['schema_version']??'')!==APKW_RESEARCH_SCHEMA_VERSION)$errors[]='RESEARCH_SCHEMA_VERSION_INVALID';
        if((string)($package['master_contract_id']??'')!==APKW_MASTER_CONTRACT_ID)$errors[]='RESEARCH_MASTER_CONTRACT_MISMATCH';
        $declared=(string)($package['content_sha256']??'');
        if(!preg_match('/^[a-f0-9]{64}$/',$declared))$errors[]='RESEARCH_CONTENT_HASH_INVALID';
        $copy=$package;unset($copy['content_sha256']);$calculated=self::canonical_hash($copy);
        if($declared!==''&&!hash_equals($declared,$calculated))$errors[]='RESEARCH_CONTENT_HASH_MISMATCH';
        $site=(string)($package['existing_inventory']['site_url']??'');
        if($site!==''&&rtrim($site,'/')!==rtrim((string)home_url('/'),'/'))$errors[]='RESEARCH_SITE_MISMATCH';
        if(!is_array($package['global_discovery']??null)||!is_array($package['global_discovery']['items']??null))$errors[]='RESEARCH_GLOBAL_DISCOVERY_MISSING';
        $global_package=$package['global_coverage_package']??null;
        if(!is_array($global_package))$errors[]='RESEARCH_GLOBAL_COVERAGE_PACKAGE_MISSING';
        else {
            $gv=self::verify_global_coverage($global_package);
            if(!$gv['valid'])foreach($gv['errors'] as $e)$errors[]='RESEARCH_EMBEDDED_'.$e;
            $binding=$package['global_coverage_binding']??[];
            if((string)($binding['package_id']??'')!==(string)($global_package['package_id']??''))$errors[]='RESEARCH_GLOBAL_COVERAGE_BINDING_ID_MISMATCH';
            if((string)($binding['content_sha256']??'')!==(string)($global_package['content_sha256']??''))$errors[]='RESEARCH_GLOBAL_COVERAGE_BINDING_HASH_MISMATCH';
        }
        $source=$package['source_draft']??null;
        if(!is_array($source)||!is_array($source['package']??null))$errors[]='RESEARCH_SOURCE_DRAFT_MISSING';
        else {
            $source_hash=(string)($source['content_sha256']??'');
            if($source_hash===''||!hash_equals($source_hash,self::canonical_hash($source['package'])))$errors[]='RESEARCH_SOURCE_DRAFT_HASH_MISMATCH';
            $scope_hash=(string)($source['research_scope_sha256']??'');
            if(!preg_match('/^[a-f0-9]{64}$/',$scope_hash))$errors[]='RESEARCH_SCOPE_HASH_INVALID';
            elseif(!hash_equals($scope_hash,self::research_scope_hash($source['package'])))$errors[]='RESEARCH_SCOPE_HASH_MISMATCH';
            $source_project=is_array($source['package']['project']??null)?$source['package']['project']:[];
            $market=is_array($package['market']??null)?$package['market']:[];
            if(trim((string)($market['location_name']??''))!==trim((string)($source_project['target_market']??'')))$errors[]='RESEARCH_MARKET_MISMATCH';
            if(trim((string)($market['language_code']??''))!==trim((string)($source_project['language_code']??'')))$errors[]='RESEARCH_LANGUAGE_MISMATCH';
        }
        return ['valid'=>count($errors)===0,'errors'=>$errors,'declared_sha256'=>$declared,'calculated_sha256'=>$calculated];
    }

    public static function verify_binding(array $category_package,array $research_package):array{
        $binding=is_array($category_package['research_binding']??null)?$category_package['research_binding']:[];
        $errors=[];
        $expected_id=(string)($research_package['package_id']??'');$expected_hash=(string)($research_package['content_sha256']??'');
        if((string)($binding['package_id']??'')!==$expected_id)$errors[]='RESEARCH_BINDING_PACKAGE_ID_MISMATCH';
        if((string)($binding['content_sha256']??'')!==$expected_hash)$errors[]='RESEARCH_BINDING_HASH_MISMATCH';
        $project_id=(string)($category_package['project']['project_id']??'');$research_project=(string)($research_package['project']['project_id']??'');
        if($project_id===''||$research_project===''||$project_id!==$research_project)$errors[]='RESEARCH_BINDING_PROJECT_MISMATCH';
        $expected_scope=(string)($research_package['source_draft']['research_scope_sha256']??'');
        $actual_scope=self::research_scope_hash($category_package);
        if($expected_scope===''||!hash_equals($expected_scope,$actual_scope))$errors[]='RESEARCH_BINDING_SCOPE_MISMATCH';
        return ['valid'=>count($errors)===0,'errors'=>$errors,'expected'=>['package_id'=>$expected_id,'content_sha256'=>$expected_hash,'project_id'=>$research_project,'research_scope_sha256'=>$expected_scope],'actual'=>['package_id'=>(string)($binding['package_id']??''),'content_sha256'=>(string)($binding['content_sha256']??''),'project_id'=>$project_id,'research_scope_sha256'=>$actual_scope]];
    }

    private static function assert_market_contract(array $package,string $location_name,string $language_code):void{
        $project=is_array($package['project']??null)?$package['project']:[];
        if(trim((string)($project['target_market']??''))!==trim($location_name) || trim((string)($project['language_code']??''))!==trim($language_code)){
            throw new RuntimeException('DataForSEO-Marktparameter weichen vom hashgebundenen PROJECT CONTRACT ab. Erneute Sichtfreigabe erforderlich.');
        }
    }

    public static function project_discovery_scope_hash(array $package):string{
        $project=is_array($package['project']??null)?$package['project']:[];
        $scope=['master_contract_id'=>(string)($package['master_contract_id']??''),'project_id'=>(string)($project['project_id']??''),'project_scope'=>trim((string)($project['scope']??'')),'target_market'=>trim((string)($project['target_market']??'')),'language_code'=>trim((string)($project['language_code']??'')),'project_exclusions'=>self::normalized_string_set($project['exclusions']??[]),'discovery_seed_keywords'=>self::normalized_string_set($project['discovery_seed_keywords']??[])];
        $json=wp_json_encode($scope,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
        return hash('sha256',(string)$json);
    }

    public static function research_scope_hash(array $package):string{
        $project=is_array($package['project']??null)?$package['project']:[];
        $scope=['master_contract_id'=>(string)($package['master_contract_id']??''),'project_id'=>(string)($project['project_id']??''),'project_scope'=>trim((string)($project['scope']??'')),'target_market'=>trim((string)($project['target_market']??'')),'language_code'=>trim((string)($project['language_code']??'')),'project_exclusions'=>self::normalized_string_set($project['exclusions']??[]),'discovery_seed_keywords'=>self::normalized_string_set($project['discovery_seed_keywords']??[]),'clusters'=>[]];
        foreach(is_array($package['research_clusters']??null)?$package['research_clusters']:[] as $cluster){
            if(!is_array($cluster))continue;$id=trim((string)($cluster['cluster_id']??''));if($id==='')continue;
            $scope['clusters'][$id]=['scope'=>trim((string)($cluster['scope']??'')),'exclusions'=>self::normalized_string_set($cluster['exclusions']??[]),'seed_keywords'=>self::normalized_string_set($cluster['seed_keywords']??[])];
        }
        ksort($scope['clusters'],SORT_STRING);
        $json=wp_json_encode($scope,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
        return hash('sha256',(string)$json);
    }

    public static function canonical_hash(array $package):string{
        $copy=$package; unset($copy['content_sha256']);
        $json=wp_json_encode($copy,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
        return hash('sha256',(string)$json);
    }

    private static function draft_global_coverage(array $draft,array $global_items):array{
        $keyword_to_core=[];
        foreach($global_items as $item){
            if(!is_array($item))continue;
            $core=self::core_key($item);$keyword=self::key((string)($item['keyword']??''));
            if($core==='')continue;
            $keyword_to_core[$core]=$core;
            if($keyword!=='')$keyword_to_core[$keyword]=$core;
        }
        $covered=[];
        $claim=static function(string $value,string $source) use (&$covered,$keyword_to_core):void{
            $key=self::key($value);
            if($key==='')return;
            $core=$keyword_to_core[$key]??null;
            if($core===null)return;
            $covered[$core][]=$source;
        };
        foreach(is_array($draft['research_clusters']??null)?$draft['research_clusters']:[] as $cluster){
            if(!is_array($cluster))continue;$cid=(string)($cluster['cluster_id']??'');
            $claim((string)($cluster['name']??''),'cluster_name:'.$cid);
            foreach(is_array($cluster['seed_keywords']??null)?$cluster['seed_keywords']:[] as $seed)$claim((string)$seed,'cluster_seed:'.$cid);
        }
        foreach(is_array($draft['nodes']??null)?$draft['nodes']:[] as $node){
            if(!is_array($node)||!APKW_Validator::active_node($node))continue;$id=(string)($node['concept_id']??'');
            $claim((string)($node['primary_keyword']??''),'node_primary:'.$id);
            $claim((string)($node['name']??''),'node_name:'.$id);
        }
        foreach($covered as &$sources){$sources=array_values(array_unique($sources));sort($sources,SORT_STRING);}unset($sources);
        return $covered;
    }


    private static function global_review_groups(array $items):array{
        $groups=[];
        foreach($items as $position=>$item){
            if(!is_array($item))continue;
            $core=self::core_key($item);if($core==='')continue;
            $rank=isset($item['provider_rank'])&&is_numeric($item['provider_rank'])?(int)$item['provider_rank']:(int)$position+1;
            $vol=isset($item['search_volume'])&&is_numeric($item['search_volume'])?(int)$item['search_volume']:0;
            if(!isset($groups[$core]))$groups[$core]=['core_keyword'=>$core,'top_keyword'=>(string)($item['keyword']??$core),'max_search_volume'=>$vol,'search_volume_sum'=>$vol,'min_provider_rank'=>$rank,'keyword_count'=>1,'top_intent'=>$item['main_intent']??null,'selected_by'=>[]];
            else{
                $groups[$core]['search_volume_sum']+=$vol;$groups[$core]['keyword_count']++;
                if($rank<$groups[$core]['min_provider_rank'])$groups[$core]['min_provider_rank']=$rank;
                if($vol>$groups[$core]['max_search_volume']){$groups[$core]['max_search_volume']=$vol;$groups[$core]['top_keyword']=(string)($item['keyword']??$core);$groups[$core]['top_intent']=$item['main_intent']??null;}
            }
        }
        $rel=array_values($groups);usort($rel,static fn($a,$b)=>($a['min_provider_rank']<=>$b['min_provider_rank'])?:($b['max_search_volume']<=>$a['max_search_volume'])?:strcmp($a['core_keyword'],$b['core_keyword']));
        $vol=array_values(array_filter($groups,static fn($g)=>(int)($g['max_search_volume']??0)>0));usort($vol,static fn($a,$b)=>($b['max_search_volume']<=>$a['max_search_volume'])?:($a['min_provider_rank']<=>$b['min_provider_rank'])?:strcmp($a['core_keyword'],$b['core_keyword']));
        $selected=[];
        foreach(array_slice($rel,0,self::GLOBAL_RELEVANCE_REVIEW_LIMIT) as $g){$g['selected_by'][]='PROVIDER_RELEVANCE';$selected[$g['core_keyword']]=$g;}
        foreach(array_slice($vol,0,self::GLOBAL_VOLUME_REVIEW_LIMIT) as $g){if(isset($selected[$g['core_keyword']]))$selected[$g['core_keyword']]['selected_by'][]='SEARCH_VOLUME';else{$g['selected_by'][]='SEARCH_VOLUME';$selected[$g['core_keyword']]=$g;}}
        $out=array_values($selected);usort($out,static fn($a,$b)=>($a['min_provider_rank']<=>$b['min_provider_rank'])?:($b['max_search_volume']<=>$a['max_search_volume'])?:strcmp($a['core_keyword'],$b['core_keyword']));
        return $out;
    }

    private static function core_key(array $item):string{
        $core=self::key((string)($item['core_keyword']??''));
        return $core!==''?$core:self::key((string)($item['keyword']??''));
    }


    private static function cluster_research_seeds(string $cluster_id,array $cluster,array $nodes):array{
        $all=self::clean_keywords($cluster['seed_keywords']??[]);
        $seen=[];$out=[];
        foreach($all as $kw){$k=self::key($kw);if($k!==''&&!isset($seen[$k])){$seen[$k]=true;$out[]=$kw;}}
        foreach($nodes as $node){
            if(!APKW_Validator::active_node($node))continue;
            if((string)($node['block']??'')!=='content')continue;
            if((string)($node['research_cluster_id']??'')!==$cluster_id)continue;
            if(empty($node['is_leaf']))continue;
            $kw=preg_replace('/\s+/u',' ',trim((string)($node['primary_keyword']??'')));
            if($kw==='')continue;$k=self::key($kw);
            if(!isset($seen[$k])){$seen[$k]=true;$out[]=$kw;}
        }
        return $out;
    }

    private static function planned_overview_keywords(array $nodes):array{
        $keywords=[];
        foreach($nodes as $node){
            if(!APKW_Validator::active_node($node))continue;
            foreach([(string)($node['primary_keyword']??''),(string)($node['name']??'')] as $kw){$kw=preg_replace('/\s+/u',' ',trim($kw));if($kw==='')continue;$keywords[self::key($kw)]=$kw;}
        }
        return array_values($keywords);
    }
    private static function clean_keywords(array $keywords):array{$out=[];foreach($keywords as $kw){$kw=preg_replace('/\s+/u',' ',trim((string)$kw));if($kw==='')continue;$out[self::key($kw)]=$kw;}return array_values($out);}
    private static function dedupe_items(array $items):array{$out=[];foreach($items as $item){if(!is_array($item))continue;$k=self::key((string)($item['keyword']??''));if($k!==''&&!isset($out[$k]))$out[$k]=$item;}return array_values($out);}
    private static function normalized_string_set($values):array{if(!is_array($values))return [];$out=[];foreach($values as $v){$v=preg_replace('/\s+/u',' ',trim((string)$v));if($v==='')continue;$k=self::key($v);$out[$k]=$k;}ksort($out,SORT_STRING);return array_values($out);}
    private static function key(string $v):string{$v=html_entity_decode($v,ENT_QUOTES|ENT_HTML5,'UTF-8');$v=preg_replace('/\s+/u',' ',trim($v));return function_exists('mb_strtolower')?mb_strtolower((string)$v,'UTF-8'):strtolower((string)$v);}
    private static function issue(string $code,string $path,string $message):array{return ['code'=>$code,'path'=>$path,'message'=>$message];}
    private static function uuid4_fallback():string{$data=random_bytes(16);$data[6]=chr((ord($data[6])&0x0f)|0x40);$data[8]=chr((ord($data[8])&0x3f)|0x80);return vsprintf('%s%s-%s-%s-%s-%s%s%s',str_split(bin2hex($data),4));}
}
