"""Einzige Writer-Tür des Concept-Agent-Büros."""
from typing import Protocol
from contracts import ArticleJob, Fact, Draft


class WriterPort(Protocol):
    def run(self, job: ArticleJob, facts: list[Fact]) -> Draft:
        ...


def writer_name(writer) -> str:
    return getattr(writer, "provider", writer.__class__.__name__)
