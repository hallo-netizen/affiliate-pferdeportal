<?php
/**
 * Plugin Name: Robotik Strukturdesign (Test)
 * Description: Monochrome, sehr einfache Strukturansicht mit einem gemeinsamen Kopfbereich, Mega-Menü und Footer aus echten Robotik-Seiten.
 * Version: 0.2.5
 * Requires at least: 6.4
 * Requires PHP: 8.1
 * Text Domain: robotik-strukturdesign
 */
if (!defined('ABSPATH')) { exit; }
final class Robotik_Strukturdesign {
    private static bool $header_rendered=false;
    private static bool $footer_rendered=false;
    private static ?array $tree=null;
    private const VERSION='0.2.5';
    private const ROOTS=['haushalt','garten','freizeit','sport','bildung','pflege','humanoide','gewerbe'];

    public static function boot():void {
        add_filter('body_class',[self::class,'body_class']);
        add_filter('template_include',[self::class,'home_template'],999);
        // WordPress owns the route; our plain test home owns the entire document.
        add_action('template_redirect',[self::class,'root_route'],-10000);
        add_action('wp_enqueue_scripts',[self::class,'assets']);
        add_action('wp_body_open',[self::class,'header'],1);
        add_action('wp_footer',[self::class,'footer'],5);
        add_filter('the_content',[self::class,'product_categories'],30);
    }
    /** Root and WordPress front-page recognition, including reverse-proxy/subdirectory mappings. */
    private static function is_exact_home_request():bool {
        if(is_admin() || is_feed() || (defined('REST_REQUEST') && REST_REQUEST) ||
           (function_exists('wp_doing_ajax') && wp_doing_ajax()))return false;
        $method=strtoupper((string)($_SERVER['REQUEST_METHOD'] ?? 'GET'));
        if(!in_array($method,['GET','HEAD'],true))return false;
        $request=(string)($_SERVER['REQUEST_URI'] ?? '');
        if($request==='')return false;
        $query=(string)parse_url($request,PHP_URL_QUERY);
        // Search, pagination and arbitrary query requests must not be replaced.
        if($query!=='' && !preg_match('/^(?:preview=true|_rtd_test=1)$/',$query))return false;
        $path=(string)parse_url($request,PHP_URL_PATH);
        if($path==='')return false;
        $normalise=static function(string $p):string {
            $p=rawurldecode($p);
            return '/'.trim($p,'/');
        };
        $request_path=$normalise($path);
        // Public domain root is valid even when internal home_url() points to a subdirectory.
        $known=['/'];
        foreach([home_url('/'),function_exists('site_url')?site_url('/'):home_url('/')] as $url){
            $p=(string)parse_url((string)$url,PHP_URL_PATH);
            if($p!=='')$known[]=$normalise($p);
        }
        if(in_array($request_path,$known,true))return true;
        // A static page selected as the genuine WordPress front page also qualifies.
        return function_exists('is_front_page') && is_front_page();
    }
    public static function root_route():void {
        if(!self::is_exact_home_request())return;
        if(function_exists('nocache_headers'))nocache_headers();
        if(!headers_sent())header('X-Robotik-Strukturdesign: '.self::VERSION);
        require __DIR__.'/templates/struktur-startseite.php';
        exit;
    }
    /** Fallback for normal WordPress theme selection; never touches internal pages. */
    public static function home_template(string $template):string {
        if(is_admin()||is_feed())return $template;
        return self::is_exact_home_request() ? __DIR__.'/templates/struktur-startseite.php' : $template;
    }
    public static function body_class(array $classes):array {
        if(!is_admin()&&!is_feed())$classes[]='robotik-structure-test';
        return $classes;
    }
    public static function assets():void {
        if(is_admin()||is_feed())return;
        wp_enqueue_style('robotik-strukturdesign',plugins_url('assets/struktur.css',__FILE__),[], self::VERSION);
        wp_enqueue_script('robotik-strukturdesign',plugins_url('assets/struktur.js',__FILE__),[], self::VERSION,true);
    }
    private static function permitted($p):bool {
        if (!$p || $p->post_type!=='page') return false;
        if ($p->post_status==='publish') return true;
        // Restore the original admin-only work preview: draft pages are not public.
        return current_user_can('manage_options') && in_array($p->post_status,['draft','private','pending'],true);
    }
    private static function link($p):string {
        if (!self::permitted($p)) return '';
        if ($p->post_status==='publish') return (string)get_permalink($p->ID);
        return current_user_can('manage_options') && function_exists('get_preview_post_link')
            ? (string)get_preview_post_link($p) : '';
    }
    private static function tree():array {
        if(self::$tree!==null)return self::$tree;
        $posts=get_posts(['post_type'=>'page','post_status'=>['publish','draft','private','pending'],
            'posts_per_page'=>-1,'orderby'=>'menu_order title','order'=>'ASC','suppress_filters'=>true]);
        $pages=[];$children=[];
        if(is_array($posts))foreach($posts as $p){
            if(!self::permitted($p)||(string)get_post_meta((int)$p->ID,'_robotik_kategorie_node_id',true)==='')continue;
            $pages[(int)$p->ID]=$p;
        }
        foreach($pages as $p){
            $parent=(int)$p->post_parent;
            if($parent===0||isset($pages[$parent]))$children[$parent][]=$p;
        }
        foreach($children as &$items)usort($items,static fn($a,$b)=>strnatcasecmp((string)$a->post_title,(string)$b->post_title));unset($items);
        $roots=[];
        foreach(self::ROOTS as $slug)foreach(($children[0]??[]) as $p){
            if((string)$p->post_name===$slug){$roots[]=$p;break;}
        }
        self::$tree=['pages'=>$pages,'children'=>$children,'roots'=>$roots];return self::$tree;
    }
    private static function anchor($p,string $class=''):string {
        $link=self::link($p);$title=esc_html((string)$p->post_title);
        if($link==='')return '<span class="'.esc_attr($class).'">'.$title.'</span>';
        return '<a class="'.esc_attr($class).'" href="'.esc_url($link).'">'.$title.'</a>';
    }
    private static function utility():string {
        $targets=[
            ['Magazin',['magazin','robotikmagazin']],['Glossar',['roboterglossar','glossar']],
            ['Roboterfinder',['roboterfinder']],['Anzeigenmarkt',['anzeigenmarkt','anzeigen']],
        ];
        $html='';foreach($targets as [$name,$slugs]){
            $page=null;foreach($slugs as $slug){
                $found=get_page_by_path($slug,OBJECT,'page');
                if($found&&self::permitted($found)){$page=$found;break;}
            }
            $url=$page?self::link($page):'';
            $html.=$url!==''?'<a href="'.esc_url($url).'">'.esc_html($name).'</a>':
                '<span class="rtd-pending" title="Noch nicht als WordPress-Seite angelegt">'.esc_html($name).'</span>';
        }
        return $html;
    }
    /** Render descendants without dropping landing pages at depth 3+ (Industrie). */
    private static function nested_links($parent,array $children,int $depth=0):string {
        if ($depth>=8) return '';
        $nodes=$children[(int)$parent->ID]??[];
        if(!$nodes)return '';
        $html='<ul'.($depth?' class="rtd-nested"':'').'>';
        foreach($nodes as $p){
            $html.='<li>'.self::anchor($p);
            $html.=self::nested_links($p,$children,$depth+1);
            $html.='</li>';
        }
        return $html.'</ul>';
    }
    /** Menu styling is not a new WordPress category or page. */
    private static function menu_blocks($root,array $children):array {
        $blocks=[];$direct=[];
        foreach(($children[(int)$root->ID]??[]) as $entry){
            $kids=$children[(int)$entry->ID]??[];
            $role=(string)get_post_meta((int)$entry->ID,'_robotik_page_role',true);
            if(!$kids && $role==='product'){$direct[]=$entry;continue;}
            // Deliberate Industrie landing-page group, even if no immediate products.
            $count=1;
            $walk=static function($p,$depth=0)use(&$walk,$children,&$count):void {
                if($depth>=8)return;
                foreach(($children[(int)$p->ID]??[]) as $kid){$count++;$walk($kid,$depth+1);}
            };
            $walk($entry);
            $blocks[]=['type'=>'group','node'=>$entry,'weight'=>$count];
        }
        if($direct)$blocks[]=['type'=>'direct','nodes'=>$direct,'weight'=>count($direct)+1];
        return $blocks;
    }
    private static function render_header():void {
        $tree=self::tree();$children=$tree['children'];
        echo '<header id="robotik-strukturkopf" class="rtd-header" role="banner" aria-label="Robotik Testkopf">';
        echo '<div class="rtd-topbar"><div class="rtd-topbar-inner">';
        echo '<a class="rtd-logo" href="'.esc_url(home_url('/')).'">ROBOTIK</a>';
        echo '<button class="rtd-mobile-toggle" type="button" aria-expanded="false" aria-controls="rtd-mainnav">Menü <span aria-hidden="true">☰</span></button>';
        echo '<nav class="rtd-mainnav" id="rtd-mainnav" aria-label="Hauptkategorien">';
        foreach($tree['roots'] as $root){
            $blocks=self::menu_blocks($root,$children);
            $total=array_sum(array_column($blocks,'weight'));
            // Balance real groups over 2-4 full-width columns; do not change WordPress hierarchy.
            $colcount=min(4,count($blocks),max(2,(int)ceil($total/7)));
            if($colcount<1)$colcount=1;
            $distribution=array_fill(0,$colcount,[]);
            $heights=array_fill(0,$colcount,0);
            // Tall groups first prevents one isolated column with a large empty neighbor.
            $indexes=array_keys($blocks);
            usort($indexes,static fn($a,$b)=>($blocks[$b]['weight']<=>$blocks[$a]['weight'])?:($a<=>$b));
            foreach($indexes as $idx){
                $target=array_search(min($heights),$heights,true);
                $distribution[$target][]=$blocks[$idx];
                $heights[$target]+=$blocks[$idx]['weight'];
            }
            echo '<details class="rtd-section" data-section="'.esc_attr((string)$root->post_name).'">';
            echo '<summary>'.esc_html((string)$root->post_title).'<span class="rtd-caret" aria-hidden="true">⌄</span></summary>';
            echo '<div class="rtd-mega" aria-label="Unterkategorien '.esc_attr((string)$root->post_title).'">';
            echo '<div class="rtd-mega-top">'.self::anchor($root,'rtd-all-link').'</div><div class="rtd-mega-grid" style="--rtd-columns:'.(int)$colcount.'">';
            foreach($distribution as $column){
                echo '<div class="rtd-mega-column">';
                foreach($column as $block){
                if($block['type']==='group'){
                    $node=$block['node'];
                    $industry=(string)$node->post_name==='industrie';
                    echo '<section class="rtd-mega-group'.($industry?' rtd-industry':'').'"><h3>'.self::anchor($node).'</h3>';
                    echo self::nested_links($node,$children).'</section>';
                }else{
                    echo '<section class="rtd-mega-group rtd-direct-products"><h3>Weitere Robotertypen</h3><ul>';
                    foreach($block['nodes'] as $p)echo '<li>'.self::anchor($p).'</li>';
                    echo '</ul></section>';
                }
                }
                echo '</div>';
            }
            echo '</div></div></details>';
        }
        echo '</nav></div></div>';
        echo '<div class="rtd-utils"><div class="rtd-utils-inner">'.self::utility().'</div></div>';
        echo '</header>';
        if(!$tree['roots']&&current_user_can('manage_options'))echo '<p class="rtd-missing">Keine veroeffentlichten Robotik-Seiten gefunden.</p>';
    }
    /** Vertiefende WordPress-Kategorien are shown below exactly their product page. */
    public static function product_categories(string $content):string {
        if(is_admin() || !function_exists('is_singular') || !is_singular('page') ||
            !function_exists('in_the_loop') || !in_the_loop() ||
            !function_exists('is_main_query') || !is_main_query()) return $content;
        $page=function_exists('get_queried_object_id')?(int)get_queried_object_id():0;
        if($page<1 || (string)get_post_meta($page,'_robotik_page_role',true)!=='product')return $content;
        $terms=get_terms(['taxonomy'=>'category','hide_empty'=>false,'meta_query'=>[
            ['key'=>'_robotik_product_page_id','value'=>$page,'compare'=>'=','type'=>'NUMERIC']
        ]]);
        if(!is_array($terms) || !$terms)return $content;
        usort($terms,static fn($a,$b)=>strnatcasecmp((string)get_term_meta((int)$a->term_id,'_robotik_short_label',true),(string)get_term_meta((int)$b->term_id,'_robotik_short_label',true)));
        $html='<section class="rtd-product-categories" aria-label="Robotertyp vertiefen"><h2>Zum Robotertyp</h2><ul>';
        foreach($terms as $term){
            $label=(string)get_term_meta((int)$term->term_id,'_robotik_short_label',true);
            if($label==='')$label=(string)$term->name;
            // Empty WordPress category archives should not create misleading SEO links.
            $html.='<li>';
            if((int)$term->count>0){
                $url=get_term_link($term,'category');
                if(!is_wp_error($url))$html.='<a href="'.esc_url((string)$url).'">'.esc_html($label).'</a>';
                else $html.='<span>'.esc_html($label).'</span>';
            }else{$html.='<span>'.esc_html($label).'</span>';}
            $html.='</li>';
        }
        return $content.$html.'</ul></section>';
    }
    public static function header():void {
        if(is_admin()||is_feed()||self::$header_rendered)return;
        self::$header_rendered=true;self::render_header();
    }
    public static function footer():void {
        if(is_admin()||is_feed()||self::$footer_rendered)return;
        self::$footer_rendered=true;
        if(!self::$header_rendered)self::header();
        // The category tree belongs ONLY to the top Mega Menu, not in the footer.
        echo '<footer id="robotik-strukturfuss" class="rtd-footer" role="contentinfo">';
        echo '<div class="rtd-footer-inner"><div class="rtd-footer-header"><strong>ROBOTIK</strong><span>Einfacher Test-Footer</span></div>';
        echo '<div class="rtd-footer-bottom"><div class="rtd-footer-utils">'.self::utility().'</div><div class="rtd-legal">';
        foreach([['Impressum','impressum'],['Datenschutz','datenschutzerklaerung']] as [$label,$slug]){
            $page=get_page_by_path($slug,OBJECT,'page');
            if($page&&self::permitted($page))echo '<a href="'.esc_url(self::link($page)).'">'.esc_html($label).'</a>';
        }
        echo '</div><span class="rtd-version" aria-label="Designversion">Strukturansicht '.esc_html(self::VERSION).'</span></div></div></footer>';
    }

}
Robotik_Strukturdesign::boot();