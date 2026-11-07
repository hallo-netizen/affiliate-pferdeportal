#!/usr/bin/env python3
"""Test real PHP output of the consolidated banner code; no WordPress/database writes."""
from pathlib import Path
import tempfile,zipfile,hashlib,subprocess
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH")
path=root/"PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip"
hd003=root/"PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip"
main="affiliate-portal-router/hobby-depot-affiliate-router.php"
css="affiliate-portal-router/assets/hdar-amazon-start.css"
pairs={
"affiliate-portal-router/assets/hdar-ci-logo-original.png":"affiliate-portal-template-kit/assets/hobby-depot-v150617/eigenwerbung-v150790/logo-original-ohne-unterzeile.png",
"affiliate-portal-router/assets/hdar-ci-malen-zeichnen.webp":"affiliate-portal-template-kit/assets/hobby-depot-v150617/hero-masters-v150684/malen-zeichnen.webp",
"affiliate-portal-router/assets/hdar-ci-modellbau.webp":"affiliate-portal-template-kit/assets/hobby-depot-v150617/hero-masters-v150684/modellbau.webp"}
with zipfile.ZipFile(path) as z,zipfile.ZipFile(hd003) as design:
    assert z.testzip() is None
    entries={i.filename:z.read(i.filename) for i in z.infolist() if not i.is_dir()}
    for target,source in pairs.items():
        assert entries[target]==design.read(source),target+" NOT Original"
