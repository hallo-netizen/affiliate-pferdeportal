<?php
if (!defined('ABSPATH')) { exit; }

final class APKW_ResearchEvidence {
    /**
     * Operational review cap, not a global minimum-volume rule.
     * We review the strongest distinct DataForSEO core groups per declared cluster.
     */
    private const COVERAGE_RELEVANCE_LIMIT = 15;
    private const COVERAGE_VOLUME_LIMIT = 15;
    private const GLOBAL_COVERAGE_RELEVANCE_LIMIT = 20;
    private const GLOBAL_COVERAGE_VOLUME_LIMIT = 20;

    public static function analyze(array $category_package, array $research_package, array $validation): array {
        if (!$validation['valid']) {
            return [
                'valid'=>false,
                'status'=>'BLOCKED_SCHEMA',
                'errors'=>[],
                'warnings'=>[],
                'nodes'=>[],
                'clusters'=>[],
                'overlap_groups'=>[],
                'hierarchy_signals'=>[],
                'cross_cluster_overlaps'=>[],
                'global_coverage'=>[],
            ];
        }

        $mode=(string)($category_package['mode']??'');
        $overview_items=$research_package['planned_keyword_overview']['items']??[];
        $overview_by_keyword=[];
        foreach(is_array($overview_items)?$overview_items:[] as $item){
            if(!is_array($item))continue;
            $k=self::key((string)($item['keyword']??''));
            if($k!==''&&!isset($overview_by_keyword[$k]))$overview_by_keyword[$k]=$item;
        }

        $cluster_items=[];
        foreach(($research_package['cluster_research']['clusters']??[]) as $cluster){
            if(!is_array($cluster))continue;
            $cid=(string)($cluster['cluster_id']??'');
            if($cid==='')continue;
            $cluster_items[$cid]=is_array($cluster['items']??null)?$cluster['items']:[];
        }

        $global_items=is_array($research_package['global_discovery']['items']??null)?$research_package['global_discovery']['items']:[];

        $errors=[];$warnings=[];$node_rows=[];$node_core=[];$node_item=[];
        foreach($validation['nodes'] as $node){
            if(!APKW_Validator::active_node($node))continue;
            $id=(string)$node['concept_id'];
            $cid=(string)($node['research_cluster_id']??'');
            $pk=self::key((string)($node['primary_keyword']??''));
            $name=self::key((string)($node['name']??''));
            $overview=$pk!==''?($overview_by_keyword[$pk]??null):null;
            $name_overview=$name!==''?($overview_by_keyword[$name]??null):null;

            $pool=$cluster_items[$cid]??[];
            $pool_by_keyword=[];$pool_by_core=[];
            foreach($pool as $item){
                if(!is_array($item))continue;
                $ik=self::key((string)($item['keyword']??''));
                if($ik==='')continue;
                $pool_by_keyword[$ik]=$item;
                $core=self::core_key($item);
                if($core!=='')$pool_by_core[$core][]=$item;
            }

            $matched_cluster=$pk!==''?($pool_by_keyword[$pk]??null):null;
            $matched_name_cluster=$name!==''?($pool_by_keyword[$name]??null):null;
            // A corrected final keyword may come from Keyword Ideas and was therefore not part of the original exact Overview request.
            // Exact keyword evidence from the bound cluster is valid fallback evidence; unrelated cluster items are not.
            $primary_evidence=is_array($overview)?$overview:$matched_cluster;
            $name_evidence=is_array($name_overview)?$name_overview:$matched_name_cluster;
            $primary_evidence_source=is_array($overview)?'KEYWORD_OVERVIEW':(is_array($matched_cluster)?'KEYWORD_IDEAS_EXACT':'NONE');
            $name_evidence_source=is_array($name_overview)?'KEYWORD_OVERVIEW':(is_array($matched_name_cluster)?'KEYWORD_IDEAS_EXACT':'NONE');
            $core=is_array($primary_evidence)?self::core_key($primary_evidence):'';
            if($core==='')$core=$pk;
            $node_core[$id]=$core;
            $node_item[$id]=$primary_evidence;

            $planned_volume=self::volume($primary_evidence);
            if(!is_array($primary_evidence)){
                $warnings[]=self::issue('DFS_PRIMARY_KEYWORD_NO_BOUND_EVIDENCE','node:'.$id.'.primary_keyword','Für das finale Primärkeyword liegen weder exaktes Keyword-Overview noch ein exakter Treffer im gebundenen Research-Cluster vor.');
                if(in_array($mode,['READ_ONLY_PREVIEW','FINAL_APPROVED'],true))$errors[]=self::issue('DFS_PRIMARY_KEYWORD_UNRESOLVED','node:'.$id.'.primary_keyword','Finale Struktur benötigt ein in der gebundenen DataForSEO-Evidenz belegtes Primärkeyword.');
            }

            // Category naming audit: visible category name must itself be checked, not only an invisible primary keyword.
            $name_volume=self::volume($name_evidence);
            $category_name_signals=[];
            if(!is_array($name_evidence)){
                $category_name_signals[]='NO_BOUND_NAME_DATA';
                $warnings[]=self::issue('DFS_VISIBLE_NAME_NO_BOUND_EVIDENCE','node:'.$id.'.name','Für die sichtbare Kategorienbezeichnung liegen weder exaktes Overview noch ein exakter Treffer im gebundenen Research-Cluster vor.');
                if(in_array($mode,['READ_ONLY_PREVIEW','FINAL_APPROVED'],true) && $name!==$pk && trim((string)($node['category_name_justification']??''))===''){
                    $errors[]=self::issue('DFS_VISIBLE_NAME_UNRESOLVED','node:'.$id.'.category_name_justification','Sichtbarer Kategoriename weicht vom belegten Primärkeyword ab und ist selbst nicht belegt; Name muss geändert oder begründet werden.');
                }
            }
            if($name!=='' && $pk!=='' && $name!==$pk){
                $category_name_signals[]='NAME_DIFFERS_FROM_PRIMARY';
                $warnings[]=self::issue('DFS_VISIBLE_NAME_DIFFERS_FROM_PRIMARY_KEYWORD','node:'.$id.'.name','Sichtbare Kategoriebezeichnung und Primärkeyword unterscheiden sich; Keywordstärke und Lesbarkeit müssen bewusst gegeneinander abgewogen werden.');
                if($planned_volume!==null && $planned_volume>0 && ($name_volume===null || $name_volume<$planned_volume)){
                    $category_name_signals[]='NAME_WEAKER_THAN_PRIMARY';
                    $warnings[]=self::issue('DFS_VISIBLE_NAME_WEAKER_THAN_PRIMARY_KEYWORD','node:'.$id.'.name','Das geplante Primärkeyword ist nach DataForSEO stärker als die sichtbare Kategorienbezeichnung.');
                    if(in_array($mode,['READ_ONLY_PREVIEW','FINAL_APPROVED'],true) && trim((string)($node['category_name_justification']??''))===''){
                        $errors[]=self::issue('DFS_CATEGORY_NAME_CHOICE_UNRESOLVED','node:'.$id.'.category_name_justification','Stärkeres belegtes Primärkeyword vorhanden; finaler sichtbarer Kategoriename muss angepasst oder begründet werden.');
                    }
                }
            }

            // Verify declared intent against provider intent. DataForSEO is evidence, not an autonomous decision maker,
            // so a mismatch can be justified but may not pass silently in final mode.
            $provider_intent=is_array($primary_evidence)?self::key((string)($primary_evidence['main_intent']??'')):'';
            $declared_intent=self::key((string)($node['search_intent']??''));
            $intent_mismatch=false;
            if($provider_intent!=='' && self::is_standard_intent($declared_intent) && $provider_intent!==$declared_intent){
                $intent_mismatch=true;
                $warnings[]=self::issue('DFS_DECLARED_INTENT_MISMATCH','node:'.$id.'.search_intent','Deklarierter Search Intent '.$declared_intent.' weicht vom DataForSEO-Hauptintent '.$provider_intent.' ab.');
                if(in_array($mode,['READ_ONLY_PREVIEW','FINAL_APPROVED'],true) && trim((string)($node['intent_justification']??''))===''){
                    $errors[]=self::issue('DFS_INTENT_MISMATCH_UNRESOLVED','node:'.$id.'.intent_justification','Intent-Abweichung muss vor finaler Freigabe korrigiert oder fachlich begründet werden.');
                }
            }

            // Stronger candidates are compared only inside the same DataForSEO core and with compatible intent.
            $candidates=$core!==''?($pool_by_core[$core]??[]):[];
            usort($candidates,[__CLASS__,'sort_volume_desc']);
            $stronger=[];
            foreach($candidates as $cand){
                $ck=self::key((string)($cand['keyword']??''));
                if($ck===''||$ck===$pk)continue;
                $vol=self::volume($cand);
                if($planned_volume!==null&&$vol!==null&&$vol>$planned_volume&&self::intent_compatible((string)($node['search_intent']??''),(string)($cand['main_intent']??''))){
                    $stronger[]=self::compact_item($cand);
                    if(count($stronger)>=5)break;
                }
            }
            if($stronger){
                $warnings[]=self::issue('DFS_STRONGER_CATEGORY_KEYWORD_CANDIDATE','node:'.$id.'.primary_keyword','Im selben DataForSEO-Core-Cluster existieren stärkere passende Suchbegriffe: '.implode(' | ',array_column($stronger,'keyword')));
                if(in_array($mode,['READ_ONLY_PREVIEW','FINAL_APPROVED'],true)&&trim((string)($node['keyword_choice_justification']??''))===''){
                    $errors[]=self::issue('DFS_STRONGER_KEYWORD_UNRESOLVED','node:'.$id.'.keyword_choice_justification','Stärkerer Keyword-Kandidat vorhanden; Auswahl des finalen Primärkeywords muss begründet oder korrigiert sein.');
                }
            }

            // Content leaves need real, node-bound longtails. Merely existing somewhere in the same broad cluster is not enough.
            $longtail_candidates=[];
            if((string)$node['block']==='content'&&!empty($node['is_leaf'])){
                foreach($pool as $item){
                    if(!is_array($item))continue;
                    $ik=self::key((string)($item['keyword']??''));
                    if($ik===''||$ik===$pk)continue;
                    if(self::is_longtail_for($item,$pk,$core))$longtail_candidates[]=self::compact_item($item);
                }
                usort($longtail_candidates,[__CLASS__,'sort_volume_desc']);
                $longtail_candidates=array_slice($longtail_candidates,0,30);
                if(count($longtail_candidates)<3)$warnings[]=self::issue('DFS_LONGTAIL_CANDIDATES_INSUFFICIENT','node:'.$id.'.longtail_potential','Im gebundenen Cluster-Research wurden weniger als drei zum Knoten passende Longtail-Kandidaten gefunden.');

                if(in_array($mode,['READ_ONLY_PREVIEW','FINAL_APPROVED'],true)){
                    $evidence_by_keyword=[];
                    foreach($pool as $item){if(is_array($item)){$ik=self::key((string)($item['keyword']??''));if($ik!=='')$evidence_by_keyword[$ik]=$item;}}
                    foreach(array_values(array_unique(array_map('strval',$node['longtail_potential']??[]))) as $lt){
                        $lk=self::key($lt);
                        if($lk==='')continue;
                        if(!isset($evidence_by_keyword[$lk])){
                            $errors[]=self::issue('DFS_LONGTAIL_NOT_EVIDENCED','node:'.$id.'.longtail_potential','Longtail ist nicht im gebundenen DataForSEO-Cluster belegt: '.$lt);
                            continue;
                        }
                        if(!self::is_longtail_for($evidence_by_keyword[$lk],$pk,$core)){
                            $errors[]=self::issue('DFS_LONGTAIL_NOT_BOUND_TO_NODE','node:'.$id.'.longtail_potential','Longtail existiert im Cluster, gehört nach Core-/Keywordbindung aber nicht zu diesem Content-Knoten: '.$lt);
                        }
                    }
                }
            }

            $node_rows[]=[
                'concept_id'=>$id,
                'block'=>(string)$node['block'],
                'research_cluster_id'=>$cid,
                'name'=>(string)$node['name'],
                'primary_keyword'=>(string)$node['primary_keyword'],
                'declared_search_intent'=>(string)$node['search_intent'],
                'provider_main_intent'=>$provider_intent!==''?$provider_intent:null,
                'intent_mismatch'=>$intent_mismatch,
                'exact_primary_evidence'=>is_array($primary_evidence)?self::compact_item($primary_evidence):null,
                'primary_evidence_source'=>$primary_evidence_source,
                'exact_visible_name_evidence'=>is_array($name_evidence)?self::compact_item($name_evidence):null,
                'visible_name_evidence_source'=>$name_evidence_source,
                'resolved_core_keyword'=>$core,
                'category_name_signals'=>$category_name_signals,
                'stronger_same_core_candidates'=>$stronger,
                'longtail_candidates'=>$longtail_candidates,
                'keyword_choice_justified'=>trim((string)($node['keyword_choice_justification']??''))!=='',
                'category_name_justified'=>trim((string)($node['category_name_justification']??''))!=='',
                'intent_justified'=>trim((string)($node['intent_justification']??''))!=='',
            ];
        }

        $overlap_groups=self::analyze_node_core_overlaps($validation['nodes'],$node_core,$mode,$errors,$warnings);
        $hierarchy=self::analyze_hierarchy($validation['nodes'],$validation['index'],$node_core,$node_item,$mode,$errors,$warnings);
        $coverage=self::analyze_cluster_coverage($category_package,$validation['nodes'],$node_core,$cluster_items,$mode,$errors,$warnings);
        $cross_cluster=self::cross_cluster_overlaps($cluster_items);
        $global_coverage=self::analyze_global_coverage($category_package,$global_items,$cluster_items,$mode,$errors,$warnings);
        foreach($cross_cluster as $g){
            $warnings[]=self::issue('DFS_CROSS_CLUSTER_CORE_OVERLAP_REVIEW','core_keyword:'.$g['core_keyword'],'Keyword-Core taucht in mehreren Research-Clustern auf: '.implode(' | ',$g['cluster_ids']).'. Eigentümerschaft im Master prüfen.');
        }

        return [
            'valid'=>count($errors)===0,
            'status'=>count($errors)===0?'PASS_WITH_RESEARCH_EVIDENCE':'BLOCKED_RESEARCH_EVIDENCE',
            'research_package_id'=>(string)($research_package['package_id']??''),
            'research_content_sha256'=>(string)($research_package['content_sha256']??''),
            'errors'=>$errors,
            'warnings'=>$warnings,
            'nodes'=>$node_rows,
            'clusters'=>$coverage,
            'overlap_groups'=>$overlap_groups,
            'hierarchy_signals'=>$hierarchy,
            'cross_cluster_overlaps'=>$cross_cluster,
            'global_coverage'=>$global_coverage,
            'policy'=>[
                'exact_visible_name_duplicate'=>'BLOCK_GLOBAL_IN_SCHEMA',
                'category_name_strength'=>'EXACT_NAME_METRICS_PLUS_PRIMARY_AND_CORE_CANDIDATE_COMPARISON',
                'declared_intent'=>'COMPARE_WITH_DATAFORSEO_MAIN_INTENT; MISMATCH_REQUIRES_FINAL_JUSTIFICATION',
                'stronger_keyword'=>'REVIEW_REQUIRES_JUSTIFICATION_NOT_BLIND_RENAME',
                'missing_global_topics'=>'TOP_PROJECT_WIDE_CORE_GROUPS_REQUIRE_DECLARED_CLUSTER_COVERAGE_OR_EXPLICIT_DECISION',
                'missing_top_core_groups'=>'OWNER_OR_EXPLICIT_DECISION_REQUIRED',
                'same_core_same_pillar'=>'CANNIBALIZATION_GATE',
                'cross_pillar_overlap'=>'SIMILAR_CORE_ALLOWED_WITH_DISTINCT_PILLAR_ROLE_AND_JUSTIFICATION; EXACT_PRIMARY_PLUS_SAME_INTENT_BLOCKED_IN_SCHEMA',
                'longtails'=>'FINAL_CONTENT_LEAF_REQUIRES_AT_LEAST_3_REAL_NODE_BOUND_DATAFORSEO_LONGTAILS; TYPICAL_TARGET_3_TO_5_OR_MORE',
                'cluster_coverage_policy'=>'UNION_OF_TOP_PROVIDER_RELEVANCE_AND_TOP_SEARCH_VOLUME_CORE_GROUPS',
                'cluster_relevance_limit'=>self::COVERAGE_RELEVANCE_LIMIT,
                'cluster_volume_limit'=>self::COVERAGE_VOLUME_LIMIT,
                'global_coverage_policy'=>'UNION_OF_TOP_PROVIDER_RELEVANCE_AND_TOP_SEARCH_VOLUME_CORE_GROUPS',
                'global_relevance_limit'=>self::GLOBAL_COVERAGE_RELEVANCE_LIMIT,
                'global_volume_limit'=>self::GLOBAL_COVERAGE_VOLUME_LIMIT,
                'search_volume'=>'SIGNAL_NOT_SOLE_DECISION',
            ],
        ];
    }

