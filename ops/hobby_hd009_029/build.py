#!/usr/bin/env python3
"""HD009 0.1.29: real article Amazon cards only with authorized product images.
The original product store, ASIN approval, exact WP post targets, tracking ID
and CSS remain authoritative. No new table/plugin, no paid API call, no
imageless fallback and no change to the approved HD003 1.50.806 design.
"""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from tempfile import TemporaryDirectory
from hashlib import sha256
import subprocess
ROOT=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE')
SOURCE=ROOT/'HOBBY_DEPOT_AFFILIATE_HD009_0.1.28.zip'
CURRENT=ROOT/'CURRENT.zip'
TARGET=ROOT/'HOBBY_DEPOT_AFFILIATE_HD009_0.1.29.zip'
EXPECTED='ad4685633516cde1f22af21a2d8ecc92965bab658f7a9411f287c58f85bb39cd'
MAIN='affiliate-portal-router/hobby-depot-affiliate-router.php'
CLASS='affiliate-portal-router/includes/class-hdar-amazon-start.php'
CSS='affiliate-portal-router/assets/hdar-amazon-start.css'
assert sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED,"Unexpected original ZIP: stop"
def one(s,old,new,where):
    count=s.count(old)
    assert count==1,(where,count,old[:150])
    return s.replace(old,new)

with ZipFile(SOURCE) as z:
    assert z.testzip() is None and len(z.namelist())==41
    m=z.read(MAIN).decode()
    cls=z.read(CLASS).decode()
    css=z.read(CSS).decode()
m=one(m,' * Version: 0.1.28',' * Version: 0.1.29','main header')
cls=one(cls,"'0.1.28'","'0.1.29'","CSS cache version")
cls=one(cls,
    "        add_action('admin_post_hdar_amazon_remove', array(__CLASS__, 'remove'));",
    "        add_action('admin_post_hdar_amazon_remove', array(__CLASS__, 'remove'));\n"
    "        add_action('admin_post_hdar_amazon_image', array(__CLASS__, 'save_image'));\n"
    "        add_filter('the_content', array(__CLASS__, 'render_article_cards'), 1350);",
    "single Bootstrap")
