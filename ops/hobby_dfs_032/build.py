#!/usr/bin/env python3
"""HD009 0.1.32: one existing Amazon/DataForSEO worker, contextual product search.

Source official HD009 0.1.31, exact hash. No new WordPress plugin, table,
feed, source document or internet call. The only modified PHP files are the
existing plugin version header and the original Amazon worker class.
"""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from hashlib import sha256
from tempfile import TemporaryDirectory
import subprocess

ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE")
SOURCE=ROOT/"HOBBY_DEPOT_AFFILIATE_HD009_0.1.31.zip"
CURRENT=ROOT/"CURRENT.zip"
OUT=ROOT/"HOBBY_DEPOT_AFFILIATE_HD009_0.1.32.zip"
EXPECTED="3b3d65bd534a249c6ac645a20eac3da9aae68c7e82e52ad7e121639399b46e87"
MAIN="affiliate-portal-router/hobby-depot-affiliate-router.php"
AMAZON="affiliate-portal-router/includes/class-hdar-amazon-start.php"

def one(s,old,new,label):
    n=s.count(old)
    assert n==1,(label,n,old[:170])
    return s.replace(old,new)
assert sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED,"HD009 CURRENT has changed – stop"
with ZipFile(SOURCE) as z:
    assert len(z.namelist())==41 and z.testzip() is None
    main=z.read(MAIN).decode("utf8")
    amazon=z.read(AMAZON).decode("utf8")

main=one(main," * Version: 0.1.31"," * Version: 0.1.32","WordPress plugin version")
amazon=one(amazon,"'0.1.31'","'0.1.32'","style asset version")

# KISS: one machine produces every keyword from the reviewed equipment list,
# and one matching gate checks all returned products. No keyword file copied
# out of HD007. The first list item is not presumed to be purchasable.
candidate=r'''
    /** Only the first reviewed equipment entry may be a paid-search term.
     * No blind fallback to a later item (e.g. "Farben" for model aircraft).
     */
    private static function auto_candidate_word($text,$hobby='') {
        $parts=preg_split('/[,;]/u',trim((string)$text));
        $name=isset($parts[0])?trim((string)$parts[0]," \t\n\r\0\x0B."):'';
        if ($name==='') { return ''; }
        $normalized=self::auto_norm($name);
        if ($normalized==='' || mb_strlen($name,'UTF-8')>55 ||
            count(explode(' ',$normalized))>5) { return ''; }
        // The reviewed product name Metallringe is too broad. For any
        // attested "...flechten" craft, name the literal product's use.
        if (preg_match('/^(?:metall|stahl|alu|edelstahl)?ringe$/',$normalized) &&
            preg_match('/^(.+?)flechten$/u',(string)$hobby,$m)) {
            $base=trim($m[1]);
            if (mb_strlen($base,'UTF-8')>=5) { return $base.' Ringe'; }
        }
        $generic=array(
          'karton','holz','papier','material','werkzeug','werkzeuge',
          'computer','wasser','schere','farbe','farben','modell','schrauben',
          'leitung','leinen','lupe','kleber','buch','bogen','rute',
          'behaelter','aufbewahrung','saatgut','platz','zeit','geduld',
          'licht','luft','erde','werkstatt','grundplatte','metallringe',
          'wetterfeste kleidung','outdoor kleidung','sichere aufbewahrung',
          'trockene aufbewahrung','grundmaterial','modellbausatz',
          'modellbaumaterial','freie arbeitsflaeche','frisches holz',
          'geeignetes holz','rohes material','passendes werkzeug',
          'kamera','rolle','stoff','stoffe','pflanzen','pflanze',
          'wachs','tinte','pfeile','schuhe','magnet','substrat',
          'sammelbeutel','sammelbehaelter','arbeitsplatz',
          'sichere standflaeche','sicheres gelaende','erlaubten fundplatz',
          'wetterdaten','amateurfunklizenz','bestimmungshilfe',
          'stauraum','glasobjekt','brennerplatz','glasstudio mit ofen',
          'saubere gefaesse','je nach technik perlen'
        );
        if (in_array($normalized,$generic,true) ||
            (mb_strlen($name,'UTF-8')<8 &&
             !preg_match('/^(?:rc|3d|cb|fpv|cnc|sdr)-/i',$name))) {
            return '';
        }
        if (preg_match('/\b(?:und|oder|platz|zeit|frei(?:e|er|es)?|geeignet(?:e|er|es)?|erlaubt(?:e|er|es|en)?|erfahrung|kenntnisse|wind|wetter|flaeche|anleitung|sicherheit|umgebung|arbeitsplatz|haltung|arbeitsflaeche|optionale?|passend(?:e|er|es|en)?|sauber(?:e|er|es|en)?|zuverlaessig(?:e|er|es|en)?|staubgeschuetzt(?:e|er|es|en)?|je|nach)\b/',$normalized)) {
            return '';
        }
        return $name;
    }
'''
start=amazon.index("    private static function auto_candidate_word(")
end=amazon.index("    private static function auto_hobby_catalog(",start)
amazon=amazon[:start]+candidate+amazon[end:]
amazon=one(amazon,
    "$term=self::auto_candidate_word($equipment);",
    "$term=self::auto_candidate_word($equipment,(string)($row['canonical_name']??''));",
    "catalog must use product and hobby context")


