"""Alleinige Ablaufsteuerung des Concept-Agent-Prototyps."""
from dataclasses import dataclass
from contracts import ArticleJob, ResearchEvidence, Draft
from agents import ResearchAgent, ResearchInput, FactsAgent, WriterAgent, RepairAgent
from handoff_guard import check_job, check_research, check_facts, check_draft
from article_guard import check_article


@dataclass
class RunResult:
    status: str
    draft: Draft | None
    trace: list[str]


class ConceptAgentController:
    def __init__(self):
        self.research_agent=ResearchAgent()
        self.facts_agent=FactsAgent()
        self.writer_agent=WriterAgent()
        self.repair_agent=RepairAgent()

    def run(self, job: ArticleJob, source_pool: list[ResearchEvidence]) -> RunResult:
        trace=[]

        errors=check_job(job)
        if errors:
            return RunResult("BLOCKED_INPUT", None, errors)
        trace.append("INPUT_PASS")

        research=self.research_agent.run(ResearchInput(job, source_pool))
        errors=check_research(research)
        if errors:
            return RunResult("BLOCKED_RESEARCH", None, trace+errors)
        trace.append("RESEARCH_PASS")

        facts=self.facts_agent.run(research)
        errors=check_facts(facts, research)
        if errors:
            return RunResult("BLOCKED_FACTS", None, trace+errors)
        trace.append("FACTS_PASS")

        draft=self.writer_agent.run(job, facts)
        errors=check_draft(draft, job)
        if errors:
            return RunResult("BLOCKED_DRAFT_HANDOFF", None, trace+errors)
        trace.append("DRAFT_HANDOFF_PASS")

        errors=check_article(job, draft)
        if errors:
            trace.append("ARTICLE_REPAIR_REQUIRED")
            repaired=self.repair_agent.run(draft, errors)
            errors2=check_article(job, repaired)
            if errors2:
                return RunResult("BLOCKED_AFTER_REPAIR", repaired, trace+errors2)
            draft=repaired
            trace.append("REPAIR_PASS")
        else:
            trace.append("ARTICLE_PASS")

        return RunResult("FINAL_FILE_READY", draft, trace)