    private static function analyze_node_core_overlaps(array $nodes,array $node_core,string $mode,array &$errors,array &$warnings):array{
        $groups=[];
        foreach($nodes as $node){
            if(!APKW_Validator::active_node($node))continue;
            $id=(string)$node['concept_id'];
            $core=$node_core[$id]??'';
            if($core==='')continue;
            $groups[$core][]=$node;
        }
        $out=[];
        foreach($groups as $core=>$items){
            if(count($items)<2)continue;
            $by_block=[];
            foreach($items as $n)$by_block[(string)$n['block']][]=$n;
            $out[]=[
                'core_keyword'=>$core,
                'concept_ids'=>array_map(static fn($n)=>(string)$n['concept_id'],$items),
                'blocks'=>array_values(array_unique(array_map(static fn($n)=>(string)$n['block'],$items))),
                'pillar_roles'=>array_values(array_unique(array_map(static fn($n)=>(string)($n['pillar_role']??''),$items))),
                'names'=>array_map(static fn($n)=>(string)$n['name'],$items),
            ];

            foreach($by_block as $same){
                if(count($same)<2)continue;
                $intents=array_values(array_unique(array_map(static fn($n)=>self::key((string)$n['search_intent']),$same)));
                $warnings[]=self::issue('DFS_CORE_OVERLAP_WITHIN_PILLAR_REVIEW','core_keyword:'.$core,'Mehrere Kategorien derselben Säule liegen im selben DataForSEO-Core-Cluster: '.implode(' | ',array_map(static fn($n)=>(string)$n['name'],$same)));
                if(in_array($mode,['READ_ONLY_PREVIEW','FINAL_APPROVED'],true)){
                    if(count($intents)===1){
                        $errors[]=self::issue('DFS_CORE_CANNIBALIZATION_SAME_INTENT','core_keyword:'.$core,'Gleicher Core-Cluster und gleiche Suchintention innerhalb derselben Säule sind nicht final freigabefähig.');
                    } else {
                        foreach($same as $n){
                            if(trim((string)($n['overlap_justification']??''))==='')$errors[]=self::issue('DFS_CORE_OVERLAP_JUSTIFICATION_MISSING','node:'.$n['concept_id'].'.overlap_justification','Core-Overlap innerhalb einer Säule benötigt explizite Trennbegründung.');
                        }
                    }
                }
            }

            if(count($by_block)>1){
                $intents=array_values(array_unique(array_map(static fn($n)=>self::key((string)$n['search_intent']),$items)));
                $warnings[]=self::issue('DFS_CORE_OVERLAP_CROSS_PILLAR_REVIEW','core_keyword:'.$core,'Säulenübergreifender Core-Overlap ist zulässig, wenn Content, Marketplace und Journal unterschiedliche Aufgaben erfüllen und die Trennung begründet ist.');
                if(count($intents)===1)$warnings[]=self::issue('DFS_CORE_CROSS_PILLAR_SAME_COARSE_INTENT_REVIEW','core_keyword:'.$core,'DataForSEO ordnet die überlappenden Säulen demselben groben Search Intent zu; deshalb ist die funktionale Trennung über Säulenrolle und Seitenaufgabe besonders kritisch zu prüfen.');
                if(in_array($mode,['READ_ONLY_PREVIEW','FINAL_APPROVED'],true)){
                    foreach($items as $n){
                        if(trim((string)($n['overlap_justification']??''))==='')$errors[]=self::issue('DFS_CORE_CROSS_PILLAR_JUSTIFICATION_MISSING','node:'.$n['concept_id'].'.overlap_justification','Säulenübergreifender DataForSEO-Core-Overlap benötigt im finalen Stand eine explizite funktionale Trennbegründung.');
                    }
                }
            }
        }
        return $out;
    }

