#!/usr/bin/env python3
"""Rebuild HD-003 from the exact approved 1.50.794 ZIP, changing only footer links."""
import hashlib
import pathlib
import subprocess
import tempfile
import zipfile

BASE = pathlib.Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip")
DEST = pathlib.Path("dist/HOBBY_DEPOT_HD003_1.50.795_FOOTER_AGB_WERBEBEDINGUNGEN_VOLLPLUGIN.zip")
MAIN = "affiliate-portal-template-kit/pferde-template-kit.php"
PROFILE = "affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php"
EXPECTED_SHA = "52d7d67149ac09e22b7406ef59421ec7e4110c5d0efb11349e0f5357f8c4aa6f"

def replace_one(src, old, new, purpose):
    count = src.count(old)
    assert count == 1, f"{purpose} anchor expected once, found {count}"
    return src.replace(old, new, 1)

def change_profile(src):
    footer_fix = """
        // 1.50.795: AGB in Rechtliches; Werbebedingungen ausschliesslich im Service.
        $legal = array_values(array_filter($legal, static function($item) {
            $label_slug = sanitize_title((string)($item['label'] ?? ''));
            $path = parse_url((string)($item['url'] ?? ''), PHP_URL_PATH);
            $url_slug = sanitize_title((string)basename(trim((string)$path, '/')));
            return !in_array($label_slug, ['werbebedingungen', 'werb-anzeigebedingungen'], true)
                && !in_array($url_slug, ['werbebedingungen', 'werb-anzeigebedingungen'], true);
        }));
        $agb_url = self::page_link(['agb']);
        if ($agb_url !== '') {
            $agb_exists = false;
            foreach ($legal as $item) {
                $label_slug = sanitize_title((string)($item['label'] ?? ''));
                $path = parse_url((string)($item['url'] ?? ''), PHP_URL_PATH);
                $url_slug = sanitize_title((string)basename(trim((string)$path, '/')));
                if ($label_slug === 'agb' || $url_slug === 'agb') {
                    $agb_exists = true;
                    break;
                }
            }
            if (!$agb_exists) { $legal[] = ['label' => 'AGB', 'url' => $agb_url]; }
        }

"""
    legal_fallback = """        // Fail-safe nur fuer Rechtliches, falls der Import wirklich fehlt.
        if (!$legal) {
            foreach ([[['impressum'],'Impressum'],[['datenschutz'],'Datenschutz']] as $entry) {
                $url = self::page_link($entry[0]);
                if ($url !== '') { $legal[] = ['label'=>$entry[1], 'url'=>$url]; }
            }
        }
"""
    src = replace_one(src, legal_fallback, legal_fallback + footer_fix, "legal block")
    src = replace_one(src,
        "        $service = $compact([\n",
        "        $terms_url = self::page_link(['werb-anzeigebedingungen', 'werbebedingungen']);\n        $service = $compact([\n",
        "service header")
    src = replace_one(src,
        "            $make_item('Preise', $prices_url),\n            $make_item('Kontakt', $contact_url),",
        "            $make_item('Preise', $prices_url),\n            $make_item('Werbebedingungen', $terms_url),\n            $make_item('Kontakt', $contact_url),",
        "service menu")
    return src

def main():
    source_sha = hashlib.sha256(BASE.read_bytes()).hexdigest()
    assert source_sha == EXPECTED_SHA, f"Unexpected source version: {source_sha}"
    with zipfile.ZipFile(BASE) as source:
        assert source.testzip() is None
        infos = source.infolist()
        assert len(infos) == 1290, len(infos)
        contents = {i.filename: source.read(i.filename) for i in infos}
    assert len(contents) == len(infos), "Duplicate archive paths"
    assert MAIN in contents and PROFILE in contents
    altered = contents.copy()
    for name in (MAIN, PROFILE):
        src = altered[name].decode("utf-8")
        if name == PROFILE:
            src = change_profile(src)
        assert "1.50.794" in src, f"Missing source version in {name}"
        altered[name] = src.replace("1.50.794", "1.50.795").encode("utf-8")
    changed = [name for name in contents if contents[name] != altered[name]]
    assert set(changed) == {MAIN, PROFILE}, changed
    DEST.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DEST, "w") as destination:
        for info in infos:
            destination.writestr(info, altered[info.filename])
    with zipfile.ZipFile(DEST) as check:
        assert check.testzip() is None
        assert check.namelist() == [i.filename for i in infos]
        assert all(check.read(k) == contents[k] for k in contents if k not in (MAIN, PROFILE))
        with tempfile.TemporaryDirectory() as tmp:
            for name in (MAIN, PROFILE):
                path = pathlib.Path(tmp) / pathlib.Path(name).name
                path.write_bytes(check.read(name))
                result = subprocess.run(["php", "-l", str(path)], capture_output=True, text=True)
                assert result.returncode == 0, result.stdout + result.stderr
    result_sha = hashlib.sha256(DEST.read_bytes()).hexdigest()
    print("PASS: input SHA+CRC / 1290 files / only two edited PHP files / PHP syntax / no changed other files")
    print("RELEASE_SHA256=", result_sha)
    print("RELEASE_SIZE=", DEST.stat().st_size)

if __name__ == "__main__":
    main()
