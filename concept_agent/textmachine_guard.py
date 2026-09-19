"""Eigene isolierte Spiegelprüfung fachlicher Textmaschinenregeln."""
from urllib.parse import urlparse
from contracts import ArticleJob, Draft


def check_textmachine_snapshot(job: ArticleJob, draft: Draft) -> list[str]:
    errors=[]
    body=draft.body

    # Exakt alle vorgegebenen internen Links müssen vorhanden sein.
    for link in job.internal_links:
        if link not in body:
            errors.append("TEXTMACHINE_REQUIRED_INTERNAL_LINK_MISSING")

    # Keine externen http(s)-Links im finalen Text.
    tokens=body.replace("(", " ").replace(")", " ").replace("<", " ").replace(">", " ").split()
    for token in tokens:
        if token.startswith(("http://","https://")):
            errors.append("TEXTMACHINE_EXTERNAL_LINK_FORBIDDEN")
            break

    # Isolierter Prototyp fordert eine Tabellenmarkierung.
    if "<table" not in body.lower() and "|---" not in body and "[TABLE]" not in body:
        errors.append("TEXTMACHINE_MANDATORY_TABLE_MISSING")

    return errors
