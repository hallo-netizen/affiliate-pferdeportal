#!/usr/bin/env python3
"""Only root fix: original HTML gets parsed FIRST, before sanitize_text_field
can remove HTML attributes. Store extracted safe evidence in existing payload;
never store untrusted executable HTML. Legacy stored records re-read available
fields once, but already lost markup cannot be fabricated.
"""
from io import BytesIO
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile
R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
raw=P.read_bytes()
assert sha256(raw).hexdigest()=="c45eab25fa6b029faaf7c87ca52850ba81d05bc02c8f0e13330c06e6a4e25e4b","RC40 source required"
B="affiliate-portal-router/"
CRE=B+"includes/trait-ppar-creative-library.php"
OUT=B+"includes/trait-ppar-output-objects.php"
MAIN=B+"affiliate-portal-router.php"
README=B+"readme.txt"
def once(s,a,b):
    assert s.count(a)==1,("Source changed",s.count(a),a[:140])
    return s.replace(a,b,1)
with ZipFile(BytesIO(raw)) as original:
    assert original.testzip() is None and len(original.namelist())==36
    data={x.filename:original.read(x.filename) for x in original.infolist()}
    c=data[CRE].decode()
    c=once(c,
        "private function creative_library_read_original_banner_once($row) {",
        "private function creative_library_read_original_banner_once($row, $original_html = '') {")
    c=once(c,
        """        if((int)($payload['_source_read_version']??0)===1
           && is_array($payload['_source_evidence']??null)) return $row;
        $html=(string)($payload['html']??'');""",
        """        if((int)($payload['_source_read_version']??0)>=2
           && is_array($payload['_source_evidence']??null)) return $row;
        // The raw HTML is used here IN MEMORY, at the first workflow step,
        // BEFORE normalization strips tag attributes. Only safe extracted
        // evidence is persisted; the original untrusted markup is not.
        $html=$original_html!==''?(string)$original_html:(string)($payload['html']??'');
        $older_evidence=is_array($payload['_source_evidence']??null)
            ? $payload['_source_evidence'] : array();""")
    c=once(c,
        """        $payload['_source_evidence']=array(
            'destination'=>sanitize_text_field(trim($destination_evidence)),
            'provider'=>sanitize_text_field($provider),
            'text'=>sanitize_text_field($text),
            'image_hint'=>sanitize_text_field($image_hint),
        );
        $payload['_source_read_version']=1;""",
        """        $new_evidence=array(
            'destination'=>sanitize_text_field(trim($destination_evidence)),
            'provider'=>sanitize_text_field($provider),
            'text'=>sanitize_text_field($text),
            'image_hint'=>sanitize_text_field($image_hint),
        );
        // A legacy v1 may contain bona fide extracted evidence not available
        // after prior sanitization. Never delete that valid source evidence.
        foreach($new_evidence as $field=>$value) {
            if($value==='' && is_string($older_evidence[$field]??null)){
                $new_evidence[$field]=sanitize_text_field($older_evidence[$field]);
            }
        }
        $payload['_source_evidence']=$new_evidence;
        $payload['_source_read_version']=2;
        $payload['_original_html_attributes_available']=$original_html!==''?1:0;""")
    c=once(c,
        """            $normalized=$this->creative_library_read_original_banner_once($normalized);""",
        """            // REQUIRED FIRST STEP. The original HTML is still intact
            // here, but would lose its attributes on the payload copy.
            $normalized=$this->creative_library_read_original_banner_once($normalized,$html);""")
    data[CRE]=c.encode()
    o=data[OUT].decode()
    o=once(o,"$option='ppar_hab_rc40_tarifcheck_reconcile_v1';","$option='ppar_hab_rc41_tarifcheck_reconcile_v1';")
    data[OUT]=o.encode()
    m=data[MAIN].decode()
    m=once(m,"Version: 0.1.37-rc40","Version: 0.1.38-rc41")
    data[MAIN]=m.encode()
    rd=data[README].decode()
    rd=once(rd,"Stable tag: 0.1.37-rc40","Stable tag: 0.1.38-rc41")
    data[README]=rd.encode()
    changed={CRE,OUT,MAIN,README}
    assert all(data[n]==original.read(n) for n in original.namelist() if n not in changed)
    buff=BytesIO()
    with ZipFile(buff,"w") as z:
        for item in original.infolist():z.writestr(item,data[item.filename])
    output=buff.getvalue()
with ZipFile(BytesIO(output)) as z:
    assert z.testzip() is None and len(z.namelist())==36
    assert b"0.1.38-rc41" in z.read(MAIN)
    assert b"creative_library_read_original_banner_once($normalized,$html)" in z.read(CRE)
P.write_bytes(output)
print("RC41_FIRST_SOURCE_BEFORE_HTML_SANITIZATION_BUILD_PASS",len(output),sha256(output).hexdigest())
