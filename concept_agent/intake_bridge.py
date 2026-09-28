#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from concept_agent.konzept8_verbot.engine import k8_intake_bridge as _k8

for _name in dir(_k8):
    if not _name.startswith("__"):
        globals()[_name] = getattr(_k8, _name)

if __name__ == "__main__":
    raise SystemExit(_k8.main(sys.argv))