    private static function analyze_hierarchy(array $nodes,array $index,array $node_core,array $node_item,string $mode,array &$errors,array &$warnings):array{
        $signals=[];
        foreach($nodes as $node){
            if(!APKW_Validator::active_node($node))continue;
            $parent_id=(string)($node['parent_concept_id']??'');
            if($parent_id===''||!isset($index[$parent_id]))continue;
            $parent=$index[$parent_id];
            if(!APKW_Validator::active_node($parent))continue;
            $id=(string)$node['concept_id'];
            $pcore=$node_core[$parent_id]??'';
            $ccore=$node_core[$id]??'';
            $same_cluster=(string)($parent['research_cluster_id']??'')===(string)($node['research_cluster_id']??'');
            $same_core=$pcore!==''&&$ccore!==''&&$pcore===$ccore;
            $pvol=self::volume($node_item[$parent_id]??null);
            $cvol=self::volume($node_item[$id]??null);
            $row=[
                'parent_concept_id'=>$parent_id,
                'child_concept_id'=>$id,
                'same_research_cluster'=>$same_cluster,
                'parent_core_keyword'=>$pcore,
                'child_core_keyword'=>$ccore,
                'same_core_keyword'=>$same_core,
                'parent_search_volume'=>$pvol,
                'child_search_volume'=>$cvol,
            ];
            $signals[]=$row;
            if(!$same_cluster)$warnings[]=self::issue('DFS_PARENT_CHILD_CROSS_CLUSTER_REVIEW','node:'.$id.'.research_cluster_id','Eltern- und Kindknoten liegen in unterschiedlichen Research-Clustern.');
            if($same_core){
                $warnings[]=self::issue('DFS_PARENT_CHILD_SAME_CORE_REVIEW','node:'.$id,'Eltern- und Kindknoten liegen im selben DataForSEO-Core-Cluster; Synonym-/Hierarchieproblem prüfen.');
                if(in_array($mode,['READ_ONLY_PREVIEW','FINAL_APPROVED'],true)&&trim((string)($node['hierarchy_justification']??''))==='')$errors[]=self::issue('DFS_PARENT_CHILD_SAME_CORE_UNRESOLVED','node:'.$id.'.hierarchy_justification','Finale Parent-Child-Hierarchie im selben Core-Cluster benötigt eine belastbare Trennbegründung oder Korrektur.');
            }
            if($pvol!==null&&$cvol!==null&&$cvol>$pvol)$warnings[]=self::issue('DFS_CHILD_VOLUME_HIGHER_THAN_PARENT_SIGNAL','node:'.$id.'.primary_keyword','Kindkeyword hat höheres Suchvolumen als Elternkeyword; Hierarchie fachlich prüfen, nicht automatisch ändern.');
        }
        return $signals;
    }

