from __future__ import annotations

import base64
import hashlib
import re
from pathlib import Path

BEGIN = "SYSTEM3_ARTICLE_B64_BEGIN"
END = "SYSTEM3_ARTICLE_B64_END"
PASS = "SYSTEM3_RETURN_PASS"
SHA_PREFIX = "SYSTEM3_ARTICLE_SHA256:"


class ReturnError(RuntimeError):
    pass


def decode_return(body: str) -> bytes:
    if not isinstance(body, str):
        raise ReturnError("SYSTEM3_RETURN_BODY_INVALID")
    pattern = re.compile(
        rf"\A{BEGIN}\n([A-Za-z0-9+/=\n]+)\n{END}\n{SHA_PREFIX}([0-9a-f]{{64}})\n{PASS}\Z"
    )
    match = pattern.fullmatch(body.strip())
    if not match:
        raise ReturnError("SYSTEM3_RETURN_SCHEMA_FAIL")
    encoded = "".join(match.group(1).splitlines())
    try:
        raw = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise ReturnError("SYSTEM3_RETURN_BASE64_FAIL") from exc
    digest = hashlib.sha256(raw).hexdigest()
    if digest != match.group(2):
        raise ReturnError("SYSTEM3_RETURN_SHA_FAIL")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ReturnError("SYSTEM3_RETURN_UTF8_FAIL") from exc
    if not text.strip():
        raise ReturnError("SYSTEM3_RETURN_EMPTY")
    return raw


def materialize(body: str, output_path: Path) -> str:
    raw = decode_return(body)
    output_path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()
