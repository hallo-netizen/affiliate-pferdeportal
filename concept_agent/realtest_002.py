import json
import sys
from pathlib import Path

OFFICE=Path(__file__).resolve().parent
sys.path.insert(0,str(OFFICE))

from contracts import ArticleJob,ResearchEvidence
from controller import ConceptAgentController
from realtest_writer import RealTestWriter
from final_file import canonical_json

job_raw=json.loads((OFFICE/"fixtures/realtest_002_job.json").read_text(encoding="utf-8"))
sources_raw=json.loads((OFFICE/"fixtures/realtest_002_sources.json").read_text(encoding="utf-8"))

job=ArticleJob(
    job_id=job_raw["job_id"],
    title=job_raw["title"],
    keyword=job_raw["keyword"],
    article_type=job_raw["article_type"],
    category=job_raw["category"],
    internal_links=job_raw["internal_links"],
)
sources=[ResearchEvidence(**x) for x in sources_raw]

result=ConceptAgentController(RealTestWriter()).run(job,sources)
print("CONCEPT_AGENT_REALTEST_002")
print("STATUS="+result.status)
for step in result.trace:
    print(step)
if result.status!="FINAL_FILE_READY" or result.final_file is None:
    raise SystemExit(1)

out=OFFICE/"test_output"
out.mkdir(exist_ok=True)
path=out/"CONCEPT_AGENT_FINAL_ARTICLE_V1.json"
path.write_text(canonical_json(result.final_file),encoding="utf-8")
print("FINAL_FILE="+str(path))
print("ARTICLE_SHA256="+result.final_file["article_sha256"])
