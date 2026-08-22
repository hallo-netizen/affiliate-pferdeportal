<?php
if (!defined('ABSPATH')) { exit; }

/**
 * MASTER016-R8: lossless dynamic coverage ledger.
 *
 * This class does not decide category architecture from keywords. It proves that
 * every bound provider keyword remains routed into one of the existing category,
 * editorial, review-candidate or retained-audit paths. Structural EXCLUDED or
 * OUT_OF_SCOPE decisions never delete research evidence and never cascade to
 * narrower/specialized phrases.
 */
final class APKW_CoverageLedger {
    public const CONTRACT = 'MASTER016_R8_LOSSLESS_DYNAMIC_COVERAGE_LEDGER_V1';

    public static function build(array $category_package, array $research_package, array $validation): array {
        $entries=[];
        $active_content=[];$primary_owner=[];
        foreach(is_array($validation['nodes']??null)?$validation['nodes']:[] as $node){
            if(!is_array($node)||!APKW_Validator::active_node($node)||(string)($node['block']??'')!=='content')continue;
            $id=(string)($node['concept_id']??'');$cid=(string)($node['research_cluster_id']??'');$kw=self::key((string)($node['primary_keyword']??''));
            if($id==='')continue;$active_content[$id]=$node;
            if($kw!==''){$primary_owner[$kw][]=$id;self::add($entries,(string)$node['primary_keyword'],'ACTIVE_CONTENT_PRIMARY',$cid,$id,null);}
        }

        foreach(is_array($research_package['specialization_depth_research']['nodes']??null)?$research_package['specialization_depth_research']['nodes']:[] as $row){
            if(!is_array($row))continue;$cid=(string)($row['research_cluster_id']??'');$concept=(string)($row['concept_id']??'');
            foreach(is_array($row['items']??null)?$row['items']:[] as $item)if(is_array($item))self::add($entries,(string)($item['keyword']??''),'STAGE10_NODE_EXACT',$cid,$concept,$item);
        }
        // Legacy node-exact evidence is part of the same lossless registry when not superseded.
        foreach(is_array($research_package['leaf_depth_research']['leaves']??null)?$research_package['leaf_depth_research']['leaves']:[] as $row){
            if(!is_array($row))continue;$cid=(string)($row['research_cluster_id']??'');$concept=(string)($row['concept_id']??'');
            foreach(is_array($row['items']??null)?$row['items']:[] as $item)if(is_array($item))self::add($entries,(string)($item['keyword']??''),'LEGACY_NODE_EXACT',$cid,$concept,$item);
        }
        foreach(is_array($research_package['cluster_research']['clusters']??null)?$research_package['cluster_research']['clusters']:[] as $cluster){
            if(!is_array($cluster))continue;$cid=(string)($cluster['cluster_id']??'');
            foreach(is_array($cluster['items']??null)?$cluster['items']:[] as $item)if(is_array($item))self::add($entries,(string)($item['keyword']??''),'CLUSTER_KEYWORD_IDEAS',$cid,'',$item);
        }
        foreach(is_array($research_package['global_discovery']['items']??null)?$research_package['global_discovery']['items']:[] as $item)if(is_array($item))self::add($entries,(string)($item['keyword']??''),'GLOBAL_KEYWORD_IDEAS','','',$item);

        $spec=[];foreach(is_array($category_package['specialization_coverage_decisions']??null)?$category_package['specialization_coverage_decisions']:[] as $d){if(!is_array($d))continue;$cid=(string)($d['cluster_id']??'');$kw=self::key((string)($d['candidate_keyword']??''));if($cid!==''&&$kw!=='')$spec[$cid.'|'.$kw]=$d;}
        $cluster_dec=[];foreach(is_array($category_package['keyword_coverage_decisions']??null)?$category_package['keyword_coverage_decisions']:[] as $d){if(!is_array($d))continue;$cid=(string)($d['cluster_id']??'');$core=self::key((string)($d['core_keyword']??''));if($cid!==''&&$core!=='')$cluster_dec[$cid.'|'.$core]=$d;}
        $global_dec=[];foreach(is_array($category_package['global_coverage_decisions']??null)?$category_package['global_coverage_decisions']:[] as $d){if(!is_array($d))continue;$core=self::key((string)($d['core_keyword']??''));if($core!=='')$global_dec[$core]=$d;}

        $routing_counts=[];$unassigned=[];$rows=[];$structure_excluded_retained=0;$out_of_scope_retained=0;$review_candidates=0;
        foreach($entries as $kw=>$entry){
            $route=null;$owner_ids=[];$decision=null;
            if(isset($primary_owner[$kw])){$route='CATEGORY_OWNER';$owner_ids=array_values(array_unique($primary_owner[$kw]));}
            if($route===null){
                foreach($entry['cluster_ids'] as $cid){
                    $d=$spec[$cid.'|'.$kw]??null;if(!is_array($d))continue;$decision=$d;$code=(string)($d['decision']??'');$owner=trim((string)($d['owner_concept_id']??''));
                    if($code==='CATEGORY'){$route='CATEGORY_OWNER';if($owner!=='')$owner_ids[]=$owner;}
                    elseif($code==='ARTICLE_ONLY'){$route='EDITORIAL_OWNER';if($owner!=='')$owner_ids[]=$owner;}
                    elseif($code==='COVERED_BY_PARENT'){$route='EXPLICIT_CATEGORY_COVERAGE';if($owner!=='')$owner_ids[]=$owner;}
                    elseif($code==='DEFERRED'){$route='CATEGORY_REVIEW_CANDIDATE';$review_candidates++;}
                    elseif($code==='OUT_OF_SCOPE'){$route='STRUCTURE_OUT_OF_SCOPE_RETAINED';$out_of_scope_retained++;}
                    if($route!==null)break;
                }
            }
            if($route===null){
                foreach($entry['cluster_ids'] as $cid){
                    foreach($entry['core_keywords'] as $core){$d=$cluster_dec[$cid.'|'.$core]??null;if(!is_array($d))continue;$decision=$d;$code=(string)($d['decision']??'');
                        if($code==='ARTICLE_ONLY')$route='EDITORIAL_CLUSTER_BACKLOG';
                        elseif($code==='DEFERRED'){$route='CATEGORY_REVIEW_CANDIDATE';$review_candidates++;}
                        elseif($code==='EXCLUDED'){$route='STRUCTURE_EXCLUDED_RETAINED';$structure_excluded_retained++;}
                        if($route!==null)break 2;
                    }
                }
            }
            if($route===null){
                foreach($entry['core_keywords'] as $core){$d=$global_dec[$core]??null;if(!is_array($d))continue;$decision=$d;$code=(string)($d['decision']??'');$owner=trim((string)($d['owner_concept_id']??''));
                    if(in_array($code,['MAIN_TOPIC','SUBTOPIC'],true)){$route='CATEGORY_OWNER';if($owner!=='')$owner_ids[]=$owner;}
                    elseif($code==='ARTICLE_ONLY')$route='EDITORIAL_CLUSTER_BACKLOG';
                    elseif($code==='DEFERRED'){$route='CATEGORY_REVIEW_CANDIDATE';$review_candidates++;}
                    elseif($code==='OUT_OF_SCOPE'){$route='STRUCTURE_OUT_OF_SCOPE_RETAINED';$out_of_scope_retained++;}
                    if($route!==null)break;
                }
            }
            if($route===null){
                if(!empty($entry['source_concept_ids'])){$route='NODE_BOUND_EDITORIAL_BACKLOG';$owner_ids=array_values(array_filter($entry['source_concept_ids'],fn($id)=>isset($active_content[$id])));}
                elseif(!empty($entry['cluster_ids']))$route='CLUSTER_EDITORIAL_BACKLOG';
                elseif(!empty($entry['sources']))$route='GLOBAL_EDITORIAL_BACKLOG';
            }
            if($route===null){$route='UNASSIGNED';$unassigned[]=$entry['keyword'];}
            $owner_ids=array_values(array_unique(array_filter($owner_ids,fn($id)=>$id!=='')));
            $routing_counts[$route]=($routing_counts[$route]??0)+1;
            $rows[]=$entry+['route'=>$route,'owner_concept_ids'=>$owner_ids,'decision'=>$decision,'retained'=>true,'may_be_repromoted_as_category_candidate'=>!in_array($route,['CATEGORY_OWNER','CATEGORY_REVIEW_CANDIDATE'],true)];
        }
        usort($rows,static fn($a,$b)=>strcmp((string)$a['normalized_keyword'],(string)$b['normalized_keyword']));ksort($routing_counts,SORT_STRING);
        $total=count($entries);$routed=$total-count($unassigned);
        return [
            'contract'=>self::CONTRACT,
            'semantic_completeness_claim'=>false,
            'dynamic_discovery_required'=>true,
            'total_distinct_bound_keywords'=>$total,
            'routed_keyword_count'=>$routed,
            'unassigned_keyword_count'=>count($unassigned),
            'silently_dropped_keyword_count'=>0,
            'parent_cascade_drop_count'=>0,
            'structure_excluded_but_retained_count'=>$structure_excluded_retained,
            'out_of_scope_but_retained_count'=>$out_of_scope_retained,
            'category_review_candidate_count'=>$review_candidates,
            'routing_counts'=>$routing_counts,
            'unassigned_keywords'=>$unassigned,
            'keyword_registry'=>$rows,
            'valid'=>count($unassigned)===0 && $routed===$total,
            'hard_gate'=>'READY_FINAL_REQUIRES_ALL_BOUND_KEYWORDS_LOSSLESSLY_ROUTED; STRUCTURAL_EXCLUSION_NEVER_DELETES_EVIDENCE; PARENT_DECISIONS_NEVER_CASCADE; FUTURE_NEW_KEYWORDS_ENTER_DELTA_RESEARCH',
        ];
    }