s=entries[main].decode("utf-8")
assert s.count("Version: 0.1.18-dev")==1
assert "hdar_approved_rental_banner_fallback" not in s
assert "hdar_ci_register_footer" in s
assert "hdar-ci-logo-original.png" not in s
assert "Entdecke deine Ausrüstung" not in s
assert "hdar-amazon-available-at-amazon-de-official.png" in s
assert "hdar-ci-amazon-arrow" in s
assert "html_entity_decode($topic" in s
assert "hdar-ci-amazon-slot" in s
assert "array('glossary_single_banner','glossary_single_desktop_banner','glossary_single_mobile_banner'), true);" in s, "Glossar own banner must be square desktop AND mobile"
assert "if ($post_id === 0 && is_numeric($content_id))" in s, "Posts use native content ID for right picture"
# Original HD007 uses canonical_name (never 'name') and image_entry source/path.
assert "($register_row['canonical_name'] ?? '')" in s, "register banner topic must use original canonical_name"
assert "($item['canonical_name'] ?? '')" in s, "register router must match original canonical_name"
assert "$name=(string)$row['canonical_name'];" in s
assert "($entry['path'] ?? '')" in s and "($entry['source'] ?? '')" in s
assert "hd-hobbyregister-core/assets/" in s and "affiliate-portal-template-kit/assets/" in s
assert "strpos($production, 'OPEN') !== 0" in s, "unapproved HD007 image must not become advertising"
assert s.count("add_action('wp_footer', array($this, 'hdar_ci_register_footer'), 55);")==1
assert "overview_wide_banner_campaign_eligible" in s
assert "'ratio_min'=>5.00,'ratio_max'=>12.00" in s
assert "campaign_matches_contract_slot_rule" in s
assert "HDAR_Amazon_Start::render_slot" in s
assert s.index("select_campaign_for_slot($context, $slot_type") < s.index("if ($launch) {\n            $house = $this->hdar_ci_amazon_banner(")
c=entries[css].decode('utf8')
assert "aspect-ratio:4.2/1" in c and "aspect-ratio:1/1" in c
assert ".hd-next-partner-banner:has(.hdar-ci-amazon-slot)" in c
assert "object-fit:contain" in c and "overflow:visible" in c
assert "Erhältlich bei Amazon" in s
assert "Hier könnte Ihre Werbung stehen" not in s
start=s.index("    private function hdar_ci_amazon_banner(")
end=s.index("    /** HD007 owns",start)
method=s[start:end]
assert "mb_strtolower" not in method, "PHP mbstring is optional"
harness=r'''<?php
error_reporting(E_ALL);
function sanitize_key($s){return strtolower(preg_replace("/[^a-z0-9_-]/i","",(string)$s));}
function sanitize_text_field($s){return strip_tags((string)$s);}
function sanitize_title($s){$s=strtolower(str_replace("&"," ",$s));return trim(preg_replace("/-+/","-",preg_replace("/[^a-z0-9]+/","-",$s)),"-");}
function esc_attr($s){return htmlspecialchars((string)$s,ENT_QUOTES);}
function esc_html($s){return htmlspecialchars((string)$s,ENT_QUOTES);}
function esc_url($s){return htmlspecialchars((string)$s,ENT_QUOTES);}
function esc_url_raw($s){return (string)$s;}
function absint($n){return abs((int)$n);}
function plugin_dir_path($p){return dirname($p)."/";}
function plugins_url($p,$file){return "https://hobby-depot.de/wp-content/plugins/affiliate-portal-router/".ltrim($p,"/");}
function wp_parse_url($s,$x){return parse_url((string)$s,$x);}
function get_the_post_thumbnail_url($id,$size){return false;}
class HDAR_Amazon_Start {
    public static $launch=true;
    public static function launch_active(){return self::$launch;}
}
class Audit {
    public static $active=true;
    public static $amazon_ready=true;
    private function is_enabled(){return self::$active;}
    private function overview_wide_banner_slot($slot){
        return in_array($slot,array('start_after_topics','hub_after_cards','product_after_category_tiles','category_recommendation','glossary_overview_banner','journal_banner'),true);
    }
    private function amazon_settings(){return array('enabled'=>self::$amazon_ready,'tracking_id'=>'hobbydepot-21');}
'''
harness+=method
harness+=r'''
    public function try_banner($name,$slot) {
        return $this->hdar_ci_amazon_banner(array('primary_name'=>$name,'post_id'=>0),$slot,'check',null);
    }
}
function check($pass,$message){if(!$pass){fwrite(STDERR,"FAILED: ".$message."\n");exit(2);}echo "PASS ".$message."\n";}
$a=new Audit();
$wide=$a->try_banner("Malen & Zeichnen","product_after_category_tiles");
check(strpos($wide,'hdar-ci-amazon-banner-wide')!==false,"native wide category slot");
check(strpos($wide,'hdar-ci-logo-original.png')===false,"no own logo");
check(strpos($wide,'Entdecke deine Ausrüstung')===false,"no redundant slogan");
check(strpos($wide,'hdar-amazon-available-at-amazon-de-official.png')!==false,"exact approved German Amazon asset");
check(strpos($wide,'hdar-ci-amazon-arrow')!==false,"arrow in yellow CTA");
check(strpos($wide,'hdar-ci-malen-zeichnen.webp')!==false,"correct painting picture");
check(strpos($wide,'amazon.de/s?k=')!==false&&strpos($wide,'tag=hobbydepot-21')!==false,"real tracking search URL");
check(strpos($wide,'hdar-ci-content')<strpos($wide,'hdar-ci-photo'),"slim title precedes large photo");
check(strpos($wide,'Malen')!==false && strpos($wide,'Zeichnen')!==false,"correct hobby title");
check(strpos($wide,'Hier könnte Ihre Werbung stehen')===false,"no rental banner");
check($a->try_banner("Malen & Zeichnen","product_after_category_tiles")==='',"max 1 wide on page");
$square=$a->try_banner("Modellbau","glossary_single_desktop_banner");
check(strpos($square,'hdar-ci-amazon-banner-square')!==false,"square glossary desktop");
check(strpos($square,'hdar-ci-modellbau.webp')!==false,"matching modelbuilding picture");
check($a->try_banner("Astronomie","glossary_single_desktop_banner")==='',"fail closed for topic without image");
check($a->try_banner("Hobbyregister","glossary_single_desktop_banner")==='',"no nonspecific register-index ad");
HDAR_Amazon_Start::$launch=false;
check($a->try_banner("Modellbau","glossary_single_desktop_banner")==='',"launch mode off");
HDAR_Amazon_Start::$launch=true;
Audit::$amazon_ready=false;
check($a->try_banner("Modellbau","glossary_single_desktop_banner")==='',"invalid credentials block own promo");
Audit::$amazon_ready=true;
Audit::$active=false;
check($a->try_banner("Modellbau","glossary_single_desktop_banner")==='',"plugin off blocks own promo");
echo "ALL 11 POSITIVE/NEGATIVE PHP CASES PASS\n";
'''
with tempfile.TemporaryDirectory() as tmp:
    out=Path(tmp)/"affiliate-portal-router"
    out.mkdir()
    for n,data in entries.items():
        if n.endswith((".php",".png",".webp",".css")):
            dest=Path(tmp)/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    dest=out/"ci-test-runtime.php"
    dest.write_text(harness,encoding="utf8")
    check=subprocess.run(["php","-l",str(dest)],capture_output=True,text=True)
    assert check.returncode==0,(check.stdout,check.stderr)
    check=subprocess.run(["php",str(dest)],capture_output=True,text=True)
    assert check.returncode==0,(check.stdout,check.stderr)
    print(check.stdout)
assert len(entries)==33
badge=entries["affiliate-portal-router/assets/hdar-amazon-available-at-amazon-de-official.png"]
assert hashlib.sha256(badge).hexdigest()=="fb6db85f898078fa6df03740b58d65f431b8a6186c97f6b8a72e95f11b9ab8e5"
assert "affiliate-portal-router/assets/hdar-ci-logo-original.png" not in entries
print("CI FULL QA PASS - ZIP:",hashlib.sha256(path.read_bytes()).hexdigest(),"bytes",path.stat().st_size)
