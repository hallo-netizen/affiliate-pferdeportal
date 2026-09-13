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
            page=await browser.new_page(viewport={'width':width,'height':1100})
            await page.goto(BASE+'/glossar/',wait_until='networkidle')
            # Real page and real AJAX UI, not an invented DOM.
            await page.locator('#uge-search').fill('Hu')
            await page.wait_for_timeout(800)
            visible=await page.locator('.uge-search-suggestions').is_visible()
            if not visible:
                failures.append(f'AJAX_SUGGESTIONS_NOT_VISIBLE:{width}')
            else:
                txt=await page.locator('.uge-search-suggestions').inner_text()
                if 'Hufbein' not in txt or 'Hufpflege' not in txt:
                    failures.append(f'AJAX_RESULTS_WRONG:{width}:{txt[:120]}')
            m=await page.evaluate('''() => {
              const b=s=>{const e=document.querySelector(s); if(!e)return null; const r=e.getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height,b:r.bottom}};
              return {hero:b('.uge-hero'),img:b('.uge-hero-image'),form:b('.uge-search-form'),input:b('#uge-search'),sug:b('.uge-search-suggestions')};
            }''')
            measurements[width]=m
            if not all(m[k] for k in ('hero','img','form','input','sug')):
                failures.append(f'MISSING_FRONTEND_GEOMETRY:{width}:{m}')
            else:
                gap=abs(m['sug']['y']-m['input']['b'])
                xgap=abs(m['sug']['x']-m['form']['x'])
                wgap=abs(m['sug']['w']-m['form']['w'])
                if gap>4 or xgap>4 or wgap>4:
                    failures.append(f'AJAX_POSITION_FAIL:{width}:v={gap:.1f}:x={xgap:.1f}:w={wgap:.1f}')
            await page.close()

        hs=[measurements[w]['img']['h'] for w in (1200,900,720,500)]
        ws=[measurements[w]['img']['w'] for w in (1200,900,720,500)]
        if not (ws[0]>ws[1]>ws[2]>ws[3]): failures.append('HERO_WIDTH_FAIL:'+str(ws))
        if not (hs[0]>hs[1]+10 and hs[1]>hs[2]+10 and hs[2]>hs[3]+10): failures.append('HERO_HEIGHT_FAIL:'+str(hs))

        page=await browser.new_page(viewport={'width':1200,'height':1100})
        # Real category must not collapse to home.
        r=await page.goto(BASE+'/glossar/gesundheit/',wait_until='networkidle')
        if r.status != 200: failures.append(f'CATEGORY_HTTP:{r.status}')
        if await page.locator('.uge-category-head').count()!=1: failures.append('CATEGORY_HEAD_MISSING')
        if await page.locator('.uge-hero').count()!=0: failures.append('CATEGORY_WRONGLY_HOME_HERO')
        if await page.locator('.uge-tools').count()!=0: failures.append('CATEGORY_WRONGLY_HOME_TOOLS')
        if await page.locator('a[href*="/glossar/begriff/hufbein/"]').count()<1: failures.append('CATEGORY_TERM_LINK_MISSING')
        # Real single term must contain actual glossary article and sentinel content.
        r=await page.goto(BASE+'/glossar/begriff/hufbein/',wait_until='networkidle')
        if r.status != 200: failures.append(f'TERM_HTTP:{r.status}')
        if await page.locator('article.uge-single-wrap').count()!=1: failures.append('TERM_ARTICLE_MISSING')
        body=await page.content()
        if 'FULL-HUFBEIN-SENTINEL' not in body: failures.append('TERM_CONTENT_MISSING')
        # Negative routes.
        r=await page.goto(BASE+'/glossar/begriff/nicht-da/',wait_until='domcontentloaded')
        if r.status != 404: failures.append(f'MISSING_TERM_NOT_404:{r.status}')
        r=await page.goto(BASE+'/glossar/begriff/hufentwurf/',wait_until='domcontentloaded')
        if r.status != 404: failures.append(f'DRAFT_PUBLIC:{r.status}')
        await browser.close()

    print('REAL_DESIGN_BROWSER_MEASUREMENTS='+json.dumps(measurements,separators=(',',':')))
    if failures:
        for f in failures: print(f)
        raise SystemExit(1)
    print('REAL_DESIGN_AJAX_PASS')
    print('REAL_DESIGN_HERO_RESPONSIVE_PASS')
    print('REAL_DESIGN_CATEGORY_DISTINCT_PASS')
    print('REAL_DESIGN_TERM_LINK_PASS')
    print('REAL_DESIGN_NEGATIVE_PASS')
    print('REAL_DESIGN_RUNTIME_BROWSER_PASS')

asyncio.run(main())
