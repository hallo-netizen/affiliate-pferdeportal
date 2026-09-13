#!/usr/bin/env python3
import asyncio, json
from playwright.async_api import async_playwright

BASE='http://127.0.0.1:8080'

async def main():
    failures=[]
    measurements={}
    async with async_playwright() as pw:
        browser=await pw.chromium.launch(headless=True,args=['--no-sandbox'])
        for width in (1200,900,720,500):
            page=await browser.new_page(viewport={'width':width,'height':1200})
            r=await page.goto(BASE+'/glossar/',wait_until='networkidle')
            if r.status != 200: failures.append(f'HOME_HTTP:{width}:{r.status}')
            await page.locator('#uge-search').fill('Hu')
            await page.wait_for_timeout(800)
            if not await page.locator('.uge-search-suggestions').is_visible():
                failures.append(f'AJAX_SUGGESTIONS_NOT_VISIBLE:{width}')
            else:
                txt=await page.locator('.uge-search-suggestions').inner_text()
                if 'Hufbein' not in txt or 'Hufpflege' not in txt:
                    failures.append(f'AJAX_RESULTS_WRONG:{width}:{txt[:120]}')
            m=await page.evaluate('''() => {
              const b=s=>{const e=document.querySelector(s); if(!e)return null; const r=e.getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height,b:r.bottom}};
              const img=document.querySelector('.uge-hero-image');
              return {hero:b('.uge-hero'),img:b('.uge-hero-image'),form:b('.uge-search-form'),input:b('#uge-search'),sug:b('.uge-search-suggestions'),natural:img?{w:img.naturalWidth,h:img.naturalHeight}:null};
            }''')
            measurements[width]=m
            if not all(m[k] for k in ('hero','img','form','input','sug','natural')):
                failures.append(f'MISSING_FRONTEND_GEOMETRY:{width}:{m}')
            else:
                gap=abs(m['sug']['y']-m['input']['b'])
                if gap>4: failures.append(f'AJAX_VERTICAL_POSITION_FAIL:{width}:{gap:.1f}')
                if abs(m['sug']['x']-m['form']['x'])>4 or abs(m['sug']['w']-m['form']['w'])>4:
                    failures.append(f'AJAX_HORIZONTAL_POSITION_FAIL:{width}')
                # Real responsive image requirement: image itself controls its size,
                # stays within the hero and preserves the actual image ratio.
                if abs(m['img']['w']-m['hero']['w'])>2:
                    failures.append(f'HERO_IMAGE_WIDTH_NOT_FLUID:{width}:{m}')
                nr=m['natural']['h']/m['natural']['w']
                rr=m['img']['h']/m['img']['w']
                if abs(nr-rr)>0.015:
                    failures.append(f'HERO_IMAGE_RATIO_CHANGED:{width}:natural={nr:.4f}:rendered={rr:.4f}')
            await page.close()

        ws=[measurements[w]['img']['w'] for w in (1200,900,720,500)]
        hs=[measurements[w]['img']['h'] for w in (1200,900,720,500)]
        if not (ws[0]>ws[1]>ws[2]>ws[3]): failures.append('HERO_WIDTH_NOT_RESPONSIVE:'+str(ws))
        if not (hs[0]>hs[1]>hs[2]>hs[3]): failures.append('HERO_HEIGHT_NOT_RESPONSIVE:'+str(hs))

        page=await browser.new_page(viewport={'width':1200,'height':1400})
        # Correct requirement: category has its own category content but the same
        # complete visual shell as the Glossar start page.
        r=await page.goto(BASE+'/glossar/gesundheit/',wait_until='networkidle')
        if r.status != 200: failures.append(f'CATEGORY_HTTP:{r.status}')
        for sel,label in [('.uge-category-head','CATEGORY_HEAD_MISSING'),('.uge-hero','CATEGORY_HERO_MISSING'),('.uge-tools','CATEGORY_TOOLS_MISSING'),('.uge-topic-nav','CATEGORY_TOPIC_NAV_MISSING')]:
            if await page.locator(sel).count()!=1: failures.append(label)
        if await page.locator('.uge-category-head h1').inner_text() != 'Gesundheit': failures.append('CATEGORY_H1_WRONG')
        links=page.locator('a[href*="/glossar/begriff/hufbein/"]')
        if await links.count()<1:
            failures.append('CATEGORY_TERM_LINK_MISSING')
        else:
            # Click the real rendered link instead of merely opening a hardcoded URL.
            await links.first.click()
            await page.wait_for_load_state('networkidle')
            if '/glossar/begriff/hufbein/' not in page.url: failures.append('TERM_LINK_WRONG_DESTINATION:'+page.url)
            if await page.locator('article.uge-single-wrap').count()!=1: failures.append('TERM_CLICK_ARTICLE_MISSING')
            if 'FULL-HUFBEIN-SENTINEL' not in await page.content(): failures.append('TERM_CLICK_CONTENT_MISSING')

        r=await page.goto(BASE+'/glossar/begriff/nicht-da/',wait_until='domcontentloaded')
        if r.status != 404: failures.append(f'MISSING_TERM_NOT_404:{r.status}')
        r=await page.goto(BASE+'/glossar/begriff/hufentwurf/',wait_until='domcontentloaded')
        if r.status != 404: failures.append(f'DRAFT_PUBLIC:{r.status}')
        await browser.close()

    print('REAL_DESIGN_029_BROWSER_MEASUREMENTS='+json.dumps(measurements,separators=(',',':')))
    if failures:
        for f in failures: print(f)
        raise SystemExit(1)
    print('REAL_DESIGN_029_AJAX_PASS')
    print('REAL_DESIGN_029_TRUE_RESPONSIVE_IMAGE_PASS')
    print('REAL_DESIGN_029_CATEGORY_FULL_SHELL_PASS')
    print('REAL_DESIGN_029_CLICKED_TERM_LINK_PASS')
    print('REAL_DESIGN_029_NEGATIVE_PASS')
    print('REAL_DESIGN_029_BROWSER_PASS')

asyncio.run(main())
