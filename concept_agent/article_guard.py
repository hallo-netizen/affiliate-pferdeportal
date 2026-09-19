"""Eigene Artikelprüfung im Concept-Agent-Büro.

Noch kein Ersatz für produktive Prüfer. Sie beweist nur die interne Agentenlogik.
"""
from contracts import ArticleJob, Draft


def check_article(job: ArticleJob, draft: Draft) -> list[str]:
    errors=[]
    if draft.job_id != job.job_id:
        errors.append("DRAFT_JOB_MISMATCH")
    if not draft.body.strip():
        errors.append("DRAFT_EMPTY")
        return errors
    if f"# {job.title}" not in draft.body:
        errors.append("TITLE_MISSING_IN_DRAFT")
    if job.keyword.lower() not in draft.body.lower():
        errors.append("KEYWORD_MISSING_IN_DRAFT")
    for link in job.internal_links:
        if link not in draft.body:
            errors.append("REQUIRED_LINK_MISSING")
    if len(draft.body.split()) < 8:
        errors.append("DRAFT_TOO_SHORT")
    return errors
