import json
import sys
from pathlib import Path

OFFICE=Path(__file__).resolve().parent
sys.path.insert(0,str(OFFICE))

from contracts import ArticleJob
from handoff_guard import check_job

raw=json.loads((OFFICE/"fixtures/real_wordpress_job_001.json").read_text(encoding="utf-8"))
job=ArticleJob(
    job_id=raw["job_id"],
    title=raw["title"],
    keyword=raw["keyword"],
    article_type=raw["article_type"],
    category=raw["category"],
    internal_links=raw["internal_links"],
)
errors=check_job(job)

print("CONCEPT_AGENT_REALTEST_001")
print("SOURCE=READ_ONLY_COPY_FROM_WORDPRESS_LIVE_FIXTURE")
print("PUBLISH_ALLOWED=false")
if errors == ["EXACT_THREE_INTERNAL_LINKS_REQUIRED"]:
    print("RESULT=EXPECTED_BLOCK_PASS")
    print("ERROR=EXACT_THREE_INTERNAL_LINKS_REQUIRED")
    raise SystemExit(0)
print("RESULT=FAIL")
print("ERRORS="+",".join(errors))
raise SystemExit(1)
