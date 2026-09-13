#!/usr/bin/env python3
import asyncio, json
from playwright.async_api import async_playwright
BASE='http://127.0.0.1:8080'

async def geom(page):
    return await page.evaluate('''() => {
      const b=s=>{const e=document.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height,b:r.bottom}};
      return {primary:b('#primary'),bc:b('.uge-breadcrumbs'),hero:b('.uge-hero')};
    }''')

async def main():
    fail=[]; data={}
    async with async_playwright() as pw:
        browser=await pw.chromium.launch(headless=True,args=['--no-sandbox'])
        page=await browser.new_page(viewport={'width':1200,'height':1400})

        r=await page.goto(BASE+'/glossar/',wait_until='networkidle')
        if r.status!=200: fail.append(f'HOME_HTTP:{r.status}')
        home=await geom(page); data['home']=home
        text=await page.locator('.uge-hero-copy').inner_text()
        if 'Begriffe schnell finden, fachlich einordnen und verständlich nachschlagen.' in text:
            fail.append('REJECTED_FALLBACK_TEXT_ON_HOME')

        r=await page.goto(BASE+'/glossar/gesundheit/',wait_until='networkidle')
        if r.status!=200: fail.append(f'CATEGORY_HTTP:{r.status}')
        cat=await geom(page); data['category']=cat
        if not all(home.values()) or not all(cat.values()):
            fail.append('BREADCRUMB_GEOMETRY_MISSING')
        else:
            # User screenshot: home spacing/breadcrumb is the baseline. Category
            # must sit on exactly the same vertical axis beneath the same header.
            if abs(home['primary']['y']-cat['primary']['y'])>2:
                fail.append(f'CATEGORY_PRIMARY_TOP_DIFF:{home["primary"]["y"]}:{cat["primary"]["y"]}')
            if abs(home['bc']['y']-cat['bc']['y'])>2:
                fail.append(f'CATEGORY_BREADCRUMB_TOP_DIFF:{home["bc"]["y"]}:{cat["bc"]["y"]}')
            home_gap=home['hero']['y']-home['bc']['b']
            cat_gap=cat['hero']['y']-cat['bc']['b']
            if abs(home_gap-cat_gap)>2:
                fail.append(f'CATEGORY_BREADCRUMB_HERO_GAP_DIFF:{home_gap}:{cat_gap}')
        if await page.locator('.uge-breadcrumbs [aria-current="page"]').inner_text()!='Gesundheit':
            fail.append('CATEGORY_BREADCRUMB_CURRENT_WRONG')
        ctext=await page.locator('.uge-hero-copy').inner_text()
        if 'Begriffe schnell finden, fachlich einordnen und verständlich nachschlagen.' in ctext:
            fail.append('REJECTED_FALLBACK_TEXT_ON_CATEGORY')

        # Click an actual rendered card after the main WP loop has deliberately
        # been emptied by the test poison plugin. 0.2.9 produced a blank shell in
        # exactly this failure class; 0.2.10 must render from the requested URL.
        link=page.locator('a[href*="/glossar/begriff/hufbein/"]').first
        if await link.count()!=1:
            fail.append('TERM_LINK_MISSING')
        else:
            await link.click(); await page.wait_for_load_state('networkidle')
            if '/glossar/begriff/hufbein/' not in page.url: fail.append('TERM_CLICK_DESTINATION_WRONG')
            if await page.locator('article.uge-single-wrap').count()!=1: fail.append('TERM_ARTICLE_MISSING_AFTER_LOOP_POISON')
            if await page.locator('.uge-single-header h1').count()!=1: fail.append('TERM_H1_MISSING_AFTER_LOOP_POISON')
            else:
                if await page.locator('.uge-single-header h1').inner_text()!='Hufbein': fail.append('TERM_H1_WRONG')
            if 'FULL-HUFBEIN-SENTINEL' not in await page.content(): fail.append('TERM_CONTENT_MISSING_AFTER_LOOP_POISON')
            term=await geom(page); data['term']=term

        await browser.close()
    print('UGE0210_BROWSER_GEOMETRY='+json.dumps(data,separators=(',',':')))
    if fail:
        for f in fail: print(f)
        raise SystemExit(1)
    print('UGE0210_CATEGORY_BREADCRUMB_SPACING_MATCH_HOME_PASS')
    print('UGE0210_REJECTED_HERO_FALLBACK_ABSENT_PASS')
    print('UGE0210_SINGLE_SURVIVES_EMPTY_MAIN_LOOP_PASS')
    print('UGE0210_BROWSER_PASS')

asyncio.run(main())
