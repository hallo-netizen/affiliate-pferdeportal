import sys
from pathlib import Path
import unittest

OFFICE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OFFICE))

from contracts import ArticleJob,ResearchEvidence,Draft
from batch_controller import BatchItem,ConceptAgentBatchController


class BatchWriter:
    provider="batch-test-writer"
    def run(self,job,facts):
        body=f"# {job.title}\n\n{job.keyword}\n\n{facts[0].statement}\n\n[TABLE]\n\n" + "\n".join(job.internal_links) + "\n\nAusreichender Testinhalt für die vollständige isolierte Batchstrecke."
        return Draft(job.job_id,body)


def item(i):
    job=ArticleJob(
        f"job-{i}",f"Titel {i}",f"Keyword {i}","Beratung",f"kategorie-{i}",
        [f"/test/{i}/a/",f"/test/{i}/b/",f"/test/{i}/c/"]
    )
    src=[ResearchEvidence(f"src-{i}","https://example.org/source",f"Belegter Fakt {i}")]
    return BatchItem(job,src)


class Batch1NTest(unittest.TestCase):
    def run_n(self,n):
        items=[item(i) for i in range(n)]
        result=ConceptAgentBatchController(BatchWriter).run(items)
        self.assertEqual("BATCH_FINAL_READY",result.status)
        self.assertEqual(n,len(result.results))
        self.assertEqual([f"job-{i}" for i in range(n)],[r.final_file["job_id"] for r in result.results])
        self.assertTrue(all(r.final_file["status"]=="FINAL_FILE_READY" for r in result.results))

    def test_one(self): self.run_n(1)
    def test_three(self): self.run_n(3)
    def test_seven(self): self.run_n(7)

    def test_failure_stops_without_silent_drop(self):
        good=item(0)
        bad=item(1)
        bad=BatchItem(ArticleJob("job-1","Titel 1","Keyword 1","Beratung","kategorie-1",[]),bad.sources)
        later=item(2)
        result=ConceptAgentBatchController(BatchWriter).run([good,bad,later])
        self.assertEqual("BLOCKED_ITEM",result.status)
        self.assertEqual(2,len(result.results))
        self.assertEqual("FINAL_FILE_READY",result.results[0].status)
        self.assertEqual("BLOCKED_INPUT",result.results[1].status)

    def test_empty_batch_blocks(self):
        result=ConceptAgentBatchController(BatchWriter).run([])
        self.assertEqual("BLOCKED_EMPTY_BATCH",result.status)


if __name__=="__main__":
    unittest.main()
