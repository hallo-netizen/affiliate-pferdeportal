#!/usr/bin/env python3
"""Temporary offline source inspection, no credentials loaded and no WP connection."""
from pathlib import Path
import re,zipfile
p=Path(__file__).resolve().parents[1]/"PLUGINS"/"WASSERTECHNIK_KATEGORIE_WORKFLOW_0.1.4_FORTSETZUNG_OHNE_NEUSTART_NUR_TEST.zip"
wanted={"class-wassertechnik-paid-research.php":["boot","verify_site","auth","planned","panel","fetch","cost","paid","export"],
"class-wassertechnik-dataforseo.php":["boot","credentials","has_credentials","free_request","build_preflight","post_preflight","screen"]}
with zipfile.ZipFile(p) as z:
 for name in z.namelist():
  short=name.rsplit("/",1)[-1]
  if short not in wanted:continue
  src=z.read(name).decode("utf-8")
  for method in wanted[short]:
   matches=list(re.finditer(r"(?:public|private|protected)\s+static\s+function\s+"+re.escape(method)+r"\s*\(",src))
   if not matches:continue
   start=matches[0].start()
   brace=src.find("{",start)
   if brace<0:continue
   depth=1
   for idx in range(brace+1,len(src)):
    if src[idx]=="{":depth+=1
    if src[idx]=="}":
     depth-=1
     if depth==0:break
   # source-only, no stored WP credentials or live data
   print("BEGIN_W38_SOURCE",short,method)
   print(src[start:idx+1])
   print("END_W38_SOURCE",short,method)
