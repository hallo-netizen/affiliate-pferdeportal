"""1..N-Steuerung für Concept Agent."""
from dataclasses import dataclass
from contracts import ArticleJob, ResearchEvidence
from controller import ConceptAgentController, RunResult


@dataclass
class BatchItem:
    job: ArticleJob
    sources: list[ResearchEvidence]


@dataclass
class BatchResult:
    status: str
    results: list[RunResult]


class ConceptAgentBatchController:
    def __init__(self, writer_factory):
        self.writer_factory=writer_factory

    def run(self, items: list[BatchItem]) -> BatchResult:
        if not items:
            return BatchResult("BLOCKED_EMPTY_BATCH", [])
        results=[]
        for item in items:
            writer=self.writer_factory()
            result=ConceptAgentController(writer).run(item.job,item.sources)
            results.append(result)
            if result.status!="FINAL_FILE_READY":
                return BatchResult("BLOCKED_ITEM",results)
        if len(results)!=len(items):
            return BatchResult("BLOCKED_ITEM_COUNT_MISMATCH",results)
        return BatchResult("BATCH_FINAL_READY",results)
