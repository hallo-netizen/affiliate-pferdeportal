from __future__ import annotations

import re
from collections import Counter
from typing import Any, Mapping

from isolated_system3.engine import System3Fail


class IndependentCheckFail(System3Fail):
    pass


def _words(text: str) -> list[str]:
    return re.findall(r"\b[\wÄÖÜäöüß-]+\b", text, flags=re.UNICODE)


def build_rule_evidence(raw: Mapping[str, Any], article: str) -> dict[str, Any]:
    if not isinstance(article, str) or not article.strip():
        raise IndependentCheckFail("RULE_ARTICLE_MISSING")

    words = _words(article)
    if not 250 <= len(words) <= 450:
        raise IndependentCheckFail(f"RULE_WORD_COUNT_FAIL:{len(words)}")

    topic = str(raw.get("source_payload", {}).get("topic", "")).strip()
    if not topic:
        raise IndependentCheckFail("RULE_TOPIC_MISSING")

    first_heading = next((line.strip() for line in article.splitlines() if line.strip()), "")
    if first_heading != f"# {topic}":
        raise IndependentCheckFail("RULE_TITLE_BINDING_FAIL")

    if sum(1 for line in article.splitlines() if line.startswith("## ")) < 2:
        raise IndependentCheckFail("RULE_STRUCTURE_FAIL")

    forbidden = (
        "jetzt kaufen",
        "hier kaufen",
        "jetzt bestellen",
        "veröffentlichen",
        "wordpress",
        "system3",
        "system 3",
        "diese anweisung",
        "diese instruktion",
    )
    lower = article.casefold()
    hit = next((x for x in forbidden if x in lower), None)
    if hit:
        raise IndependentCheckFail(f"RULE_FORBIDDEN_LANGUAGE_FAIL:{hit}")

    return {
        "status": "PASS",
        "all_rules_exact": True,
        "checker": "SYSTEM3_INDEPENDENT_RULE_CHECK_V1",
        "word_count": len(words),
    }


def build_quality_evidence(article: str) -> dict[str, Any]:
    words = [w.casefold() for w in _words(article)]
    if len(words) < 250:
        raise IndependentCheckFail("QUALITY_TOO_SHORT")

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", article) if p.strip() and not p.lstrip().startswith("#")]
    if len(paragraphs) < 5:
        raise IndependentCheckFail("QUALITY_PARAGRAPH_DEPTH_FAIL")

    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", " ".join(paragraphs)) if s.strip()]
    if len(sentences) < 10:
        raise IndependentCheckFail("QUALITY_SENTENCE_DEPTH_FAIL")

    lexical = [w for w in words if len(w) >= 4]
    if not lexical:
        raise IndependentCheckFail("QUALITY_LEXICAL_EMPTY")
    counts = Counter(lexical)
    most_common_share = counts.most_common(1)[0][1] / len(lexical)
    if most_common_share > 0.08:
        raise IndependentCheckFail("QUALITY_REPETITION_FAIL")

    avg_sentence_words = len(words) / max(len(sentences), 1)
    if not 8 <= avg_sentence_words <= 30:
        raise IndependentCheckFail(f"QUALITY_READABILITY_FAIL:{avg_sentence_words:.2f}")

    return {
        "status": "PASS",
        "quality_floor_pass": True,
        "checker": "SYSTEM3_INDEPENDENT_QUALITY_CHECK_V1",
        "paragraph_count": len(paragraphs),
        "sentence_count": len(sentences),
        "avg_sentence_words": round(avg_sentence_words, 2),
    }
