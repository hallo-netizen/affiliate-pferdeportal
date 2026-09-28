from __future__ import annotations
import html
import re

CONTRACT = "K8_SECTION_BALANCE_POLICY_V2"
MIN_WORDS = 60
MAX_WORDS = 120
EXEMPT_BLOCKS = {"table", "conclusion", "further_information"}
CONCLUSION_TARGET_RATIO = 0.12
CONCLUSION_MAX_RATIO = 0.18
CONCLUSION_MAX_PARAGRAPHS = 3

class SectionBalanceError(RuntimeError):
    pass

def _plain(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"(?is)<[^>]+>", " ", value))).strip()

def _words(value: str) -> int:
    return len(re.findall(r"\b[\wÄÖÜäöüß-]+\b", _plain(value), re.UNICODE))

def inspect(article_html: str) -> list[dict]:
    if not isinstance(article_html, str) or not article_html.strip():
        raise SectionBalanceError("K8_ARTICLE_EMPTY")
    headings = list(re.finditer(r"(?is)<h2\b[^>]*>(.*?)</h2>", article_html))
    rows = []
    for pos, heading in enumerate(headings):
        end = headings[pos + 1].start() if pos + 1 < len(headings) else len(article_html)
        body = article_html[heading.end():end]
        block = re.search(r'(?is)\bdata-block\s*=\s*(["\'])([^"\']+)\1', body)
        block_id = block.group(2) if block else ""
        rows.append({
            "block_id": block_id,
            "heading": _plain(heading.group(1)),
            "word_count": _words(body),
            "paragraph_count": len(re.findall(r"(?is)<p\b[^>]*>", body)),
        })
    return rows

def validate(article_html: str) -> dict:
    rows = inspect(article_html)
    if not rows:
        raise SectionBalanceError("K8_H2_SECTION_MISSING")

    normal = [r for r in rows if r["block_id"] not in EXEMPT_BLOCKS]
    if not normal:
        raise SectionBalanceError("K8_NORMAL_H2_SECTION_MISSING")
    bad = [r for r in normal if r["word_count"] < MIN_WORDS or r["word_count"] > MAX_WORDS]
    if bad:
        first = bad[0]
        raise SectionBalanceError(
            f'K8_H2_SECTION_WORD_RANGE:{first["word_count"]}:{MIN_WORDS}:{MAX_WORDS}:{first["heading"]}'
        )

    conclusions = [r for r in rows if r["block_id"] == "conclusion"]
    if len(conclusions) != 1:
        raise SectionBalanceError(f"K8_CONCLUSION_BLOCK_COUNT:{len(conclusions)}")
    conclusion = conclusions[0]
    total_words = _words(article_html)
    if total_words <= 0:
        raise SectionBalanceError("K8_TOTAL_WORD_COUNT_INVALID")
    conclusion_ratio = conclusion["word_count"] / total_words
    if conclusion_ratio > CONCLUSION_MAX_RATIO:
        raise SectionBalanceError(
            f"K8_CONCLUSION_RATIO_TOO_HIGH:{conclusion_ratio:.6f}:{CONCLUSION_MAX_RATIO:.6f}"
        )
    if conclusion["paragraph_count"] > CONCLUSION_MAX_PARAGRAPHS:
        raise SectionBalanceError(
            f'K8_CONCLUSION_PARAGRAPHS_TOO_HIGH:{conclusion["paragraph_count"]}:{CONCLUSION_MAX_PARAGRAPHS}'
        )

    return {
        "status": "PASS",
        "contract": CONTRACT,
        "minimum_words": MIN_WORDS,
        "maximum_words": MAX_WORDS,
        "exempt_blocks": sorted(EXEMPT_BLOCKS),
        "conclusion_target_ratio": CONCLUSION_TARGET_RATIO,
        "conclusion_maximum_ratio": CONCLUSION_MAX_RATIO,
        "conclusion_maximum_paragraphs": CONCLUSION_MAX_PARAGRAPHS,
        "conclusion_ratio": conclusion_ratio,
        "sections": rows,
    }
