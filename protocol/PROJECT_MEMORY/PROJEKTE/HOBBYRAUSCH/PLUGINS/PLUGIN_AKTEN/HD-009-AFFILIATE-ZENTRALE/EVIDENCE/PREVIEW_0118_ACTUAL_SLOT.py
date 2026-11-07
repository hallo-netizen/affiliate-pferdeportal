#!/usr/bin/env python3
"""Real CSS + 76px original theme wrapper regression in headless Chrome, four sizes."""
from pathlib import Path
import base64,zipfile,subprocess,tempfile,hashlib,html,shutil,re,json
from PIL import Image
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH")
zpath=root/"PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip"
hd007=root/"PLUGINS/ISOLIERTE_PLUGINS/HD-007-HOBBYREGISTER-CORE/CURRENT.zip"
evidence=root/"PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE"
with zipfile.ZipFile(zpath) as z,zipfile.ZipFile(hd007) as reg:
    css=z.read("affiliate-portal-router/assets/hdar-amazon-start.css").decode("utf8")
    badge=z.read("affiliate-portal-router/assets/hdar-amazon-available-at-amazon-de-official.png")
    malen=z.read("affiliate-portal-router/assets/hdar-ci-malen-zeichnen.webp")
    airbrush=reg.read("hd-hobbyregister-core/assets/portraits/final-masters/airbrush-modellbau.webp")
assert hashlib.sha256(badge).hexdigest()=="fb6db85f898078fa6df03740b58d65f431b8a6186c97f6b8a72e95f11b9ab8e5"
def data(raw,mime):return "data:"+mime+";base64,"+base64.b64encode(raw).decode()
THEME_CSS="""
/* Exact former fixed-height effect from real HD003 public CSS */
.hd-next-partner-banner{min-height:82px!important;overflow:hidden!important;border:1px solid #ddd!important;border-radius:5px!important;position:relative!important}
.hd-next-partner-banner>span{position:absolute!important;z-index:4!important;left:11px!important;top:8px!important;padding:3px 7px!important;color:#786e58;font-size:8px;background:rgba(255,255,255,.95)!important}
.hd-next-partner-banner>div,.hd-next-partner-banner>div>.ppar-affiliate-slot,.hd-next-partner-banner img{height:76px!important;min-height:76px!important;max-height:76px!important}
"""
def create(topic,photo,kind,width):
    body=f'''<div class="ppar-affiliate-slot hdar-ci-amazon-slot hdar-ci-amazon-slot-{kind}" data-ppar-slot="glossary_single_desktop_banner">
    <span class="hdar-ci-label">Anzeige</span>
    <a class="hdar-ci-amazon-banner hdar-ci-amazon-banner-{kind}" href="https://www.amazon.de/" rel="sponsored nofollow noopener noreferrer" target="_blank">
      <span class="hdar-ci-content"><strong class="hdar-ci-title">{html.escape(topic)}</strong></span>
      <span class="hdar-ci-photo"><img src="{data(photo,'image/webp')}" alt="{html.escape(topic)}" />
        <span class="hdar-ci-button"><img class="hdar-ci-amazon-official" src="{data(badge,'image/png')}" alt="Erhältlich bei Amazon"><span class="hdar-ci-amazon-arrow" aria-hidden="true">→</span></span>
      </span></a></div>'''
    if kind=="wide":
        body=f'<div class="hd-next-partner-banner hd-banner-span-3" aria-label="Anzeige · Partner"><span>Anzeige · Partner</span><div>{body}</div></div>'
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
        body{{background:#fff;font-family:Montserrat,Arial,sans-serif;margin:16px}}
        #testarea{{width:{width}px;max-width:100%}}
        {THEME_CSS}
        {css}
        </style></head><body>
        <div id="testarea">{body}</div>
        <script>
        window.addEventListener('load',function(){{
          var card=document.querySelector('.hdar-ci-amazon-banner');
          var wrap=document.querySelector('.hd-next-partner-banner');
          var photo=document.querySelector('.hdar-ci-photo');
          var logo=document.querySelector('.hdar-ci-amazon-official');
          var button=document.querySelector('.hdar-ci-button');
          var label=document.querySelector('.hdar-ci-label');
          var r=(x)=>x?{{w:Math.round(x.getBoundingClientRect().width),h:Math.round(x.getBoundingClientRect().height)}}:null;
          document.body.dataset.sizeReport=JSON.stringify({{card:r(card),wrap:r(wrap),photo:r(photo),badge:r(logo),button:r(button),labelDisplay:getComputedStyle(label).display,hasSiteLogo:!!document.querySelector('.hdar-ci-logo')}});
        }});
        </script>
        </body></html>'''
chrome=shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
assert chrome,"Headless browser missing"
cases=[
("square-large","Airbrush-Modellbau",airbrush,"square",700,780,800),
("square-sidebar","Airbrush-Modellbau",airbrush,"square",186,235,280),
("wide-page","Malen & Zeichnen",malen,"wide",770,830,370),
("wide-mobile","Malen & Zeichnen",malen,"wide",355,405,310),
]
for slug,topic,photo,kind,width,viewport_x,viewport_y in cases:
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp)
        page=tmp/"a.html";page.write_text(create(topic,photo,kind,width),encoding="utf8")
        shot=tmp/"screen.png"
        cmd=[chrome,"--headless","--no-sandbox","--disable-gpu","--hide-scrollbars","--disable-background-networking","--virtual-time-budget=1100",f"--window-size={viewport_x},{viewport_y}",f"--screenshot={shot}",page.as_uri()]
        res=subprocess.run(cmd,capture_output=True,text=True,timeout=90)
        assert res.returncode==0 and shot.exists(),(slug,res.returncode,res.stderr[-600:])
        result=subprocess.run([chrome,"--headless","--no-sandbox","--disable-gpu","--disable-background-networking","--virtual-time-budget=1100","--dump-dom",page.as_uri()],capture_output=True,text=True,timeout=90)
        assert result.returncode==0,(slug,result.stderr[-500:])
        m=re.search(r'data-size-report="([^"]+)"',result.stdout)
        assert m is not None,("Missing browser measurements",slug)
        measure=json.loads(html.unescape(m.group(1)))
        assert measure["card"]["h"]>80,(slug,measure)
        assert measure["photo"]["h"]>=round(measure["card"]["h"]*.65),(slug,measure)
        assert measure["badge"]["w"]>=140,(slug,measure)
        assert measure["button"]["w"]<=width,(slug,measure)
        assert not measure["hasSiteLogo"],(slug,measure)
        if kind=="wide":
            assert measure["wrap"]["h"]>110,(slug,measure)
            assert measure["labelDisplay"]=="none",(slug,measure)
        out=evidence/("HD009_0118_VARIANT4_"+slug.upper()+".jpg")
        Image.open(shot).convert('RGB').save(out,"JPEG",quality=83,optimize=True)
        print("CHROMIUM PASS",slug,measure,"screenshot",out.name,out.stat().st_size)