begin=cls.index('    private static function product_card(')
end=cls.index('    public static function enqueue()',begin)
assert begin<end
replacement=r'''
    /** Product photo is an existing WP image with an explicit use-rights
     * confirmation from the portal owner. Never copy DataForSEO/Amazon
     * image URLs or render a text-only substitute. */
    private static function verified_image($item) {
        if (!is_array($item) ||
            (string)($item['image_source'] ?? '') !== 'own_or_licensed') { return ''; }
        $id = absint($item['image_id'] ?? 0);
        if (!$id || !function_exists('wp_attachment_is_image') ||
            !wp_attachment_is_image($id)) { return ''; }
        $src = wp_get_attachment_image_url($id, 'medium_large');
        return is_string($src) && $src !== '' ? $src : '';
    }

    private static function product_card($match, $position, $slot = 'category_product_1') {
        $items = array_values((array)($match['data']['items'] ?? array()));
        $item = $items[$position-1] ?? null;
        if (!is_array($item) ||
            !preg_match('/^[A-Z0-9]{10}$/D',(string)($item['asin'] ?? ''))) { return ''; }
        $img = self::verified_image($item);
        $tag = self::tracking_id();
        if ($tag === '' || $img === '') { return ''; }
        $asin = $item['asin'];
        $url = 'https://www.amazon.de/dp/'.rawurlencode($asin).'?tag='.rawurlencode($tag);
        $title = trim((string)($item['title'] ?? ''));
        if ($title === '') { return ''; }
        return '<article class="ppar-affiliate-slot hdar-amazon-product hdar-amazon-photo-product" data-ppar-slot="'.esc_attr($slot).'">'
            .'<a class="hdar-amazon-photo-link" href="'.esc_url($url).'" rel="sponsored nofollow noopener" target="_blank">'
            .'<img src="'.esc_url($img).'" alt="'.esc_attr($title).'" loading="lazy" decoding="async">'
            .'</a><h3>'.esc_html($title).'</h3>'
            .'<a class="hdar-amazon-button" href="'.esc_url($url).'" rel="sponsored nofollow noopener" target="_blank">'
            .'Bei Amazon ansehen</a></article>';
    }

    /** One article product area, attached to the existing full-article content.
     * Works inside the Hab-inspired right column if it exists. Otherwise
     * it is an ordinary responsive block at the end of a standard article.
     * An existing product section always wins: never duplicate product boxes.
     */
    public static function render_article_cards($content) {
        if (!is_string($content) || !self::launch_active() || is_admin() ||
            is_feed() || !is_singular('post') || !in_the_loop() || !is_main_query()) {
            return $content;
        }
        $id = absint(get_the_ID());
        if (!$id || post_password_required($id) ||
            (string)get_post_status($id) !== 'publish') { return $content; }
        if (strpos($content,'hdar-amazon-article-products') !== false ||
            strpos($content,'ppar-article-products') !== false ||
            strpos($content,'post_bottom_products') !== false) { return $content; }
        $key = 'post:'.$id;
        $stored = self::products();
        if (empty($stored[$key]['items'])) { return $content; }
        $match = array('key'=>$key,'data'=>$stored[$key]);
        $cards = array();
        for ($pos=1; $pos<=3; $pos++) {
            $html = self::product_card($match,$pos,'article_product_'.$pos);
            if ($html !== '') { $cards[]=$html; }
        }
        if (!$cards) { return $content; }
        $section='<section class="hdar-amazon-article-products" aria-label="Passende Amazon-Produkte">'
            .'<span class="hdar-amazon-label">Anzeige</span>'
            .'<h2>Passende Ausrüstung</h2>'
            .'<div class="hdar-amazon-article-grid">'.implode('',$cards).'</div></section>';
        // Do not alter HD003's markup; inject inside the one approved sidebar
        // when it exists, without requiring a change to the design plugin.
        $needle='<aside class="hd-article-sidebar-v150804"';
        $at=strpos($content,$needle);
        if ($at!==false) {
            $close=strpos($content,'>',$at);
            if ($close!==false) {
                return substr($content,0,$close+1).$section.substr($content,$close+1);
            }
        }
        return $content."\n".$section;
    }

'''
cls=cls[:begin]+replacement+cls[end:]
image_method=r'''
    /** Only portal-owned or separately licensed photographs from the
     * existing WordPress Media Library can be attached here.
     * There is no automatic approval of rights or product identity. */
    public static function save_image() {
        self::guard('hdar_amazon_image');
        $key=sanitize_text_field(wp_unslash((string)($_POST['hdar_key'] ?? '')));
        $asin=strtoupper(sanitize_text_field(wp_unslash((string)($_POST['hdar_asin'] ?? ''))));
        $id=absint($_POST['hdar_image_id'] ?? 0);
        if (!preg_match('/^(?:post:[0-9]+|term:[a-z0-9_-]+:[0-9]+)$/D',$key) ||
            !preg_match('/^[A-Z0-9]{10}$/D',$asin)) { self::back('target'); }
        $all=self::products();
        if (empty($all[$key]['items']) || !is_array($all[$key]['items'])) {
            self::back('expired');
        }
        $index=null;
        foreach ($all[$key]['items'] as $i=>$item) {
            if (($item['asin'] ?? '')===$asin) { $index=$i; break; }
        }
        if ($index === null) { self::back('expired'); }
        if ($id!==0) {
            if (empty($_POST['hdar_image_rights']) ||
                !current_user_can('edit_post',$id) ||
                !wp_attachment_is_image($id) ||
                !wp_get_attachment_image_url($id,'medium_large')) {
                self::back('image_rights');
            }
            $all[$key]['items'][$index]['image_id']=$id;
            $all[$key]['items'][$index]['image_source']='own_or_licensed';
        } else {
            // Explicit 0 removes the link, so an image can be withdrawn.
            unset($all[$key]['items'][$index]['image_id'],
                  $all[$key]['items'][$index]['image_source']);
        }
        update_option(self::PRODUCTS_OPTION,$all,false);
        self::back($id ? 'image_saved' : 'image_removed');
    }

'''
cls=one(cls,'    public static function remove() {',image_method+'    public static function remove() {','image save entry')
# Add a native WP Media picker for one approved product; no JS library/plugin.
cls=one(cls,
"        $creds = self::credentials();$ready = self::tracking_id()!=='';",
"        $creds = self::credentials();$ready = self::tracking_id()!=='';\n"
"        if (function_exists('wp_enqueue_media')) { wp_enqueue_media(); }",
"media library")
cls=one(cls,
"          'limit'=>'Maximal drei ausgewählte Produkte pro Hobby-Ziel.', 'removed'=>'Produktzuordnung entfernt.',",
"          'limit'=>'Maximal drei ausgewählte Produkte pro Hobby-Ziel.', 'removed'=>'Produktzuordnung entfernt.',\n"
"          'image_saved'=>'Das freigegebene Produktfoto ist zugeordnet.',\n"
"          'image_removed'=>'Produktfoto-Verknüpfung entfernt.',\n"
"          'image_rights'=>'Nur ein echtes WordPress-Bild mit bestätigten Nutzungsrechten ist zulässig.',",
"admin messages")
cls=one(cls,
"        <p>Amazon und idealo können getrennt Produkte liefern. Weitere Partner bleiben gespeichert. DataForSEO-Recherche erfolgt nur nach Klick. Banner und ihre automatische Themen-/Formatzuordnung laufen über die bestehende zentrale Affiliate-Automatik.</p>",
"        <p>Amazon und idealo können getrennt Produkte liefern. Weitere Partner bleiben gespeichert. DataForSEO-Recherche erfolgt nur nach Klick. Banner und ihre automatische Themen-/Formatzuordnung laufen über die bestehende zentrale Affiliate-Automatik.</p>\n"
"        <p><strong>Artikel-Produktboxen:</strong> Ein freigegebenes Produkt erscheint nur, wenn ein eigenes oder ausdrücklich lizenziertes echtes Produktfoto in der WordPress-Mediathek zugeordnet wurde. Keine kopierten Amazon- oder DataForSEO-Produktfotos.</p>",
"admin explanation")
needle="          <button class=\"button\">Entfernen</button></form><?php endforeach; ?><?php endforeach; ?>"
assert needle in cls
new=r'''          <button class="button">Entfernen</button></form>
          <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="margin:6px 0 18px;padding:10px;border:1px solid #dcdcde">
            <input type="hidden" name="action" value="hdar_amazon_image">
            <input type="hidden" name="hdar_key" value="<?php echo esc_attr($key); ?>">
            <input type="hidden" name="hdar_asin" value="<?php echo esc_attr($item['asin']); ?>">
            <?php wp_nonce_field('hdar_amazon_image'); ?>
            <strong>Artikelbild:</strong> <?php echo !empty($item['image_id']) && self::verified_image($item) !== '' ? 'gültig hinterlegt' : 'fehlt – Produktbox wird nicht ausgegeben'; ?>
            <p><label>Medien-ID <input class="small-text hdar-own-product-photo-id" name="hdar_image_id" type="number" min="0" value="<?php echo esc_attr((string)absint($item['image_id'] ?? 0)); ?>"></label>
            <button type="button" class="button hdar-choose-product-photo">Bild aus Mediathek wählen</button></p>
            <p><label><input type="checkbox" name="hdar_image_rights" value="1">
            Ich bestätige, dass dieses Foto das Produkt korrekt zeigt und ich die Nutzungsrechte für die Werbeverwendung habe. Keine ungeprüft kopierten Amazon- oder DataForSEO-Bilder.</label></p>
            <button class="button button-primary">Produktfoto speichern</button>
            <small>Mit Medien-ID 0 wird eine vorhandene Bildzuordnung entfernt.</small>
          </form><?php endforeach; ?><?php endforeach; ?>
          <script>
          document.addEventListener('click',function(event){
            var button=event.target.closest('.hdar-choose-product-photo');
            if(!button||!window.wp||!wp.media)return;
            event.preventDefault();
            var input=button.closest('form').querySelector('.hdar-own-product-photo-id');
            var frame=wp.media({title:'Eigenes Produktfoto auswählen',button:{text:'Übernehmen'},multiple:false,library:{type:'image'}});
            frame.on('select',function(){
              var selected=frame.state().get('selection').first();
              if(selected)input.value=selected.get('id');
            });
            frame.open();
          });
          </script>'''
