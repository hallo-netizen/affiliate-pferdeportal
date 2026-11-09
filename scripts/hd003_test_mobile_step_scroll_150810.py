#!/usr/bin/env python3
"""Run the actual HD003 1.50.810 Hobbyfinder JS in responsive Playwright fixtures."""
from pathlib import Path
import zipfile,re,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
ZIP=ROOT/'dist/HOBBY_DEPOT_DESIGN_HD003_1.50.810_MOBILE_WEITER_SCROLL.zip'
SOURCE='affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php'
with zipfile.ZipFile(ZIP) as z:
    php=z.read(SOURCE).decode('utf8')
    assert z.testzip() is None
start=php.index('<script id="hd-hf-script-v150705">')+len('<script id="hd-hf-script-v150705">')
end=php.index('</script>',start)
js=php[start:end]
hobby={'id':'test-1','name':'Münzen sammeln','world':'sammeln','image':'','url':'/sammeln/muenzen/',
'motivation':[],'social':[],'location':[],'time':'unter_30_min','budget':'0_bis_25','rental':'leicht','space':'minimal',
'physical':1,'schedule':'jederzeit_spontan','continuity':'jederzeit_pausierbar','surprise':0,
'profile':{'what_is_it':'Sammlungen aufbauen','what_do_you_do':'Münzen ordnen','what_do_you_need':'Album','appeal':'Entdecken'}}
substitutions={
'<?php echo $json; ?>':json.dumps([hobby],ensure_ascii=False),
'<?php echo $hero_json; ?>':json.dumps('https://example.com/unused.jpg'),
"<?php echo $embedded_magazine_v150719 ? 'true' : 'false'; ?>":'true',
}
for old,new in substitutions.items():
    assert js.count(old)==1,(old,js.count(old))
    js=js.replace(old,new,1)
assert '<?php' not in js
assert 'mobileScrollToNextStepV150810()' in js
assert "app.querySelector('.hd-hf-panel,.hd-hf-results-head')" in js
css_start=php.index('<style id="hd-hf-style-v150705">')+len('<style id="hd-hf-style-v150705">')
css_end=php.index('</style>',css_start)
css=php[css_start:css_end]
assert '.hd-hf-choices,.hd-hf-grid{grid-template-columns:1fr}' in css
page_html='''<!doctype html><html lang="de"><head><meta name="viewport" content="width=device-width,initial-scale=1"/>
<style>
 body{margin:0;font-family:Arial,sans-serif}
 .hd-head-v150616{height:64px;background:#f7f8f9;border-bottom:1px solid #bbb;position:sticky;top:0;z-index:10;box-sizing:border-box;padding:14px}
 .before{height:1100px;background:#f9fafb}
 .after{height:1500px}
 </style>
 <style>'''+css+'''</style></head><body>
 <header class="hd-head-v150616">Dein Hobby Depot</header>
 <div class="before">Inhalt vor dem Hobbyfinder</div>
 <section class="hd-hf"><div class="hd-hf-inner" id="hd-hf-app"></div></section>
 <div class="after"></div>
 <script>
 window.__scrollCalls=[];
 const oldScrollTo=window.scrollTo.bind(window);
 window.scrollTo=function(){window.__scrollCalls.push([...arguments]);oldScrollTo(...arguments)};
 </script>
 <script>'''+js+'''</script></body></html>'''
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    for width in (360,390,700,1024):
        page=browser.new_page(viewport={'width':width,'height':790},is_mobile=(width<800),has_touch=(width<800),device_scale_factor=1)
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content(page_html,wait_until='load')
        assert page.locator('.hd-hf-panel').count()==1,('missing question panel',width,errors)
        before_count=page.evaluate('window.__scrollCalls.length')
        for step in range(1,9):
            page.locator('[data-pick="egal"]').first.click(timeout=8000)
            page.locator('[data-action="next"]').click(timeout=8000)
            page.wait_for_timeout(90)
            node='.hd-hf-results-head' if step==8 else '.hd-hf-panel'
            assert page.locator(node).count()==1,(width,step,'missing next step',errors)
            m=page.evaluate("""selector => {
                const t=document.querySelector(selector);
                const choice=document.querySelector('.hd-hf-choice');
                const rect=t.getBoundingClientRect();
                const first=choice?.getBoundingClientRect();
                return {top:rect.top,firstTop:first?.top,header:document.querySelector('.hd-head-v150616').getBoundingClientRect().height,scroll:window.scrollY,calls:window.__scrollCalls.length,question:document.querySelector('.hd-hf-question')?.textContent};
            }""",node)
            if width<=720:
                assert 65<=m['top']<=115,(width,step,m)
                if step<8: assert m['firstTop']<790,(width,step,m)
                assert m['calls']==before_count+step,(width,step,m)
            else:
                assert m['calls']==before_count,(width,step,m)
            print('NEXT_SCROLL_PASS',width,'STEP',step,'METRICS',m)
        assert not errors,(width,errors)
        page.close()
    browser.close()
print('ACTUAL_HOBBYFINDER_JS_ALL_EIGHT_STEPS_MOBILE_AND_DESKTOP_PASS')
