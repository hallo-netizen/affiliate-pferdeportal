#!/usr/bin/env python3
"""Proves real WordPress DOM after footer hook and HD007 responsive CSS – desktop and mobile."""
import subprocess,shutil,re,html,json
from pathlib import Path
chrome=shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
assert chrome,"Chromium is not installed"
url="http://127.0.0.1:8989/hobbyregister/airbrush-modellbau/"
report=[]
for label,width,height in [("desktop",1420,1000),("mobile",430,900)]:
    cmd=[chrome,"--headless","--no-sandbox","--disable-gpu","--disable-background-networking","--hide-scrollbars",
         f"--window-size={width},{height}","--virtual-time-budget=2400","--dump-dom",url]
    p=subprocess.run(cmd,capture_output=True,text=True,timeout=95)
    assert p.returncode==0,(label,p.stderr[-1300:])
    m=re.search(r'data-hd009-e2e="([^"]+)"',p.stdout)
    assert m,(label,"WordPress did not emit a browser placement report",p.stdout[-1200:])
    d=json.loads(html.unescape(m.group(1)))
    print("REAL WORDPRESS",label,json.dumps(d,ensure_ascii=False))
    assert d["sideIndex"]==d["factsIndex"]+1,(label,"Ad must follow facts in original sidebar")
    assert d["groupIndex"]==d["sideIndex"]+1,(label,"Hobbygruppe must follow ad")
    assert d["inlineAfterEquipment"],(label,"Article slot must follow Kosten und Ausrüstung")
    assert not d["sideHidden"] and not d["inlineHidden"],(label,"Both visible")
    assert d["sideAdCount"]==1,(label,"One square sidebar banner")
    assert d["inlineAdCount"]==1,(label,"One in-article banner")
    if label=="desktop":
        assert d["factsRect"][1]<=d["sideRect"][0]+2,(label,"Ad after facts")
        assert d["sideRect"][1]<=d["groupRect"][0]+2,(label,"Ad before hobby group")
    else:
        assert d["mainRect"][1]<=d["sideRect"][0]+3,(label,"Mobile sidebar ad must occur AFTER article")
        assert d["sideRect"][1]<=d["groupRect"][0]+3,(label,"Mobile sidebar ad first below article")
        assert d["sideGridArea"]=="tail",(label,"HD007 mobile layout has facts/copy/tail; ad must be tail")
    report.append(d)
proof=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/HD009_0119_WP_REAL_BROWSER_PASS.txt")
proof.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in report)+"\nREAL WordPress+MariaDB+HD007+HD003+HD009 DOM PASS: desktop and mobile after render and CSS\n",encoding="utf8")
print("PASS all actual WordPress DOM placement checks")