    private static function analyze_cluster_coverage(array $package,array $nodes,array $node_core,array $cluster_items,string $mode,array &$errors,array &$warnings):array{
        $decision_map=[];
        foreach(($package['keyword_coverage_decisions']??[]) as $d){
            if(!is_array($d))continue;
            $decision_map[(string)($d['cluster_id']??'').'|'.self::key((string)($d['core_keyword']??''))]=$d;
        }
        $nodes_by_cluster=[];
        foreach($nodes as $n){
            if(!APKW_Validator::active_node($n))continue;
            $cid=(string)($n['research_cluster_id']??'');
            if($cid!=='')$nodes_by_cluster[$cid][]=$n;
        }

        $rows=[];
        foreach($cluster_items as $cid=>$items){
            $review=self::select_review_groups($items,self::COVERAGE_RELEVANCE_LIMIT,self::COVERAGE_VOLUME_LIMIT);
            $owned=[];
            foreach($nodes_by_cluster[$cid]??[] as $n){
                $c=$node_core[(string)$n['concept_id']]??'';
                if($c!=='')$owned[$c][]=(string)$n['concept_id'];
            }
            $checks=[];
            foreach($review as $g){
                $key=$cid.'|'.$g['core_keyword'];
                $owner=$owned[$g['core_keyword']]??[];
                $decision=$decision_map[$key]??null;
                $decision_code=is_array($decision)?(string)($decision['decision']??''):'';
                $status=$owner?'OWNED':($decision_code==='DEFERRED'?'DEFERRED_BLOCKED':(is_array($decision)?'DECIDED':'UNRESOLVED'));
                $checks[]=$g+['status'=>$status,'owner_concept_ids'=>$owner,'decision'=>$decision];
                if($status==='UNRESOLVED'){
                    $warnings[]=self::issue('DFS_TOP_KEYWORD_GROUP_UNOWNED','cluster:'.$cid.'.core:'.$g['core_keyword'],'Relevanter DataForSEO-Keyword-Core ohne Kategorieeigentümer oder dokumentierte ARTICLE_ONLY/EXCLUDED-Entscheidung; DEFERRED bleibt blockierend: '.$g['top_keyword']);
                    if(in_array($mode,['READ_ONLY_PREVIEW','FINAL_APPROVED'],true))$errors[]=self::issue('DFS_TOP_KEYWORD_GROUP_UNRESOLVED','cluster:'.$cid.'.core:'.$g['core_keyword'],'Finale Struktur muss den relevanten Keyword-Core zuordnen oder begründet aus der Kategoriearchitektur ausschließen.');
                }
                if($status==='DEFERRED_BLOCKED'&&in_array($mode,['READ_ONLY_PREVIEW','FINAL_APPROVED'],true))$errors[]=self::issue('DFS_TOP_KEYWORD_GROUP_DEFERRED_BLOCKS_FINAL','cluster:'.$cid.'.core:'.$g['core_keyword'],'DEFERRED darf keinen finalen PASS erzeugen. Core muss vor Sichtprüfung final zugeordnet, ARTICLE_ONLY oder EXCLUDED entschieden werden.');
            }
            $rows[]=['cluster_id'=>$cid,'review_core_groups'=>$checks,'selection_policy'=>'UNION_OF_TOP_PROVIDER_RELEVANCE_AND_TOP_SEARCH_VOLUME_CORE_GROUPS','relevance_limit'=>self::COVERAGE_RELEVANCE_LIMIT,'volume_limit'=>self::COVERAGE_VOLUME_LIMIT];
        }
        return $rows;
    }

