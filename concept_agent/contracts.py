"""Eigene Datenverträge des vollständig isolierten Concept-Agent-Büros."""

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class ArticleJob:
    job_id: str
    title: str
    keyword: str
    article_type: str
    category: str
    internal_links: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class ResearchEvidence:
    source_id: str
    url: str
    evidence: str


@dataclass(frozen=True)
class Fact:
    fact_id: str
    statement: str
    source_id: str


@dataclass(frozen=True)
class Draft:
    job_id: str
    body: str


@dataclass(frozen=True)
class CheckResult:
    passed: bool
    errors: List[str] = field(default_factory=list)
