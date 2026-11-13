#!/usr/bin/env python3
"""RC28: fix verified Hab product-family blind spots in EXISTING category catalog.
- Use the already mapped published owner/topic page when the editorial leaf
  omits the physical product noun.
- Recognize ordinary German plural endings and actual source spelling variants.
- Preserve all original categories/URLs, product safety and partner logic.
Only HAB-004; no new architecture, table, worker, or external request.
"""
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from hashlib import sha256

ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
PLUGIN=ROOT/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
old=PLUGIN.read_bytes()
assert sha256(old).hexdigest()=="7754f9c4e16cb76f78bc3b5a5cf61110789ef55be275a23ce2ecba85c3a13485", "Unexpected, unapproved RC27 source"
prefix="affiliate-portal-router/"
bridge=prefix+"includes/class-ppar-hab-bewahr-bridge.php"
main=prefix+"affiliate-portal-router.php"
readme=prefix+"readme.txt"
def once(s,a,b):
    count=s.count(a)
    assert count==1,("RC27 anchor changed",count,a[:140])
    return s.replace(a,b,1)

with ZipFile(BytesIO(old)) as z:
    assert z.testzip() is None and len(z.namelist())==36
    f={i.filename:z.read(i.filename) for i in z.infolist()}
    b=f[bridge].decode("utf-8")
    # These existing keys do not match WordPress's already normalized German
    # product labels. Preserve old aliases to avoid unrelated changes.
    for before,after in [
        ("'feuerloscher'=>'Feuerlöscher'","'feuerloescher'=>'Feuerlöscher','feuerloscher'=>'Feuerlöscher'"),
        ("'videotursprechanlage'=>'Video-Türsprechanlage'","'video-tuersprechanlage'=>'Video-Türsprechanlage','videotuersprechanlage'=>'Video-Türsprechanlage','videotursprechanlage'=>'Video-Türsprechanlage'"),
        ("'turschloss'=>'Türschloss'","'tuerschloss'=>'Türschloss','turschloss'=>'Türschloss'"),
        ("'frostwachter'=>'Frostwächter'","'frostwaechter'=>'Frostwächter','frostwachter'=>'Frostwächter'"),
        ("'akkuladegeraet'=>'Akkuladegerät'","'akku-ladegeraet'=>'Akkuladegerät','akkuladegeraet'=>'Akkuladegerät'"),
    ]:
        b=once(b,before,after)
    b=once(b,
        "$pattern='~(?<![a-z])'.preg_quote($needle,'~').'(?![a-z])~';",
        """// End-of-word German inflections only: -e/-en/-n/-s and
                // -ien (e.g. original public WP category "Abdichtungsmaterialien").
                // Never match inside longer compounds or random brand fragments.
                $pattern='~(?<![a-z])'.preg_quote($needle,'~').'(?:ien|en|e|n|s)?(?![a-z])~';""")
    b=once(b,
        "            'recognized_product_categories'=>0,'unclassified_examples'=>array(),",
        "            'recognized_product_categories'=>0,'from_topic_page_categories'=>0,'unclassified_examples'=>array(),")
    b=once(b,
        """            $family = self::product_family($category_label);
            if ($is_insurance) {""",
        """            $family = self::product_family($category_label);
            $from_topic_page = false;
            // The WP category is an editorial article facet; its closest
            // *published* parent page is the authoritative product topic.
            // Do not guess a product if neither label identifies a real good.
            if ($family === '' && (string)($parent['id']??'') !== (string)($world['id']??'')
                && function_exists('get_post_status')
                && get_post_status((int)($parent['wp_id']??0)) === 'publish') {
                $family = self::product_family((string)($parent['name']??''));
                $from_topic_page = ($family !== '');
            }
            if ($is_insurance) {""")
    b=once(b,
        """            } else {
                $coverage_audit['recognized_product_categories']++;
            }
            $target_slug = '';""",
        """            } else {
                $coverage_audit['recognized_product_categories']++;
                if ($from_topic_page) $coverage_audit['from_topic_page_categories']++;
            }
            $target_slug = '';""")
    f[bridge]=b.encode("utf-8")
    m=f[main].decode()
    m=once(m,"Version: 0.1.24-rc27","Version: 0.1.25-rc28")
    f[main]=m.encode()
    rd=f[readme].decode()
    rd=once(rd,"Stable tag: 0.1.24-rc27","Stable tag: 0.1.25-rc28")
    f[readme]=rd.encode()
    t=f[prefix+"includes/trait-ppar-idealo.php"].decode()
    t=once(t,
        """<strong>Zu prüfen:</strong> <?php echo absint($hb_tree['unclassified_review']??0); ?> weitere Kategorien, deren Produktart bislang nicht eindeutig erkannt wurde.</p>""",
        """<strong>Zu prüfen:</strong> <?php echo absint($hb_tree['unclassified_review']??0); ?> weitere Kategorien, deren Produktart bislang nicht eindeutig erkannt wurde.
                      <strong>Über zugehörige Themenseite erkannt:</strong> <?php echo absint($hb_tree['from_topic_page_categories']??0); ?> Kategorien.</p>""")
    f[prefix+"includes/trait-ppar-idealo.php"]=t.encode()
    touched={bridge,main,readme,prefix+"includes/trait-ppar-idealo.php"}
    assert all(f[n]==z.read(n) for n in z.namelist() if n not in touched)
    out=BytesIO()
    with ZipFile(out,"w") as target:
        for item in z.infolist():target.writestr(item,f[item.filename])
    blob=out.getvalue()
with ZipFile(BytesIO(blob)) as verify:
    assert verify.testzip() is None and len(verify.namelist())==36
    assert b"Version: 0.1.25-rc28" in verify.read(main)
    assert b"from_topic_page_categories" in verify.read(bridge)
PLUGIN.write_bytes(blob)
print("HAB_RC28_KISS_BUILD_PASS",len(blob),sha256(blob).hexdigest(),"modified",sorted(touched))
