"""Platzhaltervertrag für einen späteren Claude-Writer.

Absichtlich KEIN Netzwerkcode und KEIN API-Key-Zugriff.
Der Adapter definiert nur die eine zukünftige Anschlussstelle.
"""
from contracts import ArticleJob, Fact, Draft


class ClaudeWriterAdapter:
    provider = "claude"
    connected = False

    def build_request(self, job: ArticleJob, facts: list[Fact]) -> dict:
        return {
            "role": "writer",
            "job_id": job.job_id,
            "title": job.title,
            "keyword": job.keyword,
            "article_type": job.article_type,
            "category": job.category,
            "internal_links": list(job.internal_links),
            "facts": [
                {"fact_id": f.fact_id, "statement": f.statement, "source_id": f.source_id}
                for f in facts
            ],
        }

    def run(self, job: ArticleJob, facts: list[Fact]) -> Draft:
        raise RuntimeError("CLAUDE_NOT_CONNECTED")