    private static function analyze_global_coverage(array $package,array $global_items,array $cluster_items,string $mode,array &$errors,array &$warnings):array{
        $decision_map=[];
        foreach(($package['global_coverage_decisions']??[]) as $d){
            if(!is_array($d))continue;
            $core=self::key((string)($d['core_keyword']??''));
            if($core!=='')$decision_map[$core]=$d;
        }
        $cluster_core_map=[];
        foreach($cluster_items as $cid=>$items){
            foreach($items as $item){
                if(!is_array($item))continue;
                $core=self::core_key($item);if($core==='')continue;
                $cluster_core_map[$core][$cid]=true;
            }
        }
        $review=self::select_review_groups($global_items,self::GLOBAL_COVERAGE_RELEVANCE_LIMIT,self::GLOBAL_COVERAGE_VOLUME_LIMIT);$checks=[];
        foreach($review as $g){
            $core=$g['core_keyword'];$covered=array_keys($cluster_core_map[$core]??[]);$decision=$decision_map[$core]??null;
            $decision_code=is_array($decision)?(string)($decision['decision']??''):'';
            $status=$decision_code==='DEFERRED'?'DEFERRED_BLOCKED':(is_array($decision)?'DECIDED':'UNRESOLVED');
            $checks[]=$g+['status'=>$status,'covered_cluster_ids'=>$covered,'decision'=>$decision];
            if($status==='UNRESOLVED'){
                $warnings[]=self::issue('DFS_GLOBAL_TOPIC_GAP_REVIEW','global_core:'.$core,'Projektweiter relevanter DataForSEO-Core ist in keinem Research-Cluster abgedeckt und kann ein vergessenes Themenfeld sein: '.$g['top_keyword']);
                if(in_array($mode,['READ_ONLY_PREVIEW','FINAL_APPROVED'],true))$errors[]=self::issue('DFS_GLOBAL_TOPIC_GAP_UNRESOLVED','global_core:'.$core,'Vor finaler Freigabe muss dieses Themenfeld einem Research-Cluster zugeordnet oder mit MAIN_TOPIC/SUBTOPIC/ARTICLE_ONLY/OUT_OF_SCOPE fachlich entschieden werden.');
            }
            if($status==='DEFERRED_BLOCKED'&&in_array($mode,['READ_ONLY_PREVIEW','FINAL_APPROVED'],true))$errors[]=self::issue('DFS_GLOBAL_TOPIC_GAP_DEFERRED_BLOCKS_FINAL','global_core:'.$core,'DEFERRED ist kein finaler Coverage-Abschluss und blockiert READY/FINAL.');
        }
        return ['review_core_groups'=>$checks,'selection_policy'=>'UNION_OF_TOP_PROVIDER_RELEVANCE_AND_TOP_SEARCH_VOLUME_CORE_GROUPS','relevance_limit'=>self::GLOBAL_COVERAGE_RELEVANCE_LIMIT,'volume_limit'=>self::GLOBAL_COVERAGE_VOLUME_LIMIT,'purpose'=>'detect_missing_main_topics_before_final_release'];
    }

