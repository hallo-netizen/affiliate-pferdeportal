#!/usr/bin/env python3
"""HAB-004 RC32: actual display-root fixes, NOT another architecture.
Proof: live pages render HB insurance placeholder (design bridge OK), but real
Tarifcheck is absent. RC31's automatic banner-to-branch record is dropped on
subsequent materialization; provider=manual originals are rejected by the
insurance campaign gate even when explicitly saved as Tarifcheck.
Keep verified dimensions/format gates, data, assets, exact category safety.
"""
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from hashlib import sha256

ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=ROOT/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
raw=P.read_bytes()
assert sha256(raw).hexdigest()=="fa72cf9519ccaf92c672581eff35a8e4908a3f15511a1ef5f272448a36c99d56","Only verified RC31 ZIP is allowed"
prefix="affiliate-portal-router/"
main=prefix+"affiliate-portal-router.php"
output=prefix+"includes/trait-ppar-output-objects.php"
readme=prefix+"readme.txt"
def once(s,a,b):
    n=s.count(a)
    assert n==1,("RC31 anchor unexpectedly changed",n,a[:180])
    return s.replace(a,b,1)

with ZipFile(BytesIO(raw)) as original:
    assert original.testzip() is None and len(original.namelist())==36
    files={i.filename:original.read(i.filename) for i in original.infolist()}
    m=files[main].decode()
    m=once(m,"Version: 0.1.28-rc31","Version: 0.1.29-rc32")
    m=once(m,
        """        $network = sanitize_key((string)($campaign['network'] ?? ''));
        if ($creative !== 'banner' || !in_array($network, array('direct','awin','adcell'), true)) { return false; }""",
        """        $network = sanitize_key((string)($campaign['network'] ?? ''));
        // RC32: Tariffcheck originals imported through the legacy "manual"
        // provider must not be blocked merely because of this old provider
        // label. Require TWO real stored partner identity fields; generic
        // manual banners still stay blocked in all insurance branches.
        $direct_identity=sanitize_key((string)($campaign['advertiser_id']??''));
        $actual_partner=strtolower(remove_accents((string)($campaign['partner']??'')));
        $verified_manual_direct=$network==='manual'
            && in_array($direct_identity,array('tarifcheck','check24'),true)
            && strpos($actual_partner,$direct_identity)!==false;
        if ($creative !== 'banner' || (!in_array($network,array('direct','awin','adcell'),true)
            && !$verified_manual_direct)) { return false; }""")
    files[main]=m.encode()
    out=files[output].decode()
    # Previously storing a ready campaign discarded the branch path, reducing
    # a specialist policy to a single R3 page on the next planning pass.
    out=once(out,
        """            'destination_url'=>esc_url_raw((string)($row['destination_url']??'')),
            'compatible_slots'=>array_values(array_unique(array_map('sanitize_key',(array)$compatible_slots))),""",
        """            'destination_url'=>esc_url_raw((string)($row['destination_url']??'')),
            // Source-backed descendant target edges must survive EVERY plan,
            // not only the initial RC31 migration run. Never invent edges.
            'path_target_keys'=>array_values(array_unique(array_filter(
                array_map('sanitize_text_field',(array)($classification['_ppar_banner_target_keys']??array()))
            ))),
            'compatible_slots'=>array_values(array_unique(array_map('sanitize_key',(array)$compatible_slots))),""")
    out=once(out,
        "$option='ppar_hab_rc31_tarifcheck_reconcile_v1';",
        "$option='ppar_hab_rc32_tarifcheck_reconcile_v1';")
    files[output]=out.encode()
    read=files[readme].decode()
    read=once(read,"Stable tag: 0.1.28-rc31","Stable tag: 0.1.29-rc32")
    files[readme]=read.encode()
    changed={main,output,readme}
    assert all(files[name]==original.read(name) for name in original.namelist() if name not in changed)
    buff=BytesIO()
    with ZipFile(buff,"w") as dest:
        for item in original.infolist():dest.writestr(item,files[item.filename])
    data=buff.getvalue()
with ZipFile(BytesIO(data)) as final:
    assert final.testzip() is None and len(final.namelist())==36
    assert b"0.1.29-rc32" in final.read(main)
    assert b"ppar_hab_rc32_tarifcheck_reconcile_v1" in final.read(output)
P.write_bytes(data)
print("HAB_RC32_ROOTFIX_BUILD_PASS",len(data),sha256(data).hexdigest())
