"""Vier strikt getrennte Concept-Agent-Rollen.

Diese Implementierung ist absichtlich providerfrei. Für Tests arbeiten die Rollen
mit fest übergebenen Daten; später kann der Writer über einen Adapter ersetzt werden.
"""
from dataclasses import dataclass
from contracts import ArticleJob, ResearchEvidence, Fact, Draft


@dataclass(frozen=True)
class ResearchInput:
    job: ArticleJob
    source_pool: list[ResearchEvidence]


class ResearchAgent:
    def run(self, data: ResearchInput) -> list[ResearchEvidence]:
        return [x for x in data.source_pool if x.evidence.strip()]


class FactsAgent:
    def run(self, research: list[ResearchEvidence]) -> list[Fact]:
        facts=[]
        for idx, item in enumerate(research, start=1):
            statement=item.evidence.strip()
            facts.append(Fact(f"fact-{idx}", statement, item.source_id))
        return facts


class WriterAgent:
    def run(self, job: ArticleJob, facts: list[Fact]) -> Draft:
        fact_text=" ".join(f.statement for f in facts)
        links=" ".join(job.internal_links)
        body=(
            f"# {job.title}\n\n"
            f"Keyword: {job.keyword}\n\n"
            f"{fact_text}\n\n"
            f"[TABLE]\n\n"
            f"{links}".strip()
        )
        return Draft(job.job_id, body)


class RepairAgent:
    def run(self, job: ArticleJob, draft: Draft, errors: list[str]) -> Draft:
        body=draft.body
        if "TITLE_MISSING_IN_DRAFT" in errors:
            body=f"# {job.title}\n\n"+body
        if "DRAFT_TOO_SHORT" in errors:
            body=body+"\n\n"+"Ergänzung aus bereits akzeptiertem Inhalt."
        if "TEXTMACHINE_MANDATORY_TABLE_MISSING" in errors:
            body=body+"\n\n[TABLE]"
        for link in job.internal_links:
            if "TEXTMACHINE_REQUIRED_INTERNAL_LINK_MISSING" in errors and link not in body:
                body=body+"\n"+link
        return Draft(draft.job_id, body)
