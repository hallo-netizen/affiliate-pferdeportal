#!/usr/bin/env python3
"""Apply C22 472-category second wave to the exact existing 1.14.8.30 plugin tree.

Inputs must already be present:
  includes/class-apkw-c22-472-add-only.php
  profiles/hab-und-bewahr-c22-472-add-only.json
Never edits WordPress or reruns the original C22 importer.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("affiliate-portal-kategorie-workflow")
def patch(file_name, needle, replacement):
    p = root / file_name
    old = p.read_text(encoding="utf-8")
    if old.count(needle) != 1:
        raise RuntimeError(f"Unexpected input; patch cancelled: {file_name}: {old.count(needle)} matches")
    p.write_text(old.replace(needle, replacement), encoding="utf-8")

if not (root / "includes/class-apkw-c22-472-add-only.php").is_file():
    raise RuntimeError("Verified second-wave PHP module missing")
if not (root / "profiles/hab-und-bewahr-c22-472-add-only.json").is_file():
    raise RuntimeError("Verified 472-category manifest missing")
patch("affiliate-portal-kategorie-workflow.php",
      "* Version: 1.14.8.30", "* Version: 1.14.8.31")
patch("affiliate-portal-kategorie-workflow.php",
      "APKW_C22_AddOnly::init();",
      "APKW_C22_AddOnly::init();\n\n"
      "// C22 category-only second wave. Original 743 jobs are never replayed.\n"
      "require_once APKW_DIR.'includes/class-apkw-c22-472-add-only.php';\n"
      "APKW_C22_472_AddOnly::init();")
patch("includes/class-apkw-c22-fachpruefung.php",
      "if (class_exists('APKW_C22_AddOnly')) APKW_C22_AddOnly::render_controls();",
      "if (class_exists('APKW_C22_AddOnly')) APKW_C22_AddOnly::render_controls();\n"
      "        if (class_exists('APKW_C22_472_AddOnly')) APKW_C22_472_AddOnly::render_controls();")
patch("includes/class-apkw-c22-add-only.php",
      "if($rev!==$expected || (string)($snapshot['revision']??'')!==$expected)\n"
      "            $errors[]='C22_REVISION_MISMATCH';",
      "$revised=$expected;\n"
      "        if(class_exists('APKW_C22_472_AddOnly') &&\n"
      "           (APKW_C22_472_AddOnly::state()['status']??'')==='COMPLETE') {\n"
      "            // Revision from second category wave; audit all 472 new terms independently.\n"
      "            $extra=APKW_C22_472_AddOnly::completion_audit();\n"
      "            if(empty($extra['valid']))$errors[]='C22_SECOND_WAVE_INVALID';\n"
      "            $revised=(string)($extra['revision']??'');\n"
      "        }\n"
      "        if($rev!==$revised || (string)($snapshot['revision']??'')!==$revised)\n"
      "            $errors[]='C22_REVISION_MISMATCH';")
with (root / "README.txt").open("a", encoding="utf-8") as f:
    f.write("\n\nVersion 1.14.8.31 – Hab & Bewahr C2.2 second category-only wave\n")
    f.write("Adds only 472 flat WordPress categories under 172 existing topic pages. ")
    f.write("No old 743 nodes, historic categories, posts, URLs or bindings are changed. ")
    f.write("20 small steps per AJAX request, protected rollback and separate admin approval.\n")
print("APKW 1.14.8.31 C22 472 additive plugin patch applied.")
