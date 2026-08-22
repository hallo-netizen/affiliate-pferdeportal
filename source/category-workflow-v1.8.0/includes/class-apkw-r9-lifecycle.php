<?php
if (!defined('ABSPATH')) { exit; }

/**
 * MASTER016-R9: SEO-demand + affiliate-fit + learning lifecycle gate.
 *
 * DataForSEO remains evidence only. This gate never invents categories, never
 * changes the MASTER and never interprets a broad parent decision as coverage of
 * narrower phrases. It only proves that every active structural node has bound
 * demand evidence and an explicit project-bound affiliate path.
 */
final class APKW_R9Lifecycle {
    public const CONTRACT='MASTER016_R9_DYNAMIC_SEO_AFFILIATE_LEARNING_LIFECYCLE_V1';
    private const FITS=['DIRECT','ASSISTED'];
    private const BLOCK_FITS=[
        'content'=>['DIRECT','ASSISTED'],
        'marketplace'=>['DIRECT'],
        'magazine'=>['DIRECT','ASSISTED'],
    ];
    private const BLOCK_INTENTS=[
        'content'=>['informational','commercial','transactional'],
        'marketplace'=>['commercial','transactional','navigational'],
        'magazine'=>['informational','commercial','transactional'],
    ];

    public static function analyze(array $package,array $research,array $validation,array $node_evidence):array{
        $errors=[];$warnings=[];$rows=[];$demand_pass=0;$affiliate_pass=0;$gate_applies=in_array((string)($package['mode']??''),['READ_ONLY_PREVIEW','FINAL_APPROVED'],true);
        if(empty($validation['valid']))return ['contract'=>self::CONTRACT,'valid'=>false,'status'=>'BLOCKED_SCHEMA','errors'=>[],'warnings'=>[],'nodes'=>[]];
        $project=is_array($package['project']??null)?$package['project']:[];
        $model=is_array($project['affiliate_model']??null)?$project['affiliate_model']:[];
        $paths=array_values(array_unique(array_filter(array_map('strval',is_array($model['monetization_paths']??null)?$model['monetization_paths']:[]),static fn($v)=>trim($v)!=='')));
        $evidence_by_id=[];foreach($node_evidence as $row)if(is_array($row)&&trim((string)($row['concept_id']??''))!=='')$evidence_by_id[(string)$row['concept_id']]=$row;
        $cluster_items=self::cluster_items($research);
        $active_count=0;
        foreach($validation['nodes'] as $node){
            if(!APKW_Validator::active_node($node)||!in_array((string)($node['block']??''),array_keys(self::BLOCK_FITS),true))continue;
            $active_count++;$id=(string)$node['concept_id'];$block=(string)$node['block'];$ev=$evidence_by_id[$id]??[];
            $demand=self::demand_evidence($node,$ev,$cluster_items[(string)($node['research_cluster_id']??'')]??[]);
            if($demand['valid'])$demand_pass++;elseif($gate_applies)$errors[]=self::issue('R9_SEO_DEMAND_UNRESOLVED','node:'.$id.'.primary_keyword','Kein gebundener positiver Nachfragebeleg für diesen Kategorienraum. Exaktes Primär-/Namenssignal oder ein klar gebundener positiver Core-/Intent-Cluster ist erforderlich.');

            $fit=strtoupper(trim((string)($node['affiliate_fit']??'')));$path=trim((string)($node['affiliate_path']??''));$why=trim((string)($node['affiliate_fit_justification']??''));
            $allowed=self::BLOCK_FITS[$block];$fit_valid=in_array($fit,self::FITS,true)&&in_array($fit,$allowed,true);
            if(!$fit_valid&&$gate_applies)$errors[]=self::issue('R9_AFFILIATE_FIT_BLOCKED','node:'.$id.'.affiliate_fit','Affiliate-Fit fehlt oder ist für den Block unzulässig. Erlaubt: '.implode(', ',$allowed).'.');
            if(($path===''||!in_array($path,$paths,true))&&$gate_applies)$errors[]=self::issue('R9_AFFILIATE_PATH_UNBOUND','node:'.$id.'.affiliate_path','Affiliate-Pfad muss ausdrücklich aus dem gebundenen Projekt-Affiliate-Modell stammen.');
            if($why===''&&$gate_applies)$errors[]=self::issue('R9_AFFILIATE_FIT_JUSTIFICATION_MISSING','node:'.$id.'.affiliate_fit_justification','Affiliate-Fit benötigt eine nachvollziehbare Begründung; Werbeeinblendung allein genügt nicht.');
            $intent=self::key((string)($node['search_intent']??''));$intent_valid=in_array($intent,self::BLOCK_INTENTS[$block],true);
            if(!$intent_valid&&$gate_applies)$errors[]=self::issue('R9_BLOCK_INTENT_INVALID','node:'.$id.'.search_intent','Search Intent passt nicht zum R9-Säulenvertrag für '.$block.'.');
            if($fit_valid&&$path!==''&&in_array($path,$paths,true)&&$why!==''&&$intent_valid)$affiliate_pass++;
            $rows[]=[
                'concept_id'=>$id,'block'=>$block,'name'=>(string)$node['name'],'primary_keyword'=>(string)$node['primary_keyword'],
                'search_intent'=>(string)$node['search_intent'],'demand'=>$demand,'affiliate_fit'=>$fit!==''?$fit:null,'affiliate_path'=>$path!==''?$path:null,
                'affiliate_fit_justification'=>$why!==''?$why:null,'affiliate_valid'=>$fit_valid&&$path!==''&&in_array($path,$paths,true)&&$why!==''&&$intent_valid,
            ];
        }
        $valid=!$gate_applies||(count($errors)===0&&$active_count===$demand_pass&&$active_count===$affiliate_pass);
        return [
            'contract'=>self::CONTRACT,'gate_applies'=>$gate_applies,'valid'=>$valid,'status'=>!$gate_applies?'RESEARCH_DRAFT_GATE_NOT_APPLIED':($valid?'PASS_SEO_AFFILIATE_LIFECYCLE':'BLOCKED_SEO_AFFILIATE_LIFECYCLE'),
            'active_structural_node_count'=>$active_count,'seo_demand_pass_count'=>$demand_pass,'affiliate_fit_pass_count'=>$affiliate_pass,
            'errors'=>$errors,'warnings'=>$warnings,'nodes'=>$rows,
            'policy'=>[
                'new_structure_requires_seo_evidence'=>true,'fixed_min_search_volume'=>false,'manual_idea_direct_publish'=>false,
                'allowed_affiliate_fits'=>self::FITS,'marketplace_requires_direct'=>true,'baseline_is_not_freeze'=>true,
                'new_paid_research_only_for_new_identity'=>true,'master_self_modification'=>false,
            ],
        ];
    }