    private static function select_review_groups(array $items,int $relevance_limit,int $volume_limit):array{
        $groups=[];
        foreach($items as $position=>$item){
            if(!is_array($item))continue;
            $core=self::core_key($item);if($core==='')continue;
            $rank=isset($item['provider_rank'])&&is_numeric($item['provider_rank'])?(int)$item['provider_rank']:(int)$position+1;
            $vol=self::volume($item)??0;
            if(!isset($groups[$core]))$groups[$core]=['core_keyword'=>$core,'max_search_volume'=>$vol,'search_volume_sum'=>$vol,'top_keyword'=>(string)($item['keyword']??$core),'top_intent'=>$item['main_intent']??null,'keyword_count'=>1,'min_provider_rank'=>$rank,'selected_by'=>[]];
            else{
                $groups[$core]['search_volume_sum']+=$vol;$groups[$core]['keyword_count']++;
                if($rank<$groups[$core]['min_provider_rank'])$groups[$core]['min_provider_rank']=$rank;
                if($vol>$groups[$core]['max_search_volume']){$groups[$core]['max_search_volume']=$vol;$groups[$core]['top_keyword']=(string)($item['keyword']??$core);$groups[$core]['top_intent']=$item['main_intent']??null;}
            }
        }
        $rel=array_values($groups);usort($rel,static fn($a,$b)=>($a['min_provider_rank']<=>$b['min_provider_rank'])?:($b['max_search_volume']<=>$a['max_search_volume'])?:strcmp($a['core_keyword'],$b['core_keyword']));
        $vol=array_values(array_filter($groups,static fn($g)=>(int)($g['max_search_volume']??0)>0));usort($vol,static fn($a,$b)=>($b['max_search_volume']<=>$a['max_search_volume'])?:($a['min_provider_rank']<=>$b['min_provider_rank'])?:strcmp($a['core_keyword'],$b['core_keyword']));
        $selected=[];
        foreach(array_slice($rel,0,$relevance_limit) as $g){$g['selected_by'][]='PROVIDER_RELEVANCE';$selected[$g['core_keyword']]=$g;}
        foreach(array_slice($vol,0,$volume_limit) as $g){if(isset($selected[$g['core_keyword']]))$selected[$g['core_keyword']]['selected_by'][]='SEARCH_VOLUME';else{$g['selected_by'][]='SEARCH_VOLUME';$selected[$g['core_keyword']]=$g;}}
        $out=array_values($selected);usort($out,static fn($a,$b)=>($a['min_provider_rank']<=>$b['min_provider_rank'])?:($b['max_search_volume']<=>$a['max_search_volume'])?:strcmp($a['core_keyword'],$b['core_keyword']));
        return $out;
    }