    private static function add(array &$entries,string $raw,string $source,string $cluster_id,string $concept_id,?array $item):void{
        $raw=trim($raw);$key=self::key($raw);if($key==='')return;
        if(!isset($entries[$key]))$entries[$key]=[
            'keyword'=>$raw,'normalized_keyword'=>$key,'sources'=>[],'cluster_ids'=>[],'source_concept_ids'=>[],'core_keywords'=>[],
            'max_search_volume'=>null,'best_provider_rank'=>null,'main_intents'=>[],
        ];
        $e=&$entries[$key];$e['sources']=array_values(array_unique(array_merge($e['sources'],[$source])));
        if($cluster_id!=='')$e['cluster_ids']=array_values(array_unique(array_merge($e['cluster_ids'],[$cluster_id])));
        if($concept_id!=='')$e['source_concept_ids']=array_values(array_unique(array_merge($e['source_concept_ids'],[$concept_id])));
        if(is_array($item)){
            $core=self::key((string)($item['core_keyword']??''));if($core==='')$core=$key;if($core!=='')$e['core_keywords']=array_values(array_unique(array_merge($e['core_keywords'],[$core])));
            if(isset($item['search_volume'])&&is_numeric($item['search_volume'])){$v=(int)$item['search_volume'];if($e['max_search_volume']===null||$v>$e['max_search_volume'])$e['max_search_volume']=$v;}
            if(isset($item['provider_rank'])&&is_numeric($item['provider_rank'])){$r=(int)$item['provider_rank'];if($e['best_provider_rank']===null||$r<$e['best_provider_rank'])$e['best_provider_rank']=$r;}
            $intent=trim((string)($item['main_intent']??''));if($intent!=='')$e['main_intents']=array_values(array_unique(array_merge($e['main_intents'],[$intent])));
        }else{$e['core_keywords']=array_values(array_unique(array_merge($e['core_keywords'],[$key])));}
        unset($e);
    }

    private static function key(string $value):string{$value=html_entity_decode($value,ENT_QUOTES|ENT_HTML5,'UTF-8');$value=preg_replace('/\s+/u',' ',trim($value));return function_exists('mb_strtolower')?mb_strtolower((string)$value,'UTF-8'):strtolower((string)$value);}
}
