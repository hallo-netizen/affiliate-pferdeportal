"""Eigene isolierte Spiegelprüfung fachlicher Textmaschinenregeln."""
import re
from urllib.parse import urlparse
from contracts import ArticleJob, Draft


def _normalise_surface(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().casefold())


def _weak_beratung_title(title: str, keyword: str) -> bool:
    title_n=_normalise_surface(title)
    kw=_normalise_surface(keyword)
    weak={
        f"so findest du {kw}",
        f"so wählst du {kw}",
        f"so waehlst du {kw}",
        f"{kw} wählen",
        f"{kw} waehlen",
        f"{kw} auswählen",
        f"{kw} auswaehlen",
        f"{kw} finden",
        f"das wichtigste über {kw}",
        f"das wichtigste ueber {kw}",
        f"wissenswertes über {kw}",
        f"wissenswertes ueber {kw}",
    }
    return title_n in weak


def _mechanical_beratung_h2(heading: str) -> bool:
    h=_normalise_surface(re.sub(r"<[^>]+>", "", heading))
    if h in {"fazit","weiterführende informationen","weiterfuehrende informationen"}:
        return False
    patterns=[
        r"\bam pferd\s+(?:sicher|richtig|fachlich|realistisch)\s+(?:beurteilen|einordnen|bewerten|prüfen|pruefen)\b",
        r"\b(?:sicher|fachlich|realistisch)\s+(?:beurteilen|einordnen|bewerten)\b",
        r"\bpassend\s+zum\s+(?:bedarf|einsatz)\s+einordnen\b",
        r"\bnach\s+(?:bedarf|anforderungen|nutzen|einsatz)\s+beurteilen\b",
    ]
    return any(re.search(p,h,re.IGNORECASE) for p in patterns)


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

    # Beratungstitel: alte/nackte Generatoroberflächen dürfen nicht mehr in die Produktion.
    # Gute, bereits natürliche Titel bleiben erlaubt; Attribute wie passend/geeignet/richtig/
    # optimal/ideal sind Präsentationssprache, keine SEO-Autorität.
    if job.article_type.strip().casefold()=="beratung" and _weak_beratung_title(job.title,job.keyword):
        errors.append("TEXTMACHINE_BERATUNG_TITLE_WEAK_SURFACE")

    # HTML-Textfluss: ein Inline-Link darf nicht direkt mit dem nächsten Wort verklebt sein.
    # Beispiel BLOCK: </a>ordnet. Erlaubt bleiben Satzzeichen direkt nach dem Link.
    if re.search(r"(?is)</a>(?=[A-Za-zÄÖÜäöüß0-9])",body):
        errors.append("TEXTMACHINE_INLINE_LINK_TRAILING_SPACE_MISSING")

    # Beratung-H2 müssen wie normale menschliche Zwischenüberschriften klingen.
    # Bürokratisch-generische Restphrasen werden fail-closed blockiert.
    if job.article_type.strip().casefold()=="beratung":
        for h2 in re.findall(r"(?is)<h2\b[^>]*>(.*?)</h2>",body):
            if _mechanical_beratung_h2(h2):
                errors.append("TEXTMACHINE_BERATUNG_H2_MECHANICAL")
                break

    return errors
