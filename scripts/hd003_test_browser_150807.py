#!/usr/bin/env python3
"""Local browser integration test of the exact HD003 1.50.807 image and CSS layout.
Not a WordPress live test: markup is an isolated representative fixture.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re, html, base64, shutil

HERE=Path(__file__).parent
ROOT=HERE.parent
SCRIPT=(HERE/'build_150807.py').read_text() if (HERE/'build_150807.py').exists() else (HERE/'hd003_build_150807.py').read_text()
css=re.search(r"css = r'''(.*?)'''",SCRIPT,re.S).group(1).replace(r'\"','"')
hfile=ROOT/'hobbyfinder_lupe_approved.webp'
if not hfile.exists(): hfile=ROOT/'protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/ASSETS/hobbyfinder-lupe-approved-v150807.webp'
hero='data:image/webp;base64,'+base64.b64encode(hfile.read_bytes()).decode()
afile=ROOT/'hobbyfinder_ad_flat_approved.webp'
if not afile.exists(): afile=ROOT/'protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/ASSETS/hobbyfinder-banner-flat-approved-v150807.webp'
ad='data:image/webp;base64,'+base64.b64encode(afile.read_bytes()).decode()
fixture=f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
*{{box-sizing:border-box}}body{{margin:0;background:white;font-family:Arial,sans-serif;color:#12313e}}
.hd-mag-target-v150719{{max-width:1180px;margin:0 auto;padding:28px 20px}}
.hd-mag-hero-v150719{{background:#f4efe7;display:flex;min-height:220px;align-items:stretch;border-radius:8px;overflow:hidden}}
.hd-bp-hero-copy{{width:48%;padding:32px 35px;flex-shrink:0;z-index:1;align-self:center}}
.hd-bp-hero-copy .claim{{color:#138d92;font-style:italic}}
.hd-bp-hero-copy h1{{font-size:clamp(30px,3vw,47px);margin:12px 0 10px}}
.hd-bp-hero-copy p{{font-size:16px;line-height:1.4;margin:0}}
.hd-bp-hero-media{{width:52%;overflow:hidden}}
.hd-bp-hero-media img{{height:100%;width:100%;object-fit:cover;object-position:63% center;display:block}}
.hd-hf-rental-v150807{{margin-top:28px}}
@media(max-width:640px){{.hd-mag-target-v150719{{padding:15px}}.hd-mag-hero-v150719{{flex-direction:column;min-height:0}}
.hd-bp-hero-copy{{width:100%;padding:24px}}.hd-bp-hero-media{{width:100%;height:150px}}}}
{css}
</style></head><body><div class="hd-mag-target-v150719" data-hd-magazine-target="hobbyfinder">
<section class="hd-mag-hero-v150719"><div class="hd-bp-hero-copy"><span class="claim">Finde, was zu dir passt.</span><h1>Hobbyfinder</h1><p>Das passende Hobby für dich.</p></div>
<div class="hd-bp-hero-media"><img alt="Hobbyideen entdecken" src="{hero}"></div></section>
<section class="hd-rental hd-hf-rental-v150807"><div class="hd-hf-own-ad-v150807"><img src="{ad}" alt="Hobby Depot – Hier könnte Ihre Werbung stehen" width="1250" height="90">
<strong class="hd-hf-ad-mobile-title-v150807">Hier könnte Ihre Werbung stehen</strong>
<a href="https://hobby-depot.de/werbebedingungen/" class="hd-hf-ad-action-v150807 is-terms" aria-label="Werbebedingungen"><span>Werbebedingungen</span></a>
<a href="https://hobby-depot.de/preise/" class="hd-hf-ad-action-v150807 is-prices" aria-label="Preise"><span>Preise</span></a>
</div></section></div></body></html>'''
(HERE/'hobbyfinder_test_fixture_150807.html').write_text(fixture)

with sync_playwright() as pw:
    browser_path=shutil.which('chromium') or shutil.which('chromium-browser') or shutil.which('google-chrome')
    browser=pw.chromium.launch(headless=True, executable_path=browser_path,args=['--no-sandbox'])
    count=0
    for width in (1440,960,768,640,390,360):
        page=browser.new_page(viewport={'width':width,'height':850},device_scale_factor=1)
        page.set_content(fixture,wait_until='load')
        page.wait_for_timeout(180)
        assert page.locator('h1').inner_text()=='Hobbyfinder';count+=1
        assert page.locator('.hd-bp-hero-copy p').inner_text()=='Das passende Hobby für dich.';count+=1
        assert page.locator('.hd-bp-hero-media img').evaluate('(img)=>img.complete && img.naturalWidth > 0');count+=1
        assert page.locator('.hd-hf-own-ad-v150807>img').evaluate('(img)=>img.complete && img.naturalWidth > 0');count+=1
        assert page.locator('a.is-terms').get_attribute('href').endswith('/werbebedingungen/');count+=1
        assert page.locator('a.is-prices').get_attribute('href').endswith('/preise/');count+=1
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'Horizontal overflow {width}';count+=1
        a=page.locator('a.is-terms').bounding_box();b=page.locator('a.is-prices').bounding_box()
        assert a and b and a['width']>0 and b['width']>0 and a['x']+a['width'] <= width+1 and b['x']+b['width']<=width+1,(width,a,b);count+=1
        assert a['x']+a['width'] < b['x']+2,(width,'overlapping links');count+=1
        if width<=640:
            assert page.locator('.hd-hf-own-ad-v150807>img').is_hidden();count+=1
            assert page.locator('.hd-hf-ad-mobile-title-v150807').is_visible();count+=1
            assert page.locator('a.is-terms span').is_visible();count+=1
            assert page.locator('a.is-prices span').is_visible();count+=1
            assert a['height']>=39 and b['height']>=39;count+=1
            assert a['width']>=95 and b['width']>=56,('mobile link labels clipped',width,a,b);count+=1
        else:
            assert page.locator('.hd-hf-own-ad-v150807>img').is_visible();count+=1
            assert page.locator('.hd-hf-ad-mobile-title-v150807').is_hidden();count+=1
        page.screenshot(path=str(HERE/f'hobbyfinder-150807-{width}px.png'),full_page=True)
        print(f'BROWSER_PASS {width}px | banner height={page.locator(".hd-hf-own-ad-v150807").bounding_box()["height"]:.1f}px | links={a["width"]:.1f}/{b["width"]:.1f}')
        page.close()
    browser.close()
print('TOTAL_ASSERTIONS_PASS',count)