<?php
if (!defined('ABSPATH')) { exit; }

final class APKW_Validator {
    private const ALLOWED_BLOCKS = ['content','marketplace','magazine','glossary'];
    private const CORE_BLOCKS = ['content','marketplace','magazine'];
    private const PILLAR_ROLE_BY_BLOCK = [
        'content'=>'CONTENT_EVERGREEN',
        'marketplace'=>'MARKETPLACE_TRANSACTIONAL',
        'magazine'=>'JOURNAL_EDITORIAL',
        'glossary'=>'GLOSSARY_REFERENCE',
    ];
    private const ALLOWED_STATUSES = ['SOURCE_CONFIRMED','PROPOSED','APPROVED','BLOCKED','DEPRECATED','REJECTED'];
    private const ACTIVE_STATUSES = ['SOURCE_CONFIRMED','PROPOSED','APPROVED'];
    private const ALLOWED_MODES = ['RESEARCH_DRAFT','READ_ONLY_PREVIEW','FINAL_APPROVED'];
    private const ALLOWED_ADAPTERS = ['wordpress_page','wordpress_taxonomy'];
    private const MAX_NODES = 10000;
    private const MAX_CLUSTERS = 100;

    public static function validate(array $package): array {
        $errors=[]; $warnings=[]; $nodes=[]; $index=[];
        self::require_string($package,'format',$errors,'PACKAGE_FORMAT_MISSING');
        self::require_string($package,'schema_version',$errors,'SCHEMA_VERSION_MISSING');
        self::require_string($package,'package_id',$errors,'PACKAGE_ID_MISSING');
        if (($package['format']??'') !== 'affiliate-portal-category-package') $errors[]=self::issue('PACKAGE_FORMAT_UNSUPPORTED','format','Erwartet wird affiliate-portal-category-package.');
        $schema=(string)($package['schema_version']??'');
        if ($schema !== APKW_CATEGORY_SCHEMA_VERSION) $errors[]=self::issue('SCHEMA_VERSION_UNSUPPORTED','schema_version','Erwartet wird Schema '.APKW_CATEGORY_SCHEMA_VERSION.'.');
        self::require_string($package,'master_contract_id',$errors,'MASTER_CONTRACT_ID_MISSING');
        if ((string)($package['master_contract_id']??'') !== APKW_MASTER_CONTRACT_ID) $errors[]=self::issue('MASTER_CONTRACT_ID_MISMATCH','master_contract_id','Paket gehört nicht zum verbindlichen Master-016-HARDLOCK-Vertrag.');
        if (!isset($package['package_version']) || !is_int($package['package_version']) || $package['package_version']<1) $errors[]=self::issue('PACKAGE_VERSION_INVALID','package_version','package_version muss eine positive Ganzzahl sein.');
        $mode=(string)($package['mode']??'');
        if (!in_array($mode,self::ALLOWED_MODES,true)) $errors[]=self::issue('MODE_INVALID','mode','Zulässig sind RESEARCH_DRAFT, READ_ONLY_PREVIEW und FINAL_APPROVED.');
        if (in_array($mode,['READ_ONLY_PREVIEW','FINAL_APPROVED'],true)) self::validate_research_binding($package,$errors);
        if ($mode==='FINAL_APPROVED') self::validate_human_sight_review($package,$errors);
        self::validate_project($package,$errors,$warnings);
        $clusters=self::validate_clusters($package,$errors,$warnings);
        if (!isset($package['nodes']) || !is_array($package['nodes'])) {
            $errors[]=self::issue('NODES_MISSING','nodes','nodes muss ein Array sein.');
            return self::result($errors,$warnings,[],[],[], $clusters);
        }
        if (count($package['nodes'])>self::MAX_NODES) $errors[]=self::issue('NODE_LIMIT_EXCEEDED','nodes','Maximal 10.000 Knoten pro Paket.');
        self::validate_source_binding($package,$errors,$warnings);

        foreach($package['nodes'] as $position=>$raw){
            $path='nodes['.$position.']';
            if(!is_array($raw)){ $errors[]=self::issue('NODE_NOT_OBJECT',$path,'Knoten muss ein Objekt sein.'); continue; }
            $before=count($errors);
            foreach(['concept_id','block','name','slug','status','primary_keyword','search_intent','intent_key','scope','pillar_role'] as $field){
                self::require_string($raw,$field,$errors,'NODE_FIELD_MISSING',$path.'.'.$field);
            }
            if(!array_key_exists('keyword_owner',$raw)||!is_bool($raw['keyword_owner'])) $errors[]=self::issue('KEYWORD_OWNER_INVALID',$path.'.keyword_owner','keyword_owner muss boolesch sein.');
            if(!isset($raw['exclusions'])||!is_array($raw['exclusions'])) $errors[]=self::issue('EXCLUSIONS_INVALID',$path.'.exclusions','exclusions muss ein Array sein.');
            if(!isset($raw['longtail_potential'])||!is_array($raw['longtail_potential'])) $errors[]=self::issue('LONGTAILS_INVALID',$path.'.longtail_potential','longtail_potential muss ein Array sein.');
            if(!array_key_exists('is_leaf',$raw)||!is_bool($raw['is_leaf'])) $errors[]=self::issue('IS_LEAF_INVALID',$path.'.is_leaf','is_leaf muss boolesch sein.');
            if(!isset($raw['level'])||!is_int($raw['level'])||$raw['level']<1||$raw['level']>20) $errors[]=self::issue('NODE_LEVEL_INVALID',$path.'.level','level muss eine Ganzzahl zwischen 1 und 20 sein.');
            foreach(['overlap_justification','keyword_choice_justification','category_name_justification','intent_justification','hierarchy_justification','single_child_justification','title_length_justification'] as $optional_text){
                if(isset($raw[$optional_text])&&!is_string($raw[$optional_text])) $errors[]=self::issue('NODE_OPTIONAL_TEXT_INVALID',$path.'.'.$optional_text,$optional_text.' muss Text sein.');
            }

            $concept_id=trim((string)($raw['concept_id']??''));
            if($concept_id!==''&&!preg_match('/^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$/',$concept_id)) $errors[]=self::issue('CONCEPT_ID_INVALID',$path.'.concept_id','concept_id enthält unzulässige Zeichen oder Länge.');
            if($concept_id!==''&&isset($index[$concept_id])) $errors[]=self::issue('CONCEPT_ID_DUPLICATE',$path.'.concept_id','concept_id ist mehrfach vorhanden.');
            $block=(string)($raw['block']??'');
            if(!in_array($block,self::ALLOWED_BLOCKS,true)) $errors[]=self::issue('BLOCK_INVALID',$path.'.block','Unzulässiger Portalblock.');
            if(!in_array(($raw['status']??''),self::ALLOWED_STATUSES,true)) $errors[]=self::issue('STATUS_INVALID',$path.'.status','Unzulässiger Status.');
            if(isset(self::PILLAR_ROLE_BY_BLOCK[$block]) && (string)($raw['pillar_role']??'')!==self::PILLAR_ROLE_BY_BLOCK[$block]) $errors[]=self::issue('PILLAR_ROLE_MISMATCH',$path.'.pillar_role','pillar_role passt nicht zum Block.');
            if(in_array($block,self::CORE_BLOCKS,true)){
                $cluster_id=trim((string)($raw['research_cluster_id']??''));
                if($cluster_id==='') $errors[]=self::issue('RESEARCH_CLUSTER_ID_MISSING',$path.'.research_cluster_id','Kern-Säulen benötigen research_cluster_id.');
                elseif(!isset($clusters[$cluster_id])) $errors[]=self::issue('RESEARCH_CLUSTER_UNKNOWN',$path.'.research_cluster_id','research_cluster_id ist nicht definiert.');
            }
            $name=trim((string)($raw['name']??'')); $name_len=self::length($name);
            if((int)($raw['level']??0)===1&&$name_len>24&&trim((string)($raw['title_length_justification']??''))==='') $errors[]=self::issue('ROOT_TITLE_TOO_LONG',$path.'.name','Haupttitel >24 Zeichen benötigt Begründung.');
            if((int)($raw['level']??0)>1&&$name_len>40&&trim((string)($raw['title_length_justification']??''))==='') $errors[]=self::issue('LOWER_TITLE_TOO_LONG',$path.'.name','Untertitel >40 Zeichen benötigt Begründung.');
            $slug=(string)($raw['slug']??'');
            if($slug!==''&&sanitize_title($slug)!==$slug) $errors[]=self::issue('SLUG_NOT_CANONICAL',$path.'.slug','Slug ist nicht kanonisch.');
            $parent=$raw['parent_concept_id']??null;
            if($parent!==null&&!is_string($parent)) $errors[]=self::issue('PARENT_ID_INVALID',$path.'.parent_concept_id','parent_concept_id muss String oder null sein.');
            if($parent!==null&&$parent===$concept_id) $errors[]=self::issue('SELF_PARENT',$path.'.parent_concept_id','Knoten darf nicht sein eigener Elternknoten sein.');
            self::validate_target($raw,$path,$errors);
            if(count($errors)===$before&&$concept_id!==''){ $nodes[]=$raw; $index[$concept_id]=$raw; }
        }

        self::validate_three_pillars($nodes,$errors);
        foreach($nodes as $node) self::validate_hierarchy_node($node,$index,$errors);
        foreach(self::find_cycles($index) as $cycle) $errors[]=self::issue('HIERARCHY_CYCLE','nodes','Zyklus erkannt: '.implode(' -> ',$cycle));
        self::validate_global_collisions($nodes,$package,$mode,$errors,$warnings);
        self::validate_source_paths($nodes,$index,$errors);
        self::validate_leaf_rules($nodes,$index,$mode,$errors);
        self::validate_single_child_rules($nodes,$index,$errors);
        self::validate_cluster_usage($nodes,$clusters,$warnings);
        self::validate_coverage_decisions($package,$clusters,$errors);
        self::validate_global_coverage_decisions($package,$errors);
        self::validate_longtail_collisions($nodes,$mode,$errors);
        $rule_report=self::automatic_rule_report($nodes,$index,$package,$errors);
        return self::result($errors,$warnings,$nodes,$index,$rule_report,$clusters);
    }

