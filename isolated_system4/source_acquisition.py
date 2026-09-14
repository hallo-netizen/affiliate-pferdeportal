from __future__ import annotations

import base64
import hashlib
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Callable, Mapping

CONTRACT = 'SYSTEM4_MACHINE_SOURCE_ACQUISITION_V1'
PROVIDER = 'DATAFORSEO_GOOGLE_ORGANIC_LIVE_ADVANCED'
ENDPOINT = 'https://api.dataforseo.com/v3/serp/google/organic/live/advanced'
LOCATION_NAME = 'Germany'
LANGUAGE_CODE = 'de'
MAX_ORGANIC_RESULTS = 12
MIN_BOUND_SOURCES = 3
MAX_FETCH_BYTES = 1_500_000
MIN_EXTRACT_CHARS = 400
USER_AGENT = 'PferdeAtelier-System4-SourceAcquisition/1.0'


class SourceAcquisitionError(RuntimeError):
    pass


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {'script', 'style', 'noscript', 'svg'}:
            self.skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {'script', 'style', 'noscript', 'svg'} and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            text = re.sub(r'\s+', ' ', html.unescape(data)).strip()
            if text:
                self.parts.append(text)


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _host(url: str) -> str:
    return (urllib.parse.urlsplit(url).hostname or '').lower().removeprefix('www.')


def _valid_public_url(url: str) -> bool:
    try:
        p = urllib.parse.urlsplit(url)
    except Exception:
        return False
    if p.scheme not in {'http', 'https'} or not p.hostname:
        return False
    host = p.hostname.lower()
    if host in {'localhost', '127.0.0.1', '::1'} or host.endswith('.local'):
        return False
    if host == 'pferde-atelier.de' or host.endswith('.pferde-atelier.de'):
        return False
    return True


def organic_candidates(response: Mapping[str, Any], max_results: int = MAX_ORGANIC_RESULTS) -> list[dict[str, Any]]:
    if int(response.get('status_code') or 0) != 20000:
        raise SourceAcquisitionError('DATAFORSEO_TOP_STATUS_NOT_OK')
    tasks = response.get('tasks')
    if not isinstance(tasks, list) or len(tasks) != 1 or not isinstance(tasks[0], Mapping):
        raise SourceAcquisitionError('DATAFORSEO_TASK_SHAPE_INVALID')
    task = tasks[0]
    if int(task.get('status_code') or 0) != 20000:
        raise SourceAcquisitionError('DATAFORSEO_TASK_STATUS_NOT_OK')
    result = task.get('result')
    if not isinstance(result, list) or len(result) < 1 or not isinstance(result[0], Mapping):
        raise SourceAcquisitionError('DATAFORSEO_RESULT_MISSING')
    items = result[0].get('items')
    if not isinstance(items, list):
        raise SourceAcquisitionError('DATAFORSEO_ITEMS_MISSING')

    rows: list[dict[str, Any]] = []
    seen_urls: set[str] = set()
    seen_hosts: set[str] = set()
    organic = [x for x in items if isinstance(x, Mapping) and x.get('type') == 'organic']
    organic.sort(key=lambda x: (int(x.get('rank_group') or 10**9), int(x.get('rank_absolute') or 10**9)))
    for item in organic:
        url = str(item.get('url') or '').strip()
        if not _valid_public_url(url):
            continue
        normalized = urllib.parse.urlunsplit(urllib.parse.urlsplit(url)._replace(fragment=''))
        host = _host(normalized)
        if normalized in seen_urls or host in seen_hosts:
            continue
        seen_urls.add(normalized)
        seen_hosts.add(host)
        rows.append({
            'rank_group': int(item.get('rank_group') or 0),
            'rank_absolute': int(item.get('rank_absolute') or 0),
            'url': normalized,
            'title': str(item.get('title') or '').strip(),
            'domain': str(item.get('domain') or host).strip(),
        })
        if len(rows) >= max_results:
            break
    if len(rows) < MIN_BOUND_SOURCES:
        raise SourceAcquisitionError('DATAFORSEO_TOO_FEW_ORGANIC_SOURCES')
    return rows


def extract_html_text(raw: bytes, charset: str = 'utf-8') -> str:
    try:
        decoded = raw.decode(charset or 'utf-8', errors='replace')
    except LookupError:
        decoded = raw.decode('utf-8', errors='replace')
    parser = _TextExtractor()
    parser.feed(decoded)
    text = re.sub(r'\s+', ' ', ' '.join(parser.parts)).strip()
    return text


def fetch_extract(url: str) -> str:
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT, 'Accept': 'text/html,text/plain;q=0.9,*/*;q=0.1'})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            final_url = resp.geturl()
            if not _valid_public_url(final_url):
                raise SourceAcquisitionError('SOURCE_REDIRECT_NOT_PUBLIC')
            content_type = (resp.headers.get_content_type() or '').lower()
            if content_type not in {'text/html', 'text/plain', 'application/xhtml+xml'}:
                raise SourceAcquisitionError('SOURCE_CONTENT_TYPE_UNSUPPORTED')
            raw = resp.read(MAX_FETCH_BYTES + 1)
            if len(raw) > MAX_FETCH_BYTES:
                raise SourceAcquisitionError('SOURCE_BODY_TOO_LARGE')
            charset = resp.headers.get_content_charset() or 'utf-8'
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise SourceAcquisitionError('SOURCE_FETCH_FAILED') from exc
    text = extract_html_text(raw, charset)
    if len(text) < MIN_EXTRACT_CHARS:
        raise SourceAcquisitionError('SOURCE_EXTRACT_TOO_SHORT')
    return text


