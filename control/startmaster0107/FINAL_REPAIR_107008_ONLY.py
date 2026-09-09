#!/usr/bin/env python3
from __future__ import annotations

import ast
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DUAL = REPO / "control/startmaster0107/STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py"
RELEASE = REPO / "control/output-quarantine/output_release_gate.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}:EXPECTED_1_MATCH_GOT_{count}")
    return text.replace(old, new, 1)


def patch_dual() -> None:
    text = DUAL.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "elif a==['finalize'] and len(a)==2:o=finalize_after_107008(REPO,a[1])",
        "elif len(a)==2 and a[0]=='finalize':o=finalize_after_107008(REPO,a[1])",
        "CLI_FINALIZE_FIX",
    )

    resolver = '''def resolve_signer_cmd()->str:\n    direct=os.environ.get('PSERC_SIGNER_CMD','').strip()\n    if direct:return direct\n    found=[]\n    for k,v in os.environ.items():\n        value=str(v or '').strip()\n        if k!='PSERC_SIGNER_CMD' and k.endswith('_SIGNER_CMD') and value:\n            found.append(value)\n    unique=[]\n    for value in found:\n        if value not in unique:unique.append(value)\n    if len(unique)==1:\n        os.environ['PSERC_SIGNER_CMD']=unique[0]\n        return unique[0]\n    if len(unique)>1:raise Blocked('HOST_SIDE_WORKFLOW_SUPERVISOR_SIGNER_ACCESS_AMBIGUOUS')\n    raise Blocked('HOST_SIDE_WORKFLOW_SUPERVISOR_SIGNER_ACCESS_MISSING')\n\n'''
    marker = "def finalize_after_107008(repo:Path,receipt_ref:str)->dict:\n"
    if resolver not in text:
        if marker not in text:
            raise RuntimeError("SIGNER_RESOLVER_INSERT_POINT_MISSING")
        text = text.replace(marker, resolver + marker, 1)

    old = "ctx=context_from_release(repo,receipt_ref);cmd=os.environ.get('PSERC_SIGNER_CMD','').strip()\n        if not cmd:raise Blocked('HOST_SIDE_WORKFLOW_SUPERVISOR_SIGNER_ACCESS_MISSING')"
    new = "ctx=context_from_release(repo,receipt_ref);cmd=resolve_signer_cmd()"
    text = replace_once(text, old, new, "SIGNER_BINDING_FIX")

    ast.parse(text)
    DUAL.write_text(text, encoding="utf-8")


def patch_release() -> None:
    text = RELEASE.read_text(encoding="utf-8")
    old = '''    release_receipt_path = destination / receipt_name\n    release_receipt_path.write_text(json.dumps(release_receipt, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n    return {\n'''
    new = '''    release_receipt_path = destination / receipt_name\n    release_receipt_path.write_text(json.dumps(release_receipt, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n    durable_destination = REPO / "control/startmaster0107/durable_release_archive" / prepared["batch_sha256"]\n    durable_destination.mkdir(parents=True, exist_ok=True)\n    durable_outputs = []\n    for row in released:\n        src = REPO / rel(row["released_ref"])\n        dst = durable_destination / src.name\n        if dst.exists() and sha256(dst) != row["sha256"]:\n            raise Blocked("DURABLE_DESTINATION_COLLISION:" + dst.name)\n        if not dst.exists():\n            shutil.copyfile(src, dst)\n        if sha256(dst) != row["sha256"]:\n            raise Blocked("DURABLE_COPY_HASH_MISMATCH:" + dst.name)\n        durable_outputs.append({"source_ref": row["source_ref"], "released_ref": str(dst.relative_to(REPO)), "sha256": row["sha256"]})\n    durable_receipt = dict(release_receipt)\n    durable_receipt["outputs"] = durable_outputs\n    durable_receipt_path = durable_destination / receipt_name\n    durable_receipt_path.write_text(json.dumps(durable_receipt, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n    return {\n'''
    text = replace_once(text, old, new, "DURABLE_RELEASE_FIX")
    ast.parse(text)
    RELEASE.write_text(text, encoding="utf-8")


def verify() -> None:
    dual = DUAL.read_text(encoding="utf-8")
    release = RELEASE.read_text(encoding="utf-8")
    required = [
        "elif len(a)==2 and a[0]=='finalize':o=finalize_after_107008(REPO,a[1])",
        "def resolve_signer_cmd()->str:",
        "cmd=resolve_signer_cmd()",
        'durable_release_archive',
        'DURABLE_COPY_HASH_MISMATCH',
    ]
    combined = dual + "\n" + release
    missing = [x for x in required if x not in combined]
    if missing:
        raise RuntimeError("VERIFY_MISSING:" + "|".join(missing))
    if "elif a==['finalize'] and len(a)==2:o=finalize_after_107008(REPO,a[1])" in dual:
        raise RuntimeError("OLD_CLI_BUG_STILL_PRESENT")
    ast.parse(dual)
    ast.parse(release)


def main() -> int:
    patch_dual()
    patch_release()
    verify()
    print("FINAL_REPAIR_107008_PASS")
    print("CHANGED_ONLY=control/startmaster0107/STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py,control/output-quarantine/output_release_gate.py")
    print("WORKFLOW_CHANGED=false")
    print("CONTENT_OR_QUALITY_CHANGED=false")
    print("PUBLISH_ALLOWED=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
