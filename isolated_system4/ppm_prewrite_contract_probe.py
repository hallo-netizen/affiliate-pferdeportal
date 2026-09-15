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
TARGET_CONTRACTS = {
    'portal_link_registry_snapshot_v2',
    'WORDPRESS_LINK_TARGET_SNAPSHOT_V1',
    'PSTE_PORTAL_TAXONOMY_SNAPSHOT_V3',
    'PSERC_PORTAL_STRUCTURE_REGISTRY_V1',
}
TARGET_CATEGORY = 'checklisten-fuer-pferdeanhaenger-faq'


def interesting(value: dict) -> bool:
    contract = value.get('contract')
    if contract in TARGET_CONTRACTS:
        return True
    if value.get('slug') == TARGET_CATEGORY:
        return True
    if value.get('category') == TARGET_CATEGORY:
        return True
    if value.get('category_slug') == TARGET_CATEGORY:
        return True
    return False


def walk(value, path='$', *, source_name: str):
    if isinstance(value, dict):
        contract = value.get('contract')
        if contract == 'content_structure_language_binding_v2' or 'portal_link_registry' in value or 'link_bindings' in value:
            print('QUALITY_AUTHORITY_OBJECT=' + source_name + ':' + path)
            print(json.dumps(value, ensure_ascii=False, sort_keys=True))
        if interesting(value):
            print('UNDERLYING_AUTHORITY_OBJECT=' + source_name + ':' + path)
            print(json.dumps(value, ensure_ascii=False, sort_keys=True))
        for key, child in value.items():
            walk(child, path + '.' + str(key), source_name=source_name)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            walk(child, path + f'[{index}]', source_name=source_name)


def main() -> int:
    underlying = 0
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
            marker_before = []
            def collect(v, path='$'):
                nonlocal underlying
                if isinstance(v, dict):
                    if interesting(v):
                        underlying += 1
                    for k, c in v.items():
                        collect(c, path + '.' + str(k))
                elif isinstance(v, list):
                    for i, c in enumerate(v):
                        collect(c, path + f'[{i}]')
            collect(value)
            walk(value, source_name=name)
    print('PPM679_UNDERLYING_AUTHORITY_COUNT=' + str(underlying))
    if underlying < 1:
        raise SystemExit('PPM679_UNDERLYING_PREWRITE_AUTHORITY_NOT_FOUND')
    print('PPM679_PREWRITE_AUTHORITY_PROBE_PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
