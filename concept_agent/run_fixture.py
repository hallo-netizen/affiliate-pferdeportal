"""Lokaler, rein isolierter Concept-Agent-Probelauf."""
import json
from pathlib import Path
from contracts import ArticleJob, ResearchEvidence
from controller import ConceptAgentController

BASE=Path(__file__).resolve().parent

job_data=json.loads((BASE/"fixtures/sample_job.json").read_text(encoding="utf-8"))
source_data=json.loads((BASE/"fixtures/sample_sources.json").read_text(encoding="utf-8"))

job=ArticleJob(**job_data)
sources=[ResearchEvidence(**x) for x in source_data]
result=ConceptAgentController().run(job, sources)

print(result.status)
for step in result.trace:
    print(step)
if result.draft:
    print("---FINAL---")
    print(result.draft.body)
