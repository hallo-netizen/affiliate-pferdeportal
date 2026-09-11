from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROMPT = ROOT / "codex_prompt.md"
INPUT = ROOT / "live_fixture" / "wordpress_input.json"
TOKEN = ROOT / ".cloud_entry.json"
OUTPUT = ROOT / "codex_output.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def start() -> int:
    if not PROMPT.is_file() or not INPUT.is_file():
        print("SYSTEM3_CLOUD_ENTRY_FAIL")
        return 2
    token = {
        "prompt_sha256": sha256(PROMPT),
        "input_sha256": sha256(INPUT),
        "allowed_output": "isolated_system3/codex_output.md",
        "publish": False,
    }
    TOKEN.write_text(json.dumps(token, sort_keys=True), encoding="utf-8")
    print("SYSTEM3_CLOUD_ENTRY_PASS")
    return 0


def verify() -> int:
    if not TOKEN.is_file() or not OUTPUT.is_file():
        print("SYSTEM3_CLOUD_VERIFY_FAIL")
        return 3
    token = json.loads(TOKEN.read_text(encoding="utf-8"))
    ok = (
        token.get("prompt_sha256") == sha256(PROMPT)
        and token.get("input_sha256") == sha256(INPUT)
        and token.get("allowed_output") == "isolated_system3/codex_output.md"
        and token.get("publish") is False
        and OUTPUT.stat().st_size > 0
    )
    print("SYSTEM3_CLOUD_VERIFY_PASS" if ok else "SYSTEM3_CLOUD_VERIFY_FAIL")
    return 0 if ok else 4


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in {"start", "verify"}:
        print("USAGE: cloud_entry.py start|verify")
        return 1
    return start() if sys.argv[1] == "start" else verify()


if __name__ == "__main__":
    raise SystemExit(main())
