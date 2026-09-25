from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from isolated_system3.live_adapter import run_live_boundary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    envelope = run_live_boundary(
        args.input,
        args.evidence,
        args.output,
        {
            "ratgeber": "PROFILE_RATGEBER_LIVE_TEST_V1",
            "produktvergleich": "PROFILE_PRODUKTVERGLEICH_LIVE_TEST_V1",
        },
    )
    print(json.dumps({
        "status": "SYSTEM3_LIVE_BOUNDARY_PASS",
        "article_id": envelope["result"]["article_id"],
        "output_hash": envelope["result"]["output_hash"],
        "envelope_hash": envelope["envelope_hash"],
        "publish_allowed": envelope["publish_allowed"],
        "wordpress_write_allowed": envelope["wordpress_write_allowed"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
