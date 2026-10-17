import base64,hashlib,sys
from pathlib import Path
source=Path(__file__).with_name('HAB_UND_BEWAHR_KATEGORIE_WORKFLOW_1.14.8.32.zip.b64')
target=Path(sys.argv[1]) if len(sys.argv)>1 else Path('HAB_UND_BEWAHR_KATEGORIE_WORKFLOW_1.14.8.32.zip')
raw=base64.b64decode(''.join(source.read_text().split()),validate=True)
expected='e72e30aa6f9394e62d64cfcc29fca7848399dbd9787b619da7d4fd80f170b79e'
if len(raw)!=308081 or hashlib.sha256(raw).hexdigest()!=expected:
    raise SystemExit('Invalid release archive')
target.write_bytes(raw)
print(target)