    private static function cross_cluster_overlaps(array $cluster_items):array{
        $core_clusters=[];$core_top=[];
        foreach($cluster_items as $cid=>$items){
            foreach($items as $item){
                if(!is_array($item))continue;
                $core=self::core_key($item);
                if($core==='')continue;
                $core_clusters[$core][$cid]=true;
                $vol=self::volume($item)??0;
                if(!isset($core_top[$core])||$vol>$core_top[$core]['search_volume'])$core_top[$core]=['keyword'=>(string)$item['keyword'],'search_volume'=>$vol];
            }
        }
        $out=[];
        foreach($core_clusters as $core=>$clusters){
            if(count($clusters)>1)$out[]=['core_keyword'=>$core,'cluster_ids'=>array_keys($clusters),'top_keyword'=>$core_top[$core]['keyword']??$core,'top_search_volume'=>$core_top[$core]['search_volume']??0];
        }
        usort($out,static fn($a,$b)=>($b['top_search_volume']<=>$a['top_search_volume'])?:strcmp($a['core_keyword'],$b['core_keyword']));
        return $out;
    }

    private static function is_longtail_for(array $item,string $pk,string $core):bool{
        $ik=self::key((string)($item['keyword']??''));
        if($ik===''||$ik===$pk)return false;
        $ic=self::core_key($item);
        if($core!==''&&$ic===$core)return self::word_count($ik)>self::word_count($pk);
        if($pk!==''&&str_contains($ik,$pk))return self::word_count($ik)>self::word_count($pk);
        return false;
    }

