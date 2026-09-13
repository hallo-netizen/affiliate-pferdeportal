from __future__ import annotations

import html
import re
from collections import defaultdict
from typing import Any, Sequence

MIN_SENTENCE_WORDS = 10
MIN_ARTICLES_PER_REPEAT = 4
MAX_MAJORITY_REPEATED_SENTENCES = 6


class BatchRepetitionError(RuntimeError):
    pass


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise BatchRepetitionError(code)


def _visible_text(article: str) -> str:
    value = re.sub(r"(?is)<!--.*?-->", " ", article)
    value = re.sub(r"(?is)<(script|style)\b[^>]*>.*?</\1>", " ", value)
    value = re.sub(r"(?s)<[^>]+>", " ", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def _normalized_sentences(article: str) -> set[str]:
    text = _visible_text(article)
    pieces = re.split(r"(?<=[.!?])\s+", text)
    result: set[str] = set()
    for piece in pieces:
        words = re.findall(r"\b[\wÄÖÜäöüß-]+\b", piece.casefold(), flags=re.UNICODE)
        if len(words) >= MIN_SENTENCE_WORDS:
            result.add(" ".join(words))
    return result


def validate_batch_repetition(bodies: Sequence[str]) -> dict[str, Any]:
    _require(isinstance(bodies, Sequence) and len(bodies) >= 2, "BATCH_REPETITION_INPUT_INVALID")
    occurrences: dict[str, list[int]] = defaultdict(list)
    for index, body in enumerate(bodies):
        _require(isinstance(body, str) and body.strip(), f"BATCH_REPETITION_BODY_INVALID:{index}")
        for sentence in _normalized_sentences(body):
            occurrences[sentence].append(index)

    majority_repeats = [
        (sentence, indexes)
        for sentence, indexes in occurrences.items()
        if len(indexes) >= MIN_ARTICLES_PER_REPEAT
    ]
    majority_repeats.sort(key=lambda row: (-len(row[1]), -len(row[0].split()), row[0]))
    count = len(majority_repeats)
    _require(
        count <= MAX_MAJORITY_REPEATED_SENTENCES,
        f"BATCH_REPEATED_SENTENCE_TEMPLATE_BLOCKED:{count}>{MAX_MAJORITY_REPEATED_SENTENCES}",
    )
    return {
        "status": "PASS",
        "minimum_sentence_words": MIN_SENTENCE_WORDS,
        "minimum_articles_per_repeat": MIN_ARTICLES_PER_REPEAT,
        "majority_repeated_sentence_count": count,
        "maximum_allowed": MAX_MAJORITY_REPEATED_SENTENCES,
    }
