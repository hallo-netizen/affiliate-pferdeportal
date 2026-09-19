"""Fail-closed runtime preflight for the isolated Concept Agent office."""
import hashlib
import json
import os
from pathlib import Path

BASE=Path(__file__).resolve().parent
MANIFEST=json.loads((BASE/"runtime/runtime_manifest.json").read_text(encoding="utf-8"))

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda:fh.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def run():
    ppm=BASE.parent/MANIFEST["ppm"]["path"]
    errors=[]
    if not ppm.is_file():
        errors.append("PPM679_ISOLATED_COPY_MISSING")
    elif sha256(ppm)!=MANIFEST["ppm"]["sha256"]:
        errors.append("PPM679_ISOLATED_COPY_HASH_MISMATCH")

    jar=os.environ.get("CONCEPT_AGENT_LANGUAGETOOL_JAR","").strip()
    if not jar:
        errors.append("LT68_JAR_NOT_BOUND")
    else:
        p=Path(jar)
        if not p.is_file():
            errors.append("LT68_JAR_MISSING")
        elif sha256(p)!=MANIFEST["languagetool"]["commandline_jar_sha256"]:
            errors.append("LT68_JAR_HASH_MISMATCH")

    if errors:
        print("CONCEPT_AGENT_RUNTIME_BLOCKED")
        for e in errors: print(e)
        return 2
    print("CONCEPT_AGENT_RUNTIME_PREFLIGHT_PASS")
    print("PPM=6.7.9")
    print("LANGUAGETOOL=6.8")
    print("PUBLISH_ALLOWED=false")
    return 0

if __name__=="__main__":
    raise SystemExit(run())
