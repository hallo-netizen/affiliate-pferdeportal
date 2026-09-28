from __future__ import annotations
import html
import re

CONTRACT = "K8_SECTION_BALANCE_POLICY_V1"
MIN_WORDS = 60
MAX_WORDS = 120
EXEMPT_BLOCKS = {"table", "conclusion", "further_information"}

class SectionBalanceError(RuntimeError):
    pass

def _plain(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"(?is)<[^>]+>", " ", value))).strip()

def _words(value: str) -> int:
    return len(re.findall(r"\b[\wÄÖÜäöüß-]+\b", _plain(value), re.UNICODE))

def inspect(article_html: str) -> list[dict]:
    if not isinstance(article_html, str) or not article_html.strip():
        raise SectionBalanceError("K8_ARTICLE_EMPTY")
    rows = []
    for section in re.finditer(
        r'(?is)<section\b[^>]*data-block\s*=\s*(["\'])([^"\']+)\1[^>]*>(.*?)</section>',
        article_html,
    ):
        block_id = section.group(2)
        body = section.group(3)
        if block_id in EXEMPT_BLOCKS:
            continue
        headings = list(re.finditer(r"(?is)<h2\b[^>]*>(.*?)</h2>", body))
        for pos, heading in enumerate(headings):
            end = headings[pos + 1].start() if pos + 1 < len(headings) else len(body)
            rows.append({
                "block_id": block_id,
                "heading": _plain(heading.group(1)),
                "word_count": _words(body[heading.end():end]),
            })
    return rows

def validate(article_html: str) -> dict:
    rows = inspect(article_html)
    if not rows:
        raise SectionBalanceError("K8_NORMAL_H2_SECTION_MISSING")
    bad = [r for r in rows if r["word_count"] < MIN_WORDS or r["word_count"] > MAX_WORDS]
    if bad:
        first = bad[0]
        raise SectionBalanceError(
            f'K8_H2_SECTION_WORD_RANGE:{first["word_count"]}:{MIN_WORDS}:{MAX_WORDS}:{first["heading"]}'
        )
    return {
        "status": "PASS",
        "contract": CONTRACT,
        "minimum_words": MIN_WORDS,
        "maximum_words": MAX_WORDS,
        "exempt_blocks": sorted(EXEMPT_BLOCKS),
        "sections": rows,
    }
