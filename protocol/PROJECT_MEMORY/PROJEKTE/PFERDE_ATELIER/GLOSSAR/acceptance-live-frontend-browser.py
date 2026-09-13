#!/usr/bin/env python3
from pathlib import Path
import argparse, asyncio, json, os, re
from playwright.async_api import async_playwright

parser=argparse.ArgumentParser()
parser.add_argument('frontend_php')
args=parser.parse_args()
src=Path(args.frontend_php).read_text(encoding='utf-8')

# Use the candidate's own inline CSS.
marker="return '.uge{'.$v.'"
if marker not in src:
    raise SystemExit('ACCEPT_BROWSER_SOURCE_PARSE_FAIL:CSS')
start=src.index(marker)+len(marker)
end=src.index("';\n    }\n}",start)
css='.uge{--uge-olive:#35422A;--uge-olive2:#4F5C43;--uge-ochre:#9A6400;--uge-paper:#F9F7F2;--uge-text:#172018;--uge-muted:#5e665f;--uge-line:#e7ebe7;--uge-surface:#fff;'+src[start:end]

# Use the candidate's actual search DOM literal instead of inventing a fixed test DOM.
m=re.search(r"printf\('(<form class=\"uge-search-form\".*?uge-search-suggestions.*?</div>)',\s*esc_url\(self::home_url\(\)\)",src,re.S)
if not m:
    raise SystemExit('ACCEPT_BROWSER_SOURCE_PARSE_FAIL:SEARCH_DOM')
search_html=m.group(1)
if search_html.count('%s') != 4:
    raise SystemExit('ACCEPT_BROWSER_SOURCE_PARSE_FAIL:SEARCH_PLACEHOLDERS')
search_html=search_html % ('#','/ajax','nonce','rö')
# Suggestions must be visible so geometry can be measured. Populate the exact candidate container.
search_html=search_html.replace(' hidden></div>','><a class="uge-suggestion">Ganache</a><a class="uge-suggestion">Röhrbein</a><a class="uge-suggestion">Widerrist</a></div>')

html=f'''<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;padding:0}}body{{font-family:Arial,sans-serif}}.site-content{{padding-top:18px}}.ast-container{{max-width:1320px;margin:0 auto}}
{css}
</style></head><body class="uge-glossary-home"><div class="site-content"><div class="ast-container"><main id="primary"><div class="entry-content"><div class="uge">
<section class="uge-hero"><img class="uge-hero-image"><i></i><div class="uge-hero-copy"><span>Glossar</span><h1>Pferdewissen</h1><p>Begriffe schnell finden und verständlich nachschlagen.</p></div></section>
<div class="uge-tools">{search_html}<nav class="uge-az"><a>A</a><a>B</a></nav></div>
</div></div></main></div></div></body></html>'''

async def main():
    failures=[]; measurements={}
    async with async_playwright() as pw:
        launch={'headless':True,'args':['--no-sandbox']}
        if os.environ.get('CHROMIUM_PATH'):
            launch['executable_path']=os.environ['CHROMIUM_PATH']
        browser=await pw.chromium.launch(**launch)
        for width in (1200,900,720,500):
            page=await browser.new_page(viewport={'width':width,'height':1000})
            await page.set_content(html,wait_until='load')
            m=await page.evaluate('''() => {const b=s=>{const r=document.querySelector(s).getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height,b:r.bottom,r:r.right}};return {hero:b('.uge-hero'),img:b('.uge-hero-image'),input:b('.uge-search-form input'),form:b('.uge-search-form'),sug:b('.uge-search-suggestions')}}''')
            measurements[width]=m
            gap=abs(m['sug']['y']-m['input']['b'])
            xgap=abs(m['sug']['x']-m['form']['x'])
            wgap=abs(m['sug']['w']-m['form']['w'])
            if gap>3 or xgap>3 or wgap>3:
                failures.append(f'AJAX_POSITION_FAIL:{width}:vertical={gap:.1f}:x={xgap:.1f}:width={wgap:.1f}')
            await page.close()
        await browser.close()

    hs=[measurements[w]['img']['h'] for w in (1200,900,720,500)]
    ws=[measurements[w]['img']['w'] for w in (1200,900,720,500)]
    if not (ws[0]>ws[1]>ws[2]>ws[3]):
        failures.append('HERO_WIDTH_RESPONSIVE_FAIL:'+','.join(f'{v:.1f}' for v in ws))
    if not (hs[0]>hs[1]+10 and hs[1]>hs[2]+10 and hs[2]>hs[3]+10):
        failures.append('HERO_HEIGHT_RESPONSIVE_FAIL:'+','.join(f'{v:.1f}' for v in hs))

    print('ACCEPT_BROWSER_MEASUREMENTS='+json.dumps(measurements,separators=(',',':')))
    if failures:
        for f in failures: print(f)
        raise SystemExit(1)
    print('ACCEPT_BROWSER_AJAX_POSITION_PASS')
    print('ACCEPT_BROWSER_HERO_RESPONSIVE_PASS')
    print('ACCEPT_BROWSER_PASS')

asyncio.run(main())