original_article_match="""            $topic=self::auto_norm((string)$post->post_title);
            $needle=self::auto_norm((string)$row['keyword']);
            $hobby=self::auto_norm((string)$row['hobby']);
            if (strpos(' '.$topic.' ',' '.$needle.' ')===false &&
                strpos(' '.$topic.' ',' '.$hobby.' ')===false) { continue; }"""
safer_article_match="""            $topic=self::auto_norm((string)$post->post_title);
            $topic_compact=str_replace(' ','',$topic);
            $needle=self::auto_norm((string)$row['keyword']);
            // The category alone is insufficient. Every meaningful term
            // must be in the concrete article title, also in compounds.
            $supported=true;
            foreach (explode(' ',$needle) as $part) {
                if (strlen($part)>=4 && strpos($topic_compact,$part)===false) {
                    $supported=false;break;
                }
            }
            if (!$supported) { continue; }"""
amazon=one(amazon,original_article_match,safer_article_match,"exact WP article topic evidence")

# Subject-specific evidence must be part of the review, not just the keyword.
# Source title matching allows German compounds ("Kettenhemdringe") and
# punctuation without admitting another topic or different host.
old="""            $tokens=' '.self::auto_norm($title).' ';
            $ok=true;
            foreach ($words as $word) {
                if (strlen($word)<2) { continue; }
                if (strpos($tokens,' '.$word.' ')===false) { $ok=false;break; }
            }"""
new="""            $tokens=' '.self::auto_norm($title).' ';
            $compact=str_replace(' ','',$tokens);
            $ok=true;
            foreach ($words as $word) {
                if (strlen($word)<2) { continue; }
                // Products often spell the same exact subject as a German
                // compound (Kettenhemdringe); do not broaden to synonyms.
                if (strpos($tokens,' '.$word.' ')===false &&
                    (strlen($word)<4 || strpos($compact,$word)===false)) {
                    $ok=false;break;
                }
            }"""
amazon=one(amazon,old,new,"original ASIN product topic match")

# Consent made under the weak 0.1.31 keyword logic cannot silently authorize
# new paid queries after updating. The current WP setting is not erased;
# users can re-enable after checking the new no-cost preview.
start=amazon.index("    private static function auto_state()")
end=amazon.index("    private static function auto_save_state(",start)
state=amazon[start:end]
assert "return array_merge(array('enabled'=>false" in state
state=one(state,"        return array_merge(array('enabled'=>false",
                "        $s=array_merge(array('enabled'=>false","default state")
assert ",'last_candidate'=>''),$s);" in state
state=one(state,",'last_candidate'=>''),$s);",
  """,'last_candidate'=>''),$s);
        if (($s['consent_version']??'')!=='0.1.32') {
            $s['enabled']=false;
            $s['status']='needs_review';
            $s['message']='Nach der neuen fachlichen Suchwort-Prüfung sind kostenpflichtige Aufträge gesperrt. Erst kostenlos prüfen, dann ausdrücklich neu aktivieren.';
        }
        return $s;""","require renewed consent after weak keyword logic")
amazon=amazon[:start]+state+amazon[end:]
amazon=one(amazon,
   "        $s['enabled']=!empty($_POST['hdar_dfs_auto_enabled']);",
   "        $s['enabled']=!empty($_POST['hdar_dfs_auto_enabled']);\n"
   "        $s['consent_version']='0.1.32';",
   "save renewed paid-search consent")

out=BytesIO()
changed=[]
with ZipFile(SOURCE) as z,ZipFile(out,"w") as w:
    for i in z.infolist():
        original=z.read(i.filename)
        updated=main.encode() if i.filename==MAIN else (amazon.encode() if i.filename==AMAZON else original)
        if updated!=original:changed.append(i.filename)
        w.writestr(i,updated)
    w.comment=z.comment
assert set(changed)=={MAIN,AMAZON},changed
data=out.getvalue()
with ZipFile(BytesIO(data)) as z:
    assert len(z.namelist())==41 and z.testzip() is None
    php=[n for n in z.namelist() if n.endswith(".php")]
    assert len(php)==24
    with TemporaryDirectory() as td:
        for n in php:
            f=Path(td)/n
            f.parent.mkdir(parents=True,exist_ok=True)
            f.write_bytes(z.read(n))
            check=subprocess.run(["php","-l",str(f)],capture_output=True,text=True)
            assert check.returncode==0,(n,check.stderr)
OUT.write_bytes(data)
CURRENT.write_bytes(data)
assert OUT.read_bytes()==CURRENT.read_bytes()
print("HD009_032_FULL_BUILD_PASS","bytes",len(data),"sha256",sha256(data).hexdigest(),
      "php",24,"zip",41,"changed",changed)
