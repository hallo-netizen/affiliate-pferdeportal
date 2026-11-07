#!/usr/bin/env python3
"""Preview actual WordPress CI CSS and unmodified HD003 assets, no third-party resources."""
from pathlib import Path
from PIL import Image
import subprocess,tempfile,zipfile,base64,shutil,html,hashlib
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH")
zip_path=root/"PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip"
evidence=root/"PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE"
with zipfile.ZipFile(zip_path) as z:
    base="affiliate-portal-router/assets/"
    css=z.read(base+"hdar-amazon-start.css").decode('utf8')
    logo=z.read(base+"hdar-ci-logo-original.png")
    wide=z.read(base+"hdar-ci-malen-zeichnen.webp")
    square=z.read(base+"hdar-ci-modellbau.webp")
def data(b,mime):return "data:"+mime+";base64,"+base64.b64encode(b).decode('ascii')
def page(topic,photo,size):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
    body{{font-family:Montserrat,Arial,sans-serif;background:#fff;margin:0;padding:18px;}}
    .container{{max-width:1200px;margin:auto;}}
    {css}
    </style></head><body><div class="container">
    <div class="ppar-affiliate-slot hdar-ci-amazon-slot hdar-ci-amazon-slot-{size}">
      <span class="hdar-ci-label">Anzeige</span>
      <a class="hdar-ci-amazon-banner hdar-ci-amazon-banner-{size}" href="https://www.amazon.de/" target="_blank">
        <span class="hdar-ci-content">
          <img class="hdar-ci-logo" src="{data(logo,'image/png')}" alt="Hobby Depot">
          <span class="hdar-ci-subline">Entdecke deine Ausrüstung</span>
          <strong class="hdar-ci-title">{html.escape(topic)}</strong>
          <span class="hdar-ci-button">Bei Amazon entdecken</span>
        </span><span class="hdar-ci-photo"><img src="{data(photo,'image/webp')}" alt="{html.escape(topic)}"></span>
      </a></div></div></body></html>'''
chrome=shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
assert chrome,"No headless browser available to verify actual CSS."
for topic,photo,size,width,height,output in [
    ("Malen & Zeichnen",wide,"wide",1260,390,"HD009_0117_BANNER_WIDE_CI_PREVIEW.jpg"),
    ("Modellbau",square,"square",780,840,"HD009_0117_BANNER_SQUARE_CI_PREVIEW.jpg")
]:
    with tempfile.TemporaryDirectory() as temp:
        basepath=Path(temp)
        doc=basepath/"preview.html";doc.write_text(page(topic,photo,size),encoding="utf8")
        screen=basepath/"screen.png"
        cmd=[chrome,"--headless","--no-sandbox","--disable-gpu","--hide-scrollbars","--disable-background-networking",f"--window-size={width},{height}",f"--screenshot={screen}",doc.as_uri()]
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=65)
        assert p.returncode==0 and screen.is_file(),f"Chrome QA failure: {p.returncode} {p.stderr[-500:]}"
        im=Image.open(screen).convert("RGB")
        dest=evidence/output
        im.save(dest,format="JPEG",quality=78,optimize=True)
        print("VISUAL PASS",size,im.size,dest.stat().st_size,hashlib.sha256(dest.read_bytes()).hexdigest())
