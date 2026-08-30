#!/usr/bin/env python3
from __future__ import annotations
import base64, gzip, hashlib, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / 'source'
EXPECTED_PLAN_SHA256 = '0535129cb98fd78e1167007870eb628bee16e34e844d2fc91588a987c3465334'
EXPECTED_PLAN_BYTES = 114929
EXPECTED_BATCH_SHA256 = '7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a'
RAW = [
    ('gen1.plan.gz.b64.part00','22b347171d3ae27840c033eafdc98f432ae03e3bafc2189df74f50e5308e5df2'),
    ('gen1.plan.gz.b64.part01','b0c0989c9b5e782ad93265addcd02f8368a0654dadb6a6c44cc5fdbd75660cbf'),
    ('gen1.plan.gz.b64.part02','d476d5b6eeb4b82492a0a1bacf5faa9e967544e1e00277ad70a5265aa36f44d4'),
]
WRAPPED = [
    ('gen1.plan.transport.part03.json','ce3536162da3b5c84099a193833add46602b5663807cb837e1ecd0ff5292c559','03'),
    ('gen1.plan.transport.part04.json','000278faa3b0d5e3b795ead365a8d323295dc2da027530d1f093e90405a127ed','04'),
    ('gen1.plan.transport.part05.json','4f65ac6d2ae0275276e04c03a69147e75e54ce7d16bd820f65ba232366d97186','05'),
    ('gen1.plan.transport.part06.json','9080c7e49f169b2f95e8fb485cec7a11adb82905b5adf9829189bce816180c5b','06'),
]

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) == 2 else Path('/tmp/GENERATION1_7_ARTIKEL_PRODUKTIONSPLAN.json')
    parts: list[str] = []
    for name, expected in RAW:
        data = (SRC / name).read_bytes()
        if sha(data) != expected:
            raise SystemExit('SOURCE_CHUNK_HASH_MISMATCH:' + name)
        parts.append(data.decode('ascii'))
    for name, expected, number in WRAPPED:
        data = (SRC / name).read_bytes()
        if sha(data) != expected:
            raise SystemExit('SOURCE_CHUNK_HASH_MISMATCH:' + name)
        obj = json.loads(data.decode('utf-8'))
        if obj != {'purpose': f'Generation 1 source transport chunk {number}', 'encoding': 'base64-fragment', 'data': obj.get('data')}:
            raise SystemExit('SOURCE_WRAPPER_SHAPE_INVALID:' + name)
        fragment = obj.get('data')
        if not isinstance(fragment, str) or not fragment:
            raise SystemExit('SOURCE_FRAGMENT_INVALID:' + name)
        parts.append(fragment)
    try:
        raw = gzip.decompress(base64.b64decode(''.join(parts), validate=True))
    except Exception as exc:
        raise SystemExit('SOURCE_RECONSTRUCTION_INVALID') from exc
    if len(raw) != EXPECTED_PLAN_BYTES or sha(raw) != EXPECTED_PLAN_SHA256:
        raise SystemExit('SOURCE_PLAN_IDENTITY_MISMATCH')
    obj = json.loads(raw.decode('utf-8'))
    source = obj.get('source_ready_batch') if isinstance(obj, dict) else None
    items = obj.get('items') if isinstance(obj, dict) else None
    if obj.get('contract') != 'production_plan_v4':
        raise SystemExit('SOURCE_CONTRACT_INVALID')
    if not isinstance(source, dict) or source.get('generation') != 1 or source.get('batch_sha256') != EXPECTED_BATCH_SHA256:
        raise SystemExit('SOURCE_BATCH_BINDING_INVALID')
    if not isinstance(items, list) or len(items) != 7:
        raise SystemExit('SOURCE_ITEM_COUNT_INVALID')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    print(json.dumps({'ok': True, 'status': 'GENERATION1_SOURCE_RECONSTRUCTED_EXACT', 'path': str(out), 'bytes': len(raw), 'sha256': sha(raw), 'generation': 1, 'item_count': 7, 'batch_sha256': EXPECTED_BATCH_SHA256}, ensure_ascii=False))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
