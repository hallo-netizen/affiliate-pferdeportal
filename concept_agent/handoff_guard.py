"""Eigene harte Übergabeprüfung für Concept Agent."""

from contracts import ArticleJob, ResearchEvidence, Fact, Draft


def check_job(job: ArticleJob) -> list[str]:
    errors=[]
    if not job.job_id.strip(): errors.append("JOB_ID_MISSING")
    if not job.title.strip(): errors.append("TITLE_MISSING")
    if not job.keyword.strip(): errors.append("KEYWORD_MISSING")
    if not job.article_type.strip(): errors.append("ARTICLE_TYPE_MISSING")
    if not job.category.strip(): errors.append("CATEGORY_MISSING")
    if len(job.internal_links) != 3: errors.append("EXACT_THREE_INTERNAL_LINKS_REQUIRED")
    if len(set(job.internal_links)) != len(job.internal_links): errors.append("INTERNAL_LINK_DUPLICATE")
    return errors


def check_research(items: list[ResearchEvidence]) -> list[str]:
    errors=[]
    if not items:
        return ["RESEARCH_EMPTY"]
    seen=set()
    for item in items:
        if not item.source_id.strip(): errors.append("SOURCE_ID_MISSING")
        if item.source_id in seen: errors.append("SOURCE_ID_DUPLICATE")
        seen.add(item.source_id)
        if not item.url.startswith(("https://","http://")): errors.append("SOURCE_URL_INVALID")
        if not item.evidence.strip(): errors.append("EVIDENCE_MISSING")
    return errors


def check_facts(facts: list[Fact], research: list[ResearchEvidence]) -> list[str]:
    errors=[]
    valid_sources={r.source_id for r in research}
    if not facts:
        return ["FACTS_EMPTY"]
    for fact in facts:
        if not fact.fact_id.strip(): errors.append("FACT_ID_MISSING")
        if not fact.statement.strip(): errors.append("FACT_STATEMENT_MISSING")
        if fact.source_id not in valid_sources: errors.append("FACT_SOURCE_NOT_ACCEPTED")
    return errors


def check_draft(draft: Draft, job: ArticleJob) -> list[str]:
    errors=[]
    if draft.job_id != job.job_id: errors.append("DRAFT_JOB_MISMATCH")
    if not draft.body.strip(): errors.append("DRAFT_EMPTY")
    return errors
