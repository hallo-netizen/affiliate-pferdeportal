"""Providerfreie Grundstruktur für Concept Agent.

Noch keine externe KI, kein WordPress, kein Fremdsystem.
Die Rollen und Übergaben werden zuerst isoliert stabilisiert.
"""

from enum import Enum


class Stage(str, Enum):
    INPUT = "INPUT"
    RESEARCH_REQUIRED = "RESEARCH_REQUIRED"
    RESEARCH_CHECK_REQUIRED = "RESEARCH_CHECK_REQUIRED"
    FACTS_REQUIRED = "FACTS_REQUIRED"
    FACTS_CHECK_REQUIRED = "FACTS_CHECK_REQUIRED"
    WRITE_REQUIRED = "WRITE_REQUIRED"
    ARTICLE_CHECK_REQUIRED = "ARTICLE_CHECK_REQUIRED"
    REPAIR_REQUIRED = "REPAIR_REQUIRED"
    FINAL_FILE_REQUIRED = "FINAL_FILE_REQUIRED"
    DONE = "DONE"


ALLOWED_TRANSITIONS = {
    Stage.INPUT: Stage.RESEARCH_REQUIRED,
    Stage.RESEARCH_REQUIRED: Stage.RESEARCH_CHECK_REQUIRED,
    Stage.RESEARCH_CHECK_REQUIRED: Stage.FACTS_REQUIRED,
    Stage.FACTS_REQUIRED: Stage.FACTS_CHECK_REQUIRED,
    Stage.FACTS_CHECK_REQUIRED: Stage.WRITE_REQUIRED,
    Stage.WRITE_REQUIRED: Stage.ARTICLE_CHECK_REQUIRED,
    Stage.ARTICLE_CHECK_REQUIRED: Stage.FINAL_FILE_REQUIRED,
    Stage.REPAIR_REQUIRED: Stage.ARTICLE_CHECK_REQUIRED,
    Stage.FINAL_FILE_REQUIRED: Stage.DONE,
}


def next_stage(current: Stage) -> Stage:
    if current not in ALLOWED_TRANSITIONS:
        raise ValueError(f"No automatic transition from {current}")
    return ALLOWED_TRANSITIONS[current]
