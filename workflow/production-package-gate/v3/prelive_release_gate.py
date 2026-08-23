#!/usr/bin/env python3
import json,hashlib,sys,re
from pathlib import Path
p=Path(sys.argv[1]); q=Path(sys.argv[2]); pkg=json.loads(p.read_text()); qa=json.loads(q.read_text())
html=pkg['production_plan']['items'][0]['canonical_article']['body_html']
checks={
 'qa_prelive':qa.get('status')=='PRELIVE_PASS_LIVE_REPLAY_REQUIRED',
 'same_sha':qa.get('delivery_sha256')==hashlib.sha256(p.read_bytes()).hexdigest(),
 'same_package_id':qa.get('package_id')==pkg.get('package_id'),
 'no_raw_ampersand':re.search(r'&(?!#\d+;|#x[0-9A-Fa-f]+;|[A-Za-z][A-Za-z0-9]+;)',html) is None,
 'not_named_final': 'FINAL' not in p.name,
 'publish_false':pkg['workflow_release'].get('wordpress_write_performed') is False,
}
status='PRELIVE_RELEASE_GATE_PASS_LIVE_REPLAY_REQUIRED' if all(checks.values()) else 'PRELIVE_RELEASE_GATE_BLOCKED'
print(json.dumps({'status':status,'checks':checks},indent=2));sys.exit(0 if all(checks.values()) else 3)
