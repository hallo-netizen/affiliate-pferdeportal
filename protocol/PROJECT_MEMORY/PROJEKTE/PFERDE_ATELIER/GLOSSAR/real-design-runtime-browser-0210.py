#!/usr/bin/env python3
import asyncio, json
from playwright.async_api import async_playwright
BASE='http://127.0.0.1:8080'

async def geom(page):
    return await page.evaluate('''() => {
      const b=s=>{const e=document.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height,b:r.bottom}};
      return {primary:b('#primary'),bc:b('.uge-breadcrumbs'),hero:b('.uge-hero')};
    }''')

async def assert_term(page, slug, title, fail, marker=None):
    if f'/glossar/begriff/{slug}/' not in page.url:
        fail.append(f'{slug}:WRONG_URL:{page.url}')
    if await page.locator('article.uge-single-wrap').count()!=1:
        fail.append(f'{slug}:ARTICLE_MISSING')
    h=page.locator('.uge-single-header h1')
    if await h.count()!=1:
        fail.append(f'{slug}:H1_MISSING')
    elif await h.inner_text()!=title:
        fail.append(f'{slug}:H1_WRONG:{await h.inner_text()}')
    if marker and marker not in await page.content():
        fail.append(f'{slug}:CONTENT_MARKER_MISSING')

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
            if abs(home['primary']['y']-cat['primary']['y'])>2:
                fail.append(f'CATEGORY_PRIMARY_TOP_DIFF:{home["primary"]["y"]}:{cat["primary"]["y"]}')
            if abs(home['bc']['y']-cat['bc']['y'])>2:
                fail.append(f'CATEGORY_BREADCRUMB_TOP_DIFF:{home["bc"]["y"]}:{cat["bc"]["y"]}')
            home_gap=home['hero']['y']-home['bc']['b']; cat_gap=cat['hero']['y']-cat['bc']['b']
            if abs(home_gap-cat_gap)>2:
                fail.append(f'CATEGORY_BREADCRUMB_HERO_GAP_DIFF:{home_gap}:{cat_gap}')
        if await page.locator('.uge-breadcrumbs [aria-current="page"]').inner_text()!='Gesundheit':
            fail.append('CATEGORY_BREADCRUMB_CURRENT_WRONG')
        ctext=await page.locator('.uge-hero-copy').inner_text()
        if 'Begriffe schnell finden, fachlich einordnen und verständlich nachschlagen.' in ctext:
            fail.append('REJECTED_FALLBACK_TEXT_ON_CATEGORY')

        # Existing test term: real rendered category link must be clickable and must
        # survive the deliberately emptied WordPress main loop.
        hufbein=page.locator('a[href*="/glossar/begriff/hufbein/"]').first
        if await hufbein.count()!=1:
            fail.append('HUFBEIN_LINK_MISSING')
        else:
            await hufbein.click(); await page.wait_for_load_state('networkidle')
            await assert_term(page,'hufbein','Hufbein',fail,'FULL-HUFBEIN-SENTINEL')
            term=await geom(page); data['term']=term

        # New cluster: click from category into Hufrehe, then only through visible
        # "Verwandte Begriffe" links to Strahlfäule and Hufabszess, then back to
        # the visible category link. This is the user-facing proof that the new
        # articles are actually inspectable by clicking, not merely HTTP 200.
        await page.goto(BASE+'/glossar/gesundheit/',wait_until='networkidle')
        hufrehe=page.locator('a[href*="/glossar/begriff/hufrehe/"]').first
        if await hufrehe.count()!=1:
            fail.append('HUFREHE_CATEGORY_LINK_MISSING')
        else:
            await hufrehe.click(); await page.wait_for_load_state('networkidle')
            await assert_term(page,'hufrehe','Hufrehe',fail)
            rel=page.locator('p:has(strong:text("Verwandte Begriffe")) a[href*="/glossar/begriff/strahlfaeule/"]').first
            if await rel.count()!=1:
                fail.append('HUFREHE_TO_STRAHLFAEULE_RELATED_LINK_MISSING')
            else:
                await rel.click(); await page.wait_for_load_state('networkidle')
                await assert_term(page,'strahlfaeule','Strahlfäule',fail)
                rel2=page.locator('p:has(strong:text("Verwandte Begriffe")) a[href*="/glossar/begriff/hufabszess/"]').first
                if await rel2.count()!=1:
                    fail.append('STRAHLFAEULE_TO_HUFABSZESS_RELATED_LINK_MISSING')
                else:
                    await rel2.click(); await page.wait_for_load_state('networkidle')
                    await assert_term(page,'hufabszess','Hufabszess',fail)
                    catlink=page.locator('a[href*="/glossar/gesundheit/"]').first
                    if await catlink.count()!=1:
                        fail.append('HUFABSZESS_CATEGORY_LINK_MISSING')
                    else:
                        await catlink.click(); await page.wait_for_load_state('networkidle')
                        if '/glossar/gesundheit/' not in page.url or await page.locator('.uge-category-head').count()!=1:
                            fail.append('CATEGORY_RETURN_LINK_FAIL:'+page.url)

        await browser.close()
    print('UGE0210_BROWSER_GEOMETRY='+json.dumps(data,separators=(',',':')))
    if fail:
        for f in fail: print(f)
        raise SystemExit(1)
    print('UGE0210_CATEGORY_BREADCRUMB_SPACING_MATCH_HOME_PASS')
    print('UGE0210_REJECTED_HERO_FALLBACK_ABSENT_PASS')
    print('UGE0210_EXISTING_SINGLE_CLICK_PASS')
    print('UGE0210_NEW_CLUSTER_CLICK_CHAIN_PASS')
    print('UGE0210_SINGLE_SURVIVES_EMPTY_MAIN_LOOP_PASS')
    print('UGE0210_BROWSER_PASS')

asyncio.run(main())
