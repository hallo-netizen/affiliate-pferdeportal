#!/usr/bin/env python3
"""RC27: fix only the *proven* RC26 selection bug. A feed name, or zero from
iPN metadata, does not prove real topic/product coverage. Keep explicit,
authorized source; show both actual API metrics and previous imported rows.
"""
from pathlib import Path
from io import BytesIO
from hashlib import sha256
from zipfile import ZipFile
R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
old=P.read_bytes()
assert sha256(old).hexdigest()=="9dc124b48dead1d56b4ec8be89151e69c8d6fd94883610f460fde3624135898b", "Only the successful RC26 is allowed as base"
base="affiliate-portal-router/"
trait=base+"includes/trait-ppar-idealo.php"
main=base+"affiliate-portal-router.php"
readme=base+"readme.txt"
def once(text,old,new):
    assert text.count(old)==1,(text.count(old),old[:170])
    return text.replace(old,new,1)
with ZipFile(BytesIO(old)) as z:
    assert z.testzip() is None and len(z.namelist())==36
    content={it.filename:z.read(it.filename) for it in z.infolist()}
    t=content[trait].decode()
    t=once(t,
        "        if (count($standards)===1) $selected=$standards[0];",
        """        // RC27: DO NOT override an explicitly authorized non-test feed
        // because ANOTHER feed happens to be named Standard. The true Hab
        // example has 2901 'Standard' with API count 0, despite 1949 real
        // products in the previous import; 2747 'Fashion, Sport, Outdoor'
        // reports 548821 but thematic suitability is not yet proven.
        if (!$selected && count($standards)===1
            && absint($standards[0]['number_of_products']??0)>0) {
            $selected=$standards[0];
        }""")
    t=once(t,
        """        $settings['api_last_message']='Partner-API PASS: Standardfeed '.(string)$selected['feed_id'].' geprüft.';""",
        """        $settings['api_last_message']='Partner-API PASS: Feed '.(string)$selected['feed_id'].' geprüft.'
            .' API-Meldung: '.absint($selected['number_of_products']).' Produkte.'
            .' Letzter tatsächlicher Import: '.absint($settings['last_import_count']??0)
            .' Produkte (frühere Herkunft nicht rückwirkend belegbar).';""")
    t=once(t,
        """        $message='iPN: '.(string)$selected['name'].' – Feed '.(string)$selected['feed_id'].
            ', '.absint($selected['number_of_products']).' Produkte (Adspace 568944). Mock/Test nicht importiert.';""",
        """        $message='iPN: '.(string)$selected['name'].' – Feed '.(string)$selected['feed_id'].
            ', '.absint($selected['number_of_products']).' Produkte laut API; '.
            absint($settings['last_import_count']??0).
            ' beim letzten echten Import. API-Zähler und Import sind verschiedene Messungen. Mock/Test ausgeschlossen.';""")
    oldfield='''<p><label>Eigene Hab-&amp;-Bewahr-Feed-ID<br><input type="text" inputmode="numeric" name="ppar_provider[idealo][feed_id]" value="<?php echo esc_attr((string)$s['feed_id']); ?>"></label></p>'''
    newfield=r'''<p><label>iPN-Produktfeed (nur für Hab & Bewahr freigegebene Quellen)<br>
            <select name="ppar_provider[idealo][feed_id]">
            <?php $safe_feeds=array();
            foreach ((array)($s['api_feed_inventory']??array()) as $entry) {
                if (!is_array($entry) || !empty($entry['mock'])) continue;
                $safe_feeds[(string)($entry['feed_id']??'')]=$entry;
            }
            if (empty($safe_feeds)): ?>
                <option value="<?php echo esc_attr((string)$s['feed_id']); ?>"><?php echo esc_html('Bisheriger Feed '.$s['feed_id'].' – noch kein vollständiger Quellenvergleich'); ?></option>
            <?php else: foreach ($safe_feeds as $entry): ?>
                <option value="<?php echo esc_attr((string)$entry['feed_id']); ?>" <?php selected((string)$s['feed_id'],(string)$entry['feed_id']); ?>>
                  <?php echo esc_html((string)$entry['name'].' – Feed '.(string)$entry['feed_id'].' – '.absint($entry['number_of_products']).' Produkte laut API'); ?>
                </option>
            <?php endforeach; endif; ?>
            </select></label>
            <span class="description">Die API-Produktzahl allein sagt nichts über passende Sicherheitsprodukte. Ein Feedwechsel setzt die bisherige Ausgabe bis zum erfolgreichen Import aus.</span></p>'''
    t=once(t,oldfield,newfield)
    t=once(t,
        "          · <?php echo absint($entry['number_of_products']); ?> Produkte",
        "          · <?php echo absint($entry['number_of_products']); ?> Produkte laut Partner-API<?php if ((int)$entry['number_of_products']===0): ?> (kein Nachweis, dass die Download-Datei leer ist)<?php endif; ?>")
    t=once(t,
        "<p>Nur Feeds, die die Partner-API für die Hab-&-Bewahr-Werbefläche gemeldet hat. Keine Schätzungen aus dem Idealo-Gesamtsortiment.</p>",
        "<p>Nur Feeds, die die Partner-API für die Hab-&-Bewahr-Werbefläche gemeldet hat. Zahlen laut API sind nicht die Zahl der passenden Produkte im realen Import.</p><p><strong>Letzter tatsächlicher Import:</strong> <?php echo absint($s['last_import_count']??0); ?> passende Produkte; <?php echo absint($s['last_feed_rows_seen']??0); ?> eingelesene Feedzeilen. Das sind keine Produktzahlen je Feed – vor RC27 wurde die Feed-Herkunft nicht gesondert mitgespeichert.</p>")
    content[trait]=t.encode()
    m=content[main].decode()
    m=once(m,"Version: 0.1.23-rc26","Version: 0.1.24-rc27")
    content[main]=m.encode()
    rd=content[readme].decode()
    rd=once(rd,"Stable tag: 0.1.23-rc26","Stable tag: 0.1.24-rc27")
    content[readme]=rd.encode()
    touched={trait,main,readme}
    assert all(content[n]==z.read(n) for n in z.namelist() if n not in touched)
    out=BytesIO()
    with ZipFile(out,"w") as o:
        for item in z.infolist():o.writestr(item,content[item.filename])
    out=out.getvalue()
with ZipFile(BytesIO(out)) as verify:
    assert verify.testzip() is None and len(verify.namelist())==36
    assert b"Version: 0.1.24-rc27" in verify.read(main)
P.write_bytes(out)
print("RC27_BUILD_PASS",len(out),sha256(out).hexdigest())
