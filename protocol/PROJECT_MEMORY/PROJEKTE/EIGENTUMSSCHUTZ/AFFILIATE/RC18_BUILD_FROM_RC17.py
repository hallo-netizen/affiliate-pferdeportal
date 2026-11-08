#!/usr/bin/env python3
"""Rebuild HAB-004 RC18 from the verified RC17 CURRENT.zip. No other plugins."""
from pathlib import Path
from zipfile import ZipFile
import hashlib,io

root=Path('protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ')
path=root/'PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip'
source=path.read_bytes()
digest=lambda b:hashlib.sha256(b).hexdigest()
old_zip_sha='c1b7be31270c9b670787e70bc005812c69bfa9431580b45d86e05feac1251b90'
official_zip_sha='b22e4d49a56b25e3fc2e46c9bdd0ccbd7c6c16eb7c1f6bb48ae005db0ba50a03'
assert digest(source) in (old_zip_sha,official_zip_sha),'Source changed: refuse to overwrite unknown plugin'
def rep(s,old,new,count=1):
    assert s.count(old)==count,('Mismatch',old[:110],s.count(old))
    return s.replace(old,new)
fixed={}
with ZipFile(io.BytesIO(source)) as src:
    assert len(src.namelist())==36 and src.testzip() is None
    rootdir='affiliate-portal-router/'
    main=rootdir+'affiliate-portal-router.php'
    bridge=rootdir+'includes/class-ppar-hab-bewahr-bridge.php'
    trait=rootdir+'includes/trait-ppar-hb-amazon.php'
    readme=rootdir+'readme.txt'
    s=src.read(main).decode()
    s=rep(s,'Version: 0.1.14-rc17','Version: 0.1.15-rc18')
    s=rep(s,'public function hab_bw_area_slot($page_id, $kind) {',"public function hab_bw_area_slot($page_id, $kind, $verified_node_id = '') {")
    old="""        $context=$this->get_content_context($page_id);
        $type=PPAR_HB_Design_Contract::affiliate_page_type($page_id);
        if ($type==='') { return ''; }"""
    new="""        $context=$this->get_content_context($page_id);
        $type=PPAR_HB_Design_Contract::affiliate_page_type($page_id);
        // The current design tree already knows the exact page node. Validate it
        // against the active snapshot and WP page ID, then keep it through the
        // original campaign-first renderer to the existing Amazon fallback.
        $key=(string)$verified_node_id;
        $verified=$key!=='' && class_exists('PPAR_HB_Integration')
            ? (PPAR_HB_Integration::verified_nodes()[$key] ?? array()) : array();
        if (($verified['type'] ?? '')==='page' && absint($verified['wp_id'] ?? 0)===$page_id) {
            $context['hb_verified_node_id']=$key;
            if (strpos($key,'core:world:')===0) { $type='hub1'; }
            elseif (strpos($key,'core:area:')===0 || strpos($key,'core:c22:area:')===0) { $type='hub2'; }
            elseif (($verified['pillar'] ?? '')==='core') { $type='leaf'; }
        }
        if ($type==='') { return ''; }"""
    s=rep(s,old,new)
    fixed[main]=s.encode()
    s=src.read(bridge).decode()
    s=rep(s,"return Portal_Affiliate_Router::instance()->hab_bw_area_slot($id,$kind);",
      "return Portal_Affiliate_Router::instance()->hab_bw_area_slot($id,$kind,(string)$node['id']);",count=2)
    fixed[bridge]=s.encode()
    s=src.read(trait).decode()
    old="""        $post_type=(string)($context['post_type'] ?? '');
        $node=array();
        $topic='';
        if ($post_type === 'category_archive') {"""
    new="""        $post_type=(string)($context['post_type'] ?? '');
        $node=array();
        $topic='';
        // The design passes its verified immutable node ID for page tiles.
        // Do not re-derive this identity from translated titles or ambiguous WP page indices.
        $verified_id=(string)($context['hb_verified_node_id'] ?? '');
        if ($verified_id!=='' && isset($nodes[$verified_id])
            && ($nodes[$verified_id]['type'] ?? '')==='page'
            && absint($nodes[$verified_id]['wp_id'] ?? 0)===absint($context['post_id'] ?? 0)) {
            $node=$nodes[$verified_id];$topic=(string)$node['name'];
        } elseif ($post_type === 'category_archive') {"""
    s=rep(s,old,new)
    old="""        $name=sanitize_title((string)$world['name']);
        // Six original, inspected HAB-001 subjects, separately copied just like
        // HD009 0.1.25. Insurances has no relevant Amazon merchandise category.
        $images=array(
            'einbruch-diebstahl'=>'hb-amazon-world-einbruch.webp',
            'vandalismus-zerstorung'=>'hb-amazon-world-vandalismus.webp',
            'wasser-feuchtigkeit'=>'hb-amazon-world-wasser.webp',
            'feuer-gase'=>'hb-amazon-world-feuer.webp',
            'wetter-naturgefahren'=>'hb-amazon-world-wetter.webp',
            'technik-ausfalle'=>'hb-amazon-world-technik.webp',
            'versicherungen'=>'hb-amazon-kategorie-tresore.webp',
            'insurance'=>'hb-amazon-kategorie-tresore.webp',
        );
        $file=(string)($images[$name] ?? '');"""
    new="""        $world_id=(string)$world['id'];
        // Use EXACT immutable world IDs. WordPress in de_DE turns Ö/Ä into
        // "oe"/"ae"; title slugs therefore do NOT match hard-coded ASCII
        // keys (e.g. "Zerstörung" or "Ausfälle"). This affected entire worlds.
        // The same mapping now works for worlds, R2, R3 and WP leaf categories.
        $images=array(
            'core:world:einbruch-und-diebstahl'=>'hb-amazon-world-einbruch.webp',
            'core:world:vandalismus-und-zerstorung'=>'hb-amazon-world-vandalismus.webp',
            'core:world:wasser-und-feuchtigkeit'=>'hb-amazon-world-wasser.webp',
            'core:world:feuer-und-gase'=>'hb-amazon-world-feuer.webp',
            'core:world:wetter-und-naturgefahren'=>'hb-amazon-world-wetter.webp',
            'core:world:technik-und-ausfalle'=>'hb-amazon-world-technik.webp',
            'core:world:insurance'=>'hb-amazon-kategorie-tresore.webp',
        );
        $file=(string)($images[$world_id] ?? '');"""
    s=rep(s,old,new)
    s=rep(s,"if ($name==='einbruch-diebstahl'","if ($world_id==='core:world:einbruch-und-diebstahl'")
    fixed[trait]=s.encode()
    fixed[readme]=rep(src.read(readme).decode(),'Stable tag: 0.1.14-rc17','Stable tag: 0.1.15-rc18').encode()
    expected={
      main:'2f0acc92a358f465c64e9cffbc43f43ad42e3f167a9109b802f1b48ee85234a8',
      bridge:'4b63ba29aa4492ec91c321ab339cf7dbee08e7cfba35ffea48e25641b7e42b5a',
      trait:'9fc12e6696c3ab2c83fb54a513cad6726d8f4dba078ea875661c94925cb9f3e2',
      readme:'52441c3c4cb631c01718349205da5fb5798c8aefd52673339b402aea2dfbcc6e',
    }
    for key,sha in expected.items(): assert digest(fixed[key])==sha,(key,digest(fixed[key]))
    buf=io.BytesIO()
    with ZipFile(buf,'w') as dst:
        for info in src.infolist(): dst.writestr(info,fixed.get(info.filename,src.read(info.filename)))
out=buf.getvalue()
with ZipFile(io.BytesIO(out)) as z:
    assert z.testzip() is None and len(z.namelist())==36
path.write_bytes(out)
print('RC18 READY',len(out),'SHA256',digest(out),'36 ZIP files, exactly 4 changed')