cls=one(cls,needle,new,"save original admin forms")
css += r'''

/* 0.1.29 – true Amazon article boxes with permitted WP-owned images only.
   Existing Hugo/Hobbyregister/hero banner styles are unaffected. */
.hdar-amazon-article-products{
  box-sizing:border-box;max-width:100%;margin:25px 0;
  border:1px solid #d7e7e3;border-radius:6px;padding:17px;
  background:#f7faf8;color:#23454a
}
.hdar-amazon-article-products>.hdar-amazon-label{
  display:block;font-size:11px;font-weight:600;color:#596b6d;
  margin:0 0 8px
}
.hdar-amazon-article-products>h2{
  font-family:Montserrat,'Segoe UI',Arial,sans-serif;
  font-size:19px!important;line-height:1.3!important;
  color:#1b4047;margin:0 0 14px!important;padding:0!important;
}
.hdar-amazon-article-grid{
  display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,170px),1fr));
  gap:12px;max-width:100%
}
.hdar-amazon-article-grid .hdar-amazon-photo-product{
  box-sizing:border-box;min-width:0;margin:0!important;padding:12px;
  border:1px solid #dde7e2;border-radius:4px;background:white;
  display:flex;flex-direction:column;gap:10px;overflow:hidden;
}
.hdar-amazon-article-grid .hdar-amazon-photo-link{
  display:block;width:100%;aspect-ratio:4/3;background:#f7f8f6;
  border-radius:3px;overflow:hidden;
}
.hdar-amazon-article-grid .hdar-amazon-photo-link img{
  display:block;max-width:100%;width:100%;height:100%;
  object-fit:contain;object-position:center;
}
.hdar-amazon-article-grid h3{
  font-family:Montserrat,'Segoe UI',Arial,sans-serif;
  font-size:14px!important;line-height:1.38!important;font-weight:700;
  margin:0!important;padding:0!important;color:#173e45;
  overflow-wrap:anywhere
}
.hdar-amazon-article-grid .hdar-amazon-button{
  display:block!important;max-width:100%;margin-top:auto!important;
  background:#e7ae62!important;color:#283c3a!important;
  padding:10px 12px!important;border-radius:4px!important;
  font-size:12px!important;line-height:1.3!important;
  font-family:Montserrat,'Segoe UI',Arial,sans-serif!important;
  text-align:center;text-decoration:none!important;font-weight:700;
}
@media(max-width:700px){
 .hdar-amazon-article-products{padding:14px 11px;margin:20px 0}
 .hdar-amazon-article-grid{grid-template-columns:1fr;gap:10px}
 .hdar-amazon-article-grid .hdar-amazon-photo-product{
    display:grid;grid-template-columns:95px minmax(0,1fr);gap:7px 12px;
    align-items:center;
 }
 .hdar-amazon-article-grid .hdar-amazon-photo-link{
    grid-row:1 / span 2;aspect-ratio:1;
 }
 .hdar-amazon-article-grid .hdar-amazon-button{grid-column:2;margin:0!important}
}
'''
out=BytesIO();changed=[]
with ZipFile(SOURCE) as z,ZipFile(out,'w') as w:
    for item in z.infolist():
        old=z.read(item.filename)
        new=(m.encode() if item.filename==MAIN else cls.encode() if item.filename==CLASS
             else css.encode() if item.filename==CSS else old)
        if old!=new:changed.append(item.filename)
        w.writestr(item,new)
    w.comment=z.comment
assert set(changed)=={MAIN,CLASS,CSS},changed
data=out.getvalue()
with ZipFile(BytesIO(data)) as z:
    assert len(z.namelist())==41 and z.testzip() is None
    files=[n for n in z.namelist() if n.endswith('.php')]
    assert len(files)==24
    with TemporaryDirectory() as td:
        for name in files:
            file=Path(td)/name
            file.parent.mkdir(parents=True,exist_ok=True)
            file.write_bytes(z.read(name))
            result=subprocess.run(['php','-l',str(file)],capture_output=True,text=True)
            assert result.returncode==0,(name,result.stderr)
CURRENT.write_bytes(data)
TARGET.write_bytes(data)
assert CURRENT.read_bytes()==TARGET.read_bytes()
print('HD009_029_BUILD_PASS',len(data),sha256(data).hexdigest(),'PHP',24,'ZIP',41,'MODIFIED',changed)