    public static function normalized_target(array $node,array $package):?array{
        if(isset($node['target'])&&is_array($node['target'])) return ['adapter'=>(string)($node['target']['adapter']??''),'taxonomy'=>isset($node['target']['taxonomy'])?(string)$node['target']['taxonomy']:null,'object_id'=>isset($node['target']['object_id'])?(int)$node['target']['object_id']:null];
        $defaults=$package['default_targets']??null; $block=(string)($node['block']??'');
        if(is_array($defaults)&&isset($defaults[$block])&&is_array($defaults[$block])) return ['adapter'=>(string)($defaults[$block]['adapter']??''),'taxonomy'=>isset($defaults[$block]['taxonomy'])?(string)$defaults[$block]['taxonomy']:null,'object_id'=>isset($node['source_object_id'])?(int)$node['source_object_id']:null];
        return null;
    }
    public static function visible_name_key(string $name):string{ return self::key($name); }
    public static function active_node(array $node):bool{ return self::is_active($node); }

    private static function validate_project(array $package,array &$errors,array &$warnings=[]):void{
        $project=$package['project']??null;
        if(!is_array($project)){ $errors[]=self::issue('PROJECT_MISSING','project','project muss ein Objekt sein.'); return; }
        foreach(['project_id','name','scope','target_market','language_code'] as $f) self::require_string($project,$f,$errors,'PROJECT_FIELD_MISSING','project.'.$f);
        if(!isset($project['exclusions'])||!is_array($project['exclusions'])) $errors[]=self::issue('PROJECT_EXCLUSIONS_INVALID','project.exclusions','project.exclusions muss ein Array sein.');
        $discovery=$project['discovery_seed_keywords']??null;
        if(!is_array($discovery)||!$discovery){ $errors[]=self::issue('PROJECT_DISCOVERY_SEEDS_MISSING','project.discovery_seed_keywords','Mindestens ein projektweiter Discovery-Seed ist erforderlich, damit fehlende Hauptthemen geprüft werden können.'); }
        else {
            $clean=array_values(array_unique(array_filter(array_map(static fn($v)=>self::key((string)$v),$discovery),static fn($v)=>$v!=='')));
            if(count($clean)>APKW_DataForSEO::max_idea_seeds()) $errors[]=self::issue('PROJECT_DISCOVERY_SEEDS_TOO_MANY','project.discovery_seed_keywords','Maximal 200 projektweite Discovery-Seeds.');
            if(count($clean)<3) $warnings[]=self::issue('PROJECT_DISCOVERY_SEEDS_NARROW_REVIEW','project.discovery_seed_keywords','Weniger als drei unterschiedliche Discovery-Seeds können die projektweite Coverage schwächen. Das ist ein Review-Hinweis, kein starres Mengen-Gate.');
        }
    }

