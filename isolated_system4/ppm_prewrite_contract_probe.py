from __future__ import annotations

import json
import zipfile
from pathlib import Path

import production_checks

REPO = Path(__file__).resolve().parent.parent
PACKAGE = REPO / production_checks.PPM_PACKAGE_REL
TARGETS = {
    'portal-production-machine/contracts/content-structure-language-gate-v2.json',
    'portal-production-machine/contracts/article-type-templates.json',
}


def walk(value, path='$'):
    if isinstance(value, dict):
        contract = value.get('contract')
        if contract == 'content_structure_language_binding_v2' or 'portal_link_registry' in value or 'link_bindings' in value:
            print('AUTHORITY_OBJECT=' + path)
            print(json.dumps(value, ensure_ascii=False, sort_keys=True))
        for key, child in value.items():
            walk(child, path + '.' + str(key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            walk(child, path + f'[{index}]')


def main() -> int:
    with zipfile.ZipFile(PACKAGE) as archive:
        names = archive.namelist()
        for name in sorted(TARGETS):
            if name not in names:
                raise SystemExit('PPM679_PREWRITE_AUTHORITY_MISSING:' + name)
            value = json.loads(archive.read(name).decode('utf-8'))
            print('AUTHORITY_FILE=' + name)
            print(json.dumps(value, ensure_ascii=False, sort_keys=True))
        for name in names:
            if not name.endswith('.json'):
                continue
            try:
                value = json.loads(archive.read(name).decode('utf-8'))
            except Exception:
                continue
            before = name.lower()
            if ('link' in before or 'quality' in before or 'structure' in before or 'article-type' in before or 'faq' in before):
                walk(value, name)
    print('PPM679_PREWRITE_AUTHORITY_PROBE_PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
