"""Writer für Variante A.

Dieser Port beschreibt die Übergabe an diesen Chat. Er führt selbst keine externe
Verbindung aus. Für lokale Tests kann ein bereits gelieferter Chat-Text eingespeist werden.
"""
from contracts import ArticleJob, Fact, Draft


class ManualChatWriter:
    provider="chat-manual"

    def __init__(self, supplied_text: str | None = None):
        self.supplied_text=supplied_text

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
                {"fact_id":f.fact_id,"statement":f.statement,"source_id":f.source_id}
                for f in facts
            ]
        }

    def run(self, job: ArticleJob, facts: list[Fact]) -> Draft:
        if self.supplied_text is None:
            raise RuntimeError("CHAT_TEXT_NOT_SUPPLIED")
        return Draft(job.job_id,self.supplied_text)
