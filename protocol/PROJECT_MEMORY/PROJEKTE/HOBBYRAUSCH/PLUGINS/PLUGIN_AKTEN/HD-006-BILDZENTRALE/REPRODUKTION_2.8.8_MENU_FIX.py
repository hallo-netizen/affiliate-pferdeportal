#!/usr/bin/env python3
"""Deterministic small-scoped patch 2.8.7 -> 2.8.8; never touches media or mappings.
Usage: python REPRODUKTION_2.8.8_MENU_FIX.py HOBBY_DEPOT_BILDZENTRALE_2.8.7...zip output.zip
"""
import pathlib,zipfile,hashlib,sys
OLD='9ea589793bce56cf6407d3845086572678099a0bbfe3215098c9b116fae1df5d'
NEW='dd076c7772c820adcceabea85897a6bcfe79a47dd66430475b988d413541787a'
MAIN='hobby-depot-bildzentrale/hobby-depot-bildzentrale.php'
SUB='hobby-depot-bildzentrale/includes/class-hdbz-hobbyregister.php'
def replace_one(s,old,new):
    assert s.count(old)==1, (old[:50],s.count(old))
    return s.replace(old,new,1)
def transform(s):
    s=replace_one(s,' * Version: 2.8.7',' * Version: 2.8.8')
    s=replace_one(s,"    private const OPTION_PIXABAY = 'hdbz_pixabay_api_key';", "    private const ADMIN_MENU_SLUG = 'hdbz-bilder-erstellen'; // unique WP admin page; do NOT reuse old image-assignment slug\n    private const LEGACY_ASSIGN_MENU_SLUG = 'hobby-depot-bildzentrale'; // existing independent image-assignment screen\n    private const OPTION_PIXABAY = 'hdbz_pixabay_api_key';")
    s=replace_one(s,"        add_action('admin_menu', [self::class, 'admin_menu']);", "        add_action('admin_menu', [self::class, 'admin_menu']);\n        add_action('admin_menu', [self::class, 'clarify_legacy_assignment_menu'], 9999);")
    old="""    public static function admin_menu(): void {
        add_menu_page(
            'Hobby Depot Bildzentrale',
            'Bildzentrale',
            'manage_options',
            'hobby-depot-bildzentrale',
            [self::class, 'render_page'],
            'dashicons-format-image',
            58
        );
    }
"""
    new="""    public static function admin_menu(): void {
        // KISS: independent creation workspace, never the legacy mapping slug.
        add_menu_page(
            'Hobby Depot – Bilder erstellen',
            'Bilder erstellen',
            'manage_options',
            self::ADMIN_MENU_SLUG,
            [self::class, 'render_page'],
            'dashicons-format-image',
            58
        );
    }

    public static function clarify_legacy_assignment_menu(): void {
        // Existing mapping menu is owned by ANOTHER plugin. Change its DISPLAY name only,
        // never callback, slug, permissions, database state or menu position.
        global $menu;
        if (!is_array($menu)) { return; }
        foreach ($menu as &$entry) {
            if (!is_array($entry) || (string)($entry[2] ?? '') !== self::LEGACY_ASSIGN_MENU_SLUG) { continue; }
            if (trim(wp_strip_all_tags((string)($entry[0] ?? ''))) === 'Bildzentrale') {
                $entry[0] = 'Bilder zuordnen';
            }
        }
        unset($entry);
    }
"""
    s=replace_one(s,old,new)
    for a,b in [
        ("['page' => 'hobby-depot-bildzentrale', 'hdbz_tab' => $tab]","['page' => self::ADMIN_MENU_SLUG, 'hdbz_tab' => $tab]"),
        ("admin_url('admin.php?page=hobby-depot-bildzentrale&edit_post=' . $post_id)","admin_url('admin.php?page=' . self::ADMIN_MENU_SLUG . '&edit_post=' . $post_id)"),
        ("admin_url('admin.php?page=hobby-depot-bildzentrale&removed=1')","admin_url('admin.php?page=' . self::ADMIN_MENU_SLUG . '&removed=1')"),
        ("admin_url('admin.php?page=hobby-depot-bildzentrale&content_removed=1')","admin_url('admin.php?page=' . self::ADMIN_MENU_SLUG . '&content_removed=1')"),
        ("'page' => 'hobby-depot-bildzentrale',","'page' => self::ADMIN_MENU_SLUG,"),
        ("['page' => 'hobby-depot-bildzentrale'], admin_url('admin.php')","['page' => self::ADMIN_MENU_SLUG], admin_url('admin.php')"),
    ]: s=replace_one(s,a,b)
    assert 'page=hobby-depot-bildzentrale' not in s
    assert s.count("rest_url('hobby-depot-bildzentrale/v1/magnific-webhook')")==2
    assert "register_rest_route('hobby-depot-bildzentrale/v1'" in s
    return s
def main():
    src,dst=map(pathlib.Path,sys.argv[1:])
    assert hashlib.sha256(src.read_bytes()).hexdigest()==OLD,'source is not proven 2.8.7'
    with zipfile.ZipFile(src) as zin:
        assert zin.testzip() is None and set(zin.namelist())=={MAIN,SUB}
        s=transform(zin.read(MAIN).decode('utf8'))
        entries=[(entry,s.encode('utf8') if entry.filename==MAIN else zin.read(entry)) for entry in zin.infolist()]
    with zipfile.ZipFile(dst,'w') as z:
        for info,payload in entries:z.writestr(info,payload)
    with zipfile.ZipFile(dst) as z:
        assert z.testzip() is None and z.read(SUB)==dict((x.filename,v) for x,v in entries)[SUB]
    assert hashlib.sha256(dst.read_bytes()).hexdigest()==NEW, 'Unexpected output; abort'
    print("PASS: byte-identical vetted plugin ZIP generated",NEW)
if __name__=='__main__':main()
