from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'codex_output.md'


def start() -> int:
    required = [ROOT/'codex_prompt.md', ROOT/'live_fixture'/'wordpress_input.json']
    if not all(p.is_file() for p in required):
        print('SYSTEM3_CLOUD_ENTRY_FAIL:MISSING_REQUIRED_INPUT')
        return 2
    print('SYSTEM3_CLOUD_ENTRY_PASS')
    return 0


def verify() -> int:
    if not OUT.is_file():
        print('SYSTEM3_VERIFY_FAIL:OUTPUT_MISSING')
        return 2
    text = OUT.read_text(encoding='utf-8').strip()
    if len(text.split()) < 120:
        print('SYSTEM3_VERIFY_FAIL:OUTPUT_TOO_SHORT')
        return 2
    print(f'SYSTEM3_VERIFY_PASS:{len(text.split())}')
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in {'start','verify'}:
        print('SYSTEM3_CLOUD_ENTRY_FAIL:BAD_COMMAND')
        raise SystemExit(2)
    raise SystemExit(start() if sys.argv[1] == 'start' else verify())