    private static function demand_evidence(array $node,array $ev,array $cluster_items):array{
        $primary=is_array($ev['exact_primary_evidence']??null)?$ev['exact_primary_evidence']:null;
        $visible=is_array($ev['exact_visible_name_evidence']??null)?$ev['exact_visible_name_evidence']:null;
        $pv=self::volume($primary);if($pv!==null&&$pv>0)return ['valid'=>true,'basis'=>'EXACT_PRIMARY_POSITIVE_VOLUME','search_volume'=>$pv,'keyword'=>(string)($primary['keyword']??$node['primary_keyword'])];
        $nv=self::volume($visible);if($nv!==null&&$nv>0)return ['valid'=>true,'basis'=>'EXACT_VISIBLE_NAME_POSITIVE_VOLUME','search_volume'=>$nv,'keyword'=>(string)($visible['keyword']??$node['name'])];
        $core=self::key((string)($ev['resolved_core_keyword']??''));if($core==='')$core=self::key((string)($node['primary_keyword']??''));
        $best=null;$best_vol=null;$intents=[];
        foreach($cluster_items as $item){
            if(!is_array($item))continue;$icore=self::key((string)($item['core_keyword']??''));if($icore==='')$icore=self::key((string)($item['keyword']??''));if($icore!==$core)continue;
            $v=self::volume($item);if($v===null||$v<=0)continue;$intent=self::key((string)($item['main_intent']??''));if($intent!=='')$intents[$intent]=true;
            if($best_vol===null||$v>$best_vol){$best_vol=$v;$best=$item;}
        }
        if(is_array($best))return ['valid'=>true,'basis'=>'BOUND_CORE_CLUSTER_POSITIVE_DEMAND','search_volume'=>$best_vol,'keyword'=>(string)($best['keyword']??''),'core_keyword'=>$core,'observed_intents'=>array_keys($intents)];
        return ['valid'=>false,'basis'=>'NO_BOUND_POSITIVE_DEMAND','search_volume'=>null,'keyword'=>(string)($node['primary_keyword']??''),'core_keyword'=>$core];
    }

    private static function cluster_items(array $research):array{
        $out=[];
        foreach(is_array($research['cluster_research']['clusters']??null)?$research['cluster_research']['clusters']:[] as $cluster){if(!is_array($cluster))continue;$cid=(string)($cluster['cluster_id']??'');if($cid!=='')$out[$cid]=is_array($cluster['items']??null)?$cluster['items']:[];}
        foreach(array_merge(is_array($research['leaf_depth_research']['leaves']??null)?$research['leaf_depth_research']['leaves']:[],is_array($research['specialization_depth_research']['nodes']??null)?$research['specialization_depth_research']['nodes']:[]) as $row){if(!is_array($row))continue;$cid=(string)($row['research_cluster_id']??'');if($cid==='')continue;foreach(is_array($row['items']??null)?$row['items']:[] as $item)if(is_array($item))$out[$cid][]=$item;}
        return $out;
    }
    private static function volume($item):?int{return is_array($item)&&isset($item['search_volume'])&&is_numeric($item['search_volume'])?(int)$item['search_volume']:null;}
    private static function key(string $v):string{$v=html_entity_decode($v,ENT_QUOTES|ENT_HTML5,'UTF-8');$v=preg_replace('/\s+/u',' ',trim($v));return function_exists('mb_strtolower')?mb_strtolower((string)$v,'UTF-8'):strtolower((string)$v);}
    private static function issue(string $code,string $path,string $message):array{return ['code'=>$code,'path'=>$path,'message'=>$message];}
}
