from __future__ import annotations
import hashlib, json, re, sys, zipfile
from pathlib import Path

PACKAGE=Path(sys.argv[1])
OUT=Path(sys.argv[2])
EXPECTED_SHA="acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"
SPECS={
    "content_validator":("portal-production-machine/includes/content-validator.php",52,"err"),
    "structure_gate":("portal-production-machine/includes/content-structure-language-gate.php",34,"error"),
    "known_error_gate":("portal-production-machine/includes/known-error-gate.php",14,"error"),
}
W4_CODES=[
    "BLOCKED_QF03_RENDERED_H1_COUNT",
    "BLOCKED_QF03_RENDERED_DUPLICATE_HEADINGS",
    "BLOCKED_QF03_RENDERED_ADJACENT_HEADINGS",
    "BLOCKED_QF03_RENDERED_EVIDENCE_CLASS",
]
RENDERED="portal-production-machine/includes/rendered-dom-validator.php"

def sha256(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def parse(text:str, member:str, method:str):
    # Rule identity is the actual validator call: error code + failed rule.
    rx=re.compile(r"self::"+re.escape(method)+r"\(\s*'([^']+)'\s*,\s*'([^']+)'",re.S)
    out=[]
    for m in rx.finditer(text):
        out.append({
            "legacy_rule_id": member+":"+str(text.count("\n",0,m.start())+1)+":"+m.group(1)+":"+m.group(2),
            "member":member,
            "line":text.count("\n",0,m.start())+1,
            "error_code":m.group(1),
            "failed_rule":m.group(2),
        })
    return out

actual=sha256(PACKAGE)
if actual!=EXPECTED_SHA:
    raise SystemExit("PPM_SHA_MISMATCH:"+actual)
rows=[]
counts={}
with zipfile.ZipFile(PACKAGE) as zf:
    for group,(member,expected,method) in SPECS.items():
        text=zf.read(member).decode("utf-8")
        parsed=parse(text,member,method)
        unique={}
        for row in parsed:
            key=(row["error_code"],row["failed_rule"])
            unique.setdefault(key,row)
        parsed=list(unique.values())
        counts[group]=len(parsed)
        if len(parsed)!=expected:
            raw=len(parse(text,member,method))
            raise SystemExit(f"PPM_SCOPE_COUNT_MISMATCH:{group}:unique={len(parsed)}:raw={raw}:expected={expected}")
        for row in parsed:
            row["legacy_group"]=group
            row["legacy_rule_id"]=member+":"+row["error_code"]+":"+row["failed_rule"]
        rows.extend(parsed)
    text=zf.read(RENDERED).decode("utf-8")
    parsed=parse(text,RENDERED,"error")
    chosen=[]
    for code in W4_CODES:
        hits=[r for r in parsed if r["error_code"]==code]
        if len(hits)!=1:
            raise SystemExit(f"PPM_W4_RULE_IDENTITY_MISMATCH:{code}:{len(hits)}")
        hit=hits[0]
        hit["legacy_group"]="rendered_dom_w4"
        hit["wave4_rule_id"]={
            "BLOCKED_QF03_RENDERED_H1_COUNT":"W4::R8-0786",
            "BLOCKED_QF03_RENDERED_DUPLICATE_HEADINGS":"W4::R8-0787",
            "BLOCKED_QF03_RENDERED_ADJACENT_HEADINGS":"W4::R8-0788",
            "BLOCKED_QF03_RENDERED_EVIDENCE_CLASS":"W4::R8-0790",
        }[code]
        chosen.append(hit)
    counts["rendered_dom_w4"]=len(chosen)
    rows.extend(chosen)

if len(rows)!=104:
    raise SystemExit("PPM_TOTAL_SCOPE_MISMATCH:"+str(len(rows)))
ids=[r["legacy_rule_id"] for r in rows]
if len(ids)!=len(set(ids)):
    raise SystemExit("PPM_LEGACY_RULE_ID_DUPLICATE")
legacy_values={}
with zipfile.ZipFile(PACKAGE) as zf:
    validator=zf.read("portal-production-machine/includes/content-validator.php").decode("utf-8")
    constants={}
    for name in ("MIN_WORDS","MIN_PARAGRAPHS","MIN_H2","MIN_TABLE_BODY_ROWS","MIN_FACT_PACK_COVERAGE_RATIO","MIN_TRACE_LEXICAL_SUPPORT_RATIO","MAX_DUPLICATE_SENTENCE_RATIO","MAX_INTRO_PAIR_SIMILARITY"):
        m=re.search(r"const\s+"+re.escape(name)+r"\s*=\s*([^;]+);",validator)
        if not m:
            raise SystemExit("PPM_CONSTANT_MISSING:"+name)
        raw=m.group(1).strip()
        constants[name]=float(raw) if "." in raw else int(raw)
    legacy_values["content_validator_constants"]=constants
    for key,member in {
        "structure_contract":"portal-production-machine/contracts/content-structure-language-gate-v2.json",
        "known_error_contract":"portal-production-machine/contracts/known-error-gate-v1.json",
        "article_type_templates":"portal-production-machine/contracts/article-type-templates.json",
    }.items():
        legacy_values[key]=json.loads(zf.read(member).decode("utf-8"))

report={
    "contract":"K10_PPM679_EXACT_104_RULE_INVENTORY_V2",
    "status":"PASS",
    "source_commit":"2cc8167fa1e31b4ffa2ff76c9819314be4b98555",
    "package_sha256":actual,
    "expected_total":104,
    "actual_total":len(rows),
    "group_counts":counts,
    "rules":rows,
    "legacy_values":legacy_values,
    "publish_allowed":False,
}
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print("K10_PPM_EXACT_104_PASS:"+json.dumps(counts,sort_keys=True))
