#!/usr/bin/env python3
"""Rebuild the exact tested 1.14.8.31 plugin ZIP from its tracked base64 payload."""
import base64,hashlib,sys
from pathlib import Path
source=Path(__file__).with_name("HAB_UND_BEWAHR_KATEGORIE_WORKFLOW_1.14.8.31.zip.b64")
target=Path(sys.argv[1]) if len(sys.argv)>1 else Path("HAB_UND_BEWAHR_KATEGORIE_WORKFLOW_1.14.8.31.zip")
raw=base64.b64decode(source.read_text().strip(),validate=True)
checksum=hashlib.sha256(raw).hexdigest()
expected="6cd47955df14a65d681c7508e1674be94e98cad4dd68df5a6605ce8ef534d933"
if len(raw)!=265246 or checksum!=expected:
    raise SystemExit("STOP: ZIP bytes/hash differ from tested build")
target.write_bytes(raw)
print(f"Recovered verified ZIP: {target} | sha256 {checksum}")
