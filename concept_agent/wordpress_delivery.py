"""Letzte Concept-Agent-Grenze: Nur ein echt signiertes ENDSTEMPEL-Paket darf als WordPress-Datei ausgegeben werden."""
from __future__ import annotations
import json
from wordpress_output_contract import assert_wordpress_ready

FINAL_FILENAME="GEN1_7_ARTIKEL_PSERC_APPROVED_PRODUCTION_PACKAGE_107008_FINAL.json"

def wordpress_delivery_bytes(pkg:dict)->bytes:
    assert_wordpress_ready(pkg)
    return (json.dumps(pkg,ensure_ascii=False,indent=2)+"\n").encode("utf-8")

def wordpress_delivery_filename(pkg:dict)->str:
    assert_wordpress_ready(pkg)
    return FINAL_FILENAME