    private static function validate_clusters(array $package,array &$errors,array &$warnings):array{
        $raw=$package['research_clusters']??null; $index=[];
        if(!is_array($raw)||!$raw){ $errors[]=self::issue('RESEARCH_CLUSTERS_MISSING','research_clusters','Mindestens ein begrenzter Research-Cluster ist erforderlich.'); return $index; }
        if(count($raw)>self::MAX_CLUSTERS) $errors[]=self::issue('RESEARCH_CLUSTER_LIMIT_EXCEEDED','research_clusters','Maximal 100 Research-Cluster.');
        foreach($raw as $i=>$cluster){
            $path='research_clusters['.$i.']';
            if(!is_array($cluster)){ $errors[]=self::issue('RESEARCH_CLUSTER_INVALID',$path,'Cluster muss ein Objekt sein.'); continue; }
            foreach(['cluster_id','name','scope'] as $f) self::require_string($cluster,$f,$errors,'RESEARCH_CLUSTER_FIELD_MISSING',$path.'.'.$f);
            $id=trim((string)($cluster['cluster_id']??''));
            if($id!==''&&!preg_match('/^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$/',$id)) $errors[]=self::issue('RESEARCH_CLUSTER_ID_INVALID',$path.'.cluster_id','cluster_id ungültig.');
            if($id!==''&&isset($index[$id])) $errors[]=self::issue('RESEARCH_CLUSTER_ID_DUPLICATE',$path.'.cluster_id','cluster_id ist mehrfach vorhanden.');
            $seeds=$cluster['seed_keywords']??null;
            if(!is_array($seeds)||!$seeds) $errors[]=self::issue('RESEARCH_CLUSTER_SEEDS_MISSING',$path.'.seed_keywords','Jeder Cluster braucht mindestens ein Seed-Keyword.');
            elseif(count(array_unique(array_map([__CLASS__,'key'],array_map('strval',$seeds))))>APKW_DataForSEO::max_idea_seeds()) $errors[]=self::issue('RESEARCH_CLUSTER_SEEDS_TOO_MANY',$path.'.seed_keywords','Maximal 200 eindeutige Seed-Keywords pro Cluster.');
            if(!isset($cluster['exclusions'])||!is_array($cluster['exclusions'])) $errors[]=self::issue('RESEARCH_CLUSTER_EXCLUSIONS_INVALID',$path.'.exclusions','Cluster-exclusions muss ein Array sein.');
            if($id!=='') $index[$id]=$cluster;
        }
        return $index;
    }

    private static function validate_three_pillars(array $nodes,array &$errors):void{
        $counts=array_fill_keys(self::CORE_BLOCKS,0);
        foreach($nodes as $n) if(self::is_active($n)&&isset($counts[$n['block']])) $counts[$n['block']]++;
        foreach($counts as $block=>$count) if($count===0) $errors[]=self::issue('THREE_PILLAR_BLOCK_MISSING','nodes','Die verbindliche Drei-Säulen-Struktur benötigt mindestens einen aktiven Knoten in '.$block.'.');
    }

