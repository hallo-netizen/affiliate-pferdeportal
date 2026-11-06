#!/usr/bin/env python3
"""HD003 image-only packaging. Only for already verified missing Hobby Depot category slugs."""
import argparse, hashlib, io, json, re, sys, zipfile
from pathlib import Path
from PIL import Image, ImageOps

ROOT='affiliate-portal-template-kit/'
BASEROOT=ROOT+'assets/hobby-depot-v150617/'
CURRENT_SHA256='05ea37f040c1189ea9fda29c2dd795740351d83fe8022f8d966a453679fec7a8'
WORLDS={'gestalten','fertigen','technik','forschen','pflanzen','tiere','bewegen','sammeln'}
def h(data): return hashlib.sha256(data).hexdigest()
def stop(message): raise ValueError('STOP: '+message)

def build(base, source, manifest, output):
    m=json.loads(Path(manifest).read_text(encoding='utf-8'))
    slug=m.get('slug',''); world=m.get('world','')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug): stop('invalid slug')
    if world not in WORLDS: stop('invalid world')
    if m.get('visual_review')!='PASS': stop('visual inspection not approved')
    if m.get('wordpress_slot_verified') is not True: stop('WordPress target/slot not verified')
    src=Path(source).read_bytes()
    if m.get('source_sha256') != h(src): stop('source file mismatch')
    if h(Path(base).read_bytes()) != CURRENT_SHA256: stop('unverified or outdated source plugin')
    with Image.open(io.BytesIO(src)) as image:
        if image.width<900 or image.height<600: stop('source too small')
        if not 1.4<=image.width/image.height<=2.1: stop('wrong source aspect ratio')
        image=ImageOps.fit(image.convert('RGB'),(600,320),Image.Resampling.LANCZOS)
        buf=io.BytesIO();image.save(buf,format='WEBP',quality=82,method=6)
        approved_photo=buf.getvalue()
    hero=BASEROOT+'hero-masters-v150684/'+slug+'.webp'
    tile=BASEROOT+'subcategories/'+world+'/'+slug+'-v150634.webp'
    with zipfile.ZipFile(base) as original:
        if original.testzip(): stop('base ZIP broken')
        names=original.namelist()
        if any(path in names for path in [hero,tile]): stop('image already in plugin; refuse overwrite')
        code=original.read(ROOT+'includes/class-hobby-depot-profile-v150709.php').decode('utf-8','replace')
        if slug not in code: stop('slug missing from real design profile')
        if 'category_image_v150774' not in code: stop('current tile binding incompatible')
        with zipfile.ZipFile(output,'w') as output_zip:
            for obj in original.infolist():
                output_zip.writestr(obj,original.read(obj.filename))
            output_zip.writestr(hero,approved_photo,compress_type=zipfile.ZIP_DEFLATED)
            output_zip.writestr(tile,approved_photo,compress_type=zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile(output) as check,zipfile.ZipFile(base) as original:
        if check.testzip(): stop('output ZIP broken')
        if len(check.namelist())!=len(original.namelist())+2: stop('unexpected ZIP entry count')
        if set(check.namelist())-set(original.namelist())!={hero,tile}:stop('unexpected new files')
        if any(h(check.read(n))!=h(original.read(n)) for n in original.namelist()):stop('existing files changed')
        if check.read(hero)!=check.read(tile):stop('different photos assigned')
    print(json.dumps({'status':'PACKAGED_LOCAL_PASS','slug':slug,'world':world,
        'original_entries':len(names),'new_entries':2,'unchanged_originals':len(names),
        'output_sha256':h(Path(output).read_bytes()),'live_installed':False},ensure_ascii=False))
    return 0

def main():
    p=argparse.ArgumentParser()
    for name in ('base','source','manifest','output'):p.add_argument('--'+name,required=True)
    a=p.parse_args()
    try:return build(a.base,a.source,a.manifest,a.output)
    except Exception as e: print(str(e),file=sys.stderr); return 2
if __name__=='__main__': sys.exit(main())
