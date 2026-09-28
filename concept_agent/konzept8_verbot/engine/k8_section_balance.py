from __future__ import annotations
import html
import re

CONTRACT = "K8_SECTION_BALANCE_POLICY_V3"
MIN_WORDS = 80
MAX_WORDS = 240
EXEMPT_BLOCKS = {"table", "conclusion", "further_information"}
MAIN_MIN_RATIO = 0.55
CONCLUSION_TARGET_RATIO = 0.12
CONCLUSION_MAX_RATIO = 0.18
CONCLUSION_MAX_PARAGRAPHS = 3
FURTHER_INFORMATION_MAX_WORDS = 60

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
        section_body = section.group(3)
        h2 = re.search(r"(?is)<h2\b[^>]*>(.*?)</h2>", section_body)
        if h2 is None:
            continue
        body = section_body[h2.end():]
        rows.append({
            "block_id": block_id,
            "heading": _plain(h2.group(1)),
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

    main_words = sum(r["word_count"] for r in normal)
    main_ratio = main_words / total_words
    if main_ratio < MAIN_MIN_RATIO:
        raise SectionBalanceError(
            f"K8_MAIN_TEXT_RATIO_TOO_LOW:{main_ratio:.6f}:{MAIN_MIN_RATIO:.6f}"
        )

    conclusion_ratio = conclusion["word_count"] / total_words
    if conclusion_ratio > CONCLUSION_MAX_RATIO:
        raise SectionBalanceError(
            f"K8_CONCLUSION_RATIO_TOO_HIGH:{conclusion_ratio:.6f}:{CONCLUSION_MAX_RATIO:.6f}"
        )
    if conclusion["paragraph_count"] > CONCLUSION_MAX_PARAGRAPHS:
        raise SectionBalanceError(
            f'K8_CONCLUSION_PARAGRAPHS_TOO_HIGH:{conclusion["paragraph_count"]}:{CONCLUSION_MAX_PARAGRAPHS}'
        )

    further = [r for r in rows if r["block_id"] == "further_information"]
    if len(further) == 1 and further[0]["word_count"] > FURTHER_INFORMATION_MAX_WORDS:
        raise SectionBalanceError(
            f'K8_FURTHER_INFORMATION_TOO_LONG:{further[0]["word_count"]}:{FURTHER_INFORMATION_MAX_WORDS}'
        )

    return {
        "status": "PASS",
        "contract": CONTRACT,
        "minimum_words": MIN_WORDS,
        "maximum_words": MAX_WORDS,
        "main_minimum_ratio": MAIN_MIN_RATIO,
        "main_word_count": main_words,
        "main_ratio": main_ratio,
        "exempt_blocks": sorted(EXEMPT_BLOCKS),
        "conclusion_target_ratio": CONCLUSION_TARGET_RATIO,
        "conclusion_maximum_ratio": CONCLUSION_MAX_RATIO,
        "conclusion_maximum_paragraphs": CONCLUSION_MAX_PARAGRAPHS,
        "conclusion_ratio": conclusion_ratio,
        "further_information_maximum_words": FURTHER_INFORMATION_MAX_WORDS,
        "sections": rows,
    }