    private static function validate_research_binding(array $package,array &$errors):void{
        $binding=$package['research_binding']??null;
        if(!is_array($binding)){ $errors[]=self::issue('RESEARCH_BINDING_MISSING','research_binding','Finales Schema benötigt research_binding.'); return; }
        foreach(['package_id','content_sha256'] as $field) if(!isset($binding[$field])||!is_string($binding[$field])||trim($binding[$field])==='') $errors[]=self::issue('RESEARCH_BINDING_FIELD_MISSING','research_binding.'.$field,$field.' fehlt.');
        if(isset($binding['content_sha256'])&&!preg_match('/^[a-f0-9]{64}$/',(string)$binding['content_sha256'])) $errors[]=self::issue('RESEARCH_BINDING_HASH_INVALID','research_binding.content_sha256','content_sha256 muss SHA-256 sein.');
    }
    public static function review_scope_hash(array $package):string{
        $scope=[
            'master_contract_id'=>(string)($package['master_contract_id']??''),
            'project'=>is_array($package['project']??null)?$package['project']:[],
            'research_clusters'=>is_array($package['research_clusters']??null)?$package['research_clusters']:[],
            'global_coverage_decisions'=>is_array($package['global_coverage_decisions']??null)?$package['global_coverage_decisions']:[],
            'keyword_coverage_decisions'=>is_array($package['keyword_coverage_decisions']??null)?$package['keyword_coverage_decisions']:[],
            'nodes'=>is_array($package['nodes']??null)?$package['nodes']:[],
            'default_targets'=>is_array($package['default_targets']??null)?$package['default_targets']:[],
            'research_binding'=>is_array($package['research_binding']??null)?$package['research_binding']:[],
        ];
        $normalized=self::normalize_review_value($scope);
        $json=wp_json_encode($normalized,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
        return hash('sha256',(string)$json);
    }

    private static function validate_human_sight_review(array $package,array &$errors):void{
        self::validate_review_object($package['human_sight_review']??null,'APPROVED_AFTER_VISIBLE_REVIEW',self::review_scope_hash($package),'human_sight_review','final',$errors);
    }

    private static function normalize_review_value($value){
        if(!is_array($value)) return $value;
        $is_list=array_keys($value)===range(0,count($value)-1);
        if(!$is_list){
            $out=[];$keys=array_keys($value);sort($keys,SORT_STRING);
            foreach($keys as $key)$out[(string)$key]=self::normalize_review_value($value[$key]);
            return $out;
        }
        $out=array_map([__CLASS__,'normalize_review_value'],$value);
        usort($out,static fn($a,$b)=>strcmp((string)wp_json_encode($a,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),(string)wp_json_encode($b,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)));
        return $out;
    }

    public static function initial_review_scope_hash(array $package):string{
        $scope=[
            'master_contract_id'=>(string)($package['master_contract_id']??''),
            'project'=>is_array($package['project']??null)?$package['project']:[],
            'research_clusters'=>is_array($package['research_clusters']??null)?$package['research_clusters']:[],
            'nodes'=>is_array($package['nodes']??null)?$package['nodes']:[],
            'default_targets'=>is_array($package['default_targets']??null)?$package['default_targets']:[],
        ];
        $normalized=self::normalize_review_value($scope);
        $json=wp_json_encode($normalized,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
        return hash('sha256',(string)$json);
    }

    public static function validate_initial_review_gate(array $package):array{
        $errors=[];
        self::validate_review_object($package['initial_human_sight_review']??null,'APPROVED_INITIAL_TREE',self::initial_review_scope_hash($package),'initial_human_sight_review','initial',$errors);
        return ['valid'=>count($errors)===0,'errors'=>$errors,'review_scope_sha256'=>self::initial_review_scope_hash($package)];
    }

    public static function global_gap_review_scope_hash(array $package):string{
        $scope=[
            'master_contract_id'=>(string)($package['master_contract_id']??''),
            'project'=>is_array($package['project']??null)?$package['project']:[],
            'research_clusters'=>is_array($package['research_clusters']??null)?$package['research_clusters']:[],
            'global_coverage_decisions'=>is_array($package['global_coverage_decisions']??null)?$package['global_coverage_decisions']:[],
            'nodes'=>is_array($package['nodes']??null)?$package['nodes']:[],
            'default_targets'=>is_array($package['default_targets']??null)?$package['default_targets']:[],
            'global_coverage_binding'=>is_array($package['global_coverage_binding']??null)?$package['global_coverage_binding']:[],
        ];
        $normalized=self::normalize_review_value($scope);
        $json=wp_json_encode($normalized,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
        return hash('sha256',(string)$json);
    }

    public static function validate_global_gap_review_gate(array $package,array $global_package):array{
        $errors=[];
        $binding=is_array($package['global_coverage_binding']??null)?$package['global_coverage_binding']:[];
        $expected_id=(string)($global_package['package_id']??'');
        $expected_hash=(string)($global_package['content_sha256']??'');
        if((string)($binding['package_id']??'')!==$expected_id)$errors[]=self::issue('GLOBAL_GAP_REVIEW_BINDING_ID_MISMATCH','global_coverage_binding.package_id','Korrigierter Draft ist nicht an dieses Global-Coverage-Paket gebunden.');
        if((string)($binding['content_sha256']??'')!==$expected_hash)$errors[]=self::issue('GLOBAL_GAP_REVIEW_BINDING_HASH_MISMATCH','global_coverage_binding.content_sha256','Korrigierter Draft ist nicht hashgebunden an dieses Global-Coverage-Paket.');
        self::validate_review_object($package['global_gap_human_review']??null,'APPROVED_GLOBAL_GAP_CORRECTION',self::global_gap_review_scope_hash($package),'global_gap_human_review','global_gap',$errors);
        return ['valid'=>count($errors)===0,'errors'=>$errors,'review_scope_sha256'=>self::global_gap_review_scope_hash($package)];
    }

    public static function create_signed_review_receipt(array $package,string $stage,string $summary,int $user_id,?string $approved_at_utc=null):array{
        $summary=trim($summary);
        if($summary==='') throw new RuntimeException('Review-Zusammenfassung fehlt.');
        if($user_id<1) throw new RuntimeException('Freigebender WordPress-Benutzer fehlt.');
        if($stage==='initial'){
            $status='APPROVED_INITIAL_TREE';
            $hash=self::initial_review_scope_hash($package);
        }elseif($stage==='global_gap'){
            $status='APPROVED_GLOBAL_GAP_CORRECTION';
            $hash=self::global_gap_review_scope_hash($package);
        }elseif($stage==='final'){
            $status='APPROVED_AFTER_VISIBLE_REVIEW';
            $hash=self::review_scope_hash($package);
        }else{
            throw new RuntimeException('Unbekannte Review-Stufe.');
        }
        $approved_at_utc=$approved_at_utc??gmdate('Y-m-d\TH:i:s\Z');
        if(!preg_match('/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/',$approved_at_utc)) throw new RuntimeException('approved_at_utc muss UTC-ISO mit Z sein.');
        $receipt=[
            'status'=>$status,
            'review_scope_sha256'=>$hash,
            'approved_at_utc'=>$approved_at_utc,
            'review_summary'=>$summary,
            'approved_by_user_id'=>$user_id,
        ];
        $receipt['receipt_signature_sha256']=self::review_receipt_signature($stage,$receipt);
        return $receipt;
    }

    private static function validate_review_object($review,string $expected_status,string $expected_hash,string $path,string $stage,array &$errors):void{
        if(!is_array($review)){
            $errors[]=self::issue(strtoupper($path).'_MISSING',$path,'Verbindliche sichtbare Freigabe fehlt.');
            return;
        }
        if((string)($review['status']??'')!==$expected_status)$errors[]=self::issue(strtoupper($path).'_STATUS_INVALID',$path.'.status','Erwartet wird '.$expected_status.'.');
        $hash=(string)($review['review_scope_sha256']??'');
        if(!preg_match('/^[a-f0-9]{64}$/',$hash))$errors[]=self::issue(strtoupper($path).'_HASH_INVALID',$path.'.review_scope_sha256','review_scope_sha256 muss SHA-256 sein.');
        elseif(!hash_equals($expected_hash,$hash))$errors[]=self::issue(strtoupper($path).'_SCOPE_CHANGED',$path.'.review_scope_sha256','Der sichtbare Review-Scope wurde nach Freigabe verändert. Erneute Sichtprüfung erforderlich.');
        $approved_at=trim((string)($review['approved_at_utc']??''));
        if($approved_at===''||!preg_match('/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/',$approved_at))$errors[]=self::issue(strtoupper($path).'_TIMESTAMP_INVALID',$path.'.approved_at_utc','approved_at_utc muss UTC-ISO mit Z sein.');
        if(trim((string)($review['review_summary']??''))==='')$errors[]=self::issue(strtoupper($path).'_SUMMARY_MISSING',$path.'.review_summary','Dokumentierte Sichtprüfungs-Zusammenfassung fehlt.');
        $user_id=(int)($review['approved_by_user_id']??0);
        if($user_id<1)$errors[]=self::issue(strtoupper($path).'_USER_INVALID',$path.'.approved_by_user_id','Freigabe benötigt einen WordPress-Administrator als technischen Freigabeakteur.');
        $signature=(string)($review['receipt_signature_sha256']??'');
        if(!preg_match('/^[a-f0-9]{64}$/',$signature)){
            $errors[]=self::issue(strtoupper($path).'_SIGNATURE_MISSING',$path.'.receipt_signature_sha256','Review-Hash/Status dürfen nicht manuell injiziert werden; es fehlt die serverseitig signierte Freigabequittung.');
        }else{
            try{
                $expected_signature=self::review_receipt_signature($stage,$review);
                if(!hash_equals($expected_signature,$signature))$errors[]=self::issue(strtoupper($path).'_SIGNATURE_INVALID',$path.'.receipt_signature_sha256','Review-Quittung ist nicht serverseitig gültig oder wurde nachträglich verändert.');
            }catch(Throwable $e){
                $errors[]=self::issue(strtoupper($path).'_SIGNATURE_UNVERIFIABLE',$path.'.receipt_signature_sha256','Review-Quittung kann serverseitig nicht verifiziert werden.');
            }
        }
    }

    private static function review_receipt_signature(string $stage,array $review):string{
        if(!function_exists('wp_salt')) throw new RuntimeException('WordPress-Signaturschlüssel nicht verfügbar.');
        $secret=(string)wp_salt('auth');
        if($secret==='') throw new RuntimeException('WordPress-Signaturschlüssel leer.');
        $payload=[
            'master_contract_id'=>APKW_MASTER_CONTRACT_ID,
            'stage'=>$stage,
            'status'=>(string)($review['status']??''),
            'review_scope_sha256'=>(string)($review['review_scope_sha256']??''),
            'approved_at_utc'=>(string)($review['approved_at_utc']??''),
            'review_summary'=>(string)($review['review_summary']??''),
            'approved_by_user_id'=>(int)($review['approved_by_user_id']??0),
        ];
        $json=wp_json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
        return hash_hmac('sha256',(string)$json,$secret);
    }

    private static function validate_source_binding(array $package,array &$errors,array &$warnings):void{
        $source=$package['source']??null;
        if($source===null){ $warnings[]=self::issue('SOURCE_METADATA_MISSING','source','Quellenmetadaten fehlen.'); return; }
        if(!is_array($source)){ $errors[]=self::issue('SOURCE_INVALID','source','source muss ein Objekt sein.'); return; }
        $site=trim((string)($source['site']??$source['site_url']??''));
        if($site!==''&&rtrim($site,'/')!==rtrim((string)home_url('/'),'/')) $errors[]=self::issue('SOURCE_SITE_MISMATCH','source.site','Paket gehört zu einer anderen WordPress-Installation.');
    }
    private static function validate_target(array $raw,string $path,array &$errors):void{
        if(!isset($raw['target'])) return;
        if(!is_array($raw['target'])){ $errors[]=self::issue('TARGET_INVALID',$path.'.target','target muss ein Objekt sein.'); return; }
        $adapter=(string)($raw['target']['adapter']??'');
        if(!in_array($adapter,self::ALLOWED_ADAPTERS,true)) $errors[]=self::issue('TARGET_ADAPTER_INVALID',$path.'.target.adapter','Unbekannter Zieladapter.');
        if($adapter==='wordpress_taxonomy'&&trim((string)($raw['target']['taxonomy']??''))==='') $errors[]=self::issue('TARGET_TAXONOMY_MISSING',$path.'.target.taxonomy','Taxonomie fehlt.');
    }
    private static function validate_hierarchy_node(array $node,array $index,array &$errors):void{
        $id=(string)$node['concept_id']; $parent=$node['parent_concept_id']??null;
        if($parent===null||$parent===''){ if((int)$node['level']!==1) $errors[]=self::issue('ROOT_LEVEL_MISMATCH','node:'.$id,'Wurzelknoten muss level 1 haben.'); return; }
        if(!isset($index[$parent])){ $errors[]=self::issue('PARENT_NOT_FOUND','node:'.$id,'Elternknoten fehlt im Paket.'); return; }
        $pn=$index[$parent];
        if(($pn['block']??'')!==($node['block']??'')) $errors[]=self::issue('CROSS_BLOCK_PARENT','node:'.$id,'Elternbeziehung über Portalblöcke hinweg ist unzulässig.');
        if((int)$node['level']!==((int)$pn['level']+1)) $errors[]=self::issue('LEVEL_PARENT_MISMATCH','node:'.$id,'level stimmt nicht mit dem Elternknoten überein.');
    }

    private static function validate_global_collisions(array $nodes,array $package,string $mode,array &$errors,array &$warnings):void{
        $visible=[];$block_slugs=[];$intent_keys=[];$primary=[];$target_slugs=[];
        foreach($nodes as $node){
            if(!self::is_active($node)) continue; $id=(string)$node['concept_id'];
            $name_key=self::key((string)$node['name']);
            if($name_key!==''){ if(isset($visible[$name_key])) $errors[]=self::issue('VISIBLE_NAME_DUPLICATE_GLOBAL','node:'.$id.'.name','Identische sichtbare Kategoriebezeichnung bereits bei '.$visible[$name_key].'.'); else $visible[$name_key]=$id; }
            $slug_key=(string)$node['block'].'|'.strtolower((string)$node['slug']);
            if(isset($block_slugs[$slug_key])) $errors[]=self::issue('SLUG_DUPLICATE_WITHIN_BLOCK','node:'.$id.'.slug','Slug ist innerhalb des Blocks bereits vergeben.'); else $block_slugs[$slug_key]=$id;
            $intent=trim((string)($node['intent_key']??''));
            if($intent!==''){ if(isset($intent_keys[$intent])) $errors[]=self::issue('INTENT_KEY_DUPLICATE','node:'.$id.'.intent_key','intent_key ist bereits bei '.$intent_keys[$intent].' primär belegt.'); else $intent_keys[$intent]=$id; }
            $pk=self::key((string)($node['primary_keyword']??''));
            if($pk!==''){
                foreach($primary[$pk]??[] as $prev){
                    if((string)$prev['block']===(string)$node['block']){
                        $errors[]=self::issue('PRIMARY_KEYWORD_DUPLICATE_WITHIN_BLOCK','node:'.$id.'.primary_keyword','Dasselbe Primärkeyword ist innerhalb derselben Säule bereits bei '.$prev['concept_id'].' belegt.');
                        continue;
                    }
                    $same_intent=self::key((string)$prev['search_intent'])===self::key((string)$node['search_intent']);
                    if($same_intent){
                        $errors[]=self::issue('PRIMARY_KEYWORD_CROSS_PILLAR_SAME_INTENT','node:'.$id.'.primary_keyword','Dasselbe Primärkeyword mit gleicher Suchintention ist säulenübergreifend bereits bei '.$prev['concept_id'].' belegt.');
                    } else {
                        $warnings[]=self::issue('PRIMARY_KEYWORD_CROSS_PILLAR_REVIEW','node:'.$id.'.primary_keyword','Dasselbe Primärkeyword wird mit anderer Säulen-/Suchintention genutzt; funktionale Trennung muss begründet bleiben.');
                        if(in_array($mode,['READ_ONLY_PREVIEW','FINAL_APPROVED'],true) && (trim((string)($node['overlap_justification']??''))==='' || trim((string)($prev['overlap_justification']??''))==='')){
                            $errors[]=self::issue('CROSS_PILLAR_OVERLAP_JUSTIFICATION_MISSING','node:'.$id.'.overlap_justification','Finaler säulenübergreifender Primärkeyword-Overlap benötigt Begründung auf beiden Knoten.');
                        }
                    }
                }
                $primary[$pk][]=['concept_id'=>$id,'block'=>(string)$node['block'],'search_intent'=>(string)$node['search_intent'],'overlap_justification'=>(string)($node['overlap_justification']??'')];
            }
            $target=self::normalized_target($node,$package);
            if($target!==null){
                $adapter=(string)($target['adapter']??'');
                $taxonomy=(string)($target['taxonomy']??'');
                $parent=(string)($node['parent_concept_id']??'');
                // WordPress taxonomy slugs are a taxonomy-wide technical namespace; hierarchical page slugs may depend on parent.
                $slug_scope=$adapter==='wordpress_taxonomy'?'GLOBAL_TAXONOMY':$parent;
                $key=implode('|',[$adapter,$taxonomy,$slug_scope,strtolower((string)$node['slug'])]);
                if(isset($target_slugs[$key])) $errors[]=self::issue('PACKAGE_TARGET_SLUG_COLLISION','node:'.$id,'Gleicher technischer Ziel-Slug kollidiert mit '.$target_slugs[$key].'.');
                else $target_slugs[$key]=$id;
            }
        }
    }

    private static function validate_leaf_rules(array $nodes,array $index,string $mode,array &$errors):void{
        $child_counts=[]; foreach($nodes as $node){ if(!self::is_active($node))continue; $p=(string)($node['parent_concept_id']??''); if($p!=='')$child_counts[$p]=($child_counts[$p]??0)+1; }
        foreach($nodes as $node){ if(!self::is_active($node)||($node['block']??'')!=='content')continue; $id=(string)$node['concept_id']; $leaf=!isset($child_counts[$id]); if((bool)$node['is_leaf']!==$leaf)$errors[]=self::issue('IS_LEAF_MISMATCH','node:'.$id.'.is_leaf','is_leaf stimmt nicht mit der realen Hierarchie überein.'); if(in_array($mode,['READ_ONLY_PREVIEW','FINAL_APPROVED'],true)&&$leaf){ $lts=is_array($node['longtail_potential']??null)?array_values(array_filter(array_map('strval',$node['longtail_potential']),static fn($v)=>trim($v)!=='')):[]; $keys=array_unique(array_map([__CLASS__,'key'],$lts)); if(count($keys)<3)$errors[]=self::issue('CONTENT_LEAF_LONGTAILS_INSUFFICIENT','node:'.$id.'.longtail_potential','Finaler unterster Content-Knoten benötigt mindestens drei eigenständige recherchierte Longtails; drei bis fünf oder mehr tragfähige Beiträge sind der reguläre Freigabebereich.'); } }
    }
    private static function validate_single_child_rules(array $nodes,array $index,array &$errors):void{
        $children=[]; foreach($nodes as $n){ if(!self::is_active($n))continue; $p=(string)($n['parent_concept_id']??''); if($p!=='')$children[$p][]=$n; }
        foreach($children as $pid=>$items) if(count($items)===1&&trim((string)(($index[$pid]??[])['single_child_justification']??''))==='') $errors[]=self::issue('SINGLE_CHILD_HIERARCHY_UNJUSTIFIED','node:'.$pid,'Ein-Kind-Hierarchie benötigt Begründung.');
    }
    private static function validate_source_paths(array $nodes,array $index,array &$errors):void{
        foreach($nodes as $node){ if(!isset($node['path'])||trim((string)$node['path'])==='')continue; $expected=self::build_declared_path((string)$node['concept_id'],$index); if($expected!==null&&self::normalize_path($expected)!==self::normalize_path((string)$node['path']))$errors[]=self::issue('DECLARED_PATH_MISMATCH','node:'.$node['concept_id'].'.path','Deklarierter Pfad stimmt nicht mit der Elternkette überein.'); }
    }
    private static function validate_cluster_usage(array $nodes,array $clusters,array &$warnings):void{
        $used=[]; foreach($nodes as $n) if(self::is_active($n)&&in_array((string)$n['block'],self::CORE_BLOCKS,true))$used[(string)($n['research_cluster_id']??'')]=true;
        foreach($clusters as $id=>$cluster) if(!isset($used[$id]))$warnings[]=self::issue('RESEARCH_CLUSTER_UNUSED','research_clusters.'.$id,'Research-Cluster hat keinen aktiven Knoten.');
    }
    private static function validate_coverage_decisions(array $package,array $clusters,array &$errors):void{
        if(!isset($package['keyword_coverage_decisions']))return;
        if(!is_array($package['keyword_coverage_decisions'])){ $errors[]=self::issue('KEYWORD_COVERAGE_DECISIONS_INVALID','keyword_coverage_decisions','keyword_coverage_decisions muss ein Array sein.'); return; }
        $allowed=['ARTICLE_ONLY','EXCLUDED','DEFERRED']; $seen=[];
        foreach($package['keyword_coverage_decisions'] as $i=>$d){ $path='keyword_coverage_decisions['.$i.']'; if(!is_array($d)){ $errors[]=self::issue('KEYWORD_COVERAGE_DECISION_INVALID',$path,'Entscheidung muss Objekt sein.'); continue; } foreach(['cluster_id','core_keyword','decision','reason'] as $f)self::require_string($d,$f,$errors,'KEYWORD_COVERAGE_DECISION_FIELD_MISSING',$path.'.'.$f); $cid=(string)($d['cluster_id']??''); if($cid!==''&&!isset($clusters[$cid]))$errors[]=self::issue('KEYWORD_COVERAGE_CLUSTER_UNKNOWN',$path.'.cluster_id','Unbekannter cluster_id.'); if(isset($d['decision'])&&!in_array((string)$d['decision'],$allowed,true))$errors[]=self::issue('KEYWORD_COVERAGE_DECISION_VALUE_INVALID',$path.'.decision','Zulässig: ARTICLE_ONLY, EXCLUDED, DEFERRED.'); $key=$cid.'|'.self::key((string)($d['core_keyword']??'')); if(isset($seen[$key]))$errors[]=self::issue('KEYWORD_COVERAGE_DECISION_DUPLICATE',$path,'Doppelte Coverage-Entscheidung.'); $seen[$key]=true; }
    }

    private static function validate_global_coverage_decisions(array $package,array &$errors):void{
        if(!isset($package['global_coverage_decisions']))return;
        if(!is_array($package['global_coverage_decisions'])){ $errors[]=self::issue('GLOBAL_COVERAGE_DECISIONS_INVALID','global_coverage_decisions','global_coverage_decisions muss ein Array sein.'); return; }
        $allowed=['MAIN_TOPIC','SUBTOPIC','ARTICLE_ONLY','OUT_OF_SCOPE','DEFERRED']; $seen=[];
        $clusters=[]; foreach(is_array($package['research_clusters']??null)?$package['research_clusters']:[] as $c){ if(is_array($c)&&trim((string)($c['cluster_id']??''))!=='')$clusters[(string)$c['cluster_id']]=true; }
        $nodes=[]; foreach(is_array($package['nodes']??null)?$package['nodes']:[] as $n){ if(is_array($n)&&self::is_active($n)&&trim((string)($n['concept_id']??''))!=='')$nodes[(string)$n['concept_id']]=$n; }
        foreach($package['global_coverage_decisions'] as $i=>$d){
            $path='global_coverage_decisions['.$i.']';
            if(!is_array($d)){ $errors[]=self::issue('GLOBAL_COVERAGE_DECISION_INVALID',$path,'Entscheidung muss Objekt sein.'); continue; }
            foreach(['core_keyword','decision','reason'] as $f) self::require_string($d,$f,$errors,'GLOBAL_COVERAGE_DECISION_FIELD_MISSING',$path.'.'.$f);
            $decision=(string)($d['decision']??'');
            if($decision!==''&&!in_array($decision,$allowed,true)) $errors[]=self::issue('GLOBAL_COVERAGE_DECISION_VALUE_INVALID',$path.'.decision','Zulässig: MAIN_TOPIC, SUBTOPIC, ARTICLE_ONLY, OUT_OF_SCOPE, DEFERRED.');
            $key=self::key((string)($d['core_keyword']??''));
            if($key!==''&&isset($seen[$key])) $errors[]=self::issue('GLOBAL_COVERAGE_DECISION_DUPLICATE',$path,'Doppelte globale Coverage-Entscheidung.');
            $seen[$key]=true;
            if(in_array($decision,['MAIN_TOPIC','SUBTOPIC','ARTICLE_ONLY'],true)){
                $cluster_id=trim((string)($d['target_cluster_id']??''));
                if($cluster_id==='') $errors[]=self::issue('GLOBAL_COVERAGE_TARGET_CLUSTER_MISSING',$path.'.target_cluster_id','Diese Entscheidung benötigt target_cluster_id.');
                elseif(!isset($clusters[$cluster_id])) $errors[]=self::issue('GLOBAL_COVERAGE_TARGET_CLUSTER_UNKNOWN',$path.'.target_cluster_id','target_cluster_id ist im korrigierten Draft nicht vorhanden.');
            }
            if(in_array($decision,['MAIN_TOPIC','SUBTOPIC'],true)){
                $owner=trim((string)($d['owner_concept_id']??''));
                if($owner==='') $errors[]=self::issue('GLOBAL_COVERAGE_OWNER_MISSING',$path.'.owner_concept_id','MAIN_TOPIC/SUBTOPIC benötigt owner_concept_id.');
                elseif(!isset($nodes[$owner])) $errors[]=self::issue('GLOBAL_COVERAGE_OWNER_UNKNOWN',$path.'.owner_concept_id','owner_concept_id ist im korrigierten Draft nicht aktiv vorhanden.');
                elseif(isset($d['target_cluster_id']) && (string)($nodes[$owner]['research_cluster_id']??'')!==(string)$d['target_cluster_id']) $errors[]=self::issue('GLOBAL_COVERAGE_OWNER_CLUSTER_MISMATCH',$path,'owner_concept_id gehört nicht zum angegebenen target_cluster_id.');
                if($decision==='MAIN_TOPIC' && isset($nodes[$owner]) && (int)($nodes[$owner]['level']??0)!==1) $errors[]=self::issue('GLOBAL_COVERAGE_MAIN_TOPIC_OWNER_NOT_ROOT',$path.'.owner_concept_id','MAIN_TOPIC muss auf einen aktiven Wurzelknoten (level 1) zeigen.');
            }
        }
    }

    private static function validate_longtail_collisions(array $nodes,string $mode,array &$errors):void{
        if(!in_array($mode,['READ_ONLY_PREVIEW','FINAL_APPROVED'],true))return;
        $primary=[];$longtails=[];
        foreach($nodes as $n){
            if(!self::is_active($n))continue;
            $pk=self::key((string)($n['primary_keyword']??''));
            if($pk!=='')$primary[$pk][]=(string)$n['concept_id'];
        }
        foreach($nodes as $n){
            if(!self::is_active($n)||($n['block']??'')!=='content')continue;
            $id=(string)$n['concept_id'];
            foreach(is_array($n['longtail_potential']??null)?$n['longtail_potential']:[] as $lt){
                $k=self::key((string)$lt);if($k==='')continue;
                if(isset($longtails[$k])&&$longtails[$k]!==$id) $errors[]=self::issue('LONGTAIL_DUPLICATE_OWNERSHIP','node:'.$id.'.longtail_potential','Longtail ist bereits einem anderen Content-Knoten zugeordnet: '.$longtails[$k].'.');
                else $longtails[$k]=$id;
                foreach($primary[$k]??[] as $owner){ if($owner!==$id) $errors[]=self::issue('LONGTAIL_COLLIDES_WITH_PRIMARY_KEYWORD','node:'.$id.'.longtail_potential','Longtail ist Primärkeyword eines anderen Knotens: '.$owner.'.'); }
            }
        }
    }

    private static function automatic_rule_report(array $nodes,array $index,array $package,array $errors):array{
        $codes=array_column($errors,'code'); $checks=[]; $map=[
            'H-001'=>['BLOCK_INVALID','THREE_PILLAR_BLOCK_MISSING'],
            'H-002'=>['PARENT_NOT_FOUND','ROOT_LEVEL_MISMATCH','LEVEL_PARENT_MISMATCH'],
            'H-003'=>['HIERARCHY_CYCLE'], 'H-004'=>['PARENT_NOT_FOUND'], 'H-005'=>['CONCEPT_ID_INVALID','CONCEPT_ID_DUPLICATE'],
            'H-006'=>['SLUG_DUPLICATE_WITHIN_BLOCK'], 'H-007'=>['NODE_FIELD_MISSING','KEYWORD_OWNER_INVALID','EXCLUSIONS_INVALID','LONGTAILS_INVALID','IS_LEAF_INVALID'],
            'H-008'=>['INTENT_KEY_DUPLICATE','PRIMARY_KEYWORD_DUPLICATE_WITHIN_BLOCK','PRIMARY_KEYWORD_CROSS_PILLAR_SAME_INTENT'],
            'H-010'=>['CONTENT_LEAF_LONGTAILS_INSUFFICIENT','LONGTAIL_DUPLICATE_OWNERSHIP','LONGTAIL_COLLIDES_WITH_PRIMARY_KEYWORD'], 'H-019'=>['VISIBLE_NAME_DUPLICATE_GLOBAL'], 'H-020'=>['HUMAN_SIGHT_REVIEW_MISSING','HUMAN_SIGHT_REVIEW_STATUS_INVALID','HUMAN_SIGHT_REVIEW_HASH_INVALID','HUMAN_SIGHT_REVIEW_SCOPE_CHANGED','HUMAN_SIGHT_REVIEW_TIMESTAMP_INVALID','HUMAN_SIGHT_REVIEW_SUMMARY_MISSING'], 'H-012'=>['SINGLE_CHILD_HIERARCHY_UNJUSTIFIED'], 'H-013'=>['ROOT_TITLE_TOO_LONG'], 'H-014'=>['LOWER_TITLE_TOO_LONG'], 'H-017'=>[]
        ];
        foreach($map as $rule=>$cs){$failed=(bool)array_intersect($cs,$codes);$checks[]=['rule'=>$rule,'status'=>$failed?'FAIL':'PASS_AUTOMATED','evidence'=>$rule==='H-017'?'APKW_CONTENT_WRITE_CAPABILITY=false':'validator'];}
        foreach(['H-009','H-011','H-015','H-016','H-018'] as $rule)$checks[]=['rule'=>$rule,'status'=>'MASTER_REVIEW_REQUIRED','evidence'=>'qualitative_or_external_scope'];
        return $checks;
    }
    private static function build_declared_path(string $id,array $index):?string{ $parts=[];$seen=[];$cursor=$id; while($cursor!==''&&isset($index[$cursor])){ if(isset($seen[$cursor]))return null; $seen[$cursor]=true; array_unshift($parts,html_entity_decode((string)$index[$cursor]['name'],ENT_QUOTES|ENT_HTML5,'UTF-8')); $cursor=(string)($index[$cursor]['parent_concept_id']??''); } return implode(' > ',$parts); }
    private static function normalize_path(string $v):string{$parts=preg_split('/\s*>\s*/u',html_entity_decode($v,ENT_QUOTES|ENT_HTML5,'UTF-8'))?:[];return implode(' > ',array_map(static fn($p)=>trim($p),$parts));}
    private static function find_cycles(array $index):array{$cycles=[];$done=[];foreach(array_keys($index) as $start){if(isset($done[$start]))continue;$path=[];$pos=[];$cursor=$start;while($cursor!==null&&$cursor!==''&&isset($index[$cursor])){if(isset($pos[$cursor])){$cycles[]=array_slice($path,$pos[$cursor]);break;}if(isset($done[$cursor]))break;$pos[$cursor]=count($path);$path[]=$cursor;$cursor=$index[$cursor]['parent_concept_id']??null;}foreach($path as $v)$done[$v]=true;}return $cycles;}
    private static function is_active(array $node):bool{if(isset($node['active'])&&$node['active']===false)return false;return in_array((string)($node['status']??''),self::ACTIVE_STATUSES,true);}
    private static function key(string $v):string{$v=html_entity_decode($v,ENT_QUOTES|ENT_HTML5,'UTF-8');$v=preg_replace('/\s+/u',' ',trim($v));return function_exists('mb_strtolower')?mb_strtolower((string)$v,'UTF-8'):strtolower((string)$v);}
    private static function length(string $v):int{return function_exists('mb_strlen')?mb_strlen($v,'UTF-8'):strlen($v);}
    private static function require_string(array $data,string $field,array &$errors,string $code,?string $path=null):void{if(!isset($data[$field])||!is_string($data[$field])||trim($data[$field])==='')$errors[]=self::issue($code,$path??$field,$field.' fehlt oder ist leer.');}
    private static function issue(string $code,string $path,string $message):array{return ['code'=>$code,'path'=>$path,'message'=>$message];}
    private static function result(array $errors,array $warnings,array $nodes,array $index,array $rule_report,array $clusters):array{return ['valid'=>count($errors)===0,'errors'=>$errors,'warnings'=>$warnings,'nodes'=>$nodes,'index'=>$index,'automatic_rule_report'=>$rule_report,'clusters'=>$clusters];}
}