    private static function is_standard_intent(string $value):bool{return in_array($value,['informational','commercial','transactional','navigational'],true);}
    private static function intent_compatible(string $declared,string $actual):bool{
        $d=self::key($declared);$a=self::key($actual);
        if($a==='')return true;
        if(self::is_standard_intent($d))return $d===$a;
        return true;
    }
    private static function core_key(array $item):string{$core=self::key((string)($item['core_keyword']??''));return $core!==''?$core:self::key((string)($item['keyword']??''));}
    private static function compact_item(array $item):array{return ['keyword'=>(string)($item['keyword']??''),'search_volume'=>self::volume($item),'main_intent'=>$item['main_intent']??null,'core_keyword'=>$item['core_keyword']??null,'keyword_difficulty'=>$item['keyword_difficulty']??null,'cpc'=>$item['cpc']??null];}
    private static function volume($item):?int{return is_array($item)&&isset($item['search_volume'])&&is_numeric($item['search_volume'])?(int)$item['search_volume']:null;}
    private static function sort_volume_desc(array $a,array $b):int{return (self::volume($b)??-1)<=>(self::volume($a)??-1) ?: strcmp((string)($a['keyword']??''),(string)($b['keyword']??''));}
    private static function word_count(string $value):int{$parts=preg_split('/\s+/u',trim($value))?:[];return count(array_filter($parts,static fn($v)=>$v!==''));}
    private static function key(string $value):string{$value=html_entity_decode($value,ENT_QUOTES|ENT_HTML5,'UTF-8');$value=preg_replace('/\s+/u',' ',trim($value));return function_exists('mb_strtolower')?mb_strtolower((string)$value,'UTF-8'):strtolower((string)$value);}
    private static function issue(string $code,string $path,string $message):array{return ['code'=>$code,'path'=>$path,'message'=>$message];}
}
