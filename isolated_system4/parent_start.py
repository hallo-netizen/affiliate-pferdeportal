from __future__ import annotations

import hashlib
import html.parser
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import point0_snapshot
import root_entry

CONTRACT = 'SYSTEM4_PARENT_LAUNCH_V1'
PROD_CONTRACT = 'SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1'
BATCH_CONTRACT = 'PSERC_TEXTMACHINE_METADATA_BATCH_V2'
MAX_SOURCE_BYTES = 1_500_000
HERE = Path(__file__).resolve().parent
REPO = HERE.parent


class ParentStartError(RuntimeError):
    pass


def canon(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class _TextExtractor(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'style', 'noscript', 'svg'}:
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in {'script', 'style', 'noscript', 'svg'} and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            text = ' '.join(str(data).split())
            if text:
                self.parts.append(text)

    def text(self) -> str:
        return ' '.join(self.parts)


def _within(child: Path, parent: Path) -> bool:
    child = child.resolve()
    parent = parent.resolve()
    return child == parent or parent in child.parents


def _validate_launch(value: dict) -> tuple[list[dict], list[list[str]]]:
    if not isinstance(value, dict) or value.get('contract') != CONTRACT:
        raise ParentStartError('PARENT_LAUNCH_CONTRACT_INVALID')
    if value.get('publish_allowed') is not False:
        raise ParentStartError('PARENT_LAUNCH_PUBLISH_MUST_BE_FALSE')
    items = value.get('items')
    source_urls = value.get('source_urls')
    if not isinstance(items, list) or not items:
        raise ParentStartError('PARENT_LAUNCH_ITEMS_INVALID')
    if not isinstance(source_urls, list) or len(source_urls) != len(items):
        raise ParentStartError('PARENT_LAUNCH_SOURCE_COUNT_MISMATCH')
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            raise ParentStartError('PARENT_LAUNCH_ITEM_INVALID:' + str(idx))
        for key in ('title', 'target_keyword', 'category', 'article_type', 'plan_slot'):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ParentStartError('PARENT_LAUNCH_ITEM_FIELD_INVALID:' + str(idx) + ':' + key)
        if not re.fullmatch(r'[0-9a-f]{64}', item['plan_slot']):
            raise ParentStartError('PARENT_LAUNCH_PLAN_SLOT_INVALID:' + str(idx))
        urls = source_urls[idx]
        if not isinstance(urls, list) or not urls:
            raise ParentStartError('PARENT_LAUNCH_SOURCE_URLS_EMPTY:' + str(idx))
        for url in urls:
            if not isinstance(url, str) or not re.match(r'^https?://', url):
                raise ParentStartError('PARENT_LAUNCH_SOURCE_URL_INVALID:' + str(idx))
    return items, source_urls


def _fetch_source(url: str, source_id: str) -> dict:
    req = urllib.request.Request(url, headers={'User-Agent': 'pferde-atelier-system4-parent-start/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            status = int(getattr(response, 'status', 0) or 0)
            raw = response.read(MAX_SOURCE_BYTES + 1)
            final_url = response.geturl()
            content_type = str(response.headers.get('Content-Type', ''))
    except Exception as exc:
        raise ParentStartError('PARENT_SOURCE_FETCH_FAILED:' + url + ':' + exc.__class__.__name__) from exc
    if status < 200 or status >= 300:
        raise ParentStartError('PARENT_SOURCE_HTTP_FAIL:' + url + ':' + str(status))
    if len(raw) > MAX_SOURCE_BYTES:
        raise ParentStartError('PARENT_SOURCE_TOO_LARGE:' + url)
    charset = 'utf-8'
    match = re.search(r'charset=([^;\s]+)', content_type, flags=re.I)
    if match:
        charset = match.group(1).strip('"\'')
    try:
        decoded = raw.decode(charset, errors='replace')
    except LookupError:
        decoded = raw.decode('utf-8', errors='replace')
    if 'html' in content_type.lower() or '<html' in decoded[:500].lower():
        parser = _TextExtractor()
        parser.feed(decoded)
        evidence = parser.text()
    else:
        evidence = ' '.join(decoded.split())
    if len(evidence.strip()) < 20:
        raise ParentStartError('PARENT_SOURCE_EVIDENCE_EMPTY:' + url)
    title = final_url
    title_match = re.search(r'<title[^>]*>(.*?)</title>', decoded, flags=re.I | re.S)
    if title_match:
        clean_title = re.sub(r'<[^>]+>', ' ', title_match.group(1))
        clean_title = ' '.join(clean_title.split())
        if clean_title:
            title = clean_title
    return {
        'source_id': source_id,
        'source_title': title,
        'source_url': final_url,
        'retrieved_at': datetime.now(timezone.utc).isoformat(),
        'evidence': evidence,
        'snapshot_sha256': sha256(evidence.encode('utf-8')),
        'http_status': status,
        'source_kind': 'parent_machine_http',
    }


def _build_production_snapshot(items: list[dict], manifest: str) -> bytes:
    material = {
        'contract': BATCH_CONTRACT,
        'content_or_format_payload_present': False,
        'item_count': len(items),
        'items': items,
        'maximum_articles': 0,
        'maximum_articles_per_type': 0,
        'publish_allowed': False,
        'status': 'READY_FOR_TEXTMACHINE_METADATA_INTAKE',
    }
    material['batch_sha256'] = sha256(canon(material))
    value = {
        'contract': PROD_CONTRACT,
        'next_textmachine_metadata_batch': material,
        'source_snapshot_original_sha256': sha256(canon(items)),
        'system4_root_manifest_sha256': manifest,
    }
    return canon(value)


def run(launch_path: Path, runtime_root: Path) -> list[Path]:
    if not launch_path.is_file():
        raise ParentStartError('PARENT_LAUNCH_FILE_MISSING')
    if _within(launch_path, REPO) or _within(runtime_root, REPO):
        raise ParentStartError('PARENT_RUNTIME_MUST_BE_OUTSIDE_REPO')
    try:
        launch = json.loads(launch_path.read_text(encoding='utf-8'))
    except Exception as exc:
        raise ParentStartError('PARENT_LAUNCH_JSON_INVALID') from exc
    items, source_urls = _validate_launch(launch)
    manifest = root_entry._critical_manifest_sha256()
    head = root_entry._git('rev-parse', '--verify', 'HEAD')
    production_bytes = _build_production_snapshot(items, manifest)
    runtime_root.mkdir(parents=True, exist_ok=False)
    workspaces: list[Path] = []
    for index, urls in enumerate(source_urls):
        prepared = point0_snapshot.prepare(
            production_snapshot_bytes=production_bytes,
            root_manifest_sha256=manifest,
            head_sha=head,
        )
        sources = [_fetch_source(url, f'parent-{index}-{src_index}') for src_index, url in enumerate(urls)]
        final = point0_snapshot.finalize(
            prepared,
            research_provider='SYSTEM4_PARENT_MACHINE_HTTP_V1',
            sources=sources,
        )
        point0_path = runtime_root / f'point0-{index}.json'
        point0_path.write_bytes(point0_snapshot.canon(final))
        workspace = runtime_root / f'item-{index}'
        rc = root_entry.main(['root_entry.py', 'start-point0', str(point0_path), str(workspace), str(index)])
        if rc != 0:
            raise ParentStartError('PARENT_ROOT_START_FAILED:' + str(index) + ':' + str(rc))
        workspaces.append(workspace)
    receipt = {
        'contract': 'SYSTEM4_PARENT_START_RECEIPT_V1',
        'head_sha': head,
        'root_manifest_sha256': manifest,
        'article_count': len(items),
        'workspaces': [str(path) for path in workspaces],
        'publish_allowed': False,
    }
    (runtime_root / 'parent_start_receipt.json').write_bytes(canon(receipt))
    return workspaces


def main(argv: list[str]) -> int:
    try:
        if len(argv) != 4 or argv[1] != 'start':
            raise ParentStartError('PARENT_START_BAD_COMMAND')
        workspaces = run(Path(argv[2]), Path(argv[3]))
        print('SYSTEM4_PARENT_START_PASS:POINT0_ROOT_DISPATCH_READY:ARTICLE_COUNT=' + str(len(workspaces)))
        for index, workspace in enumerate(workspaces):
            print('SYSTEM4_PARENT_WORKSPACE:' + str(index) + ':' + str(workspace))
        return 0
    except Exception as exc:
        print('SYSTEM4_PARENT_START_FAIL:' + str(exc))
        return 2


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
