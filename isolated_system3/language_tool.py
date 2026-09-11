from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Any, Dict


LT_ENDPOINT = "http://127.0.0.1:8081/v2/check"
LT_VERSION = "6.8"


class LanguageToolFail(RuntimeError):
    pass


def check_text(text: str, timeout: int = 20) -> Dict[str, Any]:
    if not isinstance(text, str) or not text.strip():
        raise LanguageToolFail("LANGUAGETOOL_TEXT_MISSING")
    payload = urllib.parse.urlencode({"language": "de-DE", "text": text}).encode("utf-8")
    req = urllib.request.Request(
        LT_ENDPOINT,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status != 200:
                raise LanguageToolFail(f"LANGUAGETOOL_HTTP_FAIL:{response.status}")
            data = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        if isinstance(exc, LanguageToolFail):
            raise
        raise LanguageToolFail(f"LANGUAGETOOL_ACCESS_FAIL:{type(exc).__name__}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("matches"), list):
        raise LanguageToolFail("LANGUAGETOOL_SCHEMA_FAIL")
    return {
        "status": "PASS",
        "version": LT_VERSION,
        "endpoint": LT_ENDPOINT,
        "match_count": len(data["matches"]),
        "matches": data["matches"],
    }