def build_source_pool(
    keyword: str,
    response: Mapping[str, Any],
    fetcher: Callable[[str], str] = fetch_extract,
    retrieved_at_utc: str | None = None,
) -> dict[str, Any]:
    keyword = str(keyword or '').strip()
    if not keyword:
        raise SourceAcquisitionError('SOURCE_KEYWORD_REQUIRED')
    candidates = organic_candidates(response)
    timestamp = retrieved_at_utc or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    sources: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    for row in candidates:
        try:
            extract = re.sub(r'\s+', ' ', str(fetcher(row['url']) or '')).strip()
            if len(extract) < MIN_EXTRACT_CHARS:
                raise SourceAcquisitionError('SOURCE_EXTRACT_TOO_SHORT')
        except SourceAcquisitionError as exc:
            failures.append({'url': row['url'], 'error': str(exc)})
            continue
        source_id = 'src-' + hashlib.sha256(row['url'].encode('utf-8')).hexdigest()[:16]
        sources.append({
            'source_id': source_id,
            'url': row['url'],
            'title': row['title'] or row['domain'],
            'publisher': row['domain'] or _host(row['url']),
            'retrieved_at_utc': timestamp,
            'extract_text': extract,
            'content_sha256': hashlib.sha256(extract.encode('utf-8')).hexdigest(),
            'serp_rank_group': row['rank_group'],
            'serp_rank_absolute': row['rank_absolute'],
        })
    if len(sources) < MIN_BOUND_SOURCES:
        raise SourceAcquisitionError('SOURCE_POOL_MINIMUM_NOT_REACHED')
    provider_response_sha = sha256_bytes(canon(response))
    source_pool_sha = sha256_bytes(canon(sources))
    return {
        'contract': CONTRACT,
        'provider': PROVIDER,
        'keyword': keyword,
        'location_name': LOCATION_NAME,
        'language_code': LANGUAGE_CODE,
        'provider_response_sha256': provider_response_sha,
        'source_pool': sources,
        'source_pool_sha256': source_pool_sha,
        'fetch_failures': failures,
    }


def _post_dataforseo(keyword: str) -> dict[str, Any]:
    login = os.environ.get('DATAFORSEO_LOGIN', '').strip()
    password = os.environ.get('DATAFORSEO_PASSWORD', '')
    if not login or not password:
        raise SourceAcquisitionError('DATAFORSEO_CREDENTIALS_MISSING')
    payload = [{
        'keyword': keyword,
        'location_name': LOCATION_NAME,
        'language_code': LANGUAGE_CODE,
        'depth': 20,
        'group_organic_results': True,
    }]
    token = base64.b64encode((login + ':' + password).encode('utf-8')).decode('ascii')
    req = urllib.request.Request(
        ENDPOINT,
        data=canon(payload),
        method='POST',
        headers={'Authorization': 'Basic ' + token, 'Content-Type': 'application/json', 'User-Agent': USER_AGENT},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read(4_000_000)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise SourceAcquisitionError('DATAFORSEO_TRANSPORT_FAILED') from exc
    try:
        value = json.loads(raw.decode('utf-8'))
    except Exception as exc:
        raise SourceAcquisitionError('DATAFORSEO_RESPONSE_INVALID_JSON') from exc
    if not isinstance(value, dict):
        raise SourceAcquisitionError('DATAFORSEO_RESPONSE_NOT_OBJECT')
    return value


def acquire(keyword: str) -> dict[str, Any]:
    return build_source_pool(keyword, _post_dataforseo(keyword))


def main(argv: list[str]) -> int:
    try:
        if len(argv) != 4 or argv[1] != 'acquire':
            raise SourceAcquisitionError('USAGE: source_acquisition.py acquire <keyword-file> <output-json>')
        keyword_path = Path(argv[2])
        out = Path(argv[3])
        if not keyword_path.is_file():
            raise SourceAcquisitionError('KEYWORD_FILE_MISSING')
        keyword = keyword_path.read_text(encoding='utf-8').strip()
        value = acquire(keyword)
        out.parent.mkdir(parents=True, exist_ok=True)
        tmp = out.with_suffix(out.suffix + '.tmp')
        tmp.write_bytes(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True).encode('utf-8'))
        tmp.replace(out)
        print('SYSTEM4_SOURCE_ACQUISITION_PASS:' + value['source_pool_sha256'])
        return 0
    except (SourceAcquisitionError, OSError, ValueError) as exc:
        print('SYSTEM4_SOURCE_ACQUISITION_FAIL:' + str(exc))
        return 2


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
