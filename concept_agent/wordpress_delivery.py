"""Final Concept-Agent boundary: only the proven Redaktionsplan upload payload may leave as WordPress file."""
from __future__ import annotations
import json
from wordpress_output_contract import assert_wordpress_ready

FINAL_FILENAME="GEN1_7_ARTIKEL_WORDPRESS_REDAKTIONSPLAN_UPLOAD_107008_PASS.json"

def wordpress_delivery_bytes(pkg:dict)->bytes:
    assert_wordpress_ready(pkg)
    return (json.dumps(pkg,ensure_ascii=False,indent=2)+"\n").encode("utf-8")

def wordpress_delivery_filename(pkg:dict)->str:
    assert_wordpress_ready(pkg)
    return FINAL_FILENAME
